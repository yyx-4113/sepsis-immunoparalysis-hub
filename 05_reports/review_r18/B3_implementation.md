# Reviewer B3 — Implementation / Reproducibility assessment (Round 18, independent)

**Manuscript:** `05_reports/manuscript.md` (tag `v1.18.0`; evaluated commit `1212f7b` = `v1.16.0`)
**Article type claimed:** Article (original research) / computational biology — methods-and-resources; contribution framed as *reproducible auditable pipeline + honest external validation + experimental blueprint*, **not** novel hub-gene discovery.
**Audit gate run:** `02_scripts/python/check_audit_assertions.py` → exit 0, all 32 assertions green.
**Reviewer stance:** every judgement below derives only from files I read and numbers I recomputed; I did not open any prior-round or other-reviewer file.

---

## § Stands up (verified — several items I suspected were broken but confirmed correct)

1. **Audit gate #30 is now genuinely derived, not hard-coded 37→38.** `check_audit_assertions.py` (assertion block 30) computes `_exp_n = max(in-text citation number)`, then checks (a) reference list length equals that max, (b) entries contiguous 1…N, (c) first body citation is `[1]`, (d) every reference is cited, (e) Vancouver first-appearance order equals numeric order, (f) no DOI trailing period. It runs against the live body text, so adding/removing a reference cannot make it spuriously pass/fail. The run reported **38 entries contiguous 1..38, first citation [1], all cited, Vancouver order preserved**. This directly answers the brief's "recently changed" item #1.

2. **FIS1 re-scoping is complete and internally consistent across all sites.** I grepped for every residual pre-revision phrasing (`three of the five assessable hubs`, `three of five assessable hubs`, `widens rather than converges`, unqualified `reduced checkpoint engagement`, `conservative approximation`, `honest independent`, `v1.17.0`) — **zero matches**. The consistent phrasing is "two of the four assessable immune hubs (HLA-DQA1, CD14)" in §3.10, §4, §5 and §6, with FIS1 explicitly "not counted among the concordant hubs / reported as a passenger-gene observation rather than model-concordant." The 4-site framing is coherent.

3. **L1000 ranks are uniformly "descriptive only / not supportive evidence" — no contradiction between §3.9 and §4/§6.** I suspected §3.9 might still use the lenalidomide/azithromycin ranks *supportively*, but it does not: §3.9 ends "the reverse-connectivity therefore supports only the **direction** of the small-molecule candidates, not their functional or clinical benefit… the L1000 'rescue' proxy is not a validated marker of immune restoration," and §4/§6 both state "that ranking is descriptive only and not supportive evidence." Consistent.

4. **Every headline external-validation / MR / AUC / calibration number traces exactly to a deposited CSV (independently recomputed).** Verified against the files: external oriented-sum AUC 0.6382 → 0.638, CI 0.5317–0.7475 → 0.532–0.748, n=106, 52 deaths (`09_external_validation.csv`); L1-locked 0.5848 → 0.585; IRG-3 benchmark 0.5288 → 0.529; calibration slope 0.50 / intercept −0.04 (`09_ext_calibration_dca.csv`); Mars1-vs-Other DEG 3597, sepsis-vs-healthy DEG 448, consensus immune counts 23/22/21; Table-2 Mann–Whitney P (Mars1 vs Mars2 0.4671, vs Mars3 1.85e-18, vs Mars4 1.32e-3); CV AUC 0.6586 → 0.659, train 0.7495 → 0.750; primary MR CD14 Egger OR 0.906 / P 0.0488 → 0.049. All match the manuscript. The green gate reflects real arithmetic consistency, not just metadata.

5. **Reference [20] is a real, resolvable record.** `Wang, C., Liu, J., Wu, Q. et al. The role of TIM-3 in sepsis: a promising target for immunotherapy? Front. Immunol. 15, 1328667 (2024), doi:10.3389/fimmu.2024.1328667` resolves (verified by fetching the DOI) to exactly that TIM-3/sepsis review — matching the brief's requirement.

6. **The DCA within-window NB margins are arithmetically correct.** Against `09_ext_dca_grid.csv`: model−treat-all = 0.0122 at 0.30, 0.0944 at 0.50 (text "0.01–0.09"), 0.1667 at 0.55, 1.0471 at 0.75 (text "0.17–1.05"). Only the *wrapper* phrase around them is wrong (see F2).

---

## Findings

