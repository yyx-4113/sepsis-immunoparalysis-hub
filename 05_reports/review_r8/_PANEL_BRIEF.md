# Panel Brief — Round-8 independent review of v1.7.0

**Target:** `05_reports/manuscript.md` @ v1.7.0 (commit c07cd94, tag v1.7.0)
**Date:** 2026-09-27
**Article type under review:** computational re-analysis / in-silico multi-omics + drug-repositioning (single-author bioinformatics)
**Pre-specified design:** Tier-1 biology-inevitable positive; Tier-2 method positive-control; Tier-3 (MR) hypothesis-generating.

## Independence discipline (mandatory)
Forbidden to read: `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `05_reports/review_r7/`, `.workbuddy/`, `SUBMISSION_MANIFEST.md`, any prior review or git review history.
Reviewers must treat the manuscript as a first submission and recompute every verifiable number from source CSVs themselves.
Each reviewer wrote to `05_reports/review_r8/<codename>_<role>.md`; reviewers did not read each other's outputs.

## Output contract (per finding)
【问题】 / 【证据】 file:line + recomputed numbers / 【为何重要】 / 【具体修改】 + §站得住的 + §向作者提问 + §我实际核查了什么.

## Panel (4 independent reviewers, fresh context)
- A1 domain/sepsis-immunology — biology plausibility, novelty boundary, FIS1-as-hub, ImmunoSep contextualisation, literature gaps.
- A2 design/biostat/MR — MR multiple-testing & Egger t-dist, sample overlap, DCA/calibration, EPV, family-wise error, bootstrap CI.
- A3 implementation/provenance — audit-gate behaviour, number-to-source traceability, data-availability honesty, file-level claims.
- A4 venue editor/reporting — STROBE-MR adherence, headline-vs-caveat consistency, article-type fit, references, IRB/data-availability mapping.

## Editor verification (own script, raw sources only)
1. `08b_clinical_translation.csv` `rescue_fraction_S08` for IL-7/GM-CSF/IFN-γ = 1.0 / 0.833 / 0.714 vs `08_candidates_drugs.csv` (Table 2) 0.80 / 0.667 / 0.571 → **confirmed +1-numerator inflation** on the three top-ranked drugs.
2. `git ls-files 01_data` → 0; `.gitignore` excludes `01_data/`; `03_results/` has 45 tracked files → **confirmed** "processed matrices are available in the repository" is literally false.
3. Spot-checked A2's MR BH recomputation and min-IVW-P (0.236 ≥ 0.23) — consistent with CSVs.
