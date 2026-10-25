"""The scorer for Module 2. Supplied; read it, do not edit it.

A reply counts as right when the expected label is the first label word that
appears in it. A reply that names two labels is scored by the first one, so a
hedge is a miss. There is no target score: the point is the habit of changing
one thing, scoring, and opening a miss to see whose fault it was, the model's
or the label's. Two of the labeled documents are genuinely arguable; the
corpus README says which.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABELS = ["experimental", "computational", "theoretical", "qualitative", "review", "mixed"]


def cases(which="cases"):
    """doc_id -> expected label, for 'cases' (ten) or 'heldout' (six)."""
    return json.load(open(ROOT / "corpus" / "labels.json"))[which]


def first_label(reply):
    """The first label word in the reply, or None."""
    words = re.findall(r"[a-z]+", reply.lower())
    for w in words:
        if w in LABELS:
            return w
    return None


def score(answers, expected):
    right = 0
    misses = []
    for doc_id, want in expected.items():
        got = first_label(answers.get(doc_id, ""))
        if got == want:
            right += 1
        else:
            misses.append((doc_id, want, got, answers.get(doc_id, "").strip()))
    print(f"Score: {right} out of {len(expected)}")
    for doc_id, want, got, raw in misses:
        shown = raw.replace("\n", " ")[:90]
        print(f"  miss {doc_id}: expected {want}, got {got or 'no label'}   reply: {shown}")
    return right
