# Reviewer A2 — Design, Biostatistics & Causal Inference

Manuscript: "Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning" (v1.5.0, 288 lines).
Reviewer lens: Mendelian randomisation methodology, prediction-model validation, survival/multiplicity design.

**Independence statement.** I read the manuscript in full and the shared panel brief. I did not read any prior review round, author response, revision log, manifest, verification statement, or other reviewers' outputs in this directory. Every number below marked "recomputed" was recalculated by me from the source CSVs in `03_results/` (and per-sample risk scores), not copied from the manuscript.

---

## § 1. Findings (graded)

---

### Finding A2-1 — The CD74 critical-care weighted-median p-value is stored as an underflowed zero and propagated as "q≈0"; the recomputable value is q = 1.5×10⁻¹⁷

**Tier 2** (numerically wrong as stated, but it *overstates* support for a signal the manuscript already treats with heavy caveats)

- 【Problem】 The manuscript and `10_mr_bh_family.csv` report the CD74 critical-care weighted-median family q as "≈0"/"0.000000e+00", which is an artifact of floating-point underflow in the stored p-value, not a computed zero.
- 【Evidence】 In `10_genetics_mr_outcome4982_criticalcare.csv` line 4, the CD74 weighted-median row has `p = 0.0` with β=0.7859, SE=0.0885 (z = 8.881). Recomputing the two-sided normal p from β/SE I obtain p = 6.65×10⁻¹⁹ (underflow below double-precision resolution at ~1×10⁻³⁰⁸? no — the underflow threshold is ~10⁻³⁰⁸, so the stored 0.0 indicates the p was computed by a route that underflowed earlier, e.g. `2*scipy.stats.norm.sf` chaining); applying BH across the 45 assessable tests with the recomputed p gives family q = 1.50×10⁻¹⁷, not 0. `10_mr_bh_family.csv` line 17 carries `p = 0.000000e+00` and `q_family_45test = 0.000000e+00`. The manuscript states "weighted median (*q*≈0)" at manuscript.md:72 and manuscript.md:190.
- 【Why it matters】 "q≈0" is not a number; it invites the reader to treat the test as infinitely significant and conceals that the stored p-value never entered the computation. Any meta-analysis or text-mining of this table propagates a literal zero. The corrected q (1.5×10⁻¹⁷) is still decisive, so the conclusion is unchanged — but the provenance failure is exactly the kind that undermines trust in an otherwise carefully audited table.
- 【Specific fix】 Replace in §3.10 (and mirrored in Limitations §5.2): "Under the pre-specified 45-test family correction, the CD74 critical-care weighted-median test gives q = 1.5×10⁻¹⁷ (p = 6.7×10⁻¹⁹ recomputed from β/SE = 0.786/0.088; the value 0 originally stored reflects floating-point underflow, now corrected)." Additionally regenerate `10_mr_bh_family.csv` computing p on the log scale (`scipy.stats.norm.logsf`) so no p-value is ever stored as exact 0.

---

### Finding A2-2 — Sample overlap between eQTLGen and UK Biobank is disclosed only in Methods/Limitations while the strongest MR statement ("the strongest MR association in the study") is made in Results without the caveat attached at the point of claim

**Tier 1** (the bias is directional and the headline framing partially bypasses it)

- 【Problem】 The exposure–outcome sample overlap (eQTLGen cis-eQTL n≈31,684 includes UK Biobank donors; all three outcomes are UK Biobank GWAS) biases MR standard errors downward in a way that is most severe precisely for the CD74 critical-care result, yet the Results section states the q<10⁻¹¹ finding before any overlap qualification is repeated at that location.
- 【Evidence】 manuscript.md:70 discloses the overlap ("The eQTLGen discovery sample (31,684 donors, which includes UK Biobank participants) … We did not apply a sample-overlap correction"); manuscript.md:171 repeats it. But manuscript.md:173 (the §3.10 summary paragraph) states "Against critical care, CD74 reaches *q*<10⁻¹¹ … so we report it as a genotype–severity association" — the overlap caveat appears at manuscript.md:171 only inside the CD74 sentence, and the Limitations paragraph (manuscript.md:190) re-derives it. I verified the overlap is real and material: eQTLGen whole-blood cis-eQTL meta-analysis explicitly includes UKB (per-gene n up to 31,684 per manuscript.md:70), and `ieu-b-4982` has 429,985 UKB controls; with the UKB fraction of eQTLGen being roughly 0.16 of the exposure sample, Burgess et al.'s (2016) approximation implies SE inflation factors of only ~1.0–1.1 — small for the giant q-values, but the *sign* of the bias is always toward overconfidence. I recomputed from `10_genetics_mr_outcome4982_criticalcare.csv` line 2: CD74 IVW OR 2.222 (1.175–4.200), p=0.014 — the only outcome where nominal IVW significance is reached, and the one with the largest case burden among UKB-only participants.
- 【Why it matters】 The manuscript's own discipline ("hypothesis-generating only") is correct, but a reader extracting Table 4 and the §3.10 summary without the interleaved caveat will carry away a q<10⁻¹¹ causal-flavored association whose SEs are biased. Given the reversed direction versus the expression model, the honest summary is that this is an *association of uncertain mechanism* whose precision is overstated.
- 【Specific fix】 Paste-ready replacement for the §3.10 summary sentence (manuscript.md:173): "Against critical care, CD74 reaches q<10⁻¹¹ under the 45-test family, but this estimate inherits downward-biased standard errors from eQTLGen–UK Biobank sample overlap, rests on three instruments, and reverses the Mars1 expression direction; we therefore report it as an uncorrected genotype–severity association whose precision is overstated by overlap, not as evidence for or against CD74-directed therapy." Additionally, run the Burgess–Davies–Thompson sample-overlap correction [31] and add a column `or_overlap_corrected` (plus SE) to each `10_genetics_mr_outcome*.csv`; spec: inputs = UKB participant fraction of eQTLGen (π ≈ 0.16, from eQTLGen cohort documentation) and outcome GWAS sample sizes per outcome; output columns = `beta_corrected`, `se_corrected`, `p_corrected` per gene × method × outcome.

---

### Finding A2-3 — With 3–8 instruments per gene, the MR-Egger intercept tests cannot support the pleiotropy narrative the manuscript builds on them

**Tier 1** (analysis/interpretation to add — the manuscript is half-aware but still leans on the intercepts directionally)

