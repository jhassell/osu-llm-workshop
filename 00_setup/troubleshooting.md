# For helpers: the first ten minutes

Carry this on a laptop or a printout. Order matters: the common fixes are first.

1. No terminal, or a terminal with only a `$`. Click in it, type `bash setup.sh`, Enter. If there is no terminal panel at all: the menu at the top left, Terminal, New Terminal.
2. The key prompt is waiting. Pasting does not show anything; that is on purpose. Paste once, press Enter once. If someone typed `bash setup.sh` into the key prompt, setup says so and asks again.
3. Setup chooses the endpoint from the key: a key starting `sk-or-` goes to OpenRouter, one starting `nvapi-` goes to NVIDIA's hosted endpoint, anything else is treated as the OSU workshop key from the card. The workshop address comes from `workshop-endpoint.txt` in their repository, or, if that is blank, from the instructor's current copy online, so an old copy of the repository finds it too.
   - "That looks like the OSU workshop key, but the workshop endpoint is not set up yet." Ask what they pasted. If it was an OpenRouter or NVIDIA key, the paste lost its first characters: copy the whole key and paste again. If it was the card key, tell the instructor: either the address is not published yet, or their Codespace could not download it.
   - "That key was not accepted." Nine times out of ten the paste caught a space or missed a character. `bash setup.sh --reset-key`, paste again from the card.
4. The check prints `reachable` and then `not reachable: HTTP 401` or `403`. The key was refused. `bash setup.sh --reset-key`, paste again.
5. The check prints `completion: (empty reply, twice)`. The model answered with no text, even after a retry with more room. Run the check once more. If it stays empty for several people, tell the instructor.
6. `not reachable` with a network error. The check runs in the Codespace, on GitHub's machine, so the laptop's wifi is not the path that failed, as long as the terminal still responds. If the browser tab lost its connection, VS Code shows a reconnecting message and nothing typed works: fix the laptop's wifi first. Otherwise read the error text: a name that cannot be resolved, a refused connection, or a timeout. Run the check again, and give the instructor the exact error line if it repeats.
7. `not reachable` with HTTP 429 or 503. The endpoint is busy. Wait thirty seconds and run the check again. If it persists, tell the instructor.
8. After `bash setup.sh --model <name>`, the check still names the old model. The labs and the check read only `.env`, so look at the model line in setup's last box; if setup reported an error, the model name is wrong for this endpoint. A Codespaces secret `LLM_MODEL` only matters to setup, and `--model` overrides it.
9. Trust Folder dialog never clicked. The terminal cannot start until it is. It is a blue button in the editor area, easy to miss behind a tab.
10. Codespace stuck on "Setting up your codespace" for more than five minutes. Go to github.com/codespaces, stop it, start it again. If that fails, delete it and create a new one from their repository; it builds in three minutes.
11. No GitHub account, or the template step was skipped. Pair them with a neighbor for the morning. A helper creates the repository and Codespace with them at the break.
12. After the instructor switches the room (`bash 00_setup/switch_backend.sh ...` on screen), every pasted key goes to that endpoint, so make sure people paste the key for it. To redo the paste after a switch, run the switch command again, not `bash setup.sh --reset-key`, which lets the key choose the endpoint again.

What not to do: do not open, print or edit anyone's `.env` by hand, do not type a key for them on a shared screen, and do not delete `mine/`. To see which settings `.env` holds without showing the key: `grep -o '^[A-Z_]*=' .env`.
