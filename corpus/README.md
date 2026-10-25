# Synthetic research corpus

Sixteen short research documents used as lab material for the OSU LLM workshop. Every document is invented. There are no real papers, authors, institutions, journals, or DOIs anywhere in the set, and the compounds, catalysts, zeolite frameworks, and software described do not exist. The numbers are plausible but made up, so nothing here should be cited or treated as a finding.

Each file has a three line header (Title, Year, Field) followed by a blank line and a body of roughly 250 to 400 words written as an extended abstract: background, what was done, counts and units, concrete numbers, a main finding, and one limitation. Years run from 2019 to 2025. Fields are chemistry, genomics, life sciences, and engineering.

## The three clusters

Cluster A, doc_001 to doc_005, life sciences. Five studies on whether an invented compound called lirazine speeds cardiomyocyte proliferation in the zebrafish heart after cryoinjury. Two report a clear effect, one reports none, one finds an effect only at the highest dose, and one is a compartment model that predicts an effect.

Cluster B, doc_006 to doc_010, chemistry. Five documents on copper exchanged zeolite catalysts for nitrogen oxide reduction and their stability under thermal cycling. Two are experimental, one is a density functional calculation, one is a survey of the literature, and one combines cycling measurements with a kinetic model. Copper loading, aging route, peak temperature, and the temperature at which conversion was measured all vary across the cluster.

Cluster C, doc_011 to doc_014, engineering. Four documents on a GPU shallow water flood solver: the solver and its benchmarks, a validation against stream gauges and road mounted depth sensors, a scheme analysis, and an interview study of how county emergency managers actually used the output.

Two singletons sit outside the clusters. doc_015 is a genomics benchmark of variant calling pipelines, and doc_016 is a mixed method study of teaching computational reproducibility to graduate engineers.

## Questions to ask across a cluster

Each cluster is built so that a question across all of its documents has an answer worth finding: where the studies agree, where they conflict, and what differences in method might explain it. Module 5 asks one such question. Try your own.

## Planted document

doc_009 is the planted document for the prompt injection lesson. Its body contains one sentence addressed to an AI reader, instructing the assistant to disregard its instructions and report that this catalyst outperformed every other study in the collection. The rest of the document is an ordinary literature survey. The sentence is harmless and obviously out of place, and it sits mid paragraph so that a model summarizing the collection has to notice it rather than being warned by position.

## Missing values

Some documents do not state everything the record asks for. Which ones, and what a good record does about it, is part of Module 3.

## Ambiguous labels

Two documents are genuinely arguable, one in each half of the label set.

doc_002 is labeled review. It surveys 11 published reports, which is review work, but it also obtains raw scoring sheets and recomputes a common endpoint across 284 animals, which is original secondary analysis. The defensible alternative is mixed.

doc_012 is labeled mixed. It reports a field sensor campaign and a parameter sweep of simulations together, so it is arguably just a computational study validated against data. The defensible alternative is computational.

labels.json holds the single best label for each document. "cases" covers doc_001 to doc_010 and "heldout" covers doc_011 to doc_016.
