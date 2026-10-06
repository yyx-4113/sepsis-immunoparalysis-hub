# A3 — Implementation-track provenance / recomputation audit (round 21, v1.22.0)

**Auditor:** A3 (independent, implementation track)
**Manuscript:** `05_reports/manuscript.md` (tag v1.22.0, commit d507c1c)
**Submission artefact audited:** `07_submission_bmc_v1.21.0/Manuscript.docx` + `BMC_structured_abstract.md`
**Independence statement:** Treated as a first submission. I did **not** open any file under `06_review/` (any round, including `round20_v1.21.0/`), nor `REVIEW_*.md` / `RESPONSE_*.md` / `REVISION_*.md` / `SUBMISSION_MANIFEST.md` / `CITATION.cff`, nor any author-verification statement or other reviewer output. Every headline number below was re-derived from the raw CSVs with managed Python 3.13 (`pandas`/`numpy`/`scipy`/`python-docx`); the manuscript was not trusted.

---

## 1. Recomputation ledger

| # | Claim (as reported) | Recomputed from raw CSV | Source file | Match |
|---|---|---|---|---|
| 1 | 802 samples (760 sepsis / 42 ctrl) | expr.csv header = 803 cols → **802 sample columns**; pheno = **802 rows**, group `{sepsis:760, healthy:42}` | `01_data/GSE65682/GSE65682_expr.csv`, `GSE65682_pheno.csv` | ✅ |
| 2 | Endotype Mars1=132, Mars2=176, Mars3=118, Mars4=53, unassigned=323 | `{Mars1:132, Mars2:176, Mars3:118, Mars4:53, unassigned:323}` | `GSE65682_pheno.csv` (`mars_endotype`) | ✅ |
| 3 | death_28d 114 / 365 / 323 | `{1.0:114, 0.0:365, unassigned:323}` | `GSE65682_pheno.csv` (`death_28d`) | ✅ |
| 4 | 23/25 immune genes directionally down; 22/25 FDR<0.05 sig; 21 both down & sig | n_total=25, down=23, sig(adj.P<0.05)=22, both=21 | `03_results/S01_immunoparalysis_direction.csv` | ✅ |
| 5 | FIS1 logFC +1.26, t ≈ +17.2 | logFC = **1.261433**, t = **17.1567** | `03_results/S01_mars1_deg.csv` (FIS1 row) | ✅ |
| 6 | External locked-L1 AUC 0.585 (95% CI 0.469–0.696) | AUC = **0.5848**, CI = **0.4687–0.6959** | `03_results/09_external_validation.csv` | ✅ (rounds) |
| 7 | Equal-weight sensitivity AUC 0.638 (95% CI 0.532–0.748) | AUC = **0.6382**, CI = **0.5317–0.7475** | `09_external_validation.csv` | ✅ (rounds) |
| 8 | Within-cohort 5-fold CV AUC 0.659 | CV = **0.658558** (≈0.659); train 0.749507 (≈0.750) | `03_results/S06_auc_compare.csv` | ✅ |
| 9 | Calibration slope 0.50 / intercept −0.04 | slope = **0.5028**, intercept = **−0.0382**; slope CI 0.095–0.906; intercept CI −0.43–0.35 | `03_results/09_ext_calibration_dca.csv` | ✅ |
| 10 | DCA net-benefit grid | 18 threshold rows (0.05–0.90); nb_thr0.20=0.3632, nb_thr0.30=0.2844, nb_thr0.50=0.0755 — identical to `09_ext_calibration_dca.csv` columns | `03_results/09_ext_dca_grid.csv` | ✅ |
| 11 | External n = 106, 52 deaths | n_validated=106, n_deaths=52, n_survivors=54 | `09_external_validation.csv` | ✅ |
| 12 | Lenalidomide rank 5435 (26.6%) | rescue_rank=**5435**, pct=**0.26625** | `03_results/S08_l1000_candidate_scores.csv` | ✅ |
| 13 | Azithromycin rank 9152 (44.8%) | rescue_rank=**9152**, pct=**0.44834** | `S08_l1000_candidate_scores.csv` | ✅ |
| 14 | Prednisone 3.2nd percentile (rank 651 / 20,413) | rescue_rank=**651**, pct=**0.03189** = 651/20413 | `03_results/S08_l1000_positive_control.csv` | ✅ |
| 15 | Published IRG benchmark 0.619 | **0.619** (IRG 基准 E-MTAB-4451) | `S06_auc_compare.csv` | ✅ |
| 16 | IRG-3 proxy 0.5288 | **0.5288** (`auc_IRG3_benchmark_EMTAB4451`) | `09_external_validation.csv` | ✅ |
| 17 | ΔAUC vs SRS +0.028, perm P 0.69 | ΔAUC = **+0.0278**, perm P = **0.694** | `03_results/09_ext_benchmark_vs_srs.csv` | ✅ (rounds) |
| 18 | Mars1-vs-Other DEG 3597 (|logFC|≥0.3) | DEG_0.3=True = **3597** | `03_results/S01_mars1_deg.csv` | ✅ |
| 19 | Sepsis-vs-healthy DEG 448 (|logFC|≥0.3) | DEG_0.3=True = **448** | `03_results/S01_deg_sepsis_vs_ctrl.csv` | ✅ |
| 20 | Exactly 40 references, contiguous, all cited, Vancouver-ordered | 40 entries, contiguous 1..40, 0 missing, 0 uncited, first-appearance order == numeric order (0 violations) | `manuscript.md` §References + body | ✅ |

