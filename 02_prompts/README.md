# Module 2: getting it to do what you mean

By the end you can improve a prompt by changing one thing at a time, see the effect on ten labeled documents, and say which misses were the model's fault and which were the labels'.

The one command:

    python 02_prompts/starter.py

Predict first. Four changes will be made to a bad prompt: a role, constraints, an output format, two worked examples. Which one do you expect to help most?

## Build

1. Run the starter: the bad prompt, the ten documents, the score. The prompt is the plain string `PROMPT` at the top of the file. That is the only thing to edit.
2. Change one thing, run, write the score on your card.
3. Checkpoint: one change, one score, one miss opened. Open the document for a miss, read it, and show your pair why the model said what it said.
4. One more change. Two changes are the deliverable; there is no target score.
5. Stretch, in either order: a third change, or run your best prompt on the held-out documents with `--heldout` and see whether it holds.

The labels live in `corpus/labels.json`. Two of the ten are genuinely arguable, and the corpus README says which. A miss on one of those is a fact about the label, not the prompt.

## Cut rule

The stretch. Two changes always happen.

Carries forward: the method prompt, which becomes one column of the Module 3 table.
