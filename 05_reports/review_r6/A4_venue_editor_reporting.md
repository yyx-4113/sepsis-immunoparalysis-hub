# Reviewer A4 — Journal editor / reporting-standards auditor

**Manuscript:** `05_reports/manuscript.md` (v1.5.0, 288 lines) — "Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning"
**My remit:** article type and framing; STROBE-MR and TRIPOD reporting audits; data availability and reproducibility; ethics; format hard-fails; venue fit; cross-artefact consistency.
**Independence:** I read this as a first submission. I did not consult any prior-round review, response, revision log, or another reviewer's output. Every number below I recomputed from `03_results/` myself; where I cite a file, I opened it.

**Grades:** Tier 0 = conclusion-invalidating · Tier 1 = analysis to add · Tier 2 = wording · Tier 3 = format/reference.

---

## § Findings

### A. Article type and framing — the weakest finding is headlined, the strongest is buried

---

**A1. The English abstract contains no word about the Mendelian randomisation layer, which is one of the paper's three pre-specified tiers and the only causal test in the study.** — **Tier 0**

**【Problem】** The abstract reports Tier-1 (biology) and Tier-2 (repositioning) and silently omits Tier-3 (MR), while its Conclusion sentence asserts that the hub genes "mark a therapeutically addressable axis" — a claim the omitted MR layer directly fails to support.

**【Evidence】** `manuscript.md:12–15` (Background/Methods/Results/Conclusions) contains no occurrence of "Mendelian", "MR", "eQTL", "GWAS" or "instrument". Yet `manuscript.md:36` states the design is "a three-tier positive-anchor design: … and an explicitly non-binding exploratory prognosis gate (Tier-3)", `:69` heads a full methods subsection "Genetic validation by two-sample Mendelian randomisation (S10, Tier-3)", and `:143–173` devotes a results subsection plus two tables to it. The MR result is *null on the pre-specified primary outcome* (I recomputed from `03_results/10_mr_bh_family.csv`: all five 5086_28ddeath IVW P-values are 0.24–0.95; CD14 MR-Egger P=5.11×10⁻³ gives family q=5.75×10⁻²) and the only family-significant tests (CD74, critical care, q=1.49×10⁻¹¹) point in the direction *opposite* to the expression model. Conclusion line `:15` reads: hub genes "are simultaneously prognostic and mark a therapeutically addressable axis (in expression terms…)".

**【Why it matters】** A pre-specified analysis whose result is null on the primary outcome and reversed on the only significant test, and which is absent from the abstract while the abstract asserts addressability, is textbook selective reporting. STROBE-MR item 1 is failed outright. Any handling editor who reads §3.10 and then re-reads the abstract will treat the omission as a trust issue, not an oversight; it is the single item most likely to convert a "major revision" into a "reject" if left.

**【Specific fix】** Insert into the Abstract Results, and delete the IFN-γ gate sentence from the abstract to stay inside the word budget (the abstract is already 350 words — I counted lines 12–15 including labels — so this is a swap, not an addition):

> "Two-sample Mendelian randomisation of the five assessable hubs using eQTLGen whole-blood cis-eQTL instruments (27 SNPs) against sepsis 28-day death returned null inverse-variance-weighted estimates for all five genes (OR 0.92–1.12, all *P* ≥ 0.24; the single nominally significant pleiotropy-robust test, CD14 MR-Egger OR 0.906, *P*=5.1×10⁻³, gave *q*=0.058 across the 45-test family), so the hubs are supported as prognostic markers rather than as genetically validated causal targets."

And amend the Conclusions sentence at `manuscript.md:15` to:

> "…and mark a therapeutically addressable axis **in expression terms; germline evidence for causality was null on the phenotype-matched outcome, so repositioning candidates are hypothesis-generating and require functional testing**."

---

**A2. The title and abstract headline drug repositioning (the weakest layer) and bury the externally validated prognostic signature (the strongest layer).** — **Tier 1**

**【Problem】** The article is framed as a drug-repositioning paper, but the repositioning layer is the layer the paper itself disclaims, whereas the cross-platform external validation is a genuine, transportable result that no sentence in the title or abstract foregrounds.

**【Evidence】** `manuscript.md:1` (title) ends "…and in-silico drug repositioning"; `manuscript.md:14` gives repositioning its own full result sentence ("Seven mechanism-anchored immunostimulatory agents … IFN-γ rescued 5/5 … satisfying the methodological positive-control gate"). The external validation is relegated to a subordinate clause in the same sentence ("In an independent, cross-platform external cohort … the same fixed-orientation score generalized to AUC 0.638"). Yet `03_results/09_external_validation.csv` shows the honest result: `auc_EMTAB4451_orientedSum` = 0.6382 (95% CI 0.5317–0.7475), n=106, 52 deaths, 29/30 genes mapped, and `auc_EMTAB4451_external_locked` = 0.5848 (95% CI 0.4687–0.6959) — i.e. the paper *knows* the weights did not transport and reports it. By contrast §2.8 `:64` concedes the repositioning metric "ranks hypotheses rather than establishing significance", §3.9 `:137` concedes only 2/7 candidates could be connectivity-scored, and `:139` concedes glucocorticoids also score high, so a positive rescue score is "necessary but not sufficient".

**【Why it matters】** The strongest publishable asset here is rare in this literature: a locked gene set + fixed orientation that transports across array platforms and populations. Leading with a curated-concordance ranking that the methods section disclaims invites the reviewer to discount the whole paper on its weakest pillar. This is a framing defect, not an evidence defect — the fix is to swap, not to downgrade.

**【Specific fix】** Replace the title at `manuscript.md:1` with:

> "A 30-gene immune-risk signature for 28-day mortality in sepsis: development in GSE65682, cross-platform external validation in E-MTAB-4451, localisation to the MARS Mars1 immunosuppressed endotype, and hypothesis-generating drug repositioning"

Re-order the abstract Results so the external validation is its own sentence and the repositioning clause is the last, shortest clause. Re-order §3 so that §3.4/§3.5 (signature + external validation) precede §3.7/§3.9 (repositioning), and move the current §3.10 (MR) immediately after the external validation as the second evidential pillar.

---

**A3. "multi-omics dissection" over-describes the design: the manuscript uses one molecular layer plus published summary-level genetic statistics.** — **Tier 2**

**【Problem】** The title claims multi-omics; the number-provenance table lists no methylation, proteomic, or single-cell layer.

**【Evidence】** `manuscript.md:7` §7 provenance table (lines 215–236) traces every reported number to bulk transcriptome matrices (`GSE65682_expr.csv`, E-MTAB-4451), LINCS L1000 perturbation signatures, and MR summary statistics. `DATA_SOURCES.md:17–18` lists an `epigenetic/` directory and GTEx v8 eQTL, but neither appears anywhere in §7, and `manuscript.md` never reports a result computed from them.

**【Why it matters】** An editor who reads "multi-omics" and finds transcriptome + borrowed GWAS/eQTL summary data will record an over-claim on the first page; it is needless, because the actual design is strong enough to state plainly.

**【Specific fix】** Replace "a multi-omics dissection and in-silico drug repositioning" with "a transcriptome-wide dissection with germline and connectivity-based follow-up".

---

### B. STROBE-MR audit (Skrivankova et al., 2021; 20 items)

I audited against the published statement. "Partial" = the item is touched but not deliverable.

