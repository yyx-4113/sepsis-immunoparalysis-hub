# Reviewer B2 — Design / Statistics / Causal Inference

**Manuscript:** `05_reports/manuscript.md` (v1.18.0) · **Journal:** Scientific Reports
**Treated as:** first submission. No prior review round, checklist, or memory file was consulted.
**Scope of my review:** external-validation leakage structure, calibration and decision-curve analysis, multiplicity and dependence in the MR family, MR interpretation and overlap bias, L1000 connectivity evidence, and statistical over-reading / internal contradiction.

---

## MAJOR ITEMS

### B2-1. The single "family-significant" MR result — quoted in the Abstract — is arithmetically impossible as reported

【Problem】
The CD74 critical-care weighted-median estimate (OR 2.194, *P* = 6.6×10⁻¹⁷…10⁻¹⁹, family *q* ≈ 3×10⁻¹⁷) cannot be produced by three individually non-significant instruments, and its standard error is smaller than the IVW standard error computed from the same three variants — which is impossible for a median-type estimator.

【Evidence】
From `03_results/10_genetics_mr_outcome4982_harmonised.csv` (rows 2–4) I recomputed each CD74 instrument's own ratio estimate β_out/β_exp and its SE (SE = se_out/|β_exp|):

| rsid | β_exp | β_out | ratio | SE | z | two-sided P |
|---|---|---|---|---|---|---|
| rs2305480 | −0.07345 | −0.05016 | 0.6830 | 0.5348 | 1.28 | 0.202 |
| rs4810485 | −0.08132 | −0.07572 | 0.9312 | 0.5608 | 1.66 | 0.097 |
| rs12478601 | 0.06661 | 0.05271 | 0.7913 | 0.5983 | 1.32 | 0.186 |

My IVW recomputation from these three variants gives β = 0.7983, SE = 0.3250 — an exact match to the deposited `10_genetics_mr_outcome4982_criticalcare.csv` (β = 0.79828, SE = 0.32496), so my reconstruction of the pipeline is correct.

The weighted median reported in the same file is β = 0.78589 with **SE = 0.08849**, i.e. **0.272 × the IVW SE from the same three SNPs**. Three independent contradictions follow:

1. **No instrument is even nominally significant** (minimum single-SNP P = 0.097). Three estimates of 0.68, 0.93 and 0.79 with individual SEs of 0.53–0.60 cannot jointly identify an effect to 17 decimal places.
2. **A median estimator is asymptotically *less* efficient than the mean**, not 13× more precise. Under homogeneous instruments the weighted-median SE should be ≈1.2–1.3 × the IVW SE (≈0.39–0.42), or ≈0.53–0.60 if anchored on the median variant's own uncertainty. Either way the honest P is 0.06–0.19, not 6.6×10⁻¹⁹.
3. **It contradicts the paper's own power calculation.** `05_reports/manuscript.md:60` states the minimum detectable OR for CD74 (3 instruments) is ≈2.12. Using the deposited IVW SE of 0.3250, the MDE at 80 % power / two-sided α = 0.05 is exp(2.8016 × 0.3250) = **OR 2.49**. The reported OR is 2.19–2.22 — at or *below* the detection threshold. A design with <80 % power for this effect size cannot yield *P* = 6.6×10⁻¹⁹.

Root cause is visible in the Methods: `manuscript.md:60` specifies "the weighted median (SE by 2,000 bootstrap resamples)". Bootstrapping **three** instruments is degenerate — the bootstrap distribution of a median of three points is concentrated on the three observed values and grossly under-estimates dispersion. The manuscript applies exactly this scrutiny to the MR-Egger SE (0.111 vs IVW 0.325) at `manuscript.md:174`, but never to the weighted-median SE (0.0885 vs IVW 0.325), which is *more* extreme and is the one that drives the headline.

【Why it matters】
This is the **only** family-significant result in the entire 45-test MR layer and it is quoted in the Abstract (`manuscript.md:14`: "the single family-significant result (CD74 critical care, OR 2.19)"). A *P*-value wrong by ~17 orders of magnitude, published in a Nature-family journal, is a retraction-grade computational error if left standing, and it will be the first thing any competent statistical reviewer recomputes. It also invalidates the "one test survives correction" narrative in §3.10 (`:176`), §4 (`:186`) and Limitation 2 (`:195`), and the `family_sig_q<0.05 = YES` flag in `10_mr_bh_family.csv:17`.

【Specific fix】
Delete the weighted-median *P*/q for every gene with <10 instruments and replace with the IVW-based inference. Paste-ready replacement for `manuscript.md:162`:

> Against **critical care**, CD74 gave OR ≈ 2.2 in all three estimators (IVW OR 2.222, 95 % CI 1.175–4.200, *P* = 0.014; MR-Egger slope OR 2.222, *P* = 0.088; weighted median OR 2.194). We do **not** report a *P*-value for the weighted median: with three instruments its bootstrap standard error (0.088) falls below the inverse-variance-weighted standard error computed from the same three variants (0.325), an ordering that is impossible for a median-type estimator, and no individual instrument is nominally significant (*P* = 0.097, 0.186, 0.202). Referred to a t(2) distribution the weighted-median *P* would be 0.012. **No test in the MR layer therefore survives the pre-specified 45-test family correction**, and the CD74 critical-care association is reported as a nominal, reversed-direction observation only.

Paste-ready Abstract replacement (same length, keeps the abstract ≤200 words):

> …one sensitivity test (CD14 MR-Egger, OR 0.91, P = 0.049) was nominally significant and only one further test (CD74 critical care, OR 2.19, P = 0.014) reached nominal significance, running opposite to the expression model; nothing survived family correction.

And in `manuscript.md:176`, `:186`, `:195`, replace "the single family-significant result" / "the only MR association surviving family correction" / "*q* ≈ 3×10⁻¹⁷" with "the only nominally significant critical-care signal (CD74, IVW *P* = 0.014; weighted-median *P* not reported)". Set `family_sig_q<0.05` to `no` for row `10_mr_bh_family.csv:17` and blank the weighted-median `p` and `q_family_45test` cells wherever `nsnp < 10`.

---

### B2-2. The headline transport comparison switches models: the like-for-like external AUC is 0.585, not 0.638

