# Round-17 Blind Design Review — A2 (statistics / causal inference)

**Manuscript tag:** v1.17.0 · **Commit evaluated:** 1212f7b (tagged v1.16.0; v1.17.0 built on top) · **Status:** first submission (treated as such).
**Focus:** statistical and causal-inference design soundness of the external validation, decision-curve analysis, calibration, L1000 repurposing evidence, and Mendelian-randomisation interpretation.
Every number below was re-derived from the deposited CSVs; recomputed values match the manuscript unless noted.

---

## Issues

### Issue 1 — DCA "divergence" at threshold 0.80 is a formula artifact, not a model gain (priority)
【Problem】The claim that at threshold 0.80 "model NB = 0.00 while treat-all NB = −1.55 (they DIVERGE, not converge)" presents a DCA-formula artefact as if the model decisively wins.
【Evidence】`03_results/09_ext_dca_grid.csv`: at thr 0.80 `nb_model = 0.00`, `nb_treat_all = −1.5472` (manuscript quotes −1.55). Treat-all net benefit at threshold *t* is `prevalence − (1−prevalence)·t/(1−t)`; with prevalence 52/106 = 0.4906 this gives `0.4906 − 0.5094·0.80/0.20 = −1.547`, i.e. the −1.55 is pure algebra, independent of the model. The model NB = 0.00 at 0.80 equals the **treat-none** baseline (NB is always 0), meaning the calibration-corrected probabilities never exceed 0.80, so the model treats *nobody* at that threshold. The "divergence" is simply treat-all NB → −∞ as *t*→1 while the model correctly withholds action.
Across thresholds the actual model-vs-treat-all NB is:
- 0.05–0.25: identical (model == treat-all, NB equal) — at low thresholds the model behaves exactly like treat-all;
- 0.30: 0.2844 vs 0.2722 (margin +0.012); 0.45: 0.1029 vs 0.0738 (+0.029); 0.50: 0.0755 vs −0.0189 (+0.094); 0.60: 0.0472 vs −0.2736 (+0.321); 0.75: 0.0094 vs −1.0377 (+1.05); 0.80: 0.00 vs −1.5472.
Model NB itself is small everywhere (peaks ≈0.10 around thr 0.45–0.50, then decays toward 0 at 0.75–0.90). The large apparent margins at thr ≥0.55 are driven almost entirely by the treat-all penalty collapsing, not by model discrimination.
【Why it matters】The DCA is the paper's only clinical-utility claim. Framing an artefact as a "divergence" overstates decision value and is the kind of statement a reviewer (and a clinical reader) will challenge; it can be read as spin on a weak signal.
【Specific fix】Replace with: "The calibration-corrected model had positive net benefit versus treat-none across thresholds 0.10–0.75 (peak NB ≈0.10 at threshold 0.45–0.50) and exceeded the treat-all strategy only modestly, by ≤0.04 NB, in the 0.30–0.50 band; at thresholds ≥0.55 the apparent gap is driven by the treat-all net benefit collapsing toward −∞ as the threshold approaches 1, while the model (recommending no treatment above 0.80) ties the treat-none baseline. The decision-curve therefore supports risk ranking, not a clinically decisive treatment-trigger threshold."

