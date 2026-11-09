# Stop 6: Build one thing from your week

The morning made one-off things: an analysis of a dataset, a research question answered from papers with every value checked against its page, a chart read back into data. This stop turns one of them into a tool you will run again on Monday, on your own material. You pick a recipe, start from its working starter, adapt it with the agent, and then test it on an input it has never seen, including one that is wrong on purpose. At 5:00 you leave with a program, not a chat.

About 95 minutes, from 2:25. Folder: `06_build/`. You type requests into `openclaw chat`, in the terminal at the bottom, and run your tool in a second terminal (the **+** at the top right of the terminal panel). Open every file it makes by clicking it in the Explorer.

## You will be able to

- Turn something you did once today into a program that runs on a new input with one command.
- Test it on an input the agent never saw, and on a bad one, and say what it did with each.
- Leave with everything needed to run it after today: the code, a sample input, the command, the expected output, and your own key.

## Pick one on your card before lunch (if unsure, the first)

Each recipe has a starter that already runs, a sample input, a bad input, an unseen input for the 3:15 swap, and a minimum result that counts as done. The bad inputs write their results beside your good ones, never over them.

1. A folder-to-table tool, on Stop 3's rule that a value counts only with the sentence it rests on. A folder of the documents you read every week (papers, reports, proposals, protocols, theses) becomes a table with the columns you choose. For every value the table has the quoted sentence, the page where the program found it, and a check: `yes` (the quote is there word for word), `NO` (a quote that is not in the document), `not stated` (the document does not say, and the model said so) or `UNSUPPORTED` (a value with no quote at all: treat it as unchecked).
   - Starter: `python 06_build/table/build_table.py corpus/papers`. Click `results/build/table.csv` to read it.
   - Your columns: `06_build/table/fields.json`, one line each: a name and the sentence the model reads to fill it.
   - Bad input: `python 06_build/table/build_table.py 06_build/table/bad --out results/build-bad` (an empty file, meeting minutes that are not a study, a spreadsheet). It writes `results/build-bad/`, so your good table stays.
   - Qualitative material works the same way: `python 06_build/table/build_table.py 06_build/table/interviews 06_build/table/fields-interviews.json` codes three invented interview transcripts (role, main barrier, workaround, support wanted, sentiment), each code with the sentence it rests on. Do you agree with every code?
   - Unseen input for 3:15: a folder of your partner's documents, or the interviews if they have none.
   - Done: your own columns, run on a folder of at least three documents of yours or the shipped ones, with the table in `results/build/table.csv`, and one row's quotes found by you in the document (a `yes` means the sentence is there, not that it supports the value).

