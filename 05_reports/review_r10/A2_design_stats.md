# A2 — Design & statistics reviewer report
**Manuscript:** "Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning" (v1.9.0, single-author, treated as first submission)
**Reviewer role:** Causal inference / biostatistics (independent first-look)
**Scope:** Design and statistics layer — MR validity, family correction, signature AUC, calibration/DCA, selection circularity, article-type fit.

---

## What I actually checked (files, commands, recomputed values, discrepancies)

**Files read:** `manuscript.md`, `03_results/10_genetics_mr_outcome5086_28ddeath.csv`, `03_results/10_genetics_mr_outcome4982_criticalcare.csv`, `03_results/10_mr_bh_family.csv`, `03_results/09_external_validation.csv`, `03_results/09_ext_calibration_dca.csv`, `03_results/09_ext_dca_grid.csv`, `03_results/S06_auc_compare.csv`.

**Recomputations (Python 3.13, `scipy.stats`):**
- MR-Egger two-sided p from `β` and `SE` with `df = n_snp − 2`, compared to both `2·st.t.sf(|t|, df)` and `2·st.norm.sf(|t|)`.
- Family-BH readout: counted rows, `family_sig_q<0.05` flags, primary-outcome IVW significance.
- Calibration slope/intercept and DCA net-benefit grid parsed directly.

**Recomputed values (primary 28-day-death Egger, `10_genetics_mr_outcome5086_28ddeath.csv`):**

| Gene | n_snp | df | t | stored p | t-dist p | normal p | match |
|------|------|------|------|------|------|------|------|
| CD74 | 3 | 1 | 0.1918 | 0.879369 | 0.879369 | 0.847909 | **t-dist** |
| HLA-DQA1 | 4 | 2 | 0.6968 | 0.558047 | 0.558047 | 0.485956 | **t-dist** |
| CD14 | 6 | 4 | 2.8000 | 0.048809 | 0.048809 | 0.005110 | **t-dist** |
| HAVCR2 | 6 | 4 | 0.0606 | 0.954613 | 0.954613 | 0.951708 | **t-dist** |
| FIS1 | 8 | 6 | 0.7332 | 0.491091 | 0.491091 | 0.463450 | **t-dist** |

All five primary Egger p-values, and the five critical-care Egger p-values, match the **t-distribution** to 6 d.p. and diverge substantially from the normal distribution (e.g., CD14: t-dist 0.0488 vs normal 0.0051). **No discrepancy** between the recomputed t-distribution value and the printed Table 3 values (CD74 0.88, HLA-DQA1 0.56, CD14 4.9e-2, HAVCR2 0.95, FIS1 0.49).

**Family BH (`10_mr_bh_family.csv`):** 45 rows total; exactly **1** with `family_sig_q<0.05` = YES (CD74 weighted median, critical care, OR 2.194, p=6.65e-19, q_family=2.99e-17). Primary-outcome (5086) IVW: 5 rows, **0** with p<0.05 (p = 0.236, 0.260, 0.473, 0.718, 0.847). Verified.

**Calibration/DCA:** `09_ext_calibration_dca.csv` → slope **0.5028**, intercept **−0.0382**. `09_ext_dca_grid.csv` → `nb_model` > 0 from threshold 0.05 to 0.75; `nb_model == nb_treat_all` at 0.05–0.25; first `nb_model`=0 at threshold 0.80 (converges near 0.77). Verified.

**Discrepancies / inconsistencies found (minor):**
1. **IRG benchmark label collision.** `09_external_validation.csv` stores the *recomputed* E-MTAB-4451 IRG as **0.604** (the value the manuscript actually uses for comparison), but `S06_auc_compare.csv` labels a row `IRG 基准(E-MTAB-4451), 0.619` — that 0.619 is Peng et al.'s *reported* value, not the recomputed one. Two different numbers sit under an "E-MTAB-4451" IRG label. A reader can conflate them.
2. **CV-AUC rounding drift.** Manuscript prints CV AUC 0.659; `S06_auc_compare.csv` = 0.6586; `09_external_validation.csv` `auc_GSE65682_CV_locked` = 0.6582. Trivial, but the three should agree to the same precision.
3. **"Well behaved" calibration is overstated** (see item 6).

---

## Verification findings

### Item 1 — MR-Egger p-values are t-distributed (no discrepancy, but a df caveat)

**【Problem】** The manuscript claims Egger p-values were corrected to the t(n−2) distribution; this must be confirmed against a normal-distribution alternative.

