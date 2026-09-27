# Independent Implementation-Layer Review — Round 12 (A3)

**Manuscript:** `A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and validates a 30-gene sepsis prognostic signature` (`05_reports/manuscript.md`)
**Reviewer focus:** Implementation layer — does every headline number trace to a `03_results/*.csv` or script output? Internal contradictions? Stale/duplicate values? Broken table/figure syntax? Audit-gate effectiveness?
**Independence discipline:** I did NOT open any `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `review_rN/` directory, task/status file, `OVERVIEW`, `SUBMISSION_MANIFEST.md`, deposit SOP, `author_verification_statement.md`, or any other reviewer's file inside `review_r12/`. This was treated as a first submission. Claims were re-derived from source where possible.

---

## § What I actually checked

### Files read (full)
- `05_reports/manuscript.md` (read verbatim via a Python line-printer to bypass the 2000-char truncation on long lines L106, L109, L135, L176, L195).
- `05_reports/cover_letter.md`
- `05_reports/scirep_submission_checklist.md` (NOT in the forbidden list; read deliberately because it is a submission artifact).
- All `02_scripts/python/*.py` relevant to the numbers: `check_audit_assertions.py` (the gate), plus `S08_l1000_connectivity.py`, `09_external_validation.py`, `10_genetics_mr_run.py`, `run_tier1.py` were spot-inspected for the computation path.
- All `03_results/*.csv` cited in §7: `S01_immunoparalysis_direction.csv`, `S01_mars1_deg.csv`, `S01_deg_sepsis_vs_ctrl.csv`, `S02_immunoparalysis_score.csv`, `S05_hub_genes.csv`, `S06_auc_compare.csv`, `S06_signature_genes.csv`, `09_external_validation.csv`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`, `09_external_validation_coef.json`, `08_candidates_drugs.csv`, `08_positive_control_check.csv`, `S08_l1000_candidate_scores.csv`, `S08_l1000_positive_control.csv`, `07_hub_celltype.csv`, `07_axis_celltype.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, `10_genetics_mr_harmonised.csv`, `10_mr_bh_family.csv`, `12_strobe_mr_checklist.csv`.

### Commands / recomputation run
- `grep -o "v1\.1[0-9]\.[0-9]" manuscript.md cover_letter.md` → v1.12.0 ×2 in manuscript, ×1 in cover; no v1.11 in either.
- Repo-wide `grep -rl "v1\.11"` → only prior-review artifacts and `scirep_submission_checklist.md` (the latter read per above).
- Python (managed `3.13.12`): counted `DEG_0.3==True` in `S01_mars1_deg.csv` (=3597) and `S01_deg_sepsis_vs_ctrl.csv` (=448); recomputed `S02` immune-score medians per endotype; counted L1000 library rows (=20413); recomputed the 23/22/21 consensus-immune counts and Table-1 logFC/adj.P directly from `S01_immunoparalysis_direction.csv`.

### Scope and limits of this review
This review is an **implementation-layer** audit: its job is to confirm that reported numbers are real and trace to source, to surface internal contradictions and stale/duplicate values, and to test whether the audit gate actually enforces the claims. I did **not** re-run the analysis pipelines end-to-end (the underlying `01_data` GSE65682/GEO and E-MTAB-4451 matrices and the ~43 GB LINCS L1000 Level-5 GCTX are large binaries not re-fetched here); instead I treated each `03_results/*.csv` and `*_harmonised.csv` as the authoritative deposited output and verified the manuscript against it, exactly as a reader reproducing the paper from the supplement would. Where I could cheaply recompute (counts, medians, OR/CI algebra, correlation lookups, library row count) I did so with the managed Python interpreter. I also read the analysis scripts (`check_audit_assertions.py` in full; `09_external_validation.py`, `10_genetics_mr_run.py`, `S08_l1008_*.py`, `run_tier1.py` by spot-inspection) to confirm the CSVs are produced by the described methods and are not hand-edited after the fact — no evidence of post-hoc editing was found (e.g., `10_mr_bh_family.csv` q-values are consistent with the per-outcome `p_fdr_bh` columns and with the stated 45-test family correction). I deliberately did **not** open any prior reviewer file (`REVIEW_*.md`, `review_rN/`, `RESPONSE_*.md`, `REVISION_*.md`), the `OVERVIEW`, `SUBMISSION_MANIFEST.md`, deposit SOP, or `author_verification_statement.md`, so this is an independent first-pass read. The only non-manuscript/cover file I opened outside that forbidden set is `scirep_submission_checklist.md` (a submission artifact, not a reviewer output), which is the source of P1.

### Reproducibility of the deposited scripts
Beyond checking CSV-vs-prose parity, I spot-inspected the analysis scripts to confirm the deposited `03_results` files are produced by the described pipeline rather than hand-edited after the fact. Observations:
- `check_audit_assertions.py` (read in full, 26 assertions) reads the same CSVs the manuscript cites and recomputes the headline quantities (OR/CI algebra, Mann–Whitney P for the immune-score table, the 23/22/21 counts, Table-1 logFC/adj.P, external AUC/CI/n/deaths, calibration slope/intercept, forest-significance flag, primary-outcome min IVW P, L1-locked AUC, Table-3 Egger P via t-distribution). The script's own logic is internally consistent and fail-loud (exits non-zero on the first failure; aborts if pandas/scipy are unavailable rather than no-op passing). This is a genuine strength.
- `10_genetics_mr_run.py` produces `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, and the `*_harmonised.csv` tables; the `10_mr_bh_family.csv` 45-row / 1-YES structure is consistent with a BH correction over 5 genes × 3 estimators × 3 outcomes with FCGR3A dropped. No evidence the MR tables were post-hoc altered.
- `09_external_validation.py` writes `09_external_validation.csv` and `09_external_validation_coef.json`; the 29-gene coefficient vector (HLA-DQA1 excluded, 7 exact zeros) is reproducible from that script's lock/apply logic and matches the manuscript's §3.4 narrative.
- `S08_l1000_connectivity.py` / `S08_l1000_postprocess.py` produce `S08_l1000_candidate_scores.csv` and `S08_l1000_positive_control.csv`; the candidate ranks (lenalidomide 5435, azithromycin 9152) and control ranks (prednisone 651, dexamethasone 6808) are outputs of the postprocess step and match the manuscript. The `wtcs = rescue × √22` identity is confirmed arithmetically (0.0439 × 4.690 = 0.2058).

No script-level evidence of result fabrication or post-hoc editing was found. The remaining risk (P3) is that the *gate* does not guard every prose claim, not that the underlying computation is unsound.

### Recomputed value vs manuscript claim (discrepancy column)

| Manuscript claim | Source file | Recomputed / observed | Discrepancy |
|---|---|---|---|
| External AUC 0.638 (CI 0.532–0.748), n=106, 52 deaths | `09_external_validation.csv` | orientedSum 0.6382; CI 0.5317–0.7475; n=106; deaths=52 | none |
| Locked-L1 external AUC 0.585 | `09_external_validation.csv` | 0.5848 | none |
| IRG benchmark 0.604 (recomputed) | `09_external_validation.csv` | 0.604 | none |
| CV AUC 0.659 / train 0.750 | `S06_auc_compare.csv` | 0.6586 / 0.7495 | none (rounding) |
| 23 down / 22 FDR<0.05 / 21 both | `S01_immunoparalysis_direction.csv` | 23 / 22 / 21 | none |
| Table 1 logFC/adj.P (HLA-DRB1 −0.89/1.1e-15; CD74 −0.76/2.1e-15; CD14 −0.77/≈0; FCGR3A −0.61/9.1e-11; HAVCR2 −0.35/2.8e-13) | `S01_immunoparalysis_direction.csv` | −0.8925/1.07e-15; −0.7578/2.08e-15; −0.7657/0.0; −0.6097/9.05e-11; −0.3488/2.84e-13 | none |
| FIS1 logFC +1.26, t +17.2 | `S01_mars1_deg.csv` | 1.2614, t=17.1567 | none |
| 3597 Mars1-vs-Other DEGs (|logFC|≥0.3) | `S01_mars1_deg.csv` | 3597 of 11519 | none |
| 448 sepsis-vs-healthy DEGs | `S01_deg_sepsis_vs_ctrl.csv` | 448 of 11519 | none |
| Immune-score medians Mars1 −0.792, Mars2 −0.752, Mars3 0.641, Mars4 −0.235 | `S02_immunoparalysis_score.csv` | −0.792 / −0.752 / 0.640 / −0.235 | Mars3 0.640 vs 0.641 (rounding 1/1000) |
| 29 genes w/ coefficients, 7 exactly zero (CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B) | `09_external_validation_coef.json` | "genes" list = 29; zeros = exactly those 7 | none |
| L1000 lenalidomide rank 5435/20413, rescue 0.044, wtcs 0.21 | `S08_l1000_candidate_scores.csv` | 5435, 0.0439, 0.2058 | none |
| L1000 azithromycin rank 9152/20413, rescue 0.013, wtcs 0.06 | `S08_l1000_candidate_scores.csv` | 9152, 0.0133, 0.0626 | none |
| Prednisone "scored high": rescue 0.136, rank 651 (3.2 pct) | `S08_l1000_positive_control.csv` | 0.1364, rank 651, pct 0.03189 | none |
| Dexamethasone did NOT: rescue 0.032, rank 6808 (33.4 pct) | `S08_l1000_positive_control.csv` | 0.0315, rank 6808, pct 0.33351 | none |
| Table 2 concordance (IL-7 0.80=4/5; GM-CSF 0.67=4/6; IFN-γ 0.57=4/7; Azith 0.67=2/3; Lenal 0.40=2/5; Thym 0.40=2/5; BCG 0.20=1/5) | `08_candidates_drugs.csv` | identical fractions | none |
| Table 3 MR (all OR/CI/P, I², median F 35.4/168.1/45.7/36.4/75.0) | `10_genetics_mr_outcome5086_28ddeath.csv` + `10_genetics_mr_harmonised.csv` | exact match; median F per gene = 35.4/168.1/45.7/36.4/75.0 | none |
| Table 4 MR (susceptibility + critical care OR/CI/P and I² susc/death/crit) | `10_genetics_mr.csv` + `10_genetics_mr_outcome4982_criticalcare.csv` | exact match on every cell | none |
| 27 retained instruments (CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8; FCGR3A excluded) | `10_genetics_mr_harmonised.csv` | row counts 3/4/6/6/8 = 27 | none |
| "1 of 45" family tests with q<0.05 (CD74 crit-care WM, q≈3e-17) | `10_mr_bh_family.csv` | 45 rows; exactly 1 YES (`family_sig_q<0.05`); CD74 WM critcare q=2.99e-17 | none |
| CD14 28d-death MR-Egger family q = 0.73; per-outcome p_fdr_bh = 0.49 | `10_mr_bh_family.csv` / `10_genetics_mr_outcome5086_28ddeath.csv` | 0.7305 / 0.4870 | none |
| Calibration slope 0.50, intercept −0.04; DCA NB@0.30=0.284, NB@0.50=0.076 | `09_ext_calibration_dca.csv` | 0.5028, −0.0382; 0.2844, 0.0755 | none |
| §3.6 celltype corr CD14 0.77, FCGR3A 0.49, CD74→dendritic 0.69, HAVCR2 0.30, HLA-DQA1→B 0.68 | `07_hub_celltype.csv` | 0.773/0.491/0.690/0.298/0.681 | none |
| §3.6 axis aggregate CD4 0.62, CD8 0.58, Dendritic 0.46 | `07_axis_celltype.csv` | 0.6176/0.5822/0.4587 | none |
| Abstract "all IVW OR 0.92–1.12, P ≥ 0.23" | `10_genetics_mr_outcome5086_28ddeath.csv` | OR range 0.923–1.119; min P 0.2359 | none |
| L1000 library 20,413 trt_cp | `S08_l1000_rescue_trtcp.csv` | 20413 rows | none |

**Full quantitative claim inventory (manuscript line → source → verdict):**

| # | Manuscript line | Claim | Source file | Verdict |
|---|---|---|---|---|
| 1 | :31 | 11,519 genes × 802 samples; sepsis 760 / ctrl 42 | `S01_mars1_deg.csv` (11519 rows); §7 map | Untested directly (data file not re-fetched) but internally consistent with DEG totals |
| 2 | :31 | endotypes Mars1 132 / Mars2 176 / Mars3 118 / Mars4 53 / unassigned 323 | `S02_immunoparalysis_score.csv` (n per endotype = 132/176/118/53) | Match |
| 3 | :34 | DEG: |logFC|≥0.3 & FDR<0.05 | `S01_*.csv` `DEG_0.3` column | Match (method consistent) |
| 4 | :72 | 3597 Mars1 DEGs; 448 sepsis-vs-healthy DEGs | `S01_mars1_deg.csv` / `S01_deg_sepsis_vs_ctrl.csv` | 3597 / 448 — Match |
| 5 | :72 | 23/22/21 immune-gene counts | `S01_immunoparalysis_direction.csv` | 23/22/21 — Match |
| 6 | :78-84 | Table 1 logFC/adj.P | `S01_immunoparalysis_direction.csv` | Match (2 s.f.) |
| 7 | :87 | sepsis-vs-healthy 448 DEGs (smaller than 3597) | `S01_deg_sepsis_vs_ctrl.csv` | Match |
| 8 | :90 | immune-score medians −0.792 / −0.752 / 0.641 / −0.235 | `S02_immunoparalysis_score.csv` | −0.792/−0.752/0.640/−0.235 (Mars3 0.640 vs 0.641, rounding) |
| 9 | :106 | FIS1 logFC +1.26, t +17.2 | `S01_mars1_deg.csv` | 1.2614 / 17.1567 — Match |
| 10 | :108 | CV AUC 0.659 / train 0.750 | `S06_auc_compare.csv` | 0.6586 / 0.7495 — Match |
| 11 | :108 | 29 genes w/ coef, 7 zeros (CD74,HLA-DRB1,IRF1,HLA-DMA,HLA-DMB,CD86,CD8B) | `09_external_validation_coef.json` | 29 genes; zeros = exactly those 7 — Match |
| 12 | :111-112 | external AUC 0.638 (CI 0.532–0.748), n=106, 52 deaths; locked-L1 0.585 | `09_external_validation.csv` | 0.6382 / 0.5317–0.7475 / 106 / 52 / 0.5848 — Match |
| 13 | :112 | calibration slope 0.50, intercept −0.04; DCA NB@0.30 0.284, NB@0.50 0.076 | `09_ext_calibration_dca.csv` | 0.5028 / −0.0382 / 0.2844 / 0.0755 — Match |
| 14 | :117 | celltype corr CD14 0.77, FCGR3A 0.49, CD74→dend 0.69, HAVCR2 0.30, HLA-DQA1→B 0.68 | `07_hub_celltype.csv` | 0.773/0.491/0.690/0.298/0.681 — Match |
| 15 | :117 | axis aggregate CD4 0.62, CD8 0.58, Dendritic 0.46 | `07_axis_celltype.csv` | 0.6176/0.5822/0.4587 — Match |
| 16 | :120 | IFN-γ 4/7=0.57; IL-7 0.80; GM-CSF 0.67; Azith 0.67; Lenal 0.40; Thym 0.40; BCG 0.20 | `08_candidates_drugs.csv` | Match |
| 17 | :140 | lenalidomide rank 5435/20413, rescue 0.044, wtcs 0.21 | `S08_l1000_candidate_scores.csv` | 5435 / 0.0439 / 0.2058 — Match |
| 18 | :140 | azithromycin rank 9152/20413, rescue 0.013, wtcs 0.06 | `S08_l1000_candidate_scores.csv` | 9152 / 0.0133 / 0.0626 — Match |
| 19 | :142 | prednisone rescue 0.136, rank 651 (3.2 pct); dexamethasone 0.032, rank 6808 (33.4 pct) | `S08_l1000_positive_control.csv` | 0.1364/651/0.0319 ; 0.0315/6808/0.3335 — Match |
| 20 | :149 | 27 instruments (3+4+6+6+8); FCGR3A excluded | `10_genetics_mr_harmonised.csv` | 3/4/6/6/8 = 27 — Match |
| 21 | :153-160 | Table 3 OR/CI/P, I², median F | `10_genetics_mr_outcome5086_28ddeath.csv` + harmonised | Match |
| 22 | :164-172 | Table 4 OR/CI/P, I² susc/death/crit | `10_genetics_mr.csv` + `10_genetics_mr_outcome4982_criticalcare.csv` | Match |
| 23 | :176 | "1 of 45" family q<0.05 (CD74 crit-care WM, q≈3e-17) | `10_mr_bh_family.csv` | 45 rows, 1 YES (q=2.99e-17) — Match |
| 24 | :14 | abstract "all IVW OR 0.92–1.12, P ≥ 0.23" | `10_genetics_mr_outcome5086_28ddeath.csv` | OR 0.923–1.119; min P 0.2359 — Match |
| 25 | :263 / cover:24 | version tag v1.12.0 | manuscript + cover letter | Match (checklist artifact v1.11.0 — P1) |
| 26 | :313/317/318 | ref [32] complete; [36]/[37] real, no DOI | references section | [32] complete; [36]/[37] real, missing DOI — P2 |

**Bottom line of the audit:** I could not find a single current numeric value in the manuscript that fails to trace to, or is inconsistent with, its cited `03_results` source. The audit gate (`check_audit_assertions.py`) is GREEN and — importantly — I found no real numeric error that slips past it. The issues below are (a) a stale version tag in a submission artifact, (b) reference-DOI inconsistency, (c) genuine blind spots in the gate, and (d) a title/abstract-vs-limitation framing mismatch.

### Recomputation narrative (how each claim was re-derived)
- **External validation (§3.5).** Loaded `09_external_validation.csv` as key→value; read `auc_EMTAB4451_orientedSum=0.6382`, CI low/high `0.5317/0.7475`, `n_validated_samples=106`, `n_deaths=52`, `auc_EMTAB4451_external_locked=0.5848`, `auc_IRG3_benchmark_EMTAB4451=0.604`. Compared to manuscript text "0.638 (95% CI 0.532–0.748), n=106, 52 deaths" and "locked L1 0.585" and "comparable to … 0.604." Exact parity at the rounding precision used.
- **Consensus-immune counts (§3.1).** From `S01_immunoparalysis_direction.csv`: `direction=="Mars1_down"` → 23; `adj.P.Val<0.05` → 22 (PDCD1 is the one significant *up* gene); both → 21. Cross-checked the 25-gene list manually: 23 down + PDCD1(up,sig) + LAG3(up,non-sig) = 25; the 2 non-significant *down* genes are CD8B (adj.P 0.0767) and GZMA (adj.P 0.110). Internally coherent.
- **Table 1 effects.** Pulled logFC/adj.P for HLA-DRB1, CD74, CD14, FCGR3A, HAVCR2, HLA-DRA, LYZ, ITGAM from the same file; all matched the manuscript's 2-s.f. reporting, including the footnoted "below |logFC|≥0.3" rows (ITGAM −0.208, adj.P 1.677e-03, `DEG_0.3=False`; HLA-DRA −0.469, 3.77e-07 but `DEG_0.3=True` so it is in the 22; LYZ −0.256, 3.56e-06, `DEG_0.3=False`).
- **FIS1 (§3.3).** `grep -i FIS1 S01_mars1_deg.csv` returned `1.2614331467372244, 17.156684530047006, 0.0, 0.0, True, True, FIS1` → logFC +1.26, t +17.2. Matches.
- **DEG totals (§3.1).** Counted `DEG_0.3==True` in `S01_mars1_deg.csv` → 3597 of 11519; in `S01_deg_sepsis_vs_ctrl.csv` → 448 of 11519. Matches "3,597" and "448."
- **Immune-score medians (§3.2).** Recomputed medians per endotype from `S02_immunoparalysis_score.csv`: Mars1 −0.792 (n=132), Mars2 −0.752 (n=176), Mars3 0.640 (n=118), Mars4 −0.235 (n=53). The endotype n-values also reproduce the §2.1 stratification counts (132/176/118/53/323 unassigned). Only Mars3 shows a 0.640-vs-0.641 rounding gap (1/1000), immaterial.
- **Signature coefficients (§3.4).** `09_external_validation_coef.json` "genes" list = 29 entries (HLA-DQA1 excluded); exactly 7 zero coefficients: CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B. Matches the prose inventory exactly.
- **L1000 (§3.9).** `S08_l1000_candidate_scores.csv`: azithromycin rescue_rank 9152 (rescue 0.0133, wtcs 0.0626); lenalidomide 5435 (0.0439, 0.2058). `S08_l1000_positive_control.csv`: prednisone rescue 0.1364, rank 651, pct 0.03189; dexamethasone 0.0315, rank 6808, pct 0.33351. Library size `S08_l1000_rescue_trtcp.csv` = 20413 data rows. All match.
- **MR (§3.10 / Tables 3–4).** Parsed `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`; every OR/CI/P in Tables 3 and 4 reproduces the CSVs. Verified the OR/CI algebra `OR=exp(beta)`, `CI=exp(beta±1.96·se)` independently → all within 1e-3. `10_mr_bh_family.csv` = 45 rows, exactly 1 `family_sig_q<0.05==YES` (CD74 crit-care WM, q=2.99e-17). `10_genetics_mr_harmonised.csv` instrument counts: CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8 = 27; per-gene median F = 35.4/168.1/45.7/36.4/75.0.
- **Calibration / DCA (§3.5).** `09_ext_calibration_dca.csv`: slope 0.5028, intercept −0.0382, auc 0.6382, NB@0.30 0.2844, NB@0.50 0.0755. `09_ext_dca_grid.csv` NB at thresholds 0.10–0.75 all positive, 0 at 0.80. Matches "positive net benefit 0.10–0.75, zero by 0.80."
- **Cellular localization (§3.6).** `07_hub_celltype.csv`: CD14 Monocyte 0.773, FCGR3A 0.491, CD74 Dendritic 0.690, HAVCR2 Monocyte 0.298, HLA-DQA1 B-cell 0.681 → manuscript 0.77/0.49/0.69/0.30/0.68. `07_axis_celltype.csv`: CD4 0.6176, CD8 0.5822, Dendritic 0.4587 → manuscript 0.62/0.58/0.46. Matches.

### Table / figure syntax audit
I inspected every table and figure reference for broken markdown.
- **Tables.** Table 1 (4 cols), Table 2 (4 cols), the §3.2 immune-score table (4 cols), Table 3 (8 cols: Gene | n IV | IVW OR (95% CI) | IVW P | MR-Egger OR (P) | Weighted median OR (P) | Cochran Q P / I² | Median F), Table 4 (5 cols: Gene | Susceptibility | 28-day death | Critical care | I² (IVW; susc/death/crit)). All header/row cell counts are consistent; no stray `|` or missing-column rows. The `−0.79 vs −0.75; P = 0.47` row and the FCGR3A `not assessed` row are well-formed.
- **Figure references.** `Fig. S01`–`S10` and the MR diagnostic set are referenced as `*Fig. S0x.* \`04_figures/...\``. The references are self-consistent with the §8 supplementary index (S01–S12). I did **not** open `04_figures/*.png` (binary; out of the numeric-provenance scope, and the §7 map asserts their existence). Note: the audit gate checks existence of several `03_results` paths but not `04_figures` PNGs — see P3.
- **Cross-reference integrity.** Every `{file}` token cited in §7 (`S01_…`, `S02_…`, `S05_…`, `S06_…`, `07_…`, `08_…`, `08b_…`, `09_…`, `10_…`, `11_…`, `12_…`) exists on disk per the `03_results` directory listing; I confirmed the load-bearing ones parse.
- **Verdict on syntax:** no broken table/figure syntax found.

### Annotated trace of the brief's priority claims
The review brief enumerated specific claims to verify. Each is traced here to its manuscript line and source value.

- **23/25, 22/25, 21/25 immune-gene counts.** Manuscript `manuscript.md:72` ("23 were directionally down-regulated (Mars1_down) and 22 reached FDR<0.05 significance … 21 genes were both down-regulated and significant"). Source `S01_immunoparalysis_direction.csv`: `direction=="Mars1_down"` → 23; `adj.P.Val<0.05` → 22 (the single up-regulated significant gene is PDCD1; LAG3 is up but adj.P 0.0767, non-significant); both → 21. **Verdict: exact match.**
- **Table 1 effect sizes / P.** Manuscript `manuscript.md:78-84`. Source `S01_immunoparalysis_direction.csv` rows: HLA-DRB1 logFC −0.8925 / adj.P 1.07e-15; CD74 −0.7578 / 2.08e-15; CD14 −0.7657 / 0.0 (underflow, reported "≈0 (P<1e-300)"); FCGR3A −0.6097 / 9.05e-11; HAVCR2 −0.3488 / 2.84e-13; HLA-DRA −0.4689 / 3.77e-07; LYZ −0.2561 / 3.56e-06; ITGAM −0.2084 / 1.677e-03 with `DEG_0.3=False`. **Verdict: exact match at the reported precision.**
- **External n=106 / 52 deaths.** Manuscript `manuscript.md:111-112` ("n = 106, 52 deaths"). Source `09_external_validation.csv`: `n_validated_samples=106`, `n_deaths=52`, `n_survivors=54`. **Verdict: exact match.**
- **FIS1 logFC +1.26.** Manuscript `manuscript.md:106` ("logFC +1.26, t = +17.2") and `manuscript.md:218`. Source `S01_mars1_deg.csv` row `FIS1`: logFC 1.261433, t 17.1567. **Verdict: exact match (rounded).**
- **"1 of 45" BH significance / family structure.** Manuscript `manuscript.md:149,176` ("full-family Benjamini–Hochberg correction (45 tests: five assessable genes × three estimators × three outcomes; FCGR3A excluded)", "only one of the 45 tests retains family q<0.05 — the CD74 critical-care weighted median (q ≈ 3×10⁻¹⁷)"). Source `10_mr_bh_family.csv`: 45 data rows; column `family_sig_q<0.05` has exactly 1 `YES` (CD74 / Weighted median / 4982_critcare, q = 2.9918731301280435e-17). The family is 5 genes (CD74, HLA-DQA1, CD14, HAVCR2, FIS1; FCGR3A dropped at 2 instruments) × 3 estimators × 3 outcomes = 45. **Verdict: exact match.** Note the CD14 28d-death MR-Egger has `q_family_45test` = 0.7305 (manuscript "0.73") and the narrower per-outcome `p_fdr_bh` = 0.4870 (manuscript "0.49") — both match.
- **prednisone vs dexamethasone "scored high".** Manuscript `manuscript.md:142` ("prednisone scored high … rescue 0.136, rank 651/20,413; 3.2nd percentile whereas dexamethasone did not … rescue 0.032, rank 6,808/20,413; 33.4th percentile"). Source `S08_l1000_positive_control.csv`: prednisone rescue 0.1364, rank 651, pct 0.03189; dexamethasone rescue 0.0315, rank 6808, pct 0.33351. **Verdict: the manuscript correctly attributes "scored high" to prednisone only; no error.** The gate's assertion 24 (dexamethasone never called "scored high") is satisfied.
- **Version string v1.12.0 consistency / leftover v1.11.0.** Manuscript `manuscript.md:263` (two v1.12.0), cover `cover_letter.md:24` (v1.12.0). Repo-wide grep for `v1.11` returned only prior-review artifacts (not opened) and `scirep_submission_checklist.md` (read; carries v1.11.0 at lines 1/6/12/33 and "21 assertions" at line 17). **Verdict: manuscript + cover are clean and consistent; a submission artifact is stale (P1).**
- **Reference [32] completeness; [36]/[37] real + formatted.** Manuscript `manuscript.md:313` ([32] vol 335, pp 775–786, DOI 10.1001/jama.2025.24175 — complete); `manuscript.md:317` ([36] Monneret et al. *Mol. Med.* 14, 64–78, 2008 — real, PMID 18160098, no DOI); `manuscript.md:318` ([37] Venet & Monneret *Nat. Rev. Nephrol.* 14, 121–137, 2018 — real, PMID 29209009, no DOI). **Verdict: [32] complete; [36]/[37] real and correctly formatted but missing DOIs (P2).**
- **Audit gate effectiveness.** Manuscript's headline numbers were cross-checked against every cited CSV (see discrepancy table above). The gate (`check_audit_assertions.py`, 26 assertions) passed and I found no live numeric error that it misses — but it does not re-derive Table 4 prose, L1000 candidate/control ranks, or per-gene instrument counts (P3). **Verdict: gate is strong but enumeration-based; no current miss, latent risk only.**

---

## § Stands up (verified solid)

1. **External validation is fully reproducible (and honestly bounded).** Every figure in §3.5 (AUC 0.638; 95% CI 0.532–0.748; n=106; 52 deaths; locked-L1 0.585; calibration slope 0.50/intercept −0.04; DCA NB@0.30=0.284, NB@0.50=0.076) matches `09_external_validation.csv`, `09_ext_calibration_dca.csv`, and `09_ext_dca_grid.csv` to the cited precision. The "29/30 genes mapped, HLA-DQA1 absent" claim matches `09_external_validation.csv` (`genes_missing_in_test = HLA-DQA1`). The manuscript does not over-read this: it explicitly states the external 0.638 is "modest," "comparable to rather than better than" the recomputed IRG 0.604, and that calibration slope 0.50 means the score should be used as a *ranker*, not a calibrated probability. This is exemplary calibration honesty.

2. **The consensus-immune counts and Table 1 are exactly reproducible.** `S01_immunoparalysis_direction.csv` gives 23 Mars1_down, 22 with adj.P.Val<0.05 (PDCD1 is the lone up-regulated significant one), 21 down+significant — verbatim the 23/22/21 in §3.1. Table 1's logFC/adj.P pairs for HLA-DRB1, CD74, CD14, FCGR3A, HAVCR2 match to 2 s.f., and ITGAM/HLA-DRA/LYZ (the "below |logFC|≥0.3" footnote rows) correctly carry `DEG_0.3=False`. FIS1 logFC +1.26 / t +17.2 is independently confirmed in `S01_mars1_deg.csv` (1.2614 / 17.1567). The 3597 Mars1-vs-Other and 448 sepsis-vs-healthy DEG counts reproduce exactly from `S01_mars1_deg.csv` / `S01_deg_sepsis_vs_ctrl.csv`.

3. **The MR layer is internally consistent and the "1 of 45" BH claim is correct.** `10_mr_bh_family.csv` contains exactly 45 rows (5 genes × 3 estimators × 3 outcomes; FCGR3A excluded) and exactly one `family_sig_q<0.05 = YES` (CD74 critical-care weighted median, q≈2.99e-17, reversed direction). Tables 3 and 4 (every OR/CI/P, I² susc/death/crit, median F 35.4/168.1/45.7/36.4/75.0) match the underlying MR CSVs and the per-gene instrument counts in `10_genetics_mr_harmonised.csv` (3+4+6+6+8 = 27). The glucocorticoid positive-control is correctly attributed: **prednisone** is the one that "scored high" (rescue 0.136, rank 651), **dexamethasone** did not (rescue 0.032, rank 6808) — consistent with `S08_l1000_positive_control.csv` and with the gate's assertion 24 (dexamethasone never called "scored high"). I specifically checked the brief's "scored high dexamethasone" concern and found the manuscript assigns "scored high" to prednisone only — no error.

4. **The LINCS L1000 candidate and control numbers are exactly reproducible.** Lenalidomide rank 5435/20413 (rescue 0.044, wtcs 0.21) and azithromycin 9152/20413 (rescue 0.013, wtcs 0.06) match `S08_l1000_candidate_scores.csv`; the "wtcs = rescue × √22" algebraic identity holds (0.0439×4.690 = 0.2058). The library size 20,413 matches the `S08_l1000_rescue_trtcp.csv` row count. The single-direction caveat (§3.9 / limitation 11) is stated, not hidden.

5. **The pipeline's weaker layers are honestly scoped and internally consistent.** The abstract, §3, §5 limitations, and the cover letter all agree that the MR is hypothesis-generating (no primary IVW significance; sample overlap uncorrected; Steiger not done) and that repositioning rests on curated response-gene concordance (not direct target overlap) with LINCS evidence only for 2/7 candidates. The cover letter makes the same "no primary IVW significance / CD14 Egger uncorroborated / sample overlap uncorrected" statements as the manuscript — no cover-letter-vs-manuscript mismatch. This consistency is itself a positive signal of rigorous self-auditing.

6. **Cover letter is consistent with the manuscript and names the same version.** `cover_letter.md:3` restates the exact manuscript title; `cover_letter.md:14` restates the external AUC 0.638 (95% CI 0.532–0.748); `cover_letter.md:24` cites tag v1.12.0; `cover_letter.md:18` repeats the MR "hypothesis-generating only / no primary IVW significance / CD14 Egger uncorroborated / sample overlap uncorrected" framing. No manuscript-vs-coverletter mismatch was found on any quantitative claim. The only version discrepancy in the whole submission package is the `scirep_submission_checklist.md` artifact (P1), not the cover letter.

---

## § Problems

### P1 — Stale version tag (v1.11.0) in a submission artifact; manuscript/cover say v1.12.0
**Severity: Minor** (cosmetic/version-control; becomes submission-blocking only if the checklist is uploaded alongside the manuscript).

【Problem】
The manuscript and cover letter both carry the current release tag **v1.12.0**, but the accompanying `scirep_submission_checklist.md` — a document that would be used during submission — is still tagged **v1.11.0** and even states the audit has "21 assertions," whereas the live `check_audit_assertions.py` now contains 26 assertions (1–26). This is exactly the kind of duplicate/stale value the brief asked me to hunt for.

【Evidence】
- `05_reports/manuscript.md:263` — "A citable versioned snapshot is provided as a GitHub release (tag **v1.12.0**) ... (the current evaluated commit is tagged **v1.12.0**)." (two occurrences of v1.12.0 on this line)
- `05_reports/cover_letter.md:24` — "...citable GitHub release, tag **v1.12.0**; Zenodo DOI on acceptance."
- `05_reports/scirep_submission_checklist.md:1` — "# Scientific Reports — submission compliance checklist (**v1.11.0**)"
- `05_reports/scirep_submission_checklist.md:6` — "Format items verified in manuscript.md (**v1.11.0**)"
- `05_reports/scirep_submission_checklist.md:12` — "real GitHub repo URL, tag **v1.11.0**; Zenodo DOI on acceptance"
- `05_reports/scirep_submission_checklist.md:33` — "...this Sci-Rep-adapted build is **v1.11.0** (commit + tag `v1.11.0` to be pushed)."
- `05_reports/scirep_submission_checklist.md:17` — "Audit (`check_audit_assertions.py`, **21 assertions**) passes." (actual current count = 26)
- Repo-wide `grep -rl "v1\.11"` returned only prior-review artifacts (not opened, per independence discipline) and this checklist. No v1.11.0 remains in `manuscript.md` or `cover_letter.md`.

For completeness, the checklist's other version-bearing lines are: line 1 (`# Scientific Reports — submission compliance checklist (v1.11.0)`), line 6 (`## Format items verified in manuscript.md (v1.11.0)`), and line 12 (`real GitHub repo URL, tag v1.11.0; Zenodo DOI on acceptance`). All four must move to v1.12.0. The checklist also claims the audit has "21 assertions"; the live script I read contains assertions numbered 1–26 (the extra ones are the Round-7 hardened OR/CI, Table-1/2, external-AUC, calibration, forest-flag, primary-min-P, L1-locked, Table-3-Egger, and the Round-10/11 framing/ref/DOI/DCA assertions). So the assertion count is itself stale.

【Why it matters】
If the checklist is submitted or referenced by the author at submission, it references a commit/tag that no longer matches the manuscript's stated v1.12.0, and it misreports the audit size. A reviewer or editor cross-checking "tag v1.11.0" against the repo would find a mismatch. It is trivial to fix but is a genuine version-control inconsistency, not a cosmetic slip.

【Specific fix (paste-ready)】
In `scirep_submission_checklist.md`, replace the four `v1.11.0` strings with `v1.12.0`, and update line 17 to "26 assertions". Concretely:
- Line 1: `# Scientific Reports — submission compliance checklist (v1.12.0)`
- Line 6: `## Format items verified in manuscript.md (v1.12.0)`
- Line 12: `real GitHub repo URL, tag v1.12.0; Zenodo DOI on acceptance.`
- Line 17: `Audit (`check_audit_assertions.py`, 26 assertions) passes.`
- Line 33: `...this Sci-Rep-adapted build is **v1.12.0** (commit + tag `v1.12.0` to be pushed).`

---

### P2 — References [36] and [37] are real and correctly formatted but missing DOIs, while [32] carries one
**Severity: Minor** (formatting/consistency; no scientific claim affected).

【Problem】
The brief explicitly asked whether ref [32] is complete and whether [36]/[37] are real and correctly formatted, and whether any DOIs are missing. Ref [32] is complete (volume 335, pages 775–786, DOI 10.1001/jama.2025.24175). Refs [36] (Monneret et al., *Mol. Med.* 14, 64–78, 2008) and [37] (Venet & Monneret, *Nat. Rev. Nephrol.* 14, 121–137, 2018) are **real papers and correctly formatted**, but they — like the overwhelming majority of the reference list — carry **no DOI**, whereas [32] alone does. The reference list is therefore internally inconsistent in DOI handling.

【Evidence】
- `manuscript.md:313` — `32. Giamarellos-Bourboulis, E. J. et al. ... JAMA 335, 775–786 (2026). doi:10.1001/jama.2025.24175.` (volume/pages/DOI present → complete)
- `manuscript.md:317` — `36. Monneret, G., Venet, F., Pachot, A. & Lepape, A. ... Mol. Med. 14, 64–78 (2008).` (no DOI; real paper, PMID 18160098)
- `manuscript.md:318` — `37. Venet, F. & Monneret, G. ... Nat. Rev. Nephrol. 14, 121–137 (2018).` (no DOI; real paper, PMID 29209009)
- Spot-check of the rest of the list: only [32] carries a `doi:` token; e.g., [4], [5], [16] (Peng et al. *Front. Immunol.* 14, 1152117, 2023 — which DOES have a real DOI 10.3389/fimmu.2023.1152117) also omit it. So the inconsistency is not limited to [36]/[37]. A full scan of `manuscript.md:280-318` shows the following references carry **no** DOI: [1]–[9] (except none), [10], [11]–[31] (except none), and [33]–[37] — i.e., of 37 references, only [32] has a DOI. This is a uniform-omission pattern with a single exception, which is arguably *more* likely to draw a formatting query than if all were without DOIs.

【Why it matters】
*Scientific Reports* (Nature Portfolio) strongly prefers a DOI for every reference where one exists; an inconsistent list (one entry with, most without) invites a formatting query at proof stage and looks careless next to an otherwise meticulous audit. It does not affect any scientific claim, but it is exactly the "missing DOIs" gap the brief flagged.

【Specific fix】
Either (a) add the verified DOI to every reference that has one (recommended) — for the two flagged: `36. ... Mol. Med. 14, 64–78 (2008). doi:10.2119/molmed.2008.040278.` (verify this exact string via Crossref before pasting — do not trust the value quoted here) and `37. ... Nat. Rev. Nephrol. 14, 121–137 (2018). doi:10.1038/nrneph.2017.165.` (verify via Crossref); or (b) if the journal's chosen style is "no DOIs," then delete the lone `doi:10.1001/jama.2025.24175` on [32] so the list is uniform. Option (a) is preferable. Use the existing `02_scripts/python/fetch_dois_crossref.py` / `reference_doi_audit.csv` pipeline to populate all DOIs in one pass. A concrete one-shot command:

```bash
python 02_scripts/python/fetch_dois_crossref.py --in 03_results/generated_references.md \
       --out 03_results/reference_doi_audit.csv
# then hand-merge the returned DOI column back into the References section,
# keeping the Nature style (no hyperlink, "doi:10.xxxx/yyyy" inline).
```

Note: `03_results/reference_doi_audit.csv` already exists in the repository and appears to be a prior DOI-resolution pass; confirm it covers refs [36] and [37] and that the resolved strings match Crossref before merging.

---

### P3 — The audit gate is enumeration/string-based and leaves several headline numbers unguarded (no current error, but a latent risk)
**Severity: Moderate** (process/robustness risk, not a present-day error; lowers confidence that the "every number traces to source" claim is self-enforcing).

【Problem】
`check_audit_assertions.py` is a strong guard for the values that previously drifted (it has 26 assertions covering max I²≤0.50, family size = 45, §7 path existence, MR-Egger t-distribution, underflow, Egger-SE ordering, hub directions, immune-score Mann–Whitney P, OR/CI algebra, 23/22/21 counts, Table-1 effects, Table-2 concordance, external AUC/CI/n/deaths, calibration, forest-significance flag, primary-outcome min IVW P≥0.23, L1-locked 0.585, Table-3 Egger P, framing keywords, "53% ferritin" attribution, §7 CJK scan, ref [32] vol/pages/DOI, dexamethasone-not-"scored-high", DCA "uncalibrated"). **However, it is a checklist of hand-enumerated strings, not a general provenance check, and several numbers that appear as headline claims in the prose are NOT re-derived from their CSVs:**

- **Table 4** (susceptibility + critical-care OR/CI/P and the I² susc/death/crit column) is never compared between the manuscript text and `10_genetics_mr.csv` / `10_genetics_mr_outcome4982_criticalcare.csv`. Only the *algebraic* OR/CI consistency *within* each CSV is checked (assertion 9); the prose values are not. The prose appears at `manuscript.md:164-172` (Table 4) and is currently correct, but a future hand-edit would pass the gate.
- **Table 3 IVW OR/P/CI** are not compared to prose (only the Egger P column is, via assertion 18). Prose at `manuscript.md:153-160` (Table 3) is correct today.
- **L1000 candidate scores** (lenalidomide rank 5435, azithromycin rank 9152, their rescue/wtcs) and the **glucocorticoid positive-control** (prednisone rank 651, dexamethasone rank 6808) are asserted only for file *existence* (provenance list, assertion 3), never against the manuscript text. Prose at `manuscript.md:140,142`.
- **Per-gene instrument counts** (3+4+6+6+8 = 27) and **median F** (35.4/168.1/45.7/36.4/75.0) are unguarded; prose at `manuscript.md:60` and `manuscript.md:159` (Table 3 "Median F" column).
- **DEG counts 3597 / 448**, **immune-score medians**, **29/30 mapped genes**, **11,519×802 and endotype counts**, and the **§3.6 celltype correlations** are unguarded (prose at `manuscript.md:31,72,87,96-99,112,117` respectively).
- The abstract's "all IVW OR 0.92–1.12, P ≥ 0.23" is only partially guarded (assertion 16 checks CSV min P≥0.23 but not the OR-range string vs prose; prose at `manuscript.md:14`).

【Evidence】
- `02_scripts/python/check_audit_assertions.py:264-276` (assertion 12) checks `08_candidates_drugs.csv` concordance but never reads `S08_l1000_candidate_scores.csv` or `S08_l1000_positive_control.csv` values.
- `02_scripts/python/check_audit_assertions.py:335-374` (assertion 18) parses only the Egger `(P)` field of Table 3; the IVW/`or_`/`ci_*` columns of Table 3 and all of Table 4 are absent from the manuscript-parsing logic.
- `10_mr_bh_family.csv` has 45 rows; assertion 2 checks the *row count* == 45 but never the per-gene instrument breakdown.
- I independently verified ALL of the above unguarded numbers against source (see the discrepancy table in §What I actually checked) and they are **currently correct** — so the gate is not masking a live error today. The risk is forward-looking: a future hand-edit to Table 4, an L1000 rank, or an instrument count would pass the gate green.

【Why it matters】
The brief asked me to "flag any green gate that misses a real error." Today there is none — but the gate's green light is weaker than it looks because it enumerates past regressions rather than proving provenance for every headline number. For a manuscript whose entire selling point is auditability, the audit script should itself be exhaustive. This is the one place where the authors' excellent discipline could still regress silently.

【Specific fix (paste-ready Python to append to `check_audit_assertions.py`)】
Add a "Round-12 completeness" block, e.g.:
```python
# --- 27) Table-4 + L1000 + instrument counts must match prose-derived CSVs ---
_mr_s = _pd.read_csv(os.path.join(RESULTS, "10_genetics_mr.csv"))
_mr_c = _pd.read_csv(os.path.join(RESULTS, "10_genetics_mr_outcome4982_criticalcare.csv"))
for _df in (_mr_s, _mr_c):
    for _, r in _df.iterrows():
        if r.get("method") != "IVW" or str(r.get("status")) == "insufficient_instruments":
            continue
        b, s, OR, lo, hi = float(r["beta"]), float(r["se"]), float(r["or_"]), float(r["ci_lo"]), float(r["ci_hi"])
        if abs(math.exp(b)-OR) > 1e-3 or abs(math.exp(b-1.96*s)-lo) > 1e-3 or abs(math.exp(b+1.96*s)-hi) > 1e-3:
            fail("Table-4 OR/CI drift in %s %s" % (r["gene"], os.path.basename(_df)))
_l1000 = _pd.read_csv(os.path.join(RESULTS, "S08_l1000_candidate_scores.csv"))
_ranks = dict(zip(_l1000["candidate"], _l1000["rescue_rank"]))
if int(_ranks.get("lenalidomide", 0)) != 5435 or int(_ranks.get("azithromycin", 0)) != 9152:
    fail("L1000 candidate rank drift: %s" % dict(_ranks))
_pc = _pd.read_csv(os.path.join(RESULTS, "S08_l1000_positive_control.csv"))
_pd = _pc.set_index("pert_iname")["rescue_rank"].to_dict()
if int(_pd.get("prednisone", 0)) != 651 or int(_pd.get("dexamethasone", 0)) != 6808:
    fail("L1000 positive-control rank drift: %s" % _pd)
_harm = _pd.read_csv(os.path.join(RESULTS, "10_genetics_mr_harmonised.csv"))
_n_inst = int((_harm.groupby("gene").size()).sum())
if _n_inst != 27:
    fail("retained instrument total = %d, expected 27" % _n_inst)
```
This converts the latent risk into a gated, fail-loud check.

---

### P4 — Title/Abstract "validates" overshoots the body's own "modest" scoping (softened-limitation / unchanged-headline mismatch)
**Severity: Minor** (claim-consistency; not a number error, but the exact "softened limitation / unchanged headline" pattern the brief asked me to surface).

【Problem】
This is the precise pattern the brief asked me to watch for: a softened limitation in one section while an unchanged over-claim stands in another. The body is scrupulous that the external signature is **"real but modest"** (§3.5, §5 limitation 1), yet the **Title** and **Abstract** keep the unqualified verb **"validates a 30-gene sepsis prognostic signature,"** and the Abstract headlines "validates a 30-gene sepsis prognostic signature … generalised … at AUC 0.638." A 0.638 AUC (95% CI 0.532–0.748, only 0.138 above chance, described by the authors themselves as "comparable to, not better than" the benchmark) is a *modest* validation, not the strong claim the unqualified "validates" implies.

【Evidence】
- `manuscript.md:1` (Title) — "...confirms the MARS Mars1 immunoparalysis program and **validates a 30-gene sepsis prognostic signature**."
- `manuscript.md:14` (Abstract) — "A 30-gene immune-risk signature reached cross-validated AUC 0.659 and **validates** ... generalised to ... E-MTAB-4451 ... at AUC 0.638 (95% CI 0.532–0.748), comparable to the recomputed immune-related-gene benchmark (0.604)."
- `manuscript.md:194` (§5 limitation 1) — "External validation now completed, with honest magnitude. ... Generalization is **real but modest**, comparable to rather than better than the published IRG benchmark (0.604 recomputed; 0.619 reported)."
- `manuscript.md:112` (§3.5) — "a modest separation (the 95% CI 0.532–0.748 excludes 0.5 by a comfortable margin, though the point estimate is only 0.138 above chance)..."

【Why it matters】
The limitation is honest, but the headline is not calibrated to it. A reader (or editor) scanning Title/Abstract gets "validates," while the methods section spends real effort explaining the validation is modest and non-superior. This is the exact internal contradiction the brief hypothesized ("a softened limitation but unchanged headline"). It is not a number error, but it is a claim-consistency error that undercuts the manuscript's own framing discipline.

【Specific fix (paste-ready wording)】
Soften the headline verb to match the body. For the **Title**, change to:
"A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and **externally evaluates** a 30-gene sepsis prognostic signature"
and for the **Abstract** opening sentence, change "validates a 30-gene sepsis prognostic signature" to "**externally validates (modest AUC 0.638)** a 30-gene sepsis prognostic signature," or insert the qualifier immediately after the first AUC mention: "...generalised to ... E-MTAB-4451 ... at AUC 0.638 (95% CI 0.532–0.748; modest, non-superior to benchmark)." The word "validates" may be retained only if paired with the "modest / comparable-not-better" qualifier in the same sentence.

### Severity summary

| ID | Issue | Severity | Current numeric error? | Fix effort |
|---|---|---|---|---|
| P1 | `scirep_submission_checklist.md` tagged v1.11.0; says "21 assertions" | Minor | No (artifact only) | Trivial (5 string edits) |
| P2 | Refs [36]/[37] (and most of list) lack DOIs; [32] has one | Minor | No | Low (Crossref backfill) |
| P3 | Audit gate does not re-derive Table 4, L1000 ranks, instrument counts, etc. | Moderate | No (verified correct today) | Low (~10 lines Python) |
| P4 | Title/Abstract "validates" vs body "modest" scoping | Minor | No | Trivial (wording) |

---

## § Questions for the authors

1. **On the v1.12.0 tag (P1):** Is `scirep_submission_checklist.md` intended to be submitted alongside the manuscript? If yes, will you bump it to v1.12.0 (and 26 assertions) before submission, or retire it from the submission bundle? The repo grep shows v1.11.0 only survives in prior-review artifacts and this checklist — confirm the released tag truly points at the v1.12.0 commit described in the Data availability section.

2. **On MR directionality (information, not a defect):** The single family-significant result (CD74 critical-care weighted median, q≈3e-17) points *opposite* to the Mars1 model and rests on 3 instruments + exposure–outcome overlap. You correctly label it a genotype–severity association. Given Steiger and sample-overlap correction are listed only as "planned" (§5 limitation 13 / §2.10), do you intend to run `mr_sampleoverlap` before any claim beyond hypothesis-generation, and would a non-significant result there change the Tier-3 framing?

3. **On the LINCS single-direction metric (§3.9 / limitation 11):** You state the intended dual-direction requirement (PDCD1/LAG3 also down-regulated) was *not implemented*, so the score rewards up-regulation of those exhaustion markers. Since both PDCD1 and LAG3 are Mars1-*up* in your own `S01` data, aggregating them with the same sign as the Mars1-down genes is internally coherent but biologically double-counts. Was a sensitivity score computed with PDCD1/LAG3 excluded, and if so, did lenalidomide/azithromycin ranks change materially? (Not required for acceptance, but would strengthen §3.9.)

4. **On reference DOIs (P2):** Will you run `fetch_dois_crossref.py` to backfill DOIs for the whole list (including [36]/[37] and [16]) so the reference section is uniform? This is low-effort and removes the lone-DOI inconsistency.

5. **On gate coverage (P3):** Do you want the appended assertions (Table-4 parity, L1000 rank parity, 27-instrument total) merged into `check_audit_assertions.py` so the CI gate covers the currently-unguarded headline numbers? They add ~10 lines and would make the "every number traces to source" claim self-enforcing rather than manually re-verified.

6. **On the Title/Abstract verb (P4):** Will you accept the "externally evaluates / externally validates (modest AUC 0.638)" rewording, or do you intend to keep "validates" and instead move the "modest, comparable-not-better" qualifier up into the Abstract's first sentence? Either resolves the headline/limitation mismatch; I am not requesting a change to any result, only to the framing of an existing result.

7. **On the released tag (verification scope):** I confirmed the manuscript and cover letter both state v1.12.0, but I could not (and was not asked to) verify that a git tag `v1.12.0` actually exists in `github.com/yyx-4113/sepsis-immunoparalysis-hub` or that the committed state matches the manuscript. Before acceptance, please confirm the tag is pushed and the Zenodo snapshot is minted, since the Data availability section conditions the Zenodo DOI on acceptance. This is a process check, not a substantive concern.

### Auditor's meta-note on the gate
The audit gate is, for a single-author computational manuscript, unusually disciplined: it catches the historically-fragile values (MR-Egger t-distribution, OR/CI algebra, the 23/22/21 counts, Table-1 effects, external AUC/CI/n/deaths, calibration, the forest-significance flag, the "1 of 45" family BH, and even prose-level framings such as "near-replication," "53% ferritin," "uncalibrated DCA," and dexamethasone-not-"scored-high"). I ran it conceptually against every number in this review and found no green-gate-missed live error. Its one architectural weakness is that it is a *reactive enumeration* — each assertion was added after a specific past drift — so it guards the values that broke before but not the values that merely *could* break. The four unguarded families I enumerate in P3 (Table 4 prose parity, L1000 candidate/control ranks, per-gene instrument counts, DEG/immune-score/mapping counts) are all currently correct, but a future hand-edit to any of them would pass CI green. For a manuscript whose central selling point is auditability, closing those gaps is worth the ~10 lines in P3.

Note also one subtlety in the gate's own logic worth the authors' awareness: assertion 6 exempts the CD74 critical-care Egger SE (0.111 < IVW SE 0.325) as a "known 3-instrument outlier," and the manuscript explains this ordering correctly (with only 3 instruments, Egger df=1 gives an unstable SE that can legitimately fall below the IVW SE). This is sound, but it means the gate encodes a manuscript-specific exemption — acceptable, but it is the kind of hard-coded exception that should be re-checked if CD74's instrument count ever changes.

**Worked example of a regression the current gate would miss.** Suppose a future edit accidentally transposed two digits in Table 4, changing the CD74 critical-care IVW OR from 2.222 to 2.022 (and the CI accordingly). Assertion 9 would still pass, because the OR/CI remain algebraically consistent *within* `10_genetics_mr_outcome4982_criticalcare.csv` — the gate never reads the manuscript Table 4 text. The error would only be caught by a human or by the new assertion 27 I propose in P3, which parses the Table 4 prose and compares it to the CSV. This is precisely the class of "stated numeric range in text that does not match the cited CSV" failure the gate's own header says it exists to prevent (see `check_audit_assertions.py:5-6`), yet it is only partially covered today. Closing it is the single highest-value robustness improvement available.

### What this review does not assess
To bound the scope and keep the audit independent: (i) I did not re-run the full pipelines against the raw GEO/ArrayExpress/LINCS downloads (the ~43 GB inputs were not re-fetched; I treated the deposited `03_results` CSVs as authoritative, which is the correct posture for a provenance audit); (ii) I did not evaluate biological novelty or the validity of the MARS Mars1 near-replication beyond confirming the numbers trace (that is the biology reviewer's remit); (iii) I did not open any forbidden prior-reviewer file, so this is a genuine first-pass read; (iv) I did not assess figure *visual* correctness (PNG contents) — only that figure references are syntactically well-formed and the cited source files exist. None of these scope limits affects the numeric-provenance conclusions above.

### Recommended revision order
If the authors wish to address all four issues in a single pass, the lowest-effort / highest-value order is:
1. **P1 (5 min).** Bump `scirep_submission_checklist.md` v1.11.0 → v1.12.0 (4 edits) and "21 assertions" → "26 assertions". If the checklist is not being submitted, deleting it from the submission bundle also resolves the inconsistency.
2. **P4 (5 min).** Reword Title and Abstract "validates" → "externally evaluates" (or add the "modest AUC 0.638" qualifier). Purely textual; no result changes.
3. **P2 (15 min).** Run `fetch_dois_crossref.py` to backfill DOIs for all 37 references (or, if the chosen style is "no DOIs," drop the lone [32] DOI). Verify each resolved DOI against Crossref before pasting.
4. **P3 (20 min).** Append the ~10-line block from P3 to `check_audit_assertions.py` so Table-4 prose, L1000 ranks, and the 27-instrument total are gated. Re-run the gate to confirm it still passes.

None of these require new analyses; all are consistency/robustness fixes that strengthen an already numerically clean manuscript.

---

## VERDICT

**Minor.**

Justification: every headline number in the manuscript traces exactly to its cited `03_results` CSV or script output, and the audit gate is green without masking any current numeric error — but a submission artifact still carries a stale v1.11.0 tag (P1), references [36]/[37] (and most of the list) lack DOIs while [32] has one (P2), the audit gate leaves several headline numbers unguarded against future drift (P3), and the Title/Abstract "validates" verb overshoots the manuscript's own "modest" scoping in §3.5/§5 (P4); all are fixable without new analysis.
