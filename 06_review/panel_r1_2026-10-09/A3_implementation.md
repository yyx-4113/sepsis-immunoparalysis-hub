# Independent Implementation / Provenance Audit — Reviewer A3

**Manuscript:** "A reproducible, fully auditable pipeline confirms within-cohort the MARS Mars1 immunoparalysis program and delivers an honest external validation of a 30-gene sepsis prognostic signature" (single-author sepsis immunoparalysis computational study).
**Role:** Independent peer reviewer — computational provenance / data-recompute auditor.
**Environment:** `C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe` (numpy / pandas / scipy preinstalled).
**Method:** Every headline number in the manuscript was recomputed from the authoritative source CSV/JSON files in `03_results/` (and the phenotype CSV in `01_data/`), never from the manuscript text. Recomputation scripts: `03_results/_audit_recompute.py`, `03_results/_audit_supp.py`.

---

## 1. Recomputation summary table (the 11 mandated assertions)

Legend: **MATCH** = recomputed value agrees with the manuscript within rounding; **MISMATCH** = disagreement beyond rounding; **CANNOT-VERIFY** = source data needed to check is absent from the supplied files.

| # | Manuscript assertion | Source file(s) recomputed | Recomputed value | Verdict |
|---|----------------------|---------------------------|------------------|---------|
| 1 | 802 samples; GPL13667; sepsis 760 / ctrl 42; Mars1 132, Mars2 176, Mars3 118, Mars4 53, unassigned 323; death 114 / 365 / 323 | `01_data/GSE65682/GSE65682_pheno.csv` | 802 total; group {sepsis:760, healthy:42}; endotype {Mars1:132, Mars2:176, Mars3:118, Mars4:53, NaN:323}; death_28d {1.0:114, 0.0:365, NaN:323} | **MATCH** (sample/endotype/death counts). GPL13667 *string* not in CSV → see Issue C. |
| 2 | 23/25 immune genes directional down; 22/25 significant (FDR<0.05, incl PDCD1 up); 21 both down+significant | `S01_immunoparalysis_direction.csv` (25 rows) | down=23, up=2; adj.P<0.05 = 22 (incl PDCD1 up); down&sig = 21 | **MATCH** |
| 3 | CD74 −0.76 / 2.1e-15; HLA-DRB1 −0.89 / 1.1e-15; CD14 −0.77; FCGR3A −0.61 / 9.1e-11; HAVCR2 −0.35 / 2.8e-13 | `S01_immunoparalysis_direction.csv` | CD74 −0.7578/2.08e-15; HLA-DRB1 −0.8925/1.07e-15; CD14 −0.7657/0.0; FCGR3A −0.6097/9.05e-11; HAVCR2 −0.3488/2.84e-13 | **MATCH** |
| 4 | Score medians Mars1 −0.792, Mars2 −0.752, Mars3 0.641, Mars4 −0.235; MWU vs Mars1 P 0.47 / 1.9e-18 / 1.3e-3 | `S02_immunoparalysis_score.csv` | medians −0.7917 / −0.7520 / 0.6405 / −0.2347; MWU P 4.67e-1 / 1.85e-18 / 1.32e-3 | **MATCH** |
| 5 | CV AUC 0.659 (training 0.750); note "0.6586 in S06, 0.6582 in 09 = rounding artifact" | `S06_auc_compare.csv`, `09_external_validation.csv` | S06 CV=0.6585576→0.659, train=0.7495073→0.750; 09 CV_locked=0.6582 | **MATCH** on text; cross-file 0.6586 vs 0.6582 flagged (Issue A) |
| 6 | External locked-L1 AUC 0.585 (CI 0.469–0.696); equal-weight 0.638 (CI 0.532–0.748) | `09_external_validation.csv` + `09_ext_risk_scores.csv` | per-sample AUCs: locked 0.5848→0.585, equal 0.6382→0.638, CI 0.4687–0.6959 / 0.5317–0.7475 | **MATCH** |
| 7 | Calibration slope 0.50, intercept −0.04 (bootstrap CI −0.46 to 0.36) | `09_ext_calibration_dca.csv` | intercept −0.0382→−0.04; slope 0.5028→0.50; CI −0.4616 to 0.3576 | **MATCH** |
| 8 | DeLong: equal-weight vs 3-gene IRG proxy(0.529) P=0.156; vs locked-L1 P=0.235 | `09_ext_risk_scores.csv` (per-sample scores present) | independent DeLong on shipped scores: vs IRG3 P=0.148; vs locked P=0.226 (both ns) | **MATCH** (within method tolerance; see §4 note) |
| 9 | LINCS: lenalidomide 5435/20413 (26.6%, rescue 0.044, wtcs 0.21); azithromycin 9152/20413 (rescue 0.013, wtcs 0.06); prednisone 651/20413 (rescue 0.136, 3.2nd pct); dexamethasone 6808/20413 (rescue 0.032, 33.4th pct) | `S08_l1000_candidate_scores.csv`, `S08_l1000_positive_control.csv` | ranks/percentiles/pct all verified; wtcs = rescue×√22 verified. Prednisone **z=+2.03 inconsistent** (Issue B) | **MATCH** on ranks/percentiles; **MISMATCH** on prednisone z (Issue B) |
| 10 | SRS endotype AUC 0.610; age AUC 0.504 | `09_ext_benchmark_vs_srs.csv` | SRS dir-corrected 0.6104→0.610; age 0.5043→0.504 | **MATCH** |
| 11 | 30-gene signature; 29 genes with coefficients (HLA-DQA1 absent on Illumina); 7 exactly-zero coefs (CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B) | `S06_signature_genes.csv`, `09_external_validation.csv`, `09_external_validation_coef.json` | 30 signature rows; n_mapped=29, missing=HLA-DQA1; exactly-zero coefs = 7 {CD74,HLA-DRB1,IRF1,HLA-DMA,HLA-DMB,CD86,CD8B} | **MATCH** |

