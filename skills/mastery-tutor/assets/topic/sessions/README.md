# Session logs

One file per session: `YYYY-MM-DD-<module>.md` (practice: `YYYY-MM-DD-practice-phase-N.md`). These logs are the evidence; `knowledge/` is the map of what was taught, and every claim there points back here.

Each log holds:
- **Probe result:** per thread, the highest level answered well, the lowest missed, wrong ideas found, and where teaching starts.
- **Questions**, in order, each headed `### Q<n> · <role> · <node>`:
  - `Q<n>` numbers through the whole module, across sessions. Cite it elsewhere as `<module>-Q<n>`; practice as `P<phase>-Q<n>`.
  - Role: warm-up · probe · predict · check · practice · explain-back.
  - Node: the map node slug, or `—` outside the map.
  - Then: the question; the answer key and why (written **before** asking); the belief behind each wrong option; the learner's answer, confidence, verdict and reasoning.
  - The answer line reads `**Answer:** B · Fairly sure (~75%) · ❌ Wrong. <reasoning>` (✅ for right, `_pending_` until answered); the map view and `scripts/calibration.py` read it. One answer line per question: a question asked again gets its own heading (`### Q6b · predict · <node>`).
- **Parking lot:** side questions, and where they were answered.
- **Uncertain facts:** anything not fully verified, and how it was resolved.
- **Map changes:** each new map version and why.
