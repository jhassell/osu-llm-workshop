"""Stop 4: put the model's numbers next to the picture they came from.

    python 04_see/compare.py <image> <extracted.csv> [<truth.csv>]

Always writes results/seen/<image-stem>-compare.png: the original image beside
a fresh plot of the extracted CSV. If there is a truth CSV (given, or a CSV
with the same name next to the image, as every shipped chart has), it also
draws truth and extracted on the same axes, and prints and saves an error
table, results/seen/<image-stem>-errors.csv, one row per column:

    matched     truth points the model gave a value for, out of all of them
    mean_err    mean absolute error, in the data's units
    max_err     the largest absolute error, in the data's units
    pct_range   mean_err as a percent of the axis range (the span of the true
                values on that axis; for bar charts, zero to the tallest bar)
    median_rel  the median error as a percent of the true value; the number to
                read for a logarithmic axis, where the range is dominated by
                the largest values

The first column of each CSV is the x axis. Other columns are matched by name
(ignoring units and capitals), or by position when the names differ.
"""
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                     # no screen needed in a Codespace
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SEEN = ROOT / "results" / "seen"


# ---------- reading the columns ----------

def unit_of(column):
    """The units in parentheses at the end of a column name, or ''."""
    found = re.search(r"\(([^()]*)\)\s*$", str(column))
    return found.group(1).strip() if found else ""


def key_of(column):
    """A column name reduced for matching: no units, no capitals, letters and digits only."""
    return re.sub(r"[^a-z0-9]", "", re.sub(r"\([^()]*\)", "", str(column).lower()))


def is_error(column):
    """True for an error-bar column, such as 'control err (mg/L)'."""
    return bool(re.search(r"\b(err|error|sd|se|sem|std|uncertainty)\b", str(column).lower()))


def numeric_x(df):
    """True when the first column holds numbers (a line or scatter), False for categories (bars)."""
    return pd.api.types.is_numeric_dtype(df.iloc[:, 0])


def series_and_errors(df):
    """Pairs of (series column, its error column or None), in table order. An
    error column belongs to the series just before it."""
    pairs = []
    for col in df.columns[1:]:
        if is_error(col) and pairs and pairs[-1][1] is None:
            pairs[-1] = (pairs[-1][0], col)
        elif not is_error(col):
            pairs.append((col, None))
    return pairs


def pair_columns(truth, seen):
    """Which extracted column goes with each truth column. By name when every
    truth column finds one; otherwise by position. A truth column with no
    partner is paired with None, so a series the model missed still shows up
    in the error table, as 0 points read. Returns (pairs, how)."""
    t_cols, s_cols = list(truth.columns[1:]), list(seen.columns[1:])
    by_name = {}
    for t in t_cols:
        same = [s for s in s_cols if key_of(s) == key_of(t)]
        near = [s for s in s_cols if is_error(s) == is_error(t)
                and (key_of(t) in key_of(s) or key_of(s) in key_of(t)) and key_of(s)]
        # Among near names, the closest in length wins ("male" prefers "male mass" to "female mass").
        near.sort(key=lambda s: abs(len(key_of(s)) - len(key_of(t))))
        found = (same or near or [None])[0]
        if found is not None and found not in by_name.values():
            by_name[t] = found
    if len(by_name) == len(t_cols):
        return list(by_name.items()), "by name"
    pairs = [(t, s_cols[i] if i < len(s_cols) else None) for i, t in enumerate(t_cols)]
    return pairs, "by position"


# ---------- drawing ----------