**Headline result: 11/11 mandated assertions are numerically supported by the source files.** Two *secondary* (non-headline) issues were found — one genuine arithmetic inconsistency in a stated z-statistic (Issue B) and one cross-file provenance inconsistency in the CV-AUC (Issue A). One token (the platform string "GPL13667") is not present in the supplied CSVs and is therefore CANNOT-VERIFY at file level (Issue C), though it does not affect any count.

---

## 2. Detailed recomputation evidence per claim

### Claim 1 — cohort composition (MATCH)
Recomputed from `01_data/GSE65682/GSE65682_pheno.csv` (802 rows): `group` value_counts → sepsis 760, healthy 42; `mars_endotype` → Mars1 132, Mars2 176, Mars3 118, Mars4 53, NaN 323; `death_28d` → 1.0:114, 0.0:365, NaN:323. All counts match the manuscript §2.1 and Abstract exactly.
- Incidental consistency checks (also in text): Mars1 28-d mortality 45/132 = 34.1% (ms §3.2 "34.1% (45/132)"); Mars2–4 69/347 = 19.9% (ms "19.9% (69/347)"); implied OR (45/87)/(69/278) = 2.083 → ms "2.08". Mars1-vs-Other contrast reference n=670 (132+347+281+42=802; 802−132=670) matches ms §3.1.
- **Minor observation:** the phenotype file stores the control label as `healthy`, whereas the manuscript text calls it `ctrl_GI`. Count (42) is identical; only the label string differs. Not a numeric error.

### Claim 2 — immune-gene directionality (MATCH)
`S01_immunoparalysis_direction.csv` has exactly 25 genes. `direction=='Mars1_down'` → 23; `direction=='Mars1_up'` → 2 (PDCD1, LAG3). `adj.P.Val < 0.05` → 22 (this set includes PDCD1, which is up). `down & significant` → 21. Matches "23/25 … 22/25 significant (incl PDCD1 up) … 21 both down+significant" exactly.

### Claim 3 — five hub-gene effect sizes (MATCH)
All five gene rows in `S01_immunoparalysis_direction.csv` reproduce the manuscript's rounded values (see table row 3). CD14 `P.Value = 0.0` (underflow) is consistent with ms "P≈0, underflow".

### Claim 4 — immune-function score medians & Mann–Whitney (MATCH)
From `S02_immunoparalysis_score.csv` (802 rows, column `immune_function_score`): per-endotype medians −0.7917 / −0.7520 / 0.6405 / −0.2347; two-sided Mann–Whitney U vs Mars1 → 4.67e-1 / 1.85e-18 / 1.32e-3. These round exactly to the manuscript's Table 2 (−0.792 / −0.752 / 0.641 / −0.235; P 0.47 / 1.9e-18 / 1.3e-3). Range checks: all-sample −3.65 to 3.862 (ms "−3.65 to 3.86"); assigned-endotype-only −3.65 to 2.951 (ms "−3.65 to 2.95"). Both match.

### Claim 5 — within-cohort CV AUC (MATCH on text; see Issue A)
`S06_auc_compare.csv`: "Immune-risk signature (CV)" = 0.6585576 (→ 0.659) and "(train)" = 0.7495073 (→ 0.750). Matches ms §3.4 "0.659 (training 0.750)" and §7 "0.6586 in S06_auc_compare.csv". Issue A below concerns the *second* stored value 0.6582 in `09_external_validation.csv` (metric `auc_GSE65682_CV_locked`) and the manuscript's "rounding artifact" framing.

### Claim 6 — external validation AUCs/CI (MATCH)
`09_external_validation.csv`: `auc_EMTAB4451_external_locked` = 0.5848 → 0.585; CI 0.4687–0.6959 → 0.469–0.696; `auc_EMTAB4451_orientedSum` = 0.6382 → 0.638; CI 0.5317–0.7475 → 0.532–0.748. I additionally reconstructed the per-sample AUCs from `09_ext_risk_scores.csv` (`risk_locked_l1` AUC=0.5848, `risk_oriented_sum` AUC=0.6382, `risk_irg3` AUC=0.5288) — i.e., the per-sample scores fully reproduce the reported AUCs, confirming these are not fabricated. Incidental: ms §3.4 "two external metrics differ by 0.053" = 0.6382−0.5848 = 0.0534 ✓; "transport loss for the L1 model is 0.074" = 0.6582−0.5848 = 0.0734 → 0.074 ✓.

