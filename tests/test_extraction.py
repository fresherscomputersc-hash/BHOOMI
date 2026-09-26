"""Unit conversion and area normalisation (SRS FR-4 helper)."""
import pytest

from app.services.extraction import (
    _is_header_leak,
    _parcel_rows_39a,
    extract_fields,
    normalize_unit,
    parse_praja_section,
    to_hectare,
)


@pytest.mark.parametrize(
    "value,unit,expected",
    [
        (1.0, "hectare", 1.0),
        (1.0, "ha", 1.0),
        (1.0, "acre", 0.404686),
        (100.0, "decimal", 0.404686),
        (1.0, "bigha", 0.1011715),
        (1.0, "katha", 0.005058575),
        (1.0, "guntha", 0.01011715),
        (1.0, "kanal", 0.05058575),
        (1.0, "marla", 0.002529),  # to_hectare rounds to 6 decimals
        (0.75, "acre", round(0.75 * 0.404686, 6)),
    ],
)
def test_to_hectare_known_units(value, unit, expected):
    ha, ok = to_hectare(value, unit)
    assert ok is True
    assert ha == pytest.approx(expected, rel=1e-4)


def test_to_hectare_unknown_unit():
    ha, ok = to_hectare(1.0, "smoot")
    assert ok is False
    assert ha == 0.0


def test_normalize_unit_strips_noise():
    assert normalize_unit("Acres.") == "acres"
    assert normalize_unit("  HA ") == "ha"
    assert normalize_unit("decimal") == "decimal"


def test_normalize_unit_indic():
    assert normalize_unit("एकड़") == "एकड़"
    ha, ok = to_hectare(2.0, "एकड़")
    assert ok is True
    assert ha == pytest.approx(2 * 0.404686, rel=1e-4)


def test_table_row_with_date_does_not_crash():
    """Regression: _table_cell_fallback unpacked re.Match (stress_05 FAILED)."""
    text = (
        "Owner Name | Relation | Khasra No | Khata | Area\n"
        "1 Ramesh Sahoo | S/o Balaram | 118/2 | 204 | 1.50\n"
        "2 Minati Sahu | D/o Hari | 118/4 | 205 | 0.75 | 22/11/2020"
    )
    out = extract_fields(text, [], profile="generic")
    assert out.fields["khasra_no"].normalized_value in ("118/2", "118/4")
    assert "22/11" not in (out.fields["khasra_no"].normalized_value or "")


@pytest.mark.parametrize(
    "value,expected",
    [
        ("ଖତୟାନ ମୌଜା", True),
        ("ର ନାମ, ଜାତି ଓ ବାସସୁାନ", True),
        ("ନମର : 262", True),
        ("Khatanumber", True),
        ("Tehsil Jatni", True),
        ("Mouza Pipli", True),
        ("FAD", True),
        ("Cell Occluded Below", True),
        ("Balarampur", False),
        ("Khordha Sadar", False),
        ("Prafulla Kumar Sahoo", False),
        ("ଭଗବାନ ନାୟକ", False),
        ("ସ୍ୱା:ଉଦୟନାଥ ମହାପାତ୍ର", False),
    ],
)
def test_header_leak_gate(value, expected):
    assert _is_header_leak(value) is expected


def test_parcel_row_reads_hectare_format():
    rows = _parcel_rows_39a(["Plot 488 some text 8400 | 0.3399"])
    assert len(rows) == 1
    assert rows[0].khasra_no == "488"
    assert rows[0].area_unit == "hectare"
    assert rows[0].area_hectare == pytest.approx(0.3399)


def test_parcel_row_keeps_decimal_format():
    rows = _parcel_rows_39a(["Plot 220 area 19.00 decimal"])
    assert len(rows) == 1
    assert rows[0].area_unit == "decimal"


def test_parcel_area_fallback_uses_first_section():
    text = (
        "Schedule I Form No.39-A\n"
        "Plot 488 8400 | 0.3399\n"
        "ଖତିୟାନ ନମ୍ବର : 489\n"
        "Plot 489 0300 | 0.0121\n"
    )
    out = extract_fields(text, [], profile="odisha_khatiyan_39a")
    assert out.fields["area"].normalized_value == "0.3399"
    assert out.fields["area"].source == "parcel_row"
    assert out.fields["area"].confidence < 70.0  # review-bound


def test_person_parser_skips_tax_prose():
    lines = [
        "ପ୍ରଜାର ନାମ, ପିତାର ନାମ, ଜାତି ଓ ବାସସ୍ଥାନ",
        "ରକ୍ଷିତ ଖଜଣା ବିବରଣ, ମୋଟ ଖଜଣା",
    ]
    owners, _res = parse_praja_section(lines)
    assert owners == []
    lines2 = [
        "ପ୍ରଜାର ନାମ, ପିତାର ନାମ",
        "ଧନେଶ୍ୱର ବରାଳ ପି: ଚିନ୍ତାମଣି ବରାଳ, ଜା: ମହାଲାଏକ",
    ]
    owners2, _res2 = parse_praja_section(lines2)
    assert len(owners2) == 1
    assert owners2[0]["relation_type"] == "father"


def test_parcel_row_captures_kisam_word():
    rows = _parcel_rows_39a(["Plot 488 8400 | 0.3399 କୃଷି"])
    assert len(rows) == 1
    assert rows[0].kisam == "କୃଷି"


