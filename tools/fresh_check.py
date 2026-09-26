import sqlite3
c = sqlite3.connect("data/bhuverify.db")
for fn in ("eng_01_clean_ror.png", "stress_05_mutation.png", "hin_01_up_khatauni.png"):
    d = c.execute("select doc_id, status, ocr_word_count, processed_at from source_documents where original_filename=?", (fn,)).fetchone()
    print(fn, d)
    r = c.execute("select record_id, owner_name, khasra_no, khata_no, plot_no, village, previous_owner, new_owner, mutation_no, registration_no from land_records where document_id=?", (d[0],) if isinstance(d[0], int) else None) if False else None
    doc = c.execute("select id from source_documents where original_filename=?", (fn,)).fetchone()
    for row in c.execute("select record_id, owner_name, khasra_no, khata_no, plot_no, village, previous_owner, new_owner, mutation_no, registration_no from land_records where document_id=?", (doc[0],)):
        print("  rec:", row)
