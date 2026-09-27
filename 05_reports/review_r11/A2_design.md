# A2 — Design & Statistical Validity review (independent, first-submission basis)

**Manuscript:** "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and validates a 30-gene sepsis prognostic signature" (Scientific Reports, computational-biology / methods-and-resources).
**Reviewer role:** design / methods — biostatistics, causal inference, Mendelian randomisation.
**Remit:** I verified the MR multiple-testing readout, the Egger t-distribution correction, the CD74 critical-care standard-error ordering, the external calibration, the prognostic-signature evidence, and the LINCS L1000 rescue metric directly from the deposited CSVs. Recomputed values are reported under each item.

---

## 1. MR sample overlap is flagged but not corrected — "hypothesis-generating only" is not a statistical correction

【Problem】 The exposure–outcome overlap (eQTLGen discovery sample includes UK Biobank participants; UK Biobank sepsis GWAS is the outcome) is identified as a limitation but is never corrected (no `mrSampleOverlap` / overlap bias estimator). Calling the layer "hypothesis-generating only" is a framing, not a bias correction, and does not protect the single test that crosses the family threshold.

【Evidence】 Manuscript §2.10, §3.10 and §5 limitation 2 state the overlap is "flagged as a limitation" and "interpreted only as hypothesis-generating." The one result that survives the pre-specified 45-test family Benjamini–Hochberg correction is the CD74 critical-care **weighted median**, family *q* = 2.99×10⁻¹⁷ (`10_mr_bh_family.csv` row 17). Burgess, Davies & Thompson, *Genet Epidemiol.* 2016 (ref. [31]) show that overlap (i) pulls the MR estimate toward the confounded observational association and (ii) biases the empirical standard error **downward**, inflating type-I error. The downward-biased SE is exactly what manufactures the tiny *p* = 6.65×10⁻¹⁹ (see Item 2), so the test that "survives" correction is the one most contaminated by the uncorrected overlap.

【Why it matters】 The headline "only one of 45 retains family *q*<0.05" (§3.10, §5) is presented as the MR layer's chief positive signal, yet that *q* is computed from an overlap-biased *p*. "Hypothesis-generating only" does not reverse a downward-biased SE on the very test that crosses threshold; the claim of one surviving signal is therefore unreliable, not merely cautious.

【Specific fix】 Apply the overlap-correction of Burgess, *Int. J. Epidemiol.* 2020 (`mrSampleOverlap` / `mr_ivw_multiple`) and report the overlap-corrected SEs and *q*-values; if the overlap fraction is unknown, state explicitly: "All *q*-values in `10_mr_bh_family.csv` are computed from overlap-biased *p*-values; the single family-significant result (CD74 critical-care weighted median, *q* = 3×10⁻¹⁷) may not survive overlap correction and must not be read as evidence for CD74-directed therapy." Remove any implication that "hypothesis-generating" neutralises the overlap-induced inflation of the one crossing-threshold result.

---

## 2. Benjamini–Hochberg family readout — arithmetic confirmed (exactly 1 of 45), but the survivor is mis-described

【Problem】 The count "45 tests = 5 assessable genes × 3 estimators × 3 outcomes; FCGR3A excluded" and the claim "only one of 45 retains family *q*<0.05 (CD74 critical-care weighted median, *q*≈3×10⁻¹⁷)" are **arithmetically correct**, but the manuscript's accompanying wording ("after correcting the MR-Egger p-values to the t(n−2) distribution, only one of 45 …") misattributes the survival to the Egger correction.

【Evidence】 Recomputing the BH procedure from the 45 *p*-values in `10_mr_bh_family.csv` (standard step-up BH with monotonicity enforcement, *m* = 45): exactly **one** test has *q*<0.05 — CD74 / Weighted median / `4982_critcare`, *p* = 6.6486×10⁻¹⁹, *q* = *p*·45/1 = 2.9919×10⁻¹⁷ (CSV `q_family_45test` = 2.991873×10⁻¹⁷, match). The next smallest family *q* is CD74 IVW critical-care at 0.316 — far above 0.05. The 15-test per-outcome BH for `5086_28ddeath` recomputes to a minimum *q* = 0.487 (CD14 Egger; CSV 0.48697, match). **However**, the surviving test is the *weighted median*, not an Egger; the weighted-median *p* is a normal-approximation value (see Item 4), and the BH simultaneously covers the 15 IVW and 15 weighted-median *p*-values, which were **not** t-corrected. The phrase "after correcting the MR-Egger p-values" therefore over-states what the correction did.

