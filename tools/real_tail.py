import json
rep = json.load(open("/home/ubuntu/BhuSure-pilot/data/realror/report_full.json"))
for d in rep:
    if d.get("file") in ("313.pdf", "4-19.pdf"):
        print("=" * 60)
        print(d["file"], d.get("status"), "ocr:", d.get("ocr_words"), d.get("ocr_conf"),
              "ms:", d.get("total_ms"), "rec:", d.get("record_conf"))
        print("fields:", json.dumps(d.get("fields"), ensure_ascii=False)[:700])
        print("owners:", json.dumps(d.get("owners"), ensure_ascii=False)[:400])
        print("sources:", [s for s in (d.get("sources") or []) if s[1] != "regex"])
        print("findings:", json.dumps(d.get("findings"), ensure_ascii=False)[:700])
