from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import re

SVG = Path("contrib-heatmap-exact.svg")
OUT = Path("contrib-ripple-slow.gif")
TEMP = Path("_capture.svg")

WIDTH = 912
HEIGHT = 226
FPS = 12
SECONDS = 16
SLOW = 2.0

svg = SVG.read_text(encoding="utf-8")

svg = svg.replace("pop 0.8s", f"pop {0.8*SLOW:.2f}s")
svg = svg.replace("ripple 5s", f"ripple {5*SLOW:.2f}s")
svg = svg.replace("sheen 7s", f"sheen {7*SLOW:.2f}s")

def slow_delay(m):
    a = float(m.group(1))
    b = float(m.group(2))
    return f"animation-delay:{a*SLOW:.2f}s,{b*SLOW:.2f}s"

svg = re.sub(
    r"animation-delay:([0-9.]+)s,([0-9.]+)s",
    slow_delay,
    svg
)

TEMP.write_text(svg, encoding="utf-8")

frames = []

with sync_playwright() as p:
    browser = p.chromium.launch()

    page = browser.new_page(
        viewport={
            "width": WIDTH,
            "height": HEIGHT
        },
        device_scale_factor=1
    )

    page.goto(TEMP.resolve().as_uri())
    page.wait_for_timeout(300)

    for i in range(FPS * SECONDS):
        frame = Path(f"_frame_{i:04d}.png")

        page.screenshot(
            path=str(frame),
            clip={
                "x": 0,
                "y": 0,
                "width": WIDTH,
                "height": HEIGHT
            },
            animations="allow"
        )

        frames.append(frame)
        page.wait_for_timeout(int(1000 / FPS))

    browser.close()

images = [
    Image.open(frame).convert("P", palette=Image.ADAPTIVE)
    for frame in frames
]

images[0].save(
    OUT,
    save_all=True,
    append_images=images[1:],
    duration=int(1000 / FPS),
    loop=0,
    optimize=False
)

for frame in frames:
    frame.unlink()

TEMP.unlink()

check = Image.open(OUT)

print()
print("===================================")
print(" FINAL CONTRIBUTION GIF CREATED")
print("===================================")
print("SIZE   :", check.size)
print("FRAMES :", check.n_frames)
print("FPS    :", FPS)
print("SPEED  :", f"{SLOW}x slower")
print("FILE   :", OUT)
print("===================================")