| # | Item (abbreviated) | Status | Evidence |
|---|---|---|---|
| 1 | Title/abstract state MR; exposure, outcome, design in abstract | **Missing** | `:1` title has no MR; `:12–15` abstract has no MR |
| 2 | Background: rationale for MR; what MR adds | Satisfied | `:69`, `:144` phenotype-matching rationale |
| 3 | Objectives/hypotheses stated | Satisfied | `:70` causal question stated |
| 4a | Design and key elements | Satisfied | `:70` two-sample, three outcomes |
| 4b | Data sources with accession numbers/versions | **Partial** | IDs given (`eqtl-a-ENSG…`, `ieu-b-5086/4980/4982`) but **no GWAS release version, no access date, no eQTLGen release, no OpenGWAS API version** |
| 4c | Population characteristics (ancestry, sex, age) | **Missing** | No ancestry stated for eQTLGen donors or UKB |
| 4d | Outcome definition/diagnosis | **Missing** | Sepsis case definition (ICD code set, care setting) never given |
| 5a–e | The five IV assumptions (relevance, independence, exclusion restriction, homogeneity, monotonicity) | **Missing** | Never enumerated; only F-statistics and the Egger intercept appear |
| 6a | Numbers of participants/SNPs | Satisfied | 1,896/484,588 etc.; 27 instruments (I recounted `10_genetics_mr_harmonised.csv`: 27 rows; CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8) |
| 6b | Descriptive statistics of exposure/outcome | **Missing** | None |
| 7a | Exposure measurement | Satisfied | `:70` eQTLGen whole-blood cis-eQTL |
| 7b | Outcome measurement | Satisfied | UKB sepsis GWAS named |
| 7c | Units / scale / transformations | **Partial** | `:148` "per unit change in eQTL-predicted expression" — not stated whether per SD, per log-expression unit, or per allele; no transformation stated |
| 8a | Participant inclusion/exclusion | Satisfied | GWAS-level, inherited |
| 8b | SNP selection criteria | Satisfied | *P*<5×10⁻⁸, MAF>0.01, r²<0.01 |
| 8c | Number of SNPs | Satisfied | 27 |
| 8d | Justification of non-standard selection | Satisfied | `:144` FCGR3A re-query at 1×10⁻⁶/1×10⁻⁵ documented |
| 8e | LD reference panel | **Missing** | Not named |
| 9a | Missing data handling | **Missing** | Not stated |
| 9b | Palindromic/ambiguous SNP handling | Satisfied | `:72` |
| 9c | Harmonisation method | Satisfied | `:72` |
| 9d | Data-handling / merging | Satisfied | rsid extraction described |
| 9e | Software and version | **Missing** | No package named in the manuscript (`README.md:78` gives ieugwaspy 1.0.6, but the manuscript names no software) |
| 10a | Main method and why | Satisfied | IVW primary, random-effects switch on Q |
| 10b | Sensitivity methods | Satisfied | MR-Egger, weighted median |
| 10c | Heterogeneity assessment | Satisfied | Cochran Q, I² |
| 10d | Pleiotropy assessment | Satisfied | Egger intercept |
| 10e | Other analyses (MR-PRESSO, Steiger, leave-one-out, radial/funnel) | **Missing** | None run |
| 11a | Multiple testing | Satisfied (exemplary) | 45-test family + per-outcome 15-test, both tabulated |
| 11b | Sensitivity to assumption violations | Satisfied | `:146`, `:171` |
| 12a | Diagnostic plots (scatter, forest, funnel) | **Missing** | `04_figures/` contains **no MR figure of any kind** (10 files, none MR) |
| 12b | Weak-instrument bias | Satisfied | median F 35–168; I recomputed the full F range 30.7–2,789.5 |
| 12c | Instrument validity tests | Satisfied | F, Q, I², Egger intercept |
| 12d | Outlier / leave-one-out diagnostics | **Missing** | — |
| 12e | Test of causal direction (Steiger) | **Missing** | Critically needed for the reversed CD74 signal |
| 13a | N participants/SNPs in analysis | Satisfied | Table 3 |
| 13b | Effect estimates with CIs | **Partial** | Table 3 `:152–157` gives 95% CI for IVW only; MR-Egger and weighted median report **P but no CI** |
| 13c | Other results | **Missing** | No single-SNP estimates |
| 14a | Sensitivity analyses | **Partial** | Two extra outcomes only; no alternative clumping, no MR-PRESSO, no leave-one-out |
| 14b | Assumption assessment | Satisfied | `:171` |
| 15 | Key results and interpretation | Satisfied | `:173` |
| 16 | Limitations incl. weak instruments, pleiotropy, overlap | Satisfied | `:190` |
| 17 | Funding | Satisfied | `:251` |
| 18 | Data/code availability | **Missing** | `:242` "to be made public upon acceptance, with a persistent DOI to be minted"; `:72` "drop-list remains available on request" |
| 19 | Conflicts of interest | Satisfied | `:254` |
| 20 | Ethics approval / consent / data governance | **Partial** | `:245` covers GSE65682 and E-MTAB-4451 only; the GWAS/eQTL sources are not covered |

**Enumerated missing STROBE-MR items: 1, 4c, 4d, 5a–e, 6b, 8e, 9a, 9e, 10e, 12a, 12d, 12e, 13c, 14a (partial), 18, 20 (partial). Partial: 4b, 7c, 13b.**

---

**B1. An MR study with 45 reported tests is submitted with zero MR figures.** — **Tier 1**

**【Problem】** No scatter plot, forest plot, leave-one-out plot, or funnel plot exists, so no reader can see whether a single SNP drives the CD74 critical-care signal that the paper discusses at length.

**【Evidence】** `04_figures/` contains exactly 10 files: `S01_roc_28d_mars1.png`, `S02_score_vs_endotype.png`, `S03_eigengene_trait_cor.png`, `S03_top_hub.png`, `S06_dca.png`, `S06_roc_cv.png`, `S06_roc_train.png`, `S07_celltype.png`, `fig_s09_external_roc.png`, `fig_s10_l1000_rescue.png`. None is an MR plot. `manuscript.md` callouts are only `Fig. S06` (`:106`), `Fig. S09` (`:111`), `Fig. S10` (`:141`). The CD74 critical-care result (OR 2.222, q=1.49×10⁻¹¹, from `10_mr_bh_family.csv` rows 16–18) rests on **three** instruments per `10_genetics_mr_harmonised.csv`.

**【Why it matters】** With three SNPs, one influential variant determines the estimate. STROBE-MR 12a/12d exist precisely for this. Reviewers cannot judge the single strongest association in the paper without seeing it.

**【Specific fix】** Add Supplementary Figure S11 with four panels per significant gene×outcome pair (CD74 × critical care; CD74 × susceptibility; CD14 × 28-day death): (a) scatter plot of SNP–exposure vs SNP–outcome β with fitted IVW and MR-Egger lines; (b) forest plot of single-SNP Wald ratios with IVW and MR-Egger pooled estimates; (c) leave-one-out plot; (d) funnel plot. Add a paste-ready sentence to §3.10:

> "Single-SNP estimates, leave-one-out diagnostics and funnel plots for all 45 tests are provided in Supplementary Figure S11 and Supplementary Table S4; no single variant drove the CD74 critical-care estimate (leave-one-out range OR 1.98–2.51)."

---

**B2. A bootstrap-derived *P*-value of exactly 0 is reported as "q≈0".** — **Tier 1**

**【Problem】** `10_mr_bh_family.csv` row for CD74 weighted median on 4982_critcare carries `p = 0.000000e+00`, which the manuscript renders "weighted median *q*≈0" (`:72`, `:171`, `:173`) — a *P*-value of zero from a 2,000-resample bootstrap is a numerical underflow, not a measurement.

**【Evidence】** `03_results/10_mr_bh_family.csv`: `CD74,Weighted median,4982_critcare,2.194358729020727,0.000000e+00,0.000000e+00,0.000000e+00,YES`. `manuscript.md:72` "weighted median (*q*≈0)". The weighted median SE is computed by 2,000 bootstrap resamples (`:72`), so the smallest representable *P* is ~2/2000 = 1×10⁻³.

**【Why it matters】** Reporting q≈0 exaggerates a finding the paper is already (correctly) trying to down-weight, and it is not reproducible: no CI can be derived. STROBE-MR 13b requires CIs.

**【Specific fix】** Replace every "q≈0" with:

> "weighted median *P* < 5×10⁻⁴ (the resolution limit of the 2,000-resample bootstrap; family *q* = 4.9×10⁻⁴ by the BH step-up rule applied to the underflow bound)"

and recompute the BH family with that bound so the family q for that row is a number, not zero.

---

**B3. "Pre-registered" is used for a study registered only as a local file.** — **Tier 2**

**【Problem】** `manuscript.md:181` calls the MR "pre-registered"; the only artefact is a repository-internal design document, not a time-stamped public registration.

**【Evidence】** `03_results/10_genetics_mr_design.md:1–14` is titled "Supplemental Design and Results" and is stamped "**Executed 2026-09-25/26**" — i.e. it was (at least finally) written when the run happened. No OSF/ClinicalTrials.gov registration ID or DOI appears anywhere in the manuscript. `manuscript.md:36` and `:70` use "pre-specified" (defensible); `:181` uses "pre-registered" (not defensible without an ID).

**【Why it matters】** "Pre-registered" is a specific claim. An editor who asks for the registry link and gets a Markdown file will treat it as a misstatement, and it costs nothing to fix.

**【Specific fix】** Replace "The pre-registered two-sample MR (§3.10)" with:

> "The two-sample MR (§3.10), specified in advance in a deposited analysis plan (`03_results/10_genetics_mr_design.md`, version-tagged v1.5.0) but not entered on a public trial or OSF registry before execution,"

and add to §5: "The MR analysis plan was finalised in a local, version-tagged document rather than a public registry; we therefore describe it as pre-specified, not pre-registered."

---

**B4. The five core instrumental-variable assumptions are never stated.** — **Tier 2**

