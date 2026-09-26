set -e
cd /home/ubuntu/Bhuverify-pilot
STRESS="DOC-7E22D7E8FE,DOC-A34D3132C0,DOC-77EADAF0A1,DOC-0311738E10,DOC-5F11B732FA"
HINDI="DOC-D31D0C5D90,DOC-ABBCBF9EC0,DOC-17A725D645,DOC-40792819A6,DOC-A214441E0D"
ENG="DOC-FDDAE6896C,DOC-1A616C1640,DOC-F935EE7D6B,DOC-6A0657EB42,DOC-8BC2DF5952"
./venv-pilot/bin/python - "$STRESS,$HINDI,$ENG" <<'PYEOF'
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
    print(d, "reprocess:", urllib.request.urlopen(req, timeout=1800).status, flush=True)
PYEOF
./venv-pilot/bin/python tools/refetch.py --dir data/stress --docs "$STRESS" >/dev/null 2>&1
./venv-pilot/bin/python tools/refetch.py --dir data/stress_hindi --docs "$HINDI" >/dev/null 2>&1
./venv-pilot/bin/python tools/refetch.py --dir data/stress_english --docs "$ENG" >/dev/null 2>&1
./venv-pilot/bin/python tools/acceptance.py
