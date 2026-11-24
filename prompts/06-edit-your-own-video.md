# Edit your own talking video into a motion-graphics piece

Everything else in this repo draws from scratch. This brief starts from footage you recorded: a portrait phone video of you talking, turned into a 1920×1080 landscape edit with graphics, word-synced captions and a quiet soundtrack.

Give it to a coding agent that has a shell, with your video attached. A plain chat can't render video.

**The agent doesn't listen to your audio.** A speech-to-text model (Whisper) turns it into words with start and end times, and the agent animates to those. Fix names and misheard words in the blanks below, and listen to the result yourself.

## The ask (fill in the blanks)

```
Edit my portrait phone video into a 1920x1080 landscape video. Keep every
frame and every word; don't cut anything. Add motion graphics that support
what I'm saying: bold color, strong type, simple diagrams, and word-synced
captions. Move my portrait around the wide frame. Add lo-fi synthesized
background music and light sound effects, kept under my voice. It should be
legible, not distracting. Deliver the MP4 and the source.

- Names on screen and their spelling: ___
- Words that are hard to hear, and what I said: ___
- Anything to anonymize: ___
```

## Method that worked

One 2:15 talk took about 1.5 hours and about $18 of model use at API prices.

1. Extract frames and audio with ffmpeg. Transcribe with Whisper and keep word timings: `[word, start, end]`.
2. Write a web page with `renderAt(t)` that draws the whole 1920×1080 frame on a canvas from time alone: background, the footage frame for `t`, graphics, captions. Keep no state between frames.
3. Lay out the footage with keyframes: the portrait card's position, size and corner radius over time (big, left, right, picture-in-picture), with eased moves. Check that every source frame is used once, in order.
4. Optional: run a background-removal model (ISNet or rembg) only on the frames where text goes behind the speaker or they step out of the card. Switch into the cutout with a wipe so mask flicker doesn't show.
5. Give each sentence at most one graphic (diagram, chip, timeline, UI mock-up). Use one color per idea everywhere, and 2 or 3 fonts.
6. Captions: one sentence per page, at most 3 lines, at least 0.6 s per page, with the current word highlighted.
7. Review stills before the full render: render 10 to 12 timestamps into one contact sheet, fix, repeat. Then render every frame in headless Chromium (Playwright): seek, screenshot, 4 workers, resumable.
8. Make the audio from the same timeline in numpy/scipy: lo-fi chords, sub bass, soft drums and vinyl crackle, with sound effects at the graphic cues. High-pass and gently compress the voice, duck the music under words, normalize to about −16 LUFS, and limit true peaks to about −2 dBFS. Mux with ffmpeg.
9. Encode with libx264 (crf 20, yuv420p, +faststart). Check frames from the final MP4 and the loudness numbers, then listen yourself.

## Gotchas

- If the sandbox can't reach the model hub, look for the weights packaged on npm or PyPI (`@imgly/background-removal-node` bundles ISNet).
- Load fonts from local woff2 files (`@fontsource` on npm) and preload every weight before rendering, or the canvas silently falls back.
- Never `pkill -f` a pattern that also matches the shell running the command.

Related stages: [build the scene on one clock](../guide/3-scene.md), [sound and mix](../guide/4-sound.md), [make it legible](../guide/7-craft.md).
