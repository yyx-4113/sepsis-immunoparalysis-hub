# Reviewer A1 — Domain expert (sepsis immunology / critical-care clinician-scientist)

**Manuscript under review:** "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and externally evaluates a 30-gene sepsis prognostic signature" (v1.20.0; BMC Medical Genomics, Article / methods-and-resources).
**Reviewer role:** Domain. I assessed (i) correctness of the immunoparalysis / Mars1 biology, (ii) must-cite literature for a sepsis-immunology domain editor, (iii) whether any clinical claim is false or overstated, and (iv) whether the "confirm/validate" framing honestly matches what was actually done.
**Independence note:** Treated as a first submission. I read only `05_reports/manuscript.md`, the `03_results/*.csv` files, and recomputed selected values locally; I did not read any prior review/response/revision files, manifests, or the other reviewers' reports.

---

## Summary verdict (domain)

The analytical hygiene is genuinely strong for a single-author computational paper: every reported number I spot-checked reproduces to the digit, the authors pre-register the optimistic/portable metrics, and the prednisone L1000 caveat shows real self-awareness. **But the biology framing over-reaches in four places that a sepsis-immunology editor will flag.** The headline claim "confirms the MARS Mars1 immunoparalysis program" is a within-cohort recapitulation (the endotype labels come from the same GSE65682 that defined them), not an independent confirmation; the composite immune score cannot separate Mars1 from Mars2; HAVCR2/TIM-3 is the least-supported of the five hubs yet is labelled a central hub; and the drug "prioritisation" is circular, sits at or below background expectation, and rests on a connectivity metric that is conceptually inverted for the exhaustion component. None of these are fatal, and the authors already caveat most of them — but the **title, abstract, and conclusion currently assert more than the data support**, and that gap must be closed before acceptance.

---

## Major points

### M1. "Confirms the Mars1 immunoparalysis program" is within-cohort recapitulation, not independent confirmation
【Problem】 The study re-analyses GSE65682 using the MARS-consortium endotype labels that were themselves *derived* from GSE65682, so demonstrating that Mars1 genes are down-regulated is largely definitional rather than an independent test of the immunoparalysis hypothesis.
【Evidence】 `manuscript.md:31` states the `mars_endotype` column is taken from GEO characteristics of GSE65682 and `manuscript.md:22` explicitly calls this "the MARS consortium" endotype stratification; the Mars1 biology is therefore read off the same samples that defined Mars1. The external cohort E-MTAB-4451 (`manuscript.md:55`, `manuscript.md:106`) is used *only* for the 30-gene mortality signature — there is no cross-cohort replication of the Mars1 antigen-presentation program anywhere in the paper.
【Why it matters】 The title (`manuscript.md:1`) and abstract (`manuscript.md:14`) sell "confirms the Mars1 immunoparalysis program," implying an external replication that does not exist. A domain editor will read this as a confirmation claim the data cannot carry, and it is the single最容易challenged sentence in the paper.
【Specific fix】 Replace the title/abstract framing with explicit within-cohort language, e.g.:
> "A reproducible pipeline recapitulates the MARS Mars1 immunosuppressed transcriptome in its discovery cohort (GSE65682) and externally evaluates, on an independent cross-platform cohort, a 30-gene sepsis mortality signature."
And in the abstract: "We re-analysed GSE65682 (802 samples) with an auditable multi-omics pipeline that *recapitulates* — within the cohort that defined the endotypes — the Mars1 antigen-presentation/monocytic program, and *independently* evaluates (cohort- and platform-independent, label-dependent) a 30-gene mortality signature on E-MTAB-4451."

