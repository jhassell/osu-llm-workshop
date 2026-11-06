# Stop 6: Build one thing from your week

The morning made one-off things: an analysis, an evidence table, a chart read back into data. This stop turns one of them into a tool you will run again on Monday, on your own material. You pick a recipe, start from its working starter, adapt it with the agent, and then test it on an input it has never seen, including one that is wrong on purpose. At 5:00 you leave with a program, not a chat.

About 95 minutes, from 2:25. Folder: `06_build/`. You type in `openclaw chat` and in a terminal.

## You will be able to

- Turn something you did once today into a program that runs on a new input with one command.
- Test it on an input the agent never saw, and on a bad one, and say what it did with each.
- Leave with everything needed to run it after today: the code, its sample input, the command, the expected output, and your own key.

## Pick one on your card before lunch (if unsure, the first)

Each recipe has a starter that already runs, a sample input, a bad input, and a minimum result that counts as done.

1. A folder-to-table tool, from Stop 3. A folder of the documents you read every week (papers, reports, proposals, protocols, theses) becomes a table with the columns you choose, every value with a quoted sentence and a found or not-found check.
   - Starter: `python 06_build/table/build_table.py corpus/papers`
   - Your columns: `06_build/table/fields.json`, one line each: a name and the sentence the model reads to fill it.
   - Bad input: `06_build/table/bad/` (an empty file, meeting minutes that are not a study, a spreadsheet).
   - Qualitative material works the same way: `python 06_build/table/build_table.py 06_build/table/interviews 06_build/table/fields-interviews.json` codes three invented interview transcripts (role, main barrier, workaround, support wanted, sentiment), each code with the sentence it rests on. Do you agree with every code?
   - Done: your own columns, run on a folder of at least three documents of yours or the shipped ones, with the table in `results/build/table.csv` and every "found" spot-checked for one row.

2. A page for your dataset, from Stop 2. Your report and figures become one web page, a single file you can email or put on a lab site.
   - Starter: first `python results/analysis.py > results/analysis-output.txt` (so the page can check the report's numbers against what the script printed), then `python 06_build/page/make_page.py --title "Your dataset"` (it reads `results/report.md` and `results/figures/`). No Stop 2 report yet: `bash catchup.sh s6` copies in the finished penguins one.
   - It refuses to write the page if the report names a figure that does not exist, or (when `results/analysis-output.txt` exists) has a number of three or more digits that the script never printed (rounding allowed). It catches figures typed in by hand, not every slip: it ignores signs and one- or two-digit numbers, so check one number yourself as in Stop 2.
   - Bad input: delete one figure the report names, and run it again.
   - Done: `results/page/index.html` built from a fresh run of `results/analysis.py`, with the number check passing. Public only if the data may be public: `mkdir -p site/data && cp results/page/index.html site/data/index.html`.

3. A literature digest, from Stop 3. Your search becomes a script, built on Stop 3's `03_lit/lit.py`, that lists what is new on your topic since last time, with each paper verified against Crossref.
   - Starter: `python 06_build/digest/digest.py "your query"`. Each run shows only papers no earlier run showed you, among the 25 best matches from this year and last.
   - Bad input: a query with a typo that matches nothing, and a paper with no abstract (it must say so, not invent a summary).
   - Done: a manually runnable script with your query saved in it, writing `results/digest-<date>.md`. Running it every Monday on its own is a Thursday task: the line to schedule it is at the end of its output.

Or your own idea, if a helper agrees it fits in an hour.

## Do it

1. Run the starter as it is, on its sample input. Read what it prints. This is the baseline: it works before you change anything.

2. Adapt it with the agent. In `openclaw chat`, say which recipe and what you want. For example:

   ```
   Read 06_build/table/build_table.py and fields.json. Change the columns for grant
   proposals: aims, budget total, duration, and the funder. Run it on mine/.
   ```

   Read its changes before you accept the result: `git diff 06_build/` shows exactly what it edited.

3. A first working result by 3:15, on your own input or a shipped one.

4. The transfer test, at 3:15. Run your tool on an input the agent has not seen, without the agent: a document, dataset or query you did not use while building it. Then on the bad input. Write on your card what it did with each: a right answer, a wrong answer, an honest "not stated" or error, or a crash.

5. Make it yours to keep. Done means all five of these are in your repository:
   - the code, saved;
   - the libraries it needs, listed (they are all in `requirements.txt` unless the agent added one);
   - a sample command, in a comment at the top of the file;
   - what that command should print, pasted below it;
   - the two lines that make it run on your own key after today (below).

   Commit and push the code, including Stop 5's repaired script: `git add 05_repair 06_build`, `git commit -m "my tool, and the repaired script"`, `git push`. Then take your results home: `bash export.sh` packs `results/` into one zip to download.

6. Post it to the wall, if you want to. Copy what you would put on a slide into `site/share/` (it is public on your site at once; nothing from your own data unless it could go on a conference slide), then `bash gallery.sh`, which posts a card linking to your site.

## After today: your own key

The workshop key stops working at 5:00. Your tool keeps working with your own key in `.env`, two lines:

```
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_API_KEY=sk-or-...your key...
```

Make a key at openrouter.ai (Keys, then Create key; give it a credit limit), or an NVIDIA key at build.nvidia.com. Then run `bash setup.sh --reset-key` and paste it: setup recognizes either kind (`sk-or-` or `nvapi-`) and writes the two lines for you.

## Checkpoint

Show your pair the bad input and what your tool did with it.

## If something goes wrong

- The starter fails before you change anything. Run `python 00_setup/check.py`: if the model is not reachable, nothing else will work. Then ask a helper.
- The agent rewrote more than you asked. `git diff 06_build/` shows it; `git checkout 06_build/<file>` puts one file back as it was.
- Your documents are scans. The model cannot read a page that is a picture. Use the shipped papers for the build, and keep the scans for later.
- The page recipe says a number is not in the script's output. Either the report has a number typed by hand, or the output file is old: run `python results/analysis.py > results/analysis-output.txt` and try again.
- You run out of time. Commit what runs, and write the next step as a comment at the top of the file. A small tool that runs beats a large one that almost does.
