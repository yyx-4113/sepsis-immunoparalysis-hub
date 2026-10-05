# A4 — Venue Expert Review (BMC Medical Genomics, handling editor + reporting-standards auditor)

**Manuscript:** "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and externally evaluates a 30-gene sepsis prognostic signature"
**Version evaluated:** v1.20.0 (tag `v1.20.0`, repo `github.com/yyx-4113/sepsis-immunoparalysis-hub`)
**Target journal / article type:** BMC Medical Genomics — Research article / Methods & Resources
**Reviewer role:** Venue (handling-editor format gate + reporting-checklist honesty)
**Review round:** round19 (treated as FIRST submission; independent of all prior review files)

---

## Editor judgement — recommendation

**MINOR REVISION.** The manuscript is **suitable for BMC Medical Genomics in principle** (in scope, complete BMC declarations, structured abstract, 36 Vancouver references all cited, 10 figures, no MR residue, v1.20.0 correctly carried, strong computational-reproducibility reporting). It is **not** desk-rejectable and does **not** require major revision. However, three issues must be fixed before submission because they are either a submission-system hazard (figure re-naming/mislabel risk), a factual inconsistency in the abstract, or a provenance drift between derived artifacts. One credibility-strengthening action (TRIPOD/CLIP for the prognostic signature) is strongly recommended but not a hard fail.

Rationale, by severity:
- **Format hard-fails: NONE.** All BMC structural requirements (structured abstract, declarations block, Vancouver refs, figures as separate files) are met in the derived `Manuscript.docx`.
- **Wording / credibility issues (must fix):** abstract misstates the drug shortlist (glucocorticoids are *not* among the seven prioritised agents); article-type self-description ("methods-and-resources") is not a BMC article-type option; commit-hash drift between `SUBMISSION_MANIFEST.md` and the manuscript/docx.
- **Process hazard (must fix before upload):** the 10 uploaded PNGs are named `Fig1–Fig10.png` while every caption in the docx/SI uses the `S`-series labels, and the multi-panel figures (`S3A/B`, `S6A/B/C`) are mapped to upload filenames in a **non-sequential** order — a mechanical 1:1 mapping will mislabel panels.
- **Source-of-truth drift (should fix):** `manuscript.md` still carries a single unstructured inline abstract and a non-standard `## Ethics statement` heading that the derived docx corrected; if the docx is ever regenerated from `manuscript.md`, those corrections are lost.

---

## § Stands up (compliant strengths — with evidence)

1. **Complete, compliant BMC Declarations block.** `Manuscript.docx` carries all seven required declarations as explicit headings: *Ethics approval and consent to participate* (paragraph "This is a purely computational re-analysis…"), *Consent for publication* ("Not applicable…"), *Data availability*, *Code availability*, *Author contributions*, *Funding*, *Competing interests*, plus an *Acknowledgements* and the §2.11 generative-AI disclosure. This is a clean pass against the BMC format gate.
2. **Structured abstract with honest confirm/validate framing and no overclaim.** `Manuscript.docx` Abstract has **Background / Methods / Results / Conclusions** each with real content. Title uses "confirms… and externally evaluates" (not "discovers/novel"); Background states "we framed this as a confirmation-and-validation question rather than novel-gene discovery"; Conclusions state "not novel hub-gene discovery." No headline-over-claim mismatch.
3. **Exemplary computational-reproducibility reporting.** §7 Number provenance table maps every reported number to a deposited `03_results/` file; §2.11 discloses generative-AI use with the fungible-model caveat; Zenodo DOI `10.5281/zenodo.23042366` and GitHub tag v1.20.0 are given. This exceeds typical MICRoR-level transparency for a single-author comp-bio paper.
4. **Rigorous, explicit Limitations (10 numbered items).** The honest treatment of the optimistic within-cohort AUC, the prednisone positive-control caveat (§3.9/§5.10), and the single-direction L1000 rescue (§5.10) materially strengthen credibility and are consistent across sections — a genuine strength for this venue.

---

## Detailed findings (each with 【Problem】/【Evidence】/【Why it matters】/【Specific fix】)

