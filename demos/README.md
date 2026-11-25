# Demos

Three short videos, each drawn frame by frame in Python with [skia-python](https://github.com/kyamagu/skia-python), with no browser. Each file is one scene: a `DURATION`, a `draw(canvas, t)` that is a pure function of time, a `checks()` that must pass before anything renders, and a `soundtrack()` written as numpy samples.

| Demo | Length | What it shows | What its check proves |
|---|---|---|---|
| [bouncing_ball.py](bouncing_ball.py) · [video](bouncing_ball.mp4) | 8 s | Physics computed from `t`; sound placed from the same physics | The first landing falls inside the "speeds up" caption, so words and picture agree |
| [pythagorean_proof.py](pythagorean_proof.py) · [video](pythagorean_proof.mp4) | 30 s | Four triangles rearranged inside one square; a live area readout | The uncovered area, sampled from the triangles as drawn, is the c² square before and exactly the a² and b² squares after; no triangle turns or flips |
| [water_cycle.py](water_cycle.py) · [video](water_cycle.mp4) | 20 s loop | Evaporation, condensation, precipitation, collection | The frame at the end matches the first frame, so it loops with no jump |

## Run them

Needs Python 3 with `numpy` and `skia-python`, and ffmpeg. On Ubuntu, skia also needs the EGL library even for CPU rendering.

```bash
git clone https://github.com/lpcode808/animation-via-code.git && cd animation-via-code
sudo apt-get install -y libegl1 ffmpeg fonts-dejavu-core   # skia needs EGL; the demos draw in DejaVu Sans
python3 -m venv .venv && . .venv/bin/activate              # newer Ubuntu and Debian refuse a plain pip install
pip install numpy skia-python
cd demos
python3 build.py bouncing_ball        # or pythagorean_proof, water_cycle
```

`build.py` runs the checks, renders the frames on four workers (resumable: frames already on disk are skipped), writes the soundtrack, joins them into `<name>.mp4` with loudness normalized and peaks limited, prints the true peak measured in the final file, and makes `<name>-sheet.jpg`, a 4×3 contact sheet taken from the final MP4.

Building writes over the `<name>.mp4` and `<name>-sheet.jpg` that ship in this folder.

Frames are cached in `work/<name>`, so after you change a scene's `draw()`, delete that folder or the old frames are reused.

To look at one moment before rendering everything, save a full-size still (here, 4.5 s into the water cycle):

```bash
python3 -c "import common; common.still('water_cycle', 4.5, 'still.png')"
```

The demos draw captions at 64 px; the [legibility stage](../guide/7-craft.md) suggests about 74 px for new pieces.

On a small cloud container each rendered at roughly 30 to 50 frames per second per worker; the 30-second proof took about six seconds. The contact sheets sample the video evenly, so a tile can catch a caption mid-fade; for review, pick the moments when each beat has settled.

## What reviewing them caught

Each first render was looked at as a contact sheet before calling it done. The fixes, as a sample of what the [review stage](../guide/6-review.md) catches:

- **Bouncing ball:** the caption panel covered the ball once it came to rest, and "It speeds up as it falls" appeared after the ball had already bounced. The floor moved up, the beats were retimed to the physics, and a check now pins them together.
- **Pythagorean proof:** the first draft placed two triangles wrong in the second arrangement (one with its legs swapped, one overlapping the a² square). The geometry checks failed before any frame rendered.
- **Water cycle:** three fade windows didn't wrap round the loop's end, so the last frame differed from the first; the seam check failed until they did. The first caption was also too wide for the frame, and rain fell through the mountain.

## Files

- `common.py`: shared helpers (frame size, colours, text and caption drawing, easing, the parallel resumable renderer, a small synth, the mux and the contact sheet).
- `build.py`: runs one demo end to end.
- `*-sheet.jpg`: the contact sheet each demo was reviewed from.