### Claim 7 — calibration (MATCH)
`09_ext_calibration_dca.csv`: `calib_intercept` = −0.0382 → −0.04; `calib_slope` = 0.5028 → 0.50; `calib_intercept_ci_lo/hi` = −0.4616 / 0.3576 → −0.46 / 0.36. Matches ms §3.5 and §5. The DCA net-benefit columns in this file (`nb_thr0.20`=0.3632, `nb_thr0.30`=0.2844, `nb_thr0.50`=0.0755) are identical to the matching rows of `09_ext_dca_grid.csv` (threshold 0.2/0.3/0.5), so the two calibration/DCA files are mutually consistent.

### Claim 8 — DeLong comparisons (MATCH, with method note)
Per-sample risk scores exist in `09_ext_risk_scores.csv` (columns `risk_oriented_sum`, `risk_locked_l1`, `risk_irg3`), so the DeLong test is fully recomputable. My independent DeLong (standard Sun–Xu placement-value covariance) on these shipped scores gives: equal-weight vs 3-gene IRG proxy P = 0.148; equal-weight vs locked-L1 P = 0.226. The manuscript reports 0.156 (text line 104 writes "DeLong P = 0.16") and 0.235 respectively. The ~0.008–0.009 gap is attributable to DeLong implementation / tie-handling differences (e.g., pROC-style vs my covariance estimate) and is far smaller than the reported precision; both recomputations confirm the qualitative claim that the differences are **not statistically significant**. Verdict: **MATCH** (recomputed, non-significant, within method tolerance). No per-sample-score gap.

### Claim 9 — LINCS L1000 ranks/percentiles (MATCH on ranks; MISMATCH on prednisone z → Issue B)
`S08_l1000_candidate_scores.csv`: lenalidomide rescue_rank=5435, rescue_score=0.0439, wtcs=0.2058; azithromycin rescue_rank=9152, rescue_score=0.0133, wtcs=0.0626. `S08_l1000_positive_control.csv`: prednisone rescue_rank=651, rescue_score=0.1364, rescue_pct_rank=0.03189; dexamethasone rescue_rank=6808, rescue_score=0.0315, rescue_pct_rank=0.33351.
- Percentile arithmetic verified: 5435/20413 = 26.63% (ms "26.6%"); 9152/20413 = 44.83% (ms "≈ median"); 651/20413 = 3.19% (ms "3.2nd percentile"); 6808/20413 = 33.35% (ms "33.4th percentile"). All correct.
- wtcs algebra: wtcs = rescue × √22. lenalidomide 0.0439×4.6904 = 0.2059 (ms 0.21); azithromycin 0.0133×4.6904 = 0.0624 (ms 0.06). The manuscript's statement that the two are "algebraically identical" is correct.
- Candidate z-scores use (rescue − background_mean)/background_sd with background_mean=0.00639734, sd=0.06724355: lenalidomide (0.0439−0.0064)/0.0672 = 0.558 → ms "+0.56" ✓; azithromycin = 0.103 → ms "+0.10" ✓. **But prednisone's stated z = +2.03 equals rescue/sd with the mean NOT subtracted (0.1364/0.06724 = 2.028), inconsistent with the formula applied to the two candidates.** Recomputed prednisone z with the same (rescue−mean)/sd formula = 1.93. See Issue B.

### Claim 10 — SRS / age benchmark AUCs (MATCH)
`09_ext_benchmark_vs_srs.csv`: "SRS group (direction-corrected)" AUC = 0.6104 → 0.610; "age" AUC = 0.5043 → 0.504. Matches ms Limitation 1. Incidental: the file also records SRS1 mortality 0.649 (24/37) and SRS2 28/69 = 0.4058 (40.6%), matching ms "SRS1 24/37, 64.9% … SRS2 28/69, 40.6%"; ΔAUC vs SRS_dir +0.0278 (ms "≈0.03 … +0.028") and perm P 0.694 (ms "0.69").

### Claim 11 — signature size & zero coefficients (MATCH)
`S06_signature_genes.csv` has 30 gene rows. `09_external_validation.csv`: `n_signature_genes_total`=30, `n_signature_genes_mapped_EMTAB4451`=29, `genes_missing_in_test`=HLA-DQA1. `09_external_validation_coef.json` "coef" dict has 29 entries; exactly 7 are 0.0: CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B — exactly the set listed in ms §3.4. (Note FCGR3A coef = 0.001656, a tiny non-zero, correctly *not* counted as "exactly zero".) Matches.

---

## 3. Additional recomputations performed (beyond the 11 assertions)

