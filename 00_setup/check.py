"""Module 0: does this Codespace reach the model?

    python 00_setup/check.py

Without a key it prints one line and stops, and that is the pre-work's success
signal. With a key it prints two lines: the model the endpoint serves, and a
one-word reply. Standard library only, so it works before anything is installed.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_env():
    path = ROOT / ".env"
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_env()
BASE = os.environ.get("LLM_BASE_URL", "").rstrip("/")
KEY = os.environ.get("LLM_API_KEY", "")

if not BASE or not KEY:
    print("Codespace ready; endpoint check pending.")
    print("When you have the workshop key, type:  bash setup.sh")
    sys.exit(0)

HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}


def get(url, data=None, timeout=60):
    req = urllib.request.Request(url, data=data, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


try:
    models = get(f"{BASE}/models", timeout=20)
    model = os.environ.get("LLM_MODEL") or models["data"][0]["id"]
    print(f"reachable; serving {model}")
    body = json.dumps({
        "model": model,
        "max_tokens": 200,
        "messages": [{"role": "user", "content": "Reply with the single word: ready"}],
    }).encode()
    reply = get(f"{BASE}/chat/completions", data=body)
    text = (reply["choices"][0]["message"].get("content") or "").strip()
    print(f"completion: {text or '(empty reply; the model may need a larger max_tokens)'}")
except urllib.error.HTTPError as err:
    print(f"not reachable: HTTP {err.code} from {err.url}")
    if err.code in (401, 403):
        print("The key was not accepted. Run:  bash setup.sh --reset-key")
    sys.exit(1)
except Exception as err:  # network, DNS, timeout
    print(f"not reachable: {err}")
    sys.exit(1)
