# Independent Statistical / Prognostic-Model-Validation Review — Design Layer

**Manuscript:** *"A reproducible, fully auditable pipeline confirms within-cohort the MARS Mars1 immunoparalysis program and delivers an honest external validation of a 30-gene sepsis prognostic signature"*
**Target venue:** BMC Bioinformatics (methodology)
**Reviewer role:** Independent statistical / prognostic-model-validation methodologist (first submission, fresh read)
**Review focus:** DESIGN-LEVEL defects that a statistical reviewer would block on — not re-praise of the already-disclosed caveats.
**Date:** 2026-10-09 (Round 1, panel reviewer A2)

---

## 0. Overall verdict

This is an unusually self-critical computational paper, and the honesty about the primary CI including 0.5 and the EPV violations is genuine and foregrounded. That honesty is an asset, but it does **not** immunize the manuscript against design-level objections. Three design decisions convert an honest result into a defensible *claim*, and all three are questionable:

1. The **inverted primary/sensitivity hierarchy** (the weaker, CI-includes-0.5 estimate is called "primary"; the stronger, CI-excludes-0.5 estimate is called "sensitivity").
2. The **over-interpretation of the calibration intercept** while the significantly sub-ideal slope (p = 0.0156) is buried.
3. The use of the word **"validation"** in the title for a gene set and orientation that are both *label-tied* to the discovery cohort.

None of these require the author to hide the truth; they require the author to **re-tier the claims to match the design**, not to let the favorable sensitivity carry the conclusion while the null-ish primary carries the label. My recomputations (Section 5) confirm every headline number in the manuscript is arithmetically correct — the problem is *framing and tiering*, not arithmetic. That actually makes the framing issues more, not less, important: there is no numerical error to hide behind.

I recommend **major revision** on design/framing grounds. The science is salvageable and the pipeline is a genuine contribution; the statistical narrative needs to be re-anchored to the design actually performed.

---

## 1. DESIGN-LEVEL ISSUES

Each issue uses the required four-part structure: 【Problem】 / 【Evidence】 / 【Why it matters】 / 【Specific fix】.

---

### Issue 1 — Inverted primary/sensitivity hierarchy is a spin signal even when pre-specified

【Problem】 The manuscript designates the weaker, coefficient-and-label-tied locked-L1 result (AUC 0.585, 95% CI 0.469–0.696, *includes 0.5*) as the **primary** external metric, and the stronger, more portable equal-weight result (AUC 0.638, CI 0.532–0.748, *excludes 0.5*) as a **sensitivity**, inverting the hierarchy a statistical reviewer expects and creating a classic spin signature.

【Evidence】
- §2.9: "The **locked-L1-weight** application … was designated the pre-specified **primary** external transport metric … A fixed-orientation equal-weight score … was added as a pre-specified **sensitivity** analysis."
- §3.5 / Abstract / Limitation 1: locked-L1 primary AUC 0.585 (CI 0.469–0.696, includes 0.5); equal-weight sensitivity AUC 0.638 (CI 0.532–0.748, excludes 0.5).
- Source `09_external_validation.csv`: `auc_EMTAB4451_external_locked = 0.5848` (CI 0.4687–0.6959); `auc_EMTAB4451_orientedSum = 0.6382` (CI 0.5317–0.7475).

【Why it matters】 A methods journal will not accept a "primary external validation" whose primary estimate is statistically indistinguishable from chance. Relegating the *only* CI-excludes-0.5 estimate to "sensitivity" while the Discussion/title lean on "real but modest" reads as outcome-tiering. The author's own justification is internally contradictory: §2.9 states the equal-weight score "is the portable component by construction," i.e. the thing that actually carries generalizable information is the gene set + orientation, NOT the learned L1 coefficients — yet the object admitted to be *less* portable (overfit coefficients, internal EPV 3.8) is called primary and the portable object is demoted. "Pre-specification" does not rescue the logic: pre-registering an inferior primary is still an inferior primary. The result is that the paper's stated conclusion ("real but modest … not validated") is honest, but its *structure* (null primary, favorable sensitivity) invites a spin rejection that the body text does not earn.