【Why it matters】 A reader infers that the t-correction of Egger *p*-values is what lets one test survive; in fact the lone survivor is a weighted-median, normal-approximated *p* on three SNPs, and the Egger correction (Item 3) is incidental to it. The claim is true but its evidentiary weight is overstated, compounding Item 1.

【Specific fix】 Rephrase §3.10 / §5 limitation 2 from "after correcting the MR-Egger p-values to the t(n−2) distribution, only one of the 45 tests retains family *q*<0.05" to: "after Benjamini–Hochberg correction over the 45 tests, only the CD74 critical-care **weighted median** (normal-approximated *p* = 6.6×10⁻¹⁹, family *q* = 3×10⁻¹⁷) crosses *q*<0.05; the MR-Egger *p*-values were additionally t(n−2)-distributed, but no Egger test survives. This *q* remains overlap-biased (see limitation 2)."

---

## 3. CD14 28-day-death MR-Egger *p* is correctly t-distributed (spot check passed)

【Problem】 (Verification — manuscript claim **holds**.) The manuscript states Egger *p*-values were corrected to the t(n−2) distribution; I spot-checked CD14 28-day-death MR-Egger P = 4.9×10⁻².

【Evidence】 `10_genetics_mr_outcome5086_28ddeath.csv` row 9: CD14 MR-Egger β = −0.0987704, SE = 0.0352746, *n* = 6 SNPs → t = −2.800, df = *n*−2 = 4. Two-sided **normal** *p* = 5.11×10⁻³; two-sided **t(4)** *p* = 4.88×10⁻². The deposited value is 4.8809×10⁻² — it matches the **t(4)** value, not the normal-approximation value. The correction is implemented correctly.

【Why it matters】 This is a genuine strength: the Egger *p* is not a normal-approximation artefact (which would have read ~0.010 and over-stated significance). The residual caveat is that the Egger SE itself remains overlap-biased (Item 1), and the Egger is not the test that survives the family correction (Item 2), so the t-correction does not rescue the MR layer's inferential status.

【Specific fix】 No change required for this *p*; retain the t-distribution correction and consider adding it to IVW/weighted-median *p*-values as well for consistency (IVW with *k* instruments has df = *k*−1; weighted median has no standard df and should be flagged as normal-approximated).

---

## 4. CD74 critical-care MR-Egger SE (0.111) < IVW SE (0.325) is NOT "physically implausible"

【Problem】 The manuscript calls the ordering "a physically implausible ordering that further cautions against over-reading the Egger point estimate." This characterisation is incorrect; the ordering is mathematically routine for MR-Egger vs IVW.

【Evidence】 Reconstructing both SEs from `10_genetics_mr_outcome4982_harmonised.csv` (the 3 retained CD74 SNPs, rs2305480 / rs4810485 / rs12478601):
- IVW SE = 1/√(Σ β_e²/se_o²) = 1/√(9.471) = **0.32496** (CSV `se` = 0.324961, exact match).
- MR-Egger slope SE (weighted regression of β_o on β_e) = **0.11107** (CSV `se` = 0.111074, exact match).
IVW SE² = 1/Σw_i (w_i = β_e²/se_o²); Egger SE² = σ²/Σw_i(x_i−x̄)². Egger SE < IVW SE whenever the exposure effects are sufficiently spread, i.e. Σw_i(x_i−x̄)² > σ²·Σw_i. Here Σw_i(x_i−x̄)² = 8.33 > σ²·Σw_i ≈ 0.97, so the ordering is expected, not anomalous.

【Why it matters】 The real weaknesses are different and should be stated instead: (i) with *n* = 3 SNPs the Egger regression has df = *n*−2 = **1** — its SE is estimated from a single residual degree of freedom and is unstable; (ii) the Egger slope (0.798) ≈ IVW slope (0.798) with a null intercept (*P* = 1.00), so the Egger adds **no independent information** beyond IVW. The "implausible ordering" language misdirects the reader from the actual 1-df fragility and the overlap-biased SE, and over-states the manuscript's own scepticism.

