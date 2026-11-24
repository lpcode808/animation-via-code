# Template: a 6-second bouncing ball

The whole browser pipeline in five small files. The scene's logic has been checked in Node with a stand-in canvas, but the full browser render hasn't been run end to end yet; the [demos](../demos/) are the fully rendered, browserless version of the same idea.

| File | Job |
|---|---|
| `scene.html` | Draws any frame with `renderAt(t)`; also lists sound cues |
| `render.mjs` | Opens the scene in headless Chromium, screenshots every frame, writes `cues.json` |
| `audio.py` | Writes `audio.wav`: a pad on a 120 bpm bar grid plus bounce sounds from the cues |
| `mux.sh` | Joins frames and audio into `out.mp4`, normalizes loudness, limits peaks, prints the true peak |
| `contact.sh` | Makes `contact.jpg`, 12 stills in a 4×3 grid, for review |

```bash
npm install && npx playwright install chromium
node render.mjs 30 3     # fps, workers
python3 audio.py
bash mux.sh 30
bash contact.sh
```

Open `scene.html` in a normal browser and run `renderAt(2.5)` in the console to see any moment.

Things to notice in the code:

- The page sets `window.__ready` after fonts load, and the renderer waits for it.
- Frames are read straight from the canvas (`toDataURL`), and frames already on disk are skipped, so a crashed render resumes and a bad range can be deleted and redone.
- `ballY(t)` computes the ball's height from `t` directly. Nothing is accumulated between frames, so frames can render in any order on any worker.
- Captions fade using each beat's own start and end, and the caption helper multiplies `globalAlpha` instead of setting it.
- Bounce sounds are placed from the same physics that draws the ball, so they land on the right frame.
- The pad uses detuned voices with random (seeded) starting phases so it doesn't throb.
- `mux.sh` adds a limiter after loudness normalization; without it the encoded file peaked above the −2 dBFS target in testing.