### M2. The immune-function score does not distinguish Mars1 from Mars2, so it cannot confirm Mars1-specific immunoparalysis
【Problem】 The composite score is statistically identical in Mars1 and Mars2 (P = 0.47), yet Mars2 is the neutrophilic/hyperinflammatory endotype — so the score is not a Mars1 (immunoparalysis)-specific readout, and the "lowest in Mars1" claim is technically true but non-discriminating.
【Evidence】 `manuscript.md:85` and Table 2: Mars1 median −0.792, Mars2 −0.752, P = 0.47 (versus Mars3 P = 1.9×10⁻¹⁸, Mars4 P = 1.3×10⁻³). I recomputed from `03_results/S02_immunoparalysis_score.csv`: Mars1 median −0.792 (n=132), Mars2 −0.752 (n=176), Mars1-vs-Mars2 Mann–Whitney P = 0.467, Mars1-vs-Mars3 P = 1.85×10⁻¹⁸, Mars1-vs-Mars4 P = 1.32×10⁻³, full range −3.65 to 3.86 — all exactly as reported. The authors themselves write (line 85) that the score "indexes a two-cluster immune gradient common to both low-score endotypes rather than a Mars1-specific signature" and is "partly definitional."
【Why it matters】 The paper's §3.2 headline is "Immune-function score is lowest in Mars1," and the abstract leans on this as confirmation. Because Mars1 ≡ Mars2 on the score, the score cannot be offered as evidence that *Mars1* is the immunoparalysis endotype; the immunoparalysis conclusion actually rests on the individual HLA-II gene directions, not the composite. The current wording invites a reviewer to conclude the confirmation is circular.
【Specific fix】 Re-scope §3.2 and the abstract so the score is presented as a *low-immune-activation gradient shared by Mars1 and Mars2*, explicitly not Mars1-specific, e.g.:
> "The composite immune score separated the low-immune-activation pair (Mars1 and Mars2) from Mars3/Mars4 (both P ≤ 1.9×10⁻¹⁸/1.3×10⁻³) but did not discriminate Mars1 from Mars2 (median −0.79 vs −0.75; P = 0.47), so it indexes a shared low-immune-activation axis rather than a Mars1-specific immunoparalysis signature; Mars1-specific immunoparalysis is therefore established from the direction of individual antigen-presentation genes (§3.1), not from the composite score."

### M3. HAVCR2/TIM-3 is the weakest-supported "hub" yet is branded a central immune hub
【Problem】 HAVCR2 is promoted to one of five immune hubs, but it has the smallest Mars1 effect of the set, is absent from the external 30-gene signature, and is absent from the LINCS L1000 platform — so none of its "hub" status survives any external or connectivity test.
【Evidence】 `03_results/S01_immunoparalysis_direction.csv`: HAVCR2 logFC −0.349 (smallest of the five hubs; CD74 −0.758, HLA-DQA1 −0.530, CD14 −0.766, FCGR3A −0.610), adj.P = 2.8×10⁻¹³. `03_results/S06_signature_genes.csv`: the 30-gene mortality signature contains CD74, HLA-DRB1, FCGR3A, HLA-DQA1, CD14, HLA-DRA, HLA-DMA, HLA-DMB, CD3D/E/G, CD8A/B, IL7R, etc., but **HAVCR2 is not present** — so HAVCR2 contributes nothing to the only externally validated product. `manuscript.md:133` states HAVCR2 is one of the three consensus genes "absent from L1000," so it was never connectivity-scored. Its hub status therefore rests entirely on the discovery-cohort tri-method ML consensus (`03_results/S05_hub_genes.csv`, all three methods = True).
【Why it matters】 Calling a gene a "hub" implies it is a robust, centrality-bearing node. HAVCR2 here is a small-effect, bulk-down checkpoint transcript whose inclusion is driven by the survival-label ML on the same cohort; it is never externally checked. For a clinician-scientist this risks mis-characterising TIM-3 biology: TIM-3/HAVCR2 is canonically an *exhaustion* marker that is *up*-regulated on exhausted T cells, whereas the bulk signal here is *down* — and the manuscript's own rescue metric (M4) would *up*-regulate it, which is the opposite of immune restoration.
【Specific fix】 Either demote HAVCR2 to "a consensus-selected but externally unvalidated exploratory gene" or justify it explicitly, e.g.:
> "HAVCR2/TIM-3 was selected by all three in-cohort selectors but carries the smallest Mars1 effect of the set (logFC −0.35), was excluded from the 30-gene external signature (§3.5) and is absent from the L1000 platform (§3.9); its status as an immune 'hub' is therefore discovery-cohort-internal and should not be read as externally established. We report it as an exploratory, bulk-down checkpoint transcript of uncertain cellular basis rather than a validated immunoparalysis node."

