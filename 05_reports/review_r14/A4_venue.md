# A4 — Venue review: Scientific Reports (Nature Portfolio)

**Reviewer role:** Venue expert — Scientific Reports (Nature Portfolio) editor perspective + reporting-standard auditor.
**Manuscript:** "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and externally evaluates a 30-gene sepsis prognostic signature"
**Files read by me:** `05_reports/manuscript.md`, `05_reports/cover_letter.md`, and source CSVs `03_results/09_ext_dca_grid.csv`, `03_results/09_ext_calibration_dca.csv`, `03_results/S08_l1000_candidate_scores.csv`.
**Independence statement:** I treated this as a *first submission*. I did not open, grep, or summarise any prior-round review (`REVIEW_round12_*.md`, `REVIEW_round13_*.md`, `review_r12/`, `review_r13/`), any `REVIEW_*/RESPONSE_*/REVISION_*.md`, `.workbuddy/memory/`, `scirep_submission_checklist.md`, or any other reviewer's output under `05_reports/review_r14/`. Every judgement below is from the manuscript/cover letter text or the source files I recomputed myself.

---

## 0. Venue fit — summary verdict

The manuscript is *scientifically within scope* for Scientific Reports: it is a single-author, fully computational re-analysis that contributes a reproducible pipeline, an honest external validation, and an experimental blueprint — exactly the "methodological rigour and validity over perceived novelty" framing Sci Rep evaluates on. The contribution is honestly framed as confirmation/replication, not novel hub-gene discovery (`manuscript.md:8`, `:184`). No venue-format item rises to an outright **desk-reject** hard fail. However, there are **three mandatory venue-format corrections** (abstract length + narrative citation, reference re-numbering, data-availability version contradiction) that must be fixed before the manuscript can clear technical/copy-edit checks. None of these is a scientific peer-review blocker, but all are required for acceptance.

---

## 1. Abstract compliance (≤200 words, no citations)

**Item A1 — Abstract is at/just over the 200-word ceiling and embeds a narrative author citation.**
【Problem】 The single-paragraph abstract sits at or marginally above the 200-word limit and contains a named-author reference to prior work ("Peng et al. reported 0.619"), which is a citation-by-mention in the abstract.
【Evidence】 `manuscript.md:14` (Abstract). Manual word count of the paragraph = **198 words**; an independent tokenizer count (splitting on alphanumeric/hyphen/`+`/`.`/`≥`/`≤` tokens) = **201 words**. Both place it at the ceiling; the tokenizer count exceeds 200. The phrase "the published immune-related-gene benchmark (Peng et al. reported 0.619 on this cohort; …)" appears inside the abstract.
【Why it matters】 Scientific Reports mandates a *non-structured abstract of no more than 200 words with no references/citations*. An at-limit count leaves zero margin for the journal's own word-counter (which may treat hyphenated compounds or numbers differently), and a named-author mention of another paper can be read as a citation in the abstract — a routine format desk-query that delays processing.
【Specific fix】 Trim ~20–25 words and remove the author name, e.g. replace:
> "…the external result is comparable to the published immune-related-gene benchmark (Peng et al. reported 0.619 on this cohort; a 3-gene IRG proxy recomputed here was 0.529, near-random)."
with:
> "…the external result is comparable to the published immune-related-gene benchmark (reported AUC 0.619 on this cohort; a 3-gene IRG proxy recomputed here was 0.529, near-random)."
Target an abstract of **≤185 words** so it clears the limit with margin.

---

## 2. Article type and scope fit

**Item A2 — Article type is correctly declared and honestly framed; no misrepresentation.**
【Problem】 None. The manuscript declares "Article (original research)" and describes the computational-biology / methods-and-resources *contribution* in prose rather than asserting a named article type — appropriate, because Scientific Reports does not have a separate "methods-and-resources" category.
【Evidence】 `manuscript.md:8` ("Article type. Article (original research). This is a computational-biology / methods-and-resources report: its contribution is a reproducible, fully auditable analytical pipeline… not novel hub-gene discovery"). The Discussion restates this boundary explicitly at `manuscript.md:184` ("The contribution of this study is therefore methodological and infrastructural rather than biological… a near-replication rather than a novel gene discovery").
【Why it matters】 Sci Rep accepts re-analyses, replications, and methodological/computational contributions as "original research" provided the added value is clear. The authors do articulate added value (auditable pipeline + independent external validation + experimental blueprint), so the article type is a defensible fit and is *not* misrepresented as a discovery paper.
【Specific fix】 No change required. Optional: in the cover letter, the phrase "methods-and-resources" (cover_letter.md:11) could be softened to "methodological/computational resource" to avoid implying a Sci Rep article category that does not exist; this is cosmetic only.

