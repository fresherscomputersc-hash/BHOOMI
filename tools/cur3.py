import sqlite3
c = sqlite3.connect("data/bhuverify.db")
for doc_id in ("DOC-5F11B732FA", "DOC-7E22D7E8FE", "DOC-D31D0C5D90"):
    d = c.execute("select original_filename, ocr_word_count from source_documents where doc_id=?", (doc_id,)).fetchone()
    r = c.execute("select owner_name, khasra_no, khata_no, plot_no, village, previous_owner, new_owner, mutation_no, registration_no, area_value from land_records where document_id=(select id from source_documents where doc_id=?)", (doc_id,)).fetchone()
    print(d[0], "words:", d[1])
    print("  ", r)
