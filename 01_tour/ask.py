"""One prompt, one reply. The whole program is the ask() line near the bottom.

    python 01_tour/ask.py "your question"
    python 01_tour/ask.py "your question" corpus/doc_003.txt     the document goes after the question
    python 01_tour/ask.py --twice "your question" corpus/doc_001.txt   the same prompt twice

Without a document the model answers from what it learned in training: some
of that is right and some is not, and nothing in the prompt lets you tell
which. With --twice you see the same prompt sent twice, so you can compare the
wording and the facts; a detail that changes is a detail to verify.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from docs import load          # noqa: E402
from llm import ask            # noqa: E402

args = sys.argv[1:]
twice = "--twice" in args
args = [a for a in args if a != "--twice"]
if not args:
    raise SystemExit('usage: python 01_tour/ask.py [--twice] "your question" [document]')

prompt = args[0]
if len(args) > 1:
    prompt += "\n\nDocument:\n" + load(args[1])["text"]

for n in (1, 2) if twice else (1,):
    if twice:
        print(f"---- reply {n} ----")
    print(ask(prompt))
    print()
