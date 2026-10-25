# For helpers: the first ten minutes

Carry this on a laptop or a printout. Order matters: the common fixes are first.

1. No terminal, or a terminal with only a `$`. Click in it, type `bash setup.sh`, Enter. If there is no terminal panel at all: the menu at the top left, Terminal, New Terminal.
2. The key prompt is waiting. Pasting does not show anything; that is on purpose. Paste once, press Enter once. If someone typed `bash setup.sh` into the key prompt, setup says so and asks again.
3. Key not accepted. Nine times out of ten the paste caught a space or missed a character. `bash setup.sh --reset-key`, paste again from the card.
4. `not reachable` with a network error. Check the laptop is on the library wifi, not a phone hotspot that has dropped. Then run `python 00_setup/check.py` again. If three people in a row see it, tell the instructor: it is the endpoint, not the laptops.
5. `not reachable` with HTTP 429 or 503. The endpoint is overloaded. Wait thirty seconds and run the check again. If it persists, the instructor switches the room.
6. Trust Folder dialog never clicked. The terminal cannot start until it is. It is a blue button in the editor area, easy to miss behind a tab.
7. Codespace stuck on "Setting up your codespace" for more than five minutes. Go to github.com/codespaces, stop it, start it again. If that fails, delete it and create a new one from their repository; it builds in three minutes.
8. No GitHub account, or the template step was skipped. Pair them with a neighbor for the morning. A helper creates the repository and Codespace with them at the break.
9. The whole room is red at 8:50. Instructor's call: `bash 00_setup/switch_backend.sh <second url> <model name>` on screen, second key on the cards. The model name matters on a hosted endpoint that serves many models.

What not to do: do not edit anyone's `.env` by hand, do not type a key for them on a shared screen, and do not delete `mine/`.
