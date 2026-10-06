"""Shared design tokens + helpers so every panel looks like one system."""
import html
BG, BAR, BORDER = "#0d1117", "#161b22", "#30363d"
INK, DIM = "#c9d1d9", "#7d8590"
GREEN, CYAN, PURPLE, YELLOW, ORANGE, PINK = "#7ee787", "#79c0ff", "#bc8cff", "#e3b341", "#ffa657", "#ff7b72"
MONO = 'ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace'
SANS = '-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif'
esc = lambda s: html.escape(str(s), quote=True)

BASE_CSS = f"""
.m{{font:12px {MONO}}} .s{{font-family:{SANS}}}
.in{{animation:in .7s cubic-bezier(.2,.8,.3,1) backwards}} @keyframes in{{from{{opacity:0;transform:translateY(10px)}}}}
.pop{{transform-box:fill-box;transform-origin:center;animation:pop .55s cubic-bezier(.2,.9,.3,1.25) backwards}}
@keyframes pop{{from{{opacity:0;transform:scale(.55)}}}}
.fade{{animation:fade .8s ease-out backwards}} @keyframes fade{{from{{opacity:0}}}}
.cur{{animation:blink 1s steps(1) infinite}} @keyframes blink{{50%{{opacity:0}}}}
"""

def open_svg(w, h, css="", defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>{BASE_CSS}{css}</style><defs>'
            f'<clipPath id="pc"><rect width="{w}" height="{h}" rx="10"/></clipPath>'
            f'<linearGradient id="shg" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="#fff" stop-opacity=".10"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'{defs}</defs>'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>')

def chrome(w, title):
    return (f'<path d="M.5 30.5V10.5a10 10 0 0 1 10-10H{w-10.5}a10 10 0 0 1 10 10V30.5Z" fill="{BAR}" stroke="{BORDER}"/>'
            '<circle cx="18" cy="15.5" r="5" fill="#ff5f56"/><circle cx="36" cy="15.5" r="5" fill="#ffbd2e"/><circle cx="54" cy="15.5" r="5" fill="#27c93f"/>'
            f'<text x="{w/2}" y="19.5" text-anchor="middle" class="m" fill="{DIM}" style="font-size:12px">{esc(title)}</text>')

def sheen_css(w, delay=6, every=9):
    return (f".sheen{{animation:sheen {every}s ease-in-out infinite {delay}s backwards}}"
            f"@keyframes sheen{{0%{{transform:translateX(-140px) skewX(-20deg)}}40%,100%{{transform:translateX({w+80}px) skewX(-20deg)}}}}")

def sheen_layer(h):
    return f'<g clip-path="url(#pc)" pointer-events="none"><rect class="sheen" x="0" y="0" width="110" height="{h}" fill="url(#shg)"/></g>'

def glyphs(text, x0, pitch):
    """Pin every non-space glyph to an exact x so the grid is identical in any monospace font."""
    pts = [(i, ch) for i, ch in enumerate(text) if ch != " "]
    return " ".join(f"{x0 + i*pitch:.2f}" for i, _ in pts), esc("".join(ch for _, ch in pts))