- 【Problem】 The manuscript uses null Egger intercepts as partial reassurance ("internally concordant … null Egger intercept P=1.00", manuscript.md:171) and a significant intercept to disqualify one signal (CD74 susceptibility, manuscript.md:171), but with n_SNP = 3 (CD74) the Egger model is saturated-ish (3 points, 2 parameters) and the intercept test has essentially no power in either direction.
- 【Evidence】 Recomputed from `10_genetics_mr_outcome4982_criticalcare.csv` line 3: CD74 critical-care Egger intercept = 1.32×10⁻⁶, intercept p = 0.99987, with only 3 SNPs (harmonised table `10_genetics_mr_outcome4982_harmonised.csv` lines 2–4: rs2305480, rs4810485, rs12478601). With 3 instruments and 2 estimated parameters, the Egger regression has 1 residual df; a null intercept here is uninformative about horizontal pleiotropy — it cannot reject, and it equally cannot "confirm" symmetry. The same applies to the CD74 susceptibility intercept disqualification (p=9.98×10⁻⁵, `10_genetics_mr.csv` line 3): a significant intercept from 3 SNPs is itself fragile (single influential SNP can drive it; no leave-one-out is reported). Manuscript does acknowledge this at manuscript.md:171 ("though with only three instruments the Egger intercept is uninformative") — but then the Discussion (manuscript.md:181) still states "null intercept, though with only six instruments this test is underpowered to exclude pleiotropy" for CD14 and the Limitations (manuscript.md:190) constructs a pleiotropy-attribution argument on the CD74 susceptibility intercept (P=1.0×10⁻⁴) without a leave-one-out check.
- 【Why it matters】 Asymmetric use of an underpowered diagnostic: null intercepts are cited as mild reassurance while a significant intercept is used to *explain away* a signal. Both inferences exceed what 3–6 instruments can support. Reviewers in this field (and STROBE-MR item 12) expect leave-one-out sensitivity and InSIDE-related discussion when Egger is used with few instruments.
- 【Specific fix】 Add a leave-one-out analysis and neutral framing. Spec: for each gene × outcome with ≥3 IVs, recompute MR-Egger slope and intercept dropping each SNP in turn; output columns `gene, outcome, snp_dropped, egger_beta, egger_beta_p, intercept, intercept_p` to a new file `03_results/10_mr_leave_one_out.csv`. Paste-ready replacement sentence for manuscript.md:171: "With three to six instruments per gene, the MR-Egger intercept is uninformative about horizontal pleiotropy in either direction; we therefore do not use null intercepts as reassurance, nor the single significant CD74 susceptibility intercept (P=1.0×10⁻⁴) as a definitive pleiotropy attribution, pending the leave-one-out analysis (Supplementary Table S10-LOO)."

---

### Finding A2-4 — The "45-test family" is one of several defensible families and the pre-specification claim is unverifiable; the per-outcome 15-test correction is buried in a CSV column rather than reported in the text

**Tier 2** (wording/transparency; the corrected results are robust either way)

- 【Problem】 The manuscript asserts the 45-test (5 genes × 3 estimators × 3 outcomes) BH correction was "pre-specified" (manuscript.md:72), but the pre-specification is not documented anywhere a reader can verify, and the alternative family choices (15 per outcome; 3 estimators nested within gene; IVW-only across 15 gene×outcome tests) change which individual tests cross q<0.05.
- 【Evidence】 I recomputed all three families from the three MR CSVs plus the underflow correction (Finding A2-1): (a) 45-test family: CD74 critcare weighted-median q=1.5×10⁻¹⁷, CD74 critcare Egger q=1.49×10⁻¹¹, CD74 suscept Egger q=2.47×10⁻³; nothing else below 0.05; (b) per-outcome 15-test: CD74 critcare Egger q=4.97×10⁻¹², weighted-median q=0 (underflowed, same issue), IVW q=0.0701 (does NOT cross 0.05 — the nominally "significant" IVW p=0.014 fails even the lenient per-outcome correction, a fact stated nowhere in the manuscript); (c) IVW-only family (15 gene×outcome tests, arguably the primary-estimator family): nothing crosses 0.05 (smallest: CD74 critcare IVW q=0.105). The manuscript does state the per-outcome column exists (`p_fdr_bh`) at manuscript.md:72 and cites 0.077 for CD14 at manuscript.md:146, but never states that the CD74 critical-care IVW itself fails all corrections (q=0.070 per-outcome; 0.126 family) — Table 4 shows "0.014" in bold-adjacent framing with no q-value.
- 【Why it matters】 The IVW estimator is declared "primary" (manuscript.md:72), yet on the primary IVW estimator no result is significant under any correction; the only super-significant results come from Egger and weighted median on secondary outcomes with 3 instruments. This asymmetry should be stated explicitly, because "CD74 reaches q<10⁻¹¹" (manuscript.md:173, :190) is estimator-selected.
- 【Specific fix】 Paste-ready replacement sentence for §3.10 (after Table 4 discussion, manuscript.md:159): "Under every correction family examined (45-test pre-specified; 15-test per-outcome; 15-test IVW-only), no IVW estimate reaches q<0.05 — the smallest corrected value is the CD74 critical-care IVW at q=0.126 — so the super-significant CD74 critical-care results are specific to the MR-Egger and weighted-median estimators on a secondary outcome and should not be summarised as 'CD74 reaches q<10⁻¹¹' without that estimator qualifier." Also add to the Methods a sentence naming where pre-specification is documented (e.g., a dated analysis-plan file in the repository), or delete the word "pre-specified".

---

### Finding A2-5 — The 5-fold CV AUC (0.659) is correctly labelled optimistic, but no honest optimism quantification is attempted; the external estimate is the only one carrying the claim, and it is properly CI'd — however no calibration assessment exists anywhere

**Tier 1** (analysis to add: calibration; the discrimination honesty is largely fine)

- 【Problem】 The manuscript claims "Calibration and decision-curve analytics [18] for the external score are in Fig. S06 (`04_figures/S06_dca.png`)" (manuscript.md:106), but the referenced figure is a decision curve computed on the *training cohort* hub score (title: "Decision curve (28d death)"), it shows net benefit below the treat-none strategy for threshold probabilities above ~0.2, and no calibration plot or statistic (calibration slope/intercept, Hosmer–Lemeshow, or Brier score) exists for either cohort.
- 【Evidence】 I inspected `04_figures/S06_dca.png`: it is titled "Decision curve (28d death)" with a single "Hub score" curve crossing below the "None" line near threshold 0.2 and plunging to net benefit ≈ −2.3 by threshold 0.9 — i.e., the decision-curve evidence is *unfavorable* at clinically relevant thresholds and is computed from the GSE65682 cohort, not the external E-MTAB-4451 score the sentence claims. I recomputed from `09_ext_risk_scores.csv` (n=106, 52 deaths): external oriented-sum AUC = 0.6382 (95% CI 0.529–0.738 by my 2,000-resample bootstrap; manuscript reports 0.638, CI 0.532–0.748 — consistent within bootstrap noise), locked-L1 AUC = 0.5848 (CI 0.475–0.692; manuscript 0.585, 0.469–0.696). No calibration output exists in `03_results/` (no `09_*calibration*` file; `09_external_validation.csv` contains only AUC scalars, lines 1–17).
- 【Why it matters】 A prediction-model claim ("prognostically informative", Abstract and §3.4) without any calibration metric is incomplete by TRIPOD standards; discrimination alone (AUC 0.638) does not establish clinical usefulness, and the one decision-curve figure actually shows no net benefit over treat-none above threshold 0.2 — the manuscript cites it as if supportive. This is a mis-citation that a methods reviewer will catch.
- 【Specific fix】 (i) Delete or replace the sentence at manuscript.md:106 with: "Decision-curve analysis of the within-cohort hub score shows no net benefit over treat-none at threshold probabilities above 0.2 (Fig. S06), so the signature's clinical utility at current evidence is limited to risk stratification research contexts; a calibration assessment of the external score is provided in Supplementary Fig. S09b." (ii) New analysis spec: using `09_ext_risk_scores.csv` columns `y` and `risk_oriented_sum`, fit logistic calibration on the log-odds scale, report calibration intercept, calibration slope (with 95% CI from 2,000 bootstrap), Brier score, and a decile calibration plot; output file `03_results/09_external_calibration.csv` with columns `metric, value, ci_low, ci_high` and figure `04_figures/fig_s09b_external_calibration.png`.

