# Independent peer review — Layer: Clinical sepsis / immunology (Domain)

**Manuscript:** *Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning* (single-author, v1.1.0)
**Reviewer layer:** A1 — Domain (clinical sepsis / immunology)
**Review type:** Fresh first-submission review (Round-2 dispatch; prior round not read, per independence discipline)

This review judges only the clinical/biological framing, the biological coherence of the hub genes and drug shortlist, the appropriateness of clinical hedging, and literature gaps. All numbers I cite were re-extracted or recomputed from the source CSVs in `03_results/`; discrepancies with the manuscript are stated explicitly.

---

## §1. Major issues

### Issue 1 — FIS1 does not belong to the antigen-presentation / monocytic / exhaustion hub theme the paper asserts

【Problem】 FIS1 is a mitochondrial-fission protein, not an antigen-presentation, monocytic, or exhaustion gene, so the manuscript's claim that all six hubs "parsimoniously recapitulate the Mars1 program" of those three functional classes is overstated.

【Evidence】 `manuscript.md:103` (§3.3): "All are antigen-presentation / monocytic / exhaustion-axis genes, so the hub parsimoniously recapitulates the Mars1 program." `03_results/S05_hub_genes.csv` confirms FIS1 is a hub (lasso/rf/univariate all `True`). `03_results/S04_candidate_genes.csv` (FIS1 row) shows `in_immune_set=False`, `in_mars1_deg=True` — i.e., FIS1 is a Mars1 DEG but is explicitly *outside* the consensus immune gene set, unlike the other five hubs (all `in_immune_set=True`). FIS1 (fission mitochondrial 1) is an outer-mitochondrial-membrane protein driving mitochondrial division.

【Why it matters】 The 6-gene hub is the central biological object of the paper. Asserting a coherent antigen-presentation/monocytic theme that one member violates undermines the "parsimonious" claim, and it lets the causal/MR narrative extend onto a gene with no established immunoparalysis link: §3.10 groups FIS1 with the other four as one of the "four of five hubs [that] returned protective estimates concordant across all three methods," even though FIS1's MR estimate (OR 0.964, P=0.46) is null and its biological tie to immunoparalysis is speculative.

【Specific fix】 Either (a) rephrase §3.3 to: "Five hubs (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) map to antigen-presentation, monocytic and exhaustion programs; FIS1 is a mitochondrial-fission gene recovered by co-expression, which we interpret as an immune-metabolic / mitochondrial-dysfunction component of the Mars1 program (cite mitochondrial dysfunction in sepsis immunosuppression)"; and add a one-paragraph FIS1 rationale in §3.3 and §5; or (b) drop FIS1 from the hub/MR and report it only as a co-expression outlier. Also rewrite the §3.10 "four of five hubs" sentence so FIS1's null protective MR estimate is not presented as reinforcing the immune-program story.

### Issue 2 — ITGAM is labelled "not significant at FDR<0.05" but its own adj.P is 1.7×10⁻³ and it is counted among the significant genes

【Problem】 Table 1 labels ITGAM "not significant at FDR<0.05" even though the adj.P it reports (1.7×10⁻³) is below 0.05, and ITGAM is in fact one of the 22 FDR-significant genes in §3.1 — an internal contradiction and a likely threshold-confusion error.

【Evidence】 `manuscript.md:92` Table 1: "ITGAM | −0.21 | 1.7e-03 | integrin αM (not significant at FDR<0.05)". `03_results/S01_immunoparalysis_direction.csv` ITGAM row: `adj.P.Val = 0.0016773155724580273` (<0.05), `direction = Mars1_down`. `DEG_0.3 = False` (|logFC|=0.208 < 0.3), so ITGAM fails the |logFC|≥0.3 DEG threshold but *is* FDR-significant. §3.1 (`manuscript.md:82`) states 22 genes are FDR<0.05 significant — a count that includes ITGAM (it is the 18th FDR-significant row in the CSV).

