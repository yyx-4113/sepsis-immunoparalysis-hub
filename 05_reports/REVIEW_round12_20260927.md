# Independent Review Panel — Round 12 Consolidated Report
**Manuscript:** `05_reports/manuscript.md` v1.12.0 — *A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and validates a 30-gene sepsis prognostic signature*
**Target venue:** Scientific Reports (Nature Portfolio), Article type
**Date:** 2026-09-27 | **Editor:** consolidated by the coordinating agent (independent of prior rounds)

---

## 1. Independence statement (mechanism + evidence it worked)

Four experts were convened with a shared `_PANEL_BRIEF.md` enforcing: (a) a forbidden-file list (all prior `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `review_rNN/` dirs, OVERVIEW, manifests, verification statements); (b) a per-item four-part output contract; (c) mandatory self-recomputation of headline numbers from `03_results/*.csv`; (d) a "§ Stands up" deliverable forcing each reviewer to report what they *suspected but found correct*.

Evidence independence worked: the four reviewers' recomputations of the external AUC (0.6382), IRG (0.604), calibration slope (0.5028), DCA zero-crossing (0.80), MR Egger/IVW SEs, and the "1/45" family structure **all independently reproduced to the quoted precision**, with discrepancies limited to bootstrap-seed noise (calibration CI upper bound 0.947 vs 0.96) and rounding (Mars3 median 0.640 vs 0.641). No reviewer relied on prior-round text. The single cross-cutting factual defect (DCA "uncalibrated" text vs code using calibrated probabilities) was found *independently* by the design reviewer (A2, Item 3) and then **re-verified by the editor** (see §3, row "DCA probability basis").

---

## 2. Verdict table

| Reviewer | Layer | Verdict | One-line rationale |
|---|---|---|---|
| A1 | Domain (sepsis immunology) | **Major** | Biology/clinical interpretation over-reaches on TIM-3/HAVCR2 framing and the glucocorticoid control undermines the repositioning axis |
| A2 | Design (biostats / causal) | **Minor** | All numbers reproduce; DCA "uncalibrated" text is wrong; MR "1/45" mis-framed; EPV/IRG/calibration framing to soften |
| A3 | Implementation (provenance) | **Minor** | Every number traces to source and gate is green; stale checklist version, missing DOIs, gate blind spots, title/abstract "validates" vs "modest" |
| A4 | Venue (Sci Rep editor) | **Minor** | Clears every desk-eval screen; only format/metadata fixes (DOIs, name the LLM, confirm repo live) |

**Distribution:** 1 Major + 3 Minor. **Overall: Major revision** (the Major is interpretive, not a type downgrade — see §8).

---

## 3. Cross-verification table (manuscript claim vs independently recomputed value)

| # | Location | Manuscript claim | Independently recomputed | Checked by | Verdict |
|---|---|---|---|---|---|
| 1 | §3.5 | external AUC 0.638 (CI 0.532–0.748), n=106, 52 deaths | 0.6382 / 0.5317–0.7475 / 106 / 52 | A2, A3, A4 | match |
| 2 | §3.4/§3.5 | locked-L1 external AUC 0.585 | 0.5848 | A2, A3 | match |
| 3 | §3.4 | IRG benchmark 0.604 | 0.604 | A2, A3 | match (but see #11) |
| 4 | §3.5 | calibration slope 0.50 / intercept −0.04 | 0.5028 / −0.0382 (z-score fit) | A2, A3 | match |
| 5 | §3.5 | DCA zero-crossing "by 0.80" | grid: NB=0.0 at 0.80 | A2, A3, editor | match |
| 6 | §3.5 | DCA "computed on the model's **(uncalibrated)** predicted probabilities" | code `_ext_calibration_dca.py:31-32,66-70` feeds **calibration-fit** `p` (= logistic fit on z-scores) | **A2 (Item 3) + editor re-read** | **CONTRADICTION — Tier-1 error** |
| 7 | §3.10 | CD74 Egger SE 0.111 < IVW SE 0.325 (3 SNPs, df=1) | 0.1111 / 0.3250 | A2, A3 | match (ordering arithmetically real) |
| 8 | §3.10 | "1 of 45" family-significant (CD74 crit-care WM, q≈3e-17) | exactly 1/45 | A2, A3 | match |
| 9 | §3.1 | 23 down / 22 sig / 21 both | 23 / 22 / 21 | A1, A3 | match |
| 10 | §3.3 | FIS1 logFC +1.26, t +17.2 | 1.2614 / 17.16 | A1, A3 | match |
| 11 | §3.4 | IRG gap 0.034 = "comparable not superior" | DeLong P=0.559; gap real BUT IRG-3 is **partially unoriented** (LTB4R, IL4R left unoriented) → gap not clean | A2 (Item 9) | match value, **flag framing** |
| 12 | §2.10 | MR sample overlap uncorrected | confirmed (no mrSampleOverlap run) | A2, A3 | match |
| 13 | §3.9 | prednisone "scored high" (rank 651, 3.2 pct); dexamethasone did not (rank 6808, 33.4 pct) | exact | A3 | match (no error) |
| 14 | §3.4 | EPV ≈ 3.8 (114 events / 30 genes) | 3.8 | A2 | match |

**Editor-verified worst finding (§1 of the skill):** Row 6 — the §3.5 sentence "computed on the model's (uncalibrated) predicted probabilities" is **false relative to the deposited code**. The DCA thresholds on `p = 1/(1+exp(−(a+b·z)))` where `(a,b)` are the *fitted calibration parameters* (intercept −0.04, slope 0.50), i.e. calibration-corrected probabilities. This is a Tier-1 factual/textual contradiction introduced when v1.12.0 adopted the Round-11 "uncalibrated" framing. (Note: the Round-11 reviewer's premise that the DCA used *uncalibrated* probs was itself based on the old manuscript text, not the code — the code has always used calibrated `p`.) Re-running the DCA on *raw* `plogis(z)` produces a different, messy curve; the deposited smooth curve depends on the calibrated `p`. **Fix: state the DCA used calibration-corrected probabilities.**

---

## 4. Graded consolidated issue list (de-duplicated across experts)

### Tier 0 — conclusion-invalidating
*None.* No expert found a conclusion-invalidating defect; all headline numbers reproduce.

### Tier 1 — must fix (correctness / honesty)
- **T1-1 (A2-3, editor).** §3.5 DCA "uncalibrated" text contradicts code (calibrated-fit probs). → reframe to "calibration-corrected probabilities."
- **T1-2 (A2-4,13).** §3.5 DCA "positive net benefit 0.10–0.75" is *absolute* (treat-all also positive there due to 0.49 prevalence). Model beats treat-all only above ≈0.50. → comparative framing + prevalence caveat.
- **T1-3 (A1-1,6,7; A3-P4).** TIM-3/HAVCR2 still labelled "the APC-expressed checkpoint" in Title/Abstract/§3.3/§4/Conclusion, and §4 re-asserts "reflecting reduced APC abundance rather than T-cell-intrinsic exhaustion" — a mechanistic reading bulk blood cannot support and which the manuscript's own PDCD1-up/HAVCR2-down discordance contradicts. → soften label + drop the §4 mechanistic over-claim.
- **T1-4 (A1-2).** Glucocorticoid positive-control (prednisone top-3% / dexamethasone 33rd pct) is presented as a soft caveat, but it actually shows the Mars1-down antigen-presentation axis is up-regulated by a clinical immunosuppressant → the L1000 "rescue" proxy is not a valid marker of immune restoration. → sharpen the caveat explicitly (validity limit on the repositioning axis).
- **T1-5 (A2-6,7,8).** MR "1 of 45" is overlap-inflated, reversed-direction, 3-SNP, and is headlined ahead of the fully-null *primary* (28-day death, 15-test) outcome. → lead with primary-outcome null; reframe the CD74 crit-care result as overlap-inflated genotype–severity association; state the three estimators "agree" only because they share the same 3 overlap-biased SNPs.
- **T1-6 (A2-1,14).** EPV 3.8 optimistic CV AUC 0.659 is featured ahead of the honest external 0.638; "fully independent" overstates (orientation is label-trained). → lead Abstract/§3.4 with 0.638, demote CV as optimistic/label-informed; "independent cross-platform application of a locked, label-oriented signature."

### Tier 2 — should fix (clarity / robustness)
- **T2-1 (A2-2).** Calibration slope CI width [0.11,0.95] should be stated (magnitude poorly constrained by n=106).
- **T2-2 (A2-9).** IRG-3 benchmark is partially unoriented (LTB4R, IL4R) → 0.034 gap not a clean estimate. → re-orient the IRG-3 genes consistently and re-run, **or** state the benchmark is a lower-bound reference (DeLong P≈0.56 is robust either way).
- **T2-3 (A2-5).** CD74 Egger SE < IVW SE on df=1 is unstable leverage-weighting, not a precision estimate → strengthen the wording.
- **T2-4 (A2-12).** External CI "excludes 0.5 by a comfortable margin" slightly oversells; state modest/uncertain.
- **T2-5 (A1-3).** Mars1 is bimodal (immune-down + heme/erythroid-up; authors' own GATA1/CGB/EPB49 module); narrative foregrounds only antigen-presentation. → acknowledge dual architecture. Also cite the 39% mortality source precisely.
- **T2-6 (A1-4).** Named hubs do not individually carry the transported score (L1 zeroes CD74/HLA-DRB1/HLA-DMA/HLA-DMB/CD86/CD8B/IRF1; HLA-DQA1 absent). → explicit sentence.
- **T2-7 (A1-5).** Missing domain citations (PD-1/TIM-3 co-expression in sepsis exhaustion; mHLA-DR recovery tracking survival; independent endotype validations; checkpoint-blockade trial context). → add a curated "must-cite" set.
- **T2-8 (A4-C).** §2.12 names WorkBuddy but not the underlying LLM(s); name them or state not individually logged.
- **T2-9 (A3-P4).** Title/Abstract "validates" vs body "modest" mismatch → soften headline verb.

### Tier 3 — format / metadata
- **T3-1 (A3-P1, A4-B).** `scirep_submission_checklist.md` still tagged v1.11.0 / "21 assertions" / abstract 173 → v1.12.0 / 26 / 180.
- **T3-2 (A3-P2, A4-F).** 36/37 references lack DOIs (only [32] has one) → backfill via `fetch_dois_crossref.py`.
- **T3-3 (A3-P3).** Audit gate does not re-derive Table 4 prose, L1000 ranks, or per-gene instrument counts → append assertions.
- **T3-4 (A4-E).** Confirm `v1.12.0` GitHub tag is public & repo contains cited dirs; ideally mint Zenodo DOI pre-acceptance (acceptable to keep "on acceptance").

---

## 5. Consensus / Complementarity / Disagreement

**Consensus (all 4):** The pipeline, external validation, limitation discipline, and audit infrastructure are genuinely strong; every headline number traces to source; the Article-type framing honestly headlines the stable confirm+validate finding and buries the null MR / "comparable-not-superior" signature; no desk-eval hard-fail.

**Complementarity:** A1 caught *biological* over-reach the others could not (TIM-3, glucocorticoid). A2 caught the *design/factual* DCA contradiction and the MR framing. A3 caught *provenance/process* gaps (stale checklist, gate blind spots). A4 caught *venue* hygiene (DOIs, AI naming). No single reviewer covered all four layers — confirms the panel was correctly composed.

**Disagreement:** Verdict severity. A1 returned Major on interpretive grounds; A2/A3/A4 returned Minor. **Adjudication (stricter verdict adopted):** A1's scope is the *biological interpretation layer*, which is a legitimate manuscript layer; its findings (T1-3, T1-4) are real over-statements, not mere wording. The lenient Minor verdicts certify the *arithmetic/provenance/venue* layers, not the whole manuscript. Per the skill's rule ("a self-limited scope does not set the manuscript's fate"), the overall handling is **Major** for this round, but the fixes are textual/reframing — **no new data or type downgrade required** (A4 explicitly confirms the Article type is correctly framed).

---

## 6. Priority must-fix list (no DESK-REJECT flagged)

- **DESK-REJECT:** none.
- **Must add analysis:** T2-2 (IRG re-orientation) is the only item needing a re-run; reversible to a caveat if the re-run is deferred.
- **Must reword (no analysis):** T1-1…T1-6, T2-1…T2-9, T3-1…T3-4. All addressable in v1.13.0 without new data.

---

## 7. What stands up (do NOT change)

Per the experts: (1) external validation AUC 0.638 / CI / n / deaths reproduces exactly and is honestly "modest"; (2) the 23/22/21 immune-direction tallies and Table 1 effects are exact; (3) the MR layer is correctly downgraded (no primary IVW significance; overlap flagged; the one family-significant result reinterpreted as genotype–severity); (4) calibration is candidly reported (slope 0.50, "ranker not probability"); (5) DeLong "comparable not superior" is correct; (6) FIS1 logFC +1.26 / t +17.2 confirmed; (7) L1000 ranks (lenalidomide 5435, azithromycin 9152; prednisone 651, dexamethasone 6808) exact; (8) the audit gate is green and genuinely useful. The revision must **preserve** these and only reframe the over-statements.

---

## 8. Recommended handling path

**Path A — restructure-and-resubmit as the same Article type (recommended).** No downgrade (A4: Article framing is honest and correctly ordered). The Major is interpretive; all fixes are textual reframing plus one optional re-run (IRG orientation). The robust real contribution (reproducible Mars1 confirm + honest external validation + experimental blueprint) stays headlined; the fragile layers (L1000 repositioning, MR) are demoted to hypothesis-generating more explicitly.

---

## 9. Process lessons (what gates could not catch)

- The audit gate passed 26/26 yet the manuscript still carried a Tier-1 *text-vs-code* contradiction (DCA "uncalibrated"). **Gates verify arithmetic/strings, not design or code–text consistency.** Lesson: a new assertion should check that the DCA sentence names the *calibrated* probabilities and matches `_ext_calibration_dca.py`.
- A2's independent recomputation surfaced that the "1/45" MR headline inverts the proper emphasis (secondary reversed result ahead of the null primary). **Gates cannot judge statistical emphasis/framing** — only human design review catches it.
- The panel re-caught the exact "softened-limitation / unchanged-headline" pattern (Title "validates" vs body "modest") that prior-round fixes are prone to leave behind. **Rule reinforced:** for every past caveat, check whether the headline statement itself was retracted, not merely qualified elsewhere.

---

*Panel files:* `05_reports/review_r12/{_PANEL_BRIEF,A1_domain,A2_design,A3_implementation,A4_venue}.md`
