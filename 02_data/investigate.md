Read 02_data/datasets/hvac-ahu/DICTIONARY.md, then investigate 02_data/datasets/hvac-ahu/ahu_trend_2017-09-25_to_2017-10-08.csv before analyzing it.

One row is one 5-minute reading from one air handling unit.

Find every problem you can: in its structure, its units, its values, and whether the equipment or process behaved as described. For each problem, show the code you ran and what it printed, the rows affected, and your decision (fix, flag, or leave alone) with a reason. Write results/findings.md. Do not change the raw file and do not drop rows silently.

Then, treating the data as you decided, make the three plots that best show supply air temperature against its setpoint (SA_TEMP minus SA_TEMPSPT, in degrees F, while the supply fan runs), day by day across the two weeks. Something other than that comparison could explain a difference: outdoor air temperature. On mild days the economizer cools with outdoor air and mechanical cooling is locked out, so a day can look odd only because of the weather; compare days with similar outdoor temperatures before blaming the equipment. Show whether it does. Save the plots in results/figures/ and write results/report.md. Every number must come from the script's printed output.
