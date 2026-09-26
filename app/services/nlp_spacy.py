"""
spaCy second pass (EC2 pilot tier, LOCAL branch only - never GitHub).

  regex (primary) -> Groq (optional) -> spaCy (optional) -> HF (optional)

Same contract as llm_groq: fills empty/low-confidence fields only, never
overwrites a trusted regex value, never fills profile-prohibited fields,
every candidate passes PATTERNS / _looks_like_name. Lazy `import spacy`
so the module imports fine without requirements-ec2.txt installed.
"""
from __future__ import annotations

from app.config import settings

SPACY_CONFIDENCE_CAP = 78.0
SPACY_FILLABLE = {
    "owner_name", "guardian_name", "previous_owner", "new_owner",
    "village", "tehsil", "district", "address",
}

_NLP = None
_RULER_READY_FOR = None


def is_enabled() -> bool:
    return bool(settings.spacy_enabled)


def status() -> dict:
    return {
        "enabled": is_enabled(),
        "model": settings.spacy_model if is_enabled() else "",
        "mode": "verifier-only (regex primary)",
        "loaded": _NLP is not None,
    }


def _load():
    global _NLP, _RULER_READY_FOR
    if _NLP is not None:
        return _NLP
    import spacy  # lazy: requirements-ec2.txt only

    _NLP = spacy.load(settings.spacy_model)
    return _NLP


def _ensure_ruler(nlp) -> None:
    """Seed an EntityRuler with land-record label aliases (idempotent)."""
    global _RULER_READY_FOR
    if _RULER_READY_FOR == settings.spacy_model:
        return
    try:
        from app.services.extraction import LABEL_ALIASES
    except Exception:
        return
    if "entity_ruler" not in nlp.pipe_names:
        try:
            ruler = nlp.add_pipe("entity_ruler", before="ner")
        except Exception:
            return
    else:
        ruler = nlp.get_pipe("entity_ruler")
    patterns = []
    for field_name, aliases in LABEL_ALIASES.items():
        for alias in aliases:
            if len(alias) < 3:
                continue
            patterns.append({"label": "LAND_FIELD", "pattern": alias})
    try:
        ruler.add_patterns(patterns)
    except Exception:
        pass
    _RULER_READY_FOR = settings.spacy_model


def extract_candidates(text: str) -> dict[str, list[str]]:
    """PERSON/GPE/ORG spans grouped for field filling. Empty when disabled."""
    if not is_enabled():
        return {}
    try:
        nlp = _load()
        _ensure_ruler(nlp)
        doc = nlp((text or "")[:6000])
    except Exception:
        return {}
    out: dict[str, list[str]] = {"PERSON": [], "GPE": [], "ORG": []}
    for ent in doc.ents:
        label = (ent.label_ or "").upper()
        val = (ent.text or "").strip(" ,.:;-\t")
        if len(val) < 3 or "|" in val or "`" in val:
            continue
        if label in ("PERSON", "PER"):
            out["PERSON"].append(val[:200])
        elif label in ("GPE", "LOC", "FAC"):
            out["GPE"].append(val[:200])
        elif label == "ORG":
            out["ORG"].append(val[:200])
    return out


def _valid(field_name: str, value: str, profile: str) -> str:
    import re

    from app.services.extraction import (
        PROHIBITED_BY_PROFILE,
        _is_header_leak,
        _looks_like_name,
    )

    if field_name not in SPACY_FILLABLE:
        return ""
    if field_name in PROHIBITED_BY_PROFILE.get(profile, set()):
        return ""
    cleaned = re.sub(r"\s+", " ", (value or "")).strip(" ,.:;-\t")[:200]
    if len(cleaned) < 3:
        return ""
    if _is_header_leak(cleaned):
        return ""
    if field_name in {"owner_name", "guardian_name", "previous_owner", "new_owner"}:
        if len(cleaned.split()) < 2 and len(cleaned) < 4:
            return ""
    if field_name in {"owner_name", "guardian_name", "previous_owner", "new_owner"}:
        ok, _s = _looks_like_name(cleaned)
        return cleaned if ok else ""
    if re.fullmatch(r"[\d\s/\-.,]+", cleaned):
        return ""  # a place is never a bare number
    return cleaned


def apply_candidates(outcome, candidates: dict[str, list[str]]) -> list[str]:
    from app.services.extraction import FieldExtraction, _fuse

    applied: list[str] = []
    persons = list((candidates or {}).get("PERSON", []))
    places = list((candidates or {}).get("GPE", [])) + list((candidates or {}).get("ORG", []))

    def _fill(field_name: str, pool: list[str]) -> None:
        current = outcome.fields.get(field_name)
        if current is None or not isinstance(current, FieldExtraction):
            return
        if current.normalized_value and current.confidence >= settings.CONFIDENCE_MEDIUM:
            return
        while pool:
            cand = pool.pop(0)
            valid = _valid(field_name, cand, outcome.profile)
            if not valid:
                continue
            current.value = valid[:200]
            current.normalized_value = valid[:200]
            current.confidence = min(SPACY_CONFIDENCE_CAP, max(current.confidence, 55.0))
            current.source = "spacy-ner"
            current.method = "spacy-ner-verifier"
            current.status = "extracted"
            current.reason = ""
            current.signals = {
                **(current.signals or {}),
                "spacy_model": settings.spacy_model,
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
    if not is_enabled():
        return outcome, []
    if not (outcome.low_confidence_fields or outcome.missing_required):
        return outcome, []
    try:
        applied = apply_candidates(outcome, extract_candidates(ocr_text))
    except Exception:
        return outcome, []
    return outcome, applied