---

## 2. Table 1 markdown / docx integrity (focus #1)

**Method:** opened the built `Manuscript.docx` with python-docx and inspected every `Table` object.

- `docx` contains **4 tables** total: Table 1 (immunoparalysis genes), Table 2 (immune-score by endotype), Table 3 (drug shortlist), and the §7 "Number provenance" table.
- **Table 1** = 9 rows × **4 columns** each. `cols_per_row = [4,4,4,4,4,4,4,4,4]` → perfectly consistent, **no stray empty trailing columns**.
- **Pipe-fragment scan:** zero cells contain a literal `|`. The string `| logFC |` does **not** appear anywhere in the docx.
- Header cells: `['Gene', 'logFC (Mars1−Other)', 'adj.P.Val', 'Function']`; cell contents (e.g. ITGAM/LYZ annotations) are clean, with no unescaped pipes breaking columns.

**Conclusion:** the prior unescaped-`|` leak that previously rendered a 6-column, corrupted table is **gone**. The table renders as a clean, well-formed table with no column corruption.

> **Observation (not a defect):** the review brief anticipated a "clean 5-column table," but the manuscript actually defines Table 1 with **4 columns** (Gene / logFC / adj.P.Val / Function). The 4-column structure is internally correct and free of corruption; the "5-column" expectation in the brief appears to be a stale/inaccurate memory. No fix is required — flagging only so the editor is not surprised by the column count.

---

## 3. Reference integrity (focus #3)

Parsed the References section and every in-text `[N]` citation in the body (pre-References):

- Numbered entries found: **40**; sequence `1,2,…,40` → **contiguous, no gaps, no duplicates**.
- In-text citations: 59 total; unique set = exactly `{1..40}` → **every reference is cited, none uncited**.
- Vancouver ordering: the first-appearance index of each `[N]` is exactly `N−1` (reference 1 cited first, then 2, … 40). **0 ordering violations** → first-appearance order == numeric order, compliant with Vancouver/sequential numbering.
- The docx References section was independently confirmed to contain **40** contiguous entries.

**Conclusion:** reference integrity is fully satisfied.

---

## 4. Structured abstract ↔ manuscript ↔ docx drift (focus #4)

- `BMC_structured_abstract.md` contains: 802, 0.585, 0.469/0.696, 0.638, 0.532/0.748, 0.659, FIS1 1.26, prednisone 3.2nd percentile — all present and matching the manuscript body/abstract.
- The built docx **Abstract** is the structured (Background/Methods/Results/Conclusions) form. Pairwise number alignment between docx-Abstract and manuscript-Abstract:
  - 802 samples ✅ · 0.585 ✅ · 0.469–0.696 ✅ · 0.638 ✅ · 0.532–0.748 ✅ · 0.659 ✅ · FIS1 +1.26 ✅ · prednisone 3.2nd percentile ✅.
- No contradictory restatement of any headline number across the three artefacts. (Minor, non-contradictory rounding: manuscript abstract/§3.5 give IRG-3 proxy "0.529" while the source dataset value is 0.5288 — consistent to 3 sig figs, not a discrepancy.)

**Conclusion:** no abstract↔manuscript↔docx numerical drift.

---

## 5. MR layer genuinely absent (focus #5)

Regex over the full manuscript body (and whole file) for `Mendelian`, `MR-Egger`, `IVW`, `instrument`, `causal` (case-insensitive):

- `Mendelian`: 0 · `MR-Egger`: 0 · `IVW`: 0 · `instrument`: 0 · `causal`: 0 (in body and in whole file).

**Conclusion:** the MR/causal-inference layer is fully removed from the narrative (only the retained `03_results/10_*` CSVs remain as an audit trail, which is expected and benign).

---

## 6. Docx ↔ manuscript number-presence (focus #6)

Extracted full docx text (paragraphs + all table cells) and tested for every key token:

`802` ✅ · `0.585` ✅ · `0.469` ✅ · `0.696` ✅ · `0.638` ✅ · `0.532` ✅ · `0.748` ✅ · `0.659` ✅ · `0.50` ✅ · `−0.04` (Unicode minus) ✅ · `106` ✅ · `52` ✅ · `30` ✅ · `FIS1` ✅ · `1.26` ✅ · `40` (references) ✅.

