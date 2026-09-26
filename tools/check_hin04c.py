import sqlite3
c = sqlite3.connect("data/bhuverify.db")
doc = c.execute("select id, ocr_text from source_documents where original_filename='hin_04_bihar_khatiyan.png' order by id desc limit 1").fetchone()
from app.services.extraction import classify_document_type, detect_profile, extract_fields
print("detect:", detect_profile(doc[1]))
out = extract_fields(doc[1], [], profile="generic")
print("classify:", classify_document_type(out))
print("owner:", out.fields["owner_name"].normalized_value)
import app.services.extraction as E
print("has-fuzzy:", "_near" in open(E.__file__).read())
