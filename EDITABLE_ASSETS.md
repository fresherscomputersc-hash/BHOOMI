# SOURCE / EDITABLE ASSETS — BHOOMI SIH 2026

All assets are real, editable, or programmatically generated from repository data. Nothing is fabricated.

## PPTX (Primary Deliverable)
- File: BHOOMI_SIH_2026_Final.pptx (1.2 MB, 6 slides, official SIH 2026 format)
- Format: Native PowerPoint (editable shapes, text, embedded images)
- Architecture diagrams: All native MSO_SHAPE nodes (rounded rectangles for services, cylinder for database, circles for decisions/users, thin rectangles for connectors/arrows). Fully editable within PowerPoint.
- Slides: Title, Proposed Solution, Technical Approach, Feasibility & Viability, Impact & Benefits, Research & References.

## PDF Preview
- File: BHOOMI_SIH_2026_Final.pdf (461 KB)
- Generated via PowerPoint automation (win32com) from the same source PPTX.

## Embedded Real Images (in PPTX)
- data/samples/sample_01_ror_clean.png — Real Odisha Record of Rights (clean scan). Embedded in slides 2, 3, 4.
- data/processed/page_annotated.png — Real OCR detection annotations (green bounding boxes + labels). Embedded in slide 3 (bottom right) and referenced in slide 4 evidence.
- assets/gis_map.png — Programmatically generated from data/geojson/sample_cadastral.geojson (actual parcel polygons: Balarampur, Golabai, Jankia, Pipli, Banapur, Tangi, Begunia). Embedded in slide 3 (GIS section) and referenced in slide 5 (impact/scalability).

## Source Code Assets (Architecture Source)
- build_final_ppt.py — Complete Python script that rebuilt the PPTX from scratch using python-pptx (editable/reproducible).
- generate_gis.py — Python script that generates assets/gis_map.png from actual GeoJSON.
- data/geojson/sample_cadastral.geojson — Real cadastral layer with 11 parcel features (properties include khasra_no, survey_no, plot_no, village, area_ha).

## Repository Evidence Files (Referenced in PPT and Claim Audit)
- README.md — Main source of all pipeline descriptions, measurement tables, requirement scorecard, legal position.
- app/services/ocr_service.py — Actual OCR/HTR implementation with word-level confidence.
- app/services/validation.py — Actual BR-1…BR-10 business rules.
- app/services/gis_service.py — Actual GIS linking and polygon area calculation.
- app/services/audit.py — Actual SHA-256 hash chain implementation.
- app/services/external_adapters.py — Actual mock adapter contracts (mode="mock", live-ready).
- app/services/extraction.py — Actual 17-field extraction with profile contracts.
- app/security.py — Actual argon2 + RBAC implementation.
- tests/ — 165/168 tests covering pipeline, validation, GIS, audit, API, routing.
- data/reports/extraction_analysis.json — Real demo extraction results.
- tools/acceptance.py — Adversarial test harness.

## Design Assets (Within PPTX — Editable)
- All architecture diagrams: Native PowerPoint shapes (not raster images). Users can click, resize, recolor, or edit any node, connector, or label directly in PowerPoint.
- Color palette: Deep institutional green (#1B3A2A), navy (#0F2847), gold (#BFA15F), light green-gray (#F0F5F0), alert red (#B4412D), success green (#2E7D4B). Consistently applied across all slides.
- Typography: Calibri family, 7–32pt range, clear hierarchy (titles 20pt+, section headings 14pt, body 8–9pt, captions 6–7pt).

## No Fabricated Assets
- No fake government logos, no fabricated partnership letters, no invented statistics charts, no stock photos presented as real UI screenshots.
- All charts/data references in the PPT are either real measured values (tests, documents, latency) or clearly labeled as demo/prototype/proposed.
