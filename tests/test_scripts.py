"""End-to-end tests for the skill's scripts. Run: uv run --with pytest --with "fsrs>=6,<7" pytest"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "mastery-tutor" / "scripts"


def run(script, *args, cwd=None):
    out = subprocess.run(
        [sys.executable, "-I", str(SCRIPTS / script), *map(str, args)],
        capture_output=True, text=True, encoding="utf-8", cwd=cwd,
    )
    assert out.returncode == 0, out.stderr
    return out.stdout


def test_new_topic_scaffolds_everything(tmp_path):
    topic = tmp_path / "rust"
    run("new_topic.py", "topic", topic, "Rust ownership")
    for f in ["AGENTS.md", "CLAUDE.md", "ROADMAP.md", "PROGRESS.md", "knowledge/propositions.md",
              "knowledge/misconceptions.md", "knowledge/reviews.md", "sessions/README.md", "sources/README.md"]:
        assert (topic / f).is_file(), f
    assert (topic / "ROADMAP.md").read_text(encoding="utf-8").startswith("# Rust ownership: roadmap")
    assert "{{" not in (topic / "ROADMAP.md").read_text(encoding="utf-8")

    run("new_topic.py", "module", topic, "phase-1-borrowing/1.1-moves", "1.1 Moves", "--lab", "ipynb")
    mod = topic / "phase-1-borrowing" / "1.1-moves"
    assert (mod / "notes.md").read_text(encoding="utf-8").startswith("# 1.1 Moves")
    nb = json.loads((mod / "lab.ipynb").read_text(encoding="utf-8"))
    assert "1.1 Moves" in "".join(nb["cells"][0]["source"])
    assert not (mod / "lab.md").exists()

    # Any subject: the default lab is a markdown lab book.
    run("new_topic.py", "module", topic, "phase-1-borrowing/1.2-dates", "1.2 Dating a letter")
    lab = (topic / "phase-1-borrowing" / "1.2-dates" / "lab.md").read_text(encoding="utf-8")
    assert lab.startswith("# 1.2 Dating a letter: lab") and "{{" not in lab
    assert not (topic / "phase-1-borrowing" / "1.2-dates" / "lab.ipynb").exists()

    run("new_topic.py", "session", topic, "1.1", "1.1 Moves", "--date", "2026-01-02")
    assert (topic / "sessions" / "2026-01-02-1.1.md").is_file()


def test_calibration_reads_logs_and_writes_progress(tmp_path):
    topic = tmp_path / "t"
    run("new_topic.py", "topic", topic, "T")
    lines = (["**Answer:** A · Certain (95%+) · ❌ Wrong. I'm certain, not uncertain."] * 6
             + ["**Answer:** B · Unsure (~50%) · ✅ Right. Not certain at all."] * 4
             + ["**Answer:** C · Fairly sure (~75%) · ✅ Right."] * 10
             + ["**Answer:** don't know · ❌ Wrong.", "**Answer:** _pending_",
                "**Q6b answer:** A · Fairly sure (~75%) · ✅ Right."])
    (topic / "sessions" / "2026-01-01-1.1.md").write_text("\n".join(lines[:10]), encoding="utf-8")
    (topic / "sessions" / "2026-01-02-1.1.md").write_text("\n".join(lines[10:]), encoding="utf-8")

    out = run("calibration.py", topic, "--recent", "10", "--write")
    first = out.splitlines()[0]
    # stated (6*95 + 4*50 + 10*75) / 20 = 76; right 14/20 = 70.
    assert "said 76%" in first and "right 70%" in first and "overconfident by 6 points" in first
    assert "Certain: right 0 of 6" in first and "Confident and wrong: 6" in first
    assert "Last 10: underconfident by 25 points (before: overconfident by 37 points)" in first
    assert "1 answered without a confidence" in first
    assert "| Certain (95%+) | 6 | 0 | 0% |" in out and "| Unsure (~50%) | 4 | 4 | 100% |" in out
    assert "Not counted" in out and "2026-01-02-1.1.md:13" in out

    prog = (topic / "PROGRESS.md").read_text(encoding="utf-8")
    assert prog.count("## Calibration") == 1 and first in prog
    assert "## Practice sessions" in prog and "## Modules" in prog


def test_new_topic_never_overwrites(tmp_path):
    run("new_topic.py", "topic", tmp_path, "First")
    (tmp_path / "ROADMAP.md").write_text("mine", encoding="utf-8")
    run("new_topic.py", "topic", tmp_path, "Second")
    assert (tmp_path / "ROADMAP.md").read_text(encoding="utf-8") == "mine"


def test_build_visual_escapes_and_wraps(tmp_path):
    src = tmp_path / "x.src.html"
    src.write_text("<title>X</title><script>const D = /*DATA*/null;</script>", encoding="utf-8")
    data = tmp_path / "x.data.json"
    data.write_text(json.dumps({"s": "</script><b>"}), encoding="utf-8")

    run("build_visual.py", src, data)
    page = (tmp_path / "x.html").read_text(encoding="utf-8")
    assert "<\\/script>" in page and "/*DATA*/" not in page
    assert not page.startswith("<!doctype")

    run("build_visual.py", src, data, "--standalone")
    page = (tmp_path / "x.html").read_text(encoding="utf-8")
    assert page.startswith("<!doctype html>") and "[hidden]{display:none!important}" in page


def test_due_replays_the_log(tmp_path):
    k = tmp_path / "knowledge"
    k.mkdir()
    (k / "propositions.md").write_text(
        "| ID | Statement | Module · node | Reading (date) | Evidence |\n|---|---|---|---|---|\n"
        "| P1 | A pipe \\| inside a cell | 1.1 · a | held | 1.1-Q1 |\n"
        "| P2 | Never checked | 1.1 · b | taught | |\n", encoding="utf-8")
    (k / "reviews.md").write_text(
        "| Date | Item | Kind | Rating | Evidence | Note |\n|---|---|---|---|---|---|\n"
        "| 2026-01-01 | P1 | lesson | Easy | 1.1-Q1 | capped at Good |\n", encoding="utf-8")
    early = run("due.py", k, "--today", "2026-01-02")
    assert "Due now (0)" in early and "P2: Never checked" in early
    late = run("due.py", k, "--today", "2026-06-01")
    assert "Due now (1)" in late and "A pipe | inside a cell" in late


def test_map_view_marks_progress(tmp_path):
    notes = tmp_path / "notes.md"
    notes.write_text(
        "# 1.1 Demo\n\n## Map (v2)\n\n```mermaid\ngraph TD\n"
        "  goal[\"Goal\"]\n  first[\"1. First\"]\n  known[\"Held: known\"]\n"
        "  known --> first\n  first --> goal\n```\n", encoding="utf-8")
    log = tmp_path / "log.md"
    log.write_text(
        "### Q1 · check · first\n**Answer:** A · Certain (95%+) · ✅ Correct.\n\n"
        "### Q2 · predict · goal\n**Answer:** _pending_\n", encoding="utf-8")
    out = tmp_path / "visuals"  # not created yet: the script makes it
    name = run("map_view.py", notes, out, log).strip()
    page = (out / name).read_text(encoding="utf-8")
    assert "class first passed" in page and "class goal current" in page and "class known held" in page


def test_recap_reads_one_module(tmp_path):
    topic = tmp_path / "t"
    run("new_topic.py", "topic", topic, "T")
    run("new_topic.py", "module", topic, "phase-1-a/1.1-first", "1.1 First")
    module = topic / "phase-1-a" / "1.1-first"
    (module / "notes.md").write_text(
        "# 1.1 First\n\n**Goal:** say why <b>\n\n## Map (v1)\n\n```mermaid\ngraph TD\n"
        "  goal[\"Goal\"]\n  first[\"1. First\"]\n  first --> goal\n```\n\n"
        "## Break it\n\nChanged the tempo.\n\n## Plug-back rule\n\n_In the learner's words._\n", encoding="utf-8")
    (topic / "sessions" / "2026-01-01-1.1.md").write_text(
        "### Q1 · predict · first\n**Answer:** A · Certain (95%+) · ❌ Wrong.\n\n"
        "### Q2 · check · first\n**Answer:** B · Fairly sure (~75%) · ✅ Right.\n", encoding="utf-8")
    (topic / "sessions" / "2026-01-02-1.2.md").write_text(  # another module: not counted
        "### Q1 · check · first\n**Answer:** B · Unsure (~50%) · ❌ Wrong.\n", encoding="utf-8")
    mis = topic / "knowledge" / "misconceptions.md"
    mis.write_text(mis.read_text(encoding="utf-8")
                   + "| M1 | Old belief | New model | 1.1-Q1 | Certain | Yes | |\n"
                   + "| M2 | Other | Model | 1.2-Q1 | Unsure | No | |\n", encoding="utf-8")

    page = Path(run("recap.py", topic, module).strip()).read_text(encoding="utf-8")
    assert "<b>1/1</b><span>Checks right" in page and "<b>0/1</b><span>Predictions right" in page
    assert "<b>1</b><span>Sessions" in page and "<b>1/1</b><span>Repaired" in page
    assert "Old belief" in page and "Other" not in page
    assert "class first passed" in page and '1#46; First' in page
    assert "You said 85% on average and were right 50%" in page
    assert "Changed the tempo." in page and "Your rule for your own work" not in page  # blank template skipped
    assert "say why &lt;b&gt;" in page
