"""One page that closes a module: what was mastered, what was repaired, how calibrated the learner was.

    python -I scripts/recap.py <topic> <module_dir>

Everything comes from the records, so nothing on the page is typed by hand:
  notes.md                   title, goal, map, Break it, Plug-back rule
  sessions/*-<N.M>*.md       questions (`### Q5 · check · node`) and answer lines
  knowledge/misconceptions   rows whose "Found in" cites this module (`1.1-Q4`)
Writes `<module_dir>/visuals/recap-<N.M>.html` (standalone, light and dark, phone first, in the look
shared by every page: page_style.py) and prints its path. Map nodes are marked passed when a check
tagged with that node was answered right; logs that tag questions some other way get the plain map.
"""
import datetime, html, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import page_style  # noqa: E402
from calibration import LEVELS, answers, describe, gap  # noqa: E402

E = html.escape


def section(notes, name):
    m = re.search(rf"^## {name}[^\n]*\n(.*?)(?=^## |\Z)", notes, re.S | re.M)
    text = m.group(1).strip() if m else ""
    return "" if text.startswith("_") else text


def questions(logs):
    """(id, role, node, verdict) per question, in order."""
    out = []
    for log in logs:
        parts = re.split(r"^#{3,4} (Q\d+\w*) · ([\w-]+) · (\S+).*$", log.read_text(encoding="utf-8"), flags=re.M)
        for i in range(1, len(parts), 4):
            ans = re.search(r"\*\*Answer:\*\*(.*)", parts[i + 3])
            verdict = "right" if ans and "✅" in ans.group(1) else "wrong" if ans and "❌" in ans.group(1) else "open"
            out.append((parts[i], parts[i + 1], parts[i + 2], verdict))
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
    """Bars: how often each confidence level was right. Dashed tick: what that level claims."""
    w, h, bar = 340, 160, 50
    out = [f'<svg viewBox="0 -14 {w} {h + 50}" role="img" aria-label="How often you were right at each confidence level">']
    for y in (0, 50, 100):
        yy = h - y * h / 100
        out.append(f'<line x1="34" x2="{w}" y1="{yy}" y2="{yy}" class="grid"/><text x="0" y="{yy + 4}" class="ax">{y}%</text>')
    for i, (name, band, claim) in enumerate(LEVELS):
        got = [r for l, r in rows if l == i]
        x, rate = 50 + i * 74, (100 * sum(got) / len(got) if got else None)
        tip = (f"{name} ({band}): right {sum(got)} of {len(got)}, {rate:.0f}%" if got else f"{name} ({band}): not used")
        out.append(f'<g class="col" tabindex="0" data-tip="{E(tip)}" style="--i:{i}"><rect x="{x - 8}" y="-14" width="{bar + 16}" height="{h + 50}" class="hit"/>')
        if got:
            top = h - rate * h / 100
            out.append(f'<rect x="{x}" y="{top}" width="{bar}" height="{h - top}" rx="4" class="bar {"over" if rate + 5 < claim else ""}"/>'
                       f'<text x="{x + bar / 2}" y="{top - 6}" class="val">{rate:.0f}%</text>')
        cy = h - claim * h / 100
        out.append(f'<line x1="{x - 5}" x2="{x + bar + 5}" y1="{cy}" y2="{cy}" class="claim"/>'
                   f'<text x="{x + bar / 2}" y="{h + 17}" class="lb">{E(name)}</text>'
                   f'<text x="{x + bar / 2}" y="{h + 32}" class="ax mid">{sum(got)}/{len(got)}</text></g>')
    return "".join(out) + "</svg>"


