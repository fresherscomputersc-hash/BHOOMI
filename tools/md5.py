import hashlib
for f in ["app/services/worker.py", "app/services/cv_preprocess.py",
          "app/services/ocr_service.py", "app/services/extraction.py"]:
    print(hashlib.md5(open(f, "rb").read()).hexdigest(), f)
