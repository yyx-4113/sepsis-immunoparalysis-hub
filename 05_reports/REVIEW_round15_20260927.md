# Round-15 Independent Blind-Panel Integration Report — v1.15.0

**Date:** 2026-09-27
**Manuscript under review:** `05_reports/manuscript.md` (tag `v1.15.0`, commit `fc5473b`)
**Target journal:** Scientific Reports (Nature Portfolio)
**Review structure:** 4 independent experts (A1 Domain / A2 Design / A3 Implementation / A4 Venue), each forbidden from reading prior rounds, plus editor synthesis with independent verification of the most severe flagged claim.

## 1. Independence statement
Each expert received the shared `_PANEL_BRIEF.md` and was explicitly forbidden from opening any `REVIEW_round*.md`, `review_r1*/` directory, `.workbuddy/memory/`, or `scirep_submission_checklist.md`. The shared brief told them to treat the manuscript as a first submission and to recompute every numeric claim from `03_results/*.csv` themselves. The diagnostic signal of independence held: the four experts converged on **Minor** with distinct, non-overlapping items, and none re-litigated prior-round points.

## 2. Verdict table

| Reviewer | Verdict | Blocking item(s) |
|---|---|---|
| A1 Domain | Minor | None blocking; flagged 39%-mortality (false positive, see §5), FIS1 "non-immune" overstatement, azithromycin "immunostimulatory" misclassification |
| A2 Design | Minor | One terminology fix (calibration "under-fitting" misnomer); 2 low-severity framing gaps |
| A3 Implementation | Minor | None blocking; `\|logFC\|` prose (false positive, see §5), optional provenance/audit-gap notes |
| A4 Venue | Minor (no desk-reject) | No format hard-fail; only cosmetic trailing-period + veiled abstract wording |

**Distribution:** 4 × Minor, 0 × Major, 0 × Desk-reject.

## 3. Cross-verification table (manuscript claim vs independently recomputed)

| # | Location | Manuscript claim | Recomputed (expert/editor) | Checked by | Verdict |
|---|---|---|---|---|---|
| 1 | §3.5 / 09_ext | external AUC 0.638, CI 0.532–0.748, n=106, 52 deaths | 0.6382 / 0.5317–0.7475 / 106 / 52 | A3 | ✓ |
| 2 | §3.5 / 09_ext_cal | slope 0.50, intercept −0.04, no CI | 0.5028 / −0.0382, no CI cols | A2, A3 | ✓ |
| 3 | §3.5 / 09_ext_dca_grid | model exceeds treat-all from 0.30; at 0.80 model NB 0.00 vs treat-all −1.55 (diverge) | 0.30 crossing (0.2844 vs 0.2722); 0.80 → 0.00 vs −1.5472 | A2, A3, A4 | ✓ |
| 4 | §3.1 / S02 | Mars1 vs Mars2/3/4 P = 0.47 / 1.9e-18 / 1.3e-3 | 0.4671 / 1.85e-18 / 1.32e-3 | A2 | ✓ |
| 5 | §3.10 / MR CSVs | primary IVW OR 0.92–1.12, min P ≥ 0.23; 45-test BH; 27 instruments | OR range confirmed; min P 0.236; 45 = 5×3×3; 27 inst | A2 | ✓ |
| 6 | §3.9 / S08 | L1000 ranks lenalidomide 5435, azithromycin 9152 | 5435 / 9152 | A2, A3 | ✓ |
| 7 | §3.1 / S01 | PDCD1 up (+0.16), HAVCR2 down (−0.35) | +0.162 / −0.349 | A1 | ✓ |
| 8 | Refs / manuscript | 37 refs, first-citation order, [32]→[31] ImmunoSep with 335/775/DOI | 37 entries, first [1], ImmunoSep=ref [31] intact | A3 | ✓ |

## 4. Graded consolidated issue list

