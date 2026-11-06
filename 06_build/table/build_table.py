"""Stop 6 recipe 1: a folder of documents you read every week becomes a table.

    python 06_build/table/build_table.py corpus/papers
    python 06_build/table/build_table.py mine 06_build/table/fields.json

The columns are yours: edit fields.json, one line per column, the sentence the
model reads to fill it. Every value comes back with a sentence quoted from the
document and the page it is on, and the program checks that the quote is really
there, exactly as Stop 3 did. PDFs, .txt and .md files are read; anything else
is listed and skipped.

Writes results/build/table.csv (open it in the editor; the CSV viewer colours
the columns) and results/build/table.jsonl with every quote. A document that
fails is a row with an error, never dropped.
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "03_lit"))
from pydantic import BaseModel, Field, create_model   # noqa: E402

import llm                                            # noqa: E402
from pdfask import find_quote, pdf_pages, paper_text   # noqa: E402

OUT = ROOT / "results" / "build"


class Evidence(BaseModel):
    value: str = Field(description="The answer, in the document's own terms, or 'not stated'.")
    quote: str = Field(description="One sentence copied word for word from the document that supports the value, or ''.")
    page: int = Field(description="The page number from the === page N === markers, or 0.")


def row_model(fields):
    """A record with one Evidence per column, each described by your sentence."""
    return create_model("Row", **{name: (Evidence, Field(description=text)) for name, text in fields.items()})


def pages_of(path):
    """The document as a list of pages. A text file is one page."""
    if path.suffix.lower() == ".pdf":
        return pdf_pages(path)
    return [path.read_text(errors="replace")]


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    folder = Path(sys.argv[1])
    folder = folder if folder.is_absolute() else Path.cwd() / folder
    fields_file = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "fields.json"
    fields = {k: v for k, v in json.loads(fields_file.read_text()).items() if not k.startswith("_")}
    Row = row_model(fields)
    rules = ("You fill one row of a table for one document. Its text has === page N === markers. "
             "For each column give the value, one sentence copied word for word that supports it, and its page. "
             "If the document does not say, write 'not stated', an empty quote and page 0. Never guess.")
    files = sorted(p for p in folder.iterdir() if p.is_file() and not p.name.startswith(".")
                   and not (p.suffix.lower() == ".md" and p.stem.isupper()))   # README.md, SOURCES.md: a folder's notes, not data
    usable = [p for p in files if p.suffix.lower() in (".pdf", ".txt", ".md")]
    for p in files:
        if p not in usable:
            print(f"skipped {p.name}: not a PDF, .txt or .md")
    if not usable:
        raise SystemExit(f"No PDF, .txt or .md files in {folder}.")
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in usable:
        print(f"{path.name} ...", flush=True)
        row = {"file": path.name}
        try:
            pages = pages_of(path)
            if sum(len(p.strip()) for p in pages) < 200:
                raise ValueError("almost no text (a scan, or empty)")
            text, cut = paper_text(pages)
            rec = llm.ask_json(f"Document: {path.name}\n{text}", Row, system=rules)
            for name in fields:
                ev = getattr(rec, name)
                hit = find_quote(ev.quote, pages) if ev.quote.strip() else 0
                row[name] = ev.value
                row[f"{name}_quote"] = ev.quote
                row[f"{name}_found"] = "yes" if hit else ("not stated" if not ev.quote.strip() else "NO")
            row["cut"] = cut
        except Exception as err:
            row["error"] = f"{type(err).__name__}: {str(err).splitlines()[0][:150] if str(err) else ''}"
            print(f"   {row['error']}")
        rows.append(row)
    with open(OUT / "table.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    columns = ["file"] + list(fields) + [f"{n}_found" for n in fields] + ["error"]
    with open(OUT / "table.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    found = sum(r.get(f"{n}_found") == "yes" for r in rows for n in fields)
    asked = sum(r.get(f"{n}_found") in ("yes", "NO") for r in rows for n in fields)
    print(f"\n{len(rows)} rows -> results/build/table.csv; {found} of {asked} quotes found word for word.")
    print(f"{llm.TOTAL['calls']} model calls" + (f", about ${llm.TOTAL['cost']:.4f}" if llm.TOTAL["cost"] else ""))


if __name__ == "__main__":
    main()
