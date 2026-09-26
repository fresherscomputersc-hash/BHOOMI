import sqlite3, json
c = sqlite3.connect("data/bhuverify.db")
for doc_id in ("DOC-17A725D645", "DOC-77EADAF0A1"):
    row = c.execute("select original_filename, layout_json, enhanced_path from source_documents where doc_id=?",
                    (doc_id,)).fetchone()
    lay = json.loads(row[1]) if isinstance(row[1], str) else row[1]
    print("=" * 20, row[0], "enhanced:", row[2])
    print("image_size:", lay.get("image_size"))
    for r in lay.get("regions", []):
        if r.get("label") == "handwritten_text":
            print("hand box:", {k: r.get(k) for k in ("x", "y", "w", "h")})
