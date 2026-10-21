"""Odds, Visualized video engine: renders a fact spec into a 1080x1920 MP4 with music."""
import math, subprocess, sys, json, random
from PIL import Image, ImageDraw, ImageFilter
from common import W, H, FPS, BG, WHITE, DIM, YELLOW, RED, DOT, font, ease, prog, text_c, brand

N_FRAMES = 420  # 14 s
VIS_TOP, VIS_H, VIS_W = 520, 1030, 900
TOP_Y = 250  # clear of the Instagram/TikTok top bar

class Writer:
    def __init__(self, path, music, seconds):
        self.p = subprocess.Popen([
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
            "-stream_loop", "-1", "-i", music,
            "-filter_complex", f"[1:a]volume=0.55,afade=t=in:d=0.4,afade=t=out:st={seconds-1.6}:d=1.6[a]",
            "-map", "0:v", "-map", "[a]", "-t", str(seconds),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", path], stdin=subprocess.PIPE)
    def add(self, img): self.p.stdin.write(img.convert("RGB").tobytes())
    def close(self):
        self.p.stdin.close(); self.p.wait()
        assert self.p.returncode == 0, "ffmpeg failed"

def glow_dot(img, x, y, r=8, g=34, f=0, col=YELLOW):
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    gr = g * (1 + 0.15 * math.sin(f / 4))
    gd.ellipse([x - gr, y - gr, x + gr, y + gr], fill=col + (130,))
    gl = gl.filter(ImageFilter.GaussianBlur(g * 0.4))
    img.paste(gl, (0, 0), gl)
    ImageDraw.Draw(img).ellipse([x - r, y - r, x + r, y + r], fill=col)

def fit_grid(n, w=VIS_W, h=VIS_H):
    cols = max(1, math.ceil(math.sqrt(n * w / h)))
    rows = math.ceil(n / cols)
    sp = min(w / cols, h / rows)
    return cols, rows, sp

# ---------------------------------------------------------------- visuals
class GridVis:
    """n dots; one (or a few) lights up."""
    def __init__(s, spec):
        s.n = spec["n"]; s.hi = spec.get("highlight", [int(s.n * 0.61)])
        s.cols, s.rows, s.sp = fit_grid(s.n)
        gw, gh = s.cols * s.sp, s.rows * s.sp
        s.x0, s.y0 = (W - gw) / 2, VIS_TOP + (VIS_H - gh) / 2
        r = max(0.9, s.sp * 0.32)
        s.base = Image.new("RGBA", (int(gw) + 2, int(gh) + 2), (0, 0, 0, 0))
        d = ImageDraw.Draw(s.base)
        shape = spec.get("shape", "dot")
        for i in range(s.n):
            rr, c = divmod(i, s.cols)
            x, y = c * s.sp + s.sp / 2, rr * s.sp + s.sp / 2
            if shape == "square":
                d.rectangle([x - r, y - r, x + r, y + r], fill=DOT)
            else:
                d.ellipse([x - r, y - r, x + r, y + r], fill=DOT)
        s.reveal_at = spec.get("reveal_at", 95)
    def pos(s, i):
        rr, c = divmod(i, s.cols)
        return s.x0 + c * s.sp + s.sp / 2, s.y0 + rr * s.sp + s.sp / 2
    def draw(s, img, f):
        h = int(s.base.height * prog(f, 0, 45))
        if h > 0:
            cr = s.base.crop((0, 0, s.base.width, h)); img.paste(cr, (int(s.x0), int(s.y0)), cr)
        d = ImageDraw.Draw(img)
        if s.reveal_at - 45 <= f < s.reveal_at:
            t = (f - s.reveal_at + 45) / 45
            for i in s.hi:
                x, y = s.pos(i); rr = 40 + 260 * (1 - t)
                d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=YELLOW, width=3)
        return img
    def top(s, img, f):
        if f >= s.reveal_at:
            for i in s.hi:
                x, y = s.pos(i); glow_dot(img, x, y, f=f)
        return img

class PeopleVis:
    """n person icons; a subset lights up, optional labels."""
    def __init__(s, spec):
        s.n = spec["n"]; s.hi = set(spec["highlight"]); s.labels = spec.get("labels")
        s.cols, s.rows, s.sp = fit_grid(s.n, VIS_W, VIS_H - 80)
        s.x0 = (W - s.cols * s.sp) / 2; s.y0 = VIS_TOP + (VIS_H - s.rows * s.sp) / 2
        s.reveal_at = spec.get("reveal_at", 120)
    def person(s, d, x, y, k, col):
        d.ellipse([x - 0.24 * k, y - 0.5 * k, x + 0.24 * k, y - 0.02 * k], fill=col)
        d.chord([x - 0.5 * k, y + 0.02 * k, x + 0.5 * k, y + 0.98 * k], 180, 360, fill=col)
    def draw(s, img, f):
        d = ImageDraw.Draw(img); k = s.sp * 0.5
        lab = font(max(14, int(s.sp * 0.17)), "Bold")
        for i in range(s.n):
            r, c = divmod(i, s.cols)
            x, y = s.x0 + c * s.sp + s.sp / 2, s.y0 + r * s.sp + s.sp * 0.42
            a = prog(f, i * (40 / s.n), 10)
            lit = f >= s.reveal_at and i in s.hi
            col = YELLOW if lit else DOT
            if a > 0:
                s.person(d, x, y, k, tuple(int(BG[j] + (col[j] - BG[j]) * a) for j in range(3)))
            if s.labels and f >= 30 + i * 4:
                la = prog(f, 30 + i * 4, 6); t = s.labels[i]; c2 = YELLOW if lit else WHITE
                d.text((x - d.textlength(t, font=lab) / 2, y + 0.55 * k), t, font=lab,
                       fill=tuple(int(BG[j] + (c2[j] - BG[j]) * la) for j in range(3)))
        return img
    def top(s, img, f): return img

class BigNumVis:
    """A huge number types itself out, digit by digit."""
    def __init__(s, spec):
        s.num = spec["number"]; s.caption = spec.get("caption", "")
    def draw(s, img, f):
        d = ImageDraw.Draw(img)
        k = int(len(s.num) * prog(f, 10, 110))
        shown = s.num[:k]
        if k < len(s.num) and k > 0:
            shown += str(random.Random(f).randint(0, 9))
        fz = 92 if len(s.num) <= 14 else 74 if len(s.num) <= 30 else 60
        # wrap the digits into lines
        y = 900 - (len(s.num) // 18) * 40
        f0 = font(fz)
        line = ""; lines = []
        toks = [t + "," for t in shown.split(",")[:-1]] + [shown.split(",")[-1]] if "," in s.num else list(shown)
        for ch in toks:
            if d.textlength(line + ch, font=f0) > 940: lines.append(line); line = ch
            else: line += ch
        lines.append(line)
        for i, ln in enumerate(lines):
            d.text(((W - d.textlength(ln, font=f0)) / 2, y + i * fz * 1.1), ln, font=f0, fill=YELLOW)
        if s.caption and f > 125:
            text_c(d, y + len(lines) * fz * 1.1 + 30, s.caption, font(44, "SemiBold"), WHITE, prog(f, 125, 12))
        return img
    def top(s, img, f): return img

class CoinVis:
    """k coins flip in a row, all heads; running odds counter."""
    def __init__(s, spec):
        s.k = spec["k"]; s.reveal_at = 30 + s.k * 11 + 10; s.stat_at = spec.get("stat_at", 160)
    def draw(s, img, f):
        d = ImageDraw.Draw(img); cols = 5; sp = 180; r = 70
        for i in range(s.k):
            t0 = 30 + i * 11
            if f < t0: continue
            row, c = divmod(i, cols)
            x = W / 2 - (cols - 1) * sp / 2 + c * sp; y = 800 + row * 200
            t = min(1, (f - t0) / 9)
            sq = abs(math.cos(t * math.pi * 2)) if t < 1 else 1  # flip squash
            rx = max(3, r * sq)
            d.ellipse([x - rx, y - r, x + rx, y + r], fill=YELLOW if t >= 1 else (200, 160, 40))
            if t >= 1:
                fh = font(64)
                d.text((x - d.textlength("H", font=fh) / 2, y - 40), "H", font=fh, fill=BG)
        done = min(s.k, max(0, (f - 30) // 11 + 1)) if f >= 39 else 0
        ca = 1 - prog(f, s.stat_at, 10)
        if done and ca > 0:
            text_c(d, 1260, f"1 in {2 ** done:,}", font(80), WHITE, ca)
            text_c(d, 1360, f"{done} head{'s' if done > 1 else ''} in a row", font(44, "SemiBold"), DIM, ca)
        return img
    def top(s, img, f): return img

VIS = {"grid": GridVis, "people": PeopleVis, "bignum": BigNumVis, "coins": CoinVis}

# ---------------------------------------------------------------- render
def render(spec, out_path, music):
    random.seed(spec["id"])
    vis = VIS[spec["type"]](spec)
    STAT, TWIST = spec.get("stat_at", 160), spec.get("twist_at", 245)
    w = Writer(out_path, music, N_FRAMES / FPS)
    for f in range(N_FRAMES):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        ha = 1 - prog(f, STAT, 12)
        y = text_c(d, TOP_Y, spec["hook"][0], font(64), WHITE, ha)
        if len(spec["hook"]) > 1:
            y2 = text_c(d, y, spec["hook"][1], font(64), YELLOW, ha)
            # animated highlight bar under the yellow line: sweeps in, then pulses (motion in the first 3 s)
            if ha > 0:
                tw = min(960, d.textlength(spec["hook"][1], font=font(64)))
                sweep = prog(f, 0, 18)
                bw = tw * sweep * (1 + 0.04 * math.sin(f / 5))
                x0 = (W - tw) / 2
                d.rectangle([x0, y2 + 2, x0 + bw, y2 + 9], fill=tuple(int(BG[j] + (YELLOW[j] - BG[j]) * ha) for j in range(3)))
            y = y2 + 12
        if spec.get("hook_note"):
            y = text_c(d, y + 4, spec["hook_note"], font(38, "SemiBold"), DIM, ha)
        ta = prog(f, 45, 12) * (1 - prog(f, STAT - 15, 12))
        if ta > 0:
            text_c(d, 1575, spec.get("tease", "Wait for the twist..."), font(40, "Bold"), WHITE, ta * (0.75 + 0.25 * math.sin(f / 6)))
        img = vis.draw(img, f)
        if f >= STAT:
            a = prog(f, STAT, 15)
            dim = 0.55 + 0.25 * prog(f, TWIST, 15)
            if spec["type"] in ("bignum", "coins"): dim = 0.82
            img = Image.blend(img, Image.new("RGB", (W, H), BG), dim * a)
        img = vis.top(img, f)
        d = ImageDraw.Draw(img)
        if f >= STAT:
            a = prog(f, STAT, 15)
            y = text_c(d, TOP_Y, spec["stat"], font(110 if len(spec["stat"]) < 14 else 84), YELLOW, a)
            text_c(d, y + 5, spec["stat_sub"], font(42, "SemiBold"), WHITE, a)
        if f >= TWIST:
            y = 1220
            for i, (txt, style) in enumerate(spec["twist"]):
                a = prog(f, TWIST + i * 30, 15)
                fz, wt, col = {"q": (48, "Bold", WHITE), "big": (78, "Black", RED),
                               "line": (44, "Bold", WHITE)}[style]
                y = text_c(d, y, txt, font(fz, wt), col, a) + 12
        brand(d, spec["source"])
        w.add(img)
    w.close()

if __name__ == "__main__":
    specs = json.load(open(sys.argv[1]))
    tracks = ["sunday", "pocket", "drift", "bounce", "night", "spark"]
    only = set(sys.argv[2:])
    for i, sp in enumerate(specs):
        if only and sp["id"] not in only: continue
        mus = f"/home/claude/odds/music/{tracks[i % len(tracks)]}.wav"
        render(sp, f"/home/claude/odds/out/{sp['id']}.mp4", mus)
        print("rendered", sp["id"], flush=True)
