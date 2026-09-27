# Reviewer A4 — Venue & Reporting-Standards Audit

**Manuscript:** *Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning* (single-author; version v1.8.0, commit `180ecb1`)
**Role:** Journal editor + reporting-standards auditor (STROBE-MR, Vancouver, data-availability truthfulness, abstract/figure-legend compliance, negative-result reporting, article-type fit)
**Declaration:** This is a fresh first-submission read. No prior review round was consulted.

---

## Verdict

**Major revision — no desk-reject flag.**

Rationale for *no desk-reject*: the prior-round risk class (a false data-availability claim) is **resolved** — the repository genuinely tracks `03_results/`, `02_scripts/`, and the force-added `01_data/GSE65682/GSE65682_pheno.csv`; the 760/42 cohort count is independently verifiable in the committed file; and the statement no longer asserts that the full ~43 GB raw inputs live in git. No data fabrication, image manipulation, or undisclosed conflict was detected, and the MR null is reported prominently and honestly. The blocking items below are reporting-standard/format defects that are fixable but currently prevent acceptance at a standards-mandating venue.

---

## 1. Data-availability truthfulness (critical)

**Conclusion: the statement is now ACCURATE; one residual scope ambiguity remains.**

Verification performed:
- `git ls-files` → `03_results/` (incl. `08b_clinical_translation.csv`, `09_ext_calibration_dca.csv`, `10_mr_bh_family.csv`, `S08_l1000_candidate_scores.csv`) and `02_scripts/` **are tracked**.
- `git ls-files` → `01_data/GSE65682/GSE65682_pheno.csv` **is present** (force-added).
- Independent read of the committed `GSE65682_pheno.csv`: 802 rows; `group`: sepsis=760 / healthy=42; `mars_endotype`: Mars1=132, Mars2=176, Mars3=118, Mars4=53, unassigned=323; `death_28d`: 1.0=114, 0.0=365, unassigned=323. The manuscript's 760/42 (and 802) counts are exactly reproducible. ✔
- `git ls-files` shows **only** `01_data/GSE65682/GSE65682_pheno.csv` under `01_data/`; the multi-GB `GSE65682_expr.csv`, `GSE65682_family.soft.gz`, and `LINCS/*.gctx` are **not** committed. The statement's "the large raw inputs (~43 GB) … are excluded from the repository only for size" is therefore truthful — it does **not** falsely claim the full raw `01_data/` is in the repo. ✔

### Issues (data-availability)

**Issue D1 — Repository not yet public / DOI not yet minted vs "available" wording.**
- 【Problem】 The Data-availability statement says results and code "are available in the project's versioned reproducibility repository," but the same sentence says it is "to be made public upon acceptance" and the persistent DOI is "to be minted" — i.e., neither is currently accessible to readers.
- 【Evidence】 manuscript.md line 258: *"available in the project's versioned reproducibility repository … to be made public upon acceptance, with a persistent DOI to be minted"*; `git tag` shows v1.0.0–v1.8.0 are local-only version tags, no public remote accessible to a reader.
- 【Why it matters】 A reader cannot reproduce from the statement as written today; "available" overstates current accessibility and can fail a journal's open-data policy at acceptance.
- 【Specific fix】 *"All result tables (03_results/) and analysis code are released under MIT in the versioned repository at https://github.com/yyx-4113/sepsis-immunoparalysis-hub and will be made public, with a Zenodo DOI, upon acceptance; the current commit evaluated here is v1.8.0 (180ecb1)."*

**Issue D2 — Internal bookkeeping files committed into a public reproducibility repo.**
- 【Problem】 Three internal/editorial files are tracked under `03_results/` and would ship publicly: `generated_references.md`, `journal_targeting.csv`, `reference_doi_audit.csv`.
- 【Evidence】 `git ls-files 03_results/` lists `03_results/generated_references.md`, `03_results/journal_targeting.csv`, `03_results/reference_doi_audit.csv`.
- 【Why it matters】 These are author/editor provenance artefacts, not "result tables"; shipping them clutters the public repo and may leak editorial/pipeline-internal state.
- 【Specific fix】 Move them to a non-published path (e.g., `05_reports/_internal/`) or add to `.gitignore` before the public release; the Data-availability statement should reference only `03_results/` deliverables.

