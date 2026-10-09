# Panel Brief — Independent Review Round 1 (2026-10-09)

**Manuscript under review:** `05_reports/manuscript.md` (v1.24.0) of the repository
`D:/2026.9/极速交付9月会员日优惠套路/05_多组学+虚拟敲除药物发现/方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位/`
A computational-biology / methods-and-resources study on sepsis immunoparalysis.
Working title: *"A reproducible, fully auditable pipeline confirms within-cohort the MARS Mars1 immunoparalysis program and delivers an honest external validation of a 30-gene sepsis prognostic signature."*
Single author: Yongxin Yang. Target venue: **BMC Bioinformatics** (Research article / Methodology article).

## Independence discipline (MANDATORY)

You are reviewing this as if it were a **first submission you have never seen**.

**Forbidden to read** (do not open, do not grep, do not list):
- Any `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `ROUND*.md` anywhere in the repo
- `06_review/` contents other than this brief and your own output file
- `SUBMISSION_MANIFEST.md`, any `*_SOP.md`, `author_verification_statement.md`
- `MEMORY.md`, `.workbuddy/memory/` (project memory)
- Any other expert's output file in this review directory

Do **not** assume the manuscript is mature or has passed prior review. Treat it as a fresh first submission.
Every judgement must come from text or source data **you** read yourself.
Any claim in the manuscript that you **can** verify, you **MUST** verify.

## Output contract (MANDATORY for every issue)

Each item must contain exactly four parts:
- **【Problem】** one sentence
- **【Evidence】** pinned to `file:line`, or `section + exact numbers`; numbers you cite must be ones you recomputed yourself where feasible
- **【Why it matters】** concrete effect on conclusions / credibility / acceptance
- **【Specific fix】** a paste-ready English replacement sentence, or an explicit spec for a new analysis (variables, strata, output columns)

Banned: "consider strengthening the discussion", "the authors may wish to…", vague suggestions. Every fix must be actionable.

## Also required in your report

1. **§ Stands up (≥3, with evidence)** — explicitly mark things you suspected were wrong but found to be CORRECT. This is a deliverable, not filler.
2. **§ Questions for the authors** — state what you need to know; do not guess answers.
3. **§ What I actually checked** — files read, commands run, values recomputed vs the manuscript's, with the discrepancy (or "no discrepancy") stated explicitly.

## Environment notes for recomputation

The recomputation venv (numpy/pandas/scipy/python-docx already installed):
`C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe`

Key source files you may (and should) read and recompute against:
- `03_results/S01_immunoparalysis_direction.csv` (immune-gene direction, logFC, adj.P)
- `03_results/S01_mars1_deg.csv`, `S01_deg_sepsis_vs_ctrl.csv`
- `03_results/S02_immunoparalysis_score.csv` (immune-function score by endotype)
- `03_results/S05_hub_genes.csv` (hub selection)
- `03_results/S06_signature_genes.csv`, `S06_auc_compare.csv` (CV/training AUC)
- `03_results/09_external_validation.csv`, `09_external_validation_coef.json` (external AUC + coef)
- `03_results/09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv` (calibration slope/intercept, DCA)
- `03_results/08_candidates_drugs.csv`, `08b_clinical_translation.csv`
- `03_results/S08_l1000_candidate_scores.csv`, `S08_l1000_positive_control.csv`, `S08_l1000_rescue_trtcp.csv` (LINCS ranks)
- `03_results/11_validation_design.md`
- `04_figures/*.png` (figures)

The large raw inputs (`01_data/`) are gitignored; do not expect them. The processed matrices above are the authoritative result tables.

## Forbidden in your output
- Do not mention what tools/agents you used. Write review comments only.
- Do not write to any file other than your assigned `<codename>_<role>.md`.
