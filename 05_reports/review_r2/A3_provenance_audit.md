# A3 — Implementation (number provenance) audit

**Layer:** Implementation / number-provenance auditor. Scope: arithmetic, provenance, internal consistency only. Biology and writing were not graded.

**Files read (all permitted):** `05_reports/manuscript.md`; `03_results/S01_immunoparalysis_direction.csv`; `08_candidates_drugs.csv`; `S08_l1000_candidate_scores.csv`; `10_genetics_mr_outcome5086_harmonised.csv`; `10_genetics_mr_outcome4982_harmonised.csv`; `10_genetics_mr_harmonised.csv`; `10_genetics_mr_outcome5086_28ddeath.csv`; `10_genetics_mr_outcome4982_criticalcare.csv`; `10_genetics_mr.csv`; `S06_auc_compare.csv`; `09_external_validation.csv`; `S02_immunoparalysis_score.csv`; `S05_hub_genes.csv`. (Forbidden review/response/manifest files were not opened.)

---

## Issues

### Issue 1 — [P0] ITGAM is labelled "not significant at FDR<0.05" but its adj.P.Val is 1.7×10⁻³ (<0.05), so it IS significant

【Problem】 Table 1 (manuscript.md:92) annotates ITGAM as "integrin αM (not significant at FDR<0.05)", but the source CSV shows ITGAM adj.P.Val = 1.6773×10⁻³, which is well below the 0.05 FDR threshold.

【Evidence】 `03_results/S01_immunoparalysis_direction.csv:19` → `ITGAM … -0.2084444637173366, 0.001188638511847806, 0.0016773155724580273, False, ITGAM, Mars1_down`. The `DEG_0.3` flag is `False` only because |logFC|=0.21 < 0.30 (effect-size cutoff), NOT because of FDR. The `adj.P.Val` column (the FDR) = 0.001677 < 0.05, so ITGAM passes FDR. The "not significant at FDR<0.05" note is false.

【Why it matters】 A reader checking the one named counterexample against the data finds the opposite of what is stated. It also undermines the credibility of every other hand-checked value in Table 1, and it contradicts the paper's own §3.1 count logic (ITGAM is correctly counted among the 21 "down + significant" genes, so the table note and the narrative are internally inconsistent).

【Specific fix】 Replace the Table 1 cell text with a cause-correct note, e.g.: "ITGAM | −0.21 | 1.7e-03 | integrin αM (below the |logFC|≥0.3 DEG cutoff; adj.P=1.7×10⁻³, so FDR-significant but excluded as a DEG on effect-size grounds)."

---

### Issue 2 — [P0] Self-contradiction on the external AUC framing: "exceeded the IRG benchmark" (§3.5) vs "comparable rather than superior" (§3.4) and "comparable to, not better than" (Discussion)

【Problem】 The same external result (AUC 0.638) is described as having "exceeded the IRG benchmark" in §3.5 but as "comparable rather than superior" in §3.4 and "comparable to, not better than" in the Discussion, with no reconciliation.

【Evidence】 manuscript.md:109 — "a significant separation that again **exceeded** the IRG benchmark recomputed on the same cohort (0.604; for context, Peng et al. [16] reported 0.619 on this cohort)." manuscript.md:106 — "Relative to the IRG benchmark (…) the signature is **comparable rather than superior**." manuscript.md:179 (Discussion) — "… an honest external AUC 0.638 (§3.5) … **comparable to, not better than**, the published benchmark." The Abstract (EN:14 "comparable to … (0.619–0.648)"; ZH:25 "相当") is correctly hedged, so the conflict is internal to the body.

【Why it matters】 A headline over-claim in one section and a caveat elsewhere is exactly the P0 self-contradiction pattern the panel brief flags. Reviewers at a methods-honest venue will read §3.5 "exceeded" against §3.4 "comparable rather than superior" and conclude the framing is unstable. Note 0.638 sits inside the abstract's own benchmark band 0.619–0.648, so "comparable" is the defensible word; "exceeded" overstates.

【Specific fix】 Use one consistent verb. Edit manuscript.md:109 to: "a significant separation that was **consistent with (and numerically aligned with) the IRG benchmark recomputed on the same cohort (0.604; Peng et al. [16] reported 0.619)**, remaining comparable rather than superior." Drop or qualify "best published" (see Issue 5) to match.

---

### Issue 3 — [P1] CD14 MR-Egger BH-FDR reported as 0.026, but the source CSV value is 0.0766

