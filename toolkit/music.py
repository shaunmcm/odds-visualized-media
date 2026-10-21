"""Original lo-fi background tracks, synthesized from scratch (copyright-free)."""
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100
rng = np.random.default_rng(1)

def midi(n): return 440.0 * 2 ** ((n - 69) / 12)

def lp(x, cut, order=2):
    b, a = butter(order, cut / (SR / 2), "low"); return lfilter(b, a, x)

def hp(x, cut, order=2):
    b, a = butter(order, cut / (SR / 2), "high"); return lfilter(b, a, x)

def keys(freq, dur, vel=0.5):
    """Electric-piano-ish tone: sine + soft harmonics, bell attack, decay."""
    t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t * 1.8) * (1 - np.exp(-t * 300))
    trem = 1 + 0.08 * np.sin(2 * np.pi * 4.5 * t)
    s = (np.sin(2 * np.pi * freq * t)
         + 0.35 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t * 4)
         + 0.12 * np.sin(2 * np.pi * 3 * freq * t) * np.exp(-t * 7))
    return vel * s * env * trem

def bass(freq, dur, vel=0.6):
    t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t * 60) * np.exp(-t * 1.2)
    return vel * (np.sin(2 * np.pi * freq * t) + 0.2 * np.sin(2 * np.pi * 2 * freq * t)) * env

def kick(vel=0.9):
    t = np.arange(int(0.35 * SR)) / SR
    f = 110 * np.exp(-t * 18) + 45
    return vel * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)

def snare(vel=0.35):
    t = np.arange(int(0.25 * SR)) / SR
    n = hp(rng.standard_normal(len(t)), 900)
    return vel * (n * np.exp(-t * 18) + 0.3 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25))

def hat(vel=0.12):
    t = np.arange(int(0.06 * SR)) / SR
    return vel * hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * 70)

def add(buf, x, at):
    i = int(at * SR); j = min(len(buf), i + len(x))
    if i < len(buf): buf[i:j] += x[: j - i]

# (name, bpm, root midi, chord intervals per bar, swing)
TRACKS = [
    ("sunday", 82, 57, [[0, 4, 7, 11], [5, 9, 12, 16], [2, 5, 9, 12], [7, 11, 14, 17]], 0.08),
    ("pocket", 90, 60, [[0, 3, 7, 10], [5, 8, 12, 15], [-2, 2, 5, 9], [3, 7, 10, 14]], 0.10),
    ("drift", 76, 55, [[0, 4, 7, 14], [-3, 0, 4, 7], [5, 9, 12, 16], [7, 11, 14, 17]], 0.06),
    ("bounce", 96, 62, [[0, 4, 7, 11], [-5, -1, 2, 7], [-3, 0, 4, 7], [5, 9, 12, 16]], 0.12),
    ("night", 72, 53, [[0, 3, 7, 10], [-4, 0, 3, 7], [-7, -3, 0, 5], [-2, 2, 5, 9]], 0.07),
    ("spark", 100, 59, [[0, 4, 7, 9], [5, 9, 12, 14], [7, 11, 14, 17], [4, 7, 11, 14]], 0.10),
]

