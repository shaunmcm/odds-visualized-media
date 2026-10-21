"""Wed Oct 21 content. Pure math or named official sources. Assumptions (random / blind guess) stated on screen."""
import json, math
D = "20261021"
NAMES = [(1e33, "decillion"), (1e30, "nonillion"), (1e27, "octillion"), (1e24, "septillion"), (1e21, "sextillion"),
         (1e18, "quintillion"), (1e15, "quadrillion"), (1e12, "trillion"), (1e9, "billion"), (1e6, "million")]
def words(n):
    for v, w in NAMES:
        if n >= v:
            x = n / v; s = f"{x:.1f}".rstrip("0").rstrip(".") if x < 100 else f"{x:.0f}"
            return f"{s} {w}"
    return f"{round(n):,}" if n >= 10 else f"{n:.1f}".rstrip("0").rstrip(".")
def odds(n): return f"1 in {words(n)}"

MM = 290472336  # Mega Millions jackpot odds (megamillions.com, game change April 2025)
EU = 37 / 18    # one color on a European wheel (18 of 37)

def short(id_, part, headline, L, R, items, cta):
    its = [dict(emoji=x[0], label=x[1], num=(x[3] if len(x) > 3 else odds(x[2])), n=x[2]) for x in items]
    its[-1]["label"] = its[-1]["label"].upper(); its[-1]["num"] = its[-1]["num"].upper()
    return dict(id=id_, series=f"RARER THAN YOU THINK · PART {part}", follow=f"Follow for Part {part + 1}", headline=headline, topic="",
                hook=dict(left=dict(emoji=L[0], label=L[1]), right=dict(emoji=R[0], label=R[1])), ranked="", items=its,
                final_line="", cta=cta, yes="YES", no="NO", source="")

rarer = [("🎲", "Double sixes", 36), ("🃏", "Pick the right card", 52), ("😈", "Three sixes", 216), ("🎯", "Yahtzee in one roll", 1296),
         ("4️⃣", "Four of a kind", 4165), ("🌊", "Straight flush", 72193), ("📱", "Guess a 6-digit code", 10 ** 6),
         ("💰", "Mega Millions jackpot", MM), ("🧩", "Rubik's cube by luck", 43252003274489856000), ("🎰", "3 jackpots in a row", MM ** 3)]
poker = [("✌️", "One pair", 1 / 0.422569, "1 in 2.4"), ("👯", "Two pair", 1 / 0.047539, "1 in 21"), ("🎯", "Three of a kind", 1 / 0.021128, "1 in 47"),
         ("📏", "A straight", 1 / 0.003925, "1 in 255"), ("♦️", "A flush", 1 / 0.001965, "1 in 509"), ("🏠", "Full house", 1 / 0.001441, "1 in 694"),
         ("4️⃣", "Four of a kind", 4165), ("🌊", "Straight flush", 72193), ("👑", "Royal flush", 649740), ("🤯", "Two royals in a row", 649740 ** 2)]
red = [(e, f"{k} in a row" if k > 1 else "Red once", EU ** k) for e, k in
       [("🔴", 1), ("✌️", 2), ("🤞", 3), ("🖐️", 5), ("😮", 7), ("🔟", 10), ("😳", 13), ("😱", 16), ("🤯", 20), ("🎰", 26)]]
monkey = [("🅰️", "Type “a”", 26), ("👋", "Type “hi”", 26 ** 2), ("🐱", "Type “cat”", 26 ** 3), ("🎲", "Type “odds”", 26 ** 4),
          ("👋", "Type “hello”", 26 ** 5), ("🍌", "Type “banana”", 26 ** 6), ("🐒", "Type “monkeys”", 26 ** 7),
          ("🔐", "Type “password”", 26 ** 8), ("✍️", "Type “shakespeare”", 26 ** 11), ("📜", "“tobeornottobe”", 26 ** 13)]
