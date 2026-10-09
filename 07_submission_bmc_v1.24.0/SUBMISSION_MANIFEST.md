# Submission manifest — BMC Medical Genomics

Manuscript version: **v1.24.0** (tag `v1.24.0`; built on commit `7704c9a` (v1.20.0, MR layer removed), which sits above the results-pinned commit `1212f7b` (v1.16.0)).
Repository: https://github.com/yyx-4113/sepsis-immunoparalysis-hub
Zenodo DOI: 10.5281/zenodo.23042366 (public).

## File -> BMC submission-system file type

| Local file | System file type | Notes |
|---|---|---|
| Manuscript.docx | Main Document / Manuscript | Structured abstract + §1-§8 body + Declarations + 40 Vancouver refs + figure captions |
| Supporting_Information.docx | Supplementary Material | S01,S02,S04,S05,S06,S07,S08,S08b,S09,S11 tables + figure-caption list |
| Cover_Letter.docx | Cover Letter | |
| Figures/Fig_S1.png, Fig_S2.png, Fig_S3A.png, Fig_S3B.png, Fig_S6A.png, Fig_S6B.png, Fig_S6C.png, Fig_S7.png, Fig_S9.png, Fig_S10.png | Supplementary Figure | 10 supplementary figures (non-contiguous numbering S1,S2,S3A/B,S6A/B/C,S7,S9,S10, matching manuscript §8); upload each separately and map to its caption in Manuscript.docx |

## Do NOT upload
- 05_reports/REVIEW_round*.md (internal review logs)
- 02_scripts/, 03_results/ raw CSVs as-is (deposited in repo, not as SI)
- build_submission_bmc.py / verify_submission_bmc.py (build tooling)
- the two MR figures (mr_forest.png, mr_diag.png) — MR layer removed in v1.20.0

## Metadata the form will ask for
- Title: as in Manuscript.docx (24 words; standard whitespace-token count).
- Article type: Research article.
- Abstract: STRUCTURED (Background / Methods / Results / Conclusions).
- Keywords: as listed under the abstract.
- References: 40, Vancouver style, DOIs present, numbered in citation order.
- Tables: main provenance table in main doc (§7); 10 supplementary in SI.
- Figures: 10, uploaded separately as PNG.
- Corresponding author: Yongxin Yang; ORCID 0009-0004-9698-6552; email 960856791@qq.com.
- Funding: none declared (state explicitly in form).
- Competing interests: declared in the manuscript (none).
- Data availability: GitHub (tag v1.24.0) + Zenodo DOI 10.5281/zenodo.23042366.
- Declarations: Ethics approval and consent to participate; Consent for publication; Data availability; Code availability; Competing interests; Funding; Author contributions.

## Open items for the author (not fabricated)
1. Confirm the corresponding-author account name in the submission system uses the Latin script (given/family), not '永新 杨'.
2. Complete the BMC declarations in the online form (the manuscript carries the full text; the form asks for checkboxes).
3. Zenodo DOI 10.5281/zenodo.23042366 already minted and pasted into Data availability.
4. Upload each Fig_Sn.png (S1, S2, S3A/B, S6A/B/C, S7, S9, S10; non-contiguous, S4/S5/S8 absent) and map it to its manuscript caption (10 figures).
5. BMC requires a 'Declarations' section (included: ethics+consent, consent for publication, data, code, competing interests, funding, author contributions).

## Verification
- `python verify_submission_bmc.py` exits 0: numeric-token diff empty both ways, no Chinese text, no placeholders, mandatory strings (repo URL, ORCID, Zenodo DOI, AI disclosure §2.11) present, 40 references in Vancouver style, 10 figures copied, no MR-residue keywords.