# A2 — Biostatistical / Design / MR Review

**Manuscript:** *Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning*
**Reviewer role:** Biostatistician / causal-inference / Mendelian-randomisation methodologist (independent first-pass review)
**Scope:** MR design, FDR correction, calibration/DCA, immune-score comparisons, cross-validation optimism.

---

## Independence statement

I have not previously seen this manuscript. I read only the raw sources permitted for this review: `05_reports/manuscript.md`, the three MR outcome CSVs, `10_mr_bh_family.csv`, the `*_harmonised.csv` instrument files, `S02_immunoparalysis_score.csv`, `09_ext_calibration_dca.csv`, `09_ext_risk_scores.csv`, `09_external_validation.csv`, `S06_auc_compare.csv`, and `S06_signature_genes.csv`. I deliberately did **not** open any `*REVIEW_*`, `*RESPONSE_*`, `*REVISION_*`, prior `*_PANEL_BRIEF.md`, other reviewers' files under `review_r7/`, or `SUBMISSION_MANIFEST.md`. Every number I cite was re-derived from the CSVs; I did not rely on the manuscript's prior review history. My judgements are based solely on the files above.

---

## Issues

### Issue 1 — The DCA "beats treat-all" message is marginal and partly artifactual 【Problem】
The decision-curve analysis is presented as showing the external score "gave positive net benefit over treat-none across the full threshold range and exceeded treat-all above ~0.20." On recomputation this framing is overstated.

【Evidence】
From `09_ext_risk_scores.csv` (n=106, 52 deaths, prevalence 0.4906) and a re-fit logistic recalibration, the model net benefit (NB) versus treat-all is:

| threshold | model NB | treat-all NB | difference |
|-----------|---------|-------------|------------|
| 0.20 | 0.3632 | 0.3632 | **+0.0000** |
| 0.30 | 0.2844 | 0.2722 | +0.0121 |
| 0.50 | 0.0755 | −0.0189 | +0.0943 |

At threshold 0.20 the model predicts **all 106 patients positive** (TP=52, FP=54), so it is *operationally identical* to treat-all — the figure's "exceeded treat-all above ~0.20" is false at exactly that threshold. The only threshold where the gap looks meaningful is 0.50, but there the model treats only ~47% of patients and the gain (0.094) sits on top of an external AUC whose 95% CI (0.532–0.748) only just excludes 0.5 and whose optimism is ~0.09.

【Why it matters】
Sepsis is a ~49%-prevalence, treat-everyone-by-default condition. Concluding the score "beats treat-all" from a +0.012 gap at n=106 (well inside bootstrap noise) invites over-reading into clinical actionability. The honestly useful output of this analysis is the **calibration slope (0.50)**, not the net-benefit advantage.

【Specific fix】
Reframe the DCA paragraph around the calibration slope (under-dispersed / over-confident probabilities — the genuinely informative quantity) and state explicitly that the model does not separate from treat-all until ≈0.30 and that even there the gap (0.012) is within sampling noise at n=106. Drop or soften "exceeded treat-all above ~0.20."

### Issue 2 — The single family-significant MR test is biologically incoherent and sits on the weakest instrument set 【Problem】
The only test surviving the pre-specified 45-test correction is the CD74 critical-care **weighted median** (family q≈3×10⁻¹⁷), but it is direction-opposite to the Mars1 expression model and rests on the most fragile instruments.

【Evidence】
- Direction: weighted-median OR 2.194 (95% CI 1.845–2.610), i.e., *higher genetically predicted CD74 → worse critical-care outcome*. Mars1 expression shows CD74 **down** (Δ=−0.76, adj.P=2.1×10⁻¹⁵); lower CD74 tracks the immunosuppressed/bad program. The MR direction is therefore opposite to the expression-level biology.
- Instrument fragility: CD74 is the **only 3-SNP gene** (median F≈35.4 — the lowest of all hubs; the next-lowest median F is CD14 ≈45.7). All other hubs carry 4–8 SNPs.
- Overlap exposure: eQTLGen⊂UK Biobank overlap biases MR SEs **downward** (Type-I inflation); the one "significant" result is the most exposed.
- Companion anomaly: the same-gene MR-Egger on this outcome has Egger SE 0.111 but IVW SE 0.325 on the same 3 SNPs (slopes nearly identical, intercept≈0) — flagged by the authors but unresolved.

