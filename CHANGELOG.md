# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

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

[0.1.0]: https://github.com/ITZSHOAIB/agent-tutor/releases/tag/v0.1.0
