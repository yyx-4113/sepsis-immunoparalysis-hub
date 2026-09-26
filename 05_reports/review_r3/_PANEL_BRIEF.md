# Round-3 Independent Panel Brief (v1.2.0)

This is a **fresh first-submission review** of a single-author computational-biology manuscript. You have NOT seen any prior review. Treat the manuscript as if new.

## Manuscript under review
`D:\2026.9\极速交付9月会员日优惠套路\05_多组学+虚拟敲除药物发现\方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位\05_reports\manuscript.md`
(288 lines; Abstract EN + 中文摘要 + §1–7 + Data availability / Ethics / Author / Funding / COI / References 1–31)

## What the study claims
- Re-analysis of GSE65682 (802 samples, 4 MARS transcriptomic endotypes; Mars1 = immunosuppressed). 23/25 consensus immune genes directionally down in Mars1, 22 FDR<0.05, 21 both.
- Six hub genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1) by co-expression + tri-method ML consensus.
- 30-gene immune-risk signature: within-cohort 5-fold CV AUC 0.659 (optimistic), honest external AUC 0.638 on E-MTAB-4451 (n=106, 52 deaths).
- Mechanism-anchored drug repositioning: 7 immunostimulatory agents ranked by `response_gene_concordance` (curated response-gene overlap, NOT direct target overlap). LINCS L1000 reverse-connectivity scored only the 2 small molecules (lenalidomide, azithromycin).
- Two-sample MR (eQTLGen × UK Biobank sepsis GWAS) on 5 of 6 hub genes (FCGR3A only 2 instruments); disclosed sample overlap; hypothesis-generating only.

## Independence discipline (mandatory)
**Forbidden to read** (any of these invalidates your independence):
`REVIEW_round1_20260926.md`, `REVIEW_round2_20260926.md`, `RESPONSE_*.md`, `REVISION_*.md`, the entire `05_reports/review/` and `05_reports/review_r2/` directories, `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, and **any other reviewer file in `05_reports/review_r3/`**.
Do not assume the manuscript passed prior review. Treat as first submission. Every judgement must come from text or source data you read yourself. Any claim you CAN verify, you MUST verify.

## Output contract — every issue needs four parts
- 【Problem】 one sentence
- 【Evidence】 pinned to manuscript.md:line or section + exact numbers (recomputed yourself from source)
- 【Why it matters】 concrete effect on credibility / acceptance
- 【Specific fix】 paste-ready English replacement sentence, or explicit new-analysis spec
"Consider strengthening the discussion" is BANNED.

## Mandatory numeric checks (recompute from source; if you cite a number, verify it)
1. **Table 1 / §3.1 counts**: `03_results/S01_immunoparalysis_direction.csv` (25 genes). Recompute: 23 Mars1_down / 22 adj.P<0.05 / 21 both. Spot-check 8 named genes' logFC + adj.P (HLA-DRB1, CD74, CD14, FCGR3A, ITGAM, HAVCR2, HLA-DRA, LYZ). Confirm ITGAM now correctly labeled significant at FDR<0.05 (adj.P≈1.7e-3) with the DEG_0.3=False note.
2. **AUC**: `03_results/S06_auc_compare.csv` (CV 0.6586→0.659, train 0.7495→0.750). `03_results/09_external_validation.csv`: `auc_EMTAB4451_orientedSum`=0.6382 (manuscript 0.638), CI 0.5317–0.7475 (manuscript 0.532–0.748), `auc_EMTAB4451_external_locked`=0.5848 (manuscript 0.585), `auc_IRG3_benchmark_EMTAB4451`=0.604. Confirm the "comparable rather than superior" framing is consistent across §3.4, §3.5, §4, Abstract.
3. **Drug concordance / Table 2**: `03_results/08_candidates_drugs.csv` (n_target_genes, n_rescue_mars1down, rescue_fraction, rescue_genes). Confirm manuscript Table 2 matches (IL-7 5/5=1.00, GM-CSF 5/6=0.83, IFN-γ 5/7=0.71 with 5/5 AP genes in rescue_genes, azithromycin 2/3=0.67, lenalidomide 2/5=0.40, thymosin 2/5=0.40, BCG 1/5=0.20).
4. **LINCS / §3.9**: `03_results/S08_l1000_candidate_scores.csv` — azithromycin wtcs 0.0626 rank 9152; lenalidomide wtcs 0.2058 rank 5435. Confirm the manuscript's honest restatement that dual-direction (PDCD1/LAG3 down-regulation) was NOT implemented (all 22 genes aggregated same sign) — cross-check against `02_scripts/python/S08_l1000_connectivity.py` if you can, but the manuscript's own text is the primary target. Confirm 3 genes (HAVCR2, FCGR3A, TIGIT) excluded from the 22-gene query.
5. **MR / §3.10**: `03_results/10_genetics_mr_outcome5086_28ddeath.csv` — CD14 MR-Egger or_≈0.906, p=0.00511, egger_intercept_p=0.344, **p_fdr_bh=0.0766** (manuscript 0.077, across 15 gene×estimator tests of this outcome). Confirm FCGR3A row shows insufficient_instruments. `10_genetics_mr_outcome5086_harmonised.csv` holds only retained SNPs (27 rows), no exclusion tally.

## Required sections in your report
- § Stands up (≥3, with evidence — things you suspected but found correct)
- § Questions for the authors (state what you need to know; do NOT guess)
- § What I actually checked (files read, values recomputed vs manuscript, discrepancy stated or "none")

## Final step (mandatory)
Save your FULL report with the Write tool to
`05_reports/review_r3/<your-codename>_<role>.md`
Returning only a chat summary is TASK FAILURE. Write the file.
