# A3 — Implementation / Provenance Recompute Audit (Round 7)

**Manuscript:** Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis (single author, `05_reports/manuscript.md`, mtime 2026-09-27 06:49)
**Auditor role:** A3, implementation & number-provenance audit. Fresh first read; no prior review rounds consulted.

---

## Independence statement

I had never seen this manuscript or its repository before this assignment. I did not read `REVIEW_round6_20260926.md`, `review_r6/`, any `REVIEW_*`/`RESPONSE_*`/`REVISION_*` file, `review_r1/`–`review_r5/`, the other r7 reviewers' files, any `_PANEL_BRIEF.md`, `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, or `author_verification_statement.md`. Every number below was recomputed by me from the raw result CSVs and pipeline scripts in this repository, using `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe`. Where a recompute script overwrites a file I first byte-backed it up (`/tmp/audit_backup/`) and diffed afterwards to prove idempotency.

---

## Part 1 — Audit of the audit gate (`02_scripts/python/check_audit_assertions.py`)

**Execution result: PASS (exit code 0).** Full output:

```
OK  max I2 across 15 MR tests = 0.502 (stated <= 0.50)
OK  MR family size = 45 (5 genes x 3 estimators x 3 outcomes); I2 computed for 15 IVW tests
OK  9 §7 provenance paths present
All baseline audit assertions passed.
OK  15 MR-Egger p-values match t(df=n-2) distribution (normal-based values differ, as required)
OK  no MR p/q value is exactly 0.0 or < 1e-300
OK  Egger SE not substantially (<95%) below IVW SE; CD74 critical-care exempted (disclosed)
OK  hub directions consistent with text: 5 Mars1-down hubs + FIS1 up (logFC +1.26)
OK  Mars1 vs Mars2 Mann-Whitney P = 4.671e-01 (text 4.700e-01)
OK  Mars1 vs Mars3 Mann-Whitney P = 1.852e-18 (text 1.900e-18)
OK  Mars1 vs Mars4 Mann-Whitney P = 1.321e-03 (text 1.300e-03)
All Round-6 root-cause audit assertions passed.
```

Assertion-by-assertion adjudication — does it guard the **headline number**, or only metadata?

| # | What it checks | Guards a headline value? | Plausible error that slips past |
|---|---|---|---|
| 1 | max I² over 3 MR CSVs ≤ 0.51 | **Partial.** Guards the *bound* "up to 0.50" (§3.10), not the specific per-gene I². A mis-stated per-gene I² (e.g., FIS1 crit 0.50 printed as 0.10) passes as long as no CSV value exceeds 0.51. | Any I² transcription error that stays ≤ 0.51; also a stated max of "0.50" would pass even if the true max were 0.5099. |
| 2 | `10_mr_bh_family.csv` has exactly 45 rows | **No — metadata only.** Guards the family *size* used in the BH correction, not any q value. | A wrong `q_family_45test` (e.g., CD74 crit WM q mis-stated as 3e-15) passes with 45 intact rows. Duplicated/deleted rows are caught, but no value is. |
| 3 | 9 §7 provenance paths exist | **No — file existence only.** | Any wrong number inside an existing file passes. |
| 4 | Every MR-Egger p equals 2·t.sf(\|β/se\|, n−2) AND ≠ normal value | **YES — the strongest guard.** Directly re-verifies the headline CD14 Egger P=4.9e-2 (df=4) and CD74 crit Egger P=0.088 (df=1) from stored β/SE. 15/15 rows checked. | An error in β or SE *itself* passes as long as p is internally consistent (it validates the distribution, not the input statistics). |
| 5 | No MR p/q = 0.0 or < 1e-300 | **Format guard only.** Catches the exact regression class of the old CD74-crit-WM p=0.0, but not the value. | A mis-stored 6.6e-19 as, say, 6.6e-21 passes (still > 1e-300). |
| 6 | Egger SE ≥ 0.95 × IVW SE, `EXEMPT_EGGER_SE = {("CD74","criticalcare")}` | **Partial — consistency guard with a hardcoded exemption.** The exempted cell (SE 0.111 < IVW SE 0.325) is disclosed in §3.10, so exemption is legitimate *today*; but a future gene with the same pathology and a silently added exemption would slip. | Exemption-list drift; no assertion forces the exempted cell to remain *disclosed* in the text. |
| 7 | Hub directions in `S01_mars1_deg.csv`: 5 down + FIS1 up | **Direction only, not magnitude.** | FIS1 logFC mis-stated as +1.62 (still positive) passes; all Table 1 Δ/adj.P values are unguarded. |
| 8 | Recompute Mars1-vs-Mars2/3/4 Mann–Whitney P from `S02` raw scores vs stated 0.47 / 1.9e-18 / 1.3e-3 | **YES.** Full recompute from the source data with sensible tolerances (±0.03 for P≥1e-2, 10 % relative below). | Only these three P values; the medians (−0.792/−0.752/0.641/−0.235) and range (−3.65/3.86) are unguarded. |

