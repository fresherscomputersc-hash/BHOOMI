# BHOOMI SIH 2026 — CLAIM AUDIT

Every claim in the presentation is backed by repository evidence. Never invented.

| CLAIM | SOURCE | IMPLEMENTATION STATUS | EVIDENCE | SLIDE |
|---|---|---|---|---|
| Problem Statement: SIH26018 (Land Record Digitization) | Official SIH 2026 template / README | Confirmed official | Template file + repo header | 1 |
| Team: Shadow Slayers | Official SIH 2026 template / README | Confirmed | Template + README line 14 | 1 |
| Theme: Smart Automation | Official SIH 2026 template / README | Confirmed | Template + README | 1 |
| End-to-end pipeline exists (upload → audit) | README section "Pipeline (all stages live)" | IMPLEMENTED | Code: app/main.py, services/* | 2 |
| Document upload (FR-1) | README / code | IMPLEMENTED | routers/documents.py | 2 |
| CV preprocessing + layout detection (FR-2) | README / code | IMPLEMENTED | services/cv_preprocess.py | 2, 3 |
| OCR / HTR with word-level confidence (FR-3) | README / code | IMPLEMENTED | services/ocr_service.py | 2, 3 |
| Script-routed second pass (39-A→Oriya, Hindi profiles→Hin) | README / code | IMPLEMENTED | ocr_service.py SCRIPT_BY_LANG + resolve_language | 2, 3 |
| Structured field extraction: 17 canonical fields, 5 doc profiles | README / code | IMPLEMENTED | services/extraction.py | 2, 3 |
| Multilingual: English / Hindi / Odia | README / services/ocr_service.py | IMPLEMENTED (prototype tier, 60-75%) | INSTALLED_LANGS check; Hindi + Odia packs verified | 2, 3 |
| Field-level confidence fusion formula (0.45·OCR + 0.30·Pat + 0.15·Prox + 0.10·Cons) | README / extraction.py | IMPLEMENTED | config settings + code references | 2, 3 |
| 10 named business rules BR-1…BR-10 | README / validation.py | IMPLEMENTED | RULE_CATALOG in services/validation.py | 2, 3, 4 |
| Duplicate detection (BR-3 / BR-7) | README / validation.py | IMPLEMENTED | rapidfuzz-based matching + master_data checks | 3, 4 |
| Cross-database verification (FR-8) | README / external_adapters.py | MOCK ADAPTER READY (contracts match live endpoints) | services/external_adapters.py (MODE = "mock"; contracts unchanged for swap) | 2, 3, 6 |
| GIS / cadastral linking (FR-9) | README / gis_service.py | IMPLEMENTED (sample GeoJSON layer + Shapely) | services/gis_service.py; data/geojson/sample_cadastral.geojson | 3, 5 |
| Human verification workflow (FR-10) | README / routers/records.py / audit.py | IMPLEMENTED (approve/reject/escalate + HTTP 409 block) | audit chain + review logic; demo walkthrough in README | 2, 4 |
| MIS dashboard (FR-11) | README / routers/dashboard.py | IMPLEMENTED | All 7 asked panels live with measured numbers | 5 |
| Audit trail (FR-12) | README / services/audit.py | IMPLEMENTED (SHA-256 chain + tamper detection) | audit.py: GENESIS + hash_payload + verify_chain() | 4, 6 |
| Government APIs (FastAPI interactive docs) | README / app/main.py | IMPLEMENTED | /docs endpoint; health endpoint returns Tesseract status | 6 |
| Secure repository + metadata (FR-15) | README / security.py | IMPLEMENTED (arg2 tokens + RBAC + hash chain) | security.py: argon2 + opaque tokens; audit chain; RBAC matrix | 4, 6 |
| 165 tests green locally / 168 on EC2 | README / tests/ | IMPLEMENTED (measured) | pytest output; 26 total docs tested; 15/15 byte-identical reruns | 4 |
| 79–84% OCR on real scans | README / data/reports/ | IMPLEMENTED (measured demo) | Real Odisha Khatiyan results in EC2 pilot records | 4 |
| 36.8% field accuracy on adversarial set (7° skew, handwriting, occlusion, 50-67% OCR) | README / acceptance.py | IMPLEMENTED (measured) | tools/acceptance.py + stability harness | 4 |
| Validation < 1 s/record; pipeline 15–127 s/doc | README / performance claims | MEASURED (prototype tier) | Tools/performance assertions; SRS budget 10 s needs production hardware | 4 |
| 26 documents exercised (6 demo + 5 stress + 5 Hindi + 5 English + 5 real Bhulekh RoRs) | README / data/ | IMPLEMENTED | File listing: data/uploads/, data/stress_*, data/samples/* | 4, 5 |
| Multilingual profiles: Odisha 39-A, UP Khatauni, MP Khasra, Bihar Khatiyan, Rajasthan | README / master_data.py / extraction.py | IMPLEMENTED (prototype) | master_data.py aliases; profile contracts verified | 2, 5 |
| Pilot AI tier: Groq LLM (gpt-oss-120b), spaCy NER, HF XLM-R — flag-gated verifiers | README / services/nlp_spacy.py / hf_transformer.py / llm_groq.py | ADAPTER READY (flag-gated; never overwrites trusted values) | Services with gate conditions; warm-up + pilot records | 2, 3 |
| TrOCR trial: base model reads Latin only — useless for Devanagari; parked pending Indic fine-tune | README / tools/check_trocr.py / trocr_trial.sh | PARTIALLY IMPLEMENTED (trialed, verdict: park) | Trial logs show Latin-only output; Indic fine-tune needed | 3, 6 |
| Before/After comparison shown visually | PPT design (slide 5) | VISUAL ONLY — no fabricated statistics | Icons + process arrows in PPT; based on actual pipeline stages | 5 |
| Impact: digitization %, review-completion tracked live | README / routers/dashboard.py | IMPLEMENTED (measured demo data) | Dashboard panels with real numbers; CSV export available | 5 |
| Scalability: SQLite → PostgreSQL + PostGIS; Tesseract → TrOCR/IndicHTR; same interfaces | README / architecture notes / services contracts | PROPOSED / ADAPTER READY | Every adapter contract unchanged; production architecture clearly separated from prototype in README section "How we achieve the remaining 30%" | 6 |
| Production architecture: K8s, GPU pool, Redis/Celery, GeoServer, SSO+MFA, WORM audit, DR | README section 2 / production swap table | PROPOSED (future funding dependent) | Clearly labeled as proposed in PPT and README; not portrayed as deployed | 6 |
| No ownership adjudication, no write-back to Bhulekh/BhuNaksha/IGR/LRMS without government approval | README / legal position / services/external_adapters.py | IMPLEMENTED (design principle + mock adapters only) | External adapters use MODE="mock"; no live endpoints connected; legal note in README and PPT footer | 4, 6 |
| Government integration: contracts match real endpoints, swap is one-line change per adapter | services/external_adapters.py / README | ADAPTER READY | Adapter function signatures match expected government APIs; contracts preserved | 2, 6 |
| Real screenshots embedded: clean RoR, annotated OCR, GIS cadastral layer | PPT / assets/ / data/ | REAL EMBEDDED ASSETS | data/samples/sample_01_ror_clean.png; data/processed/page_annotated.png; assets/gis_map.png (generated from geojson) | 3, 4, 5 |
| Architecture diagram: genuine service nodes, database cylinder, user icons, decision diamonds, flow arrows | PPT slide 3 (native PowerPoint shapes) | VISUAL ARCHITECTURE (editable shapes) | Built with MSO_SHAPE nodes, connectors, database cylinder, user role cards, security boundary — NOT text boxes | 3 |
| Pipeline diagram: visual flow document → preprocessing → layout → OCR → extraction → validation → verified record | PPT slide 3 (bottom section) | VISUAL PIPELINE (editable native shapes) | 8 horizontal stage nodes with connecting arrows and embedded screenshot evidence | 3 |
| GIS visual: parcel polygons (Balarampur / Golabai) with plot keys and area values | assets/gis_map.png (generated from data/geojson/sample_cadastral.geojson) | REAL GIS DATA VISUAL | Generated using matplotlib from actual GeoJSON features | 3, 5 |
| Audit chain visual: 3 linked record boxes with hash connections and tamper-detection label | PPT slide 4 (right column) | VISUAL DIAGRAM (editable) | Based on audit.py SHA-256 chain implementation | 4 |
| Security / audit / risk cards: color-coded severity with real mitigation descriptions | PPT slide 4 | EVIDENCE-BASED VISUAL | Based on actual code: security.py (argon2 + RBAC), validation.py (BR rules), audit.py (hash chain) | 4 |

# STATUS SUMMARY
- IMPLEMENTED: All pipeline stages, tests, extraction, validation rules, audit chain, dashboard, security (arg2 + RBAC), demo dataset, real screenshots, GIS layer.
- PARTIALLY IMPLEMENTED / ADAPTER READY: Pilot AI verifiers (Groq/spaCy/XLM-R) — flag-gated and never overwrite; TrOCR trialed but parked; government adapters mocked with live-ready contracts.
- PROPOSED: Production hardening (PostgreSQL + PostGIS HA, Redis/Celery, GPU pool, K8s, GeoServer, Department SSO+MFA, WORM audit, DR, backups).
- NEVER FABRICATED: No government partnerships, no government API access (mock only), no production deployment numbers, no unverified accuracy percentages presented as final metrics (36.8% adversarial is clearly labeled), no savings estimates, no adoption statistics.
