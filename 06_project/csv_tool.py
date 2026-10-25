"""Module 6, the default path: a summarizer over a small CSV. Two marked edits.

    python 06_project/csv_tool.py        tests the tool on its own, no model involved

The sample file is an instrument log: one row per reading, with a condition
column and a value column. Change the two marked lines so the tool reports on
your columns and answers your question, run this file to test it, then add it
to the agent in starter.py with one line.
"""
import csv
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---- EDIT 1: the file and the two columns the tool reports on. ------------
CSV_FILE = HERE / "sample_log.csv"     # or a file you dropped into mine/
GROUP_COLUMN = "condition"             # the column whose values define the groups
VALUE_COLUMN = "reading"               # the numeric column to summarize
# ---- EDIT 2: the question this tool is good at, for the model to read. ----
QUESTION_IT_ANSWERS = "the mean, spread and count of instrument readings for each experimental condition"
# ---------------------------------------------------------------------------


def summarize_csv(group: str) -> str:
    # The docstring is what the model reads. It is built from EDIT 2 just below.
    want = group.strip().lower()
    rows = list(csv.DictReader(open(CSV_FILE, newline="")))
    if not rows:
        return f"error: {CSV_FILE.name} is empty"
    for col in (GROUP_COLUMN, VALUE_COLUMN):
        if col not in rows[0]:
            return f"error: no column named {col!r}; the columns are {', '.join(rows[0])}"
    groups = {}
    for row in rows:
        try:
            groups.setdefault(row[GROUP_COLUMN].strip(), []).append(float(row[VALUE_COLUMN]))
        except ValueError:
            continue                        # a blank or non-numeric reading is skipped
    chosen = {g: v for g, v in groups.items() if want in ("all", "", "*") or g.lower() == want}
    if not chosen:
        return f"no group named {group!r}; the groups are {', '.join(sorted(groups))}"
    lines = []
    for g, vals in sorted(chosen.items()):
        sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
        lines.append(f"{g}: n={len(vals)}, mean={statistics.mean(vals):.3g}, sd={sd:.2g}, "
                     f"min={min(vals):.3g}, max={max(vals):.3g}")
    return "\n".join(lines)


summarize_csv.__doc__ = (
    f"Use this for any question about the instrument log ({CSV_FILE.name}), which is not in the "
    f"records table. It reports {QUESTION_IT_ANSWERS}. Give one group name, or 'all' for every group. "
    "Returns one line per group with the count, mean, standard deviation, minimum and maximum, "
    "so the answer rests on actual numbers rather than on a guess."
)


if __name__ == "__main__":
    print("all groups:")
    print(summarize_csv("all"))
    print("\none group:")
    first = next(csv.DictReader(open(CSV_FILE, newline="")))[GROUP_COLUMN]
    print(summarize_csv(first))
    print("\na bad input:")
    print(summarize_csv("no such group"))
