"""
EC2-only stress set (branch `ec2-pilot`, never GitHub).

Five documents beyond the six demo samples, each with recorded ground truth
and the expected rule outcome. Rendered with app.sample_documents helpers so
Tesseract must genuinely read them:

  STRESS-1  heavy degradation (7deg skew, noise 90, JPEG q30) -> confidence bands
  STRESS-2  Odia-script RoR fragment                        -> ori path + aliases
  STRESS-3  Hindi handwritten register                      -> HTR + NER assists
  STRESS-4  occluded page, classification missing           -> BR-1 must FAIL
  STRESS-5  mutation page (parties, case no, dates)         -> BR-5 / BR-10

Usage (on EC2 pilot box):
    cd /home/ubuntu/BhuSure-pilot
    ./venv-pilot/bin/python tools/stress_docs.py --out data/stress
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import ImageDraw

from app.sample_documents import Line, render_document

GROUND_TRUTH: dict[str, dict] = {}


def stress_01(out: Path) -> Path:
    p = out / "stress_01_heavy_degrade.jpg"
    render_document(
        path=p,
        header=["Record of Rights (RoR)", "District Khordha | Tehsil Jatni"],
        lines=[
            Line("District", "Khordha"),
            Line("Tehsil / Block", "Jatni"),
            Line("Village / Mouza", "Pipli"),
            Line("Khata Number", "311"),
            Line("Khasra Number", "512/3"),
            Line("Survey Number", "512"),
            Line("Plot Number", "3"),
            Line("Owner Name", "Minati Sahu"),
            Line("Father Name", "Late Birabar Sahu"),
            Line("Area", "1.50 acre"),
            Line("Classification", "Irrigated land"),
            Line("Mutation Number", "2341/2022"),
            Line("Mutation Date", "14/03/2022"),
        ],
        footer=["Stress 01: heavy degradation; all fields present."],
        skew_degrees=7.0,
        noise=90,
        jpeg_quality=30,
        seed=21,
    )
    GROUND_TRUTH[p.name] = {
        "village": "Pipli", "khasra_no": "512/3", "khata_no": "311",
        "owner_name": "Minati Sahu", "area": "1.50",
        "expect": "all fields extractable; confidence mostly <90; BR-10 pass",
    }
    return p


def stress_02(out: Path) -> Path:
    p = out / "stress_02_odia_khatiyan.png"
    render_document(
        path=p,
        header=["ଖତିୟାନ", "ଜିଲ୍ଲା ଖୋର୍ଦ୍ଧା | ତହସିଲ ଟାଙ୍ଗୀ"],
        lines=[
            Line("ଜିଲ୍ଲା", "ଖୋର୍ଦ୍ଧା"),
            Line("ତହସିଲ", "ଟାଙ୍ଗୀ"),
            Line("ମୌଜା", "ବାଣପୁର"),
            Line("ଖେୱାଟ", "45"),
            Line("ପ୍ଲଟ", "88/1"),
            Line("ପ୍ରଜା", "ଭଗବାନ ନାୟକ"),
            Line("ରକବା", "0.60 ଏକର"),
            Line("କିସମ", "କୃଷି"),
        ],
        script="oriya",
        footer=["ଚାପ ପରୀକ୍ଷା: ଓଡ଼ିଆ ଲିପି"],
        seed=22,
    )
    GROUND_TRUTH[p.name] = {
        "village": "Banapur", "plot_no": "88/1", "owner_name": "ଭଗବାନ ନାୟକ",
        "expect": "ori OCR reads script; aliases resolve village; 39-A-style numbers stay dedicated",
    }
    return p


def stress_03(out: Path) -> Path:
    p = out / "stress_03_hindi_handwritten.png"
    lines = [
        Line("ग्राम", "बेगुनिया", style="handwritten"),
        Line("खसरा संख्या", "340", style="handwritten"),
        Line("खाता संख्या", "77", style="handwritten"),
        Line("खातेदार का नाम", "रमेश चंद्र बेहरा", style="handwritten"),
        Line("पिता का नाम", "स्व० हरिहर बेहरा", style="handwritten"),
        Line("रकबा", "3.00 एकड़", style="handwritten"),
        Line("किस्म", "कृषि भूमि", style="handwritten"),
    ]
    render_document(
        path=p,
        header=["जमाबंदी पंजी", "जिला खुर्दा | तहसील बेगुनिया"],
        lines=lines,
        script="devanagari",
        footer=["हस्तलिखित पंजी पृष्ठ"],
        skew_degrees=1.5,
        noise=30,
        seed=23,
    )
    GROUND_TRUTH[p.name] = {
        "village": "Begunia", "khasra_no": "340", "owner_name": "रमेश चंद्र बेहरा",
        "expect": "HTR path; NER/Groq assists fill names; confidence <90",
    }
    return p


def stress_04(out: Path) -> Path:
    p = out / "stress_04_occluded.png"
    render_document(
        path=p,
        header=["Record of Rights (RoR)", "District Khordha | Tehsil Bhubaneswar"],
        lines=[
            Line("District", "Khordha"),
            Line("Tehsil / Block", "Bhubaneswar"),
            Line("Village / Mouza", "Patia"),
            Line("Khata Number", "512"),
            Line("Khasra Number", "88/1"),
            Line("Owner Name", "Bhagaban Nayak"),
            Line("Father Name", "Late Fakir Nayak"),
            Line("Area", "0.60 acre"),
            Line("Classification", "Plantation land"),
            Line("Registration No", "1234/2019"),
        ],
        footer=["Stress 04: classification cell occluded below."],
        seed=24,
    )
    # Occlude the classification row: black out a band near the bottom rows.
    from PIL import Image
    img = Image.open(p).convert("RGB")
    w, h = img.size
    draw = ImageDraw.Draw(img)
    # classification is row 9 of 10 -> y band approx (values depend on layout)
    draw.rectangle([60, h - 330, w - 60, h - 280], fill=(25, 25, 28))
    # torn corner
    draw.polygon([(w, 0), (w - 190, 0), (w, 190)], fill=(247, 244, 235))
    img.save(p)
    GROUND_TRUTH[p.name] = {
        "owner_name": "Bhagaban Nayak", "khasra_no": "88/1",
        "expect": "classification unreadable -> BR-1 must FAIL, record needs review",
    }
    return p


def stress_05(out: Path) -> Path:
    p = out / "stress_05_mutation.png"
    render_document(
        path=p,
        header=["Mutation Register", "Namantaran | District Khordha"],
        lines=[
            Line("District", "Khordha"),
            Line("Tehsil / Block", "Khordha Sadar"),
            Line("Village / Mouza", "Balarampur"),
            Line("Khata Number", "204"),
            Line("Khasra Number", "118/4"),
            Line("Previous Owner", "Prafulla Kumar Sahoo"),
            Line("New Owner", "Minati Sahu"),
            Line("Mutation Number", "4455/2020"),
            Line("Mutation Date", "22/11/2020"),
            Line("Registration No", "4455/2020"),
            Line("Area", "0.75 acre"),
            Line("Classification", "Irrigated land"),
        ],
        footer=["Stress 05: full mutation chain present."],
        stamp_text="REGISTERED",
        seed=25,
    )
    GROUND_TRUTH[p.name] = {
        "previous_owner": "Prafulla Kumar Sahoo", "new_owner": "Minati Sahu",
        "mutation_no": "4455/2020",
        "expect": "BR-5 chain continuity pass; parties extracted via NER",
    }
    return p


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/stress")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    made = [stress_01(out), stress_02(out), stress_03(out),
            stress_04(out), stress_05(out)]
    (out / "ground_truth.json").write_text(json.dumps(GROUND_TRUTH, indent=2,
                                                      ensure_ascii=False))
    for p in made:
        print(f"made {p} ({p.stat().st_size // 1024} KB)")
    print(f"ground truth -> {out / 'ground_truth.json'}")


if __name__ == "__main__":
    main()
