# Reviewer A2 — Design / Statistics / Epidemiology Assessment

**Manuscript:** "A reproducible, fully auditable pipeline confirms within-cohort the MARS Mars1 immunoparalysis program and delivers an honest external validation of a 30-gene sepsis prognostic signature" (tag v1.22.0, commit d507c1c)
**My role:** Independent peer reviewer — design, statistics, and epidemiology. This is treated as a first submission; I have not consulted any prior review round and I recomputed every headline number from the deposited result files.

---

## Issue 1 — DeLong P ≈ 0.56 is internally contradictory and not reproducible from the stated inputs (MODERATE)

【Problem】The manuscript reports a DeLong test ("P ≈ 0.56, not significant") comparing the equal-weight external AUC 0.638 with the *published* IRG benchmark 0.619, but the same paragraph then states that no formal test against that published benchmark was performed. The two statements cannot both be true.

【Evidence】
- `manuscript.md` §3.4 (line 104): "…the external 0.638 falls within sampling noise of 0.619 (**DeLong P ≈ 0.56, not significant**) and within the signature's own 95% CI. … the published IRG benchmark was reported as a single point estimate without a confidence interval, so **a formal difference test against it was not performed** and the difference is not established as statistically meaningful."
- `manuscript.md` Limitation 1 (line 157): "0.019 above the published IRG benchmark (Peng et al. [8], 0.619 on this cohort), a difference that is not statistically significant (**DeLong P ≈ 0.56**)."
- Recomputed from `03_results/09_external_validation.csv`: equal-weight AUC 0.638 (95% CI 0.532–0.748), IRG benchmark 0.619. The equal-weight CI *does* contain 0.619, so "not significant" is directionally plausible — but a genuine DeLong test requires both score vectors on the same 106 samples. The author possesses the equal-weight scores but only Peng's reported point AUC 0.619 (no score vectors, no CI). DeLong cannot be run against a single reported number.
- `03_results/09_ext_benchmark_vs_srs.csv` shows the only score vectors the author actually has for an IRG-style comparator is the **3-gene IRG proxy at AUC 0.529**, not the full-IRG 0.619.

【Why it matters】A reader cannot tell what was actually tested. If the DeLong used the author's own 3-gene proxy (0.529), that is a *different* comparison than the text claims ("published IRG benchmark 0.619"), and the P-value would correspond to a 0.109 gap, not a 0.019 gap. If it used a reconstructed full-IRG score, that reconstruction is undocumented. The contradiction undermines the one quantitative claim that the signature is "comparable rather than superior" to the benchmark, and it is exactly the kind of number an editor will ask to be reproduced.

【Specific fix】Pick one and make the text consistent:
- *Option A (safest):* delete the "DeLong P ≈ 0.56" sentence from §3.4 and keep the existing honest statement "a formal difference test against it was not performed." Change Limitation 1 to: "0.019 above the published IRG benchmark (Peng et al. [8], 0.619 on this cohort); because that benchmark was reported as a single point estimate without a confidence interval, a formal difference test against it was not performed and the difference is not established as statistically meaningful."
- *Option B (if a real DeLong exists):* explicitly state the two score vectors, e.g. "A DeLong test between our equal-weight score and a reconstructed Peng IRG score on the same 106 E-MTAB-4451 samples gave P ≈ 0.56," and **delete** the "formal difference test against it was not performed" sentence. Do not attribute DeLong to a merely-reported AUC.

---

## Issue 2 — "Pre-registered" overstates the designation; no deposited plan exists (MINOR)

【Problem】§2.9 calls the locked-L1 = primary designation "pre-registered rather than post-hoc," but the manuscript cites no time-stamped registered analysis plan (no registry ID/URL in Data/Code availability or §7). The claim is a self-assertion.

【Evidence】
- `manuscript.md` §2.9 (line 55): "This primary designation was fixed before the external AUC was computed, so the primary claim is **pre-registered** rather than post-hoc."
- No registration DOI/URL appears in §2.11, Data availability, or §7.

【Why it matters】"Pre-registered" carries a specific evidentiary meaning (a deposited, time-stamped protocol). Using it without an artifact invites a demand for the registration that cannot be met, and it slightly over-states the methodological guarantee. Note: the *substance* is credible and honest — choosing the **lower**-AUC model (0.585) as primary while demoting the higher (0.638) to sensitivity is anti-inflationary and the opposite of post-hoc p-hacking; this direction of choice is a genuine strength. The problem is only the word.

【Specific fix】Replace "pre-registered" with "pre-specified". Paste-ready: "This primary designation was fixed before the external AUC was computed, so the primary claim is **pre-specified** rather than post-hoc."

---

## Issue 3 — §2.9 names the primary without the "includes 0.5 / not above chance" caveat present elsewhere (MINOR)

