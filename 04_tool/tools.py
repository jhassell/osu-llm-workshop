"""Module 4's one tool: search the table. Supplied; the stretch changes it.

A tool is an ordinary Python function: string arguments in, one string out,
and a docstring that tells the model when to use it. The docstring is the
part the model reads, so write it for the model.

    python 04_tool/tools.py              test the tool alone on "zebrafish"
    python 04_tool/tools.py lirazine     test it on another word
    python 04_tool/tools.py --saved      search the saved table, not yours

It searches your Module 3 table, 03_table/records.jsonl, when that has usable
rows, and the saved table corpus/records.jsonl when it does not. --saved (here
or on the starter) searches the saved table without touching yours.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "03_table" / "records.jsonl"
SAVED = ROOT / "corpus" / "records.jsonl"
USE_SAVED = "--saved" in sys.argv
_noted = False


def _note(text):
    """Say once per run which table is searched, when it is not the obvious one."""
    global _noted
    if not _noted:
        print(f"note: {text}", file=sys.stderr, flush=True)
        _noted = True


def _read(path):
    """The usable rows of one table file, and how many lines were skipped."""
    rows, skipped = [], 0
    for line in open(path):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            skipped += 1
            continue
        if not isinstance(row, dict) or "error" in row or not row.get("doc_id"):
            skipped += 1
            continue
        rows.append(row)
    return rows, skipped


def load_table():
    """The rows the tool searches. Rows that recorded an error are skipped."""
    if USE_SAVED:
        _note("--saved: searching corpus/records.jsonl. Your 03_table/records.jsonl is untouched.")
        return _read(SAVED)[0]
    if not TABLE.exists():
        _note("no 03_table/records.jsonl yet, so the saved table corpus/records.jsonl is searched. "
              "To build yours: python 03_table/run_folder.py")
        return _read(SAVED)[0]
    rows, skipped = _read(TABLE)
    if not rows:
        _note("03_table/records.jsonl has no usable rows, so the saved table corpus/records.jsonl is searched. "
              "To rebuild yours: python 03_table/run_folder.py (add mine for your own documents)")
        return _read(SAVED)[0]
    if skipped:
        _note(f"{skipped} row(s) of 03_table/records.jsonl were unreadable or recorded an error, and are not searched. "
              "To redo them: python 03_table/run_folder.py (add mine for your own documents)")
    return rows


def search_records(query: str) -> str:
    """Search the table of research records for a keyword or phrase. Returns every
    matching record as one JSON object per line, with its doc_id, title, year,
    method, sample_size and main_claim. Returns 'no matches' if nothing matches.
    Use short queries: one or two words work better than a sentence."""
    q = query.strip().lower()
    hits = []
    for row in load_table():
        text = " ".join(str(v) for v in row.values()).lower()
        if q in text:
            # The search reads every column; only these six go back to the model.
            # The stretch adds one more here, and says so in the docstring.
            hits.append({k: row.get(k, "") for k in ("doc_id", "title", "year", "method", "sample_size", "main_claim")})
    return "\n".join(json.dumps(h) for h in hits) or "no matches"


if __name__ == "__main__":
    # Test the tool on its own before the model ever sees it.
    words = [a for a in sys.argv[1:] if not a.startswith("-")]
    print(search_records(words[0] if words else "zebrafish"))
