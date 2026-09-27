import sqlite3
c = sqlite3.connect("data/bhusure.db")
for doc_id in ("DOC-17A725D645", "DOC-77EADAF0A1"):
    r = c.execute("select original_filename, ocr_latency_ms, total_latency_ms, ocr_engine, ocr_word_count, processed_at from source_documents where doc_id=?", (doc_id,)).fetchone()
    print(r)
