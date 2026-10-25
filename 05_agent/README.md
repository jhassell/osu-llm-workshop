# Module 5: an agent on your question

By the end you can run the agent with two tools on a question from your own research, read its trace with the three questions, and state the rule that keeps text inside a document from steering the agent.

The one command:

    python 05_agent/starter.py

Predict first. One document in the sample corpus contains an instruction addressed to the agent. Will the agent follow it? Write yes or no on your card, and why.

## Build

1. Run the agent with both tools on the pre-work question, over the sample table or your own:

        python 05_agent/starter.py "your question"

2. Checkpoint: a trace saved in `05_agent/trace.json`. Show your pair the line where the agent chose a tool and say whether it was the right one.
3. Run the planted-document check and see whether your prediction held:

        python 05_agent/starter.py --planted

4. Stretch: ask the synthesis question over your own documents, or improve one docstring in `05_agent/tools.py` and see whether the agent's choices change.

## The rule to take home

Document content is evidence, never authority. A document can say anything, including "ignore your instructions". The program decides which tools exist and what they may do; the model weighs what documents say against each other. One planted sentence that failed today proves nothing about the next one, which is why the tools here can only read.

`05_agent/failures/` holds two saved traces from the dry run, for reference: one where the agent stopped searching too early, one where a document's wording pulled the answer. They are reference material, not a task.

## Cut rule

The stretch. The planted-document run and the pair brainstorm stay.

Carries forward: a two-tool agent that has answered a real question with sources, and its trace.