def make(name, bpm, root, prog, swing, seconds=20):
    beat = 60 / bpm; bar = 4 * beat
    n = int(seconds * SR); buf = np.zeros(n)
    nbars = int(np.ceil(seconds / bar))
    for b in range(nbars):
        t0 = b * bar
        ch = prog[b % len(prog)]
        for k, iv in enumerate(ch):  # slightly strummed chord
            add(buf, keys(midi(root + iv), bar * 1.1, 0.16), t0 + k * 0.012)
        add(buf, keys(midi(root + ch[-1] + 12), beat * 1.5, 0.06), t0 + 2.5 * beat)
        add(buf, bass(midi(root + ch[0] - 24), bar * 0.9), t0)
        add(buf, bass(midi(root + ch[0] - 24), beat * 1.2, 0.4), t0 + 2.5 * beat)
        add(buf, kick(), t0); add(buf, kick(0.7), t0 + 2.5 * beat)
        add(buf, snare(), t0 + beat); add(buf, snare(), t0 + 3 * beat)
        for e in range(8):
            off = (swing * beat) if e % 2 else 0
            add(buf, hat(0.12 if e % 2 == 0 else 0.07), t0 + e * beat / 2 + off)
    # warm it up: lowpass + vinyl crackle + hiss
    buf = lp(buf, 5200)
    crackle = np.zeros(n)
    idx = rng.integers(0, n, size=int(seconds * 9))
    crackle[idx] = rng.uniform(-0.15, 0.15, size=len(idx))
    buf += lp(crackle, 3000) + 0.004 * lp(rng.standard_normal(n), 4000)
    buf /= np.max(np.abs(buf)) + 1e-9
    buf *= 0.85
    st = np.stack([buf, np.roll(buf, int(0.012 * SR))], 1)  # tiny stereo width
    wavfile.write(f"/home/claude/odds/music/{name}.wav", SR, (st * 32767).astype(np.int16))

if __name__ == "__main__":
    import os; os.makedirs("/home/claude/odds/music", exist_ok=True)
    for tr in TRACKS:
        make(*tr)
        print("made", tr[0])


# ---------------------------------------------------------------- unique track per video
PROGS = [
    [[0, 4, 7, 11], [5, 9, 12, 16], [2, 5, 9, 12], [7, 11, 14, 17]],
    [[0, 3, 7, 10], [5, 8, 12, 15], [-2, 2, 5, 9], [3, 7, 10, 14]],
    [[0, 4, 7, 14], [-3, 0, 4, 7], [5, 9, 12, 16], [7, 11, 14, 17]],
    [[0, 4, 7, 11], [-5, -1, 2, 7], [-3, 0, 4, 7], [5, 9, 12, 16]],
    [[0, 3, 7, 10], [-4, 0, 3, 7], [-7, -3, 0, 5], [-2, 2, 5, 9]],
    [[0, 4, 7, 9], [5, 9, 12, 14], [7, 11, 14, 17], [4, 7, 11, 14]],
    [[0, 4, 7, 11], [9, 12, 16, 19], [5, 9, 12, 16], [7, 11, 14, 17]],
    [[0, 3, 7, 10], [8, 12, 15, 19], [3, 7, 10, 14], [10, 14, 17, 20]],
    [[0, 4, 7, 11], [2, 5, 9, 12], [4, 7, 11, 14], [5, 9, 12, 16]],
    [[0, 3, 7, 10], [5, 8, 12, 15], [7, 10, 14, 17], [3, 7, 10, 14]],
]

