# A4 — Venue fit & reporting-honesty audit (BMC Medical Genomics)

**Reviewer role:** Journal editor + reporting-standard auditor, independent peer-review panel.
**Manuscript:** "A reproducible pipeline recapitulates the MARS Mars1 immunoparalysis program within-cohort and externally evaluates a 30-gene sepsis prognostic signature" (single author, v1.21.0).
**Article type claimed:** Research article.
**Artefacts audited:** `05_reports/manuscript.md`, `07_submission_bmc_v1.21.0/Manuscript.docx`, `BMC_structured_abstract.md`, `Cover_Letter_BMC.md`, `SUBMISSION_MANIFEST.md`, `bmc_checklist.md`, `verify_submission_bmc.py`, `Figures/Fig1..Fig10.png`.
**Independence note:** Treated as a first submission; no prior-round review files, author verification statements, or co-reviewer files were read.

---

## Verdict (summary)

The submission pack is **technically sound and largely honest** — the built `Manuscript.docx` passes its own self-check, carries a compliant structured abstract, complete BMC declarations, and an unusually transparent, de-prioritised reporting posture in the body. The decisive problems are **external to the manuscript body**: the **cover letter contradicts the manuscript on two material points** (title wording; "prioritisation" of the drug candidates), the **title headlines the weakest contribution** (a near-replication) while burying the genuine one (an auditable pipeline + an honest cross-platform external-validation framework), and the **10 figures are labelled as supplementary ("Fig. S1"…) while being uploaded as main figures (`Fig1.png`…)**. None of these are fatal, but the cover-letter contradictions must be reconciled before the editor reads them as spin.

---

## Issues

### Issue 1 — Cover letter title contradicts the manuscript title (title wording + dropped qualifier)
【Problem】 The cover letter and the manuscript carry different titles.
【Evidence】
- Manuscript title (built `Manuscript.docx` para [0]; `manuscript.md:1`): "…**recapitulates** the MARS Mars1 immunoparalysis program **within-cohort** and externally evaluates…"
- Cover letter (`Cover_Letter_BMC.md:3`): "…**confirms** the MARS Mars1 immunoparalysis program and externally evaluates…" — "recapitulates"→"confirms", and the **"within-cohort"** qualifier is silently dropped.
【Why it matters】 For acceptance: an editor/cover-desk compares the cover letter title against the manuscript title and the online-submission metadata; a mismatch triggers a "title不一致" query and undermines the credibility of the rest of the cover letter. Dropping "within-cohort" also changes the claim from a self-contained replication to an apparent cross-cohort confirmation, which the data do not support (the "confirms" effect is within GSE65682 only; external validation is of the *signature*, not of the hub recapitulation).
【Specific fix】 Make the cover letter title identical to the manuscript title, verbatim:
> "A reproducible pipeline recapitulates the MARS Mars1 immunoparalysis program within-cohort and externally evaluates a 30-gene sepsis prognostic signature"

### Issue 2 — Cover letter over-claims drug "prioritisation" that the manuscript explicitly denies
【Problem】 The cover letter says the seven agents are *prioritised*, while the manuscript repeatedly states they are *hypothesis-generating and not prioritised by significance*.
【Evidence】
- Cover letter (`Cover_Letter_BMC.md:9`): "we **prioritise** seven immune-modulating agents for repurposing through an explicit positive-control gate."
- Manuscript abstract (`Manuscript.docx` para [10]; `manuscript.md:14`): "Seven immune-modulating agents were annotated as hypothesis-generating repositioning candidates **rather than prioritised by significance**".
- Manuscript Conclusion (`manuscript.md:178`): candidates are "**hypothesis-generating** axis-specific immune-restorative candidates".
- Manuscript §3.9 (`manuscript.md:137`): the LINCS screen is "**descriptive only** … not counted as supportive evidence", because the immunosuppressant prednisone ranks in the 3.2nd percentile — i.e. the positive-control gate *fails* to discriminate, it does not *support* prioritisation.
【Why it matters】 For acceptance: this is the single most damaging reporting-honesty defect. The manuscript's strongest virtue is its disciplined de-prioritisation; the cover letter inverts it and tells the editor the opposite of what the body proves. A reviewer who reads both will read the cover letter as spin, and may distrust the rest of the (honest) framing.
【Specific fix】 Replace `Cover_Letter_BMC.md:9` with language matching the manuscript:
> "We annotate seven immune-modulating agents as hypothesis-generating repositioning candidates; their curated immune-response concordance lies at or below the study's own 0.84 background and the LINCS L1000 positive-control gate was non-discriminating (the immunosuppressant prednisone ranked in the 3.2nd percentile), so none is prioritised by significance."

