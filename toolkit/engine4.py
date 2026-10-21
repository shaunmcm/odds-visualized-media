"""Odds Visualized LONG-FORM format B (16:9): "The Waiting Game" — if you tried once a day, how long until it happens?

Deliberately different from engine3 (the Ladder) so the channel doesn't look mass-produced:
dark starfield instead of bright stripes, mint/cyan accents instead of yellow, a horizontal TIME line with
history landmarks instead of a vertical meter, a rolling day counter, different pacing (6.5 s per item, 8 items + 5 s intro + 3 s outro).
Expected wait = 1/p tries (the average of a geometric distribution), at one try per day.
Spec: {"id","hook":{"emoji","top","num","bottom","loop"},"items":[{"emoji","label","denom","wait","context","source"}],
       "outro_top","outro_line","outro_cta"}
"""
import math, subprocess, sys, json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import engine2 as e2
from engine2 import font, emoji_img, paste_c, scaled_text, back, prog, WHITE, BLACK

W, H, FPS = 1920, 1080, 30
INTRO, ITEM, OUTRO = 135, 195, 120
MINT = (64, 255, 196); CYAN = (90, 200, 255); PINK = (255, 110, 170); SOFT = (200, 210, 230)

_rng = np.random.default_rng(7)
STARS = [(float(_rng.uniform(0, W)), float(_rng.uniform(0, H)), float(_rng.uniform(0.5, 2.4)), float(_rng.uniform(0, 6.28))) for _ in range(260)]
_bg = None
def base_bg():
    global _bg
    if _bg is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        t = yy / H
        top = np.array([12, 16, 40], np.float32); bot = np.array([38, 14, 60], np.float32)
        a = top[None, None, :] * (1 - t[..., None]) + bot[None, None, :] * t[..., None]
        r = np.sqrt((xx - W * 0.3) ** 2 + (yy - H * 0.35) ** 2) / W
        a *= (1.25 - 0.5 * np.clip(r, 0, 1))[..., None]
        _bg = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return _bg

def background(f):
    img = base_bg().copy(); d = ImageDraw.Draw(img)
    for x, y, s, ph in STARS:
        x2 = (x - f * 0.6 * s) % W
        b = int(140 + 110 * math.sin(f / 9 + ph))
        d.ellipse([x2 - s, y - s, x2 + s, y + s], fill=(b, b, min(255, b + 20)))
    return img

def text_l(d, x, y, s, f, fill=WHITE, max_w=1000, stroke=0):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= max_w: cur = t
        else: lines.append(cur); cur = w_
    lines.append(cur)
    for i, ln in enumerate(lines):
        d.text((x, y + i * int(f.size * 1.12)), ln, font=f, fill=fill, stroke_width=stroke, stroke_fill=BLACK)
    return y + len(lines) * int(f.size * 1.12)

# time line: log10(years) from 1 day to beyond the age of the universe
TL0, TL1, TX0, TX1, TY = -2.6, 11.2, 140, 1780, 900
MARKS = [(-1.72, "1 week"), (0, "1 year"), (1.9, "a lifetime"), (3.7, "all of history"), (5.48, "humans exist"),
         (7.82, "dinosaurs die"), (10.14, "age of universe")]
def tl_x(lg): return TX0 + (TX1 - TX0) * (min(lg, TL1) - TL0) / (TL1 - TL0)

def draw_timeline(img, done, cur_lg, emo, f):
    d = ImageDraw.Draw(img)
    d.line([TX0, TY, TX1, TY], fill=SOFT, width=4)
    d.polygon([(TX1 + 30, TY), (TX1 + 4, TY - 14), (TX1 + 4, TY + 14)], fill=SOFT)
    for i, (lg, lab) in enumerate(MARKS):
        x = tl_x(lg); up = i % 2 == 0
        d.line([x, TY - 12, x, TY + 12], fill=SOFT, width=3)
        fz = font(24, "SemiBold"); tw = d.textlength(lab, font=fz)
        d.text((x - tw / 2, TY + 22 if up else TY + 52), lab, font=fz, fill=SOFT)
    x = tl_x(cur_lg)
    d.line([TX0, TY, x, TY], fill=MINT, width=8)
    for lg, e in done:
        paste_c(img, emoji_img(e, 40), tl_x(lg), TY - 40)
    if cur_lg > TL1:  # flew off the end of time
        d = ImageDraw.Draw(img)
        d.text((TX1 - 460, TY - 120), "OFF THE CHART", font=font(44, "Black"), fill=PINK)
    paste_c(img, emoji_img(emo, 70), x, TY - 50 + 4 * math.sin(f / 3))

def fmt_days(v):
    if v < 730: return f"Day {int(v):,}"
    return f"Year {int(v / 365.25):,}"

def center(d, y, s, f, fill=WHITE, max_w=1600):
    return e2.text(d, W / 2, y, s, f, fill, 0, max_w)

def dots(d, k, n):
    gap = 44; x0 = W / 2 - gap * (n - 1) / 2
    for i in range(n):
        c = MINT if i == k else (90, 100, 130)
        r = 11 if i == k else 8
        d.ellipse([x0 + i * gap - r, 1010 - r, x0 + i * gap + r, 1010 + r], fill=c)

