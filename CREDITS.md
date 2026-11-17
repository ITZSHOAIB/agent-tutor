# Credits

Several ideas in this skill came from studying **[LearnHarness](https://github.com/amosblomqvist/learnharness)** by Eero Alvar (AGPL-3.0). Among them:

- probing a learner's edge before teaching
- a predict → teach → check cycle for each step
- recording confidence with every answer
- wrong options that each represent a specific misconception
- separate retrieval-practice sessions with graded hints
- a record of propositions across sessions

No LearnHarness text or code is included here. The skill's files are our own wording and structure, written to run in any agent environment and to put real experiments in the learner's hands. Before each release, `tools/overlap.py` checks the shipped text for shared phrasing (see [CONTRIBUTING.md](CONTRIBUTING.md)).

Many of these ideas are older than either project and come from learning science: retrieval practice, spaced repetition, interleaving, desirable difficulties and confidence-weighted testing.

Review scheduling uses **[py-fsrs](https://github.com/open-spaced-repetition/py-fsrs)** (MIT), an implementation of the FSRS algorithm by the Open Spaced Repetition project.
