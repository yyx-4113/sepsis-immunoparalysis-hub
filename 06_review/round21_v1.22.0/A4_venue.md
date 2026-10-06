# A4 — Venue fit & reporting-honesty audit (BMC Medical Genomics, Research article)

**Manuscript tag:** v1.22.0 · **Commit audited (submission pack):** 7704c9a (pack build); results pinned at 1212f7b (v1.16.0)
**Artefacts audited:** `Manuscript.docx`, `BMC_structured_abstract.md`, `Cover_Letter_BMC.md`, `SUBMISSION_MANIFEST.md`, `bmc_checklist.md`, `verify_submission_bmc.py`, `Figures/`.
**Status:** Treat-as-first-submission (no prior-round files consulted).

---

## Issue 1 — Title word count mismatch between manifest and the verbatim title

【Problem】`SUBMISSION_MANIFEST.md` line 23 states the title is **"(18 words)"**, but the verbatim title actually contains **24 whitespace tokens** by standard academic word-counting.

【Evidence】
- Title (`manuscript.md` line 1; identical in `Cover_Letter_BMC.md` line 3; carried verbatim into `Manuscript.docx`, confirmed by the pack's own title-diff check):
  *"A reproducible, fully auditable pipeline confirms within-cohort the MARS Mars1 immunoparalysis program and delivers an honest external validation of a 30-gene sepsis prognostic signature"*
- Token count: A(1) reproducible(2) fully(3) auditable(4) pipeline(5) confirms(6) within-cohort(7) the(8) MARS(9) Mars1(10) immunoparalysis(11) program(12) and(13) delivers(14) an(15) honest(16) external(17) validation(18) of(19) a(20) 30-gene(21) sepsis(22) prognostic(23) signature(24) = **24 words**.
- `SUBMISSION_MANIFEST.md` line 23: `Title: as in Manuscript.docx (18 words).`

【Why it matters】The submission-form "title word count" field is metadata an editor may glance at; an under-count (18 vs 24) is a small but real inconsistency that, if the form is auto-prefilled from the manifest, propagates a wrong value. Low acceptance risk, but it is a factual error that should be corrected before submission.

【Specific fix】Update the manifest to the standard count (24 words):
```
- Title: as in Manuscript.docx (24 words).
```
If the journal's form instead asks for *content* words only, note that explicitly; otherwise use 24.

---

## Issue 2 — Figure filename sequence is non-contiguous; manifest phrasing implies a contiguous S1–S10 set

【Problem】The manifest line 14 writes `Figures/Fig_S1.png ... Fig_S10.png`, implying a contiguous S1–S10 series. The actual 10 uploaded PNGs are **S1, S2, S3A, S3B, S6A, S6B, S6C, S7, S9, S10** — there is no `Fig_S4.png`, `Fig_S5.png`, or `Fig_S8.png`. This is *not* an error in the manuscript (its §8 figure index also lists exactly S1, S2, S3A/B, S6A/B/C, S7, S9, S10), but the manifest's compressed notation could mislead an editor expecting a gapless sequence.

【Evidence】
- `Figures/` directory contents: `Fig_S1.png, Fig_S2.png, Fig_S3A.png, Fig_S3B.png, Fig_S6A.png, Fig_S6B.png, Fig_S6C.png, Fig_S7.png, Fig_S9.png, Fig_S10.png` (10 files, all supplementary-style `S`-prefixed — no `Fig1`/`Fig10` style).
- `manuscript.md` §8 line 215: *"Fig. S1 (Mars1 28-d ROC), S2 (score vs endotype), S3A/B (hub genes; eigengene–trait correlation), S6A/B (CV and training ROC), S6C (decision-curve analysis), S7 (cellular context), S9 (external-cohort ROC), S10 (L1000 rescuers)"*.
- In-text caption labels are all supplementary-style: `Fig. S1` (line 96), `Fig. S2` (98), `Fig. S3A/B` (101), `Fig. S6` (104), `Fig. S7` (112), `Fig. S9` (109), `Fig. S10` (139). No dangling `Fig. S4/S5/S8` references exist; no `Fig1`/`Fig10` bare references found.

【Why it matters】Filename-vs-caption consistency is the key check and it **passes**: every uploaded `Fig_Sn` maps to a real caption, and all labels use the `S` supplementary prefix required by BMC. The only risk is an editor reading the manifest's `…Fig_S10.png` shorthand as a promise of a gapless S1–S10 set and flagging "missing S4/S5/S8." This is cosmetic, not a hard fail.

【Specific fix】Either leave as-is (manuscript is self-consistent) or make the manifest explicit:
```
| Figures/Fig_S1.png, Fig_S2.png, Fig_S3A.png, Fig_S3B.png, Fig_S6A.png, Fig_S6B.png, Fig_S6C.png, Fig_S7.png, Fig_S9.png, Fig_S10.png | Supplementary Figure | 10 supplementary figures (non-contiguous numbering S1,S2,S3A/B,S6A/B/C,S7,S9,S10, matching manuscript §8) |
```

---

## Issue 3 — (Confirmed clean) Cover-letter vs manuscript consistency on title and "prioritised" claim

【Problem】None — both checks pass.

【Evidence】
- **Title verbatim:** `manuscript.md` line 1 and `Cover_Letter_BMC.md` line 3 are character-identical (the 24-word title above).
- **No "prioritised" overclaim:** `Cover_Letter_BMC.md` line 9 states *"…none is prioritised by significance."* It frames the seven agents as *"hypothesis-generating repositioning candidates"* — matching `manuscript.md` abstract line 14 (*"annotated as hypothesis-generating repositioning candidates rather than prioritised by significance"*) and the structured abstract (`BMC_structured_abstract.md` line 7, same wording). The cover letter does **not** claim the 7 drugs are prioritised.

【Why it matters】This is the exact wording the journal scrutinises for over-claimed drug-repositioning results; the cover letter is correctly aligned with the (appropriately hedged) manuscript.

【Specific fix】None required.

---

## Issue 4 — (Confirmed clean) MR-removal disclosure present in cover letter

【Problem】None.

【Evidence】`Cover_Letter_BMC.md` line 15: *"An earlier draft (≤ v1.19) included a two-sample Mendelian-randomisation layer; it was removed in v1.20.0 because it did not satisfy the study's three-tier positive-anchor design and is not part of the reported contribution."* This is the required one-line disclosure.

【Why it matters】Transparency about a removed analytical layer is a reporting-honesty requirement; the disclosure is present, correctly dated (≤v1.19 → removed v1.20.0), and matches the manifest's "MR layer removed in v1.20.0" note.

【Specific fix】None required.

---

## Issue 5 — (Confirmed clean) BMC declarations carried in Manuscript.docx

【Problem】None found.

【Evidence】Inspection of the built `Manuscript.docx` declarations block shows all required BMC elements present:
- Ethics approval and consent to participate (`manuscript.md` line 227 "Ethics statement").
- **Consent for publication** — present in the DOCX (text "Consent for publication" found; `bmc_checklist.md` line 12 records it as "Not applicable", appropriate for a single-author computational re-analysis of de-identified public cohorts).
- Data availability (line 219), Code availability (223), Competing interests (236, "none"), Funding (233, "none"), Author contributions (230).
- Generative-AI disclosure §2.11 (`manuscript.md` line 60–61) — present in DOCX (string "generative" / "§2.11" found).

【Why it matters】All mandatory BMC declarations are satisfied; no acceptance blocker.

【Specific fix】None required. (Author should still tick the corresponding boxes in the online submission form, per manifest "Open items".)

---

## Issue 6 — Article-type fit: Research article vs self-described computational-biology / methods-and-resources

【Problem】Defensible as **Research article** — recommend keeping it, with a minor framing guard.

【Evidence】
- `manuscript.md` line 8 explicitly self-describes as *"computational-biology / methods-and-resources study"* yet is submitted as **Research article**.
- However, the work is **not** a pure methods/tools paper: it delivers a genuine, independent-cohort + independent-platform **external validation** (E-MTAB-4451, n=106, 52 deaths; locked-L1 AUC 0.585, equal-weight AUC 0.638) of a 30-gene signature, plus within-cohort confirmation of an established biology and an experimental blueprint. The title foregrounds *"a reproducible, fully auditable pipeline … and … an honest external validation of a 30-gene sepsis prognostic signature"* — i.e., validation of a biological result, which is squarely Research-article substance.
- `bmc_checklist.md` line 4–5 marks it original computational-biology research within scope; BMC Medical Genomics routinely publishes computational/transcriptomic validation Research articles.

【Why it matters】A methods-only paper would better fit BMC's "Software"/methodology track, but here the contribution includes real external validation of a prognostic signature, justifying Research article. The only risk is an editor reacting to the "methods-and-resources" self-label; the cover letter already mitigates this by foregrounding the validation contribution.

【Specific fix】No reclassification needed. Optional tightening of the self-description in line 8 to *"computational-biology study with a methods-and-resources component"* to reduce any appearance of self-demotion. Keep as Research article.

---

## Issue 7 — (Confirmed clean) No format hard-fail

【Problem】None found.

【Evidence】
- The bundled submission verifier exits **0** ("ALL CHECKS PASSED") — it asserts: no Chinese (CJK) text in the DOCX, no placeholder text, mandatory strings present (repo URL, ORCID, Zenodo DOI, AI-disclosure §2.11), 40 Vancouver references, 10 figures copied, no MR-residue keywords.
- Manuscript markdown renders cleanly; no broken code fences or stray placeholder tokens observed in the audited body.
- `Manuscript.docx` is a valid OOXML package; declarations and abstract render as structured (Background/Methods/Results/Conclusions) per `BMC_structured_abstract.md`.

【Why it matters】Format hard-fails (CJK in DOCX, placeholders, broken markdown) are the most common desk-reject triggers; none are present.

【Specific fix】None required.

---

## Issue 8 — (Confirmed clean) Bundled verifier exits 0

【Problem】None.

【Evidence】Running the pack's `verify_submission_bmc.py` with the managed Python interpreter returned:
```
=== BMC submission verification ===
docx chars=75472 refs=40 figs=10
ALL CHECKS PASSED
```
Exit code **0**. This confirms: 40 references, 10 figures, no MR residue, and the correct version string **v1.22.0** (the script's numeric-token/version checks passed).

【Why it matters】This is the objective gate the task asked me to confirm; it passes on every dimension (40 refs, 10 figs, no MR residue, v1.22.0).

【Specific fix】None required.

---

## § Stands up (what is already correct — evidence-based)

1. **Title is verbatim-consistent** across `manuscript.md` line 1, `Cover_Letter_BMC.md` line 3, and `Manuscript.docx` (confirmed by the pack's own title-diff gate). No title drift between cover letter and manuscript.
2. **Drug-repositioning claims are honestly hedged everywhere** — cover letter ("none is prioritised by significance"), abstract (`manuscript.md` line 14), and structured abstract (`BMC_structured_abstract.md` line 7) all say *hypothesis-generating / not prioritised by significance*, and the LINCS glucocorticoid caveat (prednisone 3.2nd percentile) is carried through. No overclaim.
3. **All mandatory BMC declarations are present in the DOCX** (ethics+consent, consent for publication, data, code, competing interests, funding, author contributions, §2.11 generative-AI), and the bundled verifier exits 0 with 40 refs / 10 figs / no MR residue / v1.22.0 — a clean, submission-ready gate.
4. **MR-removal transparency** is disclosed in both the cover letter (line 15) and the manifest, and the removed MR figures (`mr_forest.png`, `mr_diag.png`) are explicitly excluded from upload.

---

## § Questions for the authors

1. **Title word count:** The manifest says 18 words but the verbatim title is 24 words by standard counting. Did you intend a *content-word* count (which yields 18), or should the manifest be corrected to 24? (See Issue 1.)
2. **Consent for publication:** The DOCX carries "Consent for publication: Not applicable" — please confirm this is the intended wording for a single-author computational re-analysis with no identifiable individuals, so the online-form checkbox matches.
3. **Figure numbering:** Are you comfortable with the non-contiguous supplementary numbering (S1, S2, S3A/B, S6A/B/C, S7, S9, S10, with S4/S5/S8 absent)? BMC permits gaps, but confirm no figure was accidentally dropped during the S3/S6 split.
4. **Article type:** Given the self-label "methods-and-resources," do you want to keep **Research article** (recommended — genuine external validation is present) or consider BMC's methodology track? (See Issue 6.)

---

## § What I actually checked

- Read `manuscript.md` (full), `Cover_Letter_BMC.md`, `SUBMISSION_MANIFEST.md`, `BMC_structured_abstract.md`, `bmc_checklist.md`.
- Listed and verified `07_submission_bmc_v1.21.0/Figures/` (10 PNGs, supplementary `S`-style names, mapped to captions).
- Verified the built `Manuscript.docx` declarations block for all BMC-required elements (including "Consent for publication" and §2.11 generative-AI) by inspecting the document XML text.
- Grepped `manuscript.md` for figure-label style (`Fig. S1`…`Fig. S10` vs `Fig1`/`Fig10`) and confirmed no bare/`Fig1` references and no dangling S4/S5/S8 captions.
- Ran the pack's `verify_submission_bmc.py` with the managed Python 3.13 interpreter: exit 0, "ALL CHECKS PASSED", 40 refs, 10 figs, no MR residue, v1.22.0 confirmed.
- Checked cover-letter vs manuscript title verbatim equality and the "prioritised" / "hypothesis-generating" wording alignment; confirmed the MR-removal one-line disclosure in the cover letter.
- Did **not** consult any `06_review/` prior-round file, `REVIEW_*`/`RESPONSE_*`/`REVISION_*` docs, or any other reviewer's output (independence discipline upheld).

---

**A4 verdict:** Submission is **venue-fit and reporting-honest** with two minor metadata corrections to make before hitting "submit": (a) fix the title word count in `SUBMISSION_MANIFEST.md` from 18 → 24 (Issue 1); (b) optionally make the figure-list notation explicit about non-contiguous numbering (Issue 2). No hard-fail, no overclaim, no missing declaration, verifier green. Recommend **accept for technical checks / desk review**.
