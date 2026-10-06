"""Rebuild every static panel (the heatmap is refreshed daily by the GitHub Action).
   python scripts/build_all.py            -> portrait, card, panels, heatmap
   python scripts/build_all.py --photo    -> also re-cut the photo first (needs requirements.txt)"""
import subprocess, sys
steps = (["prep_photo.py", "source-photo.png"] if "--photo" in sys.argv else []), \
        ["make_ascii_svg.py"], ["make_info_card.py"], ["build_panels.py"], ["make_heatmap.py"]
for st in steps:
    if st: subprocess.run([sys.executable, f"scripts/{st[0]}", *st[1:]], check=True)
