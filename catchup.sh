#!/usr/bin/env bash
# Behind? Restore one module's lab files and the saved table, then start there.
#
#   bash catchup.sh m4      restores 04_tool/ and the saved records table
#   bash catchup.sh m6      restores 06_project/, the earlier tool files it uses,
#                           and the saved records table
#
# Before anything is restored, the files about to be replaced are copied to
# mine/catchup-backup-<date-time>/, so nothing you wrote is lost. It never
# touches .env, mine/ (apart from adding that backup), or your edits to records.py.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# DIR is the module; NEEDS are the earlier module files it imports.
case "${1:-}" in
  m1) DIR=01_tour;    NEEDS="" ;;
  m2) DIR=02_prompts; NEEDS="" ;;
  m3) DIR=03_table;   NEEDS="" ;;
  m4) DIR=04_tool;    NEEDS="" ;;
  m5) DIR=05_agent;   NEEDS="04_tool/tools.py" ;;
  m6) DIR=06_project; NEEDS="04_tool/tools.py 05_agent/tools.py" ;;
  *) echo "usage: bash catchup.sh m1|m2|m3|m4|m5|m6"; exit 2 ;;
esac
cd "$ROOT"

mkdir -p mine
BACKUP="$(mktemp -d "mine/catchup-backup-$(date +%Y%m%d-%H%M%S)-XXXX")"   # unique, even twice in a second
for item in "$DIR" $NEEDS llm.py agent.py docs.py; do
  [ -e "$item" ] || continue
  mkdir -p "$BACKUP/$(dirname "$item")"
  cp -R "$item" "$BACKUP/$item"
done
echo "Your current files are copied to $BACKUP/ first."

# shellcheck disable=SC2086
git checkout -- "$DIR" $NEEDS llm.py agent.py docs.py 2>/dev/null \
  || git checkout HEAD -- "$DIR" $NEEDS llm.py agent.py docs.py

# The table the afternoon searches. A row is usable when it has a doc_id and
# recorded no error (the same rule the Module 4 search uses).
# With no usable row (missing, empty, or only errors), the saved table is copied
# in, and an unusable table is kept beside it under a new name.
if ! python3 - 03_table/records.jsonl <<'PYEOF' 2>/dev/null
import json, sys
for line in open(sys.argv[1]):
    try:
        row = json.loads(line)
    except ValueError:
        continue
    if isinstance(row, dict) and row.get("doc_id") and "error" not in row:
        sys.exit(0)
sys.exit(1)
PYEOF
then
  if [ -s 03_table/records.jsonl ]; then
    KEEP="03_table/records.unusable-$(date +%Y%m%d-%H%M%S)-$$.jsonl"
    mv 03_table/records.jsonl "$KEEP"
    echo "Your table had no usable rows; it is kept as $KEEP."
  fi
  cp corpus/records.jsonl 03_table/records.jsonl
  echo "Saved table copied to 03_table/records.jsonl."
fi
echo "$DIR restored from the repository. Your .env, mine/ and records.py are untouched."
echo "Next: open $DIR/README.md and run its one command."
