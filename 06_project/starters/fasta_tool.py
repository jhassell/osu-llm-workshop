"""A reader for FASTA files. A tested starting point: run it, then change it.

    python 06_project/starters/fasta_tool.py
"""
from pathlib import Path

FASTA = Path(__file__).resolve().parent / "sample.fasta"     # or a file in mine/


def describe_sequences(name: str) -> str:
    """Describe the sequences in the FASTA file: for the named sequence, or for
    every sequence when the argument is 'all'. Returns one line per sequence with
    its id, description, length in bases and GC content as a percentage."""
    want = name.strip()
    records, header, seq = [], None, []
    for line in FASTA.read_text().splitlines():
        if line.startswith(">"):
            if header is not None:
                records.append((header, "".join(seq)))
            header, seq = line[1:].strip(), []
        else:
            seq.append(line.strip().upper())
    if header is not None:
        records.append((header, "".join(seq)))
    out = []
    for header, s in records:
        sid = header.split()[0]
        if want not in ("all", "", "*") and sid != want:
            continue
        gc = 100 * sum(s.count(b) for b in "GC") / max(len(s), 1)
        out.append(f"{sid}: {header[len(sid):].strip() or 'no description'}; {len(s)} bases; GC {gc:.1f}%")
    return "\n".join(out) or f"no sequence named {name!r}; ids are {', '.join(h.split()[0] for h, _ in records)}"


if __name__ == "__main__":
    print(describe_sequences("all"))
    print()
    print(describe_sequences("seq_B7"))
    print()
    print(describe_sequences("nope"))
