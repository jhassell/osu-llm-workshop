# Thursday morning: keeping this working

The workshop key stops working at the end of the day. Everything you built keeps working the moment you point it at another endpoint, because the only two things the code knows are in .env:

    LLM_BASE_URL=...
    LLM_API_KEY=...

For an OpenRouter key (starts with `sk-or-`) or an NVIDIA key (starts with `nvapi-`), run `bash setup.sh --reset-key` and paste it: setup recognizes the key and picks the endpoint and a Nemotron model itself. For any other endpoint, run `bash setup.sh --reset-key --base-url <url>` and paste its key, or edit .env by hand. Then `python 00_setup/check.py` tells you whether it worked. Three places to point it:

1. Cimarron, for anyone with an OSU HPCC account. The HPCC will supply a short note on running the same model there and reaching it from your own machine. (Paragraph to come from HPCC; this file is updated when it arrives.)
2. A hosted endpoint. NVIDIA's hosted models at build.nvidia.com serve the same API: create a free developer account, make an API key, and paste it into `bash setup.sh --reset-key`. OpenRouter (openrouter.ai) serves the same Nemotron models with a pay-as-you-go key that works the same way. Other OpenAI-compatible hosts work the same way; only the URL and key change.
3. Your own laptop. Ollama, LM Studio, and vLLM all serve the same API on localhost. For example, with Ollama running a small model, the base URL is http://localhost:11434/v1 and any non-empty string is the key. The labs are slower on a laptop and the small models make more mistakes, which is itself instructive.

Your Codespace keeps your files when it is stopped. It is deleted after a retention period you can set at https://github.com/settings/codespaces. The repository itself is yours forever; the Codespace is only a place to run it. To run the labs on your own computer instead: clone the repository, `pip install -r requirements.txt`, write .env, and the same commands work.
