# Questions: asking and reading the answer

Used everywhere an answer has to come back: probes, predictions, checks, warm-ups, practice.

## Format
Each question is one structured question (capability C1 in `capabilities.md`) with three parts:

1. **The question**, with 2–4 options, plus a way to give a free answer, "don't know", or reasoning instead.
2. **How sure are you?** on the fixed scale: 1 Guessing (≤30%) · 2 Unsure (~50%) · 3 Fairly sure (~75%) · 4 Certain (95%+).
3. **Notes:** free text for reasoning.

Ask for reasoning in the notes field. A picked option tells you little; the reasoning shows the model in their head.

Open answers (explain-back, open predictions) are plain free-text replies.

## Write the answer key first
Before posing anything, put the correct answer and the reason in the session log. Grade against that, not against what feels right after reading their reply. For open answers, list exactly which points they hit and which they missed.

## A good check
- Can be solved with only what this session covered.
- Isn't the last paragraph reworded as a question.
- Uses the idea on a case that hasn't come up yet, where possible. Pure recall only when there's nothing to apply.
- Has a miss that tells you what went wrong.

## Making the options
- Start from the correct option. For each wrong option, pick a believable wrong belief and write the answer that belief would produce. Note the belief next to it in the log.
- Make the options look alike: similar length, same style, no justification in any of them, no emphasis.
- If someone who skipped the lesson could still pick the right one, rewrite it.

## Reading answer plus confidence
- **Right and sure:** owned. Keep going.
- **Right and unsure:** could be luck. Reinforce it once.
- **Wrong and sure:** a wrong belief they rely on. The most useful thing a question can find. Name it, test how far it goes, fix it, add it to `misconceptions.md`.
- **Wrong and unsure:** a near miss or a gap. A short correction.
- **"Don't know":** a gap. Not counted as wrong.

## Afterwards: always close the loop
Every answered question ends with the learner knowing the correct answer. Leaving a wrong pick unexplained lets the wrong option stick.

1. **Verdict**, plainly: right or wrong.
2. **The correct answer, named explicitly** (e.g. "It's A: one token"), with the reason in one or two lines.
3. **On a miss, what their pick assumed:** the wrong belief that option was built from ("B is what you'd get if markers were ordinary text").
4. **Their reasoning:** where it held, where it broke.

On a miss, also ask for one line in their own words on why the right answer is right, and whether it's clear now. Producing the explanation themselves fixes it better than reading one. "Still confused" means explain it from a different angle (another example, a picture, a smaller case), not the same words again.

If the question tool already showed the learner 1–3 (some can: see the adapter), don't repeat them at length. One line naming the verdict and answer, then spend the words on 4 and on their own-words line: confirm it, or fix the part that's still off.

Timing differs by question type:
- **Predictions:** when the learner does the try, its result is the reveal; name the answer explicitly once they've seen it. Otherwise reveal at the start of the teaching that follows.
- **Checks:** reveal right away. A miss then gets a repair and a re-check in a new form, so the reveal doesn't give the re-check away.
- **Probes:** don't teach mid-probe, since that would contaminate the next question. When the probe ends, give a short answer key for every probe question missed or answered unsure.
- **Practice:** the one exception, because the effort of retrieving is the point (`practice.md`). Reveal once the problem is solved or the learner stops.
- Log the question, answer key, their answer, confidence, verdict and notes in the session log, and add a row to the review log for each idea it tested (`review.md`).