### Issue 2 — Calibration slope/intercept are fitted on the same external test set (test-set-nested), optimism undisclosed
【Problem】The calibration slope 0.50 / intercept −0.04 used to "calibration-correct" the probabilities feeding the DCA are estimated *on E-MTAB-4451 itself* — the same 106-sample set used for validation — yet this optimism is never disclosed.
【Evidence】`03_results/09_ext_calibration_dca.csv`: single row, `calib_intercept = −0.0382`, `calib_slope = 0.5028`, `n = 106`, `deaths = 52`. The §3.5 text ("the decision-curve analysis — computed on the calibration-corrected probabilities from the external logistic fit (intercept −0.04, slope 0.50)") fits the recalibration on the test set. No bootstrap/internal-CV optimism correction is reported; no CI on the slope (the brief asks to confirm none is claimed — confirmed, none stated). A slope estimated on n=106/52 events is itself noisy.
【Why it matters】The external *AUC* (0.638) is honest because the model was locked; but the recalibration and the DCA net benefit are fit on the test data, so the favourable DCA (Issue 1) is optimistic by construction. This is a second, undisclosed source of optimism layered on top of the orientation leak (Issue 5).
【Specific fix】State explicitly: "The calibration slope/intercept were estimated on the same E-MTAB-4451 test set used for validation, so the calibration-corrected DCA is optimistically biased and should be read as illustrative; a defensible calibration/DCA requires refitting on a training set and validating on a held-out cohort, or a bootstrap optimism correction." Add a CI (or a bootstrap) for the slope.

### Issue 3 — L1000 ranks of lenalidomide/azithromycin are still used as supportive evidence despite the prednisone contradiction
【Problem】After showing that prednisone — a clinical immunosuppressant — scores in the 3.2nd percentile on the same Mars1-down "rescue" axis, the manuscript still presents the lenalidomide and azithromycin L1000 ranks as directional support for the repositioning shortlist.
【Evidence】`03_results/S08_l1000_candidate_scores.csv`: azithromycin rescue 0.0133, rank 9152/20,413 (44.8th pct); lenalidomide rescue 0.0439, rank 5435/20,413 (26.6th pct). §3.9 reports prednisone rescue 0.136, rank 651/20,413 (3.2nd pct) and correctly concludes "the L1000 'rescue' proxy is not a validated marker of immune restoration." Yet §3.9, §3.10 and the Conclusion still cite "directional-but-modest LINCS L1000 rescue" as supporting evidence for these two small molecules ("In-silico repositioning ... their small-molecule counterparts lenalidomide and azithromycin show directional-but-modest LINCS L1000 rescue").
【Why it matters】This is an internal contradiction on a core translational claim. A metric that ranks an immunosuppressant in the top 3% cannot simultaneously credibly support two immunomodulators; using the same metric both as refuted (prednisone) and as supportive (lenalidomide/azithromycin) undermines the repositioning evidence base. It also feeds the DCA/clinical-utility over-claim.
【Specific fix】Either (a) demote L1000 for the two small molecules from "supportive" to "non-evidence / descriptive only," stating that the prednisone result invalidates the axis as a support metric; or (b) explicitly explain why prednisone's high score is a glucocorticoid-class anomaly that does not apply to these agents. The current "acknowledge caveat but still cite as support" wording is inconsistent and should be resolved in favour of (a).

### Issue 4 — MR "no causal support" headline understates the actual results
【Problem】The Abstract/Conclusion blanket "two-sample MR gave no causal support on the primary 28-day-death outcome (all IVW OR 0.92–1.12, P ≥ 0.23)" understates two results that survive the paper's own checks.
【Evidence】`10_genetics_mr_outcome5086_28ddeath.csv`: CD14 MR-Egger OR 0.906, **P = 4.88×10⁻²** (nominally significant, <0.05); the Egger intercept is non-significant (P=0.34). `10_mr_bh_family.csv`: CD74 critical-care weighted median OR 2.194, p = 6.6×10⁻¹⁹, **family q ≈ 3×10⁻¹⁷** (the only one of 45 tests surviving the family correction) — but reversed direction (higher predicted CD74 → worse critical-care outcome, opposite to the Mars1 down-regulation model). The body text (§3.10, §5) does discuss both; the defect is the top-line framing, which implies a uniformly null MR.
【Why it matters】"No causal support" is true only for IVW on the primary outcome. The Abstract phrasing omits (i) a nominally significant protective Egger for CD14 and (ii) a family-significant (but reversed) CD74 critical-care signal — exactly the nuance a methods-and-resources reader needs. Understating here is the mirror image of overstating the DCA.
【Specific fix】Abstract: "Two-sample MR gave no significant IVW support on the primary 28-day-death outcome (all OR 0.92–1.12, P ≥ 0.23); one estimator (CD14 MR-Egger) was nominally significant (OR 0.906, P = 0.049) and one critical-care signal (CD74 weighted median) survived family correction but in the reversed direction (OR 2.19, q ≈ 3×10⁻¹⁷), so the MR layer remains hypothesis-generating."

