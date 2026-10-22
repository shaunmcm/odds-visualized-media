# ODDS VISUALIZED — INSTAGRAM GROWTH SYSTEM (user, Oct 19 2026, permanent)
Goal: 10,000 highly engaged followers, positioned for monetization. Niche stays exactly the same: odds, probability, "rarer than you think".
The algorithm signals we build every post for: RETENTION (watch time / swipe-through), SAVES, COMMENTS, SHARES (DM sends).
No corporate fluff, no definitions, no robotic transitions. Direct, punchy, native to Instagram.

## SCHEDULE (user, Oct 19 07:45, FINAL: "three reels per day on Instagram and one carousel", same viral hook methods)
Instagram (4): 8:30 AM carousel · 11:30 AM Reel · 5:30 PM Reel · 8:00 PM Reel
YouTube: STOPPED COMPLETELY (user, Oct 22 2026 12:38 AM: "stop auto posting shorts to YouTube completely"). No Shorts, no long-form. Do not upload anything to YouTube unless the user restarts it.
TikTok (4):    9:15 AM · 12:30 PM · 5:00 PM · 8:30 PM, vertical and OVER 1 minute (engine6, 64.5 s)
The 3 Reels are Instagram only. The carousel is Instagram only.
Reels use the SAME hook system as carousels: the on-screen headline and caption line 1 come from the hook triggers below.
Carousel backlog (rendered, captions in posts_car_20261019.json): C02_montyhall, C03_birthday, C04_casino. Use these first, one per day.

## EVERY PIECE OF CONTENT GETS THESE COMPONENTS (write them into the posts/specs files)
### 1. Scroll-stopping native hook (under 10 words; it's the on-screen headline AND the caption's first line)
Use one trigger per hook, rotate them, never repeat a hook (check titles.log):
- CONTRARIAN: "Sharks are the least scary thing here." / "Your 'strong' password isn't." / "Lottery tickets aren't the worst bet."
- UNSPOKEN RULE: "Casinos never say this number out loud." / "Nobody tells you the odds on this."
- OPEN LOOP: "The last one breaks the scale." / "Number 1 isn't what you think."
- YOU-CHALLENGE: "You can't guess this in a lifetime." / "Bet you've beaten worse odds today."
- STAKES FLIP: "This is rarer than winning Powerball." / "Your PIN falls faster than you think."
Banned: "Did you know", "Here's why", "In this video", "Let's dive in", "Fun fact", any line that sounds like a textbook.
Every hook must be TRUE and backed by the numbers in the post.

### 2. Retention structure (Reels/Shorts/TikTok: already in the engines)
4.5 s obvious opening → ranked items, rarer each time, accelerating → silence + drop on the last item → YES/NO loop frame.

### 3. "Impossible-not-to-save" carousel (1 per day, carousel.py, 7-9 slides, 1080x1350)
- Slide 1 = curiosity gap: hook kicker + bold promise ("Long beats complex. Here's the math.") + one big picture + "SWIPE →".
  Never give the answer on slide 1.
- Middle slides = tactical, little-known, instantly usable; UNDER 15 WORDS EACH; one idea + one picture + one big number per slide.
  Must be something people will DO or decide with: passwords, PINs, lottery/casino house edge, everyday risk, which bets lose least,
  how to win simple games (Monty Hall, rock-paper-scissors patterns), birthday math for parties, etc. Pure math or official sources only.
- Second-to-last slide = the "whoa" number (the one people screenshot).
- Final slide = the monetization CTA (see 4). Until the comment-keyword DM automation is live, the final slide uses a SAVE + SEND CTA.

### 4. Frictionless CTAs (never "comment below", never "let me know")
Rotate; one per post, matched to the content:
- SAVE: "Save this before your next password reset." / "Save this for your next casino trip." / "Screenshot slide 5. Trust me."
- SEND (DM shares): "Send this to the friend who still uses password123." / "Send this to whoever buys tickets every week."
- BINARY COMMENT: "LONG or SHORT? Which is yours?" / "Comment the number you got stuck on." / "YES if you've rolled two nat 20s."
- PREDICT-THEN-CHECK: "Guess before you swipe. Comment your number."
- KEYWORD DM (ONLY once automation is live, see MONETIZATION): "Comment ODDS and I'll DM you the free cheat sheet." /
  "Comment SAFE for the 6-word password method." / "Comment LUCK for all 100 odds on one page."
- FOLLOW LOOP: "Part 15 drops tomorrow. Follow so you don't miss it."

### 5. Caption (same 30-day growth structure as POSTING.md)
Line 1 keyword hook + number + emoji · Line 2 comment trigger · Line 3 send/save trigger · Line 4 series/follow (Reels) ·
blank line · 5 hashtags max incl. #fyp and #oddsvisualized. Never write "#<number>".

## MONETIZATION PATH (in order; tell the user when each step needs them)
1. Lead magnet: a free one-page "Odds Cheat Sheet" PDF (100 real odds, ranked). Claude can build it.
2. Comment-keyword DMs need ManyChat (free plan) connected to the Instagram account. The user must set this up once
   (Claude can't log in for them). Once it's live, switch final slides to KEYWORD DM CTAs and set ManyChat to send the PDF link
   plus an email signup.
3. Bio link → the cheat sheet + email list (free beehiiv/Kit). The email list is the asset brand deals and products sell to.
4. Products at ~2-5k followers: a $7-12 "Odds of Everything" printable/poster pack; later a paid deep-dive.
5. Brand deals at ~5-10k: password managers, VPNs, personal-finance and education apps fit the content naturally
   (always disclosed as #ad). TikTok Creator Rewards at 10k followers; YouTube Partner Program at 1k subs + 10M Shorts views or 4k watch hours.

## WEEKLY (Sunday) — add to the GROWTH.md review
Rank IG posts by saves+shares per reach (IG insights if available). Double the formats in the top 3, retire the bottom 3.

## ACCURACY: STATE THE ASSUMPTION (user, Oct 21). If odds assume blind guessing / equal chances, say so on screen ("If you guess blindly") and in the caption. Never present coin-flip math as real-world odds for sports or skill (bracket: blind 1 in 9.2 quintillion vs NCAA informed-fan estimate ~1 in 120.2 billion).
