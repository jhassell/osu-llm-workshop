# Stop 2: Your data, analyzed and reproducible

An agent investigates a data file and shows you what is wrong with it. You check one thing yourself and correct it where you know better. Then it writes one script that rebuilds the whole analysis from the raw file. The script is what you keep.

About 70 minutes, from 9:35. You type in the OpenClaw chat (the terminal at the bottom) and run commands in a second terminal.

## You will be able to

- Have an agent investigate a data file, with evidence, before it analyzes anything.
- Check its work yourself, and correct it with what you know.
- Rebuild the whole analysis with one command.

## The data

Everyone uses the same file: two weeks of 5-minute readings from one air handler, the unit that heats, cools and ventilates a floor of a building. It is in `02_data/datasets/hvac-ahu/`. Several things in it are wrong. Click `DICTIONARY.md` there to see what each column means.

Open a second terminal now with the + at the top right of the terminal panel. The chat stays in the first.

## Do it

1. Investigate. Click `02_data/investigate.md` to read what you are asking for. Then, in the chat, type:

   ```
   Read 02_data/investigate.md and do what it says.
   ```

   It takes about two minutes. Watch the boxes: each `exec` is Python it wrote and runs. Then click `results/findings.md`. Is there evidence for each problem?

2. Check it yourself. In the second terminal:

   ```
   python 02_data/check.py
   ```

   It prints the row count, the repeated rows, and the outdoor temperature each day. Does anything look wrong that the findings do not mention?

3. Correct it. If the findings already cover what you saw, skip this step. Otherwise tell the agent what you know, with your reason, in the chat:

   ```
   Sep 30 and Oct 1 are in Celsius: Chicago is never 12 F in late September, and it changes at midnight. Verify, convert, and update findings.md.
   ```

4. Build the script. Click `02_data/reproduce.md` to read it. Then, in the chat:

   ```
   Read 02_data/reproduce.md and do what it says.
   ```

   When it is done, run the script yourself in the second terminal:

   ```
   python results/analysis.py
   ```

   Click `results/report.md` and `results/figures/tracking.png`. Every number in the report came from the script, and the script runs without the agent.

## Checkpoint

Show your pair one problem the agent found, with its evidence, and run `python results/analysis.py` for them.

## Extensions

1. Your own CSV, in `mine/`. Click `02_data/investigate-mine.md`, fill in the brackets, save (Cmd-S, or Ctrl-S), and send `Read 02_data/investigate-mine.md and do what it says.`
2. Make it break. Ask the agent to run the script on a copy of the file with ten rows deleted. Does the report change?

## If something goes wrong

- No `findings.md` after a few minutes: look at the chat. If the line went to a `$` prompt instead, type `openclaw chat` and send it again. If the agent only answered in words, type `Write results/findings.md now.` If it wrote `02_data/findings.md` instead, type `Move it to results/findings.md.`
- It runs `pip install`: tell it `Use the libraries already installed.`
- A number in the report appears in no output: ask `Which line of output does each number come from?`
- 429 or a timeout: the room shares one model. Wait a minute, then type `Continue.`
- The chat gets slow: type `/new`, then `Read results/findings.md and results/analysis.py, then continue.`
