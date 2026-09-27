# Scientific Reports — submission compliance checklist (v1.18.0)

Target journal: **Scientific Reports** (Nature Portfolio / Springer Nature). JIF 2024 ≈ 3.9, JCR Q1 (multidisciplinary; verify current JCR/IF at submission); open access, APC ≈ USD 2,190 (verify current APC at submission).
Article type in system: **Article** (the only original-research format; "Methods & Resources" is not a separate track — the contribution is described as a computational-biology / methods-and-resources *report* in the text).

## Format items verified in manuscript.md (v1.11.0)
- [x] **Title** ≤ 20 words, single scientific sentence, no subtitle/colon pun (17 words).
- [x] **Abstract** unstructured, ≤ 200 words (198), no references. (Nature policy: no citations in abstract.)
- [x] **Keywords** ≤ 6 (6 used).
- [x] **Article structure**: Title page → Abstract → Introduction → Results → Discussion → Methods → References → Acknowledgements → Author contributions → Data availability → Competing interests → (Figure/Table legends). Matches Sci Rep expected order.
- [x] **References**: Nature style (numbered, square brackets in text accepted; journal abbreviations, volume bold, ≤ 60 refs — currently 37, all with DOIs backfilled). No footnotes used.
- [x] **Data availability statement** present and mandatory (real GitHub repo URL, tag v1.18.0; Zenodo DOI on acceptance).
- [x] **Author contributions**, **Competing interests**, **Funding**, **Ethics statement** all present.
- [x] **Acknowledgements** added (optional but present).
- [x] **Generative-AI disclosure** in Methods (§2.12) per Nature Portfolio policy — mandatory because an LLM was used in manuscript preparation; no AI-generated images; AI not an author.
- [x] **Display items** ≤ 8 in main text (4 tables; all figures are Supplementary).
- [x] Audit (`check_audit_assertions.py`, 32 assertions) passes.

## Items to complete before clicking "Submit"
- [ ] **Compile a single submission file** (Sci Rep accepts one PDF/Word ≤ 3 MB for first submission, text + figures together). The manuscript currently references figures as `Fig. S0x` and the PNGs live in `04_figures/` — they must be embedded for the PDF/Word build. Use the manuscript-submission-pack workflow to produce `manuscript.docx`/`manuscript.pdf` with inline figures.
- [ ] **Supplementary Information** as one consolidated PDF (S01–S12) — currently deposited as separate CSV/PNG in `03_results/` and `04_figures/`; package per Sci Rep SI rules.
- [ ] **Reporting summary / policy compliance questionnaires** in the submission system (nature.com/srep): confirm "used/analysed research data?" = **Yes** (public GEO/ArrayExpress re-analysis); complete the AI-use question honestly (mirror §2.12); complete the ethics/IRB questionnaire (n/a for de-identified public data, but state).
- [ ] **In-text citation style** is `[n]` (brackets). Nature/Sci Rep also accept this; the typesetter converts to superscript. Optional: convert `[n]` → superscript for closer-to-final formatting (not blocking).
- [ ] **Affirmations**: confirm the manuscript is not under consideration elsewhere; all raw inputs are publicly re-used; no new primary data generated.
- [ ] **APC / funding**: confirm APC payment route (no grant; author self-funded) before acceptance.

## Outstanding scientific caveats (already disclosed in manuscript; restate if asked)
- MR layer is hypothesis-generating (no primary IVW significance; sample overlap uncorrected; Steiger test not done — Limitation 13).
- Repositioning uses curated response-gene concordance, not direct target overlap; LINCS L1000 evidence covers only 2/7 candidates.
- Functional validation is a design blueprint (S11), not data.

## Version control
- Commit `d61ce25` was v1.12.0; `0f7f907` was v1.13.0; `800063e` was v1.14.0; `fc5473b` was v1.15.0; `1212f7b` was v1.16.0; `5e1af29` was v1.17.0; **v1.18.0** is the current release (built on top of v1.16.0 / commit `1212f7b`). The canonical repo remains `github.com/yyx-4113/sepsis-immunoparalysis-hub`.

