# JAMIA working copy

Prepared against [JAMIA's instructions to authors](https://academic.oup.com/jamia/pages/General_Instructions), checked 17 October 2026. Article type: Research and Applications (4,000-word body, 250-word structured abstract, at most four tables and six figures).

## Sources and build

`main.tex` includes the abstract, background/objective, methods, results, discussion, conclusion, statements, references, and finally `figure-legends.tex`. Legends include the existing alt text and retain the figure labels used in the body. Figures are supplied separately; tables are located in the source after their first citing paragraph. `supplementary.tex` compiles independently and shares `references.bib`. Scientific content is retained from the supplied draft.

Run `..\build.ps1 -Version jamia` from this directory, or `.\build.ps1 -Version jamia` from the parent directory. The JAMIA build also requires Python and Pandoc for editable Word tables. Outputs are placed in `build/` and copied to `submission/`. A compiled PDF is permitted for a LaTeX manuscript; retain the source files for any source upload requested by ScholarOne.

## ScholarOne files

| File in `submission/` | Designation |
|---|---|
| `main.pdf` | Main Document |
| `figures/Figure1.png` | Figure 1: adherence trend |
| `figures/Figure2.png` | Figure 2: adherence and mortality |
| `figures/Figure3.png` | Figure 3: retained mortality features |
| `figures/Figure4.png` | Figure 4: recurring guideline components |
| `supplementary.pdf` | Supplementary File: appendices S1-S5, including Tables S1-S2 |
| No code ZIP uploaded | Complete archive retained locally in `supplementary-data/supplementary-code.zip`; offered on request in the cover letter |
| `Table1.docx` through `Table4.docx` | Editable Word table companions |

Use the distinct Main Document, Figure, and Supplementary designations when offered. The manuscript PDF has legends at the end and no embedded images, following the journal's standard instructions. If ScholarOne requests source files, supply this working copy's TeX/BibTeX and figure assets, not the medRxiv sources or historical notes.

## Items still requiring author input or review

- **Supplementary ZIP retained locally.** `supplementary-data/supplementary-code.zip` contains all 332 tracked files from both repositories plus README/manifest. The portal rejected full and split ZIP attempts, so no code ZIP is uploaded at this stage. The cover letter explains this and offers the complete archive on request. Redundant archive parts were removed. Regenerate using `python package_supplementary.py`; builds do not copy the archive into `submission/`.
- **Figures upscaled from existing PNGs:** `export_figures.py` creates 4x Lanczos-resampled submission copies at 600 DPI, preserving source files in `figures/`. Dimensions are 5552 x 1892, 5512 x 2124, 5440 x 1552, and 4396 x 1504 pixels. These are interpolated raster exports, not newly rendered plots. Python/Pillow is required; the JAMIA build regenerates them automatically.
- **Word counts verified using TeXcount:** body 3,907 + 47 heading words = **3,954**; abstract 249 + its heading = **250**. Title page updated to the conservative body total including headings. Git's Perl runs TeXcount directly; a standalone Perl installation is not required.
- **Tables:** four editable Word companions are generated from the LaTeX sources by `export_tables.py` (requires Pandoc and Python). Main-PDF tables each fit on one page. The PDF retains tables after their first citing paragraphs in source; LaTeX may float them. The portal/editorial office may still request a Word manuscript with the tables embedded at first citation.
- **References:** local `jamia.bst` now uses numbered citation order, surname/initials, first three authors plus et al., and journal year;volume:pages formatting. Journal abbreviations and two incomplete records were corrected. Web access dates were supplied by the corresponding author: June 2025 for the Atlas and two Israeli reports; September 2026 for the position paper and both repositories. Final bibliographic accuracy review remains an author task.
- Confirm author degrees/affiliations and corresponding-author details are current; these are populated, contrary to the old checklist.
- The finalized cover letter is available as `submission/cover-letter.docx` and `submission/cover-letter.txt`. It includes the verified medRxiv DOI, AI-use disclosure, and author-confirmed exclusive submission, approval by all authors, no other related publications/submissions, and no prior journal reviews. `cover-letter-draft.md` contains the same finalized text.
- All authors have approved the manuscript (confirmed by the corresponding author). Check funding, ethics details, CRediT roles, and any portal declarations against the manuscript. Supply related materials if requested and the #JAMIA promotional text in the portal.

The package is a working submission draft until the remaining figure, reference, portal-format and author checks are resolved. No journal submission has been made.