### Issue 3 — Title headlines the weakest contribution; the real, stable contribution is buried
【Problem】 The title leads with "recapitulates the MARS Mars1…program" (a near-replication of established biology — the lowest-novelty element) rather than the manuscript's actual, defensible contribution (a reproducible, fully auditable pipeline + an honest external-validation framework that is independent in cohort and platform but not in label).
【Evidence】
- Title (`manuscript.md:1`; `Manuscript.docx` [0]) foregrounds recapitulation.
- Article-type line (`manuscript.md:8`; `Manuscript.docx` [5]) self-describes as "a computational-biology / methods-and-resources study" and states the five hubs "recapitulate the established MARS Mars1 antigen-presentation program (a **near-replication**)".
- Discussion (`manuscript.md:147`): "The contribution of this study is therefore methodological and infrastructural rather than biological…" — the body is honest, but the title buries this.
- The honest, stable contribution is visible in the abstract Conclusion (`Manuscript.docx` [11]) and §7 provenance table (`manuscript.md:182-208`): every number traces to a deposited file, MR layer removed, external validation run on a locked model.
【Why it matters】 For acceptance: BMC Medical Genomics "Research article" implies a novel finding. Here the biology is established; the novelty is method/infrastructure + an unusually candid external-validation framework (AUC 0.585 locked-L1, explicitly flagged as including 0.5). Headlining the near-replication invites a reviewer to say "this is a replication, not a research article" and reject on article-type grounds, even though the infrastructure contribution is legitimate.
【Specific fix】 Either (a) reframe the title to foreground the pipeline + honest external-validation framework, e.g.
> "A reproducible, fully auditable pipeline and an honest cross-platform external validation of a 30-gene sepsis immunoparalysis signature"
or (b) keep "Research article" but add a one-sentence novelty statement in the abstract Background/Conclusions naming the *methodological* contribution explicitly (auditability + locked-model external validation), not the recapitulation. Pick (a) or (b) — do not leave the title as-is.

### Issue 4 — Figure labelling mismatch: in-text/captions say "Fig. S1" but files are `Fig1.png`…`Fig10.png`
【Problem】 The 10 figures are cited and captioned with supplementary-style labels ("Fig. S1", "Fig. S2", "Fig. S3A/B", "Fig. S6A/B/C", "Fig. S7", "Fig. S9", "Fig. S10") yet are uploaded as **main** figures named `Fig1.png`…`Fig10.png`.
【Evidence】
- In-text citations (`Manuscript.docx` extracted): `['Fig. S1','Fig. S2','Fig. S3A','Fig. S3B','Fig. S6','Fig. S6A','Fig. S6B','Fig. S6C','Fig. S7','Fig. S9','Fig. S10']`.
- Caption block (`Manuscript.docx` [153-162]): "Fig. S1. …", "Fig. S2. …", etc. (10 captions, S-style).
- Uploaded files (`07_submission_bmc_v1.21.0/Figures/`): `Fig1.png`…`Fig10.png` (10 files, no "S").
- Manifest (`SUBMISSION_MANIFEST.md:14,40`) lists "Figures/Fig1.png … Fig10.png" as main "Figure" file type and flags "Upload each FigN.png and map it to its manuscript caption (10 figures)" as an open item.
【Why it matters】 For acceptance: an editor/reviewer reading "Fig. S1" in the text but seeing a file named `Fig1.png` cannot map them without the author's side-table; the "S" prefix also conventionally denotes *supplementary* material, conflicting with the main-figure upload type. This is a guaranteed production query and risks the wrong figure being linked to a caption.
【Specific fix】 Choose one consistent scheme: (i) if they are main figures, renumber captions and in-text citations to "Fig. 1"…"Fig. 10" (and keep `Fig1.png`…`Fig10.png`); or (ii) if they are supplementary, upload them as supplementary material and keep the "Fig. S1"… labels. Do not ship the current mixed state. The 10 captions already exist and cover all 10 files, so only the labels need unifying.

