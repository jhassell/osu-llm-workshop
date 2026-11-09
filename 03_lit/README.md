# Stop 3: A research question, answered from papers you can check

You give the agent a research question and a few papers. It reads them, pulls out every value they report with the sentence and page each came from, and runs a checker that confirms each quote is really on that page. When the checker says no, it rereads and fixes the row. Then it forms a hypothesis for why the studies disagree, tests it against the values, searches for more papers when the ones it has cannot settle it (every DOI checked), and decides when it is done. Nobody, including the agent, knows the path in advance.

About 75 minutes, from 11:00, ending with the minute paper and your Stop 6 choice. Folder: `03_lit/`. The prompt is a file you open; you type one line into `openclaw chat`.

## You will be able to

- Turn a question and a few papers into a table of reported values, each tied to a quote and a page that a program has confirmed.
- Watch an agent act on a check that fails, and say what it changed and why.
- Judge an explanation of why studies disagree by the rows behind it.
- Say what "verified" and "no retraction found" do and do not mean.

## The idea

A model asked for references from memory writes references that look right: plausible authors, a plausible journal, a DOI of the right shape. Some do not exist. A model asked for a number from a paper can do the same with the number. So in this stop the model never has the last word on a fact. Three small programs do:

- `03_lit/pages.py` prints a paper's text page by page, exactly as the checker will read it.
- `03_lit/check_values.py` checks every row of `results/values.csv`: the quote is in the paper, on the page given; every number in the value is in the quote; a paper found by search has a DOI that Crossref confirms; and a unit conversion, written as arithmetic, really gives the converted value, sign included. Every run is added to `results/check-log.txt`, with each row's verdict and reason.
- `03_lit/lit.py` finds papers in OpenAlex, a free index of scholarly works, checks each DOI in Crossref, the registry behind most DOIs, and writes `results/refs.bib` from the records, not from the model. When a searched paper becomes a source in the table, the checker adds it to `results/sources.bib`, built the same way, and saves its abstract (the text a `doi:` row is checked against) as `results/papers/doi_<doi>.txt`.

What is left for the agent is the part only judgment can do: which values can fairly be compared, why they differ, which explanation survives the rows, when another search is worth it, and when to stop. That is what makes it an agent rather than a script: a goal, a path it chooses, and checks that push back. It is also why a smaller open model, run on campus, might do this work: it does not have to be right the first time, because the checker tells it when it is wrong. That is a reason to test a smaller model, not a result: the checks confirm where a quote is and that its numbers and conversions agree, not that the agent read it correctly.

Every check says exactly what it means:

- PASS means the quote is in the paper on that page and contains the number. It does not mean the sentence supports the row's reading of it. That part is yours.
- FLAGGED means a row failed a check and the agent says why it cannot be fixed. Read the failure beside the reason: they should be about the same thing.
- `verified` means the DOI is in Crossref and its title and first author match the record. `no retraction found in Crossref as of <date>` is a statement about Crossref on that date, not a guarantee.

## Before you start

- Where things are. Everything happens in the Codespace window. The Explorer, the file list on the left (Cmd-Shift-E, or Ctrl-Shift-E on Windows, if it is hidden), shows every file: click one to open it. A `.md` file opens formatted, and each grey box of text to type has a Copy button at its top right. A `.csv` opens as coloured columns. The terminal panel at the bottom is where `openclaw chat` runs.
- Your papers. If you brought two or three PDFs, they are in `mine/` and `python upload_check.py` said they have readable text. Your question: one quantity your papers report, with its unit, and why the reported amounts differ. If not, three open-access papers on cover crops and soil carbon are in `corpus/papers/` (licenses in `corpus/papers/SOURCES.md`), and `03_lit/question.md` already asks a question about them.

## Do it

1. Open OpenClaw's chat: in the terminal at the bottom, type `openclaw chat` and press Enter (or use the one still open from Stop 2; to start fresh, type `/new`).

2. Read the question, then hand it over. Click `03_lit/question.md` in the Explorer and read it: the question, the sources, the checks it must run, and when to stop. Your own papers? Click `03_lit/question-mine.md` instead, replace each [BRACKET] with your question, your quantity and what usually changes it in your field, and save (Cmd-S, or Ctrl-S). Then, in the chat, type one line and press Enter:

   ```
   Read 03_lit/question.md and do what it says.
   ```

   (or `question-mine.md`).

3. Watch the loop. Each line OpenClaw prints is a tool call. `pages.py` is the agent reading a paper. `check_values.py` prints PASS, FAIL or FLAGGED for every row: count the failures, then watch what it does about them. `lit.py` is a search: what made it search, and what did it search for? A `results` folder appears in the Explorer; click `results/check-log.txt` at any point to see each check's tally so far.

