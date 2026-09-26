# A2 — Design & Statistics Lens (blind)

**Mandate:** find design-level and multiple-testing defects; sparse-cell / low-power failures; whether the stated correction matches the actual data.

## Tier 0 (conclusion-invalidating)

### A2-T0-1. The 45-test Benjamini–Hochberg claim "no estimate reached q<0.05 (smallest q=0.058)" is FALSE.
【Problem】 The manuscript repeatedly asserts that under the pre-specified 45-test family correction, no MR estimate reached significance, with the smallest q being 0.058 (CD14 MR-Egger). This is arithmetically contradicted by the study's own CSV `p_fdr_bh` column and by an independent recomputation.
【Evidence】
- Recomputed 45-test BH over all 45 assessable gene×estimator tests (raw p from the three MR CSVs): **minimum q = 0.0000**; 3 tests reach q<0.05:
  - CD74 Weighted median, critical-care: raw p=0.0 → q=0
  - CD74 MR-Egger, critical-care: raw p=6.626e-13 → q≈5e-12
  - CD74 MR-Egger, susceptibility: raw p=1.648e-4 → q=0.0025
- The manuscript's own `10_genetics_mr_outcome4982_criticalcare.csv` already carries `p_fdr_bh` = 4.97e-12 (CD74 MR-Egger) and 0.0 (CD74 Weighted median) for the *narrower* 15-test per-outcome correction; the 45-test q is ≥ these, so still <<0.05. The claim "no estimate reached q<0.05" is therefore impossible given the supplied data.
- Locations of the false claim: §2.10 l.72 ("no estimate reached q<0.05 (smallest q=0.058, CD14 MR-Egger on 28-day death)"); §3.10 l.146 ("Under the pre-specified … full 45-test family … this corresponds to q=0.058 and does not cross the 0.05 threshold" — true for CD14 but omits the 3 CD74 tests that DO cross); §3.10 l.173 (CD14 "q=0.058 under the pre-specified 45-test family, but no primary IVW estimate reaches significance" — omits CD74); §5 limitation 2 l.190 ("does not survive the pre-specified Benjamini–Hochberg correction across the full 45-test family … q=0.058 … no causal claim for the hub is made"); Discussion l.181 ("this did not survive the pre-specified 45-test family correction (q=0.058)").
【Why it matters】 This is the central verdict of the entire MR layer ("MR is Tier-3, purely hypothesis-generating, nothing survives"). A statistically literate reviewer who opens the CSV will recompute and find the opposite — a credibility-destroying moment that can sink the revision. It is also a textbook "disclosure ≠ resolution" failure: the v1.3.0 edit pasted a wrong q narrative into four places.
【Specific fix】 Replace every occurrence with a correct statement, e.g. for §2.10:
> "The pre-specified primary correction was the full 45-test family (five assessable genes × three estimators × three outcomes). Under it, three CD74 tests reached q<0.05 — critical-care MR-Egger (q≈5×10⁻¹²) and weighted median (q≈0), and susceptibility MR-Egger (q=0.0025) — but each is disqualified from a causal-target claim: the critical-care signal reverses the direction predicted by the Mars1 down-regulated program and rests on only three instruments, and the susceptibility MR-Egger carries a significant Egger intercept (pleiotropy). The 28-day-death CD14 MR-Egger (q=0.058) is the only phenotype-coherent protective signal and remains suggestive."

## Tier 1

### A2-T1-1. "four of the five assessable hubs returned protective estimates concordant across all three methods" is false.
【Problem】 HAVCR2's MR-Egger estimate is 1.010 (OR>1, i.e. not protective); only its IVW (0.978) and weighted median (0.960) are <1. So HAVCR2 is NOT concordant-protective across all three methods.
【Evidence】 §3.10 Table 3 HAVCR2 row: IVW 0.978, MR-Egger 1.010, Weighted median 0.960. Same false claim in Discussion l.181 ("for four of five assessable hubs").
【Why it matters】 Overstates the coherence of the MR signal; a reviewer checking Table 3 against the prose will catch it.
【Specific fix】 "three of the five assessable hubs (HLA-DQA1, CD14, FIS1) showed protective estimates across all three methods; HAVCR2 showed two protective and one null MR-Egger (1.010), and CD74 was directionally discordant."

### A2-T1-2. "CD74 critical-care … fails correction across all 15 tests (FDR ≈ 0.21)" is false.
【Problem】 The supplied `p_fdr_bh` for CD74 critical-care is 0.070 (IVW), 4.97e-12 (MR-Egger), 0.0 (Weighted median). None is 0.21; the robust estimator is overwhelmingly significant.
【Evidence】 `10_genetics_mr_outcome4982_criticalcare.csv`; §3.10 l.171.
【Why it matters】 Same root error as T0-1; propagates the false "nothing is significant" narrative.
【Specific fix】 Replace with the correct per-outcome and 45-test q values and a biological (not correction-based) reason for caution, as in A2-T0-1.

### A2-T1-3. Sample overlap inflates the already-significant CD74 signal.
【Problem】 The eQTLGen discovery includes UK Biobank participants who also populate the UKB sepsis outcomes, so exposure–outcome overlap biases estimates toward significance. This makes the CD74 critical-care q≈5e-12 *more* inflated, not less — strengthening the case for biological (not statistical) caution.
【Evidence】 §2.10 l.70 (overlap acknowledged, no mrSampleOverlap correction applied); Burgess/Davies/Thompson 2016 (ref 31).
【Why it matters】 The manuscript acknowledges overlap but does not note it *inflates* the CD74 significance; a reviewer will raise it.
【Specific fix】 Add: "Because the overlap biases toward significance, the CD74 critical-care association is likely over-stated in magnitude; we therefore treat its direction and existence as hypothesis-generating."

## Tier 2
### A2-T2-1. Power framing for CD74 crit-care is weak.
【Problem】 1,380 cases and 3 instruments give a wide CI (1.175–4.200); this is a legitimate reason for caution but is currently swamped by the false correction claim.
【Specific fix】 Retain the precision caveat explicitly: "the 95% CI (1.175–4.200) reflects the imprecision of a 3-instrument, 1,380-case estimate."

## § Stands up (verified correct)
- CD14 28-day-death MR-Egger p=5.1e-3, q_45=0.0575 (just above 0.05) — the manuscript's *specific* q=0.058 for this test is correct; only the "smallest q / nothing survives" framing is wrong. ✓
- External AUC 0.638 CI 0.532–0.748 verified against `09_external_validation.csv`. ✓
- Egger intercept for CD74 crit-care is genuinely null (p=0.99987) — a real strength. ✓

## § Questions for the authors
1. Why does the text state CD74 crit-care "FDR≈0.21" when the result CSV shows p_fdr_bh 4.97e-12? Was an older number carried over?
2. Should the 45-test BH be reported as a table (all 15 gene×estimator×3-outcome q-values) to pre-empt reviewer recomputation?

## § What I actually checked
- Recomputed 45-test BH in Python from raw p in the three MR CSVs → min q=0.0000, 3 tests q<0.05.
- Cross-checked against the CSV `p_fdr_bh` column (per-outcome 15-test BH): values 4.97e-12 and 0.0 confirm the family-level claim is impossible.
- Verified CD14 28d Egger p and q; HAVCR2 Table-3 estimates; CD74 crit-care intercept_p.
