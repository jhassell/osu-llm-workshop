#!/usr/bin/env bash
# osu-llm-workshop setup: connects this Codespace to the workshop model.
#
# In a new Codespace this starts BY ITSELF in the first terminal (see
# .devcontainer/autostart.sh) and keeps doing so in new terminals until it has
# succeeded once. If a terminal only shows a line ending in $, type:
#
#   bash setup.sh                   set up (or repair) the connection
#   bash setup.sh --reset-key       forget the saved key and ask for a new one
#   bash setup.sh --base-url URL    point the labs at a different endpoint
#   bash setup.sh --model NAME      pick a model by name
#
# Everything the labs need is two values, written to .env in this folder:
#   LLM_BASE_URL   the endpoint, an OpenAI-compatible URL ending in /v1
#   LLM_API_KEY    the key for that endpoint
#   LLM_MODEL      optional; the model to use when the endpoint serves more than one
#
# The key decides the endpoint. Paste any of these at the prompt:
#   the OSU workshop key   (from the card)        goes to the OSU workshop endpoint
#   an OpenRouter key      (starts with sk-or-)   goes to OpenRouter
#   an NVIDIA key          (starts with nvapi-)   goes to NVIDIA's hosted endpoint
# A key is only ever sent to the endpoint it belongs to. --base-url, or a
# Codespaces secret LLM_BASE_URL, overrides this and uses that endpoint instead.
#
# Where each value comes from, first match wins:
#   1. a Codespaces secret of the same name (nothing to type)
#   2. the value saved by an earlier run, in .env (the key is skipped by --reset-key)
#   3. the terminal asks you for the key; what you paste does not show on screen.
#      Press Enter without a key to finish the pre-work: the Codespace is ready
#      and the endpoint check waits for the key.
#
# Switches for test harnesses:
#   WORKSHOP_FORCE=1     run even though setup is already running in another terminal
#   WORKSHOP_NO_PROMPT=1 never ask for a key (behave as if Enter was pressed)
#
# Adapted from jhassell/asee9 (CC BY 4.0): the run-once lock, the hidden key
# prompt and the key check are the same design; the provider is different.
set -uo pipefail

# The three endpoints a pasted key can belong to. The OSU one comes from
# workshop-endpoint.txt in this folder, which the instructor fills in when the
# workshop endpoint exists. A copy made from the template before that has an
# empty file, so setup then reads the current file from the instructor's public
# repository (a plain download; no key is sent). Until the address exists
# anywhere, a workshop key is refused with a plain message, never sent.
OSU_BASE_URL=""                                   # leave empty; set workshop-endpoint.txt instead
OSU_MODEL=""
WORKSHOP_ENDPOINT_URL="https://raw.githubusercontent.com/jhassell/osu-llm-workshop/main/workshop-endpoint.txt"
OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"
OPENROUTER_MODEL="nvidia/nemotron-3-super-120b-a12b"
NVIDIA_BASE_URL="https://integrate.api.nvidia.com/v1"
# NVIDIA opens only some hosted models to a personal account: on 2026-10-28 a fresh
# account got 404 from nvidia/nemotron-3-super-120b-a12b and 200 from this one.
NVIDIA_MODEL="nvidia/nemotron-3-ultra-550b-a55b"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$ROOT/.env"

# Everything the exit trap touches is defined here, before anything can fail,
# so `set -u` can never trip inside the trap.
TMP=""
DOTS_PID=""
DOTS_MSG=""
READING=0
STOPPED=0                                     # 1 after Ctrl+C, a closed terminal, or a kill
READY_DONE=0                                  # 1 once READY is reached
LOCK="$HOME/.osu-llm-workshop-setup.lock"     # run-once lock shared with autostart.sh
MARKER="$HOME/.osu-llm-workshop-ready"        # written at READY; autostart.sh then stays quiet
AUTOSTART_TAG="# osu-llm-workshop-autostart"
# Anything this script starts must never re-trigger the autostart hook.
export WORKSHOP_NO_AUTOSTART=1