【Why it matters】 A self-contradictory significance label in the primary directionality table signals the author may be conflating the |logFC|≥0.3 DEG filter with the FDR threshold, which undermines confidence in the otherwise-clean directionality results and internally conflicts with the §3.1 narrative count.

【Specific fix】 In Table 1 (manuscript.md:92) change the ITGAM note to: "FDR-significant (adj.P = 1.7×10⁻³) but below the |logFC|≥0.3 DEG threshold (not called a DEG)."

### Issue 3 — CD14 MR-Egger BH-FDR is reported as 0.026 but the source CSV stores 0.0766, and the "15" denominator is inconsistent

【Problem】 The reported BH-FDR for the CD14 MR-Egger estimate (0.026) does not match the value stored in the source CSV (0.0766), and the stated "15 gene × outcome" test set cannot reproduce 0.026.

【Evidence】 `manuscript.md:146` and `manuscript.md:190`: "BH-FDR 0.026 across all 15 gene × outcome MR-Egger tests." `03_results/10_genetics_mr_outcome5086_28ddeath.csv` → CD14 MR-Egger row `p_fdr_bh = 0.0766434945255301`. Recomputing BH across the 15 primary-outcome tests (5 genes × 3 methods) gives 0.0766; BH across the 5 primary-outcome Egger tests alone gives 0.0256 ≈ 0.026. Thus 0.026 is only reproducible from a 5-test set, not the stated 15. Raw CD14 Egger values match the manuscript (OR 0.90595, P 0.0051096, intercept P 0.344).

【Why it matters】 The causal-support layer leans on CD14 as the single nominally-significant, pleiotropy-robust signal; an understated/incorrect FDR value overstates how strongly it survives multiplicity control and is a transparency defect against the paper's own provenance table (§7).

【Specific fix】 Either report the CSV value (BH-FDR = 0.077 across the 15 primary-outcome tests) or explicitly state the BH set used (5 Egger tests within the primary outcome) and correct "15 gene × outcome" to the actual set. Keep the "suggestive only" interpretation since 0.077 < 0.10.

### Issue 4 — HAVCR2/TIM-3 direction contradicts the "exhaustion-axis" hub narrative

【Problem】 HAVCR2 is presented as a hub "exhaustion-axis gene" yet is down-regulated in Mars1 (−0.35), whereas the manuscript's exhaustion signal rests on PDCD1/LAG3 being up-regulated — an internal directional inconsistency.

【Evidence】 `manuscript.md:103` (hub "exhaustion-axis genes"); `manuscript.md:82` lists HAVCR2 Δ=−0.35 (Mars1_down) while PDCD1 is the up-regulated exhaustion marker (Δ=+0.16). `03_results/S01_immunoparalysis_direction.csv`: HAVCR2 `direction = Mars1_down`, PDCD1 `direction = Mars1_up`, LAG3 `direction = Mars1_up` (adj.P=0.55, not significant). §2.8/§3.9 define PDCD1 and LAG3 as the Mars1-up exhaustion markers.

【Why it matters】 TIM-3 is a co-inhibitory receptor canonically associated with *up*-regulated T-cell exhaustion; its downregulation here sits awkwardly with the "T-cell exhaustion superimposed on antigen-presentation failure" story and can confuse readers about which direction the exhaustion axis takes in Mars1.

【Specific fix】 In §3.3 clarify that the exhaustion component of the hub is represented by a *down*-regulated co-inhibitory receptor (HAVCR2), while the *up*-regulated exhaustion signal in Mars1 is carried by PDCD1/LAG3, and explicitly note the directional split rather than implying HAVCR2 is "up" as an exhaustion marker.

### Issue 5 — "Therapeutically targetable" overstates the evidence in the Abstract and Conclusion

【Problem】 The Abstract and Conclusion call the hub genes "therapeutically targetable," a stronger claim than the body supports, where only two small molecules show modest L1000 rescue and no functional validation exists.

