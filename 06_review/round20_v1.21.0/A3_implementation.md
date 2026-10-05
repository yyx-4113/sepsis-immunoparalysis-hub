# Independent provenance / recomputation audit — Implementation track (A3)

**Manuscript:** `05_reports/manuscript.md` (v1.21.0, title *"A reproducible pipeline recapitulates the MARS Mars1 immunoparalysis program within-cohort and externally evaluates a 30-gene sepsis prognostic signature"*)
**Submission artefact audited:** `07_submission_bmc_v1.21.0/Manuscript.docx` (+ `BMC_structured_abstract.md`)
**Auditor stance:** first-submission review. I did **not** read `06_review/` prior rounds, `REVIEW_*.md`, `RESPONSE_*.md`, `author_verification_statement.md`, or the other reviewers' files in this directory. Every headline number below was re-derived from the raw/source CSVs with pandas/numpy/scipy, not trusted from the manuscript.

---

## What I actually checked

**Files read (source + artefact only):**
- `05_reports/manuscript.md` (full)
- `07_submission_bmc_v1.21.0/BMC_structured_abstract.md`, `07_submission_bmc_v1.21.0/Manuscript.docx` (text extracted via python-docx)
- `01_data/GSE65682/GSE65682_pheno.csv`, `01_data/GSE65682/GSE65682_expr.csv` (header)
- `03_results/S01_immunoparalysis_direction.csv`, `S01_mars1_deg.csv`, `S01_deg_sepsis_vs_ctrl.csv`
- `03_results/S05_hub_genes.csv`
- `03_results/09_external_validation.csv`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`, `09_ext_benchmark_vs_srs.csv`
- `03_results/S06_auc_compare.csv`
- `03_results/S08_l1000_candidate_scores.csv`, `S08_l1000_positive_control.csv`
- `03_results/10_genetics_mr.csv`, `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, `10_mr_bh_family.csv`

**Commands run:** Python (pandas/numpy/scipy) recomputation of every headline number; markdown table-pipe integrity scan; in-text `[N]` vs reference-list reconciliation; docx↔manuscript number-presence and table-render check.

**Recomputed-vs-manuscript discrepancy summary:** *No numeric discrepancies were found in any headline figure.* Every reported value traces to its cited CSV. The only defects are (1) a broken markdown table that also corrupted the built docx, and (2) a nuance in the MR audit-trail minimum p-value versus the review brief's stated expectation.

---

## Recomputation ledger (every headline number re-derived)

