Read 02_data/datasets/stillwater-weather/DICTIONARY.md, then investigate 02_data/datasets/stillwater-weather/stillwater_daily_2021-2025.csv before analyzing it.

One row is one calendar day at Stillwater Regional Airport.

Find every problem you can: in its structure, its units, its values, and whether the station's records behaved as described. For each problem, show the code you ran and what it printed, the rows affected, and your decision (fix, flag, or leave alone) with a reason. Write results/findings.md. Do not change the raw file and do not drop rows silently.

Then, treating the data as you decided, make the three plots that best show the day's maximum temperature (TMAX, degrees F) on days with measurable rain (PRCP 0.01 inch or more) against the other days. Something other than that comparison could explain a difference: season. Rain is more frequent in some months than others, and the months differ in temperature, so a raw wet-against-dry comparison mixes rain with the calendar. Show whether it does. Save the plots in results/figures/ and write results/report.md. Every number must come from the script's printed output.