【Evidence】 `manuscript.md:14` (Abstract EN: "simultaneously prognostic and therapeutically targetable"); `manuscript.md:207` (Conclusion: "therapeutically targetable"). §3.9 (`manuscript.md:137`) reports azithromycin ≈ median (rank 9,152/20,413; wtcs 0.0626) and lenalidomide top 26.6% (wtcs 0.2058) — "modest," and the glucocorticoid caveat shows rescue ≠ functional restoration; §5 limitations 6/9 state functional validation is a blueprint only.

【Why it matters】 "Therapeutically targetable" implies druggability/validation the data do not establish; it risks over-claiming in the most-read sections and contradicts the otherwise careful hedging.

【Specific fix】 Replace "therapeutically targetable" with "candidate therapeutic anchors" or "hypothesised therapeutic targets" at `manuscript.md:14` and `manuscript.md:207`; retain "with functional validation still required."

### Issue 6 — Abstract "methodological positive-control gate" language can be read as overstating validation

【Problem】 The Abstract presents the IFN-γ ≥3/5 gate as a "methodological positive-control gate," but the manuscript itself states this gate only verifies a curated prior, not an independent perturbation control.

【Evidence】 `manuscript.md:14` (Abstract EN: "satisfying the methodological positive-control gate"); `manuscript.md:64` (§2.8: "consistency/sanity checks on the curated priors, not independent perturbation controls"); `manuscript.md:198` (limitation 9: "the method-positive gate is non-independent").

【Why it matters】 Readers scanning the Abstract may credit the drug shortlist with a validation step it does not have, weakening the paper's honest framing elsewhere.

【Specific fix】 At `manuscript.md:14` rephrase to: "satisfying a non-independent sanity check on the curated response-gene priors (method-positive gate, not an independent perturbation control)."

### Issue 7 — IFN-γ "5/5" (Abstract) vs Table 2 "5/7" denominator can be conflated

【Problem】 The Abstract states IFN-γ "rescued 5/5 antigen-presentation genes" while Table 2 reports its response_gene_concordance as 5/7; the two denominators can be conflated.

【Evidence】 `manuscript.md:14` and `manuscript.md:25` (Abstract) "5/5 antigen-presentation genes"; `manuscript.md:117`/`125` (Table 2) show IFN-γ n_rescue/n_target = 5/7, concordance 0.71. `03_results/08_candidates_drugs.csv` IFN-γ `rescue_genes = HLA-DRA;HLA-DRB1;HLA-DQA1;HLA-DQB1;CD74` (5 of 7 curated genes, all 5 being AP genes).

【Why it matters】 The 5/5 refers to AP genes *within* IFN-γ's 7-gene curated set; without explicit cross-reference a reader may think the overall concordance is 5/5, overstating the metric.

【Specific fix】 In the Abstract specify "rescued 5/5 of its antigen-presentation genes (5/7 overall curated-response concordance)."

### Issue 8 — Must-cite literature gaps in sepsis immunoparalysis / endotype

【Problem】 The 31-reference list omits the canonical clinical immunoparalysis biomarker literature (monocytic HLA-DR) and recent immunostimulant/MARS-endotype-validation work that would anchor and contextualise the central claims.

【Evidence】 References 1–31 (`manuscript.md:258–288`) include Scicluna 2017 (MARS endotype), Hotchkiss 2013, van der Poll 2017, but contain no dedicated citation for monocyte HLA-DR (mHLA-DR) as the established clinical immunoparalysis biomarker, no recent (post-2011) systematic review of immunostimulants in sepsis beyond Bo 2011 (ref 30), and no external-validation/generalizability study of the MARS endotypes.

【Why it matters】 The paper's core inference ("Mars1 = immunoparalysis") is a transcriptomic proxy for a functionally defined state; citing the mHLA-DR biomarker literature would ground that inference in clinically validated evidence and pre-empt the reviewer question of whether downregulated HLA-II *transcripts* equal functional immunoparalysis. A recent immunostimulant RCT overview would better support the §3.8 readiness tiering than the 2011 meta alone.

