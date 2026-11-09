# Stop 5: The agent repairs research code

`05_repair/analysis.py` is a short analysis that once reproduced a published table: the number of penguins of each species and their mean bill, flipper and body measurements, as printed in the palmerpenguins documentation. It no longer runs. You hand it to the agent with one request and watch it run the script, read the error, fix it, run it again, and keep going until an independent check says the numbers match the published ones. Then you find out whether you understood what it changed.

About 45 minutes, from 1:25, including two demonstrations from the front. Folder: `05_repair/`. Two places to type, and every step below says which:

- In the OpenClaw chat: the terminal where `openclaw chat` is running, at its prompt. Requests to the agent go here. `/exit` closes the chat and leaves you at the `$` prompt; `openclaw chat` opens it again.
- In a second terminal: click the **+** at the top right of the terminal panel to open one, and type at its `$` prompt. Commands you run yourself go here, so the agent never runs them for you.

To read a file, click it in the Explorer on the left.

## You will be able to

- Hand a broken analysis to an agent and get it repaired against an independent check, not against its own opinion.
- Read the diff and say, for each change, what was wrong and why the fix is right.
- Name the kind of fault no error message reveals, and how the check caught it.

## The idea

Research code rots. A library removes a function the script used. The script assumes a folder that exists only on the author's laptop. Someone adds a filter to try something and never takes it out. The first two fail loudly; the third runs cleanly and gives a different answer, which is the dangerous kind.

An agent with a terminal is good at the loud kind: it runs the script, reads the traceback, changes a line, runs it again. What keeps it honest on the quiet kind is a check it did not write. `05_repair/check_expected.py` runs the script and compares its output with the published numbers in `05_repair/EXPECTED.md`, within half a unit of the last published digit. The agent's job is to make that check pass; your job is to make sure it passed for the right reason, not because the agent edited the check or the expected numbers.

## Run it once yourself

Before the agent sees it, run it and read the error, in a second terminal:

```
python 05_repair/analysis.py
```

Its last line names what went wrong. Click `05_repair/analysis.py` in the Explorer to read the script itself.

## Before you start: step three, Cimarron, if it is up

This is the day's third step: a chat box, an agent in your folder, an agent on your campus cluster. If the instructor says Cimarron is up, move to it for this stop (the labs and OpenClaw follow; the first move asks for the card word). In a second terminal:

```
bash 00_setup/switch_backend.sh cimarron
```

It worked only if you see both: the box ending with READY and an endpoint that is not openrouter.ai, and after it the line saying OpenClaw is connected (`OpenClaw is connected to ...`). Then, in the OpenClaw chat, type `/exit`, and at the `$` prompt that comes back type `openclaw chat`: a chat that was already open keeps the old endpoint.

If either line is missing, or the move stops with an error, do not carry on where you are: move back explicitly, in the second terminal, `bash 00_setup/switch_backend.sh openrouter`, wait for the same two lines (READY with openrouter.ai, then OpenClaw is connected), then `/exit` and `openclaw chat` in the chat terminal, and tell a helper.

The model's work now happens on OSU hardware in Stillwater instead of at a commercial provider. Your files still sit in your GitHub Codespace, so the rule about what to bring has not changed: no unpublished results you are not free to share, no student records, nothing under an IRB protocol. At the end of the stop, `bash 00_setup/switch_backend.sh openrouter` moves you back (then `/exit` and `openclaw chat` again), because Stop 6 may need the vision model and the larger context. If Cimarron is not up, skip this; the instructor shows it from the front.

## Do it

1. Hand it over. In the OpenClaw chat:

   ```
   Run python 05_repair/analysis.py, reproduce the failure, fix the code, then run
   python 05_repair/check_expected.py until it passes. Explain the change in one paragraph.
   ```

   Watch the loop: run, error, edit, run again. Count the times it runs the script.