def plot_table(ax, df, style, label_prefix=""):
    """Draw a table on ax: lines and markers for numeric x, grouped bars or
    points for categories. Series with different units than the first go on
    a second y axis, as a dual-axis figure would. Returns the axes used."""
    pairs = series_and_errors(df)
    units = [unit_of(s) for s, _ in pairs]
    first_unit = units[0] if units else ""
    other = ax.twinx() if any(u != first_unit for u in units) else None
    x = df.iloc[:, 0]
    if not numeric_x(df):
        x = np.arange(len(df))
        ax.set_xticks(x, df.iloc[:, 0].astype(str))
    width = 0.8 / max(1, len(pairs))
    for i, (col, err) in enumerate(pairs):
        target = other if (other is not None and unit_of(col) != first_unit) else ax
        y = pd.to_numeric(df[col], errors="coerce")
        yerr = pd.to_numeric(df[err], errors="coerce") if err else None
        label = label_prefix + re.sub(r"\s*\([^()]*\)\s*$", "", str(col))
        color = f"C{i}"
        if style == "bars" and not numeric_x(df):
            target.bar(x + (i - (len(pairs) - 1) / 2) * width, y, width, yerr=yerr, capsize=3,
                       color=color, alpha=0.8, label=label)
        else:
            offset = 0 if numeric_x(df) else (i - (len(pairs) - 1) / 2) * width
            marker = {"truth": "o", "seen": "x", "plain": "o"}[style if style != "bars" else "plain"]
            line = "-" if style == "plain" and numeric_x(df) else "none"
            target.errorbar(x + offset, y, yerr=yerr, fmt=marker, linestyle=line, ms=5, capsize=2,
                            color=color, alpha=0.55 if style == "truth" else 1,
                            mfc="none" if style == "truth" else color, label=label)
    for target, on_left in ((ax, True), (other, False)):
        if target is None:
            continue
        cols = [c for c, _ in pairs if (unit_of(c) == first_unit) == on_left]
        target.set_ylabel(", ".join(sorted({unit_of(c) for c in cols})))
        values = pd.concat([pd.to_numeric(df[c], errors="coerce") for c in cols]).dropna()
        if len(values) and (values > 0).all() and values.max() / values.min() > 1000:
            target.set_yscale("log")       # spans more than three decades: draw it as the chart did
    ax.set_xlabel(str(df.columns[0]))
    return ax, other


def draw(image_path, seen, truth, out_path):
    """The comparison figure: original | replot | (truth and extracted overlaid)."""
    panels = 3 if truth is not None else 2
    fig, axes = plt.subplots(1, panels, figsize=(5.2 * panels, 4.2))
    axes[0].imshow(plt.imread(str(image_path)))
    axes[0].set_title("Original image")
    axes[0].axis("off")
    style = "plain" if numeric_x(seen) else "bars"
    a, b = plot_table(axes[1], seen, style)
    axes[1].set_title("Replotted from the extracted CSV")
    _legend(a, b)
    if truth is not None:
        a, b = plot_table(axes[2], truth, "truth", "true: ")
        # Give the extracted columns the truth names, so each lands on its own axis.
        renamed = seen.rename(columns={s: t for t, s in pair_columns(truth, seen)[0] if s is not None})
        _overlay(axes[2], b, renamed, truth)
        axes[2].set_title("Truth (circles) and extracted (crosses)")
        _legend(a, b)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def _overlay(ax, twin, seen, truth):
    """Draw extracted values as crosses on the truth panel, on the matching axis."""
    first_unit = unit_of(series_and_errors(truth)[0][0])
    x_seen = seen.iloc[:, 0] if numeric_x(truth) else _category_positions(truth, seen)
    pairs = series_and_errors(truth)
    width = 0.8 / max(1, len(pairs))
    for i, (col, err) in enumerate(pairs):
        if col not in seen.columns:
            continue
        target = twin if (twin is not None and unit_of(col) != first_unit) else ax
        offset = 0 if numeric_x(truth) else (i - (len(pairs) - 1) / 2) * width
        yerr = pd.to_numeric(seen[err], errors="coerce") if err and err in seen.columns else None
        target.errorbar(np.asarray(x_seen, dtype=float) + offset, pd.to_numeric(seen[col], errors="coerce"),
                        yerr=yerr, fmt="x", ms=6, capsize=2, color=f"C{i}", label="seen: " + re.sub(r"\s*\([^()]*\)\s*$", "", str(col)))


def _category_positions(truth, seen):
    """Where each extracted category sits on the truth chart (by name, else by order)."""
    names = [key_of(c) for c in truth.iloc[:, 0].astype(str)]
    places = [names.index(key_of(c)) if key_of(c) in names else np.nan for c in seen.iloc[:, 0].astype(str)]
    return places if not all(np.isnan(places)) else list(range(len(seen)))


def _legend(ax, twin):
    """One legend for both y axes."""
    handles, labels = ax.get_legend_handles_labels()
    if twin is not None:
        h2, l2 = twin.get_legend_handles_labels()
        handles, labels = handles + h2, labels + l2
    if handles:
        ax.legend(handles, labels, fontsize=7, frameon=False)


# ---------- measuring ----------

def match_rows(truth, seen):
    """For each truth row, the index of the extracted row at the same x, or None.
    Numbers: the nearest extracted x within 45 percent of the smallest gap
    between true x values, so one reading cannot stand for two neighbours.
    Categories: the same name, ignoring capitals and spaces, else the same order."""
    if numeric_x(truth) and numeric_x(seen):
        tx = truth.iloc[:, 0].to_numpy(float)
        sx = seen.iloc[:, 0].to_numpy(float)
        gaps = np.diff(np.unique(tx))
        tolerance = 0.45 * gaps.min() if len(gaps) else np.inf
        matches = []
        for x in tx:
            nearest = int(np.nanargmin(np.abs(sx - x))) if len(sx) else None
            matches.append(nearest if nearest is not None and abs(sx[nearest] - x) <= tolerance else None)
        return matches
    t_names = [key_of(c) for c in truth.iloc[:, 0].astype(str)]
    s_names = [key_of(c) for c in seen.iloc[:, 0].astype(str)]
    if any(n in s_names for n in t_names):
        return [s_names.index(n) if n in s_names else None for n in t_names]
    return [i if i < len(seen) else None for i in range(len(truth))]


