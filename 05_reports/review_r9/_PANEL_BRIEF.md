# Round-9 Independent Review Panel — Brief

**Manuscript:** `05_reports/manuscript.md` (current version **v1.8.0**, commit `180ecb1`)
**Title (working):** "Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning"
**Article type intended:** Research (single-author bioinformatics / translational)
**Repository:** `github.com/yyx-4113/sepsis-immunoparalysis-hub`

## Independence discipline (mandatory)
You have **never seen this manuscript before**. Treat it as a first submission.

**Forbidden to read — under any circumstances:**
- `05_reports/REVIEW_round*.md` (rounds 1–8)
- `05_reports/review/` , `review_r2/` … `review_r8/` (any prior panel output)
- `05_reports/RESPONSE*.md` , `REVISION*.md` , any `author_reply*`
- `05_reports/review_r9/` files written by the other three reviewers
- any `task_status*`, project-overview, `SUBMISSION_MANIFEST.md`, deposit SOP, `author_verification_statement.md`, `generated_references.md`, `journal_targeting.csv`, `reference_doi_audit.csv`

If you are tempted to "check what was said before" — do not. Every judgement must come from text or source data you read **yourself**.

**Allowed to read:**
- `05_reports/manuscript.md` (the whole thing)
- everything under `03_results/` (CSVs, `S0*.csv`, `10_*.csv`, `08*.csv`, `09*.csv`)
- everything under `02_scripts/python/` (especially `check_audit_assertions.py`, `10_genetics_mr.py`, `_recompute_mr_pvalues.py`, `_recompute_table2.py`, `_ext_calibration_dca.py`, `_mr_diagnostics.py`)
- `01_data/GSE65682/GSE65682_pheno.csv` (committed; 802 rows)
- `DATA_SOURCES.md`, `README.md` if relevant to data provenance

## Output contract (every issue MUST have four parts)
- **【Problem】** one sentence
- **【Evidence】** pinned to `file:line`, or `table/section` + exact numbers **that you recomputed yourself**
- **【Why it matters】** concrete effect on conclusions / credibility / acceptance
- **【Specific fix】** a paste-ready English replacement sentence, or an explicit spec for a new analysis (variables, strata, output columns)
- Banned: "consider strengthening the discussion", "the authors may wish to…"

## Also required in every report
- **§ Stands up (≥3, with evidence)** — things you suspected were wrong but verified correct. This is a deliverable.
- **§ Questions for the authors** — state what you need to know; do not guess.
- **§ What I actually checked** — files read, commands run, values recomputed vs the manuscript's, with the discrepancy stated.

## Mandatory recomputation checks (do not trust the manuscript's numbers)
- MR-Egger p-values: recompute as `2*scipy.stats.t.sf(|beta/se|, df=nsnp-2)`. The manuscript claims these now use the t-distribution; verify at least the CD74 (critical-care & susceptibility) and CD14 (28-day death) rows against `10_*.csv` and `10_mr_bh_family.csv`.
- External validation AUC 0.638 (95% CI 0.532–0.748, n=106, 52 deaths) vs L1-locked 0.585 — verify which CSV key holds each and that they are not conflated.
- Hub directions: 5 Mars1-down immune hubs + FIS1 up (logFC +1.26) — verify against `S01_mars1_deg.csv` and `S05_hub_genes.csv`.
- 23/22/21 consensus counts (down / FDR / both) and Table-1 immune-gene logFC/adj.P — verify against `S01_mars1_deg.csv` / `S01_immunoparalysis_*.csv`.
- 08b `rescue_fraction_directional` (1.0/0.833/0.714) vs Table-2 `response_gene_concordance` in `08_candidates_drugs.csv` — confirm both are present and internally consistent or explicitly disambiguated.
- Calibration slope/intercept 0.50/−0.04 and DCA NB values from `09_ext_calibration_dca.csv`.

## Panel roles
- **A1** — Domain (sepsis immunology / immunoparalysis / endotypes / drug repositioning biology)
- **A2** — Design & statistics / causal inference (MR, multiplicity, power, overlap bias, survival/prognosis)
- **A3** — Implementation & provenance audit (numbers ↔ source files, audit-assertion 1–17 fidelity, broken syntax)
- **A4** — Venue / editorial & reporting-compliance (STROBE-MR, Vancouver, data-availability truthfulness, abstract fit)

## Tool-talk prohibition
Do not mention what tools you use. Write review comments only. Use the Write/Edit tool to save your report to the assigned path; do not try to end the whole task.
