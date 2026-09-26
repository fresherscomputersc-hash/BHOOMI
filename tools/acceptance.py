"""Score records against ground_truth.json per stress set.

Usage on EC2: ./venv-pilot/bin/python tools/acceptance.py
Reads data/<set>/report_full.json + data/<set>/ground_truth.json for the
three synthetic sets. Field match: exact after casefold/strip, else
rapidfuzz token-sort >= 70 counts as hit (names), identifiers exact only.
"""
from __future__ import annotations

import json

SETS = ("stress", "stress_hindi", "stress_english")
IDENTIFIERS = {"khasra_no", "khata_no", "survey_no", "plot_no",
               "mutation_no", "registration_no"}
SKIP_KEYS = {"profile", "expect"}
# Ground-truth names vs record keys.
FIELD_MAP = {"area": "area_value"}


def _norm(value) -> str:
    return " ".join(str(value or "").split()).casefold()


def score(expected: str, actual, field: str) -> bool:
    exp, got = _norm(expected), _norm(actual)
    if not exp or not got:
        return False
    if field in IDENTIFIERS:
        return exp == got
    if field == "area":
        try:
            return abs(float(exp) - float(got)) < 0.005
        except ValueError:
            pass
    if exp == got:
        return True
    try:
        from rapidfuzz import fuzz
        return fuzz.token_sort_ratio(exp, got) >= 70
    except Exception:
        return exp in got or got in exp


def main() -> None:
    total, hits = 0, 0
    by_field: dict[str, list[int]] = {}
    print(f"{'doc':38} {'hit/total':>9}  misses")
    for name in SETS:
        try:
            rep = json.load(open(f"data/{name}/report_full.json"))
            gt = json.load(open(f"data/{name}/ground_truth.json"))
        except FileNotFoundError:
            print(f"[{name}] missing report/ground truth, skipped")
            continue
        for doc in rep:
            exp = gt.get((doc.get("file") or "").split("/")[-1], {})
            fields = doc.get("fields") or {}
            miss = []
            h = t = 0
            for field, want in exp.items():
                if field in SKIP_KEYS:
                    continue
                t += 1
                got = fields.get(FIELD_MAP.get(field, field))
                ok = score(want, got, field)
                h += ok
                by_field.setdefault(field, [0, 0])
                by_field[field][0] += ok
                by_field[field][1] += 1
                if not ok:
                    miss.append(f"{field}={want!r:.28}")
            total += t
            hits += h
            print(f"{doc.get('file', '?'):38} {h}/{t:>9}  {'; '.join(miss)[:110]}")
    print(f"\nOVERALL {hits}/{total} = {100.0 * hits / total:.1f}%" if total else "no data")
    for field, (h, t) in sorted(by_field.items()):
        print(f"  {field:22} {h}/{t} = {100.0 * h / t:.0f}%")


if __name__ == "__main__":
    main()
