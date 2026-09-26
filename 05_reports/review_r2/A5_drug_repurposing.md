# A5 — Drug repurposing / LINCS L1000 biology (independent Round-2 review)

Reviewer layer: Drug repurposing & LINCS L1000 reverse-connectivity biology.
Manuscript v1.1.0. Reviewed as a fresh first submission; no prior-round file read.

---

## Mandatory check #3 — Drug metric (§2.8, §3.7, Table 2)

- `response_gene_concordance` is defined as **curated downstream response-gene overlap**, explicitly *not* a direct protein-target overlap. `manuscript.md:64` states the metric quantifies "concordance with a curated **downstream response-gene set**, and is *not* an overlap with the drug's direct molecular targets (which were not retrieved from a pharmacologic database in this study)." Confirmed correct.
- Per-drug fractions recomputed from `03_results/08_candidates_drugs.csv` (`n_rescue_mars1down` / `n_target_genes`) and matched to Table 2 exactly:
  - IL-7 5/5 = 1.00 ✓ (Table 2: 1.00)
  - GM-CSF 5/6 = 0.833 ✓ (Table 2: 0.83)
  - IFN-γ 5/7 = 0.714 ✓ (Table 2: 0.71)
  - Azithromycin 2/3 = 0.667 ✓ (Table 2: 0.67)
  - Lenalidomide 2/5 = 0.40 ✓ (Table 2: 0.40)
  - Thymosin α1 2/5 = 0.40 ✓ (Table 2: 0.40)
  - BCG 1/5 = 0.20 ✓ (Table 2: 0.20)
  No confusion with a target-based score; denominators are the curated set sizes. Confirmed consistent.
- "IFN-γ rescued 5/5 antigen-presentation genes" resolves to the 5 AP genes in its `rescue_genes` list. `08_candidates_drugs.csv` row IFN-gamma: `rescue_genes = HLA-DRA;HLA-DRB1;HLA-DQA1;HLA-DQB1;CD74` (5 AP genes, all Mars1-down), with `n_target_genes=7`, `n_rescue_mars1down=5`. So the 5/5 AP claim is correct and the full fraction is 5/7 = 0.714. See Issue 5 for the non-independence of this "gate."

## Mandatory check #4 — LINCS L1000 (§3.9)

- **azithromycin wtcs = 0.0626 and lenalidomide wtcs = 0.2058 (NOT 1.17).** Confirmed from `03_results/S08_l1000_candidate_scores.csv`: azithromycin `wtcs=0.0626`, lenalidomide `wtcs=0.2058`. The 1.17 value belongs to pravastatin's `wtcs=1.1557` in `S08_l1000_immuno_overlap.csv` and is correctly *not* used for either candidate. Verified no 1.17 appears for the candidates.
- Query described as **22 L1000-measurable consensus genes (20 Mars1-down + 2 Mars1-up PDCD1, LAG3)**. `manuscript.md:135` states this explicitly. Confirmed in prose.
- **HAVCR2 / FCGR3A stated as absent from the L1000 platform** and excluded by design. `manuscript.md:135`: "The two hubs absent from L1000 (HAVCR2, FCGR3A) were excluded from the connectivity query by platform design." Confirmed.
- **"BRD-" prefixes described as Broad anonymized IDs, not a BET-inhibitor class.** `manuscript.md:137`: "Broad-Institute LINCS identifiers (BRD-prefixed anonymized compound IDs, not a pharmacologic class)" and "The BRD-prefixed IDs require name/pharmacologic-class resolution before any mechanistic claim and are reported here as anonymized identifiers." Confirmed correct.
- Background centering claim **supported** (see § What I actually checked): recomputed mean rescue_score = 0.0064, median = 0.0055, fraction > 0 = 0.5362 → matches manuscript "mean 0.006, median 0.006, 53.6% > 0."
- "top rescue 0.32" **supported**: global max rescue_score over all 20,413 rows = 0.31823.

---

## Issues

### Issue 1 — Dual-direction requirement is contradicted by the stated rescue_score formula (HIGH)

【Problem】 The rescue_score formula as written treats all 22 query genes with identical sign, so it cannot implement the declared "dual-direction" down-regulation of PDCD1/LAG3, and it actually rewards worsening T-cell exhaustion.

