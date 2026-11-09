# Stop 0: Everyone green

Stop 0, about 30 minutes, from 8:30. Folder: `00_setup/`.

## You will be able to

- Run one command in your Codespace that reaches the model and the agent, and say what each of the three lines it prints means.
- Say where the model runs.

## The idea

The model does not run in your Codespace. Your Codespace is a small computer that GitHub lends you; it has no GPU (the graphics chip that large models need to run fast) and holds no model. The model runs on a GPU server somewhere else, and your code reaches it over the internet.

An endpoint is the web address of that server, ending in `/v1`. Your code sends it text in an HTTPS request (the same kind of secure web request your browser makes) and gets text back. Any server that speaks the same request format, the "OpenAI-compatible" format many providers use, works for the chat-only labs. The agent stops also need a model that can call tools, and Stop 4 reads images through OpenRouter only.

A key is a long password that tells the endpoint you are allowed to use it. Setup asks for it once and saves it. Today the word on your card stands in for the key: setup exchanges it for the workshop's key.

`00_setup/check.py` makes two requests and one check. The first request asks the endpoint which models it has, and prints the one the labs will use. For example:

    reachable; serving nvidia/nemotron-3-ultra-550b-a55b

The second request asks the model for a one-word reply and prints what comes back, on a line that starts `completion:`. That text was written on the GPU server, not in your Codespace. The third line says whether OpenClaw, the agent you use from Stop 1 on, is connected to the same endpoint and model.

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
   - an OpenRouter key (starts with `sk-or-`) goes to OpenRouter, and setup then lists the models tested with this workshop (00_setup/models.txt). Press Enter for the first, `nvidia/nemotron-3-ultra-550b-a55b`, or type the number of another. `bash setup.sh --choose-model` shows the list again later
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

   Setup then connects OpenClaw, a complete agent program, to the same model, and says so on a line of its own:

       ✅ OpenClaw is connected to nvidia/nemotron-3-ultra-550b-a55b.

   It opens Stop 1's page in the editor and OpenClaw's chat in this terminal, ready for Stop 1. Leave it open and do not type there yet. If that line says ❌ instead, type `bash setup.sh --openclaw` in a second terminal and look for it again.

3. Run the check, in a second terminal: click the **+** on the terminal panel, then type

   ```
   python 00_setup/check.py
   ```

   You should see three lines. For example:

       reachable; serving nvidia/nemotron-3-ultra-550b-a55b
       completion: ready
       openclaw: connected to nvidia/nemotron-3-ultra-550b-a55b

   The wording of the second line can vary from run to run. Only when all three lines look like this, stick the green note on the back of your laptop lid. If the third line says `not connected`, type the command it gives, then run the check again.

   Before you add any files of your own: whatever you put in this Codespace is stored by GitHub, and whatever the agent reads is sent to the model service. Leave out anything unpublished you are not free to share, any student records, and anything covered by an IRB protocol.

4. If you brought files for the day (a CSV, two or three PDFs, a chart image), drag them from your laptop onto the `mine/` folder in the file tree, then check them, in the same second terminal:

   ```
   python upload_check.py
   ```

   Next comes Stop 1, open in the editor (`00_website/README.md`), typed in the OpenClaw chat in your first terminal.

## Moving to Cimarron and back

The day runs in three steps: a chat box, an agent in your folder, an agent on your campus cluster. This switch is the third step. OSU's Cimarron cluster can serve the same family of models on campus GPUs. If Cimarron is up, one command moves your Codespace there between stops, and one moves it back:

```
bash 00_setup/switch_backend.sh cimarron
bash 00_setup/switch_backend.sh openrouter
```

The first move to each asks for the word on the card; after that, moving asks for nothing. `bash 00_setup/switch_backend.sh` alone says which one you are on. The labs use the new endpoint from their next run. OpenClaw is reconnected too, but a chat that is already open keeps the old endpoint until you close it (`/exit`) and type `openclaw chat`.

On Cimarron the model's work, reading your prompt and the file contents the agent sends it and writing the reply, happens on OSU hardware in Stillwater instead of at a commercial provider. Nothing else moves: your files still sit in your GitHub Codespace.

## Choosing the model on OpenRouter

On OpenRouter you can trade Nemotron for one of the most capable agentic models from other labs, for a stop or for the day:

```
bash 00_setup/choose_model.sh
```

It lists NVIDIA Nemotron 3 Ultra first (Enter keeps it) and four others from the strongest agent benchmarks, chosen to stay under $3 for a person's whole day. That cost is provisional: it is an estimate from published prices until each model has been run through the day's replays. `bash 00_setup/choose_model.sh 3` picks number 3 without asking, and `--list` shows the list and which one you are on. The labs use the new model from their next run; OpenClaw is reconnected too, but an open chat keeps the old model until you close it (`/exit`) and type `openclaw chat`. Stop 4 reads images with Nemotron VL whatever you choose. On Cimarron there is one model, so the script tells you to move back to OpenRouter first.
