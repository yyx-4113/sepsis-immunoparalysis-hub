# Panel Brief — Round-12 Independent Review of `sepsis-immunoparalysis-hub` v1.12.0

## Manuscript under review
- **File:** `05_reports/manuscript.md` (version string inside text: **v1.12.0**, in the Data availability section; also `05_reports/cover_letter.md`)
- **Title class:** single-author computational biology / multi-omics + in-silico drug repurposing manuscript
- **Claimed contribution (confirm/validate framework):** re-confirm & externally validate the MARS immunosuppressed (Mars1) sepsis endotype; identify **5 immune hub genes** (CD74, HLA-DQA1, CD14, FCGR3A) anchored in the antigen-presentation/monocytic program **plus the APC-expressed checkpoint HAVCR2/TIM-3**, plus **1 co-expression passenger FIS1** (mitochondrial fission, Mars1 up-regulated logFC +1.26); build a 30-gene immune risk signature; report external validation AUC and in-silico virtual-knockout drug repurposing via L1000; MR layer is null.
- **Target venue:** Scientific Reports (Nature Portfolio), **Article** type.
- **Data:** public GEO / ArrayExpress / LINCS / GTEx; processed results in `03_results/*.csv`; analysis scripts in `02_scripts/python/`. Raw `01_data/` (~43 GB) is gitignored and NOT needed for this review.

## Independence discipline (mandatory)
**Forbidden to read:**
- any `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`
- the `review_r11/`, `review_r10/`, `review_r9/`, … directories and any prior review folder
- task/status files, project OVERVIEW, `SUBMISSION_MANIFEST.md`, deposit SOP, `author_verification_statement.md`
- **critically: any other reviewer's output inside `05_reports/review_r12/`**

Treat this as a **first submission**. Every judgement must come from text or source data you read yourself. Any claim you CAN verify, you MUST verify.

## Output contract (per item, four mandatory parts)
- **【Problem】** one sentence
- **【Evidence】** pinned to `file:line`, or table/section + exact numbers; numbers you cite MUST be ones you recomputed yourself
- **【Why it matters】** concrete effect on conclusions / credibility / acceptance
- **【Specific fix】** a paste-ready English replacement sentence, or an explicit spec for a new analysis (variables, strata, output columns)
- "Consider strengthening the discussion" is **banned**.

## Required sections
- **§ Stands up (≥3, with evidence)** — things you suspected but found to be correct. Deliverable, not filler.
- **§ Questions for the authors** — what you need to know; do not guess answers.
- **§ What I actually checked** — files read, commands run, values recomputed vs the manuscript, with any discrepancy stated.

## Mandatory recomputation checks (design + implementation experts)
- **External validation AUC 0.638 (95% CI 0.532–0.748, n=106, 52 deaths) vs IRG baseline 0.604** — recompute from `03_results/09_ext_risk_scores.csv` (columns `risk_oriented_sum`, `risk_irg3`, and the event/death indicator). Use sklearn `roc_auc_score`; state CI method. Also perform DeLong / paired-bootstrap test of difference (statistic ~0.034) and report P.
- **Calibration slope 0.5028 / intercept −0.0382** from `03_results/09_ext_calibration_dca.csv` and `02_scripts/python/_ext_calibration_dca.py` — confirm the slope is fit on **z-standardized scores** (`z=(x-mean)/std`), NOT raw scale; recompute; reproduce the bootstrap 95% CI (manuscript claims [0.11, 0.96]).
- **DCA net-benefit grid** `03_results/09_ext_dca_grid.csv` — confirm the zero-crossing threshold (manuscript says 0.80) and confirm the probabilities fed to DCA are **uncalibrated**.
- **MR:** 5 exposures × outcomes, IVW primary estimator; CD74 critical-care Egger SE 0.111 < IVW SE 0.325 on 3 SNPs — recompute from MR result files in `03_results/`; assess exposure–outcome sample-overlap bias; verify "1 of 45" BH-family significance (CD74 weighted-median q≈3e-17) from MR tables.
- **Signature training:** 30-gene L1 logistic; internal/bootstrap AUC; report EPV (events-per-variable). Manuscript claims EPV ~3.8.
- **FIS1 logFC +1.26 in Mars1 (up-regulated passenger)** — verify from DEG file `03_results/S01_mars1_deg.csv`.
- **Counts:** 23/25, 22/25, 21/25 triple counting; Table 1 effect sizes/P; external n=106/52. Verify against source CSVs.

## Environment traps
- Source CSVs can be large; use Read with offset/limit or python/pandas. Do NOT open ~43 GB `01_data/`.
- The calibration slope 0.5028 is on **z-standardized** scores — do NOT "rediscover" it as a bug.
- MR Egger SE < IVW SE with only 3 SNPs (df=1) is arithmetic, not a contradiction — but it does mean the Egger SE is unstable.
- Use the managed Python: `C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe` (has pandas/sklearn/numpy/scipy).

## Forbidden
- Tool talk: do not mention what tools you use; write review comments only.
- Do not write anything outside your assigned output file.
