# Independent Peer-Review Report — Domain / Clinical-Truth Assessment

**Round:** round20_v1.21.0
**Reviewer role:** Clinician-scientist, sepsis immunology / critical care medicine (independent domain reviewer)
**Manuscript:** "A reproducible pipeline recapitulates the MARS Mars1 immunoparalysis program within-cohort and externally evaluates a 30-gene sepsis prognostic signature" (BMC Medical Genomics, v1.21.0)
**Independence statement:** Treated as a first submission. No file under `06_review/`, no `REVIEW_*.md`, `RESPONSE_*.md`, `SUBMISSION_MANIFEST.md`, `CITATION.cff`, author-verification statement, or any co-reviewer output in `06_review/round20_v1.21.0/` was read. Every numeric claim below was recomputed by me from the deposited source CSVs / phenotype file.

## Overall assessment

**Recommendation: Major revision (acceptance-worthy after targeted fixes).** The computational biology is sound and, importantly, the repositioning/limitations honesty is exemplary — this is a genuine strength. However, three domain-truth problems must be corrected before acceptance: (1) the central "recapitulate / near-replication" framing is circular because the Mars1 labels are the MARS consortium's own clustering of the same GSE65682 cohort; (2) the FIS1 "co-expression passenger" framing contradicts the authors' own data showing FIS1 is a prognostically significant, 28-day-death-associated gene; and (3) a statistical wording error in §3.7 ("significantly below") contradicts the paper's own binomial result. A key mHLA-DR→28-day-mortality citation is missing. None of these invalidate the Tier-1 biology, but together they overstate independence and undersell a real secondary axis.

---

## Issue 1 — 28-day mortality is a defensible but diluted endpoint for an immunoparalysis claim, and the dilution is not discussed (counts are internally consistent)

【Problem】 28-day mortality is an acceptable sepsis endpoint but is biologically diluted for a *pure* immunoparalysis claim, yet this dilution is never discussed; the underlying mortality/endotype counts are, however, internally consistent.

【Evidence】 Recomputed death×endotype crosstab from `01_data/GSE65682/GSE65682_pheno.csv`: Mars1 deaths 45/(45+87=132) = 34.1%; Mars2 38/176; Mars3 21/118; Mars4 10/53; Mars2–4 combined 69/(38+138+21+97+10+43=347) = 19.9%; total deaths 114, survivors 365, unassigned 323 (no death data). These exactly match `manuscript.md:31` (death_28d 114/365/323) and `manuscript.md:85` (Mars1 45/132 = 34.1%; Mars2–4 69/347 = 19.9%). So the numbers are consistent. But immunoparalysis manifests as *late* death and secondary infection; 28-day mortality composites early hyperinflammatory death with late immunoparalytic death, diluting a pure antigen-presentation signal. The external AUC is accordingly modest (locked-L1 0.585, equal-weight 0.638; `manuscript.md:107`).

【Why it matters】 Presenting a diluted endpoint without comment invites a reviewer to read the modest AUC as weakness of the antigen-presentation biology rather than endpoint mismatch — undercutting the paper's own thesis that Mars1 collapse = immunoparalysis (a late-death biology).

【Specific fix】 Add to §3.4/§3.5 (or Limitation 7, `manuscript.md:164`): "Twenty-eight-day mortality in sepsis is a composite of early hyperinflammatory and late immunoparalytic deaths; because the antigen-presentation/Mars1 program should track late death and secondary infection rather than early shock death, the 28-day endpoint is expected to dilute the immunoparalysis signal, and the modest external AUC (0.585–0.638) may partly reflect this endpoint dilution rather than weakness of the axis. Ninety-day mortality — the more mechanistically aligned endpoint for an immunoparalysis claim — was unavailable in both source cohorts."

---

## Issue 2 — "Recapitulate / near-replicate" is circular: the Mars1 labels are the MARS consortium's own clustering of the same cohort

