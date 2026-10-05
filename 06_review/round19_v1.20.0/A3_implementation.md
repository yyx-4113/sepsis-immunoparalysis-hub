# A3 — Implementation / Provenance & Recompute Audit
**Manuscript:** "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and externally evaluates a 30-gene sepsis prognostic signature"
**Repo:** github.com/yyx-4113/sepsis-immunoparalysis-hub · tag **v1.20.0** · target BMC Medical Genomics
**Auditor role:** A3 (Implementation = provenance / recomputation). Every number below was recomputed by me from the raw/result files; I did **not** trust the manuscript's restated values.

---

## 1. Summary verdict
I independently recomputed all 25 headline numbers the panel asked me to check, plus ~15 secondary derived numbers. **24 of the 25 headline numbers reproduce exactly (or to the stated rounding) from the cited source files.** One "headline number" supplied to me in the panel brief — *"second cohort AUC 0.659 (n=52)"* — **does not exist as a single claim in the manuscript**; the manuscript correctly separates a within-cohort GSE65682 CV AUC of 0.659 from a single external cohort (E-MTAB-4451, n=106, **52 deaths**) at AUC 0.638. That brief wording is a Tier-0 misstatement (it would, if believed, overstate generalizability by implying two independent external replications). The manuscript text itself is clean. **No MR residue, no v1.19.1 drift, correct Zenodo DOI, no broken table syntax.** Three minor housekeeping items (CV-value harmonization, orphan MR result files, brief's `S09_` filename prefix) are flagged as Tier-1/info.

**No Tier-1 number discrepancy was found in the manuscript's own reported values.** The audit therefore largely *confirms* the manuscript's arithmetic and provenance, and I say so explicitly in §6 (Stands up).

---

## 2. Master per-number cross-check table

| # | Claim (manuscript) | Source file | Recomputed value | Match? | Tier |
|---|--------------------|-------------|------------------|--------|------|
| 1 | 802 samples / 760 sepsis / 42 control | `01_data/GSE65682/GSE65682_pheno.csv` | 802 total; 760 `sepsis`; 42 `healthy` | ✓ (label "healthy", see T1-4) | — |
| 2 | 5 immune hubs Mars1-down + FIS1 Mars1-up | `03_results/S01_mars1_deg.csv`, `S05_hub_genes.csv` | CD74 −0.758, HLA-DQA1 −0.530, CD14 −0.766, FCGR3A −0.610, HAVCR2 −0.349; FIS1 **+1.261** | ✓ | — |
| 3 | FIS1 logFC ≈ +1.26 | `S01_mars1_deg.csv` | +1.261433 | ✓ | — |
| 4 | 30-gene signature | `03_results/S06_signature_genes.csv` | 30 rows | ✓ | — |
| 5 | External AUC 0.638 (E-MTAB-4451, n=106) | `03_results/09_external_validation.csv` | orientedSum **0.6382**; n=106 | ✓ | — |
| 6 | External cohort 52 deaths | `09_external_validation.csv` | n_deaths=**52** | ✓ | — |
| 7 | Locked L1 AUC 0.585 | `09_external_validation.csv` | external_locked **0.5848** | ✓ | — |
| 8 | Within-cohort CV AUC 0.659 | `S06_auc_compare.csv` / `09_external_validation.csv` | 0.6586 / 0.6582 (both →0.659) | ✓ | T1-1 |
| 9 | IRG-3 baseline AUC 0.5288 (ms: "0.529") | `09_external_validation.csv` | **0.5288** | ✓ (ms rounds to 0.529) | — |
| 10 | Mars1 score median ≈ −0.7917 | `03_results/S02_immunoparalysis_score.csv` | **−0.791668** (ms Table 2: −0.792) | ✓ | — |
| 11 | DCA: model NB > treat-all from thr 0.30 | `03_results/09_ext_dca_grid.csv` | thr0.30: model 0.2844 > treat-all 0.2722 | ✓ | — |
| 12 | DCA at 0.80 model DIVERGES from treat-all | `09_ext_dca_grid.csv` | thr0.80: model 0.0, treat-all −1.5472 (gap widens) | ✓ | — |
| 13 | Calibration slope 0.50 (over-confident) | `03_results/09_ext_calibration_dca.csv` | **0.5028** | ✓ | — |
| 14 | Calibration intercept −0.04 (CI −0.43–0.35) | `09_ext_calibration_dca.csv` | −0.0382 (CI −0.430–0.354) | ✓ | — |
| 15 | P(slope=1)=0.016 | `09_ext_calibration_dca.csv` | p=**0.01575** | ✓ | — |
| 16 | Mars1-vs-Other DEG 3597 (|logFC|≥0.3) | `S01_mars1_deg.csv` | DEG_0.3 True = **3597** | ✓ | — |
| 17 | sepsis-vs-healthy DEG 448 | `S01_deg_sepsis_vs_ctrl.csv` | DEG_0.3 True = **448** | ✓ | — |
| 18 | 23/25 immune genes down; 22/25 sig; 21 both | `S01_immunoparalysis_direction.csv` | 23 down; 22 sig(FDR<0.05); 21 both | ✓ | — |
| 19 | Hub cell types: CD14 r=0.77, FCGR3A 0.49, CD74→DC 0.69, HAVCR2 0.30, HLA-DQA1→B 0.68 | `07_hub_celltype.csv` | 0.773/0.491/0.690/0.298/0.681 | ✓ | — |
| 20 | L1000 lenalidomide 5435/20413 (26.6%), rescue 0.044, wtcs 0.21 | `S08_l1000_candidate_scores.csv` | rank 5435, 26.6%, 0.0439, 0.2058 | ✓ | — |
| 21 | L1000 azithromycin 9152/20413 (≈median), rescue 0.013, wtcs 0.06 | `S08_l1000_candidate_scores.csv` | rank 9152, 44.8%, 0.0133, 0.0626 | ✓ | — |
| 22 | L1000 z +0.56 / +0.10; empirical P 0.27 / 0.45 | `S08_l1000_candidate_scores.csv` | 0.558/0.103; 0.266/0.449 | ✓ | — |
| 23 | SRS benchmark AUC 0.610; SRS1 24/37=64.9%; SRS2 28/69=40.6%; age 0.504; ΔAUC +0.028; perm P 0.69 | `09_ext_benchmark_vs_srs.csv` | 0.6104; 24/37=0.649; 28/69=0.406; age 0.5043; +0.0278; P 0.694 | ✓ | — |
| 24 | Drug table 7 rows (IL-7 0.80 … BCG 0.20) | `08_candidates_drugs.csv` | exact match (0.80/0.67/0.57/0.67/0.40/0.40/0.20; binom P 0.82/0.94/0.99/0.93/1.00/1.00/1.00) | ✓ | — |
| 25 | Mars1 28-d mortality 34.1% (45/132) vs Mars2–4 19.9% (69/347) | `GSE65682_pheno.csv` | 45/132=34.1%; 69/347=19.9% | ✓ | — |
| 26 | FIS1 degree rank 12 (degree 64.26) | `S03_hub_degree.csv` | rank 12 (0-indexed 11); degree 64.26 | ✓ | — |
| 27 | L1 fit: 29 genes, 7 exactly zero {CD74,HLA-DRB1,IRF1,HLA-DMA,HLA-DMB,CD86,CD8B} | `09_external_validation_coef.json` | 29 genes; 7 zeros; exact set match | ✓ | — |
| 28 | IRG benchmark 0.619 (E-MTAB-4451) / 0.648 (GSE65682) | `S06_auc_compare.csv` | 0.619 / 0.648 | ✓ | — |
| 29 | 29/30 signature genes map; HLA-DQA1 missing | `09_external_validation.csv` | 30 total, 29 mapped, HLA-DQA1 missing | ✓ | — |
| 30 | Zenodo DOI 10.5281/zenodo.23042366 | `manuscript.md:221` | present, exact string | ✓ | — |
| 31 | Version v1.20.0 consistent; v1.19.1 absent | `manuscript.md:221,225` | v1.20.0 ×2; v1.16.0 ×1 (evaluated commit); no v1.19.1 | ✓ | — |
| 32 | No MR residue in manuscript | `manuscript.md` (full grep) | no Mendelian/IVW/Egger/STROBE-MR/TwoSampleMR | ✓ | — |

---

## 3. Tier-0 flag — the one number that does NOT appear as stated

### T0-1. The brief's "second cohort AUC 0.659 (n=52)" is not a manuscript claim; it conflates two distinct numbers
- 【Problem】 The panel brief and the task brief state a headline "second cohort AUC 0.659 (n=52)", but the manuscript makes no such claim — it reports a **within-cohort** GSE65682 CV AUC of 0.659 and a **single** external cohort (E-MTAB-4451, n=106, **52 deaths**) at AUC 0.638.
- 【Evidence】 Manuscript abstract (line 14): *"Within-cohort cross-validated AUC was 0.659 (optimistic)"* and *"external cross-platform AUC of 0.638 (… E-MTAB-4451, n = 106, 52 deaths)"*. Source files: `S06_auc_compare.csv` → Immune-risk signature (CV) = 0.6586; `09_external_validation.csv` → auc_EMTAB4451_orientedSum = 0.6382, n_validated_samples = 106, n_deaths = 52. There is exactly **one** external cohort in the manuscript (SRS, age, sex are *comparators within* E-MTAB-4451, not a second cohort). No file contains an "external cohort 2 at 0.659".
- 【Why it matters】 If a reviewer accepted the brief's phrasing, they would believe the signature was independently replicated in *two* external cohorts (0.638 and 0.659), which would overstate generalizability and is not what the manuscript shows. The manuscript is actually *more honest* than the brief (it scopes 0.659 as optimistic within-cohort CV). This is a brief defect, not a manuscript defect, but it must be corrected so the panel does not chase a nonexistent claim.
- 【Specific fix】 (For the panel/brief, not the manuscript — the manuscript is correct as written.) *"The manuscript reports one external cohort, E-MTAB-4451 (n = 106; 52 deaths; AUC 0.638, locked-L1 0.585), and a within-cohort GSE65682 5-fold CV AUC of 0.659 that is explicitly labeled optimistic. There is no second external cohort at 0.659; the n = 52 belongs to the E-MTAB-4451 death count, not to a separate cohort."*

---

## 4. Tier-1 / informational flags

### T1-1. Two source files report the GSE65682 CV AUC with a 0.0004 difference
- 【Problem】 The same quantity ("within-cohort CV AUC") is stored as 0.6586 in `S06_auc_compare.csv` and 0.6582 in `09_external_validation.csv` (column `auc_GSE65682_CV_locked`).
- 【Evidence】 `S06_auc_compare.csv` row "Immune-risk signature (CV)" = 0.6585575829768802; `09_external_validation.csv` `auc_GSE65682_CV_locked` = 0.6582. Both round to 0.659, so the manuscript's printed value (0.659) is safe, but the two raw files disagree by 0.0004.
- 【Why it matters】 Low. A meticulous reviewer comparing the two CSVs could flag an apparent inconsistency, even though it is within rounding and almost certainly a seed/locking artifact between the CV run and the locked-export run.
- 【Specific fix】 Either (a) source the single printed CV value from one file and delete/relabel the other, or (b) add a one-line note: *"The GSE65682 CV AUC is 0.659; minor differences between S06_auc_compare.csv (0.6586) and 09_external_validation.csv (0.6582) reflect the CV-split seed versus the locked-export split."*

### T1-2. Orphan Mendelian-randomization result files remain in `03_results/` but are unreferenced
- 【Problem】 `03_results/` still contains `10_genetics_mr.csv`, `10_mr_bh_family.csv`, `12_strobe_mr_checklist.csv`, `10_genetics_mr_*.csv` (×4), and a `_mr_backup_20260927/` directory, none of which are cited by the manuscript and none of which appear in §7 (Number provenance) or §8 (Supplementary index).
- 【Evidence】 Full-text grep of `manuscript.md` for `10_genetics_mr|10_mr_bh|12_strobe_mr|_mr_backup|genetics` → **no matches**. §8 states *"All supplementary tables are deposited as CSV in 03_results/"* and §7 lists only non-MR files. The manuscript is text-clean of MR (T0 confirmed) but the repository carries stale MR artifacts.
- 【Why it matters】 Not a manuscript number defect and not stale *text*, but a reviewer (or a data-availability check) opening `03_results/` will see MR files that contradict the "MR layer is gone" narrative, inviting confusion about whether MR was truly removed.
- 【Specific fix】 Remove (or move to an explicitly-labeled `03_results/_archived_mr_removed/`) the files `10_genetics_mr*.csv`, `10_mr_bh_family.csv`, `12_strobe_mr_checklist.csv`, and `_mr_backup_20260927/`, and add a line to §8: *"MR-layer artifacts from v1.19.x were removed; no MR results are reported in this version."*

### T1-3. The brief's `S09_` filename prefix does not exist; files are `09_`
- 【Problem】 The task/prompt directed me to recompute from `S09_external_validation.csv`, `S09_ext_dca_grid.csv`, `S09_ext_calibration_dca.csv`. Those files do not exist; the real files are `09_external_validation.csv`, `09_ext_dca_grid.csv`, `09_ext_calibration_dca.csv` (no "S").
- 【Evidence】 `ls 03_results/` shows `09_external_validation.csv` etc.; the manuscript §7 provenance already uses the correct `09_` prefix. The "S09_" prefix in the brief is a mislabel, not a manuscript error.
- 【Why it matters】 Informational only — ensures the panel does not hunt for nonexistent `S09_` files. The manuscript is internally consistent (it uses `09_`).
- 【Specific fix】 (Panel note) Use `09_*` not `S09_*` when referring to the external-validation artifacts.

### T1-4. Phenotype `group` value is literally "healthy", not "control"
- 【Problem】 The phenotype file stores the 42 non-septic samples with `group = "healthy"`; the manuscript consistently describes them as "healthy gastrointestinal-surgery controls" (§2.1, §3.1, Limitation 3).
- 【Evidence】 `GSE65682_pheno.csv` `group` value_counts: `sepsis 760`, `healthy 42`. The manuscript's "42 control" in the brief = these 42 "healthy" rows. No numeric discrepancy; the only nuance is the literal string.
- 【Why it matters】 None for the numbers; noted for provenance completeness. The manuscript's labeling is accurate (healthy GI-surgery controls).
- 【Specific fix】 No change required. (If desired for exactness: *"group = healthy (n=42), the gastrointestinal-surgery control group."*)

---

## 5. Detailed recomputation evidence (grouped)

### 5.1 Phenotype: 802 / 760 / 42
Recomputed directly from `01_data/GSE65682/GSE65682_pheno.csv` (802 data rows). `group` value_counts → sepsis 760, healthy 42. Sum = 802. `mars_endotype` → Mars1 132, Mars2 176, Mars3 118, Mars4 53, unassigned 323 (Manuscript §2.1: 132/176/118/53/323 — all match). Mars1-vs-Other reference n = 802 − 132 = **670** (manuscript §3.1 "n = 670" — match).

### 5.2 Hub directions and FIS1 logFC
From `S01_mars1_deg.csv` (11,519 genes; columns logFC, t, P.Value, adj.P.Val, DEG_0.3, DEG_1.0). Extracted the six hub genes:
- CD74 logFC **−0.7578**, HLA-DQA1 **−0.5301**, CD14 **−0.7657**, FCGR3A **−0.6097**, HAVCR2 **−0.3488** → all Mars1-down (manuscript §3.3/Table 1 direction correct).
- FIS1 logFC **+1.2614**, t = +17.16 (manuscript "logFC +1.26, t = +17.2" — match).
- `S05_hub_genes.csv` lists exactly six genes (FIS1, HAVCR2, HLA-DQA1, CD14, FCGR3A, CD74), all True across lasso/rf/univariate — matches "5 immune hubs + 1 passenger".

### 5.3 Signature, external AUCs, IRG-3
`S06_signature_genes.csv` = 30 rows (gene, corr_with_death, abs_r) → 30-gene signature confirmed.
`09_external_validation.csv`: n_signature_genes_total 30; n_signature_genes_mapped_EMTAB4451 29; genes_missing_in_test = HLA-DQA1; n_validated_samples 106; n_deaths 52; n_survivors 54; auc_GSE65682_CV_locked 0.6582; auc_EMTAB4451_external_locked **0.5848**; auc_EMTAB4451_orientedSum **0.6382**; CI 0.5317–0.7475; auc_IRG3_benchmark_EMTAB4451 **0.5288**. Every manuscript figure (0.638, 0.585, 0.529, 0.5288) reproduces.

### 5.4 Mars1 immune-function score median
`S02_immunoparalysis_score.csv` (802 rows; `immune_function_score`, `mars_endotype`). Mars1 subset (n=132) median = **−0.7916677** → manuscript Table 2 "−0.792" and §3.2 "−0.79" are both correct roundings of the same value (the brief's −0.7917 is the 4-dp form). Per-endotype medians recomputed: Mars1 −0.7917, Mars2 −0.7520, Mars3 0.6405, Mars4 −0.2347 — exactly matching Table 2 (columns median: −0.792/−0.752/0.641/−0.235).

### 5.5 DCA grid and calibration
`09_ext_dca_grid.csv` (thresholds 0.05–0.90). Model net-benefit vs treat-all:
- thr 0.25: 0.3208 vs 0.3208 (equal); thr 0.30: 0.2844 vs 0.2722 (model first exceeds) → manuscript "model NB exceeds treat-all from threshold 0.30" confirmed.
- thr 0.80: model 0.0 (flags 0), treat-all −1.5472; thr 0.85/0.90 model stays 0.0 while treat-all falls to −2.3962 / −4.0943 → the curves **diverge** (gap widens), exactly as the manuscript states ("DIVERGES … not converges"). The "diverges" wording is correct and data-supported.
`09_ext_calibration_dca.csv`: n 106, deaths 52, prevalence 0.4906, calib_intercept −0.0382 (CI −0.430–0.354), calib_slope **0.5028** (CI 0.095–0.906), p_slope_eq_1 0.01575. Manuscript §3.5 "slope 0.50 (CI 0.10–0.91; P=0.016) … over-confident" — all match, and the over-confident framing is the *correct* interpretation of slope<1.

### 5.6 DEG and immune-direction counts
`S01_mars1_deg.csv`: DEG_0.3 True = **3597** (manuscript 3597 ✓); DEG_1.0 True = 186. `S01_deg_sepsis_vs_ctrl.csv`: DEG_0.3 True = **448** (manuscript 448 ✓). `S01_immunoparalysis_direction.csv` (25 consensus immune genes): Mars1_down = 23; adj.P.Val<0.05 = 22 (includes PDCD1 up); Mars1_down ∧ sig = 21. Manuscript "23/25 down, 22/25 significant (incl. PDCD1 up), 21 both" — exact match.

### 5.7 Cellular context, LINCS, SRS, drug table, mortality, L1
All verified in §2 rows 19–27. Notably the L1000 candidate scores (lenalidomide rank 5435/20413 = 26.6%, rescue 0.0439, wtcs 0.2058; azithromycin rank 9152 = 44.8%, rescue 0.0133, wtcs 0.0626) and z (0.558, 0.103) and empirical P (0.266, 0.449) match the manuscript to the stated rounding; the SRS benchmark (0.6104; SRS1 24/37=0.649; SRS2 28/69=0.406; age 0.5043; ΔAUC +0.0278; perm P 0.694) matches; the 7-row drug table (response_gene_concordance and binomial P) matches exactly; Mars1 mortality (45/132=34.1%, 69/347=19.9%) matches; FIS1 degree rank 12 with degree 64.26 matches; and the L1 coefficient JSON contains exactly 29 genes with exactly 7 zero coefficients {CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B} — identical to the manuscript's named set.

### 5.8 Version, DOI, MR residue
Full-text grep of `manuscript.md`: `v1.20.0` appears at lines 221 and 225 (consistent); `v1.16.0` appears once (the evaluated commit tag, a legitimate prior tag, not drift); **no `v1.19.1` anywhere**; Zenodo DOI `10.5281/zenodo.23042366` present verbatim at line 221; **no** occurrence of Mendelian / IVW / Egger / STROBE-MR / TwoSampleMR / "mendelian randomization" / "MR layer". The MR layer removal is complete in the text.

---

## 6. § Stands up (things I suspected but found correct)
1. **The external AUC 0.638 is not inflated relative to its own CI and benchmark.** I suspected the "0.638" might be a cherry-picked optimistic figure; recomputation from `09_external_validation.csv` gives 0.6382 with a 95% CI of 0.5317–0.7475 that excludes 0.5 but is wide, and it sits essentially on top of the published IRG benchmark 0.619 — exactly as the manuscript frames it ("comparable to, not better than"). The honesty is real, not performative.
2. **The DCA "diverges at 0.80" claim is literally true and not spin.** I expected "diverges" to be a misdescription of a flat/overlap region; the grid shows model NB pinned at 0.0 from 0.80 upward while treat-all falls to −1.55, −2.40, −4.09, so the gap genuinely widens. The model-vs-treat-all crossover at 0.30 (0.2844 > 0.2722) also reproduces. The DCA narrative is faithful to the data.
3. **The calibration-slope over-confidence framing is the correct direction.** A slope of 0.50 (<1) genuinely indicates over-confident (too-extreme) predicted probabilities; the manuscript both reports 0.50 and correctly calls it over-confident, with P=0.016 against slope=1. This is a place where many papers get the sign wrong — this one did not.
4. **The hub gene set is reproducible and the FIS1 passenger is honestly separated.** All five immune hubs are genuinely Mars1-down in `S01_mars1_deg.csv` and all three selectors agree (`S05_hub_genes.csv`); FIS1 is genuinely up (+1.26) and the manuscript does not smuggle it into the "immune hub" claim. The 23/25-down and 21-both-significant direction counts are exact.
5. **No version drift and no MR residue in the submitted text.** Despite the repo still containing v1.19.x submission folders and orphan MR CSVs, the v1.20.0 manuscript is internally consistent on versioning and is free of Mendelian-randomization stale text.

---

## 7. § Questions for the authors (need answers; not guessing)
1. **CV-AUC reconciliation.** `S06_auc_compare.csv` reports the GSE65682 CV AUC as 0.6586 while `09_external_validation.csv` reports `auc_GSE65682_CV_locked` = 0.6582. Are these two different CV runs (different seed/locking) or should they be the same value? Please confirm the exact procedure that produced each, and whether the printed "0.659" should cite one specific file.
2. **Orphan MR files.** `03_results/` contains `10_genetics_mr*.csv`, `10_mr_bh_family.csv`, `12_strobe_mr_checklist.csv`, and `_mr_backup_20260927/`. Since the manuscript no longer references MR, will these be removed before the BMC deposit, or archived under an explicit "removed layer" label? (This is a data-availability/clarity question, not a textual defect.)
3. **Evaluated-commit tag.** §Data availability states *"the current evaluated commit 1212f7b is tagged v1.16.0, and this v1.20.0 release is built on top of it."* Could you clarify the tag relationship — is 1212f7b the exact commit that was reviewed, and is it also reachable as v1.20.0, or is v1.20.0 a later commit? A reviewer verifying the Zenodo/DOI snapshot needs the evaluated commit to be the one deposited.
4. **DCA threshold labeling.** The DCA grid stops at 0.90 with model NB = 0; the manuscript's Fig. S6C caption (in `04_figures/S06_dca.png`) should be checked to confirm it shows the same crossover at 0.30 and the divergence beyond 0.80 that the grid reports, so the figure and the `09_ext_dca_grid.csv` cannot be misread as convergence.

---

## 8. § What I actually checked (files read, commands run, values recomputed vs manuscript)
- **`05_reports/manuscript.md`** (read in full, 279 lines). Verified all stated numbers; checked version strings, Zenodo DOI, MR residue (full grep), and table syntax (all markdown pipe tables well-formed: Table 1 ln 71–80, Table 2 ln 89–94, Table 3 ln 119–127, §7 provenance ln 184–207). **No broken table syntax found.**
- **`01_data/GSE65682/GSE65682_pheno.csv`** — recomputed 802/760/42; endotype counts 132/176/118/53/323; Mars1 mortality 45/132 and Mars2–4 69/347. **Match.**
- **`03_results/S01_mars1_deg.csv`** — recomputed FIS1 logFC +1.2614; 5 hub logFCs (all negative); DEG_0.3 = 3597. **Match.**
- **`03_results/S01_deg_sepsis_vs_ctrl.csv`** — DEG_0.3 = 448. **Match.**
- **`03_results/S01_immunoparalysis_direction.csv`** — 23 down / 22 sig / 21 both. **Match.**
- **`03_results/S05_hub_genes.csv`** — 6 genes, all selectors True. **Match.**
- **`03_results/S06_signature_genes.csv`** — 30 genes. **Match.**
- **`03_results/S06_auc_compare.csv`** — CV 0.6586, train 0.7495, IRG 0.619/0.648. **Match** (CV 0.6586 vs 09-file 0.6582 flagged T1-1).
- **`03_results/09_external_validation.csv`** — orientedSum 0.6382, external_locked 0.5848, IRG3 0.5288, n=106, deaths=52, 29/30 mapped, HLA-DQA1 missing. **Match.**
- **`03_results/09_ext_dca_grid.csv`** — crossover at 0.30 (0.2844>0.2722); divergence at 0.80 (0.0 vs −1.5472). **Match.**
- **`03_results/09_ext_calibration_dca.csv`** — slope 0.5028, intercept −0.0382, P 0.01575, CI 0.095–0.906. **Match.**
- **`03_results/S02_immunoparalysis_score.csv`** — Mars1 median −0.791668; per-endotype medians match Table 2. **Match.**
- **`03_results/07_hub_celltype.csv`** — CD14 0.773, FCGR3A 0.491, CD74→DC 0.690, HAVCR2 0.298, HLA-DQA1→B 0.681. **Match.**
- **`03_results/S08_l1000_candidate_scores.csv`** — lenalidomide 5435/20413/0.0439/0.2058; azithromycin 9152/20413/0.0133/0.0626; z 0.558/0.103; empirical P 0.266/0.449. **Match.**
- **`03_results/09_ext_benchmark_vs_srs.csv`** — SRS 0.6104 (SRS1 24/37=0.649, SRS2 28/69=0.406), age 0.5043, ΔAUC +0.0278, perm P 0.694. **Match.**
- **`03_results/08_candidates_drugs.csv`** — 7-row concordance and binomial P. **Match.**
- **`03_results/S03_hub_degree.csv`** — FIS1 degree 64.26, rank 12. **Match.**
- **`03_results/09_external_validation_coef.json`** — 29 genes, 7 zero coefficients exactly {CD74,HLA-DRB1,IRF1,HLA-DMA,HLA-DMB,CD86,CD8B}. **Match.**
- **Orphan MR files** (`10_genetics_mr*.csv`, `10_mr_bh_family.csv`, `12_strobe_mr_checklist.csv`, `_mr_backup_20260927/`) — confirmed present in `03_results/` but **not referenced** by `manuscript.md` (grep: 0 matches). Flagged T1-2.

**Discrepancies found:** (a) the brief's "second cohort AUC 0.659 (n=52)" is not a manuscript claim — corrected in T0-1 (no manuscript number changes); (b) CV AUC 0.6586 vs 0.6582 across two files — T1-1 (within rounding, no printed-value change); (c) orphan MR CSVs unreferenced — T1-2 (repository hygiene); (d) brief `S09_` vs actual `09_` prefix — T1-3 (brief mislabel); (e) phenotype `group` literal "healthy" — T1-4 (no numeric discrepancy). **No manuscript-reported number failed to reproduce.**

---

## 9. Bottom line for the panel
The manuscript v1.20.0 is **arithmetically sound and provenance-clean** for every number I was asked to verify. The only item that "does not reproduce" is a claim that the manuscript *does not make* (the brief's conflated "second cohort 0.659 / n=52"), which I flag Tier-0 so the panel does not penalize the manuscript for a brief error. Recommend acceptance of the numeric/implementation layer, with the two low-priority Tier-1 housekeeping fixes (reconcile the CV value between the two CSVs; remove or archive the orphan MR files) folded in before the BMC deposit.