【Specific fix】 Re-tier so the designation tracks portability, not the fitted-model lineage:
> *"We report two complementary external metrics. The **primary transportability metric** is the fixed-orientation equal-weight score — the gene set plus orientation, free of any cohort-specific weight — which is the portable quantity by construction and which transported at AUC 0.638 (95% CI 0.532–0.748), excluding 0.5. As a **sensitivity**, we transported the exact locked L1 model (same fitted coefficients); this declined to AUC 0.585 (95% CI 0.469–0.696), whose interval includes 0.5, showing that the discovery-fitted coefficients do **not** add portable information beyond the gene set and orientation. The honest reading is that the biology transports but the fitted model does not."*

(Alternative acceptable fix: declare dual co-primary and state plainly that the exact fitted model fails while the gene-set transports. The current single-primary-with-inverted-rank is the part that must change.)

---

### Issue 2 — "Near-zero intercept" over-states calibration; the slope is the real defect and it is significant

【Problem】 The manuscript emphasizes the "near-zero intercept (−0.04)" as a calibration-positive signal, while the calibration **slope (0.50) is significantly below 1 (p = 0.0156)** — which is the clinically important miscalibration and is never reported with its p-value or CI in the text.

【Evidence】
- §3.5: "Calibration of the external equal-weight score showed a **near-zero intercept (−0.04, 95% CI −0.46 to 0.36)** but a **sub-ideal slope of 0.50**."
- Source `09_ext_calibration_dca.csv`: `calib_intercept = −0.0382`, `calib_slope = 0.5028`, **`p_slope_eq_1 = 0.01565`** (the manuscript text reports neither the slope CI nor this p-value).
- Recomputation confirms: the slope of 0.50 derives from the discovery-derived probability mapped externally; an external-*refit* logistic gives intercept 0 / slope 1 (expected), so 0.50/−0.04 reflects genuine external miscalibration of the discovery-derived score.

【Why it matters】 Calibration requires BOTH intercept ≈ 0 AND slope ≈ 1. A slope of 0.5 with p = 0.016 means the score is **over-confident** — predicted risks are too extreme / under-shrunk and would require β ≈ 0.5 shrinkage before any risk-stratification or threshold use. Reporting only the favorable intercept invites the reader to conclude "well calibrated" when the score is, by the authors' own p-value, significantly miscalibrated in spread. This is an interpretive error at the design layer, not merely an under-emphasized caveat.

【Specific fix】 Report the slope with its CI and p-value and reframe:
> *"The external equal-weight score was miscalibrated in slope: calibration slope 0.50 (95% CI 0.10–0.93 [percentile, unstable]; Wald p = 0.016 for slope = 1), with intercept −0.04. A slope below 1 indicates over-confident (under-shrunk) predictions; the near-zero intercept alone does not establish calibration, and the score requires shrinkage before any risk-threshold application."*

---

### Issue 3 — Bootstrap percentile CI for the calibration slope is unreliable (crosses 1 while Wald p = 0.016)

【Problem】 The calibration-slope 95% CI in the source (0.10–0.93) is a bootstrap *percentile* interval that crosses 1.0 despite a Wald p-value of 0.0156 for slope = 1 — an internal inconsistency produced by the right-skewed bootstrap distribution of a lower-bounded parameter.

【Evidence】
- `09_ext_calibration_dca.csv`: `calib_slope_ci_lo = 0.1019`, `calib_slope_ci_hi = 0.9273`, `p_slope_eq_1 = 0.01565`.
- Recomputed Wald: SE(slope) ≈ 0.21 → normal CI ≈ 0.09–0.91 (wide, centered low); the percentile 0.10–0.93 is asymmetric/skewed. The two should not disagree on whether 1.0 is plausible, yet they do at the decision boundary.

【Why it matters】 A CI/p-value disagreement on the single most important calibration parameter can be read as the authors leaning on the lenient interval to imply "the slope might be fine." It also casts doubt, by association, on the AUC bootstrap CIs. The remedy is mechanical and strengthens the paper.

