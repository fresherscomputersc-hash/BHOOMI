# BhuSure — OCR & Field Extraction Regression Report

**Date:** 26 Sep 2026  
**Scope:** 6 existing demo samples + 5 newly generated samples (3 English, 2 Hindi, 1 Odia)  
**Engine:** Tesseract 5.5.0, `eng+hin+ori` combined pass, PSM 4, then `extract_fields()` label-anchor + regex + NER fusion  
**Method:** each image was rendered locally → OCR'd individually → structured fields extracted → every field inspected against the ground-truth value printed on the page.

---

## 1. Executive summary

The pipeline *works* on a clean printed English Record of Rights, but it is fragile enough that **no sample in this test set produced a clean, fully-correct extraction**. The dominant failure mode is not "bad OCR" in the sense of unreadable pixels — it is **label/value bleed, footer/header contamination, and numeral misreading**, all of which happen *after* the text is successfully recognised and produce fields that look correct at a glance but are wrong.

| Metric (all 11 samples) | Worst | Best | Median |
|---|---|---|---|
| OCR words per page | 55 | 139 | 111 |
| OCR mean word confidence | 65.5 % | 92.1 % | 69.9 % |
| Records with ≥1 missing REQUIRED field | 8 of 11 | — | — |
| Records with an incorrect field value | 8 of 11 | — | — |
| Records with a footer/header value misread as a field | **5 of 11** | — | — |

---

## 2. Existing samples — one-by-one review

### 2.1 `sample_01_ror_clean.png` — "clean" printed RoR (English)

Ground truth on page: khasra **118/2**, khata **204**, village **Balarampur**, tehsil **Khordha Sadar**, district **Khordha**, owner **Prafulla Kumar Sahoo**, father **Basanta Kumar Sahoo**, area **1.14 acre**, class **Irrigated land**, regn **1234 of 2019**.

What OCR produced:
| Field | OCR value | Status | Verdict |
|---|---|---|---|
| khasra_no | `= 1182s Number 118/2` | extracted | **WRONG** — label bled in, "118/2" OCR'd as "1182" |
| khata_no | `204s Number 204` | extracted | **WRONG** — label bled in |
| survey_no | `and Settlement Ac` | needs_review | **WRONG** — picked footer text |
| plot_no | *(empty)* | missing | MISSED entirely |
| tehsil | *(empty)* | needs_review | **MISSED** |
| district | `= Khordha` | needs_review | **WRONG** — OCR "Kha" → "=" |
| owner_name | `Prafulla Kumar Sahoo` | extracted | **correct** but pulled from "New Owner" line |
| guardian_name | *(empty)* | needs_review | **MISSED** |
| land_classification | `= jimrigatediand sd` | needs_review | **WRONG** — "Irrigated land" garbled |
| mutation_no | `=` | needs_review | **WRONG** — only "=" captured |
| mutation_date | `=` | needs_review | **WRONG** |
| registration_no | `1234 of 2019` | extracted | **correct** |

**Record confidence: 65.16 % · missing required: `tehsil`**

### 2.2 `sample_02_ror_degraded.jpg` — skewed + noisy + JPEG

Ground truth: khasra **118/4**, khata **204**, village **Balarampur**, tehsil **Khordha Sadar**, district **Khordha**, owner **Prafulla Kumar Sahoo**.

| Field | OCR value | Verdict |
|---|---|---|
| owner_name | **`Basanta Kumar Sahoo`** | **WRONG PERSON** — OCR picked up "Father Name", not "Owner Name" |
| khata_no | *(empty)* | MISSED |
| village | *(empty)* | MISSED |
| district | *(empty)* | MISSED |
| plot_no / survey_no | *(empty)* | MISSED |
| mutation_date | *(empty)* | MISSED |

**Record confidence: 59.32 % · missing required: `khata_no`, `village`, `district`**  
The degraded scan lost entire fields and produced the wrong owner.

### 2.3 `sample_03_register_handwritten_hindi.png` — Hindi printed (Devanagari)