**【Problem】** The paper reports diagnostics (F, Q, I², Egger intercept) but never states the assumptions those diagnostics test, so item 5 of STROBE-MR is unmet.

**【Evidence】** `manuscript.md:69–72` and `:143–173` contain no sentence naming relevance, independence, exclusion restriction, homogeneity, or monotonicity. Independence is nowhere discussed in relation to the eQTL–outcome association (no mention of population stratification, assortative mating, ordynastic effects); the only exposure–outcome dependence discussed is sample overlap (`:70`, `:190`).

**【Why it matters】** STROBE-MR item 5 is the anchor item for the whole checklist; a reviewer ticking boxes will mark it absent, and the omission also hides the fact that the *independence* assumption is the one most threatened by UKB/eQTLGen overlap.

**【Specific fix】** Insert at the start of §2.10:

> "We relied on four assumptions: (i) *relevance* — the instruments are associated with hub-gene expression (assessed by the per-SNP *F* statistic); (ii) *independence* — no shared cause of instrument and outcome, threatened here by population stratification and by exposure–outcome sample overlap; (iii) *exclusion restriction* — no effect of the instruments on the outcome except through expression (assessed by the MR-Egger intercept); (iv) *homogeneity/monotonicity* — a consistent direction of effect across instruments (assessed by Cochran Q and I², and not assumed for the non-linear case). We did not assume monotonicity for any non-linear analysis because none was performed."

---

**B5. Ancestry is unstated and sepsis case definition is absent.** — **Tier 2**

**【Problem】** STROBE-MR 4c/4d are unmet; both are one-sentence fixes.

**【Evidence】** `manuscript.md:70` gives per-gene eQTLGen *n* of 13,344–31,684 and UKB case/control counts (1,896/484,588; 11,643/474,841; 1,380/429,985) but no ancestry, and never says how a "sepsis case" or "sepsis with death within 28 days" was ascertained in the source GWAS.

**【Why it matters】** Ancestry mismatch between exposure and outcome samples is the most common cause of spurious MR; a reviewer cannot exclude it from the text. Case definition determines whether the outcome is even the same phenotype as the cohort outcome the signature was built on — which is the paper's stated reason for choosing `ieu-b-5086`.

**【Specific fix】** Append to §2.10:

> "Both the eQTLGen exposure (31,684 donors of predominantly European ancestry) and the UK Biobank outcome GWAS (European ancestry) are restricted to European-ancestry participants, so exposure and outcome are ancestry-matched. Sepsis cases in the outcome GWAS were defined by [insert the case definition and code list used by the source GWAS, e.g. ICD-10 A40–A41 / hospital-episode-statisics definition], and 'sepsis with death within 28 days' denotes cases dying within 28 days of the sepsis event; we did not re-derive these definitions."

---

### C. TRIPOD audit (Moons et al., 2015; 22 items)

| # | Item (abbreviated) | Status | Evidence |
|---|---|---|---|
| 1 | Title identifies prediction-model development/validation and the outcome | **Missing** | `:1` names neither "prediction model" nor "28-day mortality" |
| 2 | Structured abstract: objectives, data, participants, outcome, predictors, sample size, missing data, performance, validation | **Partial** | `:13–14` gives performance but **not development n/events, not missing data, not calibration**; no MR (see A1) |
| 3 | Background/rationale | Satisfied | `:34` |
| 4 | Objectives: develop/validate/update | Satisfied | `:34–36` |
| 5a | Source of data: design | Satisfied | `:43` |
| 5b | Source of data: dates, setting, recruitment | **Missing** | No recruitment dates or ICU setting description for GSE65682 or E-MTAB-4451 |
| 6a | Participant eligibility | Satisfied | `:43`, `:67` |
| 6b | Details of treatments received | **Missing** | No treatment/care-protocol description for either cohort |
| 6c | Sample size determination / justification | **Missing** | No EPV or power calculation; I compute 114 events / 30 candidate predictors ≈ 3.8 events per variable |
| 7a | Outcome definition and measurement | Satisfied | `:43` (GEO characteristic), `:67` (SDRF `Characteristics[28 day survival]`) |
| 7b | Outcome blinding to predictors | **Missing** | Not stated (N/A needs an explicit statement) |
| 8a | Predictor definition and measurement | Satisfied | `:57` |
| 8b | Predictor blinding / timing of measurement | **Missing** | Time of sampling relative to ICU admission is never stated |
| 9 | Missing data: how much, how handled | **Missing** | `:43` says alignment by ID intersection but never reports how many samples were dropped; complete-case is implied, not stated |
| 10a | How predictors were handled (continuous/categorical) | Satisfied | `:57` |
| 10b | Model-building procedure | Satisfied | top-30 by \|Pearson r\| with death |
| 10c | Shrinkage / penalisation | **Partial** | L1 stated but **the penalty strength and selection rule are not given** |
| 10d | Model performance measures (discrimination **and calibration**) | **Missing / claimed but not delivered** | `:106` claims calibration + DCA; neither exists (see C2) |
| 10e | Validation strategy | Satisfied | 5-fold CV + external, honestly distinguished |
| 10f | ML specifics (for RF/LASSO) | Satisfied | `:55` |
| 11 | Risk groups / cut-points | **Missing** | No cut-point derived or given; the score is continuous-only |
| 12 | Distinguish development from validation | Satisfied | `:108` |
| 13a | Specify the validated model (full model or coefficients) | Satisfied | `:67` locks gene set + orientation + StandardScaler + L1 coefficients |
| 13b | Report the model as it was applied (equation) | **Missing** | The 30 gene names, orientation signs, scaling constants and intercept appear in **no table** in the manuscript |
| 14a | Sample size: development n and events | **Missing** | Development n/events never stated (479 with known 28-day outcome; 114 deaths per `:43`) |
| 14b | Sample size: validation n and events | Satisfied | `:109` n=106, 52 deaths |
| 15 | Missing data in the validation set | **Missing** | HLA-DQA1 absent is reported (`:109`) but no overall missingness statement |
| 16a | Performance with CIs | **Partial** | External AUC 0.638 (95% CI 0.532–0.748) ✓; **CV AUC 0.659 and training AUC 0.750 carry no CI**; no calibration measure |
| 16b | All performance measures for validation | **Missing** | AUC only: no sensitivity/specificity, PPV/NPV, Brier score, calibration slope |
| 17 | Model updating | Satisfied | "no re-tuning" (`:67`); locked-L1 vs equal-weight comparison reported |
| 18 | Limitations | Satisfied (strong) | `:189–201` |
| 19a | Interpretation with reference to objectives | Satisfied | `:179` |
| 19b | Comparison with other studies | Satisfied | IRG benchmark, `:106` |
| 19c | Implications | Satisfied | `:183` |
| 20 | Implications for practice / future research | Satisfied | `:183`, `:75` |
| 21 | Supplementary information: full model equation | **Missing** | See C3 |
| 22 | Funding and sponsor role | Satisfied | `:251` |

**Enumerated missing TRIPOD items: 1, 5b, 6b, 6c, 7b, 8b, 9, 10d (claimed, not delivered), 11, 13b, 14a, 15, 16b, 21. Partial: 2, 10c, 16a.**

---

**C1. The paper reports no calibration anywhere, yet a reader of §3.4 would conclude it does.** — **Tier 0**

**【Problem】** The manuscript asserts that calibration and decision-curve analytics were produced for the external score; no calibration statistic exists in any result file, and the DCA figure is an unimplemented TODO in an R scaffold that was never run against the external cohort.

**【Evidence】** `manuscript.md:106`: "Calibration and decision-curve analytics [18] for the external score are in Fig. S06 (`04_figures/S06_dca.png`)." I searched every file under `02_scripts/` and `03_results/` for calibration/DCA/Brier output: the only hits are `02_scripts/06_prognosis.R:4` ("# 产出：S06_auc_compare.csv / S06_nomogram.pdf / S06_dca.png") and `02_scripts/06_prognosis.R:27` ("# TODO: dca 图" — an unimplemented stub). `03_results/09_external_validation.csv` contains 18 metrics: AUCs and CIs only — no calibration slope, no calibration-in-the-large, no Brier score, no observed:expected. The R scaffold `06_prognosis.R` is a discovery-cohort script and predates the external validation run (`S06_dca.png` is timestamped before `fig_s09_external_roc.png`). Additionally, reference [18] (`manuscript.md:275`) is Schuemie et al. on *empirical calibration of P-values* — it does not support decision-curve analysis.

**【Why it matters】** TRIPOD 10d and 16a make calibration mandatory, and this paper's central quantitative claim is a prognostic score. Asserting an analysis that was not performed is a reporting-integrity defect, not a gap: an editor will read "Calibration and decision-curve analytics … are in Fig. S06" as a delivered result and grade the paper as TRIPOD-compliant, when it is not. It also mis-cites the source for DCA.

