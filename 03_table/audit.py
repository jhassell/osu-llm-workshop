"""Module 3: put table rows next to their sources so you can audit them.

    python 03_table/audit.py 3 7 12      rows 3, 7 and 12 of 03_table/records.jsonl
    python 03_table/audit.py 5           any other row

For each row this prints the record field by field, excerpt last, says
whether the excerpt appears word for word in the source file, and names the
file to open. The judging is yours: is each value right, wrong, guessed where
the document is silent, or backed by an excerpt that does not support it?
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "03_table" / "records.jsonl"


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


if not TABLE.exists():
    raise SystemExit("No table yet. Run:  python 03_table/run_folder.py   (or --saved to copy the saved run)")

rows = [json.loads(line) for line in open(TABLE) if line.strip()]
wanted = [int(a) for a in sys.argv[1:] if a.isdigit()] or [3, 7, 12]

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
        continue
    if "excerpt" in row:
        found = excerpt_found(row["excerpt"], source.read_text(errors="replace"))
        print("\nIs the excerpt really in the document?", "yes" if found else "NO, check it")
    shown = source.relative_to(ROOT) if source.is_relative_to(ROOT) else source
    print(f"Open {shown} and check each value against it.\n")
