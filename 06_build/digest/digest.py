"""Stop 6 recipe 3: what is new on your topic since you last looked.

    python 06_build/digest/digest.py                       the query saved below
    python 06_build/digest/digest.py "your query" --n 15   another query, more papers

Each run asks OpenAlex for the 25 papers that best match the query, keeps
those from this year and last, newest first, drops the ones an earlier run
has already shown you (the list of seen papers is results/digest-seen.json),
checks each DOI in Crossref, and writes results/digest-<date>.md: title,
authors, venue, the DOI's state, the retraction line, and a two-sentence
summary written by the model from the abstract. A paper with no abstract gets
no summary, never an invented one.

Change QUERY to your own and this is a program you run every Monday.
"""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "03_lit"))
import lit                                 # noqa: E402

QUERY = "cover crops soil organic carbon"   # yours here
N = 10                                     # how many recent papers to report at most
POOL = 25                                  # how many best matches to look through

RESULTS = ROOT / "results"
SEEN = RESULTS / "digest-seen.json"


def summary(record):
    """Two sentences from the abstract, or a plain note that there is none."""
    if not record.get("abstract"):
        return "No abstract in OpenAlex, so no summary. Read the paper."
    import llm                             # only needed when there is an abstract
    return llm.ask("In two sentences, say what this study did and what it found, using only the abstract. "
                   "Keep its numbers. Do not add anything the abstract does not say.\n\nAbstract:\n"
                   + record["abstract"][:6000])


def main():
    import argparse
    ap = argparse.ArgumentParser(description="What is new on your topic since the last run.")
    ap.add_argument("query", nargs="?", default=QUERY, help="what to search for, in quotes")
    ap.add_argument("--n", type=int, default=N, help="how many of the newest papers to look at")
    opts = ap.parse_args()
    query, n = opts.query, opts.n
    RESULTS.mkdir(exist_ok=True)
    seen = set(json.loads(SEEN.read_text())) if SEEN.exists() else set()

    # Newest-first search ranks any paper that mentions the words anywhere, so
    # take the best matches and keep the recent ones instead.
    found = lit.search(query, n=POOL, sort="relevance")
    print(found["note"])
    if found["error"] and not found["records"]:
        raise SystemExit("No digest this time: the search did not answer. Nothing was changed.")
    records = [r for r in found["records"] if "error" not in r]
    if not records:
        raise SystemExit(f'Nothing matches "{query}". Check the spelling, or use fewer words.')
    this_year = date.today().year
    records = sorted((r for r in records if (r.get("year") or 0) >= this_year - 1),
                     key=lambda r: r.get("year") or 0, reverse=True)[:n]
    if not records:
        raise SystemExit(f"None of the {POOL} best matches is from {this_year - 1} or later.")
    new = [r for r in records if (r.get("doi") or r.get("openalex_id")) not in seen]
    print(f"{len(records)} recent papers among the best matches for \"{query}\"; {len(new)} not shown before.")

    lines = [f"# Digest: {query}", "",
             f"Run {found['date_utc']} UTC. OpenAlex, the {POOL} best matches, {len(records)} from the last two years, "
             f"{len(new)} new since the last run. {found['note']}", ""]
    for r in new:
        authors = ", ".join(a["name"] for a in r["authors"][:3]) + (" et al." if len(r["authors"]) > 3 else "")
        if r.get("doi"):
            v = lit.verify(r["doi"], r["title"], r["authors"])
            state, retraction = v["state"], v["retraction"]["line"]
        else:
            state, retraction = "missing (no DOI)", "no DOI, so no retraction check"
        lines += [f"## {r['title']}", "",
                  f"{authors} ({r.get('year')}). {r.get('venue') or 'venue not stated'}. "
                  + (f"https://doi.org/{r['doi']}" if r.get("doi") else "no DOI"), "",
                  f"DOI check: {state}. Retraction: {retraction}.", "",
                  summary(r), ""]
        print(f"  {state:<12} {r['title'][:80]}")
        seen.add(r.get("doi") or r.get("openalex_id"))
    if not new:
        lines.append("Nothing new since the last run.")
    out = RESULTS / f"digest-{date.today().isoformat()}.md"
    out.write_text("\n".join(lines) + "\n")
    SEEN.write_text(json.dumps(sorted(s for s in seen if s), indent=1))
    print(f"\nWrote {out.relative_to(ROOT)}.")
    print("To run it every Monday at 7 on a machine that stays on (a Thursday task), add to crontab -e:")
    print(f"  0 7 * * 1  cd {ROOT} && python3 06_build/digest/digest.py >> results/digest.log 2>&1")


if __name__ == "__main__":
    main()
