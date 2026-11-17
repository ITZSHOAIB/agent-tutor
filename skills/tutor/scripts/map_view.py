"""Render a module's map with the learner's position as a standalone HTML page.

Works in any browser. Theme variables (`--background`, `--primary`, ...) are used when
the host page provides them, with fallbacks otherwise.

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

status = (f"Now on <b>{html.escape(current[0])}</b> ({current[1]}, {current[3]}) · node "
          f"<code>{html.escape(current[2])}</code>") if current else "Teaching hasn't started."
classes = "\n".join(f"  class {n} {s}" for n, s in state.items())
graph = re.sub(r"^\s*graph TD", "graph BT", block.rstrip(), count=1) + "\n" + classes + "\n"  # goal on top

page = f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}: map</title>
<style>
body{{margin:0;padding:16px 20px;font-family:var(--font-sans,system-ui,sans-serif);background:var(--background,#fff);color:var(--foreground,#171717)}}
h1{{font-size:15px;margin:0 0 4px}} .sub{{font-size:12.5px;color:var(--muted-foreground,#666);margin-bottom:10px}}
code{{font-family:var(--font-mono,monospace);font-size:12px}}
.legend{{display:flex;gap:14px;font-size:12px;color:var(--muted-foreground,#666);margin-top:8px;flex-wrap:wrap}}
.sw{{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:5px;vertical-align:-1px;border:1.5px solid}}
#map svg{{max-width:100%;height:auto}}
</style></head><body>
<h1>{html.escape(title)} · map {version}</h1>
<div class="sub">{status}</div>
<div id="map"></div>
<div class="legend" id="legend"></div>
<script type="module">
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
const css = (v, fb) => getComputedStyle(document.documentElement).getPropertyValue(v).trim() || fb;
const c = {{
  fg: css('--foreground', '#171717'), card: css('--card', '#fff'), border: css('--border', '#d4d4d4'),
  muted: css('--muted', '#f2f2f2'), mutedFg: css('--muted-foreground', '#737373'),
  primary: css('--primary', '#171717'), primaryFg: css('--primary-foreground', '#fafafa'),
  pass: css('--chart-2', '#16a34a')
}};
const styles = {{
  held: `fill:${{c.muted}},stroke:${{c.border}},color:${{c.mutedFg}}`,
  passed: `fill:${{c.card}},stroke:${{c.pass}},stroke-width:2.5px,color:${{c.fg}}`,
  current: `fill:${{c.primary}},stroke:${{c.primary}},stroke-width:3px,color:${{c.primaryFg}}`,
  upcoming: `fill:${{c.card}},stroke:${{c.border}},stroke-dasharray:5 4,color:${{c.fg}}`
}};
const defs = Object.entries(styles).map(([k, v]) => `  classDef ${{k}} ${{v}}`).join('\\n');
const graph = {json.dumps(graph)} + defs;
mermaid.initialize({{ startOnLoad: false, theme: 'base', themeVariables: {{
  fontFamily: css('--font-sans', 'system-ui'), lineColor: c.mutedFg, primaryTextColor: c.fg }} }});
const {{ svg }} = await mermaid.render('m', graph);
document.getElementById('map').innerHTML = svg;
const swatch = {{ held: [c.muted, c.border], passed: [c.card, c.pass], current: [c.primary, c.primary], upcoming: [c.card, c.border] }};
const words = {{ held: 'Known before', passed: 'Check passed', current: "You're here", upcoming: 'Coming up' }};
document.getElementById('legend').innerHTML = Object.keys(words).map(k =>
  `<span><span class="sw" style="background:${{swatch[k][0]}};border-color:${{swatch[k][1]}}"></span>${{words[k]}}</span>`).join('');
</script></body></html>"""

slug = re.sub(r"[^\w.-]", "-", pathlib.Path(notes_path).parent.name)
out = pathlib.Path(out_dir) / f"map-{slug}-{int(time.time())}.html"
out.write_text(page, encoding="utf-8")
print(out.name)
