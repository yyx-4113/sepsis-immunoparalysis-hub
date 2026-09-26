# A3 — Implementation / Provenance / Recompute-audit lens

I treated the manuscript as a first submission and recomputed the load-bearing numbers from raw `03_results/` files. The MR layer is now internally consistent with its data — a major improvement. I found one incorrect stated range and a few provenance gaps.

## Findings

### Tier 1 — A3-1: I² range error (see A2-1; provenance confirmation)
【Problem】 "heterogeneity was low (I² 0.00–0.29)" is false against the data; true max I² = 0.502.
【Evidence】 Direct recomputation from the three MR CSVs: I² values 0.00 (HLA-DQA1 5086) … 0.502 (FIS1 4982 critcare). Manuscript §3.10 line 146 claims 0.00–0.29.
【Why it matters】 A reproducibility gate would catch this; the stated statistic does not match the file. Must be corrected before submission.
【Specific fix】 Same as A2-1: scope to primary outcome + disclose secondary I².

### Tier 2 — A3-2: §2.10 long line should be verified not truncated
【Problem】 The §2.10 methods paragraph is one very long line; an automated gate or future edit could silently drop its tail.
【Evidence】 The line (manuscript line 72) contains the full 45-test BH description and STROBE-MR item 9b text; grep confirms the continuation phrases ("three CD74 tests reached", "STROBE-MR item 9b") are present, so the file is intact, but the structure is fragile.
【Why it matters】 Low risk now; high risk if the file is later edited by line-based tools.
【Specific fix】 Split §2.10's BH paragraph into 2–3 sentences for edit-safety. No content change.

### Tier 2 — A3-3: STROBE-MR harmonisation drop-list is qualitative
【Problem】 The retained-instrument details are given as item 9b disclosure, but the per-SNP exclusion tally (palindromic/dropped) is only "available on request."
【Evidence】 §2.10 (line 72): "a full per-SNP drop-list is available on request."
【Why it matters】 Reproducibility reviewers increasingly expect counts in the paper; "on request" is acceptable but weaker.
【Specific fix】 Report exact counts: e.g., "of N extracted instruments, M retained after harmonisation; K palindromic/strand-ambiguous dropped" per outcome, in a supplementary table or §2.10.

### Tier 3 — A3-4: §7 provenance table references files not spot-checked this round
【Problem】 §7 lists `tier1_summary.txt`, `11_validation_design.md`, etc.; these were not re-verified this round.
【Evidence】 §7 (lines 213–236).
【Why it matters】 Consistency gate only checks enumerated values; a stale path would not be caught.
【Specific fix】 Optional: a CI step that asserts every §7 path exists. No manuscript text change required.

## § Stands up (verified correct by recomputation)
- `10_mr_bh_family.csv` is internally consistent: 45 rows, per-outcome `p_fdr_bh` matches each file's column, 45-test family q matches the three surviving CD74 tests (0, 1.49×10⁻¹¹, 0.0025).
- External AUC 0.6382 / CI 0.5317–0.7475 (`09_external_validation.csv`) → manuscript 0.638 (0.532–0.748) ✓.
- CV AUC 0.6586 → 0.659; train 0.7495 → 0.750 (`S06_auc_compare.csv`) ✓.
- IRG recomputed 0.604 (`09_external_validation.csv`) ✓.
- References: 31 defined, 31 cited, zero orphans (regex check) ✓.
- Banned overclaim phrases ("therapeutically targetable", "可药性", "0.054", "42-test", "four of five", etc.) all absent ✓.

## § Questions for the authors
- Can you add a one-line CI assertion that every §7 provenance path resolves, to prevent path rot?

## § What I actually checked
- Python recomputation of I² range, family-BH q values, external/AUC/IRG from CSVs.
- Reference regex (defined vs cited).
- Banned-phrase residual scan (0 hits).
- Grep-confirmed §2.10 line integrity.