STYLE = """
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px;box-shadow:var(--shadow)}
.stat b{display:block;font:600 26px/1.15 var(--mono);font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.stat span{font-size:12.5px;color:var(--muted)}
.stat.good b{color:var(--good)} .stat.bad b{color:var(--bad)}
@media (max-width:600px){.stat:last-child:nth-child(odd){grid-column:1/-1}}
.cal{display:grid;grid-template-columns:minmax(0,340px) 1fr;gap:22px;align-items:center}
@media (max-width:600px){.cal{grid-template-columns:1fr}}
.chart{position:relative;padding-top:30px}
.chart svg{width:100%;height:auto;overflow:visible;display:block}
svg .grid{stroke:var(--line)} svg text{fill:var(--muted);font:11px var(--sans)} svg .mid,svg .lb,svg .val{text-anchor:middle}
svg .lb{fill:var(--fg);font-weight:500} svg .val{fill:var(--fg);font:600 11px var(--mono)}
svg .bar{fill:var(--accent);transform-box:fill-box;transform-origin:bottom;animation:up .9s var(--ease) both;animation-delay:calc(.25s + var(--i) * 90ms)}
svg .bar.over{fill:var(--bad)}
svg .val{animation:rise .5s var(--ease) both;animation-delay:calc(.7s + var(--i) * 90ms)}
svg .claim{stroke:var(--fg);stroke-width:2;stroke-dasharray:4 3}
svg .hit{fill:transparent} svg .col{cursor:default;outline:none} svg .hit{transition:fill .2s} svg .col:hover .hit,svg .col:focus .hit{fill:var(--accent-soft);fill-opacity:.55}
@keyframes up{from{transform:scaleY(0)}}
.tip{position:absolute;pointer-events:none;background:var(--fg);color:var(--bg);font:500 12px var(--sans);padding:6px 9px;border-radius:6px;
white-space:nowrap;transform:translate(-50%,-4px);opacity:0;transition:opacity .15s,transform .2s var(--ease)}
.tip.on{opacity:1;transform:translate(-50%,0)}
.big{font-size:18px;line-height:1.4;font-weight:500}
.mis{display:grid;gap:10px}
.m{border:1px solid var(--line);border-radius:8px;padding:12px 14px;display:grid;gap:6px;background:var(--bg)}
.m .old{color:var(--muted);text-decoration:line-through;text-decoration-color:var(--bad)}
.m .new::before{content:"→ ";color:var(--good);font-weight:600}
.quote{border-left:3px solid var(--accent);padding:2px 0 2px 14px;white-space:pre-wrap;max-width:65ch}
"""

SCRIPT = r"""
const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
document.querySelectorAll("[data-to]").forEach((el, i) => {
  const to = +el.dataset.to, of = el.dataset.of;
  if (calm || !to) return;
  const t0 = performance.now() + 150 + i * 80;
  const step = t => { const k = Math.min(1, Math.max(0, (t - t0) / 900)), e = 1 - Math.pow(1 - k, 3);
    el.textContent = Math.round(to * e) + (of ? "/" + of : ""); if (k < 1) requestAnimationFrame(step); };
  el.textContent = "0" + (of ? "/" + of : ""); requestAnimationFrame(step);
});
const chart = document.querySelector(".chart"), tip = document.querySelector(".tip");
chart && chart.querySelectorAll(".col").forEach(g => {
  const show = () => { const b = g.getBoundingClientRect(), c = chart.getBoundingClientRect();
    tip.textContent = g.dataset.tip; tip.style.left = (b.left - c.left + b.width / 2) + "px"; tip.style.top = "0px"; tip.classList.add("on"); };
  const hide = () => tip.classList.remove("on");
  g.addEventListener("pointerenter", show); g.addEventListener("pointerleave", hide);
  g.addEventListener("focus", show); g.addEventListener("blur", hide);
});
"""