bday = [("📅", "The weekday", 7), ("🗓️", "The month", 12), ("🔢", "The date", 31), ("🎂", "The birthday", 365),
        ("📆", "Birthday + year", 36525), ("🕐", "+ the hour", 36525 * 24), ("⏱️", "+ the minute", 36525 * 24 * 60),
        ("⚡", "+ the second", 36525 * 86400), ("👥", "Two strangers' birthdays", 365 ** 2), ("🌌", "Two people, to the second", (36525 * 86400) ** 2)]
bday = sorted(bday, key=lambda x: x[2])

shorts = [
    short("S18_rarer2", 18, "Which is rarer?", ("🃏", "Pick my card"), ("🎰", "Three jackpots"), rarer, "Called the order?"),
    short("S19_poker", 19, "Every poker hand, ranked.", ("✌️", "One pair"), ("👑", "Two royals"), poker, "Ever hit a full house?"),
    short("S20_redrow", 20, "Red again? And again?", ("🔴", "Red once"), ("🎰", "26 in a row"), red, "Would you bet on red?"),
    short("S21_monkey", 21, "A monkey hits random keys.", ("🐒", "Type “a”"), ("📜", "Type Shakespeare"), monkey, "Could it type your name?"),
    short("S22_bday", 22, "Guess blindly: my birthday.", ("📅", "The weekday"), ("⚡", "To the second"), bday, "Could you guess the month?"),
]
json.dump(shorts, open(f"specs_v3s_{D}.json", "w"), indent=1, ensure_ascii=False)

