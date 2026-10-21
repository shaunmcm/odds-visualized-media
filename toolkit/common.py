import subprocess, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
BG = (14, 15, 19)
WHITE = (245, 245, 240)
DIM = (120, 124, 135)
YELLOW = (255, 210, 63)
RED = (255, 77, 77)
DOT = (58, 62, 74)

FD = "/usr/share/fonts/opentype/inter/"
def font(size, weight="Black"):
    return ImageFont.truetype(f"{FD}InterDisplay-{weight}.otf", size)

def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3

def prog(f, start, dur):
    return ease((f - start) / dur) if dur > 0 else float(f >= start)

def text_c(d, y, s, f, fill, alpha=1.0, bg=BG, max_w=960, line_gap=1.15):
    """Centered, wrapped text. Returns bottom y."""
    if alpha <= 0:
        # still compute height
        pass
    col = tuple(int(bg[i] + (fill[i] - bg[i]) * alpha) for i in range(3))
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    lh = int(f.size * line_gap)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        if alpha > 0:
            d.text(((W - tw) / 2, y + i * lh), ln, font=f, fill=col)
    return y + len(lines) * lh

def brand(d, source):
    text_c(d, 1790, "ODDS VISUALIZED", font(30, "Bold"), DIM)
    text_c(d, 1838, source, font(24, "Medium"), (80, 84, 95))

class Writer:
    def __init__(self, path):
        self.p = subprocess.Popen([
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium",
            "-crf", "20", "-c:a", "aac", "-movflags", "+faststart", path],
            stdin=subprocess.PIPE)
    def add(self, img):
        self.p.stdin.write(img.convert("RGB").tobytes())
    def close(self):
        self.p.stdin.close(); self.p.wait()
