# Review: spacing retests over time

Ideas fade on a predictable curve, and each successful recall slows the fade. So every taught idea gets a **due date**. Warm-ups and practice sessions draw from whatever is due.

## The record
One file per topic, `knowledge/reviews.md`, with one row per review event. The schedule is never stored: it's recomputed from this log, so the log is the only thing to keep correct.

| Column | Content |
|---|---|
| Date | `YYYY-MM-DD` |
| Item | A proposition ID from `propositions.md` |
| Kind | `lesson` (checked in the session it was taught) or `retrieval` (any later warm-up, practice or check) |
| Rating | `Again` · `Hard` · `Good` · `Easy` |
| Evidence | Question IDs from the session log (`1.1-Q7`) |
| Note | One line on why, especially for misses ("thought the model sees roles as metadata") |

## Rating an answer
| Answer | Rating |
|---|---|
| Wrong, or "don't know" | Again |
| Right, with confidence 1–2, or only after help or repair | Hard |
| Right, confidence 3 | Good |
| Right, confidence 4, no help | Easy |

- **A `lesson` review counts as Good at most.** Getting it right minutes after hearing it says little about whether it will come back later.
- **Several events on one item in one day count as one review, the worst one.** A predict, a check and a repair on the same step don't stack.
- **A misconception's retest is logged against the proposition that holds the correct model.** If no such proposition exists yet, add one.

## When to log
- At the end of each step, for each proposition the step's check covered.
- After every warm-up and practice problem, for each proposition it needed.

## Picking what to review
List items that are due, lowest predicted recall first, then items that were taught but never checked. Warm-ups take the top two. A practice session takes the whole list, mixed across topics. Before quizzing an item, recheck any moving claim it rests on that was last checked over 90 days ago (`grounding.md`, section 6).

## Scheduling
- **With code execution (C3):** `scripts/due.py` replays the log through the FSRS algorithm (target recall 90%) and prints what's due.
- **Without it:** use a fixed ladder of intervals: 1 → 3 → 7 → 21 → 60 days. Good or Easy moves an item one rung up, Hard keeps it on the same rung, and Again drops it back to 1 day. The agent works out due dates by reading the log.

## Calibration
The confidence picks are evidence too. `scripts/calibration.py <topic>` compares the confidence the learner stated with how often they were right, across every session log, and prints one line and a table.
- **At a warm-up,** once there are 10 or more rated answers, give its first line in a sentence and move on. Not every turn: a score on each answer turns questions into a test.
- **At a module's close,** run it with `--write`. It rewrites the Calibration section of `PROGRESS.md`.
- **When asked** ("how calibrated am I?"), show the line and the table, and name the level furthest off with one habit for it ("Certain was right 4 of 6 times: when you feel certain, check one more thing first").
- **Without code execution,** count the answer lines per confidence level at a module's close and fill the table by hand.

It isn't a grade. Under 10 answers the numbers say little, and finding out you're overconfident is the useful part.