### M4. The drug "prioritisation" is circular, sits at/below background, and the L1000 metric is conceptually inverted for the exhaustion arm
【Problem】 The seven candidates are textbook immunoparalysis agents; the selection metric is below the paper's own background expectation for every candidate; the method-positive gate is tautological; and the LINCS rescue score rewards *up*-regulation of the Mars1-*up* exhaustion markers PDCD1/LAG3, i.e. it pushes the axis in the exhaustion direction.
【Evidence】 `manuscript.md:115` and `03_results/08_candidates_drugs.csv`: expected background concordance = 21/25 = 0.84 (§3.1); every candidate is ≤ 0.84 (IL-7 0.80, GM-CSF 0.667, IFN-γ 0.571, azithromycin 0.667, lenalidomide 0.40, thymosin α1 0.40, BCG 0.20), with one-sided binomial P ≥ 0.82 for all — i.e. none exceeds chance. The IFN-γ gate "rescues 4/5 antigen-presentation genes" (`manuscript.md:115`, `08_candidates_drugs.csv` IFN-γ rescue_genes = HLA-DRA;HLA-DRB1;HLA-DQA1;CD74) is tautological because IFN-γ is the *canonical MHC-II inducer* and the Mars1-down axis *is* MHC-II. `manuscript.md:133–137`: the L1000 query aggregates 22 genes with one sign including PDCD1 and LAG3 (both Mars1-up per `S01_immunoparalysis_direction.csv`: PDCD1 +0.162, LAG3 +0.035), so a compound "rescues" by up-regulating exhaustion markers; and prednisone — a clinical immunosuppressant — scores rescue 0.136, rank 651/20,413 (3.2nd percentile, `03_results/S08_l1000_positive_control.csv`), while the two scored candidates sit at z = +0.56 (lenalidomide) and +0.10 (azithromycin), empirical P = 0.27 and 0.45 (`03_results/S08_l1000_candidate_scores.csv`).
【Why it matters】 The abstract's "Seven immune-modulating agents were prioritised" and §3.7/§4 present the candidates as if the pipeline surfaced them. In reality the pipeline re-ranks known immuno-stimulants and, by its own numbers, does not lift any above background; the connectivity metric is backwards for the exhaustion component and is non-discriminating (an immunosuppressant beats both candidates). The genuine, publishable contribution is the *honest de-prioritisation* (prednisone caveat, noise-band observation), not a candidate list.
【Specific fix】 Reframe §3.7/§4/abstract as hypothesis-annotation, not prioritisation, e.g.:
> "The seven candidates are established immuno-stimulants; under the paper's own immune-gene background (84% of consensus immune genes are Mars1-down) every candidate's response-gene concordance lies at or below expectation (one-sided P ≥ 0.82), so the metric annotates rather than ranks them. The LINCS rescue score is single-direction and rewards up-regulation of the Mars1-up exhaustion markers PDCD1/LAG3; because prednisone — an immunosuppressant — ranks in the 3.2nd percentile on the same axis, the connectivity evidence is descriptive only and does not support the candidates. We therefore present the shortlist as a literature-anchored hypothesis set requiring the S11 functional test, not as prioritised repositioning hits."

