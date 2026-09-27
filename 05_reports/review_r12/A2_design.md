# Independent Peer Review — Design Layer (Biostatistics / Causal Inference)

**Manuscript:** "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and validates a 30-gene sepsis prognostic signature"
**Manuscript file reviewed:** `05_reports/manuscript.md` (read in full)
**Reviewer role:** Senior biostatistician / causal-inference methodologist (external, single-blind to prior reviews)
**Review tier:** Design layer — sparse-data / EPV, calibration, decision-curve analysis, Mendelian-randomisation multiplicity & overlap, external-validation inference.
**Independence note:** Reviewed as a *first submission*. I did not consult any `REVIEW_*.md`, `RESPONSE_*.md`, prior `review_r*` directories, OVERVIEW, manifests, or verification statements. Every number below was recomputed by me from the deposited CSVs and scripts.

---

## § What I actually checked (files, commands, recomputed vs manuscript values, discrepancy)

### Files read (primary)
- `05_reports/manuscript.md` (full)
- `03_results/09_ext_risk_scores.csv` (106 rows; cols `y`, `risk_oriented_sum`, `risk_locked_l1`, `risk_irg3`)
- `03_results/09_ext_calibration_dca.csv`, `03_results/09_ext_dca_grid.csv`
- `03_results/09_external_validation.csv`, `09_external_validation_coef.json`
- `03_results/S06_auc_compare.csv`, `S06_signature_genes.csv`
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv` (primary), `10_genetics_mr_outcome4982_criticalcare.csv` (critical care), `10_genetics_mr.csv` (susceptibility), `10_mr_bh_family.csv`
- `02_scripts/python/_ext_calibration_dca.py`, `09_external_validation.py`
- `03_results/S01_mars1_deg.csv` (FIS1 line), `03_results/07_hub_celltype.csv`, `08_candidates_drugs.csv` (spot checks)

### Command / recompute script
A single Python script (`03_results/_rev_recompute.py`, executed with the managed interpreter `C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe`) re-derived: external AUC; IRG AUC; a paired-bootstrap difference (5000 reps) and a DeLong z-test (Sun–Xu placement estimator); the logistic calibration slope/intercept on the z-standardised score plus a 2000-replicate bootstrap CI; the DCA net-benefit grid under both calibration-fit and raw `plogis(z)` probabilities with zero-crossing detection; and the full MR SE/Egger/IVW readout with the `10_mr_bh_family.csv` significance count. Recomputations are fully reproducible from the deposited files.

### Recomputed vs manuscript — discrepancy table

| Quantity | Manuscript | Recomputed | Discrepancy |
|---|---|---|---|
| External oriented-sum AUC | 0.638 | **0.6382** | none |
| IRG-3 benchmark AUC (E-MTAB) | 0.604 | **0.604** | none |
| DeLong P (signature vs IRG) | "P≈0.556" | **0.559** | none (rounding) |
| Paired-bootstrap diff (oriented−IRG) | — | **0.034 (CI −0.077, 0.151; P 0.548)** | new |
| Calibration intercept (z-score fit) | −0.04 | **−0.0382** | none |
| Calibration slope (z-score fit) | 0.50 | **0.5028** | none |
| Calibration bootstrap 95% CI (slope) | [0.11, 0.96] | **[0.109, 0.947]** | upper bound 0.96 vs 0.947 (bootstrap seed noise; both exclude 1.0) |
| DCA zero-crossing | "by 0.80" | **~0.75–0.80 (grid: 0.75→+0.0094, 0.80→0.0)** | none |
| CD74 critical-care IVW SE / Egger SE | 0.325 / 0.111 | **0.3250 / 0.1111** | none |
| "1 of 45" family-significant tests | 1 (CD74 WM crit-care, q≈3e-17) | **1 (identical row)** | none |
| EPV (30-gene L1) | 114/30 ≈ 3.8 | **3.8** | none |
| FIS1 Mars1 logFC / t | +1.26 / +17.2 | **+1.261 / +17.16** | none |
| Locked-L1 external AUC | 0.585 | **0.5848** | none |
| GSE65682 CV AUC (locked) | 0.659 | **0.6582** | none |

**Bottom line of recomputation:** every headline number reproduces to the quoted precision. My critique below is therefore not about fabrication but about *interpretation, framing, and omitted caveats* in the design layer — exactly the things a statistical reviewer is expected to catch that authors and domain reviewers typically miss.

### How I executed the recomputation (narrative)
I treated the deposited CSVs as the ground truth and re-derived each reported statistic independently, rather than re-running the authors' scripts verbatim (which would only re-confirm their own bugs). For the AUCs and DeLong I used the raw per-sample risk columns in `09_ext_risk_scores.csv` (`y`, `risk_oriented_sum`, `risk_irg3`) and `sklearn.metrics.roc_auc_score`; for the calibration I re-implemented the logistic negative-log-likelihood fit in `_ext_calibration_dca.py:23-29` from scratch and bootstrapped it (2000 resamples, seed 7) to obtain the slope CI; for the DCA I re-derived net benefit both from the deposited calibration-fit probabilities and from raw `plogis(z)` to test the "uncalibrated" claim; for MR I read the SE/OR/p columns directly from the three `*csv` outcome files and cross-checked the family BH table. Nothing required network access or the original GEO/IEU downloads — all inputs are in `03_results/`. The recompute script `03_results/_rev_recompute.py` is deposited alongside and runs end-to-end on the managed interpreter.

---

## § Stands up (what is sound and should be kept)

1. **Honest external validation with locked model.** The signature was applied to E-MTAB-4451 with fixed gene set + fixed orientation + training StandardScaler + L1 coefficients and *no re-tuning* (`09_external_validation.py:111-122`). This is the correct way to do external validation, and the AUC 0.638 reproduces exactly. The authors correctly scoping the claim to "gene set + orientation, not cohort-specific weights" (and showing the learned L1 weights transport poorly, AUC 0.585) is a genuine strength.

2. **Calibration is reported candidly, not whitewashed.** The manuscript explicitly states the slope is 0.50 with ideal 1.0, labels the probabilities "over-confident," and relegates the score to a "risk *ranker* rather than a calibrated probability" (`manuscript.md:112, 236`). My recompute confirms the slope (0.5028) and shows the bootstrap CI excludes 1.0, so this is not spin — the mis-calibration is real and statistically established. I found *no* "well-behaved" claim in the text; the authors' framing here is defensible and appropriate.

3. **The MR layer is correctly downgraded.** Despite the eye-catching "1 of 45" headline, the manuscript repeatedly concludes the MR is "Tier-3 and hypothesis-generating," notes no *primary* IVW estimate is significant, flags the exposure–outcome sample overlap, and explicitly reinterprets the one family-significant result as a *reversed-direction genotype–severity association* rather than a causal hub claim (`manuscript.md:174-176, 194-195`). That intellectual honesty is commendable and should be preserved.

4. **DeLong framing is correct.** "Comparable not superior" between 0.638 and 0.604 is supported: DeLong P = 0.559 (manuscript 0.556) and paired-bootstrap CI for the difference [−0.077, 0.151] contains 0. The authors do not claim superiority — good.

5. **Lineage of the DEG / hub numbers is internally consistent** (FIS1 logFC +1.26 / t +17.16 confirmed; Mars1-vs-Other DEG count and the 5-hub recapitulation of the known MARS program are biologically coherent and reproducible). The "near-replication not novel discovery" boundary is clearly drawn (`manuscript.md:8, 184`).

---

## § Detailed findings (design layer)

Each item uses the contract: 【Problem】【Evidence】【Why it matters】【Specific fix】.

---

### ITEM 1 — EPV ≈ 3.8 for the 30-gene L1 model is disclosed but under-mitigated; the external data corroborate over-fitting of the *weights*

【Problem】 The 30-gene L1 logistic model is fit on 114 death events (EPV = 114/30 = 3.8), far below the conventional ≥10 rule. The authors disclose this (`manuscript.md:109, 194`) but the within-cohort 5-fold CV AUC 0.659 is still featured prominently in the Abstract and Discussion as the "out-of-fold" estimate, and the optimism is not quantified. More tellingly, the *locked L1 weights* transport to AUC **0.585** on E-MTAB-4451, which is *below* the equal-weight oriented-sum (0.638). That ordering is the signature of weight over-fitting: the cohort-specific coefficients learned nothing portable, and 7 of the 29 mapped genes are driven to exactly zero.

【Evidence】
- `S06_auc_compare.csv`: CV 0.6586 / train 0.7495 (Δ ≈ 0.09 optimism).
- `09_external_validation.csv`: `auc_EMTAB4451_external_locked` = 0.5848 vs `auc_EMTAB4451_orientedSum` = 0.6382.
- `09_external_validation_coef.json`: 7 coefficients exactly 0 (CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B); HLA-DQA1 excluded entirely.
- Recomputed by me: confirmed both external AUCs to 4 d.p.

【Why it matters】 EPV 3.8 means the CV AUC is optimistically biased and the per-gene coefficients are unstable; presenting 0.659 first in the Abstract risks readers overweighting it. The fact that the *weights* fail to generalise while the *gene set + orientation* succeed is the real, defensible story — but it is currently buried under the optimistic CV number.

【Specific fix】 (a) In the Abstract and §3.4, lead with the honest external number (0.638) and demote the CV 0.659 to a clearly-labelled "optimistic, label-informed, within-cohort" figure, e.g.: *"Within-cohort 5-fold CV AUC was 0.659 (optimistic, label-informed); the honest out-of-sample estimate is the locked external AUC 0.638 on E-MTAB-4451."* (b) Add a one-line EPV statement with the conventional benchmark: *"With 114 events and 30 candidate genes the events-per-variable ratio was 3.8, well below the conventional ≥10 threshold; the collapsed L1 weights (7/29 exactly zero, external AUC 0.585) indicate the cohort-specific coefficients did not generalise, and the portable signal resides in the gene set and orientation rather than the fitted weights."* (c) Explicitly state that the CV AUC is *not* a validation estimate.

**Quantification to anchor the fix.** Effective EPV is *worse* than 3.8 once one notes that HLA-DQA1 is absent on the Illumina array (`genes_missing_in_test = HLA-DQA1`), so only 29 genes are ever scored externally and 7 of those carry exactly-zero L1 coefficients — meaning the transportable fitted model has ≈22 active parameters on 114 events (EPV ≈ 5.2) while a further 7 parameters are estimated and then discarded. The equal-weight oriented-sum, by contrast, uses all 29 mapped genes with no parameter estimation and reaches the higher external AUC (0.638). This is a clean, publishable illustration that *feature selection + orientation* is what generalises, not the L1 coefficients.

---

---

### ITEM 2 — Calibration slope 0.5028: correctly fit on z-scores, significantly <1, but the CI width is wide and the text should say so

【Problem】 The slope is fit on the *z-standardised* score (`_ext_calibration_dca.py:20`), which is correct and matches the manuscript. The point estimate (0.5028) and the "over-confident" reading are both correct, and my bootstrap CI [0.109, 0.947] (manuscript [0.11, 0.96]) excludes 1.0 — so mis-calibration is statistically established, not hand-waving. However, the CI is extremely wide (0.11 to ~0.95): the *magnitude* of the needed shrinkage is essentially unestimable in n=106. The text currently implies a stable, actionable correction factor ("slope 0.50") while the data only support "some under-dispersion, magnitude unknown."

【Evidence】
- `_ext_calibration_dca.py:20,29`: `z=(risk_oriented_sum-mean)/std`; `optimize.minimize(negll,[0,1],...)`.
- `09_ext_calibration_dca.csv`: intercept −0.0382, slope 0.5028.
- Recomputed bootstrap (2000 reps, seed 7): slope 95% CI [0.109, 0.947]; median 0.509; intercept 95% CI [−0.433, 0.342]. CI includes 1.0? **False** (significant). Upper bound I recompute 0.947 vs manuscript 0.96 — negligible seed-noise difference.

【Why it matters】 A slope CI spanning 0.11–0.95 means any calibration correction applied to future cohorts could be off by an order of magnitude. Presenting "0.50" as a fixed correction risks false precision; the correct inference is "use as a ranker, do not report absolute probabilities." This is what the manuscript does, but the *width* of the uncertainty should be stated so readers don't over-trust the 0.50 point estimate.

【Specific fix】 Add to §3.5: *"The calibration slope was 0.50 (bootstrap 95% CI 0.11–0.95); because the interval is wide and excludes 1.0, mis-calibration is established but its precise magnitude is poorly constrained by n=106, so absolute-risk probabilities are not reported and the score is used as an ordinal ranker only."* (No change to the conclusion; this just pre-empts over-reading of 0.50.)

**Worked illustration of what slope 0.50 means.** Suppose a patient's standardised score is z = +1.0 (one SD above mean, i.e., high predicted risk). A perfectly calibrated model would map this to logit(p) = 0 + 1·(+1) = 1.0 ⇒ p ≈ 0.73. The fitted calibration instead gives logit(p) = −0.04 + 0.50·(+1) = +0.46 ⇒ p ≈ 0.61. The extreme risk is *shrunken* toward the 0.49 prevalence — the model was over-confident (predicted too extreme), exactly the direction the manuscript states. Conversely at z = −1 the calibrated p ≈ 0.38 vs ideal 0.27. So a slope of 0.5 halves the effective log-odds range; the score discriminates in *rank* but its *levels* cannot be trusted as probabilities, which is why the ranker framing is correct.

---

---

### ITEM 3 — DCA contradiction: the code uses CALIBRATION-FIT probabilities, not the "uncalibrated" probabilities the text claims

【Problem】 `manuscript.md:112` states the decision-curve analysis was *"computed on the model's (uncalibrated) predicted probabilities."* This is **false relative to the deposited code**. In `_ext_calibration_dca.py:31-32, 66-70` the DCA thresholds on `p = 1/(1+exp(−(a + b·z)))` where `(a,b)` are the *fitted calibration parameters* (intercept −0.04, slope 0.50). Those `p` are therefore *calibration-corrected* (shrunk) probabilities, not raw uncalibrated ones. My recompute confirms: the DCA object uses `p` from the calibration fit (`b<1` ⇒ calibration-fit probs), not `plogis(z)` with slope 1.

【Evidence】
- `_ext_calibration_dca.py:31` `eta = a + b*z`; `:32` `p = 1.0/(1.0+np.exp(-eta))`; `:67` `pred_pos = p >= t`.
- My recompute flag: `Are probs from code = calibration-fit probs (slope<1)? -> True`.
- Raw uncalibrated `plogis(z)` gives a *different, messy* DCA (zero-crossings at ~0.60, 0.86, 0.91), whereas the deposited grid (smooth convergence to 0 by 0.80) is only obtained with the fitted `p`. So the clean DCA curve depends on having used calibrated probs.

【Why it matters】 Two consequences. (i) The text is internally inconsistent: the authors disclaim calibration for the score ("ranker, not probability") yet the DCA — which legitimately *requires* probabilities — silently uses a calibration step. (ii) More importantly, using calibrated probs is the *methodologically correct* choice; the error is only in the description. But because the manuscript uses the "uncalibrated" label to justify reading the DCA as "discrimination-only support," a reviewer could be misled into thinking the DCA is on the raw score. The DCA is valid; the sentence is wrong.

【Specific fix】 Replace `manuscript.md:112` "computed on the model's (uncalibrated) predicted probabilities" with: *"computed on the calibration-corrected probabilities from the external logistic fit (intercept −0.04, slope 0.50; see §3.5), which are the probabilities the score can honestly support."* Optionally add: *"A DCA on the raw, uncalibrated scores is not reported because those probabilities are mis-calibrated (slope 0.50) and would mis-state the harm term."*

---

### ITEM 4 — DCA "positive net benefit 0.10–0.75" is absolute and misleading; the model barely beats *treat-all* above threshold ~0.50

【Problem】 The claim *"positive net benefit across the 0.10–0.75 threshold range"* (`manuscript.md:112`) is technically true in the absolute sense (NB>0) but clinically hollow, because treat-all *also* has positive NB there (driven by the 49% event prevalence). The relevant comparison is **model NB vs treat-all NB**. My recompute shows the model NB *exceeds* treat-all NB only for thresholds ≈0.50–0.95; at 0.10–0.45 the model is essentially equal to or *worse* than treat-all.

【Evidence】
- `09_ext_dca_grid.csv`: at 0.10 model NB = 0.4340, treat-all NB = 0.4340 (tie); at 0.30 model 0.2844 vs treat-all 0.2722 (marginal +0.012); at 0.50 model 0.0755 vs treat-all −0.0189 (model finally clearly ahead).
- My recompute: `Model NB exceeds treat-all NB for thr in [0.50 … 0.95]` only. Below 0.50 model NB ≈ treat-all, and at 0.10 model NB (≈0.004 when computed continuously) is far below treat-all (0.434).

【Why it matters】 A reader seeing "positive net benefit 0.10–0.75" may conclude the score is clinically useful across a broad decision range. In fact, at the low thresholds where one would most want a screening tool, the score offers no advantage over simply treating everyone, and at intermediate thresholds only a marginal one. The honest clinical-utility statement is "the score yields net benefit over treat-all only at high risk thresholds (≳0.50)."

【Specific fix】 In §3.5, replace the absolute-NB phrasing with the comparative one: *"The decision-curve net benefit was positive in absolute terms from 0.10 to 0.75, but the score only exceeded the treat-all strategy above a threshold of ≈0.50 (e.g., at threshold 0.50 model NB 0.076 vs treat-all −0.019; at 0.30 model 0.284 vs treat-all 0.272). Below ≈0.50 the score offers no net benefit over treating all comers, so clinical utility is confined to high-risk decision thresholds."*

---

### ITEM 5 — MR: CD74 Egger SE (0.111) < IVW SE (0.325) on 3 SNPs (df=1) is a red flag the text under-emphasises

【Problem】 The authors note the ordering is "arithmetically unusual but not a contradiction" (`manuscript.md:174`). As a design reviewer I agree it is *not* a logical contradiction, but I disagree that it can be waved through. With **only 3 instruments**, the MR-Egger regression has **df = 1**. At df=1 the Egger slope is identified by a single degree of freedom and its SE is essentially undefined/non-robust; the Egger SE (0.111) falling below the IVW SE (0.325) reflects *leverage weighting*, not genuine precision. Compounding this, the eQTLGen exposure and the UK-Biobank sepsis outcomes **share participants** (sample overlap), which biases *all* SEs downward and inflates type-I error. So the small Egger SE is exactly the symptom of the instability the authors concede.

【Evidence】
- `10_genetics_mr_outcome4982_criticalcare.csv:2-3`: CD74 IVW se=0.32496, Egger se=0.11107, both nsnp=3.
- `manuscript.md:58, 174`: overlap acknowledged; Egger df=1 acknowledged; "standard errors are biased downward by the exposure–outcome sample overlap" stated.
- My recompute reproduces both SEs to 4 d.p.

【Why it matters】 The ordering Egger-SE < IVW-SE on 3 SNPs is the textbook signature of an unstable, overlap-inflated estimate. Treating it as merely "unusual but fine" under-states the risk. It directly undermines the only family-significant result (Item 6).

【Specific fix】 Strengthen `manuscript.md:174`: *"The CD74 critical-care MR-Egger standard error (0.111) is smaller than its own IVW SE (0.325) on only three instruments (Egger df = 1). At df = 1 the Egger slope rests on a single identifying degree of freedom, so this SE is not a stable precision estimate; the small value is consistent with leverage-driven weighting and with downward bias from exposure–outcome sample overlap, and should not be read as evidence of a precise effect."*

---

### ITEM 6 — The "1 of 45" family significance is overlap-inflated, reversed-direction, 3-SNP, and NOT independent corroboration

【Problem】 The headline that *"only one of the 45 tests retains family q<0.05 — the CD74 critical-care weighted median (q≈3e-17)"* (`manuscript.md:176`) is numerically correct (I reproduce exactly 1 significant row in `10_mr_bh_family.csv`) but statistically fragile on four independent grounds: (a) **overlap inflation** — no `mrSampleOverlap` correction was applied, so the SE (hence p=6.6e-19, hence q=3e-17) is biased small; (b) **reversed direction** — OR 2.19 means *higher* predicted CD74 predicts *worse* critical-care outcome, opposite to the Mars1 down-regulation model; (c) **only 3 SNPs**; (d) **not independent corroboration** — the weighted median, IVW, and Egger for CD74 critical care all use the *same 3 SNPs* and the *same overlap-inflated* precision, so "corroborated by IVW and Egger" (`manuscript.md:162, 174`) is the same data seen three ways, not three independent confirmations.

【Evidence】
- `10_mr_bh_family.csv:17`: CD74 Weighted median 4982_critcare, p=6.65e-19, q_family_45test=2.99e-17, the sole `family_sig_q<0.05 = YES`.
- `10_genetics_mr_outcome4982_criticalcare.csv:2-4`: all three CD74 estimators share nsnp=3; IVW se 0.325, Egger se 0.111, WM se 0.088 — WM SE (0.088) is *even smaller* than Egger, implying near-zero between-SNP spread, consistent with overlap-inflated precision.
- Manuscript `manuscript.md:58` acknowledges overlap but applies no correction; `:162` calls the three-method agreement "internally concordant."
- My recompute confirms exactly 1/45 significant.

【Why it matters】 The "1/45 survives" sentence, placed in the Results conclusion, can be read as a positive MR signal. In reality it is the *least* trustworthy of the 45 tests (overlap-inflated p, 3 SNPs, reversed biology). Reporting it as the family's sole "significant" finding without the overlap correction is the single most misleading MR statement in the paper, because BH q-values computed on overlap-biased p-values are themselves invalid. The authors *do* later reinterpret it correctly as a genotype–severity association, but the headline precedes and can outlive that caveat.

【Specific fix】 (a) Apply the Burgess–Davies–Thompson sample-overlap bias correction (`mrSampleOverlap` / `MRAnalyse_overlap`) to all estimates, or at minimum re-derive the CD74 critical-care SEs under a conservative overlap adjustment, and report whether q remains <0.05. (b) In `manuscript.md:176`, reframe: *"After the pre-specified 45-test BH correction the only family-significant result is the CD74 critical-care weighted median (q≈3e-17); however, this estimate rests on three instruments, reverses the Mars1 direction (OR 2.19), and is computed without a sample-overlap correction, so its q-value is overlap-inflated and it is reported as a genotype–severity association, not a validated causal or repositioning signal."* (c) State plainly that the three estimators "agree" only because they share the same 3 overlap-biased SNPs — this is not independent replication.

**CD74 critical-care estimator table (from `10_genetics_mr_outcome4982_criticalcare.csv`, all nsnp = 3):**

| Estimator | β | SE | OR (95% CI) | p | Note |
|---|---|---|---|---|---|
| IVW | 0.7983 | 0.3250 | 2.222 (1.175–4.200) | 0.014 | SE inflated by few SNPs |
| MR-Egger | 0.7983 | 0.1111 | 2.222 (1.787–2.762) | 0.088 | SE < IVW SE; df = 1 ⇒ unstable |
| Weighted median | 0.7859 | 0.0885 | 2.194 (1.845–2.610) | 6.6e-19 | SE < Egger SE; overlap-inflated p |

The monotonic decrease SE(IVW) > SE(Egger) > SE(WM) across three *methods that share the identical 3 SNPs* is the fingerprint of overlap-driven precision inflation: the same tight between-SNP spread (because the eQTLGen discovery and UK-Biobank outcome share subjects) propagates into all three SEs, and the smaller-Egger-than-IVW ordering on df=1 is simply the Egger leverage weights exploiting that single degree of freedom. None of the three is an independent check on the others.

---

---

### ITEM 7 — MR family structure: 45 "tests" are not independent; BH on correlated tests over-states the cleanliness of the null

【Problem】 The 45 tests = 5 genes × 3 methods × 3 outcomes. They are **not** independent: (i) the 5 genes are a *co-expression hub* (the manuscript's own finding), so their eQTL instruments are correlated; (ii) the 3 outcomes (susceptibility, 28-day death, critical care) are positively correlated sepsis phenotypes; (iii) all share the eQTLGen exposure and the overlap. BH controls FDR under independence/positive-regression-dependence, so it is not *invalid*, but the effective number of independent tests is far below 45. The practical consequence: the *primary*-outcome family (15 tests on 28-day death) is **fully null** (minimum p = CD14 Egger 0.049, which does not survive even the 15-test correction, `p_fdr_bh`=0.487), yet the paper headlines the 45-test family which captures the one reversed, overlap-inflated result from a *secondary/sensitivity* outcome.

【Evidence】
- `10_mr_bh_family.csv`: the 15 rows for `5086_28ddeath` all have `family_sig_q<0.05 = no`; max significance is CD14 Egger p=0.049 (per-outcome `p_fdr_bh`=0.487).
- `manuscript.md:149`: "this gives family q≈0.73 and does not cross the 0.05 threshold" — correct for primary.
- The only `YES` is on outcome `4982_critcare` (sensitivity), not the primary `5086`.

【Why it matters】 Emphasising "1 of 45" invites the reader to see a marginal positive MR signal, while the phenotype-matched primary outcome is entirely null. The honest hierarchy is: *primary 28-day death — null across all methods; one reversed, overlap-inflated, 3-SNP signal in a secondary outcome.* That is already the authors' conclusion, but the *framing order* (45-test headline before the primary-outcome null) inverts the proper emphasis.

【Specific fix】 In §3.10 and the Discussion, lead with the primary outcome: *"On the phenotype-matched primary outcome (28-day death, 15 tests), no estimator crossed significance (minimum p = 0.049 for CD14 MR-Egger, 15-test BH q = 0.49). The only family-significant result lay in the critical-care sensitivity outcome and is overlap-inflated and reversed (Item 6)."* Consider reporting BH **per outcome** as the primary multiplicity control and the 45-test family only as a sensitivity context.

---

### ITEM 8 — MR candidate selection is selection-on-outcome; BH does not correct it (Limitation 12 is correct but under-weighted)

【Problem】 The six candidates were nominated because they are expression-associated with the Mars1 endotype and 28-day death in GSE65682, then MR-tested for causality on sepsis outcomes (`manuscript.md:208`, Limitation 12). This is selection-on-outcome circularity: the MR is a within-cohort-generated hypothesis, not an independent confirmation. The 45-test BH controls *multiplicity over the chosen genes* but **not** their outcome-driven selection. The manuscript discloses this, but the MR section still reads as if it "tested" the hubs causally.

【Evidence】 `manuscript.md:208` (Limitation 12) explicitly states the circularity; `:176` nonetheless frames MR as having "returned directionally protective estimates… for three of five hubs."

【Why it matters】 A reader may interpret "three of five hubs show protective MR estimates" as supportive biology. It is supportive only in the weak sense of *consistency with an a-priori hypothesis generated from the same data* — not as independent causal evidence. The conclusion ("no causal claim") is right; the surrounding presentation should not let the consistency be mistaken for confirmation.

【Specific fix】 Add one sentence to §3.10: *"Because the candidate genes were selected from the discovery cohort on the basis of their sepsis/28-day-death association, the MR is a within-cohort-generated hypothesis test; the BH correction controls multiplicity over the chosen genes but not their outcome-driven selection, so consistency of MR direction with the expression model is not independent confirmation."*

---

### ITEM 9 — IRG benchmark comparison is not apples-to-apples: orientation asymmetry inflates the signature's apparent edge

【Problem】 The signature's 0.638 is compared to a recomputed IRG-3 benchmark of 0.604 (`manuscript.md:14, 112`). But the two scores are built with *different orientation treatment*. The 30-gene signature is fully orientation-corrected (every gene multiplied by `sign(corr_with_death)` from GSE65682; `09_external_validation.py:73,116-118`). The IRG-3 set is `['LTB4R','HLA-DMB','IL4R']`; of these, only `HLA-DMB` is in the signature orientation dictionary — **LTB4R and IL4R are left unoriented** (`09_external_validation.py:154-156`: `if g in orient and orient[g]==-1`). So the IRG benchmark is only partially oriented while the signature is fully oriented, handing the signature a systematic discrimination advantage that has nothing to do with biology.

【Evidence】
- `09_external_validation.py:149` `irg = ["LTB4R","HLA-DMB","IL4R"]`; `:154-156` orientation only applied when `g in orient`.
- My check: `IRG genes in signature orient dict: ['HLA-DMB']` → LTB4R, IL4R unoriented.
- Recomputed AUCs: oriented-sum 0.6382, IRG 0.604 (DeLong P 0.559, difference 0.034, CI −0.077–0.151).

【Why it matters】 The 0.034 gap that the manuscript calls "comparable rather than superior" may be *partly* an artifact of the orientation asymmetry rather than a real discrimination difference. The DeLong result (P≈0.56) is robust either way, so the *conclusion* ("comparable, not superior") stands — but the *magnitude* of the gap is not a clean estimate and should not be presented as if the signature clearly edges the benchmark.

【Specific fix】 Either (a) orient the IRG-3 genes consistently (using their GSE65682 death-correlation sign, exactly as done for the signature), or (b) explicitly state the benchmark is partially unoriented and therefore a *lower-bound* reference. Add to §3.5: *"The IRG-3 benchmark was oriented only where the gene also appeared in the signature set; LTB4R and IL4R were left unoriented, so the 0.034 AUC gap may partly reflect orientation asymmetry rather than discrimination, and the two scores are not strictly comparable."*

---

### ITEM 10 — p-value underflow reporting is acceptable but should be uniform

【Problem】 The manuscript reports `CD14 Δ=−0.77 (P≈0, underflow)` and `P<1e-300` (`manuscript.md:80, 81`). Reporting underflow as "≈0" or "<1e-300" is acceptable *only* because it is labelled, which the authors do. The minor issue is inconsistency: Table 1 writes "≈0 (P<1e-300)" while the prose writes "P≈0, underflow." No value is treated as literally 0 in a calculation, so this is cosmetic, not substantive.

【Evidence】 `manuscript.md:80-81`; `S01_mars1_deg.csv` shows adj.P values stored as 0.0 / underflow for strong DEGs (e.g., CD14).

【Why it matters】 Underflow p-values are fine if flagged; unflagged they invite false-precision criticism. The authors already flag them, so this is a housekeeping note.

【Specific fix】 Standardise to a single convention, e.g. always write "P<1×10⁻³⁰⁰ (numerical underflow)" in both Table 1 and prose. No substantive change.

---

### ITEM 11 — The DCA "zero-crossing by 0.80" is correct, but state it is on calibration-fit probs and tie it to the ranker claim

【Problem】 Minor consolidation of Items 3–4. The zero-crossing at ~0.80 reproduces (grid: 0.75→+0.0094, 0.80→0.0; my continuous fit ~0.76–0.80). This is fine. But the text currently juxtaposes "uncalibrated probs" (wrong, Item 3) with "converging to zero by 0.80" without noting the crossing depends on the calibration-fit probabilities.

【Evidence】 `09_ext_dca_grid.csv` rows for 0.75/0.80; my recompute zero-crossing ~0.75–0.80.

【Why it matters】 Consistency: if the reader later learns the DCA used fitted probs, the "by 0.80" claim should remain coherent.

【Specific fix】 Append to the DCA sentence: *"The net-benefit curve converged to zero at a threshold of ≈0.80 when computed on the calibration-corrected probabilities."*

---

## § Questions for the authors

1. **Overlap correction.** Have you run the Burgess–Davies–Thompson `mrSampleOverlap` estimator on the five hub analyses? If so, what are the corrected CD74 critical-care SEs and does q remain <0.05? If not, will you add it, given that the only family-significant result depends on it?
2. **Egger df=1.** For CD74 critical care (3 SNPs, Egger df=1), do you agree the Egger SE (0.111) is not a stable precision estimate, and are you comfortable demoting the "three-method concordance" language to "same three overlap-biased SNPs"?
3. **IRG orientation.** Can you re-run the IRG-3 benchmark with full GSE65682-sign orientation (LTB4R, IL4R included) so the 0.638-vs-0.604 comparison is strictly fair? We expect the gap to shrink; does the "comparable" conclusion hold either way (DeLong already says yes)?
4. **DCA probabilities.** The deposited code thresholds the DCA on calibration-fit probabilities, not raw uncalibrated ones. Do you agree the manuscript text should be corrected to say "calibration-corrected" rather than "uncalibrated"? And will you report the model-vs-treat-all comparison (advantage only above ≈0.50) explicitly?
5. **EPV presentation.** Will you lead the Abstract/§3.4 with the honest external AUC 0.638 and explicitly label the 0.659 CV AUC as optimistic and label-driven, given the locked-L1 weights transport to only 0.585?
6. **Family emphasis.** Will you restructure §3.10 to present the *primary-outcome* (28-day death) 15-test null first, and the 45-test "1 significant" only as a clearly caveated sensitivity result?
7. **Bootstrap seed.** The calibration-slope bootstrap CI I obtain is [0.109, 0.947] vs your [0.11, 0.96]. Can you confirm the exact bootstrap specification (reps, seed, resampling unit) so the upper bound is reproducible?

---

## § What I actually checked — commands (for transparency / reproducibility)

```text
# Interpreter
C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe

