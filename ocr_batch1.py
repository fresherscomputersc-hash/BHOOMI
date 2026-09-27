import sys, json, time
sys.path.insert(0, r"E:\bhusure-deploy-fixed")
from pathlib import Path
from app.services.ocr_service import run_ocr, run_htr
from app.services.extraction import extract_fields, detect_profile

SAMPLES = Path(r"E:\bhusure-deploy-fixed\data\samples")
results = []

for f in sorted(SAMPLES.glob("*")):
    lang = "hin" if "hindi" in f.name.lower() else "eng"
    t0 = time.perf_counter()
    ocr = run_ocr(f, language=None, psm=4)
    elapsed = (time.perf_counter()-t0)*1000
    profile = detect_profile(ocr.text)
    outcome = extract_fields(ocr.text, ocr.words, language=lang, doc_type="ror", page=1)
    results.append({
        "file": f.name,
        "lang": lang,
        "ocr_ms": round(elapsed, 1),
        "words": ocr.word_count,
        "mean_conf": round(ocr.mean_confidence, 2),
        "min_conf": round(ocr.min_confidence, 2),
        "low_conf_words": ocr.low_confidence_word_count,
        "profile": profile,
        "text_preview": ocr.text[:300].replace("\n", " | "),
        "fields": {k: {"v": v.value, "conf": v.confidence, "status": v.status, "src": v.source, "ev": (v.evidence_text or "")[:70]} for k, v in outcome.fields.items()},
        "record_conf": outcome.record_confidence,
        "missing_required": outcome.missing_required,
        "area_ha": outcome.area_hectare,
        "unit_ok": outcome.area_unit_recognised,
    })
    print(f"OK {f.name} -> {ocr.word_count} w, conf {ocr.mean_confidence:.1f}%, prof={profile}, {elapsed:.0f}ms")

json.dump(results, open(r"E:\bhusure-deploy-fixed\ocr_batch1.json", "w"), indent=1, default=str)
print("\nTOTAL:", len(results))
