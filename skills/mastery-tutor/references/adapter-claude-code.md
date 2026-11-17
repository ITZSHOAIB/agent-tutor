# Adapter: Claude Code (primary)

Sessions run in chat. A page is published only when a step earns one (`visuals.md`). Paths like `scripts/due.py` are relative to this skill's folder; in a shell command write them as `<skill>/scripts/due.py`.

| Capability | How it's done here | Fallback used? |
|---|---|---|
| C1 Structured question | `AskUserQuestion` with two questions in one call: the question (2–4 options; "Other" takes a free answer, "don't know" or reasoning) and confidence (the four scale labels). Ask for reasoning in the notes field. Keep option labels short (`A · estés`) and put the longer text in each option's description. When a step has a visual, the page asks that step's prediction instead and the learner pastes back its "Copy for chat" line | No |
| C2 Files | Read / Write / Edit on the topic folder. Edit markdown tables with the edit tools, not shell one-liners: cells hold `\|` and backslashes that shell quoting mangles | No |
| C3 Code execution | For tries that compute: the learner runs the module's `lab.ipynb` in Jupyter or VS Code; the tutor writes its cells and reads the saved outputs. Other subjects use `lab.md` and need no code. The tutor's own shell is for setup and for checking facts while planning | No |
| C4 Web access | WebSearch / WebFetch | No |
| C5 Delegation | The Agent tool. Fact-checks run in the background | No |
| C6 Rendered visuals | A published Artifact page for anything the learner interacts with or opens on a phone. Without Artifacts, build with `--standalone` and give the learner the file path | No |
| C7 Shared doc with comments | Not used by default; the markdown is enough | Yes |

## Rules load automatically
Each topic folder has an `AGENTS.md` with the per-turn rules and a one-line `CLAUDE.md` that imports it (`@AGENTS.md`). Claude Code loads them whenever the session works in that folder, so the rules hold even when the skill isn't re-read. Other agents that read `AGENTS.md` get the same rules.

## From a phone
Start the session with `claude --rc` (or `/remote-control` inside one) and continue it in the Claude app or at claude.ai/code. Structured questions and permission prompts are forwarded; published pages open from their link. Check that the first question renders on the phone before relying on it. On a phone, prefer visuals and "change one value" edits over writing code (`teach.md`, "Hands on").

## Visual pages (C6)
Follow `visuals.md`. Here:
1. Copy `assets/visual.html` into the module's `visuals/` folder as `<name>.src.html` and fill only the `{{…}}` parts.
2. Write `<name>.data.py` next to it. It runs the real thing (from the topic's environment) and writes `<name>.data.json`. Build with `python -I <skill>/scripts/build_visual.py <name>.src.html <name>.data.json`, which writes `<name>.html`.
3. If the `artifact-design` skill is available, load it before publishing. Look at the page once in both themes and at phone width, and fix what that shows.
4. Publish `<name>.html` with the Artifact tool (private by default) and give the learner the link. Republishing the same path keeps the link.
5. When the learner pastes the "Copy for chat" line, log it as the step's prediction in the session log and close the loop as usual.

Leave runtime capabilities (`db` and the rest) off. Writes to a page don't wake the session; the learner would still have to say "done" in chat.

## Lab
Most subjects use `lab.md` (`new_topic.py module …`): one block per step with the try, the learner's prediction, what they did and what it showed. Write the block before asking; read it back after the learner fills it in, or take their answer from chat and write it there yourself.

When the tries compute, scaffold with `--lab ipynb` and fill in the notebook's title and goal. Imports and model loading go in the cell tagged `setup`. Per step: a markdown cell for the prediction, a code cell for the experiment (empty when the learner writes it), and a markdown cell for "What the output showed". If the learner wants JupyterLab, start it as a background command from the topic folder, for example `uv run jupyter lab --no-browser`, and read the saved notebook after each run.

## Map view
```
python -I <skill>/scripts/map_view.py <module>/notes.md <module>/visuals <session logs...>
```
It prints the HTML file it wrote. Publish that as an Artifact, or give the learner the path.

## Review queue
```
uv run <skill>/scripts/due.py <topic>/knowledge
```
Without `uv`: `pip install "fsrs>=6,<7"` once, then run it with `python`.

## Calibration
```
python -I <skill>/scripts/calibration.py <topic> [--write]
```

## Skills that help (optional)
`artifact-design` before publishing a page; any charting or diagram skill for static figures.
