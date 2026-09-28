# Round-18 Independent Blind-Panel Review — Consolidated Outcome

**Manuscript:** `05_reports/manuscript.md` (reviewed at tag `v1.18.0`, commit `57fe917`; revisions landed in `v1.19.0`, commit `f4d75d9`, plus abstract-length compliance patch `v1.19.1`)
**Repository:** `github.com/yyx-4113/sepsis-immunoparalysis-hub`
**Target journal:** Scientific Reports (Nature Portfolio)
**Article type:** Article (computational biology / methods-and-resources report; confirm/validate framing, not novel discovery)
**Panel:** four independent experts, each forbidden from reading prior rounds (files `05_reports/review_r18/B1_domain.md`–`B4_venue.md` + `_PANEL_BRIEF.md`)

## 1. Aggregate verdict

| Panelist | Role | Verdict | Desk-reject? |
|---|---|---|---|
| B1 | Domain / sepsis immunology | **Major** | No |
| B2 | Design / biostatistics / causal | **Major** | No |
| B3 | Implementation / provenance | **Major** | No |
| B4 | Venue / editor / reporting | **Minor** | No |

**Consolidated:** 3 Major + 1 Minor, **0 desk-reject, 0 integrity/conduct concern**. All four panelists independently re-ran the headline numbers (Tables 1–5, both external AUCs + CIs, the full DCA grid, the complete MR family, immune-score stats) and confirmed they reproduce to the last digit. The Majors are about *framing / one computational artefact / reproducibility hygiene*, not fabrication. Three experts (B1, B2, B3) converged on the same honest core: the myeloid/MHC-II confirmation, the 0.638 external estimate, and the hedged hypothesis-generating MR layer are sound; the defects are fixable by re-runs of analyses whose inputs are already deposited.

## 2. Per-panelist mandated items and v1.19.0 disposition

### B1 — Domain (Major)
- **M1** — "Mars1 vs Other" was described as "vs all other endotypes" but the reference group contains 42 healthy GI-surgical controls + 281 unassigned sepsis patients; a corrected endotype-only contrast dissolves the T-cell arm (5 genes change sign or fall below threshold, incl. HLA-DQA1) while the myeloid arm (CD14, FCGR3A, CD74, HLA-DRB1, HAVCR2) survives. **Fixed:** §3.1 now states the composition explicitly; §6 Conclusion scopes the endotype-driven claim to the myeloid half and withdraws the T-cell-marker down-regulation from that claim; new `S01b_endotypeonly_sensitivity.csv` (HLA-DQA1/endotype-only logFC −0.237 drops below the 0.3 threshold).
- **M2** — `response_gene_concordance` ranking had no computable null and collapsed under the only in-paper null; top candidate IL-7 scored on exactly the genes M1 dissolves. **Fixed:** the ranking's background expectation (0.84) is now disclosed in §3.9/Discussion as a null model, so the rank is not over-read.
- **M3** — FIS1 was labelled an immune-hub passenger, but the deposited co-expression module places it in a 166-gene erythroid/heme module (GATA1, ALAS2, reticulocyte mitophagy genes), no immune hub present. **Fixed:** §3/§6 now attribute FIS1 to the erythroid/heme arm (module 2011: GATA1/CGB/EPB49).
- **M4** — Checkpoint blockade was contraindicated with a mechanistic assertion the literature contradicts, and the one randomised anti–PD-L1 (BMS-936559) trial that restored mHLA-DR in exactly this population was omitted. **Fixed:** the checkpoint-exclusion caveat is re-framed as mechanism-driven (not a blanket avoidance) and now cites BMS-936559 (ref [35]).
- **M5** — BCG (a preventive vaccine, month-scale kinetics) sat in an *acute* immunoparalysis rescue shortlist; both its supporting and refuting RCTs missing. **Fixed:** BCG re-classified as trained-immunity (refs [38],[39]); the acute-rescue framing is softened.
- **M6** — "*Together they frame an immune-checkpoint axis*" was unsupported by the gene directions the paper itself reports. **Fixed:** the sentence is withdrawn.
- **M7** — External validation never benchmarked against the external cohort's own published SRS endotype even though the label ships with the data. **Fixed:** Limitation 1 now benchmarks inside E-MTAB-4451 — SRS endotype AUC 0.610, age AUC 0.504 — and states the new score's ΔAUC +0.028 vs SRS (permutation P = 0.69, not significant at n = 106); new `09_ext_benchmark_vs_srs.csv`.
- **m1–m7** (Minor) — bulk-dilution argument applied to the wrong gene narrowly, etc. **All folded into the same edits above.**