posts = [
 dict(id="S18_rarer2", caption=f"Which is rarer: guessing my card, a Mega Millions jackpot or three jackpots in a row? 🎰\nDid you call the order? Comment YES or NO 👇\nSend this to the friend who says \"someone has to win\".\nPart 18 of Rarer Than You Think. Follow for Part 19.\n\n#fyp #whichisrarer #probability #lottery #oddsvisualized",
      yt_title="Card Guess vs Three Lottery Jackpots: Which Is Rarer?",
      yt_description=f"Which is rarer? From double sixes (1 in 36) to a Mega Millions jackpot (1 in {words(MM)}) and three jackpots in a row ({odds(MM**3)}).\nDid you call the order? YES or NO in the comments.\n\nSources: megamillions.com odds; dice, card and Rubik's cube math.\n\n#Shorts #fyp #lottery",
      yt_tags=["which is rarer", "mega millions odds", "lottery odds", "royal flush odds", "yahtzee odds", "rubiks cube odds", "odds visualized", "rarer than you think"]),
 dict(id="S19_poker", caption="Poker odds for a random 5-card hand: one pair is 1 in 2.4, a royal flush is 1 in 649,740 🃏\nEver hit a full house? Comment YES or NO 👇\nSend this to your poker night group.\nPart 19 of Rarer Than You Think. Follow for Part 20.\n\n#fyp #poker #pokerhands #probability #oddsvisualized",
      yt_title="Every Poker Hand Ranked by Odds (Random 5-Card Deal)",
      yt_description=f"Odds of being dealt each hand in 5-card poker: one pair 1 in 2.4, full house 1 in 694, four of a kind 1 in 4,165, royal flush 1 in 649,740, and two royals in a row {odds(649740**2)}.\nEver hit a full house? YES or NO in the comments.\n\nSource: 5-card poker combinatorics (2,598,960 hands).\n\n#Shorts #fyp #poker",
      yt_tags=["poker hand odds", "royal flush odds", "full house odds", "poker probability", "four of a kind odds", "texas holdem odds", "odds visualized", "rarer than you think"]),
 dict(id="S20_redrow", caption="Roulette odds: red 26 times in a row on a European wheel is 1 in 137 million. Black did it in Monte Carlo in 1913 🎡\nWould you bet on red after 10 reds? Comment YES or NO 👇\nSend this to the friend who says it's \"due\".\nPart 20 of Rarer Than You Think. Follow for Part 21.\n\n#fyp #roulette #casino #probability #oddsvisualized",
      yt_title="Red 26 Times in a Row Is 1 in 137 Million (It Happened in 1913)",
      yt_description=f"Same color in a row on a European roulette wheel (18 of 37 pockets): 5 in a row {odds(EU**5)}, 10 in a row {odds(EU**10)}, 26 in a row {odds(EU**26)}. In 1913 at Monte Carlo, black came up 26 times in a row.\nEach spin is still 18 in 37. YES or NO: would you bet after 10 reds?\n\nSource: roulette math; Monte Carlo Casino, August 18, 1913.\n\n#Shorts #fyp #roulette",
      yt_tags=["roulette odds", "red in a row", "gamblers fallacy", "monte carlo 1913", "roulette streak", "casino math", "odds visualized", "rarer than you think"]),
 dict(id="S21_monkey", caption=f"Monkey on a keyboard: typing “banana” by random keys is 1 in 309 million 🐒\nCould it type your name? Comment YES or NO 👇\nSend this to someone with a long name.\nPart 21 of Rarer Than You Think. Follow for Part 22.\n\n#fyp #infinitemonkey #probability #math #oddsvisualized",
      yt_title=f"A Monkey Typing “To Be or Not to Be”: {odds(26**13).title()}",
      yt_description=f"Random typing on 26 letter keys: “cat” is 1 in 17,576, “banana” {odds(26**6)}, “password” {odds(26**8)}, “tobeornottobe” {odds(26**13)}.\nCould it type your name? YES or NO in the comments.\n\nSource: math, 26^letters (letters only, each key equally likely).\n\n#Shorts #fyp #math",
      yt_tags=["infinite monkey theorem", "monkey typing shakespeare", "random typing odds", "probability explained", "math facts", "monkey keyboard", "odds visualized", "rarer than you think"]),
 dict(id="S22_bday", caption="Guess my birthday blindly: the month is 1 in 12, the exact second I was born is 1 in 3.2 billion 🎂\nCould you guess the month? Comment YES or NO 👇\nSend this to the friend who never remembers your birthday.\nPart 22 of Rarer Than You Think. Follow for Part 23.\n\n#fyp #birthday #probability #math #oddsvisualized",
      yt_title="Guess My Birth Second Blindly: 1 in 3.2 Billion",
      yt_description="Blind-guess odds (every option equally likely, birth year within 100 years): the weekday 1 in 7, the birthday 1 in 365, birthday + year 1 in 36,525, down to the exact second at 1 in 3.2 billion.\nCould you guess the month? YES or NO in the comments.\n\nSource: math (equal-chance guessing).\n\n#Shorts #fyp #birthday",
      yt_tags=["birthday odds", "guess my birthday", "probability explained", "birthday math", "odds of guessing", "math facts", "odds visualized", "rarer than you think"]),
]
json.dump(posts, open(f"posts_v3s_{D}.json", "w"), indent=1, ensure_ascii=False)

def tt(id_, top, big, ask, rows, pay):
    st = [dict(emoji=r[0], label=r[1], num=(r[3] if len(r) > 3 else odds(r[2])), source="") for r in rows]
    return dict(id=id_, hook=dict(top=top, big=big, bottom="", ask=ask, explain=""), stops=st,
                payoff=dict(emoji=pay[0], label=pay[1], num=odds(pay[2]), line="", source=""))
