"""Neofetch-style info card (height auto-matches the portrait). Edit ROWS, then: python scripts/make_info_card.py"""
import re
from theme import *

W = 520
try: H = int(re.search(r'height="(\d+)"', open("ascii-portrait.svg").read()).group(1))
except OSError: H = 454

# (key, value, key colour) -- an empty key continues the previous line
ROWS = [
    ("Name",       "Sairaja Krishna Meka", GREEN),
    ("Role",       "CSE undergrad · Full-stack developer", GREEN),
    ("Uni",        "KL University · B.Tech CSE '28 · GPA 8.94", GREEN),
    ("Location",   "Kakinada, Andhra Pradesh, IN", GREEN),
    ("Now",        "Building React + Spring Boot + MySQL apps", CYAN),
    ("Prev",       "Siemens Data Science Virtual Intern (AICTE)", CYAN),
    ("",           "YIIC 2.0 · Scaler · Certificate of Excellence", CYAN),
    ("Langs",      "C · Java · JavaScript · Python", ORANGE),
    ("Stack",      "React · Spring Boot · REST · MVC · CI/CD", ORANGE),
    ("Data",       "MySQL · PostgreSQL · MongoDB", ORANGE),
    ("Cloud",      "AWS EC2 · S3 · VPC", ORANGE),
    ("Projects",   "Urban-Tech Dashboard", PURPLE),
    ("",           "Citizen–Politician Interaction Platform", PURPLE),
    ("",           "IR Rover Bot Navigator (Arduino)", PURPLE),
    ("Highlights", "250+ CodeChef problems solved", YELLOW),
    ("",           "AWS Cloud Practitioner · Linguaskill B2", YELLOW),
    ("Fun fact",   "I optimize animations nobody asked for.", PINK),
]
KX, VX, TOP = 26, 134, 100
LH = min(19.5, (H - TOP - 66) / len(ROWS))
css = ".ln{animation:ln .6s ease-out backwards}@keyframes ln{from{opacity:0;transform:translateX(-12px)}}" + sheen_css(W, 7, 10)
d = lambda i: .4 + i * .11
o = [open_svg(W, H, css), chrome(W, "sairaja@github: ~"),
     f'<g class="ln"><text x="{KX}" y="58" class="m" style="font-size:13px"><tspan fill="{GREEN}" font-weight="bold">$</tspan> <tspan fill="{INK}">neofetch</tspan><tspan class="cur" fill="{INK}"> ▌</tspan></text></g>',
     f'<g class="ln" style="animation-delay:.35s"><text x="{KX}" y="80" class="m" style="font-size:13px;font-weight:bold" fill="{CYAN}">sairaja<tspan fill="{DIM}">@</tspan>SAIRAJA-2K7</text>'
     f'<text x="{KX}" y="92" class="m" style="font-size:13px" fill="{BORDER}">{"─"*34}</text></g>']
y = TOP + 10
for i, (k, v, c) in enumerate(ROWS):
    o.append(f'<g class="ln" style="animation-delay:{d(i):.2f}s"><text x="{KX}" y="{y:.1f}" class="m" style="font-size:13px">'
             f'<tspan fill="{c}" font-weight="bold">{esc(k)}</tspan><tspan x="{VX}" fill="{INK}">{esc(v)}</tspan></text></g>')
    y += LH
sw = [PINK, ORANGE, YELLOW, GREEN, CYAN, "#58a6ff", PURPLE, INK]
o.append(f'<g class="ln" style="animation-delay:{d(len(ROWS)+1):.2f}s">' + "".join(
    f'<rect x="{KX+j*26}" y="{y+2:.1f}" width="22" height="12" rx="3" fill="{c}"/>' for j, c in enumerate(sw)) + '</g>')
o.append(sheen_layer(H) + "</svg>")
open("info-card.svg", "w", encoding="utf-8").write("".join(o))
print("wrote info-card.svg", W, "x", H, "| last y", round(y + 14))
