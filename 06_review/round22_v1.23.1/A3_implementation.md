# A3 — Implementation / Reproducibility review (Round-22, v1.23.1)

## 1. Independence attestation
I read only the manuscript, the submission/build/verify scripts, the audit script, `03_results/*.csv`, `CITATION.cff`, and `_PANEL_BRIEF.md`; I did **not** open any `06_review/` prior-round file, rebuttal, or git history.

## 2. Verdict
**MINOR** — the manuscript's reported numbers reconcile exactly with the authoritative CSVs (11/11 recomputed within rounding), Table 1 is pipe-clean, references are 40 / valid Vancouver / DOI-complete, and `verify_submission_bmc.py` exits 0. No Tier-0/1 factual error, contradiction, or invalid statistic was found in my lane. The issues are about audit *meaningfulness/labeling* and provenance *completeness*, not numeric correctness.

## 3. Findings

**[Tier 2]** `02_scripts/python/check_audit_assertions.py` (assertions #1,#2,#4,#5,#6,#9,#15,#16,#18 — code lines ~24-46, 105-155, 317-349, 359-379) — roughly **9 of 32 assertions** validate a **deleted Mendelian-randomisation layer** (max I2 across 15 MR tests; MR primary 15-test IVW family; MR-Egger t-dist p; Egger SE vs IVW SE; OR/CI on MR rows; forest significance flag; "retained MR trail" null; "MR layer removed" self-consistency). The manuscript removed MR at v1.20.0, so these assertions neither check nor defend any current claim. The headline **"32/32 green" overstates validation coverage of the paper's actual content**.
*Fix:* split the audit into (a) a live-claim audit (the non-MR assertions) and (b) a separately-labelled "MR audit-trail regression guard" that is **not** counted in the manuscript's 32/32; or re-label so "32/32" reflects only live claims.

**[Tier 2]** `02_scripts/python/check_audit_assertions.py:71-85` (assertion #3) — lists `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, `10_mr_bh_family.csv` as "§7 provenance paths present", but **none of these MR CSVs appear in the manuscript §7 Number-provenance table**. The audit silently depends on MR files that the paper does not cite.
*Fix:* remove the MR files from the repo/audit, or add an explicit "audit-trail (retained, not reported)" entry in §7 / manifest so the dependency is honest.

**[Tier 2]** `03_results/` retains MR CSVs (`10_genetics_mr*.csv`, `10_mr_bh_family.csv`) although the manuscript is framed as "MR-free (v1.20.0)". The submission manifest's "Do NOT upload" list excludes the two MR *figures* but **not** the MR *CSVs*. An editor/reproducer inspecting the repo sees MR data + an MR-saturated audit despite the paper claiming no MR.
*Fix:* move MR CSVs to a quarantined subfolder (e.g. `03_results/_audit_trail_mr_removed/`) referenced only by the audit guard, and state this in the manifest.

**[Tier 2]** `05_reports/manuscript.md §7` (Number provenance) — several quoted statistics are **not mapped to a source file**: SRS benchmark AUC 0.610 / SRS1 24/37 / SRS2 28/69 (§5); age-alone AUC 0.504; ΔAUC +0.028; permutation P=0.69 (§5); Mars1 mortality 34.1% (45/132) vs 19.9% (69/347) OR 2.08 (§3.2). These are recomputable from cited cohort files (`GSE65682_pheno.csv`, E-MTAB SDRF) but are absent from §7, so a strict provenance reader could flag gaps.
*Fix:* add a short provenance row/footnote tracing each secondary quoted number to its CSV/pheno source.

**[Tier 3]** `03_results/08_candidates_drugs.csv` — mechanism/evidence columns contain CJK text (e.g. "T 细胞稳态增殖，对抗 T 细胞耗竭/凋亡"). It does **not** leak into the manuscript (Table 3 uses only numeric columns) and the SI-build script strips CJK before embedding, but the raw source CSV is non-English.
*Fix:* store mechanism notes in English (or a language-tagged field) for transparency/reproducibility.

**[Tier 3]** `05_reports/manuscript.md:71-80` (Table 1) — ITGAM and LYZ rows embed raw annotation prose ("...but below the 0.3 logFC fold-change DEG threshold, DEG_0.3=False") inside the Function column. **No stray `|` characters → no column leakage; the table is a clean 4-column table (verified).** The inline annotation is editorially cluttered and mixes raw flags into a results table.
*Fix:* move the DEG_0.3 flag to a dedicated column or a footnote; keep the Function column clean.

**[Tier 3]** `05_reports/manuscript.md:242-283` (References) — ref [23] Schuemie et al. (empirical calibration of p-values in observational studies) is cited (audit #30 confirms citation) but is **tangential**: the manuscript performs no p-value calibration / empirical-null method, so its aptness is questionable.
*Fix:* confirm [23] is genuinely used; if not, drop or replace with a directly relevant citation.

**Positive checks (clean):**
- `verify_submission_bmc.py` → exit 0; `docx chars=76012 refs=40 figs=10 ALL CHECKS PASSED`. I verified via this script (it enforces `v1.23.1` string, key numbers 0.585/0.638/0.529/0.619/106/52/30/FIS1/1.26, 40 Vancouver refs, 10 figures, and MR-residue scan on both docx **and** `manuscript.md`). I did not perform a clean rebuild of the docx (to avoid side effects); the presence of the `v1.23.1` tag string in the docx plus identical key numbers is strong evidence it is the current build.
- `check_audit_assertions.py` → exit 0, 32/32 printed. 23/32 assertions are genuinely meaningful (re-derive real headline numbers, reference integrity, DCA grid, DA tag/commit). The remaining ~9 are the MR audit-trail guards noted above.
- No `v1.22.0` / `v1.21.0` stale version string in `manuscript.md` or `CITATION.cff` (both correctly at v1.23.1). Historical references to v1.16.0 (results-pinned commit) and v1.20.0 (MR removal) are legitimate. Note: the submission-pack *folder* is `07_submission_bmc_v1.21.0` while the manuscript is v1.23.1 — a minor label mismatch, not a blocker (Tier 3).
- **MR-layer residue in manuscript/tables/figures/supplements = ZERO** (grep for Mendelian/instrument/IVW/Egger/genetic/SNP/pleiotropy → no matches; verify script confirms docx + md clean; MR figures excluded from the 10 copied). The MR trail lives only in the repo CSVs + audit script (flagged Tier 2 above).

## 4. Cross-validation note (11 statistics recomputed from source CSVs — all match within rounding)

| # | Manuscript claim | Source CSV | Source value | Match |
|---|---|---|---|---|
| 1 | Locked-L1 external AUC 0.585 (CI 0.469–0.696) | `09_external_validation.csv` `auc_EMTAB4451_external_locked` / CI | 0.5848 / 0.4687–0.6959 | ✓ |
| 2 | Equal-weight sensitivity AUC 0.638 (CI 0.532–0.748) | `09_external_validation.csv` `auc_EMTAB4451_orientedSum` / CI | 0.6382 / 0.5317–0.7475 | ✓ |
| 3 | IRG-3 proxy 0.529 | `09_external_validation.csv` `auc_IRG3_benchmark_EMTAB4451` | 0.5288 | ✓ |
| 4 | External n=106, 52 deaths | `09_external_validation.csv` `n_validated_samples`/`n_deaths` | 106 / 52 | ✓ |
| 5 | Calibration slope 0.50, intercept −0.04 (CI 0.10–0.90 / −0.43–0.35) | `09_ext_calibration_dca.csv` `calib_slope`/`calib_intercept`/CIs | 0.5028 / −0.0382 / 0.095–0.906 / −0.430–0.354 | ✓ |
| 6 | DCA NB@0.30=0.284, NB@0.50=0.076 | `09_ext_calibration_dca.csv` `nb_thr0.30`/`nb_thr0.50` | 0.2844 / 0.0755 | ✓ |
| 7 | Table-1 HLA-DRB1 −0.89/1.1e-15, CD74 −0.76/2.1e-15, CD14 −0.77/≈0, FCGR3A −0.61/9.1e-11, HAVCR2 −0.35/2.8e-13 | `S01_immunoparalysis_direction.csv` | −0.8925/1.07e-15, −0.7578/2.08e-15, −0.7657/0.0, −0.6097/9.05e-11, −0.3488/2.84e-13 | ✓ |
| 8 | Table-3 concordance IL-7 0.80(4/5), GM-CSF 0.67(4/6), IFN-γ 0.57(4/7), Azithro 0.67(2/3), Lenal 0.40(2/5), Thymα1 0.40(2/5), BCG 0.20(1/5) | `08_candidates_drugs.csv` `rescue_fraction` | 0.8/0.667/0.571/0.667/0.4/0.4/0.2 | ✓ |
| 9 | L1000 lenalidomide rank 5435 (rescue 0.044, z 0.56), azithromycin 9152 (rescue 0.013, z 0.10) | `S08_l1000_candidate_scores.csv` | 5435/0.0439/0.558; 9152/0.0133/0.103 | ✓ |
| 10 | FIS1 logFC +1.26 (t=+17.2) | `S01_mars1_deg.csv` FIS1 row | logFC 1.2614, t 17.157 | ✓ |
| 11 | Consensus immune counts 23 down / 22 FDR<0.05 / 21 both | `S01_immunoparalysis_direction.csv` | 23 / 22 / 21 | ✓ |

All 11 match. The manuscript's numeric claims are faithfully traced to and reconciled with `03_results/*.csv`.

## 5. One-line integrator summary
Manuscript numbers are exact (11/11 recomputed from CSVs), Table 1 is pipe-clean, refs are 40/valid-Vancouver/DOI-complete, and the docx verifies clean (exit 0, 40 refs/10 figs/no MR residue); the one material concern is that the "32/32" audit is inflated by ~9 assertions guarding a *deleted* MR layer and the repo still ships those MR CSVs — relabel/split the audit and quarantine the MR trail before submission.