def test_classification_fallback_from_parcel_kisam():
    text = (
        "Schedule I Form No.39-A\n"
        "Plot 488 8400 | 0.3399 କୃଷି\n"
        "Plot 489 0300 | 0.0121 କୃଷି\n"
    )
    out = extract_fields(text, [], profile="odisha_khatiyan_39a")
    assert out.fields["land_classification"].normalized_value == "Agricultural land"
    assert out.fields["land_classification"].source == "parcel_row"
    assert out.fields["land_classification"].confidence < 70.0


def test_classification_fallback_majority_wins():
    text = (
        "Schedule I Form No.39-A\n"
        "Plot 488 8400 | 0.3399 କୃଷି\n"
        "Plot 489 0300 | 0.0121 ଘରବାରି\n"
        "Plot 490 0500 | 0.0202 ଘରବାରି\n"
    )
    out = extract_fields(text, [], profile="odisha_khatiyan_39a")
    assert out.fields["land_classification"].normalized_value == "Homestead land"


def test_classification_stays_missing_without_kisam():
    text = (
        "Schedule I Form No.39-A\n"
        "Plot 488 8400 | 0.3399\n"
    )
    out = extract_fields(text, [], profile="odisha_khatiyan_39a")
    assert out.fields["land_classification"].normalized_value == ""


def test_hindi_profiles_detected():
    from app.services.extraction import detect_profile, required_fields_for
    assert detect_profile("उत्तर प्रदेश खतौनी गाटा संख्या") == "up_khatauni"
    assert detect_profile("मध्य प्रदेश खसरा पटवारी") == "mp_khasra"
    assert detect_profile("बिहार जमाबंदी अंचल") == "bihar_khatiyan"
    assert detect_profile("राजस्थान जमाबंदी खसरा") == "rajasthan_jamabandi"
    assert detect_profile("Record of Rights") == "generic"
    assert "plot_no" in required_fields_for("up_khatauni")
    assert "khasra_no" in required_fields_for("mp_khasra")
    assert "khasra_no" not in required_fields_for("up_khatauni")


def test_gata_maps_to_plot_no():
    out = extract_fields("गाटा संख्या 118\nग्राम रामपुर", [], profile="up_khatauni")
    assert out.fields["plot_no"].normalized_value == "118"


def test_anchal_maps_to_tehsil():
    out = extract_fields("अंचल बिहारशरीफ\nजिला नालंदा", [], profile="bihar_khatiyan")
    assert out.fields["tehsil"].normalized_value == "बिहारशरीफ"


def test_honorific_stripped_from_owner():
    out = extract_fields("खातेदार का नाम श्री रमेश कुमार", [], profile="up_khatauni")
    assert out.fields["owner_name"].normalized_value == "रमेश कुमार"


def test_pati_alias_fills_guardian():
    out = extract_fields("पति का नाम मोहन प्रसाद", [], profile="bihar_khatiyan")
    assert out.fields["guardian_name"].normalized_value == "मोहन प्रसाद"


def test_khatauni_classifier_label():
    from app.services import extraction as ext
    out = ext.extract_fields(
        "उत्तर प्रदेश खतौनी\nगाटा संख्या 118\nग्राम रामपुर", [], profile="up_khatauni")
    doc_type, _c = ext.classify_document_type(out)
    assert doc_type == "up_khatauni"


def test_canonical_longest_alias_wins():
    from app.master_data import canonical_classification
    assert canonical_classification("Unirrigated land") == "Unirrigated land"
    assert canonical_classification("Irrigated land") == "Irrigated land"


@pytest.mark.parametrize(
    "value,expected",
    [
        ("RoR", True),
        ("Odisha", True),
        ("उत्तर प्रदेश", True),
        ("जगाबंदी", True),
        ("line deliberately absen", True),
        ("Biharsharif", False),
        ("Bhubaneswar", False),
    ],
)
def test_doc_word_leaks(value, expected):
    assert _is_header_leak(value) is expected


def test_mutation_sweep_rejects_word_fragment():
    out = extract_fields("Mutation Date 05/06/2021", [], profile="generic")
    assert out.fields["mutation_no"].normalized_value == ""


def test_registration_accepts_slash_form():
    out = extract_fields("Registration No 876/2021", [], profile="generic")
    assert out.fields["registration_no"].normalized_value == "876/2021"


def test_name_debris_stripped_before_scoring():
    out = extract_fields("Vendor = Anonymous Trust. s O Anonymous Trust",
                         [], profile="generic")
    val = out.fields["previous_owner"].normalized_value
    assert "=" not in val
    assert "[" not in val
    assert not [t for t in val.split() if len(t) == 1]


def test_fuzzy_profile_survives_mangled_heading():
    from app.services.extraction import detect_profile
    assert detect_profile("बिहार\nजगाबंदी\nअंचल") == "bihar_khatiyan"
    assert detect_profile("Record GAD FAD") == "generic"


def test_htr_degenerate_crop_returns_gracefully(tmp_path):
    from PIL import Image

    from app.services import ocr_service
    tiny = tmp_path / "sliver.png"
    Image.new("L", (200, 4), 128).save(tiny)
    result = ocr_service.run_htr(str(tiny))
    assert result.words == []
    assert result.warnings