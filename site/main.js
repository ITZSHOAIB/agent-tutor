/*
 * mastery-tutor home. The HTML is written in its finished state; scripts add motion on top, so
 * reduced motion and no script both leave a complete page. Two kinds of motion: scenes that follow
 * the reader's scroll (the loop and the map), and short loops that play while a figure is on screen
 * (the question, the calibration chart, the subjects). The pause button stops the loops.
 */
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const root = document.documentElement;
const reduced = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
const paused = () => root.hasAttribute("data-paused");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/* Calls fn(true/false) as el enters and leaves the screen. */
function onView(el, fn, threshold = 0.35) {
  new IntersectionObserver(([e]) => fn(e.isIntersecting), { threshold }).observe(el);
}

/* Things that animate once when first seen. */
function reveals() {
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) { e.target.classList.add("seen"); io.unobserve(e.target); }
  }, { threshold: 0.3 });
  for (const el of $$("h2 em, .forget, .chat")) io.observe(el);
}

/* ---------- header controls ---------- */
function controls() {
  const pause = $("#pause");
  const sync = () => {
    pause.setAttribute("aria-pressed", String(paused()));
    pause.title = paused() ? "Play animations" : "Pause animations";
  };
  sync();
  pause.addEventListener("click", () => {
    root.toggleAttribute("data-paused", !paused());
    try { localStorage.setItem("mt-paused", paused() ? "1" : "0"); } catch {}
    sync();
    dispatchEvent(new Event("mt-pause"));
  });

  $("#theme").addEventListener("click", (ev) => {
    const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    const next = dark ? "light" : "dark";
    const apply = () => {
      root.dataset.theme = next;
      try { localStorage.setItem("mt-theme", next); } catch {}
      // the demo pages read the theme from this page when they load
      for (const f of $$("iframe[src]")) f.contentWindow?.location.reload();
    };
    if (!document.startViewTransition || reduced()) return apply();
    const r = ev.currentTarget.getBoundingClientRect();
    root.style.setProperty("--vx", `${r.left + r.width / 2}px`);
    root.style.setProperty("--vy", `${r.top + r.height / 2}px`);
    document.startViewTransition(apply);
  });

  for (const box of $$("[data-copy]")) {
    const btn = $(".copy", box);
    const label = $("span", btn), use = $("use", btn);
    btn.addEventListener("click", async () => {
      try { await navigator.clipboard.writeText(box.dataset.copy); label.textContent = "Copied"; }
      catch { getSelection().selectAllChildren($("code", box)); label.textContent = "Selected"; }
      use.setAttribute("href", "#i-check");
      btn.classList.add("done");
      setTimeout(() => { label.textContent = "Copy"; use.setAttribute("href", "#i-copy"); btn.classList.remove("done"); }, 1600);
    });
  }
}

