import sqlite3, json
c = sqlite3.connect("data/bhusure.db")
row = c.execute("select original_filename, status, ocr_word_count, ocr_mean_confidence, preprocessing_stats from source_documents where doc_id='DOC-40792819A6'").fetchone()
print(row[0], row[1], row[2], round(row[3], 1))
stats = json.loads(row[4]) if isinstance(row[4], str) else row[4]
print("regions:", [(h.get("engine"), h.get("word_count")) for h in stats.get("handwritten_regions", [])])
rec = c.execute("select record_confidence, owner_name, village from land_records where document_id=(select id from source_documents where doc_id='DOC-40792819A6')").fetchone()
print("record:", rec)