### Issue 5 — "Honest / independent external validation" wording overstates independence (label not independent)
【Problem】"Honest external, cross-platform AUC," "independent external AUC 0.638," and "honest independent cross-platform external validation" appear in the Abstract, §3.5 lead, §4 and Conclusion, while the label-dependence is only disclosed later in §3.5.
【Evidence】§3.5: "The fixed orientation was trained on GSE65682 28-day labels, so the external application is independent in cohort and platform but not in label." So only cohort and platform are independent; the 28-day-label orientation leaks discovery information into the "external" score. The AUC 0.638 is on a locked *model* but a label-trained *orientation*.
【Why it matters】The headline adjective "independent" is strictly false for the label dimension; an MR/causal-inference reviewer will read "independent external validation" as fully held-out and may over-weight the 0.638. The disclosure exists in the body, so this is a framing defect, not a hidden one.
【Specific fix】Qualify the headline: "an honest external validation (independent in cohort and platform; orientation fixed on the discovery 28-day labels, so not label-independent)."

### Issue 6 — FIS1 is mis-framed as "concordant with the immunoparalysis model" in the MR result
【Problem】§3.10 states "three of the five assessable hubs (HLA-DQA1, CD14, FIS1) returned protective estimates concordant across all three methods … the direction predicted by the immunoparalysis model," but FIS1 is *up*-regulated in Mars1, so a protective MR (OR<1) is opposite to its observational association.
【Evidence】`S01_mars1_deg.csv`: FIS1 `logFC = +1.261`, t = +17.16, DEG_0.3/1.0 = True (up in Mars1). Mars1 is the high-mortality immunosuppressed endotype, so observationally higher FIS1 tracks with worse outcome. The MR estimate for FIS1 28-day death is IVW OR 0.963 (protective, OR<1) — i.e. higher genetically predicted FIS1 → lower death, the reverse of the observational direction. For the *down*-regulated hubs (CD74/HLA-DQA1/CD14/HAVCR2) a protective MR is genuinely concordant; for FIS1 (an up-regulated co-expression passenger) it is not. The manuscript itself calls FIS1 a "co-expression passenger … not a member of the down-regulated immunosuppression axis" (§3.3), so folding it into "predicted by the immunoparalysis model" is internally inconsistent.
【Why it matters】It inflates the concordance narrative (3/5 hubs "concordant" becomes 2/5 if FIS1 is excluded on directionality grounds) and is a logical error in a stated result, not merely a wording choice.
【Specific fix】"HLA-DQA1 and CD14 returned protective estimates concordant across all three methods, the direction predicted by the immunoparalysis model for the down-regulated hubs; FIS1 also gave a protective MR point estimate, but because FIS1 is up-regulated in Mars1 this direction is opposite to its observational association and is reported as a passenger-gene null-of-interest rather than as model-concordant."

### Issue 7 (minor) — §8 references four MR diagnostic plots that do not exist
【Problem】§8 lists the MR diagnostic set as "forest, scatter, funnel, leave-one-out" (four plots), but `04_figures/` contains only `mr_forest.png` and `mr_diag.png` (and `S06_dca.png`).
【Evidence】Directory listing of `04_figures/`: `mr_forest.png`, `mr_diag.png`, `S06_dca.png` only — no scatter / funnel / leave-one-out files. The §8 index therefore references non-existent figures.
【Why it matters】Phantom figure references fail Scientific Reports' figure-availability check and signal incomplete production.
【Specific fix】Either generate and deposit `mr_scatter.png`, `mr_funnel.png`, `mr_loo.png`, or correct §8 to "forest and diagnostic (mr_diag.png) plots."

