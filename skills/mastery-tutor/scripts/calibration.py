"""How well the learner's confidence matches their answers, from a topic's session logs.

    python -I scripts/calibration.py <topic> [--recent N] [--write]

Reads every answered question in `<topic>/sessions/*.md` (the line
`**Answer:** B · Fairly sure (~75%) · ✅ Right. ...`), in file-name order. Prints one line
to say in chat, then the table. `--write` replaces the `## Calibration` section of
`PROGRESS.md` with the same. Answers without a confidence ("don't know") are counted apart;
answer lines in any other format are listed by file and line, so they can be rewritten.

The line compares the confidence the learner stated with how often they were right:
  stated   the average of the levels they picked (Guessing 25%, Unsure 50%, Fairly sure 75%, Certain 95%)
  gap      stated minus right, in points; positive means overconfident
It also compares the last N answers (default 20) with the ones before, once both sides
have 10 or more.
"""
import argparse, pathlib, re, sys

LEVELS = [("Guessing", "≤30%", 25), ("Unsure", "~50%", 50), ("Fairly sure", "~75%", 75), ("Certain", "95%+", 95)]
MIN_TREND = 10


def answers(topic):
    """(level index, right) per answered question with a confidence; the count without one;
    and `file:line` for answer lines with a verdict that aren't in the `**Answer:**` format."""
    out, unrated, odd = [], 0, []
    for log in sorted(p for p in (topic / "sessions").glob("*.md") if p.name != "README.md"):
        for n, line in enumerate(log.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            m = re.match(r"\*\*Answer:\*\*(.*)", line)
            if not m:
                if re.match(r"\*\*[^*]*answer[^*]*:\*\*", line, re.I) and ("✅" in line or "❌" in line):
                    odd.append(f"{log.name}:{n}")
                continue
            if "✅" not in m.group(1) and "❌" not in m.group(1):
                continue  # still pending
            fields = [f.strip().lower() for f in m.group(1).split("·")]
            conf = fields[1] if len(fields) > 2 else ""  # answer · confidence · verdict. reasoning
            level = next((i for i, (name, _, _) in enumerate(LEVELS)
                          if conf.startswith(name.lower()) or conf == str(i + 1)), None)
            if level is None:
                unrated += 1
            else:
                out.append((level, "✅" in m.group(1)))
    return out, unrated, odd


def gap(rows):
    stated = sum(LEVELS[l][2] for l, _ in rows) / len(rows)
    right = 100 * sum(r for _, r in rows) / len(rows)
    return stated, right, stated - right


def describe(g):
    if abs(g) < 5:
        return "well calibrated"
    return f"{'over' if g > 0 else 'under'}confident by {abs(g):.0f} points"


def summary(rows, unrated, recent):
    if not rows:
        return "No rated answers yet."
    stated, right, g = gap(rows)
    line = f"Over {len(rows)} answers you said {stated:.0f}% on average and were right {right:.0f}%: {describe(g)}."
    cert = [r for l, r in rows if l == 3]
    if cert:
        line += f" Certain: right {sum(cert)} of {len(cert)}."
    bold_misses = sum(1 for l, r in rows if l >= 2 and not r)
    if bold_misses:
        line += f" Confident and wrong: {bold_misses}."
    early, late = rows[:-recent], rows[-recent:]
    if len(early) >= MIN_TREND and len(late) >= MIN_TREND:
        line += f" Last {len(late)}: {describe(gap(late)[2])} (before: {describe(gap(early)[2])})."
    if unrated:
        line += f" Plus {unrated} answered without a confidence."
    return line


def table(rows):
    out = ["| Confidence | Answers | Right | Hit rate |", "|---|---|---|---|"]
    for i, (name, band, _) in enumerate(LEVELS):
        got = [r for l, r in rows if l == i]
        rate = f"{100 * sum(got) / len(got):.0f}%" if got else ""
        out.append(f"| {name} ({band}) | {len(got)} | {sum(got)} | {rate} |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topic", type=pathlib.Path)
    ap.add_argument("--recent", type=int, default=20)
    ap.add_argument("--write", action="store_true", help="replace the Calibration section of PROGRESS.md")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    rows, unrated, odd = answers(a.topic)
    line, tbl = summary(rows, unrated, a.recent), table(rows)
    print(line + "\n\n" + tbl)
    if odd:
        print("\nNot counted, not in the `**Answer:** B · Fairly sure (~75%) · ✅ Right.` format "
              "(rewrite them, then run this again): " + ", ".join(odd))
    if a.write:
        prog = a.topic / "PROGRESS.md"
        text = prog.read_text(encoding="utf-8")
        section = ("## Calibration\n\nWritten by the skill's `scripts/calibration.py` from the session logs; "
                   f"don't edit by hand.\n\n{line}\n\n{tbl}\n\n")
        new, n = re.subn(r"## Calibration\n.*?(?=^## |\Z)", lambda _: section, text, count=1, flags=re.S | re.M)
        if not n:
            new = text.rstrip() + "\n\n" + section
        prog.write_text(new.rstrip() + "\n", encoding="utf-8", newline="\n")
        print(f"\nwrote {prog}", file=sys.stderr)


if __name__ == "__main__":
    main()
