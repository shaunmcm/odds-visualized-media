"""Monday Oct 19 content. Numbers are computed here (pure math) or copied from the named official source."""
import json, math
D = "20261019"
NAMES = [(1e33, "decillion"), (1e30, "nonillion"), (1e27, "octillion"), (1e24, "septillion"), (1e21, "sextillion"),
         (1e18, "quintillion"), (1e15, "quadrillion"), (1e12, "trillion"), (1e9, "billion"), (1e6, "million")]

def words(n):
    """Plain-word number: 1,024 / 1.2 million / 9.2 quintillion."""
    for v, w in NAMES:
        if n >= v:
            x = n / v
            s = f"{x:.1f}".rstrip("0").rstrip(".") if x < 100 else f"{x:.0f}"
            return f"{s} {w}"
    return f"{round(n):,}"

def odds(n): return f"1 in {words(n)}"

def years(days):
    y = days / 365.25
    if 330 < days < 400: return "1 year"
    if days < 14: return f"{round(days)} days"
    if days < 60: return f"{round(days / 7)} weeks"
    if days < 730: return f"{round(days / 30.44)} months"
    if y < 1e6: return f"{y:,.0f} years" if y >= 10 else f"{y:.1f} years"
    return f"{words(y)} years"

# ------------------------------------------------------------------ SHORTS (Parts 10-14 + 3 backlog)
def short(id_, part, headline, L, R, items, cta, src):
    its = [dict(emoji=e, label=l, num=odds(n), n=n) for e, l, n in items]
    its[-1]["label"] = its[-1]["label"].upper(); its[-1]["num"] = its[-1]["num"].upper()
    return dict(id=id_, series=f"RARER THAN YOU THINK · PART {part}", follow=f"Follow for Part {part + 1}",
                headline=headline, topic="", hook=dict(left=dict(emoji=L[0], label=L[1]), right=dict(emoji=R[0], label=R[1])),
                ranked="", items=its, final_line="", cta=cta, yes="YES", no="NO", source=src)

PB = [("🔴", "Just the Powerball", 38.32), ("1️⃣", "1 number + Powerball", 91.98), ("3️⃣", "3 white balls", 579.76),
      ("2️⃣", "2 numbers + Powerball", 701.33), ("🎯", "3 numbers + Powerball", 14494.11), ("4️⃣", "4 white balls", 36525.17),
      ("💵", "4 numbers + Powerball", 913129.18), ("💰", "All 5 white balls", 11688053.52), ("🏆", "The jackpot", 292201338),
      ("🤯", "Jackpot twice in a row", 292201338 ** 2)]