【Evidence】 `manuscript.md:135` declares "2 Mars1-up exhaustion markers (PDCD1, LAG3; required to be down-regulated, iLINCS-style dual-direction)" but defines the score on the same line as "rescue = mean rank-percentile of the 22 genes − 0.5; positive = axis shifted toward expression." Recomputation shows wtcs = rescue_score × √22 for every row (azithromycin 0.0133 × 4.6904 = 0.0624 ≈ 0.0626; lenalidomide 0.0439 × 4.6904 = 0.206 ≈ 0.2058; full-file ratio = 4.6904 = √22, n = 22 queried genes), confirming the score is a plain mean of 22 unsigned rank-percentiles with no sign term.

【Why it matters】 Under the stated formula a compound that up-regulates the 20 antigen-presentation genes AND also up-regulates PDCD1/LAG3 (more exhaustion) receives a *higher* rescue_score, the opposite of the biological intent. The dual-direction claim is therefore unsubstantiated, and the metric is directionally wrong for the exhaustion arm — a problem that also inflates the glucocorticoid "positive-control" reading (§3.9) in an uncontrolled way and could mis-rank genuine immunorestorative compounds.

【Specific fix】 Replace the metric definition with an explicit, signed aggregation, e.g.: "For each of the 20 Mars1-down genes we used the up-regulation rank-percentile p_g; for the 2 Mars1-up markers (PDCD1, LAG3) we used the down-regulation percentile (1 − p_g). rescue_score = mean_{g=1..22}(s_g) − 0.5, where s_g = p_g for down-genes and s_g = (1 − p_g) for up-markers; wtcs = (Σ s_g − 11)/√22." If dual-direction was in fact not implemented, delete the dual-direction claim and state the score is a single-direction reversal of the Mars1-down axis only.

### Issue 2 — wtcs and rescue_score are mathematically identical, so presenting both implies two independent scores (MEDIUM)

【Problem】 wtcs is exactly rescue_score × √22 (n = 22), so the two reported columns carry the same information; reporting them as distinct "rescue" and "wtcs" metrics is redundant and can mislead readers into believing two corroborating scores were computed.

【Evidence】 Recomputed from `S08_l1000_candidate_scores.csv` and the full `S08_l1000_rescue_trtcp.csv` (20,413 rows): the ratio wtcs/rescue_score = 4.6904 for every row, equal to √22. Consequently the "background well-centered (mean 0.006, median 0.006; 53.6% > 0)" statement in `manuscript.md:135` refers to a single distribution reported twice.

【Why it matters】 The connect-score "proxy" adds no independent information to the rescue_score, and the centering claim is effectively stated twice for one quantity; a reader could interpret wtcs as an independent iLINCS-style cosine confirmation when it is a linear rescale. (Note: wtcs as (Σ−n/2)/√n is a non-parametric signed-rank-sum z-score, a reasonable proxy but distinct from the iLINCS cosine similarity — the word "proxy" is acceptable, but the redundancy should be removed.)

【Specific fix】 State explicitly that wtcs = rescue_score × √22 is a z-scored rescaling of the same signed-rank summary, present only one as the primary score (recommend rescue_score, with wtcs shown as its scaled form), and, if a genuinely second score is intended, define wtcs as a different statistic (e.g., a weighted cosine against the L1000 signature).

### Issue 3 — The 22-gene L1000 query is not reconciled with the 25-gene consensus set; excluded genes are incompletely itemized (MEDIUM)

【Problem】 The manuscript calls the query "the 22 consensus immune genes measurable on the L1000 platform" but only names HAVCR2 and FCGR3A as L1000-absent; 25 consensus − 2 named absent = 23, leaving one gene unaccounted between 23 and the stated 22.

【Evidence】 `manuscript.md:135` ("The query signature was the 22 consensus immune genes measurable on the L1000 platform … The two hubs absent from L1000 (HAVCR2, FCGR3A) were excluded") vs `manuscript.md:82`, which states 25 consensus immune genes. No per-gene L1000-presence map is provided in the text, and the brief's mandated CSVs do not contain this mapping.

【Why it matters】 Without the explicit 25 → 22 mapping (which three genes were dropped and why), the query is not reproducible and the count discrepancy (23 vs 22) is unexplained; reviewers cannot confirm that PDCD1 and LAG3 are genuinely among the 22 queried genes, which is the linchpin of the dual-direction claim (Issue 1).

【Specific fix】 Add a supplementary table mapping all 25 consensus immune genes to L1000 measurability, listing the three excluded genes and the reason (platform absence), and explicitly confirm PDCD1 and LAG3 are present in the 22-gene query used for `S08_l1000_candidate_scores.csv`.