**【Evidence】** Recomputed above from `β`/`SE` in `10_genetics_mr_outcome5086_28ddeath.csv` and `10_genetics_mr_outcome4982_criticalcare.csv`. All 10 Egger rows match `2·st.t.sf(|β/se|, n_snp−2)` exactly; none match the normal value. Printed Table 3 values are faithful to the t-distribution.

**【Why it matters】** The claim is correctly implemented — there is no normal-vs-t error. However, for CD74 (n_snp = 3 → df = 1) the t-distribution is Cauchy and the Egger slope test has essentially **zero power** to detect pleiotropy; the corrected p is valid but uninformative (the authors already note this for the Egger *intercept*). The corrected p-values are sound; the *tests* at df=1 are not.

**【Specific fix】** No change needed to the p-values. Add one clarifying sentence: *"For the CD74 analyses (n_snp = 3) the MR-Egger slope and intercept tests have df = 1 and therefore cannot detect pleiotropy or yield a stable standard error; their p-values are reported for completeness only."*

---

### Item 2 — MR design validity (sample overlap, Steiger, concordance, reversed signal)

**【Problem】** eQTLGen exposure and UK Biobank outcomes share participants; no overlap correction was applied, and no Steiger directionality test was done — so MR estimates are not interpretable as causal.

**【Evidence】** §2.10/§3.10: eQTLGen (31,684 donors, includes UK Biobank participants) overlaps the UKB sepsis outcomes; authors state they "did not apply a sample-overlap correction." Steiger explicitly "not performed." On the primary outcome, three hubs (HLA-DQA1, CD14, FIS1) show OR<1 across **all three** estimators (IVW/Egger/weighted-median) — directional concordance is genuine but non-significant (IVW p = 0.260/0.236/0.473). The only family-significant result (CD74 critical-care weighted median, OR 2.194, q≈3e-17) **reverses** the Mars1 direction (Mars1 has CD74 *down*; MR says higher genetically predicted CD74 predicts *worse* critical care) and rests on 3 SNPs. Its Egger is not significant (p=0.088, q_family=0.79), and its Egger SE (0.111) is implausibly smaller than its own IVW SE (0.325) — the authors flag this.

**【Why it matters】** Sample overlap biases standard errors **downward**, inflating type-I error exactly where it matters most — the single "significant" signal (CD74 critical care) is the most overlap-exposed and is also direction-reversed. Without Steiger, the assumed causal direction (expression → sepsis outcome) is unverified, so even a significant MR could reflect reverse causation/pleiotropy. The MR layer cannot carry a causal claim; it is at best a directional, hypothesis-generating signal.

**【Specific fix】** Keep the existing "genotype–severity association, not a causal hub claim" framing. Add a sensitivity-analysis pledge: *"Because exposure–outcome overlap can bias MR standard errors downward (Burgess et al. 2016), we will report a sample-overlap bias-corrected sensitivity (mr_sampleoverlap) for the CD74 critical-care signal, and a Steiger directionality test, before any claim beyond hypothesis generation."* Do not promote the CD74 critical-care result beyond a genotype–severity association.

---

### Item 3 — Family correction (1/45 significant, reverses; 0/5 primary IVW) and the "MR layer is null" conclusion

**【Problem】** Verify the family-correction count and assess whether "the MR layer is null and hypothesis-generating" is an accurate conclusion.

**【Evidence】** `10_mr_bh_family.csv`: 45 tests, exactly 1 family-significant (CD74 weighted median, critical care, q=2.99e-17, direction-reversed). Primary outcome (5086) IVW: 0/5 with p<0.05. The CD14 28-day-death Egger (p=0.049) has q_family = 0.73 → not significant. Verified exactly as stated.

**【Why it matters】** The family correction is correctly executed. But "null" is imprecise: there *is* one family-significant signal (direction-reversed, genotype–severity) and a consistent **directional** (non-significant) protective pattern across three hubs on the primary outcome. "Null" should mean "no significant evidence for the expression-level causal hypothesis," not "no signal at all."

**【Specific fix】** Replace *"the MR layer is null and hypothesis-generating"* (Abstract, §3.10, §4, Conclusion) with: *"the MR layer yields no significant evidence supporting the expression-level causal hypothesis — the only family-significant result reverses the Mars1 direction and is reported as a genotype–severity association, and the primary outcome shows a consistent but non-significant protective direction across three hubs — and is therefore hypothesis-generating."*

---

### Item 4 — Selection-on-outcome circularity (Limitation 12)

**【Problem】** Six candidate genes were selected from the same cohort for expression-association with endotype/28-day death, then MR-tested for causal effect — does this void "independent confirmation"?