【Problem】
The within-cohort CV AUC (0.659) is produced by the **L1-logistic** model, but the "honest out-of-sample generalization" it is compared against (0.638) is produced by a **different score** (equal-weight oriented sum); the locked L1 model transported to 0.585 with a CI that includes 0.5.

【Evidence】
- `03_results/S06_auc_compare.csv`: "Immune-risk signature (CV)" = 0.65856 — and `09_external_validation.py:96-109` shows this CV figure comes from `LogisticRegression(penalty="l1")`, i.e. the L1 model.
- `03_results/09_external_validation.csv`: `auc_EMTAB4451_external_locked` = 0.5848 (95 % CI 0.4687–0.6959) — the **same** locked L1 model applied to E-MTAB-4451; `auc_EMTAB4451_orientedSum` = 0.6382 (95 % CI 0.5317–0.7475).
- §3.4 (`manuscript.md:109`): "this within-cohort CV estimate (L1 model) is optimistic; the honest out-of-sample generalization is the external equal-weight AUC 0.638 (§3.5)".
- §2.9 (`:55`): "A fixed-orientation equal-weight score was reported as the primary external metric" — stated, but with **no a-priori justification**, and the manuscript never states that the pre-specified model of §2.6 was the L1 model.

Like-for-like transport decay is 0.659 → 0.585 = **−0.074 AUC units**, and the external L1 95 % CI (0.469–0.696) **includes 0.5**. The text's comparison implies a decay of only 0.659 → 0.638 = −0.021, i.e. it understates the loss by 3.7×. Selecting the better-performing of two external metrics as "primary" after the fact, without pre-specification, is selective reporting.

【Why it matters】
This is the paper's central quantitative claim (it is in the title, the Abstract, §3.5, §4 and Limitation 1). If a reader discovers that the pre-specified model's external AUC does not exclude chance, the entire "honest external validation" framing — which is the manuscript's declared contribution — collapses. Scientific Reports reviewers check exactly this.

【Specific fix】
Two paste-ready edits.

In §3.4 (`manuscript.md:109`), replace "the honest out-of-sample generalization is the external equal-weight AUC 0.638 (§3.5)":

> the honest out-of-sample generalization is the external application of the **same locked L1 model**, AUC 0.585 (95 % CI 0.469–0.696), whose interval includes 0.5; a model-free fixed-orientation equal-weight score on the same external cohort gave AUC 0.638 (95 % CI 0.532–0.748) and is reported as the primary external metric because it is free of cohort-specific weights, but the two external metrics differ by 0.053 and the like-for-like transport loss for the L1 model is 0.074 AUC units.

In §2.9 (`manuscript.md:55`), append:

> This choice was made before the external AUC was computed: the equal-weight oriented sum is reported as primary because it carries no cohort-specific weights and is therefore the portable component by construction; the locked-L1 result is reported alongside it and is the like-for-like comparison to the within-cohort CV AUC.

If the choice was in fact made after seeing both numbers, say so explicitly instead — "the equal-weight score is reported as primary because the locked weights did not transport" — which is honest and still publishable.

---

### B2-3. "The model's advantage over treat-all is confined to 0.30–0.75" is false; and the high-threshold margins rest on 1–4 patients

【Problem】
The advantage over treat-all does **not** stop at 0.75 — it is largest at 0.80–0.90 (+1.55, +2.40, +4.09), where the model flags nobody. What is confined to ≤0.75 is the model's *positive* net benefit relative to treat-none, not its advantage over treat-all.

【Evidence】
Recomputed from `03_results/09_ext_risk_scores.csv` (n = 106, 52 deaths, prevalence 0.4906) with the calibration refit exactly as in `_ext_calibration_dca.py` (a = −0.0382, b = 0.5028 — both reproduce the deposited values to 4 dp):

| threshold | flagged | TP | FP | NB model | NB treat-all | margin | NB in `09_ext_dca_grid.csv` |
|---|---|---|---|---|---|---|---|
| 0.30 | 103 | 52 | 51 | 0.2844 | 0.2722 | +0.0121 | ✓ |
| 0.35 | 93 | 49 | 44 | 0.2388 | 0.2163 | +0.0225 | ✓ |
| 0.40 | 77 | 41 | 36 | 0.1604 | 0.1509 | +0.0094 | ✓ |
| 0.45 | 60 | 33 | 27 | 0.1029 | 0.0738 | +0.0292 | ✓ |
| 0.50 | 50 | 29 | 21 | 0.0755 | −0.0189 | +0.0943 | ✓ |
| 0.55 | 37 | 22 | 15 | 0.0346 | −0.1321 | +0.1667 | ✓ |
| 0.60 | 20 | 14 | 6 | 0.0472 | −0.2736 | +0.3208 | ✓ |
| 0.65 | 13 | 10 | 3 | 0.0418 | −0.4555 | +0.4973 | ✓ |
| 0.70 | **4** | 3 | 1 | 0.0063 | −0.6981 | +0.7044 | ✓ |
| 0.75 | **1** | 1 | 0 | 0.0094 | −1.0377 | +1.0472 | ✓ |
| 0.80 | 0 | 0 | 0 | 0.0000 | −1.5472 | **+1.5472** | ✓ |
| 0.85 | 0 | 0 | 0 | 0.0000 | −2.3962 | **+2.3962** | ✓ |
| 0.90 | 0 | 0 | 0 | 0.0000 | −4.0943 | **+4.0943** | ✓ |

The two quoted ranges are themselves **arithmetically correct**: min margin over 0.30–0.50 = 0.0094 → "0.01"; max = 0.0943 → "0.09"; min over 0.55–0.75 = 0.1667 → "0.17"; max = 1.0472 → "1.05". The crossover at ≈0.30 is also correct (model = treat-all exactly at 0.05–0.25, then strictly greater). The defect is the word "confined": the margin keeps growing past 0.75 and exceeds the quoted upper bound of 1.05 at every grid point from 0.80 on.

Additionally, the +1.05 margin at threshold 0.75 is generated by **one patient** (TP = 1, FP = 0), and the +0.70 margin at 0.70 by **four patients**. The manuscript never reports the number of patients driving the high-threshold net benefit.

【Why it matters】
A sentence that is literally false in a deposited, audit-claimed manuscript is worse than no sentence. More substantively, the DCA's apparent "large advantage" at high thresholds is an artefact of two things the reader is not told: (i) treat-all collapses algebraically, and (ii) the model's own contribution at those thresholds comes from 1–4 patients. As written, the passage invites the reading "the model is much better than treat-all at high thresholds", which is the opposite of the intended message.

