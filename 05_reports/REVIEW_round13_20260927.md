# Round-13 Independent Blind-Panel Review — v1.13.0

**Manuscript:** `05_reports/manuscript.md` (tag `v1.13.0`, commit `0f7f907`)
**Panel:** 4 independent experts (A1 Domain, A2 Design, A3 Implementation, A4 Venue) — none read any prior-round review.
**Date:** 2026-09-27

## 1. Independence statement
Mechanism: each expert received an identical shared brief (`review_r13/_PANEL_BRIEF.md`) that **forbade** reading `REVIEW_round12_20260927.md`, `review_r12/`, any `REVIEW_*.md`/`RESPONSE_*.md`, `.workbuddy/memory/`, the prior `scirep_submission_checklist.md`, and each other's outputs. Experts were told to treat the manuscript as a first submission and to verify every claim against source files.
Evidence it worked: the single most severe finding — the **DCA narrative contradicts the deposited `09_ext_dca_grid.csv`** — was independently identified by **two experts from different layers (A2 Design and A4 Venue)** who had no knowledge of each other. No expert re-litigated already-fixed Round-12 points (e.g., the §7 Chinese translation, ref [32] DOI, dexamethasone "scored high" — all confirmed standing). This is the diagnostic signature of a working blind panel.

## 2. Verdict table
| Expert | Layer | Verdict | Anchored severity |
|---|---|---|---|
| A1 | Domain | Minor | 1 Tier-1 (nivolumab citation over-read) + 1 Tier-2 (HAVCR2/TIM-3 direction vs exhaustion) |
| A2 | Design | Major (Path A) | DCA grid contradiction (D-1) + calibration/ranker inconsistency |
| A3 | Implementation | Minor | 1 Tier-1 (calibration-slope CI untraceable) + 1 Tier-2 (ITGAM unescaped pipe) |
| A4 | Venue | Minor | DCA grid contradiction (confirms A2) + Vancouver ref-order + article-type gloss |
| **Editor** | — | **Minor (required corrections; Path A — same article type, no new data, no downgrade)** | — |

**Editor's adjudication of the A2 "Major" vs A1/A3/A4 "Minor" split:** the DCA grid contradiction is a genuine, cross-validated, must-fix error, but it is a *description* error in a secondary analysis — it does **not** invalidate any headline conclusion (the external AUC 0.638, the MR null, and the 5-hub confirmation all stand; the model's positive net-benefit-over-treat-none is itself correct). Adopting the stricter "Major" verdict would certify a layer, not the manuscript's fate. The editor therefore rates the round **Minor with required corrections** and reclassifies the DCA item as a Tier-1 must-fix-wording rather than a conclusion-invalidating defect. No desk-reject risk: limitations are already candid, numbers trace to source, and the article type is appropriate.

## 3. Cross-verification table (numbers recomputed by the panel)
| # | Location | Manuscript claims | Independently recomputed | Who | Verdict |
|---|---|---|---|---|---|
| 1 | §3.4/§3.5 | External AUC 0.638 (95% CI 0.532–0.748), n=106, 52 deaths | 0.6382 / (0.5317–0.7475) / 106 / 52 | A3 (from `09_external_validation.csv`) | match |
| 2 | §3.4 | L1-locked external AUC 0.585 | 0.5848 | A3 | match |
| 3 | §3.4 | IRG-3 proxy 0.529 (recomputed); Peng 0.619 | 0.5288 / 0.619 | A3 | match |
| 4 | §3.5 | Calibration slope 0.50 / intercept −0.04 | 0.50 / −0.04 (point est.) | A3 | **CI 0.11–0.95 NOT traceable** |
| 5 | §3.5 | DCA: "exceeds treat-all only at ≳0.50, converging near 0.80" | grid: exceeds from 0.30; at 0.80 model=0.0, treat-all=−1.55 (**diverge**) | A2 + A4 (editor-confirmed) | **contradiction** |
| 6 | §3.6 | 5 Mars1-down hubs (CD74/HLA-DQA1/CD14/FCGR3A/HAVCR2) + FIS1 up logFC+1.26 | confirmed in `S01_mars1_deg.csv`, `S01_immunoparalysis_direction.csv` | A1, A3 | match |
| 7 | §3.10 | Mars1 vs Mars2/3/4 P = 0.47 / 1.9e-18 / 1.3e-3 | 0.467 / 1.85e-18 / 1.32e-3 | A3 | match (rounding) |
| 8 | §3.10 | MR primary OR 0.92–1.12, P≥0.23; 27 instruments; counts 23/22/21 | confirmed in `10_genetics_mr.csv`, `10_mr_bh_family.csv` | A2, A3 | match |
| 9 | §3.9 | L1000 ranks lenalidomide 5435 / azithromycin 9152 | 5435 / 9152 | A3 | match |
| 10 | Abstract | 198 words, ≤200, no citations | 198 (re-counted) | A4 | match |
| 11 | cover_letter | consistent with manuscript, tag v1.13.0 | consistent | A4 | match |
| 12 | refs | 37 DOIs present | [32]=10.1001/jama.2025.24175 real; spot-checked 4 DOIs resolve | A3, A4 | match (see R13-6 ordering) |