【Problem】 Calling the 5 hubs a within-cohort "recapitulation / near-replication" of the established Mars1 program is circular: the Mars1 endotype labels used in the Mars1-vs-Other contrast are the MARS consortium's own unsupervised clustering of GSE65682, so re-deriving CD74/HLA-DQA1/CD14/FCGR3A/HAVCR2 as Mars1-down is recovering the label's defining feature, not an independent replication.

【Evidence】 `manuscript.md:31` states `mars_endotype` is the MARS consortium's stratification and GSE65682 *is* that cohort; Scicluna et al. [5] (`manuscript.md:247`) derived the four endotypes from GSE65682. The 5 hubs are exactly the antigen-presentation genes that define Mars1 (verified Mars1_down in `03_results/S01_mars1_deg.csv`: CD14 line 1870 logFC −0.7657, CD74 line 1933 −0.7578, FCGR3A line 3652 −0.6097, HAVCR2 line 4343 −0.3488, HLA-DQA1 line 4502 −0.5301; all DEG_0.3=True, adj.P<3e-8). The independent cohort E-MTAB-4451 was used only for the 30-gene prognosis signature (`manuscript.md:106–107`), NOT for an independently Mars1-classified replication of the hub/endotype claim. The abstract (`manuscript.md:14`) and §4 (`manuscript.md:147`, "near-replication rather than a novel gene discovery") use replication language for what is a within-cohort confirmation.

【Why it matters】 A BMC reviewer will read "recapitulate / near-replication" as independent confirmation; the actual contribution is the auditable pipeline + honest external prognosis validation + drug blueprint. Overstating independence risks a reviewer concluding the central biology is tautological, which can sink the "research article" framing.

【Specific fix】 Replace the replication language with confirmation language. Abstract (`manuscript.md:14`): "We re-analysed GSE65682 (802 samples) with an auditable multi-omics pipeline that *confirms within-cohort* that the Mars1 endotype label encodes the established antigen-presentation/immunoparalysis program (a within-cohort confirmation, not an independent replication — the Mars1 labels originate from the MARS consortium's own clustering of this cohort)." §4 (`manuscript.md:147`): change "this is a near-replication rather than a novel gene discovery" to "this is a within-cohort confirmation of the antigen-presentation program that defines the Mars1 label; true replication requires an independent cohort carrying externally assigned Mars1 labels, which was not available for the hub/endotype claim."

---

## Issue 3 — FIS1's logFC +1.26 / Mars1-up is verified and biologically sound, but the "co-expression passenger" framing contradicts the authors' own death-association data

【Problem】 FIS1's direction and magnitude are verified and the erythroid interpretation is plausible, but calling it a "co-expression passenger" is contradicted by the authors' own files: FIS1 passed all three ML selectors (including the 28-day-death univariate test) and carries a *significant independent* 28-day-mortality signal.

【Evidence】 `03_results/S01_mars1_deg.csv:3716` FIS1 logFC = +1.2614, t = +17.157, DEG_0.3=True, DEG_1.0=True (Mars1-up) — matches `manuscript.md:101` ("logFC +1.26, t = +17.2"). `03_results/S05_hub_genes.csv:2` FIS1 lasso/rf/univariate = True/True/True, i.e. it passed the 28-day-death univariate selector of §2.5. `03_results/S06_hub_death_association.csv:2` FIS1 corr_with_death = +0.124, OR_per_sd = 1.34 (95% CI 1.08–1.66), p = 0.00735 — a significant independent 28-day-death association, positive direction (higher erythroid program ↔ higher death). Yet `manuscript.md:101` and the Conclusion (`manuscript.md:178`) call FIS1 a "co-expression passenger … rather than an immune hub." `manuscript.md:101` itself also states "FIS1 is therefore not a co-expression partner of the immune hubs" — so "co-expression passenger (of the hubs)" is internally contradictory: FIS1 co-expresses with erythroid module 2011, not the immune hubs.

【Why it matters】 A gene with its own significant mortality signal (p=0.007, OR 1.34) is not a "passenger"; the label undersells a genuine secondary prognostic axis (erythroid shift in critical illness) and creates an internal contradiction a careful reviewer will flag, weakening the paper's demonstrated honesty.

