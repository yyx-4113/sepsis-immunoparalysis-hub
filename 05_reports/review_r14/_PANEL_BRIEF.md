# Round-14 Independent Blind-Panel Brief — v1.14.0

**Manuscript:** `05_reports/manuscript.md` (tag `v1.14.0`, commit `800063e`)
**Repository:** `github.com/yyx-4113/sepsis-immunoparalysis-hub` (local clone at project root)
**Target journal:** Scientific Reports (Nature Portfolio)
**Article type claimed:** Article (original research) — computational-biology / methods-and-resources; contribution framed as *reproducible pipeline + honest external validation + experimental blueprint*, **not** novel hub-gene discovery.

## Independence discipline (mandatory)
**Forbidden to read (do not open, do not grep, do not summarise):**
- `05_reports/REVIEW_round12_20260927.md`, `05_reports/REVIEW_round13_20260927.md`
- `05_reports/review_r12/` and `05_reports/review_r13/` (all files)
- Any `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`
- `.workbuddy/memory/` (MEMORY.md, daily logs)
- `05_reports/scirep_submission_checklist.md`
- Any other reviewer's output file under `05_reports/review_r14/` while you are writing

Treat this manuscript as a **first submission**. Every judgement must come from text or source data you read and recompute yourself. Any claim you CAN verify, you MUST verify.

## Manuscript's stated claims (for you to test, NOT to trust)
- 5 immune hubs (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) Mars1-down; FIS1 non-immune passenger up (logFC +1.26).
- 30-gene signature: honest external cross-platform AUC **0.638** (95% CI 0.532–0.748; E-MTAB-4451, n=106, 52 deaths); CV AUC **0.659**; L1-locked **0.585**. IRG proxy recomputed **0.529** ("weak reference only; CIs overlap").
- DCA on **calibration-corrected** probabilities; model exceeds treat-all from threshold **≈0.30**, and at 0.80 the model NB is **0.00** while treat-all NB is **−1.55** (they DIVERGE, not converge). Verify against `03_results/09_ext_dca_grid.csv`.
- Calibration: external logistic fit slope **0.50**, intercept **−0.04** (NO 95% CI claimed now — confirm none is stated).
- Mars1 vs Mars2/3/4 P = **0.47 / 1.9e-18 / 1.3e-3**.
- MR primary 28-day death: all IVW **OR 0.92–1.12, P ≥ 0.23**; CD74 critical-care WM flagged (overlap-inflated, reversed); 45-test BH; 27 instruments. NEW: text now notes CD74 & HLA-DQA1 lie in same MHC-II region (LD caveat).
- L1000 rescue ranks: lenalidomide **5435**, azithromycin **9152**.
- HAVCR2/TIM-3 now described as down-regulated = "reduced checkpoint engagement in the immunosuppressed program" (NOT "T-cell exhaustion" per se).
- Nivolumab [34] now described as a Phase-1b safety/pharmacokinetic study not powered for efficacy (NOT "showed no benefit").
- External validation "independent in cohort and platform but **not in label**".

## Source files to verify against (read directly)
- `05_reports/manuscript.md`, `05_reports/cover_letter.md`
- `03_results/09_external_validation.csv`, `09_external_validation_coef.json`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`, `09_ext_dca_grid.csv`
- `03_results/S06_auc_compare.csv`, `S06_signature_genes.csv`
- `03_results/10_genetics_mr.csv`, `10_mr_bh_family.csv`, `10_genetics_mr_harmonised.csv`
- `03_results/S01_mars1_deg.csv`, `S01_immunoparalysis_direction.csv`
- `03_results/S08_l1000_candidate_scores.csv`
- `03_results/S02_immunoparalysis_score.csv`
- `02_scripts/python/09_external_validation.py`, `_ext_calibration_dca.py`, `check_audit_assertions.py` (should run 30 assertions, exit 0; you may run it)

## Output contract (every item needs all four)
- 【Problem】 one sentence
- 【Evidence】 pinned to file:line, or table/section + exact numbers you recomputed
- 【Why it matters】 concrete effect on conclusions / credibility / acceptance
- 【Specific fix】 paste-ready English replacement sentence, or explicit new-analysis spec

## Also required
- § Stands up (≥3, with evidence).
- § Questions for the authors.
- § What I actually checked — files read, computations run, values recomputed vs manuscript, discrepancies stated.

## Tool talk
Do not mention tools; write review comments only. If you cannot read a file, say which and why, but do not end the task.