set -e
cd /home/ubuntu/Bhuverify-pilot
STRESS="DOC-7E22D7E8FE,DOC-A34D3132C0,DOC-77EADAF0A1,DOC-0311738E10,DOC-5F11B732FA"
REAL="DOC-1FB224189E,DOC-32EF2C9A42,DOC-5079BA613F,DOC-8254348B5A,DOC-C6716C084E"
sed -i 's/^GROQ_ENABLED=.*/GROQ_ENABLED=0/' .env.pilot
sudo systemctl restart bhuverify-pilot
sleep 12
./venv-pilot/bin/python - "$STRESS $REAL" <<'PYEOF'
import json, sys, urllib.request
BASE = "http://127.0.0.1:8001"
tok = json.load(urllib.request.urlopen(urllib.request.Request(
    BASE + "/api/v1/auth/login",
    data=json.dumps({"username": "operator", "password": "operator123"}).encode(),
    headers={"Content-Type": "application/json"})))["token"]
for doc_id in sys.argv[1].split():
    for d in doc_id.split(","):
        req = urllib.request.Request(BASE + f"/api/v1/documents/{d}/process",
                                     data=b"", method="POST",
                                     headers={"Authorization": "Bearer " + tok})
        print(d, "reprocess:", urllib.request.urlopen(req, timeout=1200).status, flush=True)
PYEOF
./venv-pilot/bin/python tools/refetch.py --dir data/stress --docs "$STRESS" > /home/ubuntu/stress-full5.log 2>&1
./venv-pilot/bin/python tools/refetch.py --dir data/realror --docs "$REAL" > /home/ubuntu/realror-full3.log 2>&1
tail -3 /home/ubuntu/stress-full5.log
tail -3 /home/ubuntu/realror-full3.log
sed -i 's/^GROQ_ENABLED=.*/GROQ_ENABLED=1/' .env.pilot
sudo systemctl restart bhuverify-pilot
sleep 10
sudo systemctl is-active bhuverify-pilot
