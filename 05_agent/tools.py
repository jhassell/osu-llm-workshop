"""Module 5's two tools: search the table, read a whole document. Supplied.

read_document returns the full text of one document. That is where the
planted document matters: whatever a document says is evidence for the model
to weigh, never an instruction for it to follow. The program, not the
document, decides what tools exist and what they are allowed to do.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The same search tool as Module 4, loaded from its file (both files are
# called tools.py, so a plain import would find this one instead).
_spec = importlib.util.spec_from_file_location("module4_tools", ROOT / "04_tool" / "tools.py")
_m4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_m4)
search_records = _m4.search_records

FOLDERS = [ROOT / "corpus", ROOT / "mine"]


def read_document(doc_id: str) -> str:
    """Return the full text of one document, given its doc_id exactly as it
    appears in a search result (for example doc_004). Use this after a search,
    when the record's main_claim is not enough and you need the details:
    methods, numbers, limitations, or where two studies differ."""
    name = doc_id.strip()
    for folder in FOLDERS:
        path = folder / f"{name}.txt"
        if path.exists():
            text = path.read_text(errors="replace")
            return text if len(text) <= 12000 else text[:12000] + "\n[truncated]"
    return f"error: no document with doc_id {name!r}"


if __name__ == "__main__":
    print(read_document("doc_001")[:400])
