"""Module 3: from one document to one record.

    python 03_table/starter.py                  the sample document
    python 03_table/starter.py corpus/doc_013.txt   the one with missing values (stretch)

Your edit is not in this file. It is the two marked lines in records.py:
the name of your column and its one-line description. This program fills the
record for one document and prints it, field by field, excerpt last.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from docs import load               # noqa: E402
from llm import ask_json            # noqa: E402
from records import Record, FIELDS  # noqa: E402

DOCUMENT = sys.argv[1] if len(sys.argv) > 1 else "corpus/doc_001.txt"

RULES = (
    "You fill in one record for one research document. Copy doc_id and source exactly as given. "
    "The excerpt must be one sentence copied word for word from the document that supports main_claim. "
    "If the document does not state a value, write exactly: not stated. Never guess."
)


def make_record(doc):
    prompt = f"Document id: {doc['doc_id']}\nSource file: {doc['source']}\n\n{doc['text']}"
    return ask_json(prompt, Record, system=RULES)


if __name__ == "__main__":
    doc = load(DOCUMENT)
    record = make_record(doc)
    width = max(len(f) for f in FIELDS)
    for field in FIELDS:
        print(f"{field:<{width}}  {getattr(record, field)}")
    print()
    print("Is the excerpt really in the document?",
          "yes" if record.excerpt.strip() and record.excerpt.strip()[:60] in doc["text"] else "NO, check it")
