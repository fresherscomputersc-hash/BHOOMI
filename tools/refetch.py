"""Refetch full details for already-processed docs (no re-upload).

Usage on EC2: ./venv-pilot/bin/python tools/refetch.py --dir data/stress
              ./venv-pilot/bin/python tools/refetch.py --dir data/realror
Reads <dir>/report.json doc_ids, writes <dir>/report_full.json
"""
from __future__ import annotations

import argparse
import json

from run_stress import api, login, summarize


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="data/stress")
    ap.add_argument("--base", default="http://127.0.0.1:8001")
    args = ap.parse_args()
    import run_stress
    run_stress.BASE = args.base
    token = login()
    prior = json.load(open(args.dir + "/report.json"))
    full = []
    for item in prior:
        doc_id = item.get("doc_id")
        if not doc_id or item.get("error"):
            full.append(item)
            continue
        try:
            full.append(summarize(token, doc_id))
        except Exception as e:  # noqa: BLE001
            full.append({**item, "refetch_error": f"{type(e).__name__}: {e}"})
    open(args.dir + "/report_full.json", "w").write(
        json.dumps(full, indent=2, ensure_ascii=False))
    print(json.dumps(full, indent=2, ensure_ascii=False)[:6000])


if __name__ == "__main__":
    main()
