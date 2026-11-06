"""Stop 6 recipe 2: your Stop 2 analysis becomes one web page for your dataset.

    python 06_build/page/make_page.py                     from results/report.md and results/figures/
    python 06_build/page/make_page.py --title "Stillwater daily weather, 2021 to 2025"

Writes results/page/index.html: one file, figures inside it, nothing loaded from
anywhere else, so it opens on any computer and can be emailed or put on a lab
website. It stays private in results/.

To put it on your public site, only when the data may be public (the shipped
datasets may; your own data may not be):
    mkdir -p site/data && cp results/page/index.html site/data/index.html
site/ is public at once and published to GitHub Pages about a minute later.

Before it writes anything it checks that every figure the report names exists
and that the report has no number in it that analysis.py did not print, if
results/analysis-output.txt exists (make it with:
    python results/analysis.py > results/analysis-output.txt).
"""
import base64
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
RES = ROOT / "results"


def markdown_to_html(md):
    """Enough Markdown for a report: headings, paragraphs, bullet lists, bold, code, tables."""
    out, in_list, table = [], False, []

    def inline(t):
        t = html.escape(t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
        return re.sub(r"`(.+?)`", r"<code>\1</code>", t)

    def flush_table():
        if table:
            rows = [r for r in table if not re.match(r"^\|?\s*:?-{3,}", r)]
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            head = "".join(f"<th>{inline(c)}</th>" for c in cells[0])
            body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in cells[1:])
            out.append(f"<table><tr>{head}</tr>{body}</table>")
            table.clear()

    for line in md.splitlines():
        if line.strip().startswith("|"):
            table.append(line); continue
        flush_table()
        if re.match(r"^\s*[-*] ", line):
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(line.strip()[2:])}</li>"); continue
        if in_list:
            out.append("</ul>"); in_list = False
        m = re.match(r"^(#{1,4}) (.*)", line)
        if m:
            n = len(m.group(1)); out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
        elif re.match(r"^!\[.*\]\(.*\)", line.strip()):
            continue                     # figures are placed below, from the folder
        elif line.strip():
            out.append(f"<p>{inline(line)}</p>")
    flush_table()
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def numbers_not_printed(report, output):
    """Numbers in the report (three or more digits) that no number in the script's
    output rounds to. 0.179 in the report matches 0.1794 printed by the script;
    a number typed in by hand matches nothing."""
    pat = r"(?<![\w.])\d[\d,]*\.?\d*(?![\w])"
    printed = [float(x.replace(",", "")) for x in re.findall(pat, output) if x.rstrip(".,")]
    missing = []
    for raw in sorted({n.rstrip(".,") for n in re.findall(pat, report)}):
        digits = raw.replace(",", "").replace(".", "")
        if len(digits) < 3:
            continue
        value = float(raw.replace(",", ""))
        places = len(raw.split(".")[1]) if "." in raw else 0
        # within 0.6 of a unit in the last digit: allows a printed value rounded once more
        if not any(abs(x - value) <= 0.6 * 10 ** -places for x in printed):
            missing.append(raw)
    return missing


def main():
    title = sys.argv[sys.argv.index("--title") + 1] if "--title" in sys.argv else "Dataset"
    report_path = RES / "report.md"
    figdir = RES / "figures"
    if not report_path.exists():
        raise SystemExit("No results/report.md: run Stop 2 first, or make one.")
    report = report_path.read_text()
    figures = sorted(p for p in figdir.glob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".svg")) if figdir.exists() else []
    named = set(re.findall(r"figures/([\w.\-]+\.(?:png|jpe?g|svg))", report))
    missing = sorted(n for n in named if not (figdir / n).exists())
    problems = [f"the report names figures/{n}, which does not exist" for n in missing]
    out_file = RES / "analysis-output.txt"
    if out_file.exists():
        stray = numbers_not_printed(report, out_file.read_text())
        problems += [f"{n} is in the report but not in analysis.py's output" for n in stray[:10]]
    else:
        print("Note: no results/analysis-output.txt, so the numbers were not checked against the script.")
    if problems:
        print("NOT WRITTEN. Fix these first (or ask the agent to):")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    imgs = []
    for p in figures:
        kind = "svg+xml" if p.suffix.lower() == ".svg" else ("jpeg" if p.suffix.lower() in (".jpg", ".jpeg") else "png")
        data = base64.b64encode(p.read_bytes()).decode()
        imgs.append(f'<figure><img alt="{html.escape(p.stem)}" src="data:image/{kind};base64,{data}"><figcaption>{html.escape(p.stem)}</figcaption></figure>')
    page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;max-width:52em;margin:2em auto;padding:0 1em;color:#222}}
img{{max-width:100%}}figure{{margin:1.5em 0}}figcaption{{color:#555;font-size:.9em}}table{{border-collapse:collapse}}td,th{{border:1px solid #ccc;padding:4px 8px}}
code{{background:#f3f3f3;padding:0 3px}}footer{{margin-top:3em;color:#666;font-size:.85em}}</style>
<h1>{html.escape(title)}</h1>
{markdown_to_html(report)}
{''.join(imgs)}
<footer>Every figure and number on this page is rebuilt from the raw data by analysis.py.</footer></html>"""
    (RES / "page").mkdir(parents=True, exist_ok=True)
    (RES / "page" / "index.html").write_text(page)
    print(f"Wrote results/page/index.html ({len(figures)} figures, {len(page) // 1024} KB). It is private until you copy it into site/.")


if __name__ == "__main__":
    main()
