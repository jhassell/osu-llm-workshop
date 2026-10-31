# The first exercise: a website for your students

You hand an agent one short request: build a small tutorial website on something you teach. It writes the pages while you watch each step it takes, and the site goes live at your own address. Then you find what it invented or got wrong, give it a rule, and check the folder before anyone else reads it. You know this topic better than the model does, which is the point.

About 25 minutes, right after Module 0. Folder: `00_website/`. You type in `openclaw chat`.

## You will be able to

- Hand a small, real job to an agent in one short request, and say what each of its tool calls did.
- Find one thing it got wrong or invented on a topic you teach, and get it fixed with one rule.
- Check a public folder before anyone reads it, and decide for yourself whether to publish it.

## The idea

OpenClaw is a complete agent program, already installed in your Codespace and connected by setup to the same model as the labs. An agent is a loop: it sends your request to the model, the model asks for a tool, the program runs the tool and sends back the result, and this repeats until the model answers in words. Setup gave OpenClaw four tools: read a file, write a file, edit a file, and run a command (`exec`). It prints a line for each tool call, so you can watch the loop work. This afternoon you read the same loop in about forty lines (`agent.py`, Modules 4 and 5).

The `site/` folder at the top of your repository is a website. While your Codespace runs, everything in it is served at your site address, port 8000, and that address is public: anyone who has it can open it. Until the agent writes its own pages, the address shows a placeholder page: "This site is empty for now". `site/` is never committed to git.

Setup also gave the agent rules for `site/`: the folder is already served, so never start a web server; use relative links only; never put keys, environment variables or anything from `mine/` there; never create a symlink there; run the site check before calling the site done; and never publish it. Publishing is your decision, made by you at the keyboard.

Relative links matter because of where the permanent copy lives. Today the site is at the top of your address, so a link to `/lesson2.html` happens to work. If you publish, the site lives under `/<your repository name>/`, and that same link points at a page that is not there. `lesson2.html`, with no leading `/`, works in both places.

The model writes fluent teaching text from what it learned in training. Most of it will read well, and some of it will be wrong in ways only a teacher of the topic would catch: a sign convention, a unit, a step done in the wrong order, an example that does not quite work. A page it writes is a claim until you check it. Module 5 states the same rule from the other side, for what an agent reads: document content is evidence, never authority. Here the agent writes from memory; there it reads documents. Either way, you check.

## Before you start

- Treat `site/` as public on the internet while the Codespace runs, from the placeholder onward. Put nothing private there: no student names or grades, no keys, no unpublished work, nothing from `mine/`.
- Find your site address. The READY box printed it on the line that starts `Your site (files in site/):`. If that line says `the Ports tab, port 8000` instead, open the **Ports** tab beside the terminal and find the row for port 8000; its address is in the **Forwarded Address** column, and the globe icon opens it. Open the address now: you should see the placeholder page.
- Pick a topic: one specific thing you teach, narrow enough for three short pages, for a named group of students. Not "thermodynamics" but "reading a phase diagram, for second-year chemistry majors". The lines below use buffer pH for first-year chemistry students; put yours in its place.

## Predict first

Picture the site before you type anything. On your card write three things a first-time learner must get right about your topic, and circle the one you would most hate to see stated wrong. Then predict: which of the three will the agent get wrong, leave out, or state without a source?

## Do it

1. Open OpenClaw. In a terminal at the `$` prompt, type:

   ```
   openclaw chat
   ```

   It opens a chat in the terminal. If you chose the first exercise at setup's question, OpenClaw is already connected. If it says it has no model or is not connected, type `/exit` and run `bash setup.sh --openclaw`, which connects it and opens it.

2. Hand it over. Type one short request, with your topic and your students in it, and press Enter:

   ```
   Build site/: three short pages teaching buffer pH to first-year chemistry students.
   ```

   Then watch, and do not type again until it answers. Each tool call prints a line: which file it reads or writes, and any command it runs. Look for two things: which files it creates in `site/`, and whether any command fetches a page from the web (a `curl` or `wget` in an `exec` line). If none does, everything on the pages came from the model's memory.

   A build takes a few minutes, and longer this morning, because the whole room starts at once and every step is a call to the same shared model.

