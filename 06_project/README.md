# Module 6: your own tool

By the end you can give the agent one Python function and get a correct, evidence-bearing answer to a question only that function can answer.

Plan first, three minutes, on the card before any code: what the function takes, what it returns, and the one test you will run on it before the agent sees it. Pairs read each other's cards and ask one question.

## Minimum success

One function with a docstring, tested on its own, added to the agent with one line; one question answered correctly using it; the trace saved. A small, correct tool beats an impressive agent with an unsupported answer.

## The default path, which everyone can finish

`csv_tool.py` is a working summarizer over `sample_log.csv`, an instrument log with a condition column and a reading column. It has two marked edits: the columns it reports on, and the question it is good at answering.

1. Run it on its own: `python 06_project/csv_tool.py`. It prints every group, one group, and what happens on a bad input.
2. Change the two marked edits. Bring your own CSV into `mine/` if you have one; the sample is always enough.
3. Run it on its own again until it says what you want.
4. Run `python 06_project/starter.py "a question only your tool can answer"`. The `tools=[...]` line in `starter.py` is where your function joins the agent.
5. Checkpoint at 3:30: the function passes its own test.

## Optional harder paths

The `starters/` folder has three tested starting points, each with a sample file: a FASTA reader, a BibTeX reader, and an instrument log parser for a fixed-width text log. Each is a function that takes strings and returns a string, with a docstring, and each prints its own test when run directly. Or write a calculator or unit converter the model keeps getting wrong, or the function you already know you want. Lookups against public APIs are in `followon/`, not for today.

## Finished early

Give your tool a bad input and see what the agent does with the error. Then ask it a question your tool should refuse, and write down what happened.

## Cut rule

None inside the block. If the day is behind, show and tell shrinks first.

Carries forward: a repository you own and keep, with a working agent and your own tool in it.