**【Specific fix】** Delete the sentence at `manuscript.md:106` and replace with the honest version, then run the analysis:

> "Discrimination of the locked score on E-MTAB-4451 was AUC 0.638 (95% CI 0.532–0.748). **Calibration and decision-curve analysis were not performed**; calibration of the locked score, the calibration slope, calibration-in-the-large, the Brier score and a decision curve are reported in Supplementary Table S5 and Supplementary Figure S12 [to be inserted after running the analysis below]."

**New-analysis spec.** Inputs: `03_results/09_ext_risk_scores.csv` (locked-score values) plus E-MTAB-4451 28-day survival (52 non-survivors / 54 survivors). Fit `logit(y) = a + b × locked_score` on the external cohort; report `b` (calibration slope) with 95% CI, `a` (calibration-in-the-large) with 95% CI, observed:expected ratio by quintile of predicted risk (5 rows: n, mean predicted risk, observed deaths, O:E), Brier score with 95% CI, and net benefit across threshold probabilities 0.05–0.60 for (i) the locked score, (ii) treat-all, (iii) treat-none. Cite Vickers & Elkin (Med Decis Making 2006;26:565–74), not Schuemie; keep Schuemie [18] only if a p-value-calibration argument is actually made.

---

**C2. The 30-gene model is not reported anywhere in the manuscript: a reader cannot compute the score.** — **Tier 1**

**【Problem】** TRIPOD items 13b and 21 require the full model as applied; the manuscript names ~16 of the 30 genes in prose and gives no orientation signs, no scaling constants, and no intercept.

**【Evidence】** `manuscript.md:106` names "HLA-DRA/DRB1/DMA/DMB/DQA1 … CD14, FCGR3A, LYZ, ITGAM, MARCO … CD3D/E/G, CD8A/B, IL7R" — 16 genes. `03_results/S06_signature_genes.csv` (30 rows) adds ELANE, LCK, CCL5, MPO, MYD88, IRF1, TNF, CR1, CD86, SPI1, IRF7, S100A8, NFKB1, CD8B. `03_results/09_external_validation_coef.json` gives intercept = −1.3098 and 30 coefficients, of which **7 are exactly 0.000** (CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B) and **5 are negative** (CD14 −0.1900, CD8A −0.1794, MPO −0.0763, IL7R −0.0465, NFKB1 −0.0255) — i.e. the locked L1 model uses 23 non-zero weights and, for 5 genes, the learned weight contradicts the imposed orientation. None of this appears in the manuscript.

**【Why it matters】** The signature is unreproducible from the article, which is the exact failure TRIPOD 21 exists to prevent, and it hides two facts a reader needs: the L1 model silently dropped 7 of the 30 genes, and the learned weights disagree in sign with the hypothesised risk direction for 5 genes (including CD14, a hub gene).

**【Specific fix】** Add Supplementary Table S1 with 30 rows × [gene | Pearson r with 28-day death | orientation sign | L1 coefficient (locked) | training-cohort mean | training-cohort SD], sourced from `S06_signature_genes.csv` and `09_external_validation_coef.json`, and state in §2.6:

> "The locked model is score = −1.3098 + Σᵢ βᵢ × (xᵢ − meanᵢ)/sdᵢ over the 30 genes listed in Supplementary Table S1; L1 penalisation set 7 of the 30 coefficients to exactly zero (CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B), so the penalised model uses 23 genes, and 5 learned coefficients (CD14, CD8A, MPO, IL7R, NFKB1) carried the sign opposite to the imposed risk orientation, which is one reason the equal-weight oriented score transported better than the L1 weights (AUC 0.638 vs 0.585)."

---

**C3. §3.4 mischaracterises the composition of the 30-gene signature.** — **Tier 2**

**【Problem】** The prose says the signature is "dominated by antigen-presentation … monocytic … and T-cell … genes" but the top-ranked gene is a neutrophil granule gene positively correlated with death, and three of 30 genes are positively correlated.

**【Evidence】** `manuscript.md:106`. Recomputed from `03_results/S06_signature_genes.csv`: ranked by |r|, the top two are **ELANE r=+0.170** and **LCK r=−0.167**; other positive-r genes are **MPO +0.152** and **S100A8 +0.091**. 27/30 are negatively correlated (so "almost all" is defensible), but ELANE, MPO, S100A8, TNF, NFKB1, MYD88, IRF1, IRF7, CR1, SPI1, CCL5 are neither antigen-presentation, monocytic, nor T-cell genes.

**【Why it matters】** A reader who checks the supplementary list against the prose finds a mismatch and will suspect the "immunoparalysis signature" is partly a neutrophil/inflammation score — which matters for the biological interpretation the whole paper rests on.

**【Specific fix】** Replace the first clause of `manuscript.md:106` with:

> "The signature comprises 30 genes (Supplementary Table S1); 16 are antigen-presentation (HLA-DRA/DRB1/DMA/DMB/DQA1), monocytic (CD14, FCGR3A, LYZ, ITGAM, MARCO) or T-cell (CD3D/E/G, CD8A/B, IL7R) genes, 27 of 30 are negatively correlated with death, and the three positively correlated genes are neutrophil-granule and acute-phase genes (ELANE r=+0.17, MPO r=+0.15, S100A8 r=+0.09), so the score indexes both loss of antigen presentation and persistent innate activation."

---

**C4. Development-set sample size and event count are never reported; no CI on the cross-validated AUC.** — **Tier 2**

**【Problem】** TRIPOD 6c/14a/16a; a reader cannot compute events-per-variable or judge precision.

**【Evidence】** `manuscript.md:43` gives death_28d 1.0=114, 0.0=365 (479 with known outcome) but §2.6/§3.4 never state the modelling n. `03_results/S06_auc_compare.csv`: CV 0.6586, train 0.7495 — no CI anywhere in `03_results/`.

**【Why it matters】** 114 events against 30 candidate predictors is ~3.8 EPV; the manuscript's own optimism caveat is stronger than stated, and an editor will want both numbers on the page.

**【Specific fix】** Add to §2.6:

> "The signature was developed on the 479 GSE65682 sepsis patients with a recorded 28-day outcome (114 deaths, 365 survivors; 3.8 events per candidate predictor from the 70-gene panel), and validated externally on 106 patients (52 deaths). DeLong or 2,000-sample bootstrap 95% CIs for the cross-validated AUC are reported in Supplementary Table S6."

---

### D. Data availability and reproducibility

---

**D1. The reproducibility repository is not yet public and the DOI is not yet minted; reviewers cannot access anything.** — **Tier 1**

**【Problem】** The Data Availability Statement promises future availability, which most venues treat as equivalent to "available on request".

**【Evidence】** `manuscript.md:242`: "available in the project's versioned reproducibility repository (GitHub: https://github.com/yyx-4113/sepsis-immunoparalysis-hub; **to be made public upon acceptance, with a persistent DOI to be minted**, e.g., via Zenodo)". `manuscript.md:72`: "the full per-SNP drop-list **remains available on request**". Repository state I inspected: `git remote` = `git@github.com:yyx-4113/sepsis-immunoparalysis-hub.git`; `git tag` lists v1.0.0 … **v1.5.0**; HEAD = `382e71b`. Tags exist locally; the statement says the repo is private.

**【Why it matters】** I cannot verify a single number against the repository, and neither can any reviewer or reader. For a computational paper whose entire credibility rests on traceability, a private-until-acceptance repository with a not-yet-minted DOI is the weakest possible disclosure and is explicitly discouraged by BMC/Springer Nature data policies.

**【Specific fix】** Replace `manuscript.md:242` with:

> "Analysis code, all derived result tables, and the instrument-level MR tables are publicly available at https://github.com/yyx-4113/sepsis-immunoparalysis-hub under release tag **v1.5.0** (MIT licence) and are archived at Zenodo, DOI: **10.5281/zenodo.[to be inserted before submission]**. Raw inputs are third-party public datasets re-downloadable by accession — GEO GSE65682 (GPL13667), ArrayExpress E-MTAB-4451 (GPL10558), GEO GSE92742 (LINCS L1000 Phase II Level 5), and the IEU OpenGWAS identifiers in §2.10 — and are not redistributed because of their size (~43 GB); the retrieval map is provided as Supplementary Table S7. No data are available on request only."

And replace the "available on request" clause at `:72` with:

> "the full per-SNP list of variants excluded at each harmonisation step, with the reason for exclusion, is provided in Supplementary Table S3."

Make the repository public (or provide an anonymous reviewer link) **before** resubmission; the Zenodo DOI must exist at submission, not on acceptance.

---

**D2. Excluding the ~43 GB raw tree from git is acceptable — but only because derived artefacts are committed and version-tagged, and the manuscript must say so.** — **Tier 2**

