# FINAL RISKS — BHOOMI SIH 2026 PRESENTATION

These are explicitly identified gaps, mocked/proposed features, or areas where a skeptical jury member might challenge the claim. All are addressed honestly in the presentation.

## 1. GOVERNMENT INTEGRATIONS (Mock / Adapter-Ready Only)
- Risk: Jury asks whether BhuSure connects to live government APIs (Bhulekh, BhuNaksha, IGR, LRMS).
- Status: MOCK adapters only. Contracts match live endpoints; swap is a one-line change per adapter. No government approval or live endpoint access has been obtained.
- Evidence: services/external_adapters.py (MODE = "mock"); README section 2 table; PPT slide 6 adapter diagram clearly labeled.
- Mitigation in PPT: Clearly labeled "MOCK · LIVE CONTRACT READY" on every adapter card and architecture node.

## 2. PILOT AI TIER (Partially Implemented / Flag-Gated)
- Risk: Jury asks whether Groq LLM, spaCy NER, and HF XLM-R verifiers are production-ready.
- Status: ADAPTER READY / FLAG-GATED. They never overwrite trusted values; only suggest corrections when regex misses fields. Models require GPU for production-scale deployment.
- Evidence: services/nlp_spacy.py, hf_transformer.py, llm_groq.py; README pilot notes; PPT technology cards labeled as pilot.
- Mitigation in PPT: Technology stack cards clearly distinguish prototype tier (FastAPI, SQLite, Tesseract) from pilot tier (Groq, spaCy, XLM-R, PostGIS, Celery) — color-coded.

## 3. TrOCR / INDIC HTR (Parked — Trial Failed for Devanagari)
- Risk: Jury asks about handwritten recognition capability.
- Status: TrOCR base model reads Latin only — useless for Devanagari/Odia handwriting. Parked pending Indic fine-tune.
- Evidence: tools/check_trocr.py, trocr_trial.sh, README trial verdict; PPT architecture notes.
- Mitigation in PPT: Pipeline shows "Tesseract 5.5 + OpenCV handwriting chain (prototype)" with "Pilot upgrade: TrOCR / IndicHTR" clearly labeled as future.

## 4. LATENCY BUDGET (10 s/doc Target Not Met in Prototype)
- Risk: Jury asks whether the system meets production latency requirements.
- Status: Prototype runs 15–127 s/doc on 2 vCPU / 1 GB RAM. The 10 s budget requires production hardware (m7i-flex.large or GPU nodes).
- Evidence: README performance section; config settings; PPT slide 4 metric card shows both measured latency and budget note.
- Mitigation in PPT: Metric card clearly says "15–127 s/doc on 2-vCPU box (SRS budget 10 s needs production hardware)" — no false claim.

## 5. MULTILINGUAL SUPPORT (Prototype Tier Limited to 3 Languages)
- Risk: Jury asks about Bengali, Tamil, Telugu, Marathi, Gujarati support.
- Status: Only English, Hindi, and Odia packs installed and verified. More languages plug into the same profile system but require language packs + sample docs.
- Evidence: INSTALLED_LANGS in ocr_service.py; master_data.py aliases; README gap table.
- Mitigation in PPT: Pipeline shows "eng+hin+ori" explicitly; innovation card says "English · Hindi · Odia" with "Script-routed second pass" — no claim of universal language support.

## 6. PRODUCTION DEPLOYMENT (Not Deployed)
- Risk: Jury asks whether this is a deployed production system or a prototype.
- Status: PROTOTYPE only. Deployed as Docker container (Dockerfile.ec2 for pilot tier). No state-level or district-level deployment exists.
- Evidence: README quick start; Dockerfile; render.yaml; PPT scalability timeline clearly separates Phase 1 (Prototype) from Phase 2–4 (Pilot / Integration / Scale) as proposed.
- Mitigation in PPT: Title and every architecture note distinguish "prototype tier" from "production architecture"; footer note clearly states "decision support only — does not adjudicate disputes, does not change ownership, does not write back to government systems without approval."

## 7. DATA STATISTICS (Demo Data Only)
- Risk: Jury asks if accuracy/statistics represent real government-scale data.
- Status: DEMO DATA. Metrics derived from 26 test documents (demo + stress + real Bhulekh RoRs), not a full district or state dataset.
- Evidence: README measurement table; PPT slide 4 metric cards clearly describe document count and source.
- Mitigation in PPT: No percentage claimed as universal — 79–84% OCR specified for "real Odisha scans"; 36.8% adversarial clearly labeled; 165 tests clearly described.

## 8. NO GOVERNMENT PARTNERSHIP / CERTIFICATION / PATENT CLAIMED
- Status: NONE CLAIMED. The PPT does not state any government approval, certification, patent, award, or production contract.
- Evidence: Absence of such claims verified by claim audit table; PPT footer explicitly states prototype status.
- This is a strength, not a weakness — credibility is preserved by not inventing partnerships.
