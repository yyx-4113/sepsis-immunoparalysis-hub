# A4 — Scientific Reports (Nature Portfolio) submission-compliance & desk-reject audit

**Round:** 16 (independent blind panel) · **Manuscript tag:** v1.16.0 · **Focus:** Sci Rep submission-format compliance + desk-reject risk
**Reviewer posture:** first-submission read; every claim below was read from `manuscript.md` / `cover_letter.md` and recomputed from the listed `03_results/*.csv`. Prior rounds not read.

---

## § Stands up (compliant — verified)

1. **Abstract is Sci-Rep-compliant.** Non-structured single paragraph; measured **196 words** (≤200); **contains no reference numbers, no "Peng", no "et al."** — the named-author "Peng et al." benchmark is correctly absent from the abstract (described only as "the published immune-related-gene benchmark (0.619 reported on this cohort…)"). *Evidence:* `manuscript.md:14`; script count = 196 words, `Peng=False`, `[=ref]=False`, `et al.=False`.

2. **Title compliant.** Single sentence, **17 words** (≤20), no semicolon/colon mid-title. *Evidence:* `manuscript.md:1` ("A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and externally evaluates a 30-gene sepsis prognostic signature"); script count = 17.

3. **References compliant.** **37 entries**, numbered sequentially in first-appearance order (Vancouver); **all 37 carry a DOI**; every journal name is wrapped in italics (`*…*`) and every volume in bold (`**…**`). *Evidence:* `manuscript.md:280–318`; script: 37 entries, `Missing DOI=[]`, `no_italic=[]`, `no_bold=[]`.

4. **All eight mandatory statements present.** Article type, Author contributions, Competing interests, Funding, Ethics, Data availability, Acknowledgements, and Generative-AI disclosure (§2.12). *Evidence:* grep `FOUND` for `## Data availability`, `## Ethics statement`, `## Author contributions`, `## Funding`, `## Competing interests`, `## Acknowledgements`, `## 2.12 Use of generative AI`, `Article type` (`manuscript.md:8, 65–66, 261–279`).

5. **Display items within main-text limit.** **0 main-text figures** (every figure is an `Fig. S0X` supplementary item) and **4 main-text tables** (Table 1–4) ⇒ 4 display items ≤ 8. *Evidence:* regex "Non-supplementary Fig. mentions = NONE"; 4 `Table` captions.

6. **Article-type fit is honest and appropriate.** Framed throughout as *Article (original research) — computational biology / methods-and-resources*, explicitly "not novel hub-gene discovery" (near-replication + pipeline + honest external validation + blueprint). This matches Sci Rep's scope (no novelty/impact bar; validity + standards bar). *Evidence:* `manuscript.md:8` and `:184`.

7. **Headline numbers recomputed and match the text** (provenance gate): external AUC **0.6382 → 0.638**, 95% CI **0.5317–0.7475 → 0.532–0.748**, n=106 / 52 deaths (`09_external_validation.csv:11–13`); CV AUC **0.6586 → 0.659**, train 0.750 (`S06_auc_compare.csv:2–3`); calibration slope **0.5028 → 0.50**, intercept **−0.0382 → −0.04**, no slope CI claimed (`09_ext_calibration_dca.csv:2`; §3.5 text); DCA at 0.80 model NB **0.00** vs treat-all **−1.5472 → −1.55** (`09_ext_dca_grid.csv:17`); CD14 28-d Egger **OR 0.906, P=4.9e-2** (`10_genetics_mr_outcome5086_28ddeath.csv:9`); CD74 critical-care WM **OR 2.194, q≈3e-17** (`10_mr_bh_family.csv:17`); primary-outcome all IVW **OR 0.92–1.12, P≥0.23** (Table 3); L1000 lenalidomide **5435/20413**, azithromycin **9152/20413** (`S08_l1000_candidate_scores.csv`).

8. **Generative-AI disclosure exceeds the minimum.** §2.12 is explicit about LLM use in drafting/formatting/code/reference-retrieval, states no data were created/altered and no AI is an author — satisfies Sci Rep's AI-use statement requirement. *Evidence:* `manuscript.md:65–66`.

---

## Items

### Item 1 — Reference [31] DOI punctuation/identity inconsistency (minor, copy-edit; NOT a desk-reject)
【Problem】 Reference [31] carries a trailing period after the DOI and a possible year/DOI mismatch that the other 36 entries do not have.
【Evidence】 `manuscript.md:312` ends "…doi:10.1001/jama.2025.24175." (note the terminal period; all other entries terminate at the DOI with no period). Volume year is "(2026)" while the DOI string embeds "2025", which is plausible only if epub-ahead-of-print; it is unverified here.
【Why it matters】 A wrong/non-resolving DOI fails the "all DOIs" gate and breaks the reference; the stray period is a formatting inconsistency a copy editor will flag. Not a desk-reject, but a real compliance blemish on the one gate (references) that must be internally uniform.
【Specific fix】 Remove the trailing period; confirm the DOI resolves to the intended JAMA article (correct to `10.1001/jama.2026.24175` if the 2025 string is a typo) and align the year.

