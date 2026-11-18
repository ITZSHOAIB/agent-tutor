"""Regenerate the demo pages the site embeds, from the skill's own scripts and a sample topic.

Usage: python -I build.py <path to mastery-tutor repo> <path to sample topic>

Each page gets one line in its <head> that copies the site's theme choice (data-theme on the
parent page) before the page's own scripts run, so a theme switch on the site reaches the
frames when they reload.
"""
import pathlib
import shutil
import subprocess
import sys

SITE = pathlib.Path(__file__).resolve().parent
OUT = SITE / "demo"
FOLLOW = ('<script>try{var t=parent.document.documentElement.dataset.theme;'
          'if(t)document.documentElement.dataset.theme=t}catch(e){}</script>')


def run(script, *args):
    out = subprocess.run([sys.executable, "-I", str(script), *map(str, args)],
                         capture_output=True, text=True, encoding="utf-8", check=True)
    return out.stdout.strip()


def follow_theme(path: pathlib.Path):
    page = path.read_text(encoding="utf-8")
    if FOLLOW not in page:
        at = page.find("<head>")
        page = page[:at + 6] + FOLLOW + page[at + 6:] if at >= 0 else FOLLOW + page
    path.write_text(page, encoding="utf-8", newline="\n")


def main():
    repo, topic = (pathlib.Path(a) for a in sys.argv[1:3])
    scripts = repo / "skills" / "mastery-tutor" / "scripts"
    module = next((topic / "phase-1-wishes").iterdir())
    logs = sorted((topic / "sessions").glob("2026-*.md"))
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    name = run(scripts / "map_view.py", module / "notes.md", OUT, *logs)
    (OUT / name).rename(OUT / "map.html")
    recap = pathlib.Path(run(scripts / "recap.py", topic, module))
    shutil.move(str(recap), OUT / "recap.html")
    shutil.copy(repo / "examples" / "cache-explorer" / "cache-explorer.html", OUT / "step.html")

    for page in OUT.glob("*.html"):
        follow_theme(page)
    print("built", *sorted(p.name for p in OUT.iterdir()))


if __name__ == "__main__":
    main()
