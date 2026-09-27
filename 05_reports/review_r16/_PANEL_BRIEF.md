# Round-16 Independent Blind-Panel Brief — v1.16.0

**Manuscript:** `05_reports/manuscript.md` (tag `v1.16.0`, commit `1212f7b`)
**Repository:** `github.com/yyx-4113/sepsis-immunoparalysis-hub` (local clone at project root)
**Target journal:** Scientific Reports (Nature Portfolio)
**Article type claimed:** Article (original research) — computational-biology / methods-and-resources; contribution framed as *reproducible pipeline + honest external validation + experimental blueprint*, **not** novel hub-gene discovery.

## Independence discipline (mandatory)
**Forbidden to read (do not open, do not grep, do not summarise):**
- `05_reports/REVIEW_round*.md` (all prior rounds)
- `05_reports/review_r12/`, `review_r13/`, `review_r14/`, `review_r15/` (all files)
- `.workbuddy/memory/` (MEMORY.md, daily logs)
- `05_reports/scirep_submission_checklist.md`
- Any other reviewer's output file under `05_reports/review_r16/` while you are writing

Treat this manuscript as a **first submission**. Every judgement must come from text or source data you read and recompute yourself. Any claim you CAN verify, you MUST verify.

## Manuscript's stated claims (for you to test, NOT to trust)
- 5 immune hubs (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) Mars1-down; FIS1 non-immune (mitochondrial-fission) passenger up (logFC +1.26).
- 30-gene signature: honest external cross-platform AUC **0.638** (95% CI 0.532–0.748; E-MTAB-4451, n=106, 52 deaths); CV AUC **0.659**; L1-locked **0.585**. IRG proxy recomputed **0.529** ("weak reference only; CIs overlap"). IRG published benchmark (Peng et al.) **0.619**.
- DCA on **calibration-corrected** probabilities; model exceeds treat-all from threshold **≈0.30**, and at 0.80 the model NB is **0.00** while treat-all NB is **−1.55** (they DIVERGE, not converge). Verify against `03_results/09_ext_dca_grid.csv`.
- Calibration: external logistic fit **sub-ideal slope of 0.50** (over-confident predictions), intercept **−0.04** (NO 95% CI claimed — confirm none is stated).
- Mars1 vs Mars2/3/4 P = **0.47 / 1.9e-18 / 1.3e-3**.
- MR primary 28-day death: all IVW **OR 0.92–1.12, P ≥ 0.23**; CD74 critical-care WM flagged (overlap-inflated, reversed direction); 45-test BH family framed on *overlapping hypothesis structure* (same gene × multiple estimators/outcomes) — CD74 chr5q32, HLA-DQA1 chr6p21.32 are DIFFERENT chromosomes so an LD claim is correctly NOT made; 27 instruments.
- L1000 rescue ranks: lenalidomide **5435**, azithromycin **9152**.
- PD-1 (PDCD1) up-regulation is the recognised sepsis T-cell-exhaustion marker; the Mars1 program shows *down*-regulated HAVCR2/TIM-3 (reduced checkpoint engagement), NOT the canonical TIM-3-up exhaustion signature.
- References: 37 entries, numbered in order of first appearance (Vancouver); audit gate #23 number-agnostic, gate #30 guards reference-list integrity.
- External validation "independent in cohort and platform but **not in label**" (fixed orientation trained on GSE65682 28-day labels).
- Seven mechanism-anchored **immune-modulating** agents prioritised (IL-7, GM-CSF, IFN-γ, azithromycin, lenalidomide, thymosin α1, BCG).

## Source files to verify against (read directly)
- `05_reports/manuscript.md`, `05_reports/cover_letter.md`
- `03_results/09_external_validation.csv`, `09_external_validation_coef.json`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`
- `03_results/S06_auc_compare.csv`, `S06_signature_genes.csv`
- `03_results/10_genetics_mr.csv`, `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, `10_mr_bh_family.csv`, `10_genetics_mr_harmonised.csv`
- `03_results/S01_mars1_deg.csv`, `S01_immunoparalysis_direction.csv`, `S05_hub_genes.csv`
- `03_results/S08_l1000_candidate_scores.csv`, `08_candidates_drugs.csv`
- `03_results/S02_immunoparalysis_score.csv`
- `02_scripts/python/09_external_validation.py`, `_ext_calibration_dca.py`, `check_audit_assertions.py` (runs 31 assertions, exit 0; you MAY run it but must not trust it as proof — verify headline numbers yourself)

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
