# Contributing to mastery-tutor

Thanks for helping. Fixes of any size are welcome, from a typo to a new adapter.

Please read and follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to contribute

| Area | Where | Notes |
|---|---|---|
| The method | [`skills/mastery-tutor/references/`](skills/mastery-tutor/references/) | How sessions teach. Changes need a reason from real use |
| Adapters | `skills/mastery-tutor/references/adapter-*.md` | How the method runs in one environment |
| Scripts | [`skills/mastery-tutor/scripts/`](skills/mastery-tutor/scripts/) | Standard-library Python (plus `fsrs` for `due.py`), with tests |
| Templates | [`skills/mastery-tutor/assets/`](skills/mastery-tutor/assets/) | Topic scaffold, notebook, visual starter |
| Examples | [`examples/`](examples/) | Real visuals built from measured data |
| Bugs and ideas | [Issue forms](https://github.com/ITZSHOAIB/mastery-tutor/issues/new/choose) | Pick the form that fits |

## Ground rules

- **Method files name capabilities, never products.** `probe.md`, `teach.md` and the other method files talk about "a structured question (C1)", not about a specific tool. Environment details belong in an adapter. `tests/check_skill.py` enforces this.
- **Evidence before tooling.** New machinery (a script, a dashboard, a capability) lands only after the friction it fixes showed up in real sessions. Say which sessions in the PR.
- **Markdown is the record.** Anything generated (pages, maps, charts) must be rebuildable from the topic folder.
- **Keep the skill portable.** Frontmatter stays within the six fields of the [Agent Skills spec](https://agentskills.io/specification): `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. `SKILL.md` stays under 500 lines, and references stay one level deep.
- **Your own words.** Don't paste text from other tutoring prompts. Before a release, run the overlap check below.

## Adding an adapter

1. Copy the capability table from [`capabilities.md`](skills/mastery-tutor/references/capabilities.md) into `skills/mastery-tutor/references/adapter-<environment>.md`.
2. Fill in how each capability is done there and whether the fallback is used.
3. Add only what that environment needs spelled out: commands, how rules load, where pages go.
4. Link it from the "First: find your environment" list in `SKILL.md`.

## Checks

```bash
python -I tests/check_skill.py                                  # frontmatter, links, product names in method files
uv run --with pytest --with "fsrs>=6,<7" pytest                 # script tests
claude plugin validate .                                        # if you have Claude Code
```

CI runs the first two on every pull request.

### Overlap check (maintainers, before a release)

```bash
mkdir -p /tmp/lh-src && cd /tmp/lh-src
gh api "repos/amosblomqvist/learnharness/git/trees/HEAD?recursive=1" --jq '.tree[]|select(.type=="blob").path' \
  | grep -E '^(src/agent/prompts/|skills/learnharness/|docs/teaching-methodology)' \
  | while read p; do gh api "repos/amosblomqvist/learnharness/contents/$p" -H "Accept: application/vnd.github.raw" > "$(echo $p | tr / _)"; done
cd - && python -I tools/overlap.py 5 /tmp/lh-src $(find skills -name '*.md')
```

Never commit the fetched text. Reword anything beyond common phrases.

## Pull requests

- One change per PR, with what it fixes and how you checked it.
- For method changes, describe the session that showed the problem (no personal answers needed).
- Update the README or `CHANGELOG.md` when behaviour or layout changes.
