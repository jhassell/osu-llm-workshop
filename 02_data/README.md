# Stop 2: Your data, analyzed and reproducible

You hand the agent a CSV and three short requests. It explores the data, makes the plots that answer your question, writes a report, and then turns all of it into one script that rebuilds every figure and every number from the raw file. In between, you check one number yourself. What you keep is not the chat: it is `results/analysis.py`, a program that runs again next Thursday on next month's data.

About 70 minutes, from 9:35. Folder: `02_data/`. You type in `openclaw chat`.

## You will be able to

- Say in four lines what one row of your data is, what you are measuring, what you are comparing, and what else could explain a difference.
- Get from a raw CSV to figures and a short report with numbers that come from a script, not from the chat.
- Check one number yourself, and say which rows the agent dropped and why.
- Rerun the whole analysis with one command.

## The idea

A chat can describe a dataset. An agent with a terminal can do the analysis: it writes Python, runs it, reads the error, fixes it, and runs it again, in your folder, leaving files you can open. That is the difference from the chat box, and it is also the risk. A fluent report can rest on a filter you never asked for, a unit it guessed, or a number it typed in from memory instead of reading it off the script's output.

So the stop has two rules. First, every number in the report comes from the script's printed output, never retyped. Second, one number is checked by you, not by the agent: the row count, the units, and one average or total you compute yourself. If yours and the report's disagree, that is the most useful thing that happens this hour.

The deliverable is the script. Figures and a report are easy to make once; a script that rebuilds them from the raw file is what makes the work reproducible, and it is what you take home.

Everything is written to `results/`, which is never committed: what the agent builds from your data can contain your data. To keep a copy, `bash export.sh` packs `results/` into one zip to download. To show something to the room, look at it first, then copy it into `site/share/`: it is public on your site at once.

## Before you start

- Your data. If you brought a CSV, it is in `mine/` and `python upload_check.py` said it is ready. If not, or if it is not ready after three minutes, use a shipped dataset and come back to yours in Stop 6:

  ```
  ls 02_data/datasets
  ```

  Each folder holds the raw CSV, a `DICTIONARY.md` that says what every column means, a `SOURCE.md`, and a finished `reference/` to compare against at the end. Do not open `reference/` yet.

- Read the dictionary (or your own notes on your columns). The agent will guess at what a column means if you do not tell it.

## Four lines first

On your card, before any prompt, in your own words:

1. One row is a what? (a day at one weather station; one penguin; one county in one year)
2. The outcome: what is measured, with its unit.
3. The comparison: what you want to see the outcome against (a group, a time, another measurement).
4. One thing other than your comparison that could explain a difference you see.

These lines are your question. They go into the prompts below, and at the end you check the report against them. Each shipped dataset has a worked example in its `FOUR-LINES.md`; write yours before you read it.

## First, from the front: a weak prompt and a strong one

The instructor gives the agent the same CSV twice. First: `Analyze this CSV.` Then the prompt in step 2 below. Watch what changes: which question it answers, which rows it keeps, whether its numbers can be traced to anything. Most of what is called prompt engineering is in that difference: say what the data is, what you want compared, what it must not do silently, and what must be left behind to check.

## Do it

1. Open OpenClaw's chat (`openclaw chat`). If it was open from the website exercise, that is fine.

2. Prompt one, the exploration. Put your file and your four lines in it:

   ```
   Explore 02_data/datasets/<name>/<file>.csv. Report its shape, missing values and
   suspicious rows. Do not drop any rows unless you state the filter and the row count
   before and after. Then make the three plots that best show <outcome> against
   <comparison>, save them in results/figures/, and write results/report.md. Every
   number in the report must come from the script's printed output, not be retyped.
   ```

   Watch the tool calls. Each `exec` line is Python it runs. Look for three things: what it does about missing values (drops the rows, fills them, or says nothing), what it decides the units are, and whether any number in its answer appears in no output.

3. Open what it made: `results/report.md` (right-click, Open Preview) and the three figures in `results/figures/`. Do the plots answer your four lines, or a question it chose instead?