【Problem】 The manuscript reports CD14 MR-Egger "BH-FDR 0.026 across all 15 gene × outcome MR-Egger tests", but the source `10_genetics_mr_outcome5086_28ddeath.csv` p_fdr_bh for that row is 0.0766, and 0.0051 × 15 ≈ 0.0765, i.e. the CSV's value is the BH adjustment across all 15 Egger tests. The 0.026 figure corresponds to a within-5-test BH (0.0051 × 5 ≈ 0.0255), not "across all 15".

【Evidence】 `10_genetics_mr_outcome5086_28ddeath.csv:9` → `CD14 … MR-Egger … 0.9059506764792497 … 0.0051095663017020065 … p_fdr_bh=0.0766434945255301`. manuscript.md:146 and manuscript.md:190 state "BH-FDR 0.026 across all 15 gene × outcome MR-Egger tests". Raw p=0.0051096; ×15 = 0.07664 (matches CSV); ×5 = 0.02555 (matches the 0.026 the text prints).

【Why it matters】 The reported FDR denominator ("15") cannot yield 0.026; the value traceable to the source file is 0.077. If the manuscript means "across all 15 tests", the number is wrong; if it means "within the 5 primary-outcome Egger tests", the denominator wording is wrong. Either way the provenance is broken and a reviewer recomputing BH will get 0.077, not 0.026.

【Specific fix】 Either (a) report the source value: "BH-FDR 0.077 across all 15 gene × outcome MR-Egger tests" (matching `p_fdr_bh` in the CSVs), or (b) keep 0.026 only if you also state the denominator explicitly: "BH-FDR 0.026 within the five primary-outcome (ieu-b-5086) MR-Egger tests." Pick one and make the number and the denominator agree.

---

### Issue 4 — [P1] STROBE-MR harmonisation exclusion tally is claimed to be "itemised in the *_harmonised.csv tables" but those files contain no such columns

【Problem】 manuscript.md:72 states per-gene exclusion tallies (palindromic, strand-ambiguous, allele-incompatible) "are itemised in the accompanying `*_harmonised.csv` tables (STROBE-MR item 9b)", yet the three `*_harmonised.csv` files I read contain only retained-instrument columns and no exclusion-count columns.

【Evidence】 `10_genetics_mr_outcome5086_harmonised.csv` (and the 4982 and main harmonised files) have the header `rsid,ea_e,nea_e,beta_e,se_e,p_e,eaf_e,ea_o,nea_o,beta_o,se_o,p_o,eaf_o,gene,F` and list only the SNPs that survived harmonisation. There is no `palindromic` / `strand_ambiguous` / `allele_incompatible` column or any per-gene count. FCGR3A is simply absent (consistent with "not assessed"), but the *excluded* SNPs and their reasons are not present.

【Why it matters】 STROBE-MR item 9b requires the exclusion tally to be reported and traceable. As written, a reader opening the named file finds no tally, so the claim is unverifiable from the cited source. This is a provenance gap that a methods reviewer will flag, and it leaves the "FCGR3A only two instruments" statement (manuscript.md:144) unsupported by any visible dropped-SNP audit in the cited file.

【Specific fix】 Either add the exclusion columns/counts to the `*_harmonised.csv` files (e.g., append per-gene rows or a companion `*_harmonised_excluded.csv` with reason codes), or change manuscript.md:72 to point to the file that actually holds the tally (e.g., `05_reports/s10_run_log*.txt` or a new `10_genetics_mr_harmonisation_tally.csv`), and verify the numbers there match the stated FCGR3A reasoning.

---

### Issue 5 — [P2] "best published" wording remains and contradicts the "comparable" framing

【Problem】 The phrase "best published sepsis mortality signatures" survives at two locations, lightly over-claiming against the manuscript's own "comparable" stance.

【Evidence】 manuscript.md:109 — "… at a level comparable to the **best published** sepsis mortality signatures, with magnitude that is real but modest." manuscript.md:179 — "… places the signature at a level comparable to the **best published** sepsis mortality signatures." (Both are hedged by "comparable to … modest", but "best published" implies superiority the rest of the paper disclaims.)

【Why it matters】 Reinforces the Issue 2 inconsistency: calling the result "comparable to the best published" sits awkwardly next to "comparable rather than superior" and "exceeded" in the same three sections. A single consistent comparator adjective is needed.

【Specific fix】 Replace "best published sepsis mortality signatures" with "published sepsis mortality signatures" (drop "best") at both :109 and :179, keeping "comparable to … with magnitude that is real but modest."

---

### Issue 6 — [P2 / informational] "virtual-knockdown" string present but correctly negated

【Problem】 The string "virtual-knockdown" (a Round-1 flagged phrasing) is still present, but in a correct, negated context — not an over-claim.

