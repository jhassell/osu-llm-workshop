# Setup

From 8:30, with the welcome; Stop 1 starts at 9:00, or sooner if the room is ready. It connects your Codespace to the model with the word on your card, then takes you straight into Stop 1.

## Do it

1. Open your Codespace. Setup starts by itself in the terminal at the bottom. If you see only a `$` prompt, type `bash setup.sh` and press Enter.

2. At the key prompt, type the word on your card (letter case does not matter) and press Enter. You should see:

       READY. Endpoint: https://openrouter.ai/api/v1
       Model: nvidia/nemotron-3-ultra-550b-a55b
       ✅ OpenClaw is connected to nvidia/nemotron-3-ultra-550b-a55b.

3. Stick the green note on the back of your laptop lid. Setup has opened Stop 1's page in the editor and OpenClaw's chat in the terminal: go on to Stop 1.

If the last line says ❌ instead, click the + on the terminal panel and type `bash setup.sh --openclaw`. Still stuck: pink note up, and a helper comes.

Your own OpenRouter key (`sk-or-...`) or NVIDIA key (`nvapi-...`) works at the same prompt instead of the word.

## Where the model runs

The model does not run in your Codespace, which has no GPU. It runs on a server elsewhere, and your Codespace reaches it over the internet with the key that the word on your card stands for. The key is saved in `.env`, which is never committed.

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
