"""Shared look for the pages the scripts write (map_view.py, recap.py): the same tokens, type and
motion as assets/visual.html, so every page a learner sees belongs to one family.

doc(title, body, script) returns a standalone HTML document. MAP_JS renders a mermaid map whose
nodes open a panel listing that node's questions; it expects `graph` (mermaid text) and `NODES`
({node: {label, state, qs: [[id, role, verdict]]}}) defined before it.
"""
import html

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" '
         'href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700'
         '&family=JetBrains+Mono:wght@400;500&display=swap">')

LIGHT = ("--bg:#f5f6f7;--surface:#fff;--fg:#14181d;--muted:#5d6670;--faint:#8b939c;--line:#dfe3e7;--line-strong:#c3c9cf;"
         "--accent:#1d6670;--accent-soft:#e1eff0;--good:#2c7a4b;--good-soft:#e3f1e8;--bad:#b2452a;--bad-soft:#f7e6e0;"
         "--shadow:0 1px 2px rgba(20,40,50,.05),0 6px 24px -12px rgba(20,60,70,.18)")
DARK = ("--bg:#101418;--surface:#171c21;--fg:#e5e9ec;--muted:#9aa4ad;--faint:#6c7680;--line:#262d34;--line-strong:#37414a;"
        "--accent:#6cc0c9;--accent-soft:#16303a;--good:#6cc895;--good-soft:#15301f;--bad:#ec8a6c;--bad-soft:#3a1f17;"
        "--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 28px -14px rgba(0,0,0,.6);color-scheme:dark")

CSS = f"""
:root{{{LIGHT};--sans:"Instrument Sans",ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
--mono:"JetBrains Mono",ui-monospace,"Cascadia Mono",Consolas,monospace;--r:10px;--ease:cubic-bezier(.2,.8,.2,1);color-scheme:light}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{{DARK}}}}}
:root[data-theme=dark]{{{DARK}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 var(--sans);-webkit-font-smoothing:antialiased}}
main{{max-width:780px;margin:0 auto;display:grid;gap:20px;padding-block:32px 64px;
padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
h1,h2{{margin:0;text-wrap:balance}}
h1{{font-size:clamp(26px,5.5vw,38px);line-height:1.1;letter-spacing:-.02em;font-weight:700}}
h2{{font-size:13px;font-weight:600;color:var(--muted);letter-spacing:.02em}}
p{{margin:0;max-width:65ch}}
code,.mono,.num,.eyebrow{{font-variant-ligatures:none;font-feature-settings:"liga" 0,"calt" 0}}
.eyebrow{{font:500 12px var(--mono);color:var(--accent);letter-spacing:.06em;text-transform:uppercase}}
.lede{{color:var(--muted);margin-top:8px}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:18px 20px;display:grid;gap:12px;min-width:0;box-shadow:var(--shadow)}}
.hint{{font-size:13px;color:var(--muted)}}
.chip{{display:inline-flex;align-items:center;gap:6px;font:500 12px var(--mono);padding:3px 8px;border-radius:999px;background:var(--bg);color:var(--muted);border:1px solid var(--line)}}
.chip.good{{background:var(--good-soft);color:var(--good);border-color:transparent}}
.chip.bad{{background:var(--bad-soft);color:var(--bad);border-color:transparent}}
.chip.acc{{background:var(--accent-soft);color:var(--accent);border-color:transparent}}
:focus-visible{{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}}
.rise{{animation:rise .6s var(--ease) both;animation-delay:calc(var(--i,0) * 70ms)}}
@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}}}
.legend{{display:flex;flex-wrap:wrap;gap:8px 16px;font-size:12.5px;color:var(--muted)}}
.legend i{{display:inline-block;width:12px;height:12px;border-radius:4px;margin-right:6px;vertical-align:-2px;border:2px solid}}
#map{{overflow-x:auto;min-height:120px}} #map svg{{max-width:100%;height:auto;display:block;margin:0 auto}}
#map .node{{cursor:pointer;transition:opacity .25s,filter .25s}}
#map .node:hover,#map .node:focus{{filter:drop-shadow(0 4px 10px rgba(29,102,112,.25))}}
#map .node:focus{{outline:none}} #map .node:focus rect{{stroke-width:3px!important}}
#map.dim .node:not(.sel){{opacity:.45}}
#map .node.current rect{{animation:pulse 2.2s ease-in-out infinite}}
@keyframes pulse{{50%{{stroke-width:6px;stroke-opacity:.55}}}}
#map .node{{animation:rise .5s var(--ease) both;animation-delay:calc(var(--n,0) * 60ms)}}
.panel{{display:grid;grid-template-rows:0fr;transition:grid-template-rows .35s var(--ease)}}
.panel.open{{grid-template-rows:1fr}} .panel>div{{overflow:hidden}}
.panel .inner{{border-top:1px solid var(--line);margin-top:4px;padding-top:12px;display:grid;gap:8px}}
.qrow{{display:flex;flex-wrap:wrap;gap:6px;align-items:center}}
.sk{{min-height:140px;border-radius:8px;background:linear-gradient(90deg,var(--bg),var(--line),var(--bg));background-size:200% 100%;animation:sk 1.4s linear infinite}}
@keyframes sk{{to{{background-position:-200% 0}}}}
footer{{font-size:12.5px;color:var(--muted);text-align:center}}
@media (prefers-reduced-motion:reduce){{*,*::before,*::after{{animation:none!important;transition:none!important}}}}
"""

