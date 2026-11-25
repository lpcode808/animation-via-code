# 6. Check it's right, then review

Check the content first, then the frames, then ask someone who wasn't there.

Lessons are tagged **confirmed** (held up across many pieces), **tentative** (seen once or twice) or **contested** (sources disagree; see [where the notes disagree](appendix.md#where-the-notes-disagree)).

## Lessons

### Getting it right

A teaching video can look finished and still be wrong. In this collection, two science reels each held five or six factual errors that only surfaced when a review was asked for, and a made-up quote survived three versions of another piece.

**Model the process, not its picture.** (confirmed) If the subject is a machine or procedure, simulate what it actually does and let the animation show the result. One laser-cutting piece first drew overlapping letters as joined. A laser cuts every outline, so they'd fall apart; the fix was to model the cut and add the step that merges them.

**Make on-screen numbers live computations.** (confirmed) Compute counts, measurements and totals in the page, and assert them against a source the subject already has (a measurement, a dataset). When they disagree, that's a finding, not something to tune away. The [Pythagorean demo](../demos/pythagorean_proof.py) samples the uncovered area from the triangles as drawn and asserts it is c² before and a² + b² after; its first draft placed two triangles wrong, and the checks caught it before any frame rendered.

**When the subject is code, show the code that runs.** (tentative) Store it as a string, display that string, and run it to drive the picture and sound. What's on screen can't drift from what happens.

**Don't let a caption claim something you didn't compute.** (confirmed) "Where all three views agree, the object is" is only honest if the piece actually carves the object from the views. Otherwise change the caption.

**Check what a formula draws before captioning it.** (confirmed) Captions written from notes, not from the render, described patterns that didn't appear.

**Ask the agent to list its guesses.** (confirmed) "Which steps did you guess at?" points you straight at the likely mistakes. You know the subject; you're the one who catches them.

**Props leak answers.** (tentative) In classroom pieces, background props and labels gave away the decisions students were meant to make. Review incidental text against the lesson's rules, and use blanks where needed.

**Label reconstructions.** (confirmed) When a piece mixes real records (real titles, real data) with drawn stand-ins, say which parts are reconstructed.

**Beauty can hide a missing explanation.** (tentative) One piece was judged "too pretty, under-explained". Polish made it look finished while the key step was never shown. Check the source for the traps a careful reader would fall into.

**Hedge claims you can't check.** (tentative) Cultural and current-events claims get softer wording or a source on screen.

### Review and QA

**Read the video, don't watch it.** (confirmed) An agent can't watch video efficiently: about 20 minutes of footage costs tens of millions of tokens as frames, and around ten thousand as a word-level transcript. For edits of real footage, work from the transcript and pull a filmstrip only for hard spots. For code-drawn video the scene code and timeline are the text; render 15 to 20 full-size stills at the busiest moments and every scene boundary (more than the 12-still contact sheet below, because this pass is about catching mistakes, not getting an overview), check them as one sheet, fix, and only then render in full. Cap it at about three fix passes.

The single biggest quality lever was **a fresh reviewer.** (confirmed) After the first full render, start a new agent with no context, give it the video's contact sheets and caption list, and ask it to play two roles: someone seeing this for the first time, and a teacher of the subject. Ask for the top 5 problems only. It found real issues in every piece where it was tried; one first-time-reader pass on a 45-second piece listed 14 confusions.

**If you can't start a fresh reviewer, hand it over.** (tentative) An agent working alone can't review its own video as if it were new. It should give the user the [review prompt](../prompts/04-review-pass.md), the contact sheet and the caption list to run elsewhere, rather than call its own pass fresh.

Cheaper checks that each caught real bugs at least once (most held up across many pieces; caption timing is [contested](appendix.md#where-the-notes-disagree)):

- **Contact sheet:** 12 stills in a 4×3 grid, taken at moments when each beat has settled, not mid-transition.
- **Pop scan:** compare each frame to the next and flag big jumps; also flag single frames that differ from both neighbours (one-frame flashes).
- **Frozen clock check:** compare two frames one second apart in every beat. If they're identical where motion was expected, the clock isn't reaching that scene, even though stills look fine.
- **Caption timing list:** print each caption with its on-screen duration. Hold about 3 words per second, slower (about 2.5) for the key idea.
- **Read each caption alone** as a standalone claim. Is it true without the picture?
- **Check every number** on screen against what's drawn or what the synth actually plays.
- **Run the delivered folder once** from a clean copy; check the output file's timestamp is new.
- For companion web pages: check at phone width (390 px) and at 1280×720.
- **Sheet the final MP4 too.** Pull 6 to 10 frames from the encoded file and look again; this catches encode and mux problems (and text clipping) the pre-render sheet can't.
- **Size for the back row.** If labels vanish at contact-sheet scale, they'll vanish on a classroom projector. One piece went from 22 px to a 30 px minimum after this check.
- **A cold first-time viewer.** Once the cut is stable, give a fresh agent frames every 0.5 s with timestamps and ask it to retell the story, then list where it got confused. It caught jargon, skipped steps and unexplained terms that author reviews missed.
- **Review against the handout.** If the video goes with a worksheet, give the reviewer both. It found places where the video contradicted or gave away the worksheet.

## Pitfalls

Bugs that each cost real time, with the fix.

**A word count or quote is wrong.**
It was computed from a truncated copy of the source. Count only from the full text.

**"Nothing changed" but the file is new.**
Some shared or synced folders add a few kilobytes of provenance metadata to MP4 and JPEG files, so file hashes differ even when the picture didn't. Compare decoded streams instead: `ffmpeg -i a.mp4 -map 0:v -f streamhash -`.

**`console.assert` or `console.table` is missing.**
Some preview environments strip them. Wrap them, or write your own assert.

---

[← 5. Render at scale](5-render.md) · [7. Make it legible →](7-craft.md)
