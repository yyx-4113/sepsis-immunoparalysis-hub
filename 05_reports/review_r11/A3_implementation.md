# A3 — Implementation / Provenance Audit

**Manuscript:** `05_reports/manuscript.md` (Scientific Reports submission, v1.11.0)
**Auditor role:** A3, independent implementation/provenance reviewer
**Independence note:** Treated as a first submission. I did **not** read `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `review_r*/`, `cover_letter.md`, `scirep_submission_checklist.md`, `journal_recommendation.md`, `MEMORY.md`, any reviewer outputs, or author statements.

**Overall verdict:** Every quantitative claim I was asked to verify reconciles *exactly* with the underlying result files. I found **no material numeric discrepancy**. Two minor, non-blocking items are flagged (one DCA-threshold wording, one descriptive phrase). The reproducibility of this manuscript is, on the evidence I could recompute, exemplary.

---

## 1. Mars1-vs-Other DEG count = 3,597 (|logFC|≥0.3 & FDR<0.05)

【Problem】None — verified exactly.
【Evidence】`manuscript.md:72` and `manuscript.md:228` state **3,597** DEGs at |logFC|≥0.3 & FDR<0.05. Recomputed from `03_results/S01_mars1_deg.csv` (1,086,656 bytes; one row per gene): rows with `abs(logFC) >= 0.3` AND `adj.P.Val < 0.05` = **3,597** (exact match). I also cross-checked the file's own `DEG_0.3` boolean column against this rule for every row: **0 mismatches**, so the deposited flag is internally consistent. Sepsis-vs-healthy recomputed = **448** (`manuscript.md:87`, `:227` claim 448 — exact).
【Why it matters】This is the headline "endotype-driven, not case/control" signal; its magnitude anchors the whole framing.
【Specific fix】None required.

---

## 2. 23/25 consensus immune genes directionally down; 22 FDR-significant (incl. PDCD1 up); 21 both down & significant

【Problem】None — verified exactly.
【Evidence】`manuscript.md:72` (and §7 `:229`). Source `03_results/S01_immunoparalysis_direction.csv` has **25** genes:
- direction = `Mars1_down`: **23**; `Mars1_up`: **2** (PDCD1, LAG3).
- `adj.P.Val < 0.05`: **22** genes; PDCD1 (up) is among them (`adj.P.Val = 2.995e-10`), confirming "22 significant including the up-regulated PDCD1".
- down AND significant: **21** (the two non-significant-down genes are CD8B `adj.P=7.67e-2` and GZMA `adj.P=1.10e-1`; the third non-significant gene is LAG3 which is *up*).
【Why it matters】The "21 both down & significant" statement is the precise biological claim; it is arithmetically correct only if exactly two of the 23 down-genes fail FDR, which the file confirms.
【Specific fix】None required. (For transparency, the three non-significant genes are CD8B, GZMA — down; LAG3 — up.)

---

## 3. External validation — AUC 0.638 (95% CI 0.532–0.748), n=106, 52 deaths

【Problem】None — verified exactly; my independent bootstrap reproduces the deposited CI.
【Evidence】`manuscript.md:14,55,112,235` (abstract, §2.9, §3.5, §7). Source `03_results/09_ext_risk_scores.csv` (107 rows = 1 header + 106 samples): recomputed from `risk_oriented_sum` vs `y` → **AUC = 0.6382** (identical to deposited `auc_EMTAB4451_orientedSum = 0.6382`). n = **106**, deaths = **52**, survivors = **54** (matches `09_external_validation.csv` `n_deaths=52`, `n_survivors=54`). Independent 2,000-sample bootstrap (seed 42) on the same scores → CI **0.531–0.742**, matching the deposited `0.5317–0.7475` within bootstrap sampling error and clearly excluding 0.5. The locked-L1 score recomputed AUC = **0.5848** (deposited `auc_EMTAB4451_external_locked = 0.5848`; manuscript "0.585"). `n_signature_genes_mapped_EMTAB4451 = 29`, `genes_missing_in_test = HLA-DQA1` (manuscript "29/30, HLA-DQA1 absent" — `:112,235` — confirmed).
【Why it matters】This is the paper's "honest external validation" centerpiece; the point estimate and CI must be reproducible from the deposited risk scores, which they are.
【Specific fix】None required.

---

## 4. MR Table 3 (primary outcome ieu-b-5086) and family BH

【Problem】None for the reported Table-3 values — every cell matches the source CSV. One descriptive nuance: the manuscript states the Egger intercept test on the primary outcome was "not significant (P=0.34)" (`manuscript.md:149,194`); the deposited `10_genetics_mr_outcome5086_28ddeath.csv` gives CD14 MR-Egger `egger_intercept_p = 0.3440`, which is the value being referenced — consistent, but note this P belongs to the CD14 Egger intercept, not a pooled primary-outcome intercept. No correction needed; flagged only for precision.
【Evidence】`manuscript.md:155-160` (Table 3) vs `03_results/10_genetics_mr_outcome5086_28ddeath.csv` (recomputed, all exact):

| Gene | IVW OR (P) | Egger OR (P) | W-med OR (P) | I² | Median F (from harmonised) |
|------|-----------|--------------|--------------|-----|----------------------------|
| CD74 | 1.119 (0.718) | 1.093 (0.879) | 0.970 (0.937) | 0.22 | 35.4 |
| HLA-DQA1 | 0.923 (0.260) | 0.954 (0.558) | 0.930 (0.411) | 0.00 | 168.1 |
| CD14 | 0.927 (0.236) | 0.906 (4.9e-2) | 0.914 (0.065) | 0.00 | 45.7 |
| HAVCR2 | 0.978 (0.847) | 1.010 (0.955) | 0.960 (0.853) | 0.29 | 36.4 |
| FIS1 | 0.963 (0.473) | 0.964 (0.491) | 0.971 (0.768) | 0.00 | 75.0 |

All OR / P / I² / median-F values equal the manuscript to the decimals shown. Median-F per gene recomputed from `10_genetics_mr_outcome5086_harmonised.csv` (F column): CD74 35.4, HLA-DQA1 168.1, CD14 45.7, HAVCR2 36.4, FIS1 75.0 — exact. Instrument counts recomputed: CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8 = **27 total** (`manuscript.md:60,147` claim 27; FCGR3A excluded as `insufficient_instruments` — confirmed in CSV).

"Only 1 of 45 tests q<0.05" (`manuscript.md:149,176,195`): recomputed from `03_results/10_mr_bh_family.csv`, column `family_sig_q<0.05` — exactly **1** YES, namely **CD74 Weighted-median / 4982_critcare** with `q_family_45test = 2.99e-17` (manuscript "q≈3e-17" — confirmed). CD74 critical-care details (`manuscript.md:162,174`) cross-checked against `10_genetics_mr_outcome4982_criticalcare.csv`: IVW OR 2.222 (CI 1.175–4.200, P=0.014), MR-Egger slope OR 2.222 (P=0.088, intercept P=0.9999≈1.00), Weighted-median OR 2.194 (P=6.65e-19) — all exact. The noted implausible SE ordering (Egger SE 0.111 < IVW SE 0.325 on 3 SNPs) is confirmed by the CSV (`se` 0.11107 vs 0.32496).
【Why it matters】The MR layer is explicitly Tier-3/hypothesis-generating; the integrity of the "only one family-significant test, and it reverses direction" conclusion rests entirely on these 45 q-values being correctly computed — they are.
【Specific fix】None required for the numbers. Optionally, in §3.10/§5 specify that the primary-outcome "Egger intercept P=0.34" is the CD14 Egger intercept (the only primary-outcome Egger intercept the text is citing) to avoid a reader inferring a single pooled intercept test.

---

## 5. Figure / table file existence

【Problem】None — no missing files.
【Evidence】All PNGs cited in the text and in the Supplementary index (`manuscript.md:101,103,106,109,114,144,259`) exist in `04_figures/`: `S01_roc_28d_mars1.png`, `S02_score_vs_endotype.png`, `S03_top_hub.png`, `S03_eigengene_trait_cor.png`, `S06_roc_cv.png`, `S06_roc_train.png`, `S06_dca.png`, `S07_celltype.png`, `fig_s09_external_roc.png`, `fig_s10_l1000_rescue.png`, `mr_forest.png`, `mr_diag.png` — **12/12 present**. Every CSV referenced in §7 provenance (`manuscript.md:226-249`) exists in `03_results/` or `01_data/` (verified all 29 listed paths, including `01_data/GSE65682/GSE65682_expr.csv`, the three `E-MTAB-4451` files, and `01_data/LINCS/GSE92742_Level5_COMPZ.gctx`). `S01_deg_sepsis_vs_ctrl.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, `12_strobe_mr_checklist.csv`, `11_validation_design.md`, `tier1_summary.txt` all present.
【Why it matters】Provenance claims ("every number traces to a file") are only credible if the files exist.
【Specific fix】None.

