# Probe: where does teaching start?

Before a module teaches anything, spend a few questions finding out what the learner already has. The answer decides what gets skipped and where the first step goes.

## Read first
- The module's goal in `ROADMAP.md`.
- `knowledge/propositions.md` and `knowledge/misconceptions.md`. Anything marked `held` is not re-tested; anything in misconceptions is tested first.

## Pick the threads
Ask: to reach this goal, what must the learner already be able to reason about? Each of those is a thread. A module rarely has more than three.

## Ask high, walk down
Open each thread with a question at the level the goal actually needs. An experienced engineer usually clears the basics, so starting low wastes a question. Then let each answer set the next one:

| Answer | Next question |
|---|---|
| Right, sure of it | Much harder, or close the thread |
| Right, hesitant | A bit harder; mark the idea shaky |
| Wrong, sure of it | Stay here and map how far the wrong idea reaches |
| Wrong, hesitant, or "don't know" | Easier, until an answer comes back right |

A thread is located once there is a known-good level just below a known-bad one. A strong thread is evidence that nearby threads start high too.

If a question can't change where teaching starts, don't ask it.

## Stop
Two to four questions per module is the usual cost. Stop as soon as the starting point is obvious.

## Record (session log)
For each thread: highest level answered well, lowest level missed, any wrong ideas found, and the step teaching opens with. Then trim or extend the module map to match, and give the learner a short answer key for any probe question missed or answered unsure (`questions.md`).
