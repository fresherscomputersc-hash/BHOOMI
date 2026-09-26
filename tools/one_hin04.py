import json
rep = json.load(open("/home/ubuntu/Bhuverify-pilot/data/stress_hindi/report_full.json"))
for d in rep:
    if d.get("doc_id") == "DOC-40792819A6":
        print(d["file"], d["status"])
        print("fields:", json.dumps(d.get("fields"), ensure_ascii=False)[:600])
        print("findings:", json.dumps(d.get("findings"), ensure_ascii=False)[:500])
