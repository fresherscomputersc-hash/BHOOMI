import sqlite3
c = sqlite3.connect("data/bhuverify.db")
for row in c.execute(
        "select doc_id, original_filename, status from source_documents "
        "where doc_id in ('DOC-17A725D645','DOC-77EADAF0A1')"):
    print(row)