**Issue D3 — "raw … matrices … regenerable via deposited processing scripts" slightly over-scoped for E-MTAB-4451.**
- 【Problem】 The phrase implies both raw matrices regenerate via deposited scripts, but E-MTAB-4451 is used as a pre-normalised download with no regeneration script committed (only `09_external_validation.py` *applies* a locked model).
- 【Evidence】 README.md lines 40–41 list `09_external_validation.py` as the E-MTAB-4451 step (applies locked model); no `0x_emtab_*` fetch/process script appears in `git ls-files 02_scripts/`. The statement (manuscript.md line 258) couples both accessions under "via the deposited processing scripts."
- 【Why it matters】 Minor, but a strict reader cannot *regenerate* E-MTAB-4451 from a script; it is re-*downloaded*. The claim is defensible as "re-obtainable from the public accession," not "regenerable via script."
- 【Specific fix】 *"The GSE65682 processed matrix is regenerable from GEO GPL13667 via 02_scripts/00_geo_download.*; E-MTAB-4451 (GPL10558) is obtained as the published normalised matrix from ArrayExpress/BioStudies."*

---

## 2. STROBE-MR checklist audit

**Headline:** The manuscript cites "STROBE-MR item 9b" inline but **ships no completed STROBE-MR checklist** (no such file in `git ls-files`; the itemised supplement is absent). Several core items are addressed in prose; Steiger (9a directionality) is explicitly *not* performed.

| Item | Assessment | Location | Note |
|------|-----------|----------|------|
| 9a Exposure definition | PRESENT | §2.10, line 70 | eQTLGen whole-blood cis-eQTL per gene, ENSG IDs given. |
| 9a Outcome definition | PRESENT | §2.10, line 70 | 3 UKB sepsis GWAS outcomes defined with case/control N. |
| 9a Directionality / Steiger ("which variable is the instrument more associated with") | **GAP (declared not done)** | §2.10, line 72 | "We did not perform a Steiger directionality test … reverse causation biologically unlikely but not formally excluded." Justified via cis-eQTL, but the item is not satisfied. |
| 9a Power / min-detectable effect | PRESENT | §2.10, line 72 | "limited power to detect per-SD ORs smaller than ~1.1–1.2." |
| 9a Weak-instrument threshold F>10 | PRESENT | §2.10, line 72 | "median instrument F (35–168) exceed the conventional F>10 rule." |
| 9b/10 Variant-selection flow (identified → post-LD-clump → post-harmonisation → analysed) | **PARTIAL** | §2.10, lines 71–72 | Threshold (P<5e-8, MAF>0.01) and LD-clump (r²<0.01) stated; post-harmonisation counts given (27; per-gene 3/4/6/6/8); **intermediate identified- and post-clump counts per gene are not tabulated in text** (only final retained). FCGR3A exclusion stated. |
| 11 Heterogeneity | PRESENT | §3.10, line 157 | I² 0.00–0.29 (primary), up to 0.50 (secondary), per-test in `10_mr_bh_family.csv`. |
| 12 Pleiotropy | PRESENT | §3.10, lines 157–158, 182 | Egger intercept test reported with explicit low-power caveat; MR-PRESSO/LOO mentioned (diag plots). |
| 13 Results presentation | PRESENT | Tables 3–4; `04_figures/mr_forest.png` | OR (95% CI), P, per estimator. |
| 14 Sensitivity analyses | PRESENT | §3.10, line 170; Tables 3–4 | Secondary/sensitivity outcomes + MR-Egger/weighted-median. |
| 15 Multiple testing | PRESENT | §2.10, line 72; `10_mr_bh_family.csv` | Pre-specified 45-test BH family. |
| 16 Interpretation / discussion | PRESENT | §4, §5 | Null + reversed CD74 discussed. |
| 17 Strength of evidence / causal claim | PRESENT | §3.10, §5(2) | Explicitly Tier-3, hypothesis-generating, no causal claim. |

