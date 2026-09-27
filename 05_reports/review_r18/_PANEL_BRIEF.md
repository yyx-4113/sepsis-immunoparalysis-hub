# Round-18 Independent Blind-Panel Brief — v1.18.0

**Manuscript:** `05_reports/manuscript.md` (tag `v1.18.0`, commit `57fe917`, built on v1.16.0 / commit `1212f7b`)
**Repository:** `github.com/yyx-4113/sepsis-immunoparalysis-hub` (local clone at project root)
**Target journal:** Scientific Reports (Nature Portfolio)
**Article type claimed:** Article (original research) — computational biology / methods-and-resources; contribution framed as *reproducible pipeline + honest external validation + experimental blueprint*, **not** novel hub-gene discovery (confirm/validate, not discovery).

## Independence discipline (mandatory)
**Forbidden to read (do not open, do not grep, do not summarise):**
- `05_reports/REVIEW_round*.md` (all prior rounds)
- `05_reports/review_r12/` … `review_r17/` (all files)
- `.workbuddy/memory/` (MEMORY.md, daily logs)
- `05_reports/scirep_submission_checklist.md`
- Any other reviewer's output file under `05_reports/review_r18/` while you are writing

Treat this manuscript as a **first submission**. Every judgement must come from text or source data you read and recompute yourself. Any claim you CAN verify, you MUST verify. The manuscript has been through prior revision rounds — that is irrelevant to your task and you must not go looking for what those rounds said.

## Manuscript's stated claims (for you to test, NOT to trust)
- 5 immune hubs (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) Mars1-down; FIS1 non-immune (mitochondrial-fission) passenger **up** (logFC +1.26).
- 30-gene signature: external cross-platform AUC **0.638** (95% CI 0.532–0.748; E-MTAB-4451, n=106, 52 deaths); within-cohort CV AUC **0.659** (labelled optimistic); L1-locked **0.585**. Recomputed 3-gene IRG proxy **0.529**; published IRG benchmark (Peng et al.) **0.619**.
- External validation described as **independent in cohort and platform but NOT in label** (score orientation fixed on GSE65682 28-day labels).
- Calibration: slope **0.50** (described as over-confident / sub-ideal), intercept **−0.04**; now disclosed as fitted on the same 106-sample test set, hence **optimistically biased and illustrative**; no bootstrap optimism correction; **NO 95% CI claimed** — confirm none is stated.
- DCA computed on calibration-corrected probabilities; model exceeds treat-all from threshold **≈0.30**; advantage now described as confined to the **0.30–0.75** window (0.01–0.09 NB at 0.30–0.50; 0.17–1.05 at 0.55–0.75); at **≥0.80** model NB is **0.00 = treat-none** because no calibrated risk exceeds the threshold (at 0.80 treat-all NB = −1.55). Verify every number against `03_results/09_ext_dca_grid.csv`.
- Mars1 vs Mars2/3/4 P = **0.47 / 1.9e-18 / 1.3e-3**.
- MR primary 28-day death: all IVW **OR 0.92–1.12, P ≥ 0.23** — abstract now says "no significant inverse-variance-weighted estimate"; CD14 MR-Egger **OR 0.91, P = 0.049** nominal; CD74 critical-care WM **OR 2.19** family-significant but **reversed** direction; 45-test BH framed as a **dependence-ignoring approximation**; 27 instruments.
- **FIS1 is now explicitly NOT counted** among hubs "concordant with the immunoparalysis model" (it is up-regulated, so a protective MR opposes its observational association). Concordant hubs are stated as **two of the four assessable immune hubs** (HLA-DQA1, CD14).
- L1000 rescue ranks: lenalidomide **5435** (top 26.6%), azithromycin **9152** (≈ median); prednisone **651 / 3.2nd percentile** is disclosed as refuting the axis; the two small-molecule ranks are therefore labelled **descriptive only, not supportive evidence**.
- HAVCR2/TIM-3: described as **net lower bulk expression**, compatible with but not establishing reduced per-cell checkpoint engagement; new reference **Wang et al., Front. Immunol. 15, 1328667 (2024)** is cited for the sepsis TIM-3 literature in both directions.
- References: **38 entries**, numbered in first-appearance order; ref [20] is the TIM-3 review.
- Data availability: release tag **v1.18.0**; evaluated commit **1212f7b is tagged v1.16.0**. Verify against git.
- A standalone `## Code availability` section now exists. Main-text tables are numbered **1–5**.

