# Stop 4: A chart back into data

A model that can see reads a chart from a paper and gives you back the numbers behind it, as a table. Then you check the table: a replot beside the original, and, for the shipped charts, an error measured against the data the chart was drawn from. You will find where it is good enough to use, and one place where a complete, confident table is wrong.

About 25 minutes, from 1:00. Folder: `04_see/`. You type commands in a second terminal (click the **+** at the top right of the terminal panel; the chat can stay open in the first), and you look at every picture and table by clicking it in the Explorer, the file list on the left.

## You will be able to

- Get the plotted data out of a chart image as a CSV, with units.
- Measure how far the extracted numbers are from the truth, in the data's own units.
- Say which kinds of chart the model reads well, and which it does not.

## The idea

The model for this stop is NVIDIA Nemotron 3.5 Super VL, which reads images as well as text. It is a different model from the rest of the day's, reached the same way, through OpenRouter. It thinks before it answers, sometimes for several thousand tokens, so a call takes ten to forty seconds and prints what it cost (a fraction of a cent; when a provider reports no cost for an attempt, the line says so).

Reading numbers off a chart is something researchers do by hand, with a ruler or a digitizing tool, when a paper gives a figure but not its data. The model does it in one request. The question is how well, and the answer is not one number: it depends on the chart. So every shipped chart in `04_see/charts/` comes with the CSV it was drawn from. `compare.py` puts the model's table beside the truth and prints an error table:

- The first row is the x axis: how many true x values have an extracted point near them, how far the extracted x values are from the true ones, how many extracted points match no true point (`extra`), and how many repeat an x value already given (`duplicates`). A table can look complete and still hold points the chart does not have.
- Then one row per series and per error bar: how many points it read, the mean and largest error in the data's units, the mean error as a percent of the span of the true values on that axis (`pct_range`; for a bar chart, from zero to the tallest true bar), and, for a logarithmic axis, the error as a percent of each true value (`median_rel`). The span of the true values is usually smaller than the drawn axis, so this percent is the stricter of the two.

On a chart from a paper you are reading there is no truth file. Then the replot beside the original is the check. Before you judge it, make sure the two are drawn the same way: `compare.py` draws linear axes unless the values span more than three decades, and prints which scales it used. If the original has a logarithmic axis and the replot does not, or the other way round, run it again with `--yscale log` (or `--xscale log`, or `linear`). Two correct tables drawn on different scales do not look alike.

A chart is a measurement you can extract. A micrograph, a gel or a field photo is not: the model can describe it, but a number it gives you for a band intensity or a cell count is a guess. Use it for description only.

## Before you start

- This stop stays on OpenRouter: the vision model is not served on Cimarron. If you moved to Cimarron, move back first, in a terminal: `bash 00_setup/switch_backend.sh openrouter`.
- Your chart, if you brought one: a PNG or JPEG in `mine/` (a screenshot of a figure is fine). Otherwise, the six in `04_see/charts/`: `co2_line` (two series over time), `calibration_scatter` (points with error bars), `penguin_bars` (grouped bars with error bars), `growth_log` (a log axis), `bioreactor_dual` (two y axes), and `dense_overlap` (hundreds of overlapping points). `04_see/charts/SOURCES.md` says where each came from.

## Do it

1. From memory, before anything new: rerun this morning's analysis without opening the Stop 2 README. Three minutes. In the second terminal:

   ```
   python results/analysis.py
   ```

   Did it rebuild the same figures and numbers? If you cannot remember the command, that is the point of this step: write it on your card. No `results/analysis.py` (no script from Stop 2)? Rerun a finished one instead: `python 02_data/datasets/penguins/reference/analysis.py` (or the `stillwater-weather` or `oklahoma-wheat` one).

2. In the Explorer, open `04_see`, then `charts`, and click `penguin_bars.png`: it opens as a picture. Then extract its data, in the second terminal. The model takes ten to forty seconds:

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

   It finds the truth file beside the chart and prints the error table. Click `results/seen/penguin_bars-compare.png` in the Explorer: the original, the replot, and both on one set of axes. Is an error of one percent of the span good enough for what you would use these numbers for?