### F1 — Abstract: drug shortlist statement is factually wrong (credibility, must fix)
【Problem】 The structured-abstract Results claims the seven prioritised agents *include* the positive-control glucocorticoids, but glucocorticoids are explicitly excluded from the shortlist and appear only as a disqualifying positive control.
【Evidence】 `Manuscript.docx` Abstract → Results: "Seven immune-modulating agents were prioritised, **including the positive-control glucocorticoids**." Contrast with `Manuscript.docx` Table 3 (the seven = IL-7, GM-CSF, IFN-γ, Azithromycin, Lenalidomide, Thymosin α1, BCG) and §3.9/§5.10, where prednisone/dexamethasone are a positive-control caveat that *disqualifies* the L1000 ranking as supportive, not a candidate.
【Why it matters】 This is an internal contradiction a copyeditor or reviewer will catch immediately; it misrepresents the drug-repositioning conclusion and undermines the otherwise careful honesty of the paper. Credibility issue, not a format fail, but it must be corrected before submission.
【Specific fix】 Replace the clause so it reads, e.g.: "Seven immune-modulating agents (IL-7, GM-CSF, IFN-γ, azithromycin, lenalidomide, thymosin α1, BCG) were prioritised; glucocorticoids served only as a positive-control caveat in the LINCS L1000 check (§3.9) and are not part of the shortlist." Ensure the abstract shortlist list matches Table 3 exactly.

### F2 — Article-type self-description conflicts with BMC article-type options (wording, must fix)
【Problem】 The title-page line calls the work "Article (original research)" and a "computational-biology / methods-and-resources report," but "Methods & Resources" is not a BMC Medical Genomics article-type dropdown value; the manifest instructs the form to be set to "Research article."
【Evidence】 `Manuscript.docx` paragraph "Article type. Article (original research). This is a computational-biology / methods-and-resources report: …". `SUBMISSION_MANIFEST.md` line 24: "Article type: Research article."
【Why it matters】 Wording only, not a desk-reject fail, but the manuscript's self-label must match the system-selected article type or it reads as confused scope. "methods-and-resources" is a PLOS-style descriptor, not a BMC category.
【Specific fix】 Either (a) delete the "Article type." sentence entirely (BMC selects article type in the system, not in the manuscript), or (b) change it to: "Article type: Research article." Remove the phrase "methods-and-resources" or relocate it to a one-line "Study type" note that does not masquerade as the BMC article type.

### F3 — Figure upload filenames (Fig1–Fig10) vs caption labels (S-series) with non-sequential multi-panel mapping (process hazard, must fix)
【Problem】 The 10 submitted PNGs are named `Fig1.png`–`Fig10.png`, but every caption in `Manuscript.docx` and `Supporting_Information.docx` uses the `S`-series (`Fig. S1, S2, S3A, S3B, S6A, S6B, S6C, S7, S9, S10`). The multi-panel figures are mapped to upload filenames in a non-sequential order, so a mechanical/numeric 1:1 mapping will mislabel panels.
【Evidence】 `07_submission_bmc_v1.20.0/Figures/` contents vs captions:
- `Fig1.png` = `S01_roc_28d_mars1.png` → **S1**
- `Fig2.png` = `S02_score_vs_endotype.png` → **S2**
- `Fig3.png` = `S03_eigengene_trait_cor.png` → **S3B** (not S3A)
- `Fig4.png` = `S03_top_hub.png` → **S3A**
- `Fig5.png` = `S06_dca.png` → **S6C**
- `Fig6.png` = `S06_roc_cv.png` → **S6A**
- `Fig7.png` = `S06_roc_train.png` → **S6B**
- `Fig8.png` = `S07_celltype.png` → **S7**
- `Fig9.png` = `fig_s09_external_roc.png` → **S9**
- `Fig10.png` = `fig_s10_l1000_rescue.png` → **S10**
Note `S3A/S3B` and `S6A/S6B/S6C` are *reversed/scrambled* relative to upload order. `Manuscript.docx` §8 figure index and `Supporting_Information.docx` "Figure captions" both list S1, S2, S3A, S3B, S6A, S6B, S6C, S7, S9, S10 — internally consistent with the body, but not with the `FigN` filenames.
【Why it matters】 The BMC submission system requires each uploaded figure file to be mapped to its caption. Because the filename numbers do not correspond to the caption letters, an author who maps by numeric position will attach `Fig3.png` (eigengene correlation) to the "S3A hub genes" caption and vice-versa, and will attach `Fig5.png` (DCA) to "S6A CV ROC." This is a real mislabeling hazard, not a content error in the docx itself.
【Specific fix】 Provide the editorial/submission mapping table above explicitly in the cover letter or a manifest note, and in the BMC upload screen map each `FigN.png` to the correct caption by content (not by number). Better: rename the upload files to match captions, e.g. `FigS1.png … FigS3A.png, FigS3B.png, FigS6A.png, FigS6B.png, FigS6C.png, FigS7.png, FigS9.png, FigS10.png`, so filename and caption agree. Confirm `S3A/S3B` and `S6A/S6B/S6C` ordering against `04_figures/` before upload.

