"""Demo 1: the template's bouncing ball, drawn with skia-python instead of a browser.
Same idea as template/scene.html: height is computed from t, never accumulated."""
import math
from common import *

DURATION = 8.0
G, FLOOR, TOP, E = 250.0, 660.0, 140.0, 0.6        # px/s^2, px, px, bounce factor
DROP_AT = 0.8
# Captions are timed to the physics: the fall lasts from 0.8 s to about 2.8 s.
BEATS = [(0.0, 1.6, "A ball is dropped."),
         (1.6, 3.4, "It speeds up as it falls."),
         (3.4, 8.0, "Each bounce loses height.")]

def ball_y(t):
    tt = t - DROP_AT
    if tt < 0: return TOP
    fall = math.sqrt(2 * (FLOOR - TOP) / G)
    if tt < fall: return TOP + 0.5 * G * tt * tt
    tt -= fall; v = G * fall * E
    while v > 30:
        flight = 2 * v / G
        if tt < flight: return FLOOR - (v * tt - 0.5 * G * tt * tt)
        tt -= flight; v *= E
    return FLOOR

def bounce_times():
    """Sound cues come from the same physics that draws the ball."""
    fall = math.sqrt(2 * (FLOOR - TOP) / G)
    t, v, out = DROP_AT + fall, G * fall * E, []
    while v > 30 and t < DURATION:
        out.append((t, v)); t += 2 * v / G; v *= E
    return out

def draw(c, t):
    c.clear(color("#16202b"))
    c.drawRect(skia.Rect.MakeXYWH(0, FLOOR, W, 30), paint("#2d3e50"))
    y = ball_y(t)
    # ghost positions from the recent past show speed: the gaps grow as it speeds up
    for k in (3, 2, 1):
        yk = ball_y(t - 0.08 * k)
        if abs(yk - y) > 4:
            c.drawCircle(W / 2, yk - 30, 30, paint("#f2b134", 0.12 * (4 - k)))
    s = 1 - (FLOOR - y) / 900
    c.drawOval(skia.Rect.MakeXYWH(W / 2 - 60 * s, FLOOR - 12 * s + 2, 120 * s, 24 * s), paint("#000000", 0.35))
    # squash for a few frames around each landing, based on distance to the floor
    sq = clamp(1 - (FLOOR - y) / 18) * 0.25
    r = 30
    c.drawOval(skia.Rect.MakeXYWH(W / 2 - r * (1 + sq), y - 2 * r * (1 - sq), 2 * r * (1 + sq), 2 * r * (1 - sq)),
               paint("#f2b134"))
    for a, b, s_ in BEATS:
        if a <= t < b: caption(c, s_, ease(window(t, a, b, 0.25)))

def checks():
    lands = bounce_times()[0][0]
    assert BEATS[1][0] < lands < BEATS[1][1], 'the speeding-up caption must cover the first fall'
    assert ball_y(0) == ball_y(DROP_AT - 0.01) == TOP
    print('checks passed: first landing at %.2f s' % lands)

def soundtrack(path):
    n = int(DURATION * SR); music = np.zeros(n); fx = np.zeros(n)
    for bar, f in enumerate([220.0, 196.0, 174.61, 220.0]):          # 120 bpm: one bar = 2 s
        for k, ratio in enumerate([1, 1.26, 1.5]):
            place(music, 0.06 * tone(f * ratio, 2.0, "pad", seed=bar * 10 + k), bar * 2.0)
    for t, v in bounce_times():
        place(fx, (v / 700) * tone(90, 0.15, "thump"), t)
    for a, _, _ in BEATS: place(fx, tone(1800, 0.05, "tick"), a)
    write_wav(path, music, fx)
