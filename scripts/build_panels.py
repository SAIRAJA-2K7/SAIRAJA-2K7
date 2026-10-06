"""Builds hero.svg, tech-stack.svg, projects.svg, highlights.svg, footer.svg  ->  python scripts/build_panels.py"""
import textwrap
from theme import *

W = 880
def save(name, parts):
    open(name, "w", encoding="utf-8").write("".join(parts) + "</svg>")
    print("wrote", name)

# ───────────────────────── HERO ─────────────────────────
def hero():
    H = 150
    PHRASES = ["Full-stack developer · React · Spring Boot · MySQL",
               "CSE undergrad @ KL University · GPA 8.94",
               "250+ problems solved on CodeChef",
               "AWS Cloud Practitioner · Cloud-curious"]
    PITCH, FS, SLOT, TYPE, HOLD, ERASE, X0, Y = 9.6, 16, 3.8, 1.5, 1.4, .6, 52, 118
    T = SLOT * len(PHRASES)
    defs = (f'<linearGradient id="ng" gradientUnits="userSpaceOnUse" x1="30" y1="0" x2="430" y2="0" spreadMethod="reflect">'
            f'<stop offset="0" stop-color="{GREEN}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/>'
            '<animateTransform attributeName="gradientTransform" type="translate" values="0 0;800 0" dur="9s" repeatCount="indefinite"/></linearGradient>')
    p = [open_svg(W, H, sheen_css(W, 7, 10), defs)]
    p.append(f'<text x="30" y="38" class="m fade" fill="{DIM}">~ $ <tspan fill="{GREEN}">whoami</tspan></text>')
    p.append(f'<text x="30" y="84" class="s in" style="font-size:38px;font-weight:800;letter-spacing:-.5px;animation-delay:.2s" fill="url(#ng)">Sairaja Krishna Meka</text>')
    p.append(f'<text x="30" y="{Y}" class="m fade" style="font-size:{FS}px;animation-delay:.6s" fill="{GREEN}">▸</text>')
    clips, texts, ev = [], [], [(0, 0)]
    for i, ph in enumerate(PHRASES):
        full = len(ph) * PITCH + 4
        t0 = i * SLOT / T; t1 = t0 + TYPE / T; t2 = t1 + HOLD / T; t3 = t2 + ERASE / T
        kt = [t1, t2, t3, 1] if i == 0 else [t0, t1, t2, t3, 1]
        vals = [full, full, 0, 0] if i == 0 else [0, full, full, 0, 0]
        kt = [0] + kt; vals = [0] + vals
        clips.append(f'<clipPath id="k{i}"><rect x="{X0-2}" y="{Y-20}" width="0" height="28">'
                     f'<animate attributeName="width" begin="1s" dur="{T}s" repeatCount="indefinite" '
                     f'keyTimes="{";".join(f"{k:.4f}" for k in kt)}" values="{";".join(f"{v:.1f}" for v in vals)}"/></rect></clipPath>')
        xs, tx = glyphs(ph, X0, PITCH)
        texts.append(f'<text x="{xs}" y="{Y}" class="m" style="font-size:{FS}px" fill="{INK}" clip-path="url(#k{i})">{tx}</text>')
        ev += [(t0, 0), (t1, len(ph) * PITCH), (t2, len(ph) * PITCH), (t3, 0)]
    ev.append((1, 0))
    p.append("<defs>" + "".join(clips) + "</defs>" + "".join(texts))
    p.append(f'<rect y="{Y-17}" width="9" height="22" fill="{GREEN}" class="cur"><animate attributeName="x" begin="1s" dur="{T}s" repeatCount="indefinite" '
             f'keyTimes="{";".join(f"{t:.4f}" for t, _ in ev)}" values="{";".join(f"{X0+x:.1f}" for _, x in ev)}"/></rect>')
    # ripple rings (the signature motif)
    p.append('<g clip-path="url(#pc)">')
    for k in range(4):
        p.append(f'<circle cx="790" cy="75" r="6" fill="none" stroke="{GREEN}" stroke-width="1.5" opacity="0">'
                 f'<animate attributeName="r" values="6;95" dur="4.8s" begin="{k*1.2}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values=".55;0" dur="4.8s" begin="{k*1.2}s" repeatCount="indefinite"/></circle>')
    p.append(f'<circle cx="790" cy="75" r="5" fill="{GREEN}"><animate attributeName="opacity" values="1;.4;1" dur="2.4s" repeatCount="indefinite"/></circle></g>')
    p.append(sheen_layer(H)); save("hero.svg", p)

