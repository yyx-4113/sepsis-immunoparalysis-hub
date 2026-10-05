# Panel Brief — Round 19 (manuscript v1.20.0)

## What is under review
A single-author computational-biology / methods-and-resources manuscript titled
(roughly) *"A reproducible multi-omics pipeline confirms the MARS Mars1
immunoparalysis program and prioritises in-silico knockdown-repositionable
immune hubs in sepsis."* Repository: `github.com/yyx-4113/sepsis-immunoparalysis-hub`,
tag **v1.20.0**. Target venue: **BMC Medical Genomics** (article type: Research
article / Methods & Resources). The manuscript has been REFRAMED as a
confirm/validate computational paper after its Mendelian-randomisation layer was
removed (the MR layer was Tier-3, fully null, and is gone from v1.20.0 — do not
expect or hunt for MR content; if you find MR residue, flag it as a stale-text
defect, not a methodological gap).

## The manuscript's actual claims (read the text yourself to verify; this is only orientation)
- Mars1 endotype (immunoparalysis) carries a coherent immunosuppressed transcriptome (§3.1).
- An immune-function score is lowest in Mars1 (§3.2).
- Five immune hubs — CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2 (all Mars1-down) — plus one
  co-expression passenger FIS1 (Mars1-up, mitochondrial-fission, non-immune) (§3.3).
- A 30-gene immune-risk signature is associated with 28-day mortality; external AUC 0.638
  (E-MTAB-4451, n=106), locked L1-penalty AUC 0.585; a second external cohort AUC 0.659 (n=52) (§3.4–3.5).
- Cellular context from single-cell (§3.6), LINCS L1000 reverse-connectivity drug repositioning (§3.7, §3.9).
- Honest Limitations 1–10; experimental-validation blueprint in S11.

## Independence discipline (MANDATORY)
Forbidden to read: any `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, prior
`_gen_*.py` outputs, `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`,
`author_verification_statement.md`, and **other reviewers' `.md` files in this
directory** (`A1_*.md`, `A2_*.md`, `A3_*.md`, `A4_*.md`). Also forbidden:
reading the project overview / memory files. Treat this as a FIRST submission.
Do NOT assume the manuscript is mature or has passed prior review. Every judgement
must come from text or source data you read yourself. Any claim you CAN verify,
you MUST verify (recompute from raw/results files, not from the manuscript's own
restated numbers).

## Output contract (every item needs all four)
- 【Problem】 one sentence.
- 【Evidence】 pinned to `file:line`, or `table/section` + exact numbers; numbers
  you cite must be ones you recomputed yourself (state the command/file).
- 【Why it matters】 concrete effect on conclusions / credibility / acceptance.
- 【Specific fix】 a paste-ready English replacement sentence, or an explicit spec
  for a new analysis (variables, strata, output columns).
"Consider strengthening the discussion" is banned.

## Also required in your report
- § Stands up (≥3, with evidence) — things you suspected but found correct. Deliverable, not filler.
- § Questions for the authors — what you need to know; do not guess answers.
- § What I actually checked — files read, commands run, values recomputed vs the
  manuscript, with the discrepancy stated (or "no discrepancy").

## Source data you MAY read (mandatory recompute targets)
- Manuscript: `05_reports/manuscript.md`
- Results CSVs: `03_results/` — especially `S01_mars1_deg.csv`, `S01_immunoparalysis_direction.csv`,
  `S05_hub_genes.csv`, `S06_auc_compare.csv`, `S06_signature_genes.csv`, `S02_immunoparalysis_score.csv`,
  `S09_external_validation.csv`, `S09_ext_dca_grid.csv`, `S09_ext_calibration_dca.csv`,
  `S08_l1000_*.csv`, `S07_hub_celltype.csv`, `S09_ext_risk_scores.csv`.
- Phenotype file (if present on disk): `01_data/` (note: gitignored, may be large);
  `GSE65682_pheno.csv` should be force-added in the repo root or under 01_data.
- Figures: `04_figures/`.
- Python (managed venv): `C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe`
  (use for any recompute; pandas/numpy/scipy/sklearn available).

## Forbidden tool talk
Do not mention what tools you use. Write review comments only. Write your report
with the Write tool to `06_review/round19_v1.20.0/<codename>_<role>.md`.
