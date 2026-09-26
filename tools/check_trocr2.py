import sqlite3, json
c = sqlite3.connect("data/bhuverify.db")
for doc_id in ("DOC-17A725D645", "DOC-77EADAF0A1"):
    row = c.execute("select original_filename, preprocessing_stats from source_documents where doc_id=?",
                    (doc_id,)).fetchone()
    stats = json.loads(row[1]) if isinstance(row[1], str) else row[1]
    print("=" * 20, row[0])
    for h in stats.get("handwritten_regions", []):
        print("engine:", h.get("engine"), "| words:", h.get("word_count"),
              "| conf:", h.get("confidence"), "| text:", str(h.get("text"))[:150])
    if not stats.get("handwritten_regions"):
        print("no handwritten regions")