【Specific fix】 Replace the percentile slope CI with a **BCa bootstrap** (Efron) or a profile-likelihood/Wald CI, and always report `p_slope_eq_1`. Note that 2,000 resamples give adequate Monte-Carlo precision for the **AUC** CIs (reproduced here: oriented 0.530–0.740, locked 0.469–0.690, matching source) but are insufficient to stabilize the *skewed* slope percentile interval. A single sentence acknowledging this asymmetry is enough.

---

### Issue 4 — DeLong P = 0.156 between equal-weight and the 3-gene proxy cuts AGAINST the superiority framing

【Problem】 The manuscript frames the 3-gene IRG proxy as a "weak reference" and lets the favorable 0.638 point estimate imply the 30-gene score is better, but the paired DeLong (same 106 samples) returns P = 0.156 — i.e., the 30-gene equal-weight score is **not statistically distinguishable** from a 3-gene proxy.

【Evidence】
- §3.5 / Abstract: "a 3-gene IRG proxy recomputed here was 0.529 (a weak reference only; its confidence interval overlaps the other benchmarks, so the comparison is descriptive)."
- Recomputed DeLong (paired, same 106 cases — valid): equal-weight 0.6382 vs irg3 0.5288 → z = 1.420, **P = 0.1556** (matches manuscript 0.156). Also unreported: locked vs irg3 P = 0.4874.

【Why it matters】 Non-significance here does **not** support the signature's added value; it means even a crude 3-gene proxy cannot be beaten at n = 106. This is consistent with the paper's honesty, but the "weak reference" language, read alongside the 0.638 point estimate in the Discussion, can be misread as evidence of superiority. The honest statement is the opposite: incremental value over a minimal gene set is *unproven*.

【Specific fix】 State it directly:
> *"Against a 3-gene IRG proxy computed on the same 106 samples, the 30-gene equal-weight score was not statistically distinguishable (DeLong P = 0.156); its incremental discrimination over even a minimal gene set is therefore unestablished at this sample size."*

(Note: the DeLong itself is *statistically valid* — same cases, different scores, paired test — so the issue is interpretation, not the test choice.)

---

### Issue 5 — "External validation" in the title overstates a label-tied transport check

【Problem】 Both the 30-gene *selection* and the death-*orientation* were fixed on GSE65682's 28-day labels, so the external application is independent in cohort and platform but **not in label**; the title/abstract call this an "honest external validation," overselling a within-label transport consistency check.

【Evidence】
- §2.6: signature = top-30 by |r| with 28-day death, "each oriented so expression positively contributes to death risk."
- §3.5 / §5 limitation 9: "the external AUC is a transport test that remains tied to the discovery label definition; a fully label-independent confirmation … is required before the signature can be called validated."
- Title: "delivers an honest external validation of a 30-gene sepsis prognostic signature."

【Why it matters】 A signature tuned to the same label definition in both cohorts is, at best, a *transportability/consistency* assessment, not validation. Claiming "validation" in the title invites rejection for overstatement and conflates transport with confirmation. The body already says this (limitation 9) — the title and abstract do not follow.

【Specific fix】 Re-title/reframe to match the design:
> *"… and delivers an honest **label-tied external transport** of a 30-gene sepsis immune-risk signature"* and reserve the word "validated" for a design in which the gene set is fixed a priori (e.g., the published IRG panel of Peng et al.) or a second independent held-out cohort is used. One sentence in the Abstract should say "transport, not label-independent validation."

---

### Issue 6 — EPV violations make a ~21–30 gene signature un-validatable at n = 106/52; the design itself is under-powered

【Problem】 External EPV = 52/30 ≈ 1.7 (or ≈ 52/21 effective non-zero genes ≈ 2.5, since 7 locked coefficients are zero and HLA-DQA1 is missing) and internal EPV = 114/30 ≈ 3.8 — both far below the conventional ≥ 10. Transporting a signature this large to a 52-event cohort cannot yield a stable "validated" estimate regardless of framing.

【Evidence】
- Abstract / §3.4 / §3.5: "effective events-per-variable ≈ 1.7"; internal 114/30 ≈ 3.8; §3.4 notes training 0.750 vs CV 0.659.
- Source confirms 29/30 genes mapped; §3.4 states 7 locked coefficients are exactly zero.

