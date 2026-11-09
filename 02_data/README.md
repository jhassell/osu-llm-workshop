# Stop 2: Your data, analyzed and reproducible

You hand the agent a CSV and three short requests, each a file you read before you send it. First it investigates: it finds what is wrong with the file, proves each problem with code, and decides what to do about it. Then it makes the plots that answer your question, writes a report, and turns all of it into one script that rebuilds every figure and every number from the raw file. In between, you check one number yourself and tell the agent what your check showed. What you keep is not the chat: it is `results/analysis.py`, a program that runs again next Thursday on next month's data.

About 70 minutes, from 9:35. Folder: `02_data/`. You type in `openclaw chat`.

## You will be able to

- Say in four lines what one row of your data is, what you are measuring, what you are comparing, and what else could explain a difference.
- Have the agent find what is wrong with a file, with the evidence for each problem, before it analyzes anything.
- Get from a raw CSV to figures and a short report with numbers that come from a script, not from the chat.
- Check one number yourself, and say which rows the agent dropped and why.
- Rerun the whole analysis with one command.

## The idea

A chat can describe a dataset. An agent with a terminal can do the analysis: it writes Python, runs it, reads the error, fixes it, and runs it again, in your folder, leaving files you can open. That is the difference from the chat box, and it is also the risk. A fluent report can rest on a filter you never asked for, a unit it guessed, or a number it typed in from memory instead of reading it off the script's output.

So the agent investigates before it analyzes. It is not given a recipe; it is given a goal (find every problem, prove each one, decide what to do) and has to choose its own checks, read what they print, and decide what to look at next. That loop is what makes it an agent, and it is where it is most useful: duplicated rows, a unit that changes partway through, a sensor or instrument that stopped doing what it says.

The stop has two rules. First, every number in the report comes from the script's printed output, never retyped. Second, one number is checked by you, not by the agent: the row count, the units, and one average or total you compute yourself. If yours and the report's disagree, that is the most useful thing that happens this hour.

The deliverable is the script. Figures and a report are easy to make once; a script that rebuilds them from the raw file is what makes the work reproducible, and it is what you take home.

Everything is written to `results/`, which is never committed: what the agent builds from your data can contain your data. To keep a copy, `bash export.sh` packs `results/` into one zip to download. To show something to the room, look at it first, then copy it into `site/share/`: it is public on your site at once.

## Before you start

- Where things are. Everything in this stop happens in the Codespace window. The Explorer, the file list on the left (Cmd-Shift-E, or Ctrl-Shift-E on Windows, if it is hidden), shows every file: click one to open it. A `.md` file opens formatted, and each grey box of text to type has a Copy button at its top right. A `.png` opens as a picture and a `.csv` as coloured columns. The terminal panel at the bottom is where `openclaw chat` runs; you type into it and press Enter.

- Your data. If you brought a CSV, it is in `mine/` and `python upload_check.py` said it is ready. If not, or if it is not ready after three minutes, use a shipped dataset and come back to yours in Stop 6. In the Explorer, open `02_data`, then `datasets`. Each folder holds the raw CSV, a `DICTIONARY.md` that says what every column means, a `SOURCE.md`, and, for the last three, a finished `reference/` to compare against at the end. Do not open `reference/` yet. The first, `hvac-ahu`, is two weeks of trend data from a building's air handler, the kind of file a building automation system exports. Several things in it are wrong. Its answers are shown from the front at the end of the stop, so it has no `reference/`.

- Read the dictionary: click `DICTIONARY.md` (or read your own notes on your columns). The agent will guess at what a column means if you do not tell it.

## Four lines first

On your card, before any prompt, in your own words:

1. One row is a what? (one 5-minute reading from an air handler; a day at one weather station; one penguin; one county in one year)
2. The outcome: what is measured, with its unit.
3. The comparison: what you want to see the outcome against (a group, a time, another measurement).
4. One thing other than your comparison that could explain a difference you see.

These lines are your question. They go into the prompts below, and at the end you check the report against them. Each shipped dataset has a worked example in its `FOUR-LINES.md`; write yours before you read it.

## First, from the front: a weak prompt and a strong one

The instructor gives the agent the same CSV twice. First: `Analyze this CSV.` Then the prompt in `02_data/investigate.md`, the one you will send in step 2. Watch what changes: which question it answers, which rows it keeps, whether its numbers can be traced to anything. Most of what is called prompt engineering is in that difference: say what the data is, what you want compared, what it must not do silently, and what must be left behind to check.

## Do it

1. Open OpenClaw's chat: in the terminal at the bottom, type `openclaw chat` and press Enter. If it was open from the website exercise, that is fine.

