# Visuals: one-off pages for one idea

Teaching happens in chat. A visual (C6) is a single page made for one idea in one step and thrown away after the module. It isn't an app. Make one only when it does something chat can't.

## When a visual is worth making
- **The idea changes with a setting.** A pendulum's period as its length changes, compound interest across rates, a melody across tempos, a cache that breaks at an edit. If the learner would learn from moving a slider or clicking an edit, show it moving.
- **The idea has a shape the eye reads faster than prose.** A sequence's parts drawn to scale, or a curve.
- **Not** for a definition, a list, or a single number. A sentence, a table or a mermaid diagram in chat does that better and costs almost nothing.

At most one visual per step. Most steps need none.

## On request
When the learner asks for a visual ("show me this", "can I see it"), build a page, even where you wouldn't have started one. Find the setting worth moving: usually the thing their open misconception gets wrong, so moving it shows the belief failing. Give only a diagram or table in chat when they asked for one ("draw it", "a quick diagram") or the environment can't show a page. The quality rules below still apply. If they ask in the middle of a question, close that loop first, or let the page ask the question.

## What makes it good
1. **One idea, one question.** The page answers one prediction. Everything on it serves that.
2. **Real numbers.** Generate the data by running the real thing (the formula, the simulation, the real data, the software) with a script saved next to the page. Never type numbers in by hand. Say on the page how they were made, and what is exact and what is simplified.
3. **Predict first, then reveal.** The page asks the step's prediction with options and a confidence pick, and locks before anything that gives the answer away. After locking, each wrong option shows the belief it was built from. Check everything visible above the prediction for spoilers: labels, captions, pre-drawn states.
4. **Then let them poke it.** Give two to four changes they can make, each with a one-line note on what to notice. Choose changes that hit the learner's open misconception from the session log.
5. **The learner's world.** Use their kind of example (their agent, their requests), with real units and terms.
6. **Answers come back to the session.** The page ends with a "Copy for chat" line (`id · predicted B · Fairly sure · right · tried: … · noticed:`) that the learner pastes in. The tutor logs it like any other answer. The structured question (C1) stays the default way to ask. The page's own prediction replaces it only for the step it was made for.
7. **Craft.** Phone width first, light and dark themes, keyboard use, reduced motion. Use code fonts with ligatures off, so `<|` stays `<|`. Use the starter `assets/visual.html`: copy it and fill only the marked parts, so each page costs the content, not the scaffolding.

## Where it lives
Save the page in the module folder (`visuals/<name>.html`) with its data script. In `knowledge/` and the session log, record the step and the learner's pasted line, not the page itself. The adapter says how to show the page (a published page the learner can open on any device, an inline view, or a local file).
