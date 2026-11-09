Turn everything into results/analysis.py, one script that rebuilds the whole analysis from the raw file:

- It reads the raw CSV, applies each fix in results/findings.md, and prints what each fix changed (rows before and after, values converted).
- It makes every figure in results/figures/.
- It writes results/report.md itself, every number in it filled in from a value the script computed, never typed in. Delete the report you wrote by hand and let the script make it.
- It prints every number the report contains, so a reader can trace each one to a line of output.
- It never prints that anything matches unless the script actually compared the two values.

Run it. Then run it a second time and confirm the output is identical and results/report.md was rewritten from scratch.