【Evidence】 manuscript.md:103 — "this is a consistency check, not an independent perturbation (virtual-knockdown) control, and is not used to validate the repositioning pipeline." The brief listed "Virtual knockdown" among strings that "should have been removed"; here it is used to deny the analogy, which is appropriate.

【Why it matters】 No action required for accuracy; flagged only for completeness of the consistency grep. No change needed unless the journal style forbids the term entirely.

【Specific fix】 No change required. If the journal dislikes the term, replace "(virtual-knockdown) control" with "(in-silico knockdown) control" — optional.

---

## § Stands up (verified correct — suspected but confirmed)

1. **§3.1 directionality counts are exactly correct.** Recomputed from `S01_immunoparalysis_direction.csv` (25 rows): 23 Mars1_down / 2 Mars1_up; 22 with adj.P.Val<0.05; 21 both down AND adj.P<0.05 (the two down-but-not-sig are CD8B 0.0767 and GZMA 0.1100; LAG3 is up). Matches manuscript.md:82, :218.
2. **All 8 spot-checked genes match the CSV to the rounding.** HLA-DRB1 Δ−0.8925→−0.89 / adj.P 1.07e-15→1.1e-15; CD74 −0.7578→−0.76 / 2.08e-15→2.1e-15; CD14 −0.7657→−0.77 / 0.0; FCGR3A −0.6097→−0.61 / 9.05e-11→9.1e-11; HAVCR2 −0.3488→−0.35 / 2.84e-13→2.8e-13; HLA-DRA −0.4689→−0.47 / 3.77e-07→3.8e-07; LYZ −0.2561→−0.26 / 3.56e-06→3.6e-06 (ITGAM logFC −0.2084→−0.21 also matches; only its significance note is wrong — see Issue 1).
3. **Drug fractions (Table 2) reconcile exactly with `08_candidates_drugs.csv`.** IL-7 5/5=1.00; GM-CSF 5/6=0.833; IFN-γ 5/7=0.714; Azithromycin 2/3=0.667; Lenalidomide 2/5=0.40; Thymosin 2/5=0.40; BCG 1/5=0.20. All `n_target_genes`/`n_rescue_mars1down`/`rescue_fraction` columns match. The "IFN-γ rescued 5/5 antigen-presentation genes" resolves to its `rescue_genes` list = HLA-DRA;HLA-DRB1;HLA-DQA1;HLA-DQB1;CD74 (5 AP genes), all Mars1-down (manuscript.md:117, :125 consistent).
4. **LINCS wtcs values are correct and the 1.17 trap is avoided.** `S08_l1000_candidate_scores.csv`: azithromycin wtcs=0.0626 (rank 9152, rescue 0.0133); lenalidomide wtcs=0.2058 (rank 5435, rescue 0.0439). Matches manuscript.md:137 ("wtcs 0.06"/"wtcs 0.21", ranks 9,152/20,413 and 5,435/20,413). The query is described as 22 L1000-measurable genes (20 down + 2 up PDCD1/LAG3) with HAVCR2/FCGR3A excluded (manuscript.md:135) — consistent with the file.
5. **All MR Table 3 / Table 4 numbers trace to the CSVs.** CD14 Egger OR 0.90595→0.906, p 0.0051, intercept p 0.344 (manuscript.md:154); IVW/weighted-median ORs, CIs, Q-p, I² and median F (35.4/168.1/45.7/36.4/75.0) all match `10_genetics_mr_outcome5086_28ddeath.csv` + the three harmonised files. Critical-care CD74 IVW 2.222 (1.175–4.200) p 0.014, Egger intercept p≈1.00; susceptibility CD74 Egger OR 1.118 p 1.7e-4 intercept p 1.0e-4 — all match `10_genetics_mr_outcome4982_criticalcare.csv` and `10_genetics_mr.csv`. n IV counts (3/4/6/6/8; FCGR3A absent) match the harmonised files row-for-row.
6. **AUC provenance reconciles.** `S06_auc_compare.csv`: CV 0.6586→0.659, train 0.7495→0.750, Mars1 0.5782→0.578, IRG 0.619/0.648. `09_external_validation.csv`: orientedSum 0.6382→0.638 (CI 0.5317–0.7475→0.532–0.748), locked 0.5848→0.585 (CI 0.4687–0.6959→0.469–0.696), 29/30 mapped, 106 samples / 52 deaths / 54 survivors, IRG 0.604, missing gene HLA-DQA1. All match manuscript.md:106, :109, :67.
7. **Forbidden/over-claim strings correctly removed.** "rescue_fraction", "druggable", "progressively ordered", "4/5" — none present (targeted greps returned no matches). The Abstract (EN:14 / ZH:25) does NOT contain "exceeding"/"超过" and is correctly hedged ("comparable to"/"相当").
8. **References are 1–31 sequential with no gaps or duplicates** (manuscript.md:258–288). §7 provenance table entries I could trace (direction counts, hub genes, AUCs, drug fractions, LINCS, MR) all match their cited sources; the 6 hub genes match `S05_hub_genes.csv` (all True ×3 methods).