### F4 — Provenance drift: commit hash disagrees between manifest and manuscript/docx (derived-artifact drift, must fix)
【Problem】 The evaluated commit tagged v1.16.0 is given as `1212f7b` in the manuscript/docx but as `7704c9a` in `SUBMISSION_MANIFEST.md`; the three artifacts are mutually inconsistent on the underlying commit.
【Evidence】 `Manuscript.docx` Data availability: "(the current evaluated commit **1212f7b** is tagged v1.16.0, and this v1.20.0 release is built on top of it)." `manuscript.md:221` same `1212f7b`. `SUBMISSION_MANIFEST.md:3`: "built on commit **7704c9a** / tag v1.16.0."
【Why it matters】 For a paper whose central selling point is auditable reproducibility, a wrong/conflicting commit hash in the submission manifest directly undermines the "every number traces to a file" claim and will confuse reviewers checking provenance. Not a format fail, but a provenance-integrity defect that must be reconciled.
【Specific fix】 Verify the actual git object: run `git rev-parse v1.16.0` and `git rev-parse v1.20.0` in the repo, then make `manuscript.md`, `Manuscript.docx`, and `SUBMISSION_MANIFEST.md` state the *same* commit hash for v1.16.0 (and the correct HEAD commit for v1.20.0). Pick one canonical phrasing: "v1.20.0 release (commit <X>) builds on the v1.16.0 snapshot (commit <Y>)."

### F5 — Source-of-truth drift: `manuscript.md` not updated to match the derived docx (should fix)
【Problem】 `manuscript.md` still contains a single unstructured inline abstract and a non-standard `## Ethics statement` heading, both of which the derived `Manuscript.docx` corrected (structured abstract; "Ethics approval and consent to participate"). If the docx is regenerated from `manuscript.md`, the BMC-compliant corrections are lost.
【Evidence】 `manuscript.md:12-16` = one-paragraph "## Abstract (English)" with no Background/Methods/Results/Conclusions headings; `manuscript.md:227` = "## Ethics statement" (no separate "Consent for publication" heading). `Manuscript.docx` instead has the four-heading structured abstract and the BMC-standard "Ethics approval and consent to participate" + a dedicated "Consent for publication: Not applicable." block.
【Why it matters】 The docx currently passes the format gate, but the manuscript's source of truth is non-compliant; any future regeneration reintroduces the defect. It also means the repo's `manuscript.md` — which reviewers may open via the Zenodo/GitHub link — fails the BMC structured-abstract and declarations-heading requirements.
【Specific fix】 Back-port the corrections into `manuscript.md`: (a) replace the single abstract paragraph with the structured four-section abstract (use `BMC_structured_abstract.md` as the canonical source); (b) rename `## Ethics statement` to `## Ethics approval and consent to participate` and add a `## Consent for publication` heading ("Not applicable."), and add the explicit `## Competing interests` / `## Funding` headings if not already present (they are present at lines 233–237, so only ethics+consent need the rename/add).

