from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

SVG = Path("contrib-heatmap-exact.svg")
OUT = Path("contrib-ripple-slow.gif")

FPS = 12
SECONDS = 16
SLOW = 2.0

svg = SVG.read_text(encoding="utf-8")

svg = svg.replace("pop 0.8s", f"pop {0.8*SLOW:.2f}s")
svg = svg.replace("ripple 5s", f"ripple {5*SLOW:.2f}s")
svg = svg.replace("sheen 7s", f"sheen {7*SLOW:.2f}s")

import re

def slow_delay(match):
    a = float(match.group(1))
    b = float(match.group(2))
    return f"animation-delay:{a*SLOW:.2f}s,{b*SLOW:.2f}s"

svg = re.sub(
    r"animation-delay:([0-9.]+)s,([0-9.]+)s",
    slow_delay,
    svg
)

TEMP = Path("_slow_capture.svg")
TEMP.write_text(svg, encoding="utf-8")

frames = []

with sync_playwright() as p:
    browser = p.chromium.launch()

    page = browser.new_page(
        viewport={"width": 1200, "height": 800},
        device_scale_factor=1
    )

    page.goto(TEMP.resolve().as_uri())
    page.wait_for_timeout(500)

    svg_element = page.locator("svg")

    for i in range(FPS * SECONDS):
        frame = Path(f"_frame_{i:04d}.png")

        svg_element.screenshot(
            path=str(frame),
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

print("FINAL GIF CREATED")
print(f"File: {OUT}")
print(f"Frames: {len(images)}")
print(f"FPS: {FPS}")
print(f"Playback: {SLOW}x slower")