【Specific fix】
Replace the two sentences at `manuscript.md:112` beginning "and exceeds the treat-all strategy from threshold ≈0.30 onward…":

> Its net benefit was positive relative to treat-none from threshold 0.05 to 0.75 and exceeded treat-all from 0.30 onward; the margin over treat-all was 0.01–0.09 at thresholds 0.30–0.50, 0.17–1.05 at 0.55–0.75 and 1.55–4.09 at 0.80–0.90, but the last range is vacuous because at ≥0.80 no calibration-corrected risk exceeds the threshold (0 of 106 patients flagged) and treat-all collapses algebraically. The margins at the highest thresholds rest on very few patients — 4 flagged at 0.70 and 1 at 0.75 — and are not interpretable.

Also change "showed a positive net benefit over treat-none across the 0.10–0.75 threshold range" to "across the 0.05–0.75 threshold range" (model NB = 0.4638 at 0.05, also positive).

New-analysis spec for `09_ext_dca_grid.csv`: add three columns — `n_flagged`, `TP`, `FP` — so every net-benefit value is auditable against the number of patients that generated it.

---

### B2-4. The calibration slope is reported without a confidence interval, and the CI is decisive

【Problem】
The manuscript states "no bootstrap optimism correction was applied, and with 52 events the slope is itself imprecise" but declines to quantify the imprecision; the CI is trivially computable from the deposited risk scores and materially changes the reading.

【Evidence】
I refit the two-parameter logistic recalibration on the standardized external score (`09_ext_risk_scores.csv`, n = 106, 52 deaths) and obtained the observed-information covariance matrix:

- intercept a = **−0.0382, SE 0.2001, 95 % CI −0.430 to +0.354** (matches −0.04)
- slope b = **0.5028, SE 0.2079, 95 % CI 0.095 to 0.910** (matches 0.50)
- Wald test of slope = 1: z = −2.392, **P = 0.017**

So the data *do* reject ideal calibration (slope = 1) at the 5 % level — the "over-confident" claim is statistically supported, which the reader currently cannot verify — **but** the lower bound of 0.095 means the slope is also compatible with a nearly flat log-odds gradient, i.e. with a score that carries almost no calibrated risk information. Both tails matter and neither is reported.

【Why it matters】
Stating "slope 0.50 (ideal 1.0)" with no interval lets the number read as a moderately-imperfect calibration, when the honest statement is "the slope is significantly below 1 but its CI spans 0.10–0.91, so the degree of over-confidence is essentially unquantified at n = 106." This directly underwrites the paper's decision to present the score as a ranker, and the reader cannot audit that decision.

【Specific fix】
Paste-ready replacement at `manuscript.md:112`:

> Calibration of the external equal-weight score showed a near-zero intercept (−0.04, 95 % CI −0.43 to 0.35) and a slope of 0.50 (95 % CI 0.10 to 0.91; *P* = 0.017 against the ideal slope of 1.0), indicating over-confident predicted probabilities whose degree is only weakly identified at n = 106 with 52 events.

Add to `09_ext_calibration_dca.csv` the columns `calib_intercept_se`, `calib_intercept_ci_lo`, `calib_intercept_ci_hi`, `calib_slope_se`, `calib_slope_ci_lo`, `calib_slope_ci_hi`, `p_slope_eq_1`, and cite that file for the interval.

Separately — and I accept the authors' disclosure as adequate in kind — the sentence "computed on the calibration-corrected probabilities from the external logistic fit …, which was itself fitted on the same 106-sample E-MTAB-4451 set used for validation and is therefore optimistically biased and reported as illustrative (no bootstrap optimism correction was applied…)" is honest and correctly placed. My objection is only to the missing interval, not to the nesting disclosure.

---

### B2-5. The DCA is still framed as a clinical-utility result, not as a discrimination illustration

【Problem】
Having disclosed the test-set nesting, the manuscript nevertheless reports "a positive net benefit over treat-none across the 0.10–0.75 threshold range" — a net-benefit statement, i.e. a clinical-utility claim — computed on in-sample-calibrated probabilities with no optimism correction, and only *later* re-labels the analysis "discrimination-only support".

【Evidence】
`manuscript.md:112` contains, in order: (i) "showed a positive net benefit over treat-none across the 0.10–0.75 threshold range"; (ii) the nesting/optimism disclosure; (iii) at the very end, "the DCA is read as discrimination-only support — the score ranks patients by risk — rather than as a calibrated absolute-risk benefit." Net benefit > 0 is a decision-theoretic claim about consequences of acting on the model; it cannot be retro-annotated into a discrimination statement. The net benefit is also computed from a probability vector whose slope was fitted on the same 106 patients, so even the sign of NB at a given threshold is not out-of-sample.

【Why it matters】
Reviewers and readers skim for "net benefit" and "positive". A Scientific Reports statistical reviewer will require either an independent calibration set or a bootstrap optimism-corrected DCA (Vickers–Elkin: 200+ resamples, model refit in each, optimism subtracted). Without it the DCA adds no decision-analytic information beyond the ROC, while creating the impression that a clinical-utility analysis was performed.

【Specific fix】
Either (a) delete the DCA from the main text and move it to supplementary with the sentence "Net benefit is reported for completeness only; it is computed on in-sample-calibrated probabilities and is not an out-of-sample clinical-utility estimate", or (b) run the correction and report it:

> **New-analysis spec.** In `_ext_calibration_dca.py`, wrap the whole pipeline (standardization of `risk_oriented_sum` → logistic recalibration → threshold grid) in a 1,000-replicate bootstrap. For each replicate b: fit a_b, b_b in-sample, compute NB_b(t) in-sample and NB_b,test(t) on the out-of-bag patients; optimism(t) = mean_b[NB_b(t) − NB_b,test(t)]; corrected NB(t) = NB_apparent(t) − optimism(t). Output `09_ext_dca_grid.csv` columns: `threshold`, `nb_model_apparent`, `optimism`, `nb_model_corrected`, `nb_corrected_ci_lo`, `nb_corrected_ci_hi`, `nb_treat_all`, `n_flagged`, `TP`, `FP`. Report the corrected curve in Fig. S06C with the apparent curve dashed.