shorts = [
    short("S10_rarer", 10, "Which is rarer?", ("🍀", "Four-leaf clover"), ("🏀", "Perfect bracket"), [
        ("✋", "Being left-handed", 10), ("👯", "Having twins", 32), ("📅", "Born on Feb 29", 1461),
        ("🍀", "Four-leaf clover", 10000), ("⛳", "Hole-in-one", 12500), ("🃏", "Royal flush", 649740),
        ("🪙", "20 heads in a row", 2 ** 20), ("⚡", "Lightning this year", 1222000), ("🎟️", "Powerball jackpot", 292201338),
        ("🏀", "Perfect March bracket", 2 ** 63)], "Called the order?",
        "Sources: CDC twin birth rate; NWS lightning; National Hole-in-One Registry; Powerball.com; math"),
    short("S11_guess", 11, "Guess my secret.", ("🪙", "My coin flip"), ("🔐", "My password"), [
        ("🪙", "My coin flip", 2), ("🎲", "My dice roll", 6), ("🗓️", "My birth month", 12), ("🃏", "My card", 52),
        ("🎂", "My birthday", 365), ("🔢", "My 4-digit PIN", 10 ** 4), ("📆", "Birthday + year", 36525),
        ("📱", "My 6-digit code", 10 ** 6), ("☎️", "My phone number", 10 ** 10), ("🔐", "My 16-letter password", 26 ** 16)],
        "Could you guess one?", "Pure math: possible combinations"),
    short("S12_d20", 12, "Roll a natural 20.", ("🎲", "One nat 20"), ("🐉", "Ten in a row"), [
        ("🎲", "One natural 20", 20), ("✌️", "Two in a row", 20 ** 2), ("🤞", "Three in a row", 20 ** 3),
        ("😮", "Four in a row", 20 ** 4), ("😳", "Five in a row", 20 ** 5), ("😱", "Six in a row", 20 ** 6),
        ("🧙", "Seven in a row", 20 ** 7), ("🔥", "Eight in a row", 20 ** 8), ("🌋", "Nine in a row", 20 ** 9),
        ("🐉", "Ten in a row", 20 ** 10)], "Ever rolled two nat 20s?", "Pure math: (1/20)^n"),
    short("S13_heads", 13, "Flip heads. Forever.", ("🪙", "One heads"), ("😵", "100 heads"), [
        ("🪙", "1 heads", 2), ("✌️", "3 heads in a row", 2 ** 3), ("🖐️", "5 in a row", 2 ** 5), ("🔟", "10 in a row", 2 ** 10),
        ("😮", "15 in a row", 2 ** 15), ("😳", "20 in a row", 2 ** 20), ("😱", "25 in a row", 2 ** 25),
        ("🤯", "30 in a row", 2 ** 30), ("🌌", "50 in a row", 2 ** 50), ("😵", "100 in a row", 2 ** 100)],
        "Ever flipped 5 in a row?", "Pure math: (1/2)^n"),
    short("S14_powerball", 14, "Every Powerball prize.", ("🔴", "Just the red ball"), ("🏆", "The jackpot"), PB,
          "Would you still play?", "Source: Powerball.com official odds"),
    # backlog
    short("S15_bracket", 15, "Pick every winner.", ("🏀", "One game"), ("🏆", "Whole bracket"), [
        ("🏀", "Pick 1 game", 2), ("✌️", "Pick 2 games", 4), ("🤞", "Pick 3 games", 8), ("🖐️", "Pick 5 games", 32),
        ("🔟", "Pick 10 games", 2 ** 10), ("😮", "Pick 16 games", 2 ** 16), ("😳", "Pick 20 games", 2 ** 20),
        ("😱", "Whole first round", 2 ** 32), ("🤯", "Pick 48 games", 2 ** 48), ("🏆", "Perfect bracket", 2 ** 63)],
        "Ever picked 10 straight?", "Pure math: coin-flip picks, (1/2)^n"),
    short("S16_arrange", 16, "Put them in order.", ("📚", "2 books"), ("🌀", "25 books"), [
        ("📚", "2 books", math.factorial(2)), ("📗", "3 books", math.factorial(3)), ("📘", "4 books", math.factorial(4)),
        ("📙", "5 books", math.factorial(5)), ("📕", "6 books", math.factorial(6)), ("🗂️", "8 books", math.factorial(8)),
        ("🗃️", "10 books", math.factorial(10)), ("🏛️", "13 books", math.factorial(13)), ("🌍", "20 books", math.factorial(20)),
        ("🌀", "25 books", math.factorial(25))], "Could you get 5 right?", "Pure math: n! orderings, random shelf"),
    short("S17_casino", 17, "Casino odds, ranked.", ("🎰", "Red on roulette"), ("💎", "Royal flush"), [
        ("🔴", "Red on roulette", 38 / 18), ("🃏", "Blackjack on deal", 1 / (4 * 16 * 2 / (52 * 51))),
        ("🐍", "Snake eyes", 36), ("🎡", "One roulette number", 38), ("🎡", "Same number twice", 38 ** 2),
        ("🎲", "Yahtzee in one roll", 1296), ("4️⃣", "Four of a kind", 4165), ("🌊", "Straight flush", 72193),
        ("🎡", "Same number 3 times", 38 ** 3), ("💎", "Royal flush", 649740)], "Would you bet on it?",
        "Math: American roulette (38 slots), 52-card deck, 5-card poker hands"),
]
# fix ordering of casino items by odds
c = shorts[-1]["items"]; last = c[-1]
body = sorted(c[:-1], key=lambda it: it["n"]); allc = sorted(body + [last], key=lambda it: it["n"])
for it in allc: it["label"] = it["label"].title() if it["label"].isupper() else it["label"]; it["num"] = it["num"].replace("1 IN", "1 in").lower().replace("1 in", "1 in")
allc[-1]["label"] = allc[-1]["label"].upper(); allc[-1]["num"] = allc[-1]["num"].upper()
shorts[-1]["items"] = allc
shorts[-1]["hook"]["right"] = dict(emoji=allc[-1]["emoji"], label=allc[-1]["label"].title())
json.dump(shorts, open(f"specs_v3s_{D}.json", "w"), indent=1, ensure_ascii=False)

