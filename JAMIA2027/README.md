# JAMIA 2027 — Research and Applications version

Adaptation of the JBI2027 manuscript to *Journal of the American Medical
Informatics Association* (Oxford University Press). Same study, same data, same
conclusions; restructured and cut to JAMIA's format and length limits.

## Files

| File | Contents |
|---|---|
| `main.tex` | Preamble, title, authors, `\input`s everything else |
| `abstract.tex` | Structured abstract (250 words) + keywords |
| `background.tex` | BACKGROUND AND SIGNIFICANCE + OBJECTIVE |
| `methods.tex` | MATERIALS AND METHODS |
| `results.tex` | RESULTS + all 4 tables + all 4 figures |
| `discussion.tex` | DISCUSSION (Principal findings / Implications / Limitations) |
| `conclusion.tex` | CONCLUSION |
| `statements.tex` | End matter (contributions, funding, COI, data availability, ethics) |
| `supplementary.tex` | **Standalone document** — compile separately |
| `references.bib` | Shared by both documents |
| `figures/` | The 4 figures used |

Build: `pdflatex main && bibtex main && pdflatex main && pdflatex main`, and the
same for `supplementary`. Neither was compiled here — no TeX distribution is
installed on this machine — but references, citation keys, environment balance,
and table column counts were checked programmatically and are consistent.

## Compliance with JAMIA limits

| Requirement | Limit | This draft |
|---|---|---|
| Main text | 4,000 words | ~4,030 by a strict count that includes section headings; ~3,990 excluding them |
| Structured abstract | 250 words | 250 |
| Abstract headings | Objective / Materials and Methods / Results / Discussion / Conclusion | ✅ |
| Body sections | must include Background and Significance | ✅ |
| Tables | 4 | 4 |
| Figures | 6 | 4 |
| References | unlimited | 20 |

## What changed from the JBI version

**Structure**
- JBI's separate *Related Work* section is folded into Background and
  Significance, as JAMIA expects; a short OBJECTIVE section was added.
- JBI's *Statement of Significance* table was removed — that is a JBI
  requirement with no JAMIA equivalent. Its "what this paper adds" content is
  now the closing paragraph of Background and Significance.
- Discussion gained explicit `Principal findings` / `Implications` /
  `Limitations` subsections; JBI's *Future Work* section is compressed into the
  last Implications paragraph.

**Tables (7 → 4)**
- The overall-adherence table and the pre/post-change table were **merged** into
  Table 2 (mean, median, before, after, Δ with CI, *P*).
- The Firth model summary moved to the supplement as Table S2.

**Moved to supplementary material** (to make the 4,000-word limit)
- S1: OMOP extraction and unified tables, concept curation, derived concepts,
  the modified Charlson index, threshold acquisition, the score-aggregation
  staging, and the software stack.
- S2: operational definitions of all ten complications.
- S3: operational definitions of the fourteen guideline recommendations.
- S2 (table): the bias-reduced regression model summary.

**Style**
- Numbered superscript citations (`natbib` with `numbers,super`) in place of
  Elsevier's `elsarticle-num`.
- AMA-style statistics reporting: *P* values without a leading zero (`P<.001`),
  ORs given as `OR, 0.557; 95% CI, 0.514–0.603`, "vs" without a period.
- Section headings set in full capitals via `titlesec`.

## Two things to check before submitting

1. **Document class.** This uses stock `article` with a JAMIA-like preamble so
   it compiles anywhere. To use Oxford's official template, install
   `oup-authoring-template` and swap the `\documentclass` line as described in
   the comment at the top of `main.tex`.
2. **Supplementary table numbering is hardcoded.** The main text cites
   "Supplementary Table S2" for the Firth summary, because the pattern
   definitions table (S1) appears earlier in the supplement. If you reorder the
   supplement, update `results.tex` and `statements.tex` by hand — the two
   documents compile separately, so `\ref` cannot resolve across them.

## Open tasks

All outstanding items are collected in `tasks.tex`, which renders as a red box
on the title page. One switch in `main.tex` controls it and every inline
`[TODO]` marker:

```latex
\showtaskstrue     % draft: task box + inline TODOs visible
\showtasksfalse    % submission: all draft annotations suppressed
```

`tasks.tex` carries no manuscript content and is excluded from the word count.
The three open tasks are: the **funding statement**, **exporting the curated
concept indices** from the closed environment, and a **decision on the
`REDUCE_BASAL_ON_HYPOGLYCEMIA` scoring asymmetry** (see below).

The manuscript now states in three places (Methods, Appendix S1, Data
Availability) that the concept indices are supplied as supplementary material.
That is not yet true — the files must be attached before submission, or the
three statements walked back.

## Pattern revalidation — closed

The author reviewed every row of the pattern table against the knowledge base
and revised three XMLs in the process
(`ROUTINE_GLUCOSE_MEASURE`, `ROUTINE_GLUCOSE_MEASURE_ON_STEROIDS`,
`STOP_SGLT2_ON_ADMISSION`). **The table in Appendix S3 is now ground truth**;
the surrounding prose was brought into line with it, not the other way round.

What changed around the table:

- The aspect column reports **three** types (time, value, cyclic), matching the
  engine — there is no `existence` constraint mechanically, only a time
  constraint carrying `existence-compliance`. Insulin-after-hyperglycemia is
  therefore labelled `Time`, with one sentence in the appendix intro noting it
  is the limiting case: defined by an overlap rather than a delay, so no
  distance exists to grade and the constraint resolves to 1/0. Both papers
  previously showed a fourth `Existence` label in the table while the prose
  claimed three.
- The trapezoid paragraph now notes that several trapezoids are deliberately
  open on one side (full credit at or above a required count), which the two
  revised monitoring patterns rely on.
- The old "second reader" TODO and my interim revalidation footnote are gone.
  In their place is a short paragraph explaining the **basal/bolus asymmetry**
  as intended: basal is routine, so a hypoglycemic event with no following
  basal dose means the dose was withheld and scores 1; bolus is reactive, so
  such events carry no information and are excluded. This is the main reason
  the two components report 0.87 and 0.28 despite sharing a membership
  function.
- Methods in both papers now mention `existence` alongside the three graded
  constraint types.

## Both manuscripts are aligned

The JBI draft was updated in step with this one, and a script check confirms
all 14 pattern rows are now byte-identical between `JAMIA2027/supplementary.tex`
and `JBI2027/appendix.tex`. JBI's main adherence table and its appendix both
label insulin-after-hyperglycemia `Time`, which is what the engine actually
emits; the two files previously disagreed. (The JAMIA version has no Constraint
column, so that contradiction never arose here.)

JBI now carries the same `\showtasks` switch and an equivalent `tasks.tex`
(with Elsevier's funding wording instead of Oxford's). **The two task lists
should be updated together.**
