# Stop 2: Your data, analyzed and reproducible

You give the agent a data file. First it hunts for what is wrong with the file and shows the evidence. Then it makes plots and a report. You check one number yourself and tell it what you found. At the end it writes one script that rebuilds everything from the raw file. The script is what you keep.

About 70 minutes, from 9:35. You type in the OpenClaw chat, in the terminal at the bottom.

## You will be able to

- Have an agent find what is wrong with a data file, with evidence, before it analyzes anything.
- Check one number yourself, and correct the agent when it is wrong.
- Rebuild the whole analysis with one command.

## Why

An agent can write code, run it, read the result, and decide what to check next. That is what makes it useful on data, and also risky: a polished report can rest on rows it quietly dropped or a unit it guessed. So it investigates before it analyzes, every number in the report comes from the script's output, and you check one number yourself.

Everything goes into `results/`, which is never committed, because it can contain your data.

## Before you start

Pick your data. Your own CSV is in `mine/`, if `python upload_check.py` said it is ready. Otherwise use the air-handler file: in the Explorer, open `02_data`, `datasets`, `hvac-ahu`. It is two weeks of readings from a building's air handler, and several things in it are wrong. Click `DICTIONARY.md` to learn what each column means.

On your card, write four lines:

1. One row is a what? (one 5-minute reading from the air handler)
2. What is measured, with its unit?
3. What do you want to compare it against?
4. What else could explain a difference?

## Do it

1. Read the prompt. Click `02_data/investigate.md`. It asks the agent to find every problem in the file, show the evidence, decide what to do about each, and then make the plots and report.

   Your own CSV? Click `02_data/investigate-mine.md` instead, replace each [BRACKET] with your file and your four lines, and save (Cmd-S, or Ctrl-S).

2. Hand it over. In the chat, type and press Enter:

   ```
   Read 02_data/investigate.md and do what it says.
   ```

   (Use `investigate-mine.md` for your own file.) Watch the boxes: each `exec` is Python it wrote and runs, each `write` saves a file. Notice when one result sends it to look somewhere new.

3. Read what it found. A `results` folder appears in the Explorer. Click `results/findings.md`: is there evidence for each problem, and do you agree with each decision? Then click `results/report.md` and the pictures in `results/figures/`.

4. Check one number yourself. Open a second terminal with the + at the top right of the terminal panel (the chat keeps running in the first). Copy this line with the Copy button, paste it, and press Enter:

   ```
   python -c "import pandas as pd; d=pd.read_csv('02_data/datasets/hvac-ahu/ahu_trend_2017-09-25_to_2017-10-08.csv'); print(len(d), d.duplicated().sum()); print(d.groupby(d.Datetime.str[:10]).OA_TEMP.median())"
   ```

   It prints the row count, the number of duplicated rows, and the outdoor temperature for each day. Does anything look wrong that the findings do not mention?

   Your own CSV: put in your file name and two column names from your card:

   ```
   python -c "import pandas as pd; d=pd.read_csv('mine/<file>.csv'); print(len(d)); print(d.groupby('<comparison>')['<outcome>'].mean())"
   ```

5. Tell the agent what you found. Back in the chat, say it in your own words and add one instruction, for example:

   ```
   My check shows the outdoor temperature on 2017-09-30 and 2017-10-01 is about 12, against 44 to 70 on every other day. Read 02_data/revise.md and do what it says.
   ```

   If everything matched, say so: `My check agrees with your numbers. Read 02_data/revise.md and do what it says.`

   Read its answer before you accept it. It may explain your number away, as a cold snap for example. You know the subject, so push back in one line with your reason:

   ```
   Chicago is never 12 F at the end of September, and the change starts and stops at midnight. Treat it as a unit change and test that.
   ```

6. Make it reproducible. In the chat:

   ```
   Read 02_data/reproduce.md and do what it says.
   ```

   It writes `results/analysis.py`, a script that rebuilds the figures and the report from the raw file. Click it to read it.

7. Run it yourself, in the second terminal:

   ```
   python results/analysis.py
   ```

   Click `results/report.md` again. Run the script a second time: same result?

## Checkpoint

`python results/analysis.py` rebuilds the report. Show your pair one problem the agent found, with its evidence, and what it did with your check.

## Extensions

1. Compare with a finished analysis. The penguins, weather and wheat datasets each have a `reference/` folder with a report and a script. Run one, for example `python 02_data/datasets/penguins/reference/analysis.py`, and compare its choices with the agent's.

2. Make it break. Ask the agent to run the script on a copy of the file with ten rows deleted. Does the report's row count change?

## Other datasets

Each has its own prompt (`investigate-penguins.md`, `investigate-weather.md`, `investigate-wheat.md`) and its own check:

```
python -c "import pandas as pd; d=pd.read_csv('02_data/datasets/penguins/penguins_raw.csv'); print(len(d)); print(d.groupby('Species')['Culmen Depth (mm)'].mean())"
python -c "import pandas as pd; d=pd.read_csv('02_data/datasets/stillwater-weather/stillwater_daily_2021-2025.csv'); print(len(d)); d=d.dropna(subset=['TMAX','PRCP']); print(len(d)); print(d.groupby(d.PRCP>=0.01).TMAX.mean())"
python -c "import pandas as pd; d=pd.read_csv('02_data/datasets/oklahoma-wheat/ok_county_winter_wheat_2000-2025.csv', dtype=str); y=d[(d.YEAR=='2025')&(d.STATISTICCAT_DESC=='YIELD')&(d.PRODN_PRACTICE_DESC=='ALL PRODUCTION PRACTICES')&(d.COUNTY_CODE!='998')]; print(len(y), y.VALUE.astype(float).mean())"
```

## If something goes wrong

- No `results` folder yet: the agent is still working, or the line went to a `$` prompt instead of the chat. Type `openclaw chat` and send it again.
- It runs `pip install`: tell it `Use the libraries already installed: pandas, matplotlib, scipy, statsmodels, seaborn.`
- Your CSV will not load: tell it what you know (`the file is separated by semicolons`, `the header is on line 3`). After three minutes, switch to the air-handler file.
- A number in the report appears in no output: ask `Which line of output does each number come from?`
- 429 or a timeout: the room shares one model. Wait a minute, then type `Continue.`
- The chat gets slow and forgetful: type `/new`, then `Read results/findings.md, results/analysis.py and results/report.md, then continue.` Tell it your check again.
