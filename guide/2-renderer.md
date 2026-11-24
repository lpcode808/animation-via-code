# 2. Pick a renderer

Choose what draws the frames for this subject, then get it working once. The rule that matters in every renderer is the same: each frame is a pure function of time (stage 3).

Lessons are tagged **confirmed** (held up across many pieces), **tentative** (seen once or twice) or **contested** (sources disagree; see [where the notes disagree](appendix.md#where-the-notes-disagree)).

## Lessons

**There is more than one good renderer.** (confirmed) Pieces in this collection used, among others: Canvas 2D in a headless browser; SVG strings rasterized with resvg; skia-python; a numpy "shader" for pixel effects; Manim for math scenes (rendered as parallel scenes); Remotion; DOM and SVG animated with a paused animation library and stepped through DevTools; three.js in software WebGL; and real Blender (installed from pip, Cycles on CPU) for a 12-second section at 720p and low samples. Pick for the subject, not out of habit. Several of these need no browser at all.

**Canvas 2D is the default renderer.** (confirmed) It's fast, predictable and the agent knows it well. Roughly 6 to 19 frames per second per worker depending on the scene (see contested).

**Python is fine too.** (tentative) The [demos](../demos/) here use skia-python with no browser at all, at roughly 30 to 50 frames per second per worker for simple 1080p scenes. The language matters less than the pure-function-of-time rule.

**Real 3D is expensive without a GPU.** (confirmed) three.js in software rendering ran about one second per frame; one 3D piece (a 3D printer) took over 100 minutes to render. A hand-rolled 2.5D look (orthographic projection, simple prisms, back-face culling, painter's sort, flat Lambert shading) looked close and rendered in seconds.

**Software WebGL needs flags.** (confirmed) With no GPU, launch Chromium with `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader` for three.js or WebGL scenes.

**Hand-drawn brush looks are slow.** (confirmed) Brush libraries without a GPU crawl. What helped: cache static "plates" (backgrounds drawn once), use cheaper fills for large areas, and drop pixel density to about two thirds. That got one kit to about 1.6 s per frame.

**Frame rate follows style.** (tentative) 12 fps drawn "on twos" and played at 24 reads as hand-drawn; 30 for motion graphics; 60 only when fine timing (fingers on keys) matters.

**A framework may save the setup time.** (tentative) Left alone, the agent rebuilds the seek-and-screenshot harness from scratch each time, which costs 20 to 40 minutes. Remotion, Motion Canvas and HyperFrames formalize the same shape. Worth one trial if you make many videos; not tried yet in the pieces here.

**Pages you can't seek can still be recorded.** (tentative) For timer-driven pages like slide decks, Chrome's DevTools screencast (`Page.startScreencast`) works where Playwright's video recording needs its own ffmpeg. Keep each frame's timestamp and write an ffmpeg concat list with per-frame durations.

## Pitfalls

Bugs that each cost real time, with the fix.

**skia-python fails to import with a missing `libEGL.so.1`.**
It needs the EGL library even for CPU-only rendering. Install it (`apt-get install libegl1` on Ubuntu).

**CDN fonts don't load in the sandbox.**
Many agent containers block font CDNs. Install fonts from npm (woff2 files), and inline them as base64 `@font-face` in the HTML.

**Missing glyphs show as boxes.**
Check that the font actually contains every character you use. Arrows (→), not-equal (≠) and subscripts (₂) were missing more than once; write `CO2` or draw the arrow.

**Code font turns `->` or `===` into one glyph.**
Programming fonts with ligatures change what's shown. In CSS, `font-variant-ligatures: none`. On canvas the notes disagree: one piece broke ligatures with a tiny `letterSpacing` (`'0.01px'`); another found a zero-width non-joiner didn't work and drew code one character at a time on a fixed advance, which always works. Some pixel fonts also ligate `fi`/`fl`.

**An animated SVG group jumps to the top-left corner.**
A CSS animation on `transform` overrides the element's SVG `transform` attribute, so the group loses its position. Fix: wrap it: the outer `<g>` keeps the SVG `transform="translate(…)"`, the inner `<g>` gets the CSS animation. Also, CSS transitions can't animate to `auto`; animate a number.

**A shape grows fake notches where parts overlap.**
Drawing several shapes (a glyph and a bar) as one canvas path makes opposite windings cancel under the default nonzero fill. Fill each part separately, or compute a real union.

**A `</script>` inside a template literal ends the page's script.**
Write `<\/script>`.

**A model's weights won't download.**
Sandboxes often block model hubs. Look for the same weights packaged on npm or PyPI (for example, `@imgly/background-removal-node` bundles a background-removal model).

---

[← 1. Plan the piece](1-plan.md) · [3. Build the scene on one clock →](3-scene.md)
