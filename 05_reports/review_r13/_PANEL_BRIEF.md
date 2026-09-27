# Round-13 Independent Blind-Panel Brief — v1.13.0

**Manuscript:** `05_reports/manuscript.md` (tag `v1.13.0`, commit `0f7f907`)
**Repository:** `github.com/yyx-4113/sepsis-immunoparalysis-hub` (local clone at project root)
**Target journal:** Scientific Reports (Nature Portfolio)
**Article type claimed:** Article (original research) — computational-biology / methods-and-resources; contribution framed as *reproducible pipeline + honest external validation + experimental blueprint*, **not** novel hub-gene discovery.

## Independence discipline (mandatory)
**Forbidden to read (do not open, do not grep, do not summarise):**
- `05_reports/REVIEW_round12_20260927.md`
- `05_reports/review_r12/` (all files)
- Any `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md` in the repo
- `.workbuddy/memory/` (MEMORY.md, daily logs)
- `05_reports/scirep_submission_checklist.md` (it is a prior-round gate summary; avoid to prevent anchoring)
- Any other reviewer's output file in `05_reports/review_r13/` while you are writing

Treat this manuscript as a **first submission**. Do not assume it is mature or has passed previous review. Every judgement must come from text or source data you read and recompute yourself. Any claim you CAN verify, you MUST verify.

## Manuscript's stated claims (for you to test, NOT to trust)
- 5 immune hubs (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) are Mars1-down-regulated; FIS1 is a non-immune co-expression passenger up-regulated (logFC +1.26).
- 30-gene immune-risk signature: honest external cross-platform AUC **0.638** (95% CI 0.532–0.748; E-MTAB-4451, n=106, 52 deaths); optimistic within-cohort CV AUC **0.659** (label-informed); L1-locked external AUC **0.585**.
- IRG benchmark: Peng et al. reported **0.619** on this cohort; a 3-gene IRG proxy recomputed here was **0.529** (near-random, weak lower-bound reference only).
- Calibration: external logistic fit slope **0.50**, intercept **−0.04**; AUC 0.638; DCA computed on **calibration-corrected probabilities**.
- Mars1 vs Mars2/3/4 Mann–Whitney P = **0.47 / 1.9e-18 / 1.3e-3**.
- MR (primary 28-day death, 15 tests): all IVW **OR 0.92–1.12, P ≥ 0.23**; CD74 critical-care weighted-median flagged (overlap-inflated, reversed direction); 45-test family BH; 27 instruments; consensus immune counts 23/22/21.
- L1000 rescue ranks: lenalidomide **5435**, azithromycin **9152**.
- External validation described as "independent in cohort and platform but **not in label**".

## Source files to verify against (read directly)
- `05_reports/manuscript.md` (the manuscript)
- `03_results/09_external_validation.csv` (AUC, CI, n, calibration)
- `03_results/09_external_validation_coef.json` (L1 coefficients / zero-coef genes)
- `03_results/09_ext_calibration_dca.csv`, `03_results/09_ext_dca_grid.csv`
- `03_results/S06_auc_compare.csv`, `03_results/S06_signature_genes.csv`
- `03_results/10_genetics_mr.csv`, `03_results/10_mr_bh_family.csv`, `03_results/10_genetics_mr_harmonised.csv`
- `03_results/S01_mars1_deg.csv`, `03_results/S01_immunoparalysis_direction.csv`
- `03_results/S08_l1000_candidate_scores.csv`
- `03_results/S02_immunoparalysis_score.csv` (Mars1 stratification P values)
- `02_scripts/python/09_external_validation.py`, `02_scripts/python/_ext_calibration_dca.py` (or equivalent DCA script), `02_scripts/python/check_audit_assertions.py` (29 assertions)
- `05_reports/cover_letter.md` (check consistency with manuscript)

## Output contract (every item needs all four)
- 【Problem】 one sentence
- 【Evidence】 pinned to file:line, or table/section + exact numbers you recomputed
- 【Why it matters】 concrete effect on conclusions / credibility / acceptance
- 【Specific fix】 paste-ready English replacement sentence, or explicit new-analysis spec

## Also required in your report
- § Stands up (≥3, with evidence) — claims you suspected but found correct.
- § Questions for the authors.
- § What I actually checked — files read, commands/computations run, values recomputed vs manuscript, with discrepancies stated.

## Tool talk
Do not mention what tools you use; write review comments only. If you cannot read a file, say which file and why, but do not end the task — continue with what you can verify.
