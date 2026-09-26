import json, sys
for d, f in (("stress", "/home/ubuntu/Bhuverify-pilot/data/stress/report_full.json"),
             ("realror", "/home/ubuntu/Bhuverify-pilot/data/realror/report_full.json"),
             ("hindi", "/home/ubuntu/Bhuverify-pilot/data/stress_hindi/report_full.json"),
             ("english", "/home/ubuntu/Bhuverify-pilot/data/stress_english/report_full.json")):
    print("#" * 25, d)
    txt = open(f).read()
    try:
        rep = json.loads(txt)
    except Exception as e:
        print("parse-fail", e)
        continue
    for x in rep:
        flds = x.get("fields") or {}
        print("-" * 60)
        print(x.get("file"), x.get("status"), "ocr:", x.get("ocr_words"),
              x.get("ocr_conf"), "ms:", x.get("total_ms"), "rec:", x.get("record_conf"))
        print("  owner:", repr(flds.get("owner_name"))[:60],
              "| guardian:", repr(flds.get("guardian_name"))[:60])
        print("  village:", repr(flds.get("village"))[:50],
              "| tehsil:", repr(flds.get("tehsil"))[:40],
              "| area:", flds.get("area_value"), flds.get("area_unit"))
        print("  src:", [s for s in (x.get("sources") or []) if s[1] != "regex"])
        print("  findings:", [(a, b) for a, b, _ in (x.get("findings") or [])])