def render(sp, out, musicpath):
    """SIMPLE layout (user, Oct 16: first version was too hard to understand at a glance):
    one thing on screen at a time, centred, huge answer, one short line of context."""
    items = sp["items"]; n = len(items)
    N = INTRO + ITEM * n + OUTRO
    pipe = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "medium", "-crf", "20", out + ".v.mp4"], stdin=subprocess.PIPE)
    sfx = [(0.0, "boom")]
    for fr in range(N):
        img = background(fr); d = ImageDraw.Draw(img); src = ""
        if fr < INTRO:
            # COLD-OPEN HOOK (0-5 s): the most shocking answer on frame 0, then a cliffhanger
            f = fr; hk = sp["hook"]
            paste_c(img, emoji_img(hk["emoji"], int(230 * (0.85 + 0.15 * back(f / 6)))), W / 2, 230 + 6 * math.sin(f / 5))
            d = ImageDraw.Draw(img)
            center(d, 380, hk["top"], font(64, "Bold"), WHITE)
            fs = 190 if len(hk["num"]) < 12 else 150 if len(hk["num"]) < 18 else 120
            scaled_text(img, W / 2, 610, hk["num"].upper(), font(fs), 0.88 + 0.12 * back(f / 6), MINT, 0)
            d = ImageDraw.Draw(img)
            0 and center(d, 740, hk["bottom"], font(60, "Bold"), CYAN)
            if f >= 75:
                if f == 75: sfx.append((f / FPS, "whoosh"))
                center(d, 880, hk["loop"], font(58), (255, 214, 10))
        elif fr < INTRO + ITEM * n:
            k = (fr - INTRO) // ITEM; f = (fr - INTRO) % ITEM; it = items[k]
            if f == 0: sfx.append((fr / FPS, "pop"))
            center(d, 70, "IF YOU TRIED ONCE A DAY...", font(52, "Black"), CYAN)
            paste_c(img, emoji_img(it["emoji"], int(260 * (0.75 + 0.25 * back(f / 9)))), W / 2, 300 + 6 * math.sin(f / 6))
            d = ImageDraw.Draw(img)
            center(d, 460, it["label"], font(88), WHITE)
            if 20 <= f < 66:
                scaled_text(img, W / 2, 700, "?", font(170), 0.9 + 0.1 * math.sin(f / 2), (150, 160, 190), 0)
                if f % 6 == 0: sfx.append((fr / FPS, "tick"))
            if f >= 66:
                if f == 66: sfx.append((fr / FPS, "ding" if k < n - 1 else "boom"))
                fs = 170 if len(it["wait"]) < 12 else 128 if len(it["wait"]) < 18 else 104
                scaled_text(img, W / 2, 700, it["wait"].upper(), font(fs), 0.85 + 0.15 * back((f - 66) / 7), MINT, 0)
            d = ImageDraw.Draw(img)
            if False: center(d, 850, it["context"], font(54, "Bold"), WHITE)
            src = it["source"]
        else:
            f = fr - INTRO - ITEM * n
            if f == 0: sfx.append((fr / FPS, "whoosh"))
            center(d, 260, sp["outro_top"], font(96), MINT)
            center(d, 420, sp["outro_line"], font(60, "Bold"), WHITE, 1500)
            if f >= 20:
                cta = sp["outro_cta"]; tw = d.textlength(cta, font=font(56))
                d.rounded_rectangle([W / 2 - tw / 2 - 50, 650, W / 2 + tw / 2 + 50, 760], 22, fill=(230, 30, 40))
                d.text((W / 2 - tw / 2, 670), cta, font=font(56), fill=WHITE)
        d = ImageDraw.Draw(img)
        d.text((W - 360, 40), "ODDS VISUALIZED", font=font(30, "Black"), fill=(220, 225, 240))
        if False: d.text((60, 1040), src, font=font(22, "SemiBold"), fill=(150, 160, 185))
        pipe.stdin.write(img.convert("RGB").tobytes())
    pipe.stdin.close(); pipe.wait()
    e2.mix_audio(sfx, musicpath, N / FPS, out + ".a.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out + ".v.mp4", "-i", out + ".a.wav",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    os.remove(out + ".v.mp4"); os.remove(out + ".a.wav")

if __name__ == "__main__":
    import music
    specs = json.load(open(sys.argv[1])); only = set(sys.argv[2:])
    os.makedirs("/home/claude/odds/music/gen", exist_ok=True); os.makedirs("/home/claude/odds/out3", exist_ok=True)
    for sp in specs:
        if only and sp["id"] not in only: continue
        N = INTRO + ITEM * len(sp["items"]) + OUTRO
        mpath = f"/home/claude/odds/music/gen/{sp['id']}.wav"
        music.make_styled(sp["id"], mpath, seconds=N / FPS + 1, style=music.pick_style(sp["id"]))
        render(sp, f"/home/claude/odds/out3/{sp['id']}.mp4", mpath)
        print("rendered", sp["id"], flush=True)
