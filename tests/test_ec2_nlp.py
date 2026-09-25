"""EC2 pilot passes: disabled-by-default, hallucination-guarded, no model needed."""
from app.services import hf_transformer, nlp_spacy
from app.services.extraction import FieldExtraction


def _outcome(fields, low=(), missing=(), profile="generic"):
    class O:
        pass
    o = O()
    o.fields = fields
    o.low_confidence_fields = list(low)
    o.missing_required = list(missing)
    o.profile = profile
    o.record_confidence = 50.0
    return o


def test_spacy_disabled_by_default_no_import():
    assert nlp_spacy.is_enabled() is False
    out = _outcome({"village": FieldExtraction("village", "Village")},
                   missing=["village"])
    _, applied = nlp_spacy.enhance_outcome("Village Balarampur", out)
    assert applied == []


def test_hf_disabled_by_default_no_import():
    assert hf_transformer.is_ner_enabled() is False
    assert hf_transformer.is_htr_enabled() is False
    assert hf_transformer.htr_rescan("nope.png") == {}
    out = _outcome({"village": FieldExtraction("village", "Village")},
                   missing=["village"])
    _, applied = hf_transformer.enhance_outcome("Village Balarampur", out)
    assert applied == []


def test_spacy_prohibited_never_filled():
    out = _outcome({"khasra_no": FieldExtraction("khasra_no", "Khasra No")},
                   missing=["khasra_no"], profile="odisha_khatiyan_39a")
    applied = nlp_spacy.apply_candidates(out, {"PERSON": ["417"], "GPE": []})
    assert applied == []


def test_hf_invalid_identifier_rejected():
    out = _outcome({"khasra_no": FieldExtraction("khasra_no", "Khasra No")},
                   missing=["khasra_no"])
    applied = hf_transformer.apply_candidates(
        out, {"PERSON": ["hello world"], "GPE": []})
    assert applied == []


def test_spacy_valid_person_fills_owner():
    out = _outcome({"owner_name": FieldExtraction("owner_name", "Owner")},
                   missing=["owner_name"])
    applied = nlp_spacy.apply_candidates(
        out, {"PERSON": ["Ramesh Chandra Sahoo"], "GPE": []})
    assert applied == ["owner_name"]
    assert out.fields["owner_name"].source == "spacy-ner"
    assert out.missing_required == []


def test_hf_high_confidence_never_overwritten():
    f = FieldExtraction("village", "Village", value="Balarampur",
                        normalized_value="Balarampur", confidence=95.0)
    out = _outcome({"village": f})
    applied = hf_transformer.apply_candidates(out, {"PERSON": [], "GPE": ["Jatni"]})
    assert applied == []
    assert out.fields["village"].normalized_value == "Balarampur"


def test_status_helpers_do_not_load_models():
    assert nlp_spacy.status()["loaded"] is False
    assert hf_transformer.status()["ner_loaded"] is False
