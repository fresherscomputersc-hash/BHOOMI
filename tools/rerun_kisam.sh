set -e
cd /home/ubuntu/Bhuverify-pilot
REAL="DOC-1FB224189E,DOC-32EF2C9A42,DOC-5079BA613F,DOC-8254348B5A,DOC-C6716C084E"
sed -i 's/^GROQ_ENABLED=.*/GROQ_ENABLED=0/' .env.pilot
sudo systemctl restart bhuverify-pilot
sleep 12
./venv-pilot/bin/python - "$REAL" <<'PYEOF'
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
./venv-pilot/bin/python tools/refetch.py --dir data/realror --docs "$REAL" > /home/ubuntu/realror-full4.log 2>&1
./venv-pilot/bin/python tools/delta.py > /home/ubuntu/delta2.log 2>&1
tail -40 /home/ubuntu/delta2.log
sed -i 's/^GROQ_ENABLED=.*/GROQ_ENABLED=1/' .env.pilot
sudo systemctl restart bhuverify-pilot
sleep 10
sudo systemctl is-active bhuverify-pilot