| # | Manuscript claim | Recomputed from source | Source | Match |
|---|---|---|---|---|
| 1 | 802 samples; 760 sepsis / 42 ctrl | pheno rows=802; `group`: sepsis 760, healthy 42 | `GSE65682_pheno.csv` | ✅ |
| 2 | 11,519 genes × 802 samples | expr gene rows=11,519; sample cols=802 | `GSE65682_expr.csv` | ✅ |
| 3 | endotypes Mars1=132, Mars2=176, Mars3=118, Mars4=53, unassigned=323 | `mars_endotype` value_counts identical | `GSE65682_pheno.csv` | ✅ |
| 4 | death_28d 114/365/323 | `death_28d` value_counts identical | `GSE65682_pheno.csv` | ✅ |
| 5 | 23/25 directionally down; 22/25 significant (incl. PDCD1 up); 21 down & significant | down=23; adj.P<0.05=22; down&sig=21 | `S01_immunoparalysis_direction.csv` | ✅ |
| 6 | 5 hubs (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) all Mars1-down; FIS1 up | 5 hubs direction Mars1_down; FIS1 logFC=1.2614, t=17.16 | `S01_immunoparalysis_direction.csv`, `S01_mars1_deg.csv`, `S05_hub_genes.csv` | ✅ |
| 7 | FIS1 logFC +1.26, t=+17.2 | 1.2614 / 17.1567 | `S01_mars1_deg.csv` | ✅ |
| 8 | sepsis-vs-healthy DEG 448 (|logFC|≥0.3) | 448 | `S01_deg_sepsis_vs_ctrl.csv` | ✅ |
| 9 | Mars1-vs-Other DEG 3597 (|logFC|≥0.3) | 3597 | `S01_mars1_deg.csv` | ✅ |
| 10 | external locked-L1 AUC 0.585 (CI 0.469–0.696) | 0.5848; CI 0.4687–0.6959 | `09_external_validation.csv` | ✅ |
| 11 | equal-weight AUC 0.638 (CI 0.532–0.748) | 0.6382; CI 0.5317–0.7475 | `09_external_validation.csv` | ✅ |
| 12 | within-cohort CV AUC 0.659 (train 0.750) | 0.6586 (S06) / 0.6582 (09); train 0.7495 | `S06_auc_compare.csv`, `09_external_validation.csv` | ✅ |
| 13 | calibration slope 0.50 (CI 0.10–0.91), intercept −0.04 (CI −0.43–0.35), p_slope=0.016 | slope 0.5028, CI 0.095–0.906; intercept −0.0382, CI −0.430–0.354; p=0.01575 | `09_ext_calibration_dca.csv` | ✅ |
| 14 | DCA NB ≈0.36@0.20, 0.28@0.30, 0.08@0.50 | nb_thr0.20=0.3632, 0.30=0.2844, 0.50=0.0755 | `09_ext_calibration_dca.csv` | ✅ |
| 15 | DCA model exceeds treat-all from ≈0.30; margins 0.01–0.09 (0.30–0.50), 0.17–1.05 (0.55–0.75), 1.55–4.09 (0.80–0.90) | model−treat_all: 0.30→0.0122, 0.50→0.0944; 0.55→0.1667, 0.75→1.0471; 0.80→1.5472, 0.90→4.0943; model> treat_all first at 0.30 (equal at 0.25) | `09_ext_dca_grid.csv` | ✅ |
| 16 | E-MTAB-4451 n=106, 52 deaths | 106 / 52 / 54 | `09_external_validation.csv` | ✅ |
| 17 | lenalidomide rank 5,435/20,413 (26.6%); azithromycin 9,152/20,413 (≈median) | 5435 (pct 0.26625); 9152 (pct 0.44834) | `S08_l1000_candidate_scores.csv` | ✅ |
| 18 | prednisone 3.2nd percentile (rank 651/20,413) | pct_rank 0.03189 → 3.2nd; rank 651 | `S08_l1000_positive_control.csv` | ✅ |
| 19 | IRG-3 benchmark 0.5288 | 0.5288 (text rounds to 0.529) | `09_external_validation.csv` | ✅ |
| 20 | ΔAUC vs SRS +0.028, perm P 0.69; SRS1 24/37=64.9%, SRS2 28/69=40.6% | +0.0278, perm 0.694; 24/37=0.649, 28/69=0.406 | `09_ext_benchmark_vs_srs.csv` | ✅ |

---

## Issues

### Issue 1 — Broken Table 1 markdown (unescaped `|`) corrupts both source and built docx

【Problem】 Table 1 in the manuscript contains unescaped vertical-bar characters inside the ITGAM and LYZ function cells: the text reads `…below the \`|logFC| ≥ 0.3\` DEG fold-change threshold…`. The literal `|` breaks the markdown table (the cell should be 4 columns but renders with 6). This is not cosmetic: the break propagated into the submission artefact.

【Evidence】
- Source: `manuscript.md:77` (ITGAM row) and `manuscript.md:80` (LYZ row) — each has 7 pipe characters instead of the header's 5.
- Artefact: `Manuscript.docx` Table 0 ("immune genes") is rendered with **6 columns** (two stray empty trailing columns) and the visible fragment ` | logFC | ≥ 0.3 ` inside the ITGAM/LYZ Function cells (confirmed via python-docx: every row shows ` |  | ` trailing empties). The renderer did not treat the code-span pipe as protected.

【Why it matters】 A reviewer or journal production pipeline that re-parses the markdown will see a malformed table; the built BMC docx already ships with two empty columns and a literal `| logFC |` in two cells. This is exactly the kind of "broken markdown table syntax" the brief asked me to find, and it is visible to readers of the submitted docx.

【Specific fix】 Remove the pipes from those two cells (the column is already labelled `logFC (Mars1−Other)`). Paste-ready replacement for `manuscript.md:77` and `manuscript.md:80`:
```
| ITGAM | −0.21 | 1.7e-03 | integrin αM (significant at FDR<0.05, adj.P=1.7×10⁻³, but below the 0.3 logFC fold-change DEG threshold, DEG_0.3=False) |
| LYZ   | −0.26 | 3.6e-06 | lysozyme (significant at FDR<0.05, adj.P=3.6×10⁻⁶, but below the 0.3 logFC fold-change DEG threshold, DEG_0.3=False) |
```
Then **rebuild** `Manuscript.docx` from the corrected markdown (the artefact currently still carries the 6-column corruption).

---

### Issue 2 — MR audit trail: stated "min IVW P ≥ 0.23" is not met across all 15 primary tests (actual minimum 0.133)