/* ---------- the question ---------- */
function question() {
  const q = $("#q");
  const opts = $$(".opt", q);
  const track = $(".conf-track", q);
  const confs = $$("[data-conf]", q);
  const lock = $("#q-lock");
  const hint = $("#q-hint");
  const gap = $("#q-gap");
  const badge = $("#q-badge");
  const why = $("#q-why");
  const log = $("#q-log");
  const RIGHT = "B";
  const state = { opt: null, conf: null, locked: false };
  for (const o of opts) $("b", o).insertAdjacentHTML("afterbegin", `<span class="letter">${o.dataset.opt}</span>`);

  const setGap = (word) => {
    const old = $("span:not(.out)", gap);
    if (old && old.textContent === word) return;
    old?.classList.add("out");
    setTimeout(() => old?.remove(), 320);
    gap.insertAdjacentHTML("beforeend", `<span>${word}</span>`);
  };
  const sync = () => {
    for (const o of opts) { o.setAttribute("aria-checked", String(o.dataset.opt === state.opt)); o.disabled = state.locked; }
    for (const c of confs) { c.setAttribute("aria-checked", String(c.dataset.conf === state.conf)); c.disabled = state.locked; }
    lock.disabled = state.locked || !state.opt || !state.conf;
    $("#q-verdict").inert = !state.locked;
    hint.textContent = state.locked ? "" : !state.opt ? "Pick an answer and how sure you are."
      : !state.conf ? "Now, how sure are you?" : "Locked answers can't change.";
  };
  const choose = (opt) => {
    if (state.locked) return;
    state.opt = opt;
    setGap($("b", opts.find((o) => o.dataset.opt === opt)).lastChild.textContent.trim());
    sync();
  };
  const rate = (conf) => {
    if (state.locked) return;
    state.conf = conf;
    track.style.setProperty("--k", confs.findIndex((c) => c.dataset.conf === conf));
    track.setAttribute("data-set", "");
    sync();
  };
  const commit = () => {
    if (!state.opt || !state.conf) return;
    state.locked = true;
    const right = state.opt === RIGHT;
    const sure = state.conf === "Certain" || state.conf === "Fairly sure";
    for (const o of opts) {
      o.classList.toggle("is-right", o.dataset.opt === RIGHT);
      o.classList.toggle("is-wrong", o.dataset.opt === state.opt && !right);
    }
    gap.className = `gap ${right ? "right" : "wrong"}`;
    badge.textContent = `${right ? "Right" : "Wrong"} · ${state.conf}`;
    badge.className = `v-badge ${right ? "" : "bad"}`;
    const belief = $("small", opts.find((o) => o.dataset.opt === state.opt)).textContent;
    why.innerHTML = right
      ? `<b>B, <span lang="es">estés</span>.</b> A wish about someone else isn't stated as fact, so the next verb leaves the present. Next: does it still change after <i lang="es">sé que</i>?`
      : `<b>Answer: B, <span lang="es">estés</span>.</b> You went with “${belief}” That's the model to repair: a wish about someone else isn't stated as fact, so the next verb leaves the present.`;
    log.textContent = right
      ? (sure ? "Logged right and sure: spaced out in review." : "Logged right but unsure, so it comes back soon.")
      : (sure ? "Logged confident and wrong, the most useful find: named, repaired, retested later." : "Logged wrong: repaired, then back in review.");
    q.setAttribute("data-locked", "");
    sync();
  };
  const reset = () => {
    Object.assign(state, { opt: null, conf: null, locked: false });
    q.removeAttribute("data-locked");
    for (const o of opts) o.classList.remove("is-right", "is-wrong");
    track.removeAttribute("data-set");
    gap.className = "gap";
    setGap(" ");
    sync();
  };

  // the reader takes over at their first touch or key press inside the card
  let run = 0;
  // a card the demo left locked opens again for the reader
  const takeOver = (e) => {
    if (q.hasAttribute("data-user")) return;
    q.setAttribute("data-user", "");
    hint.setAttribute("aria-live", "polite"); $("#q-verdict").setAttribute("aria-live", "polite");
    run++;
    if (!state.locked) return;
    reset();
    if (e.type === "focusin") opts[0].focus();
  };
  q.addEventListener("pointerdown", takeOver, true);
  q.addEventListener("keydown", takeOver, true);
  q.addEventListener("focusin", takeOver);
  for (const o of opts) o.addEventListener("click", () => choose(o.dataset.opt));
  for (const c of confs) c.addEventListener("click", () => rate(c.dataset.conf));
  lock.addEventListener("click", commit);
  $("#q-again").addEventListener("click", () => { reset(); opts[0].focus(); });
  sync();

  if (reduced()) { $("#q-auto").hidden = true; return; }
  // plays itself: confident and wrong, then right and fairly sure
  const SCRIPTS = [["A", "Certain"], ["B", "Fairly sure"]];
  let visible = false;
  const start = async () => {
    const id = ++run;
    const wait = async (ms) => { await sleep(ms); if (id !== run) throw 0; };
    try {
      for (let n = 0; ; n++) {
        const [opt, conf] = SCRIPTS[n % 2];
        reset(); await wait(1200);
        choose(opt); await wait(900);
        rate(conf); await wait(900);
        commit(); await wait(5200);
      }
    } catch {}
  };
  const go = () => {
    if (visible && !paused() && !q.hasAttribute("data-user")) start(); else run++;
  };
  onView(q, (v) => { visible = v; go(); }, 0.5);
  addEventListener("mt-pause", go);
}

