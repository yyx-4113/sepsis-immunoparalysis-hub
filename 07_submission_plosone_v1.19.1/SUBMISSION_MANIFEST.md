# Submission manifest — PLOS ONE

Manuscript version: **v1.19.1** (tag `v1.19.1`, built on commit `1212f7b` / tag v1.16.0).
Repository: https://github.com/yyx-4113/sepsis-immunoparalysis-hub
Zenodo DOI: 10.5281/zenodo.23042366 (public).

## File -> PLOS ONE (Editorial Manager) file type

| Local file | EM file type | Notes |
|---|---|---|
| Manuscript.docx | Main Document | Text + §7 provenance table + declarations + references (Vancouver) + figure captions |
| Supporting_Information.docx | Supporting Information | S01-S12 tables + figure-caption list |
| Cover_Letter.docx | Cover Letter | |
| Figures/Fig1.png ... Fig12.png | Figure | upload each separately; map to captions in Manuscript.docx |

## Do NOT upload
- 05_reports/REVIEW_round*.md (internal review logs)
- 02_scripts/, 03_results/ raw CSVs as-is (deposited in repo, not as SI)
- build_submission_plosone.py / verify_submission_plosone.py (build tooling)

## Metadata the form will ask for
- Title: as in Manuscript.docx (17 words).
- Article type: Original Research Article.
- Abstract: unstructured, 194 words (verified, no citations).
- Keywords: as listed under the abstract.
- References: 41, Vancouver/PLOS style, DOIs present, numbered in citation order.
- Tables: main provenance table in main doc; 12 supplementary in SI.
- Figures: 12, uploaded separately as PNG.
- Corresponding author: Yongxin Yang; ORCID 0009-0004-9698-6552; email 960856791@qq.com.
- Funding: none declared (state explicitly in form).
- Competing interests: declared in the manuscript.
- Data availability: GitHub (tag v1.19.1) + Zenodo DOI 10.5281/zenodo.23042366.

## Open items for the author (not fabricated)
1. Confirm the corresponding-author account name in EM uses the Latin script (given/family), not '永新 杨'.
2. Complete the PLOS ONE submission checklist in the online form (plosone_checklist.md provided).
3. Zenodo DOI 10.5281/zenodo.23042366 already minted and pasted into the Data availability statement.
4. Upload each FigN.png and map it to its manuscript caption (12 figures).
5. PLOS ONE requires a 'statements' block (included: ethics, data, code, author contributions, funding, competing interests, acknowledgements).

## Verification
- `python verify_submission_plosone.py` exits 0: numeric-token diff empty both ways, no Chinese text, no placeholders, mandatory strings (repo URL, ORCID, AI disclosure, Zenodo DOI) present, 41 references in Vancouver style, 12 figures copied.