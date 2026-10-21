# Odds Visualized LONG-FORM (1-minute, 16:9) runbook — added Oct 16 at the user's request
User asked: "make long form videos and upload them to the same channel... like 1 min videos".
- YouTube ONLY (channel Odds Visualized, connection 0252197f-3436-8ba5-99b2-d9b07a82097c). Not Instagram. Never BPK.
- 2 per day (user, Oct 16: "Upload two long form a day. Make them different so YT does not flag it as mass produced or inauthentic"),
  uploaded at ~12:00 PM and ~4:00 PM America/Los_Angeles. Horizontal 1920x1080, ~60 s, so YouTube counts it as a
  regular video (watch hours toward monetization), NOT a Short. Never put #Shorts in these descriptions.
- Renderer: engine3.py "Odds Ladder" (intro 6 s, N rungs x 6 s, outro 6 s; 8 rungs = 60 s). Spec format is in its docstring.
  Unique music per video is automatic. Output out3/<id>.mp4, push to repo long/<id>.mp4.
  URL: https://raw.githubusercontent.com/shaunmcm/odds-visualized-media/main/long/<id>.mp4
- Each ladder has a NEW THEME (e.g. sports odds, space, your body, everyday luck, school & jobs, nature, history, tech) and
  a new title/hook; rungs may draw on facts used in Shorts, but never repeat a ladder theme or the same set of rungs.
  Every number sourced or pure math; context lines must be checked arithmetic. Rotate in new long formats over time.