【Specific fix】 Add: (a) a citation on monocyte HLA-DR as a clinical immunoparalysis biomarker (e.g., Monneret G, Venet F — monocytic HLA-DR expression in sepsis diagnosis/prognosis) in §1/§3.1; (b) a recent (2020s) systematic review/meta-analysis of immunostimulatory agents (IL-7/GM-CSF/IFN-γ) in sepsis to update §3.8 beyond Bo 2011; (c) a MARS-endotype external-validation/generalizability study (endotype derivation/validation in independent ICU cohorts) to support that Mars1's immunosuppressed classification generalises.

---

## §2. Stands up (things I suspected but found correct)

1. **The immunoparalysis directionality signal is real and accurately reported.** `03_results/S01_immunoparalysis_direction.csv`: 23/25 Mars1_down, 22 FDR<0.05 (including PDCD1 up; 21 down+significant) — exactly as stated. Named-gene values match to full precision: HLA-DRB1 −0.8925 (adj.P 1.07×10⁻¹⁵), CD74 −0.7578 (2.08×10⁻¹⁵), CD14 −0.7657 (≈0), FCGR3A −0.6097 (9.05×10⁻¹¹). The antigen-presentation/monocytic downregulation that defines "immunoparalysis" here is genuinely present in these data.

2. **Drug repositioning is honestly scoped as hypothesis-generating.** §2.8 defines `response_gene_concordance` as a curated-response-gene overlap, *not* a direct-target overlap; `03_results/08_candidates_drugs.csv` confirms `rescue_genes` are curated response genes; §3.9 confines unbiased L1000 connectivity to 2/7 candidates; §5 limitation 9 states the positive gate is non-independent. This is methodologically honest, not over-claimed — a genuine strength.

3. **Clinical hedging is appropriate throughout.** §3.8 cites opposing evidence (Bo 2011 meta: no mortality benefit for G-CSF/GM-CSF); §4 explicitly states the stratification hypothesis "requires prospective testing, not a treatment recommendation"; MR is uniformly presented as hypothesis-generating with the eQTLGen×UKB sample-overlap limitation disclosed (§2.10, §5).

4. **External-validation numbers are correctly reported and honestly caveated.** `03_results/09_external_validation.csv`: orientedSum AUC 0.6382 (95% CI 0.5317–0.7475) = the primary fixed-orientation external metric; locked L1-weight AUC 0.5848 (CI 0.4687–0.6959); IRG benchmark recomputed 0.604. The manuscript reports both and correctly admits the learned weights did not transport.

5. **MR point estimates and instrument counts trace to source.** `03_results/10_genetics_mr_outcome5086_28ddeath.csv`: CD14 MR-Egger OR 0.90595, P 0.0051, intercept P 0.344 (matches manuscript); per-gene nSNP (CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8) exactly matches the retained rows in `03_results/10_genetics_mr_outcome5086_harmonised.csv`.

6. **LINCS L1000 rescue values are correct.** `03_results/S08_l1000_candidate_scores.csv`: azithromycin wtcs 0.0626 (rank 9,152/20,413), lenalidomide wtcs 0.2058 (rank 5,435/20,413) — matching §3.9, and *not* the 1.17 trap. The query (22 L1000-measurable genes = 20 Mars1-down + PDCD1/LAG3 up) and the HAVCR2/FCGR3A L1000-absence exclusion are correctly described.

---

## §3. Questions for the authors (do not guess answers)

