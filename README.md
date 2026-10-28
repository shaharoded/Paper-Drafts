# Paper-Drafts

Working directory for paper drafts and manuscripts. LaTeX sources; compile
locally.

| Folder | What it is | Status |
|---|---|---|
| `Thesis/` | M.Sc. thesis — the full document that ties the rest of the work together. `main.pdf` is the built copy; `content/` holds the source chapters. | complete |
| `KineretClinicalStudy/JBI2027/` | Manuscript for the *Journal of Biomedical Informatics* — the clinical-study half of the thesis. | drafting |
| `KineretClinicalStudy/JAMIA2027/` | Adaptation of the JBI draft to *JAMIA*'s Research and Applications format (4 000-word limit, 4 tables, 4 figures). Same study, restructured. See its own README for the delta. | drafting |
| `INTERVenE/AAAI2027/` | AAAI 2027 submission bundle — INTERVenE-Enc paper. Includes the anonymous submission (`AnonymousSubmission/`) and the accompanying `code/` snapshot. | drafting |
| `KineretPrediction/AIIM2027/` | *Artificial Intelligence in Medicine* draft — Kineret transferability + adherence-signal study. Combines the AAAI methodology and the JBI adherence work into a seven-arm ladder on the Kineret cohort. | drafting |
| `LiarsDice/AAAI/`, `LiarsDice/NeurIPS/` | Adaptive strategy learning in Liar's Dice; independent AAAI and NeurIPS workshop projects. See `LiarsDice/README.md` for build instructions. | drafting |
| `StanceDetection/` | Earlier work — stance detection on the Gaza-war corpus (AAAI 2025 submission). PDF included. | archived |

LaTeX build artefacts (`.aux`, `.log`, `.bbl`, …) are gitignored; the built
PDFs that are worth carrying (`Thesis/main.pdf`, the AAAI compiled bundle,
`StanceDetection/*.pdf`) are kept.

## Building

Standard `pdflatex` + `bibtex` pipeline for each subfolder:

```bash
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Some subfolders have a `build.ps1` (Thesis) or their own README with
per-project build notes — check the folder before building.
