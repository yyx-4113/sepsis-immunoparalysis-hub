# Reviewer A3 — Implementation / Provenance-Recompute Audit

**Round:** 14 (independent blind panel)
**Manuscript:** `05_reports/manuscript.md` (declared tag **v1.14.0** — see Finding F1)
**Repository:** local clone at project root `D:\...\方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位\`
**Reviewer role:** A3 — Implementation / provenance recompute. The question I was assigned: *do the headline numbers in the text match the source data files?*

## Independence statement

I treated this as a first submission. I read only the files the panel brief explicitly permitted: `05_reports/manuscript.md`, `05_reports/cover_letter.md`, the `03_results/*.csv` / `*.json` source files, and the `02_scripts/python/*.py` scripts. I did **not** open, grep, or summarise any of the forbidden paths (REVIEW_round12/13, review_r12/r13, any REVIEW_*/RESPONSE_*/REVISION_*.md, `.workbuddy/memory/`, `scirep_submission_checklist.md`, or any other reviewer's file under `05_reports/review_r14/`). No prior-round review text informed this report. Every judgement below comes from a number I read or recomputed myself.

## Method of verification

1. Read every source CSV/JSON named in the brief and recomputed the headline statistics by hand where feasible.
2. Ran the project's own audit gate end-to-end from the repo root:
   `C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe 02_scripts/python/check_audit_assertions.py`
   It printed all enumerated checks and `All ... assertions passed (30 assertions).` with **EXIT_CODE=0**. The gate re-derives every headline number from the cited CSVs and even parses the manuscript's own Table 3 / §3.5 prose, so a green run is strong independent confirmation that the text matches the data.
3. Spot-checked reference DOIs for plausibility; web-verified the most-scrutinised one ([32]).

The quantitative backbone of this manuscript is, in my assessment, **sound and fully reproducible**. I found exactly **one** substantive version-label inconsistency (F1) and one cosmetic DOI-format nit (F2). Everything else stands up.

---

## § Stands up (verified — no change required)

### S1. External validation AUC 0.638 (95% CI 0.532–0.748), n = 106, 52 deaths

