# Panel Brief — Round-7 Independent Review of `manuscript.md` (v1.6.0)

> Repository: `sepsis-immunoparalysis-hub` (single-author bioinformatic re-analysis).
> Article type under review: **computational / multi-omics translational research article** (single-author, English, Vancouver-ish; claims a positive, therapeutically actionable finding).
> This review audits the **current state of v1.6.0**, treating it as a fresh first submission.

## Independence discipline (mandatory)

You have **never seen this manuscript before**. Do NOT read any of the following:
- `05_reports/REVIEW_round6_20260926.md`, `05_reports/review_r6/`, `05_reports/reVIEW*`
- any `RESPONSE_*.md`, `REVISION_*.md`, `review_r1/` … `review_r5/`, `REVIEW_r*`
- `05_reports/_PANEL_BRIEF.md` of any prior round, `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`
- the panel outputs of the OTHER three experts in `05_reports/review_r7/` (read only your own file + raw sources)

Do **not** assume the manuscript is mature or has passed any prior review. Assume it is a first submission that may contain first-submission-grade defects.

Every judgement must come from text or source data you read yourself. **Any quantitative claim in the manuscript that you CAN verify, you MUST verify by re-deriving it from the raw source file** (the CSVs in `03_results/` and the scripts in `02_scripts/python/`). A review that does not recompute numbers is incomplete and will be rejected by the editor.

## Output contract (mandatory four parts per item)

For every issue:
- **【Problem】** one sentence.
- **【Evidence】** pinned to `file:line` or `section + exact numbers`. Any number you cite as "wrong/right" must be one you recomputed yourself; show the command or the code line.
- **【Why it matters】** concrete effect on conclusions / credibility / acceptance.
- **【Specific fix】** a paste-ready English replacement sentence, OR an explicit spec for a new analysis (variables, strata, output columns). "Consider strengthening the discussion" is banned.

## Also required sections
- **§ Stands up** (≥3, with evidence) — things you suspected were wrong but found correct. This is a deliverable, not filler.
- **§ Questions for the authors** — what you need to know; do not guess answers.
- **§ What I actually checked** — files read, commands run, values recomputed vs the manuscript's, with each discrepancy stated.

## Source-data map (verify against these, not the prose)

Key raw / derived files in `03_results/`:
- `S01_mars1_deg.csv` — Mars1 differential expression (columns include `gene`, `logFC`, `t`, `FDR`). **Hub direction lives here.**
- `S02_immunoparalysis_score.csv` — per-sample Mars endotype (`mars_endotype`) and `immune_function_score` (the immunoparalysis score).
- `S01_immunoparalysis_direction.csv` — immune-gene direction table used for the 23/25 consensus claim.
- `08_candidates_drugs.csv` — repositioning candidates; `rescue_fraction`, `n_target_genes`, `n_rescue_mars1down`. The metric rule MUST be `|logFC|>=0.3 & FDR<0.05` (a.k.a. `DEG_0.3`).
- `09_external_validation.csv`, `09_ext_risk_scores.csv`, `09_ext_calibration_dca.csv` — external cohort (E-MTAB-4451, n=106, 52 deaths) AUC / calibration / DCA.
- `10_genetics_mr_outcome5086_28ddeath.csv` (primary 28-day death), `10_genetics_mr.csv` (susceptibility), `10_genetics_mr_outcome4982_criticalcare.csv` (critical care) — two-sample MR, columns include `gene`, `method` (IVW / MR-Egger / Weighted median), `beta`, `se`, `p`, `nsnp`, `I2`.
- `10_mr_bh_family.csv` — the 45-test BH family q-value table (5 genes × 3 estimators × 3 outcomes; FCGR3A excluded).
- `10_genetics_mr_harmonised.csv` + per-outcome `*_harmonised.csv` — per-SNP instruments.
- `S06_auc_compare.csv`, `S08_l1000_candidate_scores.csv`, `S08_l1000_rescue_trtcp.csv` — signature AUC and LINCS L1000 rescue.

Scripts in `02_scripts/python/`:
- `check_audit_assertions.py` — the manuscript's own gate (currently 8 assertions). **Critically:** a green gate proves arithmetic/self-consistency, NOT correctness. Check whether each assertion actually guards the *headline number* or merely metadata.
- `_recompute_mr_pvalues.py`, `_recompute_table2.py`, `_ext_calibration_dca.py`, `_mr_diagnostics.py`, `_editor_verify_egger.py` — the v1.6.0 recompute/figure scripts. Read them and confirm they do what the prose claims.

## Environment traps specific to THIS study (do not rediscover by burning budget)
1. **MR-Egger p-values must use the two-sided t-distribution on df = n_instruments − 2, NOT the normal distribution.** A normal-based p makes a borderline signal look genome-significant. Re-derive: `p = 2*scipy.stats.t.sf(abs(beta/se), df=nsnp-2)`.
2. **The immunoparalysis score does NOT distinguish Mars1 from Mars2** (median ≈ −0.79 vs −0.75; Mann–Whitney P ≈ 0.47). It only separates the low-score pair (Mars1/Mars2) from Mars3/Mars4. Any text implying the score is Mars1-specific is a contradiction.
3. **FIS1 is UP-regulated in Mars1 (logFC ≈ +1.26)**; the other five hubs are down. Any "all six hubs down" statement is false.
4. **Calibration / DCA must be computed on the external cohort**, not the discovery cohort. Verify the figure `04_figures/S06_dca.png` and `09_ext_calibration_dca.csv` actually come from E-MTAB-4451, and that net benefit is reported honestly (vs treat-none / treat-all).
5. **Sample overlap** between eQTLGen exposure and UK Biobank outcomes is unaddressed by a correction — this biases MR toward the null but must be disclosed, not silently assumed harmless.
6. **Floating-point underflow**: a stored `p = 0.0` or `P < 1e-300` is not a "discovery"; it is silent underflow and must be recomputed on the log scale.

## Forbidden language
Do not mention what tools/agents you used. Write review comments only.
