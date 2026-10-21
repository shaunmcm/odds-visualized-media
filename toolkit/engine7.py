"""Odds Visualized SHORTS v3 (user blueprint, Oct 17): 15-20 s vertical, 10 items ranked most common -> rarest,
ACCELERATING cards, silence + bass drop on the final item, comment-bait loop frame that matches frame 0.
Modelled on viral outlier "Probability Comparison: Death" (~11M views) + Zack D. Films pacing (answer fast, end, loop).

Spec: {"id","headline","hook":{"left","right"},"items":[{"emoji","label","num","n"}...10],"final_line",
       "cta","yes","no","source","bg_from","bg_to"}
"""
import math, subprocess, sys, json, os
import numpy as np
from PIL import Image, ImageDraw
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import engine2 as e2
import themes
from engine2 import font, emoji_img, paste_c, scaled_text, back, prog, ease, hexrgb, WHITE, BLACK

W, H, FPS, SR = 1080, 1920, 30, 44100
YELLOW = (255, 214, 10); RED = (255, 60, 60)
HOOK = 135                                       # 4.5 s opening (user, Oct 18)
DUR = [48, 45, 42, 39, 36, 33, 30, 30, 30]          # items 1-9, accelerating (1.6 s -> 1.0 s)
GAP = 12                                             # 0.4 s silence/black before the final item
FINAL = 66                                           # final item held 2.2 s
CTA = 54
N = HOOK + sum(DUR) + GAP + FINAL + CTA              # 600 frames = 20.0 s

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def bg(c, f):
    yy, xx = np.mgrid[0:H:8, 0:W:8].astype(np.float32)
    r = np.sqrt((xx - W / 2) ** 2 + (yy - H * 0.45) ** 2) / H
    light = 1.15 - 0.7 * np.clip(r, 0, 1)
    a = np.array(c, np.float32)[None, None, :] * light[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)

