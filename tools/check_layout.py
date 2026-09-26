import sqlite3, json
c = sqlite3.connect("data/bhuverify.db")
doc = c.execute("select layout_json from source_documents where doc_id='DOC-17A725D645'").fetchone()[0]
lay = json.loads(doc) if isinstance(doc, str) else doc
regs = lay.get("regions", lay if isinstance(lay, list) else [])
from collections import Counter
print("labels:", Counter(r.get("label") for r in regs))
for r in regs[:14]:
    print({k: r.get(k) for k in ("label", "x", "y", "w", "h")})
