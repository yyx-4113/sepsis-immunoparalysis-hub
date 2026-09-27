# Round-17 blind venue review — A4 (Scientific Reports submission-compliance & desk-reject)

**Tag:** v1.17.0 · **Commit:** 5e1af29 (evaluated 1212f7b, tagged v1.16.0)
**Status:** First submission (treated as such; no prior-round material consulted)
**Scope:** Scientific Reports (Nature Portfolio) formatting & reporting-standards compliance; desk-reject hard-fail screen.

---

## § Stands up (compliant — verified with evidence)

1. **Abstract is non-structured, single-paragraph, citation-free, and within the 200-word cap.** Automated count of `manuscript.md` §Abstract = **196 words** (4-word margin). No `[n]` reference cites; substring `"Peng et al."` is **absent** (the benchmark is described as "the published immune-related-gene benchmark (0.619 reported on this cohort …)" with no author tag). Compliant.

2. **Title is a single sentence, ≤20 words, no mid-title colon/semicolon pun.** `manuscript.md:1` = *"A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and externally evaluates a 30-gene sepsis prognostic signature"* → **17 words**, one sentence, no colon/semicolon. Compliant.

3. **All eight mandatory statements present.** Article type (`manuscript.md:8`), Author contributions (`:268`), Competing interests (`:274`), Funding (`:271`), Ethics statement (`:265`), Data availability (`:261`), Acknowledgements (`:278`), Generative-AI disclosure (§2.12, `:65`). Compliant.

4. **Display-item budget satisfied.** Main text contains **5 tables** (Table 1, an unnumbered "Table:" in §3.2, Tables 2–4) and **0 main-text figures** — every figure is a supplementary *Fig. S0X* (9 references, all `S0X`). 5 ≤ 8. Compliant (see Item 3 on the unnumbered table).

5. **Article-type fit is within Scientific Reports scope.** Framed throughout as an Article / computational-biology / methods-and-resources report, explicitly *not* novel hub-gene discovery (`:8`, cover letter `:11`). Scientific Reports has no novelty/impact bar, so this framing is admissible.

6. **References: 37 entries, all with DOIs, journals italicised, volumes bold, first-appearance order consistent (spot-checked).** Count = 37 (`:282`–`:318`). Every entry ends with a `doi:`; journal names use `*…*` and volumes `**…**`. In-text citation order in §1 (refs `[1]`–`[8]` sequential) is consistent with Vancouver first-appearance. No desk-reject issue (one punctuation defect in `[31]`, Item 2).

7. **All headline numbers recomputed and match the text** (see § What I actually checked). External AUC 0.638 / CI 0.532–0.748 / n 106 / 52 deaths; CV 0.659; calibration slope 0.50 / intercept −0.04; DCA @0.80 model NB 0.00 vs treat-all −1.55; CD14 Egger OR 0.906 / P≈0.049; CD74 critical-care WM family-q≈3×10⁻¹⁷; primary IVW OR 0.92–1.12, P≥0.23; L1000 lenalidomide 5435 / azithromycin 9152 — **all verified against source CSVs**.

---

## Items

### Item 1 — Abstract word-count margin is tight 【caution】
- 【Problem】 The abstract measures **196 words**, only a **4-word margin** under the Scientific Reports 200-word cap.
- 【Evidence】 `manuscript.md` §Abstract automated token count = 196 (no `[n]` citations; "Peng et al." absent). Brief's "~196" confirmed.
- 【Why it matters】 A journal-side word counter using different hyphenation rules (e.g., splitting "30-gene", "multi-omics", "cross-validated") can exceed 200 and trigger a desk-format query or a mandatory trim request.
- 【Specific fix】 Build a safer margin by trimming ~10–15 words, e.g. *"A tri-method consensus identified five immune hubs"* → *"A consensus identified five immune hubs"*; drop the parenthetical *(label-informed)*; *"two-sample Mendelian randomisation gave no causal support"* → *"Mendelian randomisation gave no significant primary support"*. Target ≤185 words.