---

## 3. Generative-AI statement (Nature requirement)

**Item A3 — Generative-AI use is disclosed in Methods and is adequate.**
【Problem】 None. Nature requires a generative-AI disclosure in the Methods; it is present and unusually thorough.
【Evidence】 `manuscript.md:65–66` (§2.12 "Use of generative AI"). It specifies: (i) drafting/revising text across all sections; (ii) assembling/formatting tables from direct reads of outputs; (iii) writing plotting/analysis code that renders figures from analysis outputs (no image model, no data alteration); (iv) reference retrieval/verification by identifier; (v) internal adversarial review. It explicitly states no reported data were created/generated/imputed by AI, no AI tool is an author, and the author takes full responsibility.
【Why it matters】 This satisfies the Nature Portfolio generative-AI policy (disclosure of use in preparation; no AI as author; confirmation that content is human-reviewed). It is a *model* disclosure and should be retained.
【Specific fix】 No change required. One optional tightening: add the sentence "No generative-AI tool was used to analyse data or to make any scientific judgement" to pre-empt any reviewer concern that "writing the plotting and analysis code" might extend to analytic decisions — the current text already says values are direct reads, so this is belt-and-suspenders only.

---

## 4. Data availability

**Item A4 — Data-availability paragraph contradicts itself on the version tag (v1.14.0 vs v1.13.0).**
【Problem】 The Data availability statement announces a v1.14.0 release but in the same sentence says the evaluated commit is tagged v1.13.0 — two different versions in one clause, undermining the very reproducibility claim the paper is built on.
【Evidence】 `manuscript.md:263`: "A citable versioned snapshot is provided as a GitHub release (**tag v1.14.0**); a Zenodo DOI will be minted and made public on acceptance (**the current evaluated commit is tagged v1.13.0**)." The cover letter says only "tag v1.14.0" (cover_letter.md:24). The panel brief identifies the evaluated tag as **v1.14.0 (commit 800063e)**.
【Why it matters】 The entire sales proposition of this manuscript is auditability and a pinned, citable version. A reader/reviewer cannot tell which commit actually produced the reported numbers. This is a correctness/clarity defect in the one place reproducibility is asserted, and it directly contradicts the cover letter and the submission metadata.
【Specific fix】 Replace "the current evaluated commit is tagged v1.13.0" with "the current evaluated commit is tagged v1.14.0 (commit 800063e)" (or delete the clause entirely). Ensure the cover letter and manuscript both state v1.14.0 only.

**Item A5 — Data availability is otherwise specific and does not use "available on request."**
【Problem】 None (after A4 is fixed). The statement points to a real, versioned public repository URL with a specific tag.
【Evidence】 `manuscript.md:263`: "All result tables (03_results/) and analysis code are released under MIT in the versioned repository at https://github.com/yyx-4113/sepsis-immunoparalysis-hub." No "available on request" wording appears. E-MTAB-4451 and GSE65682 are cited as public ArrayExpress/GEO deposits.
【Why it matters】 Sci Rep's data policy requires a specific, accessible location; a future Zenodo DOI "on acceptance" is an acceptable plan provided the primary repo is live now (it is). The only defect is the version-tag mismatch in A4.
【Specific fix】 No change beyond A4. Optional: move "Zenodo DOI … on acceptance" to a sentence that does not read as the sole data location, to make clear the GitHub v1.14.0 repo is the immediately accessible source.

---

## 5. Mandatory Nature end-matter sections

**Item A6 — Ethics / Author contributions / Funding / Competing interests / Acknowledgements are all present and correctly formatted.**
【Problem】 None. All five required sections exist with appropriate content.
【Evidence】
- Ethics statement: `manuscript.md:265–266` (computational re-analysis of public de-identified cohorts; no IRB needed for bioinformatics; S11 prospective design requires separate IRB).
- Author contributions: `manuscript.md:268–269` (single author: conceived, performed bioinformatics, wrote, approved).
- Funding: `manuscript.md:271–272` ("no specific grant from any funding agency"; author bears costs).
- Competing interests: `manuscript.md:274–275` ("The author declares no competing interests").
- Acknowledgements: `manuscript.md:278–279` (thanks MARS consortium, Davenport et al., and tool/resource developers).
【Why it matters】 Nature Portfolio requires each of these as distinct, explicit statements. Their presence and correct formatting mean no desk-format rejection on end-matter grounds.
【Specific fix】 No change required. Minor: the competing-interests line is the standard acceptable phrasing; keep it.