### F6 — Reporting standards: STROBE present in spirit; TRIPOD/CLIP gap for the prognostic signature (credibility, recommended)
【Problem】 The 30-gene signature is a developed-and-externally-validated prognostic model, but the manuscript supplies no TRIPOD/CLIP-aligned reporting (no prediction-model flow/diagram, no systematic model-specification, participant-flow, or optimism-correction table), and no STROBE note for the observational cohort re-analysis.
【Evidence】 `Manuscript.docx` §2.6, §3.4, §3.5 report AUC/CI, calibration slope (0.50), and DCA, but there is no TRIPOD/CLIP diagram; §2.1/§2.9 describe cohorts but no STROBE-style participant-flow or eligibility statement is invoked. The paper self-labels as "Methods & Resources," so a full TRIPOD is not mandatory, but the signature is the paper's headline quantitative claim.
【Why it matters】 Not a BMC hard fail, but a prediction model reported without TRIPOD/CLIP items is weaker and more challengeable; reviewers at a genomics-methods journal will ask how the model was specified, how missing data were handled, and how optimism was corrected. The optimism point is already honestly addressed (§3.4 within-cohort CV is "optimistic"; external 0.638 is the honest estimate) — it simply is not packaged as a reporting item.
【Specific fix】 Add a short "Prediction-model reporting" note (or a supplementary TRIPOD-style flow diagram) stating: (i) model type (L1-penalised logistic regression + fixed-orientation equal-weight score), (ii) predictor set and orientation rule, (iii) validation scheme (locked model, 5-fold stratified CV internally; external locked application on E-MTAB-4451), (iv) optimism handling (bootstrap CI on external; explicit statement that internal CV is optimistic), (v) calibration and DCA as performed. One sentence in Methods pointing to this is sufficient. Optionally add a one-line STROBE applicability statement for the two public observational cohorts.

### F7 — References: compliant; one cosmetic punctuation defect (minor)
【Problem】 All 36 references are present, Vancouver-numbered by first citation (1–36, contiguous, no gaps), all are cited in text, no duplicates, all carry DOIs — a clean pass. One reference has double terminal punctuation.
【Evidence】 `Manuscript.docx` References: 36 entries, `refs as set = 36`, `cited-but-not-in-list = []`, `in-list-but-never-cited = []` (verified programmatically). Reference 16 reads: "… immunotherapy?." (title ends with "?" immediately followed by a period). All 36 entries contain a `doi:10.…` token.
【Why it matters】 Format pass. The "?." is a cosmetic Vancouver slip only and will not block submission, but it is trivially fixable and signals care.
【Specific fix】 Change reference 16 to "… immunotherapy?" (drop the trailing period after the question mark), or restyle as "… immunotherapy?" with the journal punctuation outside. Confirm NLM/Vancouver author-list style (≤6 authors then "et al.") is applied uniformly — currently acceptable.

### F8 — Cover letter: compliant (pass)
【Problem】 None material.
【Evidence】 `Cover_Letter.docx`: addresses "Dear BMC Medical Genomics Editorial Team"; "Rationale for BMC Medical Genomics" bullet set; explicit no-prior-publication / not-under-consideration statement ("The manuscript is original, has not been published elsewhere, and is not under consideration by another journal"); funding (none) and ethics summaries present; corresponding-author ORCID/email present.
【Why it matters】 Meets the venue's cover-letter expectations; no action required. One optional tightening: the letter asserts "the repository carries 32 audit assertions" — keep this only if the number is verifiable in the repo, otherwise soften to "a set of audit assertions."
【Specific fix】 No mandatory change. If desired, replace "32 audit assertions" with "reproducibility audit assertions" to avoid a verifiable-specific count in the letter.

### F9 — No MR residue / version string check: pass, with one explanatory non-v1.20.0 string (informational)
【Problem】 No Mendelian-randomisation residue remains in the derived docx; v1.20.0 is correctly carried. A single `v1.16.0` mention remains but is an intentional "built on" explanation, not stale.
【Evidence】 `Manuscript.docx`: "Mendelian" → 0; "mr_forest"/"mr_diag" → 0; "v1.20.0" → 3 occurrences; "v1.16.0" → 1 occurrence inside the Data-availability "built on top of it" clause. `manuscript.md` shows the same (v1.20.0 ×3, v1.16.0 ×1, no MR keywords).
【Why it matters】 The MR layer was cleanly removed; the v1.16.0 string is legitimate provenance context, not a stale version. No action required beyond the F4 commit-hash reconciliation.
【Specific fix】 None required. After F4, ensure the v1.16.0 "built-on" sentence references the reconciled commit hash.

---

## § Questions for the authors

