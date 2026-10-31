#!/usr/bin/env bash
# The room switch. Rewrites .env to point every lab at a different endpoint.
#
#   bash 00_setup/switch_backend.sh https://integrate.api.nvidia.com/v1 <model name>
#
# The model name is needed on an endpoint that serves many models; a NIM that
# serves one needs only the URL.
#
# Then paste the key for that endpoint when asked. It runs setup.sh again, so
# OpenClaw is reconnected too when you answer the what-next question (Enter or
# 2). The labs read LLM_BASE_URL and LLM_API_KEY from .env and nothing else.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
URL="${1:-}"; MODEL="${2:-}"
[ -n "$URL" ] || { echo "usage: bash 00_setup/switch_backend.sh https://host/v1 [model]"; exit 2; }
if [ -n "$MODEL" ]; then exec bash "$ROOT/setup.sh" --reset-key --base-url "$URL" --model "$MODEL"; fi
exec bash "$ROOT/setup.sh" --reset-key --base-url "$URL"