# ───────────────────────── TECH STACK ─────────────────────────
def stack():
    ROWS = [("Languages", ORANGE, ["C", "Java", "JavaScript", "Python"]),
            ("Frontend",  CYAN,   ["HTML", "CSS", "React", "JSP"]),
            ("Backend",   GREEN,  ["Spring Boot", "REST APIs", "MVC"]),
            ("Databases", PURPLE, ["MySQL", "PostgreSQL", "MongoDB"]),
            ("Cloud/DevOps", YELLOW, ["AWS EC2", "AWS S3", "AWS VPC", "Git", "CI/CD"]),
            ("Core CS",   PINK,   ["DSA", "OOP in Java", "Operating Systems", "Computer Networks", "System Programming"]),
            ("Tools",     "#8b949e", ["IntelliJ IDEA", "VS Code", "Eclipse", "Power BI", "Fusion 360", "Arduino IDE", "Tinkercad"])]
    RH, TOP = 36, 56
    H = TOP + len(ROWS) * RH + 14
    p = [open_svg(W, H, sheen_css(W, 8, 11)), chrome(W, "stack.sh --list --all")]
    n = 0
    for r, (cat, col, items) in enumerate(ROWS):
        y = TOP + r * RH
        p.append(f'<text x="26" y="{y+3}" class="m in" style="font-weight:bold;animation-delay:{.2+r*.08:.2f}s" fill="{col}">{esc(cat)}</text>')
        x = 168
        for it in items:
            w = len(it) * 7.1 + 24
            d = .35 + n * .045; n += 1
            p.append(f'<g class="pop" style="animation-delay:{d:.2f}s"><rect x="{x:.1f}" y="{y-14}" width="{w:.1f}" height="26" rx="13" fill="{col}" fill-opacity=".10" stroke="{col}" stroke-opacity=".45"/>'
                     f'<text x="{x+w/2:.1f}" y="{y+3.5}" text-anchor="middle" class="m" style="font-size:11.5px" fill="{col}">{esc(it)}</text></g>')
            x += w + 10
    p.append(sheen_layer(H)); save("tech-stack.svg", p)

# ───────────────────────── PROJECTS ─────────────────────────
def projects():
    CARDS = [("Urban-Tech Dashboard", "Smart-city monitoring", GREEN,
              "Web dashboards to monitor and interact with utilities and city services. Optimized rendering and resource loading.",
              ["HTML", "CSS", "JavaScript", "Spring Boot", "MySQL"], "40% faster page loads"),
             ("Citizen–Politician Platform", "Civic issue tracking", CYAN,
              "Full-stack platform where citizens raise civic issues and track responses from their representatives.",
              ["React", "Spring Boot", "MySQL", "Git", "CI/CD"], "Automated cloud build + deploy"),
             ("IR Rover Bot Navigator", "Autonomous robot", ORANGE,
              "Arduino rover that detects obstacles with IR sensors and changes direction on its own.",
              ["Arduino Uno", "IR Sensors", "Embedded"], "Sensor-driven navigation")]
    CW, GAP, X0, TOP, H = 272, 16, 16, 46, 290
    p = [open_svg(W, H, sheen_css(W, 9, 12)), chrome(W, "projects/ — ls -la")]
    for i, (name, sub, col, desc, tags, metric) in enumerate(CARDS):
        x = X0 + i * (CW + GAP); d = .25 + i * .18
        p.append(f'<g class="in" style="animation-delay:{d:.2f}s">'
                 f'<rect x="{x}" y="{TOP}" width="{CW}" height="{H-TOP-14}" rx="8" fill="{BAR}" stroke="{BORDER}"/>'
                 f'<rect x="{x}" y="{TOP}" width="{CW}" height="3" rx="1.5" fill="{col}"/>'
                 f'<text x="{x+16}" y="{TOP+30}" class="s" style="font-size:15px;font-weight:700" fill="#f0f6fc">{esc(name)}</text>'
                 f'<text x="{x+16}" y="{TOP+47}" class="m" style="font-size:11px" fill="{col}">{esc(sub)}</text>')
        for j, ln in enumerate(textwrap.wrap(desc, 36)):
            p.append(f'<text x="{x+16}" y="{TOP+72+j*16}" class="m" style="font-size:11.5px" fill="{INK}">{esc(ln)}</text>')
        tx, ty = x + 16, TOP + 138
        for t in tags:
            w = len(t) * 6.6 + 14
            if tx + w > x + CW - 12: tx, ty = x + 16, ty + 22
            p.append(f'<rect x="{tx:.1f}" y="{ty}" width="{w:.1f}" height="18" rx="9" fill="{col}" fill-opacity=".12"/>'
                     f'<text x="{tx+w/2:.1f}" y="{ty+12.5}" text-anchor="middle" class="m" style="font-size:10px" fill="{col}">{esc(t)}</text>')
            tx += w + 6
        ch = H - TOP - 14
        p.append(f'<line x1="{x+16}" x2="{x+CW-16}" y1="{TOP+ch-38}" y2="{TOP+ch-38}" stroke="{BORDER}"/>'
                 f'<text x="{x+16}" y="{TOP+ch-14}" class="m" style="font-size:11.5px;font-weight:bold" fill="{col}">▸ {esc(metric)}</text></g>')
    p.append(sheen_layer(H)); save("projects.svg", p)

