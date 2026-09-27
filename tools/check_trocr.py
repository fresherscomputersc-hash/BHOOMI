import sqlite3
c = sqlite3.connect("data/bhusure.db")
doc = c.execute("select preprocessing_stats from source_documents where doc_id='DOC-17A725D645'").fetchone()[0]
import json
stats = json.loads(doc) if isinstance(doc, str) else doc
for h in stats.get("handwritten_regions", []):
    print({k: (str(v)[:120]) for k, v in h.items()})