【Specific fix】 Replace "the CD74 critical-care MR-Egger standard error (0.111) is additionally smaller than its own IVW standard error (0.325) on the same three SNPs — a physically implausible ordering that further cautions against over-reading the Egger point estimate (with only three instruments the Egger regression has df = 1 and essentially no power to detect pleiotropy or yield a stable SE)" with: "the CD74 critical-care MR-Egger regression has df = *n*−2 = 1, so its standard error (0.111) is estimated from a single residual degree of freedom and is unstable; the Egger slope (0.798) equals the IVW slope (0.798) with a null intercept (*P* = 1.00), so the Egger contributes no independent information beyond IVW, and both SEs remain biased downward by the exposure–outcome overlap."

---

## 5. Calibration slope 0.50 / intercept −0.04: "risk ranker" relabel is defensible for AUC but the decision-curve analysis is not

【Problem】 Re-labelling the external score a "risk ranker" because calibration slope = 0.50 is defensible for the AUC, but the manuscript then presents decision-curve-analysis (DCA) net benefit as supportive clinical utility — and DCA requires calibrated probabilities.

【Evidence】 `09_ext_calibration_dca.csv`: calib_slope = 0.5028 (ideal 1.0), calib_intercept = −0.0382 (manuscript rounds to 0.50 / −0.04, match). AUC is a pure rank statistic, so a miscalibrated model still discriminates; the external AUC 0.638 is unaffected by the slope and the "ranker" relabel is acceptable for that metric. However, §3.5 also reports "decision-curve analysis showed positive net benefit across the 0.10–0.75 threshold range" (Fig. S06, `09_ext_dca_grid.csv`). Net benefit at a stated risk threshold is computed from the **predicted probabilities**; with slope 0.50 those probabilities are shrunk toward 0.5 and are miscalibrated, so the DCA net-benefit curve is built on biased risk estimates. One cannot simultaneously claim "it is only a ranker (no calibration)" and use DCA net benefit as evidence of clinical utility. Additionally, the slope is estimated from only 52 events, so its CI is wide (plausibly ~0.1–0.9); asserting "over-confident predicted probabilities" from a noisy point estimate is strong.

【Why it matters】 The DCA "positive net benefit" is an overstatement if the probabilities feeding it are uncalibrated; readers may infer clinical decision utility that the data do not support. The honest claim is discrimination-only.

【Specific fix】 Either (a) recalibrate the external score (logistic/Platt calibration using the E-MTAB-4451 predictions) and re-run the DCA on calibrated risks, or (b) drop the DCA net-benefit utility claim and state the score is discrimination-only. In all cases report a bootstrap CI for the calibration slope (not just the point estimate), e.g.: "The calibration slope was 0.50 (95% bootstrap CI 0.10–0.90, *n* = 52 events), so predicted probabilities are not reliable and the score is presented as a risk ranker; decision-curve net benefit is reported on calibrated probabilities only."

---

## 6. Prognostic signature: EPV, "comparable not superior", and the bootstrap CI

【Problem】 Events-per-variable in the discovery L1 fit is 114/30 ≈ 3.8 (well below the ≥10 rule); the external "comparable not superior" claim to the IRG benchmark (0.604) is tenable but rests on a benchmark with no CI and no paired test; the 2000-bootstrap external CI is conditional on the fixed selected gene set and does not capture selection uncertainty.

【Evidence】 `09_external_validation.csv`: orientedSum AUC = 0.6382, 95% CI 0.5317–0.7475; *n* = 106, deaths = 52; `S06_auc_compare.csv` CV AUC = 0.6586 (training 0.7495). IRG benchmark on the same cohort = 0.604 (no CI reported). 0.604 lies inside [0.532, 0.748], so "comparable rather than superior" is tenable. Discovery EPV = 114/30 = 3.8 (manuscript §3.4/§5 acknowledges this). The external bootstrap CI is valid **conditional on the chosen 30-gene set**; because gene selection and orientation used the GSE65682 28-day labels, the CI does not reflect gene-selection variability, so it understates total uncertainty (acceptable only if stated).

【Why it matters】 The honest external AUC (0.638) is the right primary number and the manuscript scopes it well. Two gaps remain: (i) without a CI on IRG and a paired test, "comparable not superior" is descriptive, not tested; (ii) the selection-conditional CI can be read as a full uncertainty statement when it is not.