RESET_KEY=0
BASE_ARG=""
MODEL_ARG=""
while [ $# -gt 0 ]; do
  case "$1" in
    --reset-key) RESET_KEY=1 ;;
    --base-url) shift; BASE_ARG="${1:-}" ;;
    --model) shift; MODEL_ARG="${1:-}" ;;
    -h|--help) sed -n '2,25p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown option: $1   (try: bash setup.sh --help)"; exit 2 ;;
  esac
  shift
done

# The key lives in shell variables only. A Codespaces secret arrives exported;
# take it and un-export it at once, so no tool this script runs inherits it. It
# goes to curl through a config file on stdin, never on a command line.
SECRET_KEY="${LLM_API_KEY:-}"
SECRET_KEY="${SECRET_KEY//[[:space:]]/}"
unset LLM_API_KEY
SECRET_BASE="${LLM_BASE_URL:-}"
SECRET_BASE="${SECRET_BASE//[[:space:]]/}"
unset LLM_BASE_URL
SECRET_MODEL="${LLM_MODEL:-}"
SECRET_MODEL="${SECRET_MODEL//[[:space:]]/}"
unset LLM_MODEL
MODEL=""
KEY=""
BASE=""

hr() { echo "=============================================="; }

# ------------------------------------------------------------ moving dots
dots_tty() {
  [ -t 1 ] && { : >/dev/tty; } 2>/dev/null
}
dots_start() {   # $1 = message, without trailing dots
  dots_stop fail
  DOTS_MSG="$1"
  if dots_tty; then
    (
      while kill -0 $$ 2>/dev/null; do
        for d in "." ".." "..."; do
          printf '\r\033[K%s%s' "$DOTS_MSG" "$d" >/dev/tty 2>/dev/null || exit 0
          sleep 0.4
        done
      done
    ) &
    DOTS_PID=$!
  else
    echo "${DOTS_MSG}..."
  fi
}
dots_stop() {    # $1 = ok | fail
  [ -n "$DOTS_MSG" ] || return 0
  local mark="✅"
  [ "${1:-ok}" = "ok" ] || mark="❌"
  if [ -n "$DOTS_PID" ]; then
    kill "$DOTS_PID" 2>/dev/null
    wait "$DOTS_PID" 2>/dev/null
    DOTS_PID=""
    printf '\r\033[K' >/dev/tty 2>/dev/null
  fi
  echo "${DOTS_MSG}... ${mark}" 2>/dev/null
  DOTS_MSG=""
}

# ------------------------------------------------------ run-once lock
# autostart.sh takes the lock (a directory holding a PID) before it starts this
# script, so a second terminal stays quiet while setup runs. We own the lock if
# it names us, our parent (the terminal that autostart ran in), no one, or a
# process that no longer exists.
lock_owner() {
  local pid="" start=""
  { read -r pid; read -r start; } 2>/dev/null <"$LOCK/pid"
  printf '%s %s' "$pid" "$start"
}
proc_start() {
  ps -o lstart= -p "$1" 2>/dev/null | awk '{$1=$1; print}'
}
lock_write() {
  printf '%s\n%s\n' "$$" "$(proc_start $$)" >"$LOCK/pid" 2>/dev/null
}
mutex_take() {
  mkdir "$1" 2>/dev/null && return 0
  [ -n "$(find "$1" -maxdepth 0 -mmin +1 2>/dev/null)" ] || return 1
  mv "$1" "$1.old.$$" 2>/dev/null || return 1
  rm -rf "$1.old.$$"
  mkdir "$1" 2>/dev/null
}
lock_held_by_other() {
  local pid start now
  read -r pid start <<<"$(lock_owner)"
  if [ -z "$pid" ]; then
    [ -z "$(find "$LOCK" -maxdepth 0 -mmin +1 2>/dev/null)" ]
    return
  fi
  [ "$pid" != "$$" ] && [ "$pid" != "$PPID" ] || return 1
  kill -0 "$pid" 2>/dev/null || return 1
  now="$(proc_start "$pid")"
  [ -z "$start" ] || [ -z "$now" ] || [ "$start" = "$now" ]
}
lock_claim() {
  local pid start
  if mkdir "$LOCK" 2>/dev/null; then lock_write; return 0; fi
  read -r pid start <<<"$(lock_owner)"
  if [ -n "$pid" ] && { [ "$pid" = "$$" ] || [ "$pid" = "$PPID" ]; }; then
    lock_write; return 0
  fi
  if lock_held_by_other; then
    if [ -t 0 ] && [ -z "${WORKSHOP_FORCE:-}" ]; then
      echo
      echo "⚠️  Setup has already started in another terminal."
      echo "   Switch to it: the list of terminals at the right edge of this panel."
      echo "   Pick the first one. If it asks for your key, paste it there."
      exit 0
    fi
    return 0
  fi
  mutex_take "$LOCK.takeover" || return 0
  if lock_held_by_other; then rmdir "$LOCK.takeover" 2>/dev/null; return 0; fi
  rm -rf "$LOCK"
  if mkdir "$LOCK" 2>/dev/null; then lock_write; fi
  rmdir "$LOCK.takeover" 2>/dev/null
  return 0
}
lock_release() {
  [ -d "$LOCK" ] || return 0
  local pid start
  read -r pid start <<<"$(lock_owner)"
  if [ -z "$pid" ] || [ "$pid" = "$$" ]; then
    rm -rf "$LOCK"
  fi
}

