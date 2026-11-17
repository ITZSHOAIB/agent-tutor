# Adapter: plain chat (no tools)

For a chat assistant that can't read files, run code or browse (for example a claude.ai project without code execution). Everything runs on fallbacks; the method still holds.

| Capability | How it's done here | Fallback used? |
|---|---|---|
| C1 Structured question | Write the question with lettered options, then the confidence scale. The learner replies `B · 3 · reasoning…`, or `? · reasoning…` for "don't know" | Yes |
| C2 Files | The learner keeps the topic folder (even where the chat can run code: its files vanish with the conversation). Session start: the learner pastes `ROADMAP.md`, `knowledge/reviews.md`, the module's `notes.md` and the relevant `knowledge/` rows. Session end: the assistant prints every changed file in full as a code block to save | Yes |
| C3 Code execution | Only for tries that compute: the assistant gives a short script; the learner predicts the output, runs it locally and pastes the result. Other tries (a source, a sentence, a move) need no code | Yes |
| C4 Web access | Teach only stable facts; mark anything fast-moving as unverified and add it to the session's "uncertain" list | Yes |
| C5 Delegation | None. For the roadmap's independent review, the learner opens a fresh chat with only the roadmap and profile | Yes |
| C6 Rendered visuals | Mermaid or ASCII inline. Where the app renders HTML (claude.ai artifacts), a page from `assets/visual.html` | Partly |
| C7 Shared doc with comments | None; markdown only | Yes |

Sources: the learner attaches their material to the conversation (or a project's knowledge, where the app has one); keep the `sources/README.md` index in the records printed at session end.

Scheduling without `scripts/due.py`: use the fixed interval ladder in `review.md`. Calibration without `scripts/calibration.py`: count the answer lines by hand (`review.md`, "Calibration").
