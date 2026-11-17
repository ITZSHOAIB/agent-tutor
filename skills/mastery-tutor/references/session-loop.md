# Session loop: how each session runs

Sessions are live. Notes are written from what actually happened, at the end of each step and session; nothing is pre-written for the learner to read.

## Concept module (about 45–60 min)

| Step | Time | What happens | Method |
|---|---|---|---|
| **Warm-up** | 3 min | Two retrieval questions on whatever is due, lowest recall first. The idea isn't named; the learner has to recognise which idea the situation needs. From 10 rated answers on, one line on calibration | `review.md` |
| **Spot** | 2 min | The module's anchor from `ROADMAP.md`: "In your work, X happens. Why?" | |
| **Probe** | 3–5 min | 2–4 questions to find where the learner's understanding ends. Skip what they already hold | `probe.md` |
| **Map** | 2 min | A small dependency graph of the module in `notes.md`, plus two or three sentences on the approach. The learner OKs it; teaching starts next turn | `teach.md` |
| **Steps** | 20–30 min | For each step: predict → the learner tries it → check. At most one prediction and one check per step; a missed check is repaired before moving on | `teach.md`, `questions.md` |
| **Break it** | 10 min | The learner changes one thing on purpose, predicts, tries it and explains. Required | `teach.md` |
| **Plug back** | 5 min | One concrete rule for the learner's own work, in their words. Required | `teach.md` |
| **Explain back** | 3 min | The module goal in 2–3 sentences, without notes. Graded strictly. Required | `teach.md` |

**Done** means every step's check passed (after any repair) and Break it, Plug back and Explain back are in `notes.md`. If time runs out, those open the next session. Nothing else blocks progress.

## Multi-session modules
Each session opens with a Warm-up and closes with a short Plug back. Probe and Map happen in the first session; later sessions reuse the map and update it. Explain back runs at the end of the last session. `PROGRESS.md` shows "In progress (n/N)".

## Build variant
For modules whose output is something made: working code, an essay, a translation, a dish, a piece of music, a plan. Teaching merges into making.

| Step | What happens |
|---|---|
| Warm-up, Spot | As above |
| Goal | What the thing will do when it works, in one sentence |
| Map | The pieces to build, in dependency order |
| Build | Small pieces, each with predict → make it → check. Before trying: what will the result look or sound like? |
| Break | Change one thing on purpose and explain the result |
| Plug back | One rule for the learner's work |
| Explain back | Walk through what they made and say why it works |

## End of a phase
1. **Practice session** (about 45 min): problems drawn from the review queue that never name the idea they need (`practice.md`).
2. **Checkpoint:** the phase's bigger task from `ROADMAP.md`, on real work.

## After every step and session
Update, in this order: the session log, the module's `notes.md`, `knowledge/` (with a review row per check), and `PROGRESS.md` (at a module's close, its Calibration section via `scripts/calibration.py --write`). The learner skims and corrects. Formats: `records.md`.

## Picking up where you left off
At the start of any session read `PROGRESS.md`, the latest session log, and the review queue. If the last session ended mid-module, continue from its last logged step; if it ended before the close, the close comes first.
