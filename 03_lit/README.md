# Stop 3: Three papers to an evidence table

You ask the agent for three papers on your topic. It searches a scholarly index, checks every DOI against Crossref, looks for retractions, and writes a bibliography built from the records, not from its memory. Then three PDFs become an evidence table: for each paper, the question, the method, the sample and the finding, each with a sentence quoted from the paper and the page it is on, and a check that the sentence is really there.

About 75 minutes, from 11:00, ending with the minute paper and your Stop 6 choice. Folder: `03_lit/`. You type in `openclaw chat` and in a terminal.

## You will be able to

- Get three candidate papers from a recorded query, with each DOI marked verified, mismatched, missing or unavailable.
- Say what "verified" and "no retraction found" do and do not mean.
- Turn three PDFs into an evidence table and check one quoted sentence against the claim beside it.

## The idea

A model asked for references from memory writes references that look right: plausible authors, a plausible journal, a DOI of the right shape. Some do not exist. So in this stop the model never writes a reference. `03_lit/lit.py` asks OpenAlex, a free index of scholarly works, and Crossref, the registry behind most DOIs; the agent runs it and reads what comes back. The BibTeX is built by the program from the returned records.

Every answer says exactly what it is:

- The papers are candidates returned by this query, in this order, on this date. Not "the best papers on the topic".
- `verified` means the DOI is in Crossref and its title and first author match the record. `mismatched` says which does not. `missing` means there is no DOI or Crossref has never heard of it (often a typo, sometimes an invented DOI). `unavailable` means Crossref could not be reached.
- The retraction line reads `no retraction found in Crossref as of <date>`. Crossref carries Retraction Watch's data, so this is a real check, but it is a statement about Crossref on that date, not a guarantee.

The evidence table works the same way. `03_lit/pdfask.py` pulls the text out of each PDF here, page by page, sends that text to the model, and asks for each field with a quoted sentence and a page. Then the program looks for every quote in the text the model saw. Found means the sentence is in the paper. It does not mean the sentence supports the value beside it. That part is yours.

## Before you start

- Your topic, in plain words, the way you would type it into a library search. Narrow beats broad: "cover crops soil organic carbon", not "soil".
- Your papers. If you brought two or three PDFs, they are in `mine/` and `python upload_check.py` said they have readable text. If not, three open-access papers on cover crops and soil carbon are in `corpus/papers/` (licenses in `corpus/papers/SOURCES.md`).

## Predict first

On your card: of three papers an index returns for your topic, how many will have a DOI that checks out? And in an evidence table built by a model, which field is it most likely to get wrong: the question, the method, the sample, or the finding?

## Do it

1. The search, in `openclaw chat`:

   ```
   Find three papers on <your topic>, using python 03_lit/lit.py. Record the query and
   the date, verify each DOI against title and authors, and write results/refs.bib from
   the returned metadata. Do not invent any DOI or title. Then tell me which papers are
   verified and whether any is retracted.
   ```

   Watch the tool calls: the agent should run `python 03_lit/lit.py "..."`. If it answers with references without running anything, they came from memory: tell it `Run 03_lit/lit.py; do not write references yourself.`

2. Check its answer against the files, in a second terminal:

   ```
   cat results/refs.bib
   ```

   Each entry has a comment line above it with the verification state and the retraction line. Does the agent's summary say the same? Open one DOI in the browser (`https://doi.org/<doi>`): is it the paper the entry names?

3. The evidence table, in the terminal. With PDFs of your own in `mine/` it reads those; otherwise the three shipped papers:

   ```
   python 03_lit/pdfask.py
   ```

   Or name the files: `python 03_lit/pdfask.py mine/a.pdf mine/b.pdf mine/c.pdf`. It prints, for each paper and field, whether the quote was found and on which page, and writes `results/table.jsonl` and `results/evidence-table.html`.

4. Read the table. Read the printed lines, or right-click `results/evidence-table.html` in the file tree, choose Download, and open it on your laptop. Pick one field in one paper whose quote was found. Open the text the model read, `results/papers/<paper>.txt`, at that page. Does the sentence say what the value says? Find one field where it does not settle the claim: the sentence is real, but the value goes further.

5. The minute paper, at 12:10, on the card. On the same card, circle the Stop 6 recipe you will build after lunch (see `06_build/README.md`; if unsure, the first one).

## Checkpoint

Three DOIs that resolve to the right papers. One quote found in the text. One field where the quote does not settle the claim, and why.

## Extensions

1. Ten papers instead of three: `python 03_lit/lit.py "<topic>" --n 10 --sort cited`. Which are most cited, and are those the ones you would read first?
2. A DOI from a reference list you do not trust: in a terminal, `python -c "import sys; sys.path.insert(0,'03_lit'); import lit; print(lit.verify('<doi>', '<title>', '<first author>'))"`. Try one with a digit changed.
3. The web, with sources. In Python, `llm.ask(question, web=True)` lets the model search the web first, and `llm.LAST["sources"]` lists the pages it used. Ask the same question with and without it. Which answer can you check?

## What you have now

`results/refs.bib` with every entry checked, `results/lit-search.json` recording the query and the date, and an evidence table with a quote and a page for every value. Stop 6's first recipe turns `pdfask.py` into a tool with your own columns for the documents you read every week, and its third turns `lit.py` into a digest of what is new on your topic.

## If something goes wrong

- The search says it used a saved answer, or that OpenAlex did not answer. OpenAlex limits free searches per network address, and the whole room shares a few. The three topics in `python 03_lit/lit.py --topics` always work offline; use one of those, then try yours again later. Checking DOIs in Crossref is not limited.
- A DOI comes back `missing` with a note that another agency registered it. It is real but not a Crossref DOI (Zenodo, arXiv and DataCite use their own); it cannot be checked here.
- `pdfask.py` says a PDF has almost no text. It is a scan: a picture of pages. The model cannot read it here. Name the shipped papers instead, so it does not pick up the scan in `mine/` again: `python 03_lit/pdfask.py corpus/papers/*.pdf`.
- The model service is slow or down. A saved run on the shipped papers is in `03_lit/saved/`; its README says how to do step 4 on it.
- A paper is long and the line says only the first part was read. The model saw about the first 120,000 characters (roughly 20,000 words). A finding in a late section may be missed: say so in your table.
- The agent edits `lit.py` or writes its own search code. Tell it: `Use 03_lit/lit.py as it is.` `git checkout 03_lit/lit.py` restores the file.