### Issue 8 (minor/cosmetic) — smaller items
- **45-test BH "conservative approximation" wording** (Limitation 2): BH on positively-correlated MR tests (same instruments/gene across estimators and outcomes) is, at best, not strictly conservative under arbitrary dependence; the "conservative" label is loose. Defensible as a heuristic but rephrase to "a dependence-ignoring approximation."
- **"Reduced checkpoint engagement" over-read** (§3.1, §4): HAVCR2/TIM-3 down is interpreted as "reduced checkpoint engagement" from bulk data that cannot separate APC/monocyte abundance from per-cell expression. §3.1 hedges this; §4 states it more firmly. Keep the §3.1 hedge in §4.
- **Reference [31]** trailing period after the DOI (`doi:10.1001/jama.2025.24175.`) — remove the trailing period.
- **No standalone "Code availability" heading** — Sci Rep expects one; the Data availability section mentions MIT code but a separate heading is safer.
- **Table 1 ITGAM cell** contains an escaped `\|logFC\|` inside the Function text; it renders but is fragile — consider rephrasing to avoid an inline escaped pipe.

---

## § Stands up (verified)

1. **External AUC is exactly as reported.** Recomputed from `09_external_validation.csv`: `auc_EMTAB4451_orientedSum = 0.6382` (manuscript 0.638), 95% CI `0.5317–0.7475` (manuscript 0.532–0.748), `n_validated_samples = 106`, `n_deaths = 52`. Matches the stated "honest external AUC 0.638 (95% CI 0.532–0.748; n=106; 52 deaths)."
2. **Mann–Whitney P-values recompute exactly.** From `S02_immunoparalysis_score.csv`: Mars1 vs Mars2 P = 0.467 (manuscript 0.47); vs Mars3 P = 1.85×10⁻¹⁸ (manuscript 1.9×10⁻¹⁸); vs Mars4 P = 1.32×10⁻³ (manuscript 1.3×10⁻³). Medians (−0.792 / −0.752 / 0.641 / −0.235) also match.
3. **MR family BH readout is internally consistent and the reversed CD74 signal is real.** From `10_mr_bh_family.csv`: only CD74 critical-care weighted median has `family_sig_q<0.05 = YES` (q ≈ 2.99×10⁻¹⁷), OR 2.194, reversed vs Mars1 model; CD14 28-day Egger `p = 0.0488` with `q_family = 0.730`; all other 43 tests non-significant. The CSVs and manuscript agree.
4. **L1000 candidate ranks are correctly computed.** `S08_l1000_candidate_scores.csv`: lenalidomide rank 5435/20,413 = 26.6th pct (manuscript "top 26.6%"); azithromycin rank 9152/20,413 = 44.8th pct (manuscript "≈ median"). Correct.
5. **Calibration values are as stated, and no CI is claimed.** `09_ext_calibration_dca.csv`: slope 0.5028 (manuscript 0.50), intercept −0.0382 (−0.04); no CI column — consistent with the brief's "NO 95% CI claimed."

---

## § Questions for the authors

1. For the DCA, was the net benefit computed on probabilities recalibrated on E-MTAB-4451, or on the raw locked-score risks? If recalibrated on the test set, do you agree this is optimistic and should be reframed as illustrative (Issue 2)?
2. Given prednisone scores in the 3.2nd percentile on the same Mars1-down axis, on what basis do you retain the lenalidomide/azithromycin L1000 ranks as *supportive* rather than *descriptive* evidence (Issue 3)?
3. For FIS1, do you agree the protective MR direction is opposite to its observational up-regulation in Mars1, and should it therefore be removed from the "model-concordant" count (Issue 6)?
4. The §8 MR figure index lists four plots but only two exist in `04_figures/` — were the scatter/funnel/leave-one-out plots generated and, if so, where are they deposited (Issue 7)?
5. The 45-test family mixes estimators (IVW/Egger/WM) and outcomes on the same instruments/genes. Did you consider a dependence-adjusted correction (e.g., Benjamini–Yekutieli) and, if so, does the CD74 critical-care or CD14 Egger result survive it?

