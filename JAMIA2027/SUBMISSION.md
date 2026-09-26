# JAMIA submission checklist (ScholarOne)

Manuscript-side compliance has been addressed in the sources. This file
carries the items that live outside the LaTeX and are handled during the
ScholarOne submission itself.

## In the manuscript (done in the .tex)

- [x] Title page carries word count of the main text (currently **3,969**;
      recount with `texcount -inc -brief -sum=1,0,0,0 background.tex
      methods.tex results.tex discussion.tex conclusion.tex` before final
      submission).
- [x] Double-spaced (setspace + `\doublespacing`) with line numbers.
- [x] Keywords trimmed to 5: *inpatient diabetes; guideline adherence;
      temporal abstraction; electronic health records; propensity score*.
- [x] Alt text under each of the four figure captions, preceded by
      "Alt text:" as JAMIA specifies.
- [x] AI disclosure added to Acknowledgments.
- [x] Corresponding author marked (asterisk footnote on Shahar Oded).
- [ ] **Author degrees on the title page** — placeholder `TODO` in
      `main.tex` above the `\author{}` block. Add ", MD" / ", PhD" /
      ", MSc" etc. per author before recompiling for submission.
- [ ] **Corresponding author postal address + telephone** — placeholders
      in Shahar Oded's `\thanks{}`.

## In ScholarOne (submission portal)

- [ ] **Cover letter** — must repeat the AI-usage disclosure. Suggested
      sentence to include: *"Generative AI tools were used for editorial
      proofreading and formatting of the manuscript. All study design,
      data analyses, and interpretations were performed and verified by
      the authors."*
- [ ] **Figures uploaded as separate image files.** JAMIA wants TIFF,
      EPS, or high-resolution PNG (min. 300 DPI). The four figures are
      embedded in the PDF for review convenience only; upload the source
      images from the Kineret project outputs in the appropriate portal
      fields.
- [ ] **Supplementary material.** Upload `supplementary.pdf` (6 pages)
      as an online-only appendix. Additionally, upload the curated
      concept indices data file (referenced in Methods, Appendix S1,
      and the Data Availability statement).
- [ ] **Promotional tweet field** (<= 280 chars, must include `#JAMIA`):

  > Can automated EHR analysis assess national guideline adherence? Our
  > new multicenter study across 48k+ admissions shows insulin
  > management gaps track mortality and glycemic complications. Read
  > more in #JAMIA! #HealthIT #EHR

- [ ] **CRediT roles** are already declared in `statements.tex` and
      match the ScholarOne CRediT selector.
- [ ] **Funding statement** matches the ScholarOne funder table (MOST
      Kineret 0006850, National Health Policy 2020/284, IPMP 3543/21,
      Horizon Europe 101156210 CARAMEL).
- [ ] **Ethics approvals** and Helsinki numbers are in the Ethics
      Approval statement and match the six-hospital protocol table.