【Specific fix】 (a) Reconcile terminology: replace "co-expression passenger" with "erythroid-module gene co-selected with the immune hubs" at `manuscript.md:101` and `manuscript.md:178`; add to §3.3: "FIS1 was selected by all three ML selectors including the 28-day-death univariate test (S05_hub_genes.csv) and shows a significant independent univariate association with 28-day death (OR 1.34 per SD, 95% CI 1.08–1.66, p=0.00735; S06_hub_death_association.csv), so it is reported as a prognostically significant erythroid-axis gene, not merely a co-expression passenger." (b) Analysis spec: test whether the full erythroid/heme module 2011 (GATA1/KLF1/ALAS2/FECH/…) is jointly associated with 28-day death in GSE65682 and externally in E-MTAB-4451, to establish whether the erythroid program is a standalone prognostic axis distinct from the antigen-presentation axis.

---

## Issue 4 — Repositioning conclusion is honest, but §3.7 contains a statistical wording error ("significantly below")

【Problem】 The repositioning conclusion is commendably honest (descriptive only; prednisone caveat), but §3.7 states "the two lowest are significantly below it" while the binomial P(X≥k) is ≥0.82 for all seven — which actually means none differs significantly from the 0.84 chance background.

【Evidence】 `03_results/08_candidates_drugs.csv` gives concordance (IL-7 0.80 … BCG 0.20) and `binom_p_immune_bg` = IL-7 0.817, GM-CSF 0.944, IFN-γ 0.985, Azithromycin 0.931, Lenalidomide 0.997, Thymosin α1 0.997, BCG 1.000 — all ≥0.817, i.e. none significantly above chance. §3.7 (`manuscript.md:115`) writes "one-sided binomial P(X ≥ k) ≥ 0.82 for all seven; the two lowest are significantly below it." Under background 0.84 a candidate scoring 1/5 (BCG) yields P(X≥1)=1.00, so its low concordance is *expected by chance*, not "significantly below." The mHLA-DR (membrane) vs HLA-DR mRNA distinction is correctly handled at `manuscript.md:85` ("should not be equated with monocyte membrane mHLA-DR … complementary, not interchangeable"). Positive-control honesty confirmed: `03_results/S08_l1000_positive_control.csv:2` prednisone rescue 0.1364, rank 651, pct 0.03189 (3.2nd percentile, matches `manuscript.md:137`); §3.9 correctly states this makes L1000 rescue "descriptive only."

【Why it matters】 The isolated "significantly below" phrase contradicts the paper's own binomial result and could read as spin; it slightly muddies an otherwise exemplary limitations section.

【Specific fix】 Replace the sentence in §3.7 (`manuscript.md:115`) with: "Under the internal immune-gene background of §3.1 (21/25, 84%, of consensus immune genes are Mars1-down at FDR<0.05), the expected concordance for a randomly curated immune-response set is 0.84. A one-sided binomial test P(X≥k) yields p≥0.82 for all seven candidates, i.e., no candidate's concordance exceeds the chance background and none is statistically distinguishable from it (the lowest two, lenalidomide 0.40 and BCG 0.20, are also consistent with chance under the 0.84 background, not 'significantly below' it). Table 3 is therefore retained as mechanism annotation only."

---

## Issue 5 — MUST-CITE gap: the prospective low-mHLA-DR → 28-day-mortality link (and the foundational lymphocyte-apoptosis immunoparalysis papers) are missing

【Problem】 The immunoparalysis biomarker canon is largely covered, but the direct prospective link between low monocyte mHLA-DR and 28-day mortality / secondary infection — the evidentiary bridge for the paper's central endpoint claim — is absent, and the foundational sepsis-lymphocyte-apoptosis papers are missing.

