"""Static checks on every skill: portable frontmatter, working links, nothing personal or tool-specific.

usage: python -I tests/check_skill.py   (exit 1 on any problem)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORTABLE = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
# Method files describe capabilities, never products (references/capabilities.md).
METHOD = ["capabilities", "plan", "probe", "teach", "questions", "review", "practice", "voice", "visuals",
          "session-loop", "records", "role-play"]
# Word budgets: the agent re-reads these mid-session, so growth costs attention on every step.
# Raise a budget only with a reason; move rarely used detail into its own reference instead.
SKILL_WORDS, REF_WORDS = 1400, 2000
PRODUCTS = re.compile(r"\b(Claude|Codex|Cursor|Gemini|Copilot|OpenCode|ChatGPT|AskUserQuestion|Artifact)\b")
PATHLIKE = re.compile(r"`((?:references|scripts|assets)/[\w./-]+)`")

problems = []


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        if line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


for skill_md in sorted(ROOT.glob("skills/*/SKILL.md")):
    skill = skill_md.parent
    text = skill_md.read_text(encoding="utf-8")
    fm = frontmatter(text)
    if fm is None:
        problems.append(f"{skill_md}: no frontmatter")
        continue
    name, desc = fm.get("name", ""), fm.get("description", "")
    if name != skill.name or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        problems.append(f"{skill_md}: name {name!r} must match the folder and the spec charset")
    if not 1 <= len(desc) <= 1024:
        problems.append(f"{skill_md}: description is {len(desc)} chars (1-1024)")
    if extra := set(fm) - PORTABLE:
        problems.append(f"{skill_md}: non-portable frontmatter keys {sorted(extra)}")
    if len(text.splitlines()) > 500:
        problems.append(f"{skill_md}: over 500 lines")
    if (n := len(text.split())) > SKILL_WORDS:
        problems.append(f"{skill_md}: {n} words (budget {SKILL_WORDS})")
    for ref in sorted((skill / "references").glob("*.md")):
        if (n := len(ref.read_text(encoding="utf-8").split())) > REF_WORDS:
            problems.append(f"{ref.relative_to(ROOT)}: {n} words (budget {REF_WORDS})")

    for md in [skill_md, *skill.rglob("*.md")]:
        body = md.read_text(encoding="utf-8")
        for ref in PATHLIKE.findall(body):
            target = ref.split()[0].rstrip(".,")
            if "<" in target or "*" in target:
                continue
            if not (skill / target).exists():
                problems.append(f"{md.relative_to(ROOT)}: `{ref}` does not exist in the skill")
    for stem in METHOD:
        f = skill / "references" / f"{stem}.md"
        if f.exists():
            for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                if PRODUCTS.search(line):
                    problems.append(f"{f.relative_to(ROOT)}:{n}: method files name capabilities, not products")

for p in problems:
    print(p)
print(f"{len(problems)} problem(s)" if problems else "skills OK")
sys.exit(1 if problems else 0)
