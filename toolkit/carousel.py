"""Odds Visualized Instagram CAROUSEL renderer (1080x1350, 4:5) — the daily save-magnet post (IG_SYSTEM.md).

Spec: {"id", "slides": [
    {"type": "cover", "kicker": "small line", "title": "curiosity-gap headline", "big": "huge word/number", "emoji": "..."},
    {"type": "value", "n": 1, "emoji": "...", "title": "<=15 words", "big": "optional number", "note": "optional tiny line"},
    {"type": "cta", "title": "...", "keyword": "ODDS" or "", "line": "...", "save": "Save this ..."}]}
Same simplicity rules as the videos: one line + one picture + one big number per slide, plain-word numbers.
"""
import json, os, sys
from PIL import Image, ImageDraw
import themes
import engine2 as e2
from engine2 import font, emoji_img, paste_c, WHITE, BLACK

W, H = 1080, 1350

def fit(d, s, size, weight, max_w, min_size=40):
    while size > min_size and d.textlength(s, font=font(size, weight)) > max_w * 1.9: size -= 4
    return font(size, weight)

def render(sp, outdir):
    TH = themes.pick(sp["id"]); ACC = TH["accent"]
    n = len(sp["slides"]); paths = []
    for i, s in enumerate(sp["slides"]):
        t = i / max(1, n - 1)
        img = themes.background(TH, TH["dark"] if s["type"] != "value" else themes.lerp(TH["c0"], TH["c1"], t), i * 7, W, H)
        d = ImageDraw.Draw(img)
        if s["type"] == "cover":
            ty = 230
            if s.get("kicker"): ty = e2.text(d, W / 2, 120, s["kicker"], font(48, "Black"), WHITE, 6, 960) + 40
            e2.text(d, W / 2, ty, s["title"], fit(d, s["title"], 92, "Black", 960), ACC, 10, 960)
            if s.get("emoji"):
                img = themes.card_behind(img, TH, W / 2, 790, 460, 460, 0)
                paste_c(img, emoji_img(s["emoji"], 380), W / 2, 790); d = ImageDraw.Draw(img)
            if s.get("big"): e2.text(d, W / 2, 1060, s["big"], fit(d, s["big"], 110, "Black", 980), WHITE, 10, 1000)
            e2.text(d, W / 2, 1250, "SWIPE  →", font(44, "Black"), ACC, 6, 900)
        elif s["type"] == "value":
            e2.text(d, W / 2, 110, f"{s['n']}", font(70, "Black"), ACC, 8, 900)
            if s.get("emoji"):
                img = themes.card_behind(img, TH, W / 2, 470, 360, 360, 0)
                paste_c(img, emoji_img(s["emoji"], 290), W / 2, 470); d = ImageDraw.Draw(img)
            y = e2.text(d, W / 2, 700, s["title"], fit(d, s["title"], 72, "Black", 960), WHITE, 9, 960)
            if s.get("big"): e2.text(d, W / 2, max(y + 40, 960), s["big"], fit(d, s["big"], 104, "Black", 980), ACC, 10, 1000)
            if s.get("note"): e2.text(d, W / 2, 1200, s["note"], font(34, "Bold"), (235, 235, 235), 5, 960)
        else:  # cta
            e2.text(d, W / 2, 200, s["title"], fit(d, s["title"], 84, "Black", 960), WHITE, 9, 960)
            if s.get("keyword"):
                d.rounded_rectangle([W / 2 - 330, 520, W / 2 + 330, 760], 48, fill=ACC, outline=WHITE, width=8)
                kw = f"Comment “{s['keyword']}”"
                e2.text(d, W / 2, 585, kw, fit(d, kw, 84, "Black", 600), BLACK, 0, 620)
            elif s.get("emoji"):
                paste_c(img, emoji_img(s["emoji"], 300), W / 2, 640); d = ImageDraw.Draw(img)
            if s.get("line"): e2.text(d, W / 2, 850, s["line"], font(54, "Bold"), WHITE, 7, 940)
            if s.get("save"): e2.text(d, W / 2, 1110, s["save"], font(58, "Black"), ACC, 8, 960)
        d.text((48, H - 70), "ODDS VISUALIZED", font=font(30, "Black"), fill=WHITE, stroke_width=4, stroke_fill=BLACK)
        tag = f"{i + 1}/{n}"; tw = d.textlength(tag, font=font(30, "Black"))
        d.text((W - 48 - tw, H - 70), tag, font=font(30, "Black"), fill=WHITE, stroke_width=4, stroke_fill=BLACK)
        p = os.path.join(outdir, f"{sp['id']}_{i + 1}.jpg"); img.convert("RGB").save(p, quality=92); paths.append(p)
    return paths

if __name__ == "__main__":
    specs = json.load(open(sys.argv[1])); only = set(sys.argv[2:])
    os.makedirs("/home/claude/odds/out6", exist_ok=True)
    for sp in specs:
        if only and sp["id"] not in only: continue
        print(sp["id"], render(sp, "/home/claude/odds/out6"))
