# Adapter: other coding agents (Codex, Cursor, Gemini CLI, Copilot, OpenCode…)

Any agent that can read and write files and run a shell. Paths like `scripts/due.py` are relative to this skill's folder (where `SKILL.md` lives); resolve them to an absolute path before running.

| Capability | How it's done here | Fallback used? |
|---|---|---|
| C1 Structured question | The agent's own question or choice tool if it has one that returns the answer to the session. Otherwise plain text (`adapter-plain-chat.md`): lettered options, then the confidence scale; the learner replies `B · 3 · because…`. When a step has a visual, the page asks that step's prediction and the learner pastes back its "Copy for chat" line | Often |
| C2 Files | The agent's file tools on the topic folder. For PDFs in `sources/`, use the agent's PDF reading if it has one, else `pdftotext` (poppler) to a `.txt` beside the file | No |
| C3 Code execution | For tries that compute: the learner runs the module's `lab.ipynb` in Jupyter or their editor; the agent writes the cells and reads the saved outputs. Other subjects use `lab.md` | No |
| C4 Web access | Web search or fetch, if enabled | Sometimes |
| C5 Delegation | Subagents, if the agent has them; otherwise inline | Sometimes |
| C6 Rendered visuals | A page from `assets/visual.html`, built with `scripts/build_visual.py … --standalone` and opened as a local file in the browser | No |
| C7 Shared doc with comments | None; markdown only | Yes |

## Rules load automatically
The topic folder's `AGENTS.md` holds the per-turn rules. Codex, Cursor and most other agents read `AGENTS.md` from the working folder; for agents that use another file name (`GEMINI.md`, `.cursor/rules`), copy or import it there.

## Commands
- Review queue: `uv run scripts/due.py <topic>/knowledge` (or `pip install "fsrs>=6,<7"` and `python`).
- Calibration: `python -I scripts/calibration.py <topic>` (`--write` at a module's close).
- Map view: `python -I scripts/map_view.py <module>/notes.md <module>/visuals <session logs...>`, then open the printed file.
- Visual: `python -I scripts/build_visual.py <name>.src.html <name>.data.json --standalone`, then open `<name>.html`.

## Keeping the answer in the turn
A plain-text question ends the turn and the learner's reply starts the next one, which is fine. Never run a command that waits for the learner in a detached process: the agent won't see its result.
