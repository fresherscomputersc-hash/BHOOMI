"""Script-routing for the second OCR pass (Layer 1)."""
from types import SimpleNamespace

from app.services.worker import second_pass_language


def _words(*scripts):
    return [SimpleNamespace(text="w", script=s, confidence=60.0) for s in scripts]


def _page(text, scripts, conf=60.0):
    return {"text": text,
            "words": [SimpleNamespace(text="w", script=s, confidence=conf)
                      for s in scripts],
            "language": "eng+hin+ori", "mean_confidence": conf}


def test_devanagari_majority_routes_hin():
    assert second_pass_language(
        _page("खतौनी", ["Devanagari"] * 8 + ["Latin"] * 2), "generic") == ("hin", "vote")


def test_latin_page_needs_nothing():
    assert second_pass_language(
        _page("Record of Rights", ["Latin"] * 10, conf=85.0), "generic") == ("", "")


def test_39a_doc_routes_ori():
    assert second_pass_language(
        _page("488 8400", ["Latin"] * 6), "odisha_khatiyan_39a") == ("ori", "profile")


def test_odia_majority_routes_ori():
    assert second_pass_language(
        _page("ଖତିୟାନ", ["Odia"] * 5 + ["Latin"] * 2), "generic") == ("ori", "vote")


def test_hindi_profile_routes_hin_despite_garbage_tags():
    assert second_pass_language(
        _page("जगाबंदी", ["Odia"] * 5 + ["Latin"] * 2), "bihar_khatiyan") == ("hin", "profile")


def test_strong_clean_page_skips_vote_pass():
    # A stray misread glyph must not trigger an extra pass on clean pages.
    assert second_pass_language(
        _page("Record of Rights", ["Latin"] * 9 + ["Odia"], conf=85.0),
        "generic") == ("", "")