def last(sp): return sp["items"][-1]
posts = [
    dict(id="S10_rarer",
         caption=f"Which is rarer: a four-leaf clover or a perfect March bracket? 🍀\nDid you call the order? Comment YES or NO 👇\nSend this to the friend who always says \"what are the odds\".\nPart 10 of Rarer Than You Think. Follow for Part 11.\n\n#fyp #probability #whichisrarer #odds #oddsvisualized",
         yt_title="Four-Leaf Clover vs Perfect Bracket: Which Is Rarer?",
         yt_description="Which is rarer? 10 rare things ranked, from being left-handed (1 in 10) to a perfect March Madness bracket (1 in 9.2 quintillion).\nDid you call the order? YES or NO in the comments.\n\nSources: CDC (twin births), NWS (lightning), National Hole-in-One Registry, Powerball.com, coin and card math.\n\n#Shorts #fyp #probability",
         yt_tags=["which is rarer", "rarest things ranked", "four leaf clover odds", "perfect bracket odds", "hole in one odds", "royal flush odds", "struck by lightning odds", "odds visualized", "rarer than you think"]),
    dict(id="S11_guess",
         caption=f"Guessing odds: my coin flip is 1 in 2, my 16-letter password is {odds(26**16)} 🔐\nCould you guess even one? Comment YES or NO 👇\nSend this to the friend who still uses 1234.\nPart 11 of Rarer Than You Think. Follow for Part 12.\n\n#fyp #probability #passwords #cybersecurity #oddsvisualized",
         yt_title=f"Guess My 16-Letter Password: {odds(26**16).title()}",
         yt_description=f"Guessing odds ranked: a coin flip (1 in 2), a birthday (1 in 365), a 4-digit PIN (1 in 10,000) up to a 16-letter password ({odds(26**16)}).\nCould you guess one? YES or NO in the comments.\n\nSource: pure math (possible combinations).\n\n#Shorts #fyp #passwords",
         yt_tags=["guessing odds", "pin code odds", "password combinations", "how hard to guess a password", "birthday odds", "probability explained", "odds visualized", "rarer than you think"]),
    dict(id="S12_d20",
         caption=f"D20 odds: rolling ten natural 20s in a row is {odds(20**10)} 🐉\nEver rolled two nat 20s? Comment YES or NO 👇\nSend this to your D&D group.\nPart 12 of Rarer Than You Think. Follow for Part 13.\n\n#fyp #dnd #dice #probability #oddsvisualized",
         yt_title=f"Ten Natural 20s in a Row Is {odds(20**10).title()}",
         yt_description=f"Natural 20 odds ranked: one nat 20 is 1 in 20, three in a row is 1 in 8,000, ten in a row is {odds(20**10)}.\nEver rolled two in a row? YES or NO in the comments.\n\nSource: dice math, (1/20)^n.\n\n#Shorts #fyp #dnd",
         yt_tags=["natural 20 odds", "d20 probability", "nat 20 in a row", "dnd dice odds", "dice probability", "critical hit odds", "odds visualized", "rarer than you think"]),
    dict(id="S13_heads",
         caption=f"Coin flip odds: 100 heads in a row is {odds(2**100)} 🪙\nEver flipped 5 in a row? Comment YES or NO 👇\nSend this to someone who calls heads every time.\nPart 13 of Rarer Than You Think. Follow for Part 14.\n\n#fyp #probability #coinflip #math #oddsvisualized",
         yt_title=f"100 Heads in a Row Is {odds(2**100).title()}",
         yt_description=f"Coin flip odds ranked: 3 heads in a row (1 in 8), 10 in a row (1 in 1,024), 30 in a row ({odds(2**30)}) and 100 in a row ({odds(2**100)}).\nEver flipped 5 in a row? YES or NO in the comments.\n\nSource: coin math, (1/2)^n.\n\n#Shorts #fyp #coinflip",
         yt_tags=["coin flip odds", "heads in a row odds", "100 heads in a row", "coin toss probability", "probability explained", "math facts", "odds visualized", "rarer than you think"]),
    dict(id="S14_powerball",
         caption=f"Powerball odds for every prize, from just the red ball (1 in 38) to the jackpot (1 in 292 million) 🎟️\nWould you still play? Comment YES or NO 👇\nSend this to the friend who buys a ticket every week.\nPart 14 of Rarer Than You Think. Follow for Part 15.\n\n#fyp #powerball #lottery #probability #oddsvisualized",
         yt_title="Every Powerball Prize, Ranked by Odds",
         yt_description="Official Powerball odds for every prize: just the Powerball is 1 in 38.32, five white balls is 1 in 11.7 million, the jackpot is 1 in 292.2 million, and the jackpot twice in a row would be 1 in 85 quadrillion.\nWould you still play? YES or NO in the comments.\n\nSource: Powerball.com prize chart.\n\n#Shorts #fyp #powerball",
         yt_tags=["powerball odds", "powerball prize odds", "odds of winning powerball", "lottery odds", "powerball jackpot odds", "lottery math", "odds visualized", "rarer than you think"]),
    dict(id="S15_bracket",
         caption=f"March Madness odds: a perfect bracket is {odds(2**63)} 🏀\nEver picked 10 games straight? Comment YES or NO 👇\nSend this to your bracket group chat.\nPart 15 of Rarer Than You Think. Follow for Part 16.\n\n#fyp #marchmadness #bracket #probability #oddsvisualized",
         yt_title=f"A Perfect Bracket Is {odds(2**63).title()} (Coin-Flip Picks)",
         yt_description=f"Bracket odds if every pick is a coin flip: 10 games straight is 1 in 1,024, the whole first round is {odds(2**32)}, a perfect bracket is {odds(2**63)}.\nEver picked 10 straight? YES or NO in the comments.\n\nSource: math, (1/2)^63.\n\n#Shorts #fyp #marchmadness",
         yt_tags=["perfect bracket odds", "march madness odds", "bracket probability", "ncaa bracket odds", "9.2 quintillion", "probability explained", "odds visualized", "rarer than you think"]),
    dict(id="S16_arrange",
         caption=f"Shelf odds: 25 books landing in the right order by chance is {odds(math.factorial(25))} 📚\nCould you get 5 right? Comment YES or NO 👇\nSend this to the friend who alphabetizes everything.\nPart 16 of Rarer Than You Think. Follow for Part 17.\n\n#fyp #probability #math #books #oddsvisualized",
         yt_title=f"25 Books in Order by Chance: {odds(math.factorial(25)).title()}",
         yt_description=f"How many ways can books sit on a shelf? 5 books: 120. 10 books: 3.6 million. 25 books: {words(math.factorial(25))}.\nCould you get 5 right? YES or NO in the comments.\n\nSource: math (n factorial).\n\n#Shorts #fyp #math",
         yt_tags=["factorial explained", "permutations", "how many ways to arrange", "probability explained", "math facts", "random order odds", "odds visualized", "rarer than you think"]),
    dict(id="S17_casino",
         caption=f"Casino odds ranked: red on roulette is about 1 in 2, a royal flush is 1 in 649,740 🎰\nWould you bet on any of these? Comment YES or NO 👇\nSend this to your Vegas friend.\nPart 17 of Rarer Than You Think. Follow for Part 18.\n\n#fyp #casino #probability #poker #oddsvisualized",
         yt_title="Casino Odds Ranked: Roulette to Royal Flush",
         yt_description="Casino odds ranked, from red on an American roulette wheel (18 of 38) to a royal flush (1 in 649,740).\nWould you bet on any? YES or NO in the comments.\n\nSource: roulette, dice and 5-card poker math.\n\n#Shorts #fyp #casino",
         yt_tags=["casino odds", "roulette odds", "royal flush odds", "blackjack odds", "yahtzee odds", "gambling math", "odds visualized", "rarer than you think"]),
]
json.dump(posts, open(f"posts_v3s_{D}.json", "w"), indent=1, ensure_ascii=False)

