"""Prepped photo -> self-typing ASCII portrait in a terminal window. Plays once, then a soft scan-line loops."""
import numpy as np, cv2
from PIL import Image
from theme import *

COLS, W = 120, 360
KEEP_TOP = 0.76                    # keep top 76% of the cut-out (head + torso); 1.0 = full body
CW = W / COLS; LH = CW * 2.0
RAMP = " .,:;-=+*#%@"              # empty -> dense (dense = brighter on a dark background)
ROW_STEP, ROW_DUR, CH = 0.045, 0.55, 30

gray = Image.open("source-prepped.png").convert("L"); mask = Image.open("source-mask.png").convert("L")
keep = int(gray.height * KEEP_TOP)
gray, mask = gray.crop((0, 0, gray.width, keep)), mask.crop((0, 0, mask.width, keep))
rows = max(1, round(COLS * gray.height / gray.width / 2.0))
grid = lambda im, w, h: np.asarray(im.resize((w, h), Image.LANCZOS), dtype=float) / 255
g, m = grid(gray, COLS, rows), grid(mask, COLS, rows)
inside = m > 0.5
vals = np.sort(g[inside]); g = np.where(inside, np.searchsorted(vals, g) / max(len(vals), 1), 0)      # equalise tones
big = cv2.GaussianBlur(np.asarray(gray.resize((COLS * 3, rows * 3), Image.LANCZOS), dtype=np.float32), (0, 0), 1.2)
mag = np.hypot(cv2.Sobel(big, cv2.CV_32F, 1, 0), cv2.Sobel(big, cv2.CV_32F, 0, 1))
edge = np.asarray(Image.fromarray(mag).resize((COLS, rows), Image.BOX), dtype=float)
edge = np.clip(edge / (np.percentile(edge[inside], 92) + 1e-6), 0, 1)                                   # outlines
g = np.clip(0.55 * g + 0.75 * edge, 0, 1) ** 1.1

AH = round(rows * LH + 10); H = AH + CH
fs = CW / 0.6
defs = (f'<linearGradient id="ink" gradientUnits="userSpaceOnUse" x1="0" y1="{CH}" x2="0" y2="{H}">'
        f'<stop offset="0" stop-color="#f0f6fc"/><stop offset=".55" stop-color="#c9d1d9"/><stop offset="1" stop-color="{GREEN}"/></linearGradient>'
        f'<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{GREEN}" stop-opacity=".22"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="art"><rect x="0" y="{CH}" width="{W}" height="{AH}"/></clipPath>')
typed_at = 0.3 + rows * ROW_STEP + ROW_DUR
css = (f'.scan{{animation:scan 5.5s linear infinite {typed_at+1:.2f}s backwards}}'
       f'@keyframes scan{{0%{{transform:translateY({CH-50}px)}}100%{{transform:translateY({H}px)}}}}')
out = [open_svg(W, H, css, defs), chrome(W, "portrait.sh — sairaja@github")]
clips = []
for i in range(rows):
    t = 0.3 + i * ROW_STEP
    clips.append(f'<clipPath id="r{i}"><rect x="0" y="{CH+5+i*LH:.2f}" width="0" height="{LH:.2f}">'
                 f'<animate attributeName="width" from="0" to="{W}" dur="{ROW_DUR}s" begin="{t:.2f}s" fill="freeze"/></rect></clipPath>')
out.append("<defs>" + "".join(clips) + "</defs>")
out.append(f'<g class="m" style="font-size:{fs:.2f}px" fill="url(#ink)">')
for r in range(rows):
    s = "".join(" " if m[r, c] < 0.5 else RAMP[max(1, int(g[r, c] * (len(RAMP) - 1) + 0.5))] for c in range(COLS))
    if not s.strip(): continue
    xs = " ".join(f"{c*CW:.2f}" for c, ch in enumerate(s) if ch != " ")
    tx = esc("".join(ch for ch in s if ch != " "))
    out.append(f'<text clip-path="url(#r{r})" x="{xs}" y="{CH+5+r*LH+LH*0.78:.2f}">{tx}</text>')
out.append('</g>')
for r in range(rows):                                          # green block cursor riding the typing wave
    t = 0.3 + r * ROW_STEP
    out.append(f'<rect x="0" y="{CH+5+r*LH:.2f}" width="{CW*1.2:.2f}" height="{LH:.2f}" fill="{GREEN}" opacity="0">'
               f'<animate attributeName="opacity" values="0;.9;0" keyTimes="0;.1;1" dur="{ROW_DUR}s" begin="{t:.2f}s" fill="freeze"/>'
               f'<animate attributeName="x" from="0" to="{W}" dur="{ROW_DUR}s" begin="{t:.2f}s" fill="freeze"/></rect>')
out.append(f'<g clip-path="url(#art)"><rect class="scan" x="0" y="0" width="{W}" height="50" fill="url(#scan)"/></g></svg>')
open("ascii-portrait.svg", "w", encoding="utf-8").write("\n".join(out))
print("wrote ascii-portrait.svg", W, "x", H, f"({rows} rows)")