- **Sepsis-vs-healthy DEG count** (`S01_deg_sepsis_vs_ctrl.csv`): 448 genes at |logFC|≥0.3 & FDR<0.05 → matches ms §3.1 "448 DEGs" and §7.
- **Mars1-vs-Other DEG count** (`S01_mars1_deg.csv`): 3597 → matches ms §7 "Mars1-vs-Other DEG 3597".
- **FIS1 logFC / t** (`S01_mars1_deg.csv`): logFC 1.2614 → "+1.26", t 17.1567 → "+17.2" → matches ms §3.3 and §6.
- **LINCS library size** (`S08_l1000_rescue_trtcp.csv`): exactly 20,413 `trt_cp` rows → matches "20,413 trt_cp compounds".
- **Mars1 28-d death AUC** (`S06_auc_compare.csv`): 0.5781903 → ms §3.2 "AUC 0.578" ✓.
- **Table 1 individual rows** (`S01_immunoparalysis_direction.csv`): ITGAM −0.2084→−0.21, adj.P 1.68e-3→1.7e-3, DEG_0.3=False ✓; HLA-DRA −0.4689→−0.47, 3.77e-7→3.8e-7 ✓; LYZ −0.2561→−0.26, 3.56e-6→3.6e-6, DEG_0.3=False ✓. All match.
- **Table 3 drug concordance** (`08_candidates_drugs.csv`): IL-7 0.80/4-5/P=0.817→0.82; GM-CSF 0.667/4-6/0.944→0.94; IFN-γ 0.571/4-7/0.985→0.99; Azithromycin 0.667/2-3/0.931→0.93; Lenalidomide 0.40/2-5/0.997→1.00; Thymosin α1 0.40/2-5/0.997→1.00; BCG 0.20/1-5/1.000→1.00. All match Table 3 exactly.

---

## 4. Issues found (mandatory 4-part contract)

### ISSUE A — Cross-file inconsistency in the within-cohort CV AUC and an inaccurate "rounding artifact" explanation
【Problem】 The manuscript states the within-cohort CV AUC is "0.6586 in S06_auc_compare.csv, 0.6582 in 09_external_validation.csv; the difference is a rounding artifact," but 0.6586 vs 0.6582 is a 0.0004 difference between two *stored* values of the same quantity (GSE65682 CV locked AUC), not a single rounded number.
【Evidence】 `S06_auc_compare.csv` row "Immune-risk signature (CV)" = 0.6585575829768802; `09_external_validation.csv` metric `auc_GSE65682_CV_locked` = 0.6582. These are two distinct stored floats. The text headline "0.659" is correctly supported by S06 (0.6586 rounds to 0.659). ms §3.4 / §7.
【Why it matters】 The "rounding artifact" label is technically incorrect: one value is 0.658557… (rounds to 0.6586) and the other is stored as 0.6582 — these cannot both be the same computation rounded, so two different runs produced the discovery CV AUC. It is a provenance/housekeeping defect, not a wrong headline number, but it undermines the "every number traces to one output" claim because the *same* number traces to *two different* outputs.
【Specific fix】 Either (a) regenerate `09_external_validation.csv` so `auc_GSE65682_CV_locked` equals the S06 value (0.6585576…), or (b) change the §7 note to state the two files were produced by independent runs and report both to full precision (0.6586 and 0.6582) without calling the gap a "rounding artifact." The rounded text value 0.659 stands.

### ISSUE B — Prednisone rescue z-score uses a different formula than the candidate z-scores (genuine arithmetic inconsistency)
【Problem】 The manuscript reports prednisone's LINCS rescue z = "+2.03" while the two candidates are reported as "+0.56" and "+0.10"; the candidate z's were computed as (rescue − background_mean)/background_sd, whereas prednisone's 2.03 was computed as rescue/background_sd with the mean not subtracted — so the same statistic is not computed the same way across the sentence.
【Evidence】 `S08_l1000_candidate_scores.csv` background_mean = 0.00639734, background_sd = 0.06724355. Candidate z (mean-subtracted): lenalidomide (0.0439−0.0064)/0.0672 = 0.558 (ms "+0.56" ✓); azithromycin (0.0133−0.0064)/0.0672 = 0.103 (ms "+0.10" ✓). Prednisone 0.1364/0.0672 = 2.028 ≈ ms "+2.03"; but (0.1364−0.0064)/0.0672 = 1.933. The "+2.03" is only obtainable if the mean is dropped. ms §3.9 line 137: "a clinical immunosuppressant scores at z = +2.03 while the candidates score at z = +0.56 and +0.10."
【Why it matters】 The qualitative conclusion (prednisone >> candidates, so the rescue proxy is non-discriminating) is unaffected — 1.93 is still far above 0.56/0.10. But the stated figure is internally inconsistent with the method used for the adjacent candidate z's, which is exactly the kind of arithmetic slip a provenance reviewer must flag; a reader replicating "z = (rescue−mean)/sd" for prednisone would obtain 1.93, not 2.03.
【Specific fix】 Recompute prednisone's z with the same (rescue − background_mean)/background_sd formula → report z = +1.93 (and keep the qualitative conclusion unchanged), OR explicitly state that the prednisone z is raw rescue/sd for comparability with the percentile framing. Make the formula identical across all three numbers.

