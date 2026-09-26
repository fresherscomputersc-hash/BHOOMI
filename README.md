---
title: BhuVerify
emoji: 🗺️
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# BhuVerify

**Intelligent Land Record Digitization and Validation System**
Smart Hackathon problem statement **SIH26018** (Ministry of Rural Development) · Theme: Smart Automation · Team: **Shadow Slayers**

BhuVerify converts legacy land records — scanned registers, handwritten pages, PDFs and
cadastral maps — into structured, validated, GIS-linked digital records. It is not an OCR
wrapper: the pipeline runs computer-vision preprocessing, printed OCR and handwritten
recognition, structured field extraction with field-level confidence, ten named business
rules, duplicate detection, cross-database checks and cadastral linking, then hands the
result to a **government reviewer who holds final authority**. Every AI output and every
human correction is written to an immutable, hash-chained audit trail.

---

## PART 1 — What we have now (measured, not claimed)

### Pipeline (all stages live)

```
Document upload (FR-1)
      ↓
CV preprocessing + layout detection (FR-2)      OpenCV (deskew, denoise, CLAHE,
                                                table/handwriting/stamp/map regions)
      ↓
OCR / HTR with word-level confidence (FR-3)     Tesseract 5.5, eng+hin+ori packs,
                                                script-routed second pass (39-A→ori,
                                                Hindi profiles→hin, weak pages by vote)
      ↓
Structured field extraction (FR-4)              17 canonical fields, 5 doc profiles
      (generic, Odisha 39-A, UP Khatauni, MP Khasra, Bihar, Rajasthan),
      label aliases (Latin+Devanagari+Odia) + regex + NER-style scoring,
      optional verifiers: Groq LLM, spaCy NER, HF transformers (XLM-R)
      ↓
Field-level confidence fusion (FR-5)            0.45·OCR + 0.30·pattern + 0.15·proximity + 0.10·consistency
      ↓
GIS / cadastral linking (FR-9)                  Shapely, sample GeoJSON layer
      ↓
Business rule validation BR-1…BR-10 (FR-6/7)
      ↓
Cross-database verification (FR-8)              Bhulekh/BhuNaksha/IGR/LGD/LRMS adapters
                                                (deterministic mocks, live-ready contracts)
      ↓
Reviewer verification (FR-10)                   approve / reject / escalate (HTTP 409 blocks
                                                approval with open critical findings)
      ↓
Immutable audit trail (FR-12)                   SHA-256 hash chain + tamper detection
      ↓
MIS dashboard, search, APIs (FR-11/13/17)       measured accuracy, confidence bands,
                                                error fields, state-wise progress, CSV export
```

Stack: FastAPI · SQLAlchemy · OpenCV · Tesseract · Shapely · rapidfuzz · argon2 (+ opt-in: Groq API, spaCy, transformers/torch).
Frontend is vanilla JS with a hash router and no build step, so it runs unchanged in a
network-isolated environment. The map is rendered as inline SVG rather than pulling
Leaflet from a CDN.

### Measured results

| Metric | Figure | Evidence |
|---|---|---|
| Test suite | **165 tests local / 168 on EC2**, all green | `python -m pytest tests/ -q` |
| Documents exercised | 6 demo + 5 stress + 5 Hindi + 5 English + **5 real Bhulekh RoRs** (26 total) | `data/*/report_full.json` |
| Determinism | **15/15 docs byte-identical fields across reruns** (Groq-off core) | stability harness |
| Acceptance (adversarial set: 7° skew, handwriting, occlusion, 50–67% OCR) | **36.8% field accuracy**; 100% routed to review, 0 crashes, 0 hallucinated identifiers | `tools/acceptance.py` |
| Real Odisha Khatiyans (360–510 words, 79–84% OCR) | owners + person relations + parcel areas correct; BR-1 shrunk to classification-only | EC2 pilot records |
| Hindi profiles live | `up_khatauni`, `mp_khasra`, `bihar_khatiyan` fire incl. fuzzy match on mangled headings | EC2 pilot records |
| Verifier assists observed | Groq (gpt-oss-120b), spaCy NER, XLM-R NER fill fields regex misses | `source` column per field |
| Pipeline latency | 15–127 s/doc on 2 vCPU / 1 GB RAM box (SRS budget 10 s needs production hardware); validation < 1 s/record held | MIS performance panel |
| OCR stack verified | Tesseract 5.5.0, packs `eng+hin+ori+osd` | `/api/v1/system/status` |

### Requirement scorecard (SIH26018 clauses 7–15)

