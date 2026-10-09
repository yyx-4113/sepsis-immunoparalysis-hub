# A4 — Venue / Submission-fit review (Round-22, independent)

**Independence attestation:** I did NOT read `06_review/` (any prior round), any rebuttal/response letter, or git history for prior reviews; this verdict is based solely on `05_reports/manuscript.md` (v1.23.1), `07_submission_bmc_v1.21.0/` artifacts, and the repository metadata files named in the brief.

---

## Verdict: MAJOR

The manuscript *proper* is clean for BMC Medical Genomics (scope fits, article type appropriate, all declarations present in the docx, no MR residue in the paper, title/figure maps consistent). However, the **submission package as a whole is internally contradictory**: the reproducibility guide (README) and cited metadata files (CITATION.cff, author_verification_statement) contain stale MR content, a wrong version tag, and a mismatched title. These must be fixed before submission. The docx also omits the keywords that both the source .md and BMC's form require.

---

## Findings

### [Tier 1] README.md still documents an executed S10 two-sample MR layer — contradicts the "MR removed in v1.20.0" claim
- **File:line:** `README.md:45` (`10_genetics_mr_run.py | S10: two-sample MR of hub genes ... requires OpenGWAS JWT`); `README.md:98` (full "S10 two-sample MR is executed … CD14 MR-Egger OR 0.906, P=4.9×10⁻² … CD74 critical-care weighted median OR 2.194, P=6.6×10⁻¹⁹ … no causal claim is made").
- **Claim:** The submission brief, `build_submission_bmc.py:4-5`, `SUBMISSION_MANIFEST.md:20` and `:507` all assert the Mendelian-randomisation layer was removed in v1.20.0 and that the two MR figures are excluded.
- **Problem:** The manuscript's own §8 supplementary index lists S09 (deferred) and S11 but **not S10**, and the manuscript body has zero MR content — yet the README (the regeneration guide that `manuscript.md:221` points to via "deposited processing scripts") keeps S10 MR as a live pipeline step and *reports MR statistics*. This is precisely the "dangling MR content that confuses reviewers" the panel brief warned about. A reviewer opening the repo will see an active MR section the paper says was removed. `verify_submission_bmc.py` only scans the exported manuscript text, so this residue slips through its guard.
- **Fix:** Either (a) delete the S10 MR row from the README key-scripts table and delete the entire MR paragraph in "Stated caveats" (line 98), or (b) if MR is genuinely retained as a non-submitted supplement, add an explicit, unambiguous note that S10 is excluded from the BMC submission and is not cited anywhere in the manuscript. Do not leave an executed-MR narrative dangling.

### [Tier 1] CITATION.cff title does not match the manuscript title
- **File:line:** `CITATION.cff:2` → `"Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics confirmation and in-silico drug repositioning"`; `manuscript.md:1` → `"A reproducible, fully auditable pipeline confirms within-cohort the MARS Mars1 immunoparalysis program and delivers an honest external validation of a 30-gene sepsis prognostic signature"`.
- **Problem:** `manuscript.md:225` (Code availability) states "CITATION.cff included." A reader who cites via the deposited CITATION.cff gets a **different, stale title** than the submitted paper. Version in CITATION.cff is correctly 1.23.1 (line 12), but the title is an older variant.
- **Fix:** Set `CITATION.cff` title to the exact v1.23.1 manuscript title.

### [Tier 1] author_verification_statement.md cites wrong version tag (v1.0.0) and a mismatched title
- **File:line:** `author_verification_statement.md:3` (title variant "a multi-omics dissection and in-silico drug repositioning"); `author_verification_statement.md:22` → "versioned repository … (tag v1.0.0)".
- **Problem:** The statement says the repository is released at **tag v1.0.0**, but the manuscript/manifest/CITATION.cff all use **v1.23.1** (and Zenodo DOI 10.5281/zenodo.23042366). A reviewer cross-checking the cited tag will not find the submitted version. The title is also a third variant.
- **Fix:** Change "tag v1.0.0" → "tag v1.23.1"; align the title with the manuscript; add the Zenodo DOI for consistency with the Data availability section.