### Issues (STROBE-MR)

**Issue S1 — No completed STROBE-MR checklist supplied.**
- 【Problem】 The paper reports a two-sample MR but provides no itemised STROBE-MR checklist (extension for MR), despite invoking "STROBE-MR item 9b" by name.
- 【Evidence】 `git ls-files | grep -i strobe` → no file; manuscript text references "STROBE-MR item 9b" only at line 72, with no checklist table/supplement.
- 【Why it matters】 Most epidemiology/genetics journals mandate the STROBE-MR checklist as a required supplement; its absence is a citable reporting gap, not a cosmetic one.
- 【Specific fix】 Add a `STROBE-MR_checklist.csv`/supplement mapping all 20+ items to manuscript sections, explicitly marking 9a-Steiger as "Not performed (cis-eQTL rationale)" and 9b intermediate counts as "see harmonised CSVs."

**Issue S2 — Variant-selection flow missing intermediate-stage counts.**
- 【Problem】 STROBE-MR 9b/10 requires the number of SNPs at each stage (identified → post-clump → post-harmonisation → analysed); only the final post-harmonisation and analysed counts are given.
- 【Evidence】 §2.10 lines 71–72 give P<5e-8/MAF>0.01 thresholds and final retained (27; per-gene 3/4/6/6/8) but no identified or post-LD-clump per-gene tallies.
- 【Why it matters】 Readers cannot judge attrition/clumping aggressiveness; the harmonised CSVs contain the data but the manuscript must summarise the flow.
- 【Specific fix】 Add a one-line flow per gene, e.g., *"CD74: 11 SNPs identified at P<5e-8 → 4 post-clump → 3 post-harmonisation (analysed)."* (pull from `10_genetics_mr_*_harmonised.csv`).

---

## 3. Vancouver reference formatting

Scan of all 35 references. No obviously wrong DOI syntax (all `doi:10.xxxx/…`). Author "et al." usage is correct (≥6 authors → et al.). Concrete defects observed:

### Issues (Vancouver)

**Issue R1 — Inconsistent journal-title style (full vs abbreviated).**
- 【Problem】 Refs 34 and 35 use abbreviated journal titles while the other 33 references use full titles.
- 【Evidence】 Ref 34: *"Intensive Care Med. 2019;45(10):1360-1371."*; Ref 35: *"Front Immunol. 2023;14:1130214."* — contrast Ref 13 "Nature Medicine", Ref 16 "Frontiers in Immunology", Ref 17 "Nature Reviews Immunology" (full).
- 【Why it matters】 Vancouver (ICMJE) requires a single, consistent journal-title convention (either all NLM-abbreviated or all full); mixed style fails technical copy-editing.
- 【Specific fix】 Use full titles: *"Intensive Care Medicine"* and *"Frontiers in Immunology"* (matching Ref 16), or convert all 35 to NLM abbreviations consistently.

**Issue R2 — Truncated page ranges for two JAMA references.**
- 【Problem】 Refs 2 and 3 give a single start page where the article spans a range.
- 【Evidence】 Ref 2: *"JAMA. 2011;306(23):2594."* (article is 2594–2603); Ref 3: *"JAMA. 2016;315(8):801."* (article is 801–810).
- 【Why it matters】 Incomplete pagination is a Vancouver defect and impedes locating the exact article.
- 【Specific fix】 *"JAMA. 2011;306(23):2594-2603."* and *"JAMA. 2016;315(8):801-810."*

