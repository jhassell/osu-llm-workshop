# Prediction cards

One card per stop, printed two to a page and handed out at 8:30. Each card has the prediction for that stop, a line for the answer, the checkpoint, and what you write during the build. Nobody collects the cards; they are for the person holding them and the pair conversation. The two minute papers are torn off and handed in. A wrong prediction costs nothing.

---

## Stop 0, everyone green

Workshop word, for the key prompt: OpeningDayToken (letter case does not matter)

Prediction: when the check runs, what will its second line say?

My answer:

Checkpoint: which machine produced each of the two lines?

First line:                          Second line:

Into mine/: nothing you would not show the model service. No student records, nothing under an IRB protocol, no unpublished results you are not free to share.

Early finisher: what one row of the data is, and one number in it I could check by hand:

---

## Stop 1, a website for your students

Prediction: three things a first-time learner must get right about your topic. Circle the one you would most hate to see stated wrong.

1.

2.

3.

Which of the three will the agent get wrong, leave out, or state without a source?

Checkpoint, from the build: the one thing the agent got wrong or invented, and the rule I gave it:

---

## Stop 2, your data, analyzed and reproducible

Four lines, before any prompt, in my own words:

One row is a:

The outcome, with its unit:

The comparison:

One other thing that could explain a difference:

My hand check, before the debrief:

Row count, mine:                     Row count, the report's:

My number:                           The report's number:

Rows the agent dropped, and why:

Explain to your partner in sixty seconds how you checked it.

Checkpoint: results/analysis.py reproduces the report.

---

## Stop 3, three papers to an evidence table

Prediction: of three papers an index returns for my topic, how many will have a DOI that checks out?   0   1   2   3

The field a model is most likely to get wrong (circle one): question / method / sample / finding

From the build: the field where the quote does not settle the claim, and why:

Checkpoint: three DOIs resolve to the right papers; one quote found in the text.

At 12:10, after the minute paper: circle the Stop 6 recipe I will build after lunch (if unsure, the first).

folder to table / a page for my dataset / a literature digest / my own idea, if a helper agrees

---

## Minute paper, 12:10 (anonymous, tear off)

The main point of the morning in one sentence:

The muddiest point:

---

## Stop 4, a chart back into data

From memory, the command that rebuilds this morning's analysis:

Prediction: the model will read better (circle one): the bar chart / the dense scatter

On the harder one it will (circle one): say it is unsure / return a full table anyway

Checkpoint, one sentence: I would trust this for these charts, and not for these:

---

## Stop 5, the agent repairs research code

If Cimarron is up: bash 00_setup/switch_backend.sh cimarron at the start, bash 00_setup/switch_backend.sh openrouter at the end.

Prediction: how many separate problems does the script have?

Which one will the agent find last?

For each changed line, what was wrong:

The quiet fault, before the debrief:

Which line:

What it did to the counts of each species:

If this were my script, the one check I would add:

Explain it to your partner in sixty seconds.

Checkpoint: check_expected.py prints PASS, and the check and the expected numbers are unchanged.

---

## Stop 6, build one thing from your week

My recipe (circled on the Stop 3 card):

What I will change in the starter:

The transfer test, at 3:15, run without the agent. Circle what it did.

An input it had not seen:     right answer / wrong answer / honest "not stated" or error / crash

The bad input:                right answer / wrong answer / honest "not stated" or error / crash

Checkpoint: show your pair the bad input and what your tool did with it.

---

## The close, before you go

bash export.sh run, and the zip downloaded:   yes

The two lines that put my own key in .env (06_build/README.md, After today):

LLM_BASE_URL=

LLM_API_KEY=  (your key, in .env only, never on this card)

---

## Minute paper, at the close (anonymous, tear off)

The main point of the day:

The muddiest point:

The first thing I will build on Thursday:
