"""
Hindi-belt stress set, EC2/localhost use (branch `ec2-pilot`).

  HIN-1 clean UP Khatauni (Lucknow... Sitapur)   -> up_khatauni profile, Gata
  HIN-2 degraded MP Khasra                       -> mp_khasra + deskew stress
  HIN-3 handwritten Hindi register               -> HTR + hin second pass
  HIN-4 Bihar Khatiyan with Anchal               -> bihar_khatiyan + anchal alias
  HIN-5 Hindi mutation with parties              -> BR-5 chain, Hindi dates

Usage: python tools/stress_docs_hindi.py --out data/stress_hindi
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.sample_documents import Line, render_document

GROUND_TRUTH: dict[str, dict] = {}


def hin_01(out: Path) -> Path:
    p = out / "hin_01_up_khatauni.png"
    render_document(
        path=p,
        header=["खतौनी", "उत्तर प्रदेश | जिला सीतापुर | तहसील महमूदाबाद"],
        lines=[
            Line("जिला", "सीतापुर"),
            Line("तहसील", "महमूदाबाद"),
            Line("ग्राम", "रामपुर"),
            Line("खाता संख्या", "45"),
            Line("गाटा संख्या", "118"),
            Line("खातेदार का नाम", "श्री रमेश कुमार"),
            Line("पिता का नाम", "स्व० हरदयाल"),
            Line("क्षेत्रफल", "1.25 हेक्टेयर"),
            Line("भूमि का प्रकार", "कृषि भूमि"),
        ],
        script="devanagari",
        footer=["उत्तर प्रदेश खतौनी परीक्षण पृष्ठ"],
        seed=31,
    )
    GROUND_TRUTH[p.name] = {
        "profile": "up_khatauni", "village": "रामपुर", "khata_no": "45",
        "plot_no": "118", "owner_name": "रमेश कुमार",
        "expect": "up_khatauni profile; Gata->plot_no; honorific stripped",
    }
    return p


def hin_02(out: Path) -> Path:
    p = out / "hin_02_mp_khasra.jpg"
    render_document(
        path=p,
        header=["खसरा पंचशाला", "मध्य प्रदेश | जिला सीहोर | पटवारी हल्का 12"],
        lines=[
            Line("जिला", "सीहोर"),
            Line("तहसील", "सीहोर"),
            Line("ग्राम", "बिलकिसगंज"),
            Line("खसरा संख्या", "227/1"),
            Line("खातेदार", "सुनीता प्रधान"),
            Line("पति का नाम", "रमेश प्रधान"),
            Line("रकबा", "2.00 एकड़"),
            Line("किस्म", "सिंचित भूमि"),
        ],
        script="devanagari",
        footer=["मध्य प्रदेश खसरा परीक्षण"],
        skew_degrees=5.0,
        noise=70,
        jpeg_quality=35,
        seed=32,
    )
    GROUND_TRUTH[p.name] = {
        "profile": "mp_khasra", "khasra_no": "227/1",
        "owner_name": "सुनीता प्रधान",
        "expect": "mp_khasra profile; deskew recovers 5deg; पति alias",
    }
    return p


def hin_03(out: Path) -> Path:
    p = out / "hin_03_handwritten_register.png"
    render_document(
        path=p,
        header=["रोज़नामचा पंजी", "जिला जटनी... खुर्दा | तहसील जटनी"],
        lines=[
            Line("ग्राम", "तरबोई", style="handwritten"),
            Line("खसरा संख्या", "512/3", style="handwritten"),
            Line("खातेदार का नाम", "मिनाती साहू", style="handwritten"),
            Line("पिता का नाम", "बिराबर साहू", style="handwritten"),
            Line("रकबा", "1.50 एकड़", style="handwritten"),
        ],
        script="devanagari",
        footer=["हस्तलिखित पंजी"],
        skew_degrees=1.5,
        noise=30,
        seed=33,
    )
    GROUND_TRUTH[p.name] = {
        "khasra_no": "512/3", "owner_name": "मिनाती साहू",
        "expect": "HTR path + hin second pass; Devanagari not read as Odia",
    }
    return p


def hin_04(out: Path) -> Path:
    p = out / "hin_04_bihar_khatiyan.png"
    render_document(
        path=p,
        header=["जमाबंदी", "बिहार | जिला नालंदा | अंचल बिहारशरीफ"],
        lines=[
            Line("जिला", "नालंदा"),
            Line("अंचल", "बिहारशरीफ"),
            Line("ग्राम", "सोहसराय"),
            Line("खाता संख्या", "12"),
            Line("खेसरा संख्या", "340"),
            Line("खातेदार का नाम", "श्रीमती गीता देवी"),
            Line("पति का नाम", "मोहन प्रसाद"),
            Line("रकबा", "0.80 एकड़"),
        ],
        script="devanagari",
        footer=["बिहार खतियान परीक्षण"],
        seed=34,
    )
    GROUND_TRUTH[p.name] = {
        "profile": "bihar_khatiyan", "khata_no": "12",
        "owner_name": "गीता देवी",
        "expect": "bihar profile via anchal; अंचल alias; honorific stripped",
    }
    return p


def hin_05(out: Path) -> Path:
    p = out / "hin_05_mutation.png"
    render_document(
        path=p,
        header=["नामांतरण पंजी", "उत्तर प्रदेश | दाखिल खारिज"],
        lines=[
            Line("जिला", "सीतापुर"),
            Line("तहसील", "महमूदाबाद"),
            Line("ग्राम", "रामपुर"),
            Line("पूर्व खातेदार", "रमेश कुमार"),
            Line("नया खातेदार", "सुरेश कुमार"),
            Line("नामांतरण संख्या", "4455/2020"),
            Line("नामांतरण दिनांक", "22/11/2020"),
            Line("गाटा संख्या", "118"),
            Line("रकबा", "0.75 एकड़"),
        ],
        script="devanagari",
        stamp_text="स्वीकृत",
        seed=35,
    )
    GROUND_TRUTH[p.name] = {
        "previous_owner": "रमेश कुमार", "new_owner": "सुरेश कुमार",
        "expect": "BR-5 chain; Hindi mutation aliases; parties via NER",
    }
    return p


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/stress_hindi")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    made = [hin_01(out), hin_02(out), hin_03(out), hin_04(out), hin_05(out)]
    (out / "ground_truth.json").write_text(
        json.dumps(GROUND_TRUTH, indent=2, ensure_ascii=False), encoding="utf-8")
    for p in made:
        print(f"made {p} ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