# ───────────────────────── HIGHLIGHTS ─────────────────────────
def highlights():
    TILES = [("8.94", "GPA", "KL University", GREEN), ("250+", "Problems solved", "CodeChef", CYAN),
             ("AWS", "Cloud", "Practitioner", YELLOW), ("B2", "Cambridge", "Linguaskill CEFR", PURPLE),
             ("2", "Internships", "Siemens · YIIC", ORANGE)]
    TW, GAP, X0, TOP, H = 152, 20, 20, 48, 158
    p = [open_svg(W, H, sheen_css(W, 10, 13)), chrome(W, "achievements.log")]
    for i, (val, l1, l2, col) in enumerate(TILES):
        x = X0 + i * (TW + GAP); d = .3 + i * .14
        p.append(f'<g class="pop" style="animation-delay:{d:.2f}s"><rect x="{x}" y="{TOP}" width="{TW}" height="{H-TOP-18}" rx="8" fill="{BAR}" stroke="{BORDER}"/>'
                 f'<text x="{x+TW/2}" y="{TOP+44}" text-anchor="middle" class="s" style="font-size:34px;font-weight:800" fill="{col}">{esc(val)}</text>'
                 f'<text x="{x+TW/2}" y="{TOP+66}" text-anchor="middle" class="m" style="font-size:11.5px" fill="{INK}">{esc(l1)}</text>'
                 f'<text x="{x+TW/2}" y="{TOP+82}" text-anchor="middle" class="m" style="font-size:10.5px" fill="{DIM}">{esc(l2)}</text>'
                 f'<rect x="{x+TW/2-18}" y="{TOP+H-48-14}" width="36" height="3" rx="1.5" fill="{col}"><animate attributeName="width" values="12;36;12" dur="3.2s" begin="{d}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="x" values="{x+TW/2-6};{x+TW/2-18};{x+TW/2-6}" dur="3.2s" begin="{d}s" repeatCount="indefinite"/></rect></g>')
    p.append(sheen_layer(H)); save("highlights.svg", p)

# ───────────────────────── FOOTER ─────────────────────────
def footer():
    H, PITCH = 112, 9.0
    line = '$ echo "thanks for visiting — let\'s build something together"'
    defs = (f'<linearGradient id="wg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>'
            f'<clipPath id="tp"><rect x="26" y="20" width="0" height="26"><animate attributeName="width" from="0" to="{len(line)*PITCH+6}" begin=".6s" dur="2.6s" fill="freeze"/>'
            f'</rect></clipPath>')
    def wave(y, a, per, op, dur, ph=0):
        n = int(W / per) + 3
        d = f"M{-per*2+ph} {y} q{per/4} {-2*a} {per/2} 0" + f" t{per/2} 0" * (2 * n) + f" V{H} H{-per*2+ph}Z"
        return (f'<path d="{d}" fill="url(#wg)" opacity="{op}"><animateTransform attributeName="transform" type="translate" '
                f'from="0 0" to="{per} 0" dur="{dur}s" repeatCount="indefinite"/></path>')
    p = [open_svg(W, H, sheen_css(W, 5, 12), defs)]
    xs, tx = glyphs(line, 26, PITCH)
    p.append(f'<text x="{xs}" y="38" class="m" style="font-size:15px" fill="{INK}" clip-path="url(#tp)">{tx}</text>')
    p.append('<g clip-path="url(#pc)">' + wave(86, 7, 220, .10, 9, 40) + wave(92, 6, 160, .16, 6) + wave(99, 5, 110, .26, 4, 20) + '</g>')
    p.append(sheen_layer(H)); save("footer.svg", p)

if __name__ == "__main__":
    hero(); stack(); projects(); highlights(); footer()
