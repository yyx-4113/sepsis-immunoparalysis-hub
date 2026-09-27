# A4 — Venue / Compliance Review (Scientific Reports)

**Reviewer role:** Venue & reporting-standard auditor, acting as a *Scientific Reports* (Nature Portfolio) editor for an independent peer-review panel.
**Manuscript version reviewed:** v1.11.0 (`manuscript.md`) + `cover_letter.md`.
**Independence statement:** Treated as a first submission. I read only `manuscript.md` and `cover_letter.md` under `05_reports/`; I did not consult any `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `review_r*/`, checklists, memory, or other reviewers' outputs.

---

## Findings

### Finding 1 — Reference [32] is incomplete (missing volume, pages, and DOI) — HARD FAIL
【Problem】 Reference [32] (Giamarellos-Bourboulis et al., JAMA 2025) is recorded without a journal volume, page range, or DOI. Nature style requires `Journal **volume**, pages (year)`; a bare `*JAMA* (2025)` is non-compliant and would be sent back for correction.

【Evidence】 `manuscript.md:315` — `32. Giamarellos-Bourboulis, E. J. et al. Precision immunotherapy to improve sepsis outcomes: the ImmunoSep randomized clinical trial. *JAMA* (2025).` (Compare the compliant neighbours, e.g. `manuscript.md:316` `33. ... *JAMA* **321**, 2003–2017 (2019).`)

【Why it matters】 Scientific Reports enforces Nature reference style at copy-editing; an entry lacking volume/pages cannot be typeset and is a mandatory fix before acceptance. Incomplete citation also weakens the paper's own "caution" argument in §3.8, which leans on this trial.

【Specific fix】 Replace line 315 with the complete entry (fill in the real volume, first–last pages, and DOI from the published article):
```
32. Giamarellos-Bourboulis, E. J. et al. Precision immunotherapy to improve sepsis outcomes: the ImmunoSep randomized clinical trial. *JAMA* **[VOL]**, [PAGES] (2025). https://doi.org/[DOI]
```
Verify the volume/pages/DOI against the PubMed or publisher record before resubmission.

---

### Finding 2 — "Competing interests" statement uses non-standard wording
【Problem】 The competing-interests statement reads "The author declares no conflict of interest." Nature Portfolio's standard template phrase is "The authors declare no competing interests." Using "conflict of interest" instead of "competing interests" diverges from the journal's mandated heading/terminology.

【Evidence】 `manuscript.md:276-277` — `## Competing interests` / `The author declares no conflict of interest.` (Compare the journal's required label "Competing interests" already used as the heading, but the sentence body says "conflict of interest.")

【Why it matters】 Scientific Reports requires the statement to match its house template wording so the editorial system and readers parse it consistently; non-standard phrasing triggers a mechanical correction request.

【Specific fix】 Replace the sentence body with:
```
The author declares no competing interests.
```

---

### Finding 3 — Chinese-language text appears in the main manuscript body
【Problem】 Section 7 heading and its provenance table contain Chinese characters in the main text. Scientific Reports requires the article to be written in English; non-English prose in the body (not merely a translated supplement) is a language-compliance issue.

【Evidence】 `manuscript.md:222` — `## 7. 数字溯源表 (Number provenance)`; and the table rows, e.g. `manuscript.md:229` — `| 23/25 免疫基因方向性下调（Mars1_down）、22/25 显著（FDR<0.05，含 PDCD1 上调）、21 既下调又显著 | ... |` and `manuscript.md:226-249` generally.

【Why it matters】 A mixed-language main text fails the journal's English-language requirement and will be flagged by editorial screening; it also hurts readability for the international audience.

【Specific fix】 Translate the Section 7 heading and every table cell to English, e.g.:
```
## 7. Number provenance
| Reported number | Source file |
|------|------|
| 23/25 immune genes directionally down (Mars1_down); 22/25 significant (FDR<0.05, including up-regulated PDCD1); 21 both down and significant | `03_results/S01_immunoparalysis_direction.csv` |
```
(Translate all remaining rows 226–249 likewise; keep only the file-path tokens in backticks.)

---

### Finding 4 — Body word count likely exceeds the ~4,500-word guideline
【Problem】 Scientific Reports recommends Articles stay within ~4,500 words excluding Abstract, Methods, References, and figure legends. My section-level estimate of the body (Introduction + Results + Discussion + Limitations + Conclusion) is materially above that.

【Evidence】 Body sections: Introduction `manuscript.md:20-24`; Results `manuscript.md:69-176` (very dense, ~2,800 words); Discussion `manuscript.md:180-188` (continues past truncation, long); Limitations `manuscript.md:192-212` (13 numbered items, ~1,600 words); Conclusion `manuscript.md:216-218`. Estimated total body ≈ 6,000–6,500 words.

【Why it matters】 Although the word limit is a guideline rather than a hard rejection threshold, exceeding it by ~40% invites an editorial "condense" request and lengthens review; the Limitations section (13 items) and Discussion are the obvious trim targets.

【Specific fix】 Condense Limitations (several items overlap, e.g. items 9/11 on repositioning, items 10/12 on selection/circularity) and tighten Discussion; aim to bring the body under ~4,500 words. (This is a recommendation, not a hard fail.)

---

