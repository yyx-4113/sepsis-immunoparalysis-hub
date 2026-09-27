# Round-15 Independent Blind Review — Statistics / Causal-Inference / Epidemiology Design

**Manuscript:** `05_reports/manuscript.md` (tag v1.15.0)
**Focus:** statistical and causal-inference design correctness; every headline number recomputed from the deposited CSVs.
**Reviewer stance:** first submission, no prior-round knowledge. No forbidden files were opened.

---

## Issues

### Issue 1 — Calibration-slope description mislabels the direction of miscalibration (genuine, minor)
【Problem】 The external score is described as having "an **under-fitting** slope of 0.50 (ideal = 1.0), indicating over-confident predicted probabilities." The adjective "under-fitting" is the wrong term for a calibration slope < 1.

【Evidence】 `03_results/09_ext_calibration_dca.csv`: `calib_slope = 0.5028`, `calib_intercept = −0.0382`. Manuscript §3.5 (line 112) writes "under-fitting slope of 0.50 … indicating over-confident predicted probabilities." The same sentence pairs a term implying too little model (under-fitting) with the correct consequence (over-confident). In prediction-model calibration (Steyerberg *Clinical Prediction Models*, 2nd ed.; Van Calster et al., *Ann Intern Med* 2019), a slope **< 1** is the signature of **over-confident / too-extreme predictions** (classically an over-fit-to-development or poorly transported model), not under-fitting. With AUC 0.638 the discrimination is fine, which is precisely why "under-fitting" is incorrect — under-fitting would also damage discrimination.

【Why it matters】 A slope of 0.5 with adequate AUC means the model *ranks* well but its predicted probabilities are too spread out. Calling it "under-fitting" could mislead a clinical reader into thinking the model lacks signal, contrary to the actual finding, and undermines the otherwise careful calibration language in the same paragraph.

【Specific fix】 Replace "an under-fitting slope of 0.50" with "a calibration **slope of 0.50 (over-fit / over-confident: predictions too extreme), intercept −0.04**". Keep "over-confident predicted probabilities" — that part is correct.

---

### Issue 2 — Abstract's "honest external, cross-platform" headline omits the label-dependence that the body discloses (minor, framing)
【Problem】 The Abstract presents "an honest external, cross-platform AUC of 0.638" without noting that the signature *orientation* was locked on GSE65682's own 28-day labels, so the external test is cross-cohort and cross-platform but **not** label-blind.

【Evidence】 `02_scripts/python/09_external_validation.py` (locked orientation from training-set correlation with death) and manuscript §2.9 / §3.5 / Limitation 1: "The fixed orientation was trained on GSE65682 28-day labels, so the external application is independent in cohort and platform but not in label." The Abstract (line 14) states only "honest external, cross-platform AUC of 0.638" and repeats "honest external validation" in the Conclusion (line 218) without the qualifier.

【Why it matters】 Not a hidden flaw — the body is explicit and honest — but the single-word "honest" in the Abstract over-states independence relative to the disclosed design. A reader who only scans the Abstract could take the 0.638 as a fully independent estimate, when part of the model (orientation) was fit to the discovery labels. The L1-locked external AUC (0.585) already signals orientation matters, which the manuscript reports; the framing should match.

【Specific fix】 In the Abstract, change "honest external, cross-platform AUC of 0.638" to "honest external, cross-platform AUC of 0.638 (orientation locked on discovery labels, so cross-cohort/cross-platform but not label-independent)". One sentence, no structural change.

---

### Issue 3 — DCA thresholds rest on a calibration slope estimated in-sample on the 106-sample validation set, with no CI (low severity, transparency gap)
【Problem】 The DCA is computed on "calibration-corrected probabilities from the external logistic fit (intercept −0.04, slope 0.50)"; both the slope/intercept and the DCA are derived from the *same* 106-patient / 52-event external cohort, so the DCA threshold locations inherit the slope estimate's sampling uncertainty, which is nowhere given.

【Evidence】 `02_scripts/python/_ext_calibration_dca.py` lines 29–32 fit `a, b` on the external `z, y` and lines 66–70 compute NB from `p = 1/(1+exp(−(a+b·z)))`. `09_ext_calibration_dca.csv` reports slope/intercept with no CI. The grid (`09_ext_dca_grid.csv`) shows model NB first exceeds treat-all at threshold 0.30 by only 0.0122 (0.2844 vs 0.2722), and the "exceeds treat-all from ≈0.30" claim is sensitive to that single estimated slope.

【Why it matters】 The qualitative DCA conclusion (model beats treat-all across the mid-threshold range, and at 0.80 sits at treat-none level while treat-all is deeply negative) is robust and correctly stated. But the *precise* threshold at which the model first diverges (≈0.30) is a soft number: with 52 events the slope 0.50 has a wide CI, so the exact crossing point is uncertain. This does not invalidate the DCA, but the manuscript presents the 0.30 crossing as if established.