**Issue R3 — Advance-access reference lacks volume/issue/pages (Ref 32).**
- 【Problem】 Ref 32 is cited as "Published online December 8, 2025" with only a DOI; no volume/issue/pages.
- 【Evidence】 Ref 32: *"JAMA. Published online December 8, 2025. doi:10.1001/jama.2025.24175."*
- 【Why it matters】 Acceptable for advance access but the final volume/issue/pages must be supplied at proof; flag for the author to update before publication.
- 【Specific fix】 On final assignment, replace with *"JAMA. 2025; [vol]([issue]):[pages]."* or keep "Epub ahead of print" with a note to update.

**Issue R4 — Reference DOI/existence not independently verifiable by this review.**
- 【Problem】 The manuscript asserts "DOIs verified 2026-09-26" (§5 limitation 7) but I did not (and was not permitted to) open `03_results/reference_doi_audit.csv`; I cannot certify every DOI resolves or that none is retracted.
- 【Evidence】 §5(7): *"DOIs verified 2026-09-26"*; audit CSV is out of scope per review rules.
- 【Why it matters】 A reporting auditor should not assert clean provenance it cannot see; this is a transparency limitation, not a confirmed error.
- 【Specific fix】 Author to confirm the DOI-audit CSV will ship with the public repo, and to re-run it against a live Crossref lookup at acceptance.

---

## 4. Abstract compliance

### Issues (Abstract)

**Issue A1 — Structured format OK, but English abstract ≈460 words exceeds typical bioinformatics caps.**
- 【Problem】 The abstract is correctly structured (Background/Methods/Results/Conclusions) but the English block is ~460 words, far above the 250–350 cap common at methods/bioinformatics venues.
- 【Evidence】 Word count of manuscript.md lines 10–17 (English abstract only) = **463 words** (regex `[A-Za-z0-9\-]+`). Results sentence (line 14) alone is ~190 words and packs the MR null, external AUC, repositioning shortlist, and L1000 rescue.
- 【Why it matters】 Many target journals (e.g., PLOS Computational Biology 300; Briefings in Bioinformatics ~250–350) will desk-trim or return it; the overloaded Results sentence also risks burying the MR null.
- 【Specific fix】 Compress the Results sentence: keep the MR null (*"Two-sample MR did not support a causal effect of any hub gene on 28-day sepsis death (all IVW OR 0.92–1.12, P≥0.23)"*) and the external AUC (0.638, 95% CI 0.532–0.748) as the headline numbers; move repositioning/L1000 detail to the body. Target ≤300 words.

**Issue A2 — Dual-language abstract may not match the target journal's policy.**
- 【Problem】 Both an English and a Chinese (中文摘要) abstract are present; most international bioinformatics venues publish English-only.
- 【Evidence】 manuscript.md lines 21–28 (中文摘要).
- 【Why it matters】 If submitted to an English-language journal, the Chinese block is superfluous and may trigger format rejection; if to a bilingual venue, it is appropriate.
- 【Specific fix】 Confirm target journal policy; retain only the required language(s).

---

## 5. Negative-result reporting

**Assessment: ADEQUATE.**
- The MR primary-outcome null is prominent, not buried: abstract line 14 (*"Two-sample Mendelian randomisation did not support a causal effect of any hub gene … all IVW OR 0.92–1.12, P ≥ 0.23"*), §3.10, §4, and §5(2).
- The reversed, family-significant CD74 critical-care signal is explicitly framed as a *genotype–severity association, not a causal hub claim* (§3.10 lines 170, 182; §5(2)) — balanced, not hedged away.
- Limitations §5 are unusually thorough (11 numbered items, including sample overlap, FIS1 passenger status, single-direction L1000 rescue, selection-chain FWER, docking deferred by design). The only "positive" Tier-1 biology is correctly scoped as a near-replication.
- No evidence of spun or suppressed nulls.

---

## 6. Figure / table legends

### Issues (Figures/Tables)

