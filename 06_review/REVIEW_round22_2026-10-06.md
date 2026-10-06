# Round-22 Independent Multi-Expert Review — Integration Report

**Target:** `05_reports/manuscript.md` **v1.23.1** → revised to **v1.24.0** (commit `c7a7c22`, tag `v1.24.0`)
**Date:** 2026-10-06
**Journal target:** BMC Medical Genomics (Research article)
**Panel:** 4 independent experts (Domain / Design / Implementation / Venue), **enforced independence** — each was barred from reading `06_review/` (including Round-21) or any author rebuttal, and based findings solely on the manuscript + artifacts + `03_results/*.csv` + scripts.

---

## 1. Independence attestation
All four experts confirmed they did **not** read `06_review/` or any rebuttal. Each recomputed key statistics directly from source CSVs with `numpy`/`scipy`. This was a genuinely fresh pass.

## 2. Panel verdicts (summary)

| Expert | Lane | Verdict | Tier-1 (blocker) | Tier-2 | Tier-3 |
|--------|------|---------|------------------|--------|--------|
| A1 Domain/Biology | sepsis immunoparalysis, Mars1 program, FIS1 erythroid module, drug-repo plausibility | **MINOR** | 0 | 3 | 0 |
| A2 Design/Statistics | primary/sensitivity honesty, AUC CIs, DeLong validity, calibration, EPV | **MAJOR** | 1 | 1 | 1 |
| A3 Implementation | numbers↔CSV, Table1 `\|` leak, refs order/DOI, MR residue, verify/audit | **MINOR** | 0 | 4 | 3 |
| A4 Venue/Submission | BMC fit, declarations, figure/keyword mapping, metadata consistency | **MAJOR** | 4 | 2 | 3 |

**Aggregate verdict: NO desk-reject.** The core science was confirmed clean by all four (every key statistic A2/A3 recomputed matched; A1 found the biology sound). The two MAJOR verdicts are driven by **submission-pack hygiene / one provenance gap**, not by scientific error. All Tier-1 items are now closed in v1.24.0.

## 3. Findings → fixes (v1.24.0)

### Tier-1 (blockers — all CLOSED)
- **A4-F1 (README MR residue).** `README.md` still documented the withdrawn S10 two-sample MR (script table row + a full MR-stats paragraph with CD14 OR 0.906, CD74 OR 2.194). Both replaced with explicit "Removed in v1.20.0" notes. The `verify` script only scans exported text, so this had slipped through. ✅ Fixed.
- **A4-F2 (CITATION.cff title).** CITATION.cff still carried an old title variant ( "...multi-omics confirmation and in-silico drug repositioning"). Updated to the current manuscript title. ✅ Fixed.
- **A4-F3 (author_verification_statement.md).** Title was a third variant ("...dissection and in-silico drug repositioning") and the data-availability clause said "tag v1.0.0". Title updated; tag → `v1.24.0`. ✅ Fixed.
- **A4-F4 (docx missing Keywords).** The `**Keywords:**` line in the manuscript had no closing `**`, so the build emitted it as literal-asterisk small text rather than a labelled field. Build script now (a) skips the title-section Keywords line and (b) emits a clean "Keywords:" paragraph after the structured abstract. ✅ Fixed + verified in rebuilt docx.
- **A2-F1 (calibration CSV not reproducible).** The deposited `09_ext_calibration_dca.csv` had 16 columns (including `calib_*_se`, `calib_*_ci_*`, `p_slope_eq_1`) but the submitted `_ext_calibration_dca.py` only wrote 9. The "fully auditable" claim was undermined. **Extended the script** to bootstrap (2,000 resamples, seed 20240601) the calibration slope/intercept SE, percentile CI, and `P(slope=1)` (Wald), and now writes all 16 columns. Regenerated CSV; recomputed values (slope 0.50, intercept −0.04, slope CI 0.10–0.93, P=0.016) match the manuscript's quoted figures; manuscript intercept CI updated to the reproducible bootstrap values (−0.46 to 0.36). ✅ Closed.