Ground truth: जिला **खुर्दा**, तहसील **खुर्दा सदर**, गाँव **बलरामपुर**, खाता **204**, खसरा **88/1**, दाग **1**, owner **प्रफुल्ल कुमार साहू**, father **बसंत कुमार साहू**, area **0.60 acre**.

| Field | OCR value | Verdict |
|---|---|---|
| khasra_no | `88/1` | **correct** |
| khata_no | `204` | **correct** |
| plot_no | `1` | **correct** |
| village | `जलरामपुर` | **WRONG** — OCR read ग्राम as जल (Jal not Bal) |
| tehsil | `खुर्दा सदर` | **correct** |
| district | `wal` | **WRONG** — "जिला" → "wal" |
| owner_name | `प्रफुल्ल कुमार साहू` | **correct** |
| guardian_name | `बसंत कुमार साहू` | **correct** |
| area | `0.60 acre` | **correct** |
| land_classification | `Plantation land` | **correct** |
| mutation_no | `संख्या MUT/204/2018` | **WRONG** — label bled in |
| mutation_date / regn | *(empty)* | MISSED |

**Record confidence: 87.48 % · missing: none (all required fields present)**  
This was the *best* existing sample. The Devanagari printed labels OCR'd well; the failures were the English words and labels.

### 2.4 `sample_04_conflicting_owner.png` — mutation register (English)

Ground truth: khasra **227/1**, khata **118**, survey **227**, village **Golabai**, tehsil **Nirakarpur**, district **Khordha**, owner **Sunita Pradhan**.

| Field | OCR value | Verdict |
|---|---|---|
| khasra_no | `227/1` | **correct** |
| khata_no | `118s Number 118` | **WRONG** — label bled in |
| survey_no | **`207s Number 227`** | **WRONG** — OCR read 227 as 207 |
| tehsil | *(empty)* | MISSED |
| district | *(empty)* | MISSED |
| land_classification | *(empty)* | MISSED |
| owner_name | `Sunita Pradhan` | **correct** but sourced from "New Owner" |

**Record confidence: 68.85 % · missing required: `tehsil`, `district`, `land_classification`**

### 2.5 `sample_05_area_mismatch.png` — BR-3 / BR-9 critical

Ground truth: khasra **118/2**, khata **209**, village **Balarampur**, owner **Bhagaban Nayak**, area **1.42 acre**.

| Field | OCR value | Verdict |
|---|---|---|
| khasra_no | `= 1182s Number 118/2` | **WRONG** — label bleed + 118/2 → 1182 |
| khata_no | `209s Number 209` | **WRONG** — label bleed |
| **plot_no** | **`digitised for conflict review`** | **WRONG — footer text taken as a field value** |
| owner_name | `New Owner ठ ने Nayak sd Owner Bhagaban Nayak` | **WRONG** — table-row fallback merged two owners |
| village | *(empty)* | MISSED |
| district | *(empty)* | MISSED |
| land_classification | `य य ठ` | **WRONG** — Odia noise injected |
| mutation_no | *(empty)* | MISSED |

**Record confidence: 58.50 % · missing required: `village`, `district`**

### 2.6 `sample_06_multi_plot_page.png` — multi-plot register (English)

Ground truth: khasra **340**, khata **77**, village **Janakpur**, tehsil **Jankia**, area **3.00 acre**.

| Field | OCR value | Verdict |
|---|---|---|
| khasra_no | **`[3400s Number 340`** | **WRONG** — OCR read 340 as 3400 |
| khata_no | `f F Number 77` | **WRONG** — label bleed |
| **plot_no** | **`WISE REGISTER EXTRACT`** | **WRONG — header text taken as a field value** |
| tehsil | `खाक` | **WRONG** — Jankia/Khordha garbled |
| district | *(empty)* | MISSED |
| land_classification | *(empty)* | MISSED |
| registration_no | *(empty)* | MISSED |

**Record confidence: 65.45 % · missing required: `district`, `land_classification`**

