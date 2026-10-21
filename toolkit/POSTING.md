# Odds Visualized posting runbook (for scheduled runs in this session)

Standing rules from the user: 5 posts per day, permanently, fully automatic. On-screen brand is
"ODDS VISUALIZED" (no comma). Never repeat a topic. Keep strictly separate from Broke Proof Kids.

ACCOUNTS (never mix with Broke Proof Kids):
- Instagram: @oddsvisualized, instagramPageId 17841423585967011 (Zapier InstagramBusinessCLIAPI publish_video)
- YouTube: Odds Visualized channel UChgp89TuX4y7HgCeaObfF2Q, Zapier YouTubeV4CLIAPI connection_id 0252197f-3436-8ba5-99b2-d9b07a82097c (ALWAYS pass it: the Zapier default YouTube connection is Broke Proof Kids)
  NEVER use connection 027a94d6-f9c3-89c1-b9f4-531f75a19b93 (Broke Proof Kids) or IG page 17841440839365671 (Kids & Money).
- Video URL: https://raw.githubusercontent.com/shaunmcm/odds-visualized-media/main/v/<id>.mp4
- Repo clone: /home/claude/odds-visualized-media (commit as Claude <noreply@anthropic.com>)

Every Zapier call that succeeds costs 2 Zapier tasks, so keep calls minimal:
per post = 1 Instagram publish + 1 YouTube upload (plus a recovery read only if Instagram says "still processing").
The YouTube channel check (channels?mine=true on connection 0252197f...) is done ONCE per night in production, not per post.

TO POST <id> (captions live in posts_v2*.json for new-style videos; MP4s from engine2 in out2/):
1. Confirm v/<id>.mp4 is in the repo (git -C /home/claude/odds-visualized-media ls-files v/<id>.mp4).
2. Instagram publish_video with ig_caption. If it errors "Video is still processing", wait 60s, GET
   graph.facebook.com/v19.0/17841423585967011/media?fields=id,caption&limit=3 and retry ONLY if it did not post. Never post twice.
3. YouTube upload_video on connection 0252197f... with title yt_title (as is), description yt_description,
   tags yt_tags (if present), privacy public, made_for_kids false, notify_subscribers true.
4. Append "<id> | ig media id | yt url | time" to posted.log. SendUserMessage one line with the YouTube link
   (Instagram link: instagram.com/oddsvisualized).

FAILURES / CREDITS — tell the user right away with SendUserMessage, plainly, and what they need to do:
- Zapier error mentioning "task limit" / plan / billing  -> Zapier tasks ran out; user must upgrade or wait for reset.
- Zapier auth/connection expired errors -> user must reconnect that app in Zapier.
- GitHub push refused (403) -> user must re-approve the Claude GitHub app.
- Instagram/YouTube rejecting uploads (quota, spam, policy) -> report the exact message; do not retry in a loop.
Don't stop the whole system for one failed post: log it, report it, and move on to the next scheduled post.

CONTENT RULES (user approved the NEW STYLE on Oct 16 — use engine2.py for every video from now on; engine.py/old style is retired):
- Format: bright topic colour + big emoji icon + the shocking number on frame 0, an open loop line by 0.5s
  ("...but what's even RARER?"), a counter scene (ticks + ding), a "Which is RARER?" guess scene with 3-2-1
  countdown, then the reveal with RARER stamp + punchline + "Follow for more odds". ~11.5 s, sound effects + music.
- The opening hook (icon + number + open loop) stays on screen ~3.7 s (HOLD=60 in engine2.py) so people can read it — user asked twice; never shorten it. Everything after the hook keeps the same pacing.
- MUSIC: every video gets its OWN track in a DIFFERENT STYLE (music.make_styled + music.pick_style; 8 styles, none repeated within the last 5 videos; engine2.py does this automatically). Never reuse a track or let same-day videos share a style.
- Text sits low enough to clear the app's top bar (titles at y≈250).
- Every video = a NEW sourced fact + a NEW comparison fact; compute ratios exactly and round honestly ("about 52x").
- Avoid YouTube's "inauthentic content" problem: vary topics, colours, emoji and wording every time; never reuse a
  fact pair; as the backlog grows, add new formats (e.g. "Odds of X by age", "This happens every X seconds")
  and rotate them. Never make an unverifiable claim; every number is sourced or pure math.