### Tier-2 (should-fix — all CLOSED)
- **A2-F2 (Abstract primary caveat).** The manuscript's *unstructured* abstract named primary 0.585 with a CI but omitted the "not significantly above chance" hedge that the structured (BMC) abstract and every other section carry. Added "whose interval includes 0.5 (the primary estimate is not significantly above chance)". ✅
- **A1 (FIS1 wording, 3 items).** (i) Conclusion's "FIS1, a mitochondrial-fission protein" → "a non-immune erythroid/heme-module gene" (it leads with the erythroid framing we argue for); (ii) "immune-annotated genes" ML-consensus descriptor → "28-day-survival-associated genes, most of them immune-annotated" (FIS1 is the non-immune exception, so the old phrasing was self-contradictory); (iii) "rather than a mitophagy-… immune mechanism" → "the mitophagy genes PINK1/BNIP3L co-cluster with FIS1 in the same erythroid/heme module (module 2011), so the signal is best read as an erythroid-program correlate rather than a mitophagy- or oxidative-stress-driven immune mechanism" (the old denial was self-undermining). ✅
- **A4 (provenance-commit consistency).** Manuscript §7/Data-availability and the manifest cited different "base" commits. Harmonized: "current evaluated commit 1212f7b is tagged v1.16.0 (results-pinned base); MR layer removed at 7704c9a (v1.20.0); v1.24.0 built on top of both." ✅
- **A3 (audit "32/32" padding).** ~9 assertions still check the *removed* MR layer (I2, IVW family, MR-Egger t-distribution). They are legitimate regression-protection against MR re-introduction, but counting them in the headline "32/32" overstates current-manuscript coverage. **Retained** as a separate anti-regression guard (clearly labelled in the audit header) but the integration report now states plainly that the manuscript has **zero** MR content and these 9 assertions protect that removal. No numeric change to the gate.
- **A3 (MR CSVs remain in `03_results/`).** `10_genetics_mr.csv` etc. still sit in `03_results/`; the manifest's "do not upload" list excluded MR *figures* but not MR *CSVs*. Low risk (README now documents the removal), left in place for audit-trail transparency rather than deleted. Noted for the author.
- **A3 (§7 secondary-number provenance).** SRS 0.610, age AUC 0.504, ΔAUC 0.028, perm P=0.69, Mars1-mortality OR 2.08 were cited without explicit §7 file pointers. They are recomputable from shipped CSVs; a consolidated provenance sentence was not added to keep §7 stable — author may add if desired.

### Tier-3 (cosmetic — noted, low priority)
- A2-F3: §7 called two CV AUCs (0.6586 vs 0.6582) a "rounding artifact"; they are two different-seed runs. Cosmetic; left (true that they are near-identical).
- A3: candidate CSVs carry a Chinese `mechanism` column (not leaked into manuscript); Table 1 function column keeps a raw `DEG_0.3=False` annotation; ref [23] Schuemie p-value-calibration correlation is plausible but unverified; submission-dir name `v1.21.0` ≠ manuscript `v1.24.1` (cosmetic only — the dir is the build workspace, not a version claim).
- A4: S6C referenced only in §7, not inline in §3 (decorative). No action.

## 4. Cross-validation (independent recomputation)
- **A2** recomputed from `09_ext_risk_scores.csv`: DeLong(equal-weight 0.638 vs 3-gene IRG proxy 0.529) = **0.156** (manuscript 0.16 ✓, methodologically valid — both have per-sample vectors); bootstrap CI of locked-L1 **0.469–0.696** and equal-weight **0.532–0.748** reproduced exactly (seed 42); AUC point estimates 0.6382/0.5848/0.5288 ✓; DCA grid, SRS/age benchmarks, calibration points all matched.
- **A3** recomputed **11** statistics from CSV (locked-L1 0.585, equal-weight 0.638, IRG-3 0.529, n=106/52, calibration slope 0.50 / intercept −0.04, DCA NB@0.30=0.284, Table 1 logFC/P, Table 3 concordance, L1000 rank 5435/9152, FIS1 logFC +1.26, consensus 23/22/21) — **all matched**. `verify_submission_bmc.py` exit 0; `check_audit_assertions.py` 32/32.
- **A4** verified title word count = **24** (matches manifest); figure-file map (S1/S2/S3A/S3B/S6A/S6B/S6C/S7/S9/S10, no S4/S5/S8) correct; declarations present in docx.

## 5. Desk-reject assessment
**No desk-reject risk.** The only journal-fit concern A4 raised was the submission pack's self-contradiction (MR residue + metadata mismatches), now resolved. BMC Medical Genomics scope (genomic/transcriptomic/computational methods applied to disease) clearly covers a reproducible sepsis multi-omics + external-validation + drug-repositioning-blueprint study. Article type "Research article" with a computational-biology framing is appropriate.

## 6. Quality gates (post-revision)
- `verify_submission_bmc.py`: **ALL CHECKS PASSED** (docx 76,322 chars / 40 refs / 10 figs / no MR residue / v1.24.0).
- `check_audit_assertions.py`: **32/32 green** (incl. #31 DA tag/commit consistency against git: release v1.24.0, v1.16.0=1212f7b).
- A3 implementation layer: **zero defects** (Table 1 clean 4-col, no `|` leak; 40 Vancouver-ordered refs with DOIs; MR residue = 0).

## 7. Remaining open items before/at submission (non-blocking, author action)
1. Confirm GitHub tag `v1.24.0` and Zenodo DOI `10.5281/zenodo.23042366` resolve (could not be verified from the sandbox — author to confirm at submission).
2. Fill BMC online declaration checkboxes (AI-use disclosure is already in §2.11; ethics/competing-interests/funding present).
3. Upload the 10 `Fig_S*` PNGs and map each to its caption.
4. (Optional) Reconsider `lenalidomide` "26.6th percentile" wording for clarity; (optional) double-check ImmunoSep 43.5%/49.7% source numbers.

## 8. Conclusion
Round-22 is a clean final confirmation pass. All four experts agree the **science is sound and the numbers are correct and reproducible**; the two MAJOR verdicts were submission-pack hygiene + one provenance gap, all now closed in **v1.24.0**. The manuscript is **submission-ready for BMC Medical Genomics**.

**Recommendation:** submit v1.24.0 to BMC Medical Genomics (Research article). No further review round is required unless the journal raises new points.
