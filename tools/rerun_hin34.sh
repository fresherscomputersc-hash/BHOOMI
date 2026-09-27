set -e
cd /home/ubuntu/BhuSure-pilot
DOCS="DOC-17A725D645,DOC-40792819A6"
./venv-pilot/bin/python - "$DOCS" <<'PYEOF'
import json, sys, urllib.request
BASE = "http://127.0.0.1:8001"
tok = json.load(urllib.request.urlopen(urllib.request.Request(
    BASE + "/api/v1/auth/login",
    data=json.dumps({"username": "operator", "password": "operator123"}).encode(),
    headers={"Content-Type": "application/json"})))["token"]
for d in sys.argv[1].split(","):
    req = urllib.request.Request(BASE + f"/api/v1/documents/{d}/process",
                                 data=b"", method="POST",
                                 headers={"Authorization": "Bearer " + tok})
    print(d, "reprocess:", urllib.request.urlopen(req, timeout=1200).status, flush=True)
PYEOF
./venv-pilot/bin/python tools/refetch.py --dir data/stress_hindi --docs "$DOCS" > /home/ubuntu/hin34.log 2>&1
grep -E "hin_0|owner:|village:|ocr:|findings:|engine" /home/ubuntu/BhuSure-pilot/data/stress_hindi/report_full.json | head -5
./venv-pilot/bin/python - <<'PYEOF'
import json
rep = json.load(open("/home/ubuntu/BhuSure-pilot/data/stress_hindi/report_full.json"))
for d in rep:
    if d.get("doc_id") in ("DOC-17A725D645", "DOC-40792819A6"):
        print("=" * 40)
        print(d["file"], d["status"], "ocr:", d["ocr_words"], d["ocr_conf"])
        print("fields:", json.dumps(d.get("fields"), ensure_ascii=False)[:700])
        print("src:", [s for s in (d.get("sources") or []) if s[1] != "regex"])
        print("findings:", [(a, b) for a, b, _ in (d.get("findings") or [])])
PYEOF
