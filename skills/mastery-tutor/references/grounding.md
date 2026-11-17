# Grounding: teaching only what a source supports

A model's memory is a stale, unlabelled source: it can't tell which of its facts have changed since training, and a wrong fact feels as sure as a right one. So nothing the learner is taught rests on the tutor's memory alone where a source can be found. Every claim the module stands on is **supported** (a quoted passage from a named source), **dated** (when it was checked) and **correctable** (a later fix reaches everything built on it). That makes errors rare and visible; it doesn't make them impossible, so say so if asked.

The one rule under everything below: **a check counts only if it returns a quoted passage and where it sits in the source.** A verdict without a quote is one model agreeing with another, and goes down as unverified.

## 1. Profile the topic (planning)
Rate each area of the topic, not the topic as a whole:

| Rating | Means | Example |
|---|---|---|
| Stable | Settled for decades | grammar rules, calculus, the physics of a lever |
| Moving | Changes within a year or two | software versions and APIs, prices, current law and tax, clinical guidelines, rankings |

Mark **high stakes** where a wrong fact could cost the learner health, money, legal standing or safety. Write the profile in the roadmap's Learner section; it decides how much checking each area gets.

## 2. Research before drafting (planning)
Before the roadmap exists, hand a separate worker (C5) the learner's goal and the profile, and nothing else, with web access (C4). It returns a short source index, never a draft and never long extracts, ranked in tiers:

| Tier | What counts |
|---|---|
| 1 | The primary source: official documentation or specification, the statute or regulation, the standard, the original paper or dataset, a reference grammar or dictionary |
| 2 | Established secondary: a current textbook, a review article, a recognised reference work |
| 3 | Leads only: blogs, forums, videos, other models' answers. They point to a source; they never support a claim |

Keep it small: about three sources for a stable topic, up to eight for a moving one, the fewest that cover the roadmap. Each entry gets an ID (`R1`, `R2`), the version or edition, and the date accessed, in `sources/README.md` next to the learner's own `S` sources.

**Store references, not copies.** The index holds the link and the place inside; the quotes that matter live in the module ledgers. Save a file into `sources/` only when the learner will read it as a try (a statute section, a spec page) or it may disappear. Copies freeze an old version, cost context and may not be yours to keep. Research comes first so that sources shape the roadmap; research done after a draft turns into hunting for agreement. Hand this index to the independent reviewer too (`plan.md`, step 6).

## 3. A claim ledger per module (before teaching it)
Once per module, before its probe, list what the module stands on as short single claims: the goal, and each step's "what's actually true". Include every number, name, version, date, quotation and example output. Then hand a separate worker (C5) the claims and the source index, not your reasoning or the lesson, and have it return for each claim: supported, contradicted or not found, with the quote and its place (`R2 §3.1`).

Write the result in the module's `notes.md` under **Claims**: claim · rating · source and place · checked (date) · status.

- **Moving or high-stakes claims** need a tier 1 source, or two independent tier 2 sources.
- **Stable claims** may rest on one tier 1 or 2 source, still with a quote. "Standard knowledge" is not a source.
- **Contradicted:** teach what the source says; if the learner's own material says otherwise, follow "Their sources" in `plan.md`.
- **Sources disagree:** teach the disagreement and which source is newer or more primary.
- **Not found:** don't teach it as fact. Drop it, or teach it labelled as unverified and list it in the roadmap's Unverified section.

## 4. Teaching from the ledger
- State ledger claims plainly; cite the source for moving ones (`R2 §3.1`) so the learner can read it.
- A claim that comes up mid-session and isn't in the ledger: say it's unchecked, add it to the ledger as unverified, check it in the background (C5), and correct it next turn if it was wrong.
- **The try outranks every source.** When the learner's own result (output of the cell, the dictionary entry, the statute's text) contradicts what the tutor said, the result wins. Fix the ledger and log it as a tutor error in the session log.

## 5. Correcting what was taught
When a taught claim turns out wrong: tell the learner at the start of the next session, in one line, what was wrong and what's true; fix the notes, propositions and answer keys that used it; and mark every review row built on it as due now, so the corrected version gets practised.

## 6. Keeping it fresh
Before quizzing an idea in review or practice, look at its module's ledger. A moving claim last checked more than 90 days ago gets checked again first, with the same quote rule.

## Without web access
Say so at the start of the first session: moving areas are taught from training data and may be out of date. Lean on the learner's sources and on tries, which check themselves. Every moving claim goes in the ledger as unverified.