---

## 6. References — numbering order (the key flag)

**Item A7 — Reference list is NOT numbered in order of first appearance (Vancouver/citation-order violation).**
【Problem】 The reference list is numbered sequentially 1–37, but the *first* citation in the body text is `[3]`, not `[1]`; reference `[1]` does not appear until much later. The list is therefore out of citation order.
【Evidence】
- First bracketed citation in the entire manuscript is `manuscript.md:22` ("Sepsis **[3]**"); the same sentence then cites `[2]`, `[17]`, `[22]`, `[4]`, `[33]`. So first-appearance order begins 3, 2, 17, 22, 4, 33…
- Reference `[1]` (Aran/xCell) first appears at `manuscript.md:49` ("xCell **[1]**"), far downstream of `[3]`.
- The list itself is ordered 1. Aran, 2. Boomer, 3. Singer, 4. Scicluna, 5. Davenport … (`manuscript.md:282–318`).
- The numbering is *internally consistent* (each `[n]` maps to list entry n), but the order does not track first appearance, which is what Nature/Sci Rep require ("References should be numbered in the order in which they appear in the text").
【Why it matters】 This is a clear deviation from the journal's reference style. It is **not a scientific peer-review blocker** — it does not affect the validity of any result — and Nature's production/copy-editing stage will renumber the list regardless. However, if the author revises before acceptance, a mis-ordered list is a fertile source of in-text/list mismatches, and the journal explicitly requires authors to supply citation-ordered references. Fixing it now avoids copy-edit churn and re-review loops.
【Specific fix】 Re-sort the reference list by first-appearance order and renumber all in-text citations accordingly, or regenerate the bibliography with a reference manager set to "number by citation order." This is a **production-stage / copy-edit fix, not a peer-review blocker**, but it must be done before acceptance. (The individual entries themselves are correctly formatted for Nature — numbered, article title present, journal italicised, volume bold, doi included — so only the ordering needs correction.)

---

## 7. Cover letter vs manuscript consistency

**Item A8 — Cover letter and manuscript agree on title and HAVCR2 framing; the only mismatch is the version tag, already covered in A4.**
【Problem】 Title and HAVCR2/TIM-3 framing match; the data-availability tag mismatch lives only because the manuscript's own sentence (A4) introduces v1.13.0, which the cover letter does not repeat.
【Evidence】
- Title: identical — `manuscript.md:1` and `cover_letter.md:3`: "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and externally evaluates a 30-gene sepsis prognostic signature."
- HAVCR2 framing: cover_letter.md:14 ("co-inhibitory checkpoint HAVCR2/TIM-3 (expressed on T cells and antigen-presenting cells)") matches the manuscript's repeated phrasing (`manuscript.md:14`, `:106`, `:182`, `:218`).
- Data-availability tag: cover_letter.md:24 says only "tag v1.14.0"; the manuscript `manuscript.md:263` adds the contradictory "v1.13.0" (see A4).
【Why it matters】 Title and HAVCR2 consistency is good. The tag inconsistency is the same reproducibility defect as A4 and should be resolved there.
【Specific fix】 Resolve via A4 (make both documents state v1.14.0 unambiguously).

---

## 8. Reporting honesty audit

**Item A9 — MR null is honestly reported; no over-claim of causality.**
【Problem】 None. The primary MR outcome is reported as null and the layer is consistently framed as hypothesis-generating.
【Evidence】 Abstract states "two-sample Mendelian randomisation gave no causal support on the primary 28-day-death outcome (all IVW OR 0.92–1.12, P ≥ 0.23)" (`manuscript.md:14`). Table 3 (`manuscript.md:155–159`) shows all primary-outcome IVW P ≥ 0.24 (CD74 0.72, HLA-DQA1 0.26, CD14 0.24, HAVCR2 0.85, FIS1 0.47) — consistent with the abstract's "OR 0.92–1.12, P ≥ 0.23" (0.923→0.92, 1.119→1.12; min P 0.24 ≥ 0.23). The Discussion (`manuscript.md:186`) and Limitations (`:194–195`) repeatedly call the MR "hypothesis-generating," note no primary IVW is significant, and flag the CD74 critical-care result as a *reversed-direction* genotype–severity association rather than a causal hub claim.
【Why it matters】 This is exemplary honesty for a weak/negative genetic layer and matches the panel brief's stated claims exactly. No contradiction found.
【Specific fix】 No change required.