【Why it matters】 This is a *design* defect, not a caveat: no amount of honest framing converts an EPV ≈ 1.7 external test into a validation. A statistical reviewer will ask why a 30-gene signature was evaluated in a 52-event cohort instead of a pre-specified parsimonious sub-signature sized to the event count.

【Specific fix】 Either (a) report a **pre-specified parsimonious sub-signature** (e.g., top-k genes by cross-cohort stability or by |r|, with k chosen so EPV ≥ 10 is even approximately feasible given 52 events — realistically k ≤ 5) as the true validation target, or (b) explicitly frame the entire external step as **hypothesis-generating** and drop "validation." Add an EPV table (internal 3.8, external 1.7, effective-nonzero 2.5) so the reader sees the constraint quantified.

---

### Issue 7 — Chained selection FWER is uncontrolled and the orientation step is outcome-tautological; name it as a distinct optimism source

【Problem】 The selection chain (|logFC| ≥ 0.3 DEG → top-2000 co-expression degree → tri-method ML consensus → 30-gene |r|-ranking + orientation by death sign) reuses the same cohort and the same 28-day labels at every stage, leaving effective FWER uncontrolled and making orientation a direct function of the outcome.

【Evidence】
- §2.2–2.6 and §5 limitation 9 (the author acknowledges the chain and the label-tie, but does not separate *feature-selection* optimism from *orientation* optimism).

【Why it matters】 Because orientation = sign of correlation with 28-day death in the discovery cohort, the external score is guaranteed to be at least weakly aligned with the same-definition outcome. The external AUC therefore partly measures **label-consistency** rather than independent prognostic information. This is the mechanism by which the "label-tied" critique bites, and it is a *separate* optimism source from the within-cohort CV (which only controls for the inner-loop coefficient fit, not for the full-cohort feature+orientation selection). Naming it explicitly strengthens, rather than weakens, the paper's honesty claim.

【Specific fix】 Add a **negative-control analysis** to quantify the tautology:
- Re-orient the gene set using a *permuted/shuffled* 28-day label in the discovery cohort, transport that randomized-orientation score to E-MTAB-4451, and show the external AUC collapses toward 0.5.
- Report: `AUC_real_orientation = 0.638` vs `AUC_permuted_orientation (mean over K shuffles) ≈ 0.5`, with the difference attributed to orientation-tautology vs genuine transport. This converts the "label-tied" limitation from a disclaimer into a quantified design diagnostic.

---

### Issue 8 — SRS benchmark relies on a post-hoc direction flip; incremental value over existing classifiers is non-significant

【Problem】 The SRS endotype comparison uses `max(AUC, 1−AUC)` direction correction on a 3-level ordinal label, and the 30-gene score's advantage over SRS is non-significant (ΔAUC +0.028, perm P = 0.694).

【Evidence】
- `09_ext_benchmark_vs_srs.csv`: SRS ordinal raw AUC 0.3896 → direction-corrected 0.6104; "ΔAUC vs SRS_dir +0.0278, perm P 0.694"; age AUC 0.5043, sex 0.5046.

【Why it matters】 Combined with the DeLong-against-3-gene null (Issue 4), the signature shows **no demonstrable incremental value** over (a) a 3-gene proxy or (b) an existing transcriptomic endotype in these 106 patients. The "real but modest" framing must be explicit that "modest" includes "not better than cheaper, already-published classifiers."

【Specific fix】 One Results sentence:
> *"Against two existing, cheaper benchmarks — a 3-gene IRG proxy (DeLong P = 0.156) and the published SRS endotype (ΔAUC +0.028, permutation P = 0.694) — the 30-gene score shows no significant incremental discrimination in n = 106; its transport is real but adds nothing demonstrable over established classifiers in this cohort."*

---

## 2. § Stands up (things I suspected were wrong but found correct)

1. **DCA "net benefit ≥ 0.80 collapses to treat-none" — VERIFIED correct.** Source `09_ext_dca_grid.csv`: at threshold 0.80, `nb_model = 0.0` and `nb_treat_all = −1.5472`; the model's net benefit equals the treat-none line (0.0) at 0.80 and stays 0.0 at 0.85/0.90. The claim is stated accurately and is not a misread. (The legitimate follow-up is interpretive: a model that only beats treat-none below threshold 0.80 has narrow clinical utility — but the *factual* statement is right.)

