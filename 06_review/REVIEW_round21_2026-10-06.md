# Round-21 Independent Review — Integration Report
**Manuscript version reviewed:** v1.22.0 (commit `d507c1c`) · **Reviewed as:** first submission (independence discipline enforced)
**Resulting version:** v1.23.1 (commit `e8ba121`, tag `v1.23.1`) — all findings below closed
**Date:** 2026-10-06
**Target venue:** BMC Medical Genomics (Research article)

---

## 1. Independence declaration
A `_PANEL_BRIEF.md` was distributed to all four reviewers forbidding access to any `06_review/` history, `REVIEW_*.md` / `RESPONSE_*.md` / `REVISION_*.md`, `SUBMISSION_MANIFEST.md`, `CITATION.cff`, author-verification statements, or other reviewers' outputs. Every headline number was independently recomputed by each reviewer from the deposited `03_results/` CSVs / raw matrices. No reviewer consulted a prior round.

## 2. Panel composition & verdicts
| Reviewer | Track | Verdict | Blocking defects |
|---|---|---|---|
| A1 | Domain / clinical truth (sepsis immunology) | Improved honesty; residual FIS1 circularity fixed | 0 (all minor) |
| A2 | Design / statistics / epidemiology | Core design sound; one contradiction fixed | 0 after fix (1 MODERATE pre-fix) |
| A3 | Implementation / provenance / recomputation | **No defects** | 0 |
| A4 | Venue fit / reporting honesty (BMC) | Venue-fit & honest; 2 metadata nits fixed | 0 |

**Overall editorial裁定: NO DESK-REJECT.** The manuscript is fit for technical-checks / desk review at BMC Medical Genomics. All blocking and minor issues identified were resolved in v1.23.0 (Round-21 main fixes) and v1.23.1 (Round-21 loose-ends).

## 3. Cross-validation (what all four independently confirmed)
- **Framing is now consistent and honest:** "within-cohort confirmation, not independent replication" appears in title, abstract, article-type note, §1, §3.3, Discussion. External validation is scoped "independent in cohort and platform, not in label."
- **Primary/sensitivity framework is internally consistent across 8 locations** (title, abstract, §2.9, §3.4, §3.5, Limitation 1, Conclusion, §7): locked-L1 AUC **0.585** = pre-specified **primary** (95% CI 0.469–0.696 includes 0.5 → "not significantly above chance"); equal-weight **0.638** = pre-specified **sensitivity** (95% CI 0.532–0.748).
- **All 20 recomputed headline numbers trace to source CSVs** (A3 ledger): 802 samples / 760+42; endotypes 132/176/118/53/323; death 114/365/323; 23/22/21 immune-gene counts; external AUCs/CI; CV 0.659; calibration slope 0.50/intercept −0.04; DCA grid; L1000 ranks (lenalidomide 5435/20413=26.6%, azithromycin 9152=44.8%, prednisone 651=3.2nd pct); IRG-3 proxy 0.5288; ΔAUC vs SRS +0.028 (P=0.69).
- **MR layer fully removed** from narrative (0 hits for Mendelian/MR-Egger/IVW/instrument/causal).
- **Document integrity clean:** Table 1 = 9 rows × 4 columns, zero pipe corruption; 40 references contiguous, all cited, Vancouver first-appearance order; abstract↔manuscript↔docx no drift; verify exits 0; audit 32/32 green at v1.23.1.