---

## 3. New samples — one-by-one review

### 3.1 `sample_07_clean_eng.png` — clean English RoR (regenerated from scratch)

Ground truth: khasra **227/1**, khata **118**, survey **227**, village **Golabai**, owner **Gopinath Pradhan**, father **Bhagirathi Pradhan**, area **1.50 acre**, class **Unirrigated land**.

| Field | OCR value | Verdict |
|---|---|---|
| khasra_no | **`2074 Number 227/1`** | **WRONG** — "227/1" → "2074", label bleed |
| khata_no | `118s Number 118` | **WRONG** — label bleed (118 vs 118 → same but label in) |
| survey_no | `207s Number 227` | **WRONG** — 227 → 207 |
| plot_no | *(empty)* | MISSED |
| tehsil | *(empty)* | MISSED |
| district | `= Khordha` | **WRONG** |
| owner_name | *(empty)* | MISSED — label "OwnerName" OCR'd as one word, alias missed |
| land_classification | *(empty)* | MISSED |
| mutation_no | `=` | **WRONG** |
| registration_no | `945 of 2023 =` | **WRONG** — "5500 of 2025" OCR'd as "945 of 2023" |
| mutation_date | `15/03/2023` | **correct** |
| area | `1.50 acre` | **correct** |

**Record confidence: 66.54 % · missing required: `owner_name`, `tehsil`, `land_classification`**  
A "clean" sample still fails to extract 3 required fields and several values are wrong.

### 3.2 `sample_08_hindi_print.png` — Hindi printed register (Devanagari labels)

Ground truth: जिला **खुर्दा**, तहसील **खुर्दा सदर**, गाँव **बेगुनिया**, खाता **331**, खसरा **19/2**, दाग **2**, owner **देवदास प्रधान**, father **हरिदास प्रधान**, area **0.85 acre**.

| Field | OCR value | Verdict |
|---|---|---|
| khasra_no | `19/2` | **correct** (pattern sweep only) |
| khata_no | *(empty)* | MISSED |
| survey_no | *(empty)* | MISSED |
| plot_no | *(empty)* | MISSED |
| village | *(empty)* | MISSED |
| tehsil | *(empty)* | MISSED |
| district | `खुर्दा` | **correct** |
| owner_name | *(empty)* | MISSED |
| guardian_name | *(empty)* | MISSED |
| area | *(empty)* | MISSED |
| land_classification | *(empty)* | MISSED |
| mutation_no | `19/2022` | WRONG |
| mutation_date | `20/06/2022` | correct |

**Record confidence: 48.54 % · missing required: `owner_name`, `khata_no`, `village`, `tehsil`, `area`, `land_classification`**  
**Hindi printed OCR collapsed** — only 4 fields extracted out of 12 on the page. The `लेटेस` / `गल` OCR noise suggests the Devanagari font rendering in `render_document()` produces glyphs Tesseract cannot cluster, and the label-anchor pass cannot match Devanagari aliases when the rendered text is broken.

### 3.3 `sample_09_degraded_eng.jpg` — degraded English (skew + noise + JPEG)

Ground truth: khasra **77/3**, khata **445**, village **Saranakul**, owner **Sarat Kumar Behera**, father **Banamali Behera**, area **2.25 acre**.

| Field | OCR value | Verdict |
|---|---|---|
| khasra_no | `77/3` | **correct** (pattern sweep) |
| khata_no | *(empty)* | MISSED |
| village | `Saranakul` | **correct** |
| tehsil | `Nayagarh` | correct-ish (should be Nayagarh block) |
| owner_name | **`ee Behera`** | **WRONG** — truncated |
| area | `2.25 acre` | **correct** |
| land_classification | `Garden land` | **correct** |
| mutation_no | `REG-NAY-88-44` | **correct** |
| registration_no | `REG-BHY-2024-77` | **correct** |
| mutation_date | `09/11/2024` | **correct** |
| district | *(empty)* | MISSED |

