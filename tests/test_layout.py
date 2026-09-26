"""Layout region labelling: handwriting inside tables, no border-maps."""
import numpy as np
from PIL import Image, ImageDraw

from app.services.cv_preprocess import _detect_map_regions, detect_layout


def _ruled_page():
    import cv2
    W, H = 900, 700
    img = Image.new("L", (W, H), 245)
    d = ImageDraw.Draw(img)
    d.rectangle([20, 20, W - 20, H - 20], outline=60, width=3)
    rng = np.random.RandomState(7)
    for y in range(120, H - 60, 60):
        d.line([(40, y), (W - 40, y)], fill=90, width=2)
    for x in (60, 420):
        d.line([(x, 100), (x, H - 60)], fill=90, width=2)
    for i in range(8):
        y0 = 130 + i * 60
        pts = [(80 + x, y0 + int(6 * np.sin(x / 18.0 + i))) for x in range(0, 300, 8)]
        d.line(pts, fill=40, width=1)
    arr = np.array(img)
    _, binary = cv2.threshold(arr, 180, 255, cv2.THRESH_BINARY)
    return binary, arr


def test_handwriting_inside_table_is_detected():
    binary, gray = _ruled_page()
    lay = detect_layout(binary, gray, None)
    assert lay["counts"]["handwritten_text"] >= 1


def test_page_border_is_not_a_map():
    binary, gray = _ruled_page()
    boxes = _detect_map_regions(255 - binary, gray)
    assert all(b["w"] * b["h"] <= 0.9 * gray.shape[1] * gray.shape[0]
               for b in boxes)
    lay = detect_layout(binary, gray, None)
    assert lay["counts"]["map"] == 0


def test_clean_print_has_no_hand_boxes():
    import cv2
    from PIL import ImageFont
    img = Image.new("L", (900, 400), 250)
    d = ImageDraw.Draw(img)
    try:
        fnt = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 30)
    except OSError:
        fnt = ImageFont.load_default()
    for i, line in enumerate(["Record of Rights", "Village Balarampur",
                              "Khasra Number 118/2", "Owner Prafulla Sahoo"]):
        d.text((70, 60 + i * 70), line, font=fnt, fill=20)
    arr = np.array(img)
    _, binary = cv2.threshold(arr, 180, 255, cv2.THRESH_BINARY)
    lay = detect_layout(binary, arr, None)
    assert lay["counts"]["handwritten_text"] == 0
