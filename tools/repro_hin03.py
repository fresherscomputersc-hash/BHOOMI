import json, urllib.request
BASE = "http://127.0.0.1:8001"
tok = json.load(urllib.request.urlopen(urllib.request.Request(
    BASE + "/api/v1/auth/login",
    data=json.dumps({"username": "operator", "password": "operator123"}).encode(),
    headers={"Content-Type": "application/json"})))["token"]
req = urllib.request.Request(BASE + "/api/v1/documents/DOC-17A725D645/process",
                             data=b"", method="POST",
                             headers={"Authorization": "Bearer " + tok})
print("reprocess:", urllib.request.urlopen(req, timeout=1800).status, flush=True)
