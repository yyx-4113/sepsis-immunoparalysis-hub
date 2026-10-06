# Independent Peer Review — Reviewer A1
**Role:** Domain / Clinical-Truth Assessment — clinician-scientist in sepsis immunology and critical care medicine  
**Manuscript:** "A reproducible, fully auditable pipeline confirms within-cohort the MARS Mars1 immunoparalysis program and delivers an honest external validation of a 30-gene sepsis prognostic signature"  
**Version reviewed:** tag v1.22.0, commit d507c1c (as stated in Data availability §)  
**Treatment:** First submission. Per the independence discipline I did **not** read any file under `06_review/`, nor `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `SUBMISSION_MANIFEST.md`, `CITATION.cff`, or any other reviewer's output. Every numeric claim I could verify was recomputed from the source CSVs / raw matrices. The built `07_submission_bmc_v1.21.0/Manuscript.docx` was not used as primary evidence; the markdown `05_reports/manuscript.md` is the source of truth.

---

## Summary verdict
This revision has materially improved honesty: the "within-cohort confirmation, not independent replication" framing is now consistent across title, abstract, article-type note, §1, §3.3, §4 and Discussion, and the external validation is reported with appropriate modesty (primary AUC 0.585, 95% CI crossing 0.5). The FIS1 OR/CI numbers are arithmetically correct. **However, the single most important residual problem is the FIS1 death-association claim in §3.3**: it is presented as an *independent* corroboration of prognosis, but FIS1 was selected into the hub precisely by the 28-day-death univariate test, so the reported odds ratio is the selection criterion restated — circular, and the word "independent" is statistically wrong for an unadjusted univariate model. The "erythroid-module gene / genuine prognostic signal" phrasing also overstates FIS1's biology and robustness. These are fixable with wording changes, not new analyses.

---

## Issues

### Issue 1 — FIS1 "independent univariate association" with 28-day death is circular and mislabeled
【Problem】 The manuscript reports FIS1's "significant independent univariate association with 28-day death (OR 1.34 per SD, p = 0.00735)" as if it corroborates FIS1 as a prognostic signal, but FIS1 entered the hub because it passed the very same 28-day-death univariate test used by the tri-method ML consensus, so the quoted OR is the selection test restated, not an independent prognostic confirmation; "independent" is also wrong for an unadjusted univariate model.
【Evidence】 `manuscript.md:101` — "It also passed all three ML selectors including the 28-day-death univariate test (S05_hub_genes.csv) and carries a significant independent univariate association with 28-day death (OR 1.34 per SD … p = 0.00735 …), so it is reported as a genuine secondary erythroid-axis prognostic signal rather than a mere co-expression passenger." `03_results/S05_hub_genes.csv` confirms FIS1 `univariate = True`. `03_results/S06_hub_death_association.csv` row FIS1: `or_per_sd = 1.34, ci = [1.08,1.66], p = 0.00735`. I recomputed the logistic regression `death_28d ~ z(FIS1)` on `GSE65682_expr.csv × GSE65682_pheno.csv` (n = 479 with known 28-day outcome; sepsis-only subset identical): **OR 1.340, 95% CI [1.083, 1.658], p = 0.0071** — the OR and CI reproduce exactly; only the p is trivially different (see Issue 4). The point estimate is therefore real, but it is the same test that qualified FIS1 for the hub.
【Why it matters】 Circular reasoning. A clinician reading this will believe FIS1's prognostic value was established *outside* the selection process, when it is the selection process. Calling an unadjusted univariate odds ratio "independent" implies adjustment for confounders that was never done (see Issue 3 for why that matters clinically).
【Specific fix】 Replace the sentence in §3.3 with:
> "It also passed all three ML selectors including the 28-day-death univariate test (S05_hub_genes.csv); the same univariate signal is reported in S06_hub_death_association.csv (OR 1.34 per SD, 95% CI 1.08–1.66, p = 0.0071, recomputed). Because this odds ratio is the selection test restated rather than an independent prognostic confirmation, FIS1 is reported as an exploratory correlate of 28-day mortality that co-segregates with the erythroid/heme axis, not as a validated prognostic marker or a mechanistic immune target."

---

### Issue 2 — Residual "passenger" label contradicts the new §3.3 wording
【Problem】 Having promoted FIS1 from "passenger" to "genuine secondary erythroid-axis prognostic signal … rather than a mere co-expression passenger" in §3.3, the §7 Number-provenance table still calls it "FIS1 passenger," an internal contradiction a careful reader (and the BMC technical editor) will catch.
【Evidence】 `manuscript.md:192` — "6 co-expression-associated genes (5 immune hubs + FIS1 passenger) | `03_results/S05_hub_genes.csv`". Contrast `manuscript.md:101` which explicitly says FIS1 is "rather than a mere co-expression passenger."
【Why it matters】 Inconsistent terminology undermines the manuscript's claim to full auditability and suggests the provenance table was not updated in step with the text.
【Specific fix】 In the §7 table change:
> "6 co-expression-associated genes (5 immune hubs + FIS1 passenger)"
to
> "6 co-expression-associated genes (5 immune hubs + FIS1, an erythroid/heme-module co-expressed gene)".

---

### Issue 3 — "erythroid-module gene" and "genuine prognostic signal" overstate FIS1's biology and robustness
【Problem】 FIS1 (Fission-1, mitochondrial) is a housekeeping mitochondrial-fission protein expressed in essentially all nucleated cells; it is *not* an erythroid-specific gene. Calling it an "erythroid-module gene" conflates "co-expressed with an erythroid/heme co-expression module" with "erythroid gene," and calling its unadjusted univariate OR a "genuine … prognostic signal" ignores that the association is unadjusted and plausibly confounded by the erythroid/stress-erythropoiesis response of critical illness (and, in whole blood, by packed-RBC transfusion effects, sampling timing, haemoglobin/renal status).
【Evidence】 `manuscript.md:101` and `:178` use "erythroid-module gene"; `:101` uses "genuine secondary erythroid-axis prognostic signal." The module assignment (module 2011, GATA1/KLF1/ALAS2/FECH/HBD/AHSP/SLC4A1/EPB49 + reticulocyte mitophagy genes PINK1/BNIP3L/FUNDC2) is author-derived from `S03_module_trait_cor.csv` / `S03_modules.csv`, which I did not recompute; it is internally consistent but does not make FIS1 itself erythroid. The OR 1.34 per SD is univariate (Issue 1) and is the selection test restated.
【Why it matters】 As a clinician-scientist, the claim that a mitochondrial-fission gene "independently predicts sepsis death" is only defensible as a surrogate of the erythroid/reticulocyte response to critical illness, not as an immune mechanism or a stand-alone prognostic biomarker. Presenting it as "genuine" invites over-reading. The label is generous but, with the right caveat, defensible.
【Specific fix】 (a) In §3.3, change "one non-immune, erythroid/heme-module gene, FIS1 — a mitochondrial-fission protein (Yoon et al. [22])" to "one non-immune gene, FIS1 — a mitochondrial-fission protein (Yoon et al. [22]) that co-segregates with the erythroid/heme co-expression module (module 2011) in this cohort". (b) In the Conclusion (`:178`), change "reported as an erythroid-module gene rather than an immune hub" to "reported as a mitochondrial-fission gene that co-segregates with the erythroid/heme module, rather than an immune hub". (c) Drop "genuine" from the prognosis wording (covered by the Issue 1 replacement).

---

### Issue 4 — p-value nominal mismatch (trivial, but should be aligned)
【Problem】 The reported p = 0.00735 for FIS1 does not match an independent recomputation (p = 0.0071); the difference is negligible but the manuscript should report the value its own analysis actually produces (or round consistently).
【Evidence】 `03_results/S06_hub_death_association.csv`: `p = 0.00735`. Recomputed logistic regression on source data: `b1 = 0.2925, SE = 0.1087, z = 2.69, p = 0.0071` (two-sided). OR and CI ([1.083, 1.658] vs reported [1.08, 1.66]) match to two decimals.
【Why it matters】 Not a substantive error, but a reproducibility/journal-auditability paper should not show a p that a reviewer cannot regenerate; it invites a "numbers don't trace" query.
【Specific fix】 Either (i) regenerate `S06_hub_death_association.csv` with the same solver used for the recomputation and report `p = 0.0071`, or (ii) keep 0.00735 and add a one-line methods note that p was obtained by [solver/SE convention] so it is reproducible. I recommend (i) for internal consistency with the rest of the pipeline, and using p = 0.0071 in the text.

---

## Stands up (verified, with evidence)

1. **Within-cohort framing is now consistent and honest.** The phrase "within-cohort confirmation, not independent replication" appears in the title (`manuscript.md:1`), abstract (`:14`, twice), the article-type note (`:8`), §1 (`:22`, "a confirmation/replication question"), the Discussion (`:147`, "true replication would require an independent cohort carrying externally assigned Mars1 labels, which was not available for the hub/endotype claim"). No sentence claims the *hub biology* was independently replicated; the external validation is explicitly scoped to the 30-gene signature and is "independent in cohort and platform, but not in label" (`:54`, `:106`). I found **no residual over-claim that the hubs were independently validated**.

2. **FIS1 OR and 95% CI are arithmetically correct.** Recomputed from `GSE65682_expr.csv × GSE65682_pheno.csv`: OR 1.340 per SD, 95% CI [1.083, 1.658] — matches the reported OR 1.34, CI [1.08, 1.66] exactly. FIS1 Mars1 logFC +1.26 and t = +17.2 are confirmed in `03_results/S01_mars1_deg.csv` (logFC 1.261433, t 17.156685, DEG_0.3/1.0 = True). Directionality check "5 of 6 hubs Mars1-down, FIS1 Mars1-up" is confirmed in `S06_hub_death_association.csv` (FIS1 +1.261; CD74 −0.758, HLA-DQA1 −0.530, CD14 −0.766, FCGR3A −0.610, HAVCR2 −0.349).

3. **External validation is reported with appropriate modesty and the numbers trace.** From `09_external_validation.csv`: locked-L1 AUC 0.5848 → text 0.585, CI [0.4687, 0.6959] → text [0.469, 0.696] (includes 0.5, correctly called "not significantly above chance"); equal-weight sensitivity AUC 0.6382 → 0.638, CI [0.5317, 0.7475] → [0.532, 0.748]; 29/30 genes mapped, HLA-DQA1 absent; n = 106, 52 deaths; IRG-3 proxy 0.5288 → 0.529. All match. `09_ext_benchmark_vs_srs.csv`: SRS (direction-corrected) 0.6104 → text 0.610; age 0.5043 → 0.504; ΔAUC vs SRS +0.0278 → +0.028; permutation P 0.694 → 0.69. SRS1 24/37 = 64.9%, SRS2 28/69 = 40.6% match the text. Limitation 1 correctly states the primary estimate is "not significantly above chance."

4. **Citations Landelle 2013 [21] and Hotchkiss 2001 [16] are present, correctly placed, and supportive.** Ref [21] (Landelle et al., *Crit. Care* 17:R247, doi:10.1186/cc13072 — "Decreased monocyte HLA-DR expression is associated with increased mortality in septic shock") is cited at `manuscript.md:85` in the sentence establishing mHLA-DR as "the validated bedside immunoparalysis biomarker" — it directly supports the mHLA-DR→mortality link. Ref [16] (Hotchkiss et al., *J. Immunol.* 167:5443, doi:10.4049/jimmunol.167.9.5443 — "Apoptotic death of T and B lymphocytes in sepsis") is cited at `manuscript.md:67` for "sepsis-induced lymphocyte apoptosis" underpinning T-cell exhaustion — an exact match.

5. **ImmunoSep 2025 [32] is fairly presented.** Ref [32] (Giamarellos-Bourboulis et al., *JAMA* 335:775–786, 2025, doi:10.1001/jama.2025.24175) is discussed at `manuscript.md:130` as a *caution*: SOFA improvement in the IFN-γ/immunoparalysis arm but "no mortality benefit and more haemorrhagic events," the trial "underpowered to detect a mortality difference (43.5% vs 49.7% 28-day mortality; P = .34)," and 53% of screened patients unclassifiable by the dual ferritin-and-mHLA-DR algorithm. This is a balanced, non-spin presentation of a null/negative precision-immunotherapy trial and is appropriately used to temper the repositioning claim. (Authors should double-check the precise 43.5%/49.7% figures against the primary publication's Table, but the framing is fair.)

6. **Limitation 7 adequately addresses 28-day-mortality dilution.** `manuscript.md:164` correctly notes that 28-day all-cause mortality is a composite of early hyperinflammatory and late immunoparalytic deaths, that the antigen-presentation/Mars1 program should track late death and secondary infection rather than early shock death, and that the modest external AUC "may partly reflect this endpoint dilution rather than weakness of the axis." This is the right caveat and is stated plainly.

---

## Questions for the authors

1. For FIS1: beyond the erythroid/heme co-expression module, did you test whether the FIS1–death association survives adjustment for any available confounder in `GSE65682_pheno.csv` (e.g., age, pneumonia aetiology, diabetes, thrombocytopenia, ICU-acquired infection)? If not, please state explicitly that the association is unadjusted.
2. Is the FIS1 OR computed on all 479 samples with known 28-day outcome, or restricted to a subgroup? (My recomputation on both the full known-outcome set and the sepsis-only subset gave identical results, so this is just for provenance clarity.)
3. The "53% unclassifiable" figure for ImmunoSep [32] — is that from the per-protocol immunoparalysis subgroup or the whole screened cohort? Please confirm against the primary Table so the citation is exact.
4. Could the direction of the erythroid/heme program in Mars1 simply reflect a higher proportion of stress-erythropoiesis / reticulocyte signal in that endotype's whole-blood samples, independent of immune paralysis? If so, should FIS1 be framed even more cautiously as a *co-expression correlate* rather than an "axis"?

---

## What I actually checked

**Files read (source, not review artefacts):**
- `05_reports/manuscript.md` (full, v1.22.0).
- `03_results/S01_mars1_deg.csv` (FIS1 row verified: logFC 1.261433, t 17.156685, P≈0, DEG_0.3/1.0 True).
- `03_results/S05_hub_genes.csv` (FIS1 lasso/rf/univariate = True; 5 immune hubs + FIS1).
- `03_results/S06_hub_death_association.csv` (FIS1 or_per_sd 1.34, ci [1.08,1.66], p 0.00735; directionality of all 6 genes).
- `03_results/09_external_validation.csv`, `03_results/09_ext_benchmark_vs_srs.csv`, `03_results/08_candidates_drugs.csv`, `03_results/08b_clinical_translation.csv` (all values match the manuscript text, see Stands-up #3).
- `01_data/GSE65682/GSE65682_expr.csv` (11,519 genes × 802 samples) and `GSE65682_pheno.csv` (802 rows; death_28d: 114 dead / 365 alive / 323 NaN).

**Recomputations performed (from raw matrices):**
- FIS1 logistic regression `death_28d ~ z(FIS1)` among the 479 samples with known 28-day outcome: **OR 1.340, 95% CI [1.083, 1.658], p = 0.0071** (Pearson r = 0.1239). Sepsis-only subset identical.
- Cross-checked that the manuscript's claimed OR 1.34 and CI [1.08, 1.66] reproduce exactly; only p differs (0.0071 vs reported 0.00735 — trivial; see Issue 4).

**Values recomputed vs manuscript — discrepancy stated:**
| Quantity | Manuscript | Recomputed / CSV | Agreement |
|---|---|---|---|
| FIS1 OR per SD | 1.34 | 1.340 (CSV 1.34) | exact |
| FIS1 95% CI | [1.08, 1.66] | [1.083, 1.658] | exact to 2 dp |
| FIS1 p | 0.00735 | 0.0071 | trivial (solver/SE convention) |
| FIS1 Mars1 logFC / t | +1.26 / +17.2 | 1.2614 / 17.157 | exact |
| External locked AUC / CI | 0.585 / [0.469,0.696] | 0.5848 / [0.4687,0.6959] | exact |
| External equal-weight AUC / CI | 0.638 / [0.532,0.748] | 0.6382 / [0.5317,0.7475] | exact |
| SRS (dir-corrected) / age AUC | 0.610 / 0.504 | 0.6104 / 0.5043 | exact |
| Drug concordance fractions (IL-7 0.80 … BCG 0.20) | as Table 3 | as `08_candidates_drugs.csv` | exact |

**Not independently recomputed (author-derived, treated as internally consistent):** the WGCNA module assignment / module-2011 membership of FIS1 (`S03_modules.csv`, `S03_module_trait_cor.csv`), the tri-method hub selection internals, and the LINCS L1000 rescue ranks beyond confirming the candidate scores quoted in §3.9 against `S08_l1000_candidate_scores.csv`. These were not the focus of this round and I raise no issue with them.

**Bottom line:** the numerical skeleton is sound and the honesty framing is much improved; the FIS1 prognostic claim needs de-circularising and de-overstating (Issues 1–3), plus a trivial p-value alignment (Issue 4). None of these require new experiments.
