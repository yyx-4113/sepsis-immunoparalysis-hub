# Reviewer B4 — Venue / Journal-Fit assessment (Scientific Reports, Nature Portfolio)

**Manuscript:** `05_reports/manuscript.md` (tag `v1.18.0`, commit `57fe917`)
**Declared type:** Article (original research) — computational biology / methods-and-resources; framed as *reproducible pipeline + honest external validation + experimental blueprint*, **not** novel hub-gene discovery.
**Independence:** Treated as first submission. I did not open any prior-round review file, `scirep_submission_checklist.md`, or other reviewers' `review_r18/` outputs. All findings are recomputed from the manuscript, cover letter, and source data I read directly.

---

## § Stands up (verified — these I specifically suspected but found correct)

1. **Title length & structure.** "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and externally evaluates a 30-gene sepsis prognostic signature" = 17 words (≤20); single sentence, no colon/subtitle. Compliant.
2. **Abstract is unstructured, ≤200 words, and citation-free.** I recounted the abstract paragraph (manuscript.md:14) with a word tokenizer → **194 words** (≤200). No bracketed citations `[n]` appear in the abstract; the only in-text tokens are dataset IDs (GSE65682, E-MTAB-4451) and metric values, which are permitted. Compliant.
3. **Generative-AI-use statement (§2.12, manuscript.md:65–66) is present and Nature-compliant.** It names the tool environment (WorkBuddy routing to fungible commercial LLMs), enumerates the five permitted uses (text drafting/revising, table assembly, plotting/analysis code, reference retrieval, internal adversarial review), states no data were created/altered by AI, that no AI is an author, and that the author takes full responsibility. This satisfies Nature's mandatory disclosure location (Methods) and content.
4. **Data-availability names a real, versioned repository and the tag exists in git.** Statement (manuscript.md:263) gives `https://github.com/yyx-4113/sepsis-immunoparalysis-hub` and release tag `v1.18.0`. I ran `git tag -l v1.18.0`, `git describe --tags` (→ `v1.18.0`), and `git ls-remote --tags` → the annotated tag exists on the remote and dereferences to commit `57fe917`, exactly as the panel brief states. The "Zenodo DOI on acceptance" deferral is acceptable for Scientific Reports.
5. **Reference list is contiguous, first-appearance-ordered, fully cited, and correctly Nature-styled; ref [20] is real.** 38 entries (manuscript.md:286–323); my citation scan found all 38 cited with **zero orphans** and zero citations to non-existent numbers. Ref [20] (Wang, C., Liu, J., Wu, Q. *et al.*, *Front. Immunol.* **15**, 1328667 (2024), doi:10.3389/fimmu.2024.1328667) was resolved via Crossref to a genuine record whose title/journal/volume/article-number/year match the manuscript exactly; the `et al.` after three named authors and the `doi:` suffix are Nature-correct.
6. **"Independent in cohort and platform but not in label" is consistently qualified at 4 sites in the manuscript, and the pre-revision residual-phrase sweep is clean.** The qualification appears in the Article-type line (manuscript.md:8), §3.5 (manuscript.md:111), and Discussion (manuscript.md:184), plus the abstract's qualified wording (manuscript.md:14). My grep for `three of the five assessable hubs`, `three of five assessable hubs`, `widens rather than converges`, unqualified `reduced checkpoint engagement`, `conservative approximation`, `honest independent`, and `v1.17.0` returned **no matches** — the re-scoping left no stale copies.
7. **DCA "0.30–0.75 window" wording matches the source grid and is arithmetically correct; calibration is adequately caveated.** I recomputed net-benefit advantage (`nb_model − nb_treat_all`) from `03_results/09_ext_dca_grid.csv`: at 0.30–0.50 the advantage spans 0.0095–0.0944 (≈0.01–0.09, matches manuscript); at 0.55–0.75 it spans 0.1667–1.0471 (≈0.17–1.05, matches); at 0.80 `nb_model = 0.0` and `nb_treat_all = −1.5472` (matches "model NB = 0.00 = treat-none; treat-all −1.55"). The calibration slope 0.50 / intercept −0.04 is disclosed as fitted on the same 106-sample test set and therefore optimistic, and **no 95% CI is claimed for calibration** (consistent with the brief). The DCA does not read as an unqualified clinical-utility claim.

---

## Items (each with the four required parts)

