# /// script
# requires-python = ">=3.10"
# dependencies = ["fsrs>=6,<7"]
# ///
"""List what's due for review, by replaying a topic's review log through FSRS.

    uv run scripts/due.py <topic>/knowledge [--today YYYY-MM-DD] [--all]
    (or: pip install "fsrs>=6,<7" && python due.py ...)

Reads `reviews.md` (the log) and `propositions.md` (statements, and which items exist)
from the knowledge folder. Writes nothing. Rules are in `references/review.md`:
  - same-day events on one item collapse into one review, keeping the worst rating
  - a `lesson` review counts as Good at most
  - day-level scheduling: no intra-day learning steps, no fuzzing (same log, same output)
"""
import argparse, pathlib, re, sys
from datetime import date, datetime, timezone

from fsrs import Card, Rating, Scheduler

RATINGS = {"again": Rating.Again, "hard": Rating.Hard, "good": Rating.Good, "easy": Rating.Easy}


def table_rows(path):
    """Rows of the first markdown table in a file, as dicts keyed by lowercased header."""
    if not path.exists():
        return []
    lines = [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return []
    cells = lambda l: [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", l.strip()[1:-1])]  # `\|` is a pipe inside a cell
    header = [h.lower() for h in cells(lines[0])]
    return [dict(zip(header, cells(l))) for l in lines[2:] if any(cells(l))]


def col(row, name):
    return next((v for k, v in row.items() if k.startswith(name)), "")


def utc(d):
    return datetime(d.year, d.month, d.day, tzinfo=timezone.utc)


def queue(kdir, today):
    """Replay the log. Returns (statements, rows); rows are (is_due, recall, item, due, last, n), most urgent first."""
    kdir = pathlib.Path(kdir)
    statements = {col(r, "id"): col(r, "statement") for r in table_rows(kdir / "propositions.md") if col(r, "id")}

    days = {}  # (item, date) -> worst rating that day
    for r in table_rows(kdir / "reviews.md"):
        item, rating = col(r, "item"), RATINGS.get(col(r, "rating").lower())
        if not item or rating is None:
            print(f"skipped row: {r}", file=sys.stderr)
            continue
        if col(r, "kind").lower() == "lesson":
            rating = min(rating, Rating.Good)
        day = date.fromisoformat(col(r, "date"))
        if day > today:
            continue  # "as of" view: ignore later reviews
        key = (item, day)
        days[key] = min(days.get(key, rating), rating)

    scheduler = Scheduler(learning_steps=(), relearning_steps=(), enable_fuzzing=False)
    cards = {}
    for (item, day), rating in sorted(days.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        card, n, _ = cards.get(item, (Card(), 0, None))
        card, _ = scheduler.review_card(card, rating, utc(day))
        cards[item] = (card, n + 1, rating)

    now = utc(today)
    rows = []
    for item, (card, n, last) in cards.items():
        recall = scheduler.get_card_retrievability(card, now)
        rows.append((card.due.date() <= today, recall, item, card.due.date(), last.name, n))
    rows.sort(key=lambda r: (not r[0], r[1]))
    return statements, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("knowledge_dir")
    ap.add_argument("--today", type=date.fromisoformat, default=date.today())
    ap.add_argument("--all", action="store_true", help="also list items not yet due")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    statements, rows = queue(args.knowledge_dir, args.today)

    def show(title, selected):
        print(f"## {title} ({len(selected)})\n")
        if selected:
            print("| Item | Statement | Due | Recall now | Last | Reviews |\n|---|---|---|---|---|---|")
            for _, recall, item, due, last, n in selected:
                print(f"| {item} | {statements.get(item, '?')} | {due} | {recall:.0%} | {last} | {n} |")
        print()

    print(f"# Review queue · {args.today}\n")
    show("Due now", [r for r in rows if r[0]])
    reviewed = {r[2] for r in rows}
    never = [i for i in statements if i not in reviewed]
    print(f"## Taught, never checked ({len(never)})\n")
    for i in never:
        print(f"- {i}: {statements[i]}")
    print()
    if args.all:
        show("Not yet due", [r for r in rows if not r[0]])
    unknown = sorted(reviewed - set(statements))
    if unknown and statements:
        print(f"Warning: reviewed items missing from propositions.md: {', '.join(unknown)}", file=sys.stderr)


if __name__ == "__main__":
    main()
