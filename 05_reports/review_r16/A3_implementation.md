# Round-16 Independent Blind Audit — Implementation Review (A3)

**Reviewer stance:** treated as first submission; every claim re-derived from the manuscript text or the cited CSVs. The audit gate (`check_audit_assertions.py`, 31 assertions, exit 0) was run but is treated as non-proof per the brief.

---

## § Issues

### Issue 1 — Version/commit mislabel in Data availability (PRIMARY)
【Problem】The manuscript states the evaluated commit is `fc5473b` and that this commit "is tagged v1.16.0", but the repository shows `v1.16.0` points to `1212f7b` and `fc5473b` is actually the `v1.15.0` tag.
【Evidence】`manuscript.md:263` — "a Zenodo DOI will be minted … (the current evaluated commit **fc5473b** is tagged v1.16.0)." Git: `HEAD = 1212f7be…` with tag `v1.16.0`; `git log` shows `fc5473b v1.15.0 — Round-14 (Minor) mandatory revisions`. So `fc5473b` ≠ `v1.16.0`.
【Why it matters】This directly breaks the panel's VERSION-consistency requirement (manuscript Data-availability, cover letter, and checklist must all state `v1.16.0` @ `1212f7b`). A reader who checks out `fc5473b` retrieves the *previous* (v1.15.0) code; if any result file changed between v1.15.0 and v1.16.0, the deposit would not reproduce what the text claims. It also undercuts the manuscript's central "every number traces to a deposited source file" provenance promise.
【Specific fix】Replace `the current evaluated commit fc5473b is tagged v1.16.0` with `the current evaluated commit 1212f7b is tagged v1.16.0`. Recommended: add `commit 1212f7b` to `cover_letter.md` (line 24) and to the submission checklist as well, so all three documents name the same tag *and* hash.

### Issue 2 — MR diagnostic figure index over-promises (MINOR)
【Problem】§8 lists the MR diagnostic set as "(forest, scatter, funnel, leave-one-out)", but `04_figures/` contains only `mr_forest.png` and `mr_diag.png`.
【Evidence】`manuscript.md:257` (supplementary index); directory listing of `04_figures/` returns `S01_roc_28d_mars1`, `S02_score_vs_endotype`, `S03_*`, `S06_*`, `S07_celltype`, `fig_s09_external_roc`, `fig_s10_l1000_rescue`, `mr_diag.png`, `mr_forest.png` — no scatter / funnel / leave-one-out files.
【Why it matters】A figure-reference mismatch: four plots are promised, two exist. A reviewer expecting the full diagnostic suite sees dangling references; it also weakens the "every figure traces to a deposited file" claim.
【Specific fix】Either deposit `mr_scatter.png`, `mr_funnel.png`, `mr_loo.png` (or equivalently named) or trim the §8 index to "the MR diagnostic set (forest and diagnostic plots: `04_figures/mr_forest.png`, `04_figures/mr_diag.png`)".

### Issue 3 — Audit gate is green but blind to commit provenance (GATE-INTEGRITY / "vacuous" note)
【Problem】`check_audit_assertions.py` (31 assertions, exit 0) verifies internal numeric consistency but contains **no assertion** that the manuscript's stated commit equals the repository HEAD, nor that the `v1.16.0` tag points to the evaluated commit.
【Evidence】Scan of `02_scripts/python/check_audit_assertions.py`: assertions cover max I² (≤0.50), BH family size (45), §7 path existence, MR-Egger t-dist p, OR/CI algebra, 23/22/21, external AUC/CI, calibration, DCA grid, reference-list integrity (37 / first [1] / none >37) — but nowhere does it read the Data-availability commit string or compare it to `git rev-parse v1.16.0`. The `fc5473b` vs `1212f7b` error in Issue 1 passes the gate silently.
【Why it matters】Green CI gives false assurance of provenance integrity — exactly the version-consistency class the panel asked me to police is invisible to the gate. The 31 assertions prove the *numbers* reconcile; they do **not** prove the manuscript is deposited at `1212f7b`/`v1.16.0`.
【Specific fix】Add an assertion that:
```python
import subprocess
head = subprocess.check_output(["git","rev-parse","HEAD"]).decode().strip()[:7]
tag  = subprocess.check_output(["git","rev-parse","v1.16.0"]).decode().strip()[:7]
assert head == tag == "1212f7b"
# AND parse manuscript.md Data-availability for the commit string and assert it == "1212f7b"
```
failing otherwise. This closes the coverage gap that let Issue 1 through.

### Issue 4 — Fragile escaped-pipe cell in Table 1 (MINOR / robustness)
【Problem】The ITGAM row of Table 1 embeds a literal `|` inside a cell, escaped as `\|logFC\|≥0.3`; some Markdown renderers still mis-parse this and can break the table.
【Evidence】`manuscript.md:82` — `… but below the \|logFC\|≥0.3 DEG fold-change threshold, DEG_0.3=False) |`. The backslash escapes are present, so it is *technically* valid, but it is the only table cell relying on escaping and is a single-parser-hiccup away from a broken table.
【Why it matters】The panel explicitly asks to flag unescaped/risky pipes in table cells; even an escaped pipe is a fragility worth removing before camera-ready rendering.
【Specific fix】Rephrase to avoid the pipe glyph, e.g. "… but below the absolute-logFC ≥ 0.3 DEG fold-change threshold (DEG_0.3 = False)".

---

## § Stands up (verified independent of the green gate)

