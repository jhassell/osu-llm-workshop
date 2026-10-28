# Module 0: Everyone green

Before anything else, every Codespace in the room has to reach the model. This module connects yours with one key and proves it with one command. Every later module sends the same kind of request this check sends, with different text in it.

About 30 minutes. Folder: `00_setup/`.

## You will be able to

- Run one command in your Codespace that reaches the model, and say what each of the two lines it prints means.
- Say where the model runs, and which two settings in `.env` tell the labs how to reach it.

## The idea

The model does not run in your Codespace. Your Codespace is a small computer that GitHub lends you; it has no GPU (the graphics chip that large models need to run fast) and holds no model. The model runs on a GPU server somewhere else, and your code reaches it over the internet.

An endpoint is the web address of that server, ending in `/v1`. Your code sends it text in an HTTPS request (the same kind of secure web request your browser makes) and gets text back. Any server that speaks the same request format, the "OpenAI-compatible" format many providers use, works with every lab today.

A key is a long password that tells the endpoint you are allowed to use it. Setup asks for it once and saves it.

`.env` is a small file in the top folder of your repository where setup saves its settings: `LLM_BASE_URL` (the endpoint), `LLM_API_KEY` (the key), and sometimes `LLM_MODEL` (which model to ask, when the endpoint serves several). Every lab reads its settings from there, so moving to a different model service means changing `.env`, never the code. (If you ever set up a Codespaces secret with one of these names in GitHub, setup uses it and writes it into `.env`; the labs themselves read only `.env`.) `.env` is never committed, which means git never saves it into your repository's history, and you never need to open it, print it, or share it.

`00_setup/check.py` makes two requests. The first asks the endpoint which models it has, and prints the one the labs will use. For example:

    reachable; serving nvidia/nemotron-3-super-120b-a12b

The second request asks the model for a one-word reply and prints what comes back, on a line that starts `completion:`. That text was written on the GPU server, not in your Codespace.

## Predict first

When the check runs, what will its second line say? Write your answer on your card before you run it.

## Do it

1. Remember what the pre-work already did. You copied the template with **Use this template**, created a Codespace, clicked **Trust Folder & Continue**, and pressed Enter at the key prompt with no key. In a new Codespace, setup starts by itself in the first terminal and keeps starting in each new terminal until it has succeeded once. Pressing Enter with no key ended with:

       Codespace ready; endpoint check pending.

   This morning you finish the job. Open your Codespace. If no terminal is open, click the **+** on the terminal panel.

2. Run setup and paste the key from your card. What you paste does not show on screen; that is on purpose. Paste once and press Enter once.

   ```
   bash setup.sh
   ```

   Setup picks the endpoint from the kind of key you paste, and sends the key only to that endpoint:

   - the OSU workshop key from the card goes to the OSU workshop endpoint
   - an OpenRouter key (starts with `sk-or-`) goes to OpenRouter, using `nvidia/nemotron-3-super-120b-a12b`
   - an NVIDIA key (starts with `nvapi-`) goes to NVIDIA's hosted endpoint, using `nvidia/nemotron-3-ultra-550b-a55b`, one of the few models NVIDIA opens to a personal account

   Setup finds the workshop endpoint's address in `workshop-endpoint.txt`, or downloads the instructor's current copy of that file if yours is blank, so a repository made weeks ago still finds it. If the address is not published yet, setup says so plainly and sends the key nowhere. The one exception to choosing by key: if the instructor switches the room to another endpoint, every key you paste goes to that endpoint, so paste the key that goes with it. The same is true if you have set up your own Codespaces secret named `LLM_BASE_URL`.

   You should end at a READY box. For example, with an OpenRouter key:

       Checking the key against the endpoint... ✅
       ==============================================
        READY. Endpoint: https://openrouter.ai/api/v1
        Model: nvidia/nemotron-3-super-120b-a12b
        The key is saved in .env (never committed).

        Next:   python 00_setup/check.py

3. Run the check.

   ```
   python 00_setup/check.py
   ```

   You should see two lines. For example:

       reachable; serving nvidia/nemotron-3-super-120b-a12b
       completion: ready

   The wording of the second line can vary from run to run. Compare it with your prediction, then turn your card green.

## Checkpoint

Show your pair your two lines, and say which machine produced each one: what ran in your Codespace, and what came back from the server.

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
   bash setup.sh --model nvidia/nemotron-3-super-120b-a12b
   python 00_setup/check.py
   ```

4. Stretch (optional), for early finishers. Open `corpus/doc_001.txt` in the editor and read it. Write on your card one thing you would want a program to pull out of it. Look for: a fact you could check against the text.

## What you have now

A Codespace connected to a model, with the endpoint and key saved in `.env`, which every later module reads. You can tell whether the connection works with `python 00_setup/check.py`, and you know the model runs on a server, not in your Codespace. Module 1 uses the same connection through `llm.py`, starting with `ask(prompt)`.

## If something goes wrong

- Setup says "That looks like the OSU workshop key, but the workshop endpoint is not set up yet." If you pasted an OpenRouter or NVIDIA key, the paste lost its first characters: copy the whole key and paste it again. If you pasted the card key, tell a helper.
- "That key was not accepted", or the check prints `reachable` and then `not reachable: HTTP 401`. The paste usually caught a space or missed a character. Run `bash setup.sh --reset-key` and paste the key again. If the instructor has switched the room to another endpoint, run the switch command shown on the screen again instead, because `--reset-key` lets the key choose the endpoint again.
- The check prints `completion: (empty reply, twice)`. The endpoint answered but the model sent no text. Run the check again; if it stays empty, tell a helper.
- Setup says the endpoint "does not know that address or model" after `--model`. The name was mistyped or that endpoint does not serve it. Nothing in `.env` changed, so you are still connected as before.
- With your own NVIDIA key, setup says the endpoint "does not know that address or model" with HTTP 404, and the model list loaded fine. The key was accepted; NVIDIA opens only some hosted models to a personal account. Use the model setup suggests, or ask help@build.nvidia.com to enable Public API Endpoints for your account.
- After `--model`, the check still names the old model. Run `bash setup.sh --model <name>` again and read its last box: it shows the model it saved. Ask a helper if it still differs.