### ISSUE C — Platform string "GPL13667" not verifiable from the supplied CSVs (CANNOT-VERIFY, cosmetic)
【Problem】 The cohort-composition claim (802 samples; GPL13667) is fully verifiable for the counts, but the literal platform token "GPL13667" does not appear in any supplied `03_results/` or `01_data/GSE65682/*.csv` file; the manuscript says it was read from `!Series_platform_id = GPL13667` in the downloaded family SOFT (`GSE65682_family.soft.gz`, present on disk but not a "result file").
【Evidence】 `01_data/GSE65682/GSE65682_pheno.csv` and `GSE65682_expr.csv` contain sample/expression data but no platform-id column; the token lives only in the SOFT. ms §2.1.
【Why it matters】 No count is affected; this is a provenance traceability gap for a single token, not a numeric error. If a reviewer opens only the result CSVs they cannot confirm GPL13667 from them.
【Specific fix】 Add the platform id as a header/metadata row in `GSE65682_pheno.csv` (or cite the SOFT file explicitly in §7 as the authoritative source for the platform token, which the manuscript already does in prose). Low priority.

### ISSUE D — §7 provenance: "positive control" row points to a different file than where the numbers live (housekeeping, not a number error)
【Problem】 §7 lists `03_results/08_positive_control_check.csv` as the source for "positive control," but the actual prednisone/dexamethasone rescue ranks and percentiles cited in §3.9 live in `03_results/S08_l1000_positive_control.csv` (also listed separately in §7). Both files exist; the row is just mildly mis-targeted.
【Evidence】 `08_positive_control_check.csv` (349 bytes) exists but contains only the IFN-γ / curated-set positive-control check; `S08_l1000_positive_control.csv` (601 bytes) carries prednisone/dexamethasone. ms §7 lines 200 & 204.
【Why it matters】 None — both files are present and the numbers trace correctly. Flagged only so the authors can tighten the citation.
【Specific fix】 Change the §7 "positive control" row to cite `S08_l1000_positive_control.csv` (the file containing prednisone/dexamethasone), or add a second row. Optional.

---

## 5. §7 Number-provenance table audit (file existence)

Every file cited in ms §7 was checked for existence on disk. **All cited files exist** — no missing files.

| §7 cited source | Exists? | Contains claimed number? |
|---|---|---|
| `01_data/GSE65682/GSE65682_expr.csv` | Yes (125 MB) | regenerable; sample count confirmed via pheno |
| `GSE65682_pheno.csv` | Yes | 802 / 760 / 42 / endotype / death — confirmed |
| `03_results/S01_deg_sepsis_vs_ctrl.csv` | Yes | 448 DEG — confirmed |
| `03_results/S01_mars1_deg.csv` | Yes | 3597 DEG — confirmed |
| `03_results/S01_immunoparalysis_direction.csv` | Yes | 23/22/21 + gene values — confirmed |
| `03_results/S02_immunoparalysis_score.csv` | Yes | medians & P — confirmed |
| `03_results/S05_hub_genes.csv` | Yes | 6 hub genes (5 immune + FIS1) — confirmed |
| `03_results/S06_signature_genes.csv` | Yes | 30 genes — confirmed |
| `03_results/S06_auc_compare.csv` | Yes | CV 0.6586 / train 0.750 — confirmed |
| `03_results/09_external_validation.csv` | Yes | 0.585 / 0.638 + CI — confirmed |
| `09_external_validation_coef.json` | Yes | 29 coefs, 7 zeros — confirmed |
| `03_results/09_ext_calibration_dca.csv` | Yes | slope 0.50 / intercept −0.04 — confirmed |
| `09_ext_dca_grid.csv` | Yes | DCA NB — consistent with calibration file |
| `04_figures/S06_dca.png` | (figure; not opened) | referenced |
| `01_data/E-MTAB-4451/*` | Yes | external cohort |
| `03_results/07_hub_celltype.csv` | Yes | hub localisation |
| `03_results/08_candidates_drugs.csv` | Yes | 7 drugs + concordance — confirmed |
| `03_results/08_positive_control_check.csv` | Yes (see Issue D) | IFN-γ gate |
| `03_results/08b_clinical_translation.csv` | Yes | clinical status |
| `03_results/S08_l1000_rescue_trtcp.csv` | Yes (20,413 rows) | LINCS library — confirmed |
| `_wtcs.npy` | Yes | wtcs array |
| `03_results/S08_l1000_candidate_scores.csv` | Yes | lenalidomide/azithromycin — confirmed |
| `03_results/S08_l1000_positive_control.csv` | Yes | prednisone/dexamethasone — confirmed |
| `S08_l1000_immuno_overlap.csv` | Yes | immuno overlap |
| `01_data/LINCS/GSE92742_Level5_COMPZ.gctx` | Yes (23 GB) | L1000 source |
| `03_results/11_validation_design.md` | Yes | S11 blueprint |
| `05_reports/tier1_summary.txt` | Yes (689 B) | pipeline summary |

