# Plan: turning "teach me X" into a roadmap

A topic starts with a conversation, not a syllabus. The roadmap that comes out of it is the contract for every later session, so it's worth an hour.

## 1. Find out who is learning
Ask, a few at a time, in chat:
- **Why this topic, and what would "done" let them do?** Push for something they could demo or decide, not "understand X".
- **What does their world look like?** Job, projects, hobbies, the tools or materials they handle. Every module gets anchored in this world.
- **What do they already know, and how do they know it?** Claimed knowledge is checked later by probes; here it only sets the starting altitude.
- **Constraints:** time per session, how many sessions a week, devices (desk, phone), what they can do hands-on (run code, play the instrument, cook, read sources in the original language), any equipment or budget limits.
- **Their material:** a textbook, course notes, a syllabus, a past exam, a manual, a reading list? Ask every time; learners rarely offer it. Files go in `sources/` (see "Their sources" below).

Write the answers as a short profile at the top of `ROADMAP.md`. Don't quiz yet; that's what probes are for.

### Their sources
If the learner has material, read it before laying out phases, and index it in `sources/README.md`: an ID (`S1`, `S2`), what it is, and which sections the roadmap uses. For a long book, index the chapters and read only the ones a module needs.
- **Follow their material where it's sound.** Use its terms, its examples and its order when nothing argues against them; the learner will meet them in class or at work.
- **A course or exam sets the endpoint.** A past exam becomes the checkpoint's format, and practice problems copy its style (`practice.md`).
- **Check it like any other source.** When it's wrong or out of date, write the issue in the index's "Issues found" column and the roadmap's Unverified section, and teach the correct version where that section comes up, saying where the source differs. If an examiner marks by the source, say what to write in the exam and what's true.

### Profile and research
Rate each area of the topic stable or moving, mark high stakes, and have a worker build the source index before you draft anything (`grounding.md`, sections 1 and 2).

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
| Try | The one thing they will do or change to see it: a cell to run, a calculation, a source to read, a sentence to say, a move to practise, a scene to play with the tutor as the other side (`teach.md`, "Hands on") |

Decide the lab: `lab.ipynb` when the tries compute, `lab.md` for everything else. When the skill is used with another person (languages, negotiation, management, interviews, clinical or legal work), plan a role-play into most modules (`role-play.md`); the tutor is a real partner for it, not a stand-in. Mark modules that will take more than one session, and modules whose output is something built (they use the build variant in `session-loop.md`).

## 5. Check the facts
Every claim in the roadmap about a moving or high-stakes area is checked against the source index now, with the quote rule in `grounding.md`. What couldn't be supported goes in the roadmap's Unverified section.

## 6. Get an independent review
Hand the roadmap, the profile and the source index, and nothing else, to a separate worker (C5) playing a working expert in the field (a translator, a historian, a coach, an engineer). Ask it for: missing prerequisites, wrong order, things an expert would cut, stale facts, and whether each checkpoint really tests the phase. Apply what holds up; note what you rejected and why. Without delegation, the learner opens a fresh chat with only those two documents.

## 7. Set up the folder
Create the topic folder from the skill's scaffold (`scripts/new_topic.py`), fill `ROADMAP.md`, show the learner the phase overview, and agree on the first module. The first session starts with that module's probe.

## Changing the roadmap later
The roadmap moves when evidence says so: a probe shows a module is already known (skip it and say so in `PROGRESS.md`), a module keeps failing (split it), or the learner's goal changes (re-run steps 2–6 on what's left). Never delete history; strike through and note the date.
