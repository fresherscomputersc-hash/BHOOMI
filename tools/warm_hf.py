import os
os.environ.setdefault("HF_HUB_OFFLINE", "0")
from app.config import settings
print("model:", settings.hf_ner_model)
from transformers import pipeline
pipe = pipeline("token-classification", model=settings.hf_ner_model,
                aggregation_strategy="simple")
out = pipe("Ramesh Chandra Sahoo lives in Balarampur village")
print("hf-ner-ok", [(e["word"], e["entity_group"], round(e["score"], 2)) for e in out][:6])