# ------------------------------------------------ autostart line in ~/.bashrc
install_autostart_line() {
  [ "${CODESPACES:-}" = "true" ] || return 0
  local hook="$ROOT/.devcontainer/autostart.sh" rc="$HOME/.bashrc" line
  [ -f "$hook" ] || return 0
  line="$(printf 'if [ -f %q ]; then . %q; fi  %s' "$hook" "$hook" "$AUTOSTART_TAG")"
  touch "$rc" 2>/dev/null || return 0
  grep -qxF "$line" "$rc" && return 0
  if grep -qF "$AUTOSTART_TAG" "$rc"; then
    grep -vF "$AUTOSTART_TAG" "$rc" >"$rc.ac.$$" && cat "$rc.ac.$$" >"$rc"
    rm -f "$rc.ac.$$"
  fi
  printf '\n%s\n' "$line" >>"$rc"
}

# ------------------------------------------------- the pasted-command catch
# Setup starts by itself, so people sometimes type "bash setup.sh" at the key
# prompt, and with hidden input they cannot see that they did.
entry_is_command() {
  case "$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')" in
    *setup.sh*|*"bash "*|*python*) return 0 ;;
  esac
  return 1
}

# ------------------------------------------------------------ exit paths
on_exit() {
  dots_stop fail
  if [ "$READING" -eq 1 ]; then
    stty echo </dev/tty 2>/dev/null
    echo
  fi
  if [ -n "$TMP" ]; then rm -rf "$TMP"; fi
  lock_release
  if [ "$STOPPED" -eq 1 ] && [ "$READY_DONE" -eq 0 ]; then
    echo "Setup stopped. To start again, type: bash setup.sh" 2>/dev/null
  fi
}
trap on_exit EXIT
trap 'STOPPED=1; exit 130' INT
trap 'STOPPED=1; exit 143' TERM
trap 'STOPPED=1; exit 129' HUP

die() {
  dots_stop fail
  echo
  echo "❌ $1"
  echo
  echo "   $2"
  echo "   Still stuck? See the Troubleshooting table in README.md."
  exit 1
}

lock_claim

hr; echo " osu-llm-workshop: setup"; hr
echo "Repository version: $(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null || echo unknown)"
if [ -n "${WORKSHOP_AUTOSTARTED:-}" ]; then
  echo "Setup started by itself."
fi

install_autostart_line 2>/dev/null || true

# ------------------------------------------------------------- 1. tooling
# Everything that does not need your key happens first, so a container problem
# surfaces before you are asked for a key.
if ! python3 -c 'import openai, pydantic, pypdf, docx' 2>/dev/null; then
  echo "Installing Python libraries (this only happens once)..."
  pip install --user --quiet -r "$ROOT/requirements.txt" >/tmp/python-install.log 2>&1 || true
  python3 -c 'import openai, pydantic, pypdf, docx' 2>/dev/null \
    || die "The Python libraries could not be installed." \
           "Read the last lines of /tmp/python-install.log. Then stop and start the Codespace, or rebuild it (Ctrl+Shift+P, Codespaces: Rebuild Container); both keep your files."