## Source files to verify against (read directly)
- `05_reports/manuscript.md`, `05_reports/cover_letter.md`
- `03_results/09_external_validation.csv`, `09_external_validation_coef.json`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`
- `03_results/S06_auc_compare.csv`, `S06_signature_genes.csv`
- `03_results/10_genetics_mr.csv`, `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, `10_mr_bh_family.csv`, `10_genetics_mr_harmonised.csv`
- `03_results/S01_mars1_deg.csv`, `S01_immunoparalysis_direction.csv`, `S05_hub_genes.csv`
- `03_results/S08_l1000_candidate_scores.csv`, `08_candidates_drugs.csv`
- `03_results/S02_immunoparalysis_score.csv`
- `02_scripts/python/09_external_validation.py`, `_ext_calibration_dca.py`, `_mr_diagnostics.py`, `check_audit_assertions.py` (runs 32 assertions, exit 0; you MAY run it but must not treat green as proof — verify headline numbers yourself)
- Enumerate `04_figures/` to cross-check the §8 figure index.

## Output contract (every item needs all four)
- 【Problem】 one sentence
- 【Evidence】 pinned to file:line, or table/section + exact numbers you recomputed
- 【Why it matters】 concrete effect on conclusions / credibility / acceptance
- 【Specific fix】 paste-ready English replacement sentence, or explicit new-analysis spec

"Consider strengthening the discussion" is banned. Every item must be actionable.

## Also required
- § Stands up (≥3, with evidence) — explicitly mark things you suspected but found correct. This is a deliverable, not filler.
- § Questions for the authors — state what you need to know, do not guess.
- § What I actually checked — files read, computations run, values recomputed vs the manuscript's, discrepancies stated.
- A closing **VERDICT** line: Accept / Minor / Major / Desk-reject, with a one-paragraph justification and an explicit statement of whether any item is a desk-reject hard-fail.

## Tool talk
Do not mention tools; write review comments only. If you cannot read a file, say which and why, but do not end the task.

## Regression sweep required this round (the manuscript was edited in many places at once)
A revision that touched four FIS1 sites, four "independent" sites, the whole abstract, the table numbering and the reference list can leave stale copies behind. You MUST:
1. grep for **every** residual occurrence of the pre-revision phrasings: `three of the five assessable hubs`, `three of five assessable hubs`, `widens rather than converges`, `reduced checkpoint engagement` (unqualified), `conservative approximation`, `honest independent`, `v1.17.0`.
2. Grep for the **value** rather than the expected location: table numbers (`Table 2`, `Table 3`, `Table 4`, `Table 5`), the version string, and every reference number that could have shifted.
3. Check that the new caveat in one section did not leave an over-claim standing in another (e.g. §3.3 still calling FIS1 a passenger while §3.10 excludes it from concordance is intended — but confirm the two do not contradict; check the Abstract, §4, §6 Conclusion and Limitation 2 all say the same thing about FIS1).
4. Verify the renumbered tables: each `Table N` caption exists once and every in-text cross-reference points at the right table.
5. Verify the 38-entry reference list is contiguous, in first-appearance order, all cited, and that ref [20] is a real resolvable record (check its DOI/metadata yourself).

## Carry-forward re-examination (re-verify independently; state Minor vs escalates)
- FIS1: is the re-scoping complete and internally consistent across all four sites?
- DCA: does the new 0.30–0.75 window wording match `09_ext_dca_grid.csv` exactly? Are the quoted NB margins (0.01–0.09 and 0.17–1.05) arithmetically correct?
- Calibration test-set nesting: is the disclosure adequate, or does the DCA still read as a clinical-utility claim?
- L1000: is the "descriptive only" demotion applied everywhere the ranks are cited (Abstract, §3.9, §4, §6)?
- MR abstract wording: does it now accurately reflect the body (no significant IVW; CD14 Egger nominal; CD74 reversed)?
- TIM-3: is ref [20] used correctly, and is the reconciliation with the TIM-3-up literature adequate?
- New in v1.18.0: standalone Code availability — does it conflict with or duplicate Data availability?
- New in v1.18.0: abstract at ~193 words — recount it yourself and confirm ≤200 and citation-free and non-structured.
