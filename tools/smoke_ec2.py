import spacy, transformers, torch
print("spacy", spacy.__version__)
print("transformers", transformers.__version__)
print("torch", torch.__version__)
n = spacy.load("en_core_web_sm")
print("spacy-model-ok", [(e.text, e.label_) for e in n("Ramesh Chandra Sahoo lives in Balarampur").ents])
import app.services.nlp_spacy as s, app.services.hf_transformer as h
print("lazy-status-ok", s.status()["enabled"], h.status()["ner_enabled"])