### Issue 5 — Submission metadata says title is "17 words"; the actual title is 18 words
【Problem】 Minor factual mismatch between declared and actual title length.
【Evidence】
- `SUBMISSION_MANIFEST.md:23`: "Title: as in Manuscript.docx (**17 words**)."
- Actual title (`Manuscript.docx` [0]) word-split count = **18** ("A reproducible pipeline recapitulates the MARS Mars1 immunoparalysis program within-cohort and externally evaluates a 30-gene sepsis prognostic signature").
【Why it matters】 For acceptance: trivial on its own, but it is the kind of metadata discrepancy that, alongside Issues 1–2, suggests the cover/metadata were not proof-read against the manuscript. Fix while correcting Issue 1.
【Specific fix】 Change the manifest wording to "18 words" (or delete the word count, since BMC does not require it).

### Issue 6 — MR layer removal is not disclosed to the editor
【Problem】 The submission silently dropped a whole analytic layer (two-sample MR) between v1.19 and v1.21; the manuscript and cover letter do not mention it, so an editor has no visibility.
【Evidence】
- `SUBMISSION_MANIFEST.md:3`: "built on commit `7704c9a` (v1.20.0, **MR layer removed**)".
- Repo root contains `remove_mr_layer.py` and `remove_mr_discussion.py` (build-tooling present); `verify_submission_bmc.py:53-57,117-121` enforces **no MR residue** and passes.
- Neither `manuscript.md` nor `Cover_Letter_BMC.md` states that a prior version contained an MR layer that was removed.
【Why it matters】 For acceptance: removing an entire analytic module between versions can look like post-hoc selective reporting if discovered later (e.g. via the preprint/repo history or the retained scripts). Voluntary disclosure protects the author and the editor. The removal itself is appropriate (the body is internally consistent without MR), but the *transparency* gap should be closed.
【Specific fix】 Add one sentence to the cover letter (or a Methods note): "An earlier draft (≤v1.19) included a two-sample Mendelian-randomisation layer; it was removed in v1.20.0 because it did not satisfy the study's three-tier positive-anchor design and is not part of the reported contribution." This is a disclosure only, not a request to re-add the analysis.

### Issue 7 (article-type fit) — "Research article" is defensible but the self-description points to Methodology/Database
【Problem】 The manuscript self-identifies as "computational-biology / methods-and-resources" yet is submitted as "Research article".
【Evidence】
- `manuscript.md:8` / `Manuscript.docx` [5]: "This is a computational-biology / methods-and-resources study".
- The genuine outputs are (i) a reproducible pipeline, (ii) a locked-model external-validation framework, (iii) a deposited, versioned resource (GitHub tag v1.21.0 + Zenodo DOI 10.5281/zenodo.23042366, `manuscript.md:221`), (iv) an experimental blueprint (S11).
【Why it matters】 For acceptance: BMC Medical Genomics also offers "Methodology" and "Database" article types that fit a methods-and-resources contribution more naturally than "Research article", which presupposes a novel biological finding. Keeping "Research article" is acceptable *if* Issue 3 is fixed (title foregrounds the methodological contribution); otherwise a reviewer may route it to "Methodology".
【Specific fix】 Decide deliberately: keep "Research article" + apply Issue 3 fix, **or** reclassify as "Methodology" (or "Database") and adjust the cover-letter rationale accordingly. State the choice explicitly in the cover letter.

---

## § Stands up (what is already compliant — with evidence)

