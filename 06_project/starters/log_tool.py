"""A parser for a fixed-width instrument log. A tested starting point.

    python 06_project/starters/log_tool.py
"""
from pathlib import Path

LOG = Path(__file__).resolve().parent / "sample.log"       # or a file in mine/


def log_summary(channel: str) -> str:
    """Summarize the potentiostat log for one channel (CH1, CH2) or 'all'. Returns,
    per channel, the number of readings, the potential range in volts, the
    maximum current in microamps, and any rows flagged other than ok."""
    want = channel.strip().upper()
    per = {}
    for line in LOG.read_text().splitlines():
        parts = line.split()
        if not parts or parts[0].startswith("#") or len(parts) < 5:
            continue
        t, ch, v, i, flag = parts[:5]
        if want not in ("ALL", "", "*") and ch != want:
            continue
        d = per.setdefault(ch, {"n": 0, "v": [], "i": [], "flags": []})
        d["n"] += 1
        d["v"].append(float(v))
        d["i"].append(float(i))
        if flag != "ok":
            d["flags"].append(f"{t} {flag}")
    if not per:
        return f"no channel named {channel!r}"
    return "\n".join(
        f"{ch}: {d['n']} readings; potential {min(d['v']):+.3f} to {max(d['v']):+.3f} V; "
        f"max current {max(d['i']):.2f} uA; flagged: {', '.join(d['flags']) or 'none'}"
        for ch, d in sorted(per.items()))


if __name__ == "__main__":
    print(log_summary("all"))
    print()
    print(log_summary("CH2"))
    print()
    print(log_summary("CH9"))