## 4. Issue tier status (Round-21 findings)
| # | Reviewer | Issue | Tier | Status in v1.23.1 |
|---|---|---|---|---|
| 1 | A1 | FIS1 "independent univariate association" w/ 28-day death is circular (it was the selection test) | MODERATE | **FIXED** — restated as "selection criterion restated, not independent confirmation"; dropped "genuine" |
| 2 | A1 | §7 provenance table still called FIS1 "passenger" (contradicts §3.3) | MINOR | **FIXED** — "passenger" removed |
| 3 | A1 | "erythroid-module gene"/"genuine prognostic signal" overstates biology (FIS1 is a mitochondrial-fission housekeeper) | MINOR | **FIXED** — Conclusion + §3.3 reworded to "co-segregates with erythroid/heme module, not an immune hub"; "genuine" dropped |
| 4 | A1 | FIS1 p = 0.00735 (text) vs 0.0071 (independent recompute) | TRIVIAL | **ACKNOWLEDGED, not changed** — text matches deposited `S06_hub_death_association.csv` (p=0.00735); difference is solver/SE convention, negligible. Text cites the CSV, so it is reproducible. |
| 5 | A2 | DeLong P ≈ 0.56 contradictory & misattributed (no per-sample IRG benchmark exists) | MODERATE (pre-fix only block) | **FIXED** — removed the misattributed claim; the only real DeLong now compares equal-weight (0.638) vs the 3-gene IRG proxy (0.529) on the same 106 samples (P = 0.16, correctly attributed, not significant). Comparison to published 0.619 is now explicitly described as not formally testable. |
| 6 | A2 | "pre-registered" overstated (no deposited plan) | MINOR | **FIXED** — "pre-specified" |
| 7 | A2 | §2.9 names primary without the "CI includes 0.5" caveat present elsewhere | MINOR | **FIXED** — caveat added to §2.9 |
| 8 | A2 | "title's 'prognostic / immune-risk'" points to a phrase absent from the title | VERY MINOR | **FIXED** — "the title's 'prognostic' and the abstract's 'immune-risk' wording" |
| 9 | A3 | Table 1 is 4 columns, not 5 (brief's expectation stale) | OBSERVATION | No action — table is correct & uncorrupted |
| 10 | A3 | "top 26.6%" slightly ambiguous direction | OBSERVATION | Editorial; left as-is (rank/percentile internally consistent) |
| 11 | A3 | CV AUC 0.6586 (S06) vs 0.6582 (09_ext) rounding artifact | OBSERVATION | Benign; 0.659 reported |
| 12 | A4 | Manifest title word count 18 (or 17) ≠ 24 actual | MINOR (metadata) | **FIXED** — manifest + build template now state 24 (standard whitespace count) |
| 13 | A4 | Manifest figure list implied contiguous S1–S10; actual is non-contiguous (S4/S5/S8 absent) | MINOR (metadata) | **FIXED** — build template + manifest now list the actual 10 files explicitly |
| 14 | A4 | Cover-letter vs manuscript title consistency | CLEAN | Verified verbatim-equal |
| 15 | A4 | MR-removal disclosure present | CLEAN | Present in cover letter + manifest |
| 16 | A4 | BMC declarations all present in docx | CLEAN | Ethics/consent/data/code/competing/funding/authors/§2.11 AI all present |
| 17 | A4 | Article-type fit (Research article) | CLEAN | Genuine external validation justifies Research article; kept |
| 18 | A4 | No format hard-fail; verifier exits 0 | CLEAN | Confirmed (40 refs, 10 figs, no MR residue, v1.23.1) |

## 5. Key decision records
- **DeLong (A2 #5):** The original "DeLong P ≈ 0.56 vs published 0.619" was both misattributed (no per-sample scores exist for Peng's 0.619) and internally contradictory (same paragraph said "no formal test performed"). Resolved by (a) deleting the misattributed number, (b) keeping the honest "no formal test against the published point estimate is possible," and (c) reporting the *real* DeLong that the author can actually compute — equal-weight (0.638) vs the in-repo 3-gene IRG proxy (0.529) on the same 106 samples, P = 0.16, not significant. This preserves the "real but modest, not superior" message without a fabricated statistic.
- **FIS1 (A1 #1–3):** The univariate OR 1.34 (p=0.00735) is the *same test* that selected FIS1 into the hub, so it cannot serve as independent corroboration. Reframed as an exploratory correlate co-selected with the erythroid/heme module, explicitly not a validated prognostic marker or mechanistic target. This aligns the prose with the §7 provenance table and the Conclusion.
- **"Pre-registered" → "pre-specified" (A2 #6):** No time-stamped registered analysis plan exists, so the stronger term was dropped; the anti-inflationary substance (lower-AUC model chosen as primary) is retained and is a genuine strength.

## 6. Open items (non-blocking, author action at submission)
1. Corresponding-author name in the submission system must be Latin-script (Yongxin Yang), not '永新 杨'.
2. Tick BMC online-declaration checkboxes (full text already in manuscript).
3. Zenodo DOI 10.5281/zenodo.23042366 already minted and in Data availability.
4. Upload the 10 `Fig_S*` PNGs (non-contiguous S1/S2/S3A/B/S6A/B/C/S7/S9/S10) and map each to its caption.
5. (Optional, A3 #10) Consider "26.6th percentile of 20,413 compounds" instead of "top 26.6%" for lenalidomide.
6. (Optional, A1 Q3) Confirm the exact 43.5%/49.7% 28-day mortality figures against the ImmunoSep primary Table.

## 7. Publishability assessment
- **Desk-reject risk:** None. No format hard-fail, no scope mismatch, no over-claim, no missing declaration, MR layer transparently disclosed and removed.
- **Scientific claim strength:** Honest and appropriately hedged. Primary external AUC 0.585 is explicitly "not significantly above chance"; equal-weight 0.638 is "real but modest, comparable to published benchmarks, not established as superior"; repositioning candidates are "hypothesis-generating, not prioritised by significance." This matches the self-described computational-biology / methods-and-resources contribution.
- **Evidence tier:** Computational pipeline + within-cohort confirmation + independent-cohort/independent-platform external validation (n=106, 52 deaths) + experimental blueprint (S11, not executed). Consistent with BMC Medical Genomics scope.
- **Verdict:** **Submission-ready.** Recommend submitting v1.23.1 to BMC Medical Genomics as a Research article.

## 8. Process lessons (carried into the audit gate)
- A "DeLong P ≈ 0.56" had survived prior rounds because no assertion checked it; it was only caught by an independent statistician reading the prose. **Gate lesson reinforced:** audit assertions must check that every reported significance test names its two input score vectors and that both are present in the deposited data. A number with no computable inputs is a red flag.
- The manifest/checklist are *generated* by `build_submission_bmc.py`, so edits to `SUBMISSION_MANIFEST.md` alone are silently overwritten on rebuild — fixes belong in the build template. (Resolved: template corrected at L501/L510/L530/L578.)
- Annotated tag + `git ls-remote` confirmation should follow every push; the sandbox transparent proxy is intermittently flaky for github.com:443 (multiple retries, eventually succeeds).
