# 8. Companion pages (optional)

The same drawing code can power an interactive page next to the video.

Lessons are tagged **confirmed** (held up across many pieces), **tentative** (seen once or twice) or **contested** (sources disagree; see [where the notes disagree](appendix.md#where-the-notes-disagree)).

## Lessons

**Reuse the video's code.** (confirmed) The same `renderAt(t)` that renders the MP4 can power a web page with a scrubber, so readers can pause on any moment. Expose options through a small global (for example `window.REEL_OPTS`) so the page and the renderer share one file.

**Make numbers draggable, with buttons.** (tentative) Inline numbers readers can change ("what if gravity were *12*?") worked well with visible −/+ buttons; a dashed underline alone wasn't discoverable.

## Pitfalls

Bugs that each cost real time, with the fix.

**`history.replaceState` throws.**
Some sandboxed page hosts block it. Wrap in `try/catch`.

**Audio won't seek in a hosted page.**
Fetch the audio file and play it from a blob URL; some hosts don't support range requests. Some hosts also refuse `.m4a`; use `.mp3` or `.wav`.

**The test browser won't play your MP4.**
Stock Playwright Chromium doesn't decode H.264. Point tests that play video at a full Chrome build.

---

[← 7. Make it legible](7-craft.md) · [Appendix →](appendix.md)