### M5. Whole-blood HLA-class-II/CD74 mRNA is used as an immunoparalysis proxy without acknowledging dissociation from monocyte mHLA-DR
【Problem】 The paper equates down-regulated HLA-DR/CD74/HLA-DQA1 *transcript* (whole blood) with the antigen-presentation/immunoparalysis axis, but bedside immunoparalysis is defined by *membrane* monocyte HLA-DR (mHLA-DR) by flow, and mRNA and surface protein can dissociate.
【Evidence】 `manuscript.md:37` builds the score from HLA-II/ T-cell / exhaustion *gene sets*; `manuscript.md:67–80` reports HLA-DRB1/CD74/HLA-DQA1/HLA-DRA as Mars1-down *mRNA*. Limitation 7 (`manuscript.md:164`) says mHLA-DR "remains the canonical, complementary bedside immunoparalysis biomarker and is not replaced by the transcriptomic signature" — but the paper never states the stronger, mechanistic point that whole-blood HLA-II *mRNA* has not been shown to track monocyte *mHLA-DR* in these cohorts, nor cites the flow-cytometry measurement standard it invokes.
【Why it matters】 For a critical-care audience, "antigen-presentation program down" is read as immunosuppression at the protein/membrane level. Presenting mRNA down-regulation as immunoparalysis without the dissociation caveat overstates the clinical parallelism and is exactly the claim a domain editor will ask to soften. The authors already cite Monneret 2008 (#27) and Venet & Monneret 2018 (#29), so the anchor exists — the explicit caveat is missing.
【Specific fix】 Add to Limitation 7 (or §3.1) a direct caveat, e.g.:
> "The antigen-presentation signal reported here is whole-blood *HLA-class-II/CD74* mRNA; monocyte membrane mHLA-DR measured by flow cytometry is the validated bedside immunoparalysis biomarker (Monneret et al., 2008; Venet & Monneret, 2018) and its correlation with whole-blood HLA-II transcript levels in these cohorts is not established. The transcriptomic axis is therefore a proxy for, not a measurement of, monocyte mHLA-DR."

---

## Medium points

### M6. The IL-7 "all four response genes fall below |logFC|≥0.3 in the endotype-only contrast" statement is inaccurate
【Problem】 The manuscript claims all four of IL-7's scored response genes drop below the |logFC|≥0.3 threshold in the Mars1-vs-Mars2–4 contrast, but LCK does not.
【Evidence】 `manuscript.md:115` ("IL-7's four scored response genes (CD3D, CD8A, IL7R, LCK) all fall below the |logFC| ≥ 0.3 DEG threshold in the endotype-only contrast of Supplementary Table S01b"). `03_results/S01b_endotypeonly_sensitivity.csv`: CD3D −0.152 (no), CD8A −0.128 (no), IL7R −0.204 (no), but **LCK −0.404, adj.P = 4.97×10⁻⁵, retains_0.3_FDR05 = yes**. So 3/4 fall below; LCK retains.
【Why it matters】 Minor factual error in a sentence that undercuts IL-7's candidacy; a careful domain reader will check S01b and find the claim overstated, which erodes trust in the surrounding (already cautious) repositioning text.
【Specific fix】 Replace with:
> "Three of IL-7's four scored response genes (CD3D −0.15, CD8A −0.13, IL7R −0.20) fall below |logFC|≥0.3 in the endotype-only contrast, although LCK (−0.40, P = 5.0×10⁻⁵) retains the threshold; IL-7's concordance is therefore only partially maintained there."

### M7. TIM-3/HAVCR2 biology is supported only by a 2024 review; a primary human-sepsis exhaustion citation is expected
【Problem】 HAVCR2/TIM-3 is elevated to a hub, yet the only TIM-3 citation is a 2024 review (Wang et al., #16); the paper's reconciliation of "bulk TIM-3 down but exhaustion markers PD-1/LAG-3 up" needs a primary human-sepsis reference.
【Evidence】 `manuscript.md:67` and `manuscript.md:145` discuss TIM-3 down-regulation versus exhausted-T-cell up-regulation and cite only #16 (Wang 2024, a review). The manuscript itself notes (line 67) "lower TIM-3 mRNA in peripheral blood mononuclear cells has been reported in severe sepsis relative to sepsis [16]" — but [16] is the review, not the primary study it paraphrases.
【Why it matters】 A BMC Medical Genomics domain editor expects primary literature for a gene promoted to hub status, especially where the direction is counter-intuitive (TIM-3 usually reported *up* in exhaustion). Citing the primary human-sepsis TIM-3 study (not just the review) is a must-fix for credibility.
【Specific fix】 Add a primary citation (e.g. a human sepsis TIM-3/PBMC study) wherever the bulk-down TIM-3 claim is made, e.g. replace "[16]" in the "lower TIM-3 mRNA … severe sepsis" sentence with the primary report, and keep #16 as the review. (Confirm the exact primary DOI against PubMed before citing.)

### M8. FIS1 molecular identity / mitochondrial-fission function is asserted with no citation
【Problem】 FIS1 is named in the title, abstract, and conclusion as a "mitochondrial-fission protein," but no reference anchors its molecular function or its mitophagy link.
【Evidence】 `manuscript.md:14` (abstract: "FIS1 (logFC +1.26, up-regulated)"), `manuscript.md:101` and `manuscript.md:178` describe FIS1 as mitochondrial-fission; References list contains no FIS1/Hall/Mozdy/Yoon mitochondrial-fission paper. I verified the direction independently: `03_results/S01_mars1_deg.csv` → FIS1 logFC +1.261, t = +17.16, adj.P = 0 (DEG_0.3 = True) — direction is correct, only the molecular-identity citation is missing.
【Why it matters】 For a gene given abstract-level prominence, the editor will require at least one citation establishing FIS1 as the mitochondrial fission 1 / DRP1-adaptor protein and its role in mitophagy, so the reader can judge the (correctly caveated) erythroid/reticulocyte interpretation.
【Specific fix】 Cite the molecular-identity primary, e.g.:
> "FIS1 (mitochondrial fission 1 protein; Yoon et al., J Cell Biol 2003 — DRP1-adaptor mitochondrial fission; implicated in reticulocyte mitophagy), logFC +1.26, Mars1-up…"

### M9. The "immune-risk/immunoparalysis" signature is a generic mortality signature (it includes neutrophilic/inflammatory genes)
【Problem】 The 30-gene signature mixes antigen-presentation-down genes with clearly inflammatory/neutrophilic genes that are *positively* correlated with death, so it is not immunoparalysis-specific.
【Evidence】 `03_results/S06_signature_genes.csv`: ELANE r = +0.170, MPO r = +0.152, S100A8 r = +0.091 are all *positively* correlated with 28-day death (neutrophil/azurophil/calprotectin markers), alongside the antigen-presentation-down block (CD74 −0.163, HLA-DRB1 −0.162, CD14 −0.141, etc.). The signature is therefore a two-armed mortality risk score.
【Why it matters】 Title/abstract emphasise "immunoparalysis" and "immune-risk"; a clinician reading "immunoparalysis signature" expects an immunosuppression-specific signal. The text is internally honest ("immune-risk signature," §3.4), but the headline framing overstates specificity and invites the inference that the external AUC validates *immunoparalysis* prediction, which it does not.
【Specific fix】 In title/abstract, call it what it is, e.g.:
> "…and externally evaluates a 30-gene sepsis mortality risk signature (dominated by antigen-presentation and monocytic genes but also capturing neutrophilic/inflammatory signals)…"
And add one sentence in §3.4 noting the inflammatory-arm genes (ELANE/MPO/S100A8) make the signature a general mortality, not immunoparalysis-specific, score.

### M10. "Confirm/validate" framing vs the declared article type is internally inconsistent in the headline
【Problem】 The article type (`manuscript.md:8`) correctly says "not novel hub-gene discovery," yet the title and abstract lead with "confirms" and "immune hubs," which reads as a discovery/confirmation claim about biology that the Discussion then walks back to "near-replication."
【Evidence】 `manuscript.md:8` ("not novel hub-gene discovery (see Discussion)"); `manuscript.md:147` ("The five immune hubs largely *recapitulate* … this is a near-replication rather than a novel gene discovery"); but `manuscript.md:1` and `manuscript.md:14` use "confirms" and present five "immune hubs" as the contribution.
【Why it matters】 A methods-and-resources paper is judged on honest scope. The front matter currently promises biological confirmation the body qualifies; tightening the front matter to match the declared article type removes the easiest reject trigger.
【Specific fix】 Align the title with the article-type statement, e.g.:
> "A reproducible, auditable pipeline recapitulates the MARS Mars1 antigen-presentation program and externally evaluates a 30-gene sepsis mortality signature: a methods-and-resources report."

---

## Minor / clarifying points

### M11. Risk of misreading the within-cohort CV AUC (0.659) as a second external cohort
【Problem】 The abstract lists the 0.659 AUC next to the 0.638 external result; a reader (and the summary brief) may infer a "second cohort" at AUC 0.659, but 0.659 is the *within-cohort* 5-fold CV on GSE65682.
【Evidence】 `manuscript.md:14` ("Within-cohort cross-validated AUC was 0.659 (optimistic)") and `03_results/S06_auc_compare.csv` (Immune-risk signature (CV) 0.6586; train 0.7495). No second external cohort exists — the only external cohort is E-MTAB-4451 (n=106, AUC 0.638). I found no second external-validation block in the manuscript or `03_results/`.
【Why it matters】 Prevents a scope inflation where the optimistic CV is mistaken for independent replication.
【Specific fix】 Keep "within-cohort" qualifier adjacent to 0.659 wherever it appears, and avoid any phrasing that pairs it with the E-MTAB-4451 result as if it were a second independent cohort.

### M12. FIS1 "co-expression passenger" claim should be backed by explicit module-membership evidence
【Problem】 FIS1 is reported as a co-expression passenger outside the immune axis (module 2011, erythroid/heme), but I could not independently verify its WGCNA module assignment from the deposited CSVs I read.
【Evidence】 `manuscript.md:101` states FIS1 is in module 2011 with GATA1/KLF1/ALAS2/FECH/… and that none of the five hubs share that module; the supporting file `03_results/S03_modules.csv` / `S03_key_module_genes.csv` is large and I did not fully parse it. The claim is plausible and consistent with FIS1's Mars1-up direction, but the explicit module-membership table should be surfaced.
【Why it matters】 If the module assignment is wrong, FIS1 could be mis-labelled as a passenger; the authors should make the evidence one click away.
【Specific fix】 Add a short supplementary panel (or a row in S05) showing FIS1's module ID and the absence of the five hubs from module 2011, citing `03_results/S03_modules.csv`.

---

## § Stands up (claims I suspected were weak but verified as correct)

1. **The immunoparalysis direction counts are exact and honest.** I recomputed from `03_results/S01_immunoparalysis_direction.csv`: 23/25 consensus immune genes directionally Mars1-down, 22/25 FDR-significant (including PDCD1 up), 21 down *and* significant — exactly as stated (`manuscript.md:67`, `manuscript.md:189`). The "21 both down and significant" phrasing is precise, not rounded up.
2. **FIS1 is genuinely Mars1-up and strong (not a mis-labelled immune gene).** `03_results/S01_mars1_deg.csv`: FIS1 logFC +1.261, t = +17.16, adj.P = 0, DEG_0.3 = True — the largest Mars1 effect in the paper. Its correct identification as a non-immune, erythroid/heme passenger is a real strength.
3. **The endotype-only robustness claim holds for the myeloid/APC hubs.** `03_results/S01b_endotypeonly_sensitivity.csv`: CD14 (−0.771), HLA-DRB1 (−0.591), CD74 (−0.485), HLA-DMA (−0.617), FCGR3A (−0.555), HAVCR2 (−0.389) all retain |logFC|≥0.3 and FDR<0.05 when Mars1 is compared only with Mars2–4 — exactly as the Discussion asserts (`manuscript.md:145`). This is the most defensible biology in the paper.
4. **Every immune-score statistic I recomputed reproduces to the digit.** From `03_results/S02_immunoparalysis_score.csv`: Mars1 median −0.792, Mars2 −0.752, Mars3 0.64, Mars4 −0.235; Mars1-vs-Mars2 P = 0.467, vs Mars3 1.85×10⁻¹⁸, vs Mars4 1.32×10⁻³; full range −3.65 to 3.86; assigned-endotype range −3.65 to 2.95 — all match `manuscript.md:85` / Table 2. The pre-registered "portable vs optimistic" metric split is trustworthy.
5. **The external-validation numbers are exactly as reported and honestly scoped.** `03_results/09_external_validation.csv`: oriented-sum AUC 0.6382 (95% CI 0.5317–0.7475), locked-L1 AUC 0.5848 (CI 0.4687–0.6959); `03_results/S06_auc_compare.csv`: CV 0.6586, train 0.7495. The authors do not hide that the CI of the locked-L1 includes 0.5 and that the primary external metric is the equal-weight score — commendable.
6. **The prednisone/dexamethasone positive-control discrepancy is a genuine, well-handled self-check.** `03_results/S08_l1000_positive_control.csv`: prednisone rescue 0.136 (rank 651, 3.2nd percentile) while dexamethasone 0.0315 (rank 6,808, 33.4th percentile). Recognising that an immunosuppressant scores high on the "rescue" axis and thereby disqualifies the metric as supportive evidence is exactly the analytical humility a domain reviewer wants to see.

---

## § Questions for the authors (I do not assume; please answer)

1. **External test of Mars1 biology.** Was E-MTAB-4451 ever assigned MARS (Mars1–4) endotype labels, or only the SRS endotypes? My reading is that the Mars1 antigen-presentation program is *never* tested in an independent cohort — only the 30-gene mortality signature is. Please confirm, and if any cross-cohort Mars1 replication exists, show it; otherwise please soften the "confirm" language per M1.
2. **mRNA vs mHLA-DR correlation.** Do you have, or can you cite, any evidence correlating whole-blood HLA-DR/CD74 *mRNA* with monocyte membrane *mHLA-DR* in GSE65682 or E-MTAB-4451? If not, please add the dissociation caveat (M5).
3. **Why retain HAVCR2 as a hub.** Given HAVCR2 is the smallest-effect hub, is absent from the external signature, and absent from L1000 (M3), what justified keeping it among the five "immune hubs" rather than reporting it as exploratory? Was any stability/permutation check run for hub membership?
4. **Gene selection inside or outside the CV loop.** The 30-gene list was selected by |r| with 28-day death and oriented on the same labels (`manuscript.md:46`, `manuscript.md:104`). Was gene selection performed *inside* the 5-fold CV loop or *outside* it? If outside, the EPV caveat (114/30 ≈ 3.8) and the optimism are even larger than stated; please clarify the procedure.
5. **SRS benchmark provenance.** `manuscript.md:157` reports the SRS endotype classifying E-MTAB-4451 mortality at AUC 0.610 (SRS1 24/37, SRS2 28/69). Is this SRS assignment from the published Davenport et al. calls or recomputed by you? Please state the source so the ΔAUC comparison is auditable.
6. **FIS1 module evidence.** Please surface the explicit WGCNA module-membership table showing FIS1 in module 2011 and the five hubs outside it (M12), or correct the module assignment if my reading of `S03_modules.csv` differs.

---

## § What I actually checked

**Files read (allowed set only):**
- `05_reports/manuscript.md` (full).
- `03_results/S01_immunoparalysis_direction.csv` — verified 23/25 down, 22 sig, 21 down+sig; HAVCR2 −0.349; PDCD1 +0.162; LAG3 +0.035 (ns).
- `03_results/S01b_endotypeonly_sensitivity.csv` — verified the six myeloid/APC hubs retain |logFC|≥0.3 & FDR<0.05 vs Mars2–4; LCK −0.404 retains (contradicts M6 claim).
- `03_results/S05_hub_genes.csv` — confirmed the 6 hub genes (FIS1, HAVCR2, HLA-DQA1, CD14, FCGR3A, CD74), all three methods True.
- `03_results/S02_immunoparalysis_score.csv` — recomputed medians and Mann–Whitney P-values (see § Stands up #4); exact match.
- `03_results/S06_signature_genes.csv` — confirmed HAVCR2 absent; confirmed ELANE/MPO/S100A8 inflammatory genes positively correlated with death (M9).
- `03_results/S06_auc_compare.csv` — CV 0.6586, train 0.7495, Mars1 0.5782 (match).
- `03_results/09_external_validation.csv` — oriented-sum 0.6382 (CI 0.5317–0.7475), locked-L1 0.5848 (CI 0.4687–0.6959) (match).
- `03_results/08_candidates_drugs.csv` — verified concordance fractions and binomial P vs the 0.84 background (M4).
- `03_results/S08_l1000_candidate_scores.csv` and `03_results/S08_l1000_positive_control.csv` — verified lenalidomide/azithromycin rescue ranks and prednisone 3.2nd-percentile (M4).
- `03_results/S01_mars1_deg.csv` — verified FIS1 logFC +1.261, t +17.16 (M8 direction).

**Values recomputed locally (command form, not from any prior review):**
- Immune-function score medians + Mars1-vs-{Mars2,Mars3,Mars4} Mann–Whitney U from `S02_immunoparalysis_score.csv`: Mars1 −0.792 / Mars2 −0.752 / Mars3 0.64 / Mars4 −0.235; P = 0.467 / 1.85×10⁻¹⁸ / 1.32×10⁻³; range −3.65–3.86. Exact match to manuscript.
- Per-endotype 28-day mortality + OR from `S02_immunoparalysis_score.csv`: Mars1 45/132 = 34.1%, Mars2–4 69/347 = 19.9%, OR = 2.08 — exact match to `manuscript.md:85`.

**Discrepancies / inaccuracies found:**
- M6: "IL-7's four response genes all fall below |logFC|≥0.3 in endotype-only" is false for LCK (retains, S01b line 10).
- M1/M10: "confirms the Mars1 immunoparalysis program" is not backed by any independent cohort; it is within-GSE65682 recapitulation.
- No other numeric discrepancy; the reported statistics are internally consistent and reproducible.

**Not verified (out of scope of files I read):** WGCNA module membership of FIS1 (M12); the SRS-label source for the E-MTAB-4451 benchmark (Q5); whether gene selection was inside the CV loop (Q4). These require author clarification, not assumption.

**Independence:** I did not open any `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `*_gen_*.py`, `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, or the other reviewers' (`A2_*.md`, `A3_*.md`, `A4_*.md`) files. All judgements above are from the manuscript and the result CSVs I read directly.
