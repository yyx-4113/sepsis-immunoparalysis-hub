# Reviewer A2 — Design layer (statistics + causal inference)

**Manuscript:** *Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning* (single-author, v1.1.0)
**Review layer:** Design — optimism in the prognostic signature, TRIPOD calibration/DCA compliance, MR sample overlap, instrument strength/power, multiple-comparison control, and the selection-chain family-wise error.
**Independence note:** This is treated as a fresh first-submission review. Every number below was re-extracted or recomputed from the `03_results/` CSVs, not paraphrased from the text.

---

## Issues

### Issue 1 — The "honest external 0.638" is a different scoring rule than the CV model, so the stated optimism gap is understated
【Problem】 The external AUC 0.638 that the manuscript calls the "honest out-of-sample generalization" of the 0.659 CV model is the equal-weight fixed-orientation score, whereas the CV 0.659 comes from the L1-logistic model; the L1 model itself transported to only 0.585, so the true portability loss of the trained model is ~0.074, not the implied ~0.021.
【Evidence】 `03_results/09_external_validation.csv`: `auc_GSE65682_CV_locked = 0.6582`, `auc_EMTAB4451_external_locked = 0.5848`, `auc_EMTAB4451_orientedSum = 0.6382`; `S06_auc_compare.csv` CV = 0.6586, train = 0.7495. Manuscript.md:106 ("this within-cohort CV estimate is optimistic; the honest out-of-sample generalization is the external AUC 0.638") and manuscript.md:109 (locked L1 model "transported less well (AUC 0.585)").
【Why it matters】 Comparing CV(L1)=0.659 to external(orientedSum)=0.638 is apples-to-oranges. A reader concludes the trained discriminative model generalizes with only a 0.021 drop, when in fact the L1 model drops to 0.585 — below the recomputed IRG benchmark of 0.604 — i.e. the *model* barely beats (or loses to) benchmark out-of-cohort, while only the simpler equal-weight score reaches 0.638. This inflates the perceived robustness of the developed model.
【Specific fix】 Replace the current framing with a like-for-like statement, e.g.: "The locked L1-logistic model yielded a cross-validated AUC of 0.659 on GSE65682 but transported to only 0.585 (95% CI 0.469–0.696) on E-MTAB-4451, below the recomputed IRG benchmark of 0.604; the more portable component is the gene set and fixed orientation, whose equal-weight score reached 0.638 (95% CI 0.532–0.748). The 0.638 is therefore a portability estimate for the orientation-locked score, not for the trained L1 model."

