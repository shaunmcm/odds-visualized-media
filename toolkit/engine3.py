"""Odds Visualized LONG-FORM (16:9, ~60 s): "The Odds Ladder" — 8 odds ranked from everyday to impossible.

YouTube counts a horizontal 16:9 video as a regular (long-form) video, so these build watch hours.
Timeline (30 fps, 60 s):
  0-6 s     HOOK: "8 odds, from EVERYDAY to IMPOSSIBLE", all 8 icons pop in a row, "Guess which one breaks the scale"
  6-54 s    8 RUNGS x 6 s: level badge, icon pops, label, the number counts up, a marker climbs the
            log-scale rarity meter on the right, then a "that's like..." context line
  54-60 s   OUTRO: the rarest one + subscribe CTA
Spec: {"id","title_top","title_main","title_sub","rungs":[{"emoji","label","num","log10","context","source","color"}],
       "outro_top","outro_line","outro_cta"}
"""
import math, subprocess, sys, json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import engine2 as e2
from engine2 import font, emoji_img, paste_c, scaled_text, back, prog, hexrgb, WHITE, BLACK, YELLOW, RED

W, H, FPS = 1920, 1080, 30
INTRO, RUNG, OUTRO = 180, 180, 180

def background(color, f):
    base = np.array(color, dtype=np.float32)
    yy, xx = np.mgrid[0:H:8, 0:W:8].astype(np.float32)
    r = np.sqrt((xx - W * 0.4) ** 2 + (yy - H * 0.45) ** 2) / (W * 0.6)
    light = 1.18 - 0.55 * np.clip(r, 0, 1)
    stripes = 1 + 0.035 * np.sign(np.sin((xx + yy + f * 5) / 46))
    a = base[None, None, :] * (light * stripes)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)

def text(d, cx, y, s, f, fill=WHITE, stroke=6, max_w=1100):
    return e2.text(d, cx, y, s, f, fill, stroke, max_w)

# rarity meter (log10 scale 0..MAXLOG) on the right
MX, MTOP, MBOT = 1640, 150, 900
TICKS = [(1, "1 in 10"), (3, "thousand"), (6, "million"), (9, "billion"), (12, "trillion"), (18, "quintillion"), (30, "10^30"), (50, "10^50")]

def meter_y(lg, maxlog): return MBOT - (MBOT - MTOP) * min(1, lg / maxlog)

def draw_meter(img, rungs, upto, cur_lg, maxlog, f):
    """The scale zooms out as the odds get rarer (maxlog animates per rung)."""
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([MX - 22, MTOP - 10, MX + 22, MBOT + 10], 22, fill=(20, 20, 26), outline=WHITE, width=4)
    fillh = meter_y(cur_lg, maxlog)
    grad_top = (255, 70, 70); grad_bot = (255, 214, 10)
    for y in range(int(fillh), MBOT + 1, 3):
        t = (MBOT - y) / (MBOT - MTOP)
        c = tuple(int(grad_bot[i] + (grad_top[i] - grad_bot[i]) * t) for i in range(3))
        d.rectangle([MX - 14, y, MX + 14, y + 3], fill=c)
    last_y = 10 ** 9
    for lg, lab in TICKS:
        if lg > maxlog: continue
        y = meter_y(lg, maxlog)
        if last_y - y < 44: continue
        last_y = y
        d.line([MX - 34, y, MX - 24, y], fill=WHITE, width=3)
        tw = d.textlength(lab, font=font(24, "Bold"))
        d.text((MX - 44 - tw, y - 14), lab, font=font(24, "Bold"), fill=WHITE, stroke_width=4, stroke_fill=BLACK)
    for i in range(upto):  # earlier rungs as icons beside the meter
        y = meter_y(rungs[i]["log10"], maxlog)
        x = MX + 60 + (i % 3) * 58
        paste_c(img, emoji_img(rungs[i]["emoji"], 48), x, y)
    d = ImageDraw.Draw(img)
    d.text((MX - 100, MTOP - 72), "RARITY METER", font=font(30, "Black"), fill=YELLOW, stroke_width=5, stroke_fill=BLACK)
    return fillh

def scale(lg): return max(1.6, lg * 1.18)

def fmt_count(v): return f"1 in {int(v):,}"

