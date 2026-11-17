"""One page that closes a module: what was mastered, what was repaired, how calibrated the learner was.

    python -I scripts/recap.py <topic> <module_dir>

Everything comes from the records, so nothing on the page is typed by hand:
  notes.md                   title, goal, map, Break it, Plug-back rule
  sessions/*-<N.M>*.md       questions (`### Q5 · check · node`) and answer lines
  knowledge/misconceptions   rows whose "Found in" cites this module (`1.1-Q4`)
Writes `<module_dir>/visuals/recap-<N.M>.html` (standalone, light and dark) and prints its path.
Map nodes are marked passed when a check tagged with that node was answered right; logs that tag
questions some other way get the map without marks.
"""
import datetime, html, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from calibration import LEVELS, answers, describe, gap  # noqa: E402

E = html.escape


def section(notes, name):
    m = re.search(rf"^## {name}[^\n]*\n(.*?)(?=^## |\Z)", notes, re.S | re.M)
    text = m.group(1).strip() if m else ""
    return "" if text.startswith("_") else text


def questions(logs):
    """(role, node, verdict) per question, in order."""
    out = []
    for log in logs:
        parts = re.split(r"^#{3,4} Q\d+\w* · ([\w-]+) · (\S+).*$", log.read_text(encoding="utf-8"), flags=re.M)
        for i in range(1, len(parts), 3):
            ans = re.search(r"\*\*Answer:\*\*(.*)", parts[i + 2])
            verdict = "right" if ans and "✅" in ans.group(1) else "wrong" if ans and "❌" in ans.group(1) else "open"
            out.append((parts[i], parts[i + 1], verdict))
    return out


def misconceptions(topic, mid):
    f = topic / "knowledge" / "misconceptions.md"
    rows = []
    for line in (f.read_text(encoding="utf-8").splitlines() if f.exists() else []):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 6 and re.match(r"M\d+$", cells[0]) and f"{mid}-Q" in cells[3]:
            rows.append(cells)
    return rows


def calib_svg(rows):
    """Bars: how often each confidence level was right; a tick: what that level claims."""
    w, h, bar = 320, 150, 46
    parts = [f'<svg viewBox="0 -12 {w} {h + 46}" role="img" aria-label="Hit rate per confidence level">']
    for y in (0, 50, 100):
        yy = h - y * h / 100
        parts.append(f'<line x1="28" x2="{w}" y1="{yy}" y2="{yy}" class="grid"/><text x="0" y="{yy + 4}" class="ax">{y}%</text>')
    for i, (name, _, claim) in enumerate(LEVELS):
        got = [r for l, r in rows if l == i]
        x = 44 + i * 70
        if got:
            rate = 100 * sum(got) / len(got)
            parts.append(f'<rect x="{x}" y="{h - rate * h / 100}" width="{bar}" height="{rate * h / 100}" class="bar"/>')
        parts.append(f'<line x1="{x - 4}" x2="{x + bar + 4}" y1="{h - claim * h / 100}" y2="{h - claim * h / 100}" class="claim"/>')
        parts.append(f'<text x="{x + bar / 2}" y="{h + 15}" class="lb">{E(name)}</text>'
                     f'<text x="{x + bar / 2}" y="{h + 29}" class="ax" text-anchor="middle">{sum(got)}/{len(got)}</text>')
    return "".join(parts) + "</svg>"


def main():
    topic, module = (pathlib.Path(a) for a in sys.argv[1:3])
    sys.stdout.reconfigure(encoding="utf-8")
    mid = re.match(r"\d+\.\d+", module.name).group(0)
    notes = (module / "notes.md").read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", notes, re.M).group(1)
    goal = (re.search(r"^\*\*Goal:\*\*\s*(.+)$", notes, re.M) or [None, ""])[1]
    logs = sorted(p for p in (topic / "sessions").glob(f"*-{mid}*.md") if re.search(rf"-{re.escape(mid)}(-|\.md)", p.name))

    qs = questions(logs)
    preds = [v for r, _, v in qs if r == "predict"]
    checks = [v for r, _, v in qs if r == "check"]
    rated, unrated, _ = answers(topic, logs)
    miscs = misconceptions(topic, mid)

    block = re.search(r"```mermaid\n(.*?)```", notes, re.S)
    graph, passed = "", set()
    if block:
        nodes = set(re.findall(r"^\s*(\w+)\[", block.group(1), re.M))
        passed = {n for r, n, v in qs if r == "check" and v == "right" and n in nodes}
        held = {n for n in nodes if re.search(rf"^\s*{n}\[\"Held", block.group(1), re.M)}
        graph = re.sub(r"^\s*graph TD", "graph BT", block.group(1).rstrip(), count=1) + "\n"
        graph = re.sub(r'\["(\d+)\. ', r'["\1#46; ', graph)  # "1. …" would render as a markdown list
        graph += "".join(f"  class {n} passed\n" for n in passed) + "".join(f"  class {n} held\n" for n in held - passed)

    legend = '<div class="leg">Solid border: a check on that step passed.</div>' if passed else ""
    stats = [("Predictions right", f"{preds.count('right')}/{len(preds)}"),
             ("Checks right", f"{checks.count('right')}/{len(checks)}"),
             ("Misconceptions found", str(len(miscs))),
             ("Repaired", f"{sum(1 for m in miscs if m[5].lower().startswith('yes'))}/{len(miscs)}"),
             ("Sessions", str(len(logs)))]
    if rated:
        stated, right, g = gap(rated)
        cal_line = f"You said {stated:.0f}% on average and were right {right:.0f}%: {describe(g)}."
    else:
        cal_line = "No rated answers in this module."
    if unrated:
        cal_line += f" {unrated} more answered without a confidence."

    def words(name, label):
        text = section(notes, name)
        if not text:
            return ""
        short = text if len(text) <= 700 else text[:700].rsplit(" ", 1)[0] + " …"
        return f'<section><h2>{label}</h2><p class="words">{E(short)}</p></section>'

    misc_html = "".join(
        f'<li><span class="id">{E(m[0])}</span><s>{E(m[1])}</s><span>{E(m[2])}</span>'
        f'<em>{"repaired" if m[5].lower().startswith("yes") else "not yet repaired: comes back in review"}</em></li>'
        for m in miscs) or "<li class='none'>None found in this module.</li>"

    page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(mid)} recap</title>