【Why it matters】
A "survives family correction" result that is direction-opposite to biology, built on 3 SNPs and overlap-contaminated SEs, should not be left where a casual reader cites it as a positive MR finding. The manuscript already calls it a "genotype–severity association rather than a causal hub claim," but the headline "one test survives q<0.05" can be misread.

【Specific fix】
Keep the explicit non-causal framing; add a one-line quantitative overlap-bias note (overlap inflates significance, so this is the *most* exposed result) and, ideally, a Burgess–Davies–Thompson overlap-corrected SE or leave-overlap-out sensitivity.

### Issue 3 — Sample overlap is disclosed but its *direction of bias* is under-weighted 【Problem】
§2.10 and §5.2 disclose the eQTLGen⊂UK Biobank overlap and label the MR hypothesis-generating, but the bias is described as generic uncertainty rather than a specific Type-I inflation.

【Evidence】
Burgess, Davies & Thompson (2016, ref [31]) show exposure–outcome sample overlap shrinks MR standard errors, pushing estimates toward false positives. This is not symmetric uncertainty — it is directional. The single family-significant result (Issue 2) is precisely the one most inflated.

【Why it matters】
"Hypothesis-generating only" undersells that the bias moves *toward* significance, so the null MR reading is the right one *despite* the one surviving test, not merely because of caution.

【Specific fix】
State the direction of bias explicitly in §5.2 and, if feasible, report an overlap-corrected sensitivity or at least a qualitative statement that every MR SE in this layer is conservatively biased toward significance.

### Issue 4 — CD74 critical-care MR-Egger SE < IVW SE is unresolved 【Problem】
On the same 3 SNPs the Egger SE (0.111) is ~3× smaller than the IVW SE (0.325), while the slopes are essentially identical (0.79828 vs 0.79828, intercept ≈1.3×10⁻⁶). With k=3 the Egger and IVW slope variances should be of the same order.

【Evidence】
`10_genetics_mr_outcome4982_criticalcare.csv`: CD74 IVW se=0.32496, Egger se=0.11107. The authors flag this ordering as "physically implausible" but do not re-derive it.

【Why it matters】
A 3× smaller Egger SE suggests a possible variance-formula error in the Egger column for this gene. It does **not** change conclusions (Egger family q=0.79 either way), but it weakens confidence in the Egger estimates for the weakest instrument set.

【Specific fix】
Re-derive the Egger SE against a reference implementation (e.g., the standard MR-Egger closed form) and confirm; if a bug, correct and re-report the Egger column for CD74 critical care.

### Issue 5 — "Multiplicative random effects" terminology and the Q>df RE trigger are non-standard 【Problem】
The IVW random/fixed switch is described as "multiplicative random effects when Cochran Q exceeded its df," and the `model` column switches to random-effects whenever Q>df even when heterogeneity is non-significant.

【Evidence】
Example: CD74 28-day-death has Q=2.55, Q_df=2.0, Q_p=0.279 → `model=random` (Q>df triggers RE despite non-significant heterogeneity). The term "multiplicative random effects" is not the standard DerSimonian–Laird / additive random-effects MR vocabulary.

【Why it matters】
Non-standard terminology can confuse reviewers about the variance model actually used; the Q>df rule (vs Q_p<0.05) is conservative but should be stated so readers don't assume a significance-based trigger.

【Specific fix】
Clarify which random-effects variant is implemented and that the trigger is Q>df (conservative). Editorial, not validity-threatening — the application is internally consistent.

### Issue 6 — 45-test vs 15-test BH columns risk reader confusion 【Problem】
`10_mr_bh_family.csv` carries both `p_fdr_bh_per_outcome_15test` and `q_family_45test`; §2.10 correctly states the 45-test family is primary, but the per-outcome column is prominent.

【Evidence】
CD14 28-day-death MR-Egger: per-outcome `p_fdr_bh`=0.48697 (not significant), but the pre-specified family q=0.730. A reader scanning the per-outcome column could mistake 0.49 for the corrected value.

【Why it matters】
The whole point of the 45-test family is that the per-outcome view over-states significance; the two columns must be visually distinguished.

【Specific fix】
Mark the 15-test column as "reference only — not the primary correction" and keep the 45-test family q as the decision threshold.

