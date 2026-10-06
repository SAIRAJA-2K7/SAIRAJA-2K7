import os, math, json, random, datetime, urllib.request

USER = os.environ.get("GH_USER", "SAIRAJA-2K7")
PROMPT_NAME = "sairaja"
TOKEN = os.environ.get("GH_TOKEN")
OUT = os.environ.get("OUT", "contrib-heatmap.svg")

CELL, GAP = 12, 4
PITCH = CELL + GAP
LEFT, TOP = 44, 64
RIPPLE_SPEED = 0.035   # seconds of delay per pixel of distance (smaller = faster wave)
DURATION = 5           # seconds per ripple cycle
INTRO_SPEED = 0.0028   # intro wave: delay per pixel (smaller = faster reveal)
SHEEN_EVERY = 7        # seconds between light sweeps across the grid
INTRO_DUR = 0.8        # how long each cell takes to pop in

def fetch():
    q = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
      totalContributions weeks{contributionDays{date contributionCount weekday}}}}}}"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": q, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"})
    cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return cal["totalContributions"], cal["weeks"]

def mock():
    random.seed(4)
    d = datetime.date.today() - datetime.timedelta(days=364)
    weeks, total = [], 0
    while d <= datetime.date.today():
        days = []
        for _ in range(7):
            c = random.choice([0, 0, 1, 3, 6, 10, 18]) if d <= datetime.date.today() else 0
            total += c
            days.append({"date": d.isoformat(), "contributionCount": c, "weekday": (d.weekday() + 1) % 7})
            d += datetime.timedelta(days=1)
        weeks.append({"contributionDays": days})
    return total, weeks

def color(c, mx):
    if c == 0: return "#161b22"
    t = math.sqrt(c / mx)                       # sqrt so small counts stay visible
    lo, hi = (14, 68, 41), (108, 232, 128)      # dark green -> softer mint
    return "#%02x%02x%02x" % tuple(int(a + (b - a) * t) for a, b in zip(lo, hi))

total, weeks = fetch() if TOKEN else mock()
mx = max(d["contributionCount"] for w in weeks for d in w["contributionDays"]) or 1
W = LEFT + len(weeks) * PITCH + 20
H = TOP + 7 * PITCH + 50
cx, cy = LEFT + len(weeks) * PITCH / 2, TOP + 3.5 * PITCH   # ripple origin (centre). Change to LEFT, cy for left-to-right wave

max_dist = math.hypot(max(cx - LEFT, W - cx), max(cy - TOP, TOP + 7 * PITCH - cy))
T0 = max_dist * INTRO_SPEED + INTRO_DUR   # loop starts only after the whole intro has finished
flat = [d for w in weeks for d in w["contributionDays"]]
counts = [d["contributionCount"] for d in flat]
longest = run = 0
for c in counts:
    run = run + 1 if c else 0; longest = max(longest, run)
cur, seq = 0, counts[:]
if seq and seq[-1] == 0: seq = seq[:-1]          # today may not have contributions yet
for c in reversed(seq):
    if c: cur += 1
    else: break
best = max(flat, key=lambda d: d["contributionCount"])
best_s = datetime.date.fromisoformat(best["date"]).strftime("%b %d")
active = sum(1 for c in counts if c)
legend = '<text x="{lx}" y="{ly}" class="lbl" text-anchor="end">Less</text>'
cells, glows, gloss, clips, months, last = [], [], [], [], [], None
for i, w in enumerate(weeks):
    x = LEFT + i * PITCH
    m = datetime.date.fromisoformat(w["contributionDays"][0]["date"]).strftime("%b")
    if m != last and i < len(weeks) - 2:
        months.append(f'<text x="{x}" y="{TOP-10}" class="lbl">{m}</text>'); last = m
    for d in w["contributionDays"]:
        y = TOP + d["weekday"] * PITCH
        dist = math.hypot(x - cx, y - cy)
        intro = dist * INTRO_SPEED
        delay = T0 + (dist * RIPPLE_SPEED) % DURATION   # same wave phase, but every cell joins the loop within the first cycle
        cnt = d["contributionCount"]
        sty = f'style="animation-delay:{intro:.2f}s,{delay:.2f}s"'
        clips.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3"/>')
        if cnt:
            gloss.append(f'<rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="url(#gloss)" {sty}/>')
        if cnt and math.sqrt(cnt / mx) > 0.45:
            glows.append(f'<rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{color(cnt, mx)}" {sty}/>')
        cells.append(f'<rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
                     f'fill="{color(d["contributionCount"], mx)}" style="animation-delay:{intro:.2f}s,{delay:.2f}s"/>')

