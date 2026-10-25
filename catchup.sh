#!/usr/bin/env bash
# Behind? Restore one module's lab files and the saved table, then start there.
#
#   bash catchup.sh m4      restores 04_tool/ and the saved records table
#   bash catchup.sh m6      restores 06_project/ and the saved records table
#
# It never touches .env, mine/, your edits to records.py, or any other module.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
case "${1:-}" in
  m1) DIR=01_tour ;; m2) DIR=02_prompts ;; m3) DIR=03_table ;;
  m4) DIR=04_tool ;; m5) DIR=05_agent ;;  m6) DIR=06_project ;;
  *) echo "usage: bash catchup.sh m1|m2|m3|m4|m5|m6"; exit 2 ;;
esac
cd "$ROOT"
git checkout -- "$DIR" llm.py agent.py docs.py 2>/dev/null || git checkout HEAD -- "$DIR" llm.py agent.py docs.py
if [ ! -s 03_table/records.jsonl ]; then
  cp corpus/records.jsonl 03_table/records.jsonl
  echo "Saved table copied to 03_table/records.jsonl."
fi
echo "$DIR restored from the repository. Your .env, mine/ and records.py are untouched."
echo "Next: open $DIR/README.md and run its one command."