1. **Drug shortlist vs glucocorticoids:** Please confirm the intended seven-agent shortlist is exactly IL-7, GM-CSF, IFN-γ, azithromycin, lenalidomide, thymosin α1, BCG, and that glucocorticoids are *only* a positive-control caveat (so the abstract can be corrected per F1). Which of the seven, if any, do you consider the primary translational lead?
2. **Figure mapping:** Will you rename the upload PNGs to the `S`-series (F3) or instead supply an explicit `FigN → caption` mapping table at upload? Please confirm `S3A/S3B` and `S6A/S6B/S6C` contents against `04_figures/` before submitting.
3. **Commit/version provenance:** What are the actual git commit hashes for tags `v1.16.0` and `v1.20.0`? Please reconcile `manuscript.md` / `Manuscript.docx` (`1212f7b`) with `SUBMISSION_MANIFEST.md` (`7704c9a`) (F4).
4. **Prediction-model reporting:** Are you willing to add a TRIPOD/CLIP-aligned short reporting note or flow diagram for the 30-gene signature (F6), given BMC does not mandate it but reviewers likely will ask?
5. **Article type:** Will you set the BMC system article type to "Research article" and remove/relabel the "methods-and-resources" self-description (F2)?
6. **Reproducibility of the hub result:** Given Limitation 9 (uncontrolled family-wise error across the selection chain), do you have any truly independent cohort (other than E-MTAB-4451, which shares the label-orientation training) that could serve as a second confirmation of the five hubs, even qualitatively?

---

## § What I actually checked (files read + format checks performed)

**Files read (allowed set only):**
- `05_reports/manuscript.md` (full).
- `07_submission_bmc_v1.20.0/Manuscript.docx` (full paragraph/style dump + programmatic scans).
- `07_submission_bmc_v1.20.0/Supporting_Information.docx` (headings + figure-caption list).
- `07_submission_bmc_v1.20.0/Cover_Letter.docx` (full).
- `07_submission_bmc_v1.20.0/SUBMISSION_MANIFEST.md`, `bmc_checklist.md`, `BMC_structured_abstract.md`.
- `04_figures/` directory listing (10 PNGs) and `07_submission_bmc_v1.20.0/Figures/` listing (Fig1–Fig10).
- (Cross-checked, not read as review content: `06_review/round19_v1.20.0/` is the output target only.)

**Format / reporting checks performed (programmatic, on the docx):**
1. Structured abstract: confirmed `Background:` / `Methods:` / `Results:` / `Conclusions:` all present with non-empty content.
2. Declarations: confirmed headings *Ethics approval and consent to participate*, *Consent for publication* ("Not applicable"), *Data availability*, *Code availability*, *Author contributions*, *Funding*, *Competing interests* all present; plus §2.11 AI disclosure.
3. Article-type / overclaim: scanned title + abstract for "discovery/novel/confirm/validate" framing; no overclaim found; flagged the non-standard "methods-and-resources" self-label.
4. References: extracted reference-list numbers and in-text `[n]` citations; verified 36 entries, contiguous 1–36, no duplicates, all cited, no orphan citations, all 36 carry DOIs; flagged ref-16 "?." .
5. Figures: extracted all `Fig. S#` tokens from docx (S1, S2, S3A, S3B, S6A, S6B, S6C, S7, S9, S10 = 10) and cross-checked against `04_figures/` PNG names and the `Figures/Fig1–Fig10` upload names; built the mapping table and identified the non-sequential multi-panel hazard.
6. Reporting standards: assessed STROBE/TRIPOD/CLIP/MICRoR coverage; identified TRIPOD gap for the signature and noted MICRoR strengths (§7 provenance, §2.11, Zenodo).
7. Derived-vs-source drift: confirmed docx = v1.20.0, no MR residue, 36 refs, 10 figures; detected commit-hash disagreement (`1212f7b` vs `7704c9a`) and source `manuscript.md` not carrying the structured abstract / BMC ethics heading.
8. Cover letter: confirmed editor address, BMC rationale, no-prior-publication declaration, funding/ethics summaries.

**Out of scope (not performed):** I did not re-run the analysis pipeline or verify the numeric values against `03_results/` CSVs (that is the audit-assertion domain, not the venue-format gate); I treated all reported numbers as author-asserted. I did not read any prior `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, other `A1–A3` reviews, or project memory.

---

## One-line verdict
**Minor revision** — format-compliant and in scope for BMC Medical Genomics; resolve the abstract shortlist error (F1), the figure-mapping hazard (F3), the commit-hash drift (F4), and the article-type wording (F2) before submission; TRIPOD note (F6) recommended.
