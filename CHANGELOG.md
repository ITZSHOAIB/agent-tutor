# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Module recap: `scripts/recap.py` builds one page from the records when a module closes: the map with passed steps, predictions and checks, calibration in this module as a chart, the wrong models found and whether they're repaired, and the learner's Break it and rule. Offered at the close, or on "recap this module".

### Changed
- Pages are human in the loop: the tutor offers any page (step visual, map, recap) in one line and builds it only on a yes. Asking for one counts as yes; a no isn't asked again for that step.
- Map labels starting with a number (`1. …`) no longer render as "Unsupported markdown: list".
- Role-play moved out of `teach.md` into its own reference, `role-play.md`, read only when a scene is played. `teach.md`, which the agent re-reads every step, is about 340 words shorter.
- `tests/check_skill.py` holds `SKILL.md` to 1,400 words and each reference to 2,000, so the skill can't quietly grow.
- The topic's `AGENTS.md` asks the tutor to cite the learner's sources by ID. The README covers material in planning, `calibration.py` in the FAQ, and the small-context rule.

## [0.4.0] - 2026-11-17

### Added
- Calibration: `scripts/calibration.py` compares the confidence the learner stated with how often they were right, from the session logs. It prints one line (average stated vs right, Certain's record, confident misses, and the trend over the last 20 answers) and the per-level table; `--write` rewrites the Calibration section of `PROGRESS.md`. The tutor gives the line at warm-ups once there are 10 rated answers, writes it at each module's close, and shows it when asked ("how calibrated am I?"). Answer lines it can't read are listed, not guessed.
- Role-play as a full kind of try (`teach.md`, "Role-play"): the tutor plays the other side in a short scene from the learner's world, after a written prediction, then steps out to check and runs it again with one change. Planning puts it into most modules of language and people-skill topics, and "can we role-play it?" is on the list of things the learner can ask for.
- Your sources: new topics get a `sources/` folder with an index (`S1`, `S2`). Planning asks for the learner's material every time, follows it where it's sound, takes a past exam's format for the checkpoint and practice, and records errors in the material so they're taught against at the right step. Steps cite it (`S1 §4.2`) and use its passages as tries. Adapters say how to read PDFs.

## [0.3.2] - 2026-11-17

### Added
- "What the learner can ask for": plain-language requests the tutor honours at any point (show me this, where am I, what's due, give me a problem, skip, is that true, stop here). The tutor mentions them once at the end of a topic's first session; the README lists them.
- Visuals on request: when the learner asks to see a step, the tutor builds a page even where it wouldn't have started one, with the setting chosen to hit the learner's open misconception.

### Changed
- The Claude Code adapter's sample option label no longer comes from language models.

## [0.3.1] - 2026-11-17

### Changed
- Examples in the skill's references now come from many subjects (languages, history, physics, law, cooking, money) instead of mostly from language models.
- `examples/cache-explorer`: dropped the details that referred to one learner and one session.

## [0.3.0] - 2026-11-17

Renamed from agent-tutor to **mastery-tutor**, after mastery learning: no moving on until a module is mastered, misses repaired and retested, and spaced review to keep it.

### Changed
- Repository, plugin and marketplace: `ITZSHOAIB/mastery-tutor` (the old URL redirects). Install with `/plugin marketplace add ITZSHOAIB/mastery-tutor` and `/plugin install mastery-tutor@mastery-tutor`.
- Skill: `tutor` is now `mastery-tutor` (`skills/mastery-tutor/`), so it no longer shares a folder name with other tutor skills in `.agents/skills/`. Run it as `/mastery-tutor` (Skills CLI) or `/mastery-tutor:mastery-tutor` (plugin).

### Upgrading
Remove the old install (`/plugin uninstall agent-tutor@agent-tutor` and `/plugin marketplace remove agent-tutor`, or delete `.agents/skills/tutor/`), then install again. Existing topic folders work unchanged; their `AGENTS.md` mentions the old skill name, which is harmless.

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
- `tutor` skill (now `mastery-tutor`): plan a topic, probe, map, predict-run-check steps, Break it, Plug back, Explain back, practice sessions and spaced review.
- Method references written against capabilities (C1–C7), with adapters for Claude Code, other coding agents and plain chat.
- Topic scaffold (`scripts/new_topic.py`) with `AGENTS.md` / `CLAUDE.md` rules that load every turn.
- `scripts/due.py`: FSRS review queue replayed from a markdown log.
- `scripts/map_view.py`: module map with the learner's position.
- `scripts/build_visual.py` and `assets/visual.html`: one-idea visual pages with a locked prediction and a "Copy for chat" line; `--standalone` for local files.
- Claude Code plugin marketplace manifest.
- Worked example: the prefix-cache explorer, built from real tokenizer measurements.

[Unreleased]: https://github.com/ITZSHOAIB/mastery-tutor/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/ITZSHOAIB/mastery-tutor/compare/v0.3.2...v0.4.0
[0.3.2]: https://github.com/ITZSHOAIB/mastery-tutor/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/ITZSHOAIB/mastery-tutor/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/ITZSHOAIB/mastery-tutor/releases/tag/v0.3.0
[0.2.0]: https://github.com/ITZSHOAIB/mastery-tutor/releases/tag/v0.2.0
[0.1.0]: https://github.com/ITZSHOAIB/mastery-tutor/releases/tag/v0.1.0