4. The hard one, the same two steps on the dense chart:

   ```
   python 04_see/see.py 04_see/charts/dense_overlap.png --extract
   python 04_see/compare.py 04_see/charts/dense_overlap.png results/seen/dense_overlap.csv
   ```

   Read the error table, its x-axis row first, then click `results/seen/dense_overlap-compare.png`. Where does the model's curve follow the points, and where does it start drawing a line of its own? The prompt asks for a table and nothing else, so the model has no room to say it is unsure: the error table and the overlay are the only way to see where it guessed.

Vision extraction is good enough for a first look at a published figure and for checking your reading of one. It is not good enough for quantitative work on a figure you cannot check, and never for a measurement from a micrograph, gel or photograph.

## Checkpoint

The comparison images for the two charts and their error tables, and one sentence: for which charts would you trust this, and for which not?

## Extensions

1. Your own chart, if you brought one, with its own name in both commands:

   ```
   python 04_see/see.py mine/<chart>.png --extract
   python 04_see/compare.py mine/<chart>.png results/seen/<chart>.csv
   ```

   With no truth file you get the replot beside the original; match the scales first (`--yscale log` if the original's y axis is logarithmic). Does it look like the same chart?
2. A plain question: `python 04_see/see.py 04_see/charts/co2_line.png "What is on each axis, with units?"`
3. Run all six and make your own ranking: `python 04_see/smoke_test.py` (a few cents, a few minutes).
4. Let the agent judge. Click `04_see/judge.md` to read it: a bounded goal for OpenClaw, to extract one shipped chart, read the error table, decide whether one retry is worth it, and write `results/verdict.md` saying for what uses the extraction is good enough, with the numbers that decide it. Then, in `openclaw chat` (the first terminal), type `Read 04_see/judge.md and do what it says.` This extension has not been rehearsed: read its verdict against the error table it printed, and note anything it claims that the table does not show.
5. Feed the extracted CSV to your Stop 2 script, or ask the agent in `openclaw chat` to fit a line or a growth curve to it. How much does the extraction error change the fitted value?
6. A whiteboard photo or handwritten notes: `python 04_see/see.py mine/board.jpg "Transcribe this exactly; use LaTeX for the equations."` Check every symbol.
7. A figure of your own: `python 04_see/see.py mine/fig.png "Write alt text for this figure, then the one criticism a reviewer would make of it."`

## What you have now

`results/seen/`: the extracted CSVs, the model's raw replies, the comparisons and the error tables. The habit is the day's: a full table is a claim until the overlay says otherwise.

## If something goes wrong

- The vision model is slow or down. `04_see/saved/` holds every shipped chart's extraction, comparison image and error table from a run on November 6. Click `04_see/saved/penguin_bars-compare.png` and `04_see/saved/dense_overlap-compare.png` in the Explorer, and read `penguin_bars-errors.csv` and `dense_overlap-errors.csv` beside them: that is the checkpoint.
- "Stop 4 needs OpenRouter": you are on another endpoint. `bash 00_setup/switch_backend.sh openrouter`, then run the command again.
- It takes more than a minute, or says it ran past the deadline and is trying again. The model thinks at length, and the whole room is asking at once. Let the retry run.
- "The reply is not a table pandas can read", or that a table row has the wrong number of cells. Nothing was saved, and any earlier CSV of that chart was removed so it cannot pass for this run's. Click the `.reply.txt` file in `results/seen/`: the model may have described the chart, or written a row with an extra comma. Run `--extract` again, or add a note: `--extract "one row per x value"`.
- The comparison says not every column matched by name. It prints how each truth column was paired; a column it could not pair safely shows as 0 points read. Check the pairing before you read the errors.
- A series is missing (`0/12 matched`). The model left it out, often one named in a legend with a comma. Run `--extract` again.
