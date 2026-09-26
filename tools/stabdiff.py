import json
for name in ("stress", "hindi", "english"):
    a = {d["doc_id"]: d for d in json.load(open(f"/home/ubuntu/Bhuverify-pilot/data/roundA/{name}.json"))}
    b = {d["doc_id"]: d for d in json.load(open(f"/home/ubuntu/Bhuverify-pilot/data/roundB/{name}.json"))}
    print("#" * 20, name)
    for doc_id in a:
        fa, fb = a[doc_id].get("fields") or {}, b[doc_id].get("fields") or {}
        diffs = [k for k in set(list(fa) + list(fb)) if fa.get(k) != fb.get(k)]
        wa = a[doc_id].get("ocr_words") == b[doc_id].get("ocr_words")
        print(f"{a[doc_id].get('file')}: ocr_stable={wa} ({a[doc_id].get('ocr_words')} vs {b[doc_id].get('ocr_words')}) field_diffs={diffs}")