def make_unique(seed_text, out_path, seconds=12):
    """A different original track for every video: key, tempo, chords, swing, tone,
    drum pattern and a little melody are all derived from the video's id."""
    import hashlib
    seed = int(hashlib.sha256(seed_text.encode()).hexdigest()[:8], 16)
    r = np.random.default_rng(seed)
    global rng
    rng = np.random.default_rng(seed + 1)
    bpm = int(r.integers(78, 112))
    root = int(r.integers(52, 64))
    prog = [list(c) for c in PROGS[int(r.integers(len(PROGS)))]]
    if r.random() < 0.5:
        prog = prog[1:] + prog[:1]  # rotate the progression
    swing = float(r.uniform(0.04, 0.14))
    decay = float(r.uniform(1.2, 2.6))
    bright = float(r.uniform(0.2, 0.5))
    kick_alt = r.random() < 0.5
    hat_16 = r.random() < 0.4
    scale = [0, 2, 4, 7, 9, 12, 14, 16]  # pentatonic-ish for the melody
    beat = 60 / bpm; bar = 4 * beat
    n = int(seconds * SR); buf = np.zeros(n)

    def keys_v(freq, dur, vel):
        t = np.arange(int(dur * SR)) / SR
        env = np.exp(-t * decay) * (1 - np.exp(-t * 300))
        s = (np.sin(2 * np.pi * freq * t) + bright * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t * 4)
             + 0.12 * np.sin(2 * np.pi * 3 * freq * t) * np.exp(-t * 7))
        return vel * s * env * (1 + 0.07 * np.sin(2 * np.pi * 4.5 * t))

    for b in range(int(np.ceil(seconds / bar))):
        t0 = b * bar; ch = prog[b % len(prog)]
        for k, iv in enumerate(ch):
            add(buf, keys_v(midi(root + iv), bar * 1.1, 0.15), t0 + k * 0.012)
        add(buf, bass(midi(root + ch[0] - 24), bar * 0.9), t0)
        add(buf, kick(), t0)
        add(buf, kick(0.7), t0 + (2.5 if kick_alt else 2.0) * beat)
        add(buf, snare(), t0 + beat); add(buf, snare(), t0 + 3 * beat)
        steps = 16 if hat_16 else 8
        for e in range(steps):
            off = (swing * beat) if e % 2 else 0
            add(buf, hat(0.10 if e % 2 == 0 else 0.06), t0 + e * bar / steps + off)
        for m in range(4):  # short melody line, different every bar
            if r.random() < 0.7:
                note = root + 12 + scale[int(r.integers(len(scale)))]
                add(buf, keys_v(midi(note), beat * 0.9, 0.07), t0 + m * beat + (0.5 * beat if r.random() < 0.3 else 0))
    buf = lp(buf, float(r.uniform(4200, 6500)))
    crackle = np.zeros(n); idx = rng.integers(0, n, size=int(seconds * 8))
    crackle[idx] = rng.uniform(-0.12, 0.12, size=len(idx))
    buf += lp(crackle, 3000) + 0.004 * lp(rng.standard_normal(n), 4000)
    buf /= np.max(np.abs(buf)) + 1e-9; buf *= 0.85
    st = np.stack([buf, np.roll(buf, int(0.012 * SR))], 1)
    wavfile.write(out_path, SR, (st * 32767).astype(np.int16))
    return dict(bpm=bpm, root=root)


# ---------------------------------------------------------------- v2: different STYLES, not just different notes
STYLES = ["lofi", "synthwave", "marimba", "piano", "chiptune", "trap", "funk", "ambient", "phonk", "tension"]

def _osc(kind, freq, n, detune=0.0):
    t = np.arange(n) / SR
    ph = 2 * np.pi * freq * t
    if kind == "sine": return np.sin(ph)
    if kind == "square": return np.sign(np.sin(ph)) * 0.6
    if kind == "saw":
        s = 2 * ((freq * t) % 1) - 1
        if detune: s = 0.5 * s + 0.5 * (2 * ((freq * (1 + detune) * t) % 1) - 1)
        return s * 0.6
    if kind == "tri": return 2 * np.abs(2 * ((freq * t) % 1) - 1) - 1
    return np.sin(ph)

def _note(kind, freq, dur, vel, att=0.005, dec=2.0, sus=0.0, h2=0.0):
    n = max(1, int(dur * SR)); t = np.arange(n) / SR
    env = np.minimum(1, t / att) * (sus + (1 - sus) * np.exp(-t * dec))
    rel = min(n, int(0.03 * SR)); env[-rel:] *= np.linspace(1, 0, rel)
    s = _osc(kind, freq, n)
    if h2: s = s + h2 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t * dec * 2)
    return vel * s * env

def _noise_hit(dur, vel, lo, hi, dec, r):
    n = int(dur * SR); x = r.standard_normal(n)
    from scipy.signal import butter, lfilter
    b, a = butter(2, [lo / (SR / 2), min(hi, SR / 2 - 100) / (SR / 2)], "band")
    return vel * lfilter(b, a, x) * np.exp(-np.arange(n) / SR * dec)

def _kick808(vel=0.9, length=0.6):
    t = np.arange(int(length * SR)) / SR
    f = 55 + 90 * np.exp(-t * 25)
    return vel * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.5)

