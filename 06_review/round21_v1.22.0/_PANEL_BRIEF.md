# Round-21 independent review panel — sepsis immunoparalysis hub + in-silico repositioning (v1.22.0)

## Manuscript under review
- File: `05_reports/manuscript.md` (repository root = project dir; tag `v1.22.0`, commit `d507c1c`).
- Title: "A reproducible, fully auditable pipeline confirms within-cohort the MARS Mars1 immunoparalysis program and delivers an honest external validation of a 30-gene sepsis prognostic signature"
- Article type claimed: **Research article** (BMC Medical Genomics); framed as a computational-biology / methods-and-resources *study* whose contribution is a reproducible pipeline + honest external validation + experimental blueprint, NOT novel hub-gene discovery.
- Core claims to stress-test:
  1. Five immune hubs (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2/TIM-3) "confirm within-cohort" the established MARS Mars1 antigen-presentation program (a within-cohort confirmation, NOT an independent replication — the Mars1 labels originate from the MARS consortium's own clustering of the same GSE65682 cohort).
  2. A 30-gene immune-risk signature: **locked-L1 external transport AUC 0.585** (pre-specified **primary**, honest out-of-sample, CI 0.469–0.696 includes 0.5) and **equal-weight oriented-sum AUC 0.638** (pre-specified **sensitivity**); within-cohort CV AUC 0.659 (optimistic); benchmark 0.619.
  3. Drug repositioning: 7 immune-modulating agents **annotated as hypothesis-generating candidates rather than prioritised by significance**; curated immune-response concordance ≤ study's own 0.84 background; **no agent cleared the LINCS L1000 positive-control gate** (prednisone ranked 3.2nd percentile); connectivity screen non-discriminating.
  4. FIS1: a **non-immune, erythroid/heme-module gene** (logFC +1.26, Mars1-up), co-selected with the immune hubs; carries a significant independent 28-day-death association (OR 1.34 per SD, 95% CI 1.08–1.66, p = 0.00735).
  5. Data: re-analysis of public GSE65682 (802 samples: 760 sepsis, 42 controls) + external E-MTAB-4451 (n=106, 52 deaths). Public research data, no new primary data.
- Removed layer: the Tier-3 Mendelian-randomisation analysis was removed at v1.20.0 (MR CSVs retained only as an audit trail proving it was genuinely null). Treat MR as absent from the manuscript.
- Prior round: Round-20 (on v1.21.0) found NO desk-reject; all Tier-1 blocking items were fixed in v1.22.0. **Do NOT read the Round-20 report or any prior review file** — treat this as a first submission.

## Independence discipline (MANDATORY)
- **Forbidden to read**: any file under `06_review/` (all prior rounds, including `round20_v1.21.0/` and `REVIEW_round20_2026-10-07.md`), `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `SUBMISSION_MANIFEST.md`, `CITATION.cff`, `author_verification_statement.md`, and — critically — **each other reviewer's output files in this directory (`06_review/round21_v1.22.0/`)**.
- Do NOT assume the manuscript is mature or has passed previous review. Treat it as a **first submission**.
- Every judgement must come from text or source data you read yourself. Any claim you CAN verify, you MUST verify.
- The manuscript's own audit (`02_scripts/python/check_audit_assertions.py`, 32 assertions) is green — that proves arithmetic/provenance, NOT design soundness. Your job is the design and reporting layer.

## Source data locations (read these; recompute, do not trust)
- `03_results/S01_*.csv` — DEG / immunoparalysis direction / Mars1 DEG
- `03_results/S05_hub_genes.csv` — hub selection
- `03_results/S06_auc_compare.csv`, `S06_hub_death_association.csv`, `S06_signature_genes.csv` — signature AUC / hub death association
- `03_results/09_external_validation.csv`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`, `09_ext_benchmark_vs_srs.csv` — external validation, calibration, DCA
- `03_results/08_candidates_drugs.csv`, `08_positive_control_check.csv`, `08b_clinical_translation.csv`, `S08_l1000_*.csv` — repositioning / L1000
- `03_results/11_validation_design.md` — experimental blueprint
- `04_figures/` — the 10 figures (Fig_S1, Fig_S2, Fig_S3A/B, Fig_S6A/B/C, Fig_S7, Fig_S9, Fig_S10)
- `07_submission_bmc_v1.21.0/` — built Manuscript.docx / Supporting_Information.docx / Cover_Letter_BMC.md / BMC_structured_abstract.md (you MAY inspect the built docx as the submission artefact, but verify against the markdown source)

## Output contract (mandatory for every item)
- 【Problem】 one sentence.
- 【Evidence】 pinned to file:line, or table/section + exact numbers; numbers you cite must be ones you recomputed yourself.
- 【Why it matters】 concrete effect on conclusions / credibility / acceptance.
- 【Specific fix】 a paste-ready English replacement sentence, or an explicit spec for a new analysis (variables, strata, output columns).
"Consider strengthening the discussion" is banned.

## Also required
- § Stands up (≥3, with evidence) — things you suspected but found correct.
- § Questions for the authors — state what you need to know; do not guess answers.
- § What I actually checked — files read, commands run, values recomputed vs the manuscript, with the discrepancy stated.

## Tool-talk forbidden
Do not mention what tools you use; write review comments only. Write your report with the Write/Edit tool to `<this_dir>/<codename>_<role>.md` (do not try to end the whole task).
