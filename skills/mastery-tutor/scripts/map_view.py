"""Render a module's map with the learner's position as a standalone HTML page.

Works in any browser, light and dark, phone first, in the look shared by every page
(page_style.py). Tap a step to see the questions asked on it.

Reads the mermaid map from the module's notes.md and the question headings
(`### Q5 · predict · node_slug`) from its session logs. Nothing is typed by hand,
so the picture always matches the records.

    python -I scripts/map_view.py <notes.md> <out_dir> <session-log.md> [more logs...]

Node states:
  held      label starts with "Held:" (known before the module)
  passed    has a check answered right
  current   node of the most recent tagged question
  upcoming  everything else
"""
import html, json, pathlib, re, sys, time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import page_style  # noqa: E402

notes_path, out_dir, *logs = sys.argv[1:]
notes = pathlib.Path(notes_path).read_text(encoding="utf-8")

block = re.search(r"```mermaid\n(.*?)```", notes, re.S).group(1)
title = re.search(r"^# (.+)$", notes, re.M).group(1)
version = (re.search(r"## Map \((v\d+)", notes) or [None, "v?"])[1]
nodes = dict(re.findall(r"^\s*(\w+)\[\"(.+?)\"\]", block, re.M))

questions = []  # (id, role, node, verdict)
for log in logs:
    text = pathlib.Path(log).read_text(encoding="utf-8")
    parts = re.split(r"^#{3,4} (Q\d+) · ([\w-]+) · (\S+).*$", text, flags=re.M)
    for i in range(1, len(parts), 4):
        qid, role, node, body = parts[i], parts[i + 1], parts[i + 2], parts[i + 3]
        ans = re.search(r"\*\*Answer:\*\*(.*)", body)
        verdict = "pending" if not ans or "pending" in ans.group(1) else ("right" if "✅" in ans.group(1) else "wrong")
        questions.append((qid, role, node, verdict))

state = {n: ("held" if label.lower().startswith("held") else "upcoming") for n, label in nodes.items()}
for qid, role, node, verdict in questions:
    if node in state and role == "check" and verdict == "right":
        state[node] = "passed"
tagged = [q for q in questions if q[2] in nodes]
current = tagged[-1] if tagged else None
if current:
    state[current[2]] = "current"

passed_n = sum(1 for s in state.values() if s in ("passed", "held"))
status = (f"Now on <b>{html.escape(current[0])}</b> · {html.escape(current[1])} · {current[3]}") if current else "Teaching hasn't started."
classes = "\n".join(f"  class {n} {s}" for n, s in state.items())
graph = re.sub(r"^\s*graph TD", "graph BT", block.rstrip(), count=1) + "\n" + classes + "\n"  # goal on top
graph = re.sub(r'\["(\d+)\. ', r'["\1#46; ', graph)  # "1. …" would render as a markdown list
info = {n: {"label": re.sub(r"^\d+\.\s*", "", nodes[n]), "state": s,
            "qs": [[q, r, {"right": "right", "wrong": "wrong"}.get(v, "open")] for q, r, nd, v in questions if nd == n]}
        for n, s in state.items()}
pct = round(100 * passed_n / len(state)) if state else 0

body = f"""<main>
<header class="rise"><div class="eyebrow">Module map · {version}</div><h1>{html.escape(title)}</h1>
<p class="lede">{status}</p></header>
<section class="card rise" style="--i:1"><div style="display:flex;justify-content:space-between;align-items:baseline;gap:12px">
<h2>Progress</h2><span class="num mono" style="font-size:14px">{passed_n} of {len(state)} steps</span></div>
<div style="height:8px;border-radius:99px;background:var(--bg);overflow:hidden"><div class="bar" style="--w:{pct}%"></div></div></section>
{page_style.MAP_CARD.format(i=2, heading="The path to the goal")}
<footer class="rise" style="--i:3">Drawn from notes.md and the session logs by map_view.py. Nothing typed by hand.</footer>
</main>
<style>.bar{{height:100%;width:var(--w);background:linear-gradient(90deg,var(--accent),var(--good));border-radius:99px;animation:grow 1s var(--ease) .2s both}}
@keyframes grow{{from{{width:0}}}}</style>"""
script = f"const graph = {json.dumps(graph)};\nconst NODES = {json.dumps(info, ensure_ascii=False)};\n{page_style.MAP_JS}"
page = page_style.doc(f"{title}: map", body, script)

slug = re.sub(r"[^\w.-]", "-", pathlib.Path(notes_path).parent.name)
out = pathlib.Path(out_dir) / f"map-{slug}-{int(time.time())}.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(page, encoding="utf-8")
print(out.name)