def axis_ranges(truth):
    """The span of the true values on each y axis (grouped by units). Error
    columns use the span of their series' axis. Bar charts start at zero."""
    spans = {}
    for unit in {unit_of(c) for c, _ in series_and_errors(truth)}:
        cols = [c for c, _ in series_and_errors(truth) if unit_of(c) == unit]
        values = truth[cols].apply(pd.to_numeric, errors="coerce").to_numpy(float).ravel()
        values = values[~np.isnan(values)]
        low = min(values.min(), 0) if not numeric_x(truth) else values.min()
        spans[unit] = (values.max() - low) or abs(values.max()) or 1.0
    return spans


def error_table(truth, seen):
    """One row per truth column: how many points were read, and how far off."""
    pairs, how = pair_columns(truth, seen)
    rows_matched = match_rows(truth, seen)
    spans = axis_ranges(truth)
    rows = []
    for t_col, s_col in pairs:
        true = pd.to_numeric(truth[t_col], errors="coerce").to_numpy(float)
        got = (pd.to_numeric(seen[s_col], errors="coerce").to_numpy(float) if s_col is not None
               else np.full(len(seen), np.nan))        # a series the model left out
        read = np.array([got[i] if i is not None else np.nan for i in rows_matched])
        ok = ~np.isnan(true) & ~np.isnan(read)
        err = np.abs(read[ok] - true[ok])
        span = spans.get(unit_of(t_col), next(iter(spans.values())))
        rel = err / np.where(true[ok] != 0, np.abs(true[ok]), np.nan)
        rows.append({"column": t_col, "matched to": s_col,
                     "matched": f"{ok.sum()}/{(~np.isnan(true)).sum()}",
                     "mean_err": _round(err.mean()) if ok.any() else np.nan,
                     "max_err": _round(err.max()) if ok.any() else np.nan,
                     "pct_range": round(100 * err.mean() / span, 1) if ok.any() else np.nan,
                     "median_rel": round(100 * np.nanmedian(rel), 1) if ok.any() and not np.isnan(rel).all() else np.nan})
    return pd.DataFrame(rows), how


def _round(value):
    """Three significant figures, so 0.0123 and 2,345,000 both print sensibly."""
    return float(f"{value:.3g}")


def compare(image_path, seen_csv, truth_csv=None, quiet=False):
    """Write the comparison figure and, given truth, the error table. Returns
    the table (a DataFrame) or None when there is no truth to measure against."""
    image_path, seen_csv = Path(image_path), Path(seen_csv)
    stem = image_path.stem
    if truth_csv is None and image_path.with_suffix(".csv").exists():
        truth_csv = image_path.with_suffix(".csv")
        if not quiet:
            print(f"Truth found beside the image: {truth_csv}")
    seen = pd.read_csv(seen_csv)
    truth = pd.read_csv(truth_csv) if truth_csv else None
    SEEN.mkdir(parents=True, exist_ok=True)
    out = SEEN / f"{stem}-compare.png"
    table, how = (error_table(truth, seen) if truth is not None else (None, None))
    draw(image_path, seen, truth, out)
    if not quiet:
        print(f"Wrote {out.relative_to(ROOT)}")
    if table is None:
        if not quiet:
            print("No truth CSV, so no error table. Look at the two panels side by side.")
        return None
    table.to_csv(SEEN / f"{stem}-errors.csv", index=False)
    if not quiet:
        if how == "by position":
            print("Column names differ, so columns were matched by position:")
            for t, s in pair_columns(truth, seen)[0]:
                print(f"   truth '{t}'  <->  extracted '{s}'" if s else f"   truth '{t}'  <->  nothing (the model left it out)")
        print(table.drop(columns="matched to").to_string(index=False))
        print(f"Saved {(SEEN / f'{stem}-errors.csv').relative_to(ROOT)}")
    return table


def main():
    args = sys.argv[1:]
    if len(args) < 2 or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    for path in args:
        if not Path(path).is_file():
            raise SystemExit(f"No such file: {path}")
    compare(args[0], args[1], args[2] if len(args) > 2 else None)


if __name__ == "__main__":
    main()