【Problem】 The review brief expected `min IVW P ≥ 0.23` as confirmation of a genuine null. Recomputation shows the minimum primary IVW p across the 15 primary tests (5 genes × 3 outcomes; FCGR3A excluded — "insufficient_instruments") is **0.133354** (CD74 → critical-care, outcome 4982), below 0.23. The threshold is met only if restricted to the susceptibility (4980) outcome, whose minimum IVW p is 0.301.

【Evidence】
- `10_mr_bh_family.csv`: `family_role == primary` → 15 rows. Primary IVW p-values: 4980 → {0.591, 0.465, 0.776, 0.301, 0.459}; 5086 → {0.752, 0.342, 0.289, 0.855, 0.496}; 4982 → {0.133, 0.568, 0.180, 0.799, 0.533}. Minimum = 0.133354 (line for `CD74,IVW,4982_criticalcare`).
- Recomputed min within susceptibility outcome only = 0.301009 (HAVCR2).

【Why it matters】 This is **not** a faked-null problem — every one of the 15 primary IVW tests is far from significance (none < 0.05), 0/15 are family-significant (all `sig_15test_q05 == no`, BH q ≥ 0.806), and the SE/p-values are internally consistent (Issue 3 below). The trail is honest. But the brief's stated "≥0.23" figure cannot be confirmed from the data and should not be quoted as the summary statistic; the audit-trail note should state the actual minimum (0.13 across all outcomes, 0.30 within susceptibility).

【Specific fix】 If an audit-trail summary sentence exists (or is added) for the retained MR CSVs, replace any "all IVW p ≥ 0.23" wording with the accurate statement, e.g.: *"All 15 primary IVW tests were non-significant (minimum p = 0.13, CD74→critical-care; minimum within the susceptibility outcome p = 0.30); 0/15 survived BH correction at q<0.05."*

---

### Issue 3 — Observation (non-defect): one MR-Egger *sensitivity* test is nominally significant

【Problem】 Within the retained MR CSVs, the CD14 → 28-day-death MR-Egger estimate is nominally significant at p = 0.0488 (`10_genetics_mr_outcome5086_28ddeath.csv:9`). This is a *sensitivity* (Egger) row, not a primary IVW test, so it does not violate "0 family-significant under 15-test primary". I flag it only so the audit trail is read correctly.

【Evidence】 `10_genetics_mr_outcome5086_28ddeath.csv:9` — CD14 MR-Egger: beta=−0.0988, se=0.0353, df=4 (t(4)), reported p=0.04881. Recomputed two-sided t(4) p from beta/se = 0.0488 — **internally consistent**, so the value is real, not an arithmetic error. Egger intercept p = 0.344 (no pleiotropy signal). All other Egger p-values across all three outcomes were independently recomputed against their declared `p_refdist` t(df) and matched exactly (e.g., CD74 4980 Egger p=0.16517, HAVCR2 4980 Egger p=0.18989, CD14 4982 Egger p=0.15566, etc.).