2. Prompt one, the investigation. The prompt is a file, so you can read it before you send it. Click `02_data/investigate.md` in the Explorer: it is the strong prompt from the front, filled in for the air-handler file. Read what it asks for: the dictionary first, every problem with its evidence, a decision for each, nothing dropped silently, and numbers only from printed output.

   Another shipped dataset? Each has its own prompt, filled in the same way: `investigate-penguins.md`, `investigate-weather.md`, `investigate-wheat.md`. Your own CSV? Click `02_data/investigate-mine.md` instead, replace each [BRACKET] with your file and your four lines, and save it (Cmd-S, or Ctrl-S).

   Then, in the chat, type one line and press Enter:

   ```
   Read 02_data/investigate.md and do what it says.
   ```

   (with the name of the file you chose, if not the air handler's). The agent reads the file and starts. Watch the tool calls: each `exec` line is Python it wrote and runs, and each `write` saves a file. Count how many different checks it tries, and notice when one result sends it to look somewhere new. Look also for what it does about missing values (drops the rows, fills them, or says nothing), what it decides the units are, and whether any number in its answer appears in no output.

3. Open what it made. A `results` folder appears in the Explorer as it works. Click `results/findings.md` and `results/report.md`, and click each picture in `results/figures/`. For each problem in the findings, is there evidence you could show someone, and do you agree with the decision? Do the plots answer your four lines, or a question it chose instead?

4. Your own check, not the agent's. Open a second terminal with the **+** at the top right of the terminal panel; the chat keeps running in the first. Copy the line for your dataset from this page (in the preview) and paste it in, or type it, then press Enter. Each counts the rows and recomputes something the report should state.

   The air handler: the row count, the exact duplicate rows, and the outdoor temperature day by day.

   ```
   python -c "import pandas as pd; d=pd.read_csv('02_data/datasets/hvac-ahu/ahu_trend_2017-09-25_to_2017-10-08.csv'); print(len(d), d.duplicated().sum()); print(d.groupby(d.Datetime.str[:10]).OA_TEMP.median())"
   ```

   The weather: the row count, the days left once a blank high or blank rainfall is dropped, and the mean high on wet days against the rest.

   ```
   python -c "import pandas as pd; d=pd.read_csv('02_data/datasets/stillwater-weather/stillwater_daily_2021-2025.csv'); print(len(d)); d=d.dropna(subset=['TMAX','PRCP']); print(len(d)); print(d.groupby(d.PRCP>=0.01).TMAX.mean())"
   ```

   The penguins: the row count and the mean bill depth by species.

   ```
   python -c "import pandas as pd; d=pd.read_csv('02_data/datasets/penguins/penguins_raw.csv'); print(len(d)); print(d.groupby('Species')['Culmen Depth (mm)'].mean())"
   ```

   The wheat (numbers are stored as text, one statistic per row): the 2025 counties and their mean yield.

   ```
   python -c "import pandas as pd; d=pd.read_csv('02_data/datasets/oklahoma-wheat/ok_county_winter_wheat_2000-2025.csv', dtype=str); y=d[(d.YEAR=='2025')&(d.STATISTICCAT_DESC=='YIELD')&(d.PRODN_PRACTICE_DESC=='ALL PRODUCTION PRACTICES')&(d.COUNTY_CODE!='998')]; print(len(y), y.VALUE.astype(float).mean())"
   ```

   Your own CSV: put in your file and the outcome and comparison column names from your card. This form fits a comparison of groups; for a continuous comparison, print the row count and one mean.

   ```
   python -c "import pandas as pd; d=pd.read_csv('mine/<file>.csv'); print(len(d)); print(d.groupby('<comparison>')['<outcome>'].mean())"
   ```

   Compare with the report and the findings. Do the row counts match? If not, the agent dropped or filtered rows: find in its tool calls where and why. Do the units match the dictionary? Does your check show anything the findings do not mention? Write your number and the report's on the card, then explain to your partner in a minute how you checked it.

5. Tell the agent what your check showed. This is the step that catches what the agent missed. Click `02_data/revise.md` to read it: it asks the agent to rerun your check, investigate what it shows, and either fix what it missed or show why the report already agrees. Then, back in the chat (the first terminal), type what you found in your own words, followed by the same instruction, for example:

   ```
   My check shows the outdoor temperature on 2017-09-30 and 2017-10-01 is about 12, against 44 to 70 on every other day. Read 02_data/revise.md and do what it says.
   ```

   If your check agreed with everything, say that instead: `My check agrees with your row count and your numbers. Read 02_data/revise.md and do what it says.`

   Read its answer before you accept it. It may explain your number away, as a cold snap or a rare event; in our test run it did. You know your equipment and your place better than the model, so push back in one line, with your reason, as you would with a student, for example: `Chicago is never 12 F at the end of September, and the change starts and stops at midnight. Treat it as a unit change and test that.` Then check that its new explanation names the cause, not just the days.

6. The deliverable. Click `02_data/reproduce.md` to read it: the script must write the report itself, from the numbers it computes. Then, back in the chat:

   ```
   Read 02_data/reproduce.md and do what it says.
   ```

   `results/analysis.py` appears in the Explorer; click it to read the script the agent wrote, and find where it writes `results/report.md`.

7. Run it yourself, in the second terminal:

   ```
   python results/analysis.py
   ```

   It should rebuild the figures, rewrite `results/report.md` and print every number in it: click the report again and compare. Change nothing and run it twice: same output both times?

## The debrief, from the front

First, the air-handler file's answers: what was wrong with it, how each problem shows in the data, and a show of hands for how many each pair's agent found. Then whether anyone's agent "fixed" a fault by making it look normal, or dropped rows without saying so.

Then the instructor shows a screenshot of a chat box given the penguins file: a good answer (in testing, Grok matched the reference numbers and even caught the Simpson's paradox), but nothing in your folder: no script to inspect, rerun on next month's data, or show a reviewer. That is step one of the day's three: a chat box, an agent in your folder, an agent on your campus cluster. You just did step two: an agent in your folder that left `results/analysis.py`. Step three is the same agent with its model on OSU's Cimarron cluster, in Stop 5, if Cimarron is up.

## Checkpoint

`python results/analysis.py` reproduces the report. One number in the report matches your hand check. You can say which rows the agent dropped and why, show one problem it found with the evidence for it, and say what the agent did with your check. Show your pair the findings, the script, one figure, and the number you checked.

## Extensions

1. Compare with the finished reference (penguins, weather, wheat; the air-handler file's is shown from the front). In the Explorer, open `02_data/datasets/<name>/reference/`, click `report.md` and the figures, then run its `analysis.py` in the second terminal (`python 02_data/datasets/<name>/reference/analysis.py`). Where does the agent's analysis differ from it, and which choice would you defend?
2. The rehearsed next step, on the penguins, weather and wheat files only. Each of their `reference/extension.py` runs one test, regression or trend that suits that data, and says its assumptions. Ask the agent for the same analysis, then compare its choice of model with the reference. On your own data, the right model is a question for you, not for a one-hour stop: write it down for Thursday.
3. Ask for a methods paragraph: `Write a methods paragraph for this analysis, citing results/analysis.py.` It is a draft for you to correct, never text to paste. Check every number and every claim about what was done against the script.
4. Make it break. Ask the agent to run the script on a copy of the CSV with ten rows deleted. The report is rewritten by the script, so its row count should change: does it?

## What you have now

`results/findings.md`, `results/analysis.py`, `results/report.md` and `results/figures/`: what was wrong with the file and a small analysis that rebuilds from the raw file with one command. The habits carry through the day: write the question before the prompt, have the agent investigate before it analyzes, read the tool calls rather than the summary, and check one number yourself. Stop 6 can turn it into a page for your dataset, or you can point it at the numbers Stop 4 reads off a chart.

## If something goes wrong

- The agent says a library is missing (`No module named pandas`). The Codespace image has pandas, numpy, matplotlib, scipy, statsmodels and seaborn. If it still says so, run `python -c "import pandas"` in a terminal; if that fails, run `bash setup.sh`, which repairs the libraries.
- It installs packages with `pip install`. It does not need to. Tell it: `Use the libraries already installed: pandas, matplotlib, scipy, statsmodels, seaborn.`
- Your CSV will not load: an encoding error, one column instead of many, or a header on the third line. Tell the agent what you know (`the file is separated by semicolons`, `the header is on line 3`). If three minutes pass, switch to a shipped dataset.
- The figures are empty or all on one point. Usually the outcome column was read as text. Ask: `Which columns did you read as numbers?`
- The report has a number the script never printed. Tell it: `Which line of output does each number in the report come from?` Then fix or remove the ones without a line.
- It takes a long time, or OpenClaw shows an error such as 429 or a timeout. The whole room calls the same model. Wait a minute rather than repeating the request; if it gave up, type `Continue.`
- The chat gets slow and starts forgetting what it did. A long session fills the model's context. Type `/new` to start fresh, then: `Read results/findings.md, results/analysis.py and results/report.md, then continue.` (After `/new` the agent has forgotten your check: tell it again.)
