import math
from PIL import Image, ImageDraw, ImageFilter
from common import *

COLS, ROWS, SP, R = 102, 150, 8, 2.6
GW, GH = COLS * SP, ROWS * SP
GX, GY = (W - GW) // 2, 420
PICK = (71, 88)

grid = Image.new("RGBA", (GW, GH), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid)
for r in range(ROWS):
    for c in range(COLS):
        x, y = c * SP + SP / 2, r * SP + SP / 2
        gd.ellipse([x - R, y - R, x + R, y + R], fill=DOT)
assert COLS * ROWS == 15300

px = GX + PICK[0] * SP + SP / 2
py = GY + PICK[1] * SP + SP / 2

out = Writer("/home/claude/odds/out/01_lightning.mp4")
N = 400
for f in range(N):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Hook (visible from frame 0)
    hook_a = 1 - prog(f, 150, 12)
    text_c(d, 120, "One of these 15,300 people", font(64), WHITE, hook_a)
    text_c(d, 200, "gets struck by lightning.", font(64), YELLOW, hook_a)

    # Grid reveal top-to-bottom
    rv = prog(f, 0, 45)
    h = int(GH * rv)
    if h > 0:
        img.paste(grid.crop((0, 0, GW, h)), (GX, GY), grid.crop((0, 0, GW, h)))

    # Search pulse then strike
    if 50 <= f < 95:
        t = (f - 50) / 45
        rr = 40 + 260 * (1 - t)
        d.ellipse([px - rr, py - rr, px + rr, py + rr], outline=YELLOW, width=3)
    if f >= 95:
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        g = ImageDraw.Draw(glow)
        pulse = 1 + 0.15 * math.sin(f / 4)
        gr = 34 * pulse
        g.ellipse([px - gr, py - gr, px + gr, py + gr], fill=YELLOW + (110,))
        glow = glow.filter(ImageFilter.GaussianBlur(14))
        img.paste(glow, (0, 0), glow)
        d = ImageDraw.Draw(img)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=YELLOW)
    # flash
    if 95 <= f < 103:
        a = 1 - (f - 95) / 8
        fl = Image.new("RGB", (W, H), (255, 255, 235))
        img = Image.blend(img, fl, 0.75 * a)
        d = ImageDraw.Draw(img)

    # Stat card
    if f >= 150:
        a = prog(f, 150, 15)
        ov = Image.new("RGB", (W, H), BG)
        img = Image.blend(img, ov, (0.55 + 0.25 * prog(f, 235, 15)) * a)
        d = ImageDraw.Draw(img)
        y = text_c(d, 110, "1 in 15,300", font(120), YELLOW, a)
        text_c(d, y + 5, "lifetime odds of being struck by lightning in the US", font(42, "SemiBold"), WHITE, a)

        # keep the struck dot bright on top of the dimmed grid
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        g = ImageDraw.Draw(glow)
        gr = 34 * (1 + 0.15 * math.sin(f / 4))
        g.ellipse([px - gr, py - gr, px + gr, py + gr], fill=YELLOW + (130,))
        glow = glow.filter(ImageFilter.GaussianBlur(14))
        img.paste(glow, (0, 0), glow)
        d = ImageDraw.Draw(img)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=YELLOW)

    # Twist
    if f >= 235:
        a = prog(f, 235, 15)
        y = text_c(d, 1270, "Winning the Powerball jackpot?", font(48, "Bold"), WHITE, a)
        y = text_c(d, y, "1 in 292,201,338", font(72), RED, a)
        a2 = prog(f, 285, 15)
        text_c(d, y + 20, "You're about 19,000x more likely to get struck by lightning.", font(44, "Bold"), WHITE, a2)

    brand(d, "Sources: National Weather Service; Powerball")
    out.add(img)
out.close()
