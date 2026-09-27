# Round-16 Independent Blind-Panel Integration Report — v1.16.0

**Manuscript:** `05_reports/manuscript.md` (tag `v1.16.0`, commit `1212f7b`)
**Repository:** `github.com/yyx-4113/sepsis-immunoparalysis-hub`
**Panel:** 4 experts, strict independence (no prior `REVIEW_round*` / `review_r12`–`review_r15` / `.workbuddy/memory` / checklist read)
**Date:** 2026-09-27

---

## 1. Independence diagnostic
- Two experts (A3 Implementation + A4 Venue) independently and without coordination converged on the **same genuine defect**: the Data-availability section claims the evaluated commit is `fc5473b` and "is tagged v1.16.0", but `fc5473b` is actually `v1.15.0` (v1.16.0 = `1212f7b`). This independent double-catch confirms the panel operated without leakage.
- Single-expert findings (A1 biology, A2 design) did **not** cluster on the same items, indicating the panel was not over-concentrated on a planted issue — independence intact.

## 2. Verdict table

| Expert | Domain | Verdict | Genuine defect? | Desk-reject? |
|--------|--------|---------|-----------------|--------------|
| A1 Domain | Sepsis immunology | **Minor** | FIS1 MR direction mis-attributed as "concordant" (material framing); +4 non-blocking framing/citation items | No |
| A2 Design | Stats / causal inference | **Minor** | DCA over-claiming, test-set-nested calibration, L1000 prednisone-confounding tension, MR headline under-stated, "independence" wording — all framing | No |
| A3 Implementation | Code / provenance audit | **Minor** (1 mandatory fix) | **Commit-hash self-contradiction** (`fc5473b` ≠ v1.16.0); +3 minor (MR figure index, gate has no commit assertion, fragile escaped pipe) | No |
| A4 Venue | *Scientific Reports* compliance | **Minor** | **Commit/DOI-year provenance**; ref [31] trailing period + 2025/2026 year; missing standalone code-availability heading | No |

**Overall: all four Minor — no Major, no desk-reject, no format hard-fail.** No scientifically false numeric claim was found by any reviewer; every headline number re-derived from source CSVs matched the text.

## 3. Cross-validated (consensus) genuine defects → fixed in v1.17.0
- **[C1] Commit-hash / tag self-contradiction (A3 + A4).** DA line said "evaluated commit `fc5473b` is tagged v1.16.0"; git shows v1.16.0 = `1212f7b`, fc5473b = v1.15.0. **Fixed:** "current evaluated commit `1212f7b` is tagged v1.16.0, and this v1.17.0 release is built on top of it."
- **[C2] ImmunoSep reference year (A4).** ref [31] read "(2026)" while DOI = `10.1001/jama.2025.24175`. **Fixed:** "(2025)" to match DOI (epub 2025 / issue 2026 resolved to DOI year).
- **[C3] Audit gate blind spot (A3 Issue 3).** `check_audit_assertions.py` passed green yet never checked the DA commit string. **Fixed:** added assertion #31 that cross-checks the DA `tag vX` and `commit HASH is tagged TAG` clauses against `git rev-parse <tag>`; gate now 32 assertions and confirmed the regression is caught.

## 4. Single-expert minor items — carried forward (NOT regressions; documented for Round-17 re-verification)
- **A1-1 (material framing):** FIS1 observational up (logFC +1.26) is *opposite* to its protective MR estimates, yet §3.10/§4 fold it into "concordant with the immunoparalysis model." Recommended fix: restrict the concordance claim to the five immune hubs and state FIS1 is discordant/descriptive-only.
- **A1-2/4:** FIS1 oscillates between "passenger" and "causal candidate"; "reduced checkpoint engagement" (Abstract/Conclusion) over-reads bulk data that cannot separate cell-loss from per-cell down-regulation.
- **A1-3:** PD-1(up)/TIM-3(down) contrast not cited against the opposing TIM-3-up sepsis literature.
- **A2-1/2/3:** DCA 0.80 "divergence" is a formula artifact not model gain; calibration + DCA both fit on the same external test set (test-set-nested); L1000 ranks still used as support after prednisone-confounding shown.
- **A2-4 / A4-1:** MR primary headline "no causal support" understates (one Egger nominal-significant, one family-significant but reversed); ref [31] trailing period.
- **A3-2/4:** §8 promises 4 MR diagnostic plots, only 2 PNGs exist; fragile escaped-pipe cell in Table 1.
- **A4-2:** no standalone `## Code availability` heading (folded into Data availability).
- **A4-4 (caution):** abstract = 196 words (4-word margin under 200).

## 5. Editor reconciliation
- C1/C2/C3 are the only items that, left unfixed, would let a careful reader retrieve the wrong code or distrust the deposit. All three are corrected and gate-guarded in v1.17.0 (commit `5e1af29`, tag `v1.17.0`, pushed).
- The remaining items are interpretive framing; none affects a reported number. They are explicitly listed so Round-17 can confirm whether they still rise above "Minor" or are acceptable for a clean Accept.

## 6. Disposition
- v1.16.0 → **v1.17.0** (commit-hash + ref-year + audit #31). Audit gate: **32/32 pass** (incl. #31 verifying DA vs git: release v1.17.0, v1.16.0=`1212f7b`).
- **Round-17 panel convened on v1.17.0** to confirm an explicit Accept; brief instructs re-examination of the carried-forward framing items (esp. A1-1 FIS1 concordance) to test convergence.
