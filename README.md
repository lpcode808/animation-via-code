# Animation via code

Short explainer videos made by asking an AI coding agent to *write code that draws every frame*, instead of asking an image or video model to generate pixels.

This repo collects what was learned making a few dozen of these pieces (mostly 15 seconds to 3 minutes: science explainers, music lessons, product walkthroughs, talk translations, trailers). It is a set of notes, prompts, a tiny template and three small demos, not a framework.

> Lessons are marked **confirmed** (held up across many pieces), **tentative** (seen once or twice) or **contested** (sources disagree). See [where the notes disagree](guide/appendix.md#where-the-notes-disagree).

## Why code instead of a video model

A video model *grows* a clip: fast, beautiful, and hard to correct. Code *builds* one: every shape, number and caption is exact, editable and repeatable.

That matters for teaching. If a caption says "3 + 4 = 7", the diagram can be checked against it. If a reviewer says "the arrow points the wrong way", you change one line and re-render, and every other frame stays the same.

The cost is that you (or the agent) have to describe things precisely, and rendering takes minutes, not seconds.

## How it works, in one picture

```
prompt ──► agent writes scene code ──► renderAt(t) draws one frame
                                            │
             headless browser captures every frame (30 or 60 fps)
                                            │
            numpy writes the music and sound effects as raw samples
                                            │
                 ffmpeg joins frames + audio into an MP4
                                            │
       agent reviews contact sheets, scans for pops, fixes, re-renders
```

The diagram shows the most common route, not the only one. Pieces here also used SVG rasterizers, skia-python with no browser (that's how the [demos](demos/) were made), Manim, Remotion and headless Blender. Pick for the subject; see [Pick a renderer](guide/2-renderer.md).

The key idea: **each frame is a pure function of time.** `renderAt(t)` must draw the same picture for the same `t` no matter what was drawn before. That lets you render in parallel, re-render one second, and trust that what you previewed is what you ship.

## Start here

1. **Try it with a prompt.** Paste the [prompt card](prompts/01-prompt-card.md) into a coding agent that can run a browser and ffmpeg, filling in your topic. Expect 10 to 20 minutes for a 20 to 30 second clip.
2. **Watch and read the demos.** [`demos/`](demos/) has three short videos with their full source: a bouncing ball, a Pythagorean proof whose on-screen area is computed and checked, and a water cycle that loops with no seam.
3. **Run the template.** [`template/`](template/) is a simpler 6-second browser version of the bouncing ball: one HTML scene, a render script, a synth soundtrack and a mux step, in about 200 lines. Its audio, mux and contact-sheet steps and the scene's logic have been tested, but the browser render itself hasn't been run yet, so expect to fix small things.
4. **Read the guide before your second video.** [The guide](guide/) is filed by stage: plan, pick a renderer, build the scene on one clock, sound, render, review, legibility and companion pages. Each stage has its lessons and then the bugs that cost time there.
5. **Steal a prompt.** [prompts/](prompts/) has short demo prompts, a review-pass prompt, a long one-shot "single HTML film" prompt, and a brief for turning a video of yourself talking into a motion-graphics edit.

## Running the template

Needs Node 18+, Python 3 with numpy, and ffmpeg. Not yet run end to end in a browser; if a step fails, the [demos](demos/) are the fully tested version of the same idea.

```bash
cd template
npm install            # installs Playwright
npx playwright install chromium
node render.mjs        # writes frames/ (180 JPEGs)
python3 audio.py       # writes audio.wav
bash mux.sh            # writes out.mp4
```

## A caution on using these notes

Don't paste the whole guide into an agent's standing instructions. When that was tried, every new video converged on the same pipeline and look. Give the agent the short prompt, and reach for the lessons when something breaks or you want to push past the default.

## What's in here

| File | What it is |
|---|---|
| [guide/](guide/) | Lessons and pitfalls, one file per stage, with how sure we are of each |
| [demos/](demos/) | Three short rendered videos and the Python that draws them |
| [template/](template/) | Minimal browser pipeline |
| [prompts/](prompts/) | Prompts that worked, ready to copy |
| [EXAMPLES.md](EXAMPLES.md) | The pieces these lessons came from, by renderer, with the lesson each added |

## Credits

- The beat order used for explainers (analogy, diagram, example, plain English, technical) is adapted from BetterExplained's ADEPT method.
- Some hand-drawn-style pieces used a public third-party starter kit, ClaudeAnimationBase, built on [p5.brush](https://github.com/acamposuribe/p5.brush) (MIT). Credit and license for both belong to their authors; nothing from either is included here.
- Interactive explainer pages were influenced by Bret Victor's *Explorable Explanations*.

## License

Code (the `demos/` and `template/` folders, and code blocks in the prompts) is under the [MIT License](LICENSE). Text and the demo videos are under [CC BY 4.0](LICENSE-docs.md): reuse them with credit.
