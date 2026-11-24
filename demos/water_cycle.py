"""Demo 3: the water cycle as a seamless 20-second loop.

Everything moves with the phase u = t / T. Anything that repeats inside the loop
repeats a whole number of times, so the frame at t = T is the frame at t = 0 and
the clip can play on repeat with no jump. checks() renders both and compares them."""
import math
from common import *

DURATION = T = 20.0
SEA_Y = 700                      # sea surface
RNG = np.random.default_rng(7)   # one seeded stream, used only at import time
VAPOR = [(RNG.uniform(140, 760), RNG.uniform(0, 1), RNG.uniform(0, 2 * math.pi)) for _ in range(46)]
RAIN = [(RNG.uniform(-150, 150), RNG.uniform(0, 1)) for _ in range(70)]

STAGES = [(0.0, 5.0, "Evaporation", "The sun warms the sea, and water rises as vapor."),
          (5.0, 10.0, "Condensation", "High up it cools and gathers into a cloud."),
          (10.0, 15.0, "Precipitation", "The wind carries the cloud inland, and it rains."),
          (15.0, 20.0, "Collection", "Rivers carry the water back to the sea.")]

def frac(x): return x - math.floor(x)
def smooth_window(t, a, b, fade):
    """A soft on/off window on the loop's clock: an interval that runs past T wraps round to 0."""
    return ease(max(window(t + k * T, a, b, fade) for k in (-1, 0, 1)))

def cloud_state(t):
    """Cloud size 0..1 and centre x. It is gone at t = 0 and t = T, so the loop is seamless."""
    grow = ease((t - 3.5) / 5.5)                    # forms from 3.5 s to 9 s
    shrink = 1 - ease((t - 12.5) / 5.0)             # rains itself out from 12.5 s to 17.5 s
    size = grow * shrink
    x = lerp(460, 1320, ease((t - 9.2) / 2.6))      # drifts inland 9.2 s to 11.8 s
    return size, x

def rain_amount(t): return smooth_window(t, 11.8, 17.2, 0.8)
def river_amount(t): return 0.35 + 0.65 * smooth_window(t, 13.0, 22.0, 1.5)

MOUNTAIN = [(980, SEA_Y + 20), (1180, 470), (1300, 520), (1420, 360), (1600, 500), (1760, 560), (1920, 600), (1920, H), (1150, H)]
RIVER = [(1420, 400), (1390, 470), (1330, 540), (1250, 600), (1150, 650), (1040, 690), (930, SEA_Y + 6)]

def path_from(points, close=False):
    p = skia.Path(); p.moveTo(*points[0])
    for q in points[1:]: p.lineTo(*q)
    if close: p.close()
    return p

def draw_cloud(c, cx, cy, size, a):
    if size <= 0.01: return
    pnt = paint("#e8eef6", a)
    for dx, dy, r in [(-110, 10, 70), (-40, -30, 90), (50, -10, 80), (120, 15, 60), (0, 30, 75)]:
        c.drawCircle(cx + dx * size, cy + dy * size, r * size, pnt)