【Specific fix】 Add one sentence in §3.5 after the DCA description: "The calibration slope/intercept (and hence the DCA threshold locations) were estimated in-sample on the 106-patient validation set and carry wide uncertainty (no CI shown); the model-vs-treat-all divergence threshold (≈0.30) is therefore illustrative, while the qualitative net-benefit advantage is robust." This is consistent with the existing "ranker not a probability" framing.

---

## § Stands up (verified by recomputation)

1. **External AUC 0.638 and CI 0.532–0.748, n=106, 52 deaths.** `09_external_validation.csv`: `auc_EMTAB4451_orientedSum = 0.6382`, `CI95_low = 0.5317`, `CI95_high = 0.7475`, `n_validated_samples = 106`, `n_deaths = 52`. Locked-L1 external `0.5848` → 0.585 (CI 0.469–0.696) ✓; IRG-3 proxy `0.5288` → 0.529 ✓; GSE65682 CV locked `0.6582` → 0.659 ✓. All match the manuscript to rounding.

2. **DCA grid is internally consistent with the prose, and DCA uses calibration-corrected probabilities (per deposited code).** `09_ext_dca_grid.csv`: model NB equals treat-all NB at 0.05–0.25 (0.4638/0.434/0.4007/0.3632/0.3208) and first *exceeds* treat-all at 0.30 (0.2844 vs 0.2722); at 0.80 model NB = 0.0000 while treat-all = −1.5472 (the diverging pair the brief specified). `_ext_calibration_dca.py` lines 31–32 and 67 confirm DCA is run on `p = 1/(1+exp(−(a+b·z)))` with the fitted intercept/slope — i.e., calibration-corrected, exactly as claimed. Model NB is positive across 0.10–0.75 (0.434 → 0.0094), matching "positive net benefit over treat-none" ✓.

3. **Mars1 vs Mars2/3/4 Mann–Whitney P = 0.47 / 1.9e-18 / 1.3e-3.** Recomputed from `S02_immunoparalysis_score.csv` (scipy `mannwhitneyu`, two-sided): Mars2 P = 0.467 (→0.47), Mars3 P = 1.85e-18 (→1.9e-18), Mars4 P = 1.32e-3 (→1.3e-3). Medians recomputed: Mars1 −0.792, Mars2 −0.752, Mars3 0.64, Mars4 −0.235 — all match Table in §3.2.

4. **MR primary 28-day-death IVW OR 0.92–1.12, min P ≥ 0.23.** `10_genetics_mr_outcome5086_28ddeath.csv`: CD74 1.119 (P 0.718), HLA-DQA1 0.923 (P 0.260), CD14 0.927 (P 0.236), HAVCR2 0.978 (P 0.847), FIS1 0.963 (P 0.473). All OR within 0.92–1.12, minimum P = 0.236 ≥ 0.23 ✓. CD14 MR-Egger P = 0.0488 (→4.9e-2), family q = 0.730 ✓.

5. **45-test BH family = 5 × 3 × 3 = 45; 27 instruments.** `10_mr_bh_family.csv` contains exactly 45 test rows (5 assessable genes × 3 estimators × 3 outcomes; FCGR3A excluded). Instrument counts sum to 27: CD74 3 + HLA-DQA1 4 + CD14 6 + HAVCR2 6 + FIS1 8 (`*_28ddeath.csv` `nsnp` column) ✓. BH correctly applied (smallest p, CD74 crit-care WM 6.65e-19, gives q = 6.65e-19·45/1 = 3.0e-17, matching the file).

6. **CD74 critical-care signal is reversed and overlap-flagged, not over-claimed.** `10_genetics_mr_outcome4982_criticalcare.csv`: CD74 WM OR 2.194 (P 6.65e-19, family q 3e-17), IVW OR 2.222 (1.175–4.200, P 0.014), Egger OR 2.222 (P 0.088, intercept P 1.00). All point the *opposite* direction to the Mars1 model; manuscript §3.10 and Limitation 2 repeatedly call it "reversed / overlap-inflated / genotype–severity association rather than causal hub claim." Correctly handled.

7. **Exposure–outcome sample overlap acknowledged with the correct bias direction.** §2.10, §3.10, Limitation 2 state eQTLGen includes UK Biobank participants → overlap; and that overlap biases SEs *downward*, inflating Type-I error ("the true association may be weaker or null"). That is the correct Burgess–Davies–Thompson (2016) consequence; no sample-overlap correction was applied and the results are framed hypothesis-generating. Appropriate.

8. **MR family correction is framed on overlapping hypothesis structure, NOT on shared chromosome/LD.** Limitation 2 explicitly states the 45 tests are correlated because "same gene × multiple estimators/outcomes," and calls the independence assumption "a conservative approximation rather than a strict independence guarantee." No claim is made that CD74 (chr5q32) and HLA-DQA1 (chr6p21.32) share LD; the correction is correctly grounded in hypothesis overlap, so no false LD assertion exists.

