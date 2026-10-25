# Module 4: giving the model a tool

By the end you can say what happens, in order, when the model uses a tool: what the model asked for, what Python ran, what evidence came back. And you can show a question where the tool changed the answer, and one where the model said the table does not establish it.

The one command:

    python 04_tool/starter.py

Predict first. The model will be asked a question about the table twice, once with a search tool and once without. Will the evidence improve the answer, and how will you tell?

## How it works, in one paragraph

A tool is an ordinary Python function with a docstring (`04_tool/tools.py`). The adapter in `agent.py` turns its name, parameters and docstring into a description the model sees. The program sends the question and that description. The model never runs anything: it replies with a request, "call search_records with query zebrafish". The program runs the function here, sends the result back as a message from the tool, and asks the model again. When the model answers in words instead of asking for a tool, the loop stops. A turn limit stops it if it never does.

## Build

1. Run the starter with the supplied search tool and the demo question. Read the transcript on screen against `04_tool/trace.md`, the annotated one.
2. In pairs, two minutes each way: answer three questions from the trace. What did the model request? What did Python run? What evidence came back?
3. Checkpoint: both of you can answer the three questions. Pair check only.
4. Ask the question you wrote in the pre-work, with and without the tool:

        python 04_tool/starter.py "your question"
        python 04_tool/starter.py --no-tool "your question"

   Write one sentence on the card about what changed.
5. Ask one question the table cannot answer and see what the model does.
6. Stretch: change `search_records` so it also returns the excerpt, and see what the model does with it. Test the function on its own first: `python 04_tool/tools.py`.

## Cut rule

The stretch, then the cannot-answer question. The with-and-without comparison and the pair reading stay.

Carries forward: `agent.py` with one tool, and the three questions to ask of any trace.