### Issue 7 — Immune-score / signature share partial circularity (acknowledged, but keep explicit) 【Problem】
The immune-function score is built from HLA-II/T-cell/exhaustion gene sets that also *define* Mars1, and the 30-gene signature reuses the same 28-day labels for selection and orientation.

【Evidence】
§3.2 admits the score is "partly definitional"; §5.10 acknowledges the selection-chain family-wise error is uncontrolled. Recomputed Mars1-vs-Mars3 separation (P=1.85×10⁻¹⁸) largely recapitulates the score's construction.

【Why it matters】
The within-cohort separation should not be sold as independent biology; the honest external AUC 0.638 is what carries the prognostic claim. The manuscript already handles this well — this is a "keep the honesty, don't weaken it" note.

【Specific fix】
No new analysis needed; optionally add one sentence that the score's endotype separation is *expected by construction* and the external cohort is the validatable test.

---

## § Stands up

**1. MR-Egger p-values are computed with the correct t(n−2) distribution.** All 15 MR-Egger rows reproduce to <1e-9, and **zero** rows equal the normal-distribution value. The t-correction is decisive: CD74 critical-care Egger normal p=6.6×10⁻¹³ (would have survived) vs t p=0.088 (does not); CD14 28-day-death Egger normal 5.1×10⁻³ vs t 4.9×10⁻². This is the single most error-prone step in MR reporting and it is done right.

**2. The 45-test BH family correction is correct, and exactly one test survives.** Recomputed q for CD74 critical-care weighted median = 2.99×10⁻¹⁷ vs stored 2.99×10⁻¹⁷ (diff 9×10⁻¹⁶). The next-smallest p (CD74 critical-care IVW, 0.014) gives q=0.316, so the family is clean. The surviving test's direction opposes the Mars1 expression model — correctly interpreted as non-causal.

**3. External calibration/DCA reproduces exactly.** AUC 0.6382; recalibration (standardised score) slope 0.5005, intercept −0.0381 vs reported 0.5028 / −0.0382; the net-benefit table matches to 4 decimals. The recalibration is on the external cohort and is correctly executed.

**4. Immune-score Mann–Whitney comparisons reproduce.** Mars1 vs Mars2 P=0.467, vs Mars3 1.85×10⁻¹⁸, vs Mars4 1.32×10⁻³ — exactly as reported — and the score does *not* separate Mars1/Mars2 but *does* separate the low pair from Mars3 (P=3.7×10⁻²⁸) and Mars4 (P=1.1×10⁻⁴).

**5. Instrument strength clears the F>10 rule for every retained SNP.** Minimum F is ≈30.7 (CD74 rs12478601) and ≈30.9 (HAVCR2 rs9266629); all others far higher. Median F values in Table 3 (35.4, 168.1, 45.7, 75.0) all reproduce from the harmonised files. No weak-instrument gene — though CD74 (3 SNPs, F≈35) is the weakest and coincidentally hosts the only family-significant (direction-opposite) result. Max I² across all tests = 0.502 (FIS1 critical care), matching the manuscript's "≈0.50" claim.

**6. External and CV AUCs verify, and optimism is correctly flagged.** External AUC 0.638 (95% CI 0.532–0.748) from n=106/52; CV AUC 0.659 vs training 0.750 (optimism ≈0.09) — the manuscript explicitly treats the within-cohort CV as optimistic and reports the external 0.638 as the honest estimate. Both are correct.

---

## § Questions for the authors

1. Can you confirm `04_figures/S06_dca.png` is the **external-cohort** DCA (n=106) and not a discovery-cohort plot? The backing CSV (`09_ext_calibration_dca.csv`, n=106, 52 deaths) is unambiguously external, but I could not visually verify the PNG content here.
2. For CD74 critical care, please re-derive the MR-Egger SE (0.111) against a reference implementation — its 3× deficit versus the IVW SE (0.325) on identical slopes is suspicious (conclusion unchanged).
3. Was any overlap-bias correction (Burgess–Davies–Thompson) attempted, even as a sensitivity? Given the only family-significant result is overlap-exposed, a sensitivity would harden the "hypothesis-generating" caveat.
4. Is the equal-weight score intended as a **risk-ranker** (AUC) or a **probability generator**? The recalibration slope of 0.50 means uncalibrated probabilities are over-confident; the DCA framing should match the intended use.

---

## § What I actually checked

