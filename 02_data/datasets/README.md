# Fallback datasets for Stop 2

Three real public datasets, for anyone who did not bring a CSV of their own. Each folder has the raw file as the source gives it (warts included), DICTIONARY.md (what each column means, its units, how missing values look), SOURCE.md (where it came from, the license, how to cite it), and FOUR-LINES.md (a worked example of the four lines you write before the first prompt).

- penguins: 344 adult penguins from three species near Palmer Station, Antarctica, 2007 to 2009. Bill, flipper and body measurements, sex, blood isotopes. CC0.
- stillwater-weather: daily high and low temperature, precipitation and wind at Stillwater Regional Airport, 2021 to 2025, from NOAA. Public domain.
- oklahoma-wheat: winter wheat yield, acres and production for every published Oklahoma county, 2000 to 2025, from USDA NASS. Public domain.

Each folder's reference/ holds a completed run to compare yours against once you have your own: analysis.py rebuilds the figures and report.md from the raw file, and extension.py runs the one rehearsed inferential model for that dataset and writes extension.md. Look after you have tried, not before. From the labs/ folder:

    python 02_data/datasets/penguins/reference/analysis.py
    python 02_data/datasets/penguins/reference/extension.py