## 4. Graded consolidated issue list
**Tier 1 — must fix (wording / provenance; no new data)**
- **R13-1 (A2 D-1 + A4, editor-confirmed):** §3.5 DCA sentence contradicts the deposited grid. Fix to: model NB = treat-all up to 0.25, **exceeds treat-all from ≈0.30 onward**, and the gap **widens** at higher thresholds (at 0.80 model NB=0.00 while treat-all NB=−1.55; not "converging"). Replace the "only at ≳0.50, converging toward treat-all near 0.80" clause.
- **R13-2 (A1):** §3 Discussion line 188 calls the Hotchkiss-2019 nivolumab study "showed no benefit [34]". That paper is a **Phase-1b safety/tolerability/PK/PD study** (31 pts; primary endpoints safety+PK; mortality ~40% both arms; not powered for efficacy). Rephrase to "tested only in a Phase 1b safety/pharmacokinetic study that was not powered to show efficacy."
- **R13-3 (A3 + A2 D-3):** §3.5 states calibration slope "0.50 (95% CI 0.11–0.95)". The CI is **not computed anywhere** in `_ext_calibration_dca.py` or the deposited CSV — it is untraceable. Remove the CI; keep the point estimate and "ideal = 1.0".
- **R13-4 (A3):** Table 1 ITGAM row (manuscript.md:82) contains an unescaped `|logFC|` inside a Markdown table cell, which breaks table parsing. Escape as `\|logFC\|` or rephrase.

**Tier 2 — should fix (wording / biological accuracy)**
- **R13-5 (A1):** §4 line 182 frames down-regulated HAVCR2/TIM-3 as "consistent with, but not by itself establishing, T-cell exhaustion." Down-regulated TIM-3 is the *opposite* of the canonical exhausted-T-cell signature (which up-regulates TIM-3); PDCD1/LAG3 are the up-regulated exhaustion markers here. Rephrase so the direction is biologically coherent (reduced checkpoint engagement in the immunosuppressed program; exhaustion-like transcription without canonical TIM-3 elevation).
- **R13-8 (A2 D-4):** The 45-test BH assumes test independence, but CD74 and HLA-DQA1 lie in the same MHC-II region with potentially linked instruments. Add one sentence noting the family-error control is a conservative approximation, not a strict independence guarantee.
- **R13-9 (A2 D-6/D-7):** The three AUCs (0.638 / 0.619 / 0.529) have overlapping CIs; "near-random 0.529" overstates the distinction. Soften to "weak lower-bound reference (CIs overlap, so the comparison is descriptive)."