1. **Structured abstract is complete and honest, and matches the body.** `Manuscript.docx` [8-11] carries all four BMC sections (Background / Methods / Results / Conclusions) with real content; Results report AUC 0.585 (locked-L1, primary), 0.638 (equal-weight sensitivity), 0.659 (within-cohort CV) — exactly as in the body (`manuscript.md:104,107`). The abstract does **not** over-claim; it repeats the body's de-prioritisation ("rather than prioritised by significance").
2. **All BMC declarations are present and non-empty, including the two easy-to-miss ones.** `Manuscript.docx` [99-111]: Ethics approval and consent to participate [100-101], Consent for publication [110-111] ("Not applicable…"), Data availability [95-96], Code availability [97-98], Author contributions [102-103], Funding [104-105], Competing interests [106-107], plus the Generative-AI disclosure §2.11 (`manuscript.md:60-61`; `Manuscript.docx` [36]). Note: "Consent for publication" was absent from the `manuscript.md` source and was correctly injected by the build — good catch by the build pipeline.
3. **The self-check passes and the pack is internally consistent on the hard gates.** `verify_submission_bmc.py` exits 0: no CJK characters, no unfilled placeholders, 38 Vancouver references, 10 figure PNGs, no MR residue, and all key numeric tokens (802/0.585/0.638/0.659/0.469/0.696/0.529/0.619/106/52/30/FIS1/1.26…) preserved. The §7 number-provenance table (`manuscript.md:182-208`) makes every reported figure traceable to a deposited CSV — a model of auditability.
4. **The body is honestly scoped about no-new-primary-data and the modest external AUC.** `manuscript.md:221` ("used and re-analyzed public research data… no new primary data were generated") and `manuscript.md:157` (external AUC is "real but modest", locked-L1 0.585 "whose interval includes 0.5"). The prednisone caveat (`manuscript.md:137`) is a genuine, non-spinning limitation. This is the posture a methods/validation article should have.

---

## § Questions for the authors

1. Per Issue 7: do you intend "Research article" or should this be reclassified as "Methodology" / "Database"? The body reads as methods-and-resources.
2. Per Issue 4: are the 10 figures **main** figures or **supplementary**? The labels say "S", the upload type says "main" — which is correct?
3. Per Issue 6: will you add the one-line MR-layer-removal disclosure to the cover letter so the editor has visibility into the version history?
4. Per `SUBMISSION_MANIFEST.md:37` and `bmc_checklist.md:29`: confirm the corresponding-author name in the submission system uses Latin script (not "永新 杨"), since the manuscript/cover letter mix Latin and CJK author representation.

---

## § What I actually checked

- Read in full: `05_reports/manuscript.md` (281 lines), `07_submission_bmc_v1.21.0/BMC_structured_abstract.md`, `Cover_Letter_BMC.md`, `SUBMISSION_MANIFEST.md`, `bmc_checklist.md`.
- Ran `07_submission_bmc_v1.21.0/verify_submission_bmc.py` → **ALL CHECKS PASSED** (docx chars=71987, refs=38, figs=10, exit 0).
- Extracted `Manuscript.docx` text via python-docx and verified: structured-abstract four sections [8-11]; declaration headings and non-empty content [95-111]; figure caption block [153-162]; title text [0] and word count (18); in-text figure-citation style ("Fig. S1"…); reference count (38).
- Listed `07_submission_bmc_v1.21.0/Figures/` → 10 PNGs (`Fig1.png`…`Fig10.png`).
- Did **not** read any file under `06_review/` (prior rounds), `REVIEW_*.md`, `RESPONSE_*.md`, author verification statements, or the other reviewers' files in this `round20_v1.21.0/` directory.

---

## Priority for the editor

- **Must fix before acceptance:** Issue 2 (cover-letter "prioritisation" contradiction) and Issue 1 (title mismatch) — both are editor-facing and read as spin.
- **Should fix:** Issue 3 (title buries the real contribution) + Issue 7 (article-type decision); Issue 4 (figure label scheme).
- **Nice to fix:** Issue 5 (title word count), Issue 6 (MR-removal disclosure).
- **No action needed:** structured abstract, declarations, self-check — these stand up.
