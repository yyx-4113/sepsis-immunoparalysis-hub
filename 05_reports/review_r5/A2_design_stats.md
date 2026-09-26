# A2 — Design / Statistics / Causal-inference lens

I reviewed v1.4.0 as a fresh submission, verifying every MR statistic against `03_results/10_mr_bh_family.csv` and the three raw MR CSVs. The v1.3.0 fabrication is GONE — the MR layer is now numerically correct. My findings concern precision of the caveats and one incorrect stated range.

## Findings

### Tier 1 — A2-1: Stated I² range contradicts the source CSVs (0.00–0.29 vs true 0.00–0.502)
【Problem】 §3.10 states "heterogeneity was low (I² 0.00–0.29)," but across all 45 MR tests the true I² range is 0.00–0.502.
【Evidence】 §3.10 (line 146): "heterogeneity was low (I² 0.00–0.29)." Re-extracted all I² from `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`: max I² = 0.502 (FIS1 critical-care IVW), and 4 tests exceed 0.29 — FIS1 critcare 0.502, HAVCR2 critcare 0.391, CD14 suscept 0.379, HAVCR2 suscept 0.342. The 0.00–0.29 range is only true for the *primary* outcome (5086 death, Table 3).
【Why it matters】 This is the same "stated statistic contradicts its own data" slip class that destroyed the prior version. As written "throughout" reads as covering all outcomes; a reviewer re-running I² will flag it as an error.
【Specific fix】 Scope the claim to the primary outcome and disclose secondary heterogeneity: "heterogeneity was low across the primary-outcome tests (I² 0.00–0.29); the critical-care and susceptibility secondary outcomes showed higher I² (up to 0.50 for FIS1 under critical care), reported in the source MR CSVs."

### Tier 1 — A2-2: Egger intercept with 3 instruments is cited as reassurance
【Problem】 The null CD74 critical-care Egger intercept (P=1.00) is presented as evidence against pleiotropy, but with only 3 instruments the intercept is essentially non-estimable.
【Evidence】 §3.10 (line 159) "MR-Egger 2.222 with a null intercept, P=1.00"; §3.10 (line 171) "null Egger intercept P=1.00, I²=0.00"; §5 (line 190) "null Egger intercept P=1.00." Source `10_genetics_mr_outcome4982_criticalcare.csv`: CD74 MR-Egger nsnp=3, egger_intercept_p=0.99987. The text already says "rests on only three instruments" but still leans on the null intercept as a positive sign.
【Why it matters】 A null intercept on 3 SNPs cannot exclude directional (horizontal) pleiotropy; citing it as reassurance is misleading and is exactly what a methods reviewer will attack.
【Specific fix】 Append to each Egger-intercept mention: "although with only three instruments the Egger intercept is uninformative about pleiotropy, so its null cannot be read as evidence against it."

### Tier 1 — A2-3: Sample-overlap bias direction is imprecise
【Problem】 The CD74 critical-care significance is said to be "inflated by exposure–outcome sample overlap," implying the magnitude is exaggerated.
【Evidence】 §3.10 (line 171) and §5 (line 190): "inflated by exposure–outcome sample overlap." Per Burgess, Davies & Thompson (ref 31), overlap primarily biases standard errors *downward* (inflated type-1-error risk) and pulls the causal point estimate *toward the null* (attenuation), not upward.
【Why it matters】 The reverse-direction OR 2.22 is already hard to interpret; the "inflated" wording could be misread as the effect size being artifactually large, when the real risk is a too-small p-value (type-1 error), not a too-large OR.
【Specific fix】 "with exposure–outcome sample overlap biasing the standard errors downward (inflating type-1-error risk); the true association may be weaker or null, and the point estimate is not necessarily exaggerated."

### Tier 2 — A2-4: Secondary-outcome I² not shown in Table 4
【Problem】 Table 4 reports only IVW OR/P for the three outcomes; the higher secondary-outcome heterogeneity (A2-1) is invisible to the reader.
【Evidence】 §3.10 Table 4 (lines 163–169) shows no I²/Q column.
【Why it matters】 Drives the A2-1 discrepancy; readers cannot see the heterogeneity that tempers the secondary signals.
【Specific fix】 Add an I² column to Table 4, or footnote the max secondary I².

### Tier 2 — A2-5: Family-BH "min q = 0" wording
【Problem】 The text implies a clean "minimum q = 0" for CD74 WM critical-care; this is an underflow p (p=0.0 in CSV), so q=0 is a floor, not a precise estimate.
【Evidence】 `10_mr_bh_family.csv` row 17: CD74 Weighted median 4982_critcare p=0.0, q_family_45test=0.0.
【Why it matters】 Minor; "q≈0" is already used, which is fine. Just avoid implying a precise zero.
【Specific fix】 Keep "q≈0"; no change needed beyond A2-1 scoping.

## § Stands up (verified correct)
- Family BH: 3 CD74 tests q<0.05 (critcare WM q=0, critcare Egger q=1.49×10⁻¹¹, suscept Egger q=0.0025) — matches `10_mr_bh_family.csv` exactly.
- CD14 5086 Egger OR 0.906, P=5.1×10⁻³, per-outcome 15-test p_fdr_bh=0.0766, family q=0.0575≈0.058 — all match source (`10_genetics_mr_outcome5086_28ddeath.csv`).
- CD74 4980 Egger OR 1.118, P=1.7×10⁻⁴, intercept P=1.0×10⁻⁴ (pleiotropy) — matches.
- "median F 35–168" — matches Table 3 (CD74 35.4 … HLA-DQA1 168.1).
- 45-test family correct (5 genes × 3 estimators × 3 outcomes; FCGR3A excluded) — BH table has 45 rows.

## § Questions for the authors
- Will you report the MR-Egger intercept CIs (not just P) for the 3-instrument genes, to show the intercept estimate is also imprecise?
- Did you consider a leave-one-instrument-out sensitivity for CD74 critical-care (3 instruments only)?

## § What I actually checked
- Read `manuscript.md` v1.4.0 (MR sections §2.10, §3.10, §5).
- Parsed all three MR CSVs + `10_mr_bh_family.csv` in Python; recomputed the I² range (max 0.502), verified every cited OR/P/q/intercept_p/nsnp against source.
- Confirmed family-BH counts and q values match the manuscript's three-surviving-tests claim.
