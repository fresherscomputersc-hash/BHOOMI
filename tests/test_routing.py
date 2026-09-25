"""Script-routing for the second OCR pass (Layer 1)."""
from types import SimpleNamespace

from app.services.worker import second_pass_language


def _words(*scripts):
    return [SimpleNamespace(text="w", script=s) for s in scripts]


def test_devanagari_majority_routes_hin():
    page = {"text": "खतौनी", "words": _words(*(["Devanagari"] * 8 + ["Latin"] * 2)),
            "language": "eng+hin+ori"}
    assert second_pass_language(page, "generic") == "hin"


def test_latin_page_needs_nothing():
    page = {"text": "Record of Rights", "words": _words(*(["Latin"] * 10)),
            "language": "eng+hin+ori"}
    assert second_pass_language(page, "generic") == ""


def test_39a_doc_routes_ori():
    page = {"text": "488 8400", "words": _words(*(["Latin"] * 6)),
            "language": "eng+hin+ori"}
    assert second_pass_language(page, "odisha_khatiyan_39a") == "ori"


def test_odia_majority_routes_ori():
    page = {"text": "ଖତିୟାନ", "words": _words(*(["Odia"] * 5 + ["Latin"] * 2)),
            "language": "eng+hin+ori"}
    assert second_pass_language(page, "generic") == "ori"


def test_hindi_profile_routes_hin_despite_garbage_tags():
    page = {"text": "जगाबंदी", "words": _words(*(["Odia"] * 5 + ["Latin"] * 2)),
            "language": "eng+hin+ori"}
    assert second_pass_language(page, "bihar_khatiyan") == "hin"