- Captions in posts_long_<date>.json: yt_title keyword-first (<60 chars), description first sentence answers the search
  question, chapters (0:00, 0:06, ...), sources, 3 hashtags (no #Shorts), 6-8 yt_tags.
- TO UPLOAD <id>: confirm long/<id>.mp4 is in the repo; Zapier YouTubeV4CLIAPI upload_video on connection 0252197f...,
  privacy public, made_for_kids false, notify_subscribers true; append "<id> | yt url | time" to posted_long.log;
  SendUserMessage one line with the link. Failures/credits: same rules as POSTING.md.
- Costs 2 Zapier tasks per upload (~60/month).

TWO DIFFERENT FORMATS EVERY DAY (anti "mass-produced"/"inauthentic content"):
- Format A "Odds Ladder" = engine3.py (bright stripes, vertical rarity meter). Format B "The Waiting Game" = engine4.py
  (dark starfield, horizontal time line, "if you tried once a day"; spec in its docstring; wait = denom days, check every
  wait/context line by arithmetic). The two daily uploads must ALWAYS be different formats AND different themes, and must
  not share more than 2 facts with each other or with the previous day's long-forms.
- Alternate which format goes at noon vs 4 PM. Vary item counts (6-9), titles, intro wording, outro lines, colours, emoji.
- Within the first 2 weeks, build at least one more format (e.g. "Out of 1,000 people" dot-grid, "Odds by age", "Myth vs
  real odds") as engine5.py and rotate it in, so no format runs more than once a day. Keep adding formats over time.
- Files: specs_long_<date>.json/posts_long_<date>.json (format A), specs_longB_<date>.json/posts_longB_<date>.json (format B),
  or specs_long<X>_<date>.json for new formats.

USER RULES ADDED OCT 16 (late) — apply to every long-form:
- SIMPLE AT A GLANCE (user said the first Waiting Game was "too hard to understand when first looking at it"):
  one item on screen at a time, centred; big icon, one SHORT label (<=25 chars), one HUGE answer, one short context line
  (<=45 chars). No dense charts, no extra labels. Engines 3 and 4 already follow this; new formats must too.
- STRONG HOOK IN THE FIRST 5 SECONDS: every spec has "hook":{"emoji","top","num","bottom","loop"}. Frame 0 shows the most
  shocking number from the video (usually the last item), then a cliffhanger loop line by ~2.5 s ("But one of these takes
  just 5 weeks..."). Never open on a plain title card.
- TITLES: hook-based and different every time — a surprising claim or number up front, keyword included, under 60 chars,
  true (no clickbait lies). Never reuse a title pattern from the last 10 uploads (check titles.log, append every title).
  Examples: "A Perfect Bracket Would Take 25 Quadrillion Years", "You Beat 1 in 8×10^67 Odds Every Time You Shuffle".
- SEO: description sentence 1 asks + answers the search question with the main keyword; sentence 2 lists the headline
  numbers; then how-it-works line, chapters with the numbers, sources, 3 hashtags. 10-12 yt_tags mixing broad
  ("probability explained") and specific long-tail ("odds of a perfect bracket") phrases.
- MUSIC: every video gets a different STYLE as well as a different tune: music.make_styled + music.pick_style (8 styles:
  lofi, synthwave, marimba, piano, chiptune, trap, funk, ambient; no style repeats within the last 5 videos; logged in
  music/style_log.txt). The engines do this automatically. Same-day uploads should all use different styles.
- WARNING: Zapier's DEFAULT YouTube connection is Broke Proof Kids (027a94d6...). Every Odds upload MUST pass
  connection_id 0252197f-3436-8ba5-99b2-d9b07a82097c. Use category_id 27 (Education), default_language en.
- If Zapier says "This action has been throttled without retry", nothing was posted: wait, then retry later via send_later
  (20-30 min), checking the channel's latest uploads first so nothing is posted twice.

=== OCT 17 REDESIGN (user: the Ladder long-form "was way too confusing to read... make it more simple with a good hook,
built for attention for the payoff"; research similar bigger channels and use the same method; max 1:30) ===
RESEARCH (Oct 17): Reigarw Comparisons (~2.1M subs; "Probability Comparison: Death" ~11M views) and MetaBallStudios
(~2M subs, ~300K avg views/upload) both use ONE continuous camera move along a line of items that escalate, each item =
one picture + a few words + one big number, music, no clutter. Retention research (500 viral faceless shorts analysis;
Jenny Hoyos' formula): frame 0 simple + bright + readable, NO greeting/intro card; hook = curiosity gap that FORESHADOWS
the payoff; open loop held until the end; centre-band text only; escalate tension; short clear payoff at the very end;
rewatchable/loop-friendly ending. Narration-free is fine for this style.
RULES:
- engine3.py (Ladder) is RETIRED for new videos. Format A is now engine5.py "Rarity Road" (spec in its docstring):
  hook {top, big, bottom, ask} e.g. "One card hand is / 2,000x RARER / than winning the Powerball. / Can you guess it before
  the end?"; 6-9 stops with labels of <=4 words and one number each; the payoff is hidden as "?" until the end.
- Format B stays engine4.py "Waiting Game" (already simplified). Two daily uploads = one A + one B, different themes.
- Length 40-90 s, never over 1:30. Every on-screen line must be readable in under 1 second. If a frame needs explaining,
  it's too complicated: cut it.
- The hook's "big" number must be TRUE and computed (e.g. 635,013,559,600 / 292,201,338 = 2,173 -> "2,000x").
- OCT 17 (user): long-form videos must be OVER 1 MINUTE on both YouTube and TikTok (aim 62-75 s). Rarity Road YT
  videos therefore need 11+ stops (3.5 + 5n + 5 s); TikTok = engine6.py vertical, same rule.

## THUMBNAILS (Oct 19): long-form videos were getting 0-1 views (no custom thumbnail, so YouTube showed a random frame).
Every long-form now gets <id>_thumb.jpg (1280x720, the opening frame: one short line + one huge word/number) pushed to long/,
passed as the upload's "thumbnail". If the upload errors because of the thumbnail (custom thumbnails need a verified channel),
retry once without it and tell the user to verify the channel at youtube.com/verify.
Oct 19: thumbnail upload REJECTED ("doesn't have permissions to upload and set custom video thumbnails"), but the video itself still
uploaded. Until the user says the channel is verified, do NOT pass "thumbnail" (it errors after the upload, which risks a double post).
If a thumbnail error ever happens, check search?forMine first; never re-upload a video that already exists.


## STOPPED (user, Oct 19 2026 6:53 PM): "Stop posting the long form to YT". Do not make or upload long-form videos (incl. the Saturday weekly recap) unless the user asks again.