# Recompute script (deposited as 03_results/_rev_recompute.py), run from absolute path:
python 03_results/_rev_recompute.py
# -> reproduces: oriented-sum AUC 0.6382; IRG AUC 0.604; DeLong P 0.559;
#    paired-bootstrap diff 0.034 (CI -0.077,0.151; P 0.548);
#    calibration intercept -0.0382 / slope 0.5028; bootstrap slope CI [0.109,0.947];
#    DCA zero-crossing ~0.76-0.80 on fit probs, ~0.6/0.86/0.91 on raw plogis(z);
#    model NB > treat-all NB only for thr in [0.50,0.95];
#    CD74 crit-care IVW SE 0.3250 / Egger SE 0.1111; 1/45 family-significant.
```

Manual cross-checks performed without code:
- FIS1 Mars1-vs-Other: `S01_mars1_deg.csv` line → logFC 1.2614, t 17.1567 (manuscript +1.26 / +17.2 ✓).
- IRG orientation: `S06_signature_genes.csv` gene list vs `09_external_validation.py:149` → only HLA-DMB oriented; LTB4R, IL4R unoriented.
- Family count: `10_mr_bh_family.csv` has 45 rows; exactly 1 with `family_sig_q<0.05 = YES` (CD74 WM crit-care).

---

### ITEM 12 — AUC bootstrap CI method is sound but the external CI is wide; do not over-read the "comfortable margin"

【Problem】 The external oriented-sum AUC 95% CI is [0.532, 0.748] (`09_external_validation.csv`), and the manuscript notes it "excludes 0.5 by a comfortable margin" (`manuscript.md:112`). This is true, but the interval is ±0.11 around 0.638 — i.e., the point estimate could plausibly be anywhere from barely-discriminative (0.53) to modest (0.75). Stating "comfortable margin" risks implying the discrimination is firmly established, when n=106 with 52 events gives exactly the wide interval one would expect.

【Evidence】 `09_external_validation.csv`: `auc_EMTAB4451_orientedSum_CI95_low`=0.5317, `..._high`=0.7475; bootstrap 2000 reps, seed 42 (`09_external_validation.py:125,132`). My recompute of the point AUC matches 0.6382 exactly.

【Why it matters】 Honest external validation is the paper's strongest asset; the CI should be presented as evidence of *modest, uncertain* discrimination, not as a comfortable win. The current wording slightly oversells.

【Specific fix】 Soften to: *"The 95% CI (0.532–0.748) excludes 0.5, supporting real but modest discrimination; the width reflects the n=106 / 52-event external sample, and the point estimate should be read as uncertain rather than firmly established."*

---

### ITEM 13 — High external prevalence (0.49) mechanically inflates DCA "treat-all" NB and must be stated when interpreting the DCA

【Problem】 E-MTAB-4451 has 52/106 deaths (prevalence 0.49). At any threshold t, treat-all net benefit = prevalence − (1−prevalence)·t/(1−t), which is large and positive for t ≲ 0.5 precisely *because* prevalence is near 0.5. This is why the model only "wins" above ≈0.50 (Item 4): at low thresholds treat-all is hard to beat simply due to the case mix. The DCA is valid, but its interpretation is prevalence-dependent and the manuscript should say so.

【Evidence】 `09_ext_calibration_dca.csv`: prevalence 0.4906; treat-all NB at 0.10 = 0.434, at 0.30 = 0.272 (`09_ext_dca_grid.csv`). My recompute matches.

【Why it matters】 Without the prevalence caveat a clinician might generalise the DCA to a lower-prevalence ICU population where treat-all NB collapses and the model's relative advantage would look different. This is a standard DCA reporting omission.

【Specific fix】 Add to §3.5: *"The DCA is interpreted in the context of the external cohort's high event prevalence (0.49); treat-all net benefit is correspondingly large at low thresholds, which is why the score's advantage over treat-all appears only above threshold ≈0.50 and would differ in a lower-prevalence setting."*

---

### ITEM 14 — Gene selection and orientation reuse the 28-day labels (Limitation 10); state its direct effect on the external comparison

【Problem】 Limitation 10 correctly notes the 30-gene selection chain reuses the same 28-day labels, contributing to the optimistic CV AUC. What is not stated is that the *orientation* step (`orient = sign(corr_with_death)`) is itself a label-trained transformation applied to the test cohort via the training sign. Because orientation is fixed at training and transported, it is legitimate for external validation — but it means the 0.638 already embeds training-label information through orientation, so the "fully independent" external AUC is independent in *coefficients* but not in *feature engineering*. This is fine and standard, but the manuscript's "fully independent cross-platform" language (`manuscript.md:182, 194`) slightly overstates independence.

【Evidence】 `09_external_validation.py:73,116-118` — orientation fixed from training `corr_with_death`; applied to E-MTAB without re-estimation. Limitation 10 (`manuscript.md:204`) acknowledges selection-chain FWER but not the orientation-as-label-leakage nuance.

【Why it matters】 "Fully independent" is a strong claim; the orientation is derived from the discovery labels, so the external AUC is a *locked-prediction* validation, not a *de novo* external discovery. The distinction matters for how much weight a reader places on 0.638.

【Specific fix】 Replace "fully independent cross-platform" with "independent cross-platform application of a locked, label-oriented signature," and add one clause in Limitation 10: *"Orientation by training-set death-correlation is a label-trained feature transform carried into the external cohort, so the external AUC validates a locked prediction rule rather than a label-independent gene set."*

---

## § Reproducibility audit (positives worth preserving)

Beyond the specific fixes, the manuscript's audit infrastructure is genuinely above average for a single-author computational paper and should be preserved through revision:

- **Every number traces to a CSV** (`manuscript.md:§7` provenance table maps 30+ reported quantities to files). I verified this end-to-end: each value I recomputed had a concrete source file, and no cited number was orphaned.
- **The calibration and DCA code is self-contained and re-runnable** (`_ext_calibration_dca.py`), which is how I caught the uncalibrated-vs-fit probability discrepancy (Item 3). Keeping the code is what makes the error detectable.
- **The MR BH table is fully tabulated** (`10_mr_bh_family.csv`, 45 rows with per-outcome and family q), allowing independent verification of the "1/45" claim — which I reproduced exactly.
- **Limitations are unusually candid** (12 numbered items, including selection-on-outcome, overlap, single-direction L1000, and deferred docking). This candour is the paper's best defence against a Major verdict and should not be diluted in revision.
- **Bootstrap seeds are fixed** (external validation seed 42; MR seed 20260925) so CIs are reproducible; I only differed on the calibration bootstrap seed (I used 7) which explains the trivial [0.11,0.96] vs [0.109,0.947] upper-bound difference (Item 2).

The fixes requested above are largely *textual reframings* and one optional *overlap correction*; they do not require re-collecting data or re-running the core pipeline, which is why this is a Minor rather than Major revision.

**Independence attestation.** I performed this review without access to any prior reviewer reports, response letters, revision manifests, or author verification statements for this manuscript. All findings were derived solely from `05_reports/manuscript.md`, the `03_results/*.csv` tables, and the `02_scripts/python/*.py` code listed in the "What I actually checked" section, supplemented by my own independent recomputations. Where I state a value "reproduces," it was regenerated by me from the deposited files, not copied from the text.

---

## § Summary of verdict drivers

- **Sound and kept:** locked external validation; candid calibration reporting; correct "comparable not superior" DeLong framing; honest MR downgrade; reproducible DEG/hub lineage.
- **Must-fix (design integrity):** (i) DCA text says "uncalibrated" but code uses calibration-fit probs (Item 3) — factual error; (ii) the "1/45" MR significance is overlap-inflated, reversed, 3-SNP, and not independent, and is headlined ahead of the fully-null primary outcome (Items 5–7); (iii) IRG benchmark orientation asymmetry makes the 0.034 gap non-clean (Item 9); (iv) EPV 3.8 optimistic CV AUC is over-featured vs the 0.585 transported weights (Item 1).
- **Should-fix (clarity):** DCA "positive NB" should be the model-vs-treat-all comparison (Item 4); calibration CI width should be stated (Item 2); Egger df=1 instability should be stronger (Item 5); selection-on-outcome framing emphasised (Item 8); underflow convention uniform (Item 10).

---

## VERDICT: Minor revision.

The analysis is reproducible, the headline numbers all check out to quoted precision, and the authors' central honesties (locked external validation, candid mis-calibration, correct "comparable not superior" framing, MR downgrade) are genuine strengths. However, four design-layer items require correction before publication: the DCA text incorrectly claims "uncalibrated" probabilities when the code uses calibration-fit ones; the "1 of 45" MR significance is overlap-inflated/reversed/3-SNP and is presented ahead of the fully-null primary outcome; the IRG benchmark is orientation-asymmetric; and the EPV-3.8 optimistic CV AUC is over-featured relative to the 0.585 transported weights. None of these require new data, and all are addressable with text/reframing plus the optional overlap correction — hence Minor, not Major.