【Specific fix】 Add a DeLong paired comparison of the signature vs IRG AUCs on the 106 E-MTAB-4451 samples and report its *p*-value; and add the sentence: "The 2,000-bootstrap 95% CI for the external AUC is conditional on the selected 30-gene set and orientation and does not capture uncertainty from the discovery-cohort gene selection; it quantifies uncertainty of this specific signature, not of 'a 30-gene signature selected this way'." State EPV = 3.8 explicitly in §3.4.

---

## 7. LINCS L1000 single-direction rescue undermines the repositioning conclusion; dexamethasone is mis-described as "scored high"

【Problem】 The rescue metric aggregates all 22 query genes with the same sign, including the Mars1-**up** exhaustion markers PDCD1 and LAG3. Up-regulating PDCD1/LAG3 (worsening exhaustion) *increases* the rescue score — the opposite of the intended dual-direction reversal — so the metric cannot separate antigen-presentation rescue from exhaustion worsening. Separately, the manuscript states "prednisone and dexamethasone (glucocorticoids) also scored high," but dexamethasone did not.

【Evidence】 §3.9 / §5 limitation 11: rescue = mean rank-percentile of the 22 genes − 0.5, all same sign; the 22-gene set contains PDCD1 and LAG3 (Mars1-up). `S08_l1000_positive_control.csv`: prednisone rescue 0.1364, rank 651/20,413 = **3.2nd percentile** (genuinely high — positive-control logic holds); dexamethasone rescue 0.0315, rank 6,808/20,413 = **33.4th percentile** (below median). The manuscript's "both … scored high" is false for dexamethasone. The two small-molecule candidates rest on this ambiguous proxy: lenalidomide rank 5,435 (top 26.6%), azithromycin rank 9,152 (≈ median) — `S08_l1000_candidate_scores.csv`.

【Why it matters】 Because PDCD1/LAG3 enter with the same sign as the Mars1-down antigen-presentation genes, a compound that worsens T-cell exhaustion can score as a "rescuer," and the glucocorticoid caveat (prednisone high) already shows the metric is non-specific. The repositioning ranking of lenalidomide/azithromycin is therefore "directional-but-ambiguous," weaker than "directional-but-modest rescue of the Mars1-down axis." The dexamethasone misstatement further weakens the positive-control caveat.

【Specific fix】 Recompute rescue as a **dual-direction** score: Mars1-down genes contribute +signed percentile, Mars1-up genes (PDCD1, LAG3) contribute −signed percentile, and re-rank the candidates on the corrected score. Correct the statement to: "prednisone scored high (rank 651/20,413, 3.2nd percentile); dexamethasone was below median (rank 6,808/20,413, 33.4th percentile)." Retain the single-direction result as a sensitivity analysis only.

---

## § Stands up (what is sound)

1. **The MR-Egger t(n−2) correction is real and correctly applied** — verified for CD14 28-day-death (t(4) *p* = 4.88×10⁻² matches the deposited value; normal-approx would have been 5.11×10⁻³).
2. **The 45-test BH arithmetic is correct** — I recomputed it from `10_mr_bh_family.csv` and exactly one test (CD74 critical-care weighted median) crosses *q*<0.05, at *q* = 2.99×10⁻¹⁷, matching the manuscript.
3. **The external validation is genuinely independent and honest** — different platform (Illumina GPL10558 vs Affymetrix GPL13667), different population (UK CAP sepsis), locked model with no retuning, AUC 0.638 (95% CI 0.532–0.748) reported as the primary honest estimate rather than the optimistic CV AUC 0.659.
4. **The CD74 IVW and Egger SEs reconstruct exactly** from the harmonised instruments (IVW SE 0.32496, Egger SE 0.11107), confirming the deposited MR outputs are internally consistent.
5. **Unusual transparency about limitations** — selection-chain FWER, outcome-driven MR gene selection, single-direction L1000, and the overlap flag are all disclosed rather than hidden; the manuscript scopes its claims appropriately in most places.

---

## § Questions for the authors