4. Check one row yourself. Click `results/values.csv`. Pick a row that passed. Its text is in `results/papers/`: `<paper>.txt` for a PDF, or `doi_<doi>.txt` for a `doi:` row, whose text is the abstract (page 0). Click that file, press Cmd-F (Ctrl-F) and type a few words of its quote. Is it on the page the row says? Does the sentence say what the row says, or does the row go further? Then pick a flagged row: is the reason in its note the same thing the check complained about? Run the check yourself to see both, in a second terminal (the **+** at the top right of the terminal panel):

   ```
   python 03_lit/check_values.py
   ```

5. Read the answer. Click `results/answer.md`. For each part of the explanation, which rows support it? Was each hypothesis tested against the rows, or only asserted? Which values did it set aside as not comparable, and why? If it used any paper it found by search, click `results/sources.bib`: each entry has its DOI check and its retraction line above it. Open one in the browser at `https://doi.org/` followed by its DOI: is it the paper the entry names? No `sources.bib` means no searched paper became a source: was the search needed, and does the answer say why not?

6. The minute paper, at 12:10, on the card. On the same card, circle the Stop 6 recipe you will build after lunch (see `06_build/README.md`; if unsure, the first one).

## Checkpoint

One row you checked yourself: the quote on its page, and whether it says what the row says. The agent's explanation and the rows behind it. One thing you would test next.

## Extensions

1. Push back. In the chat: `Your explanation leaves <a row> unexplained. Test another hypothesis against the rows.` Does it test, or only argue?
2. The same papers through a fixed pipeline, in the second terminal: `python 03_lit/pdfask.py corpus/papers/*.pdf` (your own: `python 03_lit/pdfask.py mine/*.pdf`) fills the same four columns (question, method, sample, finding) for every paper, with a quote each, and no decisions at all. What does the pipeline do that the agent did not, and the other way round?
3. Ten papers instead of three, in the second terminal: `python 03_lit/lit.py "<topic>" --n 10 --sort cited`. Which are most cited, and are those the ones you would read first?
4. A DOI from a reference list you do not trust, in the second terminal: `python -c "import sys; sys.path.insert(0,'03_lit'); import lit; print(lit.verify('<doi>', '<title>', '<first author>'))"`. Try one with a digit changed.

## What you have now

`results/values.csv` (every value with its quote, page and conditions), `results/answer.md` (the answer, with the hypotheses tested), `results/sources.bib` if it used searched papers (every DOI checked), and `results/check-log.txt`, the record of how the table was corrected, row by row. Stop 6's first recipe turns `pdfask.py` into a tool with your own columns for the documents you read every week, and its third turns `lit.py` into a digest of what is new on your topic.

## If something goes wrong

- The search says it used a saved answer, or that OpenAlex did not answer. OpenAlex limits free searches per network address, and the whole room shares a few. The three topics in `python 03_lit/lit.py --topics` always work offline. Tell the agent: `Use only the papers you have and the search topics listed by python 03_lit/lit.py --topics.` Checking DOIs in Crossref is not limited.
- A DOI comes back `missing` with a note that another agency registered it. It is real but not a Crossref DOI (Zenodo, arXiv and DataCite use their own); it cannot be checked here.
- `pages.py` says a PDF has almost no text. It is a scan: a picture of pages. Nothing in it can be read or checked here. Use your other papers, or the shipped ones (`question.md`).
- A quote keeps failing on a paper whose text comes out jumbled (two columns, equations, tables). The checker can only match what `pages.py` printed. Tell the agent: `Copy the quote from python 03_lit/pages.py output for that page, or flag the row and say so.`
- The agent stops with rows still failing. Type: `Run python 03_lit/check_values.py and fix or flag every failing row.`
- The model service is slow or down. A saved run on the shipped papers is in `03_lit/saved/`. Click `03_lit/saved/values.csv`, `03_lit/saved/check-log.txt` and `03_lit/saved/answer.md` (read `03_lit/saved/README.md` first), and do steps 4 and 5 on those files: the papers' text is in `03_lit/saved/papers/`. To see every row's check, in the second terminal: `python 03_lit/check_values.py 03_lit/saved/values.csv`. One row, line 30, fails: read why.
- The agent edits `lit.py`, `pages.py` or `check_values.py`, or writes its own search code. Tell it: `Use the 03_lit tools as they are.` In the second terminal, `git checkout 03_lit/check_values.py 03_lit/pages.py 03_lit/quotes.py 03_lit/lit.py` restores the tools and leaves your `question-mine.md` as you edited it.
- The chat gets slow and forgetful. Type `/new`, then, for the shipped question: `Read 03_lit/question.md and the files it has written in results/ so far, then continue.` For your own papers: `Read 03_lit/question-mine.md and the files it has written in results/ so far, then continue.`
