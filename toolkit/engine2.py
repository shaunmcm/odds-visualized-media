"""Odds Visualized v2: bright, fast, number-first 'Which is rarer?' format with icons and sound effects.

Timeline (30 fps, ~9.5 s):
  0.0-1.7s  HOOK: big icon + the shocking number on frame 0, plus an open loop ("...but what's even rarer?")
  1.7-4.7s  COUNTER: attempts race from 1 to N with ticking, ends on a flash ("HOLE IN ONE!")
  4.7-6.7s  GUESS: "Which is RARER?" two cards + 3-2-1 countdown -> people comment their guess
  6.7-9.5s  REVEAL: numbers drop in, the rarer card is stamped, punchline + follow CTA
"""
import math, subprocess, sys, json, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.io import wavfile

W, H, FPS = 1080, 1920, 30
HOLD = 60  # opening hook held 2 extra seconds (user asked twice on Oct 16 for more reading time)
N = 285 + HOLD
SR = 44100
WHITE = (255, 255, 255); BLACK = (10, 10, 14); YELLOW = (255, 214, 10); RED = (255, 70, 70)
FD = "/usr/share/fonts/opentype/inter/"
EMOJI = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
_fc = {}
def font(sz, w="Black"):
    k = (sz, w)
    if k not in _fc: _fc[k] = ImageFont.truetype(f"{FD}InterDisplay-{w}.otf", sz)
    return _fc[k]

def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3
def back(t):  # overshoot pop
    t = max(0.0, min(1.0, t)); c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def prog(f, s, d): return ease((f - s) / d) if d else float(f >= s)

_ec = {}
def emoji_img(ch, size):
    k = (ch, size)
    if k not in _ec:
        im = Image.new("RGBA", (136, 128), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((0, 0), ch, font=EMOJI, embedded_color=True)
        im = im.crop(im.getbbox() or (0, 0, 136, 128))
        r = size / max(im.size)
        _ec[k] = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
    return _ec[k]

def paste_c(img, im, cx, cy, alpha=1.0):
    if alpha < 1:
        im = im.copy(); a = im.getchannel("A").point(lambda v: int(v * alpha)); im.putalpha(a)
    img.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)

def text(d, cx, y, s, f, fill=WHITE, stroke=7, max_w=980, gap=1.08, anchor_top=True):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= max_w: cur = t
        else: lines.append(cur); cur = w_
    lines.append(cur)
    lh = int(f.size * gap)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        d.text((cx - tw / 2, y + i * lh), ln, font=f, fill=fill, stroke_width=stroke, stroke_fill=BLACK)
    return y + len(lines) * lh

def scaled_text(img, cx, cy, s, f, scale, fill=WHITE, stroke=8):
    """Render text to a layer and scale it (for pops)."""
    tmp = Image.new("RGBA", (1, 1)); dd = ImageDraw.Draw(tmp)
    bb = dd.textbbox((0, 0), s, font=f, stroke_width=stroke)
    lay = Image.new("RGBA", (bb[2] - bb[0] + 4, bb[3] - bb[1] + 4), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((-bb[0] + 2, -bb[1] + 2), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=BLACK)
    if scale != 1:
        lay = lay.resize((max(1, int(lay.width * scale)), max(1, int(lay.height * scale))), Image.LANCZOS)
    paste_c(img, lay, cx, cy)

def hexrgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def background(color, f):
    """Bold topic colour, radial light, slow diagonal stripes for constant motion."""
    base = np.array(color, dtype=np.float32)
    yy, xx = np.mgrid[0:H:8, 0:W:8].astype(np.float32)
    r = np.sqrt((xx - W / 2) ** 2 + (yy - H * 0.42) ** 2) / (H * 0.75)
    light = 1.18 - 0.55 * np.clip(r, 0, 1)
    stripes = 1 + 0.035 * np.sign(np.sin((xx + yy + f * 6) / 46))
    a = base[None, None, :] * (light * stripes)[..., None]
    small = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return small.resize((W, H), Image.BILINEAR)

def card(img, cx, cy, w, h, emo, label, num, reveal, win, f):
    d = ImageDraw.Draw(img)
    x0, y0 = cx - w / 2, cy - h / 2
    glow = win and reveal > 0.5
    if glow:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(g).rounded_rectangle([x0 - 18, y0 - 18, x0 + w + 18, y0 + h + 18], 46, fill=YELLOW + (int(150 + 60 * math.sin(f / 3)),))
        g = g.filter(ImageFilter.GaussianBlur(16)); img.paste(g, (0, 0), g); d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 34, fill=(255, 255, 255), outline=BLACK, width=6)
    paste_c(img, emoji_img(emo, 170), cx, y0 + 130)
    d = ImageDraw.Draw(img)
    text(d, cx, y0 + 235, label, font(44, "Black"), fill=BLACK, stroke=0, max_w=w - 40)
    if reveal > 0:
        f2 = font(54 if len(num) < 14 else 40, "Black")
        col = (200, 30, 30) if win else (40, 40, 48)
        yy = y0 + h - 95 + 30 * (1 - reveal)
        tw = d.textlength(num, font=f2)
        d.text((cx - tw / 2, yy), num, font=f2, fill=col)
    return d

