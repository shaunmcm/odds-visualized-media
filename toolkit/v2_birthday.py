import random
from PIL import Image, ImageDraw
from common import *

random.seed(7)
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
alld = [f"{m} {d}" for m, n in zip(MONTHS, DAYS) for d in range(1, n + 1)]
alld.remove("Mar 14")
dates = random.sample(alld, 21)
A, B = 6, 17
dates.insert(A, "Mar 14"); dates.insert(B, "Mar 14")
assert len(dates) == 23 and dates.count("Mar 14") == 2 and len(set(dates)) == 22

COLS, SX, SY, R = 5, 190, 220, 46
pos = []
for i in range(23):
    r, c = divmod(i, COLS)
    n_in_row = COLS if r < 4 else 3
    x0 = W / 2 - (n_in_row - 1) * SX / 2
    pos.append((x0 + c * SX, 470 + r * SY))

def person(d, x, y, col):
    d.ellipse([x - 22, y - 46, x + 22, y - 2], fill=col)
    d.chord([x - 46, y + 2, x + 46, y + 90], 180, 360, fill=col)

out = Writer("/home/claude/odds/out/02_birthday.mp4")
for f in range(420):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    hook_a = 1 - prog(f, 205, 12)
    text_c(d, 110, "23 strangers in a room.", font(66), WHITE, hook_a)
    text_c(d, 195, "Do two share a birthday?", font(66), YELLOW, hook_a)

    lab = font(32, "Bold")
    for i, (x, y) in enumerate(pos):
        a = prog(f, i * 1.2, 10)
        match = f >= 170 and i in (A, B)
        col = YELLOW if match else DOT
        if a > 0:
            person(d, x, y, tuple(int(BG[k] + (col[k] - BG[k]) * a) for k in range(3)))
        t0 = 30 + i * 5.5
        if f >= t0:
            la = prog(f, t0, 6)
            s = dates[i]
            tw = d.textlength(s, font=lab)
            c2 = YELLOW if match else WHITE
            d.text((x - tw / 2, y + 52), s, font=lab,
                   fill=tuple(int(BG[k] + (c2[k] - BG[k]) * la) for k in range(3)))
    if f >= 170:
        a = prog(f, 170, 15)
        (x1, y1), (x2, y2) = pos[A], pos[B]
        xa, ya = x1, y1 + 120
        xb = x1 + (x2 - x1) * a; yb = ya + (y2 + 120 - ya) * a
        d.line([xa, ya, xb, yb], fill=YELLOW, width=6)

    if f >= 205:
        a = prog(f, 205, 15)
        img = Image.blend(img, Image.new("RGB", (W, H), BG), 0.7 * a)
        d = ImageDraw.Draw(img)
        a = a * (1 - prog(f, 275, 10))
        y = text_c(d, 110, "50.7%", font(150), YELLOW, a)
        text_c(d, y, "chance at least two of 23 people share a birthday", font(44, "SemiBold"), WHITE, a)
    if f >= 275:
        a = prog(f, 285, 15)
        y = text_c(d, 90, "Make it 70 people?", font(56, "Bold"), WHITE, a)
        y = text_c(d, y, "99.9%", font(130), RED, a)
        a2 = prog(f, 325, 15)
        text_c(d, y - 10, "It's not luck. It's math.", font(46, "Bold"), WHITE, a2)
    brand(d, "Birthday problem; assumes 365 equally likely birthdays")
    out.add(img)
out.close()
