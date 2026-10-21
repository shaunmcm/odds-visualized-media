import math
from PIL import Image, ImageDraw, ImageFilter
from common import *

# Stage 1: 10,000 people grid
G1 = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
g = ImageDraw.Draw(G1)
for r in range(100):
    for c in range(100):
        x, y = c * 8 + 4, r * 8 + 4
        g.ellipse([x - 2.5, y - 2.5, x + 2.5, y + 2.5], fill=DOT)

# Stage 2: 29,220 specks, each = 10,000 people (292.2 million)
TILES, COLS, SP, TS = 29220, 166, 6, 4
ROWS = math.ceil(TILES / COLS)
FW, FH = COLS * SP, ROWS * SP
FX, FY = (W - FW) // 2, 520
FIELD = Image.new("RGBA", (FW, FH), (0, 0, 0, 0))
fg = ImageDraw.Draw(FIELD)
for i in range(TILES):
    r, c = divmod(i, COLS)
    fg.rectangle([c * SP, r * SP, c * SP + TS - 1, r * SP + TS - 1], fill=(72, 77, 92))
WIN = 17543
wr, wc = divmod(WIN, COLS)
wx, wy = FX + wc * SP + TS / 2, FY + wr * SP + TS / 2

out = Writer("/home/claude/odds/out/03_powerball.mp4")
for f in range(420):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    hook_a = 1 - prog(f, 215, 12)
    if f < 88:
        y_ = text_c(d, 250, "What lottery odds really look like:", font(58), WHITE, 1 - prog(f, 80, 8)); text_c(d, y_, "This is 10,000 people.", font(64), YELLOW, 1 - prog(f, 80, 8))
    else:
        text_c(d, 250, "This is 292 million.", font(66), WHITE, hook_a * prog(f, 88, 8))
        text_c(d, 335, "Each speck = 10,000 people.", font(48, "Bold"), DIM, hook_a * prog(f, 96, 8))

    if f < 120:
        s = 1 - prog(f, 70, 50) * (1 - TS / 800)
        cx = W / 2 + (FX + TS / 2 - W / 2) * prog(f, 70, 50)
        cy = 1050 + (FY + TS / 2 - 1050) * prog(f, 70, 50)
        sz = max(1, int(800 * s))
        gi = G1.resize((sz, sz), Image.LANCZOS)
        img.paste(gi, (int(cx - sz / 2), int(cy - sz / 2)), gi)
    if f >= 115:
        a = prog(f, 115, 40)
        h = max(1, int(FH * a))
        cr = FIELD.crop((0, 0, FW, h))
        img.paste(cr, (FX, FY), cr)

    if f >= 165:
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gg = ImageDraw.Draw(glow)
        rr = 30 * (1 + 0.15 * math.sin(f / 4))
        gg.ellipse([wx - rr, wy - rr, wx + rr, wy + rr], fill=YELLOW + (140,))
        glow = glow.filter(ImageFilter.GaussianBlur(12))
        if f >= 215:
            img = Image.blend(img, Image.new("RGB", (W, H), BG), 0.72 * prog(f, 215, 15))
        img.paste(glow, (0, 0), glow)
        d = ImageDraw.Draw(img)
        d.ellipse([wx - 6, wy - 6, wx + 6, wy + 6], fill=YELLOW)
        if f < 215:
            t = min(1, (f - 165) / 30)
            pr = 300 * (1 - t) + 30
            d.ellipse([wx - pr, wy - pr, wx + pr, wy + pr], outline=YELLOW, width=3)
            text_c(d, 1590, "Only ONE person wins the jackpot.", font(50), YELLOW, prog(f, 175, 12))

    if f >= 215:
        a = prog(f, 215, 15)
        y = text_c(d, 250, "1 in 292,201,338", font(96), YELLOW, a)
        text_c(d, y, "odds of winning the Powerball jackpot", font(44, "SemiBold"), WHITE, a)
    if f >= 285:
        a = prog(f, 285, 15)
        y = text_c(d, 1150, "Play every drawing for 100 years? (15,600 tickets)", font(52, "Bold"), WHITE, a)
        y = text_c(d, y + 10, "Still about 1 in 18,700.", font(84), RED, prog(f, 320, 15))
    brand(d, "Odds: Powerball official game odds")
    out.add(img)
out.close()