/* ---------- scroll scenes ---------- */
function scrollies() {
  // Wide screens follow the scroll. Phones play the same scenes on a timer, with a tappable step bar.
  const phone = matchMedia("(max-width: 920px)");
  const scenes = $$("[data-scrolly]").map((el) => {
    const n = +getComputedStyle(el).getPropertyValue("--n");
    const items = $$("[data-i]", el);
    const track = $(".track", el);
    const dots = track ? $$("li", track) : [];
    const nav = document.createElement("div");
    nav.className = "scene-nav";
    nav.setAttribute("role", "tablist");
    nav.setAttribute("aria-label", "Scene steps");
    nav.innerHTML = Array.from({ length: n }, (_, i) => `<button type="button" role="tab" aria-label="Step ${i + 1} of ${n}"></button>`).join("");
    $(".stage", el).append(nav);
    return { el, n, items, track, dots, nav: $$("button", nav), step: -1, user: false, visible: false, timer: 0 };
  });
  const set = (s, step) => {
    s.step = step;
    s.el.dataset.step = step;
    const mark = (list) => list.forEach((d, i) => { d.classList.toggle("is-cur", i === step); d.classList.toggle("is-past", i < step); });
    for (const it of s.items) { const i = +it.dataset.i; it.classList.toggle("is-cur", i === step); it.classList.toggle("is-past", i < step); }
    mark(s.dots);
    mark(s.nav);
    s.nav.forEach((b, i) => b.setAttribute("aria-selected", String(i === step)));
    s.track?.style.setProperty("--tp", step / (s.n - 1));
  };
  // the ring scene needs a full Predict, Try, Check cycle
  const dwell = (s) => (s.el.dataset.scrolly === "loop" && s.step === 4 ? 7600 : 4200);
  const tick = (s) => {
    clearTimeout(s.timer);
    s.nav.forEach((b) => b.classList.remove("run"));
    if (!phone.matches || !s.visible || s.user || paused() || reduced()) return;
    const ms = dwell(s);
    const b = s.nav[s.step];
    b.style.setProperty("--dur", ms + "ms");
    void b.offsetWidth;
    b.classList.add("run");
    s.timer = setTimeout(() => { set(s, (s.step + 1) % s.n); tick(s); }, ms);
  };
  for (const s of scenes) {
    s.nav.forEach((b, i) => b.addEventListener("click", () => { s.user = true; set(s, i); tick(s); }));
    s.items.forEach((it) => it.addEventListener("click", () => { if (!phone.matches) return; s.user = true; set(s, (s.step + 1) % s.n); tick(s); }));
    new IntersectionObserver(([e]) => { s.visible = e.isIntersecting; tick(s); }, { threshold: 0.35 }).observe($(".stage", s.el));
  }
  const update = () => {
    if (phone.matches) return;
    for (const s of scenes) {
      const r = s.el.getBoundingClientRect();
      const run = r.height - innerHeight;
      const p = Math.min(1, Math.max(0, -r.top / run));
      const step = Math.min(s.n - 1, Math.floor(p * s.n));
      if (step !== s.step) set(s, step);
    }
  };
  const mode = () => { for (const s of scenes) { if (phone.matches && s.step < 0) set(s, 0); tick(s); } update(); };
  let queued = false;
  addEventListener("scroll", () => { if (!queued) { queued = true; requestAnimationFrame(() => { queued = false; update(); }); } }, { passive: true });
  addEventListener("resize", update);
  addEventListener("mt-pause", () => scenes.forEach(tick));
  phone.addEventListener("change", mode);
  mode();
}

