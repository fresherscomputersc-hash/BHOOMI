import sqlite3
c = sqlite3.connect("data/bhuverify.db")
doc = c.execute("select id, ocr_text from source_documents where original_filename='hin_04_bihar_khatiyan.png' order by id desc limit 1").fetchone()
print("words:", c.execute("select ocr_word_count from source_documents where id=?", (doc[0],)).fetchone())
for w in ("बिहार", "जमाबंदी", "जगाबंदी", "अंचल", "खाता", "खेसरा", "नालंदा"):
    print(repr(w), "present:", w in doc[1])