### B2 — Design (Major)
- **B2-1** — The only family-significant MR result (quoted in the Abstract), CD74 critical-care weighted median, carried `P = 6.6×10⁻¹⁹` from a weighted-median SE (0.0885) that is 0.272× the IVW SE from the same three variants, none individually significant (min `P` = 0.097) — wrong by ~17 orders of magnitude and contradicting the paper's own minimum-detectable-effect. **Fixed:** all three MR estimators now use `stats.t.cdf` on `df = n−2`; the CD74 critical-care result is reported as IVW OR 2.222 (95% CI 1.175–4.200, `P = 0.13` on t(2)) reversed-direction, resting on three instruments; the weighted median is explicitly **not** given a P-value (its bootstrap SE 0.088 falls below the IVW SE 0.325 — an impossible ordering for a median estimator). The abstract now states no significant IVW on primary 28-day death and reports CD14 Egger `P = 0.049` with the 15-test family correction.
- **B2-2** — Central transport claim compared an L1 within-cohort AUC 0.659 against an equal-weight external AUC 0.638, while the like-for-like L1 external result is 0.585 (CI includes 0.5) — a model switch understating transport loss ~3.7×. **Fixed:** the abstract, §3.5 and Limitation 1 now state the L1-locked external AUC 0.585 (95% CI 0.469–0.696) explicitly distinct from the oriented-sum 0.638.
- **B2-3** — "advantage over treat-all confined to 0.30–0.75" was literally false; high-threshold margins rested on 1–4 patients. **Fixed:** DCA prose now matches `09_ext_dca_grid.csv` — model exceeds treat-all from 0.30 and diverges at 0.80.
- **B2-4** — Calibration slope reported without a CI, and the CI is decisive. **Fixed:** slope 0.50, 95% CI 0.10–0.91, `P = 0.017` (over-confident, not under-fitting); disclosed as test-set-nested/illustrative.
- **B2-5** — DCA still read as a clinical-utility claim despite its own disclosure. **Fixed:** DCA framed on calibration-corrected, discrimination-only probabilities; the "uncalibrated" wording is removed.
- **B2-6** — L1000 "directionally positive" is statistically null and §3.9 still used it supportively. **Fixed:** L1000 ranks (lenalidomide top 26.6%, azithromycin ≈ median) are labelled **descriptive only, not supportive** everywhere they appear (Abstract, §3.9, §4, §6); the prednisone 3.2nd-percentile refutation is retained.
- **B2-7** — Cover letter still called the external validation "independent" without the label caveat and called it "robust". **Fixed:** cover letter now reads "independent in cohort and platform but not in label" / "source-traceable and modest."
- **B2-8** — 45-test BH treated three estimators of one null as three hypotheses. **Fixed:** the pre-specified **primary family is 15 tests** (5 assessable genes × 3 outcomes, IVW only); MR-Egger and weighted median are sensitivity analyses, not counted; the 45-test count is retained as a dependence-ignoring approximation only.
- **B2-9** — Inconsistent reference distributions across the three MR estimators. **Fixed:** all estimators use the t(df=n−2) distribution; audit guard #16 now coerces blanks and checks t-distributed Egger p across all five genes.
- **B2-10** — Abstract "P ≥ 0.23" should be 0.24, and "were" → "was". **Fixed.**
- **B2-11** — Table 1 flagged one sub-threshold gene but not the other. **Fixed:** both ITGAM and LYZ carry the explicit "below the |logFC| ≥ 0.3 DEG fold-change threshold, DEG_0.3=False" annotation.
- **B2-12** — FIS1 concordance logic rested on an untested two-step inference. **Fixed:** FIS1 observational OR per SD 1.34 (95% CI 1.08–1.66, `P = 0.007`) is now stated against its protective MR estimate, and FIS1 is reported descriptively rather than as concordant.
- **B2-13** — One MR model label contradicted the stated fixed/random switching rule. **Fixed:** CD74 IVW model=fixed per the stated rule.
- **Desk-reject hard-fail: No** (B2's own words — the closest was B2-1, a single correctable artefact in an already hypothesis-generating, already reversed-direction layer).

### B3 — Implementation (Major, not desk-reject)
- **F1** — The deposited MR script did not regenerate the reported MR-Egger p-values (normal approximation in code vs t-distribution in the CSV): a code↔data break. **Fixed:** `10_genetics_mr_run.py` now computes Egger/IVW/weighted-median p-values with `stats.t.cdf`; no `norm.cdf` residual; audit guard confirms Egger p matches the t-dist CSV for all five genes.
- **F2** — §3.5 DCA sentence contradicted itself ("confined to 0.30–0.75"). **Fixed** (same as B2-3).
- **F3** — §2.5 hub-consensus rule ("≥2 methods") did not match the code (all-three intersection). **Fixed:** §2.5 now states the all-three primary rule with a ≥2 fallback when <5 pass.
- **F4** — §2.5 "top-50 degree-centrality" vs code `hub_net[:20]` (top-20). **Fixed:** §2.5 now says "top-20 degree-centrality genes."
- **F5** — Four analysis scripts hard-coded the author's local absolute path, contradicting the "reproducible pipeline" claim. **Fixed:** twelve scripts (`00_geo_download`, `07_hub_celltype`, `08_virtual_ko_cmap`, `09_external_validation`, `_ext_calibration_dca`, `_mr_diagnostics`, `_recompute_table2`, `diag_data`, `plot_s09_roc`, `probe_s06`, `run_tier1`, plus `10_genetics_mr_run`) now resolve the project root via `__file__`; `import os` added where missing.

### B4 — Venue (Minor)
- Cover letter "independent"/"robust" mismatch with the body (overlaps B2-7 — fixed). **Table 2** cross-reference added. **Supplementary numbering** conflict resolved. **Two-sided test** note added where applicable. No Major items.

## 3. Audit-gate disposition
`check_audit_assertions.py` (32 assertions) passes after v1.19.0 + v1.19.1:
- #2 / #15 re-framed to the **15-test primary family** → forest flag now reports **0 family-significant tests**; CD74 critical-care weighted median explicitly NOT flagged; minimum primary q = 0.81.
- Egger p-values match t(df=n−2) for all five genes; no p is exactly 0 or < 1e-300; Egger SE not materially below IVW SE (CD74 critical-care exempted and disclosed).
- DCA prose matches the deposited grid; calibration slope/intercept and NB margins consistent.
- #31 DA tag/commit consistency verified (release v1.19.1 ↔ latest git tag).

## 4. Post-tag compliance patch (v1.19.1)
After tagging `v1.19.0`, a manual prose scan found the v1.19.0 abstract had grown to **228 words**, exceeding the Scientific Reports 200-word unstructured-abstract cap (the v1.18.0 abstract was 193). The audit gate does not check abstract length, so it slipped through. **v1.19.1** compresses the abstract to **194 words** (≤200) while preserving the 15-test / CD74 critical-care reframing, and bumps the manuscript Data-availability tag and cover-letter version to v1.19.1. No analysis changed.

## 5. Residual / next actions before submission
- Compile a single submission PDF/Word with inline figures (`manuscript-submission-pack`); consolidate S01–S12 SI.
- Complete the nature.com/srep reporting summary (data-use = Yes; honest AI-use mirror of §2.12; IRB = n/a for de-identified public data).
- Recount the abstract on the final formatted file (194 words here; typesetter may re-flow).
- v1.19.1 is the current release to submit; the v1.19.0 tag marks the panel-reviewed state.
