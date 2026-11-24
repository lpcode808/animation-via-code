# Review pass prompt

Run this in a **fresh** agent session (no memory of making the video). Give it the contact sheet images and the caption list with timings.

```
You are reviewing a short explainer video. You have never seen it before.
Attached: a contact sheet of stills in time order, and every caption with
its start and end time.

Review it twice:
1. As someone in the audience ([who it's for]) seeing it once at normal
   speed. Where would you get lost, misread something, or stop watching?
2. As a teacher of [subject]. What is wrong, misleading, or
   oversimplified without saying so?

Also check:
- Read each caption alone. Is it true on its own?
- Does every number on screen match what's drawn?
- Is any caption on screen too briefly to read (under 1 s per 3 words)?
- Does any viewpoint change (flat to 3D, zoom, cut) happen without
  showing where we are?

Return only the top 5 problems, most important first. For each: the
timestamp, what's wrong, and the smallest fix.
```

## Why top 5

Asking for everything produced long lists of taste notes. Asking for five forced the real problems to the top. A typical pass found 3 to 20 issues; the top five were nearly always worth fixing.

## When to disagree with the reviewer

If a suggestion would make the video less true to the real thing (a real object's shape, a real data value), keep the true version and note why.
