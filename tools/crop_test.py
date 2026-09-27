import sqlite3, json, traceback
c = sqlite3.connect("data/bhusure.db")
row = c.execute("select enhanced_path, layout_json from source_documents where doc_id='DOC-17A725D645'").fetchone()
lay = json.loads(row[1]) if isinstance(row[1], str) else row[1]
from app.services.ocr_service import crop_region
for r in lay.get("regions", []):
    if r.get("label") != "handwritten_text":
        continue
    print("box:", r["x"], r["y"], r["w"], r["h"])
    try:
        crop = crop_region(row[0], r)
        print("crop shape:", None if crop is None else crop.shape)
    except Exception:
        traceback.print_exc()