**Issue F1 — Orphan figure: `04_figures/S01_roc_28d_mars1.png` is committed but never referenced in text.**
- 【Problem】 One committed figure file is not cited anywhere in the manuscript.
- 【Evidence】 `git ls-files 04_figures/` lists `S01_roc_28d_mars1.png`; `grep -oE "04_figures/[A-Za-z0-9_]+\.png" manuscript.md` returns 11 references, none being `S01_roc_28d_mars1.png`.
- 【Why it matters】 Either a missing in-text citation (figure omitted from the narrative) or dead repository clutter; both are editorial defects.
- 【Specific fix】 Either cite it (e.g., in §3.4 as the discovery-cohort ROC) or delete it from the repo/figure set.

**Issue F2 — Figure legends are minimal and not stand-alone.**
- 【Problem】 Figure captions are one-line titles plus a file path; they lack methods/results/abbreviation expansions needed to stand alone.
- 【Evidence】 e.g., line 111 *"Fig. S02. Immune-function score by MARS endotype. [04_figures/S02_score_vs_endotype.png]"*; line 152 *"Fig. S10. Top LINCS L1000 rescuers … [04_figures/fig_s10_l1000_rescue.png]"*.
- 【Why it matters】 ICMJE/Vancouver require legends that are self-contained (what was measured, how, key result); current captions force the reader back into the body.
- 【Specific fix】 Expand each legend to 1–2 sentences: population, panel meaning, and the reported statistic (e.g., for S10: "Rank of lenalidomide (5,435/20,413) and azithromycin (9,152/20,413) among trt_cp rescuers of the Mars1-down axis; glucocorticoids shown as positive controls.").

**Issue F3 — Undefined abbreviations on first use.**
- 【Problem】 `mHLA-DR` and `MALS` appear without expansion.
- 【Evidence】 §3.8 line 143: *"the mHLA-DR criterion (the canonical immunoparalysis biomarker [35])"* and *"recombinant IFN-γ for the immunoparalysis arm, anakinra for the MALS arm"* — neither `mHLA-DR` (monocyte HLA-DR) nor `MALS` (macrophage activation-like syndrome) is spelled out.
- 【Why it matters】 Breaks abbreviation-first-expansion rule; mildly impedes non-specialist readers.
- 【Specific fix】 On first use: *"monocyte HLA-DR (mHLA-DR)"* and *"macrophage activation-like syndrome (MALS)"*.

---

## 7. Article-type fit

**Recommendation: the editor should consider downgrading from "Research" to "Computational Biology / Methods & Resources" (or a "Brief/Report" format).**

Evidence level: (i) the MR primary outcome is **null** (no IVW significant; the only family-significant result reverses direction and is disclaimed); (ii) the five immune hubs are explicitly a **near-replication** of the MARS-consortium biology (§4 line 192: *"this is a near-replication rather than a novel gene discovery"*); (iii) the drug-repositioning layer is **hypothesis-generating** (curated-response concordance, not target-overlap; L1000 rescue single-direction; experimental validation is a blueprint only).

A "Research" article is *defensible* only if the venue values methodological triangulation + an honest independent cross-platform external validation (AUC 0.638) as the contribution. But the causal and translational claims are explicitly tentative, so framing it as a "Research" original article invites reviewer pushback that the advance is incremental. **Suggested handling:** accept as "Computational Biology" / "Methods & Resources," or keep "Research" only with the honest "near-replication + methodological" framing already present in §4. Do **not** present it as a discovery of novel causal hubs.

---

## § Stands up (verified strengths)

1. **Data-availability is now truthful and verifiable.** `03_results/`, `02_scripts/`, and the force-added `01_data/GSE65682/GSE65682_pheno.csv` are git-tracked; the committed pheno.csv independently reproduces 760/42 sepsis/control and the endotype/death counts (verified by direct read). The statement correctly excludes the ~43 GB raw inputs.
2. **Negative MR result is reported prominently and honestly**, with the reversed CD74 signal explicitly disclaimed as a genotype–severity association, not a causal claim (§3.10, §5).
3. **Headline numbers are audit-guarded and internally consistent.** The repository ships `02_scripts/python/check_audit_assertions.py` (17 assertions: OR/CI↔β/se, MR-Egger t-distribution, I²≤0.50, 45-test family size, 23/22/21 immune counts, external AUC 0.638/CI, calibration/DCA) — a genuine, unusual provenance strength.
4. **Limitations are exceptionally balanced** (11 items) and include the authors' own structural caveats (selection-chain FWER, single-direction L1000, docking deferred by design, sample overlap).
5. **STROBE-MR analytical content is largely present in prose**: exposure/outcome defined, F>10 rule met (median F 35–168), power quantified (OR<1.1–1.2), heterogeneity and pleiotropy reported, 45-test BH pre-specified.