MAP_JS = r"""
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const STYLE = {
  held: () => `fill:${css('--bg')},stroke:${css('--line-strong')},color:${css('--muted')}`,
  passed: () => `fill:${css('--good-soft')},stroke:${css('--good')},stroke-width:2px,color:${css('--fg')}`,
  current: () => `fill:${css('--accent')},stroke:${css('--accent')},stroke-width:3px,color:${css('--surface')}`,
  upcoming: () => `fill:${css('--surface')},stroke:${css('--line-strong')},stroke-dasharray:5 4,color:${css('--fg')}`,
};
const WORD = { held: "Known before", passed: "Check passed", current: "You're here", upcoming: "Coming up" };
const VERDICT = { right: ["good", "right"], wrong: ["bad", "wrong"], open: ["", "open"] };
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
async function drawMap() {
  const box = document.getElementById("map");
  box.innerHTML = '<div class="sk"></div>';
  let mermaid;
  try { mermaid = (await import("https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs")).default; }
  catch { box.innerHTML = '<pre class="hint" style="white-space:pre-wrap">' + esc(graph) + "</pre>"; return; }
  const defs = Object.entries(STYLE).map(([k, f]) => `  classDef ${k} ${f()}`).join("\n");
  mermaid.initialize({ startOnLoad: false, theme: "base", flowchart: { curve: "basis", padding: 12, wrappingWidth: innerWidth < 560 ? 130 : 200, nodeSpacing: innerWidth < 560 ? 16 : 40, rankSpacing: 34 },
    themeVariables: { fontSize: innerWidth < 560 ? "15px" : "16px", fontFamily: css("--sans"), lineColor: css("--line-strong"), primaryTextColor: css("--fg") } });
  const { svg } = await mermaid.render("m" + Date.now(), graph + "\n" + defs);
  box.innerHTML = svg;
  const panel = document.getElementById("panel");
  [...box.querySelectorAll(".node")].forEach((g, i) => {
    const id = (g.id.match(/flowchart-(.+)-\d+$/) || [])[1], n = NODES[id];
    if (!n) return;
    g.style.setProperty("--n", i);
    if (n.state === "current") g.classList.add("current");
    g.setAttribute("tabindex", "0"); g.setAttribute("role", "button");
    g.setAttribute("aria-label", `${n.label}: ${WORD[n.state]}`);
    const open = () => {
      const was = g.classList.contains("sel");
      box.querySelectorAll(".node.sel").forEach(x => x.classList.remove("sel"));
      box.classList.toggle("dim", !was); panel.classList.toggle("open", !was);
      if (was) return;
      g.classList.add("sel");
      const qs = n.qs.length ? n.qs.map(([q, role, v]) =>
        `<div class="qrow"><span class="chip">${esc(q)}</span><span class="hint">${esc(role)}</span><span class="chip ${VERDICT[v][0]}">${VERDICT[v][1]}</span></div>`).join("")
        : '<p class="hint">No questions tagged with this step yet.</p>';
      panel.querySelector(".inner").innerHTML = `<div class="qrow"><b>${esc(n.label)}</b><span class="chip acc">${WORD[n.state]}</span></div>${qs}`;
    };
    g.addEventListener("click", open);
    g.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } });
  });
}
drawMap();
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", drawMap);
"""

LEGEND = ('<div class="legend"><span><i style="background:var(--bg);border-color:var(--line-strong)"></i>Known before</span>'
          '<span><i style="background:var(--good-soft);border-color:var(--good)"></i>Check passed</span>'
          '<span><i style="background:var(--accent);border-color:var(--accent)"></i>You\'re here</span>'
          '<span><i style="background:var(--surface);border-color:var(--line-strong);border-style:dashed"></i>Coming up</span></div>')

MAP_CARD = ('<section class="card rise" style="--i:{i}"><h2>{heading}</h2><div id="map"></div>' + LEGEND +
            '<p class="hint">Tap a step to see its questions.</p><div class="panel" id="panel"><div><div class="inner"></div></div></div></section>')


def doc(title, body, script=""):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            f"<title>{html.escape(title)}</title>{FONTS}<style>{CSS}</style></head><body>{body}"
            + (f'<script type="module">{script}</script>' if script else "") + "</body></html>\n")