2. A page for your dataset, from Stop 2. Your report and figures become one web page, a single file you can email or put on a lab site.
   - Starter, in the second terminal: `python results/analysis.py > results/analysis-output.txt` (so the page can check the report's numbers against what the script printed), then `python 06_build/page/make_page.py --title "Your dataset"`. It reads `results/report.md` and `results/figures/` and writes `results/page/index.html`. No Stop 2 analysis of your own: `bash catchup.sh s6` copies in a `results/analysis.py` that reruns the finished penguins analysis, with its report and figures; then the same two commands work.
   - To look at the page: right-click `results/page/index.html` in the Explorer, choose Download, and open it on your laptop. Clicking it in the Codespace shows the HTML source, not the page.
   - It refuses to write the page if the report names a figure that does not exist, or (when `results/analysis-output.txt` exists) has a number with three or more significant digits that the script never printed (rounding allowed). It catches figures and numbers typed in by hand, not every slip: it ignores signs and shorter numbers, so check one number yourself as in Stop 2. The page's footer says which checks ran.
   - Bad input: `python 06_build/page/make_page.py --from 06_build/page/bad --out results/page-bad`, a shipped report that names a missing figure and has a number typed by hand. It must say NOT WRITTEN and name both.
   - Unseen input for 3:15: another finished analysis, shipped with the datasets. `python 02_data/datasets/stillwater-weather/reference/analysis.py > results/weather-output.txt`, then `python 06_build/page/make_page.py --from 02_data/datasets/stillwater-weather/reference --output results/weather-output.txt --out results/page-weather --title "Stillwater weather"` (if your page is the weather data, use `oklahoma-wheat` instead).
   - Done: `results/page/index.html` built from a fresh run of `results/analysis.py`, with the number check passing. Public only if the data may be public: `mkdir -p site/data && cp results/page/index.html site/data/index.html`.

3. A literature digest, built on Stop 3's search tool `03_lit/lit.py`. Your searches become a script that lists what is new on your topic since last time, with each paper verified against Crossref.
   - Starter: `python 06_build/digest/digest.py`, with the query saved in the file (cover crops and soil carbon). Then put your own query in `QUERY` near the top of `06_build/digest/digest.py`, or try it first: `python 06_build/digest/digest.py "your query"`. Each run shows only papers no earlier run showed you, among the 25 best matches from this year and last, and writes a new `results/digest-<date>.md` (a second run the same day writes `digest-<date>-2.md`; no digest is overwritten).
   - Bad input, from saved answers so it needs no network: `python 06_build/digest/digest.py --records 06_build/digest/fixtures/no-match.json` (a misspelled query that matches nothing: it must say so and change nothing) and `python 06_build/digest/digest.py --records 06_build/digest/fixtures/no-abstract.json` (papers with no abstract: it must say so, not invent a summary). These write `results/digest-test-<date>.md` and leave your list of seen papers alone.
   - Unseen input for 3:15: your partner's topic, as a query.
   - Done: a manually runnable script with your query saved in it, writing `results/digest-<date>.md`. Running it every Monday on its own is a Thursday task: the line to schedule it is at the end of its output.

Or your own idea, if a helper agrees it fits in an hour.

## Do it

1. Run the starter as it is, on its sample input. Read what it prints. This is the baseline: it works before you change anything.

2. Adapt it with the agent. In `openclaw chat`, say which recipe and what you want. For example:

   ```
   Read 06_build/table/build_table.py and 06_build/table/fields.json. Change the columns
   for grant proposals: aims, budget total, duration, and the funder. Run it on mine/.
   ```

   Read its changes before you accept the result: `git diff 06_build/`, in the second terminal, shows exactly what it edited (press `q` to leave it).

3. A first working result by 3:15, on your own input or a shipped one.

4. The transfer test, at 3:15. Swap with your pair. You run their tool and they run yours, cold: from the comment at the top of the file alone, with no agent and no explaining, first on the recipe's unseen input (above), then on its bad input. Write on your card what their tool did with each: a right answer, a wrong answer, an honest "not stated" or error, or a crash, and where the comment at the top left you stuck. Then swap back and fix the comment.

5. Make it yours to keep. Done means all five of these are in your repository:
   - the code, saved;
   - the libraries it needs, listed in `requirements.txt` (check `git diff requirements.txt`: if the agent installed one, add it there);
   - a small sample input it runs on, saved beside the code in `06_build/<recipe>/sample/`, and only one that may be public: your repository on GitHub may be public, and `mine/` is never committed. A shipped paper or dataset is always fine;
   - a sample command, in a comment at the top of the file, and what it should print, pasted below it;
   - the two lines that make it run on your own key after today (below).

   First make sure `results/` holds your good result, not a test: if you ran anything in place of it, run your tool on its good input once more. Then, in the second terminal, commit and push the code, including Stop 5's repaired script:

   ```
   git add 05_repair 06_build requirements.txt
   git commit -m "my tool, and the repaired script"
   git push
   bash export.sh
   ```

   `git push` keeps the code in your repository on GitHub; `bash export.sh` packs `results/` into one zip: right-click it in the Explorer and Download it.

6. Show and tell, at 4:00. Show your pair your tool running on their file, and watch theirs on yours. Then volunteers nominate what they saw in their partner's work, and the nominee shows it to the room from their seat. Nobody presents their own work. If you want what you showed to be public, copy it into `site/share/` (public on your site at once; nothing from your own data unless it could go on a conference slide), then `bash gallery.sh` posts a card linking to your site.

## After today: your own key

The workshop key stops working at 5:00. Your tool keeps working with your own key in `.env`, two lines:

```
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_API_KEY=sk-or-...your key...
```

Those two lines are for an OpenRouter key. Make one at openrouter.ai (Keys, then Create key; give it a credit limit), or an NVIDIA key at build.nvidia.com. Then run `bash setup.sh --reset-key` and paste it: setup recognizes either kind (`sk-or-` or `nvapi-`) and writes the two lines for you, with NVIDIA's address instead of OpenRouter's for an `nvapi-` key.

## Checkpoint

Tell your pair what their tool did on your input and on its bad input, and where its comment left you stuck.

## If something goes wrong

- The starter fails before you change anything. Run `python 00_setup/check.py`: if the model is not reachable, nothing else will work. Then ask a helper.
- The agent rewrote more than you asked. `git diff 06_build/` shows it; `git checkout 06_build/<file>` puts one file back as it was.
- Your documents are scans. The model cannot read a page that is a picture. Use the shipped papers for the build, and keep the scans for later.
- The page recipe says a number is not in the script's output. Either the report has a number typed by hand, or the output file is old: run `python results/analysis.py > results/analysis-output.txt` and try again. If that command says there is no `results/analysis.py`, run `bash catchup.sh s6` first.
- You run out of time. Commit what runs, and write the next step as a comment at the top of the file. A small tool that runs beats a large one that almost does.