---

## § Questions for the authors

1. Will the GitHub repo be made public and a Zenodo DOI minted **before** acceptance, or only after? (Affects whether "available" in the statement is currently true for readers.)
2. For STROBE-MR item 9b/10, can you supply the per-gene SNP counts at *identified* and *post-LD-clump* stages (not just post-harmonisation)?
3. Ref 32 (Giamarellos-Bourboulis, JAMA 2025) — please confirm the final volume/issue/pages once assigned and re-run the DOI audit at acceptance.
4. Is `04_figures/S01_roc_28d_mars1.png` intended to be cited in §3.4, or should it be removed?
5. Which journal is targeted, and does it permit a Chinese-language abstract alongside the English one?

---

## § What I actually checked

**Files read (full):**
- `05_reports/manuscript.md` (entire, 309 lines) — abstract, methods, results, discussion, limitations, data-availability, references.
- `02_scripts/python/check_audit_assertions.py` (entire, 336 lines) — confirmed 17 assertions guard the headline numbers.
- `DATA_SOURCES.md`, `README.md`, `CITATION.cff` (entire).

**Git commands run in ROOT:**
- `git ls-files` — confirmed `03_results/`, `02_scripts/`, and `01_data/GSE65682/GSE65682_pheno.csv` tracked; confirmed full raw `01_data/` (expr/soft/gctx) is **not** committed; confirmed no `STROBE-MR*` checklist file.
- `git log --oneline -1` → `180ecb1 docs(manuscript): v1.8.0 — Round-8 revisions`.
- `git tag` → v1.0.0 … v1.8.0 (local version tags).
- `git status --short` → only `?? 05_reports/review_r9/` untracked (this review).

**Direct data verification:**
- Parsed committed `01_data/GSE65682/GSE65682_pheno.csv` with Python: 802 rows; `group` sepsis=760/healthy=42; endotype Mars1=132/Mars2=176/Mars3=118/Mars4=53/unassigned=323; death_28d 1.0=114/0.0=365/unassigned=323. Matches manuscript exactly.

**Other checks:**
- Abstract English word count (lines 10–17) = 463 via regex.
- `grep` of `04_figures/*.png` references in manuscript vs `git ls-files 04_figures/` → 11 referenced, 1 orphan (`S01_roc_28d_mars1.png`).
- `grep -ni strobe` → only inline "STROBE-MR item 9b" at line 72; no checklist file.
- Reference scan (35 entries) for Vancouver defects → R1–R4.

**Forbidden files (not opened, per brief):** all `REVIEW_round*.md`, `review/`, `review_r2/`…`review_r8/`, `A1_*.md`/`A2_*.md`/`A3_*.md` under `review_r9/`, `generated_references.md`, `journal_targeting.csv`, `reference_doi_audit.csv`, `author_verification_statement.md`. (Note: `generated_references.md`, `journal_targeting.csv`, `reference_doi_audit.csv` *appear in* `git ls-files 03_results/` and would ship publicly — see Issue D2.)

**Discrepancies / observations:**
- `CITATION.cff` version is `1.0.0` (date-released 2026-09-25) while the repo is at `v1.8.0` — metadata staleness (minor; not a manuscript defect per se).
- The Data-availability statement is internally consistent with `DATA_SOURCES.md` (~43 GB excluded for size) and with the git reality — the prior over-claim risk is resolved.
