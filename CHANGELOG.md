# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-11-17

Any subject, not only code.

### Added
- `assets/lab.md`: a markdown lab book (prediction, what I did, what it showed) for any subject. `new_topic.py module` creates it by default; `--lab ipynb` creates the notebook for topics that compute.
- "Hands on" in `teach.md` describes a **try** per kind of subject: code, maths and science, languages, history and law, physical and creative skills, professional cases.

### Changed
- Experiments are now tries: the learner runs, reads, says or does something, with a prediction first. Code execution is only needed for tries that compute.
- Planning asks about the learner's world (hobbies and materials, not only tools) and what they can do hands-on; roadmap rows have a Try column.
- Facts that always get verified now include statistics, current law, dates and exact quotations.
- The build variant covers anything made: an essay, a translation, a dish, a piece of music.

## [0.1.0] - 2026-11-17

First public release.

### Added
- `tutor` skill: plan a topic, probe, map, predict-run-check steps, Break it, Plug back, Explain back, practice sessions and spaced review.
- Method references written against capabilities (C1–C7), with adapters for Claude Code, other coding agents and plain chat.
- Topic scaffold (`scripts/new_topic.py`) with `AGENTS.md` / `CLAUDE.md` rules that load every turn.
- `scripts/due.py`: FSRS review queue replayed from a markdown log.
- `scripts/map_view.py`: module map with the learner's position.
- `scripts/build_visual.py` and `assets/visual.html`: one-idea visual pages with a locked prediction and a "Copy for chat" line; `--standalone` for local files.
- Claude Code plugin marketplace manifest.
- Worked example: the prefix-cache explorer, built from real tokenizer measurements.

[0.2.0]: https://github.com/ITZSHOAIB/agent-tutor/releases/tag/v0.2.0
[0.1.0]: https://github.com/ITZSHOAIB/agent-tutor/releases/tag/v0.1.0