2. Run the check yourself, in a second terminal:

   ```
   python 05_repair/check_expected.py
   ```

   It should end with `PASS`. If it says FAIL, read which values are off.

3. Read what changed. In the second terminal:

   ```
   git diff HEAD -- 05_repair/
   ```

   A diff shows what changed in a file since it was last committed. Lines starting with `-` (red) were removed; lines starting with `+` (green) were added; the lines around them are unchanged context. If the output fills the screen and ends with `:`, the terminal is showing it a page at a time: press the space bar for more and `q` to get back to the `$` prompt.

   For each changed line, write on your card what was wrong. Then check the two files the agent should not have touched:

   ```
   git diff HEAD -- 05_repair/check_expected.py 05_repair/EXPECTED.md
   ```

   It should print nothing. `HEAD` matters: it compares with the files as they came in the template, so it also shows a change the agent staged with `git add`, which a plain `git diff` would hide.

4. Find the quiet fault. One of the changes made a script that already ran give the right answer. Write on your card, before the debrief: which line it was, and what it did to the counts of each species. Then one more line: if this were your script, what one check would you add?

   Look back at the agent's tool calls in the chat: did it run `check_expected.py` and read a FAIL before it touched that line, or did it spot the line by reading the code? Either is fine, but only the first shows the check catching the fault. If yours never ran the check first, the instructor shows what the check says about that line at the debrief.

## Checkpoint

`python 05_repair/check_expected.py` prints PASS, `git diff HEAD -- 05_repair/check_expected.py 05_repair/EXPECTED.md` prints nothing, and you can say what each change fixed.

## Extensions

1. Extend it: in the OpenClaw chat, ask the agent to add the median body mass per species and per sex. There is no published number for that, so how would you check it?
2. A script of yours with a known problem, from `mine/`. Give the agent the same request, with your own check: a number you know is right.
3. Ask the agent to write a test for the quiet fault, so that if anyone adds that filter again the test fails.

## The last ten minutes: two demonstrations

- Model choice. One checkable task given to five models, names hidden until the room has judged the answers. The same question twice to one model, to show that answers vary.
- Cimarron. The same labs against OSU's Cimarron cluster, if its endpoint is up, or a model running on the laptop with the network off. What a NIM is, what changes (the model's work happens on OSU hardware in Stillwater; your files are still in GitHub's Codespace), and how to get an account. If Cimarron is up, `bash 00_setup/switch_backend.sh cimarron` in a second terminal moves you to it again later today, and `openrouter` brings you back; after either, `/exit` and `openclaw chat` in the chat terminal.

## What you have now

A repaired script that reproduces a published table, and a check that says so. The habit: give the agent a check it cannot edit, and read the diff before you believe the summary.

## If something goes wrong

- The agent edits `check_expected.py` or `EXPECTED.md` to make the check pass. That is the failure this stop is about. In the second terminal, `git checkout HEAD -- 05_repair/check_expected.py 05_repair/EXPECTED.md` puts both back as they came in the template, even if the agent staged its edits. Then, in the OpenClaw chat: `Do not change the check or the expected numbers. Fix analysis.py.`
- In the second terminal, `git log --oneline -3` shows a commit you did not make. The agent committed its edits, and `git diff HEAD` compares with that commit, so it cannot see them. Compare with your repository as it is on GitHub instead: `git diff origin/main -- 05_repair/check_expected.py 05_repair/EXPECTED.md`, and restore with `git checkout origin/main -- 05_repair/check_expected.py 05_repair/EXPECTED.md`.
- It installs an older pandas to make the old call work. It should not. In the OpenClaw chat: `Use the installed pandas; change the code.` Then, in the second terminal, `pip install pandas==3.1.0` puts the workshop's version back.
- It stops after the script runs, without running the check. In the OpenClaw chat: `Now run python 05_repair/check_expected.py.`
- Start over: in the second terminal, `bash catchup.sh s5` restores the broken script (your version is backed up in `mine/`).