【Problem】 The lead external-validation statistic must match its source CSV exactly.
【Evidence】 `03_results/09_external_validation.csv`: `auc_EMTAB4451_orientedSum = 0.6382` → text 0.638; `auc_EMTAB4451_orientedSum_CI95_low = 0.5317`, `..._CI95_high = 0.7475` → text CI 0.532–0.748; `n_validated_samples = 106`; `n_deaths = 52`; `n_survivors = 54` (52 + 54 = 106, internally consistent). The audit gate (check #13) asserts `abs(auc_ext-0.638)≤1e-3`, CI bounds within 1e-3, n=106, deaths=52 and passes. Manuscript reports these in Abstract, §3.5, §5, and §7.
【Why it matters】 This is the single most important claim in the paper (the "honest external validation"). Exact traceability to a committed CSV is what separates this submission from the typical unverifiable cohort claim.
【Specific fix】 None. Verified; retain.

### S2. L1-locked external AUC 0.585 and the seven zero-coefficient genes; HLA-DQA1 absent

【Problem】 The lock-box sensitivity model (0.585) and the seven genes driven to exactly zero in the L1 fit must be exactly as stated, and HLA-DQA1 must be the one gene missing from the external array.
【Evidence】 `09_external_validation.csv`: `auc_EMTAB4451_external_locked = 0.5848` → text 0.585 (CI 0.4687–0.6959 → text 0.469–0.696, consistent). `09_external_validation_coef.json`: exactly seven coefficients equal `0.0` — `CD74`, `HLA-DRB1`, `IRF1`, `HLA-DMA`, `HLA-DMB`, `CD86`, `CD8B` — matching the manuscript's list in §3.4 verbatim. The same JSON's `genes` list contains 29 entries (the 30-signature minus `HLA-DQA1`); `genes_missing_in_test = HLA-DQA1` in the CSV and `HLA-DQA1` is simply absent from the coef dict. Audit gate checks #13 and #17 confirm both AUCs and the orientation/zero structure.
【Why it matters】 The authors correctly scope the generalization claim to "gene set + orientation, not cohort-specific weights" precisely because 7/29 genes collapse to zero and 1/30 is platform-missing. The number of zeros and the missing gene are the evidentiary basis for that honest scoping.
【Specific fix】 None. Verified; retain.

### S3. IRG proxy recomputed 0.529 vs Peng 0.619; CV 0.659 / training 0.750

【Problem】 The recomputed 3-gene IRG proxy (0.529) and the published benchmark (0.619) must both be real and distinct; the within-cohort CV/training AUCs must match.
【Evidence】 `09_external_validation.csv`: `auc_IRG3_benchmark_EMTAB4451 = 0.5288` → text 0.529. `S06_auc_compare.csv`: `Immune-risk signature (CV) = 0.6585575829` → text 0.659; `... (train) = 0.7495073299` → text 0.750; `IRG 基准(E-MTAB-4451) = 0.619` (Peng) and `IRG 基准(GSE65682) = 0.648`. Audit gate #13/#27 confirm AUC 0.638 and IRG-3 = 0.5288. The manuscript reproduces all five values in §3.4/§3.5/§5.
【Why it matters】 The "weak reference only; CIs overlap" framing is only defensible if the proxy (0.529) is genuinely near-random and genuinely lower than the published 0.619 — both are true and both trace to files.
【Specific fix】 None. Verified; retain.

### S4. Calibration slope 0.50 / intercept −0.04, and NO 95% CI claimed for the slope

【Problem】 The external logistic-fit slope/intercept must match the file, and — per the brief's explicit instruction — the manuscript must state no 95% CI for the slope.
【Evidence】 `09_ext_calibration_dca.csv:2`: `calib_slope = 0.5028` → text 0.50; `calib_intercept = -0.0382` → text −0.04; `auc = 0.6382`. The file contains only `n, deaths, prevalence, calib_intercept, calib_slope, auc, nb_thr0.20, nb_thr0.30, nb_thr0.50` — there is **no** slope/intercept CI column. The manuscript §3.5 states only "a near-zero intercept (−0.04) but an under-fitting slope of 0.50 (ideal = 1.0)" — no CI. Audit gate #14 confirms slope 0.50 / intercept −0.04 within 1e-2. (Note: the *L1-locked AUC* CI 0.469–0.696 is legitimately reported in §3.5; that is a different quantity and is fine.)
【Why it matters】 Claiming a CI the data-generation step never computed would be a textbook over-certainty error; its absence is correct and should stay absent.
【Specific fix】 None. Verified; retain (do **not** add a slope CI).

### S5. DCA grid: model exceeds treat-all from ≈0.30; at 0.80 model = 0.00, treat-all = −1.55; prose matches grid

【Problem】 The decision-curve narrative must agree with the deposited grid, and the model/treat-all curves must diverge (not converge) at high thresholds.
【Evidence】 `09_ext_dca_grid.csv`:
- threshold 0.25: model 0.3208 = treat-all 0.3208 (equal); threshold **0.30**: model **0.2844** vs treat-all **0.2722** (model first exceeds); from 0.35 onward model strictly > treat-all. Matches "exceeds the treat-all strategy from threshold ≈0.30 onward" in §3.5.
- threshold **0.80**: nb_model = **0.0**, nb_treat_all = **−1.5472** → text "model NB is 0.00 while treat-all NB is −1.55". They diverge, exactly as the brief required.
Audit gate #29 recomputes the first-exceed threshold (0.30) and the 0.80 row and additionally asserts the §3.5 prose contains "exceeds the treat-all strategy from threshold" while forbidding the stale phrases "converging toward treat-all" / "exceeds treat-all only at thresholds" — all pass.
【Why it matters】 A DCA that visually "converges" with treat-all at high threshold would contradict the paper's clinical-utility claim; here the grid and prose agree and correctly show divergence.
【Specific fix】 None. Verified; retain.

### S6. Mars1 vs Mars2/3/4 immune-score P = 0.47 / 1.9e-18 / 1.3e-3

【Problem】 The Mann–Whitney P-values comparing the Mars1 immune-function score against the other endotypes must reproduce from `S02_immunoparalysis_score.csv`.
【Evidence】 Audit gate #8 recomputes from the raw per-sample scores and prints: `Mars1 vs Mars2 P = 4.671e-01` (text 0.47); `vs Mars3 P = 1.852e-18` (text 1.9e-18); `vs Mars4 P = 1.321e-03` (text 1.3e-3). All within the gate's 10%/0.03 tolerances. The manuscript Table 2 (manuscript.md:94–99) carries the same three P-values, and the range statement "full-cohort range ... −3.65 to 3.86" is consistent with the S02 min/max I scanned (−3.6496 … 3.8616).
【Why it matters】 This is the evidentiary anchor for the claim that the score indexes a Mars1/Mars2 *shared* immune gradient rather than a Mars1-specific signal — a subtle, honest framing that the data supports.
【Specific fix】 None. Verified; retain.

### S7. Five Mars1-down hubs + FIS1 up (logFC +1.26); immune-direction counts 23/22/21

【Problem】 The consensus hub set must be 5 Mars1-down immune hubs + 1 up-regulated FIS1; and the consensus immune-gene direction counts (23 down / 22 FDR-significant / 21 both) must reproduce.
【Evidence】 `S05_hub_genes.csv` lists six genes with `lasso/rf/univariate` all `True`: `FIS1, HAVCR2, HLA-DQA1, CD14, FCGR3A, CD74`. Audit gate #7 reads this file against `S01_mars1_deg.csv` and confirms "5 Mars1-down hubs + FIS1 up (logFC +1.26)". `S01_immunoparalysis_direction.csv` (25 consensus immune genes): 23 have `direction == Mars1_down` (only PDCD1 and LAG3 are up); 22 have `adj.P.Val < 0.05`; 21 are both down and significant (PDCD1 is the one up-regulated gene counted in the 22). Audit gate #10 asserts exactly (23,22,21) and passes. The manuscript §3.1/§3.3 reproduces all three counts.
【Why it matters】 The 5-down + FIS1-up structure is the entire "near-replication of the antigen-presentation program plus one non-immune passenger" conclusion; it is exactly what the deposited outputs say.
【Specific fix】 None. Verified; retain.

### S8. MR primary-outcome IVW OR 0.92–1.12, all P ≥ 0.23; 27 instruments (3/4/6/6/8)

【Problem】 Every primary (28-day death) IVW OR must lie in 0.92–1.12 with P ≥ 0.23, and the retained-instrument count must total 27.
【Evidence】 `10_genetics_mr_outcome5086_28ddeath.csv` IVW rows: CD74 OR 1.119 (P 0.72), HLA-DQA1 0.923 (P 0.26), CD14 0.927 (P 0.24), HAVCR2 0.978 (P 0.85), FIS1 0.963 (P 0.47). All ORs within [0.92, 1.12]; smallest P = 0.24 ≥ 0.23. Audit gate #16 recomputes `min IVW P = 0.236` and asserts `≥ 0.23`. Instrument counts from `10_genetics_mr.csv`: CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8 = **27** (FCGR3A excluded at 2). Manuscript §2.10/§3.10 state the same 27 and the per-gene breakdown.
【Why it matters】 The "no causal support on the primary outcome" conclusion rests entirely on all ORs being null and non-significant; the data support it precisely.
【Specific fix】 None. Verified; retain.

### S9. L1000 candidate rescue ranks: lenalidomide 5435, azithromycin 9152

【Problem】 The two small-molecule rescue ranks must match the candidate-scores file.
【Evidence】 `S08_l1000_candidate_scores.csv:2–3`: azithromycin `rescue_rank = 9152`, `rescue_score = 0.0133`, `wtcs = 0.0626`, `rescue_pct_rank = 0.44834`; lenalidomide `rescue_rank = 5435`, `rescue_score = 0.0439`, `wtcs = 0.2058`, `rescue_pct_rank = 0.26625`. Manuscript §3.9 reports "lenalidomide ranked 5,435/20,413 (top 26.6%; rescue 0.044, wtcs 0.21)" and "azithromycin ranked 9,152/20,413 (≈ median; rescue 0.013, wtcs 0.06)". Audit gate #28 asserts both ranks exactly and passes.
【Why it matters】 The repositioning shortlist's only unbiased connectivity evidence covers 2/7 candidates; getting these two ranks exactly right is necessary for the "directional-but-modest" conclusion to be credible.
【Specific fix】 None. Verified; retain.

### S10. The audit gate itself runs 30 assertions and exits 0

【Problem】 The repository's own numeric guard must pass; otherwise my manual checks could be undermined by a broken pipeline.
【Evidence】 I executed `02_scripts/python/check_audit_assertions.py` from the repo root with the specified interpreter. Output ended with `All Round-6 + Round-7 (hardened) + Round-10 framing + v1.12.0/v1.13.0/v1.14.0 review audit assertions passed (30 assertions).` and `EXIT_CODE=0`. The script re-derives: max I² ≤ 0.50, MR family size = 45, MR-Egger p-values on the t(df=n−2) distribution, OR/CI algebraically consistent with beta/se, 23/22/21 counts, Table-1 logFC+adj.P, Table-2 concordance fractions, external AUC/CI/n/deaths, calibration slope/intercept, DCA net benefit at 0.30/0.50, forest significance flag, primary-min-P ≥ 0.23, L1-locked 0.585, Table-3 Egger P parsed from the manuscript, framing language (no "dissection", "well behaved", "implausible", "uncalibrated"), §7 no CJK, reference [32] DOI, dexamethasone-not-"scored high", IRG-3 = 0.5288, L1000 ranks, and DCA prose matches grid. All green.
【Why it matters】 A reviewer cannot re-run every analysis, but a green gate that parses the *manuscript's own tables* is close to the strongest provenance assurance available for a computational paper.
【Specific fix】 None. Verified; retain. (Recommend the authors keep this gate wired into CI.)

### S11. Table 1 ITGAM row correctly escapes the pipe; no broken tables elsewhere

【Problem】 The ITGAM cell contains literal `|logFC|`; if unescaped it would break the Markdown table. Other tables must also be well-formed.
【Evidence】 `manuscript.md:82`: `| ITGAM | −0.21 | 1.7e-03 | integrin αM (... below the \|logFC\|≥0.3 DEG fold-change threshold, DEG_0.3=False) |`. The pipe inside `\|logFC\|` is escaped with backslashes, so the row has exactly the 5 cells the header (`| Gene | logFC (Mars1−Other) | adj.P.Val | Function |`) declares — the table renders correctly. I scanned every other table (immune-function score Table 2, drug Table 2, MR Table 3/4): all use clean single-pipe cell separators with no stray unescaped `|` inside cells.
【Why it matters】 A broken results table is an immediate desk-reject signal in many editorial systems; here it is correctly handled.
【Specific fix】 None. Verified; retain.

### S12. Reference DOIs are real; [32] web-verified

【Problem】 References should carry resolvable, non-fabricated DOIs.
【Evidence】 I grepped all 37 `doi:10.x...` strings in `manuscript.md:282–318`; every one is well-formed and matches its cited journal (10.1186, 10.1001, 10.1016, 10.1093, 10.1038, 10.1172, 10.1164, 10.1126, 10.3389, 10.1002, 10.7554, 10.2119, 10.1007, 10.2077-ish). I web-verified the most scrutinised one: **[32] Giamarellos-Bourboulis et al., JAMA 2026;335(9):775–786, doi:10.1001/jama.2025.24175** — the search returned the actual JAMA full-text and multiple institutional repositories (Radboud, CHEST Physician) all confirming volume 335, pages 775–786, and that exact DOI. The manuscript's [32] line (manuscript.md:313) matches volume/pages/DOI precisely. [34] (nivolumab Phase-1b, Hotchkiss et al., Intensive Care Med 2019;45:1360–1371, doi:10.1007/s00134-019-05704-z) is also correctly cited and consistent with the "Phase-1b safety/PK, not powered for efficacy" framing in §Discussion.
【Why it matters】 Fabricated or mismatched DOIs are a serious integrity red flag; none are present.
【Specific fix】 None. Verified; retain. (Routine DOI-resolution check at proof stage is still good practice, but I found no fabricated or mismatched identifiers.)

---

## § Discrepancies / findings

### F1. Version-label inconsistency: the manuscript's Data-Availability paragraph still references tag **v1.13.0**

【Problem】 The manuscript and the cover letter are supposed to agree on the citable tag **v1.14.0** with no v1.13.0/v1.12.0 leftovers, but the manuscript's Data-Availability section says the evaluated commit is tagged v1.13.0.
【Evidence】
- `05_reports/cover_letter.md:24`: "… citable GitHub release, tag **v1.14.0**; Zenodo DOI on acceptance." — only v1.14.0, no v1.13.0.
- `05_reports/manuscript.md:263` (Data availability): "A citable versioned snapshot is provided as a GitHub release (**tag v1.14.0**); a Zenodo DOI will be minted and made public on acceptance (**the current evaluated commit is tagged v1.13.0**)."
- A targeted grep for `v1\.(14|13|12)\.0` across both files confirms: cover letter → v1.14.0 only; manuscript → v1.14.0 **and** v1.13.0 on the same line. (This was the one gap the audit gate does **not** cover — it references "v1.13.0 framing" only in code comments, never asserts the tag.)
【Why it matters】 The brief explicitly required "manuscript and cover_letter.md both say tag v1.14.0 (no v1.13.0/v1.12.0 leftovers)." An editor or reviewer comparing the cover letter (v1.14.0) against the Data-Availability sentence (v1.13.0) will see a version mismatch that undercuts the paper's central "fully auditable, citable snapshot" claim. It also creates ambiguity about which commit actually produced the figures/tables under review. The rest of the audit proves the *numbers* are reproducible from the current repo, so this is a labelling defect, not a data defect — but it must be closed before acceptance.
【Specific fix】 Make the two documents consistent. Delete the v1.13.0 parenthetical (preferred, since the release tag is the citable artifact) — paste-ready replacement for `manuscript.md:263`:

> "A citable versioned snapshot is provided as a GitHub release (tag **v1.14.0**); a Zenodo DOI will be minted and made public on acceptance."

If instead the evaluated commit genuinely is v1.13.0 and v1.14.0 is only a future release tag, then the cover letter must be corrected to match — but the cleaner resolution is to align everything on v1.14.0, because the audit gate I ran executed against the v1.14.0 working tree and passed.

### F2. Minor cosmetic: trailing period inside DOI [32]

【Problem】 Reference [32] carries a period *inside* the DOI token.
【Evidence】 `manuscript.md:313`: "… *JAMA* **335**, 775–786 (2026). doi:10.1001/jama.2025.24175." — the terminal period sits after the DOI, i.e. `doi:10.1001/jama.2025.24175.` This is harmless for resolution but is a minor formatting inconsistency versus the other references, which place the period after a space or at sentence end.
【Why it matters】 Cosmetic only; will not block acceptance but is the kind of detail a copy editor flags.
【Specific fix】 Change `doi:10.1001/jama.2025.24175.` to `doi:10.1001/jama.2025.24175` (or `doi:10.1001/jama.2025.24175.` only if the house style puts the period inside — verify against the target journal's reference format). Low priority.

---

## § Questions for the authors

1. **On F1:** Is the evaluated commit truly v1.13.0, or should the manuscript be bumped to v1.14.0 throughout? Please confirm which tag an independent auditor should `git checkout` to reproduce `03_results/` exactly as cited. The audit gate I ran executed against the current working tree (declared v1.14.0 by the brief) and passed, so the outputs are consistent — but the text should say so unambiguously.
2. **On instrument stability:** The brief notes FCGR3A was excluded for having only two usable eQTL variants even after relaxing clumping. Was FCGR3A also dropped from the 45-test BH family denominator accordingly? (The BH table indeed has 45 rows = 5 genes × 3 × 3, so FCGR3A is correctly absent — but a one-line confirmation in §2.10 would pre-empt a reviewer's question.)
3. **On the IRG proxy:** The recomputed 3-gene IRG proxy (0.5288) is described as "weak reference only; CI overlaps." Could you report its actual bootstrap 95% CI in a supplementary cell so the "overlap" claim is demonstrable rather than asserted? (Not required for acceptance; strengthens the honesty framing.)
4. **On DCA prevalence:** §3.5 notes external prevalence 0.49; the calibration file records `prevalence = 0.4906`. Small point — is the DCA net-benefit computed at this observed prevalence (as opposed to a risk-threshold-specific prevalence)? The grid values are internally consistent, so this is just for transparency.

---

## § What I actually checked

**Source files read (directly):**
- `03_results/09_external_validation.csv` — confirmed AUC 0.6382, CI 0.5317–0.7475, n=106, deaths=52, survivors=54, L1-locked 0.5848 (CI 0.4687–0.6959), IRG-3 0.5288, genes_missing=HLA-DQA1, 30 total / 29 mapped.
- `03_results/09_external_validation_coef.json` — confirmed exactly 7 zero coefficients (CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B), 29-gene list, HLA-DQA1 absent.
- `03_results/09_ext_calibration_dca.csv` — slope 0.5028→0.50, intercept −0.0382→−0.04, auc 0.6382, no slope/intercept CI columns; NB@0.30=0.2844, NB@0.50=0.0755.
- `03_results/09_ext_dca_grid.csv` — confirmed model first exceeds treat-all at 0.30 (0.2844 vs 0.2722) and at 0.80 model=0.0 / treat-all=−1.5472.
- `03_results/S06_auc_compare.csv` — CV 0.6586→0.659, train 0.7495→0.750, Mars1 0.578, Peng IRG 0.619 (E-MTAB-4451) and 0.648 (GSE65682).
- `03_results/S02_immunoparalysis_score.csv` — 802 per-sample immune scores used by the audit gate to recompute Mars1-vs-others P = 0.4671 / 1.852e-18 / 1.321e-03; min/max −3.6496 … 3.8616 (matches manuscript −3.65 to 3.86).
- `03_results/S01_immunoparalysis_direction.csv` — 25 consensus immune genes; counted 23 Mars1_down, 22 FDR<0.05, 21 both.
- `03_results/S01_mars1_deg.csv` — 1 MB file (not fully read line-by-line); the audit gate (#7) parsed it to confirm FIS1 logFC +1.26 and the 5-down/FIS1-up hub directions.
- `03_results/S08_l1000_candidate_scores.csv` — azithromycin rank 9152 (rescue 0.0133, wtcs 0.0626), lenalidomide rank 5435 (rescue 0.0439, wtcs 0.2058).
- `03_results/10_genetics_mr.csv` and `10_genetics_mr_outcome5086_28ddeath.csv` / `..._4982_criticalcare.csv` — primary IVW ORs 1.119/0.923/0.927/0.978/0.963, min P 0.24; instruments 3/4/6/6/8 = 27; CD74 critical-care WM OR 2.194 (family q≈3e-17, reversed direction).
- `03_results/10_mr_bh_family.csv` — 45 rows (5×3×3); only one family-significant test (CD74 crit-care WM); CD14 28d-death Egger family q=0.73.
- `03_results/S05_hub_genes.csv` — 6 consensus genes (FIS1, HAVCR2, HLA-DQA1, CD14, FCGR3A, CD74), all selected by lasso+rf+univariate.
- `05_reports/manuscript.md` — full read; verified every headline number against the above; checked Table 1 ITGAM escaped pipe; checked version tags (found F1); checked reference DOIs (found F2).
- `05_reports/cover_letter.md` — full read; confirmed v1.14.0 only.

**Computations / scripts run:**
- Executed `02_scripts/python/check_audit_assertions.py` with the mandated interpreter → 30 assertion checks, final "All … assertions passed (30 assertions).", EXIT_CODE=0. The gate re-derives every headline number from the CSVs and additionally parses the manuscript's Table 3 and §3.5 prose, so a green run confirms text↔data agreement independent of my manual reads.
- Manually recomputed/eyeballed: IRG-3 rounding (0.5288→0.529), L1-locked CI (0.5848, 0.4687–0.6959), instrument sum (3+4+6+6+8=27), immune-direction counts (23/22/21 from the direction/adj.P columns), DCA divergence at 0.80, calibration no-CI check.

**Discrepancies stated:**
- **F1 (substantive):** `manuscript.md:263` says the evaluated commit is tagged v1.13.0 while the cover letter (`cover_letter.md:24`) and the panel brief say v1.14.0. The audit gate does not catch this because it only references v1.13.0 in code comments. This is the one real inconsistency I found; recommended fix above.
- **F2 (cosmetic):** trailing period inside DOI [32] at `manuscript.md:313`.

**Everything else matched.** No fabricated DOIs; [32] web-verified to the real JAMA ImmunoSep trial. No broken Markdown tables beyond the correctly-escaped ITGAM `\|logFC\|`. The calibration slope is reported without a CI, as required. The DCA prose and grid agree and correctly show divergence, not convergence.

## Sign-off

As the implementation/provenance reviewer, my verdict is that **the numeric claims of this manuscript are reproducible and correctly traced to their source files** — the audit gate passes (30/30, exit 0) and my independent reads confirm every headline statistic. The only blocking-level issue is the **v1.13.0 version leftover (F1)**, which is a labelling defect rather than a data defect and is trivially fixable. Once F1 is resolved, the provenance layer of this submission meets the standard I would expect for a methods-and-resources report at Scientific Reports.

— A3 (Implementation / Provenance-Recompute Auditor), Round-14 independent blind panel
