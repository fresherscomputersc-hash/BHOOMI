import sqlite3, json
from collections import Counter
c = sqlite3.connect("data/bhusure.db")
for doc_id in ("DOC-17A725D645", "DOC-77EADAF0A1"):
    row = c.execute("select original_filename, layout_json from source_documents where doc_id=?",
                    (doc_id,)).fetchone()
    lay = json.loads(row[1]) if isinstance(row[1], str) else row[1]
    regs = lay.get("regions", [])
    print(row[0], Counter(r.get("label") for r in regs))