**Tier 3 — editorial / copy-edit (track, fix at submission)**
- **R13-6 (A4):** References are **not** numbered in order of first appearance (Vancouver violation): [3] is the first in-text cite (line 22) but [1] first appears at line 49. Scientific Reports requires citation-order numbering. **Deferred to copy-edit** because (a) it is a production-stage task Nature's own team performs, (b) the audit gate (#23) and several in-text citations are keyed to current ref numbers, so renumbering now would desynchronise the gate and is high-risk; tracked in `scirep_submission_checklist.md` as a pre-submission step.
- **R13-7 (A4 minor):** "Methods & Resources / Computational Biology" is not a Scientific Reports article type; keep "Article (original research)" and drop the non-standard gloss in the Discussion.
- **R13-10 (A1 minor):** ImmunoSep SOFA benefit attribution, Mars1→28d link cites Scicluna (acceptable but state explicitly), and missing primary citations for PD-1/TIM-3 co-expression and TIM-3 on human APC.
- **R13-11 (A4 minor):** Abstract "Peng et al." named mention is a borderline citation; ref [32] has a trailing period after the DOI.

## 5. Consensus / complementarity / disagreement
- **Consensus:** Core numbers (AUC 0.638/0.585/0.529, MR null, 5-hub confirmation, L1000 ranks) are correct and traceable; limitations reporting is exemplary; article type is appropriate; no desk-reject risk.
- **Complementarity:** A1 caught the clinical-citation over-read (nivolumab) and the HAVCR2 direction issue; A2+A4 independently caught the DCA grid contradiction; A3 caught the untraceable calibration CI and the ITGAM pipe; A4 caught the Vancouver ref-order. Each layer contributed a distinct, non-overlapping defect — the panel was not too diffuse.
- **Disagreement:** A2 rated the DCA item Major; A4 rated it Minor. Editor adjudicated Minor (description error, not conclusion-invalidating) — see §2.

## 6. Priority must-fix list (no DESK-REJECT)
1. R13-1 — DCA narrative ↔ grid contradiction (Tier 1). *Reword.*
2. R13-2 — nivolumab "showed no benefit" over-read (Tier 1). *Reword.*
3. R13-3 — calibration-slope CI untraceable (Tier 1). *Drop CI.*
4. R13-4 — ITGAM unescaped pipe (Tier 1). *Escape.*
5. R13-5 — HAVCR2/TIM-3 direction vs exhaustion (Tier 2). *Reword.*
6. R13-8 — MHC-II LD family-independence caveat (Tier 2). *Add sentence.*
7. R13-9 — soften "near-random 0.529" (Tier 2). *Reword.*

## 7. What stands up (do NOT change)
- External AUC 0.638 (95% CI 0.532–0.748), n=106/52; L1-locked 0.585; IRG proxy 0.529.
- 5 Mars1-down hubs + FIS1 up (logFC +1.26); Mars1 vs Mars2/3/4 P values.
- MR primary-outcome null (OR 0.92–1.12, P≥0.23); 27 instruments; CD74 critical-care flagged as overlap-inflated/reversed.
- Honest limitation framing, generative-AI statement, data availability (v1.13.0), cover-letter consistency.
- 37 references all carry real DOIs (incl. [32] 10.1001/jama.2025.24175).

## 8. Recommended handling path
**Path A — restructure-and-resubmit as the same article type (Article / original research).** No new data, no downgrade. All Tier-1 items are rewordings or a CI removal; the contribution framing (confirmation + honest external validation + blueprint) is sound and already matches the evidence.

## 9. Process lessons (what gates could not catch)
- The 29-assertion audit gate passes arithmetic/provenance but **cannot catch a narrative claim that contradicts a deposited figure's content** (the DCA grid). New assertion needed: a script should extract, from `09_ext_dca_grid.csv`, the threshold at which `nb_model` first exceeds `nb_treat_all`, and the behaviour at the top threshold, then assert the §3.5 prose matches (e.g., "exceeds from ≈0.30" and "diverges at 0.80").
- The gate should not assert a calibration-slope CI that the underlying script never computes (R13-3). Assertions must derive from real deposited outputs.
- A cross-layer cluster (two independent reviewers hitting the same defect) is the strongest evidence the panel is functioning; preserve it in the record.