### Item 1 — Cover letter contradicts the manuscript's qualified independence claim and over-states strength
【Problem】 The cover letter still uses unqualified "independent" and the word "robust" for the external validation, directly contradicting the manuscript's carefully qualified "independent in cohort and platform but not in label" / "real but modest" framing.
【Evidence】 `cover_letter.md:11` — "an honest **independent** external validation"; `cover_letter.md:14` — "generalised to AUC 0.638 ... on an **independent**, cross-platform external cohort" and "**Two findings are robust** and source-traceable". Contrast `manuscript.md:8,111,184,14`, which all qualify independence as "in cohort and platform but not in label" and describe the AUC as "real but modest" / "comparable to, not better than" the benchmark.
【Why it matters】 Scientific Reports editors read both documents; an unqualified "independent"/"robust" in the cover letter misrepresents the validation's epistemic status (the score orientation was fixed on the discovery cohort's labels) and is internally inconsistent with the manuscript the editor will peer-review. It risks an editor or reviewer reading the stronger claim as the paper's position.
【Specific fix】
- `cover_letter.md:11`: replace "an honest independent external validation" with "an honest external validation that is independent in cohort and platform but not in label".
- `cover_letter.md:14` (first sentence): replace "on an independent, cross-platform external cohort" with "on a cross-platform external cohort that is independent in cohort and platform but not in label".
- `cover_letter.md:14` (second sentence): replace "Two findings are robust and source-traceable" with "Two findings are source-traceable and modest in magnitude".

### Item 2 — Table 2 has a caption but no in-text cross-reference
【Problem】 The renumbered Table 2 (immune-function score by endotype) is presented with a caption but is never cited by an explicit "(Table 2)" cross-reference in the body, unlike Tables 1, 3, 4, and 5 which are each referenced in text.
【Evidence】 Caption at `manuscript.md:92` ("*Table 2. Immune-function score by MARS endotype…*"); my grep for `Table [1-5]` shows in-text references at `manuscript.md:72` (Table 1), `:120` (Table 3), `:149` (Table 4), `:162` (Table 5), but **no** in-text "(Table 2)" anywhere. §3.2 (manuscript.md:89–90) describes the score and the Mars1-vs-Mars2 non-separation but never points the reader to Table 2.
【Why it matters】 Scientific Reports expects every table/figure to be explicitly referenced from the text; an unreferenced table is a production-stage defect that can trigger a formatting query and suggests the table may be superfluous or misplaced.
【Specific fix】 In §3.2, after "…rather than a Mars1-specific signature." (manuscript.md:90), insert a cross-reference, e.g.: "The per-endotype medians and pairwise comparisons are summarised in Table 2." (place before the Table 2 caption).

### Item 3 — Supplementary numbering: S01/S02/S06/S07/S09 are shared by both tables and figures
【Problem】 The same numeric label (S01, S02, S06, S07, S09) is used for both supplementary *tables* and supplementary *figures*, distinguished only by a "Fig." prefix in the figure list, which is ambiguous against Scientific Reports' "Supplementary Table S1" / "Supplementary Figure S1" convention.
【Evidence】 `manuscript.md:255` index lists "S01 — Mars1 differential expression…", "S02 — immune-function score…", "S06 — 30-gene signature…", "S07 — hub and axis cellular-context…", "S09 — (deferred)…" as *tables*; `manuscript.md:257` lists "Fig. S01 (Mars1 28-d ROC), S02 (score vs endotype), S06A/B (CV and training ROC), S06C (decision-curve analysis), S07 (cellular context), S09 (external-cohort ROC)" as *figures*. The collision is visible at the index level (e.g., "S06" = a table in one bullet and "Fig. S06A/B" = figures in another).
【Why it matters】 Scientific Reports production style treats Table S-series and Figure S-series as separate, explicitly labelled sequences; a bare "S06" that is simultaneously a table and a figure invites mislabeling in the typeset supplementary file and reviewer confusion about which "S06" is meant.
【Specific fix】 Either (a) relabel figures as a distinct series (e.g., Fig. S1, S2, S3A/B, S6A/B, S6C, S7, S9, S10 → Fig. S1–S10) so no number collides with the table series, or (b) write every label in full as "Supplementary Table S1"/"Supplementary Figure S1" throughout the index and body. I recommend (a) for least churn.