### F1 — Deposited MR script does not regenerate the reported MR-Egger p-values (code↔data break)  · **Major**
【Problem】 The deposited `10_genetics_mr_run.py` computes MR-Egger p-values with a normal approximation, but the deposited `10_genetics_mr_*.csv` files (and the manuscript and the audit gate) use the t(df=n−2) distribution, so re-running the script would not reproduce the reported MR-Egger significance.
【Evidence】 `02_scripts/python/10_genetics_mr_run.py:195-196`: `egger()` uses `p_s = 2 * (1 - stats.norm.cdf(abs(slope / se_slope)))` (normal). Recomputing from the deposited CD14 values (slope −0.09877, se 0.035275, df 4): **normal p = 0.00511**, but the deposited `10_genetics_mr_outcome5086_28ddeath.csv` CD14 MR-Egger **p = 0.04881** (t-dist), which is exactly what the audit assertion 4 enforces. Same break system-wide: CD74 critical-care MR-Egger would be normal p = 0.0020 from the script vs t-dist 0.1997 in the CSV (manuscript reports "slope P = 0.088… family q = 0.79 under the corrected t-distribution"). IVW and weighted-median p-values in the script *do* match the CSV (both normal), so only the Egger column diverges.
【Why it matters】 This is the core reproducibility claim of a methods-and-resources paper: "every reported number is reproducible from a deposited file." Here the deposited *code* and the deposited *results* disagree on an entire results column. It also means the green audit gate is misleading — it validates the CSV (t-dist) but the generating script emits normal, so the gate certifies numbers the committed code cannot produce. The divergence even flips the CD74 critical-care Egger from "borderline" to "highly significant," altering which tests survive correction.
【Specific fix】 Change `egger()` in `10_genetics_mr_run.py` to the t-distribution:
```python
df_eg = len(x) - 2
p_s = 2 * (1 - stats.t.cdf(abs(slope / se_slope), df_eg))
p_i = 2 * (1 - stats.t.cdf(abs(intercept / se_int), df_eg))
```
Then re-run the script for all three outcomes (`S10_OUTCOME_ID=ieu-b-4980/5086/4982`) to regenerate `10_genetics_mr*.csv` so the deposited code and data agree. The audit assertion 4 already pins the CSV to t-dist; aligning the script closes the loop. (For full consistency you may also move IVW/weighted-median to t-dist for small n, but those already match the CSV, so Egger is the only required change.)

### F2 — §3.5 DCA sentence contradicts itself: "advantage over treat-all confined to 0.30–0.75"  · **Minor-to-Major framing error**
【Problem】 The §3.5 DCA sentence claims the model's advantage over treat-all is "confined to a window" (0.30–0.75), yet the same sentence reports model NB = 0.00 vs treat-all −1.55 at threshold 0.80, and the grid shows the model *still* beats treat-all by +1.55/+2.40/+4.09 at 0.80/0.85/0.90.
【Evidence】 `manuscript.md` §3.5 DCA sentence (extracted verbatim): "the model's advantage over treat-all is confined to a window: net benefit is higher by only 0.01–0.09 across thresholds 0.30–0.50 and by 0.17–1.05 across 0.55–0.75 … At thresholds ≥0.80 the model's own net benefit is 0.00 … (model NB 0.00 versus treat-all −1.55 at threshold 0.80)." `03_results/09_ext_dca_grid.csv` rows 0.80/0.85/0.90: `nb_model` = 0.0 / 0.0 / 0.0, `nb_treat_all` = −1.5472 / −2.3962 / −4.0943. Thus model−treat-all = +1.55 / +2.40 / +4.09 — *larger*, not confined. The within-window margins (0.01–0.09, 0.17–1.05) are correct; only the "confined to a window" wrapper is false and is refuted by the sentence's own 0.80 numbers.
【Why it matters】 A reader is led to believe the model stops beating treat-all at 0.75, when in fact its advantage over treat-all widens above 0.80. Although the manuscript heavily caveats the DCA as illustrative/optimistically biased, the self-contradiction undermines the honesty framing and is exactly the kind of clinical-utility over-statement reviewers flag.
【Specific fix】 Replace the phrase so it describes the *model's own* net benefit (vs treat-none), not its advantage over treat-all:
> "…the model's own net benefit over treat-none is positive only across 0.10–0.75 and collapses to 0.00 (treat-none) at thresholds ≥0.80, because no calibration-corrected predicted risk exceeds those thresholds; the within-window margins over treat-all are 0.01–0.09 (0.30–0.50) and 0.17–1.05 (0.55–0.75). Because treat-all net benefit falls to −1.55/−2.40/−4.09 at 0.80/0.85/0.90, the model still dominates treat-all across the whole 0.30–0.90 range — an algebraic consequence of treat-all at this prevalence (0.49), not evidence of model gain."

