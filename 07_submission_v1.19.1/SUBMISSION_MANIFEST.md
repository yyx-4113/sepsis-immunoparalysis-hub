# Submission manifest — Scientific Reports (Nature Portfolio)

Manuscript version: **v1.19.1** (tag `v1.19.1`, built on commit `1212f7b` / tag v1.16.0).
Repository: https://github.com/yyx-4113/sepsis-immunoparalysis-hub

## File -> submission-system file type

| Local file | Snapp file type | Notes |
|---|---|---|
| Manuscript.docx | Main Document | Text + Tables 1-5 + §7 provenance table + references + declarations |
| Supporting_Information.docx | Supplementary Information | S01-S12 tables + 12 supplementary figures |
| Cover_Letter.docx | Cover Letter | |
| Reporting_Summary.docx | Reporting Summary (Life Sciences) | DRAFT; finalise in journal form |
| Figures/Figure_S1.png ... Figure_S12.png | Figure | map each to its caption in the SI |

## Do NOT upload
- 05_reports/REVIEW_round*.md (internal review logs)
- 02_scripts/, 03_results/ raw CSVs as-is (they are deposited in the repo, not as SI)
- build_submission.py / verify_submission.py (build tooling)

## Metadata the form will ask for
- Title: as in Manuscript.docx (<=20 words per Sci Rep; currently 17).
- Article type: Article (research).
- Abstract: unstructured, 194 words (verified).
- Keywords: as listed under the abstract.
- References: 41, Nature style, DOIs present.
- Tables: 5 main (+ §7 provenance) in the main doc; 12 supplementary in the SI.
- Figures: 12 supplementary (S1-S12) as separate PNG files.
- Corresponding author: Yongxin Yang; ORCID 0009-0004-9698-6552; email 960856791@qq.com.
- Funding: [AUTHOR: state explicitly — currently 'none declared' in the manuscript].
- Competing interests: declared in the manuscript.
- Data availability URL: https://github.com/yyx-4113/sepsis-immunoparalysis-hub (tag v1.19.1).

## Snapp / EM — "Data availability" step (mandatory for this journal)
Scientific Reports (Nature Portfolio) asks, in the submission system, **"Did you use or generate research data?"** and then a **Data availability statement** text box whose content **replaces the in-manuscript statement and is the one that will be published**. Prepare as follows (this is a re-analysis of public data, so it is NOT "no data"):
1. **"Did you use or generate research data?" → answer YES (是的).** Do NOT pick No — the No wording ("this manuscript does not report data generation or analysis") contradicts a re-analysis of public cohorts and will trigger a desk query.
2. For the data-availability options, tick: **"The datasets generated and/or analysed during the current study are available in a public repository."** — Repository name: **GitHub**; URL: **https://github.com/yyx-4113/sepsis-immunoparalysis-hub (tag v1.19.1)**.
3. Paste the verbatim content of **`Data_Availability_Statement.txt`** (same folder) into the **Data availability statement** text box. This is the published version; it already matches the in-manuscript §"Data availability" and the Reporting Summary.
4. The statement now includes the minted Zenodo DOI **10.5281/zenodo.23042366** — open item 3 below is now closed.

## Open items for the author (not fabricated)
1. Confirm the corresponding-author account name in Snapp uses the Latin script (given/family), not '永新 杨'.
2. Complete the Nature Life Sciences Reporting Summary in the journal's online form (draft provided).
3. [DONE] Zenodo DOI 10.5281/zenodo.23042366 minted and pasted into the Data availability statement.
4. Upload each Figure_Sx.png and map it to its SI caption.
5. Re-check the Funding statement wording before final submit.

## Verification
- `python verify_submission.py` exits 0: numeric-token diff empty both ways, no Chinese text, no placeholders, mandatory strings (repo URL, ORCID, AI disclosure) present, expected table counts, 12 figures embedded in the SI.