**Net assessment:** 2 of 8 assertions (#4, #8) genuinely guard specific headline numbers; #1/#6/#7 guard ranges/consistency classes; #2/#3/#5 guard metadata/structure/format. The gate is a real regression fence for the two Round-6 failure classes (normal-based Egger p; silent underflow), but the majority of headline numbers in Tables 1–4 and §3.4–3.5 are **not** under gate.

### Additional gate defect (gate can silently no-op)

`check_audit_assertions.py:82-87`: if `pandas`/`scipy` import fails, the script prints a WARN and **`sys.exit(0)`** — i.e., in an environment without pandas, assertions 4–8 are skipped and the gate *passes*. A CI runner with a broken env would report green while checking nothing beyond assertions 1–3.

### Proposed concrete new assertions (A9–A16)

- **A9 (MR effect guard):** for every IVW row assert `or_ == exp(beta)`, `ci_lo == exp(beta−1.96·se)`, `ci_hi == exp(beta+1.96·se)`, and `p == 2·norm.sf(|beta/se|)` to 1e-9; spot-pin the five Table 3 CD14/CD74/HAVCR2/FIS1/HLA-DQA1 ORs to 3 s.f. against the CSV.
- **A10 (I² value guard):** assert the exact per-gene I² values stated in Tables 3/4 (e.g., FIS1 crit I² = 0.5018 → "0.50", HAVCR2 28d I² = 0.2855 → "0.29") match the CSVs at 2 s.f. — not merely their maximum.
- **A11 (Table 1 guard):** for the 8 genes in Table 1, assert `S01_immunoparalysis_direction.csv` logFC/adj.P.Val match to 2 s.f. and that the `DEG_0.3` flag matches the text's statement for ITGAM and HLA-DQB1.
- **A12 (23/22/21 guard):** recompute from `S01_immunoparalysis_direction.csv`: `sum(direction=="Mars1_down")==23`, `sum(adj.P.Val<0.05)==22`, `sum((direction=="Mars1_down")&(adj.P.Val<0.05))==21`.
- **A13 (Table 2 guard):** recompute `rescue_fraction` from `08_candidates_drugs.csv` × the DEG_0.3 rule (logFC<0 & DEG_0.3==True) and pin the seven constants 0.80/0.67/0.57/0.67/0.40/0.40/0.20.
- **A14 (validation guard):** pin `S06_auc_compare.csv` CV 0.6586→0.659 / train 0.7495→0.750; `09_external_validation.csv` orientedSum 0.6382 CI [0.5317, 0.7475], locked 0.5848; recompute the external AUC from `09_ext_risk_scores.csv`; pin calibration slope 0.5028 / intercept −0.0382.
- **A15 (BH internal-consistency guard):** recompute BH q from the 45 p values in `10_mr_bh_family.csv` and check both q columns; check each family-table p equals the corresponding outcome-CSV p (currently true — this locks it).
- **A16 (figure guard / regression test for Issue 1):** assert `sum(sig.str.lower()=="yes") == 1` in the forest builder, or pixel-scan `mr_forest.png` for ≥50 pixels of #c0392b. Additionally, change the pandas/scipy ImportError branch from `sys.exit(0)` to `sys.exit(2)` so a degraded environment fails the gate instead of silently passing.

---

## Part 2 — Numbered issues

### Issue 1 — `mr_forest.png` title promises "red = family q<0.05" but renders zero red points

【Problem】The forest figure's own title claims family-significant tests are coloured red, but the single family-significant test — CD74 critical-care weighted median, the paper's most-cited MR result — is drawn in the same grey as the other 44.

【Evidence】`_mr_diagnostics.py:81` reads `siglist.append(s.sig=="yes")`, but the CSV column `family_sig_q<0.05` stores the uppercase string `"YES"` (`10_mr_bh_family.csv:17`). `"YES"=="yes"` is `False` in Python, so `siglist` is all-False. Pixel scan of `04_figures/mr_forest.png` for colour #c0392b: **0 matching pixels** (tolerance 40, L1). The point for CD74 Weighted median / critical care sits at OR≈2.19 in the top block, grey like all others.

【Why it matters】The figure is the visual summary of the 45-test family and its legend statement is factually unfulfilled; a reader scanning for red will conclude *no* test survived correction, or will miss that exactly one did. This is the exact "figure doesn't match data" class this audit is charged with.

【Specific fix】In `_mr_diagnostics.py` change the comparison to `str(s.sig).strip().lower()=="yes"` (or compare against the CSV literal `"YES"`), regenerate `mr_forest.png`, and add assertion A16 so the case bug cannot recur. Optionally also red-fill the WM CI bar, not just the point.

### Issue 2 — DCA claim "positive net benefit over treat-none across the full threshold range" is false at the top of the range

【Problem】§3.4 states the external score "gave positive net benefit over a treat-none strategy across the full threshold range". Recomputation shows the net benefit is **exactly zero** (a tie with treat-none, not positive) for 19 of the 91 plotted thresholds (≈0.77–0.95), because no external patient's recalibrated probability exceeds those thresholds (tp=fp=0 ⇒ NB=0).

【Evidence】Recomputed from `03_results/09_ext_risk_scores.csv` (n=106, 52 deaths; refit of `_ext_calibration_dca.py`'s logistic calibration, intercept −0.0382, slope 0.5028, AUC 0.6382 — all reproduced): strictly-negative thresholds = 0, exactly-zero thresholds = 19, min NB = 0.000000 at threshold 0.77. The plotted threshold grid runs 0.05–0.95 (`_ext_calibration_dca.py:64`).

【Why it matters】"Positive across the full range" is a checkable claim that fails at the upper end; the correct statement is "never below treat-none (tied above ≈0.77)". Relatedly, "exceeded treat-all above ~0.20" is technically true (model>treat-all from threshold 0.18) but the margin exceeds 0.02 only from threshold ≈0.35 — at 0.30 the advantage is 0.2844 vs 0.2722 (Δ=0.012, n=106). The claim as phrased overstates the visual and clinical separation.

【Specific fix】Rewrite as: "…net benefit was non-negative across the plotted 0.05–0.95 range (tied with treat-none above ≈0.77) and exceeded treat-all above ≈0.20, though the margin remains small (<0.02) until ≈0.35." Optionally extend assertion A14 to recompute NB at 0.20/0.30/0.50 and pin the tie threshold.

### Issue 3 — The 30-gene signature vs the 29-gene locked model is never reconciled

【Problem】§2.6 and the abstracts define a **30**-gene signature; §3.5 says "29/30 signature genes mapped (HLA-DQA1 absent on the Illumina array)"; but the **locked L1 coefficient file itself contains only 29 genes** — HLA-DQA1 is absent at *training* time, not just externally. §3.4's phrase "zero weight to 7 of the **29** signature genes" silently adopts the 29-gene count without explanation.

【Evidence】`S06_signature_genes.csv` lists 30 genes including HLA-DQA1 (corr_with_death −0.1179, rank 19/30). `09_external_validation_coef.json` `genes` array has **29** entries; HLA-DQA1 does not appear anywhere in the JSON (neither in `coef` nor `genes`), while the 7 zero-weight genes named in §3.4 (CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B) match the JSON's 7 zero coefficients exactly. HLA-DQA1 *is* measurable in the discovery data (present in `S01_immunoparalysis_direction.csv`, logFC −0.53).

【Why it matters】A reader cannot determine whether HLA-DQA1 was dropped when the L1 model was locked (a selection event that would also change the interpretation of the external "29/30 mapped" statement, since the locked model's 29 genes may all have mapped externally) or whether the coef file is simply incomplete. This is exactly the kind of unexplained 30↔29 drift that the provenance table is supposed to preclude.

【Specific fix】State explicitly in §3.4 which gene is missing from the locked model and why (e.g., "the L1 design matrix contained 29 of the 30 signature genes because HLA-DQA1 <reason>"), and reconcile with the §3.5 mapping statement (29/30 refers to the *signature list*, the *model* carried 29/29). If the coef JSON is incomplete, regenerate it from the training pipeline.

### Issue 4 — Abstract bound "all IVW OR 0.92–1.12, P ≥ 0.24" is derived from rounded values and is strictly false

【Problem】The English abstract states the primary-outcome IVW results as "all IVW OR 0.92–1.12, P ≥ 0.24". The smallest primary IVW p-value is 0.2359 (CD14, `10_genetics_mr_outcome5086_28ddeath.csv:8`), which is **less than 0.24**.

【Evidence】IVW p on 5086: CD74 0.7178, HLA-DQA1 0.2600, CD14 0.2359, HAVCR2 0.8475, FIS1 0.4727. min = 0.2359 < 0.24. OR range 0.9233–1.1194 → "0.92–1.12" is fine.

【Why it matters】The bound was evidently formed from the *rounded* Table 3 value (0.24) rather than the stored value; strictly the abstract misstates the data. Small, but it is precisely a "text vs CSV" provenance defect of the class this manuscript's own §7 claims to have eliminated.

【Specific fix】Change to "P ≥ 0.23" (or "all P ≥ 0.236").

### Issue 5 — §3.1 cites a ROC figure as the source of the 3,597-DEG count

【Problem】"Mars1 showed 3,597 DEGs at |logFC|≥0.3 (FDR<0.05) [`04_figures/S01_roc_28d_mars1.png`]" — a 28-day-mortality ROC figure cannot evidence a DEG count. The correct source is `S01_mars1_deg.csv` (which the §7 table cites correctly).

【Evidence】I recomputed from `S01_mars1_deg.csv`: |logFC|≥0.3 & adj.P<0.05 → **3,597** (matches), and from `S01_deg_sepsis_vs_ctrl.csv` → **448** (matches). `S01_roc_28d_mars1.png` is a ROC plot (Mars1 indicator vs 28-day death, AUC 0.578 per `S06_auc_compare.csv`).

【Why it matters】A mis-cited provenance pointer, in the manuscript's flagship provenance-by-design section, undermines the §7 claim that "every reported number traces to a concrete output".

【Specific fix】Replace the figure citation with `03_results/S01_mars1_deg.csv` (or cite both, labelling the ROC as the §3.2 AUC source).

### Issue 6 — Assertion 1 under-guards the stated I² range (metadata-level, not value-level)

【Problem】The gate checks only that no CSV I² exceeds 0.51. Every per-gene I² quoted in Tables 3 and 4 (15 values) is unguarded, as is the "I² 0.00–0.29" primary-outcome range statement.

【Evidence】I manually verified all 15 Table 3/4 I² cells against the CSVs (all match at 2 s.f., incl. FIS1 crit 0.5018→0.50, HAVCR2 28d 0.2855→0.29, CD14 suscept 0.3788→0.38). The gate would not have caught a single mis-transcribed cell.

【Why it matters】The audit gate's stated purpose (script header) is to be the "root-cause guard" for stated numeric ranges vs cited CSVs; the I² family is its own target and is only half-guarded.

【Specific fix】Add assertion A10 (Part 1).

### Issue 7 — The gate passes vacuously without pandas/scipy

【Problem】`check_audit_assertions.py:82-87` catches ImportError, prints WARN, and `sys.exit(0)`. In a pandas-less environment the numeric half of the gate (assertions 4–8, which guard the headline Egger p-values and group P values) silently disappears while CI stays green.

【Evidence】Code quoted above; no counter-example needed — the branch is unconditional on import failure.

【Why it matters】A provenance gate that can no-op is weaker than no gate, because it manufactures false confidence.

【Specific fix】`sys.exit(2)` on ImportError, or make pandas/scipy hard requirements of the check.

### Issue 8 — Minor rounding slips (text↔CSV)

【Problem】Three sub-unit rounding discrepancies, none material:
(a) §3.2 table: Mars3 median printed **0.641**; exact median = 0.64048 → 0.640.
(b) §3.9: "top rescue 0.32"; exact max = 0.3182 (→0.32 ✓) — fine; but prednisone rank is 651 in the CSV vs 652 by strict `rescue > v` ranking (rank-convention/tie artefact; `S08_l1000_positive_control.csv` internally consistent).
(c) Assertion 1's tolerance (0.51) is nearly double the gap between the stated max (0.50) and the true max (0.5018) — the gate would tolerate a stated "0.50" against a true 0.5099.

【Evidence】Recomputed medians: Mars1 −0.79167, Mars2 −0.75198, Mars3 0.64048, Mars4 −0.23466. Text: −0.792 / −0.752 / 0.641 / −0.235.

【Why it matters】Individually negligible; collectively they show the text is hand-rounded from CSVs without a single rounding rule (0.64048 was rounded up, everything else down/nearest).

【Specific fix】Adopt one rounding rule (round-half-even at displayed precision) and regenerate all in-text constants from a print script; fix Mars3 0.641→0.640.

### Issue 9 — `mr_diag.png` CD74 panel title attributes family-significance to the wrong estimator

【Problem】Panel (d) is titled "CD74 — critical care (reversed direction, family-q<0.05)" but plots only the IVW and MR-Egger fits — both of which have family q > 0.05 (0.316 and 0.792). The family-significant estimate (weighted median, q≈3e-17) is not visualized anywhere in the diagnostics figure.

【Evidence】`_mr_diagnostics.py:136-142`; `10_mr_bh_family.csv:17-19`.

【Why it matters】The title invites the reader to read IVW/Egger concordance as "the family-significant signal", when the surviving statistic is the WM. The figure is not stale (slopes match the CSVs exactly: IVW 0.798/OR 2.22; the visually identical IVW and Egger lines correctly display the disclosed SE anomaly), but the caption logic conflates estimators.

【Specific fix】Retitle to "…(reversed direction; the family-significant estimate is the weighted median, q≈3×10⁻¹⁷)" or add the WM estimate to the panel.

---

## Part 3 — Stands up (verified correct, with evidence)

1. **v1.6.0 fixed the underlying data, not just the prose — verified at the byte level.** `_mr_backup_20260927/` vs current CSVs, Egger rows (gene/method/β/SE identical, p changed): CD74 crit Egger p 6.6258e-13 (normal-based) → **0.088015** (t, df=1); CD14 28d Egger p 0.0051096 (normal) → **0.048809** (t, df=4); CD74 suscept Egger p 1.6484e-4 → **0.16517** (t, df=1); CD74 crit weighted-median p **0.0 (float cancellation)** → 6.6486e-19. All 15 IVW p-values byte-identical pre/post (script's "verified identical" claim holds). `10_mr_bh_family.csv` regenerated (45 rows; CD74 crit WM family q = 2.9919e-17, sole `YES`). My independent `_editor_verify_egger.py` recompute: 15/15 Egger rows match t(n−2), 0/15 match normal. The manuscript's §2.10/§3.10 narrative ("under this correction no CD74 MR-Egger test reaches significance… CD14 family q = 0.73") matches the corrected table exactly.
2. **Table 2 provably derives from the DEG_0.3 rule, not bare logFC<0.** Under direction-only scoring the values would be IL-7 5/5=1.00, GM-CSF 5/6=0.83, IFN-γ 5/7=0.71 (demonstrated by `_recompute_table2.py`'s old→new printout); the committed CSV holds 0.80/0.67/0.57 because CD3E, ITGAM, HLA-DQB1 etc. carry DEG_0.3=False. All seven text constants (0.80, 0.67, 0.57, 0.67, 0.40, 0.40, 0.20) match `08_candidates_drugs.csv`, and re-running the script reproduced the CSV **byte-identically**. The IFN-γ "4/5 antigen-presentation" sub-claim is consistent: of {HLA-DRA, HLA-DRB1, HLA-DQA1, HLA-DQB1, CD74}, exactly HLA-DQB1 fails DEG_0.3 (logFC −0.203, adj.P 0.0174).
3. **The 23/25 · 22/25 · 21/25 consensus counts are exactly right.** From `S01_immunoparalysis_direction.csv` (25 genes): Mars1_down = 23 (all but PDCD1, LAG3); adj.P<0.05 = 22 (all but CD8B 0.0767, GZMA 0.110, LAG3 0.552) — and the 22 do include up-regulated PDCD1 (3.0e-10), exactly as the abstract's parenthetical states; down ∧ significant = 23−2 (CD8B, GZMA) = 21. All eight Table 1 effect sizes match to the printed precision (e.g., HLA-DRB1 −0.89251/1.0657e-15 → −0.89/1.1e-15; CD14 P.Value literally 0.0, matching "P<1e-300 underflow").
4. **External validation and calibration numbers all trace.** `09_external_validation.csv`: orientedSum 0.6382 CI [0.5317, 0.7475] → 0.638 (0.532–0.748); locked L1 0.5848 CI [0.4687, 0.6959] → 0.585 (0.469–0.696); n=106/52 deaths/54 survivors; 29/30 mapped with HLA-DQA1 named as missing; IRG recomputed 0.604. `S06_auc_compare.csv`: CV 0.65857→0.659, train 0.74951→0.750, Mars1 indicator 0.57819→0.578. `09_ext_calibration_dca.csv`: slope 0.5028→0.50, intercept −0.0382→−0.04, NB 0.2844@0.30→"0.28", 0.0755@0.50→"0.08". `_ext_calibration_dca.py` re-run reproduced the CSV **and** `S06_dca.png` byte-identically.
5. **`S06_dca.png` is the external cohort and is not stale.** Panel titles read "Calibration (slope=0.50, intercept=−0.04)" and "Decision curve (external, AUC=0.638)"; the script consumes `09_ext_risk_scores.csv` (E-MTAB-4451 per-symbol scores), not the discovery cohort; no normal-based Egger p or treat-all-above-model-everywhere artefact is present (treat-all correctly dominates only at low thresholds).
6. **MR Table 3/4 values match the CSVs cell-for-cell**, including the non-obvious ones: all 15 I² cells; median F 35.4/168.1/45.7/36.4/75.0 recomputed from `*_harmonised.csv` per-gene medians; instrument counts 3/4/6/6/8 summing to the stated 27; CD14 Egger intercept P=0.344 (CSV 0.34401); CD74 suscept intercept P=9.98e-5→"1.0×10⁻⁴"; CD74 crit Egger SE 0.11107 < IVW SE 0.32496 exactly as disclosed; CD14 28d per-outcome 15-test q 0.48697→"0.49".
7. **L1000 layer verified against the raw 20,413-row table:** mean 0.0064/median 0.0055/53.6 %>0/top 0.3182→"0.32"; lenalidomide rescue 0.0439, rank 5435, pct 0.2662→"top 26.6 %", wtcs 0.2058 = 0.0439·√22 as the algebraic-identity claim states; azithromycin 0.0133/9152/0.4483→"≈median"; prednisone 0.1364/651; dexamethasone 0.0315/6808. DEG counts 3,597 and 448 recomputed exactly; hub list `S05_hub_genes.csv` = the six named genes; cell-type correlations (CD14 0.773, FCGR3A 0.491, CD74→DC 0.69, HAVCR2 0.298, HLA-DQA1→B 0.681; axis CD4 0.618/CD8 0.582/DC 0.459, monocytes lowest at 0.222) all match §3.6; score medians/n per endotype and the −3.65/3.86 range match §3.2.

---

## Part 4 — Questions for the authors

1. **(Issue 3)** Why does `09_external_validation_coef.json` contain 29 genes when the signature is defined as 30? Was HLA-DQA1 dropped from the L1 design matrix at training (and if so, why — probe aggregation? collinearity?), and does the external equal-weight score use the 30-gene oriented sum or the 29-gene locked-model gene list? These two paths give different scores and only one can be the reported 0.638.
2. **(Issue 1)** The forest was regenerated 2026-09-27 06:43, after the BH table (06:46? — file mtimes differ by minutes). Please confirm the shipped `mr_forest.png` was generated from the *post*-recompute family table, and fix the case-sensitive `"yes"` comparison; can you add the A16 pixel/significance assertion to the gate?
3. **(Issue 2)** Given NB ties treat-none above ≈0.77 and the treat-all margin is <0.02 until ≈0.35, do you consider "exceeded treat-all above ~0.20" a fair clinical summary at n=106, or should it be softened as suggested?
4. **(Gate scope)** Assertion 4 validates Egger p against stored β/SE, and assertion 8 recomputes three group P values. Do you agree the remaining headline families (Tables 1–4 ORs/CIs/I², Table 2 concordances, external AUC/calibration, 23/22/21 counts) should be brought under gate via assertions A9–A15 before the repository is deposited?
5. **(Rounding policy)** Mars3's median was rounded up (0.64048→0.641) while every other displayed constant rounds down/nearest. Is there a documented rounding rule, and can the in-text constants be emitted by script rather than by hand?
6. **(Weighted-median SE)** The CD74 critical-care WM SE (0.0885) is *smaller* than the Egger SE (0.1111) on the same three SNPs — the mirror image of the disclosed Egger<IVW anomaly, and presumably a consequence of the same 3-instrument geometry. The manuscript discloses the Egger ordering but not the WM's apparent precision. Should the disclosure cover the WM SE as well?

---

## Part 5 — What I actually checked

**Files read in full:** `05_reports/manuscript.md` (302 lines, incl. the five >2000-char lines re-extracted with `sed|fold`); `02_scripts/python/check_audit_assertions.py`, `_recompute_mr_pvalues.py`, `_recompute_table2.py`, `_ext_calibration_dca.py`, `_mr_diagnostics.py`, `_editor_verify_egger.py`; `03_results/`: `08_candidates_drugs.csv`, `S01_immunoparalysis_direction.csv`, `S02_immunoparalysis_score.csv` (grouped), `S06_auc_compare.csv`, `S06_signature_genes.csv`, `09_external_validation.csv`, `09_external_validation_coef.json`, `09_ext_calibration_dca.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, `10_mr_bh_family.csv`, `S05_hub_genes.csv`, `07_hub_celltype.csv`, `07_axis_celltype.csv`, `S08_l1000_candidate_scores.csv`, `S08_l1000_positive_control.csv`, `S08_l1000_rescue_trtcp.csv` (20,413 rows, aggregated); `03_results/_mr_backup_20260927/` (all 4 files, diffed row-wise against current).

**Figures viewed:** `04_figures/S06_dca.png`, `mr_forest.png`, `mr_diag.png` (Read tool), plus a programmatic pixel scan of `mr_forest.png` for the promised red (#c0392b): 0 pixels.

**Commands executed (all under the mandated python 3.13.12):**
1. `check_audit_assertions.py` → exit 0, all 8 assertions pass (output quoted in Part 1).
2. `_editor_verify_egger.py` → 15 Egger rows: 0 normal / 15 t(n−2); headline CD74 crit: reported 0.0880149, p_normal 6.62566e-13, p_t 0.0880149.
3. `_recompute_table2.py` after byte-backing up the CSV → printed old(direction-only) vs new(DEG_0.3) fractions; output CSV **byte-identical** to backup (`diff` clean).
4. `_ext_calibration_dca.py` after byte-backing up CSV+PNG → slope 0.5028/intercept −0.0382/AUC 0.6382; NB 0.3632/0.2844/0.0755 at 0.20/0.30/0.50; CSV **and** PNG byte-identical (`diff`/`cmp` clean).
5. Ad-hoc recomputes: Mann–Whitney P (0.4671/1.852e-18/1.321e-3); 23/22/21 counts; 3,597 and 448 DEG tallies; all 15 Table 3/4 I² cells; median F per gene (35.4/168.1/45.7/36.4/75.0); L1000 mean/median/positive-fraction/max and candidate ranks/pcts; wtcs=rescue·√22; DCA NB grid (0 strictly negative, 19 exactly zero, cross vs treat-all at 0.18, >0.02 margin from 0.35); score medians/range per endotype.

**Discrepancies found (complete list):** Issues 1–9 above — forest red-highlight bug (0 red pixels); DCA "positive across full range" false for 19/91 thresholds; 30-vs-29 signature/coef mismatch; abstract "P ≥ 0.24" vs actual min 0.2359; §3.1 figure mis-citation; Mars3 median 0.641 vs 0.640; gate `exit(0)` on missing pandas; assertion-coverage gaps (metadata-only guards for I² values, Tables 1–4 effects, Table 2, validation metrics, BH values); mr_diag panel-title estimator conflation. **No fabricated number was found**: every quantitative claim I tested traces to a real CSV value at the stated precision, and the v1.6.0 revision demonstrably corrected the stored MR p-values (backup vs current) rather than only the prose.

---

## Appendix A — Assertion-by-assertion code audit

### A#1 — max I² bound (`check_audit_assertions.py:23-45`)

```python
max_i2 = 0.0
for fn in mr_files:
    ... if r.get("I2"): max_i2 = max(max_i2, float(r["I2"]))
if max_i2 > 0.51 + 1e-9: fail(...)
```

- **What it actually verifies:** `max(I2) over 15 IVW rows in 3 CSVs = 0.5018 ≤ 0.51`. Ran clean.
- **Headline targeted:** §3.10 "Heterogeneity on the primary outcome was low (I² 0.00–0.29), but several secondary-outcome tests reached higher I² (up to 0.50, e.g. FIS1 critical care)".
- **Verdict:** guards the *upper bound sentence* only. My independent recomputation confirms every stated I² cell is correct **today** (see Appendix B.4), but a regression that mis-states one cell (e.g., 0.29→0.20) while keeping max ≤ 0.51 would pass. Also note the stated "up to 0.50" vs stored 0.5018 — correct at 2 s.f., but the assertion's 0.51 head-room is ~19× the actual slack.
- **Slip example:** Table 4 FIS1 cell printed "0.05 / 0.00 / 0.05" — assertion 1 passes; A10 would fail.

### A#2 — family-size row count (`:47-58`)

- **What it verifies:** `10_mr_bh_family.csv` has exactly 45 data rows.
- **Headline targeted:** the 45-test BH family definition (§2.10, §3.10, §5.2, repeated ≥5 times).
- **Verdict:** structural guard only. It confirms the family is the right *size* but nothing about membership (5 genes × 3 estimators × 3 outcomes could in principle be 45 rows of the wrong composition) or the q values. My recompute of BH from the stored p values reproduces both q columns exactly (Appendix B.5) — A15 would lock that.

### A#3 — provenance-path existence (`:60-75`)

- **Verdict:** pure `os.path.exists` over 9 paths. Catches deleted evidence, not wrong evidence. Necessary but trivially weak. (One §7-cited path it does *not* spot-check: `03_results/09_ext_calibration_dca.csv` — the calibration CSV that backs the §3.4 slope/intercept/DCA sentence. It existed at audit time.)

### A#4 — Egger reference distribution (`:89-121`)

- **What it verifies, per Egger row:** stored `p` == 2·t.sf(|β/se|, nsnp−2) to 1e-9 **and** != normal-based value to 1e-9. 15/15 rows pass; the double condition is well designed (the second clause is what makes a regression to the normal bug *loud* rather than silent).
- **Headlines actually guarded:** CD14 28d Egger P=4.9×10⁻² (recomputed 0.048809 from β=−0.098770, SE=0.035275, df=4 — exact match), CD74 crit Egger slope P=0.088 (β=0.798285, SE=0.111074, df=1 — exact match; the normal value is 6.6e-13, a 1.4×10¹¹ inflation factor that this assertion kills).
- **Residual gap:** it validates the p against *stored* β/SE; an error upstream in β/SE (e.g., harmonisation) is out of scope. That is acceptable — A9 (OR/CI algebraic consistency) would cover the rest.

### A#5 — underflow guard (`:123-142`)

- **What it verifies:** no `p`, `p_fdr_bh`, `q_family_45test`, `p_fdr_bh_per_outcome_15test` in the 4 MR tables is 0.0 or <1e-300. Minimum stored value today: 6.6486e-19 (CD74 crit WM) — passes with ~281 orders of magnitude of margin.
- **Verdict:** correctly targets the *observed historical failure* (backup CD74 crit WM p was literally `0.0`), but checks format, not value. A regression storing 6.6e-25 (still >1e-300) would pass; A15's BH recompute would catch it because the q columns would then disagree with a BH rebuild.

### A#6 — Egger/IVW SE ordering (`:144-173`)

- **What it verifies:** for each gene×outcome, Egger SE ≥ 0.95 × IVW SE, except the hardcoded `EXEMPT_EGGER_SE = {("CD74","criticalcare")}`.
- **Verification of the exemption:** CSV Egger SE 0.111074 < IVW SE 0.324961 × 0.95 = 0.308713, so the exemption is *load-bearing* and matches the manuscript's §3.10 disclosure (0.111 vs 0.325) — legitimate, disclosed, and correctly scoped to one cell.
- **Residual gap:** nothing forces the exemption to stay disclosed. Propose A6b: if a cell is exempted, assert the manuscript contains its SE pair.

### A#7 — hub direction (`:175-187`)

- **What it verifies:** from `S01_mars1_deg.csv`, {down} = 5 named hubs, {up} = {FIS1}. Passes; FIS1 logFC +1.2599 → the printed "+1.26" and "+17.2" t (t not asserted).
- **Verdict:** direction-level guard. Table 1's magnitudes and every §3.1 Δ/adj.P are outside the gate.

### A#8 — group P recompute (`:189-204`)

- **What it verifies:** Mann–Whitney two-sided on raw `immune_function_score` per endotype from `S02_immunoparalysis_score.csv` vs stated constants, tolerance ±0.03 absolute for P≥1e-2, 10 % relative below.
- **My independent recompute:** Mars1-vs-Mars2 4.671e-01 (stated 0.47 ✓), vs Mars3 1.852e-18 (stated 1.9e-18, rel. err 2.5 % ✓), vs Mars4 1.321e-03 (stated 1.3e-3, rel. err 1.6 % ✓).
- **Verdict:** a genuine headline-value guard, and the tolerance policy is sensible. Extension: also pin the medians (−0.792/−0.752/0.640/−0.235) and n (132/176/118/53) — the medians are currently unguarded and one of them (Mars3) is mis-rounded in the text (Issue 8a).

---

## Appendix B — Verification ledger (text value ↔ stored value)

Format: claim (location) | file:row | stored | verdict.

### B.1 — Abstract & §3.1

| Claim | Source | Stored | Verdict |
|---|---|---|---|
| 23/25 directionally down | S01_immunoparalysis_direction.csv | 23 rows `direction=="Mars1_down"` (25 genes) | ✓ |
| 22/25 FDR<0.05, incl. PDCD1↑ | same | 22 rows adj.P<0.05; PDCD1 3.00e-10 (up) included | ✓ |
| 21 down ∧ significant | same | 21 (= 23 − CD8B 0.0767 − GZMA 0.1100) | ✓ |
| HLA-DRB1 Δ=−0.89, 1.1e-15 | same:3 | −0.89251 / 1.0657e-15 | ✓ |
| CD74 Δ=−0.76, 2.1e-15 | same:4 | −0.75782 / 2.0811e-15 | ✓ |
| CD14 Δ=−0.77, P underflow | same:2 | −0.76574 / P=0.0, adj.P=0.0 | ✓ |
| FCGR3A Δ=−0.61, 9.1e-11 | same:7 | −0.60975 / 9.0524e-11 | ✓ |
| HAVCR2 Δ=−0.35, 2.8e-13 | same:6 | −0.34881 / 2.8382e-13 | ✓ |
| PDCD1 Δ=+0.16, 3.0e-10 | same:8 | +0.16186 / 2.9951e-10 | ✓ |
| ITGAM Δ=−0.21, 1.7e-3, DEG_0.3=False | same:19 | −0.20844 / 1.6773e-3 / False | ✓ |
| HLA-DRA −0.47, 3.8e-7; LYZ −0.26, 3.6e-6 | same:12,14 | −0.46894/3.7715e-7; −0.25613/3.5627e-6 | ✓ |
| "all P<1×10⁻⁸" (4 genes) | same | max adj.P among the 4 = 9.05e-11 | ✓ |
| 3,597 / 448 DEGs | S01_mars1_deg.csv; S01_deg_sepsis_vs_ctrl.csv | 3,597; 448 (recomputed, \|logFC\|≥0.3 & adj.P<0.05) | ✓ (but see Issue 5 citation) |
| IVW OR 0.92–1.12 | outcome5086 CSV | 0.9233–1.1194 | ✓ |
| IVW P ≥ 0.24 | same | min 0.23590 | ✗ (Issue 4) |

### B.2 — §3.2 score table

| Endotype | n (text/CSV) | median (text) | median (stored) | P vs Mars1 (text) | P recomputed |
|---|---|---|---|---|---|
| Mars1 | 132/132 | −0.792 | −0.79167 | — | — |
| Mars2 | 176/176 | −0.752 | −0.75198 | 0.47 | 0.46714 ✓ |
| Mars3 | 118/118 | 0.641 | **0.64048** | 1.9e-18 | 1.852e-18 ✓ |
| Mars4 | 53/53 | −0.235 | −0.23466 | 1.3e-3 | 1.321e-3 ✓ |

Range −3.65/3.86 (text) = stored min/max ✓. Mars1-indicator AUC 0.578 (text) = 0.57819 (S06_auc_compare.csv) ✓. Mars3 median mis-rounded (Issue 8a).

### B.3 — §3.4/§3.5 signature & external validation

| Claim | Source | Stored | Verdict |
|---|---|---|---|
| CV AUC 0.659 / train 0.750 | S06_auc_compare.csv:2-3 | 0.658558 / 0.749507 | ✓ |
| Zero-weight genes = 7 named | 09_external_validation_coef.json | exactly 7 zeros: CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B | ✓ |
| "7 of the 29 signature genes" | json `genes` | 29 genes; HLA-DQA1 absent (Issue 3) | ⚠ |
| 30-gene signature | S06_signature_genes.csv | 30 genes incl. HLA-DQA1 (rank 19) | ⚠ (Issue 3) |
| External 0.638 (0.532–0.748) | 09_external_validation.csv:11-13 | 0.6382 [0.5317, 0.7475] | ✓ |
| Locked L1 0.585 (0.469–0.696) | same:8-10 | 0.5848 [0.4687, 0.6959] | ✓ |
| n=106, 52 deaths, 54 survivors | same:4-6 | 106 / 52 / 54 | ✓ |
| 29/30 mapped, HLA-DQA1 absent | same:2,17 | 29 / HLA-DQA1 | ✓ |
| IRG recomputed 0.604 | same:14 | 0.604 | ✓ |
| Slope 0.50 / intercept −0.04 | 09_ext_calibration_dca.csv | 0.5028 / −0.0382 | ✓ |
| NB 0.28 @0.30; 0.08 @0.50 | same | 0.2844 / 0.0755 | ✓ |
| "positive NB across full range" | recompute from 09_ext_risk_scores.csv | 19/91 thresholds NB=0 (≥0.77) | ✗ (Issue 2) |
| "exceeded treat-all above ~0.20" | recompute | cross at 0.18; >0.02 margin from 0.35 | ⚠ (Issue 2) |

### B.4 — MR Tables 3 & 4 (all cells checked against the three outcome CSVs)

Primary (5086) Table 3 — IVW OR (P), Egger OR (P), WM OR (P), Q_p/I², medF:

| Gene | IVW | Egger | WM | I² (stored→2s.f.) | medF |
|---|---|---|---|---|---|
| CD74 | 1.1193 (0.7178) ✓ | 1.0933 (0.8794) ✓ | 0.9705 (0.9374) ✓ | 0.2160→0.22 ✓ | 35.4 ✓ |
| HLA-DQA1 | 0.9233 (0.2600) ✓ | 0.9540 (0.5580) ✓ | 0.9296 (0.4106) ✓ | 0.0 ✓ | 168.1 ✓ |
| CD14 | 0.9269 (0.2359) ✓ | 0.9060 (**0.048809** = t df4) ✓ | 0.9144 (0.0649) ✓ | 0.0 ✓ | 45.7 ✓ |
| HAVCR2 | 0.9776 (0.8475) ✓ | 1.0102 (0.9546) ✓ | 0.9604 (0.8530) ✓ | 0.2855→0.29 ✓ | 36.4 ✓ |
| FIS1 | 0.9632 (0.4727) ✓ | 0.9638 (0.4911) ✓ | 0.9712 (0.7681) ✓ | 0.0 ✓ | 75.0 ✓ |

Cross-outcome Table 4 — CD14 suscept 0.9900 (0.7636)/I² 0.3788→0.38 ✓; CD74 crit IVW 2.2217 (0.014028) CI 1.175–4.200 ✓; CD74 crit Egger 2.2217 slope P **0.088015** = t df1 ✓ (normal would be 6.6e-13), intercept P 0.99987→"1.00" ✓; CD74 crit WM 2.1944, p **6.6486e-19** ✓, family q 2.9919e-17→"≈3×10⁻¹⁷" ✓; CD74 crit Egger family q 0.7921→0.79 ✓; CD74 suscept Egger slope 1.1179 P 0.16517 ✓, intercept P 9.9788e-5→"1.0×10⁻⁴" ✓; FIS1 crit I² 0.5018→0.50 ✓; HAVCR2 crit I² 0.3914→0.39 ✓; "I² 0.00–0.29" primary max 0.2855 ✓. Egger SE anomaly: 0.111074 vs IVW 0.324961 — text "0.111 vs 0.325" exact ✓. Instruments: nsnp 3/4/6/6/8, Σ=27 = text ✓. BH: CD14 28d Egger q15 0.48697→"0.49" ✓, q45 0.73046→0.73 ✓; sole family-sig row = CD74 crit WM ✓ ("only one of 45").

### B.5 — BH internal consistency (my recompute)

Sorting the 45 stored p ascending and rebuilding BH: `q15` and `q45` columns reproduce to <1e-12 relative; the single q45<0.05 row is CD74/WM/4982. The `p` column of `10_mr_bh_family.csv` equals the corresponding outcome-CSV `p` for all 45 rows (post-recompute). No underflow anywhere.

### B.6 — §3.9 L1000 (against raw 20,413-row table)

| Claim | Stored | Verdict |
|---|---|---|
| 20,413 trt_cp compounds | 20,413 rows | ✓ |
| mean 0.006 / median 0.006 | 0.00642 / 0.00554 | ✓ (2 s.f.) |
| 53.6 % > 0 | 0.53600 | ✓ |
| top rescue 0.32 | 0.31823 | ✓ |
| lenalidomide 5,435 / 26.6 % / 0.044 / wtcs 0.21 | 0.0439 / rank 5435 / pct 0.26625 / wtcs 0.2058 | ✓ |
| azithromycin 9,152 / ≈median / 0.013 / wtcs 0.06 | 0.0133 / 9152 / pct 0.44834 / wtcs 0.0626 | ✓ |
| wtcs = rescue × √22 | 0.0439×4.6904=0.2059; 0.0133×4.6904=0.0624 | ✓ |
| prednisone 0.136 / rank 651 | 0.1364 / 651 (strict `>` gives 652 — tie convention, Issue 8b) | ⚠ trivial |
| dexamethasone 0.032 / 6,808 | 0.0315 / 6808 | ✓ |

---

## Appendix C — Backup-vs-current diff (v1.6.0 data fix, explicit answer to "data or prose?")

`03_results/_mr_backup_20260927/` (mtimes 06:30) vs current CSVs (06:46). β, SE, OR, CI, Q, I², intercept columns **identical in all rows**; only `p`, `p_fdr_bh` and the regenerated family table changed:

| Cell (gene/method/outcome) | p backup | p current | distribution of backup |
|---|---|---|---|
| CD74 / MR-Egger / 4982 critcare | 6.6258e-13 | 0.088015 | normal (t df=1 is 0.088) |
| CD74 / MR-Egger / 5086 28ddeath | 0.847909 | 0.879369 | normal |
| CD74 / MR-Egger / 4980 suscept | 1.6484e-4 | 0.165165 | normal |
| CD14 / MR-Egger / 5086 28ddeath | 0.0051096 | 0.048809 | normal |
| HLA-DQA1 / MR-Egger / 5086 | 0.485956 | 0.558047 | normal |
| HLA-DQA1 / MR-Egger / 4980 | 0.682502 | 0.722146 | normal |
| CD14 / MR-Egger / 4980 | 0.321102 | 0.377264 | normal |
| CD14 / MR-Egger / 4982 | 0.0807359 | 0.155664 | normal |
| HAVCR2 / MR-Egger / 5086 | 0.951708 | 0.954613 | normal |
| HAVCR2 / MR-Egger / 4980 | 0.114757 | 0.189890 | normal |
| HAVCR2 / MR-Egger / 4982 | 0.667756 | 0.689864 | normal |
| FIS1 / MR-Egger / all three | 0.463450 / 0.849152 / 0.600377 | 0.491091 / 0.855423 / 0.619155 | normal |
| **CD74 / Weighted median / 4982** | **0.0 (float cancellation)** | **6.6486e-19** | — (was a hard zero) |
| all 15 IVW rows | unchanged | unchanged | normal, verified identical |

Backup `10_mr_bh_family.csv` vs current: same 45-row structure; the CD74/WM/4982 p moved 0.0→6.6486e-19 and all Egger rows moved as above; the set of family-significant tests is {CD74 WM critcare} in **both** versions, so no significance verdict flipped — but the *reported magnitudes* (e.g., the old Egger p of 6.6e-13, which would have looked "genome-significant") are gone from the current evidence base. The manuscript's §2.10/§3.10/§5.2 narrative matches the **current** tables exactly. Conclusion: v1.6.0 corrected the stored data, and the prose was updated to match — not a prose-only fix.

---

## Appendix D — Figure inspection notes

- **S06_dca.png** (regenerated 06:41, byte-identical to my re-run): external cohort confirmed (right panel title "Decision curve (external, AUC=0.638)"; script consumes `09_ext_risk_scores.csv`). Calibration panel title matches the CSV to 2 d.p. Treat-all correctly dominates at low thresholds only. Visual caveat: the score (red) and treat-all (green) curves are nearly superimposed until ≈0.4, so the "exceeded treat-all above ~0.20" claim is not visually obvious at n=106 (Issue 2).
- **mr_forest.png** (06:43): layout matches the CSVs (three outcome blocks; CD74 crit block at OR≈2.2 with wide IVW CI and narrow Egger/WM CIs). **Defect:** title promises "red = family q<0.05"; pixel scan found **0** pixels near #c0392b — case-sensitivity bug in `_mr_diagnostics.py:81` (Issue 1).
- **mr_diag.png** (06:43): panel (a) CD14 IVW slope −0.076 / Egger −0.099 (int −0.010) = CSV β values exactly; panel (b) funnel consistent; panel (c) leave-one-out all CIs crossing 1.0, consistent with IVW P=0.24; panel (d) CD74 crit IVW 0.798 (OR 2.22) with Egger line visually identical — a faithful depiction of the disclosed SE anomaly. No normal-based p anywhere (no p is plotted). Issue 9: panel (d) title attributes "family-q<0.05" to a panel that displays only q>0.05 estimators.
- Not stale: all three figures postdate the 06:46 CSV recompute except by minutes and match the current tables; no figure displays a superseded (normal-based) p-value.

