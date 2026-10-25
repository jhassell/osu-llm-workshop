# Module 0: everyone green

By the end you can run one command in your Codespace that reaches the model, and say what the two lines it prints mean.

The one command:

    python 00_setup/check.py

Predict first. What will the second line say when the check runs?

## Build

1. Open your Codespace. If a terminal is not open, open one (the **+** on the terminal panel).
2. Type `bash setup.sh` and paste the key from the card at the front. It does not show as you paste; press Enter.
3. Run the check. Two lines: the model the endpoint serves, and a one-word reply. Turn your card green.
4. Early finishers: open `corpus/doc_001.txt`, read it, and write on your card one thing you would want pulled out of it.

Where does the model actually live? Not in your Codespace. The check sent one HTTPS request to the endpoint in `.env`, and a GPU somewhere else answered. Every lab today is that same request with different text in it.

## If it goes wrong

Helpers walk the room with `00_setup/troubleshooting.md`. If the room is not green by 8:50 the instructor switches everyone to a second endpoint:

    bash 00_setup/switch_backend.sh <url> <model>

and hands out a second key. Anyone still blocked by a GitHub or Codespace problem works on their pair's laptop for the morning while a helper sorts it out.