【Why it matters】 Confirms the Egger p-values are genuinely t-distribution-derived (the brief's "Egger p via t-distribution" check **passes**). The single p≈0.049 Egger is best read as play-of-chance across many sensitivity tests and as supporting the overall null; it should not be elevated into a causal claim (and MR is correctly removed from the manuscript body — 0 occurrences of "Mendelian"/"MR-Egger"/"IVW"/"instrument"/"causal" in `manuscript.md`).

【Specific fix】 No change required. If the audit-trail note is expanded, it may optionally state: *"One of the 15 × 3-method MR-Egger sensitivity tests (CD14 → 28-day death) was nominally significant at p=0.049; this is a non-primary sensitivity analysis and is consistent with chance given the multiple sensitivity tests performed."*

---

## Reference integrity (all checks PASS)

【Problem】 None. Verify (a) contiguous 1..38, (b) every in-text `[N]` maps, (c) no uncited reference, (d) first-appearance order = numeric order; spot-check ImmunoSep, Yoon-2003 FIS1, Yang-2013 TIM-3.

【Evidence】
- `manuscript.md` References section parsed: 38 entries, numbers = `[1..38]` exactly contiguous.
- In-text `[N]` scan: min=1, max=38; **cited-not-in-list = []**, **listed-but-never-cited = []**.
- First-appearance order of citations == numeric order (no out-of-order pairs).
- Spot-checks: ref [30] = Giamarellos-Bourboulis et al. 2025 (ImmunoSep) — cited at `manuscript.md:130` ("Giamarellos-Bourboulis et al. [30]"). Ref [20] = Yoon et al. 2003 (hFis1) — cited at `manuscript.md:101` ("FIS1 — a mitochondrial-fission protein (Yoon et al. [20])"), correctly placed at the FIS1 claim. Ref [17] = Yang et al. 2013 (TIM-3) — cited at `manuscript.md` (§3.1) in the sentence *"…reported in a human severe-sepsis PBMC cohort by Yang et al. [17]"*, correctly placed at a TIM-3 statement.

---

## Structured abstract ↔ manuscript ↔ docx drift (all checks PASS)

【Problem】 None material. The docx abstract is generated from `BMC_structured_abstract.md`; verify it matches the manuscript English abstract (line 14) and body, and flag any number present in one but contradictory in another.

【Evidence】
- `BMC_structured_abstract.md` Results: "five immune hubs … FIS1 (logFC +1.26, up-regulated)"; "AUC 0.585 (95% CI 0.469–0.696)"; "AUC 0.638 (95% CI 0.532–0.748)"; "within-cohort cross-validated AUC was 0.659"; "prednisone ranked in the 3.2nd percentile" — all identical to `manuscript.md:14` (English abstract) and to the body (§3.3/§3.4/§3.5).
- Docx text extraction: title matches `manuscript.md:1` exactly; all headline numbers (802/760/42, 0.585, 0.469, 0.696, 0.638, 0.532, 0.748, 0.659, 0.50, −0.04, 106, 52, 5435, 9152, 3.2, 0.529, 23, 1.26, 0.84) are present in the docx and equal the manuscript. Declarations present in docx: Competing interests ("no competing interests"), Funding ("received no specific grant"), Ethics ("no additional IRB"), Data availability, Code availability.
- Second-occurrence drift scan: the three key AUCs appear multiple times each (0.659 ×6, 0.585 ×7, 0.638 ×14) and **all with the identical value** — no contradictory restatements. (The only place a 4-decimal value 0.5288 exists is the CSV; the text consistently rounds to 0.529 — acceptable.)

---

## § Stands up (verified, with evidence)

1. **Sample / phenotype provenance is exact.** 802 total = 760 sepsis + 42 controls; endotype and death splits match `GSE65682_pheno.csv` exactly (`manuscript.md:31` ↔ `GSE65682_pheno.csv`).
2. **The immune-consensus numbers are arithmetically exact and self-consistent.** 23 directionally down / 22 significant (incl. PDCD1 up) / 21 down-and-significant recompute exactly from `S01_immunoparalysis_direction.csv`; 21/25 = 0.84 is the same "background" cited in §3.7/§3.9.
3. **External validation + calibration + DCA are fully reproducible from the cited CSVs.** AUCs 0.585/0.638/0.659, every CI, the 0.50/−0.04 calibration pair (p=0.0158), and the entire DCA grid (model first exceeds treat-all at 0.30; margins 0.01–0.09 / 0.17–1.05 / 1.55–4.09) all match `09_external_validation.csv`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`.
4. **L1000 ranks and IRG-3 benchmark trace.** lenalidomide 5435 (26.6%), azithromycin 9152 (44.8%), prednisone 3.2nd percentile (rank 651/20,413), IRG-3 = 0.5288 — all match `S08_l1000_candidate_scores.csv`, `S08_l1000_positive_control.csv`, `09_external_validation.csv`.
5. **Reference list is clean and order-correct** (38 contiguous, all cited, order = appearance).
6. **MR layer is genuinely gone from the manuscript** (0 mentions) and the retained CSVs are an honest null audit trail (0/15 primary significant; Egger p-values t-distribution-consistent).

---

## § Questions for the authors

1. **MR audit-trail minimum p:** The review brief anticipated `min IVW P ≥ 0.23`, but the minimum across the 15 primary tests is 0.133 (CD74 → critical-care). Is "0.23" a mis-statement, or was it meant to refer only to the susceptibility outcome (min 0.301)? Please confirm the audit-trail summary states the actual minimum.
2. **Table 1 / docx rebuild:** After fixing the unescaped `|` in `manuscript.md:77,80`, please confirm `Manuscript.docx` is regenerated — the currently-built docx still carries the 6-column corruption with a visible `| logFC |` fragment.
3. **CD14 MR-Egger 5086 (p=0.049):** Acknowledged as a non-primary sensitivity result; no action needed unless you intend to mention it in the retained-trail note.

---

## Bottom line

The implementation is, with one exception, a clean and fully reproducible provenance job: **every headline number re-derives exactly from its cited CSV, the docx/abstract/body show no numeric drift, and the reference list is flawless.** The single hard defect is a **broken markdown table (unescaped pipe in Table 1) that has already leaked into the submitted docx** and must be fixed and rebuilt. The MR audit trail is honest (genuinely null), with only a wording nuance around the "≥0.23" minimum-p statement to reconcile. No faked numbers, no second-occurrence drift, no hidden MR claims were found.