def vignette(img, strength):
    if strength <= 0: return img
    yy, xx = np.mgrid[0:H:8, 0:W:8].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    m = np.clip((r - 0.7) / 0.6, 0, 1) * strength
    red = Image.new("RGB", (W, H), (200, 0, 0))
    mask = Image.fromarray((m * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    return Image.composite(red, img, mask)

def fitfont(s, start, maxw=960, w="Black"):
    sz = start
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    while sz > 40 and probe.textlength(s, font=font(sz, w)) + 24 > maxw: sz -= 4
    return font(sz, w)

def center(d, y, s, f, fill=WHITE, stroke=8, mw=960): return e2.text(d, W / 2, y, s, f, fill, stroke, mw)

def count_text(n, t):
    v = max(1, int(round(n ** max(0.0, min(1.0, t)))))
    return f"1 in {v:,}"

def render(sp, out, musicpath):
    items = sp["items"]
    TH = themes.pick(sp["id"]); c0, c1 = TH["c0"], TH["c1"]; ACC = TH["accent"]
    def BG(c, fr): return themes.background(TH, c, fr, W, H)
    pipe = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20", out + ".v.mp4"],
        stdin=subprocess.PIPE)
    sfx = [(0.0, "sub")]
    starts = []; t0 = HOOK
    for d_ in DUR: starts.append(t0); t0 += d_
    gap0 = t0; fin0 = gap0 + GAP; cta0 = fin0 + FINAL
    for i, s in enumerate(starts):
        sfx += [(s / FPS, "whoosh"), ((s + 3) / FPS, "punch")]
        if i in (1, 4, 7): sfx.append(((s - 18) / FPS, "riser"))
        for k in range(3, 12, 3): sfx.append(((s + k) / FPS, "tick"))
    sfx += [(fin0 / FPS, "drop"), ((fin0 + 6) / FPS, "siren"), (cta0 / FPS, "heart"), ((cta0 + 24) / FPS, "heart")]
    for k in range(0, HOOK, 24): sfx.append((k / FPS, "heart"))

    def split_card(img, f, show_odds):
        d = ImageDraw.Draw(img)
        L, R = sp["hook"]["left"], sp["hook"]["right"]
        paste_c(img, emoji_img(L["emoji"], int(380 * (1 + 0.03 * math.sin(f / 3)))), 300, 930)
        paste_c(img, emoji_img(R["emoji"], 200), 800, 960)
        d = ImageDraw.Draw(img)
        d.line([W / 2, 720, W / 2, 1200], fill=WHITE, width=6)
        scaled_text(img, W / 2, 940, "VS", font(70), 1.0, ACC, 8)
        d = ImageDraw.Draw(img)
        e2.text(d, 300, 1150, L.get("label", ""), font(54), WHITE, 7, 480)
        e2.text(d, 800, 1150, R.get("label", ""), font(54), WHITE, 7, 480)
        if False:   # SIMPLE (user Oct 18 5:13pm): no extra explainer line
            center(d, 1290, sp.get("ranked", "10 things ranked: most likely to least likely"), font(48, "Bold"), ACC, 6, 980)
        return ImageDraw.Draw(img)

    for fr in range(N):
        if fr < HOOK:
            img = BG(TH["dark"], fr)
            d = split_card(img, fr, True)
            d = ImageDraw.Draw(img)
            if False: center(d, 238, sp["series"], font(34, "Bold"), (255, 255, 255), 5)
            y_ = center(d, 290, sp["headline"], font(96), ACC, 10, 960)
            if False: center(d, y_ + 10, sp["topic"], font(52, "Bold"), WHITE, 7, 980)
        elif fr < gap0:
            i = max(j for j in range(len(starts)) if starts[j] <= fr); f = fr - starts[i]; it = items[i]
            col = lerp(c0, c1, i / (len(items) - 1))
            img = BG(col, fr); d = ImageDraw.Draw(img)
            center(d, 400, it["label"], font(86), WHITE, 9)
            dx, dy, sc = themes.entry_offset(TH, ease(f / 6))
            img = themes.card_behind(img, TH, W / 2, 830, 520, 520, fr)
            paste_c(img, emoji_img(it["emoji"], max(10, int(360 * sc * (0.85 + 0.15 * back(f / 6))))), W / 2 + dx, 830 + dy)
            txt = count_text(it["n"], f / 9) if f < 9 else it["num"]
            scaled_text(img, W / 2, 1180, txt, fitfont(it["num"], 140), 1.0 if f < 9 else 0.9 + 0.1 * back((f - 9) / 5), ACC, 11)
            d = ImageDraw.Draw(img)
        elif fr < fin0:
            img = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(img)
        elif fr < cta0:
            f = fr - fin0; it = items[-1]
            img = BG(TH["dark"], fr); img = themes.card_behind(img, TH, W / 2, 860, 600, 600, fr); d = ImageDraw.Draw(img)
            center(d, 400, it["label"], font(96), WHITE, 10)
            zoom = 1.0 + 0.12 * (f / FINAL)
            shake = 14 * math.sin(f * 2.3) * max(0, 1 - f / 10)
            paste_c(img, emoji_img(it["emoji"], int(470 * zoom)), W / 2 + shake, 860)
            scaled_text(img, W / 2, 1210, it["num"], fitfont(it["num"], 118), 0.7 + 0.3 * back(f / 6), RED, 12)
            d = ImageDraw.Draw(img)
            if False: center(d, 1330, sp["final_line"], font(56, "Bold"), WHITE, 7)
        else:
            f = fr - cta0
            img = BG(TH["dark"], fr); d = split_card(img, f, False)
            center(d, 300, sp["cta"], font(84), ACC, 9)
            if f >= 8:
                for x, lab, colr in ((300, sp["yes"], (40, 170, 70)), (780, sp["no"], (200, 40, 40))):
                    s = back((f - 8) / 6); w, h = 300 * s, 110 * s
                    d.rounded_rectangle([x - w / 2, 1350 - h / 2, x + w / 2, 1350 + h / 2], 30, fill=colr, outline=WHITE, width=5)
                    tw = d.textlength(lab, font=font(int(60 * max(s, 0.1))))
                    d.text((x - tw / 2, 1350 - 36 * s), lab, font=font(int(60 * max(s, 0.1))), fill=WHITE)
        if not (gap0 <= fr < fin0):
            d = ImageDraw.Draw(img)
            center(d, 190, "ODDS VISUALIZED", font(34, "Black"), WHITE, 5)
            if fr >= cta0 + 14 and sp.get("follow"):
                center(d, 1530, sp["follow"], font(46, "Black"), ACC, 6)
        pipe.stdin.write(img.convert("RGB").tobytes())
    pipe.stdin.close(); pipe.wait()
    mix(sfx, musicpath, N / FPS, out + ".a.wav", (gap0 / FPS, fin0 / FPS))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out + ".v.mp4", "-i", out + ".a.wav", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    os.remove(out + ".v.mp4"); os.remove(out + ".a.wav")

# ---------------- sound design for v3 (all synthesized)
def _env(n, a, d): t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t * d)
def wave(kind):
    r = np.random.default_rng(3)
    if kind == "sub":
        n = int(0.7 * SR); t = np.arange(n) / SR
        return 1.0 * np.sin(2 * np.pi * (45 + 90 * np.exp(-t * 14)) * t) * _env(n, 0.002, 4)
    if kind == "punch":
        n = int(0.16 * SR); t = np.arange(n) / SR
        return 0.9 * np.sin(2 * np.pi * (55 + 140 * np.exp(-t * 40)) * t) * _env(n, 0.001, 18)
    if kind == "drop":
        n = int(1.6 * SR); t = np.arange(n) / SR
        return 1.0 * np.sin(2 * np.pi * np.cumsum(38 + 160 * np.exp(-t * 6)) / SR) * _env(n, 0.002, 1.6)
    if kind == "siren":
        n = int(1.5 * SR); t = np.arange(n) / SR
        f = 700 + 250 * np.sin(2 * np.pi * 1.6 * t)
        return 0.22 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.3) * np.exp(-t * 1.2)
    if kind == "riser":
        n = int(0.6 * SR); t = np.arange(n) / SR
        x = r.standard_normal(n); b, a = butter(2, [1500 / (SR / 2), 9000 / (SR / 2)], "band")
        return 0.35 * lfilter(b, a, x) * (t / t[-1]) ** 2
    if kind == "heart":
        n = int(0.5 * SR); out = np.zeros(n)
        for off, v in ((0, 0.9), (0.18, 0.6)):
            m = int(0.14 * SR); t = np.arange(m) / SR
            i = int(off * SR); out[i:i + m] += v * np.sin(2 * np.pi * (48 + 30 * np.exp(-t * 30)) * t) * np.exp(-t * 22)
        return out
    return e2.sfx_wave(kind)

