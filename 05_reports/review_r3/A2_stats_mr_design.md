# A2 — Statistics & MR Causal-Design Review (Round 3, v1.2.0)

**Independence note:** Fresh first-submission read. No prior `REVIEW_*.md` / `review*/` consulted. Numbers recomputed from `03_results/*.csv`.

## Findings

### T1-1 (Tier 1) — CD14 Egger "null intercept argues against directional pleiotropy" over-reads a null
- **【Problem】** With only 6 instruments, the MR-Egger intercept test has very low power; a non-significant intercept does *not* affirmatively argue against pleiotropy.
- **【Evidence】** `manuscript.md:146`: "its intercept was not significant (P=0.34, arguing against directional (horizontal) pleiotropy [24])". Source `10_genetics_mr_outcome5086_28ddeath.csv` row CD14 MR-Egger: `egger_intercept_p=0.344`. Confirmed P=0.34, but n_IV=6.
- **【Why it matters】** Presenting a low-power null as evidence *against* pleiotropy is a classic over-reading that can mislead editors into over-trusting the CD14 signal.
- **【Specific fix】** "its intercept was not significant (P=0.34); however, with only six instruments this test has limited power to detect pleiotropy, so the null is not strong evidence against it."

### T1-2 (Tier 1) — BH-FDR is scoped to the primary-outcome family only, not the pre-specified 45-test family
- **【Problem】** The manuscript applies BH-FDR "across the 15 gene×estimator tests of the 28-day-death outcome," but the pre-specified family is 5 assessable genes × 3 estimators × 3 outcomes = 45 tests. Restricting correction to the primary outcome is a liberal choice that is neither pre-specified nor disclosed as a choice.
- **【Evidence】** `manuscript.md:146` and `:190`. Source `10_genetics_mr_outcome5086_28ddeath.csv` `p_fdr_bh` for CD14 Egger = 0.0766 (BH within that file's 15 rows). The full 45-test BH would raise CD14 Egger's value above 0.077 (further from significance).
- **【Why it matters】** The reported "BH-FDR 0.077 (not significant)" is the most favorable correction available; readers may believe the strongest possible correction was applied. This is a reporting-transparency gap, not a number error.
- **【Specific fix】** Either (a) apply BH-FDR across all 45 pre-specified tests and report the resulting CD14 Egger q-value, or (b) explicitly state: "BH-FDR was applied within the primary-outcome family of 15 tests as a pre-specified primary-analysis correction; a full 45-test family correction across all three outcomes would be more conservative."

### T2-1 (Tier 2) — "Significant separation" overstates the modesty of the external AUC
- **【Problem】** §3.5 calls the external AUC "a significant separation," but the 95% CI (0.532–0.748) only marginally excludes 0.5 (lower bound 0.532, just 0.032 above null).
- **【Evidence】** `manuscript.md:109`; source `09_external_validation.csv`: `auc_EMTAB4451_orientedSum=0.6382`, CI 0.5317–0.7475.
- **【Why it matters】** Single external cohort, n=106, 52 deaths — the effect is real but modest; "significant separation" overstates precision. The "comparable rather than superior" framing elsewhere is the right tone; this phrase is inconsistent with it.
- **【Specific fix】** "a nominal separation (95% CI 0.532–0.748, marginally excluding 0.5)" — or simply drop "significant."

### T2-2 (Tier 2) — IRG benchmark framing nuance
- **【Problem】** By the manuscript's *own* IRG recomputation (0.604), the signature (0.638) is +0.034 higher — nominally above its own benchmark — yet §3.4 claims "comparable rather than superior."
- **【Evidence】** `manuscript.md:106` ("comparable rather than superior") vs `:109` ("comparable to the IRG benchmark recomputed on the same cohort (0.604; Peng et al. [16] reported 0.619)"). Source `09_external_validation.csv`: `auc_IRG3_benchmark_EMTAB4451=0.604`.
- **【Why it matters】** Defensible via CI overlap, but the "rather than superior" wording undersells vs the 0.604 recomputation while the comparison to Peng's 0.619 is apt. Minor framing tension.
- **【Specific fix】** Clarify: "comparable to Peng's reported 0.619 and modestly above our own recomputation (0.604); the wide CI means the difference is not significant." (Keeps honesty, removes the slight undersell.)

### T3-1 (Tier 3) — Conclusion lists CV-AUC 0.659 without re-flagging "optimistic"
- **【Evidence】** `manuscript.md:207` lists "CV-AUC 0.659; independent external AUC 0.638" side by side; §3.4/§5 correctly flag 0.659 as optimistic, but the Conclusion sentence does not.
- **【Specific fix】** Add "(optimistic)" after 0.659 in l.207, or rephrase to "an optimistic within-cohort CV-AUC 0.659 and an honest external AUC 0.638."

## § Stands up (verified correct)
- Optimistic CV is honestly flagged in §3.4 and §5 #1. ✓
- Exposure–outcome sample overlap (eQTLGen ⊃ UKB; UKB sepsis outcome) disclosed in §2.10 and §5 #2. ✓
- Harmonisation now honestly states retained-instruments only; exact exclusion tally not itemised (l.72). ✓
- Calibration/DCA referenced for the external score (Fig S06). ✓
- FCGR3A correctly noted as not assessed (only 2 instruments). ✓
- CD14 Egger numbers (OR 0.906, P=5.1e-3, intercept P=0.34, p_fdr_bh=0.0766) all match source. ✓

## § Questions for the authors
- Was the 15-test (primary-outcome) BH-FDR genuinely pre-specified, or adopted post-hoc? This determines whether T1-2 is a wording fix or a re-analysis.
- Will you report the full 45-test family BH, or formally pre-specify the primary-outcome restriction?

## § What I actually checked
- `S06_auc_compare.csv`: CV 0.6586→0.659, train 0.7495→0.750 — **match**.
- `09_external_validation.csv`: orientedSum 0.6382 (manuscript 0.638), CI 0.5317–0.7475 (manuscript 0.532–0.748), locked L1 0.5848 (manuscript 0.585), IRG 0.604 — **all match**.
- `10_genetics_mr_outcome5086_28ddeath.csv`: CD14 Egger or_=0.90595, p=0.00511, intercept_p=0.344, p_fdr_bh=0.0766 — **match**; FCGR3A row = insufficient_instruments — **match**.
- No numeric discrepancy found; T1-1/T1-2/T2-1/T2-2 are framing/transparency issues.