**Item A10 — Modest AUC is honestly scoped; calibration under-fitting is disclosed without a false CI.**
【Problem】 None. The external AUC is presented as real-but-modest, and the calibration limitation is stated without claiming a confidence interval that was not computed.
【Evidence】 `manuscript.md:112` ("a modest separation … the 95% CI 0.532–0.748 excludes 0.5, though the point estimate is only 0.138 above chance and the lower bound is close to 0.5, so the magnitude is real but uncertain"). Calibration: "near-zero intercept (−0.04) but an under-fitting slope of 0.50 (ideal = 1.0), indicating over-confident predicted probabilities; the score is therefore presented as a risk *ranker* rather than a calibrated probability." Source `03_results/09_ext_calibration_dca.csv:2` confirms intercept −0.0382 ≈ −0.04 and slope 0.5028 ≈ 0.50, with **no CI columns** — consistent with the brief's "NO 95% CI claimed." Limitation 1 (`manuscript.md:194`) reiterates the modest magnitude and that the L1 weights did not transport (AUC 0.585).
【Why it matters】 The authors resist the common temptation to over-sell a 0.638 AUC or to present uncalibrated probabilities as risks. This is reporting honesty done right.
【Specific fix】 No change required.

**Item A11 — DCA grid and prose are consistent (model NB 0.00 vs treat-all −1.55 at threshold 0.80; they diverge, not converge).**
【Problem】 None. The brief flagged a possible DCA-grid-vs-prose contradiction; I verified the grid supports the prose — they are consistent.
【Evidence】 `03_results/09_ext_dca_grid.csv`: at threshold 0.30, `nb_model=0.2844` > `nb_treat_all=0.2722` (model first exceeds treat-all, matching "from threshold ≈0.30 onward" in `manuscript.md:112`); at threshold 0.80, `nb_model=0.0` while `nb_treat_all=−1.5472` — i.e., the model flattens at 0 and treat-all diverges downward to −1.55, exactly the "they DIVERGE, not converge" description in the panel brief. The prose (`manuscript.md:112`) describes the DCA as computed on calibration-corrected probabilities (intercept −0.04, slope 0.50), which matches the calibration file. No contradiction found between grid and text.
【Why it matters】 Decision-curve claims are frequently where manuscripts quietly invert; here the numbers and narrative agree.
【Specific fix】 No change required. Optional: the exceedance at 0.30 is razor-thin (0.2844 vs 0.2722); consider stating "the model's net benefit separates from treat-all only marginally at ~0.30 and grows thereafter" to pre-empt a reader who notices the tiny gap at 0.30.

**Item A12 — "Not independent in label" disclosure is implicit but not explicit; recommend one clarifying sentence.**
【Problem】 The manuscript states the external cohort is independent in *cohort and platform* and notes the Peng benchmark was computed on the *same* E-MTAB-4451 cohort, but it does not explicitly state that the outcome-label construct (28-day mortality) is shared with discovery — i.e., the validation is "not independent in label."
【Evidence】 `manuscript.md:54` ("an independently recorded 28-day outcome") and `:112` ("different platform … different population … independently recorded 28-day outcome") assert cohort/platform independence. `manuscript.md:112` and `:194` acknowledge the Peng 0.619 was "reported … on this cohort" and that the within-cohort CV is "label-informed," but I found **no sentence** stating that the external validation shares the 28-day-mortality *label* construct with the discovery signature and is therefore not fully label-independent (a targeted grep for "not independent / not in label / shared label / overlap" returned no matches).
【Why it matters】 The panel brief lists "external validation independent in cohort and platform but *not in label*" as a stated claim. Readers should be told plainly that the validation is cross-cohort/cross-platform but uses the same outcome phenotype, so the gain over the discovery CV is cohort/platform transfer, not label independence. This is a minor honesty gap, not an over-claim, but making it explicit strengthens the "honest external validation" branding.
【Specific fix】 Add to Limitation 1 (`manuscript.md:194`) a sentence such as: "The external cohort is independent in sample and platform, but the outcome label (28-day all-cause mortality) is the same phenotype used to orient the discovery signature, so the validation demonstrates cross-cohort/platform transport rather than independence from the discovery label."