def render(sp, out, musicpath):
    rungs = sp["rungs"]; n = len(rungs)
    maxlog = max(r["log10"] for r in rungs) * 1.04
    N = INTRO + RUNG * n + OUTRO
    pipe = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "medium", "-crf", "20", out + ".v.mp4"], stdin=subprocess.PIPE)
    sfx = [(0.0, "pop")]
    LX = 760  # centre of the left content column
    for fr in range(N):
        if fr < INTRO:
            # COLD-OPEN HOOK (0-6 s): the rarest rung's number on frame 0, then the cliffhanger
            f = fr; hk = sp["hook"]
            img = background(hexrgb(sp.get("intro_color", "#1F2937")), fr); d = ImageDraw.Draw(img)
            paste_c(img, emoji_img(hk["emoji"], int(240 * (0.85 + 0.15 * back(f / 6)))), W / 2, 230 + 8 * math.sin(f / 5))
            d = ImageDraw.Draw(img)
            text(d, W / 2, 380, hk["top"], font(64), WHITE, max_w=1700)
            fs = 170 if len(hk["num"]) < 12 else 140 if len(hk["num"]) < 18 else 110
            scaled_text(img, W / 2, 600, hk["num"], font(fs), 0.88 + 0.12 * back(f / 6), YELLOW, 10)
            d = ImageDraw.Draw(img)
            text(d, W / 2, 720, hk["bottom"], font(58), WHITE, max_w=1700)
            if f >= 80:
                if f == 80: sfx.append((f / FPS, "whoosh"))
                text(d, W / 2, 860, hk["loop"], font(56), YELLOW, max_w=1700)
            src = "Sources on screen for every number"
        elif fr < INTRO + RUNG * n:
            k = (fr - INTRO) // RUNG; f = (fr - INTRO) % RUNG; r = rungs[k]
            img = background(hexrgb(r["color"]), fr); d = ImageDraw.Draw(img)
            if f == 0: sfx.append((fr / FPS, "whoosh"))
            # level badge
            d.rounded_rectangle([70, 60, 420, 140], 40, fill=BLACK)
            lab = f"LEVEL {k + 1} OF {n}"
            d.text((245 - d.textlength(lab, font=font(40)) / 2, 76), lab, font=font(40), fill=YELLOW)
            # icon
            paste_c(img, emoji_img(r["emoji"], int(230 * (0.7 + 0.3 * back(f / 8)))), LX, 300 + 8 * math.sin(f / 6))
            if f == 2: sfx.append((fr / FPS, "pop"))
            d = ImageDraw.Draw(img)
            if f >= 6: text(d, LX, 450, r["label"], font(68 if len(r["label"]) < 30 else 56), WHITE, max_w=1250)
            # number counts up (log interpolation) then lands
            target = r.get("count")
            if f >= 14:
                t = min(1, (f - 14) / 34)
                if target and t < 1:
                    v = max(1, math.ceil(target ** t))
                    s = fmt_count(v)
                    if f % 3 == 0: sfx.append((fr / FPS, "tick"))
                else:
                    s = r["num"]
                if f == 48: sfx.append((fr / FPS, "ding" if k < n - 1 else "boom"))
                fs = 120 if len(s) < 14 else 92 if len(s) < 20 else 72
                scaled_text(img, LX, 640, s, font(fs), 1.0 if f < 48 else 0.92 + 0.08 * back((f - 48) / 6), YELLOW, 10)
            d = ImageDraw.Draw(img)
            if f >= 62: text(d, LX, 760, r["context"], font(50, "Bold"), WHITE, max_w=1150)
            # meter climbs while the number counts
            prev = rungs[k - 1]["log10"] if k else 0
            cur = prev + (r["log10"] - prev) * prog(f, 14, 34)
            sc_prev = scale(rungs[k - 1]["log10"]) if k else scale(rungs[0]["log10"])
            sc = sc_prev + (scale(r["log10"]) - sc_prev) * prog(f, 14, 34)
            yv = draw_meter(img, rungs, k, cur, sc, f)
            paste_c(img, emoji_img(r["emoji"], 64), MX + 60, yv)
            d = ImageDraw.Draw(img)
            src = r["source"]
        else:
            f = fr - INTRO - RUNG * n; last = rungs[-1]
            img = background(hexrgb(sp.get("outro_color", "#111827")), fr); d = ImageDraw.Draw(img)
            if f == 0: sfx.append((fr / FPS, "whoosh"))
            text(d, W / 2, 110, sp["outro_top"], font(70), YELLOW, max_w=1700)
            paste_c(img, emoji_img(last["emoji"], int(220 * (0.7 + 0.3 * back(f / 8)))), W / 2, 380)
            d = ImageDraw.Draw(img)
            if f >= 20: text(d, W / 2, 540, sp["outro_line"], font(62), WHITE, max_w=1600)
            if f >= 60:
                if f == 60: sfx.append((fr / FPS, "pop"))
                d.rounded_rectangle([W / 2 - 430, 800, W / 2 + 430, 900], 50, fill=(230, 30, 40))
                cta = sp["outro_cta"]
                d.text((W / 2 - d.textlength(cta, font=font(52)) / 2, 818), cta, font=font(52), fill=WHITE)
            src = "Odds Visualized"
        d = ImageDraw.Draw(img)
        d.text((70, 1000), "ODDS VISUALIZED", font=font(32, "Black"), fill=WHITE, stroke_width=5, stroke_fill=BLACK)
        if src != "Odds Visualized":
            sw = d.textlength(src, font=font(26, "SemiBold"))
            d.text((W - 70 - sw, 1004), src, font=font(26, "SemiBold"), fill=(235, 235, 235), stroke_width=4, stroke_fill=BLACK)
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
        N = INTRO + RUNG * len(sp["rungs"]) + OUTRO
        mpath = f"/home/claude/odds/music/gen/{sp['id']}.wav"
        music.make_styled(sp["id"], mpath, seconds=N / FPS + 1, style=music.pick_style(sp["id"]))
        render(sp, f"/home/claude/odds/out3/{sp['id']}.mp4", mpath)
        print("rendered", sp["id"], flush=True)
