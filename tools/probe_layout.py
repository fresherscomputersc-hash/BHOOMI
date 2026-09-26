import numpy as np, cv2
from app.services.cv_preprocess import detect_layout, _detect_map_regions
from PIL import Image, ImageDraw

# ruled register page: border + table grid + thin wavy "handwriting"
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
lay = detect_layout(binary, arr, None)
print("counts:", lay["counts"])
print("map boxes:", [(b["x"], b["y"], b["w"], b["h"]) for b in lay["regions"] if b["label"] == "map"])
print("hand boxes:", len([b for b in lay["regions"] if b["label"] == "handwritten_text"]))
