# Records: the topic folder

Markdown in the topic folder is the record. Every view (map page, visual, progress chart) is generated from it, so any agent can pick a topic up where another left it.

```
<topic>/
├── AGENTS.md                 per-turn rules; CLAUDE.md imports it
├── ROADMAP.md                learner profile, endpoint, phases, modules (plan.md)
├── PROGRESS.md               module status, calibration, practice, checkpoints
├── knowledge/
│   ├── propositions.md       facts taught, latest reading, evidence IDs
│   ├── misconceptions.md     wrong models found, repaired or not
│   └── reviews.md            one row per review; scripts/due.py reads it
├── sessions/
│   └── YYYY-MM-DD-<N.M>.md   every question, key written first, answer, confidence, verdict
└── phase-N-<name>/
    └── N.M-<slug>/
        ├── notes.md          map (mermaid), steps, Break it, Plug back, Explain back
        ├── lab.md            the learner's tries: prediction, what they did, what it showed
        │                     (lab.ipynb instead when the tries compute)
        └── visuals/          only where a step earned a page: <name>.src.html, .data.py, .data.json, .html
```

Create it with `scripts/new_topic.py`:
- `topic <dir> "<name>"`: everything above the phase folders;
- `module <dir> phase-1-<name>/1.1-<slug> "1.1 <title>" [--lab ipynb]`: `notes.md` and `lab.md` (or `lab.ipynb`);
- `session <dir> 1.1 "1.1 <title>"`: today's session log.

The blank formats live in the skill's `assets/` (`topic/`, `module-notes.md`, `lab.md`, `lab.ipynb`, `session-log.md`); `assets/topic/sessions/README.md` documents the session-log fields.

## IDs that tie it together
- **Questions:** `Q<n>` per module, numbered across its sessions; cited as `1.1-Q3`, practice as `P1-Q7`.
- **Map nodes:** lowercase slugs with underscores (`wish_needs_subjunctive`), never renamed once used.
- **Propositions** `P<n>` and **misconceptions** `M<n>`: cited from reviews and evidence columns.

## Who writes what
The tutor writes every record, during the session, as it happens. The learner reads and corrects. Nothing is filled in from memory after the fact.
