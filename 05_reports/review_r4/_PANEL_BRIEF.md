# Round 4 — Independent Review Panel Brief

**Manuscript:** `05_reports/manuscript.md` (v1.3.0, commit `fd1ce44`, tag `v1.3.0`)
**Review date:** 2026-09-26 (Round 4)
**Article type under review:** single-author computational multi-omics + in-silico drug-repositioning manuscript, preprint/bioinformatics-journal target.

## Independence discipline (mandatory)
- **Forbidden to read:** `REVIEW_round*.md`, any `RESPONSE_*.md`, `REVISION_*.md`, prior `review_r*/*` directories, `<task status>`, project overview, `SUBMISSION_MANIFEST.md`, deposit SOP, `author_verification_statement.md`.
- **Do not assume the manuscript is mature or has passed prior review.** Treat as a first submission.
- Every judgement must come from text or source data read directly.
- **Any claim that can be verified, MUST be verified** against the raw result files (`03_results/*.csv`).
- No tool talk in the output; write review comments only.

## Output contract (per item)
【Problem】 one sentence
【Evidence】 file:line, or table/section + exact numbers (recomputed where possible)
【Why it matters】 effect on conclusions / credibility / acceptance
【Specific fix】 paste-ready English replacement sentence, or explicit spec for new analysis

## Also required
- § Stands up (≥3, with evidence) — things suspected but found correct.
- § Questions for the authors.
- § What I actually checked — files read, commands run, values recomputed vs manuscript.

## Panel composition (5 lenses)
- A1 Domain / clinical biology
- A2 Design & statistics (MR, multiple testing)
- A3 Implementation / provenance recompute auditor
- A4 Venue & reporting-standard auditor
- A5 Drug-repositioning specialist

## Editor verification (done before consolidation)
The single most severe claim — "under the full 45-test family no estimate reached q<0.05 (smallest q=0.058, CD14 MR-Egger)" — was recomputed independently by the editor from raw CSVs (`10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`). Result: **minimum q = 0.0000 (3 tests q<0.05: CD74 WM crit-care q=0, CD74 Egger crit-care q≈5e-12, CD74 Egger suscept q=0.0025).** The claim is false. See A2 / consolidated T0-D1.
