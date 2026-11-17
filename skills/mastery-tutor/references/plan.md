# Plan: turning "teach me X" into a roadmap

A topic starts with a conversation, not a syllabus. The roadmap that comes out of it is the contract for every later session, so it's worth an hour.

## 1. Find out who is learning
Ask, a few at a time, in chat:
- **Why this topic, and what would "done" let them do?** Push for something they could demo or decide, not "understand X".
- **What does their world look like?** Job, projects, hobbies, the tools or materials they handle. Every module gets anchored in this world.
- **What do they already know, and how do they know it?** Claimed knowledge is checked later by probes; here it only sets the starting altitude.
- **Constraints:** time per session, how many sessions a week, devices (desk, phone), what they can do hands-on (run code, play the instrument, cook, read sources in the original language), any equipment or budget limits.

Write the answers as a short profile at the top of `ROADMAP.md`. Don't quiz yet; that's what probes are for.

## 2. Pick an endpoint
One concrete thing the learner will be able to do or build at the end, in their own world. It decides what's in and what's out. If a module doesn't serve the endpoint, it's optional or gone.

## 3. Lay out phases from their world inward
Start at the layer the learner already touches and go one layer further from it per phase. Each phase gets:
- a one-line question it answers;
- 3–7 modules;
- a **checkpoint**: one bigger task on the learner's real work that needs the whole phase;
- a **practice session** before the checkpoint (`practice.md`).

Put any hard requirement (hardware, an account, an instrument, a dataset, a textbook) as a gate between phases, not inside a module.

## 4. Write each module as a row
| Column | What goes in it |
|---|---|
| Goal | A claim the learner will be able to defend, not a topic name ("why a recipe fails at altitude", "why Spanish says *espero que estés*", not "baking" or "the subjunctive") |
| Anchor | Something from the learner's own world where this already shows up |
| Try | The one thing they will do or change to see it: a cell to run, a calculation, a source to read, a sentence to say, a move to practise (`teach.md`, "Hands on") |

Decide the lab: `lab.ipynb` when the tries compute, `lab.md` for everything else. Mark modules that will take more than one session, and modules whose output is something built (they use the build variant in `session-loop.md`).

## 5. Check the facts
Anything in the roadmap that is about current products, versions, prices or specs gets verified now (C4). Note what couldn't be verified.

## 6. Get an independent review
Hand the roadmap and the profile, and nothing else, to a separate worker (C5) playing a working expert in the field (a translator, a historian, a coach, an engineer). Ask it for: missing prerequisites, wrong order, things an expert would cut, stale facts, and whether each checkpoint really tests the phase. Apply what holds up; note what you rejected and why. Without delegation, the learner opens a fresh chat with only those two documents.

## 7. Set up the folder
Create the topic folder from the skill's scaffold (`scripts/new_topic.py`), fill `ROADMAP.md`, show the learner the phase overview, and agree on the first module. The first session starts with that module's probe.

## Changing the roadmap later
The roadmap moves when evidence says so: a probe shows a module is already known (skip it and say so in `PROGRESS.md`), a module keeps failing (split it), or the learner's goal changes (re-run steps 2–6 on what's left). Never delete history; strike through and note the date.