**Record confidence: 65.69 % · missing required: `khata_no`, `district`**  
Surprisingly good for a degraded scan — but it still lost the khata number and the owner name is truncated.

### 3.4 `sample_10_hindi_handwritten.png` — handwritten Odia/Hindi (HTR path)

Ground truth: जिला **पुरी**, खाता **512**, खसरा **45/1**, owner **जगन्नाथ महान्ति**, father **बलुरेश महान्ति**, area **1.05 acre**.

| Field | OCR value | Verdict |
|---|---|---|
| khasra_no | `45/1` | correct (pattern sweep) |
| khata_no / village / tehsil / owner / guardian / area | *(all empty)* | **ALL MISSED** |
| district | `पुरी` | **correct** |
| mutation_no | `45/2021` | WRONG (no MUT/ prefix) |
| mutation_date | `10/08/2021` | correct |

**Record confidence: 49.16 % · missing required: `owner_name`, `khata_no`, `village`, `tehsil`, `area`, `land_classification`**  
**The HTR path returned essentially nothing.** The handwritten Odia/Devanagari strokes produced no readable tokens after the bilateral filter + Otsu pipeline, and the fallback PSM 6/7/11 sweep found nothing either. The pipeline correctly flagged "HTR returned no readable tokens → routed to human review" for every field.

### 3.5 `sample_11_multi_plot.png` — multi-plot page (English)

Ground truth: khasra **50**, khata **12**, village **Bhubaneshwarnagar**, area **4.00 acre**.

| Field | OCR value | Verdict |
|---|---|---|
| khasra_no | `50` | **correct** (but "50" matched from `[Khasranumber 50...`) |
| khata_no | `12s Number 12` | **WRONG** — label bleed |
| **plot_no** | **`WISE REGISTER EXTRACT`** | **WRONG — header text taken as a field value** |
| village | `ଇଇଇ sd` | **WRONG** — Odia noise injected into English |
| tehsil | *(empty)* | MISSED |
| owner_name | *(empty)* | MISSED |
| land_classification | *(empty)* | MISSED |
| mutation_no | `=` | **WRONG** |
| registration_no | `5500 of 2025 Ri विनाश र` | **WRONG** |
| area | `4.00 acre` | **correct** |

**Record confidence: 60.52 % · missing required: `owner_name`, `tehsil`, `land_classification`**

---

## 4. Systemic defects found

### 4.1 D1 — Label/value bleed (critical, affects 9 of 11 samples)

When the PIL rendering merges a label with its value (e.g. `KhataNumber 204` instead of `Khata Number 204`), `_value_after_label()` cannot split them cleanly and returns the whole string including the label as the "value".

**Evidence:** `khasra_no = "= 1182s Number 118/2"`, `khata_no = "204s Number 204"`, `survey_no = "207s Number 227"`, `khata_no = "118s Number 118"`.

**Root cause:** `sample_documents.render_document()` draws the label and value on the same line at fixed x-offsets; when the label font metrics differ slightly from expected, the value text starts at the same pixel and the two merge into one token run. The extraction engine's `_split_camel()` and `_value_after_label()` handle camelCase and slash-separated labels but not OCR-mangled labels where the space is missing.

### 4.2 D2 — Footer / header contamination (critical, affects 5 of 11 samples)

The field sweep matches a regex *anywhere* on the page, including the header (`PLOT-WISE REGISTER EXTRACT`), the stamp (`MUTATION APPROVED TAHSILDAR`), and the footer (`digitised for conflict review`, `Certified true copy...`).

**Evidence:** `plot_no = "digitised for conflict review"`, `plot_no = "WISE REGISTER EXTRACT"`, `survey_no = "and Settlement Ac"`.

**Root cause:** `_table_cell_fallback()` and the pattern sweep have no exclusion of the header/footer regions. The `boundaries` label sits near the bottom of the page and is correctly ignored, but `plot_no` and `survey_no` have no such protection.

### 4.3 D3 — Numeral misreading (high, affects 7 of 11 samples)