fi
echo "✅ Python libraries present."

TMP="$(mktemp -d)"   # private to this user (mode 700); removed on every exit

# ------------------------------------------------------------- 2. saved values
env_value() {   # $1 = name; prints the value saved in .env, or nothing
  [ -f "$ENV_FILE" ] || return 0
  sed -n "s/^$1=//p" "$ENV_FILE" | tail -1 | tr -d '[:space:]"'"'"
}
write_env() {   # $1 = base url, $2 = key (may be empty), $3 = model (may be empty)
  ( umask 077
    {
      echo "# Written by setup.sh. Two values are all the labs need."
      if [ -n "$1" ]; then echo "LLM_BASE_URL=$1"; else echo "# LLM_BASE_URL=   (bash setup.sh fills this in from the key you paste)"; fi
      if [ -n "$2" ]; then echo "LLM_API_KEY=$2"; else echo "# LLM_API_KEY=   (paste the workshop key here, or run: bash setup.sh)"; fi
      if [ -n "$3" ]; then echo "LLM_MODEL=$3"; fi
    } >"$ENV_FILE.new" ) && mv -f "$ENV_FILE.new" "$ENV_FILE" && chmod 600 "$ENV_FILE"
}

# ------------------------------------------------------------- 3. the endpoint
# BASE_SOURCE says who chose the endpoint: arg or secret (fixed: every key goes
# there), saved (the pair saved by an earlier run), or key (chosen below from
# the key itself, and chosen again if a different key is pasted).
BASE_SOURCE="key"
if [ -n "$BASE_ARG" ]; then
  BASE="$BASE_ARG"; BASE_SOURCE="arg"; echo "Endpoint from --base-url: $BASE"
elif [ -n "$SECRET_BASE" ]; then
  BASE="$SECRET_BASE"; BASE_SOURCE="secret"; echo "Endpoint from your Codespaces secret LLM_BASE_URL: $BASE"
elif [ "$RESET_KEY" -eq 0 ] && [ -z "$SECRET_KEY" ] && [ -n "$(env_value LLM_API_KEY)" ] && BASE="$(env_value LLM_BASE_URL)" && [ -n "$BASE" ]; then
  BASE_SOURCE="saved"; echo "Endpoint saved in .env: $BASE"
else
  BASE=""
fi
check_url() {
  case "$BASE" in
    http://*|https://*) BASE="${BASE%/}" ;;
    *) die "The endpoint \"$BASE\" is not a URL." "It should look like https://host/v1. Run: bash setup.sh --base-url https://host/v1" ;;
  esac
}
[ -z "$BASE" ] || check_url

# The model. Named with --model or a secret, it is used as is. Otherwise each
# endpoint has a default (above), and where that is empty the check below picks
# a Nemotron chat model from the models the endpoint lists.
MODEL_SOURCE=""
if [ -n "$MODEL_ARG" ]; then MODEL="$MODEL_ARG"; MODEL_SOURCE="named"; echo "Model from --model: $MODEL"
elif [ -n "$SECRET_MODEL" ]; then MODEL="$SECRET_MODEL"; MODEL_SOURCE="named"; echo "Model from your Codespaces secret LLM_MODEL: $MODEL"
elif [ "$BASE_SOURCE" = "saved" ] && MODEL="$(env_value LLM_MODEL)" && [ -n "$MODEL" ]; then MODEL_SOURCE="saved"; echo "Model saved in .env: $MODEL"
else MODEL=""; fi