1. FIS1 is the only hub absent from the consensus immune gene set (`S04_candidate_genes.csv` `in_immune_set=False`) and is a mitochondrial-fission gene. What biological rationale links FIS1 to the Mars1 immunoparalysis program, and was its Mars1-down directionality verified independently (it is not in the 25-gene `S01` table)? Should FIS1 be retained as a hub or reported as a co-expression outlier?
2. Table 1 labels ITGAM "not significant at FDR<0.05" while its adj.P is 1.7×10⁻³ (<0.05) and it is counted among the 22 significant genes in §3.1. Is this a |logFC| filter note mistyped as an FDR note, or a different threshold? Please confirm the intended label.
3. The CD14 MR-Egger BH-FDR is reported as 0.026 "across all 15 gene × outcome MR-Egger tests," but the primary-outcome CSV stores `p_fdr_bh = 0.0766`, and 0.026 is only reproducible from a 5-test (primary-outcome Egger) BH. Which test set was actually used, and can the manuscript be made consistent with the provenance CSV?
4. Can the authors point to the explicit STROBE-MR harmonisation exclusion tallies (palindromic / strand-ambiguous / allele-incompatible counts per gene)? The `*_harmonised.csv` files I read list retained SNPs but I did not find explicit exclusion-count columns; §2.10 claims these are "itemised," so their location should be verifiable.
5. The sample-count provenance (802 samples; 479 with assigned MARS endotype; Mars1=132) was not independently verifiable from the CSVs I was asked to check. Can the authors confirm these against `01_data/GSE65682` phenotypes, and clarify how the 323 "unassigned" samples were handled in the endotype analyses?

---

## §4. What I actually checked (files read, values recomputed, discrepancies)

**Files read (manuscript + source CSVs only; no forbidden files opened):**
- `manuscript.md` (full, 288 lines)
- `03_results/S01_immunoparalysis_direction.csv`
- `03_results/S06_auc_compare.csv`
- `03_results/09_external_validation.csv`
- `03_results/08_candidates_drugs.csv`
- `03_results/08b_clinical_translation.csv`
- `03_results/S08_l1000_candidate_scores.csv`
- `03_results/S05_hub_genes.csv`
- `03_results/S04_candidate_genes.csv`
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv`
- `03_results/10_genetics_mr_outcome5086_harmonised.csv`

**Values recomputed vs manuscript and result:**
- Directionality (`S01`): 23/25 Mars1_down; 22 FDR<0.05 (incl. PDCD1 up); 21 down+significant — **matches** manuscript §3.1. Named-gene logFC/adj.P match exactly.
- AUC (`S06`): CV 0.6586→0.659 ✓; train 0.7495→0.750 ✓; IRG 0.619/0.648 ✓.
- External (`09`): orientedSum 0.6382 (CI 0.5317–0.7475) ✓; locked L1 0.5848 (CI 0.4687–0.6959) ✓; IRG recomputed 0.604 ✓.
- Drugs (`08`): fractions 1.0/0.833/0.714/0.667/0.40/0.40/0.20 = 5/5,5/6,5/7,2/3,2/5,2/5,1/5 — **match** Table 2; IFN-γ rescue_genes = 5 AP genes — **matches** "5/5 antigen-presentation."
- L1000 (`S08_l1000_candidate_scores`): azithromycin wtcs 0.0626, lenalidomide wtcs 0.2058 — **match** §3.9 (not 1.17).
- MR (`10_..._28ddeath`): CD14 Egger OR 0.90595, P 0.0051, intercept P 0.344 — **match** Table 3; per-gene nSNP matches harmonised retained rows.

**Discrepancies stated:**
- (a) **ITGAM**: Table 1 "not significant at FDR<0.05" is wrong — `S01` adj.P.Val = 0.001677 (<0.05); ITGAM is also counted among the 22 significant genes in §3.1. Internal contradiction.
- (b) **CD14 BH-FDR**: manuscript reports 0.026 "across 15"; source CSV stores `p_fdr_bh = 0.0766`; 0.026 only reproduces from a 5-test BH. Inconsistent with provenance.

**Not verified (out of scope of provided CSVs / not found):**
- Sample counts 802 / 479 / Mars1=132 against raw `01_data/GSE65682` phenotypes (no pheno CSV was among the mandatory checks; recommend author confirmation).
- Explicit STROBE-MR exclusion-tally columns (palindromic/strand/allele-incompatible) — not present as columns in the harmonised CSV I read; §2.10 claims they are "itemised," so their storage location should be made verifiable.
- Critical-care/susceptibility MR numeric details (Table 4) were not independently recomputed; primary-outcome estimates and instrument counts were verified, and Table 4 values are internally consistent with the primary file.