## Round-13 (2026-09-27) independent blind-panel outcome
- Verdict: **Minor (required corrections, Path A — same article type, no new data, no downgrade, no desk-reject)**.
- Tier-1 fixes applied in v1.14.0: DCA prose now matches deposited `09_ext_dca_grid.csv` (model exceeds treat-all from ≈0.30; diverges at 0.80 — no more "converging near 0.80"); nivolumab re-described as Phase-1b safety/PK (not "showed no benefit"); calibration-slope 95% CI (0.11–0.95) removed (was untraceable to any script); ITGAM table pipe escaped.
- Tier-2 fixes applied: HAVCR2/TIM-3 direction vs exhaustion rephrased (reduced checkpoint engagement, not canonical TIM-3-up exhaustion); MHC-II LD family-independence caveat added; "near-random 0.529" softened to "weak reference only (CIs overlap)"; article-type gloss lowercased.
- **Tier-3 renumbering completed in v1.15.0 (no longer deferred):** references are now numbered in order of first appearance (Vancouver-compliant); audit gate #23 was made number-agnostic (matches ImmunoSep/Giamarellos entry by author+journal, not by label) so the gate survives renumbering; abstract "Peng et al." named mention removed (now "0.619 reported on this cohort"). 37 references, all DOIs intact.

## Round-14 (2026-09-27) independent blind-panel outcome
- Verdict: **Minor (no Major, no desk-reject)** — panel noted the manuscript is "close to Accept" but flagged residual defects that must be cleared before a clean Accept.
- Mandatory fixes applied in v1.15.0: (a) §3.1 PD-1/TIM-3 framing — now states PD-1 up-regulation is the recognised exhaustion marker while the Mars1 program shows *down*-regulated HAVCR2/TIM-3 (reduced checkpoint engagement), removing the internal contradiction; (b) §5.2 MHC-II family-independence caveat — corrected a genomic-error introduced in v1.14.0 ("CD74 and HLA-DQA1 lie within the same MHC-II region"); CD74 (chr5q32) and HLA-DQA1 (chr6p21.32) are on different chromosomes, so the caveat is now framed on overlapping hypothesis structure (same gene × multiple estimators/outcomes) instead; (c) Data availability version tag corrected v1.13.0→v1.15.0; (d) Vancouver reference renumbering (above).
- Round-14 residual/non-blocking notes carried forward: one reviewer suggested the external-validation magnitude framing could be tightened further, but the panel agreed the current "honest, modest" framing is appropriate and not a blocker.

## Round-15 (2026-09-27) independent blind-panel outcome
- Verdict: **all four experts returned Minor — no Major, no desk-reject, no format hard-fail.** The panel converged on only minor/cosmetic items, confirming v1.15.0 is scientifically sound and honestly framed.
- Editor-verified two flagged "material" items as FALSE POSITIVES: (a) the "39% 28-day mortality" is correctly attributed to the MARS-consortium literature (ref [5]), not to the author's GSE65682 subset (which the reviewer recomputed as 34.1%) — different cohorts, no error; (b) prose `\|logFC\|` renders literally in markdown (no table header/separator), so no escaping needed — the one true table-cell instance was already escaped in v1.14.0.
- Genuine fixes applied in v1.16.0: (a) calibration "under-fitting slope of 0.50" → "sub-ideal slope of 0.50 (over-confident predictions)" (slope < 1 = over-confident, not under-fitting); (b) umbrella term "immunostimulatory" → "immune-modulating" (azithromycin is anti-inflammatory, not stimulatory); (c) "non-immune passenger" → "non-immune (mitochondrial-fission) passenger" (softens overstatement); (d) Data availability recorded the evaluated commit. Audit gained a #30 reference-integrity guard (37 entries, first citation [1], no number > 37).
- **Correction carried from Round-16:** the v1.16.0 Data-availability edit stated "the current evaluated commit **fc5473b** is tagged v1.16.0", but `fc5473b` is actually **v1.15.0** (v1.16.0 = `1212f7b`). This was a self-contradiction introduced in v1.16.0 and fixed in v1.17.0 (now "current evaluated commit **1212f7b** is tagged v1.16.0, and this v1.17.0 release is built on top of it"). Audit gained a #31 tag/commit-hash consistency guard that cross-checks the DA clause against `git rev-parse <tag>` to prevent regression.

