# Anonymous AAAI submission

`main.pdf` is the combined 14-page anonymous submission, compiled from LaTeX: main body on pages 1-4, references on page 5, and Supplementary Material on pages 6-14. The appendix includes an additional selected-population pairwise matrix and role-conditioned table. Existing aggregate figures are retained, with their broader opponent pool explained. The supplementary header and reviewer note mark the boundary.

`code-anonymous.zip` remains the separate source-only code supplement. Results and trained weights are excluded from that archive.

Build: pdflatex main; bibtex main; pdflatex main; pdflatex main.

The active template is the unchanged aaai2027.sty and aaai2027.bst from INTERVenE/AAAI2027/AuthorKit27 in this repository (AAAI-27 author kit: https://aaai.org/authorkit27/). The preamble follows AnonymousSubmission2027.tex: fonts and bibliography style are supplied automatically. The older aaai27 files are unused.
