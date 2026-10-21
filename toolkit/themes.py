"""Visual themes so no two Odds Visualized videos look alike (user, Oct 18: "change the visuals for each of the videos...
make sure they're unique each time"). Each video gets a theme (palette + background texture + card style + entry motion
+ accent colour), chosen so it differs from the last 6 videos (logged in themes_log.txt), and within the theme the exact
hues are jittered by the video id so even a repeated theme never renders identically.
"""
import hashlib, math, os, colorsys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

LOG = "/home/claude/odds/themes_log.txt"

THEMES = {
    # name: hook/dark base, item palette from->to, accent, texture, card style, entry motion
    "crimson_noir": dict(dark=(22, 6, 10), c0=(185, 28, 28), c1=(30, 64, 175), accent=(255, 214, 10), tex="vignette", card="none", entry="up"),
    "neon_grid":    dict(dark=(8, 6, 28), c0=(91, 33, 182), c1=(14, 116, 144), accent=(0, 255, 200), tex="grid", card="glow", entry="zoom"),
    "sunset":       dict(dark=(40, 12, 20), c0=(234, 88, 12), c1=(126, 34, 206), accent=(255, 240, 120), tex="rays", card="panel", entry="left"),
    "ocean":        dict(dark=(4, 20, 40), c0=(8, 145, 178), c1=(30, 27, 75), accent=(125, 249, 255), tex="waves", card="none", entry="drop"),
    "forest":       dict(dark=(6, 24, 14), c0=(22, 163, 74), c1=(120, 53, 15), accent=(250, 204, 21), tex="bokeh", card="panel", entry="up"),
    "candy":        dict(dark=(48, 10, 40), c0=(236, 72, 153), c1=(59, 130, 246), accent=(255, 255, 255), tex="dots", card="glow", entry="zoom"),
    "gold_vault":   dict(dark=(18, 14, 6), c0=(161, 98, 7), c1=(17, 24, 39), accent=(253, 224, 71), tex="diagonal", card="panel", entry="left"),
    "arctic":       dict(dark=(10, 22, 36), c0=(56, 189, 248), c1=(99, 102, 241), accent=(255, 255, 255), tex="snow", card="glow", entry="drop"),
    "lava":         dict(dark=(30, 4, 4), c0=(220, 38, 38), c1=(251, 146, 60), accent=(255, 255, 255), tex="rays", card="none", entry="zoom"),
    "mint_chalk":   dict(dark=(12, 30, 28), c0=(16, 185, 129), c1=(15, 23, 42), accent=(253, 186, 116), tex="grid", card="panel", entry="up"),
}

def _seed(vid): return int(hashlib.sha256(vid.encode()).hexdigest()[:8], 16)

def _jitter(c, r):
    h, l, s = colorsys.rgb_to_hls(*[x / 255 for x in c])
    h = (h + r.uniform(-0.04, 0.04)) % 1; s = min(1, max(0, s * r.uniform(0.85, 1.15)))
    return tuple(int(255 * x) for x in colorsys.hls_to_rgb(h, l, s))

def pick(video_id, avoid_last=6):
    """Returns a theme dict (with 'name') for this video and records it."""
    hist = open(LOG).read().split() if os.path.exists(LOG) else []
    for h in hist:   # same id already picked -> reuse (re-renders stay consistent)
        if h.startswith(video_id + ":"):
            name = h.split(":")[1]; break
    else:
        recent = [h.split(":")[1] for h in hist[-avoid_last:] if ":" in h]
        names = [n for n in THEMES if n not in recent] or list(THEMES)
        name = names[_seed(video_id) % len(names)]
        with open(LOG, "a") as f: f.write(f"{video_id}:{name}\n")
    r = np.random.default_rng(_seed(video_id))
    t = dict(THEMES[name]); t["name"] = name
    for k in ("c0", "c1", "dark"): t[k] = _jitter(t[k], r)
    t["phase"] = float(r.uniform(0, 6.28)); t["tilt"] = float(r.uniform(-0.6, 0.6))
    return t

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def background(theme, color, f, W, H):
    """Base gradient in `color` plus the theme's moving texture."""
    yy, xx = np.mgrid[0:H:8, 0:W:8].astype(np.float32)
    r = np.sqrt((xx - W / 2) ** 2 + (yy - H * 0.45) ** 2) / max(W, H)
    light = 1.18 - 0.75 * np.clip(r, 0, 1)
    tex = theme["tex"]; ph = theme["phase"]
    if tex == "grid":
        g = ((np.abs(((xx + f * 2) % 120) - 60) < 2) | (np.abs(((yy + f * 3) % 120) - 60) < 2)).astype(np.float32)
        light = light + 0.25 * g
    elif tex == "rays":
        ang = np.arctan2(yy - H * 0.45, xx - W / 2)
        light = light * (1 + 0.10 * np.sign(np.sin(ang * 12 + f / 25 + ph)))
    elif tex == "waves":
        light = light * (1 + 0.07 * np.sin(yy / 40 + np.sin(xx / 90 + f / 15) * 2 + ph))
    elif tex == "diagonal":
        light = light * (1 + 0.05 * np.sign(np.sin((xx * (1 + theme["tilt"]) + yy + f * 5) / 40)))
    a = np.array(color, np.float32)[None, None, :] * light[..., None]
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    if tex in ("bokeh", "dots", "snow"):
        d = ImageDraw.Draw(img, "RGBA"); rr = np.random.default_rng(int(ph * 1000))
        n = {"bokeh": 26, "dots": 70, "snow": 110}[tex]
        for i in range(n):
            x0, y0 = rr.uniform(0, W), rr.uniform(0, H); sp = rr.uniform(0.5, 2.0)
            if tex == "snow": y = (y0 + f * 3 * sp) % H; x = x0 + 10 * math.sin(f / 20 + i); rad = 2 + sp * 2; alpha = 170
            elif tex == "dots": x, y = x0, (y0 - f * sp) % H; rad = 5 + 4 * sp; alpha = 60
            else: x, y = x0 + 30 * math.sin(f / 50 + i), (y0 - f * 0.6 * sp) % H; rad = 30 + 40 * sp; alpha = 35
            d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=(255, 255, 255, alpha))
    if tex == "vignette":
        m = np.clip((np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) - 0.7) / 0.6, 0, 1) * 0.6
        red = Image.new("RGB", (W, H), (200, 0, 0))
        img = Image.composite(red, img, Image.fromarray((m * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR))
    return img

def card_behind(img, theme, cx, cy, w, h, f):
    """Optional panel or glow behind the main item, depending on theme."""
    if theme["card"] == "none": return img
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if theme["card"] == "panel":
        d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 48, fill=(0, 0, 0, 90), outline=theme["accent"] + (200,), width=6)
    else:
        rr = w / 2 * (1 + 0.04 * math.sin(f / 4))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=theme["accent"] + (70,))
        lay = lay.filter(ImageFilter.GaussianBlur(40))
    img.paste(lay, (0, 0), lay)
    return img

def entry_offset(theme, t):
    """(dx, dy, scale) for the item's entrance; t in 0..1 (eased by caller)."""
    e = theme["entry"]; u = 1 - t
    if e == "up": return 0, 650 * u, 1.0
    if e == "drop": return 0, -650 * u, 1.0
    if e == "left": return -900 * u, 0, 1.0
    return 0, 0, 0.3 + 0.7 * t   # zoom