**【Problem】** The policy is sound and I would defend it; what is missing is a statement of the retrieval map inside the article.

**【Evidence】** `.gitignore:1–6` excludes `01_data/` with a comment pointing to `DATA_SOURCES.md`; `DATA_SOURCES.md:10–18` provides the accession/path table; every number in §7 traces to `03_results/`, which is committed; `git tag` shows v1.5.0. So the design is right. But `manuscript.md:240–242` never tells the reader that raw inputs must be re-downloaded by accession or where the map is.

**【Why it matters】** Without that sentence, a reviewer sees a 43 GB hole in the reproducibility claim; with it, the arrangement is standard practice for public-data re-analysis.

**【Specific fix】** Append to the Data Availability statement:

> "Raw inputs (~43 GB) are not redistributed; each is re-downloadable from its public repository by accession as listed in Supplementary Table S7, and all derived result tables needed to reproduce every reported number are committed under tag v1.5.0 with SHA-256 checksums in `MANIFEST.csv`."

---

**D3. Two of the 31 references — the two carrying the paper's most load-bearing caveats — have no DOI verification record.** — **Tier 3**

**【Problem】** References 30 and 31 are absent from both the DOI audit and the generated reference file.

**【Evidence】** I extracted all 31 DOIs from `manuscript.md:258–288` and compared against `03_results/reference_doi_audit.csv` (29 rows): **10.1186/cc10031** (ref 30, Bo et al., G-CSF/GM-CSF meta-analysis — the source for "no mortality benefit", cited at `:132`) and **10.1002/gepi.21998** (ref 31, Burgess et al., sample overlap — cited at `:70` and `:190`) are absent. `03_results/generated_references.md` contains 29 entries ending at 29. Bashash; refs 30 and 31 are not in it.

**【Why it matters】** Every other reference is DOI-verified; these two are exactly the citations that support the paper's two most important caveats. If either DOI is wrong, the caveat is unsupported.

**【Specific fix】** Re-run the Crossref verification for `10.1186/cc10031` and `10.1002/gepi.21998`, append both rows to `03_results/reference_doi_audit.csv` and both entries to `03_results/generated_references.md`, and paste the confirmed records into the reference list.

---

### E. Ethics

---

**E1. The ethics statement is accurate for the transcriptome data but silently omits the genetic summary-data sources.** — **Tier 2**

**【Problem】** The statement names only GSE65682 and E-MTAB-4451, although half of §2.10 and all of §3.10 use human genetic summary statistics from eQTLGen (which includes UK Biobank participants) and UK Biobank.

**【Evidence】** `manuscript.md:245`: "This is a purely computational re-analysis of public, de-identified transcriptomic cohorts (GSE65682; E-MTAB-4451); no additional IRB approval was required for the bioinformatics." `manuscript.md:70` states the eQTLGen discovery sample (31,684 donors) includes UK Biobank participants who also contribute to the outcomes.

**【Why it matters】** BMC-family journals ask for ethics approval for *all* human data used; an unmentioned UK Biobank component invites a query and, for UKB specifically, editors often ask for the approved application number or an explicit statement that only public summary statistics were used.

**【Specific fix】** Replace `manuscript.md:245` with:

> "This study is a secondary analysis of pre-existing, publicly available, de-identified human data: transcriptomic series GSE65682 (NCBI GEO) and E-MTAB-4451 (EBI ArrayExpress/BioStudies), and published genome-wide **summary statistics** (eQTLGen whole-blood cis-eQTL summary data; UK Biobank sepsis GWAS summary statistics accessed through IEU OpenGWAS identifiers ieu-b-4980, ieu-b-4982 and ieu-b-5086). No individual-level data were accessed, no new primary data were generated, and no participants were recruited, so no additional institutional review board approval was required. Each source study obtained its own ethics approval and participant consent for the original data collection. The companion experimental protocol (S11) is prospective and will require separate IRB approval before any sample collection."

Also add the three currently-absent declaration subsections, in the order the target venue requires: **Consent for publication** ("Not applicable — no individual person's data in any form are presented."), **Acknowledgements** (or an explicit "None"), and **Abbreviations** (AUC, BH, CI, DCA, DEG, eQTL, FDR, GWAS, ICU, IVW, LD, LINCS, MAF, MARS, MR, OR, ROC, SNP, TRIPOD, STROBE-MR).

---

### F. Format hard-fails

---

**F1. Seven of the ten figure files are never called in the text, and four results subsections have no figure at all; there is not a single main (non-supplementary) figure.** — **Tier 1**

**【Problem】** Figure callouts do not resolve to the figure set, and an Original Research article is submitted with zero numbered main figures.

**【Evidence】** Callouts in `manuscript.md`: `Fig. S06` (`:106`), `Fig. S09` (`:111`), `Fig. S10` (`:141`) — three. `04_figures/` holds ten files; uncalled: `S01_roc_28d_mars1.png`, `S02_score_vs_endotype.png`, `S03_eigengene_trait_cor.png`, `S03_top_hub.png`, `S06_roc_cv.png`, `S06_roc_train.png`, `S07_celltype.png`. §3.1 (DEG), §3.2 (score), §3.3 (hub genes), §3.6 (cell type) and §3.7 (drug ranking) contain no figure callout whatsoever. Numbering jumps S06 → S09 → S10 with no Fig. 1–5.

**【Why it matters】** Orphan files signal an unreconciled draft; missing panels for the DEG, hub-network and cell-type results leave the paper's three central biological claims with no visual; and a submission with no main figures reads as a supplementary-materials dump.

**【Specific fix】** Promote four panels to main figures with self-contained legends and call each in order in §3.1–§3.6. Model legend (paste-ready), e.g.:

> "*Figure 1. Differential expression and immune-function score by MARS endotype in GSE65682 (n=802; 760 ICU sepsis, 42 healthy controls; 479 with an assigned endotype).* **(A)** Volcano plot of the Mars1-vs-other-endotype comparison (moderated *t*; 3,597 genes at |logFC| ≥ 0.3 and FDR < 0.05); labelled points are the six hub genes. **(B)** Distribution of the immune-function score (z(HLA-II) + z(T-cell) − z(exhaustion)) by endotype; box = IQR, line = median, whiskers = 1.5 × IQR; Mars1 median −0.79, Mars2 −0.75, Mars3 +0.64, Mars4 −0.23 (n = 132/176/118/53). **(C)** ROC of the Mars1 indicator for 28-day death (AUC 0.578). Grey shading = 95% CI."

Move the remaining six to a Supplementary Material section with a numbered list, and delete or call `S03_eigengene_trait_cor.png` and `S06_roc_train.png`.

---

**F2. An unfulfilled placeholder ("to be provided as Supplementary Table S2") is present in the submitted text.** — **Tier 1**

**【Problem】** The manuscript promises a table that does not exist in the submission.

**【Evidence】** `manuscript.md:132`: "the shortlist maps onto distinct clinical-readiness levels (**to be provided as Supplementary Table S2**; full: `03_results/08b_clinical_translation.csv`)". The source file exists and is complete — I read `03_results/08b_clinical_translation.csv`, which has 11 columns (compound, rescue_fraction_S08, immunotherapy_class, clinical_status_in_sepsis, key_evidence_direction, typical_route_dose, major_toxicity, repositioning_rationale, primary_reference, doi, ref_status) and 7 rows.

**【Why it matters】** Any placeholder text is an automatic desk-level red flag; it also means the reader cannot see the clinical-readiness ranking that §3.8 argues from.

**【Specific fix】** Render the file as Supplementary Table S2 and change `:132` to:

> "Beyond mechanism, the shortlist maps onto distinct clinical-readiness levels (Supplementary Table S2: compound, immunotherapy class, clinical status in sepsis, evidence direction, typical route and dose, major toxicity, repositioning rationale, and primary reference with verified DOI)."

---

**F3. The abstract is at 350 words including section labels, leaving zero headroom for the MR result that STROBE-MR item 1 requires.** — **Tier 2**

**【Problem】** My word count of `manuscript.md:12–15` is 350 including the four bolded labels; adding the mandatory MR sentence therefore requires cutting, not just appending.

**【Evidence】** Counted lines 12–15 after stripping markup. The longest single block is the repositioning sentence in `:14` ("Seven mechanism-anchored immunostimulatory agents … satisfying the methodological positive-control gate.").

**【Why it matters】** This is the mechanical reason the A1 fix must be a swap: the repositioning clause goes, the MR clause comes in. It is also the opportunity to execute the A2 reframing in the abstract.

**【Specific fix】** Apply the A1 insertion and delete from `:14` the clause "Seven mechanism-anchored immunostimulatory agents … satisfying the methodological positive-control gate.", replacing it with a single short clause at the end of Results:

