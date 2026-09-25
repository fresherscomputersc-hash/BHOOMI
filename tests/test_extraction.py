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
