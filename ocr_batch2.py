"""
Create 5 NEW sample documents (mix English + Hindi) that expose the
OCR/label-bleed problems found in batch 1, then OCR every one and
dump a per-field report.
"""
import sys, json, time, random
sys.path.insert(0, r"E:\bhusure-deploy-fixed")
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from app.services.ocr_service import run_ocr
from app.services.extraction import extract_fields, detect_profile
from app.sample_documents import render_document, font, Line, SAMPLE_DIR

OUT = Path(r"E:\bhusure-deploy-fixed\data\samples")
json.dump([], open(r"E:\bhusure-deploy-fixed\ocr_batch2_specs.json","w"))

# ---------------------------------------------------------------- spec builder
def spec(key, filename, language, header, lines, notes="", stamp=None, seed=20, skew_degrees=0.0, noise=0, jpeg_quality=None):
    return {
        "key": key,
        "filename": filename,
        "language": language,
        "doc_type": "ror",
        "notes": notes,
        "header": header,
        "lines": [Line(*l) if isinstance(l, tuple) else l for l in lines],
        "footer": ["Sample generated for OCR regression analysis."],
        "stamp_text": stamp,
        "seed": seed,
        "skew_degrees": skew_degrees,
        "noise": noise,
        "jpeg_quality": jpeg_quality,
    }

NEW_SPECS = [
    # EN 1  -- clean but deliberately mixes label/value spacing
    spec("new_01_clean_eng", "sample_07_clean_eng.png", "eng",
         ["GOVERNMENT OF ODISHA", "RECORD OF RIGHTS (RoR)", "Revenue Department - Khordha District"],
         [("District", "Khordha"),
          ("Tehsil / Block", "Khordha Sadar"),
          ("Village / Mouza", "Golabai"),
          ("Khata Number", "118"),
          ("Khasra Number", "227/1"),
          ("Survey Number", "227"),
          ("Plot Number", "1"),
          ("Owner Name", "Gopinath Pradhan"),
          ("Father Name", "Bhagirathi Pradhan"),
          ("Total Area", "1.50 acre"),
          ("Land Classification", "Unirrigated land"),
          ("Mutation Number", "MUT/227/2023"),
          ("Mutation Date", "15/03/2023"),
          ("Registration Number", "945 of 2023")],
         notes="Clean English RoR - correct label spacing. Tests baseline accuracy.",
         stamp="REVENUE\nDEPT\nODISHA", seed=20),

    # HIN 1  -- Hindi printed register (Devanagari labels + Devanagari values)
    spec("new_02_hindi_print", "sample_08_hindi_print.png", "hin",
         ["ओडिशा सरकार", "रजिस्टर ऑफ राइट्स", "राजस्व विभाग - खुर्दा जिला"],
         [("जिला", "खुर्दा"),
          ("तहसील", "खुर्दा सदर"),
          ("गाँव", "बेगुनिया"),
          ("खाता संख्या", "331"),
          ("खसरा संख्या", "19/2"),
          ("दाग", "2"),
          ("खातेदार का नाम", "देवदास प्रधान"),
          ("पिता का नाम", "हरिदास प्रधान"),
          ("क्षेत्रफल", "0.85 acre"),
          ("जमीन का प्रकार", "Cultivable land"),
          ("नामांतरण संख्या", "MUT/19/2022"),
          ("नामांतरण दिनांक", "20/06/2022")],
         notes="Hindi printed register - tests Devanagari OCR and Indic label matching.",
         stamp="तहसीलदार\nखुर्दा", seed=21),

    # EN 2  -- degraded (skew + noise + JPEG) English with wrong registration format
    spec("new_03_degraded_eng", "sample_09_degraded_eng.jpg", "eng",
         ["GOVERNMENT OF ODISHA", "RECORD OF RIGHTS (RoR)", "Revenue Department - Khordha District"],
         [("District", "Nayagarh"),
          ("Tehsil / Block", "Nayagarh"),
          ("Village / Mouza", "Saranakul"),
          ("Khata Number", "445"),
          ("Khasra Number", "77/3"),
          ("Survey Number", "77"),
          ("Plot Number", "3"),
          ("Owner Name", "Sarat Kumar Behera"),
          ("Father Name", "Banamali Behera"),
          ("Total Area", "2.25 acre"),
          ("Land Classification", "Garden land"),
          ("Mutation Number", "REG-NAY-88-44"),
          ("Mutation Date", "09/11/2024"),
          ("Registration Number", "REG-BHY-2024-77")],
         notes="Degraded English RoR - invalid registration ref (BR-10) + skew/noise.",
         skew_degrees=3.1, noise=60, jpeg_quality=38,
         stamp="MUTATION\nTAHSILDAR", seed=22),

    # HIN 2  -- handwritten Hindi register (HTR path)
    spec("new_04_hindi_handwritten", "sample_10_hindi_handwritten.png", "hin",
         ["ओडिशा सरकार", "जमाबंदी (हस्तलिखित)", "राजस्व विभाग - पुरी जिला"],
         [("जिला", "पुरी"),
          ("तहसील", "ବଲુତୋଟ଼"),
          ("ग्राम", "ଚନ୍ଦବାଲୁ"),
          ("ଖାତା ସଂଖ୍ୟା", "512"),
          ("ଖସରା ସଂଖ୍ୟା", "45/1"),
          ("ଦାଗ", "5"),
          ("ଖାତେଦାର କାର୍ନାମ", "ଜଗନ୍ନାଥ ମହାନ୍ତି"),
          ("ପିତା କାର୍ନାମ", "ବଲୁରେଶ୍ ମହାନ୍ତି"),
          ("କ୍ଷେତ୍ରଫଳ", "1.05 acre"),
          ("ଜମୀର ପ୍ରକାର", "Fallow land"),
          ("ନାମାନ୍ତରଣ ସଂଖ୍ୟା", "MUT/45/2021"),
          ("ନାମାନ୍ତରଣ ତାରିଖ", "10/08/2021")],
         notes="Handwritten Odia/Hindi register - exercises HTR path + Odia script.",
         stamp="ତହ୍ସିଲଦାର\nପୁରୀ", seed=23),

    # EN 3  -- multi-plot page with sub-plot area mismatch (BR-2) and village typo
    spec("new_05_multi_plot", "sample_11_multi_plot.png", "eng",
         ["GOVERNMENT OF ODISHA", "PLOT-WISE REGISTER EXTRACT", "Revenue Department - Khordha District"],
         [("District", "Bhubaneswar"),
          ("Tehsil / Block", "Bhubaneswar"),
          ("Village / Mouza", "Bhubaneshwarnagar"),
          ("Khata Number", "12"),
          ("Khasra Number", "50"),
          ("Survey Number", "50"),
          ("Owner Name", "Lipika Mohanty"),
          ("Father Name", "Chiranjib Mohanty"),
          ("Total Area", "4.00 acre"),
          ("Sub Plot Khasra", "50/1  Area 2.10 acre"),
          ("Sub Plot Khasra", "50/2  Area 2.10 acre"),
          ("Mutation Number", "MUT/12/2025"),
          ("Mutation Date", "01/01/2025"),
          ("Registration Number", "5500 of 2025")],
         notes="Multi-plot page: sub-plots sum to 4.20 not 4.00 (BR-2), village typo (BR-7).",
         stamp="CERTIFIED\nREVENUE INSPECTOR", seed=24),
]

