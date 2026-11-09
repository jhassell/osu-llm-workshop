Read 02_data/datasets/oklahoma-wheat/DICTIONARY.md, then investigate 02_data/datasets/oklahoma-wheat/ok_county_winter_wheat_2000-2025.csv before analyzing it.

One row is one statistic for one county in one harvest year, so the data must be reshaped to one county-year per row first.

Find every problem you can: in its structure, its units, its values, and whether the published series behaved as described. For each problem, show the code you ran and what it printed, the rows affected, and your decision (fix, flag, or leave alone) with a reason. Write results/findings.md. Do not change the raw file and do not drop rows silently.

Then, treating the data as you decided, make the three plots that best show winter wheat yield (bushels per harvested acre) against harvest year, 2000 to 2025: has yield gone up?. Something other than that comparison could explain a difference: which counties are published. NASS published many more counties a year before 2008 than after, pooling the rest, so an average over published counties can move because the set of counties changed. Show whether it does. Save the plots in results/figures/ and write results/report.md. Every number must come from the script's printed output.
