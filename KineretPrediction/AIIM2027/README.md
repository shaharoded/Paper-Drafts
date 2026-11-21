# AIIM working manuscript

Current manuscript and supplementary material for the Kineret inpatient prediction study.

## Files

- `main.pdf` and `supplementary.pdf` are the current compiled drafts.
- `main.tex` and the chapter files contain manuscript text.
- `tables/` and the `updated_*` figures are used by the drafts.
- `prepare_results.py` regenerates tables and figures from the aggregate results export. It does not train models.
- `build.ps1` builds both PDFs from the LaTeX sources.

The paper reports the comparison of INTERVenE clinical interval representations with statistical intervals and raw-observation baselines on the Kineret cohort. The clinical knowledge base was designed for inpatient diabetes care. The QA inputs represent both the mean score and the occurrence of each named pattern in the observation window.

