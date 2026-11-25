"""Render SVGs to PNGs next to them (same name, .png): every animation frozen at --at ms (default 3000), at 2x.

The GitHub mobile app shows some SVGs as a broken-image icon, so phone-sized images ship as PNG.
usage: python scripts/render_png.py [--browser chromium|webkit] [--at ms] file.svg [...]
"""
import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# Freeze each animation at t; a short loop (a blink, 5 s or less) caught in its hidden phase is frozen at 0, where it shows.
FREEZE = """t => document.getAnimations().forEach(a => {
  a.pause(); a.currentTime = t;
  const el = a.effect && a.effect.target; if (!el) return;
  const op = () => parseFloat(getComputedStyle(el).opacity);
  const d = a.effect.getTiming().duration;
  if (typeof d === "number" && d <= 5000 && op() < 0.5) { a.currentTime = 0; if (op() < 0.5) a.currentTime = t; }
})"""

args = sys.argv[1:]
browser, at = "chromium", 3000
while args[:1] in (["--browser"], ["--at"]):
    if args[0] == "--browser":
        browser = args[1]
    else:
        at = int(args[1])
    args = args[2:]

with sync_playwright() as pw:
    b = getattr(pw, browser).launch()
    page = b.new_context(device_scale_factor=2).new_page()
    for f in map(Path, args):
        w, h = (int(float(v) + 0.999) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', f.read_text("utf-8")).groups())
        page.set_viewport_size({"width": w, "height": h})
        page.goto(f.resolve().as_uri())
        page.wait_for_timeout(300)
        page.evaluate(FREEZE, at)
        page.wait_for_timeout(100)
        out = f.with_suffix(".png")
        page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": w, "height": h}, omit_background=True)
        print(f"{out}  {w}x{h}  {out.stat().st_size // 1024} KB")
    b.close()
