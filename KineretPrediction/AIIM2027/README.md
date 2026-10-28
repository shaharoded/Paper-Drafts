# AIIM 2027 — Kineret Transferability Paper

Draft manuscript for *Artificial Intelligence in Medicine* (Elsevier).

**One-line:** the closing transferability study of INTERVenE-Enc on the
Kineret cohort, combining the methodology of the AAAI paper with the
adherence signal of the JBI/JAMIA paper into a seven-arm ladder.

## Story arc

- **AAAI companion** ([`AAAI2027/`](../../INTERVenE/AAAI2027/)) introduces INTERVenE-Enc
  and demonstrates it on MIMIC-IV. On that cohort, KBTA carries
  interpretability but not accuracy (σ-bin ablation within noise).
- **JBI companion** ([`JBI2027/`](../../KineretClinicalStudy/JBI2027/)) measures adherence to a
  national inpatient-hyperglycemia guideline across six Israeli hospitals
  and reports above-median-adherence outcome associations.
- **This paper** puts INTERVenE-Enc on the Kineret data and asks whether
  (i) the architecture transfers and (ii) the measured adherence signal
  helps prediction — under a seven-arm ladder that separates architecture,
  knowledge base, and QA effects on identical labels and patients.

## Files

| File | Contents |
|---|---|
| `main.tex` | Preamble, front matter, `\input` chain, end matter |
| `introduction.tex` | Introduction + contributions |
| `background.tex` | KBTA, deep learning for EHR, INTERVenE, adherence as a temporal problem |
| `methods.tex` | Cohort, targets, task, seven-arm ladder, containment guards, training, evaluation |
| `results.tex` | Target support, ladder, QA delta, per-outcome, onset & LoS |
| `discussion.tex` | Principal findings, ladder design, limitations |
| `conclusion.tex` | Wrap-up + reproducibility statement |
| `tasks.tex` | Draft-only open-items box (title-page red box) |
| `references.bib` | Bibliography (three companion-paper keys are placeholders) |
| `figures/` | The five paper figures (PDF), imported from `Kineret-Prediction/results/full_bench_results/figures/` |

## Build

`pdflatex main && bibtex main && pdflatex main && pdflatex main`
(untested — no TeX distribution on this machine; see task H).

## Draft status

Skeleton and prose complete; numbers all cross-checked against
`Kineret-Prediction/results/full_bench_results/benchmark_summary.csv`.
Open items — including several likely-reviewer-demanded experiments
(multi-seed variance, sensitivity to $K_{\mathrm{eval}}$, temporal
held-out, per-hospital leave-one-out, calibration reproduction, sparse-
transcoder attribution on the KB+QA arm) — are collected in `tasks.tex`.

Flip `\showtasksfalse` in `main.tex` for a clean submission PDF.