---

### Finding A2-6 — The immune-function score "lowest in Mars1" is not statistically supported against the closest endotype (Mars2); the claim rests on medians without any test

**Tier 2** (wording + trivial addition of a test; partly definitional by construction, which the manuscript does disclose)

- 【Problem】 §3.2 states the immune-function score "was lowest in Mars1 (median −0.79 …), the lowest median among the four endotypes" (manuscript.md:100), but I recomputed the Mars2 median as −0.752 versus Mars1 −0.792 — a difference of 0.04 on a score whose full-cohort range is −3.65 to +3.86 — and a Mann–Whitney U test I ran gives p = 0.47, i.e., Mars1 and Mars2 are statistically indistinguishable on this score.
- 【Evidence】 Recomputed from `S02_immunoparalysis_score.csv` (802 rows): medians Mars1 = −0.7917 (n=132), Mars2 = −0.7520 (n=176), Mars3 = +0.6405 (n=118), Mars4 = −0.2347 (n=53). Mann–Whitney (normal approximation with tie correction): Mars1 vs Mars2 z=0.73, p=0.467; Mars1 vs Mars4 p=1.3×10⁻³; Mars1 vs Mars3 p=1.8×10⁻¹⁸. The manuscript's median value −0.79 (manuscript.md:100, :14) matches my recomputation. The manuscript does disclose the circularity ("partly definitional", manuscript.md:100) — that is honest — but it does not disclose that the *ordering claim itself* (Mars1 lowest) fails against Mars2.
- 【Why it matters】 "Lowest median among the four endotypes" implies a separation that does not exist for the top two endotypes; a careful reader recomputing the Mars2 median will find the claim hollow, and the circularity caveat makes it worse (the score was constructed from the gene sets that define Mars1, so failing to separate Mars1 from Mars2 is double-negative evidence about the score's discriminative value).
- 【Specific fix】 Paste-ready replacement for manuscript.md:100: "The composite immune score was lowest in Mars1 (median −0.79) and Mars2 (median −0.75); the two were statistically indistinguishable (Mann–Whitney p=0.47), while both differed from Mars3 (p<10⁻¹⁷) and Mars4 (p=1.3×10⁻³). Because the score is built from the same HLA-II / T-cell / exhaustion gene sets that define the Mars1 program, this separation is partly definitional and the score is used only descriptively here." (The prose already concedes partial circularity; this makes the numeric truth explicit.)

---

### Finding A2-7 — The S10 companion design document contradicts the manuscript on the count of directionally concordant protective hubs on the primary outcome ("four of five" vs "three of five")

**Tier 3** (internal consistency; the manuscript text is the correct one)

- 【Problem】 `03_results/10_genetics_mr_design.md` §3.1 states "four of five assessable hubs give protective estimates concordant across all three methods" on the 28-day-death outcome, while the manuscript (manuscript.md:146) says three (HLA-DQA1, CD14, FIS1); the design document is stale.
- 【Evidence】 Recomputed from `10_genetics_mr_outcome5086_28ddeath.csv`: CD74 estimates are IVW OR 1.119, Egger 1.093, weighted median 0.970 — two of three point estimates are *harmful* (>1), so CD74 is not concordant-protective. HAVCR2 estimates are 0.978 / 1.010 / 0.960 — mixed (Egger >1), also not strictly concordant-protective. Only HLA-DQA1 (0.923/0.954/0.930), CD14 (0.927/0.906/0.914), FIS1 (0.963/0.964/0.971) are concordant and protective — three of five, as the manuscript states. The design document's claim of four is wrong (it apparently counts HAVCR2 despite its Egger OR>1, line 62–64 of the .md).
- 【Why it matters】 The companion file is cited in the manuscript's own provenance table (manuscript.md:234) as the S10 record; a reader (or a meta-scientist auditing the repo) will find the supplementary contradicting the main text on a headline directional claim.
- 【Specific fix】 In `10_genetics_mr_design.md` §3.1, replace "four of five assessable hubs give protective estimates concordant across all three methods" with "three of five assessable hubs (HLA-DQA1, CD14, FIS1) give protective estimates concordant across all three methods; HAVCR2 is directionally mixed (Egger OR 1.01) and CD74 is non-protective", and correct the same count in §4 ("four hubs protective") to three. Alternatively regenerate the .md from the CSVs so the two can never diverge.

---

### Finding A2-8 — The positive-control gate count is internally inconsistent: the manuscript and the candidates file say IFN-γ rescues 5/5 antigen-presentation genes; the positive-control check file records 4/5

**Tier 3** (consistency, but touching a "gate" — gates should never have two values)

- 【Problem】 The abstract (manuscript.md:14) and §3.7 (manuscript.md:117) state "IFN-γ rescued 5/5 antigen-presentation genes … satisfying the methodological positive-control gate", but `08_positive_control_check.csv` line 2 records "救回 4/5 抗原呈递基因: ['HLA-DRA', 'HLA-DRB1', 'HLA-DQA1', 'CD74']" — four, not five.
- 【Evidence】 `08_candidates_drugs.csv` line 4 (IFN-gamma row) lists `rescue_genes = HLA-DRA;HLA-DRB1;HLA-DQA1;HLA-DQB1;CD74` (5/5, rescue_fraction 0.714 of 7 targets). The check file's detail string lists only 4 genes and says 4/5. Both cannot be outputs of the same run unless the gate script used a different antigen-presentation list (likely omitting HLA-DQB1) than the candidates table. The gate threshold was "≥3/5" (manuscript.md:64), so the gate passes either way — but a "methodological positive-control gate" with two different pass records in the same submission is a provenance defect.
- 【Why it matters】 The entire repositioning argument leans on this gate as its one internal validity check (manuscript.md:64 explicitly calls it a consistency check). If the two files disagree about what the gate measured, the gate's value as a control is diminished and a reproducibility auditor will flag it immediately.
- 【Specific fix】 Re-run the positive-control script once, against a single frozen definition of the antigen-presentation gene set (enumerate the genes in a comment in the script), and regenerate both `08_positive_control_check.csv` and `08_candidates_drugs.csv` from that run. Then add one sentence to §2.8: "The antigen-presentation gene set used by the positive-control gate comprises exactly {list}; with this definition IFN-γ rescues {n}/5." Paste-ready sentence if the 4/5 result stands: "IFN-γ rescued 4/5 antigen-presentation genes in the positive-control check (HLA-DQB1 excluded by the gate's gene-set definition), satisfying the ≥3/5 methodological gate."

---

### Finding A2-9 — Winner's-curse / post-selection structure: all six hub genes were selected using GSE65682's outcome labels, and the MR layer then tests those same genes; the manuscript never quantifies or bounds the selection effect on the MR family size

**Tier 2** (the direction of the inference is honestly framed as hypothesis-generating, but the family-size logic deserves one explicit sentence)

- 【Problem】 The MR tests five genes that reached hub status through the same cohort's outcome labels (tri-method selection on 28-day death, §2.5), so the 45-test BH family understates the full multiplicity implicit in the pipeline (dozens of candidate genes → 6 hubs → 5 tested); the manuscript concedes selection-chain FWER is uncontrolled (Limitation 10, manuscript.md:199) but does not connect that concession to the MR layer.
- 【Evidence】 §2.5 (manuscript.md:55): candidate set from Mars1-DEG ∩ consensus immune set "expanded to top-300 death-associated DEGs when sparse"; three selectors; ≥2-method consensus produced 6 hubs. Limitation 10 (manuscript.md:199) covers the hub/signature selection chain but not the MR: "Hub-gene discovery chained several selections … so the effective family-wise error rate is uncontrolled and the hub set requires independent-cohort replication." The MR family of 45 tests is conditioned on the post-selection gene set without acknowledging that the family should logically include the genes that *failed* hub selection.
- 【Why it matters】 Genes selected for having strong expression-outcome association are precisely those whose cis-eQTL instruments are more likely to show pleiotropic outcome associations (correlated instrument-outcome horizontal paths), inflating MR false positives beyond what the 45-test BH controls. This is standard post-selection inference; it does not invalidate a Tier-3 hypothesis-generating layer, but the Limitations currently leave the impression that the MR correction (45 tests) fully handles multiplicity — it does not.
- 【Specific fix】 Paste-ready addition to Limitation 10 (manuscript.md:199), one sentence: "The same selection concern extends to the MR layer: because the five tested genes were promoted to hub status by their association with 28-day death in the discovery cohort, the pre-specified 45-test family controls multiplicity only conditional on that selection, and the MR results inherit an unquantified winner's-curse component; independent-cohort replication of the hub set (not merely the MR) is required before any causal reading."

---

### Finding A2-10 — No competing-risk or time-to-event treatment of 28-day mortality, and the signature is evaluated as a binary-day-28 classifier even for patients who died or were discharged before day 28

**Tier 2** (design note; both cohorts lack the data to do better, but the limitation should be stated precisely)

- 【Problem】 28-day mortality is treated throughout as a fixed binary label at day 28 (AUC classification), with no handling of competing discharges or censoring before day 28, and no time-to-event (Kaplan–Meier/Cox) analysis is reported despite the manuscript describing the signature as "prognostic".
- 【Evidence】 §2.1 (manuscript.md:43): `death_28d` (1.0=114, 0.0=365, unassigned=323); §3.4 evaluates AUC on this binary label; E-MTAB-4451 similarly supplies "28 day survival" as a binary SDRF field (manuscript.md:67). No survival-time field is used anywhere in the manuscript or in `09_ext_risk_scores.csv` (columns: sample, y, risk scores only). Limitation 8 (manuscript.md:197) covers the *endpoint scope* (no 90-day mortality) but never mentions the binary-classification-vs-time-to-event issue.
- 【Why it matters】 An AUC against a day-28 binary label overstates nothing if all patients have full 28-day follow-up, but ICU sepsis cohorts routinely have earlier discharges/deaths with differential follow-up; without a statement that follow-up is complete to day 28 for all 479 and all 106 patients, the AUC's denominator interpretation is ambiguous. A Cox model with the signature as a single covariate would be the field-standard presentation and costs one analysis.
- 【Specific fix】 Add one sentence to Limitation 8, paste-ready: "Within both cohorts, 28-day outcome is recorded as a complete binary status for all analysed patients (no loss to follow-up before day 28 is reported by the source studies), so the AUC treats day-28 death as a fixed binary label; time-to-event modelling (Cox regression with the signature as a continuous covariate, reporting hazard ratio per SD with 95% CI) was not possible because exact survival times are not distributed with either public dataset." If the Davenport SDRF does contain event times, replace with the actual Cox output: `03_results/09_cox_external.csv` with columns `cohort, n, n_events, hr_per_sd, ci_low, ci_high, p`.

---

### Finding A2-11 — Instrument strength is reported only as "median F 35–168" without per-gene minimums; the binding constraint is the per-gene *minimum* F (30.7 for CD74), and the weakest instruments sit exactly in the gene with the headline signal

**Tier 2** (reporting precision; values recompute correctly but the summary statistic chosen is the flattering one)

- 【Problem】 The manuscript summarises instrument strength as "median F 35–168" (manuscript.md:146) and per-gene median F in Table 3, but with 3–8 instruments per gene the minimum F is the design-relevant statistic for weak-instrument bias, and the minimums (30.7–33.4) are nowhere stated.
- 【Evidence】 Recomputed from `10_genetics_mr_outcome5086_harmonised.csv` (27 rows): per-gene min/median/max F — CD74 30.7/35.4/37.6; HLA-DQA1 86.9/168.1/1338.8; CD14 31.2/45.7/1382.2; HAVCR2 30.9/37.6/630.8; FIS1 33.4/75.0/2789.5. The manuscript's per-gene medians (Table 3, manuscript.md:152–156) match my recomputation exactly (35.4, 168.1, 45.7, 36.4*, 75.0 — *HAVCR2 median 37.6 in my computation vs 36.4 in Table 3; recomputing: HAVCR2 F values 630.8, 45.4, 37.6, 35.3, 34.0, 30.9 → sorted median = (35.3+34.0)/2 = 34.6, vs Table 3's 36.4. Recheck: values are 630.83, 45.38, 37.59, 35.30, 33.98, 30.93; sorted: 30.93, 33.98, 35.30, 37.59, 45.38, 630.83; median of 6 = (35.30+37.59)/2 = 36.44 ≈ 36.4. My earlier median was mis-sorted; Table 3's 36.4 is correct. I withdraw the discrepancy — Table 3 matches.) All F statistics exceed the conventional 10 threshold, so no weak-instrument bias is expected; the finding here is purely that the range as stated ("35–168") makes CD74's floor (30.7) look stronger than it is.
- 【Why it matters】 With 3 instruments, one borderline instrument (F=30.7) contributes disproportionate leverage to the CD74 estimates; the honest summary is "all F>30", which is still reassuring — there is no reason to hide the floor.
- 【Specific fix】 Paste-ready replacement for manuscript.md:146: "Instrument strength was adequate throughout: per-SNP F statistics ranged from 30.7 (CD74, 3 instruments) to 2,789 (FIS1), with all instruments exceeding F=30, an order of magnitude above the conventional weak-instrument threshold of 10." Add `min_F` and `max_F` columns to the per-gene summary in Table 3.

---

### Finding A2-12 — Two palindromic SNPs (rs6782228 CD14 C/G, rs6084653 FIS1 G/C) were retained despite the stated policy of dropping strand-ambiguous palindromes; both have MAF near 0.27–0.39 where strand resolution is least reliable

**Tier 1** (harmonisation-integrity check; low probability of flipping any conclusion but the stated policy and the data disagree)

- 【Problem】 The Methods state palindromic SNPs were "resolved by allele frequency and dropped when strand could not be determined" (manuscript.md:72), yet two palindromic instruments are present in the harmonised tables, and no record of the frequency-resolution decision is provided.
- 【Evidence】 Recomputed from `10_genetics_mr_outcome5086_harmonised.csv`: rs6782228 (CD14, C/G, EAF_exposure 0.2737 vs EAF_outcome 0.2674) and rs6084653 (FIS1, G/C, EAF 0.3664 vs 0.3873) are A/T- or C/G-palindromic and retained. For rs6782228, the outcome β (−0.0357, p=0.021) is one of the two drivers of the CD14 primary-outcome Egger signal (the other, rs424971, is non-palindromic); if this SNP's strand were mis-resolved the CD14 Egger estimate would shift. EAF agreement within 0.026 and 0.021 respectively suggests resolution succeeded, but the manuscript's blanket claim of "dropped when strand could not be determined" is unverifiable from the released data, and no per-SNP drop-list is included ("available on request", manuscript.md:72).
- 【Why it matters】 Palindrome handling is the most common harmonisation error in two-sample MR; a reviewer of the MR methods cannot audit the claim from the submitted files, and one of the two retained palindromes materially affects the only nominally significant primary-outcome test (CD14 Egger p=5.1×10⁻³).
- 【Specific fix】 Publish the per-SNP drop-list now (it is one CSV: `10_genetics_mr_harmonisation_log.csv` with columns `rsid, gene, action(retained/flipped/palindromic_dropped), reason, eaf_exposure, eaf_outcome, eaf_delta`) and add to §2.10: paste-ready sentence: "Two palindromic instruments (rs6782228, rs6084653) were retained after allele-frequency-based strand resolution (exposure vs outcome EAF within 0.03); the full harmonisation log, including every dropped SNP and its reason, is provided in `10_genetics_mr_harmonisation_log.csv`." As a sensitivity analysis, re-run the CD14 28-day-death MR-Egger excluding rs6782228 and report whether the nominal signal (OR 0.906, p=5.1×10⁻³) persists on five instruments.

---

### Finding A2-13 — The power narrative is incomplete: the manuscript claims the 1,896-case mortality GWAS leaves instruments "underpowered for individually small effects" but never reports the detectable OR at 80% power, which is computable and would show whether the null primary outcome is informative or merely underpowered

**Tier 1** (small analysis to add; changes how the null primary result should be read)

- 【Problem】 §3.10 and Limitation 2 assert underpowering (manuscript.md:173, :190) without quantifying it, leaving open whether the null IVW results on the primary outcome reflect absence of effect or absence of power — these have opposite implications for the paper's causal narrative.
- 【Evidence】 From `10_genetics_mr_outcome5086_harmonised.csv`, the median per-SNP F for the smallest gene (CD74, 3 IVs, median F=35.4) implies a 95% detectable-OR calculation: for a 2 d.f.-equivalent IVW test with median F≈35 and case fraction 1,896/486,484 ≈ 0.0039, the standard error of the log-OR scales as 1/(√(case fraction) × √ΣF-factor); with SE ≈ 0.31 (recomputed: CD74 IVW SE 0.312, `10_genetics_mr_outcome5086_28ddeath.csv` line 2), the 80%-power detectable |log OR| is 2.8×SE ≈ 0.87, i.e., OR 2.4 (or 0.42) — far beyond any plausible pharmacologically relevant effect. For CD14 (SE 0.064) the detectable OR is ≈1.20 — marginally adequate for effects of the size the expression model implies (OR ~0.9). The manuscript never performs or reports this arithmetic.
- 【Why it matters】 If the study can only detect ORs ≥2.4 for CD74, the null on the primary outcome is uninformative for that gene and should be labelled as such; if CD14 could detect 1.2, its null IVW (OR 0.927, p=0.24) is weakly informative. One computed sentence resolves this and preempts the standard reviewer demand.
- 【Specific fix】 New analysis spec: for each gene × outcome, compute the minimum detectable OR at 80% power and α=0.0056 (Bonferroni within the 45-test family) from the harmonised instrument set: `power = norm.power(beta_true, se_ivw, alpha)`, output `03_results/10_mr_power.csv` with columns `gene, outcome, n_iv, median_F, se_ivw, alpha, min_detectable_OR_80pct`. Paste-ready sentence for §3.10: "At 80% power under the 45-test family threshold, the primary-outcome analysis could detect only large effects for CD74 (minimum detectable OR ≈2.4 given SE 0.31), whereas CD14 (SE 0.064) could detect ORs down to ≈1.20 — so the CD74 null is uninformative while the CD14 null weakly bounds any protective effect at OR>0.83."

---

### Finding A2-14 — The abstract's signature claim chain ("reached a cross-validated AUC of 0.659 … the honest external generalization AUC 0.638") is properly ordered, but the Conclusion (§6) re-quotes the optimistic CV number first and calls the hubs "prognostically informative (within-cohort CV-AUC 0.659, optimistic; independent external AUC 0.638)" — the ordering inverts the paper's own honesty rule in its most-quoted section

**Tier 2** (wording; violates the manuscript's internal convention that the external estimate carries the claim)

- 【Problem】 §6 leads with the within-cohort CV AUC 0.659 and appends the external 0.638 in a parenthetical, whereas the manuscript's own convention (established at §3.4, Limitation 1, and the panel brief's trap list) is that the external estimate is "the honest generalization estimate" and must carry any prognostic claim.
- 【Evidence】 manuscript.md:207: "both prognostically informative (within-cohort CV-AUC 0.659, optimistic; independent external AUC 0.638 on E-MTAB-4451)". Contrast manuscript.md:189 (Limitation 1): "the external 0.638 is the honest generalization estimate." Also the hub-gene attribution conflates the 30-gene signature's AUC with the *hub genes*: the signature is 30 genes, of which the six hubs are a subset (CD74, FCGR3A, CD14, HLA-DQA1 appear in `S06_signature_genes.csv` lines 4, 6, 11, 20; HAVCR2 and FIS1 do not appear at all), yet §6 attributes the AUCs to "antigen-presentation/monocytic hub genes … that are both prognostically informative".
- 【Why it matters】 Two defects compound: (i) the optimism-ordered quoting invites quote-mining by later citing papers ("CV AUC 0.659"); (ii) the six hub genes were never themselves validated as a prognostic set — HAVCR2 and FIS1 are not in the 30-gene signature, and the signature's performance is not the hub set's performance. §3.4's first sentence ("The signature is dominated by antigen-presentation … genes", manuscript.md:106) is accurate; §6 is not.
- 【Specific fix】 Paste-ready replacement for manuscript.md:207, first clause: "The Mars1 immunosuppressed program is anchored by antigen-presentation/monocytic hub genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) — with a sixth recovered hub, FIS1, a mitochondrial-fission protein outside the immune set (§3.3) — and by a separate 30-gene immune-risk signature (which contains four of the six hubs) whose external, cross-platform AUC is 0.638 (95% CI 0.532–0.748; within-cohort CV 0.659 is optimistic and reported only as a training diagnostic)."

---

### Finding A2-15 — "Comparable to the published IRG benchmark" claim: my recomputation of the difference between the external AUC (0.638) and the recomputed benchmark (0.604) on the same 106 patients confirms the CIs overlap, but the manuscript never runs the paired test (DeLong) that would settle comparability on the same samples

**Tier 1** (one-line analysis; the claim "comparable rather than established as superior" is currently supported only by eyeballing)

- 【Problem】 §3.4/§3.5 assert the external signature is "comparable" to the IRG benchmark and that the ~0.034 AUC difference "is not statistically established" (manuscript.md:106), but no paired AUC comparison (DeLong or bootstrap of the difference on the same 106 patients) is computed, so the comparability claim rests on visual CI overlap.
- 【Evidence】 I recomputed from `09_ext_risk_scores.csv`: signature oriented-sum AUC 0.6382 (CI 0.529–0.738) and IRG3 benchmark AUC 0.6040 (CI 0.492–0.707) on the same 106 samples with the same 52 events; the per-sample paired difference is computable directly since both scores are present per patient. Overlapping marginal CIs do not establish a non-significant *paired* difference (correlated scores usually shrink the SE of the difference roughly 40–60%, so a 0.034 difference could be significant or not — only the paired test decides). The manuscript cites [18] (empirical calibration, Schuemie et al.) for "Calibration and decision-curve analytics" — a miscitation, as [18] concerns p-value calibration in observational studies, not decision-curve analysis.
- 【Why it matters】 "Comparable to benchmark" is a comparative claim about performance; with both scores measured on the same patients the paired test is the only valid basis, and its absence makes the sentence unfalsifiable either way. The miscited reference [18] compounds the impression of a statistical claim without statistical backing.
- 【Specific fix】 New analysis spec: on `09_ext_risk_scores.csv`, compute the DeLong paired test (or 2,000-resample bootstrap of the AUC difference) between `risk_oriented_sum` and `risk_irg3` against `y`; output `03_results/09_delong_signature_vs_irg.csv` with columns `auc_signature, auc_irg3, diff, se_diff, z, p, ci95_low, ci95_high`. Paste-ready replacement sentence for manuscript.md:106 (after recomputation): "On the same 106 patients, the paired DeLong test of the external signature AUC (0.638) versus the locally recomputed IRG benchmark (0.604) gives a difference of {diff} (95% CI {…}, p={p}), {supporting/failing to support} the claim of comparability."

---

### Finding A2-16 — The MR "switch to multiplicative random effects when Cochran Q exceeded its df" rule creates an estimator that varies per gene-outcome cell, but the I² heterogeneity range is quoted only for the primary outcome and the switching decision is itself data-dependent (a garden-of-forking-paths element)

**Tier 2** (wording/reporting; the per-test tabulation exists and is correctly referenced)

- 【Problem】 The fixed→random IVW switch triggered on Q for some cells (e.g., CD14 susceptibility Q=8.05 on df=5, model=random; CD74 28-day-death Q=2.55 on df=2, model=random) but not others, and the manuscript quotes heterogeneity as "low (I² 0.00–0.29)" on the primary outcome with the secondary-outcome maximum (0.50, FIS1 critical care) mentioned only in passing (manuscript.md:146).
- 【Evidence】 Recomputed from the three MR CSVs, `model` column: 28-day-death — CD74 IVW random (Q=2.55>df=2), HLA-DQA1 fixed, CD14 fixed, HAVCR2 random (Q=6.998>df=5), FIS1 fixed; susceptibility — CD74 fixed, HLA-DQA1 fixed, CD14 random, HAVCR2 random, FIS1 random; critical care — CD74 fixed, HLA-DQA1 fixed, CD14 fixed, HAVCR2 random, FIS1 random. Primary-outcome I² values recomputed: CD74 0.216, HLA-DQA1 0.00, CD14 0.00, HAVCR2 0.285, FIS1 0.00 — the manuscript's "I² 0.00–0.29" (manuscript.md:146) rounds 0.285→0.29 and 0.216→0.22 consistently with Table 4's per-cell I² column, which I verified cell-by-cell against the CSVs (all 15 values match). The data-dependent switch is disclosed in Methods (manuscript.md:72). So the tabulation is complete; the residual issue is only that the *rule itself* conditions the estimator on the data without a sensitivity note.
- 【Why it matters】 A reader comparing CD74's random-effects SE (0.312) against what a fixed-effects SE would have been (smaller) cannot tell how much the switch cost significance — CD74 critical care would have been *more* significant under fixed effects, so here the conservative choice was made, which is reassuring; but for HAVCR2 susceptibility the random switch widens an already-null estimate. One sentence noting the direction of the switch's effect on each quoted significant result would close the loop.
- 【Specific fix】 Paste-ready sentence for §3.10 after Table 4: "The Q-triggered switch from fixed to multiplicative random effects (Methods) was triggered for 5 of 15 IVW cells; for the two results emphasised here (CD74 critical care, CD14 28-day death) the switch was conservative — CD74 critical care was analysed under random effects despite Q_p=0.95 being triggered by the Q>df rule at df=2 — so quoted significances are not artifacts of an opportunistic fixed-effects choice." (Alternatively: state that fixed-effects IVW for CD74 critical care gives OR 2.222, p=0.0140, identical, since Q was near zero — the rule as implemented fires on Q>df regardless of Q_p, which for df=2 fires at trivial heterogeneity; consider re-triggering only when Q_p<0.05.)

---

### Finding A2-17 — Reference [18] is miscited as the source for "Calibration and decision-curve analytics"

**Tier 3** (reference error)

- 【Problem】 Manuscript.md:106 cites "[18]" (Schuemie et al., empirical p-value calibration for observational studies) for "Calibration and decision-curve analytics", but decision-curve analysis is Vickers et al. and calibration is not what [18] describes.
- 【Evidence】 Reference list entry 18 (manuscript.md:275): "Schuemie MJ, Ryan PB, DuMouchel W, Suchard MA, Madigan D. Interpreting observational studies: why empirical calibration is needed to correct p-values. Statistics in Medicine. 2013" — a paper on empirical calibration of p-values in observational database studies, not prediction-model assessment. The citing sentence (manuscript.md:106): "Calibration and decision-curve analytics [18] for the external score are in Fig. S06".
- 【Why it matters】 Wrong-method citation in the validation section signals the calibration/decision-curve work was not methodologically anchored; combined with Finding A2-5 (the cited figure does not even show what the sentence claims), the entire calibration/decision-curve paragraph fails audit.
- 【Specific fix】 Replace the citation with the correct methodological sources — paste-ready: "Calibration was assessed by logistic calibration (intercept and slope) and decision curves per Vickers et al. (Vickers AJ, Elkin EB. Decision curve analysis: a novel method for evaluating prediction models. Med Decis Making. 2006;26(6):565-574), and Brier score per the TRIPOD statement (Collins GS, et al. BMJ 2015;350:g7595)." — contingent on actually performing the analyses (see Finding A2-5).

---

### Finding A2-18 — The susceptibility outcome is described as "null except for a CD74 Egger signal driven by horizontal pleiotropy" but the CD74 susceptibility Egger signal is family-significant (q=0.0025) *and* carries a significant intercept — the manuscript's handling (attribute to pleiotropy, discard) is defensible but the q-value is simultaneously counted as a family-wise "hit" in the Methods summary ("three CD74 tests reached q<0.05"), double-counting one result as both evidence-bearing and disqualified

**Tier 2** (internal framing consistency)

- 【Problem】 The Methods paragraph (manuscript.md:72) counts the CD74 susceptibility Egger test among "three CD74 tests reached q<0.05", while §3.10 (manuscript.md:171) and Limitation 2 (manuscript.md:190) attribute that same test to directional pleiotropy and disqualify it — so the study's own accounting alternates between 3 significant family-wise results and 2, depending on the section.
- 【Evidence】 manuscript.md:72: "three CD74 tests reached *q*<0.05 — critical-care MR-Egger (*q*≈1.5×10⁻¹¹) and weighted median (*q*≈0), and susceptibility MR-Egger (*q*≈0.0025)". manuscript.md:171: the susceptibility Egger "was accompanied by a significantly non-zero intercept (*P*=1.0×10⁻⁴), indicating directional (horizontal) pleiotropy [24]; it is likewise not interpretable as causal." manuscript.md:173: "it confirms the three CD74 critical-care/susceptibility tests as the only ones below *q*<0.05" — again counting it. My recomputation confirms q=2.47×10⁻³ for that test (10_mr_bh_family.csv line 2) and intercept p=9.98×10⁻⁵ (10_genetics_mr.csv line 3) — both numbers match the manuscript. The inconsistency is purely in the narrative framing.
- 【Why it matters】 A careful reader meets "3 significant tests" in Methods, "2 usable significant results" in Results, and "3" again in Limitations. Since the study's central honesty move is conservative accounting, the count should be stated once, consistently, with the pleiotropy attribution applied uniformly.
- 【Specific fix】 Standardise on the conservative count. Paste-ready replacement for manuscript.md:72 (final clause): "under which two CD74 tests reached q<0.05 on the critical-care outcome (MR-Egger q≈1.5×10⁻¹¹ and weighted median q=1.5×10⁻¹⁷ after correcting an underflowed p; see §3.10), while the third nominally significant test (susceptibility MR-Egger, q≈0.0025) carries a significant pleiotropy intercept and is not interpreted." Apply the same "two usable" count at manuscript.md:173 and manuscript.md:190.

---

## § 2. Stands up (suspected wrong, verified correct — do not change these)

### S2-1 — The 45-test BH family values quoted in the manuscript are correct (after the underflow fix)

I recomputed the entire BH procedure from the raw p-values in the three outcome CSVs. The CD14 28-day-death Egger family q = 0.0575 (manuscript: 0.058 ✓); per-outcome 15-test q = 0.0766 (manuscript: 0.077 ✓); CD74 susceptibility Egger family q = 2.47×10⁻³ (manuscript: 0.0025 ✓); CD74 critical-care Egger family q = 1.49×10⁻¹¹ (manuscript: 1.5×10⁻¹¹ ✓). `10_mr_bh_family.csv`'s per-outcome and family columns reproduce BH exactly for all 45 rows (my only discrepancy was the CD74 weighted-median zero, Finding A2-1). The manuscript's framing — "this gives q≈0.058 and does not cross the 0.05 threshold" for CD14 — is accurate and appropriately deflating.

### S2-2 — The external validation numbers are genuine and reproducible from per-sample data

I recomputed the external AUCs from the 106-row per-sample file `09_ext_risk_scores.csv` (52 deaths — matches manuscript.md:67 and :109): oriented-sum AUC = 0.6382 vs manuscript 0.638 ✓; locked-L1 AUC = 0.5848 vs manuscript 0.585 ✓; my bootstrap CIs (0.529–0.738 and 0.475–0.692) match the manuscript's reported (0.532–0.748, 0.469–0.696) within bootstrap-seed variation. I also verified the gene-set bookkeeping: `S06_signature_genes.csv` has exactly 30 rows; 29 mapped genes confirmed by `09_external_validation.csv` lines 3 and 17 (HLA-DQA1 missing). The locked-L1 honesty (0.585 transported worse than the fixed-orientation 0.638, correctly interpreted as "the gene set and orientation, not the learned weights, are the portable component", manuscript.md:109) is exemplary reporting.

### S2-3 — The MR instrument bookkeeping (27 instruments; FCGR3A exclusion) is exactly as claimed

Recomputed from the harmonised tables: 27 unique rsIDs, no duplicates, per-gene counts CD74 3 / HLA-DQA1 4 / CD14 6 / HAVCR2 6 / FIS1 8 = 27 (manuscript.md:72 ✓, Table 3 ✓). All three outcome-specific harmonised files carry the identical 27 instruments with identical exposure-side effects and F statistics, as they should. FCGR3A is marked `insufficient_instruments` in all three outcome files rather than silently dropped — matching manuscript.md:144's explicit statement, and the design document's claim that re-querying at looser thresholds still returns two variants is consistent with the FCGR3A row appearing in no result file. I also verified no outcome-side p-value filtering occurred post harmonisation (outcome p-values as low as 0.0097 — rs9944715, FIS1 — are retained with null gene-level results).

### S2-4 — Per-gene median F statistics in Table 3 recompute exactly

CD74 35.4, HLA-DQA1 168.1 (mean of the two central order statistics of 1338.8/246.8/89.4/86.9), CD14 45.7, HAVCR2 36.4, FIS1 75.0 — all five match Table 3 (manuscript.md:152–156) to the reported precision. I initially suspected the HLA-DQA1 and HAVCR2 values were wrong (suspecting the mean-of-two-middle convention had been misapplied) but both recomputed correctly under the even-n median convention.

### S2-5 — The Mars1 immune-score median (−0.79) and the full-cohort range (−3.65 to 3.86) recompute exactly

From `S02_immunoparalysis_score.csv` (802 rows): Mars1 median −0.7917 (manuscript −0.79 ✓, manuscript.md:100); full-cohort min/max −3.6496/+3.8616 (manuscript −3.65/3.86 ✓). Endotype sample counts also match §2.1 exactly (Mars1 132, Mars2 176, Mars3 118, Mars4 53, unassigned 323; 479 endotyped with 114 deaths — recomputed ✓, manuscript.md:43).

---

## § 3. Questions for the authors

1. **A2-1**: At what stage was the CD74 critical-care weighted-median p-value computed such that it stored as exact 0.0 rather than ~6.7×10⁻¹⁹? Was any other p-value in the pipeline computed by the same route (e.g., in the L1000 or DEG layers)?
2. **A2-2**: What is the UK Biobank participant fraction within eQTLGen for the six specific genes tested (the per-gene n varies 13,344–31,684, so the overlap fraction is gene-specific)? Have you attempted the Burgess–Davies–Thompson [31] correction, and if not, is the per-gene UKB overlap fraction obtainable from the eQTLGen supplementary tables?
3. **A2-3**: For the CD74 susceptibility Egger signal (the pleiotropy attribution), which SNP drives the intercept? A leave-one-out table would settle whether the intercept is one influential instrument or a diffuse pattern — was this computed?
4. **A2-4**: Where is the pre-specification of the 45-test family documented (file, date, repository commit)? If it exists only in prose, will you downgrade the word "pre-specified" to "primary"?
5. **A2-5**: Was the decision-curve in `S06_dca.png` computed on the GSE65682 cohort or on the external score? If external, why does the curve title not say so, and why does the hub-score curve show net benefit below treat-none above threshold 0.2 — was this figure inspected before being cited as supportive?
6. **A2-8**: Which gene-set definition does the positive-control gate script use — the one that yields 5/5 (`08_candidates_drugs.csv`) or 4/5 (`08_positive_control_check.csv`)? Was HLA-DQB1 dropped at the gate stage, and if so why does the candidates table retain it?
7. **A2-12**: For the two retained palindromic SNPs (rs6782228, rs6084653), what EAF-difference tolerance was used for strand resolution, and does the CD14 Egger nominal signal survive dropping rs6782228?
8. **A2-10**: Do either GSE65682 or E-MTAB-4451 distribute exact survival times (days to death/discharge)? If yes for E-MTAB-4451 (the Davenport SDRF typically carries event dates), why was a Cox analysis not run?

---

## § 4. What I actually checked

**Files read in full:**
- `05_reports/manuscript.md` (all 288 lines, including the four long truncated paragraphs recovered separately)
- `05_reports/review_r6/_PANEL_BRIEF.md`
- `03_results/10_genetics_mr.csv` (17 rows: susceptibility, 15 tests + FCGR3A placeholder)
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv` (17 rows: primary outcome)
- `03_results/10_genetics_mr_outcome4982_criticalcare.csv` (17 rows: critical care)
- `03_results/10_genetics_mr_harmonised.csv`, `10_genetics_mr_outcome5086_harmonised.csv`, `10_genetics_mr_outcome4982_harmonised.csv` (27 instrument rows each)
- `03_results/10_mr_bh_family.csv` (45 rows)
- `03_results/10_genetics_mr_design.md` (S10 design document, 123 lines)
- `03_results/S06_signature_genes.csv` (30 rows), `S06_auc_compare.csv` (6 rows)
- `03_results/09_external_validation.csv`, `09_external_validation_coef.json`, `09_ext_risk_scores.csv` (106 rows)
- `03_results/08_candidates_drugs.csv`, `08_positive_control_check.csv`
- `03_results/S02_immunoparalysis_score.csv` (802 rows)
- `04_figures/S06_dca.png` (decision-curve figure, inspected visually)

**Values recomputed (manuscript value → my value → match?):**

| # | Quantity | Manuscript | My recomputation | Verdict |
|---|----------|-----------|------------------|---------|
| 1 | 45-test family q, CD74 critcare WMed | ≈0 | 1.50×10⁻¹⁷ (p underflowed in file; recomputed p=6.65×10⁻¹⁹) | **DISCREPANCY** (A2-1) |
| 2 | 45-test family q, CD74 critcare Egger | 1.5×10⁻¹¹ | 1.49×10⁻¹¹ | match |
| 3 | 45-test family q, CD74 suscept Egger | 0.0025 | 2.47×10⁻³ | match |
| 4 | 45-test family q, CD14 28d-death Egger | 0.058 | 0.0575 | match |
| 5 | 15-test per-outcome q, CD14 28d Egger | 0.077 | 0.0766 | match |
| 6 | 15-test per-outcome q, CD74 critcare IVW | not stated | 0.0701 (fails 0.05) | **OMISSION** (A2-4) |
| 7 | CD74 critcare IVW OR (CI) | 2.222 (1.175–4.200) | 2.222 (1.175–4.200) | match |
| 8 | CD74 critcare WMed z | — (p=0) | z=8.881 | underflow source identified (A2-1) |
| 9 | Instrument counts per gene | 3/4/6/6/8 | 3/4/6/6/8 (=27 unique rsIDs, no duplicates) | match |
| 10 | Per-gene median F | 35.4/168.1/45.7/36.4/75.0 | 35.4/168.1/45.7/36.4/75.0 | match (initially suspected HLA-DQA1 & HAVCR2, verified correct) |
| 11 | Per-gene minimum F | not stated | 30.7 (CD74) | omission noted (A2-11) |
| 12 | External AUC, oriented-sum | 0.638 (0.532–0.748) | 0.6382 (bootstrap 0.529–0.738) | match |
| 13 | External AUC, locked L1 | 0.585 (0.469–0.696) | 0.5848 (0.475–0.692) | match |
| 14 | IRG3 benchmark AUC on E-MTAB-4451 | 0.604 | 0.6040 (0.492–0.707) | match |
| 15 | n / deaths, external cohort | 106 / 52 | 106 / 52 | match |
| 16 | Signature gene count | 30 (29 mapped, HLA-DQA1 missing) | 30 rows; 29 mapped confirmed | match |
| 17 | Hub membership in signature | §6 attributes AUC to hubs | HAVCR2 & FIS1 absent from the 30 genes | **DISCREPANCY** (A2-14) |
| 18 | Mars1 score median | −0.79 | −0.7917 | match |
| 19 | Full-cohort score range | −3.65 to 3.86 | −3.6496 to 3.8616 | match |
| 20 | "Lowest median among four endotypes" | implied separation | Mars1 −0.792 vs Mars2 −0.752, MW p=0.467 | **NOT SUPPORTED** (A2-6) |
| 21 | Immune score AUC for death | not stated | 0.604 (recomputed, 479 patients) | context for A2-6 |
| 22 | IFN-γ positive-control gate | 5/5 | 4/5 in check file; 5/5 in candidates file | **INTERNAL CONTRADICTION** (A2-8) |
| 23 | S10 "concordant protective hubs" | three (manuscript) / four (design .md) | three (recomputed from estimates) | **INTERNAL CONTRADICTION** (A2-7) |
| 24 | Palindromic SNPs retained | "dropped when strand undetermined" | rs6782228, rs6084653 retained | **POLICY/DATA MISMATCH** (A2-12) |
| 25 | I² primary outcome range | 0.00–0.29 | 0.00–0.285 | match |
| 26 | I² max secondary | 0.50 (FIS1 critcare) | 0.5018 | match |
| 27 | CD74 suscept Egger intercept p | 1.0×10⁻⁴ | 9.98×10⁻⁵ | match |
| 28 | CV AUC / train AUC | 0.659 / 0.750 | 0.6586 / 0.7495 (S06_auc_compare.csv) | match (not independently reproducible beyond file) |
| 29 | Mars1 DEG count 3,597; sepsis-vs-ctrl 448 | stated | not recomputed (expression matrices not re-derived) | unchecked — outside my scope |
| 30 | Fig. S06 claim (calibration/DCA of external score) | cited as supportive | figure is a training-cohort DCA, net benefit < treat-none above threshold ≈0.2 | **MISCITATION** (A2-5, A2-17) |

---

## § 5. Verdict: **Major revision**

The manuscript's self-auditing culture is genuinely above the norm for this genre — the 45-test family correction, the locked-L1 honesty, the reversed-direction CD74 caveat, and the disclosure of score circularity are all things I expected to find missing and did not. But the paper still asks me to accept a multi-layer inferential structure whose weakest load-bearing element — the MR layer — rests on 3–8 instruments per gene with an exposure–outcome sample overlap it acknowledges but never corrects, an Egger-intercept diagnostic it uses asymmetrically (reassurance when null, disqualification when significant) despite power that makes both uses unsupportable, and a headline number ("q<10⁻¹¹") that is estimator-selected: under the primary IVW estimator, corrected q for that same test is 0.126 and is stated nowhere. The single strongest reason for major revision rather than minor: **the CD74 critical-care result is the manuscript's most quotable MR finding, yet no correction family and no estimator choice consistent with the paper's own declared primary estimator (IVW) supports it as significant, and the one sentence that would make this transparent ("no IVW estimate reaches q<0.05 under any family") is absent from every summary section.** The required additions are tractable — sample-overlap correction or explicit SE-inflation estimate, leave-one-out pleiotropy analysis, a paired DeLong comparison against the benchmark, one honest calibration analysis for the external score, correction of the underflowed zero, and the four internal-consistency fixes (S10 four-vs-three, 5/5-vs-4/5, §6 hub/signature conflation, the palindromic-SNP disclosure) — none of which threatens the Tier-1 expression-level findings, which is precisely why the paper should be fixed rather than rejected.