【Problem】The honest caveat ("primary CI includes 0.5, not significantly above chance") is correctly present wherever 0.585 is emphasized in §3.4, §3.5, and Limitation 1 — but the *first* location that designates the primary (§2.9, Methods) omits it. This is the one spot a methods-focused reader meets the "primary" label unhedged.

【Evidence】
- `manuscript.md` §2.9 (line 55): designates locked-L1 as "primary … because it provides the like-for-like out-of-sample comparison…"; no mention that its CI includes 0.5.
- `manuscript.md` §3.5 (line 107): "AUC 0.585 (95% CI 0.469–0.696) … whose interval includes 0.5."
- `manuscript.md` Limitation 1 (line 157): "AUC 0.585 (95% CI 0.469–0.696), whose interval includes 0.5, so the primary estimate is **not significantly above chance**."
- Recomputed from `09_external_validation.csv`: locked-L1 AUC 0.5848, 95% CI 0.4687–0.6959 → contains 0.5.

【Why it matters】Consistency of the honesty qualifier across *every* mention of the primary metric reinforces the credibility of the pre-specification claim. A reader who stops at the Methods leaves with an unhedged "primary."

【Specific fix】Append to the §2.9 primary sentence: "…same fitted coefficients, no re-tuning; its 95% CI (0.469–0.696) includes 0.5, so the primary estimate is not significantly above chance."

---

## Issue 4 — §3.4 points readers to a title phrase ("immune-risk") that is not in the title (VERY MINOR / clarity)

【Problem】§3.4 says "the title's 'prognostic / immune-risk' wording should be read accordingly," but the title actually reads "a 30-gene sepsis **prognostic** signature" — "immune-risk" appears in the Abstract (line 14), not the title.

【Evidence】
- `manuscript.md` §3.4 (line 104): "…the title's 'prognostic / immune-risk' wording should be read accordingly."
- `manuscript.md` Title (line 1): "…honest external validation of a 30-gene sepsis **prognostic** signature" (no "immune-risk").
- `manuscript.md` Abstract (line 14): "honestly externally validates a 30-gene sepsis **immune-risk** signature."

【Why it matters】Pedantic, but the sentence is meant to direct readers to the specificity caveat; pointing at a phrase not literally present in the title slightly weakens an otherwise strong caveat.

【Specific fix】Reword to: "the title's 'prognostic' and the abstract's 'immune-risk' wording should be read accordingly."

---

## § Stands up (verified recomputations and sound design choices)