def main():
    topic, module = (pathlib.Path(a) for a in sys.argv[1:3])
    sys.stdout.reconfigure(encoding="utf-8")
    mid = re.match(r"\d+\.\d+", module.name).group(0)
    notes = (module / "notes.md").read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", notes, re.M).group(1)
    goal = (re.search(r"^\*\*Goal:\*\*\s*(.+)$", notes, re.M) or [None, ""])[1]
    logs = sorted(p for p in (topic / "sessions").glob(f"*-{mid}*.md") if re.search(rf"-{re.escape(mid)}(-|\.md)", p.name))

    qs = questions(logs)
    preds = [v for _, r, _, v in qs if r == "predict"]
    checks = [v for _, r, _, v in qs if r == "check"]
    rated, unrated, _ = answers(topic, logs)
    miscs = misconceptions(topic, mid)
    fixed = sum(1 for m in miscs if m[5].lower().startswith("yes"))

    block = re.search(r"```mermaid\n(.*?)```", notes, re.S)
    graph, info = "", {}
    if block:
        labels = dict(re.findall(r"^\s*(\w+)\[\"(.+?)\"\]", block.group(1), re.M))
        state = {n: "held" if l.lower().startswith("held") else "upcoming" for n, l in labels.items()}
        for _, r, n, v in qs:
            if n in state and r == "check" and v == "right":
                state[n] = "passed"
        graph = re.sub(r"^\s*graph TD", "graph BT", block.group(1).rstrip(), count=1) + "\n"
        graph = re.sub(r'\["(\d+)\. ', r'["\1#46; ', graph)  # "1. …" would render as a markdown list
        graph += "".join(f"  class {n} {s}\n" for n, s in state.items())
        info = {n: {"label": re.sub(r"^\d+\.\s*", "", labels[n]), "state": s,
                    "qs": [[q, r, v] for q, r, nd, v in qs if nd == n]} for n, s in state.items()}

    def stat(label, n, of=None, tone=""):
        shown = f"{n}/{of}" if of is not None else str(n)
        attrs = f'data-to="{n}"' + (f' data-of="{of}"' if of is not None else "")
        return f'<div class="stat {tone}"><b {attrs}>{shown}</b><span>{label}</span></div>'

    stats = "".join([
        stat("Predictions right", preds.count("right"), len(preds)),
        stat("Checks right", checks.count("right"), len(checks), "good" if checks and "wrong" not in checks else ""),
        stat("Wrong models found", len(miscs)),
        stat("Repaired", fixed, len(miscs), "bad" if fixed < len(miscs) else ""),
        stat("Sessions", len(logs))])

    if rated:
        stated, right, g = gap(rated)
        tone = "good" if abs(g) < 5 else "bad"
        cal = (f'<p class="big">You said <b>{stated:.0f}%</b> on average and were right <b>{right:.0f}%</b>.</p>'
               f'<p><span class="chip {tone}">{E(describe(g))}</span></p>')
    else:
        cal = '<p class="big">No rated answers in this module.</p>'
    if unrated:
        cal += f'<p class="hint">{unrated} more answered without a confidence.</p>'

    mis = "".join(
        f'<div class="m"><div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap"><span class="chip">{E(m[0])}</span>'
        f'<span class="chip {"good" if m[5].lower().startswith("yes") else "bad"}">'
        f'{"repaired" if m[5].lower().startswith("yes") else "not yet: back in review"}</span></div>'
        f'<div class="old">{E(m[1])}</div><div class="new">{E(m[2])}</div></div>' for m in miscs
    ) or '<p class="hint">None found in this module.</p>'

    cards, i = [], 4
    for name, label in (("Break it", "Break it"), ("Plug-back rule", "Your rule for your own work")):
        text = section(notes, name)
        if text:
            short = text if len(text) <= 700 else text[:700].rsplit(" ", 1)[0] + " …"
            cards.append(f'<section class="card rise" style="--i:{i}"><h2>{label}</h2><p class="quote">{E(short)}</p></section>')
            i += 1

    body = f"""<main>
<header class="rise"><div class="eyebrow">Module {E(mid)} · closed</div><h1>{E(title)}</h1><p class="lede">{E(goal)}</p></header>
<div class="stats rise" style="--i:1">{stats}</div>
{page_style.MAP_CARD.format(i=2, heading="The map") if graph else ""}
<section class="card rise" style="--i:3"><h2>Calibration in this module</h2><div class="cal">
<div class="chart">{calib_svg(rated)}<div class="tip" role="status"></div></div>
<div style="display:grid;gap:10px">{cal}<p class="hint">Bars: how often you were right at each confidence. Dashed line: what that confidence claims. A bar well below its line, in red, means overconfident there.</p></div></div></section>
<section class="card rise" style="--i:3"><h2>Wrong models found</h2><div class="mis">{mis}</div></section>
{"".join(cards)}
<footer>Built from the topic records by recap.py on {datetime.date.today()}. Full text in {E(module.name)}/notes.md.</footer>
</main><style>{STYLE}</style>"""
    script = SCRIPT + (f"const graph = {json.dumps(graph)};\nconst NODES = {json.dumps(info, ensure_ascii=False)};\n"
                       + page_style.MAP_JS if graph else "")
    out = module / "visuals" / f"recap-{mid}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_style.doc(f"{mid} recap", body, script), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
