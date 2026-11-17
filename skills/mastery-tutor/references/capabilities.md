# Capabilities: what the method needs from its environment

The method is written against the capabilities below, never against a specific agent, app or tool. Each environment gets a short adapter (`adapter-<environment>.md` beside this file) that maps these capabilities to its real tools. When a capability is missing, use the fallback. The method still works, just with more manual steps.

| # | Capability | Used for | Fallback when missing |
|---|---|---|---|
| C1 | **Structured question**: options, a confidence pick and a free-text notes field, answered in one go; the adapter must return the answer to the active tutor session | Every probe, prediction, check, warm-up and practice problem | Plain text: lettered options plus the confidence scale. The learner replies like `B · 3 · because…` |
| C2 | **Files**: read and write the topic folder | The record: roadmap, session logs, `knowledge/`, notes | At session end, the agent prints every changed record as a block; the learner saves it and pastes it back at the start of the next session |
| C3 | **Code execution** | Tries that compute (a cell, a simulation), run by the learner (`teach.md`, "Hands on"); measuring data for a visual. Topics without computing don't need it | The agent gives code for the learner to run and paste back. Ask for a prediction before the output is seen |
| C4 | **Web access** | Verifying facts before teaching them | Teach only what can be checked locally or is stable; flag everything else as unverified |
| C5 | **Delegation**: a separate worker with its own context | Background fact-checks; building demos; the independent expert review of a roadmap | Do it inline (slower). For the expert review, open a fresh session that gets only the roadmap and learner profile |
| C6 | **Rendered visuals**: HTML shown inline, or a file the learner opens in a browser | Dynamic ideas (`visuals.md`), the module map with position | Mermaid or ASCII in markdown; describe what to look for. A page from `assets/visual.html` also works as a local file opened in a browser |
| C7 | **Shared document with comments** | Optional learning journal | Just the markdown |

## Confidence scale (same everywhere)
1 Guessing (≤30%) · 2 Unsure (~50%) · 3 Fairly sure (~75%) · 4 Certain (95%+)

## Rules for portability
- **Markdown in the topic folder is the record.** Anything else (inline visuals, docs, dashboards) is a view generated from it, so switching environments loses nothing.
- **Formats are plain:** markdown tables, mermaid for graphs, question headings like `### Q5 · predict · node_slug`. Any agent can read and write them.
- **Scripts in `scripts/` are standard Python** with no environment assumptions. Output paths are arguments.
- **A stored answer is not a resumed conversation.** When a structured question runs outside chat, the adapter must keep the tutor waiting or ensure the answer is picked up on the next turn.
- **Method files never name a product or tool.** They name a capability (`C1`), and the adapter says how to do it.

## Writing an adapter
An adapter is one short file per environment (`adapter-<environment>.md`): the table above with the second column filled in ("how it's done here", and whether the fallback is used), then only what that environment needs spelled out: commands, where pages go, how rules load. Never change a method file to fit an environment; if the method can't be expressed through the capabilities, add a capability.
