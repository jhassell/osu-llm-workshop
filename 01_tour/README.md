# Module 1: What the model can do

One line of Python sends a research document to the model and brings text back. This module runs six of those lines on one document so you can see, side by side, what the model does well and where it slips. Every later module in the day's one program, the document assistant, is this same call with a better prompt around it.

About 40 minutes. Folder: `01_tour/`. Behind? `bash catchup.sh m1`

## You will be able to

1. Call the model from Python with one line, `ask(prompt)`, on a document you choose.
2. Name the two or three things it did well on a research document.
3. Judge one claim against the source, using the five judgments below, and point to the passage that settles it. A claim you checked and found supported is a full answer.

## The idea

A prompt is the text you send the model. The starter builds each prompt by putting an instruction in front of the document's full text, and sends it with one call:

```python
print(ask(f"{prompt}\n\nDocument:\n{doc['text']}"))
```

The model brings two things to each reply: general knowledge it learned in training, before you ever called it, and the evidence in the prompt, which here is one document. Only the second can be checked against the source in front of you. Neither guarantees accuracy.

On a short research document the model is often useful. It compresses (a two-sentence summary), it re-levels (the same finding for a first-year student), and it lists (methods, numbers, questions a reviewer would ask).

It also slips in ways that read just as confidently as the good output. It adds things the source does not say, such as a word like "significant" when no test is reported. It loses nuance, such as a limitation, because a short rewrite has to drop something. It presents plans as things already done. And when asked about something it was not shown, it can produce precise-looking specifics.

When you check a claim, give it one of five judgments:

- Supported: the source says it, in these words or others.
- Contradicted: the source says something different.
- Added: the source does not say it at all, such as "significantly" when no test is reported.
- Dropped, and it matters: something left out changes how a reader would take the result, such as a limitation.
- Fair simplification: shorter or plainer, and a reader would still take it the right way, such as leaving out the dose in a three-sentence rewrite.

Supported means faithful to this document, not proven true: the document itself can overstate. And an accurate reply is a good outcome, not a failed exercise; the point is that you checked.

So the habit this module builds is to check one claim against the source. `grep` is a terminal command that prints every line of a file containing some text; `-n` adds line numbers and `-i` ignores capital letters. It only finds the passage. Then read the passage and ask whether it says what the reply says. A word that is missing may still be supported in other words, and a number that matches may still be used for the wrong thing.

## Predict first

The model will be asked to rewrite an abstract for a first-year student. Write on your card one thing you expect it to lose.

## Do it

1. Run the starter. It makes six calls on `corpus/doc_001.txt`, a study of an invented compound, lirazine, in injured zebrafish hearts, and prints each reply under a heading. It takes about a minute.

   ```bash
   python 01_tour/starter.py
   ```

   You should see six headings, from `Two-sentence summary` to `A question it cannot know`, each followed by a reply. For example, under `For a first-year student`:

   ```text
   In zebrafish that received a frozen-heart injury, the drug lirazine caused more heart
   cells to begin dividing than in fish that did not get the drug. Roughly twice as many
   cells were observed making new DNA, and the scarred portion of the heart was noticeably
   smaller.
   ```

2. Compare the rewrite with your prediction. Open `corpus/doc_001.txt` from the file tree and read it, especially the last paragraph. One term to know: EdU is a label that cells take up while they copy their DNA, a step before division; an EdU-positive cell has copied its DNA, which does not by itself show that it divided. Write on your card what the rewrite kept and what it dropped.

3. Check one claim against the source. Pick a word or number from any reply, find it with `grep`, then read the line it prints.

   ```bash
   grep -n -i "signific" corpus/doc_001.txt
   ```

   For example, one summary began "Lirazine treatment (25 µM) significantly boosted cardiomyocyte proliferation in cryoinjured zebrafish ventricles". The grep prints nothing. That alone does not settle it, since the document could say the same thing in other words, so read the results paragraph: it gives the two percentages and how closely the two readers agreed, and no statistical test. "Significantly" is the model's word, not the authors'. A number that is in the document prints its line:

   ```bash
   grep -n "7.6" corpus/doc_001.txt
   ```

   ```text
   9:Lirazine raised the EdU positive cardiomyocyte index from 4.1 percent in controls to
   7.6 percent in treated animals, an increase of 85 percent. ...
   ```

   The number matches. Now check that the reply used it for the same thing: the EdU-positive index in treated fish, not, say, a scar area.

4. Pick the two of the six results you would actually use. Check one claim in each the same way, and give each a judgment from the list above.

