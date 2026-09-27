set -e
cd /home/ubuntu/BhuSure-pilot
HIN="DOC-D31D0C5D90,DOC-ABBCBF9EC0,DOC-17A725D645,DOC-40792819A6,DOC-A214441E0D"
ENG="DOC-FDDAE6896C,DOC-1A616C1640,DOC-F935EE7D6B,DOC-6A0657EB42,DOC-8BC2DF5952"
sudo systemctl restart bhusure-pilot
sleep 12
./venv-pilot/bin/python - "$HIN $ENG" <<'PYEOF'
import json, sys, urllib.request
BASE = "http://127.0.0.1:8001"
tok = json.load(urllib.request.urlopen(urllib.request.Request(
    BASE + "/api/v1/auth/login",
    data=json.dumps({"username": "operator", "password": "operator123"}).encode(),
    headers={"Content-Type": "application/json"})))["token"]
for group in sys.argv[1].split():
    for d in group.split(","):
        req = urllib.request.Request(BASE + f"/api/v1/documents/{d}/process",
                                     data=b"", method="POST",
                                     headers={"Authorization": "Bearer " + tok})
        print(d, "reprocess:", urllib.request.urlopen(req, timeout=1200).status, flush=True)
PYEOF
./venv-pilot/bin/python tools/refetch.py --dir data/stress_hindi --docs "$HIN" > /home/ubuntu/hindi-full2.log 2>&1
./venv-pilot/bin/python tools/refetch.py --dir data/stress_english --docs "$ENG" > /home/ubuntu/eng-full2.log 2>&1
./venv-pilot/bin/python tools/delta.py > /home/ubuntu/delta3.log 2>&1
tail -60 /home/ubuntu/delta3.log
