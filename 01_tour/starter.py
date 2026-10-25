"""Module 1: what the model can do. Six calls on one document.

    python 01_tour/starter.py                      the sample document
    python 01_tour/starter.py corpus/doc_003.txt   another sample document
    python 01_tour/starter.py mine/paper.txt       one of your own (after convert.py)

The only things to change are below this docstring: which document, and the
six prompts. Everything else is one line per call: ask(prompt).
"""
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from docs import load          # noqa: E402
from llm import ask            # noqa: E402

# ---- Change these. -------------------------------------------------------
DOCUMENT = sys.argv[1] if len(sys.argv) > 1 else "corpus/doc_001.txt"

PROMPTS = {
    "Two-sentence summary":
        "Summarize this document in two sentences.",
    "For a first-year student":
        "Rewrite the main finding of this document for a first-year undergraduate, in three sentences, no jargon.",
    "Methods used":
        "List the methods and techniques this document reports using, one per line, nothing else.",
    "Key numbers with units":
        "List the key numbers in this document, at most ten, one per line: value, unit, what it measures. Keep it brief.",
    "Three reviewer questions":
        "Write the three questions a careful peer reviewer would ask about this document.",
    "A question it cannot know":
        "What was the total budget of this project in dollars? If the document does not say, answer exactly: not stated in the document.",
}
# --------------------------------------------------------------------------

doc = load(DOCUMENT)
print(f"Document: {doc['source']}   Title: {doc['title']}\n")

for heading, prompt in PROMPTS.items():
    print("=" * 72)
    print(heading)
    print("=" * 72)
    print(ask(f"{prompt}\n\nDocument:\n{doc['text']}"))
    print()

print("Check one claim against the source. Find the passage with a word or number from a reply,")
print("then read it and ask whether it says the same thing:")
print(f'    grep -n -i "the word" {shlex.quote(DOCUMENT)}')
