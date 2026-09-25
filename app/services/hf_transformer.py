"""
HF transformer passes (EC2 pilot tier, LOCAL branch only - never GitHub).

Two optional tasks, both lazy (no torch/transformers import at module load):

  1. NER refill  - token-classification pipeline (default XLM-R NER) fills
     empty/low-confidence name + place fields, same validation gates as
     llm_groq / nlp_spacy. Controlled by HF_ENABLED=1.
  2. HTR rescan  - TrOCR image-to-text on handwritten region crops only,
     controlled by HF_HTR_ENABLED=1. Returns text; the caller merges it
     the same way worker.py merges the Tesseract HTR pass today.

Defaults are small CPU-runnable models; override with HF_NER_MODEL /
HF_HTR_MODEL env vars. First run downloads to the HF cache (see
Dockerfile.ec2 for pre-warming).
"""
from __future__ import annotations

from pathlib import Path

from app.config import settings

HF_CONFIDENCE_CAP = 78.0
HF_FILLABLE = {
    "owner_name", "guardian_name", "previous_owner", "new_owner",
    "village", "tehsil", "district", "address",
    "khasra_no", "khata_no", "plot_no",
}

_NER_PIPE = None
_HTR_PROC = None
_HTR_MODEL = None


def is_ner_enabled() -> bool:
    return bool(settings.hf_enabled)


def is_htr_enabled() -> bool:
    return bool(settings.hf_enabled and settings.hf_htr_enabled)


def status() -> dict:
    return {
        "ner_enabled": is_ner_enabled(),
        "ner_model": settings.hf_ner_model if is_ner_enabled() else "",
        "htr_enabled": is_htr_enabled(),
        "htr_model": settings.hf_htr_model if is_htr_enabled() else "",
        "mode": "verifier-only (regex primary)",
        "ner_loaded": _NER_PIPE is not None,
        "htr_loaded": _HTR_MODEL is not None,
    }


def _ner_pipe():
    global _NER_PIPE
    if _NER_PIPE is not None:
        return _NER_PIPE
    from transformers import pipeline  # lazy: requirements-ec2.txt only

    _NER_PIPE = pipeline(
        "token-classification",
        model=settings.hf_ner_model,
        aggregation_strategy="simple",
    )
    return _NER_PIPE


def ner_candidates(text: str) -> dict[str, list[str]]:
    if not is_ner_enabled():
        return {}
    try:
        pipe = _ner_pipe()
        entities = pipe((text or "")[:2000])
    except Exception:
        return {}
    out = {"PERSON": [], "GPE": []}
    for ent in entities or []:
        group = str(ent.get("entity_group", ent.get("entity", ""))).upper()
        val = str(ent.get("word", "")).strip(" ,.:;-\t")[:200]
        score = float(ent.get("score", 0.0) or 0.0)
        if len(val) < 3 or score < 0.5 or "|" in val or "`" in val:
            continue
        if "PER" in group:
            out["PERSON"].append(val)
        elif any(k in group for k in ("LOC", "GPE", "GEO", "FAC", "ORG")):
            out["GPE"].append(val)
    return out


def _valid(field_name: str, value: str, profile: str) -> str:
    import re

    from app.services.extraction import (
        PATTERNS,
        PROHIBITED_BY_PROFILE,
        _inside_date,
        _is_header_leak,
        _looks_like_name,
    )

    if field_name not in HF_FILLABLE:
        return ""
    if field_name in PROHIBITED_BY_PROFILE.get(profile, set()):
        return ""
    cleaned = re.sub(r"\s+", " ", (value or "")).strip(" ,.:;-\t")[:200]
    if len(cleaned) < 2:
        return ""
    if _is_header_leak(cleaned):
        return ""
    pattern = PATTERNS.get(field_name)
    if pattern:
        matches = [m for m in pattern.finditer(cleaned)
                   if not _inside_date(cleaned, m)]
        if not matches:
            return ""
        return max((m.group(0).strip() for m in matches), key=len)
    if field_name in {"owner_name", "guardian_name", "previous_owner", "new_owner"}:
        ok, _s = _looks_like_name(cleaned)
        return cleaned if ok else ""
    if re.fullmatch(r"[\d\s/\-.,]+", cleaned):
        return ""
    return cleaned