- Lottery/gambling topics stay educational — never promote betting.

CAPTION / SEO RULES:
- Instagram: first line = the main search keyword phrase + hook (under ~125 characters, shows before "more"),
  e.g. "Royal flush odds, visualized ♠️ ...". Then 2-3 short lines of value, then a share/save/tag CTA,
  then a question to drive comments, then the source line, then EXACTLY 5 or fewer hashtags
  (Instagram's limit): 2 broad (#odds #probability #funfacts) + 2-3 topic-specific.
- YouTube Shorts: yt_title under ~60 characters, keyword first ("Powerball Odds Visualized: ..."), no clickbait
  lies. yt_description: first sentence answers the search question with the keyword ("What are the odds of X? ...").
  Then the source, then 3 hashtags starting with #Shorts. yt_tags: 5 search phrases.
- TITLES (user, Oct 16): YouTube titles must be hook-based and different every time (a surprising claim/number first,
  keyword included, true, <60 chars). Don't keep using "X vs Y: Which Is Rarer?" — never reuse a title pattern from the
  last 10 uploads (append every title to /home/claude/odds/titles.log and check it). yt_tags: 8 search phrases.

=== OCT 17 USER BLUEPRINT RULES (Shorts/Reels) — supersede older Shorts timing ===
- User: "find the most viral niche outliers (>10k views), replicate their methods but make it better". Target 15-20 s.
- Proven outlier: "Probability Comparison: Death" (~11M views, Reigarw Comparisons ~2.1M subs); Zack D. Films short
  "How Stitches Work" 253M views at 31 s (answer the question fast, end immediately, rewatch loop).
- Structure: 0-2 s hook (headline <6 words + high-contrast first card at 0.1 s) -> 10 items ranked most common ->
  rarest, ACCELERATING (1.6 s down to 1.0 s each) -> last item held ~2.6 s with a beat of silence then bass drop ->
  final-frame comment-bait question that loops back into the first frame. Total 15-20 s.
- SFX: whoosh + sub-bass hit per card, clock ticks that speed up, riser every 3rd item, silence + drop + siren on the
  final item, heartbeat on the loop frame.
- Captions: description under 15 words + exactly 5 hyper-targeted hashtags (IG, YT, TikTok).
- Data: real sources only (e.g. NSC Injury Facts 2024 lifetime odds of dying; ISAF shark data) or pure math.
  Avoid suicide/overdose/gun items (sensitive + ad-unfriendly); keep it non-graphic.

=== TIKTOK (added Oct 17; user: 4 TikToks per day, no permission needed to post/schedule) ===
- Account: TikTok odds.visualized via Buffer (Zapier BufferCLIAPI, connection 02411f24-fffe-8b57-b289-ed78898aaa2a,
  organizationId 6ad399bf6f9886286711d3f1, channelId 6ad39b17778b240e2f3afd12). Action buffer_add_to_queue,
  method share_now, dynamic_properties {attachment: video, video: <raw github url>, text: <caption>, scheduling_type: direct}.
- 4 per day at ~9:15 AM, 12:30 PM, 5:00 PM, 8:30 PM PT. Vertical, OVER 1 MINUTE (Creator Rewards needs >1 min):
  engine6.py (vertical Rarity Road, 11 stops + payoff = 63.5 s) -> out4/, repo tt/<id>.mp4. Rotate in more vertical
  formats over time. Captions: under 15 words + MAX 4 hashtags (never write '#<number>' in caption text; it counts as a hashtag). Log to posted_tiktok.log.

- GROWTH: read /home/claude/odds/GROWTH.md every night and apply it (series numbering in series.txt, sequels of top performers, tension/phonk music).

=== HASHTAG LIMITS (user, Oct 17 — overrides anything above) ===
Instagram: max 5 hashtags. TikTok: max 4. YouTube (Shorts and long-form): max 3 in the description (Shorts: #Shorts + 2),
always plus yt_tags (8 search-phrase tags, passed as the upload's tags). Never put '#<number>' in any caption.
ALWAYS include #fyp as one of the hashtags on every platform (user, Oct 17), within the limits above
(YouTube Shorts: #Shorts #fyp + 1 topic tag; YouTube long-form: #fyp + 2; TikTok: #fyp + 3; Instagram: #fyp + 4).

=== FIRST 4 SECONDS MUST BE OBVIOUS (user, Oct 17 — overrides earlier hook rules) ===
User: viewers can't tell what the video is ("it just shows 1 in ??? and question marks"). In the first 4 seconds a
stranger must understand WHAT the video is and WHAT is being ranked, without having to guess:
- Never show placeholder odds like "1 in ???" or a lone question-mark icon.
- Shorts (engine7): headline + "topic" line (e.g. "Lifetime odds of dying from...") + the two sides LABELLED in words
  (hook.left/right.label) + a "ranked" line ("10 things ranked: most likely to least likely").
- Long-form/TikTok Rarity Road (engine5/6): hook.explain line ("Card hands, ranked common to rarest", max ~2 lines) +
  a row of the actual item icons; payoff can stay hidden but must be described ("...and the rarest one at the end").
- Spot-check the 0.5 s and 3 s frames: if it needs explaining, rewrite it.
- send_later is rate-limited (~10 creations quickly); if 'Trigger creation rate limit reached', wait ~40 s and continue.

=== UNIQUE VISUALS EVERY VIDEO (user, Oct 18: "change the visuals for each of the videos... they are all the same across
TikTok and Instagram... make sure they're unique each time") ===
- engine7 (Shorts), engine6 (TikTok) and engine5 (YT Rarity Road) call themes.pick(video_id): 10 themes (palette, moving
  background texture: grid / rays / waves / bokeh / dots / snow / diagonal / vignette, card style: none / panel / glow,
  entrance motion: up / drop / left / zoom, accent colour), never repeating any of the last 6 videos (themes_log.txt),
  with per-video hue jitter. Never hard-code colours in specs expecting them to be used; the theme decides.
- When adding new themes, keep text contrast high (black stroke on text) and spot-check frames.
- Textured backgrounds render slower (~2-3 min per Short, ~4 min per TikTok): run long batches with nohup in the
  background and poll, so a single command never hits the 10-minute tool timeout.

## OPENING = 4.5 SECONDS (user, Oct 18 11:48 PT) — all formats
engine7 HOOK=135 (Shorts now 20.0 s, CTA trimmed to 54), engine6/engine5 HOOK=135, engine4 INTRO=135.
Long-form chapter timestamps: engine5 stop k starts at 4.5+5k s; engine4 item k at 4.5+6.5k s.

## 30-DAY GROWTH CAPTION STRUCTURE (user, Oct 18) — every post, every platform
Goal: get into search + recommendations fast (keywords), then drive comments/shares/saves (the signals that
push a new account out of its first test audience), then convert to follows via the series.
INSTAGRAM caption (4 short lines + 5 hashtags):
  1. KEYWORD HOOK: starts with the search phrase people type ("Dice odds:", "Card guessing odds:") + the shocking
     true number + 1 emoji. IG search reads captions, so the keyword goes first.
  2. COMMENT BAIT: a binary question tied to the video, "Comment YES or NO 👇".
  3. SHARE PROMPT: "Send this to the friend who…" (DM shares are the strongest reach signal).
  4. SERIES/FOLLOW: "Part N of Rarer Than You Think. Follow for Part N+1."
  Hashtags (5): #fyp #probability #<big topic> #<niche topic> #oddsvisualized
TIKTOK text (one paragraph, max 4 hashtags): keyword phrase first ("Coin flip odds:") + number/tease +
  question with YES/NO or "comment your guess 👇" (+ optional share line). Hashtags: #fyp #probability #<topic> #learnontiktok
  (TikTok search indexes the caption text, so the keyword phrase matters more than the tags).
YOUTUBE SHORTS: title = keyword + true shocking number, different every time (check titles.log).
  Description: line 1 keyword sentence, line 2 the YES/NO question "in the comments", blank, Source, blank,
  #Shorts #fyp #<topic> (3 max). yt_tags 8–11: exact search phrases ("dice odds", "how rare is…", "probability of…").
YOUTUBE LONG-FORM: description para 1 = keyword-rich answer, para 2 = "guess before you watch / comment" question,
  chapters, sources, then #fyp #<topic> #probability.
NEVER write "#<number>" anywhere ("past No. 5", not "past #5"). Fact-check every number in the caption against the spec.

## KEEP THE SCREEN SIMPLE (user, Oct 18 5:13 PM: "too much text on the screen, confusing to read") — ALL FORMATS
Engines were stripped down; never add the removed text back:
- Max 3 things on screen at once: ONE short line (≤6 words) + ONE picture + ONE big number.
- Shorts opening = headline (≤6 words) + the VS picture with two 2-word labels. No series line, no subtitle,
  no "10 things ranked" line. Cards = label + emoji + number (no "#N"). Final item = label + emoji + number (no extra line).
- TikTok/YouTube Rarity Road opening = one question line + one big word/number + a short guess prompt. No sub-line,
  no explainer line, no emoji row, no on-screen sources (sources go in the caption/description only).
- Waiting Game: no hook sub-line, no context line under the answer, no progress dots, no on-screen source.
- Numbers in plain words: "1 in 3.7 quadrillion", never "3.7 × 10^15". If a number is beyond ~sextillion, use a
  word like IMPOSSIBLE in the opening and keep the number only for the final payoff.
- Labels ≤ 5 words. If text wraps to 2 lines, shorten it.
- Before scheduling, grab frames at 1 s, mid-video and the end, and check that each frame reads in one glance.

## BACKLOG (Oct 19 build): S15_bracket, S16_arrange, S17_casino are rendered as Parts 15-17 (captions in posts_v3s_20261019.json).
Next nightly: schedule S12_d20 (Part 12) and S13_heads (Part 13) first, then S15_bracket (Part 15); S16, S17 stay backlog. New Shorts continue from Part 18 (series.txt = highest part rendered = 17).
WEEKLY REVIEW Oct 18: Shorts average ~1,000-1,500 views each; best = "Which is rarer?" A-vs-B comparisons (Twins vs 10 heads 1,478,
Hole-in-one vs Royal flush 1,322, Bracket vs Powerball 1,244) and Powerball (1,571). Make at least 1 "Which is rarer?" per day.

## SCHEDULE CHANGE (user, Oct 19 00:56): 4 POSTS PER DAY ON EVERY ODDS VISUALIZED ACCOUNT. See IG_SYSTEM.md (overrides older 5/2 counts).
Instagram: 8:30 carousel, 11:30/5:30/8:00 Reels · YouTube: 11:30 Short, 12:00 long-form, 5:30 Short, 8:00 Short ·
TikTok: 9:15/12:30/5:00/8:30, over 1 minute. Oct 19 extras moved to backlog: S13_heads, S12_d20 (Shorts), L07_guessing (long-form).

## INSTAGRAM (user, Oct 19 07:45, overrides the 00:59 carousel-only note): 3 Reels (11:30, 5:30, 8:00, same videos as the YouTube Shorts) + 1 carousel (8:30) per day.
- User deletes Instagram posts on purpose sometimes. If a post is missing, note it and do not repost unless asked.

## NO LONG-FORM ON YOUTUBE (user, Oct 19 6:53 PM). YouTube = 4 Shorts/day: 11:30, 12:00 (YouTube-only extra Short), 5:30, 8:00. No weekly recap video.

## ACCURACY: STATE THE ASSUMPTION (user, Oct 21). If odds assume blind guessing / equal chances, say so on screen ("If you guess blindly") and in the caption. Never present coin-flip math as real-world odds for sports or skill (bracket: blind 1 in 9.2 quintillion vs NCAA informed-fan estimate ~1 in 120.2 billion).

## BACKLOG after Oct 21 build: Shorts S20_redrow (Part 20), S21_monkey (Part 21), S22_bday (Part 22) — captions in posts_v3s_20261021.json; series.txt = 22, new Shorts start at Part 23.
Carousels: C04_casino (posts_car_20261019.json), C05_dice (posts_car_20261021.json). TikTok backlog: none.
