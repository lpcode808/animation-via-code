# Starter-kit prompt

When you have a folder of helpers (a renderer, a timeline module, a character, a style guide), the prompt can be very short because the kit carries the rules.

```
Read GUIDE.md first. Then make a 15 second video of [character] doing
[one action], using the kit's timeline and render script. Show me a
contact sheet before rendering the full video.
```

## What a good kit includes

- **A guide** the agent reads first: the house style, timing rules, and the pure-function-of-time rule, with one worked example.
- **A timeline helper** so scenes are written as start/end/easing rather than raw math.
- **A render script** that already handles workers, frame naming and ffmpeg.
- **Cached backgrounds ("plates")** for slow drawing styles.
- **A storyboard template**: one line per beat with time, picture, caption and sound.

## Feel vs surface

One kit separated *feel* (timing, easing, how things settle, when to hold still) from *surface* (colours, line style, fonts). Agents copied surface easily; feel had to be written down with examples. If your videos look right but feel off, the guide is missing timing rules, not colours.
