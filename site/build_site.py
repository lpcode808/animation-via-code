"""Builds index.html for the GitHub Pages front page from the repo's own guide files.
Usage, from the repo root: python3 site/build_site.py .
Re-run it after editing guide/ or prompts/ so the page matches."""
import re, sys, json, html, glob, os

REPO = sys.argv[1]
GH = "https://github.com/lpcode808/animation-via-code/blob/main/"

def inline(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)           # drop links, keep text
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    return s

def first_sentence(s):
    m = re.match(r"(.+?[.!?])(\s|$)", s)
    return m.group(1) if m else s

stages = []
for path in sorted(glob.glob(f"{REPO}/guide/[1-8]-*.md")):
    txt = open(path).read()
    title = re.search(r"^# (.+)$", txt, re.M).group(1)
    num, name = title.split(". ", 1)
    intro = txt.split("\n\n")[1].strip()
    lessons_part, _, pitfalls_part = txt.partition("## Pitfalls")
    lessons = []
    for m in re.finditer(r"^\*\*(.+?)\*\* \((confirmed|tentative|contested)[^)]*\) (.+)$", lessons_part, re.M):
        lessons.append({"t": inline(m.group(1).rstrip(".")), "tag": m.group(2), "s": inline(first_sentence(m.group(3)))})
    m = re.search(r"\*\*a fresh reviewer\.\*\* \((confirmed)\) (.+)$", lessons_part, re.M)
    if m:
        lessons.insert(0, {"t": "A fresh reviewer is the biggest lever", "tag": "confirmed", "s": inline(first_sentence(m.group(2)))})
    pitfalls = [inline(p.rstrip(".")) for p in re.findall(r"^\*\*(.+?)\*\*\s*$", pitfalls_part, re.M)]
    stages.append({"n": num, "name": name, "intro": inline(intro), "file": GH + "guide/" + os.path.basename(path),
                   "lessons": lessons, "pitfalls": pitfalls})

BLURBS = {
 "01-prompt-card.md": "The short prompt on the left, with why each line is there and what to add on a second try.",
 "02-demo-prompts.md": "Five prompts for showing the method live, each picked to show something different.",
 "03-one-shot-film.md": "A long prompt for a 60 to 120 second film in one self-contained HTML file: picture, music and recording mode together.",
 "04-review-pass.md": "Run it in a fresh agent session with the contact sheets and caption list. The single biggest quality lever.",
 "05-starter-kit.md": "When a folder of helpers carries the rules, the prompt itself can be very short.",
 "06-edit-your-own-video.md": "Starts from footage instead: a portrait phone video of you talking, turned into a landscape edit with graphics and word-synced captions.",
}
prompts = []
for path in sorted(glob.glob(f"{REPO}/prompts/*.md")):
    txt = open(path).read()
    prompts.append({"title": inline(re.search(r"^# (.+)$", txt, re.M).group(1)),
                    "blurb": BLURBS[os.path.basename(path)],
                    "url": GH + "prompts/" + os.path.basename(path)})
card = open(f"{REPO}/prompts/01-prompt-card.md").read()
card_prompt = re.search(r"```\n(.+?)```", card, re.S).group(1).strip()

n_lessons = sum(len(s["lessons"]) for s in stages)
n_pitfalls = sum(len(s["pitfalls"]) for s in stages)

def stage_html(s):
    lis = "\n".join(
        f'<li class="lesson"><span class="tag tag-{l["tag"]}" title="{l["tag"]}">{l["tag"]}</span>'
        f'<span class="lx"><span class="lt">{l["t"]}.</span> <span class="ls">{l["s"]}</span></span></li>' for l in s["lessons"])
    pits = "".join(f"<li>{p}</li>" for p in s["pitfalls"])
    return f'''
<details class="stage" id="stage-{s["n"]}">
  <summary>
    <span class="sn">{int(s["n"]):02d}</span>
    <span class="sname">{s["name"]}</span>
    <span class="scount">{len(s["lessons"])} lessons · {len(s["pitfalls"])} pitfalls</span>
  </summary>
  <div class="sbody">
    <p class="sintro">{s["intro"]}</p>
    <ul class="lessons">{lis}</ul>
    <div class="pits"><h4>Pitfalls that cost time here</h4><ul>{pits}</ul></div>
    <a class="more" href="{s["file"]}">Read stage {int(s["n"])} in full</a>
  </div>
</details>'''

prompt_rows = "\n".join(
    f'<li><a href="{p["url"]}">{p["title"]}</a><span>{p["blurb"]}</span></li>' for p in prompts)

page = open(os.path.join(os.path.dirname(__file__), "template.html")).read()
page = (page.replace("{{STAGES}}", "\n".join(stage_html(s) for s in stages))
            .replace("{{PROMPTS}}", prompt_rows)
            .replace("{{CARD}}", html.escape(card_prompt))
            .replace("{{NLESSONS}}", str(n_lessons))
            .replace("{{NPITFALLS}}", str(n_pitfalls))
            .replace("{{GH}}", GH)
            .replace("{{STAGE_NAV}}", " ".join(f'<a href="#stage-{s["n"]}">{int(s["n"]):02d} {s["name"]}</a>' for s in stages)))
assert "{{" not in page, re.findall(r"\{\{\w+\}\}", page)
open(f"{REPO}/index.html", "w").write(page)
print(f"index.html: {len(stages)} stages, {n_lessons} lessons, {n_pitfalls} pitfalls, {len(prompts)} prompts, {len(page)//1024} KB")
