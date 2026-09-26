set -e
cd /home/ubuntu/Bhuverify-pilot
sudo systemctl restart bhuverify-pilot
sleep 15
sudo systemctl is-active bhuverify-pilot
./venv-pilot/bin/python - <<'PYEOF'
import json, urllib.request
BASE = "http://127.0.0.1:8001"
tok = json.load(urllib.request.urlopen(urllib.request.Request(
    BASE + "/api/v1/auth/login",
    data=json.dumps({"username": "operator", "password": "operator123"}).encode(),
    headers={"Content-Type": "application/json"})))["token"]
req = urllib.request.Request(BASE + "/api/v1/documents/DOC-5F11B732FA/process",
                             data=b"", method="POST",
                             headers={"Authorization": "Bearer " + tok})
print("reprocess:", urllib.request.urlopen(req, timeout=600).status)
PYEOF
for i in $(seq 1 20); do
  st=$(./venv-pilot/bin/python -c "pass" 2>/dev/null; curl -s http://127.0.0.1:8001/api/v1/documents/DOC-5F11B732FA -H "Authorization: Bearer $(curl -s -X POST http://127.0.0.1:8001/api/v1/auth/login -H 'Content-Type: application/json' -d '{"username":"operator","password":"operator123"}' | ./venv-pilot/bin/python -c 'import json,sys; print(json.load(sys.stdin)["token"])')" | ./venv-pilot/bin/python -c "import json,sys; print(json.load(sys.stdin)['status'])")
  echo "poll $i: $st"
  if [ "$st" != "queued" ] && [ "$st" != "preprocessing" ] && [ "$st" != "ocr_running" ] && [ "$st" != "extracting" ] && [ "$st" != "validating" ]; then break; fi
  sleep 20
done
./venv-pilot/bin/python tools/refetch.py --dir data/stress > /home/ubuntu/stress-full2.log 2>&1
grep -A40 stress_05_mutation /home/ubuntu/stress-full2.log | head -60