### Item 2 — Code-availability statement is folded into Data availability (recommended; NOT a desk-reject)
【Problem】 Sci Rep expects an explicit code-availability statement for computational studies; here code availability is embedded in the Data availability paragraph rather than standing as its own heading.
【Evidence】 `manuscript.md:261–263` ("analysis code are released under MIT… GitHub… CITATION.cff") sits inside `## Data availability`; there is no `## Code availability` section.
【Why it matters】 Sci Rep routinely requests a separate code-availability statement at acceptance; folding it in is acceptable but invites an editorial query and slightly weakens the auditability claim that is this paper's central selling point.
【Specific fix】 Add a short `## Code availability` subsection: "Analysis code is released under the MIT licence at https://github.com/yyx-4113/sepsis-immunoparalysis-hub (tag v1.16.0; CITATION.cff provided)."

### Item 3 — Tag→commit provenance must be reconciled before acceptance (provenance; should-fix, NOT a format desk-fail)
【Problem】 The manuscript asserts the evaluated commit is `fc5473b` and is tagged v1.16.0, but the panel brief records the evaluated commit as `1212f7b`; the two hashes disagree and the mapping is not independently verifiable from the manuscript alone.
【Evidence】 `manuscript.md:263` "the current evaluated commit fc5473b is tagged v1.16.0"; panel brief line 3 "commit `1212f7b`". The cover letter names only the tag (`cover_letter.md:24`), not a commit, so there is no internal manuscript↔cover contradiction — but the manuscript's stated commit cannot be confirmed against the stated tag.
【Why it matters】 This paper's entire contribution is reproducibility/auditability; if the v1.16.0 release/tag does not point to the exact commit that generated `03_results/`, every number in §7 becomes un-retrievable. A wrong commit is a credibility (not a format) defect, but it should be fixed before acceptance.
【Specific fix】 Confirm the GitHub v1.16.0 release/tag resolves to the commit that produced `03_results/`; print that exact hash in both manuscript and cover letter; if they differ, re-tag or correct the text.

### Item 4 — Abstract word count sits 4 below the 200-word ceiling (caution; NOT a defect)
【Problem】 Abstract measures 196 words, leaving only a 4-word margin under the 200 limit.
【Evidence】 script count `manuscript.md:14` = 196 words.
【Why it matters】 No failure today, but routine author revisions during peer review could push it over 200 and trigger a format rejection at the typesetting stage.
【Specific fix】 Optional trim for safety margin, e.g. drop "(label-informed)" or "(on T cells and antigen-presenting cells)".

---

## § Questions for the authors

1. Does the GitHub **v1.16.0** tag actually point to commit `fc5473b` (the one that generated `03_results/`)? Please reconcile with the `1212f7b` recorded in the submission metadata, or correct the text.
2. Reference [31]: please confirm the DOI resolves and that the 2025/2026 year pairing is intentional (epub vs issue).
3. The calibration slope is reported as **0.50 with no 95% CI** — confirm this is deliberate (the brief flags "no CI claimed"); is any bootstrap CI available, even as a caution?
4. The MR family correction treats 45 tests as independent while noting overlapping hypothesis structure (same gene × estimators/outcomes). Was any dependence-aware correction (e.g., Golm/cluster-level) considered, or is the current conservative approximation the intended claim?
5. FCGR3A was excluded for "insufficient instruments" (2 variants even at relaxed thresholds). Was FCGR3A re-run against an alternate eQTL source, or is its omission final?

---

## § What I actually checked

**Files read:** `05_reports/manuscript.md` (full), `05_reports/cover_letter.md` (full), and CSVs: `09_external_validation.csv`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`, `S06_auc_compare.csv`, `S05_hub_genes.csv`, `S08_l1000_candidate_scores.csv`, `08_candidates_drugs.csv`, `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, `10_mr_bh_family.csv`.

**Computations / re-computations performed:**
- Abstract word count (196), title word count (17), abstract citation scan (no `[n]`/`Peng`/`et al.`) — script.
- Reference list parse: 37 entries, all with `doi:`, all with italic journal + bold volume — script.
- Mandatory-statement presence — grep (all 8 FOUND).
- Main-text display-item census: 0 non-supplementary figures, 4 tables — regex.
- External AUC/CI/n/deaths, CV/train AUC, calibration slope/intercept, DCA NB at 0.80, CD14 Egger OR/P, CD74 critical-care WM family-q, L1000 ranks — all read directly from CSVs and matched to manuscript text (see § Stands up #7).

**Discrepancies found:** only the three minor items above (ref [31] punctuation/year, missing standalone code-availability heading, tag/commit provenance). No manuscript↔cover-letter contradiction on version tag (v1.16.0), claims, or data availability. No numeric discrepancy between manuscript and the audited CSVs. No FORMAT hard-fail.

**Forbidden files not opened:** `REVIEW_round*.md`, `review_r12/`–`review_r15/`, `.workbuddy/memory/`, `scirep_submission_checklist.md`, and all other `review_r16/` outputs.

---

## VERDICT: Minor — no item is a DESK-REJECT hard-fail.

Justification: every Sci Rep submission-format gate passes on direct inspection — non-structured abstract ≤200 words with no citations (196 words, "Peng et al." absent), single-sentence 17-word title, 37 Vancouver references all with DOIs/italic journals/bold volumes, all eight mandatory statements present (incl. explicit generative-AI disclosure §2.12 and Article type), and ≤8 main-text display items (4 tables, 0 main-text figures, all figures supplementary). The article-type framing (computational biology / methods-and-resources, explicitly not novel discovery) is honest and within scope, so there is no scope-based desk-reject. The three flagged items are copy-edit/provenance matters (reference [31] DOI period + year; standalone code-availability heading; reconcile tag↔commit hash), none of which blocks desk evaluation. Recommend **Minor revision** to close the reference-format uniformity and provenance items before acceptance; no Major or Desk-reject.
