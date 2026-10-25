# One trace, annotated

This is the exchange behind `python 04_tool/starter.py`, recorded from a dry run against a Nemotron model, with a note on each message. Your own `trace.json` has the same shape. Read it with three questions in mind: what did the model request, what did Python run, what evidence came back.

## Message 1, from the program (system)

> You are a careful research assistant. Use the tools to find evidence before answering. Cite the doc_id of every record you rely on. If a search finds nothing, try one different query, then stop searching and say plainly that the evidence does not establish an answer.

The program wrote this. Alongside it, but not shown in the trace, the program sent the description of each tool: its name, its docstring, and its one string parameter. That description came from `describe()` in `agent.py`, which read it off the function.

## Message 2, from the person (user)

> Which studies in the table used zebrafish, and did they agree about lirazine? Cite doc ids.

## Message 3, from the model (assistant), a request, not an answer

> tool_calls: search_records(query="zebrafish")

What the model requested. Notice there is no text here, only a request to run a named function with an argument the model chose. The model has not seen the table. It cannot run anything.

## Message 4, from the tool

> {"doc_id": "doc_001", "title": "Lirazine Accelerates Cardiomyocyte Proliferation in Cryoinjured Zebrafish Ventricle", "year": "2021", "method": "experimental", "sample_size": "96 adult zebrafish", "main_claim": "..."}
> {"doc_id": "doc_002", ...}
> {"doc_id": "doc_003", ...}
> {"doc_id": "doc_004", ...}

What Python ran: `search_records("zebrafish")`, a substring match over every row of `03_table/records.jsonl`. What came back: four records, as text. The program put that text into a message with the role `tool` and the id of the request it answers, and sent the whole conversation back to the model.

## Message 5, from the model (assistant), the answer

> The records that involve zebrafish are doc_001, doc_002, doc_003, doc_004. Do the studies agree about lirazine? No. doc_001 and doc_002 report a clear increase in proliferating cardiomyocytes; doc_003 finds no detectable effect of a low dose at three days; doc_004 notes a dose-dependent pattern ...

Text this time, no tool request, so the loop stops. Every doc_id in the answer appears in message 4. That is what "evidence-bearing" means here: you can check each claim against a row, and each row against its source file.

## The same question without the tool

`python 04_tool/starter.py --no-tool` sends message 2 alone. In the dry run the model answered with a confident table of three invented studies, "Toxicokinetics of lirazine in Danio rerio" and two more, with doc ids 3, 7 and 12. None exist. Nothing in the reply tells you that. The difference between the two runs is the whole point of the afternoon.

## A question the table cannot answer

Asked for the total grant budget of the zebrafish studies, the model searched for "zebrafish", then for "budget", got no matches, and answered: "The records retrieved about zebrafish studies do not mention anything about a grant budget, so there is no evidence available to determine the total grant budget." Two searches, then a plain statement of what the evidence does not establish. The system message asked for exactly that behavior.