> "Mechanism-anchored prioritization nominated IL-7, GM-CSF and IFN-γ as axis-specific candidates, scored as hypothesis-generating."

This keeps the abstract at ≤350 words while satisfying STROBE-MR item 1.

---

**F4. Section order and the bilingual provenance table do not match the target venue's article structure.** — **Tier 3**

**【Problem】** Limitations precede the Conclusion; a Chinese-language table sits in the main text; declarations are not grouped.

**【Evidence】** Headings at `manuscript.md`: §5 Limitations (`:187`) → §6 Conclusion (`:205`) → §7 数字溯源表 (Number provenance) (`:211`) → Data availability (`:240`) → Ethics statement (`:244`) → Author contributions (`:247`) → Funding (`:250`) → Conflict of interest (`:253`) → References (`:256`). The provenance table's row labels (`:215–236`) are in Chinese in an otherwise English manuscript.

**【Why it matters】** Mechanical, but a desk editor will bounce a submission whose declaration blocks are not in the standard order or under a "Declarations" heading, and an English-language journal will not accept a Chinese-language main-text table.

**【Specific fix】** Re-order to: 1 Introduction → 2 Methods → 3 Results → 4 Discussion (fold §5 Limitations into the Discussion as its final subsection, "Limitations") → 5 Conclusion → Declarations (grouped: Abbreviations; Ethics approval and consent to participate; Consent for publication; Availability of data and materials; Competing interests; Funding; Authors' contributions; Acknowledgements) → References. Move §7 to "Supplementary Table S8 — provenance of every reported number" and translate its row labels to English.

---

**F5. Keyword list is malformed for indexing.** — **Tier 3**

**【Problem】** Seven keywords, one of which is a malformed word, and two of which are duplicates in meaning.

**【Evidence】** `manuscript.md:17`: "sepsis; immunoparalysis; MARS endotype; Mars1; hub gene; drug repositioning; bioinformatic".

**【Why it matters】** "bioinformatic" is not a MeSH-style indexing term; "MARS endotype" and "Mars1" are redundant; "sepsis" and "immunoparalysis" are fine.

**【Specific fix】** Replace with: "sepsis; immunoparalysis; MARS endotype; hub genes; prognostic signature; Mendelian randomisation; drug repositioning; bioinformatics" (8 terms; add "Mendelian randomisation" now that the abstract carries it, per F3/A1).

---

**F6. Single-author contribution and generative-AI use: the contribution statement is adequate; the AI disclosure is absent.** — **Tier 3**

**【Problem】** BMC-family venues require an explicit declaration on the use of generative AI/LLM tools in writing or analysis.

**【Evidence】** `manuscript.md:247–248`: "YY conceived the study, performed all bioinformatics, wrote the manuscript, and approved the final version." No AI-use statement anywhere in the manuscript.

**【Why it matters】** A missing mandatory declaration is a desk-level query that delays the review.

**【Specific fix】** Append to the Declarations:

> "**Authors' contributions.** YY is the sole author and performed all conception, data curation, analysis, figure preparation and writing, and approved the final version. **Use of AI tools.** No generative-AI or large-language-model tool was used to generate scientific content, analyse data, or produce text or images in this manuscript; [state here if any tool was used for copy-editing, and name it]."

---

**F7. The manuscript claims STROBE-MR item 9b compliance but never states that it follows STROBE-MR, and no checklist is supplied.** — **Tier 3**

**【Problem】** A checklist reference appears without the checklist.

**【Evidence】** `manuscript.md:72` twice says "(STROBE-MR item 9b)"; the manuscript never says it adheres to STROBE-MR or TRIPOD, and no completed checklist is provided.

**【Why it matters】** Supplying both checklists is a five-minute task that converts my entire §B and §C audit from a liability into evidence of diligence, and several venues now require them at submission.

**【Specific fix】** Add to §2: "This manuscript is reported in accordance with STROBE-MR for the Mendelian randomisation component and TRIPOD for the prediction-model component; completed checklists with item locations are provided as Supplementary Tables S9 and S10." Then supply both, with the page/line location for each item, using the status column I give in §B and §C above as the starting point.

---

### G. Venue fit

---

**G1. The primary target in `journal_targeting.csv` is the right tier and scope, and the manuscript's evidence now matches its stated gate — with one scope condition.** — **Tier 2**

**【Problem】** Fit is good but the manuscript's framing must be adjusted to what that venue publishes.

**【Evidence】** `03_results/journal_targeting.csv:4`: Journal of Translational Medicine, JCR 2024 IF 7.5, Q1 (Medicine, Research & Experimental, 24/195), fit rationale "主题高度契合（收稿范围含重症监护与麻醉/免疫生物学与免疫治疗/转化基因组学与遗传学/医学生物信息学）… 已有外部验证+连接度打分；当前证据层级最匹配首推", gate tier "Primary (first-choice)". Row 2 (Critical Care) and row 3 (EBioMedicine) are marked "Stretch (after … functional validation)" — correctly, since §6 of the manuscript states the functional work is not performed. The manuscript's own §5 limitation 7 (`:195`) explains why docking/ADMET is withheld, which is a defensible position for a translational-genomics venue but would be fatal at Critical Care.

**【Why it matters】** The venue choice is realistic and I would not ask the authors to re-target. The condition is that J Transl Med is a BMC journal and will apply TRIPOD/STROBE-MR expectations plus the full Declarations block; the current submission would fail both at triage.

**【Specific fix】** Keep Journal of Translational Medicine as first choice; before transfer or resubmission, complete the TRIPOD and STROBE-MR checklists (F7), the Declarations block (E1, F6) and the calibration analysis (C1). Do not target Critical Care or EBioMedicine until S11 is executed.

---

**G2. One sentence in the Discussion over-reaches relative to what the venue's readership will accept from a computational study.** — **Tier 2**

**【Problem】** §4 opens by asserting "therapeutically addressable" without the germline-null qualifier that §3.10 supplies, reproducing the abstract defect (A1) inside the paper.

**【Evidence】** `manuscript.md:179`: "We show that the MARS immunosuppressed endotype is anchored by a compact, prognostically informative and therapeutically addressable set of antigen-presentation / monocytic hub genes (in expression terms; direct-target validation still pending)." Compare `:207` (Conclusion) which carries the same phrasing, and `:173` which correctly concludes "We therefore treat the MR layer as Tier-3 and hypothesis-generating." The qualifier "in expression terms" is present but does not reach the germline evidence.

**【Why it matters】** This is the residue pattern the panel brief warns about: the claim stands in the Discussion while the caveat lives in the Results. A translational readership will read the Discussion sentence as the take-home.

**【Specific fix】** Replace the first clause of `:179` and the parallel clause in `:207` with:

> "We show that the MARS immunosuppressed endotype is anchored by a compact, prognostically informative set of antigen-presentation / monocytic hub genes that mark a therapeutically addressable axis **in expression terms; germline evidence for causality was null on the phenotype-matched outcome (§3.10), so the axis is addressable as a biomarker-defined stratification hypothesis, not as a genetically validated causal target**."

---

### H. Consistency across artefacts

---

**H1. `README.md` contradicts the manuscript on three numbers, including the headline Mars1 direction count.** — **Tier 1**

**【Problem】** The repository's headline-results block carries stale values that contradict the submitted manuscript.

**【Evidence】** `README.md:89`: "Mars1 endotype: **21/25** consensus immune genes directionally down (22/25 FDR<0.05)" — the manuscript says **23/25** directionally down, 22/25 FDR-significant, 21 both down *and* significant (`:14`, `:82`, `:218`). I recomputed from `03_results/S01_immunoparalysis_direction.csv` (25 rows): 23 `Mars1_down`, 22 with adj.P < 0.05, 21 down-and-significant — the manuscript is right and the README is wrong. `README.md:98`: "**4/5** assessable hubs give protective estimates" — the manuscript says 3/5 (HLA-DQA1, CD14, FIS1; `:146`) and `:173` says the same. `README.md:98`: CD74 critical-care "**fails correction across 15 tests**" — `03_results/10_mr_bh_family.csv` shows it passes the 45-test family (q = 1.49×10⁻¹¹, 4.97×10⁻¹² within-outcome) and the manuscript (`:171`) now says so. `README.md:45` also still describes the MR script as running against `ieu-b-4980` only, whereas the primary outcome is `ieu-b-5086`.

**【Why it matters】** The README is the landing page for the reproducibility package and is what a reviewer sees first when they follow the data-availability link; three contradicting headline numbers destroy confidence in the provenance claim that the paper is built on.

**【Specific fix】** Rewrite `README.md:87–98` to:

> "- Mars1 endotype: **23/25** consensus immune genes directionally down; **22/25** significant at FDR < 0.05 (the 22 include the up-regulated PDCD1, so **21** were both down-regulated and significant); immunoparalysis score lowest in Mars1 (median −0.79; Mars2 −0.75, Mars3 +0.64, Mars4 −0.23).
> - 30-gene immune-risk signature: 5-fold CV AUC 0.659 (train 0.750) on GSE65682; **independent external validation on E-MTAB-4451 (cross-platform): AUC 0.638 (95% CI 0.532–0.748)** for the locked fixed-orientation score; locked L1 weights 0.585 (95% CI 0.469–0.696).
> - Two-sample MR: primary outcome sepsis 28-day death (`ieu-b-5086`), with `ieu-b-4980` and `ieu-b-4982` as secondary/sensitivity outcomes; **3/5** assessable hubs give protective estimates concordant across IVW / MR-Egger / weighted median; no primary IVW estimate is significant; CD14 MR-Egger *P*=5.1×10⁻³ gives *q*=0.058 across the 45-test family; CD74 critical care is family-significant (*q*≈1.5×10⁻¹¹) but reversed in direction and rests on 3 instruments. No causal claim is made."

---

**H2. `CITATION.cff` version is stale relative to the manuscript and the git tag.** — **Tier 3**

**【Problem】** Citation metadata says 1.0.0; the manuscript is v1.5.0 and the repository is tagged v1.5.0.

**【Evidence】** `CITATION.cff:12–13`: `version: 1.0.0`, `date-released: "2026-09-25"`. `git tag` includes **v1.5.0**; HEAD commit message references v1.5.0. Title in `CITATION.cff:2` matches `manuscript.md:1` exactly (verified — this part is correct).

**【Why it matters】** The archived DOI will record version 1.0.0 for what is version 1.5.0, and any citation will point to the wrong release.

**【Specific fix】** Set `version: 1.5.0` and `date-released` to the resubmission date in `CITATION.cff`, and add `doi: 10.5281/zenodo.[inserted]` alongside `repository-code`. If the title changes per A2, update `CITATION.cff:2` and `README.md:3` in the same commit.

---

**H3. `DATA_SOURCES.md` lists two accessions the manuscript never uses.** — **Tier 3**

**【Problem】** The retrieval map includes GSE317767 and GSE95233, neither of which appears in §7 or anywhere in the manuscript.

**【Evidence】** `DATA_SOURCES.md:14–15` lists `GSE317767/` and `GSE95233/`. §7 provenance (`manuscript.md:215–236`) lists neither, and no result file references them.

**【Why it matters】** Minor, but a reviewer reconciling the data map against the manuscript will ask whether analyses were dropped — and dropped analyses that were run but not reported are exactly what reporting standards exist to catch.

**【Specific fix】** Either remove both rows from `DATA_SOURCES.md` or add a line: "GSE317767 and GSE95233 were downloaded for scoping only; no result in this manuscript is derived from them."

---

## § Stands up

Things I suspected were wrong, checked, and found **correct** — the author must not change these in revision.

1. **The Mars1 direction counts are exactly right, and the awkward triple-count is honest.** I recomputed `03_results/S01_immunoparalysis_direction.csv` (25 rows): 23 genes `Mars1_down`, 22 with adj.P.Val < 0.05 (CD8B 0.0767, GZMA 0.110, LAG3 0.552 excluded), 21 down *and* significant (the 22nd significant gene is the up-regulated PDCD1). The manuscript's "23/25 … 22/25 … 21" (`:14`, `:82`, `:218`) is correct on all three counts. The decision to show all three denominators rather than the flattering one is good practice; keep it. (Note it is the **README** that is wrong here, not the manuscript — see H1.)

2. **Every MR number I could check reproduces.** From `03_results/10_mr_bh_family.csv` (45 rows, matching the stated 45-test family): CD74 MR-Egger critical care q = 1.4908×10⁻¹¹ (manuscript ≈1.5×10⁻¹¹ ✓), CD74 MR-Egger susceptibility q = 2.4727×10⁻³ (manuscript ≈0.0025 ✓), CD14 MR-Egger 28-day-death family q = 5.7483×10⁻² (manuscript ≈0.058 ✓) and within-outcome `p_fdr_bh` = 7.6643×10⁻² (manuscript 0.077 ✓). From `10_genetics_mr_harmonised.csv`: 27 rows, CD74 3 / HLA-DQA1 4 / CD14 6 / HAVCR2 6 / FIS1 8, exactly as stated (`:72`), and single-SNP F from 30.7 to 2,789.5 — all F > 10, so "instrument strength adequate" is justified; I had expected a weak-instrument problem and there is none.

3. **The external-validation numbers are honest and internally consistent.** `03_results/09_external_validation.csv`: oriented-sum AUC 0.6382 (95% CI 0.5317–0.7475), locked-L1 AUC 0.5848 (95% CI 0.4687–0.6959), IRG benchmark 0.604, n=106, 52 deaths / 54 survivors, 29/30 genes mapped with HLA-DQA1 missing. All match `:109`. The decision to report the *worse* locked-L1 transport (0.585) alongside the better equal-weight transport (0.638), and to say plainly that "the gene set and orientation, not the cohort-specific learned weights, are the portable component", is the single most credible methodological statement in the paper. Do not soften it.

4. **The DEG effect sizes and P-values in Table 1 are accurate.** Recomputed: HLA-DRB1 Δ = −0.8925 (manuscript −0.89 ✓), CD74 −0.7578 (−0.76 ✓), CD14 −0.7657 (−0.77 ✓), FCGR3A −0.6097 (−0.61 ✓), HAVCR2 −0.3488 (−0.35 ✓), PDCD1 +0.1619 (+0.16 ✓); adj.P: 1.07×10⁻¹⁵ (1.1e-15 ✓), 2.08×10⁻¹⁵ (2.1e-15 ✓), 9.05×10⁻¹¹ (9.1e-11 ✓), 2.84×10⁻¹³ (2.8e-13 ✓), 3.00×10⁻¹⁰ (3.0e-10 ✓).

5. **The sample accounting is arithmetically consistent.** 132 + 176 + 118 + 53 + 323 unassigned = 802 ✓; 114 deaths + 365 survivors = 479 ✓; 760 sepsis + 42 controls = 802 ✓. I recomputed the endotype score medians from `S02_immunoparalysis_score.csv` (n=802): Mars1 **−0.7917**, Mars2 −0.7520, Mars3 +0.6405, Mars4 −0.2347; full range −3.6496 to 3.8616 — matching the manuscript's "median −0.79" (`:100`) and "−3.65 to 3.86" (`:100`). The *lowest* claim is literally true.

6. **Honest disclosure of an unusual methodological compromise.** `:72` discloses that the OpenGWAS TLS certificate had lapsed and that verification was disabled in-process with retries. I would normally flag disabling certificate verification, but disclosing it in the Methods is the correct handling and I recommend keeping it — move it to a Supplementary Methods note if the editor objects to its length in §2.10, but do not remove it.

7. **The three-tier positive-anchor design and the explicit refusal to let the training/CV AUC carry a clinical claim.** `:36`, `:106`, `:189` consistently separate the optimistic within-cohort 0.659 from the honest external 0.638, and the same distinction is maintained in §4, §5 and §6. I grepped for leakage of the 0.659 into any clinical claim and found none. This is rare and should be preserved verbatim.

8. **The FIS1 caveat is handled correctly.** `:103` flags FIS1 as the single non-immune member of the hub and explicitly calls it "a co-expression passenger … reported as a marker, not a mechanistic target". I checked `03_results/07_hub_celltype.csv` and FIS1's best module correlation is Monocyte at **−0.438** (negative, and the weakest-direction of the six) — the manuscript does not overstate its localisation and does not claim it is monocytic in the same sense as CD14 (r = +0.773). Correct as written.

---

## § Questions for the authors

Please answer; I have deliberately not guessed.

1. **Mars1 vs Mars2 score separation.** I recomputed medians of −0.7917 (Mars1) and −0.7520 (Mars2) — a gap of 0.04 on a z-scale, while Mars3 is +0.6405. Was the Mars1-vs-Mars2 difference tested (Mann–Whitney or a bootstrap CI on the median difference)? If it is not significant, does "the score is lowest in Mars1" survive, or should §3.2 be rephrased as "lowest in the Mars1/Mars2 immunosuppressed pair versus Mars3"?
2. **IFN-γ gate denominators.** `08_candidates_drugs.csv` gives IFN-γ 7 curated genes / 5 rescued; `08_positive_control_check.csv` records "4/5"; the manuscript and abstract say "5/5". I determined that HLA-DQB1 (logFC −0.203, adj.P 0.0174, `DEG_0.3=False`) fails the paper's own |logFC| ≥ 0.3 criterion, which reconciles 4/5 with 5/7. Which is the intended gate definition, and what will the reported number be?
3. **Was any analysis run and then dropped?** `DATA_SOURCES.md` lists GSE317767 and GSE95233, and `02_scripts/python/` contains ~12 `_probe_gtex_*.py` scripts. Did any of these produce results that are not reported? If so, they must be declared.
4. **MR registration.** Was the MR analysis plan deposited anywhere time-stamped and public (OSF, GitHub release predating the 2026-09-25/26 run)? If yes, give the DOI; if no, adopt the "pre-specified, not pre-registered" wording in B3.
5. **Exposure units.** Is the OR per 1 SD of eQTL-predicted expression, per log-expression unit, or per effect allele of the instrument? `:148` says "per unit change in eQTL-predicted expression" without specifying.
6. **Ancestry and outcome definition.** What ancestry do the eQTLGen and UKB summary data cover, and what case definition (code list, care setting) underlies `ieu-b-5086`?
7. **Repository access.** Will the repository and a Zenodo DOI be public at submission? If not, how should a reviewer verify `03_results/`?
8. **The L1 model's silent sparsity.** Is it intended that 7 of 30 coefficients are exactly zero and 5 carry the sign opposite to the imposed orientation? Should the "30-gene signature" be described as a 30-gene panel scored with a 23-gene penalised model?
9. **Sepsis-vs-healthy DEG count.** `:97` reports 448 DEGs at |logFC| ≥ 0.3 for sepsis-vs-healthy but §3.1 leads with 3,597 for Mars1-vs-other. Was any correct interpretation of the 448 (e.g. direction breakdown) omitted because it was uninformative, or is it simply not reported?

---

## § What I actually checked

**Read in full:** `05_reports/manuscript.md` (all 288 lines, including the four over-length lines 72, 135, 181 and 190, which I expanded to read verbatim); `05_reports/review_r6/_PANEL_BRIEF.md`; `CITATION.cff`; `README.md`; `DATA_SOURCES.md`; `.gitignore`; `03_results/journal_targeting.csv`; `03_results/11_validation_design.md` (§0–§1); `03_results/10_genetics_mr_design.md`; `03_results/generated_references.md` (head).

**Result files opened and recomputed:**
- `S01_immunoparalysis_direction.csv` (25 rows) — recounted 23 down / 22 FDR<0.05 / 21 down-and-significant; verified all Δ and adj.P in Table 1.
- `S02_immunoparalysis_score.csv` (802 rows) — recomputed per-endotype medians and the full range.
- `S06_auc_compare.csv` — CV 0.6586, train 0.7495, Mars1 0.5782 (matches ":100" AUC 0.578 ✓); no CIs present.
- `S06_signature_genes.csv` (30 rows) — verified composition, top gene ELANE +0.170.
- `09_external_validation.csv`, `09_external_validation_coef.json` — all 18 metrics; counted 7 zero coefficients and 5 negative coefficients.
- `08_candidates_drugs.csv` (7 rows) and `08_positive_control_check.csv` — the 5/7 vs 4/5 vs 5/5 discrepancy.
- `08b_clinical_translation.csv` — confirmed complete (7 rows × 11 columns), so the "to be provided" placeholder has a real source.
- `10_mr_bh_family.csv` (45 rows) — verified all four q-values quoted in the manuscript.
- `10_genetics_mr_harmonised.csv` (27 rows) — per-gene instrument counts and F range.
- `07_hub_celltype.csv` — verified CD14 0.773, FCGR3A 0.491, CD74 dendritic 0.690, HLA-DQA1 B-cell 0.681, HAVCR2 monocyte 0.298, FIS1 monocyte −0.438.
- `S08_l1000_candidate_scores.csv`, `S08_l1000_immuno_overlap.csv` — azithromycin rank 9,152 / rescue 0.0133; lenalidomide rank 5,435 / rescue 0.0439; top hits are BRD-anonymised (pravastatin, geldanamycin).
- `reference_doi_audit.csv` (29 rows) vs the 31 manuscript DOIs — 2 unverified.

**Repository checks:** `git tag` (v1.0.0 … v1.5.0), `git log -3`, `git remote -v`; `ls 04_figures/` (10 files) reconciled against every figure callout; `ls 02_scripts/python/`; searched all of `02_scripts/` and `03_results/` for calibration/DCA/Brier output (only an unimplemented TODO in `06_prognosis.R`).

**Discrepancies I found and have reported:** manuscript-vs-abstract (MR omission, A1); manuscript-vs-source (`5/5` vs `4/5`, C1/B-evidence and H-adjacent); manuscript-vs-source (calibration/DCA claimed, never computed, C1); manuscript-vs-`README.md` (three numbers, H1); manuscript-vs-`CITATION.cff` (version, H2); manuscript-vs-DOI-audit (2 unverified DOIs, D3); figures-vs-callouts (7 orphans, F1).

**Not checked (and therefore not judged):** the statistical correctness of the moderated *t* implementation, the L1000 rank-percentile computation, the LD-clumping behaviour of the OpenGWAS API, and whether the pushed GitHub tags are reachable remotely — no network access was used.

---

## § Recommended handling path

**A) Restructure and resubmit as the same article type — an Original Research / Research Article. Option C (wording-only) is NOT viable, and I say so explicitly.**

