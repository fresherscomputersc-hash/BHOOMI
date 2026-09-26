import time, urllib.request, json
for i in range(20):
    try:
        code = urllib.request.urlopen("http://127.0.0.1:8000/api/v1/health", timeout=10).status
    except Exception as e:
        code = type(e).__name__
    print(i, code, flush=True)
    if code == 200:
        break
    time.sleep(15)
