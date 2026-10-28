# Adaptive Strategy Learning in Liar's Dice

Moved from `Adaptive-Strategy-Learning-in-Liar-s-Dice/overleaf/workshop-paper`.

- `AAAI/`: AAAI workshop draft; `main.tex` builds the main paper. The compiled PDF includes `appendix.tex` and the selected 23-agent pairwise and role-conditioned tables in `tournament-23.tex`.
- `AAAI-Anonymous/`: anonymous AAAI submission with supplementary material and a separate source-only code archive.
- `NeurIPS/`: NeurIPS workshop draft using the supplied `neurips_2026.sty`; `main.tex` includes `appendix.tex` by default.

Both subprojects are self-contained, with their own bibliography and figure assets. Open the desired subfolder in Overleaf and select `main.tex` as the main document.

From either subfolder, build with:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The AAAI `aaai27.sty` is the original local compatibility style, not the official submission template; replace it with the venue's official style before submission. NeurIPS uses Courier for scalable monospaced text; optional microtype is enabled when installed. The unused nicefrac import was removed.