| # | Requirement | Now |
|---|---|---|
| 7 | Multilingual recognition | eng/hin/ori + script routing (60%) |
| 8 | Extraction from PDFs, images, historical docs | PDFs + images + degraded handling (75%) |
| 9 | Classification into predefined fields | 17 fields, 5 profiles, anti-hallucination gates (75%) |
| 10 | Rules + cross-db + duplicates | BR-1…BR-10 tested; govt links mocked (70%) |
| 11 | Confidence scoring + uncertain flags | fusion + bands + auto-review routing (90%) |
| 12 | Human verification workflow | queue → correct → approve/block → audit (90%) |
| 13 | Learning over time | corrections captured, not yet trained on (30%) |
| 14 | LRMS/DILRMP/GIS integration | live-ready contracts, mock data (35%) |
| 15 | Secure repo + metadata + audit | hash chain, RBAC, argon2 (70%) |
| — | Dashboards (all 7 asked panels) | live with real numbers (90%) |
| — | Government APIs | FastAPI + interactive docs (85%) |

**Overall ≈ 70% of the problem statement, with evidence for every point.**

---

## PART 2 — How we achieve the remaining 30%

| Gap | Achieve by | Needs |
|---|---|---|
| Live govt integrations (10, 14) | Swap each mock adapter for its read-only endpoint — contracts already match, callers unchanged | Department API access + approvals |
| Real learning loop (13) | Fine-tune NER/HTR on the accumulated reviewer-correction dataset; version models per record | GPU node + correction volume from pilot |
| More languages (7) | Same profile system: add Bengali/Tamil/Telugu/Marathi alias + marker packs | Language packs + sample docs |
| Production hardening (14, 15) | PostgreSQL + PostGIS HA, Redis/Celery queues, GPU pool, K8s, WORM audit log, SSO+MFA, backups, DR | Pilot → production funding |
| Latency budget (10 s/doc) | m7i-flex.large pilot (~$96/mo) → district scale; production lanes per above | Approved compute (AWS credits till Dec 2026) |

Swap contracts (prototype → production) — every row keeps its interfaces:

| Concern | Now | Production swap |
|---|---|---|
| Database | SQLite | PostgreSQL + PostGIS (change the connection URL) |
| Queue | In-process thread worker | Redis/Celery — stage names and status transitions already match |
| HTR | Tesseract + OpenCV chain | TrOCR / IndicHTR transformer — `WordToken` contract unchanged (TrOCR trialed; base model is Latin-only, Indic fine-tune needed) |
| NER assist | Regex primary, Groq/spaCy/XLM-R verifiers | Fine-tuned per-state models, same `source` column |
| Layout | OpenCV heuristics | YOLO / Detectron2 — `detect_layout` returns the same labelled boxes |
| External systems | Deterministic mocks | Read-only government APIs — `ExternalCheck` contract unchanged |
| Auth | Seeded accounts + argon2 tokens | Department SSO + MFA — routes only ever see a `User` |
| GIS | Sample GeoJSON + Leaflet-free SVG | GeoServer + PostGIS |

---

## Quick start

```bash
# system dependency
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-hin tesseract-ocr-ori

python3 -m pip install -r requirements.txt

uvicorn app.main:app --host 0.0.0.0 --port 8000
```

EC2 pilot tier (spaCy + transformers + Groq): see `requirements-ec2.txt`, `Dockerfile.ec2`
(set `SPACY_ENABLED=1 HF_ENABLED=1 GROQ_ENABLED=1 GROQ_API_KEY=...`).

Open <http://localhost:8000>. On first boot the app creates the schema, generates the six
sample documents and the cadastral layer, and runs each document through the full pipeline,
so you land on a populated reviewer queue.

Interactive API documentation: <http://localhost:8000/docs>

### Seeded accounts

| Username | Password | Role | Can |
|---|---|---|---|
| `operator` | `operator123` | Digitization Operator | upload, view queue |
| `reviewer` | `reviewer123` | Revenue Inspector | review, correct, approve/reject/escalate |
| `supervisor` | `supervisor123` | Tehsildar / Supervisor | dashboards, assign, export |
| `survey` | `survey123` | Survey Official | GIS and cadastral views |
| `auditor` | `auditor123` | Auditor | audit trail and reports |
| `admin` | `admin123` | Administrator | everything, incl. reseed |

---

## Demo walkthrough (10 minutes)

1. Sign in as `reviewer` → the queue is already populated.
2. Open the critical record (khasra 118/2) → try **Approve**. It is
   refused with HTTP 409 because a critical finding is open. That is the human-in-the-loop
   guarantee, enforced server-side rather than in the UI.
3. Open the clean record → correct the guardian name → **Save corrections**. The change is
   audit-logged with old and new values and added to the training dataset.