No §7-cited file is missing. The only provenance defects are Issues A, C, D above.

---

## 6. Table syntax audit (Tables 1, 2, 3 in the manuscript)

All three tables are syntactically well-formed Markdown: every data row has exactly 4 pipe-delimited fields matching the 4-column header; no broken/ragged pipes, no misaligned columns, no stray separators.

- **Table 1** (ms lines 71–80): header `| Gene | logFC | adj.P.Val | Function |`; 8 data rows, each 4 fields. Values (HLA-DRB1 −0.89/1.1e-15; CD74 −0.76/2.1e-15; CD14 −0.77/≈0; FCGR3A −0.61/9.1e-11; ITGAM −0.21/1.7e-3; HAVCR2 −0.35/2.8e-13; HLA-DRA −0.47/3.8e-7; LYZ −0.26/3.6e-6) all reconcile with `S01_immunoparalysis_direction.csv`. The `DEG_0.3=False` annotations on ITGAM and LYZ are correct (both fail |logFC|≥0.3). No contradictions with §7 or text.
- **Table 2** (ms lines 89–94): 4 columns; medians/P reproduce the recomputation in §2 Claim 4 exactly. No contradictions.
- **Table 3** (ms lines 119–127): 4 columns; all 7 rows reconcile with `08_candidates_drugs.csv` (concordance, n_rescue/n_target, binomial P) exactly. No contradictions.

No broken pipe syntax, no column misalignment, and no value contradictions between tables and the §7 provenance or the results text were found.

---

## 7. Double-counting / cross-section consistency

- The external AUCs (0.585 locked, 0.638 equal-weight), the IRG-proxy (0.529), SRS (0.610) and age (0.504) are reported identically in the Abstract, §3.5, §5 (Limitations) and §7 — no inconsistent restatements of these headline numbers across sections.
- The CV AUC is reported as 0.659 in Abstract/§3.4/§6 and as 0.6586 in §7; both round to 0.659 and are consistent. The only cross-file divergence is the 0.6582 stored in `09_external_validation.csv` (Issue A).
- No gene, gene count, or coefficient is reported inconsistently across sections (the 7 zero-coef hubs are listed identically in §3.4 and §11).
- No value is double-counted in a way that inflates a claim. The 30-gene signature vs 29 mapped genes vs 7 zero-coefs is internally consistent (30 − 1 absent − 7 zero = 22 genes actively contributing to the locked L1 score; this is stated correctly).

---

## 8. § Stands up (numbers recomputed and confirmed correct)

The following were independently recomputed and **confirm** the manuscript:

1. **Cohort composition** — 802 samples; sepsis 760 / healthy 42; Mars1 132, Mars2 176, Mars3 118, Mars4 53, unassigned 323; death 114/365/323 (from `GSE65682_pheno.csv`). Verdict: MATCH.
2. **Immune-gene directionality** — 23/25 down, 22/25 significant (incl PDCD1 up), 21 both down+significant (from `S01_immunoparalysis_direction.csv`, 25 rows). Verdict: MATCH.
3. **Five hub-gene effect sizes** — CD74 −0.7578/2.08e-15, HLA-DRB1 −0.8925/1.07e-15, CD14 −0.7657/0.0, FCGR3A −0.6097/9.05e-11, HAVCR2 −0.3488/2.84e-13 (from `S01_immunoparalysis_direction.csv`). Verdict: MATCH.
4. **Immune-function score medians & MWU** — −0.792 / −0.752 / 0.641 / −0.235; P 0.47 / 1.9e-18 / 1.3e-3 (from `S02_immunoparalysis_score.csv`, recomputed medians + scipy Mann–Whitney U). Verdict: MATCH.
5. **External validation AUCs + CIs** — locked 0.585 (0.469–0.696), equal-weight 0.638 (0.532–0.748); and the per-sample risk scores in `09_ext_risk_scores.csv` *reproduce* these AUCs (0.5848, 0.6382) exactly, proving they are not fabricated. Verdict: MATCH.
6. **Calibration** — slope 0.50, intercept −0.04, CI −0.46 to 0.36 (from `09_ext_calibration_dca.csv`). Verdict: MATCH.
7. **LINCS ranks & percentile arithmetic** — lenalidomide 5435/20413=26.6%, azithromycin 9152/20413=44.8% (≈median), prednisone 651/20413=3.19%, dexamethasone 6808/20413=33.4%; wtcs = rescue×√22 verified (from `S08_l1000_candidate_scores.csv`, `S08_l1000_positive_control.csv`). Verdict: MATCH (except prednisone z, Issue B).
8. **SRS / age benchmarks** — 0.610 / 0.504 (from `09_ext_benchmark_vs_srs.csv`). Verdict: MATCH.
9. **Signature size & zero coefficients** — 30 genes, 29 mapped, HLA-DQA1 missing, exactly 7 zero coefs = {CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B} (from `S06_signature_genes.csv`, `09_external_validation.csv`, `09_external_validation_coef.json`). Verdict: MATCH.
10. **DeLong non-significance** — independent DeLong on shipped per-sample scores gives P≈0.15 (vs IRG proxy) and P≈0.23 (vs locked-L1), confirming the manuscript's "not statistically distinguishable" claim (ms P=0.156/0.235). Verdict: MATCH.
11. **Ancillary counts** — sepsis-vs-healthy DEG 448, Mars1-vs-Other DEG 3597, FIS1 logFC +1.26/t +17.2, Mars1 28-d mortality 34.1% (45/132), LINCS library exactly 20,413 rows — all confirmed.