### F3 — §2.5 hub-consensus rule ("≥2 methods") does not match the code (all-three intersection)  · **Minor**
【Problem】 §2.5 states hub genes were those "recovered by ≥2 methods," but `run_tier1.py` forms the hub as the intersection of **all three** methods, with a frequency-based fallback only if fewer than five pass.
【Evidence】 `manuscript.md` §2.5: "Genes recovered by ≥2 methods formed the hub." `02_scripts/python/run_tier1.py:200`: `hub = set(lasso_genes)&set(rf_genes)&set(uni_genes)` (all three). Deposited `03_results/S05_hub_genes.csv` contains exactly 6 genes, each with `lasso=rf=univariate=True` (the all-three intersection; the <5 fallback never triggers).
【Why it matters】 The method is not reproducible as written: a reader implementing "≥2 of 3" obtains a different (larger) candidate hub unless the fallback coincidentally triggers. The deposited output matches the all-three rule, so the *text* is the inaccurate part.
【Specific fix】 Either change §2.5 to "Genes recovered by **all three** selectors formed the primary hub; when fewer than five passed, a frequency-based top-10 fallback (genes selected by ≥2 of three methods) was used," or change the code to a true ≥2-rule. Since the deposited S05 uses all-three, align the text.

### F4 — §2.5 "top-50 degree-centrality" candidate expansion vs code `hub_net[:20]` (top-20)  · **Minor**
【Problem】 §2.5 says the candidate set was "expanded to the top-50 degree-centrality ∩ DEG genes when sparse," but the code uses the **top-20** of the top-50 degree genes.
【Evidence】 `manuscript.md` §2.5 ("top-50 degree-centrality ∩ DEG genes"); `02_scripts/python/run_tier1.py:156` `hub_net = deg_df.head(50)` then `:165` `cand |= set(hub_net[:20])`.
【Why it matters】 Described and executed candidate pools differ; if top-50 were used the ML candidate set could change, affecting hub reproducibility. Low impact here (hub set is stable) but it is a real description mismatch.
【Specific fix】 Change §2.5 to "top-20 degree-centrality genes" (matches current code) — or change `:165` to `hub_net[:50]` and re-run if top-50 is intended. Text-to-code alignment is the minimal fix.

### F5 — Four analysis scripts hard-code the author's local absolute path, contradicting the "reproducible pipeline" claim  · **Minor**
【Problem】 `run_tier1.py`, `09_external_validation.py`, `_ext_calibration_dca.py` (and a dead `PY=...` line in `10_genetics_mr_run.py`) hard-code `D:/2026.9/极速交付…` / `C:/Users/Administrator/…`. They cannot run unmodified on a cloned repo; only `check_audit_assertions.py` uses a `__file__`-relative ROOT.
【Evidence】 `02_scripts/python/run_tier1.py:28`, `09_external_validation.py:20`, `_ext_calibration_dca.py:14` (`PROJ="D:/2026.9/…"`); `10_genetics_mr_run.py:29` (`PY="C:/Users/Administrator/.workbuddy/…"` — unused).
【Why it matters】 Directly undercuts the manuscript's central contribution claim (a reproducible, auditable pipeline). A user must hand-edit paths before anything runs.
【Specific fix】 In each script replace the hard-coded `PROJ` with:
```python
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```
and delete the unused `PY` line in `10_genetics_mr_run.py`.

### F6 (note, not a blocking finding) — `Code availability` partially duplicates `Data availability`, and MR script disables TLS verification
【Problem】 The new standalone `## Code availability` (§, line ~265) repeats the repo URL and `v1.18.0` tag already stated in `## Data availability`, and `10_genetics_mr_run.py:53-55` disables certificate verification (`CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE`) so it can talk to OpenGWAS with an expired cert.
【Evidence】 `manuscript.md` lines 261-267 (both sections cite `…/sepsis-immunoparalysis-hub`, tag `v1.18.0`); `10_genetics_mr_run.py:53-55`.
【Why it matters】 Redundancy is cosmetic; the TLS disable is a reproducibility/security caveat — fine because the MR outputs are deposited, but it should be flagged so a future re-run is aware. Neither blocks acceptance.
【Specific fix】 Trim `Code availability` to code-specific statements (licence, CITATION.cff, that code is in the same repo/tag) and add one sentence in Methods noting the OpenGWAS TLS exception was required for the cited run and that all MR outputs are deposited, so re-running is optional.

---

