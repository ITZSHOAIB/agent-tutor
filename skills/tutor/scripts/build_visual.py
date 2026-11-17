"""Build a lesson visual: put measured JSON into a page made from assets/visual.html.

usage: python -I build_visual.py <name>.src.html <data.json> [--standalone]

Writes <name>.html next to the source, with the data in place of `/*DATA*/null`.
The source has no <!doctype>, <html> or <body>: hosts that publish pages (such as
Claude Artifacts) add their own. Pass --standalone to wrap it in a full document
for opening as a local file or serving from any static host.
"""
import argparse
import json
from pathlib import Path

SKELETON = (
    "<!doctype html><html><head><meta charset=utf-8>"
    '<meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">'
    "<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);"
    "padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;"
    "font:14px/1.4 system-ui,sans-serif}img{max-width:100%}"
    "[hidden]{display:none!important}</style></head><body>\n{page}\n</body></html>\n"
)


def build(src: Path, data: Path, standalone: bool = False) -> Path:
    page = src.read_text(encoding="utf-8")
    if "/*DATA*/null" not in page:
        raise SystemExit(f"{src}: no /*DATA*/null placeholder")
    blob = json.dumps(json.loads(data.read_text(encoding="utf-8")), ensure_ascii=False)
    page = page.replace("/*DATA*/null", blob.replace("</", "<\\/"))
    if standalone:
        page = SKELETON.replace("{page}", page)
    out = src.with_name(src.name.replace(".src.html", ".html"))
    out.write_text(page, encoding="utf-8")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("src", type=Path)
    ap.add_argument("data", type=Path)
    ap.add_argument("--standalone", action="store_true", help="wrap in a full HTML document")
    a = ap.parse_args()
    print(build(a.src, a.data, a.standalone))