All tokens present in the built docx and equal the manuscript values.

---

## 7. Defects

**No numeric, structural, or provenance defects were identified in this round.** All 20 recomputed headline claims match their source CSVs to rounding precision, Table 1 renders cleanly with no pipe corruption, references are complete and Vancouver-ordered, the abstract/docx are numerically consistent, the MR layer is absent, and all key tokens are present in the submission artefact.

### Observations / clarifications (not defects)
1. **Table 1 column count = 4, not 5** (see §2). The table is correct and uncorrupted; the brief's "5-column" expectation does not match the manuscript's actual 4-column design.
2. **"top 26.6%" phrasing** (lenalidomide): `rescue_rank 5435 / 20413 = 0.266`, so it sits at the **26.6th percentile from the best end** (i.e. the lower ~26.6% of the library by rescue). The number is internally consistent; the wording is merely slightly ambiguous and could be clarified as "26.6th percentile" to avoid a reader reading it as "top-26.6%-best". This is editorial, not a numeric error.

---

## 8. Stands up (≥3)

1. **End-to-end cohort arithmetic is exact.** Sample count (802), group split (760/42), endotype counts (132/176/118/53/323) and 28-day death split (114/365/323) all recompute exactly from `GSE65682_pheno.csv` — the foundational denominators behind every downstream claim are sound.
2. **External-validation headline numbers are faithfully transported.** Locked-L1 AUC 0.5848 (→0.585), CI 0.4687–0.6959 (→0.469–0.696), equal-weight 0.6382 (→0.638), CI 0.5317–0.7475 (→0.532–0.748), and the optimistic CV 0.6586 (→0.659) all match their CSVs to the third decimal; 106/52 sample/death counts and the 29/30 gene mapping (HLA-DQA1 missing) are also exact.
3. **The drug-repositioning connectivity claims are reproducible.** Lenalidomide 5435/20413 (26.6%), azithromycin 9152/20413 (44.8%) and the prednisone positive-control 651/20413 (3.19%→3.2nd percentile) all rederive exactly from `S08_l1000_candidate_scores.csv` / `S08_l1000_positive_control.csv`.
4. **Document integrity is clean:** Table 1 has no pipe corruption, references are 40/contiguous/all-cited/Vancouver-ordered, the MR layer is fully absent, and the docx embed all key numbers identically to the manuscript.

---

## 9. Questions for the authors

1. Table 1 is 4 columns in both the manuscript markdown and the built docx. The review brief expected 5 — is the 4-column design (Gene / logFC / adj.P.Val / Function) intentional, or was a 5th column (e.g. a "Mars1_down / DEG_0.3" flag) dropped during the v1.20–v1.22 edits? (Not a defect; requesting confirmation only.)
2. For lenalidomide/azithromycin, consider stating the percentile explicitly (e.g. "26.6th percentile of 20,413 compounds") rather than "top 26.6%" to remove ambiguity about direction.
3. The §7 provenance table notes the CV AUC appears as 0.6586 in `S06_auc_compare.csv` and 0.6582 in `09_external_validation.csv` ("rounding artifact"). Both are benign, but could you confirm the two pipelines are intended to differ only by this ~0.0004 and that 0.659 is the reported round value? (Already consistent in the text; just a provenance note.)

---

## 10. What I actually checked

- Recomputed every headline number in the brief (items 1–6 of the focus) directly from raw CSVs: sample/endotype/death counts (`GSE65682_pheno.csv`, `GSE65682_expr.csv` header), immune-gene directionality (23/25/21/22 from `S01_immunoparalysis_direction.csv`), FIS1 statistics (from `S01_mars1_deg.csv`), external AUCs & CIs and IRG-3 proxy (from `09_external_validation.csv`), CV AUC (from `S06_auc_compare.csv`), calibration slope/intercept and DCA grid (from `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`), benchmark ΔAUC vs SRS and perm P (from `09_ext_benchmark_vs_srs.csv`), L1000 candidate and positive-control ranks/percentiles (from `S08_l1000_candidate_scores.csv`, `S08_l1000_positive_control.csv`), and DEG counts 3597 / 448.
- Opened `Manuscript.docx` with python-docx; verified Table 1 has 4 consistent columns, zero literal-pipe fragments, and no empty trailing columns; enumerated all 4 docx tables.
- Parsed the References section and all in-text `[N]` citations for count, contiguity, citation coverage, and Vancouver ordering; independently confirmed 40 docx references.
- Compared `BMC_structured_abstract.md` and the docx Abstract against the manuscript Abstract/body for numerical drift.
- Grepped the manuscript for MR/causal vocabulary (0 hits).
- Scanned the full docx text for the 16 key tokens and confirmed presence/equality.

**Verdict:** Implementation-track recomputation and document-integrity audit passes — no defects found; the manuscript and its v1.21.0 BMC submission artefact are internally consistent and traceable to source data.
