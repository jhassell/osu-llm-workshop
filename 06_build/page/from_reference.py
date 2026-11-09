"""Stop 6, page recipe: an analysis for anyone with no Stop 2 analysis of their own.

bash catchup.sh s6 copies this file to results/analysis.py when results/ has no
Stop 2 report. Then the page recipe runs exactly as for everyone else:

    python results/analysis.py > results/analysis-output.txt
    python 06_build/page/make_page.py --title "Palmer penguins"

It reruns one shipped dataset's finished analysis (02_data/datasets/<DATASET>/
reference/analysis.py), prints what that analysis prints, and copies its
report.md and figures into results/. Change DATASET to stillwater-weather or
oklahoma-wheat for another one.
"""
import shutil
import subprocess
import sys
from pathlib import Path

DATASET = "penguins"


def labs_root():
    """The labs/ folder, wherever this file is run from (results/ or 06_build/page/)."""
    for folder in Path(__file__).resolve().parents:
        if (folder / "02_data" / "datasets").is_dir():
            return folder
    raise SystemExit("Could not find 02_data/datasets/ above this file.")


def main():
    root = labs_root()
    ref = root / "02_data" / "datasets" / DATASET / "reference"
    run = subprocess.run([sys.executable, str(ref / "analysis.py")], capture_output=True, text=True, cwd=root)
    sys.stdout.write(run.stdout)
    if run.returncode != 0:
        sys.stderr.write(run.stderr)
        raise SystemExit(f"{ref / 'analysis.py'} failed (exit {run.returncode}); nothing was copied.")
    results = root / "results"
    figures = results / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ref / "report.md", results / "report.md")
    for fig in (ref / "figures").iterdir():
        if fig.is_file():
            shutil.copy2(fig, figures / fig.name)
    print(f"(from_reference: copied {DATASET}'s report and figures into results/)", file=sys.stderr)


if __name__ == "__main__":
    main()