9. **Susceptibility null and CD74-susceptibility pleiotropy caveat both verified.** `10_genetics_mr.csv` IVW P (susceptibility): CD74 0.526, HLA-DQA1 0.404, CD14 0.764, HAVCR2 0.249, FIS1 0.433 → "all IVW P ≥ 0.249" ✓. CD74 susceptibility MR-Egger intercept P = 9.98e-5 (→1.0e-4), confirming the manuscript's "significantly non-zero intercept … horizontal pleiotropy" statement (§3.10). 

10. **L1000 candidate ranks verified.** `S08_l1000_candidate_scores.csv`: lenalidomide rescue_rank 5435 (5435/20413 = top 26.6%) ✓; azithromycin rescue_rank 9152 (9152/20413 = 44.8th pct, "≈ median") ✓. Glucocorticoid positive-control caveat (prednisone high, dexamethasone low) honestly noted as showing the rescue proxy is not a validated functional marker (§3.9) — a sound negative-control-style check.

---

## § Questions for the authors

1. In the DCA grid, model NB is *exactly equal* to treat-all NB at thresholds 0.05–0.25 (to 4 d.p.). This implies all 106 calibrated probabilities exceed 0.25, i.e., the model treats effectively everyone in that band. Is that the intended behaviour, or does it reflect the calibration transform compressing the score so that low-risk Mars1 patients still receive p > 0.25? Either way it is consistent, but worth a confirmation sentence.

2. The 45-test family pools the phenotype-matched primary outcome (28-day death) with two non-primary outcomes (susceptibility, critical care). This is conservative (more nulls → stricter), and the one survivor (CD74 critical-care, reversed) is correctly demoted. Was the pooling pre-specified *before* seeing that CD74 critical-care is the only survivor, or chosen post-hoc? If pre-specified (as stated), it is fully defensible; a one-line methods note on pre-specification would pre-empt the question.

3. FCGR3A was excluded for only 2 usable instruments even after relaxing P and disabling clumping. Could a broader cis-window or a different eQTL source (e.g., a larger whole-blood eQTL) recover ≥3 instruments for a sixth gene, or is the exclusion accepted as definitive? Minor, since the manuscript already reports the re-query attempt.

---

## § What I actually checked

**Files read (directly, no forbidden files):**
- `05_reports/manuscript.md` (full).
- `03_results/09_external_validation.csv`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`.
- `03_results/S02_immunoparalysis_score.csv`, `10_mr_bh_family.csv`, `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr.csv` (susceptibility), `10_genetics_mr_outcome4982_criticalcare.csv`, `S08_l1000_candidate_scores.csv`.
- `02_scripts/python/_ext_calibration_dca.py` (to confirm DCA input probabilities).

**Computations run (equivalents):**
- Mann–Whitney U (two-sided) Mars1 vs Mars2/3/4 on `S02_immunoparalysis_score.csv` immune-function score → P = 0.467 / 1.85e-18 / 1.32e-3; medians −0.792 / −0.752 / 0.64 / −0.235.
- Verified AUC/CI/n/deaths against `09_external_validation.csv` (0.6382/0.5317–0.7475/106/52; locked-L1 0.5848; IRG3 0.5288; CV 0.6582).
- Verified DCA grid crossing points (model = treat-all at 0.05–0.25; first exceeds at 0.30 by 0.0122; at 0.80 model 0.0000 vs treat-all −1.5472) and that `_ext_calibration_dca.py` computes NB from the calibration-corrected `p`.
- Verified all 5 primary-IVW OR/P from `*_28ddeath.csv` (OR 0.92–1.12, min P 0.236); CD14 Egger P 0.0488, family q 0.730.
- Counted BH-family rows (45) and instruments (3+4+6+6+8 = 27); confirmed BH q for the smallest p = 6.65e-19 × 45 = 3.0e-17.
- Verified susceptibility IVW min P 0.249 and CD74 susceptibility Egger intercept P 9.98e-5.
- Verified L1000 ranks 5435 / 9152 and percentages.

**Recomputed values vs manuscript — discrepancies:**
- Only the calibration-slope *terminology* is wrong ("under-fitting" should be "over-fit / over-confident"); the numeric value 0.50 and the "over-confident" consequence are correct. No numeric discrepancy found in any audited claim.
- Two minor framing gaps: (a) Abstract omits the label-trained orientation qualifier that the body discloses; (b) DCA threshold locations are presented as established despite the slope being estimated in-sample with no CI.

---

## VERDICT: **Minor** — the statistical and causal-inference design is sound and honestly hedged; only one genuine (terminology) error and two low-severity framing gaps need fixing before acceptance.
