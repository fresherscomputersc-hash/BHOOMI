set -e
cd /home/ubuntu/Bhuverify-pilot
DOCS="DOC-7E22D7E8FE,DOC-A34D3132C0,DOC-77EADAF0A1,DOC-0311738E10,DOC-5F11B732FA"
./venv-pilot/bin/python - "$DOCS" <<'PYEOF'
import json, sys, time, urllib.request
BASE = "http://127.0.0.1:8001"
tok = json.load(urllib.request.urlopen(urllib.request.Request(
    BASE + "/api/v1/auth/login",
    data=json.dumps({"username": "operator", "password": "operator123"}).encode(),
    headers={"Content-Type": "application/json"})))["token"]
for doc_id in sys.argv[1].split(","):
    req = urllib.request.Request(BASE + f"/api/v1/documents/{doc_id}/process",
                                 data=b"", method="POST",
                                 headers={"Authorization": "Bearer " + tok})
    print(doc_id, "reprocess:", urllib.request.urlopen(req, timeout=900).status)
PYEOF
sleep 5
./venv-pilot/bin/python tools/refetch.py --dir data/stress --docs "$DOCS" > /home/ubuntu/stress-full4.log 2>&1
tail -4 /home/ubuntu/stress-full4.log