def make_styled(seed_text, out_path, seconds=12, style=None):
    """Original track whose STYLE (instruments, drums, tempo feel) is chosen from 8 genres, plus key/tempo/chords/melody
    all derived from seed_text. Returns the style used. Copyright-free: every sound is synthesized here."""
    import hashlib
    seed = int(hashlib.sha256(seed_text.encode()).hexdigest()[:8], 16)
    r = np.random.default_rng(seed); nr = np.random.default_rng(seed + 99)
    style = style or STYLES[seed % len(STYLES)]
    bpm = {"lofi": (76, 92), "synthwave": (100, 118), "marimba": (96, 120), "piano": (64, 80), "chiptune": (128, 150),
           "trap": (130, 150), "funk": (98, 112), "ambient": (60, 72), "phonk": (128, 140), "tension": (88, 100)}[style]
    bpm = int(r.integers(*bpm)); beat = 60 / bpm; bar = 4 * beat
    root = int(r.integers(50, 62))
    prog = [list(c) for c in PROGS[int(r.integers(len(PROGS)))]]
    if r.random() < 0.5: prog = prog[2:] + prog[:2]
    n = int(seconds * SR); buf = np.zeros(n)
    scale = [0, 2, 3, 5, 7, 9, 10, 12, 14, 15] if prog[0][1] == 3 else [0, 2, 4, 5, 7, 9, 11, 12, 14, 16]
    mel_seed = [int(r.integers(len(scale))) for _ in range(16)]
    for b in range(int(np.ceil(seconds / bar))):
        t0 = b * bar; ch = prog[b % len(prog)]
        if style == "lofi":
            for k, iv in enumerate(ch): add(buf, keys(midi(root + iv), bar * 1.1, 0.14), t0 + k * 0.015)
            add(buf, bass(midi(root + ch[0] - 24), bar * 0.9), t0)
            add(buf, kick(), t0); add(buf, kick(0.6), t0 + 2.5 * beat)
            add(buf, snare(0.3), t0 + beat); add(buf, snare(0.3), t0 + 3 * beat)
            for e in range(8): add(buf, hat(0.1 if e % 2 == 0 else 0.06), t0 + e * beat / 2 + (0.1 * beat if e % 2 else 0))
        elif style == "synthwave":
            for iv in ch: add(buf, _note("saw", midi(root + iv), bar, 0.07, att=0.08, dec=0.3, sus=0.6), t0)
            for e in range(16):  # 16th arpeggio
                iv = ch[e % len(ch)] + (12 if (e // 4) % 2 else 0)
                add(buf, _note("square", midi(root + iv + 12), beat / 4, 0.05, dec=10), t0 + e * beat / 4)
            for q in range(4):
                add(buf, kick(0.9), t0 + q * beat)
                add(buf, _note("saw", midi(root + ch[0] - 24), beat / 2, 0.22, dec=4), t0 + q * beat + beat / 2)
            add(buf, _noise_hit(0.3, 0.35, 1500, 8000, 12, nr), t0 + beat); add(buf, _noise_hit(0.3, 0.35, 1500, 8000, 12, nr), t0 + 3 * beat)
        elif style == "marimba":
            for e in range(8):
                deg = scale[(mel_seed[(b * 3 + e) % 16] + e) % len(scale)]
                x = _note("sine", midi(root + 12 + deg), 0.5, 0.16, dec=9)
                x = x + 0.4 * _note("sine", midi(root + 12 + deg) * 4, 0.5, 0.05, dec=30)
                add(buf, x, t0 + e * beat / 2)
            add(buf, _note("sine", midi(root + ch[0] - 12), bar * 0.6, 0.3, dec=2), t0)
            for e in range(16): add(buf, _noise_hit(0.05, 0.05 if e % 2 else 0.08, 5000, 12000, 80, nr), t0 + e * beat / 4)
            add(buf, _noise_hit(0.08, 0.25, 600, 2500, 40, nr), t0 + 1.5 * beat); add(buf, _noise_hit(0.08, 0.25, 600, 2500, 40, nr), t0 + 3 * beat)
            add(buf, kick(0.5), t0)
        elif style == "piano":
            for k, iv in enumerate(ch):
                add(buf, _note("sine", midi(root + iv), bar * 1.4, 0.1, dec=1.2, h2=0.5), t0 + k * 0.05)
            for e in range(4):
                deg = scale[mel_seed[(b * 4 + e) % 16]]
                if r.random() < 0.8: add(buf, _note("sine", midi(root + 12 + deg), beat * 1.5, 0.13, dec=1.6, h2=0.4), t0 + e * beat)
            add(buf, _note("sine", midi(root + ch[0] - 24), bar, 0.25, dec=0.8), t0)
        elif style == "chiptune":
            for e in range(8):
                deg = scale[mel_seed[(b * 8 + e) % 16]]
                add(buf, _note("square", midi(root + 12 + deg), beat / 2 * 0.9, 0.07, dec=3, sus=0.5), t0 + e * beat / 2)
            for e in range(8):
                add(buf, _note("tri", midi(root + ch[e % 2 * 2] - 12), beat / 2 * 0.9, 0.25, dec=1, sus=0.6), t0 + e * beat / 2)
            add(buf, _note("square", 60, 0.08, 0.3, dec=40), t0); add(buf, _note("square", 60, 0.08, 0.3, dec=40), t0 + 2 * beat)
            for q in (1, 3): add(buf, _noise_hit(0.12, 0.3, 2000, 9000, 30, nr), t0 + q * beat)
        elif style == "trap":
            for iv in ch[:3]: add(buf, _note("tri", midi(root + iv + 12), bar, 0.05, att=0.1, dec=0.2, sus=0.7), t0)
            add(buf, _kick808(0.8, bar * 0.45), t0); add(buf, _kick808(0.6, beat * 1.2), t0 + 2.75 * beat)
            add(buf, _noise_hit(0.25, 0.4, 1200, 9000, 14, nr), t0 + 2 * beat)
            steps = [i * beat / 4 for i in range(16)]
            if r.random() < 0.6: steps += [3 * beat + i * beat / 12 for i in range(6)]  # hat roll
            for s in steps: add(buf, _noise_hit(0.03, 0.07, 7000, 15000, 120, nr), t0 + s)
            for e in range(2):
                deg = scale[mel_seed[(b * 2 + e) % 16]]
                add(buf, _note("sine", midi(root + 24 + deg), beat, 0.06, dec=3), t0 + e * 2 * beat + beat)
        elif style == "funk":
            for e in range(8):
                if (b + e) % 3 != 2:
                    add(buf, _note("saw", midi(root + ch[0] - 12 + (12 if e % 4 == 3 else 0)), beat / 2 * 0.6, 0.18, dec=8), t0 + e * beat / 2)
            for e in (1, 3):
                for iv in ch: add(buf, _note("square", midi(root + iv), beat * 0.25, 0.04, dec=14), t0 + e * beat + beat / 2)
            add(buf, kick(0.9), t0); add(buf, kick(0.7), t0 + 1.75 * beat); add(buf, kick(0.8), t0 + 2.5 * beat)
            add(buf, snare(0.35), t0 + beat); add(buf, snare(0.35), t0 + 3 * beat)
            for e in range(16): add(buf, hat(0.08 if e % 4 == 2 else 0.04), t0 + e * beat / 4)
        elif style == "phonk":
            # drift-phonk feel: cowbell melody, distorted 808 slides, hard kick, snare on 3
            for e in range(8):
                deg = scale[mel_seed[(b * 8 + e) % 16] % 6]
                f0 = midi(root + 24 + deg)
                x = _note("square", f0, beat / 2 * 0.7, 0.10, dec=9) + _note("square", f0 * 1.48, beat / 2 * 0.7, 0.06, dec=9)
                add(buf, lp(x, 3800), t0 + e * beat / 2)
            k8 = np.tanh(3.0 * _kick808(0.9, bar * 0.5)) * 0.5
            add(buf, k8, t0); add(buf, np.tanh(3.0 * _kick808(0.8, beat)) * 0.45, t0 + 2.5 * beat)
            add(buf, kick(1.0), t0); add(buf, kick(0.8), t0 + 1.5 * beat)
            add(buf, _noise_hit(0.22, 0.55, 1200, 9000, 16, nr), t0 + 2 * beat)
            for e in range(16): add(buf, _noise_hit(0.03, 0.07 if e % 2 else 0.11, 7000, 15000, 120, nr), t0 + e * beat / 4)
        elif style == "tension":
            # cinematic suspense: low drone, rising Shepard-style tone, taiko hits, clock-like ticks
            n_bar = int(bar * SR); t = np.arange(n_bar) / SR
            drone = 0.10 * (np.sin(2 * np.pi * midi(root - 24) * t) + 0.5 * np.sin(2 * np.pi * midi(root - 17) * t))
            add(buf, drone, t0)
            prog_t = (b / max(1, int(np.ceil(seconds / bar)))) + t / bar / max(1, int(np.ceil(seconds / bar)))
            for o in range(4):
                fr = midi(root - 12) * 2 ** ((o + prog_t) % 4)
                amp = np.exp(-((((o + prog_t) % 4) - 2) ** 2))
                add(buf, 0.035 * amp * np.sin(2 * np.pi * np.cumsum(fr) / SR), t0)
            for q in (0, 2.5):
                add(buf, 0.9 * np.sin(2 * np.pi * (60 + 80 * np.exp(-np.arange(int(0.5 * SR)) / SR * 18)) * np.arange(int(0.5 * SR)) / SR) * np.exp(-np.arange(int(0.5 * SR)) / SR * 6), t0 + q * beat)
            for e in range(8): add(buf, _note("sine", 1800, 0.03, 0.05, dec=120), t0 + e * beat / 2)
        else:  # ambient
            for iv in ch: add(buf, _note("tri", midi(root + iv), bar * 1.6, 0.07, att=0.6, dec=0.4, sus=0.5), t0)
            for e in range(3):
                deg = scale[mel_seed[(b * 3 + e) % 16]]
                add(buf, _note("sine", midi(root + 24 + deg), beat * 2, 0.06, att=0.05, dec=1.0), t0 + e * beat * 1.33)
            add(buf, _note("sine", midi(root + ch[0] - 24), bar, 0.2, att=0.2, dec=0.3, sus=0.6), t0)
    buf = lp(buf, float(r.uniform(5000, 9000))) if style not in ("chiptune",) else buf
    if style in ("lofi",):
        crackle = np.zeros(n); idx = nr.integers(0, n, size=int(seconds * 8))
        crackle[idx] = nr.uniform(-0.12, 0.12, size=len(idx)); buf += lp(crackle, 3000)
    buf /= np.max(np.abs(buf)) + 1e-9; buf *= 0.85
    st = np.stack([buf, np.roll(buf, int(0.012 * SR))], 1)
    wavfile.write(out_path, SR, (st * 32767).astype(np.int16))
    return style


def pick_style(video_id, avoid_last=5, log="/home/claude/odds/music/style_log.txt", pool=None):
    """Choose a style for this video that none of the last `avoid_last` videos used, and record it."""
    import hashlib, os
    hist = open(log).read().split() if os.path.exists(log) else []
    recent = [h.split(":")[1] for h in hist[-avoid_last:] if ":" in h]
    base = pool or STYLES
    choices = [s for s in base if s not in recent] or base
    seed = int(hashlib.sha256(video_id.encode()).hexdigest()[:8], 16)
    st = choices[seed % len(choices)]
    with open(log, "a") as f: f.write(f"{video_id}:{st}\n")
    return st