### Finding 5 — Generative-AI disclosure is present but could name the specific model(s) more precisely
【Problem】 The §2.12 disclosure names the host environment ("WorkBuddy, which routes each request to one of several commercial large language models") but does not name the underlying commercial LLM(s). Nature's policy asks authors to identify the tool used.

【Evidence】 `manuscript.md:65-66` — `### 2.12 Use of generative AI` … "Large language model (LLM) assistants accessed through a desktop AI-agent environment (WorkBuddy, which routes each request to one of several commercial large language models) …"

【Why it matters】 The disclosure already covers the four required elements (tool, how used, no AI-generated images, AI not an author) and is correctly placed in Methods, so it is fundamentally compliant. Naming the specific model(s) would make it fully unambiguous and avoid a likely editor query.

【Specific fix】 Add the specific model name(s) after "commercial large language models", e.g.:
```
… several commercial large language models (e.g., <Model A>, <Model B>) …
```

---

## § Stands up (compliant items verified)

1. **Title length and form.** `manuscript.md:1` = "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and validates a 30-gene sepsis prognostic signature" — 16 words (≤20), one compound scientific sentence, no pun. Compliant.
2. **Abstract within limit and citation-free.** `manuscript.md:14` — single unstructured paragraph, ~170 words (≤200), and contains no `[n]` references or author–year citations. Compliant.
3. **Keywords count.** `manuscript.md:16` — "sepsis; immunoparalysis; MARS endotype; Mars1; external validation; drug repositioning" = exactly 6 (≤6). Compliant.
4. **Reference count and style (except [32]).** 35 references (≤60). All entries 1–31 and 33–35 follow Nature style: numbered, NLM journal abbreviations, **volume in bold**, pages present, no issue numbers. Only [32] fails (see Finding 1).
5. **Main-text display items within cap.** Exactly 4 main-text tables (Table 1 `manuscript.md:76`, Table 2 `:124`, Table 3 `:153`, Table 4 `:166`) and **0** main-text figures (all figures are Supplementary, e.g. Fig. S01–S10, MR diagnostics). 4 ≤ 8; all figures correctly placed in Supplementary. Compliant.
6. **All six mandatory statements present.** Data availability (`manuscript.md:265`, with real URL `https://github.com/yyx-4113/sepsis-immunoparalysis-hub` + version tag v1.11.0), Ethics (`manuscript.md:267-268`), Author contributions (`manuscript.md:270-271`), Funding (`manuscript.md:273-274`), Competing interests (`manuscript.md:276-277`), Acknowledgements (`manuscript.md:280-281`). Present.
7. **Generative-AI disclosure present in Methods** with the required elements: tool identified, usage described (i–v), explicit "no image-generation model was used," and "No AI tool is listed as an author or contributor" (`manuscript.md:65-66`).
8. **Article type consistent.** Manuscript `manuscript.md:8` "Article (original research)" matches cover letter `cover_letter.md:5` "Article (original research)"; Sci Rep article type = "Article." Consistent.
9. **Version tag consistent.** v1.11.0 appears in `manuscript.md:265` (Data availability) and `cover_letter.md:24`; title and claims align between the two documents. No mismatch found.
10. **Author ORCID supplied** (`manuscript.md:5`), a plus for the submission record.

---

## § Questions for the authors

1. For reference [32] (Giamarellos-Bourboulis et al., JAMA 2025), can you supply the actual volume, page range, and DOI so the entry is complete before we proceed?
2. The Data availability statement relies on a GitHub repository with a pending Zenodo DOI ("on acceptance"). Is the GitHub repository already public and guaranteed to remain so through peer review and publication?
3. Section 7's provenance table is currently bilingual/Chinese — is there any reason it cannot be fully English, or is it intended as a supplementary-only artifact?
4. Given the body exceeds the ~4,500-word guideline, do you plan to condense Limitations/Discussion, or do you consider the current length justified for the methods-and-resources scope?

---

## § What I actually checked

**Files read:** `05_reports/manuscript.md` (full, v1.11.0) and `05_reports/cover_letter.md` (full).

**Counts / checks performed:**
- Title word count = 16 (≤20); confirmed single sentence, no pun.
- Abstract word count ≈ 170 (≤200); scanned for citations — none found.
- Keyword count = 6 (≤6).
- Reference list enumerated 1–35 (≤60); verified Nature style (bold volume, pages, no issue number) for all 35; identified [32] as the sole entry missing volume/pages/DOI.
- Mandatory statements located and confirmed present: Data availability (with URL + v1.11.0), Ethics, Author contributions, Funding, Competing interests, Acknowledgements.
- Generative-AI disclosure read in full (§2.12); confirmed tool, usage, no-AI-images, AI-not-author.
- Main-text display items counted: 4 tables + 0 figures (all figures are Supplementary "S" items) = 4 (≤8).
- Article type compared manuscript vs cover letter — consistent ("Article (original research)").
- Version tag v1.11.0 cross-checked manuscript Data availability vs cover letter — consistent.
- Title/claims cross-checked manuscript vs cover letter — aligned.
- Body word-count estimate by section (excluding Abstract, Methods §2, References) ≈ 6,000–6,500, exceeding the ~4,500 guideline.
- Identified Chinese-language content in main-text Section 7 heading and table.