【Evidence】 Present: Monneret 2008 [18], Venet & Monneret 2018 [19], Joshi 2023 [31], Hotchkiss 2013 [3] (review), Boomer 2011 [2], Scicluna 2017 [5], Davenport 2016 [15], Giamarellos ImmunoSep 2025 [30]. Missing: (i) **Landelle C, et al. "Decreased monocyte human leukocyte antigen-DR expression is associated with increased mortality in septic shock: a prospective study." *Crit Care* 17, R247 (2013). doi:10.1186/cc13072** — the prospective demonstration that early low mHLA-DR predicts 28-day mortality and secondary infection; this is the precise bridge for using an antigen-presentation/Mars1 signal as a 28-day-mortality readout and a BMC reviewer would expect it alongside [18]/[19]. (ii) **Hotchkiss RS, et al. "Apoptotic death of T and B lymphocytes in sepsis." *J Immunol* 167, 5443–5449 (2001)** (or the 2003 *Immunol Res* lymphocyte-apoptosis review) — the foundational demonstration of sepsis-induced lymphocyte apoptosis underpinning the T-cell-exhaustion/immunoparalysis axis the paper invokes (`manuscript.md:67`, `manuscript.md:101`). (iii) The erythroid/heme program characterizing Mars1: Scicluna 2017 [5] is cited, but the paper should explicitly point to the erythroid-module description within [5] (or a MARS-consortium follow-up) when asserting FIS1 belongs to the Mars1-up erythroid arm (`manuscript.md:101`), so the erythroid claim is anchored to the primary source rather than asserted from co-expression.

【Why it matters】 Missing the prospective mHLA-DR→28-day-mortality paper leaves the central endpoint claim under-cited exactly where a clinician reviewer will look; the lymphocyte-apoptosis omission weakens the immunoparalysis-mechanism framing that the T-cell-exhaustion discussion depends on.

【Specific fix】 Add to References: "Landelle C, et al. Decreased monocyte human leukocyte antigen-DR expression is associated with increased mortality in septic shock: a prospective study. *Crit Care* 17, R247 (2013). doi:10.1186/cc13072" and "Hotchkiss RS, et al. Apoptotic death of T and B lymphocytes in sepsis. *J Immunol* 167, 5443–5449 (2001). doi:10.4049/jimmunol.167.9.5443", and add a sentence in §1/§3.2 citing Landelle alongside [18]/[19] when introducing 28-day mortality as the immunoparalysis readout.

---

## Issue 6 — Clinical-translation caveats (ImmunoSep 2025 null mortality; 53% unclassifiable) are presented fairly

【Problem】 (No defect.) The caveats are balanced and not spun.

【Evidence】 `manuscript.md:130` reports the ImmunoSep RCT [30] null 28-day mortality (43.5% vs 49.7%, P=.34), *more haemorrhagic events*, and that 53% of screened patients were unclassifiable by the ferritin-and-mHLA-DR algorithm, explicitly notes the trial was underpowered, and frames it as a *caution* for the repositioning axis ("axis reversal by IFN-γ does not equal clinical benefit"). mHLA-DR is correctly identified as the most validated single clinical anchor.

【Why it matters】 This is exactly the candour expected of a methods/resource article and should be preserved; no change requested.

---

## § Stands up (verified strengths)

1. **Repositioning honesty is exemplary.** The prednisone positive-control failure (rescue 0.1364, rank 651/20413, 3.19th percentile; `03_results/S08_l1000_positive_control.csv:2`, matching `manuscript.md:137`) is used to declare the L1000 rescue "descriptive only" and explicitly "not supportive evidence" (`manuscript.md:149`). This is the correct, conservative reading.
2. **Membrane mHLA-DR vs HLA-DR mRNA is distinguished correctly.** `manuscript.md:85` states the HLA-class-II / CD74 *mRNA* down-regulation is a transcript-level proxy and "should not be equated with monocyte membrane mHLA-DR … complementary, not interchangeable." Accurate and important.
3. **FIS1 direction/magnitude verified and erythroid reasoning biologically plausible.** `03_results/S01_mars1_deg.csv:3716` FIS1 logFC +1.2614, t +17.157, Mars1-up, exceeds every hub gene's |logFC| (max hub |logFC| = CD14 0.7657) — consistent with "exceeds that of any hub gene" (`manuscript.md:101`). The erythroid-module (2011) / reticulocyte-mitophagy interpretation is a defensible inference from co-expression.
4. **All recomputed DEG tallies match exactly.** Mars1-vs-Other DEG_0.3 = 3597; sepsis-vs-healthy DEG_0.3 = 448; consensus immune genes 23/25 directionally down, 22/25 significant (FDR<0.05), 21 both down+significant (`03_results/S01_immunoparalysis_direction.csv` lines 2–26; matches `manuscript.md:67`, `manuscript.md:188`).
5. **Mortality / endotype counts internally consistent** (GSE65682_pheno.csv crosstab; `manuscript.md:31`, `manuscript.md:85`) — no arithmetic discrepancy.
6. **Clinical-translation caveats presented fairly** (Issue 6 above).