/* ---------- calibration ---------- */
function calibration() {
  const svg = $("#cal-svg");
  const fig = svg.closest("figure");
  const range = $("#cal-range");
  const out = $("#cal-out");
  const read = $("#cal-read");
  const STATED = [25, 50, 75, 95];
  // example only: how often answers at each level were right, session by session
  const SESSIONS = [[30, 45, 60, 58], [28, 48, 64, 66], [27, 50, 68, 74], [26, 50, 71, 81], [25, 51, 73, 87], [25, 50, 74, 92]];
  const x = (s) => 60 + (s / 100) * 480;
  const y = (a) => 290 - (a / 100) * 240;
  const NS = "http://www.w3.org/2000/svg";
  const dots = STATED.map(() => $("#cal-dots").appendChild(document.createElementNS(NS, "circle")));
  const gaps = STATED.map(() => $("#cal-gaps").appendChild(document.createElementNS(NS, "line")));
  const line = $("#cal-line");
  let cur = SESSIONS[0].slice();

  const draw = (vals) => {
    line.setAttribute("d", vals.map((a, i) => `${i ? "L" : "M"}${x(STATED[i])} ${y(a)}`).join(" "));
    vals.forEach((a, i) => {
      dots[i].setAttribute("cx", x(STATED[i])); dots[i].setAttribute("cy", y(a)); dots[i].setAttribute("r", 7);
      const over = STATED[i] - a > 6;
      dots[i].classList.toggle("over", over);
      gaps[i].setAttribute("x1", x(STATED[i])); gaps[i].setAttribute("x2", x(STATED[i]));
      gaps[i].setAttribute("y1", y(STATED[i])); gaps[i].setAttribute("y2", y(a));
      gaps[i].style.opacity = over ? "" : "0";
    });
  };
  let tween = 0;
  const show = (k) => {
    range.value = k; out.textContent = k;
    const to = SESSIONS[k - 1];
    read.textContent = `Certain: said 95%, right ${to[3]}%`;
    const from = cur.slice();
    const id = ++tween;
    if (reduced()) { cur = to.slice(); return draw(cur); }
    const t0 = performance.now();
    const step = (t) => {
      if (id !== tween) return;
      const p = Math.min(1, (t - t0) / 800);
      const e = 1 - Math.pow(1 - p, 4);
      cur = from.map((a, i) => a + (to[i] - a) * e);
      draw(cur);
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  draw(cur);

  let user = false, visible = false, run = 0;
  range.addEventListener("input", () => { user = true; run++; read.setAttribute("aria-live", "polite"); show(+range.value); });
  const go = async () => {
    const id = ++run;
    if (!visible || paused() || user || reduced()) return;
    let k = +range.value;
    while (id === run) {
      await sleep(k === 6 ? 3200 : 1500);
      if (id !== run) return;
      k = k === 6 ? 1 : k + 1;
      show(k);
    }
  };
  onView(fig, (v) => { visible = v; go(); }, 0.5);
  addEventListener("mt-pause", go);
}

/* ---------- forgetting curve ---------- */
function forgetting() {
  const X = (d) => 40 + (d / 60) * 540;
  const Y = (r) => 260 - r * 220;
  // example only: each review resets recall, and the next gap is longer
  const REVIEWS = [0, 2, 7, 18, 42];
  const STAB = [3.3, 8.3, 18.3, 40, 90];
  let d = "";
  REVIEWS.forEach((t0, i) => {
    const t1 = REVIEWS[i + 1] ?? 60;
    for (let t = t0; t <= t1 + 1e-9; t += 0.25) {
      const r = Math.exp(-(t - t0) / STAB[i]);
      d += `${d ? "L" : "M"}${X(t).toFixed(1)} ${Y(r).toFixed(1)}`;
    }
  });
  $("#fsrs-curve").setAttribute("d", d);
  let n = "";
  for (let t = 0; t <= 30; t += 0.5) n += `${n ? "L" : "M"}${X(t).toFixed(1)} ${Y(Math.exp(-t / 3.3)).toFixed(1)}`;
  $("#fsrs-none").setAttribute("d", n);
  const g = $("#fsrs-dots");
  REVIEWS.slice(1).forEach((t, i) => {
    const low = Math.exp(-(t - REVIEWS[i]) / STAB[i]);
    g.insertAdjacentHTML("beforeend",
      `<g class="rv" style="transition-delay:${0.3 + (t / 60) * 3}s"><circle cx="${X(t)}" cy="${Y(low)}" r="6"/><text x="${X(t)}" y="${Y(1) - 12}">day ${t}</text></g>`);
  });
}

/* ---------- claims ledger ---------- */
function ledger() {
  const rows = $$(".claim-row");
  if (reduced()) { for (const r of rows) r.classList.add("on"); return; }
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      io.unobserve(e.target);
      setTimeout(() => e.target.classList.add("on"), 150);
    }
  }, { threshold: 0.6 });
  for (const r of rows) io.observe(r);
}