def apply_candidates(outcome, candidates: dict[str, list[str]]) -> list[str]:
    from app.services.extraction import FieldExtraction, _fuse

    applied: list[str] = []
    persons = list((candidates or {}).get("PERSON", []))
    places = list((candidates or {}).get("GPE", []))

    def _fill(field_name: str, pool: list[str]) -> None:
        current = outcome.fields.get(field_name)
        if current is None or not isinstance(current, FieldExtraction):
            return
        if current.normalized_value and current.confidence >= settings.CONFIDENCE_MEDIUM:
            return
        while pool:
            valid = _valid(field_name, pool.pop(0), outcome.profile)
            if not valid:
                continue
            current.value = valid[:200]
            current.normalized_value = valid[:200]
            current.confidence = min(HF_CONFIDENCE_CAP, max(current.confidence, 55.0))
            current.source = "hf-transformer"
            current.method = "hf-transformer-verifier"
            current.status = "extracted"
            current.reason = ""
            current.signals = {
                **(current.signals or {}),
                "hf_ner_model": settings.hf_ner_model,
            }
            try:
                current.confidence = _fuse(current.confidence, 75.0, 30.0, 70.0)
            except Exception:
                pass
            applied.append(field_name)
            return

    for name_field in ("owner_name", "guardian_name", "previous_owner", "new_owner"):
        _fill(name_field, persons)
    for geo_field in ("village", "tehsil", "district", "address"):
        _fill(geo_field, places)
    for id_field in ("khasra_no", "khata_no", "plot_no"):
        _fill(id_field, places + persons)

    if applied:
        outcome.low_confidence_fields = [
            name for name, f in outcome.fields.items()
            if f.value and f.confidence < settings.CONFIDENCE_MEDIUM
        ]
        for name in applied:
            if name in outcome.missing_required and outcome.fields[name].normalized_value:
                outcome.missing_required = [
                    m for m in outcome.missing_required if m != name
                ]
        scored = [f.confidence for f in outcome.fields.values() if f.value]
        if scored:
            outcome.record_confidence = round(sum(scored) / len(scored), 2)
    return applied


def enhance_outcome(ocr_text: str, outcome):
    if not is_ner_enabled():
        return outcome, []
    if not (outcome.low_confidence_fields or outcome.missing_required):
        return outcome, []
    try:
        applied = apply_candidates(outcome, ner_candidates(ocr_text))
    except Exception:
        return outcome, []
    return outcome, applied


def htr_rescan(crop_path: str | Path) -> dict:
    """TrOCR on one handwritten crop. Empty dict when disabled/unavailable."""
    if not is_htr_enabled():
        return {}
    try:
        from PIL import Image
        from transformers import TrOCRProcessor, VisionEncoderDecoderModel
    except Exception:
        return {}
    global _HTR_PROC, _HTR_MODEL
    try:
        if _HTR_MODEL is None:
            _HTR_PROC = TrOCRProcessor.from_pretrained(settings.hf_htr_model)
            _HTR_MODEL = VisionEncoderDecoderModel.from_pretrained(settings.hf_htr_model)
            _HTR_MODEL.eval()
        import torch

        image = Image.open(str(crop_path)).convert("RGB")
        pixel_values = _HTR_PROC(image, return_tensors="pt").pixel_values
        with torch.no_grad():
            generated = _HTR_MODEL.generate(pixel_values, max_length=128)
        text = _HTR_PROC.batch_decode(generated, skip_special_tokens=True)[0].strip()
        if not text:
            return {}
        return {"text": text[:2000], "engine": f"trocr:{settings.hf_htr_model}",
                "confidence": 65.0}
    except Exception:
        return {}