# Which endpoint a key belongs to, from its shape.
provider_of() {
  case "$1" in
    sk-or-*) echo openrouter ;;
    nvapi-*) echo nvidia ;;
    *)       echo osu ;;
  esac
}
# load_osu_endpoint: fill OSU_BASE_URL and OSU_MODEL from workshop-endpoint.txt
# here, or, if that has no address, from the instructor's current copy online.
load_osu_endpoint() {
  [ -z "$OSU_BASE_URL" ] || return 0
  local txt=""
  [ -f "$ROOT/workshop-endpoint.txt" ] && txt="$(cat "$ROOT/workshop-endpoint.txt")"
  if ! printf '%s\n' "$txt" | grep -qE '^OSU_BASE_URL=https://'; then
    txt="$(curl -fsS -m 10 "$WORKSHOP_ENDPOINT_URL" 2>/dev/null)" || txt=""
  fi
  OSU_BASE_URL="$(printf '%s\n' "$txt" | sed -n 's/^OSU_BASE_URL=//p' | tail -1 | tr -d '[:space:]')"
  OSU_MODEL="$(printf '%s\n' "$txt" | sed -n 's/^OSU_MODEL=//p' | tail -1 | tr -d '[:space:]')"
  case "$OSU_BASE_URL" in https://*) ;; *) OSU_BASE_URL=""; OSU_MODEL="" ;; esac   # HTTPS only: the key travels there
}

# endpoint_for_key: when the key decides (BASE_SOURCE=key), set BASE and the
# default MODEL for the provider the key belongs to. Returns 1, with a message,
# when that provider's endpoint is not configured.
endpoint_for_key() {
  [ "$BASE_SOURCE" = "key" ] || return 0
  local p name model
  p="$(provider_of "$KEY")"
  case "$p" in
    openrouter) BASE="$OPENROUTER_BASE_URL"; model="$OPENROUTER_MODEL"; name="an OpenRouter key" ;;
    nvidia)     BASE="$NVIDIA_BASE_URL";     model="$NVIDIA_MODEL";     name="an NVIDIA key" ;;
    osu)        load_osu_endpoint
                BASE="$OSU_BASE_URL";        model="$OSU_MODEL";        name="the OSU workshop key" ;;
  esac
  if [ -z "$BASE" ]; then
    echo "That looks like the OSU workshop key, but the workshop endpoint is not set up yet."
    echo "Use an OpenRouter key (starts with sk-or-) or an NVIDIA key (starts with nvapi-) for now,"
    echo "or press Enter to finish without a key."
    return 1
  fi
  check_url
  if [ "$MODEL_SOURCE" != "named" ]; then MODEL="$model"; fi
  echo "That is ${name}: using $BASE"
}

# ------------------------------------------------------------- 4. the key
# check_key: two requests. First GET $BASE/models, which shows the endpoint is
# there and which models it serves. Some hosted endpoints (OpenRouter, NVIDIA)
# answer that without looking at the key, so the second request asks the chosen
# model for one token: that needs a real key, and it proves the model name works.
# It costs a fraction of a cent. The key goes to curl as a config file on stdin
# (printf is a shell builtin, so it is never on any command line). Sets HTTP to
# the status of the last request, 000 on a network failure.
check_key() {
  HTTP="$(printf 'header = "Authorization: Bearer %s"\n' "$KEY" \
    | curl -s -m 20 -K - -o "$TMP/models.json" -w '%{http_code}' "$BASE/models")"
  HTTP="${HTTP:0:3}"; HTTP="${HTTP:-000}"
  [ "$HTTP" = "200" ] || return 0
  [ -n "$MODEL" ] || MODEL="$(pick_model)"
  python3 - "$MODEL" "$TMP/probe.json" <<'PYEOF' 2>/dev/null
import json, sys
body = {"messages": [{"role": "user", "content": "Reply with one word: ready"}], "max_tokens": 1}
if sys.argv[1]:
    body["model"] = sys.argv[1]
json.dump(body, open(sys.argv[2], "w"))
PYEOF
  HTTP="$(printf 'header = "Authorization: Bearer %s"\n' "$KEY" \
    | curl -s -m 60 -K - -H 'Content-Type: application/json' -d @"$TMP/probe.json" \
        -o "$TMP/probe.out" -w '%{http_code}' "$BASE/chat/completions")"
  HTTP="${HTTP:0:3}"; HTTP="${HTTP:-000}"
}
# The same wording for a 400 or 404 everywhere: a wrong endpoint address or
# model name. The endpoint's own explanation is shown when it gives one: an
# OpenAI-style {"error": ...}, NVIDIA's {"title", "detail"}, or a plain-text
# body such as "404 page not found".
not_found() {
  local why hint
  why="$(python3 - "$TMP/probe.out" "$TMP/models.json" <<'PYEOF' 2>/dev/null
import json, sys
for path in sys.argv[1:]:
    try:
        text = open(path, errors="replace").read()
    except Exception:
        continue
    msg = ""
    try:
        body = json.loads(text)
        if isinstance(body, dict):
            e = body.get("error")
            if isinstance(e, dict):
                msg = e.get("message") or ""
            elif e:
                msg = str(e)
            else:
                msg = " ".join(str(body[k]) for k in ("title", "detail", "message") if body.get(k))
    except Exception:
        msg = text if "<" not in text else ""
    msg = " ".join(msg.split())
    if msg:
        print(msg[:200])
        break
PYEOF
)"
  hint="Check the endpoint and model, for example: bash setup.sh --reset-key --model <name>"
  if [ "$(provider_of "$KEY")" = "nvidia" ] && [ "$HTTP" = "404" ]; then
    hint="NVIDIA opens only some hosted models to a personal account; the key itself was accepted.
   Ask help@build.nvidia.com to enable Public API Endpoints for your account, or try another model:"
    if [ "$MODEL" = "$NVIDIA_MODEL" ]; then
      hint="$hint bash setup.sh --reset-key --model <name>"
    else
      hint="$hint bash setup.sh --reset-key --model $NVIDIA_MODEL"
    fi
  fi
  die "The endpoint refused the request (HTTP $HTTP): it does not know that address or model${MODEL:+ ($MODEL)}.${why:+ It said: $why}" \
      "$hint"
}