tts = [
    tt("T14_poker", "Random 5-card deal:", "EVERY HAND", "Start with one pair...", poker[:10] + [("🔥", "Three royals in a row", 649740 ** 3)], ("🌌", "Four royals in a row", 649740 ** 4)),
    tt("T15_monkey", "A monkey hits random keys.", "SHAKESPEARE?", "Start with one letter...", monkey[:8] + [("⌨️", "Type “keyboards”", 26 ** 9), monkey[8], monkey[9]], ("🙈", "Type “monkeybusiness”", 26 ** 14)),
    tt("T16_red", "Red on roulette, again and again.", "26 IN A ROW?", "Start with one spin...", [(e, f"{k} in a row" if k > 1 else "Red once", EU ** k) for e, k in
        [("🔴", 1), ("✌️", 2), ("🤞", 3), ("🖐️", 5), ("😮", 7), ("🔟", 10), ("😳", 12), ("😱", 15), ("🤯", 18), ("🌋", 21), ("🎰", 24)]], ("🏛️", "26 in a row (Monte Carlo, 1913)", EU ** 26)),
    tt("T17_rarer2", "Which is rarer?", "YOU DECIDE", "Guess the rarest...", rarer[:8] + [("🎟️", "2 jackpots in a row", MM ** 2), ("🏀", "Perfect bracket (blind picks)", 2 ** 63), rarer[8]], ("🎰", "3 jackpots in a row", MM ** 3)),
]
json.dump(tts, open(f"specs_tt_{D}.json", "w"), indent=1, ensure_ascii=False)
json.dump([
 dict(id="T14_poker", text="Poker odds for a random 5-card deal: one pair to four royal flushes in a row. Ever hit a full house? YES or NO 👇 #fyp #poker #probability #learnontiktok"),
 dict(id="T15_monkey", text="A monkey hitting random keys: “cat” is easy, Shakespeare is not. Could it type your name? YES or NO 👇 #fyp #math #probability #learnontiktok"),
 dict(id="T16_red", text="Roulette odds: red 26 times in a row on a European wheel. Black actually did it in Monte Carlo in 1913. Would you bet on red? 👇 #fyp #roulette #casino #probability"),
 dict(id="T17_rarer2", text="Which is rarer: a Mega Millions jackpot, a perfect bracket picked blindly, or a lucky Rubik's cube? Call the order 👇 #fyp #whichisrarer #probability #learnontiktok"),
], open(f"posts_tt_{D}.json", "w"), indent=1, ensure_ascii=False)

# carousel (backlog after today: C04_casino + this new C05)
V = lambda n, e, t, b, note="": dict(type="value", n=n, emoji=e, title=t, big=b, note=note)
car = [dict(id="C05_dice", slides=[
    dict(type="cover", kicker="Board game players lose to this math.", title="Two dice. Some numbers win more.", emoji="🎲", big=""),
    V(1, "7️⃣", "7 comes up most", "1 in 6 rolls", "6 of 36 combos"),
    V(2, "🏆", "6 and 8 are the best spots", "5 in 36 each", "13.9% of every roll"),
    V(3, "5️⃣", "5 and 9", "4 in 36 each"),
    V(4, "🔟", "4 and 10", "3 in 36 each"),
    V(5, "🐢", "3 and 11", "2 in 36 each"),
    V(6, "🚫", "2 and 12 almost never hit", "1 in 36 each", "Once every 36 rolls, on average"),
    dict(type="cta", title="Save this for your next game night.", keyword="", emoji="💾", line="Send it to the friend who always picks 12.", save="Follow for daily odds")])]
json.dump(car, open(f"specs_car_{D}.json", "w"), indent=1, ensure_ascii=False)
json.dump([dict(id="C05_dice", slides=8, caption="Two-dice odds: 7 comes up 1 in 6 rolls, while 2 and 12 come up just 1 in 36 🎲\nWhich number do you always pick? Comment it 👇\nSend this to the friend who always picks 12.\nSave it for your next board game night.\n\n#fyp #boardgames #dice #probability #oddsvisualized")],
          open(f"posts_car_{D}.json", "w"), indent=1, ensure_ascii=False)
for s in shorts: print(s["id"], [i["num"] for i in s["items"]])
for s in tts: print(s["id"], [x["num"] for x in s["stops"]], s["payoff"]["num"])