### Issue 2 — The 0.638 is out-of-cohort but still carries orientation-selection optimism that was never measured
【Problem】 Gene orientation (sign of each gene's contribution to death risk) was derived from GSE65682 28-day labels and then "locked"; the external 0.638 is thus out-of-cohort but not label-independent, and the equal-weight score's own internal CV was never computed, so calling it the "honest generalization" is unsupported.
【Evidence】 Manuscript.md:67 ("gene set + fixed orientation by training-sign correlation with death"); `09_external_validation.csv` contains no CV value for `auc_EMTAB4451_orientedSum` (only `auc_GSE65682_CV_locked = 0.6582`, which is the L1 model). Manuscript.md:189 ("the claim is scoped to the gene set + orientation, not to cohort-specific coefficients").
【Why it matters】 TRIPOD requires that an external estimate be free of training-label leakage. The orientation was learned from the discovery 28-day labels, so the 0.638 still embeds discovery-cohort label information. Without an internal CV (or a permutation/orientation-randomisation) for the equal-weight score, it is unknown whether 0.638 itself is optimistic relative to a truly independent orientation.
【Specific fix】 Either (a) report an internal 5-fold CV AUC for the equal-weight oriented-sum score (using the same locked orientation) so its optimism can be quantified, or (b) soften the claim to: "The fixed-orientation equal-weight score generalised to 0.638 on E-MTAB-4451; because its orientation was still derived from GSE65682 death labels, this estimate may retain optimism and should be read as a portability bound rather than a fully independent validation."

### Issue 3 — Calibration and DCA are referenced only as a figure; no numeric calibration is reported in text, and the scored object is ambiguous
【Problem】 §3.4 cites Fig. S06 (`04_figures/S06_dca.png`) for "calibration and decision-curve analytics," but the text reports no calibration slope, intercept, or calibration-in-the-large, and never states whether the calibration/DCA is for the 0.638 oriented-sum score or the 0.585 L1-locked score.
【Evidence】 Manuscript.md:106 (`04_figures/S06_dca.png` exists in `04_figures/`); no calibration metric appears anywhere in the manuscript text; §3.5 distinguishes the orientedSum (0.638) from the L1-locked (0.585) external scores. TRIPOD items 11–12 require calibration to be reported with a numeric summary.
【Why it matters】 AUC alone over-interprets a prognostic claim. A signature at AUC 0.638 may be well-discriminating yet systematically miscalibrated (e.g., over-predicting risk in a different population), which cannot be judged without a calibration slope/intercept. DCA that is described but not quantified (net benefit at explicit threshold probabilities) provides no decision-making information to the reader.
【Specific fix】 Add to §3.5 a concrete sentence, e.g.: "Calibration of the locked equal-weight oriented-sum score on E-MTAB-4451 showed a calibration slope of X.XX (95% CI X.XX–X.XX) and intercept of X.XX (calibration-in-the-large), indicating [over/under]-prediction; the decision curve demonstrated positive net benefit relative to treat-all and treat-none strategies at threshold probabilities of 0.10–0.50, peaking at X.XX net benefit at threshold 0.XX. These metrics refer to the 0.638 oriented-sum score." (Insert the actual values from the figure's underlying data.)

### Issue 4 — STROBE-MR item 9b harmonisation-exclusion tally is claimed in text but absent from the harmonised CSVs
【Problem】 Manuscript §2.10 states that per-gene exclusion tallies (palindromic, strand-ambiguous, allele-incompatible) "are itemised in the accompanying `*_harmonised.csv` tables (STROBE-MR item 9b)," but the harmonised CSVs contain only retained, harmonised SNPs with no exclusion tally.
【Evidence】 Manuscript.md:72. `10_genetics_mr_outcome5086_harmonised.csv` (rows 2–28) = 27 retained SNPs with columns `rsid, ea_e, nea_e, beta_e, se_e, p_e, eaf_e, ea_o, nea_o, beta_o, se_o, p_o, eaf_o, gene, F` and no column or rows recording dropped SNPs; the same pattern holds for `10_genetics_mr_harmonised.csv` and `10_genetics_mr_outcome4982_harmonised.csv`. FCGR3A is entirely absent (only 2 instruments), confirming the files list retained SNPs only.
【Why it matters】 STROBE-MR item 9b requires reporting the number of SNPs excluded at each harmonisation step. The manuscript's claim is unverifiable from the supplied data, weakening the audit trail and reproducibility of the MR instrument set — a core requirement for a genetics-replication claim.
【Specific fix】 Add a harmonisation-exclusion summary to each harmonised file (or a companion table) with per-gene per-outcome counts: `n_extracted, n_palindromic_dropped, n_strand_ambiguous_dropped, n_allele_incompatible_dropped, n_retained`; then cite it explicitly: "Per-gene harmonisation-exclusion tallies (STROBE-MR item 9b) are provided in `…_harmonised_exclusions.csv`."

### Issue 5 — The shipped CSV's FDR column contradicts the text's reported BH-FDR, and the pooled 0.026 is diluted by tests the authors reject
【Problem】 The `p_fdr_bh` column in the result CSV gives CD14 MR-Egger FDR = 0.0766 (per primary-outcome file), contradicting the manuscript's reported BH-FDR 0.026; the 0.026 only emerges when pooling all 15 Egger tests across the three outcomes, which the text does not state, and that pool includes two CD74 Egger tests the authors themselves disown.
【Evidence】 `10_genetics_mr_outcome5086_28ddeath.csv` row 9: `p = 0.0051096`, `p_fdr_bh = 0.0766435`. Manuscript.md:146 ("BH-FDR 0.026 across all 15 gene × outcome MR-Egger tests"). I recomputed BH-FDR across the 15 Egger p-values (CD74/HLA-DQA1/CD14/HAVCR2/FIS1 × 5086/4980/4982): sorted rank-3 = CD14 primary = 5.11e-3, q = 5.11e-3 × 15 / 3 = 0.0255 ≈ 0.026 — matches the text, but only under cross-outcome pooling. The same pooled logic gives CD74 critical-care IVW FDR = 0.2105 ≈ the text's 0.21, while the per-file CSV shows 0.0701. The pooled Egger family also contains CD74 critical-care Egger (p = 6.6e-13) and CD74 susceptibility Egger (p = 1.6e-4, significant pleiotropy intercept), both of which the authors exclude from interpretation (manuscript.md:171, :190).
【Why it matters】 A reader opening the CSV sees CD14 Egger as NOT FDR-significant (0.0766), directly contradicting the text's significant 0.026 — a provenance inconsistency that undermines trust. Moreover, CD14's apparent FDR-significance is an artifact of a multiplicity family that is inflated by two CD74 estimates the authors reject as non-causal/pleiotropic, so the "0.026" overstates robustness.
【Specific fix】 (a) Add a pooled-FDR column (or a clear note that FDR was computed across the 15 tests per estimator pooled over outcomes) to the CSVs so text and data agree; (b) in §3.10 report both numbers: "CD14 MR-Egger remained nominally significant after BH-FDR correction across all 15 gene×outcome Egger tests (q = 0.026) but not within the primary-outcome family (q = 0.077), and the pooled q is sensitive to inclusion of the two CD74 Egger tests that carry directional pleiotropy; we therefore retain the suggestive-only classification."

### Issue 6 — "Arguing against directional pleiotropy" overstates a 6-SNP Egger intercept test
【Problem】 The CD14 MR-Egger intercept (P = 0.34) is presented as "arguing against directional pleiotropy," but with only 6 instruments (5 df) this test has very low power — it is absence of evidence, not evidence of absence.
【Evidence】 `10_genetics_mr_outcome5086_harmonised.csv`: CD14 n = 6 SNPs. Manuscript.md:146 ("its intercept was not significant (P = 0.34, arguing against directional pleiotropy)"). I recomputed the Egger intercept = −0.00978, P = 0.344 (matches the CSV's `egger_intercept = −0.009779`, `egger_intercept_p = 0.344`).
【Why it matters】 The CD14 signal is already uncorroborated by IVW (OR 0.927, P = 0.24) and weighted median (OR 0.914, P = 0.065). Asserting pleiotropy-robustness from a 6-SNP intercept inflates confidence in a suggestive estimate that the rest of the manuscript correctly demotes.
【Specific fix】 Rephrase to: "the Egger intercept was not significantly different from zero (P = 0.34); however, with only six instruments this test has limited power to detect directional pleiotropy, so it cannot rule it out."

### Issue 7 — The immune-function score is partly tautological and reported without a statistical test or added-value analysis
【Problem】 The composite `score = z(HLA-II) + z(T-cell) − z(exhaustion)` reuses the same gene sets that define Mars1 immunoparalysis, so "Mars1 has the lowest score" is expected by construction; no test across endotypes or added-value-beyond-endotype analysis is reported.
【Evidence】 Manuscript.md:49 (score definition), manuscript.md:100 ("lowest in Mars1 (median −0.79 … the lowest median among the four endotypes, exactly as the immunosuppressed biology predicts"). Endotype sizes from manuscript.md:43: Mars1 = 132, Mars2 = 176, Mars3 = 118, Mars4 = 53 (Mars4 is a sparse cell). No Kruskal–Wallis, ANOVA, or Cox/GLM added-value model appears in the text.
【Why it matters】 Presenting a by-construction result as confirmatory evidence risks circular reasoning. The score adds no independent information beyond the constituent DEGs and the Mars1 endotype label, and the "lowest median" claim has no significance statement despite a small Mars4 subgroup (n = 53).
【Specific fix】 Either add: "A Kruskal–Wallis test across the four endotypes rejected equality of immune-function scores (P = X.XX), with Mars1 lower than each other endotype (Dunn's pairwise P = …); in a Cox model for 28-day death, the immune-function score improved discrimination beyond Mars1 endotype alone (ΔAUC/C-index = X.XX, likelihood-ratio P = X.XX)," or explicitly relabel the score as a descriptive sanity check rather than a finding.

### Issue 8 — Exposure–outcome sample overlap is disclosed but no feasible correction was applied
【Problem】 The eQTLGen × UK Biobank participant overlap is disclosed and correctly flagged as a limitation, but no overlap correction was applied, leaving the direction and magnitude of potential bias unknown.
【Evidence】 Manuscript.md:70 and manuscript.md:190 (overlap disclosed; "We did not apply a sample-overlap correction … the estimates are consequently interpreted only as hypothesis-generating"). Confirmed: the disclosure is present and honest.
【Why it matters】 With overlap, the MR estimates can be biased toward the observational expression–outcome association; for CD14 (the only nominally significant Egger) the uncorrected protective OR could be inflated or attenuated in either direction. A "hypothesis-generating only" stance is appropriate, but the magnitude remains uninterpretable without at least a sensitivity correction.
【Specific fix】 Apply the Burgess–Davies–Thompson (2016) participant-overlap correction using the estimated UK-Biobank-in-eQTLGen overlap fraction and report: "After applying the sample-overlap correction of Burgess, Davies & Thompson (2016) (estimated overlap fraction f = X.XX), the CD14 MR-Egger OR was X.XX (95% CI X.XX–X.XX), [unchanged/reversed in direction], indicating that sample overlap [does/does not] explain the observed protective association." If the overlap fraction is unknown, at minimum state the correction was attempted and report its input requirement.

---

## § Stands up (verified correct)

1. **Optimistic-CV framing is honestly stated.** §3.4 explicitly says the 0.659 CV AUC is optimistic because gene selection/orientation used the same 28-day labels, and designates the external 0.638 as the honest estimate. I verified `S06_auc_compare.csv` CV = 0.6586 (→0.659) and train = 0.7495 (→0.750); `09_external_validation.csv` `auc_EMTAB4451_orientedSum = 0.6382` with CI 0.5317–0.7475 (matches text 0.532–0.748), and `auc_IRG3_benchmark_EMTAB4451 = 0.604` matches the recomputed IRG benchmark cited in text. The 0.638 is genuinely a locked, fixed-orientation, out-of-cohort score.
2. **CD14 MR-Egger estimate and its "suggestive-only" framing reproduce exactly.** I recomputed from `10_genetics_mr_outcome5086_harmonised.csv`: MR-Egger OR = 0.9060 (95% CI 0.845–0.971), P = 5.11e-3; intercept = −0.00978, P = 0.344. These match the text (0.906, 5.1e-3) and Table 3. The text correctly notes it is "not corroborated by IVW or the weighted median" (IVW OR 0.927, P = 0.24; weighted median OR 0.914, P = 0.065 — both verified against the CSV).
3. **Sample-overlap limitation is explicitly disclosed** in both §2.10 and §5 (limitation #2), with acknowledgment that no correction was applied — an honest treatment of a structural MR weakness.
4. **Table 3 instrument counts and median F-statistics all verify.** Recomputed per-gene medians from the harmonised F column: CD74 35.4 (3 IVs), HLA-DQA1 168.1 (4), CD14 45.7 (6), HAVCR2 36.4 (6), FIS1 75.0 (8) — all match the manuscript. Per-SNP F ≥ 30 throughout, so instrument strength is adequate; CD14's weakness is instrument count (6), not weak instruments, which the text states correctly.
5. **Selection-chain family-wise error is acknowledged** (§5 limitation #10, manuscript.md:199), covering the DEG → co-expression → tri-method ML chaining and the label-reuse in signature orientation. This is the correct honest caveat.
6. **The text's pooled BH-FDR values are arithmetically correct** when computed across the 15 tests per estimator (I recomputed CD14 Egger q = 0.0255 ≈ 0.026 and CD74 critical-care IVW q = 0.2105 ≈ 0.21), so the discrepancy in Issue 5 is a CSV/text provenance mismatch and a family-definition ambiguity, not an arithmetic error in the text.

---

## § Questions for the authors (do not guess)

1. Was the designation of `ieu-b-5086` (28-day death) as the *primary* MR outcome pre-specified before any MR result was seen, or was it chosen because the observational signature predicts 28-day mortality (i.e., motivated by the signature result)? The §2.10 rationale reads as phenotype-matching, but the motivation matters for the circularity assessment.
2. For Fig. S06, which score is the calibration/DCA computed on — the equal-weight oriented-sum (0.638) or the L1-locked (0.585)? Are the net-benefit values at specific threshold probabilities available from the underlying data?
3. The `*_harmonised.csv` files contain only retained SNPs. Where exactly are the palindromic / strand-ambiguous / allele-incompatible exclusion counts (STROBE-MR item 9b) stored? Are FCGR3A's two variants retained anywhere, or fully dropped from all outputs?
4. Is the equal-weight oriented-sum score's internal CV AUC available, or was optimism for that scoring rule never assessed? (Related to Issue 2.)
5. For the immune-function score, was any statistical test of "lowest in Mars1" across the four endotypes performed, or any added-value analysis beyond Mars1 endotype, even internally? (Related to Issue 7.)

---

## § What I actually checked

**Files read (allowed):** `manuscript.md`, `_PANEL_BRIEF.md` (brief only); `03_results/S06_auc_compare.csv`, `03_results/09_external_validation.csv`, `03_results/10_genetics_mr_outcome5086_harmonised.csv`, `03_results/10_genetics_mr_harmonised.csv` (susceptibility `ieu-b-4980`), `03_results/10_genetics_mr_outcome4982_harmonised.csv`, `03_results/10_genetics_mr_outcome5086_28ddeath.csv`, `03_results/10_genetics_mr.csv`, `03_results/10_genetics_mr_outcome4982_criticalcare.csv`, `03_results/10_genetics_mr_design.md`; confirmed `04_figures/S06_dca.png` exists.

**Values recomputed/extracted vs manuscript (discrepancy stated):**
- CV AUC: file 0.6586 → text 0.659 ✓; train 0.7495 → 0.750 ✓.
- External orientedSum: file 0.6382 → text 0.638 ✓; CI 0.5317–0.7475 → 0.532–0.748 ✓; IRG recomputed 0.604 → text 0.604 ✓; L1-locked external 0.5848 → text 0.585 ✓.
- CD14 MR-Egger: recomputed OR 0.9060, P 5.11e-3 → text 0.906 / 5.1e-3 ✓ (independent recomputation from harmonised beta_e/beta_o).
- CD14 IVW: recomputed OR 0.9269, P 0.236 → text 0.927 / 0.24 ✓; weighted median OR 0.9144, P 0.0649 → text 0.914 / 0.065 ✓.
- CD14 Egger intercept: recomputed −0.00978, P 0.344 → CSV −0.009779 / 0.344 ✓.
- Median F per gene: CD14 recomputed 45.65 → text 45.7 ✓; HLA-DQA1 168.1 ✓; CD74 35.4 ✓; HAVCR2 36.4 ✓; FIS1 75.0 ✓. n IVs 3/4/6/6/8 ✓.
- Pooled BH-FDR: CD14 Egger recomputed 0.0255 → text 0.026 ✓; CD74 critical-care IVW recomputed 0.2105 → text ≈0.21 ✓.

**Discrepancies found (none are arithmetic errors in the text; they are provenance/family-definition gaps):**
1. `10_genetics_mr_outcome5086_28ddeath.csv` `p_fdr_bh` for CD14 Egger = **0.0766** (per-primary-outcome family), contradicting the text's pooled **0.026**.
2. `10_genetics_mr_outcome4982_criticalcare.csv` `p_fdr_bh` for CD74 IVW = **0.0701** (per-outcome family), contradicting the text's pooled **≈0.21**.
3. STROBE-MR harmonisation-exclusion tally claimed in manuscript.md:72 as "itemised in the accompanying `*_harmonised.csv` tables" is **absent** from all three harmonised CSVs (they list only retained SNPs; no palindromic/strand-ambiguous/allele-incompatible counts). See Issue 4.

No forbidden files were opened.