# pick_model: from the saved /models reply, a Nemotron chat model if there is
# one (a "super" one first, then the newer nvidia/nemotron-* names), skipping
# embedding, reward, safety, retrieval and vision models; otherwise the first
# chat model; otherwise the first model. An endpoint serving one model gets it.
pick_model() {
  python3 - "$TMP/models.json" <<'PYEOF' 2>/dev/null
import json, sys
try:
    ids = [m["id"] for m in (json.load(open(sys.argv[1])).get("data") or []) if m.get("id")]
except Exception:
    ids = []
skip = ("embed", "reward", "guard", "safety", "rerank", "retriev", "parse", "ocr", "-vl", "vlm",
        "vision", "audio", "speech", "asr", "tts", "clip", "translate")
chat = [i for i in ids if not any(s in i.lower() for s in skip)]
nemo = [i for i in chat if "nemotron" in i.lower()]
nemo.sort(key=lambda i: ("super" not in i.lower(), not i.lower().startswith("nvidia/nemotron")))
for group in (nemo, chat, ids):
    if group:
        print(group[0])
        break
PYEOF
}
key_looks_right() {
  [ "${#KEY}" -ge 8 ] && [[ "$KEY" != *[[:space:]]* ]]
}

if [ "$RESET_KEY" -eq 1 ]; then
  rm -f "$MARKER"
  echo "Forgot the saved key."
  if [ -n "$SECRET_KEY" ]; then
    echo "Your Codespaces secret LLM_API_KEY is not used this time: --reset-key asks for the key instead."
    SECRET_KEY=""
  fi
fi

if [ -n "$SECRET_KEY" ]; then
  echo "Using your Codespaces secret LLM_API_KEY"
  KEY="$SECRET_KEY"
  endpoint_for_key || die "The key in your Codespaces secret LLM_API_KEY has no endpoint yet." \
    "Add a Codespaces secret LLM_BASE_URL with the endpoint, or use an OpenRouter or NVIDIA key."
  dots_start "Checking the key against the endpoint"
  check_key
  case "$HTTP" in
    200) dots_stop ok ;;
    401|403) dots_stop fail
      die "The endpoint did not accept the key in your Codespaces secret LLM_API_KEY (HTTP $HTTP)." \
          "Fix the secret at https://github.com/settings/codespaces, then stop and restart this Codespace." ;;
    400|404) not_found ;;
    000) die "Could not reach $BASE (network)." "Check your connection, then run bash setup.sh again." ;;
    *) die "Unexpected reply from the endpoint (HTTP $HTTP)." "Wait a minute, then run bash setup.sh again." ;;
  esac