# ------------------------------------------------------------------ LONG-FORM
road = dict(id="L06_games", hook=dict(top="Game odds, easy to impossible.", big="IMPOSSIBLE", bottom="", ask="Guess the last one.", explain=""),
    stops=[dict(emoji=e, label=l, num=odds(n), source="") for e, l, n in [
        ("🎲", "Roll a six", 6), ("🃏", "Blackjack on the deal", 1 / (4 * 16 * 2 / (52 * 51))), ("🐍", "Snake eyes", 36),
        ("🎡", "Hit your roulette number", 38), ("🎯", "Yahtzee in one roll", 1296), ("4️⃣", "Four of a kind", 4165),
        ("🌊", "A straight flush", 72193), ("💎", "A royal flush", 649740), ("🪙", "20 heads in a row", 2 ** 20),
        ("🎟️", "Win the Powerball", 292201338), ("🏀", "A perfect bracket", 2 ** 63)]],
    payoff=dict(emoji="🧩", label="Solve a Rubik's cube by luck", num=odds(43252003274489856000), line="", source=""))
json.dump([road], open(f"specs_road_{D}.json", "w"), indent=1, ensure_ascii=False)
lw = [("🪙", "Guess a coin flip", 2), ("📅", "Guess the weekday I was born", 7), ("🗓️", "Guess my birth month", 12),
      ("🎂", "Guess my birthday", 365), ("🔒", "Crack a 3-digit lock", 1000), ("🔢", "Guess a 4-digit PIN", 10 ** 4),
      ("📮", "Guess a 5-digit code", 10 ** 5), ("📱", "Guess a 6-digit code", 10 ** 6), ("☎️", "Guess a 7-digit number", 10 ** 7),
      ("🔐", "Guess an 8-letter password", 26 ** 8)]