/* ---------- subjects ---------- */
function subjects() {
  const SUBJECTS = [
    ["Adding one tool to the end of the list keeps every message cached.",
      "Run cell 2.3 with and without the tool; compare the reused token counts.",
      "The shared run ends inside the tools block. Prediction wrong: the order is one sequence."],
    ["Doubling the sample size halves the margin of error.",
      "Simulate it with a slider: 500 samples of n = 100, then of n = 200.",
      "It shrinks by a factor of √2, about 29%. Halving it takes four times the sample."],
    ["“Sé que estés bien” keeps the subjunctive, like espero que.",
      "Write both openers; check them against a native source.",
      "Knowing states a fact, so it flips back: sé que estás bien."],
    ["Article 231 of the Treaty of Versailles names Germany as the sole cause of the war.",
      "Read the article itself, then how German delegates read it.",
      "It assigns responsibility for loss and damage to Germany and its allies. “Sole guilt” was the reading, not the wording."],
    ["Slowing the run to 60 bpm cleans up the smudged notes.",
      "Record it at 60, 72 and 90 bpm; listen back without the score.",
      "Clean at 60, still smudged at 72: the shift between positions breaks first. Practise the shift alone."],
    ["Naming my number first will cost me in the negotiation.",
      "Role-play: the tutor plays the buyer. You open first, then again second.",
      "Opening first, their counter landed near your anchor. Compare it with the case's real outcome."],
  ];
  const box = $("#subj");
  const tabs = $$("[role=tab]", box);
  const ptc = $(".ptc", box);
  const [p, t, c] = ["#subj-p", "#subj-t", "#subj-c"].map((s) => $(s));
  let cur = 0;
  const show = (i, focus) => {
    cur = i;
    tabs.forEach((b, k) => { b.setAttribute("aria-selected", String(k === i)); b.tabIndex = k === i ? 0 : -1; });
    if (focus) tabs[i].focus();
    ptc.setAttribute("aria-labelledby", tabs[i].id);
    [p.textContent, t.textContent, c.textContent] = SUBJECTS[i];
    ptc.classList.remove("swap"); void ptc.offsetWidth; ptc.classList.add("swap");
  };
  let user = false, visible = false, run = 0;
  const stop = () => { user = true; run++; box.removeAttribute("data-auto"); ptc.setAttribute("aria-live", "polite"); };
  tabs.forEach((b, i) => {
    b.addEventListener("click", () => { stop(); show(i); });
    b.addEventListener("keydown", (e) => {
      const d = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
      if (d) { e.preventDefault(); stop(); show((cur + d + tabs.length) % tabs.length, true); }
    });
  });
  show(0);
  ptc.classList.remove("swap");
  const go = async () => {
    const id = ++run;
    const on = visible && !paused() && !user && !reduced();
    box.toggleAttribute("data-auto", on);
    if (!on) return;
    show(cur); // restarts the tab's timer bar in step with the loop
    while (id === run) {
      await sleep(6500);
      if (id !== run) return;
      show((cur + 1) % tabs.length);
    }
  };
  onView(box, (v) => { visible = v; go(); }, 0.4);
  addEventListener("mt-pause", go);
}

/* ---------- live pages ---------- */
function pages() {
  const CAPS = {
    step: "The tutor offers a single-purpose page with real measured data, and builds it only if you say yes. It asks the prediction first.",
    map: "The module map with your position, drawn from the session records.",
    recap: "One page per module: the map, your numbers, calibration, the wrong models you fixed and your rule.",
  };
  const tabs = $$(".seg [role=tab]");
  const frames = $$(".b-body iframe");
  const open = $("#b-open");
  const cap = $("#b-cap");
  const show = (name, focus) => {
    tabs.forEach((t) => { const on = t.dataset.pane === name; t.setAttribute("aria-selected", String(on)); t.tabIndex = on ? 0 : -1; if (on && focus) t.focus(); });
    for (const f of frames) {
      const on = f.dataset.pane === name;
      f.hidden = !on;
      if (on && !f.src) f.src = f.dataset.src;
    }
    $(".b-body").setAttribute("aria-labelledby", `pg-tab-${name}`);
    open.href = `demo/${name}.html`;
    cap.textContent = CAPS[name];
  };
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => show(t.dataset.pane));
    t.addEventListener("keydown", (e) => {
      const d = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
      if (d) { e.preventDefault(); show(tabs[(i + d + tabs.length) % tabs.length].dataset.pane, true); }
    });
  });
  onView($(".browser"), (v) => { if (v && !frames[0].src) show("step"); }, 0.1);
}

/* ---------- counts ---------- */
function counts() {
  for (const el of $$("[data-count]")) {
    const to = +el.dataset.count;
    if (reduced()) continue;
    el.textContent = "0";
    onView(el, (v) => {
      if (!v || el.dataset.done) return;
      el.dataset.done = "1";
      const t0 = performance.now();
      const step = (t) => {
        const p = Math.min(1, (t - t0) / 900);
        el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }, 0.8);
  }
}

controls();
reveals();
question();
scrollies();
calibration();
forgetting();
ledger();
subjects();
pages();
counts();
