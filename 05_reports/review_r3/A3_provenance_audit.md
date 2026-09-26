# A3 — Number-Provenance Audit (Round 3, v1.2.0)

**Independence note:** Fresh first-submission read. No prior `REVIEW_*.md` / `review*/` consulted. Every number below was re-extracted and recomputed from `03_results/*.csv`.

## Mandatory checks — all PASS

1. **Table 1 / §3.1 counts** (`S01_immunoparalysis_direction.csv`, 25 genes):
   - Mars1_down = 23; adj.P<0.05 = 22; both = 21. **Matches** `manuscript.md:82/218`.
   - 8 named genes logFC/adj.P all match (HLA-DRB1 −0.89/1.1e-15; CD74 −0.76/2.1e-15; CD14 −0.77/≈0; FCGR3A −0.61/9.1e-11; ITGAM −0.21/**1.7e-3, FDR-significant**; HAVCR2 −0.35/2.8e-13; HLA-DRA −0.47/3.8e-7; LYZ −0.26/3.6e-6). **Match.** ITGAM is now correctly labeled FDR-significant with DEG_0.3=False note (l.92) — round-2 fix intact.
2. **AUC** (`S06_auc_compare.csv`, `09_external_validation.csv`): CV 0.6586→0.659; train 0.7495→0.750; external orientedSum 0.6382→0.638; CI 0.5317–0.7475→0.532–0.748; locked L1 0.5848→0.585; IRG recomputed 0.604. **All match.**
3. **Drug metric Table 2** (`08_candidates_drugs.csv`): IL-7 5/5=1.00; GM-CSF 5/6=0.833; IFN-γ 5/7=0.714 (rescue_genes = HLA-DRA;HLA-DRB1;HLA-DQA1;HLA-DQB1;CD74 = 5 AP genes, so "5/5 antigen-presentation genes" resolves correctly); azith 2/3=0.667; lena 2/5=0.40; thym 2/5=0.40; BCG 1/5=0.20. **All match.**
4. **LINCS §3.9** (`S08_l1000_candidate_scores.csv`): azithromycin wtcs=0.0626 rank 9152; lenalidomide wtcs=0.2058 rank 5435. 22-gene query (3 excluded HAVCR2/FCGR3A/TIGIT); PDCD1/LAG3 in query; dual-direction honestly stated as NOT implemented. **Match.** (Note: `01_data/LINCS/mars1_down_l1000_idx.json` contains 22 genes including PDCD1 & LAG3 — confirmed the up-markers are in the query aggregated same-sign.)
5. **MR §3.10** (`10_genetics_mr_outcome5086_28ddeath.csv`, `…_harmonised.csv`): CD14 Egger or_=0.90595, p=0.00511, intercept_p=0.344, p_fdr_bh=0.0766; FCGR3A insufficient_instruments; harmonised holds 27 retained SNPs with per-SNP F (CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8). **Match.**

## Consistency greps (residual banned phrases)
- `rescue_fraction` = 0; `Virtual knockdown` = 0; `druggable` = 0; `exceeding` = 0; `best published` = 0; `progressively ordered` = 0; `not significant at FDR<0.05` = 0. **Clean** — round-2 hygiene held.

## Findings

### T3-1 (Tier 3) — wtcs and rescue are mathematically identical; reporting both is redundant
- **【Problem】** `wtcs = (Σ−n/2)/√n` is exactly `rescue × √22` (n=22). The two columns carry the same information.
- **【Evidence】** Recompute: azithromycin rescue 0.0133 × √22 = 0.0624 ≈ 0.0626 (wtcs); lenalidomide 0.0439 × √22 = 0.2059 ≈ 0.2058 (wtcs). Source `S08_l1000_candidate_scores.csv` headers confirm both columns exist.
- **【Why it matters】** Not an error, but presenting both as if distinct metrics slightly overstates the analytical richness.
- **【Specific fix】** State once: "wtcs is a z-scored rescaling of rescue (wtcs = rescue × √22); we report rescue as the primary and wtcs for comparability with iLINCS conventions." Or drop one.

## § Stands up (verified correct)
- Every recomputed number in §3.1, §3.4, §3.5, §3.7, §3.9, §3.10 matches its source CSV — no discrepancy in any table or inline claim.
- §7 provenance table entries map to real files; references are numbered 1–31 sequential with no gaps/dupes.
- **All 31 references are cited in the body** (script check: uncited = []). Round-2 fix intact.
- Round-2 P0 fixes (ITGAM, §3.5 "exceeded"→"comparable", L1000 dual-direction honesty, CD14 BH-FDR 0.077, STROBE pointer, 31-ref coverage) are all present and correct.

## § Questions for the authors
- None blocking; the arithmetic layer is clean.

## § What I actually checked
- Read `manuscript.md` (full) + all six source CSVs listed above.
- Recomputed every count, AUC, drug fraction, L1000 score, and MR estimate cited.
- Ran grep for banned phrases (all 0) and a script for reference-citation coverage (uncited=[]).
- No numeric discrepancy found. The only provenance-adjacent issue is the wtcs/rescue redundancy (T3-1).