If (b) is not run, replace the opening clause with: "As an illustrative, in-sample decision-curve analysis (not a clinical-utility estimate), the calibration-corrected probabilities gave a net benefit above the treat-none line from threshold 0.05 to 0.75…".

---

### B2-6. The L1000 "directionally positive" claim is statistically null, and §3.9 still uses it supportively

【Problem】
The two small-molecule candidates' rescue scores are within ±0.7 SD of the library background and their ranks are indistinguishable from a randomly drawn compound, yet §3.9 still says the reverse-connectivity "supports only the *direction*" of the candidates — residual supportive use that contradicts the "descriptive only" demotion applied in §4 and §6.

【Evidence】
From `03_results/S08_l1000_rescue_trtcp.csv` (n = 20,413) I recomputed the background: mean **0.00640**, median **0.00551**, SD **0.06725**, 53.62 % > 0, IQR −0.0349 to 0.0469, max 0.3182. These reproduce the manuscript's "mean 0.006, median 0.006; 53.6 % > 0" and "top rescue 0.32" exactly. Against that background:

| compound | rescue | z vs background SD | rank | empirical one-sided P |
|---|---|---|---|---|
| lenalidomide | 0.0439 | **+0.65** | 5,435 | **0.27** |
| azithromycin | 0.0133 | **+0.20** | 9,152 | **0.45** |
| prednisone | 0.1364 | **+2.03** | 651 | 0.032 |

So the positive control rejected by the authors is a **3.1× stronger** "rescuer" than the best candidate, and azithromycin (0.0133) sits essentially at the background median (0.0055) and inside the IQR. §3.9 (`:140`) still asserts "Both are directionally positive, meaning the Mars1-down axis is shifted toward expression", and §3.9 (`:142`) still asserts "The reverse-connectivity therefore supports only the *direction* of the small-molecule candidates". Neither statement is compatible with z = +0.65 / +0.20 against a 20,413-compound null. §4 (`:186`) and §6 (`:218`) do apply the "descriptive only" demotion; §3.9 does not.

【Why it matters】
§3.9 is the Results section readers cite. Leaving "supports the direction" there while §4 says "descriptive only" is an internal contradiction of exactly the sort this revision round was meant to remove, and it lets a careless reader carry away "L1000 corroborates lenalidomide and azithromycin". It also weakens the paper's strongest methodological virtue — the authors caught the prednisone problem themselves and should finish the job.

【Specific fix】
Two paste-ready replacements.

In `:140`, replace "Both are directionally positive, meaning the Mars1-down axis is shifted toward expression, but the magnitude is modest and neither reaches the library's top tier.":

> Both scores are positive but lie within the library's noise band: against the background of 20,413 compounds (mean rescue 0.006, SD 0.067) they correspond to z = +0.65 (lenalidomide) and +0.20 (azithromycin), with empirical rank *P* = 0.27 and 0.45, i.e. neither is distinguishable from a compound drawn at random; azithromycin sits at the library median.

In `:142`, replace "The reverse-connectivity therefore supports only the *direction* of the small-molecule candidates, not their functional or clinical benefit;":

> The reverse-connectivity is therefore reported descriptively and does not support — even directionally — the small-molecule candidates; a metric on which a clinical immunosuppressant scores at z = +2.03 while the candidates score at z = +0.65 and +0.20 carries no discriminating information:

Add to `03_results/S08_l1000_candidate_scores.csv` the columns `rescue_z_vs_background`, `rank_empirical_p`, `background_mean`, `background_sd` so the null is auditable.

---

## MINOR ITEMS

### B2-7. The cover letter still calls the external validation "independent" without the label caveat, and calls it "robust"

【Problem】
`cover_letter.md:11` and `:14` use unqualified "independent", contradicting the manuscript's own correctly scoped phrase.

【Evidence】
`cover_letter.md:11`: "an honest **independent** external validation"; `:14`: "generalised to AUC 0.638 … on an **independent**, cross-platform external cohort"; also `:14`: "Two findings are **robust** and source-traceable". The manuscript everywhere says "independent in cohort and platform but **not in label**" (`manuscript.md:8`, `:55`, `:111`, `:184`). The cover letter also omits the L1 external result (0.585), so the "robust" characterisation is applied to the better of two metrics.

【Why it matters】
The cover letter is the editor's first read. An unqualified "independent" there is the single most quotable over-claim in the submission, and it directly contradicts a caveat the authors took care to insert in the manuscript.