---

## § What I actually checked

**Files read (directly):**
- `05_reports/manuscript.md` (full), `05_reports/_PANEL_BRIEF.md` (full).
- `03_results/09_external_validation.csv`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`.
- `03_results/S08_l1000_candidate_scores.csv`, `10_genetics_mr_outcome5086_28ddeath.csv`, `10_mr_bh_family.csv`.
- `03_results/S02_immunoparalysis_score.csv`, `S01_mars1_deg.csv` (FIS1 row).
- Directory listing of `04_figures/` (grep for mr/dca/forest/diag/scatter/funnel/loo).

**Computations run (Python, managed interpreter):**
- Mann–Whitney U, Mars1 vs Mars2/3/4 on `S02_immunoparalysis_score.csv` → P = 0.467 / 1.85e-18 / 1.32e-3 (match manuscript).
- Verified treat-all NB formula at thr 0.80 reproduces −1.547 from prevalence 0.4906.
- Read FIS1 `logFC = +1.261` from `S01_mars1_deg.csv` (confirms up-regulation).
- Cross-checked MR CSVs: CD14 Egger P = 4.88e-2, CD74 crit-care WM q ≈ 3e-17 reversed, L1000 ranks 5435/9152 → 26.6%/44.8%.

**Recomputed vs manuscript — discrepancies:** None in the raw numbers; all recomputed values match. The discrepancies are in *interpretation/framing*: DCA 0.80 "divergence" (Issue 1), undisclosed test-set-nested calibration (Issue 2), L1000 supportive use despite prednisone (Issue 3), MR Abstract understatement (Issue 4), "independent" wording (Issue 5), FIS1 concordance mis-framing (Issue 6), phantom MR figures (Issue 7).

**Forbidden files NOT opened:** no `05_reports/REVIEW_round*.md`; no `review_r12/`–`review_r16/`; no `.workbuddy/memory/`; no `05_reports/scirep_submission_checklist.md`; no other `05_reports/review_r17/*` file besides the brief. No prior-round or memory content was consulted; this was treated as a first submission.

---

## VERDICT — Major revision

**Justification.** All recomputed numbers match the deposited CSVs, so there is no data fabrication and no desk-reject trigger. However, several *design/interpretation* defects bear directly on the paper's central translational and clinical-utility claims and must be fixed before acceptance:

- **Genuine design/interpretation defects (fixable by revision, no new data strictly required):** (1) DCA 0.80 "divergence" is a formula artefact mis-sold as a model win; (2) calibration — and thus the DCA — is fitted on the same external test set, an undisclosed optimism source; (3) the L1000 axis is used as *supportive* evidence for lenalidomide/azithromycin despite the manuscript's own prednisone result refuting that axis (internal contradiction on a core claim); (6) FIS1 is logically mis-framed as "concordant with the immunoparalysis model" when its protective MR opposes its observational up-regulation. (4) and (5) are top-line framing over-/under-statements (independence; MR "no causal support") that the body text partially mitigates but the Abstract/Conclusion do not.

- **Cosmetic / minor:** phantom MR figures (§8), 45-test BH "conservative" wording, "reduced checkpoint engagement" over-read, reference [31] trailing period, missing Code-availability heading, fragile escaped pipe in Table 1.

The revision is feasible without new experiments: it requires re-framing the DCA and calibration discussion, demoting/qualifying the L1000 supportive claim, correcting the FIS1 and MR Abstract wording, adding the label-independence caveat to the headline, and supplying or de-listing the missing MR plots. I therefore recommend **Major revision** rather than Minor, because the DCA, L1000, and FIS1 items affect the credibility of the paper's stated contributions and should not pass as-is.
