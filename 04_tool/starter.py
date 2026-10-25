"""Module 4: giving the model a tool. The same question, without and with it.

    python 04_tool/starter.py                        the demo question
    python 04_tool/starter.py "your question here"   the one from your pre-work
    python 04_tool/starter.py --no-tool "question"   without the tool, for comparison

The program prints the exchange as it happens: what the model asked for, what
Python ran, what came back, and the answer. The trace is saved to
04_tool/trace.json. Read it against 04_tool/trace.md, the annotated one.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent import run, save_trace     # noqa: E402
from llm import ask                   # noqa: E402
from tools import search_records      # noqa: E402

DEFAULT_QUESTION = "Which studies in the table used zebrafish, and did they agree about lirazine? Cite doc ids."

args = [a for a in sys.argv[1:] if not a.startswith("-")]
question = args[0] if args else DEFAULT_QUESTION
print(f"Question: {question}\n")

if "--no-tool" in sys.argv:
    print("[no tool] the model answers from memory alone:\n")
    print(ask(question))
else:
    answer, messages = run(question, tools=[search_records])
    save_trace(messages, Path(__file__).resolve().parent / "trace.json")