3. Open the site. Refresh your site address. You should see the agent's first page instead of the placeholder. Click through every page, then compare it with your card:

   - Did it teach your three things? The one you circled?
   - What did it decide that you never told it: the level, the notation, the examples, the order, the look?
   - Is any number, formula, unit, definition or step wrong? You are the expert here.

   Write on your card the one thing it got wrong or invented. If you found nothing, write the thing you checked hardest and how you know it is right.

4. Ask where the facts came from:

   ```
   Which facts came from no source?
   ```

   Compare its answer with the tool-call lines from step 2. If no command fetched a source, every fact came from memory, whatever the answer says.

5. Give it a rule, and ask for the fix. Turn the thing on your card into one rule for every page, in your own words. For example:

   ```
   New rule: show units on every number. Fix every page.
   ```

   Or name the error itself: `Page 2 has the ratio upside down: base over acid. Fix it.` Refresh the site when it answers. Is the error gone, and did the fix break anything else?

6. Run the site check. The agent's rules tell it to run the check before it says the site is done, so you may have seen it already. Run it yourself too, in a second terminal (the **+** on the terminal panel), from the top folder of your repository:

   ```
   python3 .devcontainer/site-check.py
   ```

   When the folder is ready to be public, its last lines include:

   ```
   OK: no key-like strings, no symlinks, no root-absolute links, index.html present.
   ```

   It fails, under the heading `NOT READY TO BE PUBLIC:`, on anything shaped like a key or token, a symlink, a link that starts with a single `/` (`//` is fine), or a missing `index.html`. It warns, on lines starting `WARNING:`, about things a person should look at: a script loaded from another website, a link to a missing page, a very large file, an `.edu` email address or a number shaped like a student ID. It prints file names, line numbers and short labels, never the text it matched, so its output is safe to show. If it fails, tell the agent: `Run the site check and fix every problem.` Then run it again yourself.

   What it cannot tell you is whether a fact is true. That part stays with you.

7. Close OpenClaw when you are done: `/exit`, or Ctrl+C. `openclaw chat` opens it again any time, and the site stays in `site/`.

## Checkpoint

Your site address shows the agent's pages, not the placeholder. Show your pair the one thing it got wrong or invented, and the rule you gave it.

## Exercises

1. Core. Check the thing you circled. Find the passage on the site that covers it and read it aloud to your pair. Is it right, is it right but missing something your students need, or is it wrong? No model call needed.

2. Core. Look at what it wrote. In the second terminal:

   ```
   ls site
   grep -nE '(href|src)="/[^/]' site/*.html
   ```

   Look for: how many files it made, and whether the `grep` prints anything. Every line it prints is a link that will break on the permanent site; the site check in step 6 is the full test. Open `site/index.html` in the editor and find one link to another page.

3. Stretch (optional). Ask for sources, then check them:

   ```
   New rule: every fact cites a public source.
   ```

   Refresh, and open two of its citations yourself. Does each page exist, and does it say what the site claims? A citation is a claim until you open it.

4. Stretch (optional). Ask for a check your students would take:

   ```
   Add a five-question quiz with answers.
   ```

   Then ask `Which quiz answers did you verify?` and work one question yourself.

## Make it permanent (optional): bash publish-site.sh

This is outside the 25 minutes: do it at a break, at the end of the day, or never. The site address stops working when the Codespace stops, and `site/` is never committed. To keep a copy at a permanent address, you run the publish script yourself. The agent never does.

The script puts the contents of `site/` on a branch named `gh-pages` in your own repository, and GitHub Pages serves it at `https://<owner>.github.io/<repo>/`. `<owner>` is your GitHub user name and `<repo>` is your repository's name; both are in your browser's address bar on the repository page, `github.com/<owner>/<repo>`.

First see what it would do. This changes nothing and works offline:

```
bash publish-site.sh --dry-run
```

