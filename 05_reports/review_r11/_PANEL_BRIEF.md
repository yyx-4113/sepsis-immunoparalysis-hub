# Panel brief — Round-11 independent review (v1.11.0, Scientific Reports submission-ready)

## Manuscript under review
- File: `05_reports/manuscript.md` (version v1.11.0, commit e49ccb5, tag v1.11.0, pushed).
- Title: "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and validates a 30-gene sepsis prognostic signature"
- Target venue: **Scientific Reports** (Nature Portfolio). Article type in system = "Article".
- Claim type: computational-biology / methods-and-resources report. Contribution = reproducible auditable pipeline + honest external validation + experimental blueprint. Explicitly NOT novel hub-gene discovery. Mars1 program is a near-replication of the established MARS consortium endotype.
- Data: public GSE65682 (802 samples, GPL13667) re-analysed; external E-MTAB-4451 (106 patients, GPL10558); LINCS L1000 (GSE92742); two-sample MR via IEU OpenGWAS eQTLGen + UK Biobank sepsis GWAS.
- Source result files: `03_results/` (CSVs, e.g. S01_mars1_deg.csv, 09_external_validation.csv, 10_*.csv). Figures in `04_figures/`.
- Author: single author (Yongxin Yang). LLM used in preparation (disclosed §2.12).

## Independence discipline (MANDATORY)
Treat this as a FIRST submission. You have NOT seen prior review rounds.
FORBIDDEN to read (do not open, do not grep, do not list):
- Any `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `review_r*/` folder, `cover_letter.md`, `scirep_submission_checklist.md`, `journal_recommendation.md`
- Any `MEMORY.md`, `.workbuddy/memory/*`, project overview, `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, `CITATION.cff`, `DATA_SOURCES.md`
- Other reviewers' outputs in this `review_r11/` directory.
Do not assume the manuscript is mature or has passed previous review. Every judgement must come from text or source data you read YOURSELF. Any claim you CAN verify, you MUST verify.

## Output contract (every item, four mandatory parts)
- 【Problem】 one sentence
- 【Evidence】 pinned to file:line, or table/section + exact numbers; numbers you cite must be ones you recomputed yourself
- 【Why it matters】 concrete effect on conclusions / credibility / acceptance
- 【Specific fix】 a paste-ready English replacement sentence, or an explicit spec for a new analysis

"Consider strengthening the discussion" is BANNED.

## Also required
- § Stands up (≥3, with evidence) — things you suspected but found correct. Deliverable, not filler.
- § Questions for the authors — what you need to know; do not guess answers.
- § What I actually checked — files read, commands run, values recomputed vs the manuscript, with discrepancy stated.

## Environment
- Python: `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe`
- Repo root: `D:/2026.9/极速交付9月会员日优惠套路/05_多组学+虚拟敲除药物发现/方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位`
- Result CSVs: `03_results/` ; figures: `04_figures/`
- Write your review to `05_reports/review_r11/<your_codename>_<role>.md` (Write tool creates parent dirs).
- Do NOT mention tools you use. Write review comments only.
