import os
for line in open("/home/ubuntu/BhuSure-pilot/.env.pilot").read().splitlines():
    k, _, v = line.partition("=")
    if k.strip().startswith("GROQ_"):
        os.environ[k.strip()] = v.strip()
os.environ["GROQ_ENABLED"] = "1"
os.environ["GROQ_TIMEOUT_S"] = "15"
from app.config import settings
import json, urllib.request
req = urllib.request.Request(
    "https://api.groq.com/openai/v1/models",
    headers={"Authorization": "Bearer " + os.environ["GROQ_API_KEY"]})
try:
    ids = [m["id"] for m in json.load(urllib.request.urlopen(req, timeout=20))["data"]]
    print("llama-3.3-70b-versatile available:", "llama-3.3-70b-versatile" in ids)
    print("llama-3.1-8b-instant available:", "llama-3.1-8b-instant" in ids)
except Exception as e:
    print("models-list skipped:", type(e).__name__, e)

from app.services.extraction import extract_fields
from app.services.ocr_service import WordToken
text = ("Record of Rights. Khasra No 118/2. Khata No 204. "
        "Owner Prafulla Kumar Sahoo. Village Balarampur. Area 1.14 acre.")
words = [WordToken(t, 55.0, {"x": 0, "y": 0, "w": 1, "h": 1}) for t in text.split()]
out = extract_fields(text, words)
print("before missing:", out.missing_required, "low:", out.low_confidence_fields)
from app.services import llm_groq
print("groq enabled:", llm_groq.is_enabled(), llm_groq.status()["model"])
out, applied = llm_groq.enhance_outcome(text, out)
print("groq applied:", applied)
for name in applied:
    e = out.fields[name]
    print(name, "->", repr(e.normalized_value), e.confidence, e.source)