def draw(c, t):
    t = t % T
    # sky, sun, sea, land
    c.clear(color("#0f1a2b"))
    glow = 0.5 + 0.5 * math.cos(2 * math.pi * 2 * t / T)          # two pulses per loop
    c.drawCircle(230, 170, 80 + 6 * glow, paint("#f2b53c", 0.25))
    c.drawCircle(230, 170, 62, paint("#f2b53c"))
    sea = skia.Path(); sea.moveTo(0, SEA_Y)
    for x in range(0, 1301, 20):
        sea.lineTo(x, SEA_Y + 6 * math.sin(x / 70 + 2 * math.pi * 3 * t / T))   # three wave cycles per loop
    sea.lineTo(1300, H); sea.lineTo(0, H); sea.close()
    c.drawPath(sea, paint("#2a6fb0"))
    c.drawPath(path_from(MOUNTAIN, True), paint("#3c5a3f"))
    c.drawPath(path_from([(1380, 395), (1420, 360), (1462, 392), (1440, 400), (1420, 388), (1400, 402)], True), paint("#e8eef6"))
    # river: dashes flow downhill, four laps per loop
    rv = river_amount(t)
    river = path_from(RIVER)
    c.drawPath(river, paint("#2a6fb0", 1, stroke=14))
    dash = skia.Paint(Color=color("#9fd0ff", rv), Style=skia.Paint.kStroke_Style, StrokeWidth=5, AntiAlias=True,
                      PathEffect=skia.DashPathEffect.Make([26, 30], -56 * 4 * t / T * 6))
    c.drawPath(river, dash)
    # evaporation: vapor wisps rise from the sea, two laps per loop each
    ev = 0.25 + 0.75 * smooth_window(t, 19.0, 27.0, 1.5)
    for x, off, ph in VAPOR:
        k = frac(2 * t / T + off)
        y = SEA_Y - 20 - k * 360
        xx = x + 14 * math.sin(ph + 2 * math.pi * 4 * t / T + k * 6)
        a = ev * 0.55 * math.sin(math.pi * k)
        c.drawCircle(xx, y, 5 + 4 * k, paint("#cfe6ff", a))
    # cloud and rain
    size, cx = cloud_state(t)
    draw_cloud(c, cx, 230, size, 0.95)
    ra = rain_amount(t)
    if ra > 0:
        c.save(); c.clipPath(path_from(MOUNTAIN, True), skia.ClipOp.kDifference, True)   # rain stops at the ground
        for dx, off in RAIN:
            k = frac(5 * t / T + off)                       # five falls per loop
            x0, y0 = cx + dx * max(size, 0.4), 270 + k * 300
            c.drawLine(x0, y0, x0 - 6, y0 + 26, paint("#9fd0ff", ra * 0.8 * min(1, 4 * (1 - k)), stroke=3))
        c.restore()
    # stage labels on the diagram, the current one lit
    labels = [(330, 655, 0), (cx, 88, 1), (1690, 330, 2), (1110, 590, 3)]
    for x, y, i in labels:
        a, b, name, _ = STAGES[i]
        lit = smooth_window(t, a - 0.4 if i == 0 else a, b, 0.4)
        if i == 1 and size < 0.3: continue
        text(c, name, x, y, 38, "#ffffff", 0.35 + 0.65 * lit, bold=lit > 0.5)
    for a, b, _, s in STAGES:
        al = smooth_window(t, a, b, 0.35)
        if al > 0: caption(c, s, al)

def _frame(t):
    surf = skia.Surface(W, H)
    with surf as c: draw(c, t)
    return surf.makeImageSnapshot().toarray().astype(int)

def checks():
    d = np.abs(_frame(0.0) - _frame(T - 1e-9)).max()
    assert d <= 2, f"loop seam: frame at T differs from frame 0 by {d}"
    # each stage's visible process is strongest while its caption shows
    assert cloud_state(0)[0] == 0 and cloud_state(7.5)[0] > 0.6 and rain_amount(14) > 0.9 and rain_amount(2) == 0
    print(f"checks passed: frame T matches frame 0 (max channel difference {d})")

def soundtrack(path):
    n = int(T * SR); music = np.zeros(n); fx = np.zeros(n)
    bar = 2.0                                               # 120 bpm, ten bars per loop
    prog = [[196.0, 246.94, 293.66], [164.81, 196.0, 246.94], [130.81, 164.81, 196.0], [146.83, 185.0, 220.0]]
    for k in range(10):
        for j, f in enumerate(prog[(k // 2) % 4] if k < 8 else prog[k - 8]):
            place(music, 0.045 * tone(f, bar, "pad", seed=10 * k + j), k * bar)
    rng = np.random.default_rng(11)
    for k in range(10):                                     # rising plucks while vapor rises
        if k * 0.5 < 6: place(fx, 0.25 * tone([587.33, 659.25, 783.99, 880.0][k % 4], 0.5, "pluck", seed=k), 0.5 + k * 0.5)
    place(fx, 0.3 * tone(0, 2.5, "whoosh", seed=3), 9.2)    # wind carries the cloud
    for _ in range(90):                                     # raindrops, following the rain's own envelope
        at = rng.uniform(11.8, 17.2)
        place(fx, 0.18 * rain_amount(at) * tone(rng.uniform(900, 1800), 0.12, "drop", seed=int(at * 100)), at)
    for a, _, _, _ in STAGES: place(fx, tone(1600, 0.05, "tick"), a + 0.02)
    # nothing may ring past the end, or the loop clicks
    tail = int(0.03 * SR); music[-tail:] *= np.linspace(1, 0, tail); fx[-tail:] *= np.linspace(1, 0, tail)
    write_wav(path, music, fx)