## Checkpoint

Show your pair the most useful of the six results, and one claim whose support matters: the claim, the passage you found, and your judgment. If everything you checked was supported, that is your result; say which claim you would check next.

## Exercises

1. Core: one more document, your choice. Pick one of these; one is enough.

   The bench note, `01_tour/bench_note.txt`: four sentences of a lab notebook that mix what was observed, what is only suspected, and what is planned for next week. Ask for one rewrite, not six:

   ```bash
   python 01_tour/ask.py "Rewrite the main finding of this note for a first-year undergraduate, in three sentences, no jargon." 01_tour/bench_note.txt
   ```

   Read the note itself, then sort its sentences into observed, suspected and planned. Look for whether the rewrite keeps them apart: does it say the fresh-buffer test worked, when the note only plans it? If your reply keeps them apart, compare it with one from a test run, which did not:

   ```text
   When we began preparing fresh liquid each morning and checked its acidity, the daily
   increase went away, indicating that making fresh liquid every day would stop the drift.
   ```

   Your own document: if you put PDF, Word or Markdown files in `mine/`, convert them first with `python convert.py`. If you brought none, right-click `mine/` in the file tree, choose **New File**, name it `notes.txt`, and paste in a paragraph or two of your own writing. Then:

   ```bash
   python 01_tour/starter.py mine/notes.txt
   ```

   Put the path in quotes if the name has spaces, here and in `grep`. Look for the one result you would trust, and check one claim. Plans are worth a look: does any reply describe as done something your document only proposes?

   Another sample: `doc_003` is a lirazine study that found no difference between treated and untreated fish, a contrast with `doc_001`; `doc_006` (chemistry), `doc_011` (engineering) and `doc_015` (genomics) are other fields. Run `python 01_tour/starter.py corpus/doc_003.txt` and check whether the summary keeps the reasons the result might be null.

2. Stretch (optional): change one of the six prompts. Open `01_tour/starter.py`. In `PROMPTS`, each entry is a heading in quotes, a colon, then the instruction in quotes, then a comma. Replace one entry with something you actually want from your documents, keeping the quotes and the comma, and run it again with `python 01_tour/starter.py`. Look for whether it did what you meant. If it did not, find the words in your prompt that let it go somewhere else. Module 2 is about exactly that.

3. Stretch (optional): send the same prompt twice. `01_tour/ask.py` sends one prompt, with a document after it if you give one, and `--twice` sends it twice.

   ```bash
   python 01_tour/ask.py --twice "Summarize this document in two sentences." corpus/doc_001.txt
   ```

   Look for which words change between the two replies, and whether any fact changes. The helper asks the model for a little randomness, so the wording varies from run to run. A detail that changes between runs is a detail to check against the source; a detail that stays the same still needs checking.

4. Stretch (optional): ask about a paper you know well, with no document attached. The reply comes only from what the model learned in training. Put the paper in your own words inside the quotes.

   ```bash
   python 01_tour/ask.py "What did <a paper you know well> report? Give its full title, journal, volume and pages, and three specific findings with numbers."
   ```

   Check two or three details against the paper itself, a figure or a table. Give each a judgment, and write what in the paper settled it. Specific-sounding details such as page numbers and percentages are the ones to check first.

## What you have now

- `llm.py` and its one call, `ask(prompt)`, which every later module uses.
- `01_tour/ask.py` for a quick one-off question, with or without a document.
- The habit of finding the passage behind a claim and reading it, which Module 3 turns into an audit of a whole table.
- Five judgments for any claim (supported, contradicted, added, dropped and it matters, fair simplification), which Module 3 uses to audit a whole table.
- A sense of which of the six jobs are worth asking for, which leads into Module 2.

## If something goes wrong

- A reply is empty or stops in the middle of a line. The model spent its allowance thinking before it answered. Ask for less (fewer items, or add "Keep it brief." to the prompt) and run it again.
- `No such file or directory` for your document. The path starts from the top folder of your repository. Type `ls mine` to see the exact file name, and give it as `mine/name.txt`, in quotes if it has spaces.
- The first line says `Title: not stated`. Your document has no `Title:` line at the top. That is fine; the model still reads the whole text.
- `SyntaxError` after editing `PROMPTS`. A quote or a comma went missing. Fix it, or run `bash catchup.sh m1` to restore the original `01_tour/` files. Your edited files are copied to `mine/catchup-backup-<date-time>/` first.
- Each run takes about a minute. That is six calls one after another; it is normal.
