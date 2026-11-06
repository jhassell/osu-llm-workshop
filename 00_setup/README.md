# Stop 0: Everyone green

Before anything else, every Codespace in the room has to reach the model. This stop connects yours with the word on your card and proves it with one command, then checks any files you brought. Every later stop sends the same kind of request this check sends, with different text in it.

Stop 0, about 30 minutes, from 8:30. Folder: `00_setup/`.

## You will be able to

- Run one command in your Codespace that reaches the model, and say what each of the two lines it prints means.
- Say where the model runs, and which two settings in `.env` tell the labs how to reach it.

## The idea

The model does not run in your Codespace. Your Codespace is a small computer that GitHub lends you; it has no GPU (the graphics chip that large models need to run fast) and holds no model. The model runs on a GPU server somewhere else, and your code reaches it over the internet.

An endpoint is the web address of that server, ending in `/v1`. Your code sends it text in an HTTPS request (the same kind of secure web request your browser makes) and gets text back. Any server that speaks the same request format, the "OpenAI-compatible" format many providers use, works with every lab today.

A key is a long password that tells the endpoint you are allowed to use it. Setup asks for it once and saves it. Today the word on your card stands in for the key: setup exchanges it for the workshop's key.

`.env` is a small file in the top folder of your repository where setup saves its settings: `LLM_BASE_URL` (the endpoint), `LLM_API_KEY` (the key), and sometimes `LLM_MODEL` (which model to ask, when the endpoint serves several). Every lab reads its settings from there, so moving to a different model service means changing `.env`, never the code. (If you ever set up a Codespaces secret with one of these names in GitHub, setup uses it and writes it into `.env`; the labs themselves read only `.env`.) `.env` is never committed, which means git never saves it into your repository's history, and you never need to open it, print it, or share it.

`00_setup/check.py` makes two requests. The first asks the endpoint which models it has, and prints the one the labs will use. For example:

    reachable; serving nvidia/nemotron-3-ultra-550b-a55b

The second request asks the model for a one-word reply and prints what comes back, on a line that starts `completion:`. That text was written on the GPU server, not in your Codespace.

## Predict first

When the check runs, what will its second line say? Write your answer on your card before you run it.

## Do it

1. Remember what the pre-work already did. You copied the template with **Use this template**, created a Codespace, clicked **Trust Folder & Continue**, and pressed Enter at the key prompt with no key. In a new Codespace, setup starts by itself in the first terminal and keeps starting in each new terminal until it has succeeded once. Pressing Enter with no key ended with:

       Codespace ready; endpoint check pending.

   This morning you finish the job. Open your Codespace. If no terminal is open, click the **+** on the terminal panel.

2. Run setup and type the word from your card (letter case does not matter) or paste a key. It shows on screen as you type. Press Enter once.

   ```
   bash setup.sh
   ```

   Setup picks the endpoint from the kind of key you paste, and sends the key only to that endpoint:

   - the workshop word from the card (letter case does not matter) is looked up at the address in `workshop-endpoint.txt`, and the labs then run on OpenRouter with the workshop's own key and `nvidia/nemotron-3-ultra-550b-a55b`, the most capable Nemotron model; no model list is shown
   - the OSU workshop key from the card, when the room has its own endpoint, goes to that endpoint
   - an OpenRouter key (starts with `sk-or-`) goes to OpenRouter, and setup then lists six models tested with this workshop. Press Enter for the first, `nvidia/nemotron-3-ultra-550b-a55b`, or type the number of another. `bash setup.sh --choose-model` shows the list again later
   - an NVIDIA key (starts with `nvapi-`) goes to NVIDIA's hosted endpoint, using `nvidia/nemotron-3-ultra-550b-a55b`, one of the few models NVIDIA opens to a personal account

   Setup finds the workshop addresses in `workshop-endpoint.txt`, or downloads the instructor's current copy of that file if yours is blank, so a repository made weeks ago still finds them. A word nobody published is refused with a plain message, and a key is never sent anywhere but its own endpoint. The one exception to choosing by key: if the instructor switches the room to another endpoint, every key you paste goes to that endpoint, so paste the key that goes with it. The same is true if you have set up your own Codespaces secret named `LLM_BASE_URL`.

   You should end at a READY box. For example, with an OpenRouter key:

       Checking the key against the endpoint... ✅
       ==============================================
        READY. Endpoint: https://openrouter.ai/api/v1
        Model: nvidia/nemotron-3-ultra-550b-a55b
        Your site (files in site/): https://silver-space-waddle-7vq9xw-8000.app.github.dev/
        The key is saved in .env (never committed).
       ==============================================

   Your site address will differ; it is built from your Codespace's name. If that line says `the Ports tab, port 8000` instead, the address is in the **Ports** tab beside the terminal, on the row for port 8000. Stop 1 explains what the site is.

   Setup then connects OpenClaw, a complete agent program, to the same model, opens Stop 1's page in the editor, and opens OpenClaw's chat in this terminal, ready for Stop 1. Leave it open and do not type there yet.

3. Run the check, in a second terminal: click the **+** on the terminal panel, then type

   ```
   python 00_setup/check.py
   ```

   You should see two lines. For example:

       reachable; serving nvidia/nemotron-3-ultra-550b-a55b
       completion: ready

   The wording of the second line can vary from run to run. Compare it with your prediction, then turn your card green.