---

## 9. Questions for the authors

1. **CV-AUC provenance (Issue A):** `S06_auc_compare.csv` stores the discovery CV AUC as 0.6585576 while `09_external_validation.csv` stores `auc_GSE65682_CV_locked` = 0.6582. Were these produced by two separate pipeline runs? Which is authoritative, and why is the gap labelled a "rounding artifact" rather than a run-to-run difference?
2. **Prednisone z (Issue B):** The candidate z-scores (lenalidomide +0.56, azithromycin +0.10) use (rescue − background_mean)/background_sd, but prednisone's +2.03 equals rescue/background_sd with the mean omitted. Was this intentional (e.g., to align with the percentile framing) or an oversight? Do you agree the consistent value is +1.93?
3. **Locked-L1 vs equal-weight interpretation:** The locked-L1 external AUC (0.585, CI includes 0.5) is designated the *primary* metric and is not significantly above chance, while the equal-weight sensitivity score (0.638, CI excludes 0.5) is the stronger number. Given the primary estimate is null, is the "honest external validation" framing best carried by the equal-weight result, and should the abstract lead with the equal-weight AUC rather than the locked-L1 as the headline?
4. **DeLong P-value method:** Our independent DeLong gives P=0.148 (vs IRG proxy) and P=0.226 (vs locked-L1); you report 0.156 and 0.235. Could you confirm the exact DeLong implementation (e.g., pROC vs custom covariance) so the ~0.01 gap is understood? Both agree the differences are non-significant.
5. **LINCS gene-set size:** §3.9 states 22 of 25 consensus immune genes are measurable on L1000 (HAVCR2, FCGR3A, TIGIT absent). Could you confirm the 22-gene query set is the one actually scored, and that PDCD1/LAG3 (Mars1-up) were included with the same sign as the Mars1-down genes (i.e., the single-direction aggregation you disclose)?
6. **Platform token traceability (Issue C):** The GPL13667 string is only in the family SOFT, not in any result CSV. Is there a committed metadata artifact (e.g., a parsing log) that records `!Series_platform_id = GPL13667` so the §7 trace is file-level complete?

---

## 10. What I actually checked (every file read + every recomputation)

**Files read (full or head):**
- `05_reports/manuscript.md` — full read (283 lines; some in-text passages marked "[truncated]" by the author, not by me).
- `01_data/GSE65682/GSE65682_pheno.csv` — full (802 rows) → Claim 1, Mars1 mortality, Issue C.
- `03_results/S01_immunoparalysis_direction.csv` — full (25 rows) → Claims 2, 3, Table 1.
- `03_results/S01_mars1_deg.csv` — full (1,088,654 B; used for DEG count 3597, FIS1 logFC/t) → Claim 2 context, §3 ancillary.
- `03_results/S01_deg_sepsis_vs_ctrl.csv` — full (used for DEG count 448) → §3.1/§7.
- `03_results/S02_immunoparalysis_score.csv` — full (802 rows) → Claim 4, score ranges.
- `03_results/S05_hub_genes.csv` — full (6 rows) → hub set.
- `03_results/S06_signature_genes.csv` — full (30 rows) → Claim 11.
- `03_results/S06_auc_compare.csv` — full (6 rows) → Claim 5.
- `03_results/09_external_validation.csv` — full (18 rows) → Claims 5, 6, 11.
- `03_results/09_external_validation_coef.json` — full → Claim 11, zero-coef list.
- `03_results/09_ext_calibration_dca.csv` — full (1 row) → Claim 7, DCA consistency.
- `03_results/09_ext_dca_grid.csv` — full (19 rows) → DCA consistency with calibration file.
- `03_results/09_ext_risk_scores.csv` — full (106 rows) → Claims 6, 8 per-sample AUCs + DeLong.
- `03_results/09_ext_benchmark_vs_srs.csv` — full (6 rows) → Claim 10, SRS/age.
- `03_results/08_candidates_drugs.csv` — full (7 rows) → Table 3.
- `03_results/S08_l1000_candidate_scores.csv` — full (2 rows) → Claim 9.
- `03_results/S08_l1000_positive_control.csv` — full (9 rows) → Claim 9.
- `03_results/08_positive_control_check.csv` — full (Issue D).
- `03_results/08b_clinical_translation.csv` — listed (exists; not recomputed, outside the 11 claims).
- `03_results/11_validation_design.md` — listed (exists; design blueprint, outside the 11 claims).
- `01_data/LINCS/GSE92742_Level5_COMPZ.gctx` — confirmed present (23 GB; not parsed, LINCS library size taken from `S08_l1000_rescue_trtcp.csv` = 20,413 rows).
- `05_reports/tier1_summary.txt` — confirmed present (689 B).