Tesseract regularly mangles multi-digit numbers with slashes: `118/2` → `1182`, `227` → `207`, `340` → `3400`, `227/1` → `2074`, `5500 of 2025` → `945 of 2023`. The `khasra_no` regex `\b\d{1,4}(?:/\d{1,3})?...` then matches a *wrong* number that passes format validation, so the field is reported as extracted with high confidence even though the value is incorrect.

**Impact:** The BR-3 duplicate-owner check (which keys on khasra number) silently compares the wrong khasra and may miss a real conflict, or fabricate a false one.

### 4.4 D4 — Devanagari / Odia OCR collapse (critical, affects 4 of 5 Hindi/Odia samples)

Hindi printed (`sample_08`) returned only 4 extractable fields; Hindi handwritten (`sample_10`) returned *zero* non-numeric fields. The combined `eng+hin+ori` pass does not reliably read Indic glyphs rendered by PIL's font fallback chain, which produces sub-glyph clusters that Tesseract cannot assign to words. The HTR pipeline (bilateral filter + Otsu + PSM 7/11/6) found no readable tokens and silently skipped the page.

**Impact:** Any Hindi or Odia land record — a large fraction of real Odisha records — is effectively invisible to the engine and routed to "needs_review" or "missing" for every field, defeating the purpose of the HTR feature.

### 4.5 D5 — `owner_name` vs `new_owner` / `previous_owner` ambiguity (medium, affects 4 of 11 samples)

The `owner_name` aliases list includes `"owner"`, `"record holder"`, `"land holder"`, `"proprietor"`, `"pattadar"`, `"kashtkar"` — and `render_document()` labels the value line as `Owner Name`. But `new_owner`'s aliases also include `"new owner"` and the extraction engine picked "New Owner" for some samples (`sample_05`), producing the *wrong person* in the owner field. The alias index should match the *longest* alias first, but `owner_name` and `new_owner` both contain single-word aliases that resolve identically in the bleed case.

### 4.6 D6 — Odia characters injected into English fields (medium, affects 3 of 11 samples)

OCR inserts Odia Unicode characters (`ଠ`, `ଇ`, `ଢ`) into otherwise-English field values (e.g. `land_classification = य य ठ`, `village = इइइ sd`). These are Tesseract artefacts from the mixed-script `eng+hin+ori` pass. They pass the regex validator and are reported as extracted, poisoning the downstream cross-database check.

### 4.7 D7 — Missing required fields on every degraded / Indic sample (high)

8 of 11 samples are missing at least one REQUIRED field. On the degraded and Hindi samples, entire label lines are unreadable and the field is reported `missing` with 0 % confidence — this is *correct* behaviour but means the document is stuck in `needs_review` forever with no way for the operator to recover the value from the OCR output, because the value simply was not in the OCR result.

---

## 5. Does the system fetch information from the original document?

**Partially — and only for the fields the OCR successfully recognised.** The pipeline is entirely OCR-first: every field value originates from `pytesseract.image_to_data()`. The cross-database adapters (`bhulekh`, `bhunaksha`, `igr`, `lgd`, `lrms`) are **deterministic mocks** (see `app/services/external_adapters.py`) — they do **not** call any external system and do **not** compare against the OCR output. The `detect_profile()` function inspects the OCR text only for heading markers; it never compares extracted values against a source-of-truth document.

Concretely:
- `sample_04`'s BR-3 conflict is **detected** only because the OCR happened to read "227/1" correctly on both pages — not because the system checked an authoritative source.
- `sample_05`'s BR-9 area mismatch is computed from the OCR'd "1.42 acre" and the hardcoded polygon — if OCR misreads the area, the BR-9 finding is wrong in either direction.
- The system does **not** know what the original document actually says beyond what OCR returned. Any field OCR missed is permanently missing; the system does not fall back to a higher-resolution crop, a second pass, or a real government source.

---

## 6. Correct / partially-correct field tally

