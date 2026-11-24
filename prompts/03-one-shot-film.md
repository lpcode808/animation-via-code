# One-shot film prompt (single HTML file)

A long prompt for a 60–120 second film that lives in **one self-contained HTML file**: picture, music and recording mode together. Use it when you want something you can open in a browser, scrub, and also record to MP4. This is a skeleton of a prompt that produced a 92-second film; the specifics have been replaced with brackets.

```
Make a [90] second animated film as ONE self-contained HTML file:
inline SVG and/or canvas, CSS, vanilla JavaScript. No external files,
no CDNs, no libraries.

STORY
[Three to six sentences: who or what it's about, the turn, the ending.]

ARCHITECTURE (non-negotiable)
- One master clock. Everything is drawn by draw(t), a pure function of
  time in seconds. No setInterval, no state carried between frames.
- Put the plan in tables at the top of the script, so it can be edited
  without reading the drawing code:
    SHOTS   = [{start, end, name, ...}]      // what's on screen
    SCORE   = [{bar, chord, melody, ...}]    // the music
    CAPTIONS = [{start, end, text}]          // on-screen words
    KEYS    = [{t, what}]                    // sound effect moments
- Music and effects are synthesized with the Web Audio API and
  pre-rendered once with OfflineAudioContext, then played in sync
  with the clock.
- A RECORD_MODE flag: when ?record=1 is in the URL, hide controls,
  expose window.renderAt(t), and don't autoplay, so a headless
  browser can step through frames.
- Controls in normal mode: play/pause, a scrubber, and the current time.

LEGIBILITY FLOOR
- Captions at least [74] px tall at 1920×1080, on a panel if the
  background is busy. Nothing important in the bottom 15%.
- Hold each caption at least 1 second per 3 words.

CREATIVE LATITUDE
You choose palette, character design, camera moves and transitions.
Surprise me, but every shot must serve the story above.

SOUND
Pick from: soft kick, rim click, pluck, pad, whoosh, chime, page turn,
paper slide, typing. Effects duck the music about 6 dB.

WHEN DONE
Render a contact sheet of 12 stills and list every change you'd
still make, most important first.
```

## Notes

- Putting the plan in tables (`SHOTS`, `SCORE`, `CAPTIONS`, `KEYS`) made revisions much faster: "move the chorus one bar later" is a one-line change.
- "Creative latitude" plus a short list of non-negotiables worked better than specifying every shot.
- Asking for a change list at the end gave a ready-made second prompt.