### Issue 4 — response_gene_concordance lacks a null/shuffle baseline, so the per-drug fractions cannot distinguish true rescue from chance overlap with the large Mars1-down set (MEDIUM)

【Problem】 The concordance fraction is used as a ranking/positive-gate metric, but its denominators are author-curated set sizes and there is no permutation/null showing the fractions exceed chance; with tiny sets (azithromycin n = 3, others n = 5–7) the ranking is weak.

【Evidence】 `manuscript.md:64` (§2.8 definition) and `manuscript.md:117` (§3.7 ranking). `08_candidates_drugs.csv` `n_target_genes` = 5, 6, 7, 3, 5, 5, 5; `rescue_fraction` = 1.0, 0.833, 0.714, 0.667, 0.40, 0.40, 0.20 (matches Table 2 exactly). Mars1-down contains thousands of genes, so random response sets of size 3–7 overlap it non-trivially; no empirical p-value is reported.

【Why it matters】 Without a null, "azithromycin 2/3 = 0.667" is not demonstrably better than chance, and the shortlist order (IL-7 > GM-CSF > IFN-γ > azithromycin) reflects curated-set sizes as much as biology. This weakens the "method-positive gate" claim and the justification for prioritizing IL-7/GM-CSF/IFN-γ in the first validation wave.

【Specific fix】 Add a permutation baseline: for each drug, compute the expected concordance if its curated response genes were drawn at random from the genome, report observed − expected (or an empirical p-value over ≥ 1,000 shuffles of Mars1-down membership), and state explicitly that the fractions are descriptive unless they exceed the null.

### Issue 5 — The IFN-γ "method-positive gate" is self-confirming and should not be labeled a discriminant control (LOW–MEDIUM)

【Problem】 The gate requires IFN-γ (a canonical MHC-II inducer) to show ≥3/5 concordance with antigen-presentation genes, which is true by construction of its own curated set, so it validates the annotation pipeline rather than drug efficacy.

【Evidence】 `manuscript.md:64` "A method-positive gate required IFN-γ … to show ≥3/5 concordance"; `manuscript.md:117` "IFN-γ rescued 5/5 antigen-presentation genes (HLA-DRA, HLA-DRB1, HLA-DQA1, HLA-DQB1, CD74)." Recomputed from `08_candidates_drugs.csv`: IFN-gamma `rescue_genes` = HLA-DRA;HLA-DRB1;HLA-DQA1;HLA-DQB1;CD74 (5 AP genes, all Mars1-down) → 5/5 AP concordance holds by design; full fraction 5/7 = 0.714. The glucocorticoid caveat (`manuscript.md:139`) already shows a positive score is not sufficient for functional rescue, and limitation #9 acknowledges the gate "verifies a curated prior rather than independently discriminating true from false positives."

【Why it matters】 Calling it a "method-positive gate" implies it tests the repositioning logic; in fact it only confirms the curated prior. Mislabeling risks over-interpreting the control as evidence the pipeline can separate true from false rescuers.

【Specific fix】 Rename to "curation sanity check" and state: "The IFN-γ check confirms our curated response-gene lists include the expected antigen-presentation targets; it is a sanity check on the annotation pipeline, not an independent test of rescue efficacy (see glucocorticoid caveat, §3.9)."

---

## § Stands up (verified correct)