def mix(sfx, music, dur, out, mute):
    n = int(dur * SR)
    _, m = wavfile.read(music); m = m.astype(np.float32) / 32768
    if m.ndim > 1: m = m.mean(1)
    m = np.tile(m, int(np.ceil(n / len(m))))[:n] * 0.30
    a, b = int(mute[0] * SR), int(mute[1] * SR); m[a:b] = 0          # the beat of silence before the drop
    fx = np.zeros(n)
    for ts, k in sfx:
        w = wave(k); i = int(ts * SR)
        if i < 0 or i >= n: continue
        j = min(n, i + len(w)); fx[i:j] += w[: j - i]
    fx[a:b] = 0
    mix_ = m + 0.6 * fx; mix_ /= max(1.0, np.max(np.abs(mix_)) / 0.95)
    wavfile.write(out, SR, (np.stack([mix_, mix_], 1) * 32767).astype(np.int16))

if __name__ == "__main__":
    import music
    specs = json.load(open(sys.argv[1])); only = set(sys.argv[2:])
    os.makedirs("/home/claude/odds/out5", exist_ok=True)
    for sp in specs:
        if only and sp["id"] not in only: continue
        mp = f"/home/claude/odds/music/gen/{sp['id']}.wav"
        music.make_styled(sp["id"], mp, seconds=N / FPS + 1, style=music.pick_style(sp["id"], pool=["phonk", "tension", "trap", "synthwave", "phonk", "tension"]))
        render(sp, f"/home/claude/odds/out5/{sp['id']}.mp4", mp)
        print("rendered", sp["id"], round(N / FPS, 1), "s", flush=True)
