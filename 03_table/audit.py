"""Module 3: put table rows next to their sources so you can audit them.

    python 03_table/audit.py 3 7 12      rows 3, 7 and 12 of 03_table/records.jsonl
    python 03_table/audit.py 5           any other row
    python 03_table/audit.py --mark 3    print row 3, then mark it checked by a person

For each row this prints the record field by field, excerpt last, says
whether the excerpt appears word for word in the source file, and names the
file to open. The judging is yours: is each value right, wrong, guessed where
the document is silent, or backed by an excerpt that does not support it?
With --mark, each row's doc_id is added to 03_table/checked.txt (once), and
viewer.py shows that row as checked by a person.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "03_table" / "records.jsonl"
CHECKED = ROOT / "03_table" / "checked.txt"


def excerpt_found(excerpt, text):
    """The same check as starter.py: word for word, spacing ignored."""
    excerpt, text = " ".join(excerpt.split()), " ".join(text.split())
    return bool(excerpt) and excerpt in text


def find_source(name):
    """The file a row came from. New rows hold a path such as corpus/doc_003.txt
    or mine/notes.txt; older rows (the saved table) hold only the file name."""
    if not name:
        return None
    path = Path(name) if Path(name).is_absolute() else ROOT / name
    if path.is_file():
        return path
    if "/" not in name:
        for d in ("corpus", "mine"):
            if (ROOT / d / name).is_file():
                return ROOT / d / name
    return None


def mark(row, n):
    """Add the row's doc_id to checked.txt unless it is there already, and say so."""
    doc_id = str(row.get("doc_id", "")).strip()
    if not doc_id:
        print(f"Row {n} has no doc_id, so it was not marked.\n")
        return
    old = CHECKED.read_text(errors="replace") if CHECKED.exists() else ""
    if doc_id in {line.strip() for line in old.splitlines()}:
        print(f"{doc_id} was already marked as checked by a person in {CHECKED.relative_to(ROOT)}.\n")
        return
    with open(CHECKED, "a") as f:
        f.write(("\n" if old and not old.endswith("\n") else "") + doc_id + "\n")
    print(f"Marked {doc_id} as checked by a person in {CHECKED.relative_to(ROOT)}.\n")


if not TABLE.exists():
    raise SystemExit("No table yet. Run:  python 03_table/run_folder.py   (or --saved to copy the saved run)")

rows = [json.loads(line) for line in open(TABLE) if line.strip()]
wanted = [int(a) for a in sys.argv[1:] if a.isdigit()] or [3, 7, 12]
marking = "--mark" in sys.argv[1:]
if marking and not any(a.isdigit() for a in sys.argv[1:]):
    raise SystemExit("Name the rows to mark, for example:  python 03_table/audit.py --mark 3")

for n in wanted:
    print(f"==== row {n} of {len(rows)}")
    if not 1 <= n <= len(rows):
        print("no such row\n")
        continue
    row = rows[n - 1]
    fields = [k for k in row if k != "excerpt"] + (["excerpt"] if "excerpt" in row else [])
    width = max(len(k) for k in fields)
    for k in fields:
        print(f"{k:<{width}}  {row[k]}")
    source = find_source(row.get("source", ""))
    if source is None:
        print(f"\nSource file {row.get('source')!r} not found.\n")
        if marking:
            mark(row, n)
        continue
    if "excerpt" in row:
        found = excerpt_found(row["excerpt"], source.read_text(errors="replace"))
        print("\nIs the excerpt really in the document?", "yes" if found else "NO, check it")
    shown = source.relative_to(ROOT) if source.is_relative_to(ROOT) else source
    print(f"Open {shown} and check each value against it.\n")
    if marking:
        mark(row, n)
