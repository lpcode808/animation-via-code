# 5. Render at scale

Turn the scene into thousands of frames and one MP4 without babysitting it.

Lessons are tagged **confirmed** (held up across many pieces), **tentative** (seen once or twice) or **contested** (sources disagree; see [where the notes disagree](appendix.md#where-the-notes-disagree)).

## Lessons

**Headless browser, many workers.** (confirmed) Load the scene in headless Chromium with Playwright, call `renderAt(t)` for each frame, and save it as JPEG (screenshot, or read the canvas directly with `toDataURL`). Three or four parallel workers is the sweet spot on a normal container. 1920×1080 at 30 fps is the default; 60 fps only for fast motion.

**Wait for a ready flag.** (confirmed) Have the page set something like `window.__ready = true` after fonts load and any pre-rendering finishes, and have the capture script wait for it. Otherwise the first frames render in fallback fonts.

**Write numbered frames so the run can resume.** (confirmed) `00000.jpg`, `00001.jpg`… A crashed render picks up where it stopped, and a bad range can be deleted and re-rendered: patch, don't restart.

**Run it detached.** (confirmed) Long renders die when the agent's shell is recycled. Start them with `setsid nohup … &` and poll the output folder.

**Encode for everywhere.** (confirmed) H.264, `yuv420p`, `+faststart`. Normalize loudness to about −15 or −16 LUFS integrated, and keep true peaks under about −2 dBFS.

**Local hardware changes the rules.** (tentative) Everything here was tuned in a cloud sandbox (about 2 cores, no GPU, a network allowlist). On a machine with a GPU, Blender and real WebGL become practical, you can run 8 to 16 workers, and most network workarounds disappear.

## Pitfalls

Bugs that each cost real time, with the fix.

**The first frames use the wrong font.**
The capture started before fonts loaded. Set a ready flag after `document.fonts.ready` and wait on it. Preload every weight you use; the canvas falls back silently for a weight that hasn't loaded.

**A long render dies when the session goes idle.**
Some agent sandboxes stop a session that looks idle. For multi-hour renders (Blender), keep a background job alive that waits on the render.

**`pkill render` killed the agent's own shell, or `pgrep` found itself.**
Match carefully: `pgrep -f '[r]ender.mjs'` (the bracket stops it matching its own command line), and never `pkill -f` a word that appears in your own command.

**ESM scripts can't find a globally installed package.**
`import` ignores `NODE_PATH`. Symlink `node_modules` into the folder you run from.

**A 20-second render came out 6 seconds long.**
The audio length was hard-coded and the mux used `-shortest`, so the video was cut to the audio with no error. Read the length from one place in picture, audio and mux, and assert the final file's length.

**Scripts lost their execute bit.**
Shared folders may drop permissions. Run with `bash script.sh` rather than `./script.sh`.

---

[← 4. Sound and mix](4-sound.md) · [6. Check it's right, then review →](6-review.md)