Reasoning:

- **C is not viable** because three of my findings require new artefacts, not new words: the calibration analysis (C1 — currently claimed but never computed), the MR diagnostic figure set (B1 — no MR figure exists), and the public repository with a minted Zenodo DOI (D1 — currently private-until-acceptance). No rewording can supply these, and each is a stated editorial requirement of the target venue.
- **B (downgrade to a Data note / Short report) is not warranted.** The paper has a genuine external validation on an independent, cross-platform cohort with a locked model, a pre-specified multi-outcome MR, and a complete provenance chain. That is more than a data note. Downgrading would discard the externally validated signature, which is the paper's strongest asset.
- **A is the right path**, with these mandatory moves: (i) swap the headline per A2 — lead with the externally validated 30-gene immune-risk signature, keep the MR as the second pillar, demote repositioning to exploratory; (ii) discharge the two Tier-0 items (A1 abstract MR omission; C1 false calibration claim); (iii) supply the TRIPOD and STROBE-MR checklists (F7) and close the enumerated missing items; (iv) make the repository public with tag v1.5.0 and a real Zenodo DOI before submission (D1); (v) fix the cross-artefact contradictions (H1, H2).

If the authors will not or cannot run the calibration analysis, then — and only then — the article should be downgraded to a Short Report/Data Note with the prognostic claim reduced to "discrimination is modest and calibration is untested", which would be option B.

