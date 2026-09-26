import json, urllib.request
try:
    tok = json.load(urllib.request.urlopen(urllib.request.Request(
        "http://127.0.0.1:8000/api/v1/auth/login",
        data=json.dumps({"username": "reviewer", "password": "reviewer123"}).encode(),
        headers={"Content-Type": "application/json"}), timeout=20))["token"]
    st = json.load(urllib.request.urlopen(urllib.request.Request(
        "http://127.0.0.1:8000/api/v1/system/status",
        headers={"Authorization": "Bearer " + tok}), timeout=20))
    print("live ocr:", st["ocr"]["tesseract_available"], st["ocr"]["tesseract_version"],
          st["ocr"]["installed_languages"])
except Exception as e:
    print("live-status-check-skipped:", type(e).__name__)
