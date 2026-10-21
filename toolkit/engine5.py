"""Odds Visualized LONG-FORM format A2 (16:9, 45-60 s): "The Rarity Road" — replaces the Ladder (engine3), which the
user found too confusing to read (Oct 17).

Modelled on what the big comparison channels do (Reigarw Comparisons ~2.1M subs, "Probability Comparison: Death" 11M
views; MetaBallStudios ~2M subs): ONE continuous camera move along a single line of things that get rarer, each stop
= one big picture + max ~4 words + ONE huge number. Nothing else to read. Plus retention research: frame 0 is simple and
bright, the hook FORESHADOWS the payoff (curiosity gap / open loop), no greeting, text in the centre band, the gaps
between stops visibly grow (tension), payoff at the very end, last frame loops back into the first.

Timeline (30 fps): HOOK 3.5 s -> N stops x 5 s (1 s glide + 4 s hold) -> PAYOFF 5 s.
Spec: {"id","hook":{"top","big","bottom","ask"},"stops":[{"emoji","label","num","source"}],"payoff":{"emoji","label","num","line"}}
The last stop is NOT in "stops": it is the payoff (hidden as "?" in the hook, revealed at the end).
"""
import math, subprocess, sys, json, os, colorsys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import engine2 as e2
import themes
from engine2 import font, emoji_img, paste_c, scaled_text, back, prog, ease, WHITE, BLACK

W, H, FPS = 1920, 1080, 30
HOOK, STOP, GLIDE, PAY = 135, 150, 30, 150
YELLOW = (255, 214, 10)