2. **All headline AUC and DeLong numbers reproduce exactly from per-sample scores.** Using `09_ext_risk_scores.csv` (n = 106, 52 deaths/54 survivors, columns `y`, `risk_oriented_sum`, `risk_locked_l1`, `risk_irg3`): oriented AUC 0.6382, locked 0.5848, irg3 0.5288; DeLong oriented vs irg3 P = 0.1556, oriented vs locked P = 0.2348. The manuscript's reported values and the pre-specified primary/sensitivity CIs (0.469–0.696, 0.532–0.748) match the source CSV exactly. There is **no arithmetic or transcription error** in the headline statistics — which is precisely why the framing/tiering problems (Issues 1–2, 5) carry the weight.

3. **The honest disclosure of the primary CI including 0.5 and the EPV violations is genuine and foregrounded, not a fig-leaf.** I suspected these were buried, but they appear prominently in the Abstract, §3.5, Limitation 1, and Limitation 9. The author does not hide them.

4. **The 2,000-sample bootstrap AUC CIs are reproducible and Monte-Carlo adequate.** Independent bootstrap (seed 7, B = 2000): oriented 0.530–0.740, locked 0.469–0.690, matching the source. The reliability concern is *specific to the calibration-slope percentile interval* (Issue 3), not to the AUC CIs.

5. **The SRS/age benchmarks are fair.** Age AUC 0.504 (no signal) and SRS direction-corrected 0.610 are computed on the same 106 patients from shipped metadata; the comparison is legitimate (the only caveat is the post-hoc direction flip, Issue 8).

6. **The drug-repositioning self-skepticism is correctly framed.** I suspected the prednisone/L1000 section overclaimed; instead it is correctly presented as descriptive-only (prednisone ranks 3.2nd percentile, so the rescue proxy cannot corroborate the immunomodulators). This is a strength, not a defect.

---

## 3. § Questions for the authors

1. **Pre-specification audit.** The primary/sensitivity designation is described as fixed before the external AUC was computed. Was this designation recorded in a dated analysis plan / pre-registration, or chosen after both AUCs were visible? This determines whether Issue 1 is "suboptimal pre-specification" or "post-hoc tiering."

2. **Calibration linear predictor.** The source reports slope 0.50 / intercept −0.0382 with p_slope_eq_1 = 0.0156. Confirm these are computed on the **discovery-derived** probability (orientation/scaling from GSE65682) applied externally, not on an external-refit probability (which would give slope 1 by construction, as my recomputation shows). If discovery-derived, the miscalibration is real and Issue 2 stands; if refit, the numbers are inconsistent and must be corrected.

3. **Why 30 genes given the event count?** With 52 external events, what motivated evaluating a 30-gene (effectively ~21-gene) signature rather than a pre-specified parsimonious sub-signature sized to EPV ≥ 10? Was any stability/SNR pre-screen used to justify the size?

4. **Published IRG benchmark comparison.** The DeLong against the *published* Peng et al. IRG benchmark (0.619) was impossible because that study shipped no per-sample scores. Is the descriptive comparison fair given different preprocessing (different normalization, different gene set)? Should it be downgraded from "comparable" to "not directly comparable"?

5. **Label-permutation negative control.** Was any orientation-permutation / label-shuffle analysis run to quantify how much of the 0.638 is orientation-tautology vs genuine transport (Issue 7)? If not, would the authors add it?

6. **SRS direction handling.** The SRS AUC uses `max(AUC, 1−AUC)`. Was the correct mortality direction of SRS1/SRS2/SRS3 known a priori, or was the flip applied because the raw ordinal AUC (0.3896) was < 0.5? If post-hoc, the comparison should be flagged as exploratory.

---

## 4. § What I actually checked

