"""Pre-release check: find word n-grams our files share with LearnHarness (AGPL-3.0).

Fetch their text to a temp dir OUTSIDE this folder (never vendor it here):
    mkdir -p /tmp/lh-src && cd /tmp/lh-src
    gh api "repos/amosblomqvist/learnharness/git/trees/HEAD?recursive=1" --jq '.tree[]|select(.type=="blob").path'       | grep -E '^(src/agent/prompts/|skills/learnharness/|docs/teaching-methodology)'       | while read p; do gh api "repos/amosblomqvist/learnharness/contents/$p" -H "Accept: application/vnd.github.raw" > "$(echo $p | tr / _)"; done

Run (N=6 for copied phrases, N=4-5 for a closer look):
    python -I tools/overlap.py 5 /tmp/lh-src $(find skills -name "*.md")

Only phrase-level copying shows up here. Following their structure section by section is
also a risk, so read the skill text next to their prompts before publishing.
"""
import re, sys, pathlib
N = int(sys.argv[1])
src_dir, ours = pathlib.Path(sys.argv[2]), [pathlib.Path(p) for p in sys.argv[3:]]
words = lambda t: re.findall(r"[a-z0-9']+", t.lower())
src = {}
for f in src_dir.iterdir():
    if f.suffix in ('.md', '.py') and 'LICENSE' not in f.name:
        w = words(f.read_text(encoding='utf-8', errors='ignore'))
        for i in range(len(w)-N+1): src.setdefault(' '.join(w[i:i+N]), f.name)
for o in ours:
    w = words(o.read_text(encoding='utf-8'))
    hits = sorted({(' '.join(w[i:i+N]), src[' '.join(w[i:i+N])]) for i in range(len(w)-N+1) if ' '.join(w[i:i+N]) in src})
    print(f"== {o} ({len(hits)} shared {N}-grams)")
    for h in hits: print("   ", h[0], " <-", h[1])