wait = dict(id="L07_guessing", hook=dict(emoji="🔐", top="Guessing my password daily takes", num=years(26 ** 8), bottom="", loop="The first one takes 2 days..."),
    items=[dict(emoji=e, label=l, denom=n, wait=years(n), context="", source="") for e, l, n in lw],
    outro_top="Use a long password.", outro_line="Every extra letter makes it 26 times harder.", outro_cta="Subscribe for more odds")
json.dump([wait], open(f"specs_longB_{D}.json", "w"), indent=1, ensure_ascii=False)
chap_r = "\n".join([f"0:00 Every game, ranked"] + [f"0:{int(4.5 + 5 * k):02d} {s['label']}" if 4.5 + 5 * k < 60 else f"1:{int(4.5 + 5 * k - 60):02d} {s['label']}" for k, s in enumerate(road['stops'] + [road['payoff']])])
chap_w = "\n".join([f"0:00 {years(26**8)} to guess a password"] + [(lambda t: f"{t // 60}:{t % 60:02d} {it['label']}")(int(4.5 + 6.5 * k)) for k, it in enumerate(wait['items'])])
json.dump([dict(id="L06_games", yt_title="Every Game Ranked by Odds: Dice to a Lucky Rubik's Cube",
    yt_description=f"From rolling a six (1 in 6) to a royal flush (1 in 649,740), a perfect bracket ({odds(2**63)}) and solving a Rubik's cube by random luck ({odds(43252003274489856000)}): 12 game odds ranked.\n\nWhich one have you actually done? Comment it below.\n\n{chap_r}\n\nSources: dice, card and roulette math; Powerball.com; Rubik's cube positions (43,252,003,274,489,856,000).\n\n#fyp #probability #games",
    yt_tags=["game odds ranked", "royal flush odds", "rubiks cube combinations", "yahtzee odds", "roulette odds", "perfect bracket odds", "powerball odds", "probability comparison", "odds visualized", "rarer than you think"])],
    open(f"posts_road_{D}.json", "w"), indent=1, ensure_ascii=False)
json.dump([dict(id="L07_guessing", yt_title=f"Guess One Password a Day: You'd Need {years(26**8).title()}",
    yt_description=f"If you guessed once a day, how long until you got it? A birthday takes about a year, a 4-digit PIN about 27 years, and an 8-letter lowercase password about {years(26**8)}.\n\nGuess before you watch: how long for a 6-digit code? Comment your answer, then check it.\n\nHow it works: odds of 1 in N take about N tries on average, so at one try a day it takes N days.\n\n{chap_w}\n\nSource: pure math (possible combinations).\n\n#fyp #passwords #probability",
    yt_tags=["how long to guess a password", "pin code odds", "password combinations", "brute force explained", "guessing odds", "password security", "probability explained", "odds visualized", "math facts"])],
    open(f"posts_longB_{D}.json", "w"), indent=1, ensure_ascii=False)