elif [ "$RESET_KEY" -eq 0 ] && KEY="$(env_value LLM_API_KEY)" && [ -n "$KEY" ]; then
  echo "Using the key saved in .env (to change it: bash setup.sh --reset-key)"
  endpoint_for_key || KEY=""
  if [ -n "$KEY" ]; then
    dots_start "Checking the key against the endpoint"
    check_key
    case "$HTTP" in
      200) dots_stop ok ;;
      401|403) dots_stop fail; echo "   The saved key no longer works. Forgetting it."; KEY=""
        # The next key pasted chooses its own endpoint and model again.
        if [ "$BASE_SOURCE" = "saved" ]; then BASE_SOURCE="key"; fi
        if [ "$MODEL_SOURCE" = "saved" ]; then MODEL=""; MODEL_SOURCE=""; fi ;;
      400|404) not_found ;;
      000) die "Could not reach $BASE (network)." "Check your connection, then run bash setup.sh again." ;;
      *) die "Unexpected reply from the endpoint (HTTP $HTTP)." "Wait a minute, then run bash setup.sh again." ;;
    esac
  fi
else
  KEY=""
fi

if [ -z "$KEY" ] && [ -z "${WORKSHOP_NO_PROMPT:-}" ] && { : </dev/tty; } 2>/dev/null; then
  ATTEMPT=0
  while [ "$ATTEMPT" -lt 3 ]; do
    ATTEMPT=$((ATTEMPT + 1))
    echo
    echo "Paste your key: the workshop key from the card, or your own OpenRouter key (sk-or-...)"
    echo "or NVIDIA key (nvapi-...). It will not show on screen. Then press Enter."
    echo "No key yet? Just press Enter: the Codespace is ready and the check waits for the key."
    printf "> "
    ENTRY=""
    READING=1
    IFS= read -rs ENTRY </dev/tty || true
    READING=0
    echo
    if entry_is_command "$ENTRY"; then
      echo "Setup is already running. Paste only the key, or press Enter."
      ATTEMPT=$((ATTEMPT - 1))
      continue
    fi
    KEY="${ENTRY//[[:space:]]/}"
    ENTRY=""
    [ -n "$KEY" ] || break
    echo "Received ${#KEY} characters."
    if ! key_looks_right; then
      echo "That does not look like a key: it should be at least eight characters with no spaces."
      KEY=""; continue
    fi
    endpoint_for_key || { KEY=""; continue; }
    dots_start "Checking the key against the endpoint"
    check_key
    case "$HTTP" in
      200) dots_stop ok; break ;;
      401|403) dots_stop fail; echo "That key was not accepted (HTTP $HTTP). Copy the whole key and try again."; KEY="" ;;
      400|404) not_found ;;
      000) die "Could not reach $BASE (network)." "Check your connection, then run bash setup.sh again." ;;
      *) die "Unexpected reply from the endpoint (HTTP $HTTP)." "Wait a minute, then run bash setup.sh again." ;;
    esac
  done
fi

# ------------------------------------------------------------- 5. write and report
# With an accepted key and no model named, choose one from what the endpoint lists.
if [ -n "$KEY" ] && [ -z "$MODEL" ]; then MODEL="$(pick_model)"; fi
if [ -z "$KEY" ] && [ "$BASE_SOURCE" = "key" ]; then BASE="$OSU_BASE_URL"; MODEL=""; fi
write_env "$BASE" "$KEY" "$MODEL" || die "Could not write $ENV_FILE." "Check that this folder is writable, then run bash setup.sh again."
READY_DONE=1
: >"$MARKER"
hr
if [ -n "$KEY" ]; then
  echo " READY. Endpoint: $BASE"
  [ -n "$MODEL" ] && echo " Model: $MODEL"
  echo " The key is saved in .env (never committed)."
  echo
  echo " Next:   python 00_setup/check.py"
else
  echo " Codespace ready; endpoint check pending."
  echo " When you have the workshop key, type:   bash setup.sh"
fi
hr
exit 0