4. Prompt two is yours, not the agent's: the independent check. In a second terminal (the **+** on the terminal panel), count the rows and recompute one number from the report by hand, with a one-line Python command. For example:

   ```
   python -c "import pandas as pd; d = pd.read_csv('02_data/datasets/<name>/<file>.csv'); print(len(d)); print(d.groupby('<comparison>')['<outcome>'].mean())"
   ```

   Put in the outcome and comparison column names you wrote on the card. This form fits a comparison of groups, as in the weather data (wet days against dry). If your comparison is a continuous column (penguins: bill length) or the file is in long format with numbers stored as text (the wheat data), use the one-line check in that dataset's `reference/report.md` instead, after you have made your own.

   Compare with the report. Do the row counts match? If not, the agent dropped or filtered rows: find in its tool calls where and why. Do the units in the report match the dictionary? Write your number and the report's on the card, then explain to your partner in a minute how you checked it.

5. Prompt three, the deliverable:

   ```
   Turn everything into results/analysis.py that rebuilds every figure and every
   number in the report from the raw file. Run it. The report must match what it prints.
   ```

6. Run it yourself, in the second terminal:

   ```
   python results/analysis.py
   ```

   It should rebuild the figures and print the numbers in the report. Change nothing and run it twice: same output both times?

## The debrief, from the front

The instructor shows a screenshot of a chat box given the same CSV: a good answer (in testing, Grok matched the reference numbers and even caught the Simpson's paradox), but nothing in your folder: no script to inspect, rerun on next month's data, or show a reviewer. That is step one of the day's three: a chat box, an agent in your folder, an agent on your campus cluster. You just did step two: an agent in your folder that left `results/analysis.py`. Step three is the same agent with its model on OSU's Cimarron cluster, in Stop 5, if Cimarron is up.

## Checkpoint

`python results/analysis.py` reproduces the report. One number in the report matches your hand check. You can say which rows the agent dropped and why. Show your pair the script, one figure, and the number you checked.

## Extensions

1. Compare with the finished reference. `ls 02_data/datasets/<name>/reference/`. Run its `analysis.py`. Where does the agent's analysis differ from it, and which choice would you defend?
2. The rehearsed next step, on the shipped datasets only. Each dataset's `reference/extension.py` runs one test, regression or trend that suits that data, and says its assumptions. Ask the agent for the same analysis, then compare its choice of model with the reference. On your own data, the right model is a question for you, not for a one-hour stop: write it down for Thursday.
3. Ask for a methods paragraph: `Write a methods paragraph for this analysis, citing results/analysis.py.` It is a draft for you to correct, never text to paste. Check every number and every claim about what was done against the script.
4. Make it break. Ask the agent to run the script on a copy of the CSV with ten rows deleted. Does the report notice?

## What you have now

`results/analysis.py`, `results/report.md` and `results/figures/`: a small analysis that rebuilds from the raw file with one command. The habits carry through the day: write the question before the prompt, read the tool calls rather than the summary, and check one number yourself. Stop 6 can turn it into a page for your dataset, or you can point it at the numbers Stop 4 reads off a chart.

## If something goes wrong

- The agent says a library is missing (`No module named pandas`). The Codespace image has pandas, numpy, matplotlib, scipy, statsmodels and seaborn. If it still says so, run `python -c "import pandas"` in a terminal; if that fails, run `bash setup.sh`, which repairs the libraries.
- It installs packages with `pip install`. It does not need to. Tell it: `Use the libraries already installed: pandas, matplotlib, scipy, statsmodels, seaborn.`
- Your CSV will not load: an encoding error, one column instead of many, or a header on the third line. Tell the agent what you know (`the file is separated by semicolons`, `the header is on line 3`). If three minutes pass, switch to a shipped dataset.
- The figures are empty or all on one point. Usually the outcome column was read as text. Ask: `Which columns did you read as numbers?`
- The report has a number the script never printed. Tell it: `Which line of output does each number in the report come from?` Then fix or remove the ones without a line.
- It takes a long time, or OpenClaw shows an error such as 429 or a timeout. The whole room calls the same model. Wait a minute rather than repeating the request; if it gave up, type `Continue.`
- The chat gets slow and starts forgetting what it did. A long session fills the model's context. Type `/new` to start fresh, then: `Read results/analysis.py and results/report.md, then continue.`