---

## § Questions for the authors

1. Is FIS1's erythroid module 2011 independently associated with 28-day death in GSE65682 *and* in E-MTAB-4451 — i.e., is the erythroid program a standalone prognostic axis separate from the antigen-presentation axis? (Motivated by `03_results/S06_hub_death_association.csv:2`, p=0.00735.)
2. Was any independent cohort carrying *externally assigned* Mars1 labels available to replicate the hub/endotype claim, or is the recapitulation strictly within-cohort? (`manuscript.md:14`, `manuscript.md:147`.)
3. Please reconcile §3.7's "the two lowest are significantly below it" with the binomial P(X≥k) ≥ 0.82 for all seven reported in the same paragraph (`manuscript.md:115`).
4. Is 90-day mortality truly absent in both GSE65682 and E-MTAB-4451, and would you expect the signature AUC to rise at 90 days given the late-death biology of immunoparalysis?

---

## § What I actually checked

**Files read (full or targeted):** `05_reports/manuscript.md` (281 lines, full); `03_results/S01_mars1_deg.csv` (header + targeted gene rows); `03_results/S01_immunoparalysis_direction.csv` (full, 26 lines); `03_results/S05_hub_genes.csv` (full, 7 lines); `03_results/S06_hub_death_association.csv` (full, 7 lines); `03_results/S08_l1000_candidate_scores.csv` (full); `03_results/08_candidates_drugs.csv` (full); `03_results/S08_l1000_positive_control.csv` (full); `01_data/GSE65682/GSE65682_pheno.csv` (full, 802 rows). No `06_review/` file, no `REVIEW_*.md`/`RESPONSE_*.md`, no `CITATION.cff`, no author-verification statement, and no co-reviewer file was read.

**Recomputation performed (pandas):** (i) Mars1-vs-Other DEG_0.3 count = 3597, DEG_1.0 = 186; (ii) sepsis-vs-healthy DEG_0.3 = 448; (iii) per-gene logFC / t / adj.P / DEG flags for CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1; (iv) hub direction tally = 5 down / 1 up; (v) immunoparalysis-direction tally = 23 down / 22 sig / 21 both; (vi) death×endotype crosstab from phenotype; (vii) percentile checks: prednisone 651/20413 = 3.19% (≈3.2nd), lenalidomide 5435/20413 = 26.6%, azithromycin 9152/20413 = 44.8%.

**Discrepancies stated:** No numeric discrepancy in recomputed magnitudes. Manuscript figures match source to ≤0.01: FIS1 logFC 1.2614 vs "+1.26"; t 17.157 vs "+17.2"; CD74 −0.7578 vs "−0.76"; FCGR3A −0.6097 vs "−0.61"; HAVCR2 −0.3488 vs "−0.35"; DEG counts 3597 / 448 exact; 23/22/21 exact; prednisone percentile 3.19 ≈ "3.2nd". The only mismatches are *interpretive*, not numeric: (a) FIS1 labelled "passenger" despite `S06_hub_death_association.csv:2` showing significant independent death association (p=0.00735); (b) §3.7 "significantly below" contradicts its own binomial P(X≥k) ≥ 0.82 for all seven.
