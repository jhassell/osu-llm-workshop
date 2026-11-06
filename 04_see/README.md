# Stop 4: A chart back into data

A model that can see reads a chart from a paper and gives you back the numbers behind it, as a table. Then you check the table: a replot beside the original, and, for the shipped charts, an error measured against the data the chart was drawn from. You will find where it is good enough to use, and one place where a complete, confident table is wrong.

About 25 minutes, from 1:00. Folder: `04_see/`. You type in a terminal.

## You will be able to

- Get the plotted data out of a chart image as a CSV, with units.
- Measure how far the extracted numbers are from the truth, in the data's own units.
- Say which kinds of chart the model reads well, and which it does not.

## The idea

The model for this stop is NVIDIA Nemotron 3.5 Super VL, which reads images as well as text. It is a different model from the rest of the day's, reached the same way, through OpenRouter. It thinks before it answers, sometimes for several thousand tokens, so a call takes ten to forty seconds and prints what it cost (a fraction of a cent).

Reading numbers off a chart is something researchers do by hand, with a ruler or a digitizing tool, when a paper gives a figure but not its data. The model does it in one request. The question is how well, and the answer is not one number: it depends on the chart. So every shipped chart in `04_see/charts/` comes with the CSV it was drawn from. `compare.py` puts the model's table beside the truth and reports the error per series: how many points it read, the mean and largest error in the data's units, that error as a percent of the axis range, and, for a logarithmic axis, the error as a percent of each true value.

On a chart from a paper you are reading there is no truth file. Then the replot beside the original is the check: if the two do not look alike, the table is wrong.

A chart is a measurement you can extract. A micrograph, a gel or a field photo is not: the model can describe it, but a number it gives you for a band intensity or a cell count is a guess. Use it for description only.

## Before you start

- This stop stays on OpenRouter: the vision model is not served on Cimarron. If you moved to Cimarron, move back first: `bash 00_setup/switch_backend.sh openrouter`.
- Your chart, if you brought one: a PNG or JPEG in `mine/` (a screenshot of a figure is fine). Otherwise, the six in `04_see/charts/`: `co2_line` (two series over time), `calibration_scatter` (points with error bars), `penguin_bars` (grouped bars with error bars), `growth_log` (a log axis), `bioreactor_dual` (two y axes), and `dense_overlap` (hundreds of overlapping points). `04_see/charts/SOURCES.md` says where each came from.

## Predict first

On your card: will the model read the bar chart or the dense scatter better? On the harder one, will it say it is unsure, or return a full table anyway?

## Do it

1. From memory, before anything new: rerun this morning's analysis without opening the Stop 2 README. Three minutes.

   ```
   python results/analysis.py
   ```

   Did it rebuild the same figures and numbers? If you cannot remember the command, that is the point of this step: write it on your card.

2. Look at `04_see/charts/penguin_bars.png` in the editor, then extract its data. The model takes ten to forty seconds:

   ```
   python 04_see/see.py 04_see/charts/penguin_bars.png --extract
   ```

   It saves `results/seen/penguin_bars.csv` and the model's whole reply beside it, and prints the table's shape, the time and the cost. For example:

   ```
   3 rows x 5 columns: Species, Female (g), Female err (g), Male (g), Male err (g)
   [nvidia/nemotron-3.5-super-vl via DeepInfra, 21.5 s, attempt 1, 669 tokens in, 6,778 out (mostly thinking), $0.0035]
   ```

3. Check it against the truth:

   ```
   python 04_see/compare.py 04_see/charts/penguin_bars.png results/seen/penguin_bars.csv
   ```

   It finds the truth file beside the chart, prints the error table, and writes `results/seen/penguin_bars-compare.png`: the original, the replot, and both on one set of axes. Is an error of one percent of the range good enough for what you would use these numbers for?

4. The hard one. Steps 2 and 3 again on `04_see/charts/dense_overlap.png`. Read the error table, then open the comparison image. Where does the model's curve follow the points, and where does it start drawing a line of its own? Did it say it was unsure?

Vision extraction is good enough for a first look at a published figure and for checking your reading of one. It is not good enough for quantitative work on a figure you cannot check, and never for a measurement from a micrograph, gel or photograph.

## Checkpoint

The comparison images for the two charts and their error tables, and one sentence: for which charts would you trust this, and for which not?

## Extensions

1. Your own chart, if you brought one: `python 04_see/see.py mine/<chart>.png --extract`, then `python 04_see/compare.py mine/<chart>.png results/seen/<chart>.csv`. With no truth file you get the replot beside the original. Does it look like the same chart?
2. A plain question: `python 04_see/see.py 04_see/charts/co2_line.png "What is on each axis, with units?"`
3. Run all six and make your own ranking: `python 04_see/smoke_test.py` (a few cents, a few minutes).
4. Feed the extracted CSV to your Stop 2 script, or ask the agent in `openclaw chat` to fit a line or a growth curve to it. How much does the extraction error change the fitted value?
5. A whiteboard photo or handwritten notes: `python 04_see/see.py mine/board.jpg "Transcribe this exactly; use LaTeX for the equations."` Check every symbol.
6. A figure of your own: `python 04_see/see.py mine/fig.png "Write alt text for this figure, then the one criticism a reviewer would make of it."`

## What you have now

`results/seen/`: the extracted CSVs, the model's raw replies, the comparisons and the error tables. The habit is the day's: a full table is a claim until the overlay says otherwise.

## If something goes wrong

- The vision model is slow or down. `04_see/saved/` holds every shipped chart's extraction, comparison image and error table from a run on November 6: open `penguin_bars-compare.png` and `dense_overlap-compare.png` and read their error tables, which is the checkpoint.

- "Stop 4 needs OpenRouter": you are on another endpoint. `bash 00_setup/switch_backend.sh openrouter`, then run the command again.
- It takes more than a minute, or says it ran past the deadline and is trying again. The model thinks at length, and the whole room is asking at once. Let the retry run.
- "The reply is not a table pandas can read". Open the `.reply.txt` file beside where the CSV would be: the model may have described the chart instead of tabulating it. Run `--extract` again, or add a note: `--extract "one row per x value"`.
- The comparison says it matched columns by position. The model named the series differently from the truth file; check that the order is right in the printed table.
- A series is missing (`0/12 matched`). The model left it out, often one named in a legend with a comma. Run `--extract` again.
