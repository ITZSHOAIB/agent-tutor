"""Scaffold a learning topic, a module inside it, or a session log, from the skill's assets.

    python -I new_topic.py topic   <topic_dir> "<Topic name>"
    python -I new_topic.py module  <topic_dir> <phase-folder>/<N.M-slug> "<N.M Module title>" [--lab md|ipynb]
    python -I new_topic.py session <topic_dir> <N.M> "<N.M Module title>" [--date YYYY-MM-DD]

Never overwrites an existing file; prints each path it creates.
"""
import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def fill(text: str, **values: str) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def write_new(path: Path, text: str) -> None:
    if path.exists():
        print(f"exists, kept: {path}", file=sys.stderr)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(path)


def topic(topic_dir: Path, name: str) -> None:
    src = ASSETS / "topic"
    for f in sorted(p for p in src.rglob("*") if p.is_file()):
        write_new(topic_dir / f.relative_to(src), fill(f.read_text(encoding="utf-8"), TOPIC=name))


def module(topic_dir: Path, rel: str, title: str, lab: str = "md") -> None:
    folder = topic_dir / rel
    write_new(folder / "notes.md", fill((ASSETS / "module-notes.md").read_text(encoding="utf-8"), MODULE=title))
    if lab == "md":
        write_new(folder / "lab.md", fill((ASSETS / "lab.md").read_text(encoding="utf-8"), MODULE=title))
        return
    nb = json.loads((ASSETS / "lab.ipynb").read_text(encoding="utf-8"))
    first = nb["cells"][0]
    first["source"] = [s.replace("{{module number and title}}", title) for s in first["source"]]
    write_new(folder / "lab.ipynb", json.dumps(nb, indent=1, ensure_ascii=False) + "\n")


def session(topic_dir: Path, number: str, title: str, day: str) -> None:
    text = fill((ASSETS / "session-log.md").read_text(encoding="utf-8"), DATE=day, MODULE=title)
    write_new(topic_dir / "sessions" / f"{day}-{number}.md", text)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("topic")
    t.add_argument("topic_dir", type=Path)
    t.add_argument("name")
    m = sub.add_parser("module")
    m.add_argument("topic_dir", type=Path)
    m.add_argument("path", help="e.g. phase-1-basics/1.1-first-idea")
    m.add_argument("title")
    m.add_argument("--lab", choices=["md", "ipynb"], default="md", help="lab.md for any subject (default), lab.ipynb when the tries compute")
    s = sub.add_parser("session")
    s.add_argument("topic_dir", type=Path)
    s.add_argument("number", help="module number, e.g. 1.1")
    s.add_argument("title")
    s.add_argument("--date", default=date.today().isoformat())
    a = ap.parse_args(argv)
    if a.cmd == "topic":
        topic(a.topic_dir, a.name)
    elif a.cmd == "module":
        module(a.topic_dir, a.path, a.title, a.lab)
    else:
        session(a.topic_dir, a.number, a.title, a.date)


if __name__ == "__main__":
    main()
