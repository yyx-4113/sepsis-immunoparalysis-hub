# Reviewer A2 — Study design, statistics & causal inference (MR) audit

**Manuscript:** `05_reports/manuscript.md` (v1.8.0)
**Role:** Independent design/statistics/MR auditor. I have not seen any prior review; this is a first-submission read.

## Overall verdict

**Minor Revision — no DESK-REJECT.** The MR and the associated statistics are, on the whole, competently executed and unusually candid about their own limits. The reported numbers that I could recompute all match (Egger t-distribution, instrument F-range, BH family significance, external-validation keys, calibration/DCA). The problems I raise are real but fixable and do not undermine the Tier-1/Tier-2 biology. The most important is that the single "family-significant" MR result is precisely the least trustworthy signal in the entire causal layer, and the global power figure is too optimistic for the gene that produced it.

---

## Issue 1 — The only family-significant MR result is the least trustworthy signal, yet is reported with a precision-laden q-value

**【Problem】** The lone result that survives the 45-test Benjamini–Hochberg correction (CD74 critical-care weighted median, family q ≈ 3×10⁻¹⁷) is produced by the weakest instruments, the smallest sample, and (acknowledged) exposure–outcome overlap, so the q-value overstates how firmly it is established.

**【Evidence】** `10_mr_bh_family.csv` row 17: CD74 / Weighted median / 4982_critcare, q_family_45test = 2.99×10⁻¹⁷, the only `family_sig_q<0.05 = YES` of 45. The driving p = 6.6486×10⁻¹⁹ comes from `10_genetics_mr_outcome4982_criticalcare.csv` (beta = 0.7859, se = 0.0885, nsnp = 3). I recomputed: with 3 instruments the weighted-median SE (0.0885) is **smaller than the IVW SE (0.3250)** on the same 3 SNPs, and the Egger SE (0.1111) is likewise smaller than IVW SE — giving a z-statistic of 8.88 from only three MHC variants. The normal approximation on the log scale (used in `_recompute_mr_pvalues.py`) treats this as a clean z-test, which it is not.

**【Why it matters】** A z of ~8.9 and a q of 10⁻¹⁷ from three SNPs is not a credible precision claim; it is the signature of extreme leverage among three correlated-in-effect instruments. Because BH controls *multiplicity* but not the *downward SE bias* from the sample overlap the authors themselves flag (§2.10, §3.10), the one test that "survives" is also the one most inflated by the very bias they name. A reader skimming the abstract ("only the CD74 critical-care weighted median survived correction") may take q≈3×10⁻¹⁷ as strong evidence, when the manuscript's own interpretation already walks it back to a "genotype–severity association, not a causal hub claim."

**【Specific fix】** Add after the q-value statement in §3.10: *"This q-value is conditional on standard-error estimates that are themselves anti-conservative because of exposure–outcome sample overlap (Burgess, Davies & Thompson 2016); with only three instruments the weighted-median and Egger standard errors (0.089 and 0.111) are implausibly below the IVW standard error (0.325), so the effective family threshold is not the nominal 0.05. We therefore report q≈3×10⁻¹⁷ as a descriptive ranking, not as established significance."* Optionally, replace the weighted-median p with a permutation/leave-one-SNP-out distribution over the 3-instrument set.

---

## Issue 2 — The "min detectable OR ≈ 1.25" power claim is plausible only for the best-instrumented genes and contradicts the gene that produced the headline result

**【Problem】** The stated minimum detectable OR (≈1.25 at 80% power, α = 0.05) is an under-generic figure that materially understates the detection threshold for CD74, the very gene carrying the only family-significant finding.

**【Evidence】** I recomputed the 80%-power minimum detectable OR per gene on the primary outcome as |β| = (z₀.₉₇₅ + z₀.₈₀) × SE_IVW, then OR = exp(|β|), using the IVW SEs in `10_genetics_mr_outcome5086_28ddeath.csv`: CD74 SE = 0.3120 → MDO = **2.40**; HAVCR2 SE = 0.1180 → **1.39**; HLA-DQA1 SE = 0.0708 → **1.22**; CD14 SE = 0.0640 → **1.20**; FIS1 SE = 0.0523 → **1.16**. For CD74 critical care (SE = 0.3250) the MDO is **2.49**, while the observed OR is 2.22 — i.e. the observed effect lies *below* the 80%-power detection threshold, so the result is under-powered and its significance is fragile. The global "≈1.25" is only representative of FIS1/HLA-DQA1/CD14; it is wrong by ~2× for CD74.

**【Why it matters】** The abstract and §2.10 use "≈1.25" to bound the null interpretation. For CD74 this overstates power by roughly a factor of two and hides that the headline signal is statistically under-powered even on its own terms, which compounds Issue 1.

