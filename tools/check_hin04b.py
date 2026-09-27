import sqlite3
c = sqlite3.connect("data/bhusure.db")
doc = c.execute("select ocr_text from source_documents where original_filename='hin_04_bihar_khatiyan.png' order by id desc limit 1").fetchone()[0]
for i, ln in enumerate(doc.splitlines()[:9]):
    print(i, repr(ln[:70]))
from app.services.extraction import detect_profile
print("profile:", detect_profile(doc))