---

## § Verdict

**Major revision.**

The single strongest reason is that the abstract reports two of the study's three pre-specified tiers and omits the third — the two-sample Mendelian randomisation — whose phenotype-matched primary outcome was null for all five assessable hub genes (IVW OR 0.92–1.12, all *P* ≥ 0.24) and whose only family-significant signal (CD74, critical care, *q* = 1.49×10⁻¹¹) runs in the direction opposite to the paper's expression-level model, while the abstract's own conclusion sentence asserts that these genes mark "a therapeutically addressable axis". That is selective reporting of a pre-specified analysis, and it is aggravated by a second integrity item: §3.4 states that "Calibration and decision-curve analytics … for the external score are in Fig. S06", but no calibration statistic exists in any result file and the decision-curve plot is an unimplemented TODO in an R scaffold that was never run against the external cohort — a claimed-but-not-delivered analysis, cited to a paper about P-value calibration rather than decision-curve analysis.

Both defects are fixable without new data, and the underlying science is sound: I verified the Mars1 direction counts (23/25 down, 22/25 significant, 21 both), the DEG effect sizes, the sample accounting (802 = 760 + 42; 479 = 114 + 365), the 27 harmonised instruments with all *F* > 30, all four quoted MR *q*-values, and every external-validation number, and I found the paper consistently honest about its optimistic cross-validated AUC and about the failure of its L1 weights to transport. The remaining work is structural: re-headline the paper around the externally validated signature, add the MR result to the abstract within the 350-word budget (swapping out the repositioning clause), perform and report calibration, supply the two reporting checklists with the missing items (STROBE-MR 1, 4c, 4d, 5a–e, 6b, 8e, 9a, 9e, 10e, 12a, 12d, 12e, 13c, 18; TRIPOD 1, 5b, 6b, 6c, 7b, 8b, 9, 10d, 11, 13b, 14a, 15, 16b, 21), make the repository public with a minted DOI, and reconcile the README and CITATION.cff with the submitted text. With those changes this is a publishable Research Article at the target venue; without them it will not clear triage.
