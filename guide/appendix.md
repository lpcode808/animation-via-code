# Appendix

Notes that cut across the stages.

## Working with the agent

**Version in place, keep the old cuts.** (confirmed) Iterate as v2, v3 in one conversation, and keep earlier versions as separate files when an experiment might not land. Ask the agent to flag any change you didn't request.

**Don't paste this guide into standing instructions.** (confirmed) When a best-practices file went into a project's standing instructions, every new video converged on the same pipeline and look. Give the agent the short prompt, and reach for the guide when something breaks or you want to push past the default.

## Cost and time (data points, not promises)

| Piece | Wall time | Rough cost | Note |
|---|---|---|---|
| 2D explainer of a product | ~1.5 h | ~$20 | Canvas 2D |
| 3D remake of the same product | ~20 h | ~$140 | Software three.js, many review rounds |
| 98 s making-of film | ~3 h | ~$34 | Real data, many beats |
| Short game explainer, second version | — | ~$14 | |
| Fastest 85 s piece | ~21 min | — | Captions only |
| 45–52 s captions-only pieces | 5–11 min | — | Captions only |

Takeaway: in the one direct comparison, 2D cost about a seventh as much as 3D for a similar explainer. Captions-only pieces were consistently the fastest.

## Where the notes disagree

- **Caption hold time.** One set of notes uses about 3 words per second; another uses 1 second plus 0.3 s per word (slower for short captions). Both came from review feedback.
- **Workers and speed.** Notes say two workers halves wall time; others used three or four. three.js measured about 1 s/frame in one piece and 1.5 to 3 s/frame in another.
- **The 15-minute box.** One set of notes plans for 15 minutes from prompt to MP4. Short captions-only clips made it; anything with narration, 3D, or more than ~60 seconds did not. Treat 15 minutes as a target for short captions-only clips.
- **Canvas speed.** Different pieces report 6 or 19 frames per second per worker. Scene complexity (blur, many paths, text) explains most of it; measure your own.
- **Text on screen.** One starter kit recommends no on-screen text at all, letting the drawing carry meaning. The explainer pieces relied on captions. Both produced good work; it depends whether the piece is mood or instruction.
- **ADEPT order.** It helped most explainers but felt forced for stories and personality pieces. Use it when the job is to teach one idea.
- **Reviewer suggestions vs fidelity.** A fresh reviewer sometimes asked for changes that would make the video less true to the real object. Fidelity won; record why when you reject a suggestion.
- **3D vs 2D.** The 3D remake looked better to some viewers but cost about seven times more and needed many more fixes. No consensus on when it's worth it.