**Files read (only the manuscript and the source result CSVs — no review/response/revision files, no manifest, no SOPs, no memory, per the review contract):**
- `05_reports/manuscript.md` — full read.
- `03_results/09_external_validation.csv` — external AUCs and CIs.
- `03_results/09_ext_calibration_dca.csv` — calibration intercept/slope, slope CI, p_slope_eq_1.
- `03_results/09_ext_dca_grid.csv` — DCA net-benefit grid.
- `03_results/09_ext_benchmark_vs_srs.csv` — SRS/age/sex benchmarks.
- `03_results/S06_auc_compare.csv` — internal CV/training AUCs.
- `03_results/09_ext_risk_scores.csv` — per-sample scores (the key file, see below).

**Recomputations attempted (venv `C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe`, numpy/pandas/scipy):**
- **AUC** (rank/Mann–Whitney) for the three scores → oriented 0.6382, locked 0.5848, irg3 0.5288. **Match the manuscript exactly.**
- **DeLong test** (DeLong–DeLong–Clarke–Pearson structural-components, paired on the same 106 samples — a valid use): oriented vs irg3 → P = 0.1556 (manuscript 0.156 ✓); oriented vs locked → P = 0.2348 (manuscript 0.235 ✓); locked vs irg3 → P = 0.4874 (unreported).
- **Calibration**: logistic regression of `y` on the external-refit logit(p) → intercept 0, slope 1 (expected, confirming the source's 0.50/−0.0382 reflect a *discovery-derived* probability, not a refit). The source's `p_slope_eq_1 = 0.01565` was confirmed present in the CSV but is **absent from the manuscript text**.
- **Bootstrap (B = 2000, seed 7) AUC CIs** → oriented 0.530–0.740, locked 0.469–0.690, matching the source (0.5317–0.7475 / 0.4687–0.6959). Monte-Carlo precision adequate for AUC; flagged as inadequate for the skewed slope percentile interval.

**Per-sample scores availability (answers the contract question directly):**
`09_ext_risk_scores.csv` contains, for all 106 samples, the columns `y` (28-day outcome), `risk_oriented_sum` (equal-weight), `risk_locked_l1` (locked L1), and `risk_irg3` (3-gene proxy). This is **sufficient to recompute DeLong and calibration independently** — and I did. **No discrepancy** was found between these per-sample scores and the manuscript's headline numbers. The only gap is that the source file reports the calibration-slope p-value and CI that the manuscript text omits (Issue 2/3).

**Discrepancies / concerns surfaced (not arithmetic errors, but reporting gaps):**
- The manuscript reports the calibration intercept (and its CI) but **not** the slope's CI or `p_slope_eq_1 = 0.01565`, despite the slope being the significant, clinically relevant defect.
- The DeLong locked-vs-irg3 (P = 0.4874) is unreported; minor, but it further corroborates that no score significantly beats the 3-gene proxy.
- No label-permutation negative control is present in the source to quantify orientation-tautology (Issue 7).

**Files NOT read (per instruction):** any `REVIEW_*.md` / `RESPONSE_*.md` / `REVISION_*.md` / `ROUND*.md`; the rest of `06_review/`; `SUBMISSION_MANIFEST.md`; `*_SOP.md`; `author_verification_statement.md`; `MEMORY.md`; `.workbuddy/memory/`. This review was written as a fresh first-submission read.

---

## 5. Recommended revision priority (for the editor)

**Blocking (design/framing, must change before acceptance):**
- Issue 1 (re-tier primary/sensitivity).
- Issue 2 + 3 (report slope p-value/CI; fix slope bootstrap; stop over-interpreting intercept).
- Issue 5 (title/abstract "validation" → "transport").

**Strongly recommended (design integrity):**
- Issue 6 (EPV-sized signature or explicit hypothesis-generating framing).
- Issue 7 (label-permutation negative control).

**Recommended (precision/honesty of comparisons):**
- Issue 4 (DeLong vs 3-gene: state non-inferiority, not superiority).
- Issue 8 (SRS direction flip + non-significant incremental value).

The manuscript's pipeline, provenance, and candor are real strengths. The blocking items are about *matching the claim to the design actually performed* — they are achievable within a revision and will make the paper both honest and defensible, rather than honest but rejectable on framing.