### Item 4 (minor) — Statistics reporting: side of tests not always stated
【Problem】 Several significance statements do not explicitly state whether the test was one- or two-sided, which Scientific Reports' statistics-reporting policy expects.
【Evidence】 e.g. `manuscript.md:34` ("two-sided t" is stated — good) but `manuscript.md:90` Mann–Whitney P values and `manuscript.md:109` DeLong P ≈ 0.56 are not flagged as one/two-sided; bootstrap CI method is described but the number of resamples (2,000) is stated only for the AUC CI, not for any calibration/DCA resampling.
【Why it matters】 Low risk, but incomplete statistics reporting is a common Scientific Reports desk/additional-information query and is cheap to close.
【Specific fix】 Add "(two-sided)" to the Mann–Whitney and DeLong statements, and state the bootstrap resample count (2,000) once in §2.9/§3.5 where the calibration/DCA bootstraps are introduced.

---

## § Questions for the authors

1. The cover letter (Items 1) diverges from the manuscript on the word "independent" and on "robust." Was the cover letter simply not updated in the v1.18.0 pass, or do you intend the stronger claim? Please confirm the manuscript's qualified wording is the one you stand behind.
2. Table 2 (Item 2): is the omission of an in-text reference intentional (table self-contained) or an oversight from the renumbering? Please confirm §3.2 is the intended citation point.
3. Supplementary numbering (Item 3): do you prefer the separate figure-series fix or the full "Supplementary Table/Figure S*n*" relabel? Either is acceptable to me; I only need it unambiguous.
4. The DCA model still beats "treat-all" at threshold 0.80 (model NB 0.0 vs treat-all −1.55). The "0.30–0.75 window" wording describes where net benefit is *meaningfully* positive; please confirm you do not intend "model exceeds treat-all only inside 0.30–0.75," which would be inaccurate at 0.80.

---

## § What I actually checked

- **Files read:** `05_reports/review_r18/_PANEL_BRIEF.md`, `05_reports/manuscript.md` (full), `05_reports/cover_letter.md` (full). I did **not** read `scirep_submission_checklist.md` or any other reviewer/round file, per independence.
- **Abstract:** tokenized manuscript.md:14 → 194 words; confirmed zero `[n]` citations.
- **Git:** `git tag -l v1.18.0` (present), `git describe --tags` (→ v1.18.0), `git ls-remote --tags` (annotated tag + dereferenced `57fe917` on remote). Tag is real and matches the brief.
- **References:** regex scan of all `[n]` citations vs the 1–38 list → 38 cited, 0 orphans, 0 dangling. Ref [20] resolved via Crossref to a real record matching the manuscript.
- **Residual-phrase sweep:** grep for 7 pre-revision strings → no matches.
- **DCA numbers:** recomputed `nb_model − nb_treat_all` across `03_results/09_ext_dca_grid.csv`; confirmed 0.01–0.09 (0.30–0.50) and 0.17–1.05 (0.55–0.75) margins and the 0.80 values exactly. Confirmed no calibration CI is stated.
- **Compliance statements present:** title (≤20w), unstructured abstract (≤200w, no cites), generative-AI-use (§2.12), competing interests (manuscript.md:279), author contributions (manuscript.md:272), funding (manuscript.md:275), ethics/IRB (manuscript.md:269), data availability (manuscript.md:261–263, real URL+tag), standalone code availability (manuscript.md:265–267), supplementary index (manuscript.md:251–257).

---

## VERDICT — **Minor**

**Justification.** The manuscript satisfies every mandatory Scientific Reports structural/compliance requirement I could test: title length, unstructured ≤200-word citation-free abstract, a Nature-compliant generative-AI-use statement in Methods, a data-availability statement pointing to a real, version-tagged GitHub repository (tag `v1.18.0` verified in git), a correctly Nature-formatted 38-entry reference list with no orphans and a real, resolvable ref [20], and a standalone Code-availability section that does not duplicate Data-availability. Its self-description as methods-and-resources / "not discovery" is internally consistent throughout the body — the "independent in cohort and platform but not in label" qualification is applied at all four manuscript sites and the DCA/calibration limitations are honestly disclosed. The only substantive issue is a **cover-letter-vs-manuscript inconsistency** (unqualified "independent" + "robust" in the cover letter vs the qualified, "modest" manuscript wording), which is a document-alignment defect rather than a scientific flaw and is fixed with three short edits. The remaining items (Table 2 in-text reference, supplementary-numbering collision, side-of-test reporting) are routine production-stage polish.

**Desk-reject hard-fail statement.** No item in this review constitutes a desk-reject hard-fail. There is no missing mandatory statement, no unresolved format breach that blocks peer review, no fabricated/unresolvable reference, and no claim that over-reaches the declared article type within the manuscript itself; the single contradiction (cover letter "independent"/"robust") is between submitted documents and is trivially reconcilable. The manuscript is suitable for external peer review after the Minor revisions above.
