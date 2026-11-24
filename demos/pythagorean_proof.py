"""Demo 2: why a^2 + b^2 = c^2, by rearranging four triangles inside one square.

Every triangle moves rigidly (rotate + translate), so its area never changes.
The leftover area is computed from the actual polygons each frame and checked
against a^2 + b^2 and c^2 before rendering."""
import math
from common import *

DURATION = 30.0
A, B = 3.0, 4.0
C = math.hypot(A, B)
L = A + B
S = 88.0                                   # px per unit
X0, Y0 = (W - L * S - 450) / 2, 140.0      # leave room for the readout on the right

# A triangle is placed by its right-angle corner R, the end of leg a (Pa) and the end of leg b (Pb).
ARR1 = [((0, 0), (A, 0), (0, B)),          # around a tilted square of side c
        ((L, 0), (L, A), (A, 0)),
        ((L, L), (B, L), (L, A)),
        ((0, L), (0, B), (B, L))]
ARR2 = [((0, A), (A, A), (0, L)),           # two a-by-b rectangles, leaving a^2 and b^2;
        ((L, 0), (L, A), (A, 0)),           # every triangle only slides, none turns or flips
        ((A, L), (0, L), (A, A)),
        ((A, A), (A, 0), (L, A))]

def pose(tri):
    (rx, ry), (ax, ay), (bx, by) = tri
    ang = math.atan2(ay - ry, ax - rx)
    turn = 1 if (ax - rx) * (by - ry) - (ay - ry) * (bx - rx) > 0 else -1
    return rx, ry, ang, turn

def tri_points(rx, ry, ang, turn):
    pa = (rx + A * math.cos(ang), ry + A * math.sin(ang))
    pb = (rx + B * math.cos(ang + turn * math.pi / 2), ry + B * math.sin(ang + turn * math.pi / 2))
    return [(rx, ry), pa, pb]

def lerp_pose(p, q, u):
    d = (q[2] - p[2] + math.pi) % (2 * math.pi) - math.pi     # shortest turn
    return (lerp(p[0], q[0], u), lerp(p[1], q[1], u), p[2] + d * u, p[3])

# Timeline (seconds)
T_FLY = (4.5, 7.5)                  # copies 2-4 fly in
MOVES = {3: (13.6, 15.3), 0: (15.7, 17.4), 2: (17.8, 19.5)}   # one at a time; triangle 1 stays put
OFFSCREEN = [None, (L + 6, -3, 1.2), (L + 7, L + 2, 2.6), (-6, L + 3, -2.0)]

def triangle_pose(i, t):
    p1, p2 = pose(ARR1[i]), pose(ARR2[i])
    if i > 0 and t < T_FLY[1]:
        start = (OFFSCREEN[i][0], OFFSCREEN[i][1], OFFSCREEN[i][2], p1[3])
        u = ease((t - T_FLY[0] - 0.5 * (i - 1)) / 1.6)
        return lerp_pose(start, p1, u)
    if i not in MOVES: return p1
    a, b = MOVES[i]
    return lerp_pose(p1, p2, ease((t - a) / (b - a)))

def area(poly):
    return abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]))) / 2

_g = (np.arange(140) + 0.5) * (L / 140)
GX, GY = np.meshgrid(_g, _g)

def covered(t):
    """Which grid points inside the big square are under a triangle, from the triangles as drawn."""
    hit = np.zeros(GX.shape, bool)
    for i in range(4):
        (x0, y0), (x1, y1), (x2, y2) = tri_points(*triangle_pose(i, t))
        d0 = (x1 - x0) * (GY - y0) - (y1 - y0) * (GX - x0)
        d1 = (x2 - x1) * (GY - y1) - (y2 - y1) * (GX - x1)
        d2 = (x0 - x2) * (GY - y2) - (y0 - y2) * (GX - x2)
        hit |= ((d0 >= 0) & (d1 >= 0) & (d2 >= 0)) | ((d0 <= 0) & (d1 <= 0) & (d2 <= 0))
    return hit

def leftover_area(t):
    return float((~covered(t)).sum()) * (L / 140) ** 2