### Item 2 — Reference [31] carries a stray trailing period after the DOI 【recommend】
- 【Problem】 Reference `[31]` ends with a period *after* the DOI, whereas all other 36 references (e.g. `[1]`) end with no trailing period.
- 【Evidence】 `manuscript.md:312` → *"… (2025). doi:10.1001/jama.2025.24175."* vs `manuscript.md:282` → *"… (2016). doi:10.1001/jama.2016.0287"*. DOI `10.1001/jama.2025.24175` and year **2025** are correct.
- 【Why it matters】 Inconsistent end-punctuation is a formatting defect caught by technical/reference checks; trivial but must be uniform before acceptance.
- 【Specific fix】 Delete the trailing period: *"… (2025). doi:10.1001/jama.2025.24175"*

### Item 3 — Unnumbered main-text table in §3.2 【recommend】
- 【Problem】 §3.2 contains a captioned display table (*"Table: Immune-function score by MARS endotype"*) that is **not numbered**, while the other four main-text tables are numbered Table 1–4. This yields 5 main-text tables (still ≤8, so compliant) but with an inconsistent numbering scheme.
- 【Evidence】 `manuscript.md:92` caption *"*Table: Immune-function score by MARS endotype (median; Mann–Whitney U vs Mars1).*"* with a 4-row table; other captions are "*Table 1.*", "*Table 2.*", "*Table 3.*", "*Table 4.*".
- 【Why it matters】 Scientific Reports numbers every main-text display item; an unnumbered table reads as an oversight and breaks cross-referencing.
- 【Specific fix】 Renumber it as **Table 2** and shift the subsequent three to Table 3–5 (or fold it as a companion panel under Table 1). Keep all figures as *Fig. S0X*.

### Item 4 — No standalone "## Code availability" heading 【recommend】
- 【Problem】 Code-release information is folded into the "## Data availability" section rather than given its own "Code availability" heading.
- 【Evidence】 `manuscript.md:261` "## Data availability" includes *"All result tables (03_results/) and analysis code are released under MIT …"*; no separate `## Code availability` heading exists anywhere in the manuscript.
- 【Why it matters】 Scientific Reports explicitly requests a distinct Code availability statement. Folding it in may pass, but a dedicated heading is the template-compliant, safe choice and removes ambiguity.
- 【Specific fix】 Add a standalone section, e.g.:
  > **## Code availability**
  > The analysis code is released under the MIT licence at https://github.com/yyx-4113/sepsis-immunoparalysis-hub (citable GitHub release, tag v1.17.0; CITATION.cff included).

### Item 5 — "No causal support" headline slightly understates the MR readout 【caution — content nuance, NOT a venue hard-fail】
- 【Problem】 The sweeping "gave no causal support on the primary 28-day-death outcome" line understates that (a) one primary-outcome MR-Egger (CD14) is *nominally* significant (P≈0.049) and (b) the only family-significant result in the whole 45-test grid is CD74 critical-care (family-q≈3×10⁻¹⁷, *reversed* direction). The manuscript's own body text discloses both correctly, so this is a framing inconsistency, not a numerical error.
- 【Evidence】 `10_genetics_mr_outcome5086_28ddeath.csv` CD14 MR-Egger p=0.0488; `10_mr_bh_family.csv` CD74 WM critcare `q_family_45test`=2.99×10⁻¹⁷. Body §3.10 / Limitations already state these caveats.
- 【Why it matters】 Not a format defect, but a reviewer may flag the absolute "no causal support" wording as over-stated relative to the paper's own detailed MR section.
- 【Specific fix】 Soften the abstract/cover line to: *"two-sample Mendelian randomisation gave no significant primary IVW support; the single nominally significant primary-outcome MR-Egger (CD14, P≈0.049) and the lone family-significant result (CD74 critical care, reversed direction) are reported as suggestive only."*

---

## § Questions for the authors

1. Reference `[31]` (ImmunoSep, *JAMA* 2025) — please confirm the DOI `10.1001/jama.2025.24175` resolves to the correct article and remove the trailing period (Item 2).
2. Will you add a standalone **Code availability** heading (Item 4), and renumber the §3.2 table consistently (Item 3)?
3. The abstract's "no causal support" phrasing vs the CD14 Egger (P≈0.049) and CD74 critical-care (q≈3×10⁻¹⁷, reversed) results — do you intend the absolute wording, or the softened version in Item 5?
4. The supplementary figure index (§8) lists an "MR diagnostic set (forest, scatter, funnel, leave-one-out)" — please confirm all four plots are present in `04_figures/` (this is a reproducibility/path check, not a format block).