## § Questions for the authors
- **Q1 (re F1).** Was `10_genetics_mr_run.py` `egger()` intended to report t(df=n−2) p-values (matching the deposited CSVs and the audit), with the committed script having regressed to a normal approximation? Or were the deposited CSVs post-edited? Either way, please confirm the t-dist values are the intended ones and regenerate the CSVs from the corrected script.
- **Q2 (re F1).** Given the script currently emits normal p for IVW and weighted-median but t-dist for Egger in the CSV, do you intend t-dist for *all three* estimators (recommended for low instrument counts), or only Egger? This determines whether IVW/wmedian also need changing.
- **Q3 (re F2).** Is "confined to a window" meant to describe the model's *own* positive net benefit (vs treat-none) rather than its advantage over treat-all? Confirm so the rephrasing is precise.
- **Q4 (re F3/F4).** Was the all-three hub intersection (current code/S05) the intended rule, or the "≥2 methods" stated in §2.5? This decides whether text or code changes.

---

## § What I actually checked
**Files read:** `manuscript.md` (full, including the truncated long lines re-extracted via script); `02_scripts/python/check_audit_assertions.py`, `run_tier1.py`, `09_external_validation.py`, `_ext_calibration_dca.py`, `10_genetics_mr_run.py`.
**Scripts run:** `check_audit_assertions.py` → exit 0, 32 assertions green (noted: green proves CSV arithmetic self-consistency, *not* that the generating code reproduces the CSVs — see F1).
**Result CSVs examined:** `09_external_validation.csv`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`, `S01_mars1_deg.csv` (11519 rows; DEG_0.3 = 3597), `S01_deg_sepsis_vs_ctrl.csv` (DEG_0.3 = 448), `S01_immunoparalysis_direction.csv` (23/22/21), `S02_immunoparalysis_score.csv`, `S05_hub_genes.csv` (6 genes, all-three), `S06_auc_compare.csv` (CV 0.6586, train 0.7495, Mars1 0.5782, IRG 0.619/0.648), `08_candidates_drugs.csv`, `S08_l1000_candidate_scores.csv` (lenalidomide 5435, azithromycin 9152), `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, `10_mr_bh_family.csv` (1 family-significant test).
**Values recomputed vs manuscript:** external AUC/CI/n/deaths, L1 0.585, IRG-3 0.5288, calibration 0.50/−0.04, Mars1 DEG 3597, sepsis-vs-healthy 448, consensus 23/22/21, Table-1 gene logFC/adj.P, Table-2 concordance fractions, Table-2 immune-score P-values, CV/train AUC, primary MR IVW min P 0.236 (≥0.23), CD14 Egger OR 0.906 / P 0.0488, DCA grid model−treat-all at 0.30/0.50/0.55/0.75/0.80/0.85/0.90.
**Regression-sweep greps (all clean):** no `three of the five assessable hubs`, `widens rather than converges`, `reduced checkpoint engagement` (unqualified), `conservative approximation`, `honest independent`, or `v1.17.0`; Tables 1–5 each appear exactly once; "independent in cohort and platform but not in label" consistent in Abstract/§3.5/§4; FIS1 "two of the four assessable immune hubs" consistent in §3.10/§4/§5/§6.
**Figure index cross-check:** enumerated `04_figures/` — S01, S02, S03A/B, S06A/B/C, S07, S09, S10, `mr_forest.png`, `mr_diag.png` all present and matching §8.
**Discrepancies found:** (1) MR-Egger p normal-vs-t-dist between script and CSV (F1, Major); (2) DCA "confined to a window" self-contradiction (F2); (3) hub "≥2 methods" vs code all-three (F3); (4) top-50 vs top-20 (F4); (5) hard-coded paths (F5). No untraceable reported number was found; no missing/extra figure or table.

---

## VERDICT — **Major** (revise; not a desk-reject)

The manuscript is, on the whole, unusually disciplined about provenance: the audit gate is now genuinely derived (not hard-coded), FIS1 re-scoping is complete and consistent across all four sites, the L1000 ranks are uniformly "descriptive only," the 38-reference list is contiguous and correctly ordered, ref [20] resolves, and every headline number I recomputed matches its deposited CSV exactly. However, one finding is a genuine reproducibility break that a methods-and-resources paper cannot ship as-is: the deposited `10_genetics_mr_run.py` computes MR-Egger p-values with a normal approximation while the deposited CSVs/manuscript/audit use the t-distribution, so the committed code does **not** regenerate the reported MR-Egger significance (F1). Compounding this, the green audit gate gives false assurance because it validates the CSV rather than the generator. The DCA "confined to a window" sentence self-contradicts its own 0.80 numbers (F2), and three smaller description-vs-code mismatches (F3–F5) remain. None of these is a desk-reject hard-fail: there is no data fabrication, no untraceable number, and every correct value is present and internally audited; all issues are fixable by editing the MR script (Egger → t-dist, regenerate CSVs), rephrasing one DCA sentence, and aligning three method descriptions / hard-coded paths. I recommend **Major revision** with those specific corrections; on receipt of a script-and-CSV-consistent resubmission this would be acceptable.
