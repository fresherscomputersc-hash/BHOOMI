# SLIDE-BY-SLIDE SUMMARY  ·  BHOOMI_SIH_2026_Final.pptx

Total slides: 6 (official SIH 2026 format — includes title; instruction slide 7 deleted per template rules)

## SLIDE 1 — TITLE (Official Section 1)
- Core message: BHOOMI (BhuSure) — Intelligent Land Record Digitization & Validation for SIH26018 (Smart Automation, Software, Ministry of Rural Development) by Team Shadow Slayers.
- Visual used: Deep green header bar with gold accent; three-stage transformation icon flow (Legacy Record → BHOOMI Intelligence → Verified Digital Record); document + AI + map icons; team/repo footer.
- Evidence/source: Official SIH 2026 template fields; README header (problem statement ID, theme, team); repository link.
- Speaker note: "This is BHOOMI — not an OCR wrapper, but the full value chain from legacy paper to verified, GIS-linked digital records with government reviewers holding final authority."

## SLIDE 2 — PROPOSED SOLUTION / IDEA TITLE (Official Section 2)
- Core message: Before/After transformation pipeline — from scanned registers and handwritten pages to structured, validated, auditable digital records.
- Visual used: Left column = 4 legacy source cards (Scanned Register, Handwritten Page, PDF/Image, Cadastral Map); center = vertical pipeline with 8 stage nodes connected by arrows; bottom = embedded real clean document screenshot; right = 4 innovation cards (Multilingual OCR, Field Confidence, GIS Verification, Human-in-the-Loop).
- Evidence/source: README pipeline description; real document image (data/samples/sample_01_ror_clean.png); service contracts.
- Speaker note: "The pipeline runs live — upload through audit — with 17 canonical fields, 5 document profiles, 10 validation rules, and a reviewer who must approve before any record is finalized."

## SLIDE 3 — TECHNICAL APPROACH (Official Section 3)
- Core message: Native architecture diagram + AI processing pipeline + embedded evidence screenshots + technology stack.
- Visual used: TOP — vertical architecture layers (Sources → Ingestion → Document Intelligence → Validation → Review → Output) with service nodes, database cylinder, user role cards, security boundary; BOTTOM — horizontal AI pipeline (8 stages) with connector arrows + embedded clean document + annotated OCR result + technology chips.
- Evidence/source: All architecture nodes correspond to actual code modules (app/main.py, services/*); embedded screenshots from repository (clean RoR, annotated OCR); GIS map generated from actual geojson.
- Speaker note: "Every box is a real service — not marketing. The database cylinder represents SQLite (prototype) with PostgreSQL + PostGIS swap path. User roles enforce RBAC with argon2 tokens. The AI pipeline uses Tesseract 5.5 with script routing — not a black box."

## SLIDE 4 — FEASIBILITY & VIABILITY (Official Section 4)
- Core message: Evidence-based feasibility — measured results, real documents, tested rules, human-in-the-loop, security/audit, risk mitigation.
- Visual used: LEFT — 5 metric cards (165 tests, 26 docs, 79-84% OCR, 15/15 byte-ID, <1s/record); CENTER LEFT — embedded clean RoR document with annotation callouts; CENTER RIGHT — vertical human-in-the-loop workflow (6 stages from AI Extraction → Audit Log); RIGHT — audit chain visual (3 linked SHA-256 boxes) + 2 risk cards (Invented Data, Garbled OCR) with color-coded severity.
- Evidence/source: pytest results; data/reports/; services/validation.py (BR rules); services/audit.py (hash chain); services/security.py (RBAC); README performance claims clearly labeled.
- Speaker note: "No invented statistics. 165 tests green. The adversarial set — 7° skew, handwritten pages, occlusion, 50-67% OCR — produced 36.8% field accuracy, but 100% was routed to review with zero crashes. Every discrepancy is flagged, never silently resolved."

## SLIDE 5 — IMPACT & BENEFITS (Official Section 5)
- Core message: Before vs After transformation + impact dimensions for stakeholders + scalability timeline.
- Visual used: LEFT — Before column (red dots) vs After column (green dots) with matching process steps; RIGHT — 4 impact cards in 2x2 grid (Revenue Officers, Auditors & Supervisors, Administration, Governance) with icons; BOTTOM — scalability timeline (Phase 1 Prototype → Phase 4 Multi-state Scale).
- Evidence/source: Actual pipeline stages; dashboard functionality described in README; scalability architecture clearly separated as proposed (not deployed); legal position from README.
- Speaker note: "Impact is measured — digitization percentage tracked live, review completion rates available, discrepancies flagged. Scalability is architected: the same adapter contracts, same interfaces, swap SQLite for PostGIS, Tesseract for TrOCR, in-process workers for Celery/Redis."

## SLIDE 6 — RESEARCH & REFERENCES (Official Section 6)
- Core message: Verified references + adapter contracts + production swap architecture + roadmap timeline.
- Visual used: LEFT — 6 reference cards (SIH Problem Statement, Code & Repo, Document Intelligence, GIS & Cadastral, Government Systems, Security & Audit); CENTER — adapter layer diagram (BHOOMI Adapter Layer connected to 5 government systems with "MOCK · LIVE CONTRACT READY" labels) + database cylinder + security line; RIGHT — production swap cards (6 categories: Database, Queue, HTR Engine, Layout, Auth, GIS Serving) + 4-phase roadmap timeline.
- Evidence/source: Official SIH template; repository links; services/external_adapters.py contracts; README production architecture notes; geojson data.
- Speaker note: "Every government adapter is contracted but mocked — no fabricated government partnerships. The production swap path is clearly labeled as future work requiring pilot funding. This is credible, not aspirational fiction."

# DESIGN NOTES (not on slide, for presenter)
- Typography: Calibri/Aptos family, 7–32pt range, strong hierarchy (titles 20pt+, body 7–10pt, captions 6–8pt).
- Color system: Deep institutional green (#1B3A2A) primary, dark navy (#0F2847) secondary, warm gold (#BFA15F) accent, light green-gray (#F0F5F0) cards, white background. Red (#B4412D) only for discrepancy/alert, green (#2E7D4B) for success/approval.
- Architecture rules: All system diagrams built with native MSO_SHAPE nodes (rounded rectangles for services, cylinder for database, circles for users/decisions, thin rectangles for connectors/arrows). No floating disconnected text boxes. Directional arrows connect every stage.
- Screenshot rules: Real repository assets only — sample_01_ror_clean.png, page_annotated.png, assets/gis_map.png (generated from actual geojson). No fabricated UI screenshots.
- Text density: Each slide has 2–5 supporting points maximum; detailed explanations reserved for speaker notes / verbal defense.
