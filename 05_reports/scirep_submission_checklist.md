# Scientific Reports — submission compliance checklist (v1.15.0)

Target journal: **Scientific Reports** (Nature Portfolio / Springer Nature). JIF 2024 ≈ 3.9, JCR Q1 (multidisciplinary; verify current JCR/IF at submission); open access, APC ≈ USD 2,190 (verify current APC at submission).
Article type in system: **Article** (the only original-research format; "Methods & Resources" is not a separate track — the contribution is described as a computational-biology / methods-and-resources *report* in the text).

## Format items verified in manuscript.md (v1.11.0)
- [x] **Title** ≤ 20 words, single scientific sentence, no subtitle/colon pun (17 words).
- [x] **Abstract** unstructured, ≤ 200 words (198), no references. (Nature policy: no citations in abstract.)
- [x] **Keywords** ≤ 6 (6 used).
- [x] **Article structure**: Title page → Abstract → Introduction → Results → Discussion → Methods → References → Acknowledgements → Author contributions → Data availability → Competing interests → (Figure/Table legends). Matches Sci Rep expected order.
- [x] **References**: Nature style (numbered, square brackets in text accepted; journal abbreviations, volume bold, ≤ 60 refs — currently 37, all with DOIs backfilled). No footnotes used.
- [x] **Data availability statement** present and mandatory (real GitHub repo URL, tag v1.15.0; Zenodo DOI on acceptance).
- [x] **Author contributions**, **Competing interests**, **Funding**, **Ethics statement** all present.
- [x] **Acknowledgements** added (optional but present).
- [x] **Generative-AI disclosure** in Methods (§2.12) per Nature Portfolio policy — mandatory because an LLM was used in manuscript preparation; no AI-generated images; AI not an author.
- [x] **Display items** ≤ 8 in main text (4 tables; all figures are Supplementary).
- [x] Audit (`check_audit_assertions.py`, 30 assertions) passes.

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
- Commit `d61ce25` was v1.12.0; `0f7f907` was v1.13.0; `800063e` was v1.14.0; this build is **v1.15.0** (commit + tag `v1.15.0` to be pushed). The canonical repo remains `github.com/yyx-4113/sepsis-immunoparalysis-hub`.

## Round-13 (2026-09-27) independent blind-panel outcome
- Verdict: **Minor (required corrections, Path A — same article type, no new data, no downgrade, no desk-reject)**.
- Tier-1 fixes applied in v1.14.0: DCA prose now matches deposited `09_ext_dca_grid.csv` (model exceeds treat-all from ≈0.30; diverges at 0.80 — no more "converging near 0.80"); nivolumab re-described as Phase-1b safety/PK (not "showed no benefit"); calibration-slope 95% CI (0.11–0.95) removed (was untraceable to any script); ITGAM table pipe escaped.
- Tier-2 fixes applied: HAVCR2/TIM-3 direction vs exhaustion rephrased (reduced checkpoint engagement, not canonical TIM-3-up exhaustion); MHC-II LD family-independence caveat added; "near-random 0.529" softened to "weak reference only (CIs overlap)"; article-type gloss lowercased.
- **Tier-3 renumbering completed in v1.15.0 (no longer deferred):** references are now numbered in order of first appearance (Vancouver-compliant); audit gate #23 was made number-agnostic (matches ImmunoSep/Giamarellos entry by author+journal, not by label) so the gate survives renumbering; abstract "Peng et al." named mention removed (now "0.619 reported on this cohort"). 37 references, all DOIs intact.

## Round-14 (2026-09-27) independent blind-panel outcome
- Verdict: **Minor (no Major, no desk-reject)** — panel noted the manuscript is "close to Accept" but flagged residual defects that must be cleared before a clean Accept.
- Mandatory fixes applied in v1.15.0: (a) §3.1 PD-1/TIM-3 framing — now states PD-1 up-regulation is the recognised exhaustion marker while the Mars1 program shows *down*-regulated HAVCR2/TIM-3 (reduced checkpoint engagement), removing the internal contradiction; (b) §5.2 MHC-II family-independence caveat — corrected a genomic-error introduced in v1.14.0 ("CD74 and HLA-DQA1 lie within the same MHC-II region"); CD74 (chr5q32) and HLA-DQA1 (chr6p21.32) are on different chromosomes, so the caveat is now framed on overlapping hypothesis structure (same gene × multiple estimators/outcomes) instead; (c) Data availability version tag corrected v1.13.0→v1.15.0; (d) Vancouver reference renumbering (above).
- Round-14 residual/non-blocking notes carried forward: one reviewer suggested the external-validation magnitude framing could be tightened further, but the panel agreed the current "honest, modest" framing is appropriate and not a blocker.
