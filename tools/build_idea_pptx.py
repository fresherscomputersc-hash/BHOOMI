#!/usr/bin/env python3
"""Fill the official SIH 2026 Idea template with BhuSure content.

Reads ppt/SIH2026-IDEA-Presentation-Format (3).pptx, replaces ONLY text runs
(structure, masters, placeholders, pictures untouched) and writes
ppt/BhuSure_SIH26018_Idea_Presentation.pptx.
Content: BHOOMI README facts only. Style: Arial body bullets w/ bold leads.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from pptx import Presentation
from pptx.util import Pt

HERE = Path(__file__).resolve().parent.parent
TEMPLATE = HERE / "ppt" / "SIH2026-IDEA-Presentation-Format (3).pptx"
OUT = HERE / "ppt" / "BhuSure_SIH26018_Idea_Presentation.pptx"

TEAM = "Shadow Slayers"
BODY_SIZE = Pt(18)

TITLE_IDEA = "BhuSure: Intelligent Land Record Digitization & Validation"

S2 = [
    ("What it is: ",
     "converts scanned registers, handwritten pages, PDFs and cadastral maps into structured, validated, GIS-linked digital records."),
    ("How it works: ",
     "CV preprocessing \u2192 OCR/HTR with word confidence \u2192 17-field extraction (6 doc profiles) \u2192 confidence fusion \u2192 GIS linking \u2192 ten business rules BR-1\u2026BR-10 \u2192 cross-database checks."),
    ("Human in command: ",
     "a government reviewer holds final authority; approval is server-refused (HTTP 409) while critical findings are open."),
    ("No hallucinations: ",
     "anti-hallucination contracts (plot 417 is not a khasra; khatiyan 18 is not a khata); every AI output audit-logged in a SHA-256 hash chain."),
    ("Proven, not claimed: ",
     "165 tests green, 26 documents exercised, 15/15 byte-identical reruns, 36.8% field accuracy on an adversarial set \u2014 all routed to review, zero crashes."),
]

S3 = [
    ("Stack: ",
     "FastAPI \u00b7 SQLAlchemy \u00b7 OpenCV \u00b7 Tesseract 5.5 (eng+hin+ori) \u00b7 Shapely \u00b7 rapidfuzz \u00b7 argon2; vanilla JS, no build step, runs network-isolated."),
    ("Pilot AI tier (flag-gated): ",
     "Groq LLM (gpt-oss-120b), spaCy NER, HF transformers (XLM-R) as verifiers that never overwrite trusted values."),
    ("Method: ",
     "upload \u2192 deskew/denoise/layout \u2192 script-routed OCR (39-A\u2192Oriya, Hindi belt\u2192Hindi) \u2192 label-alias + regex extraction \u2192 0.45/0.30/0.15/0.10 confidence fusion."),
    ("Validation: ",
     "BR-1\u2026BR-10, duplicate detection, Bhulekh/BhuNaksha/IGR/LGD/LRMS adapters (mocked now, live-ready contracts)."),
    ("Growth path: ",
     "SQLite\u2192PostGIS, Tesseract\u2192TrOCR/IndicHTR, OpenCV\u2192YOLO/Detectron2 \u2014 same interfaces, no rewrites."),
]

S4 = [
    ("Proven feasible: ",
     "165 tests (168 on EC2) green; 26 docs incl. 5 real Bhulekh RoRs; Tesseract 5.5 verified with hin/ori packs."),
    ("Measured: ",
     "79\u201384% OCR on real scans; validation < 1 s/record; 15\u2013127 s/doc on a 2-vCPU box (10 s budget needs production hardware)."),
    ("Risk \u2014 garbled OCR: ",
     "script-routed second pass + confidence bands; anything < 70% goes to mandatory human review."),
    ("Risk \u2014 invented data: ",
     "prohibited-field contracts per doc type; reviewers, never the AI, close a record."),
    ("Risk \u2014 privacy: ",
     "decision support only \u2014 no ownership changes, no write-back to government systems without approval."),
]

S5 = [
    ("Revenue officers: ",
     "reviewer queue, one-click corrections captured as training data, approve/reject/escalate with full evidence."),
    ("Auditors & supervisors: ",
     "tamper-evident hash-chained trail with re-verify, MIS dashboard (accuracy, pendency, error stats, state-wise progress) plus CSV export."),
    ("Administration: ",
     "digitization % and review-completion tracked live; discrepancies flagged, never silently resolved."),
    ("Governance: ",
     "reliable digital records from legacy pages; transparent, data-driven land administration."),
    ("Reach: ",
     "Odisha 39-A, UP Khatauni, MP Khasra, Bihar Khatiyan profiles live; more states plug into the same profile system."),
]

S6 = [
    ("OCR & language: ",
     "Tesseract 5.5; spaCy NER; Hugging Face transformers (XLM-R, TrOCR); Indic language packs."),
    ("Vision & GIS roadmap: ",
     "YOLO / Detectron2 for layout; GeoServer + PostGIS for cadastral serving."),
    ("Government systems: ",
     "Bhulekh, BhuNaksha, IGR, LGD, DILRMP, LRMS \u2014 adapters contracted, awaiting live endpoints."),
    ("Statement & code: ",
     "SIH26018, Ministry of Rural Development; repo: https://github.com/fresherscomputersc-hash/BHOOMI."),
]

TITLE_TEXT = "Problem Statement ID SIH26018 | BhuSure \u2014 Intelligent Land Record Digitization and Validation System | Theme: Smart Automation | PS Category: Software | Team ID- | Team Shadow Slayers"


def _run_props(run):
    return {"name": run.font.name, "size": run.font.size,
            "bold": run.font.bold, "italic": run.font.italic}


def _apply(props, run, size=None, bold=None):
    if props.get("name"):
        run.font.name = props["name"]
    run.font.size = size or props.get("size")
    if bold is not None:
        run.font.bold = bold


def set_bullets(shape, items, size=BODY_SIZE):
    tf = shape.text_frame
    tf.clear()
    base = None
    for i, (lead, rest) in enumerate(items):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.level = 0
        if base is None:
            base = {}
        r1 = para.add_run()
        r1.text = lead
        _apply(base, r1, size=size, bold=True)
        r2 = para.add_run()
        r2.text = rest
        _apply(base, r2, size=size, bold=False)


def set_lines(shape, lines, size=None):
    tf = shape.text_frame
    first_props = None
    for para in tf.paragraphs:
        for r in para.runs:
            if r.text.strip():
                first_props = _run_props(r)
                break
        if first_props:
            break
    tf.clear()
    for i, line in enumerate(lines):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.level = 0
        r = para.add_run()
        r.text = line
        if first_props:
            _apply(first_props, r, size=size)


def shape_by(slide, name):
    for sh in slide.shapes:
        if sh.name == name:
            return sh
    raise KeyError(name)


def main() -> None:
    prs = Presentation(str(TEMPLATE))
    assert len(prs.slides._sldIdLst) == 7, "template slide count changed!"

    s1 = prs.slides[0]
    set_lines(shape_by(s1, "TextBox 9"), [
        "Problem Statement ID SIH26018",
        "Problem Statement Title - BhuSure: Intelligent Land Record Digitization and Validation System",
        "Theme - Smart Automation",
        "PS Category - Software",
        "Team ID -",
        "Team Shadow Slayers",
    ])

    bodies = {1: (TITLE_IDEA, S2), 2: (None, S3), 3: (None, S4), 4: (None, S5), 5: (None, S6)}
    for idx, (title, items) in bodies.items():
        s = prs.slides[idx]
        if title:
            tf = shape_by(s, "Title 1").text_frame
            props = _run_props(tf.paragraphs[0].runs[0])
            tf.clear()
            r = tf.paragraphs[0].add_run()
            r.text = title
            _apply(props, r)
        set_bullets(shape_by(s, "TextBox 8"), items)
        for sh in s.shapes:
            if sh.name.startswith("Oval") and sh.has_text_frame:
                sh.text_frame.paragraphs[0].runs[0].text = TEAM

    prs.save(str(OUT))
    check = Presentation(str(OUT))
    assert len(check.slides._sldIdLst) == 7
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB, 7 slides, structure untouched)")


if __name__ == "__main__":
    main()