1. **Primary/sensitivity designation is fully consistent across the manuscript.** I checked title (line 1), Abstract (line 14), §2.9 (line 55), §3.4 (line 104), §3.5 (line 107), Limitation 1 (line 157), Conclusion (line 178), and §7 provenance (line 195). Every location pairs **locked-L1 = 0.585 = primary/external transport** and **equal-weight = 0.638 = pre-specified sensitivity**. I found **no** location that calls 0.585 primary while implying 0.638 is primary, or vice versa. This is a genuine strength and the central design decision of the paper holds together.
2. **External AUC numbers are exactly reproducible.** From `09_external_validation.csv`: locked-L1 AUC 0.5848 → reported 0.585 (CI 0.469–0.696); equal-weight AUC 0.6382 → reported 0.638 (CI 0.532–0.748); within-cohort CV 0.6582 → 0.659; 3-gene IRG proxy 0.5288 → 0.529. All match to rounding.
3. **External EPV ≈ 1.7 is correctly stated and is the right event-based EPV.** §3.5 (line 107): "52 death events for a 30-gene signature (effective events-per-variable ≈ 1.7)." Recomputed 52/30 = 1.733 ≈ 1.7 — correct as the nominal event-based EPV (conservative; even 52/29 mapped = 1.79, or 52/22 effective non-zero coefficients ≈ 2.4, would only strengthen the small-event caveat).
4. **Calibration is correctly framed as over-confident and the p-value is reported.** §3.5 (line 107): "sub-ideal slope of 0.50 (95% CI 0.10 to 0.91; P = 0.016 against the ideal slope of 1.0), indicating **over-confident** predicted probabilities." Recomputed from `09_ext_calibration_dca.csv`: slope 0.5028, CI 0.095–0.906, p_slope_eq_1 = 0.0158 ≈ 0.016. Slope < 1 and the CI excludes 1, so "over-confident" is statistically supported; the manuscript does **not** say "under-confident." (Note: §3.4's parallel wording "under-calibrated (slope < 1)" is a correct synonym, not "under-confident," and is consistent.)
5. **DCA grid matches `09_ext_dca_grid.csv` and the calibration-artifact caveat is explicit.** Recomputed: model first exceeds treat-all at threshold 0.30 (nb_model 0.2844 vs nb_treat_all 0.2722), equals treat-all at 0.05–0.25, and collapses to treat-none (nb = 0) at threshold 0.80 — exactly as §3.5 states ("exceeds treat-all from ≈0.30 onward … at ≥0.80 no calibration-corrected risk exceeds the threshold"). The manuscript also explicitly notes the DCA was computed on calibration-corrected probabilities from a logistic fit **on the same 106 samples**, is "optimistically biased and reported as illustrative (no bootstrap optimism correction)," and should be read as "discrimination-only support … rather than a calibrated absolute-risk benefit." This is the correct, honest framing.
6. **Label-independence limitation is explicit and adequate.** Limitation 9 (line 166) states verbatim that because the 30-gene set and death-orientation were both derived from GSE65682 28-day labels, "the external AUC is a transport test that remains tied to the discovery label definition; a fully label-independent confirmation … is required before the signature can be called validated." This satisfies the requirement directly.
7. **Signature-specificity caveat is present and sufficient; title/abstract do not over-claim.** §3.4 (line 104) twice states the signature "is best described as a generalized 28-day-mortality / immune-risk signature … rather than an immunoparalysis-specific signature" and "is more a generic 28-day-mortality signature than a specific immunoparalysis readout," citing the neutrophilic/acute-phase arm (ELANE, MPO, S100A8 positively correlated with death — confirmed in `S06_signature_genes.csv`: corr +0.170, +0.152, +0.091, orientation +1). The title says "sepsis prognostic signature" and the abstract "sepsis immune-risk signature" — neither claims immunoparalysis-specificity for the 30-gene score. The framing is honest.
8. **DeLong direction (not significant) is plausible** even though the test's pedigree is contradictory (Issue 1): the equal-weight 95% CI (0.532–0.748) contains 0.619, so non-significance is expected; the manuscript does not over-claim significance.

---

## § Questions for the authors

1. In Issue 1, what two score vectors actually entered the DeLong test that produced P ≈ 0.56? Was it (a) your equal-weight score vs your 3-gene IRG proxy (0.529), or (b) your equal-weight score vs a reconstructed full Peng IRG score on E-MTAB-4451? Please show the code/csv.
2. Is there a deposited, time-stamped analysis plan that justifies the word "pre-registered" in §2.9, or should it be softened to "pre-specified" (Issue 2)?
3. The locked-L1 model (learned coefficients) transports at 0.585 while the weight-free equal-weight reaches 0.638 — i.e., discarding the discovered coefficients *improves* external AUC. Do you read this as evidence the L1 coefficients overfit the 30-gene/52-event discovery set (consistent with EPV ≈ 1.7)? If so, a sentence making that interpretation explicit would strengthen §3.5.
4. For the DCA, you note probabilities come from an in-sample recalibration. Have you considered reporting the decision curve on the **raw/unrecalibrated** equal-weight scores as the conservative companion, so the "ranks patients by risk" claim does not rest solely on in-sample-corrected probabilities?

---

## § What I actually checked

- **Recomputed every headline number** from `03_results/`: `09_external_validation.csv` (locked-L1 0.585/CI 0.469–0.696; equal-weight 0.638/CI 0.532–0.748; CV 0.659; IRG3 proxy 0.529; n=106, 52 deaths, 29/30 mapped), `09_ext_calibration_dca.csv` (slope 0.50, CI 0.10–0.91, p=0.016; intercept −0.04), `09_ext_dca_grid.csv` (exceeds treat-all from 0.30; collapses to treat-none at ≥0.80), `09_ext_benchmark_vs_srs.csv` (SRS dir-corrected 0.610, age 0.504, ΔAUC +0.028, perm P 0.694), `S06_auc_compare.csv` (CV 0.659, train 0.750, IRG 0.619), `S06_signature_genes.csv` (ELANE/MPO/S100A8 positive with death), `09_external_validation_coef.json` (orientation +1 for the neutrophilic arm), `08_candidates_drugs.csv`, `S08_l1000_positive_control.csv` (prednisone 3.2nd percentile, lenalidomide 26.6%, azithromycin ≈ median 44.8%, dexamethasone 33.4%), `S08_l1000_candidate_scores.csv` (lenalidomide z=+0.56, azithromycin z=+0.10). All match the manuscript to rounding.
- **Audited primary/sensitivity consistency** at 8 locations (title, abstract, §2.9, §3.4, §3.5, Limitation 1, Conclusion, §7) — consistent, no reversal.
- **Verified** EPV statement (§3.5), over-confident calibration wording + p_slope (§3.5), DCA grid vs file + calibration-artifact caveat (§3.5), label-independence limitation (Limitation 9), and signature-specificity caveat (§3.4).
- **Identified one substantive contradiction** (DeLong P ≈ 0.56 vs "formal test not performed," Issue 1) and three wording/consistency nits (Issues 2–4).

**Overall:** The core design decision — locked-L1 = primary / equal-weight = sensitivity, with the primary CI including 0.5 and explicitly "not significantly above chance" — is coherent, consistently presented, and honestly hedged. The only finding that should block acceptance is the DeLong contradiction (Issue 1); Issues 2–4 are minor textual fixes.