1. What is the estimated eQTLGen ∩ UK Biobank overlap fraction, and have you run `mrSampleOverlap`? Without it, can the *q* = 3×10⁻¹⁷ for CD74 critical-care weighted median be defended as anything other than an overlap artefact?
2. FCGR3A was dropped at 2 instruments, yet CD74 is retained on critical care with 3 instruments. Is a 3-instrument minimum applied consistently, and is the CD74 critical-care result intended as any evidence or purely as a genotype–severity correlate?
3. Can you provide a DeLong paired test of signature vs IRG on E-MTAB-4451 (same 106 samples), and a bootstrap CI for the calibration slope (52 events)?
4. Will you recompute the LINCS rescue as dual-direction (PDCD1/LAG3 reverse-signed) and re-rank lenalidomide/azithromycin before the repositioning claim stands?
5. The weighted-median *p* = 6.6×10⁻¹⁹ is normal-approximated with no df; do you agree it should be flagged as normal-approx (not t-corrected) so readers do not assume the same rigour as the Egger correction?

---

## § What I actually checked

**Files read (deposited CSVs only; no review/response/revision files consulted):**
- `05_reports/manuscript.md` (full)
- `03_results/10_mr_bh_family.csv` (45 rows: gene, method, outcome, *p*, per-outcome 15-test BH, family 45-test BH, significance flag)
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv` and `…_harmonised.csv` (CD14 Egger β/SE, 6 SNPs)
- `03_results/10_genetics_mr_outcome4982_criticalcare.csv` and `…_harmonised.csv` (CD74 IVW/Egger/weighted-median β/SE; 3 SNPs)
- `03_results/09_ext_calibration_dca.csv` (slope 0.5028, intercept −0.0382)
- `03_results/09_external_validation.csv` (orientedSum AUC 0.6382, CI 0.5317–0.7475, *n*=106, deaths=52)
- `03_results/S06_auc_compare.csv` (CV AUC 0.6586, train 0.7495)
- `03_results/S08_l1000_candidate_scores.csv`, `S08_l1000_positive_control.csv` (lenalidomide/azithromycin/prednisone/dexamethasone ranks)

**Recomputed values:**
- BH family (45 tests, step-up with monotonicity): 1 significant — CD74/Weighted median/`4982_critcare`, *p* = 6.6486×10⁻¹⁹, *q* = 2.9919×10⁻¹⁷ (CSV 2.991873×10⁻¹⁷, match). Next smallest *q* = 0.316 (CD74 IVW critcare).
- Per-outcome 15-test BH for `5086_28ddeath`: minimum *q* = 0.487 (CD14 Egger; CSV 0.48697, match).
- CD14 Egger 28ddeath: t = −2.800, df = 4; normal two-sided *p* = 5.11×10⁻³; t(4) two-sided *p* = 4.88×10⁻² (CSV 4.8809×10⁻², match → correctly t-distributed).
- CD74 critcare IVW SE = 1/√(Σβ_e²/se_o²) = 0.32496 (CSV 0.324961, match); Egger slope SE (weighted β_o~β_e) = 0.11107 (CSV 0.111074, match). Egger SE < IVW SE is mathematically routine given spread of exposure effects.
- CD74 critcare weighted median: β = 0.7859, SE = 0.0885, t = 8.88, normal two-sided *p* ≈ 6.6×10⁻¹⁹ (CSV 6.6486×10⁻¹⁹, match → normal-approximated, not t-corrected).
- Calibration: slope 0.5028 / intercept −0.0382 (manuscript 0.50 / −0.04, match).
- L1000: prednisone rank 651/20,413 = 3.2nd pct (high); dexamethasone rank 6,808/20,413 = 33.4th pct (**below median**, contradicting "scored high"); lenalidomide 5,435 (26.6th pct), azithromycin 9,152 (median).

**Discrepancies / corrections required:**
- (a) Dexamethasone is described as "scored high" but is at the 33.4th percentile — false.
- (b) "CD74 critical-care MR-Egger SE < IVW SE is physically implausible" is incorrect; it reconstructs as a routine MR-Egger property. The true caveat is df = 1 and null Egger intercept.
- (c) "after correcting the MR-Egger p-values … only one of 45" misattributes the surviving test to the Egger correction; the survivor is the weighted median (normal-approx), not an Egger.
- (d) The single family-significant *q* = 3×10⁻¹⁷ is computed from an overlap-biased *p* and is not neutralised by the "hypothesis-generating" framing (Items 1–2).
