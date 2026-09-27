# Round-14 Independent Blind-Panel Integration Report — v1.14.0

**Date:** 2026-09-27
**Manuscript under review:** `05_reports/manuscript.md` (tag `v1.14.0`, commit `800063e`)
**Target journal:** Scientific Reports (Nature Portfolio)
**Review structure:** 4 independent experts (A1 Domain / A2 Design / A3 Implementation / A4 Venue), each forbidden from reading prior rounds, plus editor synthesis.

## 1. Verdict

**Minor — no Major, no desk-reject.** The panel characterised v1.14.0 as *"close to Accept"* and explicitly stated the statistical-design baseline is sound; the residual items are mandatory corrections (factual error, version-label mismatch, reference ordering) and cosmetic copy-edit, none rising to a scientific peer-review blocker.

| Reviewer | Verdict | Blocking item(s) |
|---|---|---|
| A1 Domain | Minor | FIS1 hedging to be preserved (non-blocking) |
| A2 Design | Minor (1 blocking factual error) | D-6 CD74/HLA-DQA1 MHC-II region claim is genomically false |
| A3 Implementation | Minor (1 labelling defect) | F1 Data-availability still says tag `v1.13.0` |
| A4 Venue | Minor (3 format corrections) | abstract named-author mention; reference re-numbering; version contradiction |

## 2. Cross-panel concordance

Two independent signals again validated the review process:
- **A2 (Design)** and **A3 (Implementation)** and **A4 (Venue)** *all three* independently caught the `v1.13.0` version leftover in the Data-Availability sentence — a labelling defect, not a data defect, but a credibility risk for the "fully auditable snapshot" claim.
- **A2 (Design)** caught a *new* factual error introduced in v1.14.0 (the MHC-II LD sentence) that no prior round had raised — confirming independence: the panel was not echoing prior rounds.

## 3. Tier-1 / blocking defects (all fixed in v1.15.0)

### D-6 — CD74/HLA-DQA1 "same MHC-II region" is genomically false (A2)
- **Problem:** v1.14.0 stated "CD74 and HLA-DQA1 lie within the same MHC-II region and may share linked instruments." CD74 is on **chr5q32**, HLA-DQA1 on **chr6p21.32** — different chromosomes; they cannot share LD. The motivation (the 45-test BH set is not independent) is legitimate, but the cited mechanism was wrong and invited a one-line rebuttal.
- **Fix (manuscript §5.2):** re-framed on *overlapping hypothesis structure* — "each of the five genes is assessed across three estimators and three outcomes, so the family contains overlapping hypothesis structures (same gene × multiple estimators/outcomes); the correction is therefore a conservative approximation rather than a strict independence guarantee." Verified in source `10_mr_bh_family.csv` (45 rows = 5 × 3 × 3).

### F1 — Data-availability version leftover (A3 + A4)
- **Problem:** `manuscript.md:263` said "the current evaluated commit is tagged **v1.13.0**" while cover letter said `v1.14.0`.
- **Fix:** both Data-availability mentions now read `v1.15.0`.

### V3 — References not numbered by first appearance (A4, Vancouver violation)
- **Problem:** reference [1] first appeared at line 49 while [3] appeared at line 22 — order-of-citation violated.
- **Fix:** re-numbered all 37 references to first-appearance order via an automated script; verified the body's first citation is now `[1]` (Singer/Sepsis-3) and every in-text `[N]` maps to a valid 1–37 entry. Audit gate #23 was made **number-agnostic** (matches ImmunoSep/Giamarellos by author+journal, not label) so it survives re-numbering.

## 4. Tier-2 / non-blocking but fixed in v1.15.0

- **A4 abstract named-author mention:** "Peng et al. reported 0.619" → "0.619 reported on this cohort" (removes a de-facto citation in the abstract, Sci Rep format).
- **A1 FIS1 hedging:** the "most plausibly a passenger" hedge is preserved; no change required, confirmed adequate.

## 5. Tier-3 / carried-forward (cosmetic, not blocking)

- A3-F2: trailing period inside the ImmunoSep DOI (`doi:...24175.`) — harmless; left as-is (now reference [31]).
- A2-D8: deposit the IRG-proxy bootstrap 95% CI as a supplementary cell so the "overlap" claim is demonstrable — suggested, not required; currently asserted from the recomputed 0.5288 only (its CI overlaps the other benchmarks, as stated).
- A2-D10: "calibration-in-the-large adequate" wording — cosmetic; left as-is.

## 6. Editor synthesis

v1.14.0 is a scientifically defensible methods-and-resources report whose numeric claims are reproducible (audit gate 30/30, exit 0; A3 independently confirmed every headline statistic traces to source). The single genuine factual error (D-6) and the two labelling/format defects (F1, V3) are corrected in **v1.15.0**. After this round the manuscript has no remaining Major or desk-reject risk; a further independent panel (Round-15) is convened to confirm a clean Accept.

## 7. Action log

| Item | Source | Status |
|---|---|---|
| D-6 genomic error corrected | A2 | **Done (v1.15.0)** |
| F1 version leftover fixed | A3/A4 | **Done (v1.15.0)** |
| V3 references re-numbered | A4 | **Done (v1.15.0)** |
| Abstract named-author removed | A4 | **Done (v1.15.0)** |
| Gate #23 made number-agnostic | author | **Done (v1.15.0)** |
| Audit 30/30 green | author | **Verified (v1.15.0)** |
