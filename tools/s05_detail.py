import json
rep = json.load(open("/home/ubuntu/BhuSure-pilot/data/stress/report_full.json"))
for d in rep:
    if d.get("file", "").startswith("stress_05"):
        print(d.get("status"), "err:", (d.get("error") or "")[:150])
        print("ocr:", d.get("ocr_words"), d.get("ocr_conf"), "ms:", d.get("total_ms"),
              "rec_conf:", d.get("record_conf"))
        print("fields:", json.dumps(d.get("fields"), ensure_ascii=False))
        print("sources:", d.get("sources"))
        print("findings:", json.dumps(d.get("findings"), ensure_ascii=False))
