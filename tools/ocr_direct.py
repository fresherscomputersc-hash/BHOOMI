import sqlite3, json, traceback
c = sqlite3.connect("data/bhuverify.db")
row = c.execute("select enhanced_path, layout_json from source_documents where doc_id='DOC-17A725D645'").fetchone()
lay = json.loads(row[1]) if isinstance(row[1], str) else row[1]
from app.services.worker import _ocr_document
try:
    out = _ocr_document(row[0], lay, "eng+hin+ori", page=1)
    print("mode:", out["mode"], "words:", out["word_count"])
    for h in out["handwritten_regions"]:
        print("part engine:", h.get("engine"), "words:", h.get("word_count"),
              "text:", str(h.get("text"))[:120])
except Exception:
    traceback.print_exc()
