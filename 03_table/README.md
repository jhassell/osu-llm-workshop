# Module 3: from documents to a table

By the end you can turn a folder of documents into a table of records with evidence attached, audit three rows against their sources, and say which kind of error you found.

The one command:

    python 03_table/starter.py

then

    python 03_table/run_folder.py

Predict first. Here is the record and one document. Which kind of error will show up first when the whole folder runs: a wrong value, a guessed value where the document says nothing, or an excerpt that does not support the claim?

## Build

1. Open `records.py`. At the bottom of the record are two marked lines: the name of your column and its one-line description. Change them; three worked examples sit beside them. The program handles everything else.
2. Run the starter on one document and read the record, excerpt last.
3. Checkpoint: one record on screen. Read its excerpt to your pair and say whether it supports the claim.
4. Run `run_folder.py` over the sample corpus, or over `mine` for your own documents, and open `03_table/records.jsonl`. If the endpoint is slow, `--saved` copies a saved run so the audit still happens.
5. Audit rows 3, 7, and 12 against their source files in `corpus/`. Mark each on your card as right, wrong value, guessed, or unsupported excerpt. Compare with your pair and with your prediction.
6. Stretch: run the starter on `corpus/doc_013.txt`, which states no year and no sample size, and see whether the model writes "not stated" or invents them.

This is a multi-step workflow: the method prompt from Module 2 is now one column, the record is the next step's input, and the afternoon's tools search the table this script writes.

## Cut rule

The stretch, then the personal documents run. The audit always happens.

Carries forward: `03_table/records.jsonl`, the table the afternoon's tools search.
