"""Module 4's one tool: search the table. Supplied; the stretch changes it.

A tool is an ordinary Python function: string arguments in, one string out,
and a docstring that tells the model when to use it. The docstring is the
part the model reads, so write it for the model.

    python 04_tool/tools.py              test the tool alone on "zebrafish"
    python 04_tool/tools.py lirazine     test it on another word
    python 04_tool/tools.py lirazine zebrafish effect    several words: any of them
    python 04_tool/tools.py --saved      search the saved table, not yours

It searches your Module 3 table, 03_table/records.jsonl, when that has usable
rows, and the saved table corpus/records.jsonl when it does not. --saved (here
or on the starter) searches the saved table without touching yours.
"""
import json
import re
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


# Words too common to tell records apart. They are dropped from a query, so a
# question written as a sentence still searches on the words that matter.
STOP = set("""a an and are as at be been but by can could did do does each for from had has
have how in into is it its of on or that the their them there these they this to was
were what when where which who whom why will with would about any all also than then
its find found show shows study studies paper papers document documents record records no not""".split())


def query_words(query):
    """The words of a query worth searching for: lower case, common words dropped."""
    words = re.findall(r"[a-z0-9][a-z0-9._%-]*", query.lower())
    return [w.strip(".") for w in words if w.strip(".") and w.strip(".") not in STOP]


def search_records(query: str) -> str:
    """Search the table of research records. Give one or more words; a record
    matches if it contains ANY of them (capitals ignored, common words like
    'the' or 'which' skipped). Records that match more of the words come first.
    Returns one JSON object per line with doc_id, title, year, method,
    sample_size, main_claim, and 'matched': the query words that record
    contains. A record that matched only some of your words may not be about
    your question: read it before you rely on it. Returns 'no matches' if no
    record contains any of the words."""
    words = query_words(query)
    hits = []
    for n, row in enumerate(load_table()):
        text = " ".join(str(v) for v in row.values()).lower()
        # A word counts when it starts a word in the record: "zebrafish" matches
        # "zebrafish", "lirazine" matches "lirazine", but "ph" does not match "graph".
        matched = [w for w in dict.fromkeys(words) if re.search(r"(?<![a-z0-9])" + re.escape(w), text)]
        if matched:
            # The search reads every column; only these six go back to the model.
            # The stretch adds one more here, and says so in the docstring.
            hit = {k: row.get(k, "") for k in ("doc_id", "title", "year", "method", "sample_size", "main_claim")}
            hit["matched"] = matched
            hits.append((-len(matched), n, hit))
    hits.sort(key=lambda h: (h[0], h[1]))
    return "\n".join(json.dumps(h[2]) for h in hits) or "no matches"


if __name__ == "__main__":
    # Test the tool on its own before the model ever sees it.
    words = [a for a in sys.argv[1:] if not a.startswith("-")]
    print(search_records(" ".join(words) if words else "zebrafish"))
