"""Module 4's one tool: search the table. Supplied; the stretch changes it.

A tool is an ordinary Python function: string arguments in, one string out,
and a docstring that tells the model when to use it. The docstring is the
part the model reads, so write it for the model.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "03_table" / "records.jsonl"
SAVED = ROOT / "corpus" / "records.jsonl"


def load_table():
    path = TABLE if TABLE.exists() else SAVED
    rows = [json.loads(line) for line in open(path) if line.strip()]
    return [r for r in rows if "error" not in r]


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
            # The stretch: add row["year"] or other fields to what comes back.
            hits.append({k: row.get(k, "") for k in ("doc_id", "title", "year", "method", "sample_size", "main_claim")})
    return "\n".join(json.dumps(h) for h in hits) or "no matches"


if __name__ == "__main__":
    # Test the tool on its own before the model ever sees it.
    print(search_records("zebrafish"))