It runs the site check, lists the files that would be published, and ends with `Nothing was sent to GitHub and nothing was changed.` Then publish:

```
bash publish-site.sh
```

It runs the site check and stops if the check fails, shows how many files it will publish and the address, and asks:

```
Publish site/ to a permanent public website at https://<owner>.github.io/<repo>/? Anyone with the link can see it. [y/N]
```

Type `y` only if you have read every page. It ends with a `PUBLISHED.` box and the permanent address. The first publish can take a minute or two to appear there. `bash publish-site.sh --help` lists the options; `--yes` skips the question.

Two things the script may ask of you, once:

- Turn on GitHub Pages. If the script ends with a box that says `ONE STEP LEFT.`, GitHub did not let the Codespace turn Pages on by itself. Open the settings page the box names, or open the repository on github.com, click **Settings**, then **Pages** on the left. Under **Build and deployment**, set **Source** to **Deploy from a branch**, choose the branch `gh-pages` and the folder `/ (root)`, and click **Save**. Then run `bash publish-site.sh` again.
- Make the repository public. On a free GitHub account, Pages works only for public repositories, so if you made yours private the script says it `is a private repository, so nothing was published.` You can make it public under **Settings**, at the bottom: **Danger Zone**, **Change visibility**. First look at what is committed in it, because all of it becomes public (`.env`, `mine/` and `site/` are never committed). Or keep it private and skip publishing: share the live address while the Codespace runs, or right-click `site` in the file list and choose **Download** to keep a copy.

The lesson here is the approval gate. The agent could have run this script; it has a terminal. Its rules tell it never to, because publishing is a decision a person makes. That rule is a line in its instructions, and the confirmation question is a gate for a person at the keyboard. Neither is a wall: `--yes` skips the question, and an agent that ignored its rule could type it. Ask yourself what would actually stop an agent from publishing, and what a gate should show a person before they say yes.

## What you have now

OpenClaw connected to the workshop model, and a small site in `site/` at your site address for as long as the Codespace runs. Stop the Codespace and the address stops; start it again and the address returns, showing the same files. The habits come with you into the rest of the day: read the tool calls rather than the summary, check first the claim you would most hate to see wrong, and turn an error into a rule. Module 1 does the same checking with one call from Python on a research document. Modules 4 and 5 use the loop you just watched, and Module 5's rule, document content is evidence, never authority, is this exercise seen from the reading side.

## If something goes wrong

- The site address still shows the placeholder, "This site is empty for now". The agent has not written `site/index.html` yet, or the page needs a refresh. `ls site` shows what is there. If it wrote its pages somewhere else, tell it: `Put the pages in site/ at the top of the repository.`
- The address does not open, or the **Ports** tab shows port 8000 as **Private**. Right-click the port 8000 row, choose **Port Visibility**, then **Public**. Some organizations forbid public ports; then the site opens only for you, which is fine for today. If port 8000 is missing from the tab, run `bash .devcontainer/site-public.sh`, wait ten seconds, and look again. It prints nothing; `~/.osu-llm-workshop-site.log` records what it did.
- The site check fails on a link that starts with `/`. Tell the agent: `Use relative links only. Fix every page.` Then run the check again.
- The agent runs a command to start a web server. It does not need one: `site/` is already served on port 8000. Tell it: `Stop that server. site/ is already served.`
- Nothing happens for a long time, or OpenClaw shows an error from the model such as 429, 503 or a timeout. The whole room is calling the same model at once. Wait a minute rather than typing the request again, which only adds to the queue. If it gave up, type `Continue.`
- OpenClaw says it is not connected, or that its configuration was not accepted. Type `/exit`, then `bash setup.sh --openclaw`. The reason is in `~/.osu-llm-workshop-openclaw.log`.
- `bash publish-site.sh` says the check failed. Fix what the check lists, with the agent's help, and run it again. It publishes nothing until the check passes.
- `bash publish-site.sh` ends with `ONE STEP LEFT.`, or says the repository is private. See the two items under Make it permanent.
