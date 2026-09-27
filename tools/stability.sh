set -e
cd /home/ubuntu/BhuSure-pilot
STRESS="DOC-7E22D7E8FE,DOC-A34D3132C0,DOC-77EADAF0A1,DOC-0311738E10,DOC-5F11B732FA"
HINDI="DOC-D31D0C5D90,DOC-ABBCBF9EC0,DOC-17A725D645,DOC-40792819A6,DOC-A214441E0D"
ENG="DOC-FDDAE6896C,DOC-1A616C1640,DOC-F935EE7D6B,DOC-6A0657EB42,DOC-8BC2DF5952"
ALL="$STRESS,$HINDI,$ENG"
repro() {
./venv-pilot/bin/python - "$ALL" <<'PYEOF'
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
}
sed -i 's/^GROQ_ENABLED=.*/GROQ_ENABLED=0/' .env.pilot
sudo systemctl restart bhusure-pilot
sleep 40
repro
./venv-pilot/bin/python tools/refetch.py --dir data/stress --docs "$STRESS" >/dev/null 2>&1
./venv-pilot/bin/python tools/refetch.py --dir data/stress_hindi --docs "$HINDI" >/dev/null 2>&1
./venv-pilot/bin/python tools/refetch.py --dir data/stress_english --docs "$ENG" >/dev/null 2>&1
mkdir -p data/roundA
cp data/stress/report_full.json data/roundA/stress.json
cp data/stress_hindi/report_full.json data/roundA/hindi.json
cp data/stress_english/report_full.json data/roundA/english.json
repro
./venv-pilot/bin/python tools/refetch.py --dir data/stress --docs "$STRESS" >/dev/null 2>&1
./venv-pilot/bin/python tools/refetch.py --dir data/stress_hindi --docs "$HINDI" >/dev/null 2>&1
./venv-pilot/bin/python tools/refetch.py --dir data/stress_english --docs "$ENG" >/dev/null 2>&1
mkdir -p data/roundB
cp data/stress/report_full.json data/roundB/stress.json
cp data/stress_hindi/report_full.json data/roundB/hindi.json
cp data/stress_english/report_full.json data/roundB/english.json
./venv-pilot/bin/python - <<'PYEOF'
import json
for name in ("stress", "hindi", "english"):
    a = {d["doc_id"]: d for d in json.load(open(f"/home/ubuntu/BhuSure-pilot/data/roundA/{name}.json"))}
    b = {d["doc_id"]: d for d in json.load(open(f"/home/ubuntu/BhuSure-pilot/data/roundB/{name}.json"))}
    print("#" * 20, name)
    for doc_id in a:
        fa, fb = a[doc_id].get("fields") or {}, b[doc_id].get("fields") or {}
        diffs = [k for k in set(list(fa) + list(fb)) if fa.get(k) != fb.get(k)]
        wa = a[doc_id].get("ocr_words") == b[doc_id].get("ocr_words")
        print(f"{a[doc_id].get('file')}: ocr_words stable={wa} ({a[doc_id].get('ocr_words')} vs {b[doc_id].get('ocr_words')}) field_diffs={diffs}")
PYEOF
sed -i 's/^GROQ_ENABLED=.*/GROQ_ENABLED=1/' .env.pilot
sudo systemctl restart bhusure-pilot
sleep 30
sudo systemctl is-active bhusure-pilot