def checks():
    for arr in (ARR1, ARR2):
        for tri in arr:   # each placement really is an a-b-c right triangle
            pts = tri_points(*pose(tri))
            assert all(abs(p[0] - q[0]) < 1e-9 and abs(p[1] - q[1]) < 1e-9 for p, q in zip(pts, tri)), tri
    for i in range(4):
        assert pose(ARR1[i])[3] == pose(ARR2[i])[3], f"triangle {i} would need a flip"
        assert abs(pose(ARR1[i])[2] - pose(ARR2[i])[2]) < 1e-9, f"triangle {i} would need to turn"
    # Before: what's uncovered is exactly the tilted square of side c.
    corners = [(A, 0), (L, A), (B, L), (0, B)]
    inside_c = np.ones(GX.shape, bool)
    for (x0, y0), (x1, y1) in zip(corners, corners[1:] + corners[:1]):
        inside_c &= (x1 - x0) * (GY - y0) - (y1 - y0) * (GX - x0) > 0
    assert (~covered(10) == inside_c).mean() > 0.995, "first arrangement leaves something other than c^2"
    # After: what's uncovered is exactly the a^2 square plus the b^2 square, and nothing overlaps.
    sq = ((GX < A) & (GY < A)) | ((GX > A) & (GY > A))
    assert ((~covered(22)) == sq).all(), "second arrangement leaves something other than a^2 + b^2"
    assert abs(leftover_area(10) - C * C) < 0.3 and abs(leftover_area(22) - (A * A + B * B)) < 1e-9
    assert font(64).unicharToGlyph(ord("²")) != 0, "font lacks the superscript two"
    print(f"checks passed: leftover area {leftover_area(10):.3f} before and {leftover_area(22):.3f} after")

def P(x, y): return X0 + x * S, Y0 + y * S

def poly_path(pts):
    path = skia.Path(); path.moveTo(*P(*pts[0]))
    for p in pts[1:]: path.lineTo(*P(*p))
    path.close(); return path

TRI_COLORS = ["#4f8fdb", "#4f8fdb", "#4f8fdb", "#4f8fdb"]
CAPTIONS = [(0.0, 4.4, "A right triangle with sides a, b and c."),
            (4.4, 9.0, "Put four copies inside a square of side a + b."),
            (9.0, 13.4, "The space left over is one square: c²."),
            (13.4, 20.0, "Now slide three of them. None turns or flips."),
            (20.0, 25.0, "The space left over is now a² + b²."),
            (25.0, 30.0, "Same square, same triangles: a² + b² = c².")]