def sky(t, f):
    """Background hue slides from calm green (common) to hot red/purple (impossible) as the camera travels."""
    h = 0.36 - 0.36 * t + (0.08 * max(0, t - 0.85) / 0.15)
    top = np.array(colorsys.hsv_to_rgb(h % 1, 0.55, 0.32)) * 255
    bot = np.array(colorsys.hsv_to_rgb(h % 1, 0.75, 0.62)) * 255
    yy = np.linspace(0, 1, H // 8, dtype=np.float32)[:, None, None]
    a = top[None, None, :] * (1 - yy) + bot[None, None, :] * yy
    a = np.repeat(a, W // 8, axis=1)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)

def render(sp, out, musicpath):
    global YELLOW
    TH = themes.pick(sp["id"]); YELLOW = TH["accent"]   # unique look per video
    stops = sp["stops"] + [dict(sp["payoff"], payoff=True)]
    n = len(stops)
    # world x-positions: gaps grow so the "road" visibly stretches as things get rarer
    xs = [0.0]
    for i in range(1, n):
        xs.append(xs[-1] + 1100 + 120 * i)
    N = HOOK + STOP * (n - 1) + PAY
    pipe = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "medium", "-crf", "20", out + ".v.mp4"], stdin=subprocess.PIPE)
    sfx = [(0.0, "boom")]
    ROAD_Y = 860
    for fr in range(N):
        # ---------- where is the camera?
        if fr < HOOK:
            k, f, cam = -1, fr, xs[0] - 1400
        else:
            g = fr - HOOK
            k = min(n - 1, g // STOP); f = g - k * STOP
            if k == n - 1: f = g - (n - 1) * STOP
            frm = xs[k - 1] if k > 0 else xs[0] - 1400
            cam = frm + (xs[k] - frm) * ease(f / GLIDE)
            if f == 0: sfx.append((fr / FPS, "whoosh"))
            if f == GLIDE: sfx.append((fr / FPS, "boom" if stops[k].get("payoff") else "pop"))
        t = max(0.0, min(1.0, (cam - xs[0]) / (xs[-1] - xs[0])))
        img = themes.background(TH, themes.lerp(TH['c0'], TH['c1'], t), fr, W, H); d = ImageDraw.Draw(img)
        # road + passing markers (constant motion)
        d.rectangle([0, ROAD_Y, W, ROAD_Y + 10], fill=(255, 255, 255))
        for m in range(-2, 30):
            mx = (m * 240 - cam) % (W + 240) - 120
            d.rectangle([mx, ROAD_Y + 22, mx + 90, ROAD_Y + 30], fill=(255, 255, 255, 120))
        d.text((W - 330, ROAD_Y + 50), "RARER  →", font=font(44, "Black"), fill=(255, 255, 255))
        # ---------- items on the road (only near the camera)
        for i, s in enumerate(stops):
            sx = W / 2 + (xs[i] - cam)
            if sx < -500 or sx > W + 500: continue
            is_pay = s.get("payoff")
            hidden = is_pay and not (k == n - 1 and f >= GLIDE + 20)
            near = 1 - min(1, abs(xs[i] - cam) / 1100)
            size = int(150 + 190 * near)
            if hidden:
                scaled_text(img, sx, ROAD_Y - 40 - size / 2, "?", font(size), 1.0, YELLOW, 10)
            else:
                pop = back((f - GLIDE) / 8) if (i == k and f >= GLIDE) else 1.0
                paste_c(img, emoji_img(s["emoji"], max(10, int(size * (0.85 + 0.15 * pop)))), sx, ROAD_Y - 30 - size / 2)
            d = ImageDraw.Draw(img)
        # ---------- the ONE label + ONE number for the current stop (centre band, big)
        if k >= 0 and f >= GLIDE:
            s = stops[k]; a = prog(f, GLIDE, 6)
            if s.get("payoff"):
                if f >= GLIDE + 20:
                    e2.text(d, W / 2, 80, s["label"], font(72), WHITE, 7, 1700)
                    fs = 170 if len(s["num"]) < 14 else 130
                    scaled_text(img, W / 2, 280, s["num"], font(fs), 0.8 + 0.2 * back((f - GLIDE - 20) / 7), YELLOW, 12)
                    d = ImageDraw.Draw(img)
                    if False: e2.text(d, W / 2, 380, s["line"], font(50, "Bold"), WHITE, 6, 1600)
                else:
                    e2.text(d, W / 2, 200, "And the rarest one...", font(84), WHITE, 8, 1700)
                    if f == GLIDE: sfx.append((fr / FPS, "tick"))
            else:
                e2.text(d, W / 2, 110, s["label"], font(76), WHITE, 7, 1700)
                fs = 170 if len(s["num"]) < 14 else 130
                scaled_text(img, W / 2, 330, s["num"], font(fs), 0.85 + 0.15 * back((f - GLIDE) / 7), YELLOW, 12)
                d = ImageDraw.Draw(img)
                if f == GLIDE + 2: sfx.append((fr / FPS, "ding"))
        # ---------- HOOK: foreshadow the payoff, ask for a guess (frame 0 already readable)
        if fr < HOOK:
            hk = sp["hook"]
            e2.text(d, W / 2, 90, hk["top"], font(72), WHITE, 8, 1700)
            scaled_text(img, W / 2, 300, hk["big"], font(180), 0.88 + 0.12 * back(fr / 6), YELLOW, 12)
            d = ImageDraw.Draw(img)
            0 and e2.text(d, W / 2, 420, hk["bottom"], font(64), WHITE, 7, 1700)
            0 and e2.text(d, W / 2, 530, hk.get("explain", ""), font(52, "Black"), YELLOW, 7, 1700)
            row = []   # SIMPLE: no emoji row
            gap = min(160, (W - 120) / max(1, len(row)))
            for j, em in enumerate(row):
                if fr >= 6 + j * 4:
                    paste_c(img, emoji_img(em, int(120 * back((fr - 6 - j * 4) / 6))), W / 2 + (j - (len(row) - 1) / 2) * gap, 760)
            d = ImageDraw.Draw(img)
            if fr >= 40:
                if fr == 40: sfx.append((fr / FPS, "whoosh"))
                e2.text(d, W / 2, 920, hk["ask"], font(54, "Black"), YELLOW, 6, 1700)
        # brand + tiny honest source line (well outside the centre band)
        d.text((60, 1012), "ODDS VISUALIZED", font=font(30, "Black"), fill=WHITE, stroke_width=4, stroke_fill=BLACK)
        if False and k >= 0 and f >= GLIDE and not (stops[k].get("payoff") and f < GLIDE + 20):
            src = stops[k].get("source", "")
            sw = d.textlength(src, font=font(22, "SemiBold"))
            d.text((W - 60 - sw, 1016), src, font=font(22, "SemiBold"), fill=(235, 235, 235), stroke_width=3, stroke_fill=BLACK)
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
        N = HOOK + STOP * len(sp["stops"]) + PAY
        mpath = f"/home/claude/odds/music/gen/{sp['id']}.wav"
        music.make_styled(sp["id"], mpath, seconds=N / FPS + 1, style=music.pick_style(sp["id"]))
        render(sp, f"/home/claude/odds/out3/{sp['id']}.mp4", mpath)
        print("rendered", sp["id"], N / FPS, "s", flush=True)