days = "".join(f'<text x="8" y="{TOP + r*PITCH + 10}" class="lbl">{n}</text>'
               for r, n in ((1, "Mon"), (3, "Wed"), (5, "Fri")))

lx0 = W - 20 - 5 * 16 - 38
leg = (f'<g class="fade" style="animation-delay:{T0*0.6:.2f}s"><text x="{lx0}" y="{TOP+7*PITCH+21}" class="lbl" text-anchor="end">Less</text>'
       + "".join(f'<rect x="{lx0+6+k*16}" y="{TOP+7*PITCH+11}" width="{CELL}" height="{CELL}" rx="3" fill="{color(max(1, round(f*mx)) if f else 0, mx)}"/>' for k, f in enumerate([0, .12, .35, .65, 1]))
       + f'<text x="{lx0+6+5*16+4}" y="{TOP+7*PITCH+21}" class="lbl">More</text></g>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .bg{{fill:#0d1117}} .lbl{{fill:#7d8590;font:11px -apple-system,Segoe UI,sans-serif}}
  .term{{fill:#fff;font:bold 15px ui-monospace,Consolas,monospace}}
  .tot{{fill:#fff;font:bold 13px -apple-system,Segoe UI,sans-serif}}
  .c{{transform-box:fill-box;transform-origin:center;
        animation:pop {INTRO_DUR}s cubic-bezier(.2,.8,.3,1) backwards, ripple {DURATION}s ease-in-out infinite}}
  @keyframes pop{{
    0%{{transform:scale(0);opacity:0;filter:brightness(1.8)}}
    60%{{transform:scale(1.5);opacity:1;filter:brightness(1.6)}}
    100%{{transform:scale(1);opacity:1;filter:brightness(1)}}
  }}
  .fade{{animation:fade .8s ease-out backwards}} @keyframes fade{{from{{opacity:0}}}}
  @keyframes ripple{{
    0%,40%,100%{{transform:scale(1);filter:brightness(1)}}
    15%{{transform:scale(1.35);filter:brightness(1.5)}}
    28%{{transform:scale(.8);filter:brightness(.8)}}
  }}
  .sheen{{animation:sheen {SHEEN_EVERY}s ease-in-out infinite {T0+1:.2f}s backwards}}
  @keyframes sheen{{0%{{transform:translateX(-120px) skewX(-20deg)}} 40%,100%{{transform:translateX({W+60}px) skewX(-20deg)}}}}
  .cur{{animation:blink 1s steps(1) infinite}} @keyframes blink{{50%{{opacity:0}}}}
</style>
<defs>
  <linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".38"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3.2"/></filter>
  <clipPath id="grid">{"".join(clips)}</clipPath>
</defs>
<rect class="bg" x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" stroke="#30363d"/>
<g class="fade"><rect x="{LEFT+4}" y="12" width="{len(PROMPT_NAME)*9+262}" height="26" rx="5" fill="#1c2128"/>
<text x="{LEFT+12}" y="30" class="term">{PROMPT_NAME}@github ~ $ ./contributions.sh<tspan class="cur"> ▌</tspan></text></g>
{"".join(months)}{days}
<g filter="url(#glow)" opacity=".55">{"".join(glows)}</g>
{"".join(cells)}
{"".join(gloss)}
<g clip-path="url(#grid)"><rect class="sheen" x="0" y="{TOP-4}" width="90" height="{7*PITCH+8}" fill="url(#sheen)"/></g>
<text x="{LEFT}" y="{TOP+7*PITCH+22}" class="tot fade" style="animation-delay:{T0*0.6:.2f}s">{total:,} contributions in the last year<tspan class="lbl" font-weight="normal">  ·  {active} active days  ·  current streak {cur}d  ·  longest {longest}d  ·  best day {best["contributionCount"]} ({best_s})</tspan></text>
{leg}
</svg>'''

os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w", encoding="utf-8").write(svg)
print("wrote", OUT, len(svg)//1024, "KB")
