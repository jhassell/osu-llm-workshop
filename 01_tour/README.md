# Module 1: what the model can do

By the end you can call the model from Python with one line, name the two or three things it did well on a research document, and name one thing it got wrong and what evidence would settle it.

The one command:

    python 01_tour/starter.py

Predict first. The model will be asked to rewrite an abstract for a first-year student. Write on your card one thing you expect it to lose.

## Build

1. Run the starter. It makes six calls on `corpus/doc_001.txt` and prints each result under a heading. The whole interface is one line per call: `ask(prompt)`.
2. Change the document: another file in `corpus/`, or one of your own after `python convert.py`. Run it again.
3. Checkpoint: six results for a document you chose. Pick the two you would actually use and read them properly. Show your pair the best one and the worst one.
4. Change one of the six prompts in `PROMPTS` to something you actually want from your documents. Run it again.
5. Stretch: ask it about a paper you know well. Write down what it gets wrong, and what evidence would settle it.

## Cut rule

The stretch, then the prompt change.

Carries forward: `llm.py`, the helper with `ask(prompt)`, and a sense of what is worth asking.