# ------------------------------------------------------------------ TIKTOK (11 stops + payoff = 64.5 s)
def tt(id_, top, big, ask, rows, pay):
    return dict(id=id_, hook=dict(top=top, big=big, bottom="", ask=ask, explain=""),
                stops=[dict(emoji=e, label=l, num=odds(n), source="") for e, l, n in rows],
                payoff=dict(emoji=pay[0], label=pay[1], num=odds(pay[2]), line="", source=""))
tts = [
    tt("T08_powerball", "Powerball jackpot odds:", "1 in 292 million", "Now every other prize...",
       PB[:9] + [("🔁", "Jackpot two draws in a row", 292201338 ** 2), ("🎰", "Jackpot 3 draws in a row", 292201338 ** 3)],
       ("🌌", "Jackpot 4 draws in a row", 292201338 ** 4)),
    tt("T09_rarer", "Which is rarer?", "YOU DECIDE", "Guess the rarest...", [
        ("✋", "Being left-handed", 10), ("👯", "Having twins", 32), ("📅", "Born on Feb 29", 1461),
        ("🍀", "Four-leaf clover", 10000), ("⛳", "Hole-in-one", 12500), ("🃏", "Royal flush", 649740),
        ("🪙", "20 heads in a row", 2 ** 20), ("⚡", "Lightning this year", 1222000), ("🎟️", "Powerball jackpot", 292201338),
        ("🪙", "30 heads in a row", 2 ** 30), ("🏀", "Perfect bracket", 2 ** 63)], ("🧩", "Solve a Rubik's cube by luck", 43252003274489856000)),
    tt("T10_guess", "Could you guess my secret?", "NOPE", "Start with my coin...", [
        ("🪙", "My coin flip", 2), ("🎲", "My dice roll", 6), ("🗓️", "My birth month", 12), ("🃏", "My card", 52),
        ("🎂", "My birthday", 365), ("🔢", "My 4-digit PIN", 10 ** 4), ("📆", "Birthday + year", 36525),
        ("📱", "My 6-digit code", 10 ** 6), ("☎️", "My phone number", 10 ** 10), ("🔐", "My 8-letter password", 26 ** 8),
        ("🗝️", "My 12-letter password", 26 ** 12)], ("🛡️", "My 16-letter password", 26 ** 16)),
    tt("T11_d20", "Roll natural 20s in a row.", "HOW MANY?", "Start with one...", [
        ("🎲", "One natural 20", 20)] + [(e, f"{w} in a row", 20 ** k) for e, w, k in [
        ("✌️", "Two", 2), ("🤞", "Three", 3), ("😮", "Four", 4), ("😳", "Five", 5), ("😱", "Six", 6), ("🧙", "Seven", 7),
        ("🔥", "Eight", 8), ("🌋", "Nine", 9), ("🐉", "Ten", 10), ("🌌", "Fifteen", 15)]], ("👑", "Twenty in a row", 20 ** 20)),
]
json.dump(tts, open(f"specs_tt_{D}.json", "w"), indent=1, ensure_ascii=False)
json.dump([
    dict(id="T08_powerball", text="Powerball odds for every prize, from just the red ball to the jackpot 4 draws in a row. Would you still play? YES or NO 👇 #fyp #powerball #lottery #probability"),
    dict(id="T09_rarer", text="Which is rarer: a four-leaf clover, a perfect bracket or a lucky Rubik's cube? Call the order in the comments 👇 #fyp #whichisrarer #probability #learnontiktok"),
    dict(id="T10_guess", text="Guessing odds: my coin flip, my PIN, my 16-letter password. How far would you get? Comment your guess 👇 #fyp #passwords #probability #learnontiktok"),
    dict(id="T11_d20", text="Natural 20 odds: how many in a row before it's impossible? Ever rolled two? YES or NO 👇 Send this to your D&D group. #fyp #dnd #dice #probability"),
], open(f"posts_tt_{D}.json", "w"), indent=1, ensure_ascii=False)
print("ok")
for sp in shorts: print(sp["id"], [it["num"] for it in sp["items"]])
for sp in tts: print(sp["id"], [s["num"] for s in sp["stops"]], sp["payoff"]["num"])
print(road["payoff"]["num"], [s["num"] for s in road["stops"]]); print([it["wait"] for it in wait["items"]], wait["hook"]["num"])
print(chap_r); print(chap_w)