def fmt_count(v):
    return f"{int(v):,}"

def render(sp, out, music):
    color = hexrgb(sp["color"]); n_count = sp["counter_n"]
    frames = []
    pipe = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "medium", "-crf", "20", out + ".v.mp4"], stdin=subprocess.PIPE)
    sfx = []  # (time_s, kind)
    sfx.append((0.0, "pop"))
    A, B = sp["vs"]["a"], sp["vs"]["b"]
    rarer = "a" if A["p"] < B["p"] else "b"
    for fr in range(N):
        img = background(color, fr)
        d = ImageDraw.Draw(img)
        hold_off = 0 if fr < 52 + HOLD else HOLD
        f = fr - hold_off
        # ---------------- HOOK 0-2.7 s
        if fr < 52 + HOLD:
            text(d, W / 2, 250, sp["hook_top"], font(66), YELLOW)
            em = emoji_img(sp["emoji"], 330)
            bob = 10 * math.sin(f / 4)
            paste_c(img, em, W / 2, 720 + bob)
            sc = 0.9 + 0.1 * back(f / 7)
            scaled_text(img, W / 2, 1080, sp["main_num"], font(150 if len(sp["main_num"]) < 12 else 104), sc, WHITE, 10)
            d = ImageDraw.Draw(img)
            if f >= 14:
                text(d, W / 2, 1240, sp["open_loop"], font(54, "Black"), WHITE)
                if f == 14: sfx.append(((f + hold_off) / FPS, "whoosh"))
        # ---------------- COUNTER 52-142
        elif f < 142:
            t = (f - 52) / 80
            v = 1 if t <= 0 else min(n_count, math.ceil(n_count ** min(1, t)))
            text(d, W / 2, 260, sp["counter_title"], font(62), YELLOW)
            shake = 6 * math.sin(f * 2.1) if t < 1 else 0
            paste_c(img, emoji_img(sp["emoji"], 260), W / 2 + shake, 700)
            d = ImageDraw.Draw(img)
            text(d, W / 2, 900, sp["counter_label"], font(56, "Bold"), WHITE)
            fz = 140 if len(fmt_count(n_count)) <= 9 else 96 if len(fmt_count(n_count)) <= 15 else 70
            scaled_text(img, W / 2, 1100, fmt_count(v), font(fz), 1.0, WHITE, 9)
            if f < 132 and f % 3 == 0: sfx.append(((f + hold_off) / FPS, "tick"))
            if f >= 132:
                a = prog(f, 132, 4)
                d = ImageDraw.Draw(img)
                if f == 132: sfx.append(((f + hold_off) / FPS, "ding"))
                scaled_text(img, W / 2, 1330, sp["hit_text"], font(92), 0.8 + 0.2 * back((f - 132) / 6), YELLOW, 10)
        # ---------------- GUESS 142-202
        elif f < 202:
            if f == 142: sfx.append(((f + hold_off) / FPS, "whoosh"))
            text(d, W / 2, 250, sp["vs"]["question"], font(84), YELLOW)
            s1 = prog(f, 142, 8); s2 = prog(f, 148, 8)
            card(img, 275 - 400 * (1 - s1), 900, 430, 560, A["emoji"], A["label"], A["num"], 0, False, f)
            card(img, 805 + 400 * (1 - s2), 900, 430, 560, B["emoji"], B["label"], B["num"], 0, False, f)
            d = ImageDraw.Draw(img)
            scaled_text(img, W / 2, 900, "VS", font(64), 1.0, YELLOW, 8)
            k = 3 - (f - 160) // 14
            if f >= 160 and k >= 1:
                if (f - 160) % 14 == 0: sfx.append(((f + hold_off) / FPS, "beep"))
                scaled_text(img, W / 2, 1380, f"Guess in {k}...", font(80), 0.9 + 0.1 * back(((f - 160) % 14) / 5), WHITE, 9)
            elif f < 160:
                text(d, W / 2, 1340, "Comment your guess!", font(64), WHITE)
        # ---------------- REVEAL 202-285
        else:
            if f == 202: sfx.append(((f + hold_off) / FPS, "boom"))
            text(d, W / 2, 250, sp["vs"]["question"], font(84), YELLOW)
            r = prog(f, 202, 10)
            card(img, 275, 900, 430, 560, A["emoji"], A["label"], A["num"], r, rarer == "a", f)
            card(img, 805, 900, 430, 560, B["emoji"], B["label"], B["num"], r, rarer == "b", f)
            d = ImageDraw.Draw(img)
            if f >= 208:
                cx = 275 if rarer == "a" else 805
                scaled_text(img, cx, 600, "RARER", font(70), 0.7 + 0.3 * back((f - 208) / 6), RED, 9)
                if f == 208: sfx.append(((f + hold_off) / FPS, "pop"))
            if f >= 222:
                d = ImageDraw.Draw(img)
                text(d, W / 2, 1250, sp["punch"], font(64), WHITE)
            if f >= 250:
                d = ImageDraw.Draw(img)
                text(d, W / 2, 1560, "Follow for more odds", font(46, "Bold"), YELLOW, stroke=6)
        # brand + source
        d = ImageDraw.Draw(img)
        text(d, W / 2, 1735, "ODDS VISUALIZED", font(32, "Black"), WHITE, stroke=5)
        text(d, W / 2, 1782, sp["source"], font(24, "SemiBold"), (235, 235, 235), stroke=4)
        pipe.stdin.write(img.convert("RGB").tobytes())
    pipe.stdin.close(); pipe.wait()
    mix_audio(sfx, music, N / FPS, out + ".a.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out + ".v.mp4", "-i", out + ".a.wav",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    import os; os.remove(out + ".v.mp4"); os.remove(out + ".a.wav")

# ---------------- sound design (synthesized, copyright-free)
def _env(n, a, dcy): t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t * dcy)
def sfx_wave(kind):
    rng = np.random.default_rng(len(kind))
    if kind == "pop":
        n = int(0.12 * SR); t = np.arange(n) / SR
        return 0.9 * np.sin(2 * np.pi * (900 * np.exp(-t * 30) + 200) * t) * _env(n, 0.002, 35)
    if kind == "tick":
        n = int(0.03 * SR); t = np.arange(n) / SR
        return 0.25 * np.sin(2 * np.pi * 2400 * t) * _env(n, 0.001, 160)
    if kind == "ding":
        n = int(1.0 * SR); t = np.arange(n) / SR
        return 0.55 * (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 1975 * t) + 0.3 * np.sin(2 * np.pi * 2637 * t)) * _env(n, 0.002, 4)
    if kind == "beep":
        n = int(0.14 * SR); t = np.arange(n) / SR
        return 0.4 * np.sin(2 * np.pi * 880 * t) * _env(n, 0.003, 18)
    if kind == "whoosh":
        n = int(0.4 * SR); x = rng.standard_normal(n)
        from scipy.signal import butter, lfilter
        b, a = butter(2, [800 / (SR / 2), 4000 / (SR / 2)], "band")
        env = np.sin(np.linspace(0, np.pi, n)) ** 2
        return 0.5 * lfilter(b, a, x) * env
    if kind == "boom":
        n = int(0.9 * SR); t = np.arange(n) / SR
        return 1.0 * np.sin(2 * np.pi * (60 + 120 * np.exp(-t * 12)) * t) * _env(n, 0.003, 4.5)
    return np.zeros(1)