**Tier 0 (conclusion-invalidating):** none.
**Tier 1 (must fix — genuine):**
- D1 (A2): "under-fitting slope of 0.50" is wrong terminology — slope < 1 means *over-confident / too-extreme* predictions, which is exactly what the adjacent "over-confident predicted probabilities" already states. Fix adjective → "sub-ideal slope of 0.50 (over-confident predictions)". **→ fixed v1.16.0.**
- D2 (A1): umbrella "immunostimulatory agents" misclassifies azithromycin (anti-inflammatory/immunomodulatory). Rephrase to "immune-modulating". **→ fixed v1.16.0.**

**Tier 2 (wording):**
- W1 (A1): "non-immune passenger" overstates FIS1's immunological irrelevance (mitochondrial fission modulates macrophage/monocyte function). Soften → "non-immune (mitochondrial-fission) passenger". **→ fixed v1.16.0.**
- W2 (A3): record evaluated commit hash in Data availability for provenance. **→ fixed v1.16.0 (commit fc5473b recorded).**

**Tier 3 (format / optional, non-blocking):**
- F1 (A4): ref [31] trailing period inside DOI — cosmetic.
- F2 (A4): abstract's veiled benchmark numbers (0.619/0.529) without citation marker — acceptable at ≤200-word limit; "Peng et al." named mention already removed in v1.15.0.
- F3 (A3): audit does not yet guard CV 0.659 / DEG 3,597 / reference integrity / v1.x cross-file consistency — **→ new assertion #30 added in v1.16.0** (37 refs, first citation [1], no number > 37).

## 5. Editor-verified false positives (not acted upon as errors)
- **A1 "39% 28-day mortality" discrepancy:** the manuscript attributes Mars1's "39% 28-day mortality" to the **MARS-consortium literature** (line 22, ref [5] = Davenport/Scicluna), a published MARS figure. The reviewer recomputed 34.1% (45/132) from *this study's* GSE65682 Mars1 subset — a different cohort. The manuscript's cited 39% is correctly attributed; **no change needed.**
- **A3 "`|logFC|` unescaped" in prose:** all `|logFC|` occurrences are inline prose; markdown renders a bare `|…|` literally unless preceded by a header+separator row (a table). The single true table-cell instance was already escaped in v1.14.0. **No change needed.**

## 6. Priority must-fix list
- [x] D1 calibration terminology — fixed v1.16.0
- [x] D2 azithromycin misclassification — fixed v1.16.0
- [x] W1/W2 wording + provenance — fixed v1.16.0
- [x] F3 audit guard — added #30 v1.16.0
- [ ] F1/F2 cosmetic — optional, non-blocking

No DESK-REJECT flags.

## 7. What stands up (do NOT change)
The Mars1 endotype framing and "near-replication, not discovery" boundary; the 5-hub + FIS1(1+5) structure; the honest external AUC 0.638 (modest, comparable to benchmark, not superior); the IRG "weak reference only" hedge; the DCA divergence framing (matches grid); the MR "hypothesis-generating, no primary IVW significance" scoping; the CD74 critical-care result correctly demoted to genotype–severity; the ImmunoSep caution citation; the 23/22/21 immune-count reproduction; L1000 ranks.

## 8. Recommended handling
**Path A — accept as-is after the v1.16.0 minor wording fixes** (no new data, no article-type change, no downgrade). All four reviewers returned Minor with no Major/desk-reject; the two "material" flags were editor-verified false positives. The manuscript is scientifically sound, numerically reproducible (audit 31/31), and honestly framed. A Round-16 panel is convened to confirm an explicit Accept.

## 9. Process lesson
Gates verify arithmetic + provenance, not design or terminology; a "green" audit co-existed with a wrong calibration adjective ("under-fitting") that only a design reviewer caught. The new #30 reference-integrity assertion extends gate coverage to the re-numbering layer. Trust-but-verify: two reviewer "factual" flags were independently confirmed as false positives (different-cohort mortality; prose markdown rendering) — editor verification prevented unnecessary churn.