---

## 9. Format hard-fails / desk-evaluation risks

**Item A13 — No outright desk-reject format failure, but two items will trigger format queries if uncorrected.**
【Problem】 No single defect is a hard desk-reject, yet the abstract (A1) and reference ordering (A7) are exactly the kind of format non-compliance Sci Rep's technical check flags pre-peer-review.
【Evidence】 Sci Rep's stated format requirements: unstructured abstract ≤200 words, no citations (violated at the margin by A1); references numbered in citation order (violated by A7); generative-AI statement in Methods (satisfied, A3); data availability with specific location (satisfied aside from A4); mandatory end-matter sections (satisfied, A6). The data-availability version contradiction (A4) is a clarity/reproducibility defect, not a desk reject.
【Why it matters】 Manuscripts that fail technical format checks are often returned unreviewed ("desk evaluation") for correction before peer review. Fixing A1 and A7 proactively prevents a avoidable bounce.
【Specific fix】 Prior to resubmission: (i) trim abstract to ≤185 words and remove the "Peng et al." mention (A1); (ii) re-number references in citation order (A7); (iii) reconcile the v1.14.0/v1.13.0 tag (A4). These three are the only format blockers to a clean technical check.

---

## § Stands up (what is compliant / strong)

1. **Generative-AI disclosure is present and exemplary** — `manuscript.md:65–66` (§2.12) exceeds the Nature minimum: it scopes AI use to text/table/code drafting and reference verification, explicitly denies any data creation/alteration, denies AI authorship, and affirms human responsibility. This is a model statement.
2. **Honest null/modest reporting throughout** — MR primary outcome null with no causal over-claim (`manuscript.md:14`, `:155–159`, `:186`); external AUC 0.638 framed as "real but modest" with CI excluding 0.5 but lower bound near 0.5 (`manuscript.md:112`); calibration under-fitting (slope 0.50) disclosed and the score demoted to a "ranker" (`manuscript.md:112`; source `09_ext_calibration_dca.csv:2`). No over-claim detected.
3. **DCA grid and prose agree** — verified `03_results/09_ext_dca_grid.csv`: model NB 0.00 vs treat-all −1.55 at 0.80 (diverge, not converge); model exceeds treat-all from ~0.30. Consistent with `manuscript.md:112`. No hidden inversion.
4. **All mandatory Nature end-matter sections present and correctly formatted** — Ethics (`manuscript.md:265–266`), Author contributions (`:268–269`), Funding (`:271–272`), Competing interests (`:274–275`), Acknowledgements (`:278–279`), Data availability (`:263`).
5. **Article-type and novelty boundary honestly stated** — declared "Article (original research)" with a prose description of the computational/methods contribution, and the Discussion (`:184`) explicitly positions the five hubs as a *near-replication* of the established Mars1 program, not novel discovery. No misrepresentation.
6. **L1000 rescue ranks verified against source** — `03_results/S08_l1000_candidate_scores.csv:2–3` confirms lenalidomide rank 5435 (rescue 0.0439) and azithromycin rank 9152 (rescue 0.0133), matching the manuscript's "5435" and "9152" claims (`manuscript.md:140`). The glucocorticoid positive-control caveat (prednisone high, dexamethasone not) is retained (`manuscript.md:142`), correctly capping the rescue interpretation.
7. **HAVCR2/TIM-3 and nivolumab framings match the required honest language** — HAVCR2 down-regulation described as "reduced checkpoint engagement in the immunosuppressed program" not "T-cell exhaustion" (`manuscript.md:182`); nivolumab described as a "Phase 1b safety/pharmacokinetic study that was not powered to show efficacy [34]" (`manuscript.md:188`), not "showed no benefit." Both match the panel brief's stated framings.

---

## § Questions for the authors

