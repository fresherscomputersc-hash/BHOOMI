from app.services.extraction import extract_fields
from app.services.ocr_service import WordToken

text = ("Ramesh Chandra Sahoo resides at Balarampur in Khordha district. "
        "Plot area 0.45 acre. Khasra number not readable.")
words = [WordToken(t, 80.0, {"x": 0, "y": 0, "w": 1, "h": 1}) for t in text.split()]
out = extract_fields(text, words)
print("before missing:", out.missing_required)
print("before low:", out.low_confidence_fields)

from app.services import nlp_spacy, hf_transformer
out, a1 = nlp_spacy.enhance_outcome(text, out)
print("spacy applied:", a1)
out, a2 = hf_transformer.enhance_outcome(text, out)
print("hf applied:", a2)
for f in ("owner_name", "village", "district"):
    e = out.fields[f]
    print(f, "->", repr(e.normalized_value), e.confidence, e.source)