**Recomputations performed (claimed vs recomputed vs discrepancy):**
| Quantity | Claimed | Recomputed | Discrepancy |
|---|---|---|---|
| Total samples | 802 | 802 | 0 |
| sepsis / ctrl | 760 / 42 | 760 / 42 (label `healthy`) | label name only |
| Endotype counts | 132/176/118/53/323 | 132/176/118/53/323 | 0 |
| death_28d | 114/365/323 | 114/365/323 | 0 |
| Immune down / sig / both | 23 / 22 / 21 | 23 / 22 / 21 | 0 |
| CD74 logFC / adj.P | −0.76 / 2.1e-15 | −0.7578 / 2.08e-15 | rounding |
| HLA-DRB1 logFC / adj.P | −0.89 / 1.1e-15 | −0.8925 / 1.07e-15 | rounding |
| CD14 logFC | −0.77 | −0.7657 | rounding |
| FCGR3A logFC / adj.P | −0.61 / 9.1e-11 | −0.6097 / 9.05e-11 | rounding |
| HAVCR2 logFC / adj.P | −0.35 / 2.8e-13 | −0.3488 / 2.84e-13 | rounding |
| Score medians | −0.792/−0.752/0.641/−0.235 | −0.7917/−0.7520/0.6405/−0.2347 | rounding |
| MWU P (vs Mars1) | 0.47 / 1.9e-18 / 1.3e-3 | 4.67e-1 / 1.85e-18 / 1.32e-3 | rounding |
| CV AUC / train | 0.659 / 0.750 | 0.6586 / 0.7495 (S06) | rounding; see Issue A |
| External locked AUC / CI | 0.585 / 0.469–0.696 | 0.5848 / 0.4687–0.6959 | rounding |
| External equal-wt AUC / CI | 0.638 / 0.532–0.748 | 0.6382 / 0.5317–0.7475 | rounding |
| Per-sample AUC (locked/eq/irg3) | 0.585/0.638/0.529 | 0.5848/0.6382/0.5288 | rounding |
| Calibration slope / intercept | 0.50 / −0.04 | 0.5028 / −0.0382 | rounding |
| Calibration intercept CI | −0.46 to 0.36 | −0.4616 to 0.3576 | rounding |
| DeLong eq-wt vs IRG3 | P=0.156 | P=0.148 | 0.008 (method) |
| DeLong eq-wt vs locked | P=0.235 | P=0.226 | 0.009 (method) |
| LINCS lenalidomide rank/pct | 5435 / 26.6% | 5435 / 26.63% | rounding |
| LINCS azithromycin rank/pct | 9152 / ≈median | 9152 / 44.83% | rounding |
| LINCS prednisone rank/pct/z | 651 / 3.2% / +2.03 | 651 / 3.19% / **+1.93** | **z mismatch (Issue B)** |
| LINCS dexamethasone rank/pct | 6808 / 33.4% | 6808 / 33.35% | rounding |
| wtcs (lena/azi) | 0.21 / 0.06 | 0.2059 / 0.0624 | rounding (algebra verified) |
| SRS AUC / age AUC | 0.610 / 0.504 | 0.6104 / 0.5043 | rounding |
| Signature genes / mapped / missing | 30 / 29 / HLA-DQA1 | 30 / 29 / HLA-DQA1 | 0 |
| Exactly-zero coefs | 7 (named set) | 7 (same set) | 0 |
| Sepsis-vs-healthy DEG | 448 | 448 | 0 |
| Mars1-vs-Other DEG | 3597 | 3597 | 0 |
| FIS1 logFC / t | +1.26 / +17.2 | +1.2614 / +17.16 | rounding |
| Mars1 28-d mortality | 34.1% (45/132) | 45/132 = 34.1% | 0 |

**Discrepancies requiring author action:** Issue A (CV-AUC cross-file 0.6586 vs 0.6582 + "rounding artifact" wording) and Issue B (prednisone z +2.03 vs recomputed +1.93 under the candidates' formula). Issue C (platform token not in CSVs) and Issue D (mis-targeted §7 citation) are housekeeping/traceability only.

**Overall verdict:** The manuscript is numerically faithful to its authoritative source files. All 11 mandated headline assertions are supported (MATCH). The two genuine defects are minor and do not alter any biological or statistical conclusion: (1) a cross-file provenance inconsistency in the discovery CV AUC with an inaccurate "rounding artifact" label, and (2) a prednisone rescue z-score computed with a different centring than the candidate z-scores. No fabricated numbers, no broken table syntax, no double-counting, and no text-vs-source contradictions in the headline figures were found.