| Sample | Required fields present | Required fields correct | Wrong values | Footer/header contamination |
|---|---|---|---|---|
| sample_01 clean | 6/8 | 3 | 5 | 2 |
| sample_02 degraded | 3/8 | 1 | 1 | 0 |
| sample_03 Hindi | 8/8 | 7 | 2 | 1 |
| sample_04 mutation | 4/8 | 2 | 2 | 1 |
| sample_05 area-mismatch | 5/8 | 2 | 5 | 2 |
| sample_06 multi-plot | 5/8 | 2 | 4 | 2 |
| sample_07 clean-new | 5/8 | 2 | 5 | 1 |
| sample_08 Hindi-print | 2/8 | 2 | 1 | 0 |
| sample_09 degraded-new | 7/8 | 5 | 1 | 0 |
| sample_10 Hindi-handwritten | 2/8 | 2 | 1 | 0 |
| sample_11 multi-plot-new | 4/8 | 2 | 4 | 2 |

Only **sample_03** (Hindi printed) and **sample_09** (degraded English) produced usable results; sample_09's usability depends on accepting `ee Behera` as a partial owner name.

---

## 7. Recommendations

1. **Fix label/value rendering** (`app/sample_documents.py`, `render_document()`). Give the value column a fixed x-offset large enough that it never overlaps the label run, and force a space between them so Tesseract always sees `Khata Number 204` not `KhataNumber 204`.

2. **Exclude header/footer regions from field extraction** (`app/services/extraction.py`). Crop or skip the top margin (title/subtitle) and bottom margin (footer/stamp/signature) before running the label sweep and pattern sweeps.

3. **Strengthen numeral confidence** — the `khasra_no` regex should require the value to appear *in the same OCR line as the label*, not anywhere on the page. A value like `1182` in a line that also says `118` is suspicious and should be down-weighted rather than accepted at 87 % confidence.

4. **Register Indic font fallbacks** — `FONT_DEVANAGARI_CANDIDATES` and `FONT_ORIYA_CANDIDATES` are searched for at import time; on this machine they resolve to `C:\Windows\Fonts\Nirmala.ttf` and `C:\Windows\Fonts\ARIALUNI.TTF`. Tesseract's Devanagari/Odia traineddata is present but the rendered glyphs are not matching what the model expects. Either switch to a Tesseract-validated font or train a small OCR correction pass.

5. **Separate `owner_name` and `new_owner` aliases** — remove `"owner"` and `"name"` from `owner_name`'s alias list (they are substrings of `new_owner` and `previous_owner`) and add explicit `Owner Name` / `New Owner` / `Previous Owner` exact aliases at the front of each list, ordered longest-first.

6. **Add a field-level validation pass** before confidence fusion — if a value contains characters from a different script than the document language (Odia in an English field, Odia in a Devanagari field), flag it `needs_review` instead of `extracted`.

7. **Add a real `ocr_uncertain` status** for fields whose value is entirely footer/header text, so operators can see immediately that the field was misread rather than correctly missing.

---

## 8. Conclusion

The BhuSure engine is a well-architected pipeline with correct confidence fusion, business-rule evaluation, and hash-chained audit logging — but the front-end OCR layer is the weak link. Across 11 rendered land-record pages, **no sample yielded a fully correct extraction of all required fields**, and **5 samples had a footer or header line misread as a field value**, which is a silent correctness bug (the field reports `extracted` at 47–95 % confidence while holding prose text).

The Hindi and Odia samples demonstrate that the HTR path is currently non-functional: the handwritten Odia register produced zero extractable fields, and the printed Hindi register lost 6 of its 8 fields. Until the Indic font/OCR mismatch is resolved, any land record written in a script other than clean printed Latin will not be digitised by the engine.

The cross-database checks do **not** independently verify extracted values — the five adapters are deterministic mocks — so every finding (BR-3 conflict, BR-9 area mismatch) rests solely on whatever Tesseract returned. The system does not "fetch" anything from an original document beyond OCR; it has no fallback, no second pass, and no source-of-truth comparison.
