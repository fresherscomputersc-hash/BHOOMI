"""
English stress set, EC2/localhost use (branch `ec2-pilot`).

  ENG-1 clean printed RoR                 -> identifiers + NER assist
  ENG-2 degraded print (6deg, noise, q32) -> deskew/denoise limits
  ENG-3 sale deed abstract                -> parties, BR-10, dates
  ENG-4 tabular khatauni (NIC-style)      -> table-row/cell fallbacks
  ENG-5 stamp-heavy + missing tehsil      -> BR-7 mismatch, stamp noise

Usage: python tools/stress_docs_english.py --out data/stress_english
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.sample_documents import Line, render_document

GROUND_TRUTH: dict[str, dict] = {}


def eng_01(out: Path) -> Path:
    p = out / "eng_01_clean_ror.png"
    render_document(
        path=p,
        header=["Record of Rights (RoR)", "Odisha | District Khordha"],
        lines=[
            Line("District", "Khordha"),
            Line("Tehsil / Block", "Khordha Sadar"),
            Line("Village / Mouza", "Balarampur"),
            Line("Khata Number", "204"),
            Line("Khasra Number", "118/2"),
            Line("Owner Name", "Prafulla Kumar Sahoo"),
            Line("Father Name", "Late Jadumani Sahoo"),
            Line("Area", "1.14 acre"),
            Line("Classification", "Irrigated land"),
            Line("Registration No", "1234/2019"),
        ],
        footer=["Clean English RoR control page."],
        seed=41,
    )
    GROUND_TRUTH[p.name] = {
        "khasra_no": "118/2", "owner_name": "Prafulla Kumar Sahoo",
        "expect": "near-full extraction, high confidence",
    }
    return p


def eng_02(out: Path) -> Path:
    p = out / "eng_02_degraded.jpg"
    render_document(
        path=p,
        header=["Record of Rights (RoR)", "Odisha | District Khordha"],
        lines=[
            Line("District", "Khordha"),
            Line("Tehsil / Block", "Jatni"),
            Line("Village / Mouza", "Taraboi"),
            Line("Khata Number", "98"),
            Line("Khasra Number", "512/3"),
            Line("Owner Name", "Minati Sahu"),
            Line("Area", "1.50 acre"),
            Line("Classification", "Unirrigated land"),
        ],
        footer=["Degraded English page."],
        skew_degrees=6.0,
        noise=80,
        jpeg_quality=32,
        seed=42,
    )
    GROUND_TRUTH[p.name] = {
        "khasra_no": "512/3", "owner_name": "Minati Sahu",
        "expect": "deskew recovers 6deg; confidence medium, review-bound",
    }
    return p


def eng_03(out: Path) -> Path:
    p = out / "eng_03_sale_deed.png"
    render_document(
        path=p,
        header=["Sale Deed Abstract", "Sub-Registrar Office Khordha"],
        lines=[
            Line("District", "Khordha"),
            Line("Village / Mouza", "Bhubaneswar"),
            Line("Vendor", "Anonymous Trust"),
            Line("Purchaser", "Sunita Pradhan"),
            Line("Khasra Number", "227/1"),
            Line("Area", "2.00 acre"),
            Line("Registration No", "876/2021"),
            Line("Mutation Date", "05/06/2021"),
        ],
        stamp_text="REGISTERED",
        footer=["Deed abstract for cross-check testing."],
        seed=43,
    )
    GROUND_TRUTH[p.name] = {
        "previous_owner": "Anonymous Trust", "new_owner": "Sunita Pradhan",
        "registration_no": "876/2021",
        "expect": "vendor/purchaser parties; BR-10 registration format",
    }
    return p


def eng_04(out: Path) -> Path:
    p = out / "eng_04_table_khatauni.png"
    render_document(
        path=p,
        header=["Khatauni Table", "Village Register Extract"],
        lines=[
            Line("Owner Name | Relation | Khasra No. | Khata | Area", ""),
            Line("1 Ramesh Chandra Behera | S/o Harihar | 340 | 77 | 3.00", ""),
            Line("District", "Khordha"),
            Line("Village / Mouza", "Jankia"),
            Line("Tehsil / Block", "Jankia"),
        ],
        table=False,
        footer=["Tabular page for row/cell fallback."],
        seed=44,
    )
    GROUND_TRUTH[p.name] = {
        "owner_name": "Ramesh Chandra Behera", "khasra_no": "340",
        "expect": "table-row owner + cell identifiers, no label anchoring",
    }
    return p


def eng_05(out: Path) -> Path:
    p = out / "eng_05_stamp_missing_tehsil.png"
    render_document(
        path=p,
        header=["Record of Rights (RoR)", "Odisha | District Khordha"],
        lines=[
            Line("District", "Khordha"),
            Line("Village / Mouza", "Golabai"),
            Line("Khata Number", "118"),
            Line("Khasra Number", "227/1"),
            Line("Owner Name", "Sunita Pradhan"),
            Line("Area", "2.00 acre"),
            Line("Classification", "Unirrigated land"),
        ],
        stamp_text="VERIFIED",
        footer=["Tehsil line deliberately absent."],
        seed=45,
    )
    GROUND_TRUTH[p.name] = {
        "khasra_no": "227/1",
        "expect": "BR-7 hierarchy flags missing tehsil; stamp ignored",
    }
    return p


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/stress_english")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    made = [eng_01(out), eng_02(out), eng_03(out), eng_04(out), eng_05(out)]
    (out / "ground_truth.json").write_text(
        json.dumps(GROUND_TRUTH, indent=2, ensure_ascii=False), encoding="utf-8")
    for p in made:
        print(f"made {p} ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