**【Evidence】** Limitation 12 (verbatim intent): *"The MR is therefore a within-cohort-generated hypothesis test rather than an independent confirmation of the expression signal."* Genes were chosen because they are expression-associated with the sepsis endotype and 28-day death in GSE65682, then tested for causal effect on sepsis outcomes.

**【Why it matters】** The framing is **honest** — the authors do not claim the MR as independent confirmation, and they correctly note the BH correction controls multiplicity over the chosen genes but not their outcome-driven selection. The circularity means the MR null can neither *confirm* nor *refute* the expression association (different level of evidence: observational expression vs germline causality), and it weakens even the "hypothesis-generating" value because the genes were not independently chosen. This is a limitation, not a fabrication.

**【Specific fix】** Strengthen Limitation 12 one line: *"Consequently, the MR result does not confirm or refute the expression-level association; it is a separate, weaker test of germline causality on a candidate set selected for its expression association, and should be read as hypothesis-generating only."*

---

### Item 5 — Signature AUC (optimism, EPV, IRG comparison)

**【Problem】** The 5-fold CV AUC 0.659 is label-informed/optimistic; external orientedSum 0.638 (CI 0.532–0.748); EPV ≈ 3.8 (<10 rule); IRG comparison is point-estimate only.

**【Evidence】** `S06_auc_compare.csv`: CV 0.6586, train 0.7495 (manuscript 0.659/0.750). `09_external_validation.csv`: orientedSum 0.6382, CI 0.5317–0.7475. EPV = 114 deaths / 30 genes = **3.8** (confirmed). IRG recomputed on E-MTAB-4451 = 0.604 (no CI, no formal test); the signature CI (0.532–0.748) *contains* 0.604, so descriptively comparable but not demonstrated as "comparable." The locked L1 model transported poorly (AUC 0.585) and 7/29 coefficients are exactly zero — consistent with EPV-driven instability.

**【Why it matters】** The "real but modest, comparable not superior" framing is *mostly* honest (the authors concede no CI/formal test on IRG), but the headline slightly oversells: without an IRG confidence interval and an equivalence/non-inferiority test, "comparable" is asserted, not shown. The signature is a biological signal, not a clinical predictor — the EPV of 3.8 and zero-coefficient instability cap confidence. The IRG label collision in `S06_auc_compare.csv` (0.619 vs 0.604) can mislead a reader about which benchmark is being compared.

**【Specific fix】** (a) Relabel the `S06_auc_compare.csv` row as `IRG benchmark (E-MTAB-4451, Peng reported) = 0.619` to distinguish it from the recomputed 0.604. (b) Soften the claim: *"The external AUC 0.638 (95% CI 0.532–0.748) is real but modest; it overlaps the recomputed IRG benchmark (0.604, point estimate only, no CI), so the two are descriptively similar rather than established as equivalent — a formal DeLong test is precluded by the missing IRG CI."* (c) State explicitly that the signature is a biological-ranker, not a calibrated clinical predictor, given EPV 3.8.

---

### Item 6 — Calibration / DCA (slope 0.50 is NOT "well behaved")

**【Problem】** The external calibration slope is 0.50 (ideal = 1.0) yet the manuscript calls calibration "well behaved"; the DCA net benefit equals treat-all at low thresholds.

**【Evidence】** `09_ext_calibration_dca.csv`: slope **0.5028**, intercept **−0.0382**. A slope of 0.50 means observed log-odds are ~half the predicted — the score's probabilities are **over-confident / require recalibration** (logistic slope/intercept update). The intercept −0.04 is good (centered). `09_ext_dca_grid.csv`: `nb_model` > 0 from 0.05–0.75, but `nb_model == nb_treat_all` at 0.05–0.25 (model adds nothing over treat-all there); first `nb_model`=0 at 0.80 (converges near 0.77). The DCA claim "net benefit >0 across 0.10–0.75, converging to 0 near 0.77" is numerically verified.

**【Why it matters】** Calling a slope-0.50 calibration "well behaved" is inaccurate and overstates the external-validation strength. The AUC *discrimination* generalises, but the *calibration* does not — the score should be used as a ranker, not as calibrated probabilities, until recalibrated. The DCA supports discrimination-based decision utility only in a mid-range and only after the calibration caveat is acknowledged.

**【Specific fix】** Replace *"Calibration of the external equal-weight score was well behaved (slope 0.50, intercept −0.04)"* with: *"The external equal-weight score had an acceptable calibration intercept (−0.04) but a calibration slope of 0.50, indicating over-confident predicted probabilities that would require logistic recalibration before threshold-based use; the score is therefore presented as a ranker rather than as calibrated risk probabilities."*