### [Tier 1] Manuscript.docx is missing the Keywords line
- **File:line:** `07_submission_bmc_v1.21.0/BMC_structured_abstract.md` (no `Keywords:` line); confirmed absent in `Manuscript.docx` (grep for "Keywords"/"sepsis;"/"immunoparalysis;" → False). The source `manuscript.md:16` carries keywords: *sepsis; immunoparalysis; MARS endotype; Mars1; external validation; drug repositioning*.
- **Problem:** The built docx uses the structured abstract and drops the keyword list. BMC's submission form requires keywords, and the manifest's "Metadata the form will ask for → Keywords: as listed under the abstract" implies they are present. They are not in the docx.
- **Fix:** Add a `Keywords:` line (the six .md keywords) to `BMC_structured_abstract.md` so it is carried into the docx; verify it appears in the built file.

### [Tier 2] Provenance-commit ambiguity between manuscript and manifest
- **File:line:** `manuscript.md:221` → "the current evaluated commit **1212f7b** is tagged **v1.16.0**"; `SUBMISSION_MANIFEST.md:3` → "built on commit **7704c9a** (v1.20.0, MR layer removed), which sits above the results-pinned commit 1212f7b (v1.16.0)". The brief names the target commit as `e8ba121` (tag v1.23.1).
- **Problem:** Three different commit references float around. For computational reproducibility (which BMC emphasises), the "evaluated/results-pinned" commit should be stated unambiguously and identically in the manuscript and manifest.
- **Fix:** State one consistent evaluated-commit hash + tag v1.23.1 in both the manuscript Data availability and the manifest.

### [Tier 2] README.md / author_verification_statement.md titles are stale variants (not the v1.23.1 title)
- **File:line:** `README.md:3` ("… a multi-omics dissection and in-silico drug repositioning"); `author_verification_statement.md:3` (same "dissection" variant).
- **Problem:** Descriptive repository docs use an older title that does not match the submitted manuscript title, creating minor citation/consistency confusion.
- **Fix:** Align both titles with the v1.23.1 manuscript title.

### [Tier 3] S6C (decision-curve) is enumerated in §8/figures but is not cited by an inline "Fig. S6C" label in the Results body
- **File:line:** `manuscript.md:196` (S06_dca.png referenced only in §7 provenance), `manuscript.md:215` (§8 lists S6C). The caption exists; the figure is valid, just not called out in §3.
- **Fix:** Optional — add a one-line inline reference to Fig. S6C in §3.5 (calibration/DCA) for traceability. Cosmetic.

---

## Cross-validation note (what I independently verified)
- **Title word count:** The actual manuscript title has **24 whitespace tokens** (`A reproducible, fully auditable pipeline confirms within-cohort the MARS Mars1 immunoparalysis program and delivers an honest external validation of a 30-gene sepsis prognostic signature`) — **matches the manifest's claim of 24** (SUBMISSION_MANIFEST.md:23). Confirmed programmatically.
- **Figure file list:** The manifest correctly enumerates the 10 produced PNGs — `Fig_S1, Fig_S2, Fig_S3A, Fig_S3B, Fig_S6A, Fig_S6B, Fig_S6C, Fig_S7, Fig_S9, Fig_S10` — which exactly matches the manuscript §8 index (S1, S2, S3A/B, S6A/B/C, S7, S9, S10) and the docx caption block. S4/S5/S8 are correctly noted as absent; **no false implication of a continuous S1–S10 series**. The build script's `FIG_CAPTIONS` (build_submission_bmc.py:452-467) maps each to a real source PNG. No mismatch.
- **Declaration presence (docx):** Confirmed present and complete — Ethics approval and consent to participate, Consent for publication (auto-added by build), Data availability, Code availability, Competing interests, Funding, Author contributions, Acknowledgements, and the generative-AI disclosure (§2.11). Exactly **40** Vancouver references (max ref number 40). **Zero MR-residue** keywords and **zero Chinese characters** in the docx. GitHub URL and Zenodo DOI 10.5281/zenodo.23042366 both present in the docx.
- **Limitation:** I could not reach the network from this environment, so I could **not** verify that the GitHub tag `v1.23.1` and the Zenodo DOI `10.5281/zenodo.23042366` actually resolve/live. They are internally consistent across all artifacts, but the author must confirm both resolve before submitting.

---

## One-line integrator summary
Manuscript-to-BMC fit is sound (scope, article type, declarations, title count, figure map all check out), but the submission package is contradicted by stale MR content and a wrong version tag in README/CITATION.cff/author_verification_statement and by missing keywords in the docx — fix these four packaging defects before submission.
