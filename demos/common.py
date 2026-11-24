"""Shared helpers for the demos: a parallel frame renderer, a tiny synth, and the mux step.

Each demo defines DURATION, draw(canvas, t), checks() and soundtrack(path). draw must be a
pure function of t: same t, same picture, whatever was drawn before.
Renders with skia-python (no browser). Frames go to $WORK (default ./work).
"""
import os, sys, json, subprocess, wave
from multiprocessing import Pool
import numpy as np
import skia

W, H, FPS = 1920, 1080, 30
WORK = os.environ.get("WORK", "work")

# ---------- drawing helpers ----------
def color(hex_, a=1.0):
    hex_ = hex_.lstrip("#")
    r, g, b = int(hex_[0:2], 16), int(hex_[2:4], 16), int(hex_[4:6], 16)
    return skia.Color(r, g, b, int(round(255 * max(0.0, min(1.0, a)))))

def paint(hex_, a=1.0, stroke=0.0):
    p = skia.Paint(AntiAlias=True, Color=color(hex_, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        p.setStrokeJoin(skia.Paint.kRound_Join); p.setStrokeCap(skia.Paint.kRound_Cap)
    return p

_FONT_CACHE = {}
def font(size, bold=False):
    key = (size, bold)
    if key not in _FONT_CACHE:
        style = skia.FontStyle.Bold() if bold else skia.FontStyle.Normal()
        tf = skia.Typeface.MakeFromName("DejaVu Sans", style)
        _FONT_CACHE[key] = skia.Font(tf, size)
    return _FONT_CACHE[key]

def text(c, s, x, y, size=44, hex_="#ffffff", a=1.0, bold=False, align="center"):
    f = font(size, bold)
    w = f.measureText(s)
    if align == "center": x -= w / 2
    elif align == "right": x -= w
    c.drawString(s, x, y, f, paint(hex_, a))
    return w

def caption(c, s, a=1.0):
    """Caption at 64 px bold on a dark panel, kept above the bottom 15% of the frame."""
    if a <= 0 or not s: return
    f = font(64, True)
    w = f.measureText(s) + 90
    y = 860
    c.drawRoundRect(skia.Rect.MakeXYWH((W - w) / 2, y - 66, w, 96), 18, 18, paint("#000000", 0.55 * a))
    text(c, s, W / 2, y, 64, "#ffffff", a, bold=True)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(u):
    u = clamp(u); return u * u * (3 - 2 * u)
def lerp(a, b, u): return a + (b - a) * u
def window(t, start, end, fade=0.3):
    """0..1 opacity for something shown from start to end with soft edges."""
    return min(clamp((t - start) / fade), clamp((end - t) / fade))

# ---------- rendering ----------
def _render_range(args):
    mod_name, idxs = args
    mod = __import__(mod_name)
    surf = skia.Surface(W, H)
    for i in idxs:
        path = f"{WORK}/frames/{i:05d}.jpg"
        if os.path.exists(path): continue              # resumable
        with surf as c:
            c.clear(skia.ColorBLACK)
            mod.draw(c, i / FPS)
        surf.makeImageSnapshot().save(path, skia.kJPEG, 92)
    return len(idxs)

def render(mod_name, duration, workers=4):
    os.makedirs(f"{WORK}/frames", exist_ok=True)
    n = int(round(duration * FPS))
    chunks = [(mod_name, list(range(w, n, workers))) for w in range(workers)]
    import time; t0 = time.time()
    with Pool(workers) as p: p.map(_render_range, chunks)
    dt = time.time() - t0
    print(f"{n} frames in {dt:.1f} s ({n / dt / workers:.1f} fps per worker)")
    return n

def still(mod_name, t, path):
    mod = __import__(mod_name)
    surf = skia.Surface(W, H)
    with surf as c:
        c.clear(skia.ColorBLACK); mod.draw(c, t)
    surf.makeImageSnapshot().save(path, skia.kPNG)

# ---------- audio ----------
SR = 48000
def env(n, attack=0.01, release=0.05):
    e = np.ones(n); a = max(1, int(attack * SR)); r = max(1, int(release * SR))
    e[:a] = np.linspace(0, 1, a); e[-r:] *= np.linspace(1, 0, r)   # always fade out: no clicks
    return e

def tone(freq, dur, kind="pluck", seed=0):
    n = int(dur * SR); t = np.arange(n) / SR
    rng = np.random.default_rng(seed)
    if kind == "pluck":     # additive, quick decay
        s = sum((0.6 ** k) * np.sin(2 * np.pi * freq * (k + 1) * t + rng.uniform(0, 6.28)) for k in range(4))
        return 0.5 * s * np.exp(-t * 5) * env(n, 0.004, 0.05)
    if kind == "pad":       # detuned stack, random phases so it doesn't throb
        s = sum(np.sin(2 * np.pi * (freq + d) * t + rng.uniform(0, 6.28)) for d in (-0.35, 0, 0.35))
        return 0.33 * s * env(n, min(0.4, dur / 3), min(0.5, dur / 3))
    if kind == "thump":
        return np.sin(2 * np.pi * freq * t) * np.exp(-t * 35) * env(n, 0.001, 0.02)
    if kind == "tick":
        return 0.4 * np.sin(2 * np.pi * freq * t) * np.exp(-t * 90) * env(n, 0.001, 0.01)
    if kind == "whoosh":
        noise = rng.standard_normal(n)
        k = np.ones(40) / 40; noise = np.convolve(noise, k, mode="same")   # soften highs
        return 0.8 * noise * np.sin(np.pi * t / dur) ** 2
    if kind == "drop":      # short falling blip for raindrops
        f = freq * (1 + 1.5 * np.exp(-t * 60))
        return 0.3 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 40) * env(n, 0.001, 0.01)
    raise ValueError(kind)

def place(bus, sig, at):
    s = int(at * SR); e = min(len(bus), s + len(sig))
    if 0 <= s < len(bus): bus[s:e] += sig[:e - s]

def write_wav(path, music, fx):
    fx_env = np.convolve(np.abs(fx), np.ones(2400) / 2400, mode="same")
    duck = 1 - 0.5 * np.clip(fx_env / (fx_env.max() + 1e-9) * 4, 0, 1)     # ~6 dB under effects
    out = music * duck + fx
    out *= 0.7 / (np.max(np.abs(out)) + 1e-9)
    pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

# ---------- mux and QA ----------
def mux(out_mp4, wav):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{WORK}/frames/%05d.jpg",
        "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-tune", "animation",
        "-movflags", "+faststart", "-af", "loudnorm=I=-15:TP=-2:LRA=11,alimiter=limit=0.7:level=false",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", out_mp4], check=True)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", out_mp4, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    peak = [l for l in r.splitlines() if "Peak:" in l][-1].strip()
    print("true peak after encoding:", peak)

def contact_sheet(mp4, out_jpg, n=12):
    """Sheet the FINAL MP4, not the frames, so encode problems show too."""
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                               capture_output=True, text=True).stdout)
    fps = n / dur
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-vf",
                    f"fps={fps:.5f},scale=480:-1,tile=4x3", "-frames:v", "1", out_jpg], check=True)
