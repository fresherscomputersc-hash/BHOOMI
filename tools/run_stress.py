"""Upload the stress set to the pilot API (process_sync) and report results.

Runs ON the EC2 pilot box with stdlib only:
    ./venv-pilot/bin/python tools/run_stress.py --dir data/stress --base http://127.0.0.1:8001
"""
from __future__ import annotations

import argparse
import io
import json
import time
import urllib.request

BASE = "http://127.0.0.1:8001"


def api(method: str, path: str, token: str = "", body=None, headers=None):
    req = urllib.request.Request(BASE + path, data=body, method=method)
    if token:
        req.add_header("Authorization", "Bearer " + token)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)


def login() -> str:
    payload = json.dumps({"username": "operator", "password": "operator123"}).encode()
    out = api("POST", "/api/v1/auth/login", body=payload,
              headers={"Content-Type": "application/json"})
    return out["token"]


def upload(token: str, path: str) -> dict:
    import uuid
    boundary = "----stress" + uuid.uuid4().hex
    data = open(path, "rb").read()
    fname = path.split("/")[-1]
    parts = []
    for name, value in (("doc_type", "ror"), ("language", "eng+hin+ori"),
                        ("batch_label", "stress"), ("process_sync", "true")):
        parts += [b"--" + boundary.encode(),
                  f'Content-Disposition: form-data; name="{name}"'.encode(), b"",
                  value.encode()]
    parts += [b"--" + boundary.encode(),
              f'Content-Disposition: form-data; name="files"; filename="{fname}"'.encode(),
              b"Content-Type: image/png", b"", data,
              b"--" + boundary.encode() + b"--", b""]
    body = b"\r\n".join(parts)
    return api("POST", "/api/v1/documents", token=token, body=body,
               headers={"Content-Type": "multipart/form-data; boundary=" + boundary})


def summarize(token: str, doc_id: str) -> dict:
    detail = api("GET", f"/api/v1/documents/{doc_id}", token=token)
    out = {
        "doc_id": doc_id,
        "file": detail.get("original_filename"),
        "status": detail.get("status"),
        "error": (detail.get("error_message") or "")[:300],
        "ocr_words": detail.get("ocr_word_count"),
        "ocr_conf": detail.get("ocr_mean_confidence"),
        "total_ms": detail.get("total_latency_ms"),
    }
    rid = detail.get("record_id")
    if rid:
        try:
            rec = api("GET", f"/api/v1/records/{rid}", token=token)
        except Exception as e:  # noqa: BLE001
            rec = {"_error": f"{type(e).__name__}"}
        out["record_conf"] = rec.get("record_confidence")
        out["fields"] = {k: rec.get(k) for k in (
            "owner_name", "guardian_name", "previous_owner", "new_owner",
            "khasra_no", "khata_no", "village", "tehsil", "district",
            "area_value", "area_unit", "land_classification", "mutation_no",
            "mutation_date", "registration_no", "document_type")}
        out["owners"] = rec.get("owners")
        out["sources"] = sorted({(f.get("field_name"), f.get("source"))
                                 for f in rec.get("fields", []) if f.get("source")})
        out["findings"] = [(d.get("rule_id"), d.get("severity"),
                            (d.get("message") or "")[:90])
                           for d in rec.get("discrepancies", [])]
    return out


def main() -> None:
    global BASE
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="data/stress")
    ap.add_argument("--glob", default="stress_*")
    ap.add_argument("--base", default=BASE)
    args = ap.parse_args()
    BASE = args.base
    import glob as _glob
    token = login()
    print("login ok")
    report = []
    patterns = [args.dir + "/" + args.glob + ext
                for ext in (".png", ".jpg", ".jpeg", ".pdf", ".tif", ".tiff")]
    files = sorted({p for pat in patterns for p in _glob.glob(pat)})
    for path in files:
        t0 = time.time()
        try:
            resp = upload(token, path)
            docs = resp.get("documents") or []
            skipped = resp.get("skipped_duplicates") or []
            if docs:
                doc_id = docs[0].get("doc_id")
            elif skipped:
                # Re-run on an already-ingested file: report the existing doc.
                doc_id = skipped[0].get("existing_doc_id")
            else:
                doc_id = (resp.get("accepted") or ["?"])[0]
            summary = summarize(token, doc_id)
        except Exception as e:  # noqa: BLE001 - report, don't stop
            summary = {"file": path, "error": f"{type(e).__name__}: {e}"}
        summary["client_s"] = round(time.time() - t0, 1)
        report.append(summary)
        print(json.dumps(summary, ensure_ascii=False)[:1200])
    open(args.dir + "/report.json", "w").write(
        json.dumps(report, indent=2, ensure_ascii=False))
    print("report ->", args.dir + "/report.json")


if __name__ == "__main__":
    main()