<style>
:root{{--bg:#f7f6f2;--card:#fff;--fg:#1d1c1a;--mut:#6b6860;--line:#dedbd2;--acc:#2f6f5e;--warn:#a4532b;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#141413;--card:#1d1d1b;--fg:#ecebe6;--mut:#a09d94;--line:#34332f;--acc:#6fbfa6;--warn:#e08a5c;color-scheme:dark}}}}
:root[data-theme=dark]{{--bg:#141413;--card:#1d1d1b;--fg:#ecebe6;--mut:#a09d94;--line:#34332f;--acc:#6fbfa6;--warn:#e08a5c;color-scheme:dark}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 ui-sans-serif,system-ui,sans-serif;padding-block:28px 40px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
main{{max-width:760px;margin:0 auto;display:grid;gap:22px}}
.k{{font:600 11px/1 ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--acc)}}
h1{{font-size:clamp(22px,4vw,30px);line-height:1.2;margin:6px 0 8px;text-wrap:balance}} .goal{{color:var(--mut);margin:0;max-width:65ch}}
h2{{font-size:13px;font-weight:600;color:var(--mut);margin:0 0 10px;letter-spacing:.02em}}
section{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;min-width:0}}
.stats{{display:flex;flex-wrap:wrap;gap:1px;background:var(--line);border:1px solid var(--line);border-radius:10px;overflow:hidden}}
.stats div{{flex:1 1 110px;background:var(--card);padding:12px 14px}} .stats b{{display:block;font:600 22px/1.2 ui-monospace,monospace;font-variant-numeric:tabular-nums}} .stats span{{font-size:12px;color:var(--mut)}}
#map{{overflow-x:auto}} #map svg{{max-width:100%;height:auto}}
ul{{list-style:none;margin:0;padding:0;display:grid;gap:12px}} li{{display:grid;gap:2px}} li s{{color:var(--mut)}} li em{{font-size:12px;font-style:normal;color:var(--warn)}}
.id{{font:600 11px ui-monospace,monospace;color:var(--mut)}} .none{{color:var(--mut)}}
.words{{white-space:pre-wrap;margin:0;max-width:65ch}}
svg .grid{{stroke:var(--line)}} svg .bar{{fill:var(--acc);opacity:.85}} svg .claim{{stroke:var(--fg);stroke-width:2;stroke-dasharray:4 3}}
svg text{{fill:var(--mut);font:11px ui-sans-serif,system-ui,sans-serif}} svg .lb{{text-anchor:middle;fill:var(--fg)}}
.cal{{display:grid;grid-template-columns:minmax(0,320px) 1fr;gap:18px;align-items:center}} @media (max-width:560px){{.cal{{grid-template-columns:1fr}}}}
.leg{{font-size:12px;color:var(--mut)}} footer{{font-size:12px;color:var(--mut);text-align:center}}
</style></head><body><main>
<header><div class="k">Module {E(mid)} · closed</div><h1>{E(title)}</h1><p class="goal">{E(goal)}</p></header>
<div class="stats">{"".join(f"<div><b>{v}</b><span>{k}</span></div>" for k, v in stats)}</div>
{f'<section><h2>The map</h2><div id="map"></div>{legend}</section>' if graph else ""}
<section><h2>Calibration in this module</h2><div class="cal">{calib_svg(rated)}<div><p style="margin:0 0 8px">{E(cal_line)}</p>
<div class="leg">Bars: how often you were right at each confidence. Dashed line: what that confidence claims. Bars below the line mean overconfident.</div></div></div></section>
<section><h2>Wrong models found</h2><ul>{misc_html}</ul></section>
{words("Break it", "Break it")}
{words("Plug-back rule", "Your rule for your own work")}
<footer>Built from the topic records by recap.py on {datetime.date.today()}. Full text in {E(module.name)}/notes.md.</footer>
</main>
<script type="module">
const graph = {json.dumps(graph)};
if (graph) {{
  const {{ default: mermaid }} = await import("https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs");
  const v = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const defs = `\\n  classDef default fill:${{v('--card')}},stroke:${{v('--line')}},color:${{v('--fg')}}` +
    `\\n  classDef passed fill:${{v('--card')}},stroke:${{v('--acc')}},stroke-width:2.5px,color:${{v('--fg')}}` +
    `\\n  classDef held fill:${{v('--bg')}},stroke:${{v('--line')}},color:${{v('--mut')}}`;
  mermaid.initialize({{ startOnLoad: false, theme: "base", themeVariables: {{ lineColor: v('--mut'), fontFamily: "ui-sans-serif,system-ui" }} }});
  const {{ svg }} = await mermaid.render("m", graph + defs);
  document.getElementById("map").innerHTML = svg;
}}
</script></body></html>"""
    out = module / "visuals" / f"recap-{mid}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