1. **Candidate wtcs values are correct and not the erroneous 1.17.** `S08_l1000_candidate_scores.csv`: azithromycin wtcs = 0.0626, lenalidomide wtcs = 0.2058. Recomputed azithromycin rescue 0.0133 × √22 = 0.0624 ≈ 0.0626; lenalidomide 0.0439 × √22 = 0.206 ≈ 0.2058. The 1.17 figure (pravastatin wtcs 1.1557) is correctly confined to the immuno-overlap control list.
2. **Per-drug concordance fractions match the source CSV and Table 2 exactly** (IL-7 5/5=1.0, GM-CSF 5/6=0.833, IFN-γ 5/7=0.714, azithromycin 2/3=0.667, lenalidomide 2/5=0.40, thymosin 2/5=0.40, BCG 1/5=0.20).
3. **LINCS background is well-centered, as claimed.** Recomputed from the full 20,413-row `S08_l1000_rescue_trtcp.csv`: mean rescue_score 0.0064, median 0.0055, fraction > 0 = 0.5362 → matches manuscript "mean 0.006, median 0.006, 53.6% > 0." The slight right-skew (mean 0.0064 vs median 0.0055) is negligible relative to the ±0.3 score range, so "not biased upward" is defensible.
4. **Query composition and platform exclusions are correctly stated in prose.** 22 L1000-measurable genes = 20 Mars1-down + 2 Mars1-up (PDCD1, LAG3); HAVCR2 and FCGR3A explicitly stated absent from L1000 and excluded by design (`manuscript.md:135`).
5. **"BRD-" semantics are correctly framed** as Broad anonymized LINCS IDs, not a BET-inhibitor pharmacologic class (`manuscript.md:137`).
6. **`response_gene_concordance` is honestly framed** as curated response-gene overlap, explicitly *not* a direct-target overlap, and the limitation section (#9) restates this and the 2/7 connectivity coverage.
7. **Virtual knockdown (§3.3) is correctly downgraded.** `manuscript.md:103`: "This is a consistency check, not an independent perturbation (virtual-knockdown) control, and is not used to validate the repositioning pipeline." Correctly scoped.
8. **Only 2/7 candidates received connectivity scores — honestly stated.** `manuscript.md:137` and limitation #9 both disclose that the five biologic/vaccine candidates (IL-7, GM-CSF, IFN-γ, thymosin α1, BCG) rest on mechanism-anchored annotation only.
9. **"top rescue 0.32" is supported.** Global max rescue_score over 20,413 compounds = 0.31823.

---

## § Questions for the authors

1. In the rescue_score aggregation, is the rank-percentile for PDCD1 and LAG3 sign-flipped (i.e., (1 − p) or negated) before averaging, or is the dual-direction claim inaccurate? Please provide the exact per-gene aggregation spec used to produce `S08_l1000_candidate_scores.csv`.
2. Beyond HAVCR2 and FCGR3A, which third consensus gene is absent from L1000 (to bring 25 → 22), and on what basis was it dropped? Please supply the full 25→22 gene-presence map.
3. Can you provide a permutation/null baseline for `response_gene_concordance` so the per-drug fractions can be judged against chance overlap with the (large) Mars1-down set?
4. For the five biologic/vaccine candidates, is there no L1000 genetic or overexpression perturbagen (e.g., `trt_oe`, `trt_sh`, consensus `pert_type`) that could yield a connectivity proxy, or is `trt_cp` truly the only viable path? Clarify whether "2/7" is a platform limitation or a curation one.

---

## § What I actually checked

Files read (none forbidden):
- `05_reports/manuscript.md` (full; focused §2.8, §3.1, §3.3, §3.7/Table 2, §3.9).
- `03_results/S08_l1000_candidate_scores.csv` (2 candidates).
- `03_results/S08_l1000_immuno_overlap.csv` (top immuno-relevant rescuers).
- `03_results/08_candidates_drugs.csv` (7 candidates, full columns).
- `03_results/S08_l1000_rescue_trtcp.csv` (full 20,413-row background; used Python csv/statistics, not the pipeline).

Values recomputed vs manuscript:
- azithromycin wtcs: CSV 0.0626 vs manuscript 0.06 → match (rounded).
- lenalidomide wtcs: CSV 0.2058 vs manuscript 0.21 → match (rounded).
- wtcs = rescue_score × √22 verified for all 20,413 rows (ratio 4.6904).
- Per-drug fractions from `08_candidates_drugs.csv` matched Table 2 exactly (see Mandatory #3).
- IFN-γ `rescue_genes` = HLA-DRA;HLA-DRB1;HLA-DQA1;HLA-DQB1;CD74 (5 AP genes, all Mars1-down) → 5/5 AP claim holds; full 5/7 = 0.714.
- Background: mean rescue_score 0.0064, median 0.0055, >0 fraction 0.5362 vs manuscript 0.006 / 0.006 / 53.6% → match.
- Global max rescue_score = 0.31823 vs manuscript "top rescue 0.32" → match.

Discrepancy found:
- None on the verified numeric claims.
- Two prose/logic discrepancies flagged as issues (not resolvable from CSVs): (a) the rescue_score formula (`manuscript.md:135`) contradicts the declared dual-direction requirement (Issue 1); (b) the 25-consensus → 22-query count is unreconciled given only 2 named L1000-absent genes (Issue 3).
