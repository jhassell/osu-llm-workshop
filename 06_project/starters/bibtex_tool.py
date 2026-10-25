"""A reader for BibTeX files. A tested starting point: run it, then change it.

    python 06_project/starters/bibtex_tool.py
"""
import re
from pathlib import Path

BIB = Path(__file__).resolve().parent / "sample.bib"      # or a file in mine/


def find_references(query: str) -> str:
    """Search a BibTeX reference list by any word in the title, author or year.
    Returns one line per matching entry: key, first author, year, title. Use
    'all' to list every entry."""
    want = query.strip().lower()
    entries = re.findall(r"@(\w+)\{([^,]+),(.*?)\n\}", BIB.read_text(), flags=re.S)
    lines = []
    for kind, key, body in entries:
        fields = dict(re.findall(r"(\w+)\s*=\s*\{(.*?)\}\s*,?\s*\n", body + "\n", flags=re.S))
        hay = " ".join(fields.values()).lower() + " " + key.lower()
        if want in ("all", "", "*") or want in hay:
            first = fields.get("author", "?").split(" and ")[0]
            lines.append(f"{key}: {first} ({fields.get('year', '?')}). {fields.get('title', '?')}")
    return "\n".join(lines) or f"no entry matches {query!r}"


if __name__ == "__main__":
    print(find_references("all"))
    print()
    print(find_references("okafor"))
    print()
    print(find_references("unobtainium"))