---

## 6. Reference consistency [1]–[35]

【Problem】None.
【Evidence】Parsed `manuscript.md` in-text `[n]` citations and the References section (`:282-318`). In-text citations use exactly the integers **1–35**, each appearing ≥once; no citation outside 1–35. The References list contains exactly **35** entries numbered 1–35 with **no duplicates and no gaps**. Reference [32] (Giamarellos-Bourboulis, JAMA 2025) and [35] (Joshi et al., Front Immunol 2023) are both present and cited.
【Why it matters】A clean 1–35 mapping is required for a References section to be internally valid.
【Specific fix】None.

---

## 7. Cross-manuscript numeric consistency (discrepancy scan)

【Problem】Minor — DCA "converging to zero near 0.77" is a slight over-statement of the deposited grid.
【Evidence】`manuscript.md:112` states the external decision-curve "converging to zero near 0.77." Source `03_results/09_ext_dca_grid.csv` (threshold, nb_model): model net benefit is positive through threshold **0.75** (`nb_model = 0.0094`) and is **exactly 0.0 at threshold 0.80** (row: `0.8,0.0,-1.5472`). So the true zero-crossing is 0.80, not 0.77. The descriptive phrase "near 0.77" is off by ~0.03 on the threshold axis; the underlying claim (net benefit positive across 0.10–0.75, then collapses) is correct.
【Why it matters】Low severity — the conclusion (positive net benefit over the decision-relevant range) is intact, but a reviewer checking the grid will see 0.80, not 0.77.
【Specific fix】Change "converging to zero near 0.77" to "converging to zero by 0.80" (or cite the grid's exact 0.75/0.80 values).

【Problem】None for the other flagged pairs:
- **AUC 0.638 vs L1 0.585** (`manuscript.md:112,235`): these are two *different* metrics (oriented-sum score vs locked-L1 weights). Recomputed 0.6382 and 0.5848 from `09_ext_risk_scores.csv` — both correct and correctly distinguished. Not a discrepancy.
- **Calibration slope 0.50** (`manuscript.md:112`): deposited `09_ext_calibration_dca.csv` `calib_slope = 0.5028` (intercept −0.0382); rounding to 0.50 / −0.04 is faithful.
- **29/30 mapped vs HLA-DQA1 absent** (`manuscript.md:112,235`): `09_external_validation.csv` `n_signature_genes_total=30`, `n_signature_genes_mapped_EMTAB4451=29`, `genes_missing_in_test=HLA-DQA1` — fully consistent.
- **Abstract "all IVW OR 0.92–1.12, P ≥ 0.23"** (primary outcome): from Table 3 IVW ORs 0.923–1.119, P 0.24–0.85 — exact.

【Why it matters】Confirms there is no internal contradiction among the manuscript's repeated numbers.
【Specific fix】Only the DCA threshold wording above.

---

## § Stands up (verified correct, with evidence)

1. **Mars1 DEG = 3,597** at |logFC|≥0.3 & FDR<0.05 — recomputed exactly from `S01_mars1_deg.csv`; sepsis-vs-healthy = 448 also exact. (`manuscript.md:72,87`; evidence §1 above.)
2. **Immune-gene directionality 23/25 down, 22 FDR-sig (incl. PDCD1 up), 21 both** — recomputed exactly from `S01_immunoparalysis_direction.csv`; the three non-significant genes (CD8B, GZMA down; LAG3 up) are uniquely determined. (`manuscript.md:72`; evidence §2.)
3. **External AUC 0.638 (CI 0.532–0.748), n=106, 52 deaths, 29/30 mapped** — recomputed AUC 0.6382 and an independent bootstrap CI 0.531–0.742 from `09_ext_risk_scores.csv`; deposited CI 0.5317–0.7475. (`manuscript.md:14,112,235`; evidence §3.)
4. **MR Table 3 (all 5 genes × IVW/Egger/weighted-median OR, P, I², median F) and the "1 of 45 family q<0.05" conclusion (CD74 crit-care q=2.99e-17)** — every cell matches `10_genetics_mr_outcome5086_28ddeath.csv` and `10_mr_bh_family.csv`; median-F recomputed from harmonised file. (`manuscript.md:155-160,176`; evidence §4.)
5. **§3.2 immune-score medians/range/P-values** — recomputed from `S02_immunoparalysis_score.csv`: Mars1 median −0.792 (n=132), Mars2 −0.752 (P=0.467), Mars3 0.64 (P=1.85e-18), Mars4 −0.235 (P=1.32e-3); full-cohort range −3.65 to 3.86 — all exact vs `manuscript.md:90,96-99,235`.
6. **§3.9 L1000 ranks** — lenalidomide rank 5,435/20,413 (rescue 0.0439, 26.6%), azithromycin 9,152 (rescue 0.0133), prednisone 651 (0.136), dexamethasone 6,808 (0.032); library size 20,413 compounds — all exact vs `S08_l1000_candidate_scores.csv`, `S08_l1000_positive_control.csv`, `S08_l1000_rescue_trtcp.csv` (`manuscript.md:140,142`).
7. **References [1]–[35]** — complete, no duplicates, no gaps, all cited (`manuscript.md:282-318`; evidence §6).
8. **All 12 cited PNGs and all 29 §7-provenance files exist** (`manuscript.md:226-249,259`; evidence §5).

---

## § Questions for the authors

1. **MR diagnostic figures.** `manuscript.md:176` describes four distinct diagnostic plots — a 45-test forest, a CD14-28d scatter with IVW/Egger fits, an Egger funnel, and a leave-one-out analysis, "plus the CD74 critical-care scatter" — and states they are "in `04_figures/mr_forest.png` and `04_figures/mr_diag.png`." Only two MR PNGs exist. Please confirm that `mr_forest.png` actually contains the full 45-test forest and that `mr_diag.png` embeds the scatter, funnel, leave-one-out, and CD74-critical-care scatter as separate panels (i.e., the described sub-panels are genuinely present, not merely planned). This is the only place where text describes more content than the deposited figure set obviously enumerates.
2. **Bootstrap seed.** The deposited 95% CI (0.5317–0.7475) and my independent bootstrap (0.531–0.742, seed 42) agree in magnitude; please state the exact bootstrap specification (B, seed, bias-corrected vs percentile) used to generate `09_external_validation.csv` so the CI is exactly reproducible.
3. **Phenotype counts.** I recomputed the derived n's (Mars1 n=132; external n=106, 52 deaths) which all check; I did not re-derive the 802-sample / 760-sepsis / 42-ctrl matrix or the endotype/death cross-tab from the raw `01_data/GSE65682` phenotype file. Please confirm those base counts remain as stated in `manuscript.md:31` (these feed the stratification but are outside the result-CSV set I was asked to verify).

---

## § What I actually checked

**Commands run (Python 3.13.12, `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe`):**
- Parsed `S01_mars1_deg.csv` → counted `abs(logFC)>=0.3 & adj.P.Val<0.05` = **3,597**; same rule on `S01_deg_sepsis_vs_ctrl.csv` = **448**; validated `DEG_0.3` flag column (0 mismatches).
- Parsed `S01_immunoparalysis_direction.csv` (25 rows) → 23 down / 2 up; 22 FDR-significant (PDCD1 up included); 21 down&significant; listed the 3 non-significant genes.
- Parsed `09_ext_risk_scores.csv` (106 samples) → brute-force AUC of `risk_oriented_sum` = **0.6382**, `risk_locked_l1` = **0.5848**; 2,000-sample bootstrap (seed 42) CI = **0.531–0.742**; n=106, deaths=52.
- Parsed `10_genetics_mr_outcome5086_harmonised.csv` → per-gene SNP counts (3/4/6/6/8=27) and median F (35.4/168.1/45.7/36.4/75.0). Cross-checked every Table-3 cell in `10_genetics_mr_outcome5086_28ddeath.csv`; verified CD74 critical-care rows in `10_genetics_mr_outcome4982_criticalcare.csv`; counted `family_sig_q<0.05` in `10_mr_bh_family.csv` = 1 (CD74 w-median crit-care, q=2.99e-17).
- Parsed `S02_immunoparalysis_score.csv` → medians, range, and Mann–Whitney P vs Mars1 for Mars2/3/4.
- Parsed `08_candidates_drugs.csv`, `S08_l1000_candidate_scores.csv`, `S08_l1000_positive_control.csv`, counted `S08_l1000_rescue_trtcp.csv` = 20,413 compounds.
- Parsed `manuscript.md` for `[n]` citations and the References block → 1–35 all present/cited, no dup/gap.
- `os.path.exists` check of all 12 cited PNGs and all 29 §7-provenance files → all present.

**Discrepancies found:** One minor wording issue (DCA zero-crossing 0.77 vs deposited 0.80 in `09_ext_dca_grid.csv`). **No material numeric discrepancies.** Every headline number (3,597 DEGs; 23/25/22/21 immune genes; AUC 0.638/CI 0.532–0.748; MR Table 3 + family BH) reproduces exactly from the deposited sources.
