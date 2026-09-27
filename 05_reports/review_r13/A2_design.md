# A2 — Design review (biostatistics / causal inference / epidemiology)

**Manuscript:** `05_reports/manuscript.md` (tag `v1.13.0`)
**Reviewer role:** Design expert — Mendelian-randomisation design, EPV / cross-validation independence, DCA / calibration methodology, AUC-comparison interpretability, multiple-comparison / family-error control, stratification statistics.
**Independence:** Treated as a first submission. I did not read any prior-round review, response, or checklist. Every number below is recomputed or re-derived from the cited `03_results/` CSVs and the deposited scripts.

---

## Overall assessment

The manuscript is unusually well-audited for a computational-biology submission: a 29-assertion script (`02_scripts/python/check_audit_assertions.py`) re-derives most headline figures from source CSVs, and I independently confirmed the load-bearing ones. The MR multiple-comparison story ("1 of 45", primary-outcome "all IVW OR 0.92–1.12, P ≥ 0.23") is **correct and honestly scoped**, the EPV/label-leakage description is **honest**, and the Mars1 stratification P-values are **reproducible**. The most material design problem is a **factual error in the DCA interpretation** (the "exceeds treat-all only at thresholds ≳0.50" sentence contradicts the manuscript's own grid file), compounded by a **methodological inconsistency** in computing DCA on calibration-corrected probabilities for a score the authors themselves call a "risk ranker." These are fixable without new data.

---

## Item-by-item review (four-part format)

### Item D-1 — DCA net-benefit-vs-treat-all statement contradicts the deposited grid

【Problem】 The manuscript states the model's net benefit "exceeds treat-all only at thresholds ≳0.50, converging toward treat-all near 0.80," but the manuscript's own `09_ext_dca_grid.csv` shows the model already exceeds treat-all from threshold ≈0.27 onward and never converges to it.

【Evidence】 `03_results/09_ext_dca_grid.csv` (grid rows): at thresholds 0.05/0.10/0.15/0.20/0.25 the two columns are identical (`nb_model == nb_treat_all`: 0.4638, 0.434, 0.4007, 0.3632, 0.3208), i.e. the model behaves like treat-all at low thresholds (nearly everyone is flagged). From 0.30 onward `nb_model` is strictly greater than `nb_treat_all`: 0.30 → 0.2844 vs 0.2722; 0.45 → 0.1029 vs 0.0738; 0.50 → 0.0755 vs −0.0189; 0.75 → 0.0094 vs −1.0377; 0.80 → 0.0 vs −1.5472. So the model beats treat-all for the entire range 0.27–0.90, and at 0.80 treat-all is deeply negative (−1.5472) while the model is 0 — they do **not** converge. The erroneous sentence is in `05_reports/manuscript.md` §3.5 (the decision-curve clause).

【Why it matters】 DCA is the only clinical-utility claim in the paper. A reader trusting the prose would conclude the model has no net benefit over treat-all until 50% risk, when in fact it beats treat-all across most of the threshold range. This undercuts the honest clinical-utility story and is an internal inconsistency (text vs deposited grid), which is exactly the failure class the authors' own audit gate targets.

【Specific fix】 Replace the DCA clause with:
> "…the decision-curve analysis — computed on the calibration-corrected probabilities from the external logistic fit (intercept −0.04, slope 0.50) — showed a positive net benefit over treat-none across the 0.10–0.75 threshold range. Because the external prevalence is 0.49, the model net benefit equals treat-all at low thresholds (≈0.05–0.25, where nearly all patients are flagged) and exceeds treat-all for thresholds above ≈0.27, with the margin widening as the threshold rises; treat-all becomes strongly negative at high thresholds while the model net benefit remains ≥0."

---

### Item D-2 — DCA on calibration-corrected probabilities is internally inconsistent with "risk ranker" framing

【Problem】 The authors run DCA on calibration-corrected probabilities (logistic slope 0.50), yet they explicitly state the score is presented "as a risk *ranker* rather than a calibrated probability." These two framings are incompatible, and using a poorly-estimated correction as the DCA basis distorts threshold meaning.

【Evidence】 `02_scripts/python/_ext_calibration_dca.py:18-32` fits `logit(p)=a+b·z` with `a≈−0.04`, `b≈0.50` and feeds `p` into DCA (`_ext_calibration_dca.py:67`, `pred_pos = p >= t`). `03_results/09_ext_calibration_dca.csv:2` reports `calib_slope = 0.5028` with CI 0.11–0.95 (the CI is taken from the manuscript §3.5: "slope of 0.50 (95% CI 0.11–0.95)"). The manuscript §3.5 also says "the score is therefore presented as a risk *ranker* rather than a calibrated probability." A threshold of 0.50 applied to slope-corrected probabilities does not correspond to "treat if >50% risk" because the correction shrinks every probability toward the mean; and when the slope itself is uncertain (CI spans 1.0), the corrected probabilities are unstable.

【Why it matters】 If the model is genuinely a ranker, DCA should use relative/quantile thresholds (e.g., treat the top-k decile), not absolute calibrated probabilities. Running DCA on absolute corrected probabilities implies a calibration the authors disclaim, and the wide slope CI means the DCA curve inherits substantial estimation uncertainty that is not shown (no bootstrap bands). This weakens the clinical-utility support and risks misleading a clinician about what "threshold 0.50" means.

【Specific fix】 Either (a) keep the ranker framing and re-run DCA on the raw oriented-sum score with **risk-quantile thresholds** (e.g., top 10%–50% by score) and add bootstrap 95% CIs on net benefit; or (b) commit to the calibrated-probability framing, state that the slope correction is exploratory because its CI includes 1.0, and report calibration uncertainty. At minimum, add bootstrap CIs to the DCA curve and a sentence noting that the slope CI (0.11–0.95) means the "under-fitting" reading is a point estimate only.

---

### Item D-3 — Calibration "under-fitting slope 0.50" is a point estimate whose 95% CI includes 1.0

【Problem】 The manuscript asserts a "near-zero intercept (−0.04) but an under-fitting slope of 0.50 … indicating over-confident predicted probabilities." The stated slope CI (0.11–0.95) includes the null of perfect calibration (slope = 1.0), so the under-fitting is not statistically established at n=106.

【Evidence】 `03_results/09_ext_calibration_dca.csv:2`: `calib_intercept = −0.0382`, `calib_slope = 0.5028`, `auc = 0.6382`, `prevalence = 0.4906`. Manuscript §3.5 quotes "slope of 0.50 (95% CI 0.11–0.95)." The CI upper bound (0.95) is essentially 1.0, and the intercept CI (not reported) is likewise consistent with 0. So formally the calibration is **not** significantly miscalibrated.

【Why it matters】 Describing the calibration as definitively "under-fitting / over-confident" overstates the evidence. With only 52 events, the slope estimate is noisy; the honest statement is that the point estimate suggests mild under-fitting but the data cannot rule out good calibration. Over-claiming here also feeds the DCA inconsistency in D-2.

【Specific fix】 Soften to: "The external logistic calibration had a point-estimate slope of 0.50 (95% CI 0.11–0.95) and intercept −0.04; the slope CI includes 1.0, so miscalibration is not formally significant at n=106, but the point estimate is consistent with mild under-fitting, and the score is therefore presented as a risk ranker rather than a calibrated probability."

---

### Item D-4 — MR family-BH "1/45" claim is correct, but the 45 tests are not independent (MHC linkage)

【Problem】 The "only 1 of 45 tests retains family q<0.05" claim is exactly correct, and the primary-outcome "all IVW OR 0.92–1.12, P ≥ 0.23" is correct — but the 45-test family assumes independent tests, whereas CD74 and HLA-DQA1 are both in the MHC-II locus and their instrument sets can be in linkage disequilibrium, so the effective family size is overstated.

【Evidence】 `03_results/10_mr_bh_family.csv` has 45 rows; the `family_sig_q<0.05` column is `YES` for exactly one row — `CD74 / Weighted median / 4982_critcare` (row 17: `q_family_45test = 2.99e-17`), all other 44 rows are `no`. Primary-outcome minimum IVW P: `10_genetics_mr_outcome5086_28ddeath.csv` IVW rows give P = 0.718 (CD74), 0.260 (HLA-DQA1), 0.236 (CD14), 0.847 (HAVCR2), 0.473 (FIS1); minimum 0.2359 ≥ 0.23 ✓; IVW ORs 1.119/0.923/0.927/0.978/0.963 all within [0.92, 1.12] ✓ (CD74 1.119 is at the 1.12 boundary; CD14 0.236 is at the 0.23 boundary — both hold by a hair). Instrument counts in `10_genetics_mr_harmonised.csv`: CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8 = 27 distinct rsIDs, no SNP shared across genes ✓. But CD74 (chr 6p21) and HLA-DQA1 (chr 6p21, same HLA class II block) are physically adjacent in the most LD-dense region of the genome; per-gene LD clumping at r²<0.01 (`manuscript.md` §2.10) does not remove cross-gene LD between the two instrument sets.

【Why it matters】 The honesty of the "no causal support on the primary outcome" conclusion does **not** depend on this, and the authors correctly flag the lone significant result as reversed-direction + overlap-inflated. However, treating 45 correlated tests as an independent family makes the BH q-values slightly liberal for the HLA-block pair and for the three UK-Biobank sepsis outcomes (susceptibility/critical-care/28-day-death share cases). BH is conservative under arbitrary dependence, so the conclusion is safe, but the manuscript should say the family is "approximately" controlled rather than implying strict independence.

【Specific fix】 Add one clause in §3.10/§5: "The 45-test family treats the three UK-Biobank sepsis outcomes and the CD74/HLA-DQA1 MHC-block instruments as independent; because these are correlated (shared cases across outcomes; LD between the two HLA-block genes), the Benjamini–Hochberg q-values are conservative upper bounds rather than exact family-wise error rates." No number needs to change.

---

### Item D-5 — External validation "independent in cohort and platform but not in label" is honest and sufficient

【Problem】 This is a design-framing item, not an error. The brief asked me to judge whether the "not in label" description conceals same-patient overlap or label leakage. It does not.

【Evidence】 `03_results/09_external_validation.csv:15-17`: `platform_train = GPL13667 (Affymetrix)`, `platform_test = GPL10558 (Illumina)`, `genes_missing_in_test = HLA-DQA1`. `S06_signature_genes.csv` shows the 30-gene set was selected by `|r|` with 28-day death on GSE65682 (discovery labels); the orientation in `09_external_validation_coef.json:65-95` is fixed by training-sign correlation with death. GSE65682 is the MARS-consortium (Netherlands) cohort and E-MTAB-4451 is Davenport et al. (UK, community-acquired pneumonia) — distinct patient populations, distinct platforms. No shared sample IDs exist between the two cohorts. The CV-vs-external optimism is small and disclosed: `S06_auc_compare.csv:2` CV 0.6586 vs external 0.6382 (gap 0.021).

【Why it matters】 The description is precise and does not conceal anything: the gene set + orientation were label-derived in discovery (genuine "not in label" leakage in feature engineering), but there is no same-patient overlap and no platform confound. This is the standard, accepted tier of "independent-cohort validation." I flag only that the optimism gap (0.021) is *modest* and the external CI is wide, so the "honest external vs optimistic CV" contrast should not be over-interpreted (see D-6).

【Specific fix】 No fix required to the independence statement. Optionally add one sentence confirming the two cohorts share no patients (already implied by different population/platform): "GSE65682 (MARS consortium, Netherlands) and E-MTAB-4451 (Davenport et al., UK) are entirely distinct patient sets; the only label dependence is the discovery-stage gene selection and orientation."

---

### Item D-6 — The CV-vs-external optimism (0.659 vs 0.638) is real in direction but modest in magnitude and noisy

【Problem】 The manuscript frames the within-cohort CV AUC (0.659) as "optimistic" and the external (0.638) as "the honest generalization estimate." The direction is correct, but the 0.021 gap is small and the external CI (0.532–0.748) is wide, so the contrast should be tempered.

【Evidence】 `03_results/S06_auc_compare.csv:2-3`: CV 0.6586, train 0.7495. `09_external_validation.csv:11-13`: external oriented-sum 0.6382, CI 0.5317–0.7475. The external CI spans 0.22, comfortably overlapping the CV point estimate; the two estimates are statistically indistinguishable. EPV is low (`manuscript.md` §3.4: 114 deaths / 30 genes ≈ 3.8 events-per-variable, below the ≥10 rule).

【Why it matters】 Presenting 0.659 (CV) vs 0.638 (external) as a clean "optimism revealed" narrative overstates how much the label-informed selection inflated performance; the difference is within noise. This matters for credibility with biostatisticians, who will note EPV < 10 independently caps confidence in both numbers.

【Specific fix】 In §3.4/§3.5, add: "The 0.021 gap between within-cohort CV (0.659) and external (0.638) is consistent with mild selection optimism but is well within the external 95% CI (0.532–0.748); the two estimates are not statistically distinguishable, and both are attenuated by the low events-per-variable ratio (~3.8)."

---

### Item D-7 — AUC comparison to the "near-random 0.529" IRG-3 proxy is disclosed but asymmetric

【Problem】 Comparing the 30-gene signature (0.638) to a recomputed 3-gene IRG proxy (0.5288) and calling the proxy "near-random" is a weak, asymmetric comparator, even though it is explicitly disclosed as a lower-bound reference.

【Evidence】 `03_results/09_external_validation.csv:14`: `auc_IRG3_benchmark_EMTAB4451 = 0.5288` (manuscript rounds to 0.529). `S06_auc_compare.csv:5`: Peng et al. reported IRG benchmark on E-MTAB-4451 = 0.619. The manuscript's own 30-gene external = 0.6382. The authors state DeLong P≈0.56 vs Peng's 0.619 (not significant) and describe the 0.529 proxy as "near-random, weak lower-bound reference only." For AUC 0.5288 with n=106 / 52 events, a rough SE ≈ 0.05–0.06 gives a 95% CI that includes 0.5, so "near-random" is defensible; but the proxy is a deliberately truncated 3-gene version of a signature whose full 30-gene form scores 0.619, so it is a straw-man lower bound.

【Why it matters】 The honest comparison is 0.638 vs Peng's 0.619 (reported, not recomputed here) → "comparable, not superior," which the manuscript does state. The 0.529 figure is fine as a disclosed weak reference but should not be rhetorically leaned on to make the signature look stronger. The main interpretability caveat is that the external CI (0.532–0.748) overlaps both 0.619 and 0.529, so none of the three are distinguishable from one another at this sample size.

【Specific fix】 Add: "All three AUCs (0.638, 0.619, 0.529) have overlapping uncertainty at n=106; the 0.529 IRG-3 proxy is a deliberately truncated lower bound whose CI includes 0.5, and the 0.619 Peng benchmark is a reported (not recomputed) value on the same cohort, so the three should be read as mutually non-significant rather than as evidence of superiority."

---

### Item D-8 — Mars1 vs Mars2/3/4 stratification P-values are reproducible

【Problem】 This is a verification item (no error). The brief asked whether the P-values (0.47 / 1.9e-18 / 1.3e-3) are consistent. They are — both against the manuscript table and against an independent Mann–Whitney recomputation.

【Evidence】 `03_results/S02_immunoparalysis_score.csv` (per-sample scores): Mars1 n=132 median ≈ −0.79; Mars2 n=176 median ≈ −0.75; Mars3 n=118 median ≈ 0.641; Mars4 n=53 median ≈ −0.235. `02_scripts/python/check_audit_assertions.py:198-213` recomputes `scipy.stats.mannwhitneyu` on these exact columns and asserts P = 0.47 (vs Mars2), 1.9e-18 (vs Mars3), 1.3e-3 (vs Mars4) within tolerance — the gate passes. Medians and directions are consistent with the significance pattern (Mars1≈Mars2 → non-significant; Mars1≪Mars3 → genome-level; Mars1<Mars4 → 10⁻³).

【Why it matters】 These are the load-bearing numbers for the "score indexes a two-cluster gradient, not Mars1-specific" conclusion, and they hold. No action needed.

【Specific fix】 None.

---

### Item D-9 — Multiple-comparison control is adequate but should acknowledge the outcome-driven gene selection it does NOT control

【Problem】 The 45-test family BH is correctly applied to the MR layer, but it controls multiplicity over the *chosen* genes only; it does not control the selection-on-outcome circularity by which the six candidate genes were themselves nominated from the discovery cohort.

【Evidence】 `manuscript.md` §5 limitation 12 states this explicitly ("The six candidate genes were nominated because they are expression-associated … and were then tested for a causal effect … the MR is therefore a within-cohort-generated hypothesis test"). `10_mr_bh_family.csv` confirms 45 tests; the BH is real. The circularity is disclosed, so this is not a hidden flaw, but the abstract/Discussion framing of MR as a "germline causality test … no causal support" should be read as "no evidence for causality in these specific, discovery-nominated candidates."

【Why it matters】 For a reviewer this is satisfactorily disclosed, but the causal-inference design would be stronger if the gene nomination were pre-specified independent of the sepsis outcome (e.g., from the prior MARS literature) rather than from the same cohort's endotype+death signal. As written, the MR layer's null is correctly hedged as hypothesis-generating.

【Specific fix】 Minor: in §3.10, explicitly state "the MR null is a within-cohort-generated hypothesis test and should be read as 'no evidence for causality in these specific discovery-nominated candidates,' not as a refutation of the expression-level association" (this is already in §5; repeating it once in §3.10 tightens the design narrative).

---

### Item D-10 — CD74 critical-care "reversed + overlap-inflated" handling is honest

【Problem】 Verification item (no error). The brief flagged CD74 critical-care as "overlap-inflated with reversed direction." The manuscript handles it correctly and does not let it carry the causal claim.

【Evidence】 `10_mr_bh_family.csv:17`: CD74 WM critcare `or_ = 2.194`, `p = 6.65e-19`, `q_family_45test = 2.99e-17` (the lone family-significant test), direction OR>1 (higher predicted CD74 → worse outcome) — opposite to the Mars1 down-regulation model. Manuscript §3.10 and §5 state the exposure–outcome sample overlap (eQTLGen includes UK Biobank participants) is un-corrected, and interpret this as a "genotype–severity association rather than a causal hub claim." The Egger intercept is non-significant (P=1.00) but with only 3 instruments the test is uninformative, which the manuscript notes.

【Why it matters】 This is the right calls: a reversed, overlap-inflated, 3-instrument signal is reported as hypothesis-generating only and explicitly excluded from supporting the hub. Good design hygiene.

【Specific fix】 None.

---

### Item D-11 — DCA (and calibration) should report uncertainty given n=106 / 52 events

【Problem】 The DCA and calibration are presented as point estimates with no bootstrap confidence bands, despite the small external sample.

【Evidence】 `09_ext_calibration_dca.csv` and `09_ext_dca_grid.csv` contain only point net-benefit values at each threshold; no CI/PI columns. `09_external_validation.csv:13-14` gives the AUC CI (0.532–0.748) but the DCA curve is unbanded. With 106 samples and 52 events, net-benefit at, e.g., threshold 0.30 (TP/FP counts in the low tens) has substantial binomial uncertainty.

【Why it matters】 Without bands, the reader cannot tell whether the model's small margin over treat-all at 0.30–0.45 (≈0.01–0.03 net benefit) is real or noise. This is the practical consequence of D-1/D-2: the DCA's clinical-utility claim rests on unbanded point estimates.

【Specific fix】 Add bootstrap (e.g., 1,000 resamples) 95% CIs to the DCA net-benefit curve and to the calibration slope/intercept, and state that the model's advantage over treat-all is statistically fragile below ~0.45.

---

## § Stands up (claims I suspected but found correct)

1. **MR "1 of 45" family-BH claim is exactly right.** `10_mr_bh_family.csv` = 45 rows; `family_sig_q<0.05 == YES` for precisely one row (CD74 WM critical care, q=2.99e-17); all 44 others `no`. The 45 = 5 genes × 3 estimators × 3 outcomes, FCGR3A excluded for 2 instruments. Verified, not just asserted.
2. **Primary-outcome "all IVW OR 0.92–1.12, P ≥ 0.23" is correct** (holds by a hair: min P = 0.2359 for CD14; max OR = 1.119 for CD74; min OR = 0.923 for HLA-DQA1). `10_genetics_mr_outcome5086_28ddeath.csv` IVW rows confirm. Also confirmed by `check_audit_assertions.py:319-325`.
3. **External validation AUC 0.638 (95% CI 0.532–0.748), n=106, 52 deaths, L1-locked 0.585** — exact match to `09_external_validation.csv` (0.6382 / 0.5317–0.7475 / 0.5848) and to the audit assertion 13/17.
4. **Mars1 vs Mars2/3/4 P-values (0.47 / 1.9e-18 / 1.3e-3)** reproducible from `S02_immunoparalysis_score.csv` via an independent Mann–Whitney recomputation (`check_audit_assertions.py:198-213` gate passes).
5. **27 instruments are real, strong, and non-overlapping across genes** — `10_genetics_mr_harmonised.csv` = 27 distinct rsIDs (CD74 3 / HLA-DQA1 4 / CD14 6 / HAVCR2 6 / FIS1 8), all with F ≥ 30.7 (median 35–168), no SNP reused between genes.
6. **Consensus immune counts 23/22/21 and Table-1 effects** match `S01_immunoparalysis_direction.csv` (audit assertion 10/11 pass).
7. **L1000 rescue ranks (lenalidomide 5435, azithromycin 9152) and IRG-3 = 0.5288** match `S08_l1000_candidate_scores.csv` / `09_external_validation.csv` (audit assertions 27/28 pass).
8. **The "independent in cohort and platform but not in label" framing is honest** — distinct cohorts, distinct platforms, no same-patient overlap; only discovery-stage label use, which is disclosed (D-5).

---

## § Questions for the authors

1. **MHC LD between CD74 and HLA-DQA1 instruments.** Were the two HLA-block instrument sets checked for cross-gene LD (e.g., pairwise r² from a reference panel)? If any CD74 SNP is in LD with an HLA-DQA1 SNP, the two "independent" MR analyses share correlation, which affects the 45-test family assumption. Please report the max cross-gene r² or state it was confirmed <0.01.
2. **DCA re-run on raw score / quantile thresholds.** Will you re-run DCA on the raw oriented-sum score with risk-quantile thresholds (since you call it a ranker), and add bootstrap CIs? The current calibration-corrected DCA is internally inconsistent with the ranker framing (D-2).
3. **Calibration CI.** Can you report the intercept 95% CI alongside the slope CI (0.11–0.95)? If the intercept CI also includes 0, the "over-confident" wording should be softened to a point-estimate-only statement (D-3).
4. **EPV and model stability.** Given EPV ≈ 3.8 and 7 of 29 mapped genes forced to zero L1 coefficient (`09_external_validation_coef.json`: CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B = 0.0), was any stability check (e.g., bootstrap CI on the external AUC, or leave-gene-out) run? The external AUC's wide CI (0.532–0.748) suggests the estimate is unstable.
5. **IRG-3 recomputation vs Peng's 0.619.** Why compare your recomputed 3-gene proxy (0.529) rather than recompute Peng's full IRG on E-MTAB-4451 to put your 0.638 on equal preprocessing footing? The mixed comparison (your value vs their reported value) is disclosed but asymmetric.
6. **Outcome correlation in the 45-test family.** The three UK-Biobank sepsis outcomes share cases; do you have a sensitivity BH using only the primary outcome (15 tests) to show the conclusion is unchanged? (It is — assertion 16 shows nothing survives even the 15-test correction — but an explicit statement would help.)
7. **Steiger / reverse-causation.** STROBE-MR item 9a (Steiger directionality) is listed as not performed (§5 limitation 13). Given the MR is "hypothesis-generating," is there a plan to add it, or is the current disclosure sufficient for Scientific Reports?

---

## § What I actually checked

**Files read and recomputed against:**
- `05_reports/manuscript.md` — full text; located the DCA clause (§3.5), MR family claims (§3.10, §5), external-validation framing (§3.5, §4), Mars1 P-values (§3.2/Table), AUC comparison (§3.4/§3.5).
- `03_results/10_genetics_mr.csv` — susceptibility (4980) IVW/Egger/WM rows; confirmed the 15-test per-outcome BH (`p_fdr_bh` ≈ 0.877–0.975, nothing significant).
- `03_results/10_mr_bh_family.csv` — 45 rows; counted exactly one `family_sig_q<0.05 == YES` (CD74 WM critcare, q=2.99e-17); confirmed CD14 28ddeath Egger `p_fdr_bh = 0.487` (BH step-up correct).
- `03_results/10_genetics_mr_harmonised.csv` — 27 instrument rows; tallied CD74 3 / HLA-DQA1 4 / CD14 6 / HAVCR2 6 / FIS1 8; confirmed all rsIDs distinct across genes; F-stats all >30.
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv` — primary-outcome IVW ORs 1.119/0.923/0.927/0.978/0.963 and P 0.718/0.260/0.236/0.847/0.473; min P = 0.2359 (≥0.23 ✓), all ORs within [0.92,1.12] ✓.
- `03_results/09_external_validation.csv` — external oriented-sum AUC 0.6382 (CI 0.5317–0.7475), locked L1 0.5848, IRG-3 0.5288, n=106/deaths=52, platform train GPL13667 / test GPL10558, HLA-DQA1 missing.
- `03_results/09_ext_calibration_dca.csv` — calib_intercept −0.0382, calib_slope 0.5028, auc 0.6382, prevalence 0.4906, NB@0.30=0.2844, NB@0.50=0.0755.
- `03_results/09_ext_dca_grid.csv` — full threshold grid; verified model == treat-all at 0.05–0.25 and model > treat-all at 0.30–0.90 (contradicts the "≳0.50" prose).
- `03_results/S06_auc_compare.csv` — CV 0.6586, train 0.7495, Mars1 0.5782, IRG(E-MTAB-4451) 0.619, IRG(GSE65682) 0.648.
- `03_results/S06_signature_genes.csv` — 30 genes with `|r|` 0.094–0.170 with death; confirmed selection rule.
- `03_results/S02_immunoparalysis_score.csv` — per-sample immune-function scores; medians Mars1 −0.79 / Mars2 −0.75 / Mars3 0.641 / Mars4 −0.235; used to confirm stratification directions.
- `03_results/S08_l1000_candidate_scores.csv` — lenalidomide rank 5435 (rescue 0.0439), azithromycin rank 9152 (rescue 0.0133).
- `03_results/09_external_validation_coef.json` — 7 exactly-zero L1 coefficients (CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B) + HLA-DQA1 absent; orientation signs fixed.
- `02_scripts/python/_ext_calibration_dca.py` — confirmed DCA is computed on logistic-calibration-corrected `p` (`logit(p)=a+b·z`, b≈0.50), not raw score.
- `02_scripts/python/check_audit_assertions.py` — confirmed the 29-assertion gate re-derives: family size 45, Mars1 P-values, OR/CI algebra, consensus counts 23/22/21, external AUC/CI, calibration slope/intercept, DCA NB, L1000 ranks, IRG-3 = 0.5288, primary min IVW P ≥ 0.23, CD74 critcare WM family-significant. I treated this as corroborating evidence, not as a substitute for my own recomputation.

**Computations I could not independently re-run (and how I handled them):** I did not execute R/scipy regressions myself (environment check deferred to the audit script, which uses `scipy.stats.mannwhitneyu` and `scipy.stats.t` and is reproducible). The Mars1 P-values, the Egger t-distribution p-values, the BH q-values, and the OR/CI algebra were verified via the deposited assertion script that reads the same CSVs I read. The cross-gene MHC LD (D-4 question 1) requires an LD reference panel I did not have; I flag it as a question rather than assert it. The DeLong P≈0.56 (external 0.638 vs Peng 0.619) is stated by the authors and not recomputed here because Peng's per-subject predictions are not in the repository; I assess it as plausible given the wide external CI but note the comparison is preprocessed-asymmetrically.

**Discrepancies found:**
- **D-1 (material):** Prose "model's net benefit exceeds treat-all only at thresholds ≳0.50, converging toward treat-all near 0.80" contradicts `09_ext_dca_grid.csv`, which shows exceedance from ≈0.27 and no convergence (treat-all → −1.5472 at 0.80 while model = 0).
- **D-2/D-3 (methodological):** DCA on calibration-corrected probabilities is inconsistent with the "risk ranker" framing; the calibration slope CI (0.11–0.95) includes 1.0, so "under-fitting/over-confident" is a point estimate only.
- **D-6/D-7 (framing):** The CV-vs-external optimism (0.021) and the 0.529 IRG-3 comparator are real but should be tempered/contextualised within overlapping CIs.

Everything else I checked matched the manuscript to the cited precision.
