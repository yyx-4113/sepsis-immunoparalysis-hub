# A3 — Round-17 blind implementation review (code / provenance / recompute-audit)

**Tag evaluated:** v1.17.0 · **Manuscript treated as:** first submission · **Role:** A3 (does every headline number trace to a real deposited source file, and is version/commit provenance self-consistent?) · **Target:** Scientific Reports.

---

## Issues

### Issue 1 — Commit-provenance verification (PASS; central A3 question answered)
【Problem】 None — this is a verification of the Data-availability provenance claim, required by the review contract.
【Evidence】 `git rev-parse v1.17.0` = `5e1af29611a46e171fad252574569e90a47b9934`; `git rev-parse v1.16.0` = `1212f7be9542b12fce35ac25536fa9a3d9dfd55f`; `git rev-parse 1212f7b` = `1212f7be9542b12fce35ac25536fa9a3d9dfd55f`. Therefore **v1.16.0 == 1212f7b → YES**. `git log` shows v1.17.0 (`5e1af29`) is the direct descendant of v1.16.0 (`1212f7b`), matching the manuscript §Data availability statement ("evaluated commit 1212f7b is tagged v1.16.0, and this v1.17.0 release is built on top of it"). The audit gate `check_audit_assertions.py` (#31 DA tag/commit guard) exits 0, but I re-derived the hashes independently rather than relying on the green run.
【Why it matters】 The primary A3 question — is version/commit provenance self-consistent? — is answered **yes**; the citable snapshot (v1.17.0) and the evaluated commit (v1.16.0 / 1212f7b) are correctly cross-referenced. This is the backbone of the entire reproducibility claim and it holds.
【Specific fix】 None required. Optional clarity: in §Data availability also state that v1.17.0's own commit is `5e1af29` (not only naming `1212f7b`), so the two distinct hashes are both explicit.

### Issue 2 — §8 promises an MR diagnostic set of four plots; only two are deposited
【Problem】 §8 enumerates an MR diagnostic set "(forest, scatter, funnel, leave-one-out)", but `04_figures/` contains only `mr_forest.png` and `mr_diag.png`; the scatter, funnel, and leave-one-out files are absent, and `mr_diag.png` itself is not named in §8.
【Evidence】 `ls 04_figures/` → 12 PNGs (S01_roc_28d_mars1, S02_score_vs_endotype, S03_eigengene_trait_cor, S03_top_hub, S06_dca, S06_roc_cv, S06_roc_train, S07_celltype, fig_s09_external_roc, fig_s10_l1000_rescue, mr_diag, mr_forest). No `*scatter*`, `*funnel*`, or `*loo*`/`*leave*` file exists. Manuscript §8 (line 257): "the MR diagnostic set (forest, scatter, funnel, leave-one-out)". §7 provenance (line 246) lists only `mr_forest.png` and `mr_diag.png` — i.e. §7 and §8 are internally inconsistent about how many MR diagnostic figures exist.
【Why it matters】 A supplementary figure set that is named in the index but not deposited breaks reproducibility and can trigger an editorial "missing files" hold. The MR *numerical* results are fully intact (Tables 3/4 and the three `*_harmonised.csv` files), so conclusions are not invalidated — but the deposit does not match its own index.
【Specific fix】 Preferred: deposit `mr_scatter.png`, `mr_funnel.png`, `mr_loo.png` from the analysis pipeline. If those plots were never generated, change §8 to: "the MR diagnostic plots (forest and a diagnostic overlay; `mr_forest.png`, `mr_diag.png`)" and delete the scatter/funnel/leave-one-out enumeration. Keep §7 and §8 consistent either way.

### Issue 3 — Reference [31] carries a stray trailing period after the DOI
【Problem】 Reference [31] (ImmunoSep) ends with a period after the DOI, whereas all 36 sibling entries end with the bare DOI.
【Evidence】 manuscript.md line 312 ends `…doi:10.1001/jama.2025.24175.` (trailing period); programmatic check across all 37 entries shows [31] is the **only** one with `ends_with_period=True` (entries [1]–[30], [32]–[37] all end cleanly, e.g. [30] `…doi:10.1186/cc10031`). Volume **335**, pages **775–786**, year **2025**, DOI **10.1001/jama.2025.24175** are otherwise correct; no year/DOI mismatch.
【Why it matters】 Cosmetic, but an inconsistent reference format is a routine desk-polish flag and a minor credibility signal for a manuscript whose whole pitch is meticulous provenance.
【Specific fix】 Change line 312 to end `…doi:10.1001/jama.2025.24175` (remove the trailing period) to match the other 36 entries.

### Issue 4 — No standalone "## Code availability" heading (journal compliance)
【Problem】 Scientific Reports expects a separate Code availability statement; the manuscript folds the code-release note into §Data availability with no dedicated heading.
【Evidence】 `manuscript.md` contains no `## Code availability` heading and no "Code availability" substring; the release is mentioned only inside §Data availability (lines 261–263: "Code is released under MIT with a CITATION.cff").
【Why it matters】 Missing the journal-mandated Code availability heading can prompt a mandatory formatting revision; for a reproducibility-methods paper this is an easy, expected item.
【Specific fix】 Add immediately after `## Data availability`:
"## Code availability
Analysis code is released under the MIT licence in the versioned repository at https://github.com/yyx-4113/sepsis-immunoparalysis-hub (tag v1.17.0), with a CITATION.cff."

### Issue 5 — Table 1 ITGAM cell uses a fragile escaped-pipe token `\|logFC\|`
【Problem】 The ITGAM table cell embeds an escaped-pipe sequence `\|logFC\|` that can break the table under renderers that do not honour backslash-escapes inside table cells.
【Evidence】 manuscript.md line 82: "…below the \|logFC\|≥0.3 DEG fold-change threshold, DEG_0.3=False" inside a `| … | … | … |` cell. The values themselves are correct (logFC −0.21, adj.P 1.7×10⁻³, DEG_0.3 = False).
【Why it matters】 Rendering risk only — a broken cell would visually corrupt a table that is otherwise central to the provenance story, undermining the "every number traces" presentation.
【Specific fix】 Replace "the \|logFC\|≥0.3 DEG fold-change threshold" with "the absolute-logFC ≥0.3 DEG fold-change threshold", or wrap as code: "the `|logFC| ≥ 0.3` DEG threshold" (avoids a bare pipe entirely).

### Issue 6 — DCA "divergence" at threshold 0.80 is partly a formula artifact, not a positive recommendation
【Problem】 At threshold 0.80 the model net benefit is exactly 0.00, which equals the treat-none baseline because no calibrated predicted risk exceeds 0.80; the manuscript's "model diverges from / exceeds treat-all" framing at 0.80 is numerically true (0.00 > −1.55) but can be misread as a genuine model recommendation there.
【Evidence】 `09_ext_dca_grid.csv`: threshold 0.80 → `nb_model = 0.0`, `nb_treat_all = −1.5472`. `09_ext_calibration_dca.csv` shows the calibration-corrected probabilities are bounded (max predicted risk < 0.80, since `nb_model` is 0.00 only once no subject is flagged). The genuine model-advantage window is thresholds 0.30–0.75, where `nb_model` > 0 and > `nb_treat_all`.
【Why it matters】 Not a data error — the printed numbers (first-crossing ≈0.30; NB@0.80 model 0.00 / treat-all −1.55) are exact. But the "divergence" at 0.80 should be qualified so readers do not infer the model earns a positive recommendation at high thresholds.
【Specific fix】 Add one sentence in §3.5: "At thresholds ≥0.80 the model's net benefit falls to 0.00 (equivalent to treat-none) because no calibrated risk exceeds the threshold; the model's genuine advantage over treat-all and treat-none is confined to the 0.30–0.75 range."

---

## § Stands up (verified by independent recomputation)

1. **Commit/version provenance reconciles (Issue 1).** v1.16.0 == `1212f7b`, and v1.17.0 (`5e1af29`) is built directly on it.
2. **External validation numbers are exact.** `09_external_validation.csv`: AUC 0.6382 → manuscript **0.638**; CI 0.5317–0.7475 → **0.532–0.748**; n=106, 52 deaths → **106 / 52**; 29/30 genes mapped (HLA-DQA1 absent) → matches.
3. **Consensus immune counts 23/22/21 verified.** From `S01_immunoparalysis_direction.csv`: 23 `Mars1_down`, of which 22 have adj.P<0.05 (the 22 includes PDCD1, which is up), and 21 are both down and significant (CD8B and GZMA are down but non-significant). Exactly matches §3.1.
4. **Mars1 score P-values recomputed.** Mann–Whitney U on `S02_immunoparalysis_score.csv`: Mars1 vs Mars2 P = 4.67×10⁻¹ → **0.47**; vs Mars3 1.85×10⁻¹⁸ → **1.9e-18**; vs Mars4 1.32×10⁻³ → **1.3e-3**. Match.
5. **L1000 rescue ranks verified.** `S08_l1000_candidate_scores.csv`: lenalidomide rank **5435** (rescue 0.0439), azithromycin rank **9152** (rescue 0.0133). Match.
6. **27 MR instruments verified.** `10_genetics_mr_harmonised.csv` = 27 data rows; per-gene CD74 3 / HLA-DQA1 4 / CD14 6 / HAVCR2 6 / FIS1 8 (FCGR3A absent, as stated). Match.
7. **FIS1 logFC +1.26 verified.** `S01_mars1_deg.csv`: FIS1 logFC = 1.2614, t = 17.16 → **+1.26 (t≈17.2)**. Match.
8. **Calibration + DCA grid verified.** `09_ext_calibration_dca.csv`: slope 0.5028 → **0.50**, intercept −0.0382 → **−0.04** (no CI column, consistent with "no 95% CI claimed"). `09_ext_dca_grid.csv`: model first exceeds treat-all at threshold **0.30**; NB@0.80 model **0.00** / treat-all **−1.5472** → **−1.55**. Match.
9. **CV AUC and IRG benchmark verified.** `S06_auc_compare.csv`: CV 0.6586 → **0.659**; train 0.7495 → **0.750**; IRG (E-MTAB-4451) **0.619**. Match. Mars1-vs-Other DEG DEG_0.3=True = **3597** (matches §3.1).
10. **Reference list is internally consistent.** 37 entries, numbered in order; first in-text citation is [1]; maximum reference number and maximum in-text citation are both **37**; no citation exceeds 37.

---

## § Questions for the authors

1. **FIS1 "concordant" label.** FIS1 is Mars1-*up* (logFC +1.26), yet its protective MR estimate is folded into "three hubs … concordant across all three methods, the direction predicted by the immunoparalysis model" (§3.10/§4). For a down-regulated immune gene, higher expression → protection is coherent; for an *up*-regulated passenger the same protective MR direction is observationally opposite (higher FIS1 co-occurs with the high-mortality Mars1 endotype). Could you clarify that "concordant" here refers only to the *causal* MR direction and explicitly note the observational up-regulation is directionally opposed, so the FIS1 MR should not be read as confirming the immunoparalysis model?
2. **DCA high-threshold framing (Issue 6).** Given the model NB collapses to treat-none (0.00) at ≥0.80, would you add the window caveat so the "divergence" is not read as a positive recommendation at high thresholds?
3. **L1000 prednisone caveat vs continued use of lenalidomide/azithromycin ranks.** §3.9/§5.11 already state the rescue score is necessary-not-sufficient (prednisone scores high). Is the lenalidomide/azithromycin ranking therefore presented *only* as weak directional support, and is that caveat repeated wherever the ranks are cited (Abstract, §3.9, §6)? Please confirm there is no stronger causal claim resting on the L1000 rank.
4. **Carry-forward nuance — MR primary "no causal support" headline.** The manuscript already discloses the CD14 Egger nominal signal (P=4.9×10⁻², family q=0.73) and the reversed CD74 critical-care result (family q≈3×10⁻¹⁷, opposite direction). This is handled honestly; please confirm you intend to keep the Abstract's "no causal support on the primary 28-day-death outcome" wording, which is accurate for primary IVW (all P ≥ 0.23) even though one Egger estimate is nominally significant.

---

## § What I actually checked

**Files read (directly):** `05_reports/manuscript.md`, `05_reports/cover_letter.md`; `03_results/09_external_validation.csv`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`, `S06_auc_compare.csv`, `S02_immunoparalysis_score.csv`, `S01_immunoparalysis_direction.csv`, `S01_mars1_deg.csv`, `10_genetics_mr_harmonised.csv`, `S08_l1000_candidate_scores.csv`; enumerated `04_figures/`.

**Git commands run:** `git rev-parse v1.17.0`, `git rev-parse v1.16.0`, `git rev-parse 1212f7b`, `git tag -l`, `git log --oneline -5`. Result: v1.16.0 == 1212f7b (YES); v1.17.0 = 5e1af29 is the descendant of v1.16.0.

**Computations run (independent of the manuscript's own scripts):** (a) Mann–Whitney U for immune-score medians by endotype (re-derived P = 0.467 / 1.85e-18 / 1.32e-3); (b) count of `DEG_0.3=True` in `S01_mars1_deg.csv` (= 3597); (c) per-gene instrument tally in `10_genetics_mr_harmonised.csv` (= 27: 3/4/6/6/8); (d) reference-list parse — 37 entries, max citation 37, trailing-period scan (only [31] flagged); (e) standalone code-availability-heading check (absent). I also ran `check_audit_assertions.py` (exit 0) but did **not** treat its green status as proof — every headline number above was re-derived from the raw CSVs.

**Recomputed vs manuscript — discrepancies found:** No headline-number discrepancy. The only mismatches are deposit/formatting issues, not data errors: (i) §8 names 4 MR diagnostic plots but only 2 are deposited (Issue 2); (ii) reference [31] has a trailing period after the DOI (Issue 3); (iii) no standalone Code availability heading (Issue 4); (iv) fragile `\|logFC\|` escaped pipe in Table 1 (Issue 5); (v) DCA 0.80 "divergence" is a partial formula artifact (Issue 6).

**Forbidden files NOT opened (per the panel brief):** any `05_reports/REVIEW_round*.md`; `05_reports/review_r12/` through `review_r16/` (all files); `.workbuddy/memory/` (any file); `05_reports/scirep_submission_checklist.md`; and every other `05_reports/review_r17/*` file besides `_PANEL_BRIEF.md` and this `A3_implementation.md`. I treated the manuscript as a first submission and drew every judgement from files I read and recomputed myself.

---

## VERDICT

**Minor** (with one item to watch that would escalate to **Major** only if the journal strictly enforces deposited-figure completeness).

**Justification.** The central A3 question is cleanly satisfied: every headline number I could verify — external AUC/CI/n/deaths, calibration slope/intercept, DCA grid (first-crossing 0.30; NB@0.80 model 0.00 / treat-all −1.55), consensus immune counts 23/22/21, Mars1 score P-values 0.47/1.9e-18/1.3e-3, L1000 ranks 5435/9152, 27 MR instruments, FIS1 logFC +1.26, CV AUC 0.659/train 0.750, IRG 0.619, Mars1 DEG 3597, and a 37-entry reference list with no out-of-range citation — traces exactly to a real deposited source file. Version/commit provenance (v1.16.0 == 1212f7b; v1.17.0 built on top) reconciles with git. No data-integrity defect was found.

The defects are (a) the MR diagnostic figure index gap (§8 promises scatter/funnel/leave-one-out that are not deposited — genuine, but non-data-fatal because the MR numbers are fully in Tables 3/4 and the harmonised CSVs), and (b) cosmetic items (reference [31] trailing period, missing Code availability heading, fragile escaped-pipe cell, DCA 0.80 caveat). These are all fixable by deposit or one-line edits and do not touch the scientific conclusions.

**Single most severe finding:** the missing MR diagnostic figures (scatter, funnel, leave-one-out) named in §8 but absent from `04_figures/` — **genuine** (real deposit gap), not cosmetic, though the underlying MR results remain fully available in tabular form. If Scientific Reports mandates that every referenced figure be deposited, this alone becomes a **Major** must-fix; otherwise it sits at the top of the Minor list.

**Recommendation:** accept in principle after Minor revision; explicitly require either deposit of the three MR diagnostic plots or correction of §8 to match the two figures that exist.