## Round-16 (2026-09-27) independent blind-panel outcome
- Verdict: **all four experts returned Minor — no Major, no desk-reject, no format hard-fail.** Two reviewers (Implementation + Venue) independently converged on one genuine defect: the v1.16.0 Data-availability commit-hash self-contradiction (above). The Venue reviewer additionally flagged that the ImmunoSep reference year (2026) disagreed with its DOI (10.1001/jama.**2025**.24175 → 2025).
- Genuine fixes applied in v1.17.0: (a) Data-availability commit hash corrected `fc5473b` → `1212f7b` (v1.16.0's true commit), with explicit lineage note to v1.17.0; (b) ImmunoSep reference year `(2026)` → `(2025)` to match the DOI; (c) audit #31 added ( DA tag/commit consistency vs `git rev-parse`). Version labels bumped manuscript/cover-letter/checklist v1.16.0→v1.17.0.
- After v1.17.0 the manuscript carries no remaining Major or desk-reject risk and no known self-contradiction; a Round-17 panel is convened to confirm an explicit Accept.

## Round-17 (2026-09-28) independent blind-panel outcome
- Verdict: **2 Major (domain, design) + 2 Minor (implementation, venue); 0 desk-reject.** Consolidated report: `05_reports/REVIEW_round17_20260928.md`; expert files `05_reports/review_r17/A1_domain.md`–`A4_venue.md`.
- **Editor-verified false positive:** all three of A1, A2 and A3 independently flagged §8 as naming four MR diagnostic plots while only two PNGs exist. Reading `02_scripts/python/_mr_diagnostics.py` shows `mr_diag.png` is a 2×2 composite whose panels *are* the CD14 scatter, CD14 Egger funnel, CD14 leave-one-out and CD74 critical-care scatter. No file is missing; the defect is an ambiguous index, corrected in v1.18.0 (T2.5). This is recorded because three-expert convergence was still wrong.
- Genuine fixes applied in v1.18.0 (all Tier-1 restatements, no new analysis required): (a) **FIS1** removed from "concordant … the direction predicted by the immunoparalysis model" at all four sites — FIS1 is Mars1-*up*-regulated (logFC +1.26) so a protective MR opposes its own observational association; (b) **DCA** advantage restricted to the 0.30–0.75 window with the ≥0.80 tie-to-treat-none explained (the −1.55 treat-all value is algebraic at prevalence 0.49); (c) **calibration** disclosed as test-set-nested and illustrative; (d) **L1000** ranks for lenalidomide/azithromycin demoted from supportive to descriptive-only (prednisone at the 3.2nd percentile refutes the axis); (e) **Abstract** MR wording made specific (no significant IVW; CD14 Egger P = 0.049; CD74 critical care reversed); (f) **"independent"** qualified everywhere as cohort/platform-only, not label-independent; (g) **HAVCR2/TIM-3** downgraded to net lower bulk expression, with new ref [20] (Wang et al., *Front. Immunol.* 15, 1328667, 2024) citing and reconciling the opposing sepsis TIM-3-up literature; (h) Table renumbering (new Table 2), Code availability heading, ref [31] trailing period removed, BH "dependence-ignoring" wording, escaped-pipe cell.
- Reference list grew 37 → 38 entries with the insertion at [20]; the audit gate's count expectation was changed from a hard-coded 37 to a value derived from the body's maximum citation number, so future insertions cannot fail it spuriously.
- Abstract re-measured at **193 words** (cap 200) after the MR clause was added.