**【Specific fix】** Replace the single sentence in §2.10/§5 with: *"Per-gene 80%-power minimum detectable ORs (α = 0.05) on the primary outcome were FIS1 1.16, CD14 1.20, HLA-DQA1 1.22, HAVCR2 1.39 and CD74 2.40 (CD74 critical-care 2.49); the retained instruments therefore leave CD74 and HAVCR2 under-powered for per-SD ORs below ~1.4–2.4."*

---

## Issue 3 — Candidate-gene circularity: the MR genes were selected on the basis of the very outcome they are then tested against

**【Problem】** The six MR candidate genes were chosen because they are expression-associated with the sepsis endotype and 28-day mortality in GSE65682, then Mendelian randomisation tested their causal effect on sepsis outcomes — a selection-on-outcome that the pre-specified 45-test family does not correct.

**【Evidence】** §2.5–§2.10: hubs are the output of Mars1-DEG ∩ immune set ∩ tri-method ML consensus on 28-day-survival-associated genes; §3.10 then runs MR on "the six candidate genes … on sepsis 28-day death." The candidates are therefore enriched for true outcome association by construction. Limitation 10 ("Selection-chain family-wise error not controlled") names the hub-discovery chain but does not identify this MR-specific circularity.

**【Why it matters】** Selecting instruments on the basis of outcome association can inflate the prior probability of a true MR effect (winner's curse) or, conversely, mask nulls; either way it means the "null MR" conclusion is not a clean independent test of the same genes the prognostic claim rests on. It does not invalidate the honest null interpretation, but it should be stated as a structural limit on what the MR layer can weigh.

**【Specific fix】** Add to §5 (limitations): *"The MR candidate genes were themselves selected for expression association with the sepsis endotype and 28-day mortality in GSE65682, so the MR tests are not fully independent of the discovery outcome; this circularity is a structural limit on how strongly the MR null can weigh against the expression-level findings and should be broken by an independent, outcome-blind candidate set in replication."*

---

## Issue 4 (minor) — Several retained instruments are weak (F 30–46) and sit in the MHC LD region

**【Problem】** The F>10 rule is satisfied, but the lower tail of instrument strength is close to the floor and concentrated in the MHC region for CD74/CD14/HAVCR2.

**【Evidence】** `10_genetics_mr_harmonised.csv`: minimum F = 30.69 (rs12478601, CD74); CD14 has three SNPs at F = 43.0–46.5 and HAVCR2 four at F = 33.0–45.4. CD74 median F = 35.4. The stated "median F 35–168" is accurate as a cross-gene range but the lower bound is near the 10 floor.

**【Why it matters】** F just above 10 can still leave MR-Egger biased; a stricter F>30 screen or a leave-one-SNP-out sensitivity would harden the "instrument strength adequate" claim, especially for CD74.

**【Specific fix】** Add a sensitivity row to `10_mr_bh_family.csv` (or a sentence in §3.10): *"Repeating the CD74/HAVCR2/CD14 analyses after excluding SNPs with F<30 (drop rs12478601, rs148008812, rs6782228, rs424971, rs34856868, rs6891966, rs7911264, rs116560088, rs2617170, rs13401811, rs9266629) left the directions unchanged,"* or state explicitly that no instrument fell below F>30 for the primary outcome.

---

## Issue 5 (minor) — The DCA quantitative table is too thin to audit the range/convergence claims

**【Problem】** The deposited DCA file contains only three thresholds, so the manuscript's claims about the NB range and convergence point are not directly auditable from the data.

**【Evidence】** `09_ext_calibration_dca.csv` carries only `nb_thr0.20 = 0.3632`, `nb_thr0.30 = 0.2844`, `nb_thr0.50 = 0.0755`. The text (manuscript line 117) asserts NB>0 "across roughly the 0.10–0.75 threshold range" and convergence "at high thresholds (≥ ~0.77)"; these come from the figure, not the CSV.

**【Why it matters】** A reader (or this auditor) cannot verify the 0.10–0.75 span or the 0.77 convergence without re-running the decision-curve code; this is a data-availability gap, not a numerical error (the three deposited points match the text).

**【Specific fix】** Deposit the full threshold grid (e.g., 0.05–0.95 step 0.05) as additional columns in `09_ext_calibration_dca.csv`, or as a companion CSV, and cite it where the range/convergence are claimed.

---

## § Stands up (verified correct, not just claimed)

1. **Egger p-values correctly use the t(nsnp−2) distribution, not normal.** I recomputed all 15 Egger rows across the three outcome files; every reported p matches `2·t.sf(|β/se|, nsnp−2)` to <1e-4. The contrast is dramatic: CD74 susceptibility would be p = 1.65×10⁻⁴ under a normal distribution but is correctly 0.165 under t(df=1); CD74 critical-care would be 6.6×10⁻¹³ under normal but is correctly 0.088. This is a genuine, well-executed correction.
2. **Instrument strength and counts are exactly as stated.** All 27 retained SNPs have F between 30.69 and 2789.49, all >10; per-gene counts CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8; FCGR3A excluded at 2 instruments. Matches §2.10 and `10_genetics_mr_harmonised.csv`.
3. **Multiplicity is honestly reported.** Of 45 tests only one is family-significant (CD74 critical-care weighted median) and it is directionally *reversed* versus the Mars1 expression model; primary-outcome IVW P values are all ≥ 0.236 (minimum 0.236 at CD14); IVW is correctly designated the primary estimator. Matches `10_mr_bh_family.csv`.
4. **Sample-overlap bias direction is stated correctly.** §2.10/§3.10 correctly describe bias toward the non-causal observational association, SE shrinkage, and inflated type-I error, and correctly flag the most "significant" result as most vulnerable. The Burgess–Davies–Thompson reference is the right one.
5. **External-validation keys are separated, not conflated.** AUC 0.638 (95% CI 0.532–0.748) is `auc_EMTAB4451_orientedSum` (09_external_validation.csv); the L1-locked 0.585 is `auc_EMTAB4451_external_locked` (a different key). The IRG benchmark 0.604 is a single point estimate with no CI, and the manuscript honestly frames "the IRG point estimate falls within the signature 95% CI" without a formal difference test (§3.4, §3.5).
6. **Calibration/DCA numbers match and the manuscript does not overclaim.** slope = 0.5028 (≈0.50), intercept = −0.0382 (≈−0.04), NB 0.3632@0.20 / 0.2844@0.30 / 0.0755@0.50 all match `09_ext_calibration_dca.csv`; the text explicitly states NB converges to zero at ≥~0.77 rather than claiming positive benefit across all thresholds. Good calibration-honesty.
7. **Prognosis-signature caveats are already stated.** The optimistic within-cohort CV AUC (0.659 vs external 0.638), the events-per-variable of 3.8 (114 deaths / 30 genes), and the selection-chain FWER (limitation 10) are all disclosed — consistent with a credible, self-aware prognosis claim.

---

## § Questions for the authors

- Can you supply the per-SNP Wald ratios (β_YZ, β_XZ, their SEs) for the CD74 critical-care analysis so the weighted-median and Egger SEs (0.089, 0.111) can be checked independently against the three instruments?
- Was the Burgess–Davies–Thompson overlap estimator actually run, or only acknowledged? If not run, please add it as a sensitivity analysis or re-label the family q as conditional on uncorrected, anti-conservative SEs.
- Can the candidate-gene set be selected independently of the sepsis outcome (e.g., by prior literature) to break the circularity in Issue 3, or can you at least quantify winner's-curse inflation with a permutation/leave-out check?
- Please deposit the full DCA threshold grid (0.05–0.95, step 0.05) so the 0.10–0.75 range and 0.77 convergence claims are auditable.

---

## § What I actually checked

**Files read:** `05_reports/manuscript.md` (whole); `03_results/10_mr_bh_family.csv`; `10_genetics_mr_outcome5086_28ddeath.csv`; `10_genetics_mr_outcome4982_criticalcare.csv`; `10_genetics_mr.csv` (susceptibility); `10_genetics_mr_harmonised.csv`; `09_ext_calibration_dca.csv`; `09_external_validation.csv`; `09_external_validation_coef.json`; `01_data/GSE65682/GSE65682_pheno.csv`; `02_scripts/python/_recompute_mr_pvalues.py`. (I did not open any forbidden review/response/reference file.)

**Commands run (recomputation):** Python — all 15 Egger p-values via `2·t.sf(|β/se|, nsnp−2)` and the normal alternative; F-range and per-gene instrument counts from the harmonised table; BH family-significance count and the minimum primary-outcome IVW P; per-gene 80%-power minimum detectable OR on the IVW SE; external-validation key mapping; calibration/DCA values.

**Recomputed vs manuscript — matches:** Egger t-p for all 15 rows equal the reported p (max relative diff < 1e-4); F min 30.686 / max 2789.489 / 27 SNPs / per-gene counts exactly as stated; exactly 1/45 family-significant (CD74 crit-care weighted median), reversed direction; primary IVW minimum P = 0.236 (CD14); AUC 0.638 & CI 0.532–0.748 and L1-locked 0.585 from distinct keys; IRG 0.604 point-only confirmed; calibration slope 0.5028 / intercept −0.0382 / NB 0.3632, 0.2844, 0.0755 all match.

**Recomputed vs manuscript — discrepancies:** (a) The global power claim "MDO ≈ 1.25" is contradicted by gene-specific MDOs: CD74 2.40 (primary) / 2.49 (critical care), HAVCR2 1.39 — only FIS1/HLA-DQA1/CD14 sit near 1.16–1.22. (b) The weighted-median SE (0.089) for CD74 critical care is implausibly below its IVW SE (0.325); the manuscript flags the Egger SE ordering but not the weighted-median one, yet the weighted median is what drives the q≈3×10⁻¹⁷ result. (c) The DCA range/convergence claims (0.10–0.75; 0.77) are not backed by the deposited CSV, which holds only three thresholds.