**Files read (raw sources only):** `05_reports/manuscript.md`; `03_results/10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, `10_mr_bh_family.csv`, `10_genetics_mr_harmonised.csv`, `10_genetics_mr_outcome4982_harmonised.csv`, `10_genetics_mr_outcome5086_harmonised.csv`, `S02_immunoparalysis_score.csv`, `09_ext_calibration_dca.csv`, `09_ext_risk_scores.csv`, `09_external_validation.csv`, `S06_auc_compare.csv`, `S06_signature_genes.csv`.

**Recomputation 1 — MR-Egger p-values (t-test, df=nsnp−2).** For each MR-Egger row: `p = 2*scipy.stats.t.sf(|beta/se|, nsnp-2)` and compared to the normal value `2*norm.sf(|t|)`. Result: all 15 rows reproduce the stored p to <1e-9; **0 rows** match the normal distribution. Decisive cases: CD74 critical-care Egger t=7.187, df=1 → t p=0.0880 (stored 0.0880), normal p=6.6×10⁻¹³; CD14 28-day-death Egger t=2.800, df=4 → t p=0.0488 (stored 0.0488), normal p=0.0051.

**Recomputation 2 — BH 45-test family q.** Pooled the 45 p-values (5 genes × 3 estimators × 3 outcomes; FCGR3A excluded). Manual BH (`q_(i) = min(p_(i)·45/rank, q_(i+1))`). Result: exactly **1 test** with q<0.05 — CD74 critical-care weighted median, recomputed q=2.991873×10⁻¹⁷ vs stored 2.991873×10⁻¹⁷ (max |diff| = 9.4×10⁻¹⁶). Direction: OR 2.194 > 1 ⇒ higher predicted CD74 → worse outcome, opposite to Mars1 (CD74 down). Second-smallest p (CD74 crit-care IVW 0.014) → q=0.316; CD14 28-day-death Egger (0.0488) → q=0.730; CD74 crit-care Egger (0.088) → q=0.792. All match the manuscript's stated family q's.

**Recomputation 3 — Immune-score Mann–Whitney (two-sided).** From `S02_immunoparalysis_score.csv` (Mars1 n=132, Mars2 n=176, Mars3 n=118, Mars4 n=53): Mars1 vs Mars2 P=0.467 (median −0.792 vs −0.752); Mars1 vs Mars3 P=1.85×10⁻¹⁸ (median −0.792 vs 0.640); Mars1 vs Mars4 P=1.32×10⁻³ (median −0.792 vs −0.235). Low pair (Mars1+Mars2) vs Mars3 P=3.7×10⁻²⁸, vs Mars4 P=1.1×10⁻⁴ — confirms the score does not separate Mars1/Mars2 but does separate the low pair from Mars3/Mars4.

**Recomputation 4 — Calibration / DCA.** From `09_ext_risk_scores.csv` (y, risk_oriented_sum): n=106, deaths=52, prevalence=0.4906. AUC(risk, y)=0.6382. Recalibrated (standardised score) logistic: intercept=−0.0381, slope=0.5005 (vs reported −0.0382 / 0.5028). Net benefit at thr 0.20 = 0.3632 (= treat-all, model predicts all 106 positive); thr 0.30 = 0.2844 (treat-all 0.2722, diff +0.012); thr 0.50 = 0.0755 (treat-all −0.0189). All match `09_ext_calibration_dca.csv`.

**Recomputation 5 — External AUC & CV optimism.** `09_external_validation.csv`: AUC 0.6382, CI 0.5317–0.7475, n=106, 52 deaths. `S06_auc_compare.csv`: CV AUC=0.6586, training=0.7495, optimism≈0.091 — flagged optimistic by the manuscript. Both reproduce; `09_external_validation.csv` also records the locked-L1 external AUC 0.5848 (vs oriented-sum 0.6382), consistent with the manuscript's "gene set + orientation portable, learned weights not."

**Discrepancies found:** **none** between my recomputations and the manuscript's reported statistics. Every re-derived number matched to the precision shown. The issues raised above are about *interpretation and framing* (Issues 1–3, 7) and *terminology/unresolved anomalies* (Issues 4–6), not arithmetic errors — with the single exception that the DCA's "beats treat-all" claim is numerically true only at thr≥0.30 (equal at 0.20), which I treat as overstatement rather than a calculation error.