4. **Approve** it, then open **Audit Trail** and click *Re-verify chain now*.
5. Open **Cadastral Map** → click a red-outlined plot to see the BR-9 area disagreement.
6. Sign in as `supervisor` → **MIS Dashboard**: measured accuracy, confidence bands,
   top error fields, state-wise progress → export the CSV.
7. Open **Validation Rules** → run a dry-run against an ad-hoc record.

---

## Tests

```bash
python3 -m pytest tests/ -q
```

**165 tests locally (168 on EC2, where Tesseract-dependent tests also execute).** They cover:

- unit conversion and area normalisation across acre/hectare/decimal/bigha/katha/guntha/kanal/marla
- field extraction on official layouts (NIC table-ROR, Hindi ROR, khatauni tables):
  multi-pair line splitting, table-row owner/cell fallback, date-fragment
  rejection, ROR references, खेसरा/गाटा/रकबा/किसम aliases, honorific stripping,
  header-leak rejection (state/form words can never become values)
- Hindi-belt profiles (UP Khatauni/Gata, MP Khasra, Bihar Anchal, Rajasthan):
  state-gated detection with fuzzy fallback for OCR-mangled headings
- Odisha Schedule I Form 39-A contract: multi-page PDFs (admin+persons p1,
  parcels p2), hectare-format parcel areas (`8400 | 0.3399`), first-section area
  total, kisam-to-classification fallback, prohibited identifiers
  (plot 417 is not a khasra, khatiyan 18 is not a khata, case 4837/2025 is not
  a registration), praja person parser (ପି:/ସ୍ୱା:/ଜା:/ବା:), tax-prose rejection,
  per-field extracted/missing/needs_review status
- every one of BR-1 … BR-10, including the cases that must *not* fire
  (empty-khasra BR-2 guard, out-of-scope BR-7 routing)
- script-routed second-pass OCR (profile + decisive-majority vote, gated on weak base)
- layout: handwriting inside ruled tables detected; page borders never maps
- deskew accuracy verified against synthetic skews rather than assumed
- Groq/spaCy/HF verifier gates: never overwrite trusted values, never fill
  prohibited fields, pattern-validated suggestions only
- real OCR of the generated demo pages, with a latency assertion against the SRS budget
- GIS polygon areas reconciled against declared areas
- audit chain verification **and** tamper detection
- dashboard metrics (measured accuracy, bands, error fields, state rollup)
- timezone regression: naive SQLite timestamps must not crash the pending-review alerts
- API acceptance over HTTP (health, auth, RBAC, validation budget, upload guards)
- RBAC — including that an operator cannot read the audit trail

Determinism is asserted too: the 15-doc acceptance set reprocesses byte-identical
(`tools/acceptance.py`), and validation runs in under 1 s per record.

---

## Repository layout

```
app/
  main.py                 FastAPI app + static mount + boot seeding
  config.py               confidence bands, performance budgets, paths
  models.py               14 tables (SRS 6.1 core entities)
  security.py             argon2 hashing, opaque tokens, RBAC matrix
  master_data.py          Khordha tehsil/village master + Indic-script aliases
  sample_documents.py     renders the six demo register pages
  sample_geojson.py       builds the sample cadastral layer
  seed.py                 idempotent boot seeding + demo replay
  routers/                auth, documents, records, audit, map, dashboard, system
  services/
    cv_preprocess.py      FR-2
    ocr_service.py        FR-3
    extraction.py         FR-4, FR-5 (+ Hindi/39-A profiles)
    nlp_spacy.py          spaCy verifier (pilot, flag-gated)
    hf_transformer.py     XLM-R NER + TrOCR rescan (pilot, flag-gated)
    llm_groq.py           Groq LLM verifier (flag-gated)
    validation.py         FR-6, FR-7
    gis_service.py        FR-9
    external_adapters.py  FR-8 (mocks, live-ready contracts)
    worker.py             pipeline orchestration
    audit.py              FR-12 hash chain
    metrics.py            FR-13 (+ measured accuracy, state rollup)
    notifications.py      FR-15
static/                   console (index.html, css, js) — no build step
tests/                    165 tests (168 on EC2)
tools/                    stress-doc generators (Hindi/English/Odia), acceptance
                          scorer, EC2 ops harness, deck builder
requirements-ec2.txt      pilot tier (spacy, transformers, torch)
Dockerfile.ec2            pilot image (never used by render.yaml)
BhuVerify_SIH26018_Pitch_Deck.pptx   judge-facing deck (12 slides)
```

---

## Legal position

BhuVerify is decision support. It does not adjudicate disputes, does not change ownership,
and does not write back to Bhulekh, BhuNaksha, IGR or LRMS. Discrepancies are flagged, not
resolved. Every record requires approval by an authorised reviewer, and every correction is
audit-logged. Write-back would require formal government approval.
