import sqlite3
c = sqlite3.connect("data/bhusure.db")
from app.master_data import CLASSIFICATION_ALIASES
for fn in ("4558.pdf", "313.pdf", "488.pdf"):
    doc = c.execute("select id from source_documents where original_filename=?",
                    (fn,)).fetchone()
    rec = c.execute("select id from land_records where document_id=?",
                    (doc[0],)).fetchone()
    ext = {r[0]: (r[1], r[2], r[3]) for r in c.execute(
        "select field_name, normalized_value, confidence, source from extraction_results where record_id=?",
        (rec[0],))}
    print("=" * 20, fn)
    print("class:", ext.get("land_classification"))
    print("area:", ext.get("area"))
    ocr = c.execute("select ocr_text from source_documents where id=?",
                    (doc[0],)).fetchone()[0]
    hits = {}
    for line in ocr.splitlines():
        low = line.lower()
        for k in CLASSIFICATION_ALIASES:
            if len(k) >= 3 and k in low:
                hits[k] = hits.get(k, 0) + 1
    print("kisam-alias hits:", hits)
    print("subplots:", c.execute(
        "select count(*) from extraction_results where record_id=? and field_name='area'",
        (rec[0],)).fetchone())
