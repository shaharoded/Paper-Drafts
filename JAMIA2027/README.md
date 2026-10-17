# Inpatient diabetes guideline manuscript

- `medrxiv/`: local preprint copy of the supplied sources, figures, PDFs, and build intermediates. Author contributions were corrected on 17 October 2026 at the corresponding author's request and `main.pdf` rebuilt. `original-sha256.json` records the originally supplied hashes, before this correction. The historical README, SUBMISSION.md, and tasks.tex are retained only in this snapshot to preserve provenance; their advice is outdated.
- `jamia/`: independent working copy for Journal of the American Medical Informatics Association, Research and Applications.
- `jamia/submission/`: generated manuscript and supplement PDFs, with standalone numbered figure files for ScholarOne. See `jamia/README.md` for outstanding items before upload.
- `build.ps1`: reproducible build entry point. Requires pdfLaTeX and BibTeX (MiKTeX or TeX Live); JAMIA also requires Python, Pillow and Pandoc for figure exports and Word table companions.

From this folder, run:

```powershell
.\build.ps1 -Version medrxiv
.\build.ps1 -Version jamia
```

Build intermediates and newly compiled PDFs go in each version's `build/` directory. The medRxiv build writes to `medrxiv/build/`; the local `medrxiv/main.pdf` was explicitly refreshed after the author-contribution correction. A successful JAMIA build copies both PDFs into `jamia/submission/` and regenerates figure and editable table files. The complete supplementary code ZIP is retained in `jamia/supplementary-data/` for editorial requests because the portal rejected ZIP uploads.

The snapshot preserves the files supplied locally; it has not been compared with the files served by medRxiv. No `main_3.pdf` was present; the preserved manuscript is named `main.pdf`.

To refresh the supplementary repository ZIP, run `python package_supplementary.py` before the JAMIA build. This reads the sibling `Mediator/` and `kineret-etl-repo/` repositories, retains their original concept-index format, and clears notebook outputs only in the archive copies.

Git tracks manuscript sources, original figure assets, the local preprint PDFs, build/export scripts, and submission notes. Generated build directories, upload copies, supplementary repository ZIPs, and superseded CSV exports stay local. Run `pandoc -f markdown -t docx jamia/cover-letter-draft.md -o jamia/submission/cover-letter.docx` to regenerate the finalized cover letter after building.
