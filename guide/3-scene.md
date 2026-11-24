# 3. Build the scene on one clock

Write one timeline, and draw every frame from it. Picture, captions, narration and sound all read the same clock, so changing one beat moves everything with it.

Lessons are tagged **confirmed** (held up across many pieces), **tentative** (seen once or twice) or **contested** (sources disagree; see [where the notes disagree](appendix.md#where-the-notes-disagree)).

## Lessons

**One clock for everything.** (confirmed) Write a single timeline file (a table of beats with start and end times) and drive the picture, captions and sound from it. When narration exists, generate it first, measure each line, and build the timeline from its timings. A later rescore reuses the same file.

**Frames are a pure function of time.** (confirmed) Write `renderAt(t)` so it draws the same frame for the same `t`, whatever came before. No `requestAnimationFrame` state, no accumulating positions, no unseeded `Math.random()` (use a seeded generator such as mulberry32 or a hash of the frame index). If something truly needs history (a particle trail), replay it from the start of its scene inside `renderAt`.

**Narrate what's on screen.** (tentative) When there is a voice, have it say the on-screen text word for word, space new terms about half a second apart, and define each term before using it.

**Narration is optional and expensive in time.** (tentative) A local text-to-speech model plus a speech-to-text check (to confirm the words came out right) worked, but it pushed pieces well past a 15-minute box. Captions-only pieces were consistently faster.

**Add time at the front without retiming everything.** (tentative) Keep the old timeline as "old time" (`u = t - shift`), draw the new intro in new time, and shift the sound cue list by the same amount. Every later caption and check stays untouched.

**Revisions without full re-renders.** (tentative) When an edit only changes a few seconds, remap the clock so unchanged frames are reused from the last render. Keep old versions in an `archive/` folder rather than overwriting.

**For a loop, compare the last frame with the first.** (tentative) Make everything a function of the loop's phase, make anything that repeats inside the loop repeat a whole number of times, and let any soft on/off window wrap past the end. Then render frame `T` and frame `0` and assert they match. The [water-cycle demo](../demos/water_cycle.py) does this; its first try failed the check on three windows that didn't wrap.

**Real footage: time comes from the words.** (tentative) When you edit a recording of someone talking, transcribe it with word timings (`[word, start, end]`) and hang every caption, graphic and sound cue on those times. The agent never hears the voice; it works from the transcript. See the [edit-your-own-video prompt](../prompts/06-edit-your-own-video.md).

**Real footage: use every source frame once, in order.** (tentative) Lay the footage out with keyframes (position, size, corner radius of the video card over time) and assert that each source frame appears exactly once and in order, so nothing is cut or doubled by accident.

## Pitfalls

Bugs that each cost real time, with the fix.

**Text "pops" in at full opacity for one frame.**
A helper set `ctx.globalAlpha = a` instead of multiplying the current value. Inside a scene that was already fading, the helper reset the fade. Fix: `ctx.globalAlpha *= a` inside `save()`/`restore()`.

**A fade-in plays twice or skips.**
The text animation used the global clock while the scene used a shifted local clock. Fix: pass every helper the scene's local `u` (0 to 1), never the global `t`.

**Same seed, different frame.**
`Math.random()` in a draw function makes every render different and breaks parallel rendering. Use a seeded generator keyed on scene and element index.

**The camera is on the wrong side.**
A flipped yaw sign put the "right" wall on the left. Check orientation in the first still.

---

[← 2. Pick a renderer](2-renderer.md) · [4. Sound and mix →](4-sound.md)
