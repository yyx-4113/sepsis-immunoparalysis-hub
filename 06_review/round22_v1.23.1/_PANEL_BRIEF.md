# Round-22 Independent Multi-Expert Review — Panel Brief (ENFORCED INDEPENDENCE)

**Target manuscript:** `05_reports/manuscript.md` at **v1.23.1** (commit `e8ba121`, tag `v1.23.1`).
**Submission pack under review:** `07_submission_bmc_v1.21.0/` (Manuscript.docx, SUBMISSION_MANIFEST.md, build/verify scripts).
**Audit script:** `02_scripts/python/check_audit_assertions.py` (32 assertions; should be 32/32 green).
**Target journal:** BMC Medical Genomics (Research article; computational biology / methods-and-resources framing).

## ⛔ HARD INDEPENDENCE RULES (violation = disqualifying)
1. **You MUST NOT read, open, or reference any file under `06_review/`** — including `round21_v1.22.0/`, `REVIEW_round21_*.md`, or any prior-round file. Treat all prior reviews as **non-existent**.
2. **You MUST NOT read any author rebuttal, response letter, or "what was already fixed" note.** You are a *fresh* reviewer who has never seen this manuscript before.
3. **Do NOT search the git history for prior review rounds.** Inspect only the files explicitly listed below.
4. Your verdict must be based **solely** on what the manuscript + its artifacts actually claim and compute, versus the underlying data/scripts.

## Files you MAY and SHOULD read
- `05_reports/manuscript.md` (the manuscript itself — read fully).
- `07_submission_bmc_v1.21.0/Manuscript.docx` (built artifact — cross-check against .md source).
- `07_submission_bmc_v1.21.0/SUBMISSION_MANIFEST.md`, `build_submission_bmc.py`, `verify_submission_bmc.py`.
- `02_scripts/python/check_audit_assertions.py` (read the assertions; verify they are *meaningful*, not just self-consistent).
- `03_results/*.csv` (authoritative numeric source: risk scores, AUCs, hub genes, death associations, DCA grid, calibration, L1000, SRS, IRG proxy).
- `02_scripts/python/*.py` (the actual analysis code — verify it matches what the manuscript describes, especially fit/predict feature matrices, resampling indices, labels, and any DeLong / AUC / CI computation).
- `CITATION.cff`, `README.md`, `DATA_SOURCES.md`, `MANIFEST.csv`.

## Your role (pick YOUR lane only)
- **A1 — Domain / Biology**: sepsis immunoparalysis biology, Mars1 endotype, antigen-presentation program, MHC-II, erythroid/heme module, FIS1 mitochondrial-fission protein, drug-repositioning plausibility. Flag any biological claim that is overstated, mislabeled, or contradicts literature. Verify cited references are real and apt.
- **A2 — Design / Statistics**: primary-vs-sensitivity framework honesty, AUC CIs, DeLong usage (is any DeLong claim methodologically valid given available per-sample scores?), calibration, DCA net-benefit windows, external validation EPV, endpoint-dilution, multiple-comparison accounting, power. Flag internal contradictions between numbers quoted in different sections.
- **A3 — Implementation / Reproducibility**: do the numbers in the manuscript match `03_results/*.csv` and the scripts? Is Table 1 free of markdown `|` leakage? Are references in Vancouver citation order with DOIs? Any MR-layer residue? Does `verify_submission_bmc.py` exit 0? Spot-check ≥5 key statistics by recomputing from source CSVs.
- **A4 — Venue / Submission fit**: BMC Medical Genomics scope fit, article type, declaration completeness (AI use, data availability, ethics, competing interests), figure/file mapping in manifest, title word count, any metadata mismatch between manuscript and manifest/docx.

## Required output (write to your assigned file)
Each expert writes a single markdown file:
`06_review/round22_v1.23.1/A1_domain.md` / `A2_design.md` / `A3_implementation.md` / `A4_venue.md`

Structure:
1. **Independence attestation**: one line confirming you did NOT read `06_review/` or any rebuttal.
2. **Verdict**: `DESK-REJECT` / `MAJOR` / `MINOR` / `ACCEPT`.
3. **Findings**: each with `[Tier 0/1/2/3]`, file:line citation, what the manuscript says, what is wrong/risky, and a concrete fix.
   - Tier 0 = blocks submission (factual error, contradiction, invalid statistic, missing disclosure).
   - Tier 1 = major (must fix before submission).
   - Tier 2 = minor (should fix).
   - Tier 3 = cosmetic.
4. **Cross-validation note**: which 3 numbers you independently recomputed and whether they matched.
5. **One-line summary** for the integrator.

Be specific and evidence-based. Do not soften for the author. If the manuscript is genuinely clean, say so — but only after actually checking.