1. **External validation** — `09_external_validation.csv`: AUC 0.6382, 95% CI 0.5317–0.7475, n=106, 52 deaths. Manuscript 0.638 / 0.532–0.748 / 106 / 52 — exact match. Locked-L1 AUC 0.5848 (→0.585, CI 0.469–0.696) also matches §3.5.
2. **Calibration + DCA** — `09_ext_calibration_dca.csv`: slope 0.5028 (→0.50), intercept −0.0382 (→−0.04), NB@0.30 = 0.2844, AUC 0.6382. `09_ext_dca_grid.csv`: model NB first exceeds treat-all at threshold **0.30** (0.2844 vs 0.2722); at 0.80 model NB = 0.0 while treat-all NB = −1.5472 (model NB≈0, treat-all≈−1.55, **diverging**, not converging) — exactly as the text claims. No 95% CI is stated for calibration, consistent with the brief's "NO 95% CI claimed" expectation.
3. **Immune-hub / MR / L1000 numerics** — independently recomputed: consensus immune counts 23 down / 22 FDR<0.05 / 21 both (from `S01_immunoparalysis_direction.csv`); Mars1-vs-Mars2/3/4 Mann–Whitney P = 0.4671 / 1.85×10⁻¹⁸ / 1.32×10⁻³ (matches 0.47 / 1.9e-18 / 1.3e-3); L1000 rescue ranks lenalidomide 5435 (top 26.6%), azithromycin 9152 (≈median) from `S08_l1000_candidate_scores.csv`; retained instruments 27 (CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8; FCGR3A 0/excluded) from `10_genetics_mr_harmonised.csv`; FIS1 logFC +1.2614 (→+1.26). All match the manuscript.
4. **Reference integrity** — 37 entries, numbered 1–37 in citation order; body's first citation is [1] (`manuscript.md:22`); all numbers 1–37 are cited exactly once with no gaps and none >37; ImmunoSep/Giamarellos entry [31] carries *JAMA* **335**, 775–786, DOI 10.1001/jama.2025.24175. All correct.

---

## § Questions for the authors

1. **Commit provenance:** Why does Data availability cite `fc5473b` (which git identifies as `v1.15.0`) while the `v1.16.0` tag is at `1212f7b`? Please confirm every reported CSV was regenerated/committed at `1212f7b` and not at `v1.15.0`.
2. **MR diagnostic figures:** §8 promises four MR diagnostic plots (forest, scatter, funnel, leave-one-out) but only two PNGs exist — are the remaining three intended for deposit, or should the index be trimmed?
3. **CD74 critical-care direction:** The reversed-direction CD74 critical-care signal (OR 2.22, higher predicted CD74 → worse outcome) is appropriately flagged as genotype–severity, not causal, and as overlap-inflated. Given eQTLGen↔UK-Biobank sample overlap is acknowledged, is a sample-overlap correction (e.g., Burgess/Davies/Thompson bias estimator, already cited as [17]) planned for a follow-up, or is the disclosure-as-limitation the intended final position?

---

## § What I actually checked

**Files read in full:** `manuscript.md`, `cover_letter.md`.
**CSVs read/derived:** `09_external_validation.csv`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`, `S06_auc_compare.csv`, `S02_immunoparalysis_score.csv`, `S01_immunoparalysis_direction.csv`, `S08_l1000_candidate_scores.csv`, `08_candidates_drugs.csv`, `10_genetics_mr_harmonised.csv`, `S01_mars1_deg.csv`, `S05_hub_genes.csv`; `check_audit_assertions.py` (read, not trusted).
**Computations run (independent of the gate):**
- Re-derived external AUC/CI/n/deaths, calibration slope/intercept/NB@0.30, and DCA first-crossing + NB@0.80 from the three external CSVs.
- Recomputed Mars1-vs-Mars2/3/4 Mann–Whitney P from `S02_immunoparalysis_score.csv`.
- Re-counted 23/22/21 from `S01_immunoparalysis_direction.csv`; re-read L1000 ranks and per-gene instrument counts from their CSVs; confirmed FIS1 logFC +1.26.
- Enumerated all in-text `[N]` citations in the body (1–37, all present, none >37) and confirmed the 37-entry reference list and the Giamarellos [31] volume/pages/DOI.
- `git` checks: HEAD and `v1.16.0` both = `1212f7b`; `fc5473b` = `v1.15.0`.
- `ls 04_figures/` to cross-check figure references.
**Deliberately NOT opened** (per independence discipline): `REVIEW_round*.md`, `review_r12/`–`review_r15/`, `.workbuddy/memory/`, `scirep_submission_checklist.md`, and all other `review_r16/` files. (Consequently the checklist's own stated commit could not be inspected; only the manuscript's is verifiable here, and it is wrong — see Issue 1.)

**Discrepancies found:** (a) commit mislabel `fc5473b` (Issue 1); (b) §8 MR figure index lists 4 plots, 2 exist (Issue 2); (c) audit gate has no commit-provenance assertion (Issue 3); (d) fragile escaped-pipe cell in Table 1 (Issue 4). Every headline scientific number reconciles with its deposit.

---

## VERDICT: **Minor** — with one *mandatory* fix before acceptance.

Justification: all recomputed headline statistics (external AUC/CI/n/deaths, calibration slope/intercept + NB@0.30, DCA first-crossing and 0.80 divergence, 23/22/21 immune counts, Mars1-vs-endotype P-values, L1000 ranks, 27 instruments, FIS1 +1.26) match their CSVs exactly; the reference list is intact (37 entries, first [1], Giamarellos [31] correct); tables are otherwise clean. The only substantive defect is a provenance/metadata error — the Data-availability section names `fc5473b` (actually `v1.15.0`) where it must name `1212f7b` (the true `v1.16.0`), violating the required version-consistency across manuscript/cover-letter/checklist and slipping past the green audit gate. Correcting the hash (and trimming/completing the §8 MR figure index) resolves the paper; no scientific re-analysis is warranted.