【Specific fix】
`cover_letter.md:11` — replace "an honest independent external validation":
> an honest external validation that is **independent in cohort and platform but not in label** (the score orientation was fixed on the discovery cohort's 28-day outcomes)

`cover_letter.md:14` — replace "on an independent, cross-platform external cohort":
> on a cross-platform external cohort (E-MTAB-4451; independent in cohort and platform, not in label) — with the locked L1 model transporting to 0.585 (95 % CI 0.469–0.696)

and replace "Two findings are robust and source-traceable" with "Two findings are fully source-traceable".

---

### B2-8. The 45-test BH family treats three estimators of one null as three hypotheses

【Problem】
The declared primary correction (m = 45 = 5 genes × 3 estimators × 3 outcomes) inflates the family threefold by counting IVW, MR-Egger and weighted median as three separate hypotheses, while the manuscript's own "dependence-ignoring approximation" caveat addresses only the dependence problem, not the hypothesis-structure problem.

【Evidence】
`manuscript.md:149` and `:195`: "45 tests: five assessable genes × three estimators × three outcomes". The three estimators test the *same* causal null for a given gene–outcome pair on the *same* instruments; they are sensitivity analyses, not three hypotheses. The manuscript itself concedes at `:176` that "the apparent method concordance … reflects the same three overlapping, low-power instruments shared across IVW, Egger and weighted median, so the agreement indicates shared data limitations rather than independent corroboration" — which is an admission that these are not three independent tests. The narrower 15-test per-outcome correction is computed and deposited (`p_fdr_bh`) but dismissed as "shown for completeness".

【Why it matters】
The correction is simultaneously too conservative (m is 3× too large) and too liberal (the tests are strongly positively dependent), and neither direction is quantified. A reader cannot tell whether the MR layer is null because the effects are null or because the correction is mis-specified. The conclusion does not change — under the 15-test primary-outcome correction the CD14 Egger *q* is 0.487, still non-significant — so this is cheap to fix and worth fixing properly.

【Specific fix】
**New-analysis spec.** Re-specify the family as **15 tests = 5 genes × 3 outcomes**, with IVW pre-declared as the single primary estimator per gene–outcome pair and MR-Egger / weighted median as sensitivity analyses reported without multiplicity adjustment. Rewrite `10_mr_bh_family.csv` with columns: `gene`, `outcome`, `method`, `nsnp`, `or`, `p_raw`, `p_reference_distribution`, `family_role` (`primary` | `sensitivity`), `q_bh_15test`, `sig_q05`. Then replace the sentence in `:195` with:

> The pre-specified primary family is 15 tests (five assessable genes × three outcomes) with inverse-variance weighting as the single primary estimator; MR-Egger and the weighted median are sensitivity analyses and are not counted in the family. Under this correction no test reaches *q* < 0.05 (minimum *q* = 0.49). The 45-test correction that additionally counts the two sensitivity estimators as separate hypotheses is reported in `10_mr_bh_family.csv` for completeness; it treats three analyses of the same null — and, across outcomes, the same instruments — as independent, so it is a dependence-ignoring approximation and is not the basis for any claim.

---

### B2-9. Inconsistent reference distributions across the three MR estimators

【Problem】
MR-Egger *P*-values are computed on t(n−2), IVW on the normal distribution, and the weighted median from a bootstrap; with 3–8 instruments the normal approximation for IVW is anti-conservative and should also be a t.

【Evidence】
`manuscript.md:60`: "MR-Egger … p-values are two-sided t-tests on df = n_instruments − 2"; the weighted median "SE by 2,000 bootstrap resamples"; nothing is said about the IVW reference distribution. In `10_genetics_mr_outcome4982_criticalcare.csv` the CD74 IVW row gives β = 0.79828, SE = 0.32496, *P* = 0.01403 — I verified 2 × (1 − Φ(2.457)) = 0.01403, i.e. a **normal** test on 3 instruments. On t(2) the same statistic gives *P* = 0.1324 — an order of magnitude larger. The manuscript applies the t-correction selectively, to the one estimator whose nominal hit it wishes to qualify, and not to the estimator that produced the other nominal hit.

【Why it matters】
The paper makes a virtue of the t-correction ("after correcting the MR-Egger p-values to the t(n−2) distribution", `:176`). Applying it to one estimator only is an inconsistency a statistical reviewer will spot immediately, and it makes the IVW *P*-values look better supported than they are.

【Specific fix】
**New-analysis spec.** In `10_genetics_mr_run.py`, compute all *P*-values on t-distributions: IVW and weighted median on t(n_snp − 1), MR-Egger slope on t(n_snp − 2), MR-Egger intercept on t(n_snp − 2). Add a column `p_reference_distribution` (`t(n-1)` / `t(n-2)`) to all three MR CSVs and to `10_mr_bh_family.csv`. Then correct `:60` to: "All *P*-values are two-sided t-tests: IVW and weighted median on df = n_instruments − 1, MR-Egger slope and intercept on df = n_instruments − 2." Report the CD74 critical-care IVW *P* as 0.132 rather than 0.014, and revise every downstream sentence that cites *P* = 0.014 (`:162`, `:174`, `:195`, `10_mr_bh_family.csv:18`).

---

### B2-10. Abstract: "P ≥ 0.23" should be 0.24, and "were" should be "was"

【Problem】
Two small numerical/grammatical defects in the sentence the editor reads first.

【Evidence】
`manuscript.md:14`: "all OR 0.92–1.12, P ≥ 0.23". The five primary-outcome IVW *P*-values in `10_genetics_mr_outcome5086_28ddeath.csv` are 0.718, 0.260, 0.236, 0.847, 0.473; the minimum is **0.2359**, which rounds to 0.24, not 0.23. The OR range 0.92–1.12 is correct (0.9233 … 1.1194). Same sentence: "one sensitivity test (CD14 MR-Egger, OR 0.91, P = 0.049) **were** nominally significant" — subject–verb disagreement.

【Why it matters】
Trivial in isolation; but the abstract is the one place where a wrong digit is read as evidence that the numbers were not checked. The rest of the abstract's MR sentence I verified as exactly right (see *Stands up*).

【Specific fix】
> …gave no significant inverse-variance-weighted estimate on primary 28-day death (all OR 0.92–1.12, P ≥ 0.24); one sensitivity test (CD14 MR-Egger, OR 0.91, P = 0.049) was nominally significant…</para>

---

### B2-11. Table 1 flags one sub-threshold gene but not the other

【Problem】
Table 1 is titled "Consensus immune genes significantly down in Mars1" but contains two rows that fail the paper's own `|logFC| ≥ 0.3` DEG rule, and only one of them is flagged.

【Evidence】
From `03_results/S01_mars1_deg.csv`: `ITGAM` logFC −0.2084, `DEG_0.3 = False`; `LYZ` logFC −0.2561, `DEG_0.3 = False`. `manuscript.md:82` annotates ITGAM with "significant at FDR<0.05 … but below the `|logFC| ≥ 0.3` DEG fold-change threshold, DEG_0.3=False"; `manuscript.md:85` lists `| LYZ | −0.26 | 3.6e-06 | lysozyme |` with **no** equivalent annotation.

【Why it matters】
A reader comparing Table 1 against the DEG rule will find one unexplained row and conclude the rule is applied ad hoc. Cheap to fix; not correcting it invites a wider audit of the tables.

【Specific fix】
Append to the LYZ row the same disclosure used for ITGAM:
> `| LYZ | −0.26 | 3.6e-06 | lysozyme (significant at FDR<0.05, adj.P=3.6×10⁻⁶, but below the `|logFC| ≥ 0.3` DEG fold-change threshold, DEG_0.3=False) |`

and retitle Table 1: "*Table 1. Consensus immune genes significantly down-regulated in Mars1 (FDR<0.05; selected; two rows marked as failing the |logFC| ≥ 0.3 DEG rule).*"

---

### B2-12. The FIS1 concordance logic rests on an untested two-step inference

【Problem】
FIS1 is excluded from the concordant set because it is Mars1-up-regulated, so a protective MR "opposes its observational association" — but FIS1's own association with 28-day death is never quantified anywhere in the paper.

【Evidence】
`03_results/S01_mars1_deg.csv`: FIS1 logFC +1.2614, t = +17.157, adj.P = 0 — correctly cited as "+1.26" and "t = +17.2" at `manuscript.md:106`, `:112`(§3.10), `:149`, `:218`. FIS1's MR OR on 28-day death is 0.9632 (protective, *P* = 0.47) — correctly cited. But FIS1 is **absent from `03_results/S06_signature_genes.csv`** (I checked all 30 rows), so no correlation with 28-day death is reported for it. The argument "FIS1 is up in Mars1 → therefore higher FIS1 is harmful → therefore a protective MR is discordant" is an inference across two steps, the second of which is asserted, not measured. A sceptical reading is available: Mars1-up regulation may itself be an adaptive or bystander response, in which case a protective MR would be *concordant* with a beneficial role and the exclusion would be wrong.

I confirm the **re-scoping itself is complete and internally consistent**: Abstract (`:14`, "non-immune passenger, FIS1 (logFC +1.26, up-regulated)"), §3.10 (`:149`, "not counted among the concordant hubs"), §3.10 (`:176`, "not counted here"), §4 (`:186`, "reported descriptively rather than as concordant"), Limitation 2 (`:195`, "reported descriptively"), §6 (`:218`, "co-expression passenger rather than an immune hub") — all five sites say the same thing, and §3.3's "passenger" characterisation does not contradict them.

【Why it matters】
The exclusion is defensible, but as written it is a directional assertion presented as a derivation. One extra number closes it and costs nothing.

【Specific fix】
**New-analysis spec.** In `02_scripts/python/06_signature.py` (or a new `_fis1_direction.py`), compute for FIS1 on GSE65682 sepsis samples with known 28-day outcome: Pearson r with `death_28d`, univariate logistic OR per SD (95 % CI, *P*), and the same for the five immune hubs for comparison; write `03_results/S06_hub_death_association.csv` with columns `gene`, `mars1_logFC`, `corr_with_death`, `or_per_sd`, `ci_lo`, `ci_hi`, `p`, `predicted_mr_direction`, `observed_mr_or`, `concordant`. Then replace the clause in `:149` with:

> FIS1 also returned a protective point estimate, but FIS1 is *up*-regulated in Mars1 (logFC +1.26) and higher FIS1 expression is itself associated with 28-day death in the discovery cohort (OR per SD = X.XX, 95 % CI A–B, *P* = C), so a protective MR estimate opposes its own observational direction; FIS1 is therefore reported as a passenger-gene observation rather than as model-concordant.

---

### B2-13. One MR model label contradicts the stated fixed/random switching rule

【Problem】
`10_genetics_mr_outcome4982_criticalcare.csv` labels the CD74 IVW fit `random`, although Cochran Q (0.1028) is below its df (2), which per the Methods should select fixed effects.

【Evidence】
`manuscript.md:60`: "IVW … fixed-effects with a switch to multiplicative random effects when Cochran Q exceeded its df". CD74 critical care: Q = 0.10277, Q_df = 2 → Q < df → rule says `fixed`, file says `random`. All nine other IVW rows follow the rule correctly (e.g. CD14 28-day death Q = 0.7865 < 5 → `fixed`; HAVCR2 28-day death Q = 6.998 > 5 → `random`). Numerically the impact is nil here because the random-effects inflation factor is √max(1, Q/df) = √max(1, 0.0514) = 1.

【Why it matters】
A reproducibility defect rather than a result-changing one; but it is exactly the kind of mismatch that makes a reviewer distrust the rest of the MR table.

【Specific fix】
Correct the `model` field to `fixed` in `10_genetics_mr_outcome4982_criticalcare.csv` row 2, or amend `:60` to state the actual rule implemented (e.g. "random effects were used whenever the multiplicative random-effects variance was estimable"). Add an assertion to `check_audit_assertions.py`: `model == 'random' iff Q > Q_df`.

---

## § Stands up

Things I suspected were wrong, went to the source data for, and found **correct**. These are genuine passes, not filler.

1. **The two quoted DCA margins are arithmetically exact.** I recomputed every threshold from `09_ext_risk_scores.csv` and reproduced `09_ext_dca_grid.csv` to 4 decimal places. Over 0.30–0.50 the model-minus-treat-all margins are 0.0121 / 0.0225 / 0.0094 / 0.0292 / 0.0943 → "0.01–0.09" ✓. Over 0.55–0.75 they are 0.1667 / 0.3208 / 0.4973 / 0.7044 / 1.0472 → "0.17–1.05" ✓. The crossover at ≈0.30 is also exact: model NB equals treat-all NB at every grid point from 0.05 to 0.25 and is strictly greater from 0.30.

2. **"Treat-all NB collapses toward −∞ as the threshold approaches 1 — an algebraic property at prevalence 0.49" is correct.** NB_all(t) = p − (1−p)·t/(1−t) → −∞ as t→1 whenever p < 1; with p = 0.4906 the treat-all curve crosses zero exactly at t = p = 0.4906, which the grid confirms (NB_all = +0.0738 at 0.45, −0.0189 at 0.50). The authors' interpretation — that the large margins are an artefact of the comparator, not evidence of model gain — is statistically right.

3. **"At thresholds ≥0.80 the model's own net benefit is 0.00 … because no calibration-corrected predicted risk exceeds the threshold" is correct and precisely bounded.** I refit the calibration and found **max calibrated p = 0.7606**; the counts of patients with p ≥ t are 1 at 0.75, 0 at 0.80. So the "≥0.80" cut-point is exact, and −1.55 at 0.80 matches the grid.

4. **Every number in MR Tables 4 and 5 reconciles to the source CSVs.** I re-derived the IVW estimates for CD14 28-day death (β = −0.0758, SE = 0.0640 vs deposited −0.07586 / 0.06400) and CD74 critical care (β = 0.7983, SE = 0.3250 vs 0.79828 / 0.32496) from the raw harmonised betas, and checked all 15 susceptibility/28-day/critical-care OR–CI–P triples in Table 5 plus all five I² triples. All match. "All susceptibility IVW *P* ≥ 0.249" ✓ (minimum 0.2489). "No primary IVW estimate reached significance" ✓. "Median *F* 35–168" ✓ (I recomputed all five per-gene medians: 35.38 / 168.12 / 45.65 / 36.44 / 75.01). "27 instruments (CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8)" ✓ — 27 rows, exactly as counted. MR-Egger t(n−2) *P*-values ✓ (CD74 critical care t = 7.187 on df = 1 → *P* = 0.0880; CD74 susceptibility t = 3.768 on df = 1 → *P* = 0.1649, and the accompanying intercept *P* = 9.98×10⁻⁵ ≈ 1.0×10⁻⁴).

5. **The Abstract's MR sentence is accurate on every figure it states**, with only the two defects noted in B2-10. "No significant IVW estimate on primary 28-day death (all OR 0.92–1.12)" ✓; "one sensitivity test (CD14 MR-Egger, OR 0.91, P = 0.049)" ✓ (0.90595 / 0.04881); "CD74 critical care, OR 2.19" ✓ (2.19436); "ran opposite to the expression model" ✓ (OR > 1 for a Mars1-down gene). The claim that CD14 MR-Egger is the *only* nominally significant test on the primary outcome is ✓ — no other primary-outcome test has *P* < 0.05.

6. **The immune-score table is exact.** Recomputed from the 802-row `S02_immunoparalysis_score.csv`: Mars1 median −0.7917 (n = 132); Mars2 −0.752, *P* = 0.467; Mars3 0.641, *P* = 1.85×10⁻¹⁸; Mars4 −0.235, *P* = 1.32×10⁻³; full-cohort range −3.650 to 3.862. Every figure in Table 2 and §3.2 matches, including the honest admission that the score does not separate Mars1 from Mars2.

7. **The L1000 descriptive statistics are exact.** Background mean 0.00640 / median 0.00551 / 53.6 % > 0 / max 0.3182 all reproduce; lenalidomide rank 5,435 (26.6 %) and azithromycin 9,152 (44.8 %) match `S08_l1000_candidate_scores.csv`; `wtcs = rescue × √22` verified for both (0.0439 × 4.6904 = 0.2059; 0.0133 × 4.6904 = 0.0624); prednisone 651/20,413 = 3.19 % and dexamethasone 6,808/20,413 = 33.35 % both match. The authors' decision to disclose the prednisone refutation is genuinely good practice.

8. **The FIS1 re-scoping is complete and consistent across all five sites** (Abstract `:14`, §3.10 `:149` and `:176`, §4 `:186`, Limitation 2 `:195`, §6 `:218`) — see B2-12 for the full enumeration. No residual "three of the five" phrasing survives anywhere in the manuscript; the regression sweep for `three of the five assessable hubs`, `three of five assessable hubs`, `widens rather than converges`, unqualified `reduced checkpoint engagement`, `conservative approximation` and `v1.17.0` returned zero hits in `manuscript.md`.

9. **Structural housekeeping is clean.** Abstract = **193 words**, no citations, non-structured ✓. References 1–38 contiguous and in first-appearance order ✓. Tables 1–5 each captioned exactly once at lines 74 / 92 / 122 / 151 / 164, and all 11 in-text cross-references resolve correctly ✓. All 11 files named in the §8 figure index exist in `04_figures/` ✓. Mars1 DEG count 3,597 ✓ (recomputed from `S01_mars1_deg.csv`). CD74 −0.76/2.1e-15, CD14 −0.77, FCGR3A −0.61/9.1e-11, HAVCR2 −0.35/2.8e-13, PDCD1 +0.16/3.0e-10 ✓. The standalone Data availability / Code availability sections do not conflict (one covers data + a one-line code pointer, the other code + licence) ✓.

---

## § Questions for the authors

1. Was the fixed-orientation equal-weight score declared the **primary** external metric before the locked-L1 external AUC (0.585) was computed? If it was chosen afterwards, please say so explicitly — the honesty is worth more than the framing.

2. `10_genetics_mr_harmonised.csv` contains outcome betas for **sepsis susceptibility (`ieu-b-4980`)**, not the primary 28-day-death outcome — I verified this by reconstructing the CD74 (β = 0.0717) and CD14 (β = −0.01002) IVW estimates, which match `10_genetics_mr.csv` exactly, not the 5086 file. The manuscript calls these "the accompanying `*_harmonised.csv` tables" generically. Which harmonised file does the STROBE-MR item 9b disclosure intend as the primary-outcome instrument table, and is `10_genetics_mr_outcome5086_harmonised.csv` the one readers should use? Please name the file explicitly in §2.10.

3. Which weighted-median variance estimator produced SE = 0.0885 from three instruments (§2.10 says "2,000 bootstrap resamples")? Please report the estimator and, for transparency, the weighted-median SE recomputed (a) analytically and (b) with the bootstrap applied to all genes, so readers can see which genes are affected besides CD74.

4. Why was the t(n−2) correction applied to MR-Egger *P*-values but not to IVW or weighted-median *P*-values (B2-9)?

5. Is the DeLong *P* ≈ 0.56 for the 0.638-vs-0.619 comparison (§3.4) reproducible from a deposited file? I could not verify it — Peng et al.'s own IRG score is not in the repository, only the 3-gene proxy (0.5288). If it was computed against the proxy rather than the published signature, it should be re-described.

6. The manuscript reports minimum detectable ORs of 1.16–2.12 for the **28-day-death** outcome (§2.10). Given that critical care has fewer cases (1,380 vs 1,896), what is the CD74 MDE on the critical-care outcome? My calculation from the deposited SE gives ≈2.49, which is above the reported OR of 2.19 — please confirm or correct.

7. Was any permutation or empirical null computed for the L1000 rescue score beyond the background mean/median/percentage-above-zero now reported? I derived z = +0.65 and +0.20 from the deposited background SD; if the authors have their own null, please report it.

---

## § What I actually checked

**Files read in full**
`05_reports/manuscript.md` (all 324 lines, including the 12 long lines the reader truncates — I re-extracted them separately at lines 60, 112, 138, 149, 176, 195), `05_reports/cover_letter.md`, `05_reports/review_r18/_PANEL_BRIEF.md`;
`03_results/`: `09_external_validation.csv`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`, `09_ext_risk_scores.csv` (used to refit calibration and DCA), `S06_auc_compare.csv`, `S06_signature_genes.csv`, `S01_mars1_deg.csv`, `S02_immunoparalysis_score.csv`, `S08_l1000_candidate_scores.csv`, `S08_l1000_rescue_trtcp.csv` (20,413 rows), `S08_l1000_positive_control.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, `10_mr_bh_family.csv`, `10_genetics_mr_harmonised.csv`, `10_genetics_mr_outcome4982_harmonised.csv`, `10_genetics_mr_outcome5086_harmonised.csv`;
`02_scripts/python/09_external_validation.py`, `02_scripts/python/_ext_calibration_dca.py`;
`04_figures/` (enumerated, 11 files, cross-checked against the §8 index).

**Computations I ran myself (not read from the manuscript)**
- Mars1 immune score: medians, Mann–Whitney *P* ×3, full range — **all reproduced exactly**.
- Calibration: refit the 2-parameter logistic recalibration; recovered a = −0.0382, b = 0.5028, AUC = 0.6382; computed SEs from the numerical Hessian → **slope 95 % CI 0.095–0.910, intercept 95 % CI −0.430–0.354, *P*(slope = 1) = 0.017**. Max calibrated probability 0.7606.
- DCA: rebuilt the full threshold grid from raw risk scores; reproduced all 18 deposited rows to 4 dp; computed flagged/TP/FP counts and all margins at 13 thresholds.
- MR: rebuilt IVW (fixed and random), per-SNP ratio estimates and SEs from raw harmonised betas for CD74 (both outcomes), CD14 (both outcomes), and checked all 45 family rows for consistency; verified median *F* per gene; verified t(n−2) *P*-values for every MR-Egger row; computed the t(2) and t(1) corrections for the weighted median and Egger.
- L1000: recomputed background mean/SD/median/percentage-above-zero/IQR/max over 20,413 compounds; computed z-scores and empirical rank *P* for the three named compounds.
- Text: abstract word count (193) and citation scan; reference contiguity; Table 1–5 caption/cross-reference audit; regression grep for six pre-revision phrasings plus `v1.16.0`/`v1.17.0`/`v1.18.0`.
- I ran `02_scripts/python/check_audit_assertions.py`: 32 assertions, exit 0. I treated it as evidence about **arithmetic only**; one of its assertions ("DCA prose matches deposited grid … diverges at 0.80") passes while the prose claim it is meant to guard ("advantage **confined** to 0.30–0.75") is false — see B2-3.

**Discrepancies found, stated plainly**
1. CD74 critical-care weighted-median SE = 0.0885 vs IVW SE = 0.3250 from the same 3 variants → *P* = 6.6×10⁻¹⁹ is not sustainable (B2-1). **New.**
2. The 0.659→0.638 comparison mixes the L1 model with the equal-weight score; like-for-like is 0.659→0.585 (B2-2). **New.**
3. "Advantage over treat-all confined to 0.30–0.75" — false at 0.80–0.90 (+1.55/+2.40/+4.09); the quoted ranges 0.01–0.09 and 0.17–1.05 are themselves correct (B2-3). **New.**
4. Calibration slope CI (0.10–0.91) omitted although trivially computable and decisive (B2-4). **New.**
5. L1000 candidates at z = +0.65 / +0.20 vs background SD 0.067; prednisone at z = +2.03 (B2-6). **New, quantified.**
6. Cover letter "honest independent external validation" and "robust" (B2-7). **New.**
7. Abstract "P ≥ 0.23" (should be 0.24) and "were" (should be "was") (B2-10). **New.**
8. Table 1: LYZ not flagged as sub-threshold although ITGAM is (B2-11). **New.**
9. CD74 critical-care IVW labelled `random` though Q < df (B2-13). **New, no numeric impact.**
10. IVW/weighted-median *P* on the normal distribution while MR-Egger uses t(n−2) (B2-9). **New.**
11. 45-test family counts three estimators of one null as three hypotheses (B2-8). **New framing gap; conclusion unchanged.**

**Items in the brief that I checked and found NO defect in:** the FIS1 logic and all five of its sites (defensible, with one gap noted in B2-12); the L1000 demotion in §4 and §6 (correctly applied — the gap is in §3.9 only); the MR abstract wording apart from B2-10; the treat-all −∞ algebra; the ≥0.80 NB = 0.00 claim; the calibration test-set nesting disclosure as such; the abstract length; the reference list; the table numbering; the new standalone Code availability section.

---

## VERDICT

**Major revision.**

The manuscript's design bones are sound and, unusually, its hedging is mostly earned rather than cosmetic: the label-leakage is disclosed in four places, the calibration is correctly identified as in-sample and illustrative, the MR layer is explicitly demoted to hypothesis-generating, the sample overlap is named and its direction of bias stated, and the authors disclosed the prednisone result that refutes their own connectivity axis. I verified the Mars1 confirmation, the external AUC, the immune-score table, the L1000 descriptive statistics and 40-plus MR figures directly from source data, and found them exact. That is a real pass, and none of what follows is a fabrication or integrity concern.

The revision is required because of one hard statistical error and one framing error in the headline evidence. **B2-1**: the only family-significant MR result — quoted in the Abstract — carries a *P*-value of 6.6×10⁻¹⁹ derived from a weighted-median standard error (0.0885) that is 0.272 × the IVW standard error from the same three variants, from three instruments none of which is individually significant (minimum *P* = 0.097), and it contradicts the paper's own minimum-detectable-effect calculation. That number cannot be published as it stands. **B2-2**: the paper's central transport claim compares an L1-model within-cohort AUC of 0.659 against an equal-weight external AUC of 0.638, when the like-for-like external result for the L1 model is 0.585 with a CI that includes 0.5 — a model switch that understates the transport loss by 3.7× and is the exact thing the "honest external validation" framing exists to prevent. Both are cheap to fix, but both touch the title claim.

Alongside these, the DCA passage contains a sentence that is literally false as written (B2-3) and still reads as a clinical-utility claim despite its own disclosure (B2-5); the calibration slope is reported without the interval that decides how it should be read (B2-4); and the L1000 section still uses the connectivity supportively in §3.9 after §4 and §6 have demoted it (B2-6). The remaining seven items are copy-edits, one table annotation, one estimator-labelling mismatch, and two re-specifications that do not change any conclusion.

**Desk-reject hard-fail: no.** Nothing here is fabricated, nothing is undisclosed misconduct, and no conclusion depends on a number I could not trace to a deposited file. B2-1 is the closest to a hard-fail — a *P*-value wrong by ~17 orders of magnitude in a Nature-family abstract is ordinarily disqualifying — but it is a single correctable computational artefact in a layer the manuscript already labels hypothesis-generating and already reports as reversed-direction, so withdrawing or recomputing that one number resolves it. I would not desk-reject. I would not accept either. Fix B2-1 through B2-6 and the seven minor items, and the manuscript should be acceptable.