---

## § Questions for the authors

1. Where do the STROBE-MR harmonisation exclusion tallies (palindromic / strand-ambiguous / allele-incompatible per-gene counts) actually live? The three `*_harmonised.csv` files I read contain only retained-SNP columns, so the claim at manuscript.md:72 is currently untraceable. Please point to the exact file/columns or add them.
2. For CD14 MR-Egger, was 0.026 computed within the 5 primary-outcome Egger tests or across all 15? The source CSV `p_fdr_bh` = 0.0766 (across 15). Please confirm which denominator is intended so the text and number agree (Issue 3).
3. The Mars1 immune-score median −0.79 (manuscript.md:100, §7) is cited to `S02_immunoparalysis_score.csv`; I did not independently recompute the median from the 804-row file. Please confirm it is the median of the Mars1 subgroup only (n = ?) and not the full cohort.
4. Is ITGAM's "not significant at FDR<0.05" note (manuscript.md:92) intentional, or should it read "below the |logFC|≥0.3 DEG cutoff (adj.P=1.7×10⁻³)"? The data show it is FDR-significant (Issue 1).

---

## § What I actually checked

**Files read and what was recomputed vs the manuscript (discrepancy stated):**

- `S01_immunoparalysis_direction.csv` — recomputed 23 down / 2 up; 22 adj.P<0.05; 21 down+adj.P<0.05. **Discrepancy:** ITGAM adj.P=0.001677<0.05 (significant) but manuscript.md:92 calls it "not significant at FDR<0.05" (Issue 1). Spot-check of 8 named genes' logFC+adj.P: all match except the ITGAM significance note.
- `08_candidates_drugs.csv` — recomputed all 7 fractions and rescue_genes. **None** vs manuscript Table 2 (all match); IFN-γ 5 AP rescue_genes resolve correctly.
- `S08_l1000_candidate_scores.csv` — azithromycin wtcs 0.0626, lenalidomide wtcs 0.2058. **None** vs manuscript.md:137 (both correct; the 1.17 trap avoided).
- `10_genetics_mr_outcome5086_28ddeath.csv` — recomputed all Table 3 OR/CI/p/Q/I²/median-F. **Discrepancy:** CD14 Egger p_fdr_bh=0.0766 vs manuscript "BH-FDR 0.026" (Issue 3). All other Table 3 values match.
- `10_genetics_mr_outcome4982_criticalcare.csv` — recomputed Table 4 critical-care column + §3.10 CD74 claims. **None** vs manuscript (all match).
- `10_genetics_mr.csv` — recomputed Table 4 susceptibility column + §3.10 CD74 susceptibility Egger. **None** vs manuscript (all match).
- `10_genetics_mr_outcome5086_harmonised.csv`, `10_genetics_mr_outcome4982_harmonised.csv`, `10_genetics_mr_harmonised.csv` — recomputed n IV per gene (3/4/6/6/8; FCGR3A absent) and median F. **None** vs manuscript Table 3. **Discrepancy:** no STROBE-MR exclusion-tally columns present despite manuscript.md:72 claim (Issue 4).
- `S06_auc_compare.csv` — CV 0.6586, train 0.7495, Mars1 0.5782, IRG 0.619/0.648. **None** vs manuscript.
- `09_external_validation.csv` — orientedSum 0.6382 (CI 0.5317–0.7475), locked 0.5848 (CI 0.4687–0.6959), 29/30, 106/52/54, IRG 0.604, missing HLA-DQA1. **None** vs manuscript.
- `S02_immunoparalysis_score.csv` — opened; Mars1 subgroup scores present and negative as expected. Median −0.79 NOT independently recomputed from the 804 rows (flagged in Questions).
- `S05_hub_genes.csv` — 6 genes, all True ×3 methods. **None** vs manuscript (matches the six hub genes).
- `manuscript.md` (full) — consistency greps: "rescue_fraction", "druggable", "progressively ordered", "4/5" → absent (correctly removed); "exceeded" present at :109 (Issue 2); "best published" at :109, :179 (Issue 5); "virtual-knockdown" at :103 correctly negated (Issue 6). References 1–31 sequential, no gaps/dupes.

**Severity tally:** P0 = 2 (Issues 1, 2); P1 = 2 (Issues 3, 4); P2 = 2 (Issues 5, 6).