4. If you brought files for the day (a CSV, two or three PDFs, a chart image), drag them from your laptop onto the `mine/` folder in the file tree, then check them, in the same second terminal:

   ```
   python upload_check.py
   ```

   Each file gets `ready` or `NOT READY`, and a line that says why: the columns it found in a CSV, whether a PDF has text the model can read, the size of an image. A file that is not ready gets three minutes, then the shipped example it names, with your own file saved for Stop 6. Everything in `mine/` stays out of git, and anything a stop reads from it is sent to the model service, so bring nothing you would not show that service: no unpublished results you are not free to share, no student records, nothing under an IRB protocol. `mine/README.md` says what is worth bringing.

   Next comes Stop 1, open in the editor (`00_website/README.md`), typed in the OpenClaw chat in your first terminal.

## Checkpoint

Show your pair your two lines, and say which machine produced each one: what ran in your Codespace, and what came back from the server. If you brought files, show which are ready.

## Exercises

1. Core. Read the check's two lines. Run `python 00_setup/check.py` again and look at each line on its own. Then open `00_setup/check.py` and find the two requests it makes, one to `/models` and one to `/chat/completions`. Look for: which line comes from which request, and which line proves that your key works.

2. Core. See which settings `.env` holds without showing the key. This command prints only the name in front of each `=` sign, never a value:

   ```
   grep -o '^[A-Z_]*=' .env
   ```

   Look for: the setting names from The idea, and whether `LLM_MODEL` is there. Never print the whole file, and never paste it into a chat, an email, or a shared screen.

3. Stretch (optional), only if your endpoint serves more than one model. OpenRouter does; the workshop endpoint may serve just one, and then setup refuses the other name and leaves your settings as they were. Switch to a smaller model, check, and switch back. The endpoint and key stay the same; only `LLM_MODEL` changes. First write down the model name from the first line of your check, because you need it to switch back. These commands were tested on OpenRouter:

   ```
   bash setup.sh --model nvidia/nemotron-3-nano-30b-a3b
   python 00_setup/check.py
   ```

   Look for: what changed in the first line, and whether the second line changed. Setup remembers the model you named, so switch back by naming the one you wrote down, for example:

   ```
   bash setup.sh --model nvidia/nemotron-3-ultra-550b-a55b
   python 00_setup/check.py
   ```

4. Stretch (optional), for early finishers. Open `02_data/datasets/penguins/DICTIONARY.md` in the editor and read it, or your own notes on the columns of the CSV you brought. Write on your card what one row of that data is, and one number in it you could check by hand. Look for: a column whose units the file alone does not tell you. Stop 2 starts from these.

## What you have now

A Codespace connected to a model, with the endpoint and key saved in `.env`, which every later stop reads. You can tell whether the connection works with `python 00_setup/check.py`, and you know the model runs on a server, not in your Codespace. Stop 1, in `00_website/`, uses the same connection through OpenClaw, which setup has already connected, and so do Stops 2, 3, 5 and 6. The helpers in Stops 3, 4 and 6 call the model through `llm.py`.

## Moving to Cimarron and back

The day runs in three steps: a chat box, an agent in your folder, an agent on your campus cluster. This switch is the third step. OSU's Cimarron cluster can serve the same family of models on campus GPUs. If Cimarron is up, one command moves your Codespace there between stops, and one moves it back:

```
bash 00_setup/switch_backend.sh cimarron
bash 00_setup/switch_backend.sh openrouter
```

The first move to each asks for the word on the card; after that, moving asks for nothing. `bash 00_setup/switch_backend.sh` alone says which one you are on. The labs use the new endpoint from their next run. OpenClaw is reconnected too, but a chat that is already open keeps the old endpoint until you close it (`/exit`) and type `openclaw chat`.

On Cimarron the model's work, reading your prompt and the file contents the agent sends it and writing the reply, happens on OSU hardware in Stillwater instead of at a commercial provider. Nothing else moves: your files still sit in your GitHub Codespace, so the rule about what to bring does not change. You start on OpenRouter. If Cimarron is up, Stop 5 runs on it and moves back at the end; Stop 4, which reads images, stays on OpenRouter. If Cimarron is not up, the switch says so and changes nothing.

## If something goes wrong

- "That word is not the workshop word." A typo: type it again from the card. Letter case does not matter.
- Setup says "That looks like the OSU workshop key, but the workshop endpoint is not set up yet." If you pasted an OpenRouter or NVIDIA key, the paste lost its first characters: copy the whole key and paste it again. If you typed the word from the card, tell a helper.
- "That key was not accepted", or the check prints `reachable` and then `not reachable: HTTP 401`. The paste usually caught a space or missed a character. Run `bash setup.sh --reset-key` and paste the key again. If the instructor has switched the room to another endpoint, run the switch command shown on the screen again instead, because `--reset-key` lets the key choose the endpoint again.
- The check prints `completion: (empty reply, twice)`. The endpoint answered but the model sent no text. Run the check again; if it stays empty, tell a helper.
- Setup says the endpoint "does not know that address or model" after `--model`. The name was mistyped or that endpoint does not serve it. Nothing in `.env` changed, so you are still connected as before.
- With your own NVIDIA key, setup says the endpoint "does not know that address or model" with HTTP 404, and the model list loaded fine. The key was accepted; NVIDIA opens only some hosted models to a personal account. Use the model setup suggests, or ask help@build.nvidia.com to enable Public API Endpoints for your account.
- After `--model`, the check still names the old model. Run `bash setup.sh --model <name>` again and read its last box: it shows the model it saved. Ask a helper if it still differs.
- After the key is accepted, setup says `OpenClaw is not connected yet. To try again:   bash setup.sh --openclaw`. The check does not need OpenClaw, so run the check first. Then, for Stop 1, run `bash setup.sh --openclaw`, which tries again and opens OpenClaw; the reason it failed is in `~/.osu-llm-workshop-openclaw.log`.
- `switch_backend.sh cimarron` says "Cimarron is not connected for this workshop yet". The endpoint is not up; nothing changed, and you are still on OpenRouter.