# ---------------------------------------------------------------- generate images
written = []
for s in NEW_SPECS:
    path = OUT / s["filename"]
    render_document(
        path=path,
        header=s["header"],
        lines=s["lines"],
        script="devanagari" if s["language"] == "hin" else "latin",
        stamp_text=s.get("stamp_text"),
        footer=s.get("footer"),
        skew_degrees=s.get("skew_degrees", 0.0),
        noise=s.get("noise", 0),
        jpeg_quality=s.get("jpeg_quality"),
        seed=s.get("seed", 20),
    )
    written.append({"key": s["key"], "file": s["filename"], "lang": s["language"], "size": path.stat().st_size})
    print(f"WRITTEN {s['filename']} ({path.stat().st_size:,} bytes)")

# ---------------------------------------------------------------- OCR every new sample
batch2 = []
for w in written:
    f = w["file"]
    p = OUT / f
    lang = w["lang"]
    t0 = time.perf_counter()
    ocr = run_ocr(p, language=None, psm=4)
    elapsed = (time.perf_counter()-t0)*1000
    profile = detect_profile(ocr.text)
    outcome = extract_fields(ocr.text, ocr.words, language=lang, doc_type="ror", page=1)
    rec = {
        "file": f,
        "lang": lang,
        "ocr_ms": round(elapsed, 1),
        "words": ocr.word_count,
        "mean_conf": round(ocr.mean_confidence, 2),
        "min_conf": round(ocr.min_confidence, 2),
        "low_conf_words": ocr.low_confidence_word_count,
        "profile": profile,
        "text_preview": ocr.text[:250].replace("\n", " | "),
        "fields": {k: {"v": v.value, "conf": v.confidence, "status": v.status, "src": v.source, "ev": (v.evidence_text or "")[:60]} for k, v in outcome.fields.items()},
        "record_conf": outcome.record_confidence,
        "missing_required": outcome.missing_required,
        "area_ha": outcome.area_hectare,
        "unit_ok": outcome.area_unit_recognised,
    }
    batch2.append(rec)
    print(f"OCR   {f} -> {ocr.word_count}w conf {ocr.mean_confidence:.1f}% ms={elapsed:.0f} prof={profile}")

json.dump({"written": written, "ocr_results": batch2}, open(r"E:\bhusure-deploy-fixed\ocr_batch2.json","w"), indent=1, default=str)
print("\nNEW SAMPLES:", len(written), " OCR RESULTS:", len(batch2))
