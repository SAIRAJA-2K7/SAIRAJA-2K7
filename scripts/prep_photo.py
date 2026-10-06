"""Photo -> clean grayscale cut-out for ASCII conversion.
Usage: python scripts/prep_photo.py source-photo.png
Outputs: source-prepped.png (grayscale) and source-mask.png (subject mask)."""
import sys, io
import numpy as np, cv2
from PIL import Image
from rembg import remove, new_session

src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.png"
img = Image.open(src).convert("RGB")
cut = remove(img, session=new_session("u2net"))   # small, fast model; RGBA with background removed
alpha = np.array(cut)[..., 3]
mask = (alpha > 128).astype(np.uint8) * 255
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))   # drop specks

ys, xs = np.where(mask > 0)
pad = int(0.04 * max(np.ptp(xs), np.ptp(ys)))
x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, mask.shape[1])
y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, mask.shape[0])

gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)      # local contrast
blur = cv2.GaussianBlur(gray, (0, 0), 2)
gray = cv2.addWeighted(gray, 1.8, blur, -0.8, 0)                            # unsharp mask

Image.fromarray(gray[y0:y1, x0:x1]).save("source-prepped.png")
Image.fromarray(mask[y0:y1, x0:x1]).save("source-mask.png")
print("saved source-prepped.png + source-mask.png", (x1 - x0, y1 - y0))