1. **Version pin:** Which exact commit/tag was analysed — v1.14.0 or v1.13.0? The Data availability sentence (`manuscript.md:263`) says both. Please confirm and make the manuscript and cover letter state a single tag (v1.14.0, commit 800063e).
2. **Reference ordering:** The reference list is currently numbered sequentially rather than in citation order (first body citation is `[3]`, `manuscript.md:22`). Can you regenerate the bibliography in citation order via a reference manager, or shall the production team renumber? Either way it must be citation-ordered before acceptance.
3. **Abstract:** Our word count places the abstract at/just over the 200-word limit (manual 198, tokenizer 201) and it names "Peng et al." Will you trim to ≤185 words and remove the author mention so it clears Sci Rep's abstract rules?
4. **Label independence:** Do you agree the external validation is "independent in cohort and platform but not in label" (same 28-day-mortality phenotype as discovery)? If so, would you add the explicit sentence suggested in A12 so the honesty is unambiguous to readers?
5. **CD74 critical-care / MHC-II LD:** You note CD74 and HLA-DQA1 lie in the same MHC-II region (Limitation 2, `manuscript.md:195`). Does this shared LD also mean the 45-test BH correction (treating all 45 tests as independent) is *conservative* for those two genes specifically, since overlapping instruments could inflate the family-wise error in the opposite direction? A one-line clarification would help readers parse the correction's direction.

---

## § What I actually checked

**Files read:**
- `05_reports/manuscript.md` (full) — abstract, article type, GenAI §2.12, all results/discussion/limitations, end-matter, references.
- `05_reports/cover_letter.md` (full) — title, article type, HAVCR2 framing, data-availability tag.
- `03_results/09_ext_dca_grid.csv` — verified DCA net-benefit grid (thresholds 0.05–0.90; model vs treat-all; confirmed 0.30 separation and 0.80 values 0.00 vs −1.55).
- `03_results/09_ext_calibration_dca.csv` — confirmed calib_intercept −0.0382, calib_slope 0.5028, AUC 0.6382; confirmed no CI columns (consistent with "no 95% CI claimed").
- `03_results/S08_l1000_candidate_scores.csv` — confirmed lenalidomide rank 5435, azithromycin rank 9152.

**Computations / re-counts performed:**
- Abstract word count: manual = 198 words; regex tokenizer = 201 words. Both at/over the 200 limit. Confirmed "Peng et al." present in abstract.
- Reference first-appearance order: traced from `manuscript.md:22` (first citation `[3]`) and `manuscript.md:49` (first `[1]`); confirmed list `manuscript.md:282–318` is numbered 1–37 but not in citation order.
- MR primary-outcome IVW OR range from Table 3 (`manuscript.md:155–159`): 0.923–1.119 → matches abstract "0.92–1.12"; min P 0.24 → matches abstract "P ≥ 0.23."
- Calibration slope/intercept from source CSV vs manuscript text (`manuscript.md:112`): −0.0382 vs "−0.04", 0.5028 vs "0.50" — match.
- DCA grid vs prose consistency: confirmed (see Stands-up #3).

**Discrepancies / concerns found:**
- A1: abstract at/over 200 words + narrative "Peng et al." citation.
- A4/A8: data-availability version contradiction (v1.14.0 release vs v1.13.0 evaluated commit); cover letter only says v1.14.0.
- A7: references not in citation order.
- A12: "not independent in label" not stated explicitly (minor honesty gap).
- No contradiction found between DCA grid and prose; no over-claim found in MR/AUC/calibration/HAVCR2/nivolumab framings.

**Forbidden files not opened:** I did not read `REVIEW_round12_20260927.md`, `REVIEW_round13_20260927.md`, `review_r12/`, `review_r13/`, any `REVIEW_*/RESPONSE_*/REVISION_*.md`, `.workbuddy/memory/`, `scirep_submission_checklist.md`, or any other `review_r14/` reviewer file. The manuscript was assessed as a first submission.

---

## § Recommendation (venue level)

**Minor revision — venue-format compliance required; scientifically publishable pending fixes.** The manuscript meets Scientific Reports' scope and reporting standards on substance: the generative-AI statement, end-matter sections, honest null/modest reporting, and DCA/calibration transparency are all in order and, in places, exemplary. Three mandatory format corrections must be made before the manuscript clears technical checks: (1) trim the abstract to ≤185 words and remove the "Peng et al." mention (A1); (2) re-number references in citation order (A7); (3) reconcile the data-availability version tag to a single v1.14.0 (A4). One recommended honesty clarification — an explicit "not independent in label" sentence (A12) — would further strengthen the manuscript's central "honest external validation" claim. None of these is a scientific blocker; all are achievable in a single revision pass.