def draw(c, t):
    c.clear(color("#13161c"))
    fade_all = clamp((DURATION - t) / 0.6)            # gentle fade at the very end
    # Intro: one big triangle, labelled, which then shrinks into its slot.
    big = 1 - ease((t - 3.6) / 1.2)
    grid_a = ease((t - 3.8) / 0.8)
    # Big square and its leftover highlight
    if grid_a > 0:
        c.drawRect(skia.Rect.MakeXYWH(X0, Y0, L * S, L * S), paint("#1d2230", grid_a))
        hl1 = window(t, 9.6, 13.4, 0.4); hl2 = window(t, 20.2, 30.5, 0.4)
        if hl1 > 0:
            c.drawRect(skia.Rect.MakeXYWH(X0, Y0, L * S, L * S), paint("#e0a33a", 0.85 * hl1))
        if hl2 > 0:
            c.drawRect(skia.Rect.MakeXYWH(X0, Y0, A * S, A * S), paint("#5cb87a", 0.85 * hl2))
            c.drawRect(skia.Rect.MakeXYWH(X0 + A * S, Y0 + A * S, B * S, B * S), paint("#c75b8f", 0.85 * hl2))
        c.drawRect(skia.Rect.MakeXYWH(X0, Y0, L * S, L * S), paint("#c9d1e0", grid_a, stroke=3))
    for i in range(4):
        if i > 0 and t < T_FLY[0] + 0.5 * (i - 1): continue
        pts = tri_points(*triangle_pose(i, t))
        if i == 0 and big > 0:   # intro: draw triangle 0 bigger and centred, easing into place
            k = lerp(1, 1.6, big)
            cx, cy = (lerp(X0 + 1.2 * S, W / 2 - 1.4 * S, big), lerp(Y0 + 1.5 * S, Y0 + 2.3 * S, big))
            pts = [((x - 1.0) * k + (cx - X0) / S, (y - 1.33) * k + (cy - Y0) / S) for x, y in pts]
        path = poly_path(pts)
        c.drawPath(path, paint(TRI_COLORS[i], 0.95))
        c.drawPath(path, paint("#0d1117", 1, stroke=4))
    # Side labels on the intro triangle
    la = window(t, 0.4, 4.0, 0.4)
    if la > 0:
        pts = tri_points(*triangle_pose(0, t)); k = 1.6
        cx, cy = W / 2 - 1.4 * S, Y0 + 2.3 * S
        q = [((x - 1.0) * k * S + cx, (y - 1.33) * k * S + cy) for x, y in pts]
        (rx, ry), (ax, ay), (bx, by) = q
        text(c, "a", (rx + ax) / 2, ry - 22, 56, "#ffffff", la, True)
        text(c, "b", rx - 40, (ry + by) / 2 + 18, 56, "#ffffff", la, True)
        text(c, "c", (ax + bx) / 2 + 40, (ay + by) / 2 + 30, 56, "#ffffff", la, True)
    # Labels on the leftover squares
    hl1 = window(t, 9.8, 13.4, 0.4)
    if hl1 > 0: text(c, "c²", X0 + L * S / 2, Y0 + L * S / 2 + 30, 84, "#13161c", hl1, True)
    hl2 = window(t, 20.4, 30.5, 0.4)
    if hl2 > 0:
        text(c, "a²", X0 + A * S / 2, Y0 + A * S / 2 + 26, 72, "#13161c", hl2, True)
        text(c, "b²", X0 + A * S + B * S / 2, Y0 + A * S + B * S / 2 + 30, 84, "#13161c", hl2, True)
    # Live readout: leftover area computed from the polygons on screen (a = 3, b = 4 units)
    ro = window(t, 9.6, 30.5, 0.4)
    if ro > 0:
        x = X0 + L * S + 70
        text(c, "leftover area", x, Y0 + 60, 40, "#9aa4b8", ro, align="left")
        text(c, f"{leftover_area(t):.0f} squares", x, Y0 + 125, 60, "#ffffff", ro, True, align="left")
        text(c, "with a = 3, b = 4", x, Y0 + 185, 36, "#9aa4b8", ro, align="left")
        eq = window(t, 25.3, 30.5, 0.4)
        if eq > 0: text(c, "9 + 16 = 25", x, Y0 + 290, 56, "#e0a33a", eq, True, align="left")
    for a, b, s in CAPTIONS:
        if a <= t < b: caption(c, s, ease(window(t, a, b, 0.3)))
    if fade_all < 1:
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, H), paint("#000000", 1 - fade_all))

def soundtrack(path):
    n = int(DURATION * SR); music = np.zeros(n); fx = np.zeros(n)
    # 90 bpm: a bar is 2.667 s. Chords C, Am, F, G repeating; plucks on chord tones.
    bar = 4 * 60 / 90
    chords = [[261.63, 329.63, 392.0], [220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 246.94, 293.66]]
    for k in range(int(DURATION / bar) + 1):
        ch = chords[k % 4]
        for j, f in enumerate(ch):
            place(music, 0.05 * tone(f / 2, bar, "pad", seed=k * 7 + j), k * bar)
    rng = np.random.default_rng(3)
    for i in range(1, 4):                                    # arrivals
        place(fx, 0.5 * tone([392, 440, 523.25][i - 1], 0.6, "pluck", seed=i), T_FLY[0] + 0.5 * (i - 1) + 1.6)
    for i, (a, b) in enumerate(MOVES.values()):
        place(fx, 0.25 * tone(0, b - a, "whoosh", seed=10 + i), a)
        place(fx, 0.5 * tone([523.25, 587.33, 659.25, 783.99][i], 0.7, "pluck", seed=20 + i), b)
    for a, _, _ in CAPTIONS[1:]: place(fx, tone(1600, 0.05, "tick"), a)
    for j, f in enumerate([261.63, 329.63, 392.0, 523.25]):   # resolving chord on the equation
        place(fx, 0.35 * tone(f, 2.5, "pluck", seed=40 + j), 25.3 + 0.08 * j)
    write_wav(path, music, fx)
