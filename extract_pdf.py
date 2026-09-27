import fitz  # PyMuPDF
doc = fitz.open(r"ppt\reference ppt.pdf")
for i, page in enumerate(doc):
    text = page.get_text()
    print(f"=== PAGE {i+1} ===")
    print(text[:3000])
    print("...")