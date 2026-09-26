# Round 5 Independent Review Panel — Panel Brief

**Manuscript under review:** `05_reports/manuscript.md` (v1.4.0, commit `ddb8575`, tag `v1.4.0`)
**Study:** Multi-omics dissection of the MARS immunosuppressed (Mars1) endotype in sepsis, with in-silico drug repositioning and a two-sample MR layer (S10).
**Date:** 2026-09-26

## Independence discipline (mandatory)
Forbidden to read: `REVIEW_round*.md`, `review_r2/`, `review_r3/`, `review_r4/`, `RESPONSE_*.md`. Also forbidden: reading each other's lens files in `review_r5/` before submission.
Treat this as a **first submission**. Every judgement must come from text or raw source data you read yourself.
**Any claim you can verify, you MUST verify** against `03_results/` source CSVs (MR: `10_genetics_mr*.csv`, BH table `10_mr_bh_family.csv`; external: `09_external_validation.csv`; CV: `S06_auc_compare.csv`; IRG: `S06_auc_compare.csv`; drug: `08_candidates_drugs.csv`, `08_positive_control_check.csv`).

## Output contract (per item)
- 【Problem】 one sentence
- 【Evidence】 file:line or table + exact numbers you recomputed yourself
- 【Why it matters】 concrete effect on conclusions / credibility
- 【Specific fix】 paste-ready replacement sentence, or explicit spec for a new analysis

## Also required per lens
- § Stands up (≥3, with evidence)
- § Questions for the authors
- § What I actually checked (files read, values recomputed vs manuscript)

## Mandatory checks for this round (editor directive)
1. Re-verify the MR multiple-testing claim against `10_mr_bh_family.csv` AND the three raw MR CSVs (the v1.3.0 fabrication must NOT recur).
2. Re-verify external AUC 0.638 / CI 0.532–0.748, CV 0.659/0.750, IRG 0.604 from source.
3. Re-check every *stated statistic* (I² range, F range, Egger intercept P, instrument counts) against the CSVs — the panel specifically hunts "manuscript contradicts its own data" slips.
4. Reference integrity: every `[n]` cited and every defined ref used.