---

### Item 7 — Does the article-type decision hinge on any design flaw?

**【Problem】** Whether any flaw found changes Research vs Methods/Resource classification.

**【Evidence】** The study is an integrative re-analysis of public cohorts + computational drug repositioning + MR. It introduces no new method, no new resource, and no new primary data. The flaws identified (calibration overstatement, selection circularity, overlap-inflated MR, IRG label collision) are framing/limitation issues, not article-type determinants.

**【Why it matters】** None of the design flaws change the article type. It remains a **Research** article (a bioinformatics application/integration study), not a Methods or Resource paper. The flaws argue for tightening the calibration and MR framing — not for reclassification.

**【Specific fix】** No article-type change warranted. Ensure the title/abstract do not imply a "method" or "resource" contribution the content does not deliver (the manuscript already frames it as a "multi-omics dissection," which is appropriate).

---

## § Stands up (verified, with evidence)

1. **MR-Egger p-values are correctly t-distributed.** All 10 Egger rows (primary + critical care) match `2·st.t.sf(|β/se|, n_snp−2)` to 6 d.p.; none match the normal distribution. The manuscript's "corrected to the t(n−2) distribution" claim and the printed Table 3 Egger p-values are accurate. *(Evidence: recomputation above.)*
2. **Family-BH correction is exactly as reported.** 45 tests, exactly 1 family-significant (CD74 weighted median, critical care, q≈3e-17, direction-reversed); 0/5 primary-outcome IVW significant. *(Evidence: `10_mr_bh_family.csv` parsed, counts confirmed.)*
3. **External generalisation is real and honestly scoped.** External AUC 0.638 (95% CI 0.532–0.748) excludes 0.5 by a clear margin; the authors explicitly flag the within-cohort CV AUC 0.659 as optimistic and report the poor L1 transport (0.585). *(Evidence: `09_external_validation.csv`.)*
4. **Methodological honesty about limitations is a genuine strength.** Selection-on-outcome circularity (Limitation 12), exposure–outcome overlap, the glucocorticoid positive-control caveat, and the direction-reversed CD74 signal are all disclosed rather than buried — rare and commendable for a single-author computational paper.
5. **DCA shows positive net benefit in a usable mid-range.** `nb_model` > 0 from threshold 0.05 to 0.75 (verified), supporting discrimination-based decision utility once calibration is addressed.
6. **Directional concordance across three MR estimators on three hubs** (HLA-DQA1, CD14, FIS1 all OR<1 under IVW/Egger/weighted-median on the primary outcome) is a real, if non-significant, signal worth flagging as hypothesis-generating.

---

## § Questions for the authors

1. Will you add a **sample-overlap bias-corrected sensitivity** (e.g., `mr_sampleoverlap`, Burgess et al. 2016) for the CD74 critical-care signal, given that overlap biases SEs downward precisely where the only "significant" result sits?
2. Will you add a **Steiger directionality test** as a sensitivity, to confirm the assumed eQTL→outcome causal direction?
3. Can you report the IRG benchmark on E-MTAB-4451 **with a bootstrap CI** and run a **DeLong test** against the signature before claiming "comparable"? (Currently the IRG is a single point estimate.)
4. Given calibration **slope = 0.50**, will you present a **logistic-recalibrated** version, or explicitly restrict the score to ranking use and remove the "well behaved" wording?
5. With **EPV ≈ 3.8** and 7/29 zero coefficients, can you report bootstrap stability (coefficient CIs / frequency of non-zero selection) to bound the optimism of the discovery model?
6. Can you resolve the **IRG label collision** between `S06_auc_compare.csv` (0.619, Peng reported) and `09_external_validation.csv` (0.604, recomputed) so readers do not conflate the two?

---

## § Recommendation

**Major revisions (design/statistics).** The core biology (Mars1 immunoparalysis signal, external AUC generalisation, honest limitations) is sound and the Egger p-value implementation is correct. The blocking issues are (i) the **"well behaved" calibration** overstatement (slope 0.50 is miscalibrated — Item 6), (ii) the imprecise **"MR layer is null"** wording that ignores the one reversed-direction family-significant signal (Item 3), and (iii) the **IRG comparison** asserted without CI/formal test and with a label collision (Item 5). None invalidate the study; all are fixable with wording, one recalibration note, and a sensitivity-analysis pledge. The article type (Research) is appropriate and is not affected by any flaw found.

*End of A2 report.*