def mix_audio(sfx, music, dur, out):
    n = int(dur * SR)
    sr, m = wavfile.read(music); m = m.astype(np.float32) / 32768
    if m.ndim > 1: m = m.mean(1)
    reps = int(np.ceil(n / len(m))); m = np.tile(m, reps)[:n] * 0.32
    fade = int(1.2 * SR); m[-fade:] *= np.linspace(1, 0, fade)
    fx = np.zeros(n)
    for ts, k in sfx:
        w = sfx_wave(k); i = int(ts * SR); j = min(n, i + len(w)); fx[i:j] += w[: j - i]
    mix = m + 0.55 * fx
    mix /= max(1.0, np.max(np.abs(mix)) / 0.95)
    st = np.stack([mix, mix], 1)
    wavfile.write(out, SR, (st * 32767).astype(np.int16))

if __name__ == "__main__":
    specs = json.load(open(sys.argv[1])); only = set(sys.argv[2:])
    tracks = ["bounce", "spark", "pocket", "sunday", "drift", "night"]
    for i, sp in enumerate(specs):
        if only and sp["id"] not in only: continue
        import os, music
        os.makedirs("/home/claude/odds/music/gen", exist_ok=True)
        mpath = f"/home/claude/odds/music/gen/{sp['id']}.wav"  # unique track per video
        music.make_styled(sp["id"], mpath, seconds=N / FPS + 1, style=music.pick_style(sp["id"]))
        render(sp, f"/home/claude/odds/out2/{sp['id']}.mp4", mpath)
        print("rendered", sp["id"], flush=True)