---

## § What I actually checked

**Files read (directly, this session):**
- `05_reports/manuscript.md` (full)
- `05_reports/cover_letter.md` (full)
- `03_results/09_external_validation.csv`
- `03_results/09_ext_calibration_dca.csv`
- `03_results/09_ext_dca_grid.csv`
- `03_results/S06_auc_compare.csv`
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv`
- `03_results/10_mr_bh_family.csv`
- `03_results/S08_l1000_candidate_scores.csv`

**Computations / recomputations vs manuscript:**
- Abstract word count: **196** (script count); "Peng et al." absent; no `[n]` cites → matches brief, under 200.
- Display-item inventory: **5 main-text tables** (Table 1, unnumbered §3.2 table, Tables 2–4), **0 main-text figures** (all 9 figure refs are `Fig. S0X`) → ≤8.
- External AUC: CSV `auc_EMTAB4451_orientedSum`=0.6382 → text 0.638 ✓; CI 0.5317–0.7475 → 0.532–0.748 ✓; `n_validated_samples`=106, `n_deaths`=52 ✓.
- CV AUC: `S06_auc_compare.csv` CV=0.6586 → text 0.659 ✓; train 0.7495 → 0.750 ✓.
- Calibration: `09_ext_calibration_dca.csv` slope=0.5028 → 0.50 ✓; intercept=−0.0382 → −0.04 ✓; no 95% CI claimed for slope/intercept (confirmed absent) ✓.
- DCA @0.80: `09_ext_dca_grid.csv` threshold 0.80 → `nb_model`=0.0, `nb_treat_all`=−1.5472 → −1.55 ✓ (model NB 0.00 vs treat-all −1.55, diverges, not converges).
- CD14 Egger: `10_genetics_mr_outcome5086_28ddeath.csv` OR=0.90595 → 0.906 ✓, P=0.0488 → 4.9×10⁻² ✓.
- CD74 critical-care WM: `10_mr_bh_family.csv` q_family=2.99×10⁻¹⁷ ✓ (reversed direction, OR 2.19).
- Primary IVW OR range: CD74 1.119, HLA-DQA1 0.923, CD14 0.927, HAVCR2 0.978, FIS1 0.963 → "0.92–1.12" ✓; min P = CD14 0.2359 ≥ 0.23 ✓.
- L1000: `S08_l1000_candidate_scores.csv` lenalidomide `rescue_rank`=5435 ✓; azithromycin=9152 ✓.

**Discrepancies found:**
- Headline numbers: **none** — all match source CSVs.
- Reference `[31]` trailing period after DOI (Item 2).
- Unnumbered §3.2 table (Item 3).
- Abstract word count 196 ≈ brief's "~196" (consistent; tight margin, Item 1).

**Forbidden files NOT opened (per independence rules):** `05_reports/REVIEW_round*.md`; `05_reports/review_r12/`–`review_r16/`; `.workbuddy/memory/` (any); `05_reports/scirep_submission_checklist.md`; any other `05_reports/review_r17/*` file. None were read, grepped, or summarised. This manuscript was assessed as a first submission.

---

## VERDICT

**Minor** — the submission is **format-compliant with Scientific Reports** and contains **no desk-reject hard-fail**.

Justification:
- No abstract over-length, no structured-abstract violation, no missing mandatory statement, no out-of-scope article-type misrepresentation, display items within the ≤8 budget, references complete with DOIs.
- All recomputed headline numbers match the deposited source files exactly, so there is no data-integrity or misreporting issue that would justify desk rejection.
- The only findings are **recommend**-level formatting polish (reference `[31]` trailing period; unnumbered §3.2 table; missing standalone Code-availability heading) and **caution**-level margin/framing notes (abstract 4-word margin; "no causal support" over-statement relative to the paper's own MR detail).

**Explicit statement on desk-reject hard-fail:** **NONE.** No item in this review constitutes a desk-reject hard-fail. The manuscript can proceed to scientific review; the recommend/caution items should be cleared during author revision.
