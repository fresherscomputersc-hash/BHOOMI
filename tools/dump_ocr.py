import sqlite3
c = sqlite3.connect("data/bhusure.db")
for fn in ("488.pdf", "72.pdf"):
    row = c.execute(
        "select ocr_text from source_documents where original_filename=?", (fn,)).fetchone()
    print("=" * 30, fn, len(row[0]), "chars")
    print(row[0][:3500])
