"""The only two calls the morning needs.

    from llm import ask, ask_json
    ask("Summarize this in two sentences: ...")          -> str
    ask_json("Fill in the record for ...", Record)       -> Record

Both talk to one OpenAI-compatible endpoint named by two values in .env:
LLM_BASE_URL and LLM_API_KEY. Nothing in this file is specific to a vendor.
Optional: LLM_MODEL picks a model; otherwise the first one the endpoint lists.
"""
import json
import os
import re
from pathlib import Path

from openai import OpenAI
from pydantic import BaseModel, ValidationError

ROOT = Path(__file__).resolve().parent


def _load_env():
    """Read .env next to this file into the environment, without overriding
    values already set (a Codespaces secret wins over the file)."""
    path = ROOT / ".env"
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env()
BASE_URL = os.environ.get("LLM_BASE_URL", "").rstrip("/")
API_KEY = os.environ.get("LLM_API_KEY", "")
MODEL = os.environ.get("LLM_MODEL", "")

if not BASE_URL or not API_KEY:
    raise SystemExit(
        "No endpoint or key yet. Run:  bash setup.sh   (it writes LLM_BASE_URL and LLM_API_KEY to .env)"
    )

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)


def model_name() -> str:
    """The model every call uses. Asked of the endpoint once, then remembered."""
    global MODEL
    if not MODEL:
        MODEL = client.models.list().data[0].id
    return MODEL


def chat(messages, tools=None, max_tokens=1200, temperature=0.2):
    """One round trip. Returns the assistant message object (content, tool_calls).
    max_tokens is generous because some models think before they answer, and
    the thinking counts."""
    kwargs = dict(model=model_name(), messages=messages, max_tokens=max_tokens, temperature=temperature)
    if tools:
        kwargs["tools"] = tools
    message = client.chat.completions.create(**kwargs).choices[0].message
    if message.content and "<think>" in message.content:
        # Some servers return a model's thinking inline. It is not the answer.
        message.content = re.sub(r"<think>.*?</think>\s*", "", message.content, flags=re.S)
    if not message.tool_calls and not (message.content or "").strip():
        # A thinking model occasionally finishes its thinking and says nothing.
        # One more try, with room to spare, before anyone sees an empty reply.
        kwargs["max_tokens"] = max_tokens * 2
        message = client.chat.completions.create(**kwargs).choices[0].message
    return message


def ask(prompt: str, system: str | None = None) -> str:
    """Send one prompt, get the text back."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return (chat(messages).content or "").strip()


def _json_text(text: str) -> str:
    """The first {...} block in a reply, with any code fence removed."""
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.S)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object in the reply")
    return text[start : end + 1]


def ask_json(prompt: str, Model: type[BaseModel], system: str | None = None):
    """Send one prompt, get back an instance of Model.

    The model is shown the JSON schema and asked for one object. If the reply
    does not fit the schema, the error is sent back once and the model gets one
    more try. After that the error is raised, so a bad record is never silently
    accepted."""
    schema = json.dumps(Model.model_json_schema(), indent=1)
    rules = (
        "Reply with exactly one JSON object and nothing else: no prose, no code fence. "
        "It must match this JSON schema:\n" + schema
    )
    messages = [{"role": "system", "content": (system + "\n\n" if system else "") + rules},
                {"role": "user", "content": prompt}]
    text = chat(messages).content or ""
    try:
        return Model.model_validate_json(_json_text(text))
    except (ValidationError, ValueError) as err:
        messages += [
            {"role": "assistant", "content": text},
            {"role": "user", "content": f"That did not fit the schema. The error was:\n{err}\n"
                                        "Reply again with exactly one JSON object and nothing else."},
        ]
        text = chat(messages).content or ""
        return Model.model_validate_json(_json_text(text))
