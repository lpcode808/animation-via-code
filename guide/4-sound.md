# 4. Sound and mix

Write the music and effects as code too, place them from the picture's own events, and measure the mix in the file you deliver.

Lessons are tagged **confirmed** (held up across many pieces), **tentative** (seen once or twice) or **contested** (sources disagree; see [where the notes disagree](appendix.md#where-the-notes-disagree)).

## Lessons

**Synthesize what you can.** (confirmed) Most music and effects were written as raw samples with numpy: no sample libraries, no licensing questions. A few pieces instead rendered a MIDI score through FluidSynth with a General MIDI soundfont, which is quicker for orchestral or piano parts; check the soundfont's license. Additive synthesis for piano-like tones, Karplus-Strong for plucked strings, detuned stacks with random phases for pads and choirs (identical phases pulse).

**Let the picture tell the sound where to go.** (confirmed) Scenes call something like `cue(scene, u, "whoosh")` while rendering; the renderer writes those to `cues.json`; the audio script places each sound on its exact frame. This kept hits within a few milliseconds of the picture.

**Music on a bar grid.** (confirmed) Pick a tempo so bars land on round seconds (120 bpm: one bar is 2 s) and line scene changes up with bar lines. Melodies built from chord tones sound intentional even when simple.

**Give effects their own bus.** (confirmed) Duck the music about 6 dB under effects. A short 1 to 4 kHz "crack" layer makes small hits audible on phone speakers.

**Measure peaks after encoding.** (confirmed) AAC encoding raised true peaks by 4 to 5 dB in several pieces. Limit to about −2 dBFS true peak, then measure the muxed MP4, not the WAV.

**Seed every random choice, one stream per purpose.** (confirmed) Use a seeded generator (`mulberry32(hash(seed, n))`). One extra draw on an existing stream changes every note after it, so put new randomness on a new stream instead of adding draws to an old one.

**Pin levels in tests.** (tentative) If you keep a library of instruments, test each part's loudness against the whole mix (for example ±0.5 LU). When you change a sound on purpose, re-measure and move the pin in the same change. Never loosen a check just to pass.

**Silence can be a beat.** (tentative) Cutting the music for under a second where something is supposed to happen and doesn't (a timer that never rings) made the point better than any sound.

**Licensed music goes in last.** (confirmed) If you'll use a real track, have the agent leave the music bed silent and add it in your editor.

**The agent can't hear.** (confirmed) Every report should say whether a human has listened. Automated checks catch clicks, clipping, silence and level jumps, not ugliness. One piece of tooling rendered ~1,400 synthesized notes and checked level jumps, tuning, clicks, cut-offs and DC offset against reference recordings; it found real problems, but it still isn't listening.

**A real voice comes first.** (tentative) When the video has a recorded voice, high-pass it and compress it gently, duck the music under the words, and keep effects light.

## Pitfalls

Bugs that each cost real time, with the fix.

**A pad or choir throbs.**
Stacked voices started in phase. Randomize each voice's starting phase and detune slightly.

**Clicks at note ends.**
Every note needs a short fade-out (5 to 20 ms), even percussive ones.

---

[← 3. Build the scene on one clock](3-scene.md) · [5. Render at scale →](5-render.md)
