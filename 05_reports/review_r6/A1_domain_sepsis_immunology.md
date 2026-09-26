# Reviewer A1 — Clinical & domain review (critical care medicine / sepsis immunology)

**Manuscript:** `05_reports/manuscript.md` (v1.5.0, 288 lines)
**My lens:** biological and clinical validity — MARS endotype framing, hub-gene immunology, direction-of-effect logic, clinical-trial plausibility, must-cite literature, translational honesty, cell-type coherence.
**Independence:** I read only the manuscript, the panel brief, `03_results/`, `04_figures/` and the literature. No prior-round file, author response, or other reviewer output was read.

Overall impression up front: the Tier-1 observation (Mars1 shows down-regulated antigen presentation and lymphocyte/monocyte transcripts) is real and reproduces established biology, and the authors have been unusually careful with statistics caveats. The paper's problem is not arithmetic; it is that **(i) three of its headline biological claims are confounded by whole-blood cell composition and by a non-immune co-expression module that the paper never unpacks, and (ii) one of its clinical claims is out of date by a pivotal randomised trial.** Both are fixable with 2–3 new analyses and a rewritten §3.8.

---

## 1. Findings

### F1 · Tier 0 — The "Mars1-down immunoparalysis axis" is not separable from circulating-cell depletion, and the paper never addresses the alternative explanation

**【Problem】** Every result downstream of §3.1 is equally consistent with "fewer monocytes and lymphocytes in the blood of Mars1 patients" as with "per-cell immune dysfunction", and the manuscript does not state, test, or even name this alternative.

**【Evidence】** `S01_immunoparalysis_direction.csv` (recomputed, n=25 genes): alongside the MHC-II/monocyte genes, **every lymphocyte-restricted transcript in the panel is down** — CD3D Δ=−0.436, CD3E Δ=−0.216, CD3G Δ=−0.564, LCK Δ=−0.640, CD8A Δ=−0.321, CD8B Δ=−0.136, IL7R Δ=−0.596, GZMA Δ=−0.209 (adj.P=0.110), GZMK Δ=−0.309. Simultaneously the *other* exhaustion markers are also down: HAVCR2 Δ=−0.349, TIGIT Δ=−0.157, CTLA4 Δ=−0.090. The authors cite precisely the right literature for this alternative (Boomer 2011 JAMA [2]; Hotchkiss/Monneret/Payen 2013 [17] — the latter's central mechanism is apoptosis-driven loss of CD4/CD8 T cells and monocytes) but never apply it to their own data.
The authors' own cell-module file makes the point unanswerably: `07_axis_celltype.csv` gives mean |r| with **CD4 T-cell 0.618, CD8 T-cell 0.582, Dendritic 0.459, NK 0.419, B 0.401, Neutrophil 0.319, Monocyte 0.222 — i.e. the monocyte module has the *lowest* mean |r| of all seven**, yet `manuscript.md:14` (abstract) and `manuscript.md:103` state the hubs "localized to monocytes / antigen-presenting cells". Two sentences inside one Results section point in opposite directions.

**【Why it matters】** This is the difference between "Mars1 has per-cell antigen-presentation failure that a drug can restore" and "Mars1 patients have fewer immune cells in the sampled compartment". If the latter dominates, (a) the six "hubs" are largely a cell-count signature, (b) the Q2\#negative finding that the whole translational edifice (gene set → LINCS reversal → drug nomination) rests on is unsupported, and (c) a reviewer or reader who knows the whole-blood transcriptome literature will read the paper as naive. This single point determines whether the Tier-1 claim is a biological discovery or a restatement of lymphopenia.

**【Specific fix】** Add a new analysis **`S01b_composition_check`**, specified as follows. Input: the 11,519×802 matrix already used. Steps: (1) estimate per-sample abundances for the same seven modules with the existing marker modules and report them **by endotype** with Kruskal–Wallis P; (2) recompute the Mars1-vs-Other contrast **with the estimated monocyte and lymphocyte fractions added as covariates** in the same moderated-t model; (3) report, per hub gene, the raw Δ and the composition-adjusted Δ side by side; columns = `gene, logFC_unadjusted, adj.P_unadjusted, logFC_adjusted, adj.P_adjusted, pct_change_in_logFC`. Then replace the sentence ending `manuscript.md:103` ("their loss-of-function is directionally concordant with the immunosuppressed program") with:

> "Because whole-blood transcript abundance scales with circulating cell content, we estimated CIBERSORT/xCell-style module abundances for all samples; monocyte (median module score X in Mars1 vs Y in others, P=…) and CD4/CD8 T-cell (X vs Y, P=…) modules were lower in Mars1. After adjusting the Mars1-vs-Other contrast for estimated monocyte and lymphocyte abundance, the six hub genes retained **…%** of their effect size (**CD74 −0.76 → …, CD14 −0.77 → …, HLA-DQA1 −0.53 → …, FCGR3A −0.61 → …, HAVCR2 −0.35 → …, FIS1 … → …**), indicating that the hub signal is [ / is not] explained by cell depletion alone."

---

### F2 · Tier 0 — The co-expression network that supplies one of the six hubs is dominated by an erythroid/heme module, and "degree-centrality and tri-method ML consensus converged" is contradicted by the authors' own degree file

**【Problem】** The network step contributed 20 non-immune genes to the candidate pool, all from a module that is unmistakably erythroid/heme/tissue-of-origin in origin, and none of the five genuine hubs is anywhere near the top of the degree ranking.

**【Evidence】** Recomputed from `S03_hub_degree.csv` (2,000 genes). Top-12 by degree: **GATA1 78.40** (erythroid master transcription factor), **CGB 76.12** (chorionic gonadotropin β — essentially not expressed in blood), DPM2 72.59, **EPB49 72.46** (erythrocyte dematin), BCL2L1 71.92, CDC34 71.84, **KRTAP5-2 69.17** (keratin-associated protein), ELOF1 68.42, FKBP8 67.56, C2orf24 65.77, FOXO4 64.89, **FIS1 64.26**. Positions 21–25 are ANK1 60.69 (erythrocyte ankyrin), FAM104A, DCAF12, HAGH, **EIF2AK1 59.61** (heme-regulated eIF2α kinase, erythroid-restricted). DES 61.02 (desmin) is also present.
`S04_candidate_genes.csv` contains exactly these 20 non-immune genes (all with `in_immune_set=False`) plus 15 immune genes — i.e. **the entire network contribution to the hub search is non-immune**.
Recomputed degree rank of the five immune hubs within the 2,000-gene ranking: **CD74 rank 595 (degree 22.38), HLA-DQA1 rank 1102 (13.20), FCGR3A rank 1516 (7.17), CD14 rank 1766 (3.88), HAVCR2 rank 1927 (1.59)**. Only FIS1 (rank 12) is a degree hub. `manuscript.md:103` therefore asserts a convergence that did not occur; `manuscript.md:52` ("the top-50 genes by degree define the co-expression hub") does not describe how five of the six hubs were actually obtained.

**【Why it matters】** The hub gene list is the paper's primary deliverable (it is in the title, abstract, and every downstream layer). If one member arrives via an erythroid module and the other five arrive only from the ML step, the "convergent multi-omics network + ML" design claim collapses and a knowledgeable reader will suspect the network tier is decorative. Worse, the erythroid module is *not random noise*: Scicluna et al. ([4]) reported that Mars1 is characterised by decreased innate/adaptive immune programmes **combined with increased expression of metabolic pathway genes including heme biosynthesis** — so the module is a real Mars1 feature that the paper mis-labels rather than interprets.

**【Specific fix】** (1) Restate the method honestly; replace the first sentence of `manuscript.md:103`:

> "Network degree-centrality and the tri-method ML consensus nominated six hub genes, but by different routes: only **FIS1** was a top-degree node (rank 12/2,000, degree 64.3), whereas **CD74, HLA-DQA1, CD14, FCGR3A and HAVCR2** entered through the machine-learning selectors and had low degree (ranks 595–1,927 of 2,000; degrees 1.6–22.4). The co-expression step therefore contributed chiefly mitochondrial/erythroid co-expression context, not convergent support for the immune hubs."

(2) Add **Supplementary Table S-hub-src** with columns `gene, degree_rank, degree, lasso, rf, univariate, in_immune_set, source_of_nomination`. (3) Add one sentence engaging Scicluna's heme finding: "The dominance of GATA1/EPB49/ANK1/EIF2AK1 in the top-degree module mirrors the increased heme-biosynthesis programme that Scicluna et al. [4] described for Mars1, suggesting this module reflects a genuine erythroid component of the endotype rather than technical noise; it nonetheless does not qualify FIS1 as an immune regulator (see §3.3)."

---

### F3 · Tier 1 — FIS1 is handled more honestly than I expected, but one decisive piece of evidence against it is withheld from §3.6

**【Problem】** The authors correctly label FIS1 a probable passenger (`manuscript.md:103`), but §3.6 silently drops it from the localisation table, thereby hiding the observation that FIS1 correlates **negatively** with every immune module.

**【Evidence】** `07_hub_celltype.csv`, recomputed row for FIS1: `best_celltype=Monocyte, best_corr=−0.438`; Monocyte −0.438, Neutrophil −0.013, CD4 T −0.143, CD8 T −0.111, B −0.020, NK −0.191, Dendritic −0.154. Every one of the other five hubs has a **positive** best correlation (+0.298 to +0.773). `manuscript.md:114` lists five correlations and never mentions FIS1.

**【Why it matters】** A gene whose bulk expression falls as immune-cell content rises is behaving like "everything that is not a leukocyte" (reticulocyte/platelet/plasma fraction), which is exactly the expected behaviour of a ubiquitous mitochondrial-fission transcript in whole blood. Withholding the sign makes the localisation result look more coherent than it is and deprives the reader of the strongest available support for the authors' own "passenger" conclusion.

**【Specific fix】** Append to `manuscript.md:114`:

> "The sixth hub behaved differently: FIS1 correlated *negatively* with every immune-marker module (best |r| = 0.44 against the monocyte module at r = −0.44, versus +0.30 to +0.77 for the five immune hubs), a pattern expected of a transcript contributed predominantly by the non-leukocyte fraction of whole blood, consistent with its interpretation as a co-expression passenger rather than an immune regulator."

---

### F4 · Tier 0 — The immune-function score does not statistically separate Mars1 from Mars2, the endotype with 12.5 percentage points lower mortality

**【Problem】** §3.2 reports a point estimate ("lowest median in Mars1") with no test, and the test shows the score cannot distinguish Mars1 from Mars2.

**【Evidence】** Recomputed from `S02_immunoparalysis_score.csv` (n=802): medians **Mars1 −0.792 (n=132), Mars2 −0.752 (n=176), Mars4 −0.235 (n=53), Mars3 +0.641 (n=118)**, unassigned +0.238 (n=323). Mann–Whitney Mars1 vs Mars2: **U=12 179, P=0.467** (Mars1 vs Mars3 P<1×10⁻⁶; Mars1 vs Mars4 P=0.0013). Recomputed 28-day mortality from the same file's `death_28d` column: **Mars1 45/132 = 34.1%, Mars2 38/176 = 21.6%, Mars3 21/118 = 17.8%, Mars4 10/53 = 18.9%.** So the two endotypes that this score cannot tell apart differ by 12.5 points in absolute 28-day mortality. For completeness, recomputed AUC of the (negated) immune score for 28-day death in the 479 patients with known outcome = **0.604**; raw score AUC = 0.396. Nowhere reported.

**【Why it matters】** §3.2 is used as corroboration that Mars1 is the immunosuppressed endotype and is then carried into §3.4's prognostic claim. A score that cannot separate Mars1 from Mars2 either is not measuring the Mars1-specific programme or is measuring general illness severity. This also exposes that the paper's own stated promise — "its association with 28-day death is reported separately in §3.4" (`manuscript.md:100`) — is unfulfilled: §3.4 reports the 30-gene signature, not the composite score.

**【Specific fix】** Replace the relevant clause of `manuscript.md:100`:

> "The composite immune score was lowest in Mars1 (median −0.79) but was statistically indistinguishable from Mars2 (median −0.75, Mann–Whitney U=12 179, P=0.47), differing from Mars3 (P<1×10⁻⁶) and Mars4 (P=0.0013); although Mars1 and Mars2 differ substantially in outcome (recomputed 28-day mortality 45/132 = 34.1% vs 38/176 = 21.6%), the score does not separate them and should therefore be read as a severity-graded rather than an endotype-specific index. Over the whole cohort the score discriminated 28-day death at AUC 0.604 (negated; 0.396 raw), which we report here for completeness."

Also add a four-row table of recomputed endotype-wise mortality (`endotype, n, deaths, mortality_pct, immune_score_median, P_vs_Mars1`).

---

### F5 · Tier 0 — The clinical-readiness ranking is out of date by a pivotal randomised trial: IFN-γ in mHLA-DR-defined sepsis-induced immunoparalysis has now been tested at scale

**【Problem】** `manuscript.md:132` states that IFN-γ has "limited sepsis-specific signals (Döcke et al. [13])" while IL-7 and GM-CSF "carry the most direct (though still limited) sepsis/immunoparalysis RCT signals". Since Döcke 1997 (n=9), IFN-γ has been tested in the largest mechanism-matched randomised trial in this field, and the manuscript does not cite it.

**【Evidence】** Giamarellos-Bourboulis EJ, Kotsaki A, Kotsamidi I, et al. *Precision Immunotherapy to Improve Sepsis Outcomes: The ImmunoSep Randomized Clinical Trial.* **JAMA 2025; doi:10.1001/jama.2025.24175** (NCT04990232). Double-blind, double-dummy, placebo-controlled, 276 patients (of 672 screened), six countries; patients with **sepsis-induced immunoparalysis** — ferritin ≤4420 ng/mL **and <5000 HLA-DR molecules per CD45/CD14 monocyte** — were randomised to **subcutaneous recombinant human interferon-γ** for up to 15 days. Primary endpoint (≥1.4-point SOFA decrease by day 9) 46/131 = **35.1% vs 26/145 = 17.9%, difference 17.2% (95% CI 6.8–27.2), P=0.002**; **28-day mortality not significantly different**; 1,069 serious adverse events (88.8%), with **increased haemorrhage in the interferon-γ group**. This trial is exactly the experiment this manuscript proposes as a hypothesis (`manuscript.md:183`).
Note the date: the manuscript's own reference audit (`reference_doi_audit.csv`) records DOIs "verified 2026-09-26", i.e. after ImmunoSep was available.

**【Why it matters】** Two consequences, one adverse and one favourable, both mandatory. Adverse: the clinical-readiness hierarchy in §3.8, Table 2's ranking, and the Discussion stratification hypothesis are built on a literature missing the single most relevant RCT; a reviewer or editor who knows ImmunoSep will treat its absence as evidence the literature search was not fit for purpose, and it will also be read as evading a partly negative signal (no mortality benefit, excess bleeding) for the agent at the centre of the paper's mechanism logic. Favourable, and genuinely valuable to the authors: **53% of screened patients in ImmunoSep could not be classified by ferritin + mHLA-DR at all** (7% MALS, 34% SIP, 53% unclassified) — which is the strongest available argument for why a transcriptomic endotype like Mars1 is needed, and it turns the paper's weak §3.8 into a real translational claim.

**【Specific fix】** Replace the IFN-γ clause of `manuscript.md:132` and add one sentence after it:

> "IFN-γ is approved for chronic granulomatous disease and is a canonical MHC-II inducer; unlike IL-7 and GM-CSF, it has been tested in a large mechanism-matched randomised trial — the ImmunoSep trial (Giamarellos-Bourboulis et al., *JAMA* 2025; doi:10.1001/jama.2025.24175) randomised 276 patients to precision immunotherapy, giving subcutaneous recombinant human IFN-γ to participants with sepsis-induced immunoparalysis defined by ferritin ≤4420 ng/mL and <5000 HLA-DR molecules per CD14 monocyte, and reported improved organ dysfunction at day 9 (35.1% vs 17.9%, P=0.002) **with no 28-day mortality benefit and more haemorrhagic events**."

Then add, in §4 Discussion:

> "A concrete advantage of a transcriptomic endotype is suggested by ImmunoSep itself: its two-biomarker classifier (ferritin and monocyte HLA-DR) left more than half of screened patients (53%) unclassified, so the majority could not be assigned to either immunotherapy arm. Whether a Mars1-like blood transcriptomic assignment captures part of that unclassified fraction — and thereby widens eligibility for IFN-γ or GM-CSF — is a testable proposition in any future trial cohort that banks PAXgene RNA."

---

### F6 · Tier 1 — IL-7's top rank is circular, and one of its five "response genes" is directionally wrong

**【Problem】** IL-7 attains concordance 1.00 because its curated response set is a set of pan-T-cell transcripts, and includes IL7R, whose expression IL-7 signalling down-regulates.

**【Evidence】** `08_candidates_drugs.csv` row 1: `n_target_genes=5, n_rescue_mars1down=5, rescue_fraction=1.0, rescue_genes=CD3D;CD3E;CD8A;IL7R;LCK`. All five are cell-type markers that rise whenever T-cell abundance rises — exactly the quantity that §3.1/F1 shows is reduced in Mars1 for compositional reasons. `08b_clinical_translation.csv` correspondingly justifies it as "Raises naive & central-memory T cells … Restores CD3D/CD3E/CD8A/IL7R/LCK axis (S08 rescue 1.00)". No per-gene citation is given for any of the seven curated response sets — the `evidence` column is a free-text note ("lymphopenia 复苏；PDCD1 轴上游"), not a source per gene. Separately: the IL-7 receptor (CD127/IL7R) is transcriptionally and surface-down-regulated by IL-7 engagement (negative feedback via SOCS/JAK turnover and receptor internalisation); placing **IL7R** in an "up-regulated by IL-7" list inverts the canonical direction.

**【Why it matters】** The number 1.00 is the single strongest-looking figure in Table 2 and drives the whole IL-7-first recommendation (Table 2, §3.8, §4, the S11 wet-lab design). If it is a restatement of "IL-7 increases T cells" rather than drug-specific evidence, it carries no information about IL-7 versus any other lymphoproliferative agent.

**【Specific fix】** (1) Add **Supplementary Table S-resp** with columns `drug, response_gene, direction_curated, source_PMID, source_sentence`, one row per curated gene–drug pair; drop or re-source IL7R. (2) Add to `manuscript.md:117`:

> "IL-7's curated response set (CD3D, CD3E, CD8A, LCK, IL7R) consists entirely of lineage markers whose bulk-blood abundance rises with the absolute lymphocyte count; a concordance of 1.00 therefore indexes IL-7's known effect on lymphocyte numbers rather than restoration of per-cell function, and would be matched by any intervention that expands T cells. It also conflicts with the present-day L1000 score's acknowledgement (§3.9) that up-regulating the same bulk transcripts also raises PDCD1/LAG3; we therefore do not treat IL-7's rank as drug-specific evidence."

---

### F7 · Tier 1 — "IFN-γ rescued 5/5" contradicts the authors' own positive-control file, and all of Table 2 shifts once the stated |logFC|≥0.3 threshold is applied consistently

**【Problem】** The abstract's positive-control number (5/5) disagrees with `08_positive_control_check.csv` (4/5) and with the companion protocol (4/5), and the discrepancy is not explained; recomputing Table 2 under the paper's own DEG definition changes every candidate's score and reorders the shortlist.

**【Evidence】** `manuscript.md:14` and `manuscript.md:25` and `manuscript.md:117`: "IFN-γ rescued 5/5 antigen-presentation genes". `08_positive_control_check.csv` row 1: `IFN_gamma_rescues_antigen_presentation_axis, True, 救回 4/5 抗原呈递基因: ['HLA-DRA','HLA-DRB1','HLA-DQA1','CD74']`. `11_validation_design.md:64`: "IFN-γ rescue of antigen-presentation (S08 gate: rescued 4/5 genes)". `08_candidates_drugs.csv` row 4 says 5 rescued including **HLA-DQB1**.
The divergence traced to source: in `S01_immunoparalysis_direction.csv`, **HLA-DQB1 has logFC −0.203 and `DEG_0.3=False`** — it is sub-threshold and therefore should not be in the Mars1-down axis as defined in §2.2. Recomputing every shortlist member using only `DEG_0.3=True` genes: **IL-7 4/5 = 0.80** (CD3E Δ=−0.216 excluded), **GM-CSF 4/6 = 0.67** (ITGAM Δ=−0.208 excluded), **IFN-γ 4/7 = 0.57** (HLA-DQB1 excluded), Azithromycin 2/3 = 0.67, Lenalidomide 2/5 = 0.40, Thymosin α1 2/5 = 0.40, BCG 1/5 = 0.20. The ordering changes materially (**IFN-γ moves from 3rd to below azithromycin**; IL-7 and azithromycin/GM-CSF converge).

**【Why it matters】** The positive-control gate is what certifies the repositioning pipeline across abstract, English and Chinese abstracts, Results and the companion protocol; a number that differs between the abstract and its own result file undermines trust in everything the gate licenses, and Table 2's ordering is not robust to the paper's own threshold.

**【Specific fix】** Recompute `response_gene_concordance` **once**, defined against the `DEG_0.3=True` subset of the 25 consensus genes, re-emit `08_candidates_drugs.csv` and `08_positive_control_check.csv` from the same routine (one function, one output), and replace `manuscript.md:117`'s first clause:

> "IFN-γ up-regulated 4 of the 7 curated response genes in its pathway — HLA-DRA, HLA-DRB1, HLA-DQA1 and CD74 — i.e. **4/5** of the antigen-presentation members of its curated set after excluding HLA-DQB1 (Δ=−0.20, below the |logFC|≥0.3 DEG threshold), satisfying the pre-specified method-positive gate of ≥3/5."

Update `manuscript.md:14`, `manuscript.md:25`, `11_validation_design.md:64` to the same phrasing, and relabel the gate in `manuscript.md:64` from "≥3/5 concordance" to "concordance ≥0.60 (3/5 genes)", removing the ambiguity between a count and a fraction.

---

### F8 · Tier 1 — The validation blueprint's single primary endpoint cannot test the manuscript's own top-ranked candidate

**【Problem】** S11 specifies **CD14⁺ HLA-DR MFI recovery** as the sole primary endpoint, but the top-ranked candidate (IL-7) does not restore monocyte HLA-DR — it expands lymphocytes.

**【Evidence】** `11_validation_design.md:72-77` sets the primary readout as CD14⁺HLA-DR⁺ MFI rescue ≥1.5-fold; the only T-cell-linked readout (MLR) is relegated to secondary outcome 2 (`:80-82`), and there is **no absolute-lymphocyte-count, apoptosis or STAT5-phosphorylation readout** anywhere. Rank 1 of the intervention table (`:55`) is IL-7 with dose expressed as "10–50 **ng/mL**" (the units used for a cytokine in vitro are working units; the published human exposure achieved with 10 µg/kg CYT107 in IRIS-7 [11] should be stated for scaling). By contrast, the primary endpoint is well matched to IFN-γ/GM-CSF — which is precisely the pair whose clinical status §3.8 has now been overtaken by ImmunoSep (F5).

**【Why it matters】** If executed as written, the experiment would return a false negative for the paper's headline nomination: IL-7 does not up-regulate monocyte HLA-DR, so the prespecified GO/NO-GO rule (`11_validation_design.md:136-141`) would wrongly demote it. A reader planning the definitive test from this blueprint would be misled.

**【Specific fix】** Add to `11_validation_design.md` a **dual co-primary endpoint** and re-write the GO rule:

> "Co-primary endpoints, one per axis: (a) **antigen-presentation axis** — CD14⁺ monocyte HLA-DR molecules per cell by Quantibrite-standardised flow cytometry, rescue defined as ≥1.5-fold over the LPS-tolerance baseline with P<0.05 (applies to IFN-γ and GM-CSF); (b) **lymphocyte axis** — absolute CD4⁺ and CD8⁺ T-cell yield plus STAT5 phosphorylation after 72 h of IL-7 exposure, and resistance to apoptosis measured by Annexin-V/cleaved-caspase-3, rescue defined as ≥1.5-fold increase in viable counts with P<0.05 (applies to IL-7). Each candidate is judged only against the endpoint matched to its axis; a negative result on the mismatched axis is not a no-go."

Also state the IL-7 concentration in IU-equivalent terms ("10–50 ng/mL recombinant human IL-7, bracketed by the plasma exposure achieved with 10 µg/kg CYT107 in IRIS-7 [11]").

---

### F9 · Tier 1 — The companion protocol asserts HAVCR2/TIM-3 is Mars1-**up**, which is the opposite of the source data, and expects IFN-γ to lower it, which is mechanistically doubtful

**【Problem】** `11_validation_design.md:84` states "TIM-3 (HAVCR2) surface (**S01: Mars1-up**); expected to *decrease* under IL-7/IFN-γ rescue" — both parts are unsupported.

**【Evidence】** `S01_immunoparalysis_direction.csv`: **HAVCR2 logFC −0.349, adj.P 2.84×10⁻¹³, direction `Mars1_down`**; in the same file TIGIT is −0.157 and CTLA4 −0.090, also down (`manuscript.md:93` and `:82` get this right — the error is localised to the protocol). On the second point, IFN-γ is a canonical inducer of counter-regulatory molecules including PD-L1 and, in several myeloid contexts, of the TIM-3/galectin-9 axis; expecting IFN-γ to *lower* surface TIM-3 has no cited basis.

**【Why it matters】** This is the readout that would decide HAVCR2's membership of the hub set. As written, an experimenter would wait for a direction change that neither the data nor the mechanism predicts, and mis-read it either as failed rescue or as validation of an exhaustion axis.

**【Specific fix】** Replace `11_validation_design.md:84`:

> "**Checkpoint axis** — TIM-3 (HAVCR2, Mars1-**down**, Δ=−0.35, adj.P=2.8×10⁻¹³), TIGIT (Δ=−0.16) and CTLA4 (Δ=−0.09) all fall with the falling lymphocyte pool, so bulk transcript changes here are not interpretable as per-cell checkpoint modulation. TIM-3 will therefore be measured **per cell** (median fluorescence intensity on gated CD3⁺CD8⁺ T cells and CD14⁺ monocytes) rather than as bulk mRNA, and the pre-specified expectation is registered as **unchanged or increased** under IFN-γ, because type II interferon induces several counter-regulatory checkpoint ligands; only a *decrease* below the non-treated tolerance baseline would support an anti-exhaustion interpretation."

---

### F10 · Tier 1 — "T-cell exhaustion superimposed on antigen-presentation failure" rests on one gene (PDCD1) plus one non-significant gene (LAG3), while the rest of the exhaustion panel moves in the opposite direction

**【Problem】** §3.1 and §3.3 claim an "up-regulated T-cell exhaustion axis (PDCD1, LAG3)", but LAG3 is not significant and the other four exhaustion transcripts are down.

**【Evidence】** Recomputed from `S01_immunoparalysis_direction.csv`: PDCD1 Δ=**+0.162**, adj.P=3.00×10⁻¹⁰ (genuinely up); **LAG3 Δ=+0.035, adj.P=0.552** — not significant at any threshold, and biologically negligible (≈2.5% change). Against these, HAVCR2 Δ=−0.349 (adj.P 2.8×10⁻¹³), TIGIT Δ=−0.157 (adj.P 7.0×10⁻⁴), CTLA4 Δ=−0.090 (adj.P 0.034) are all **down**. This also means the negative term of the immune score (`score = z(HLA-II) + z(T-cell) − z(exhaustion)`, `manuscript.md:49`) is being driven mostly *upward* in Mars1 by the fall in TIM-3/TIGIT/CTLA4, so the reported Mars1 nadir is achieved despite, not because of, the exhaustion term.

**【Why it matters】** "Exhaustion superimposed on antigen-presentation failure" is the mechanistic bridge from description to the IL-7 nomination. If it rests on PDCD1 alone, and if the other exhaustion markers move the other way, the paper must either drop the exhaustion framing or demonstrate it per cell. As it stands a reader can compute this in ten seconds from the published supplementary CSV.

**【Specific fix】** Replace the final sentence of `manuscript.md:82` and the matching parenthetical in `manuscript.md:103`:

> "Of the five exhaustion transcripts interrogated, only PDCD1 was up-regulated (Δ=+0.16, adj.P=3.0×10⁻¹⁰); LAG3 was flat and non-significant (Δ=+0.04, adj.P=0.55), and HAVCR2, TIGIT and CTLA4 were all down-regulated (Δ=−0.35, −0.16 and −0.09). Because these are lymphocyte-derived transcripts and the whole T-cell module is reduced, bulk data cannot separate genuine per-cell PD-1 up-regulation from lymphocyte loss; we therefore report the Mars1 programme as one of **antigen-presentation and lymphocyte/monocyte loss with retained or increased PD-1 per surviving cell**, and do not claim a coordinate exhaustion programme."

Add one sentence noting that the exhaustion term of the score is therefore partly self-cancelling in Mars1.

---

### F11 · Tier 1 — CD74 is characterised only as the MHC-II invariant chain; its role as the MIF receptor — which explains the MR discordance — is absent

**【Problem】** The paper interprets CD74 exclusively through antigen presentation, so it has no biological account of the (already down-weighted) MR result that *higher* genetically predicted CD74 predicts *worse* critical-care outcome.

**【Evidence】** `manuscript.md:89` labels CD74 "MHC-II invariant chain" only. CD74 is also the high-affinity cell-surface receptor for **macrophage migration-inhibitory factor (MIF)** and for D-dopachrome tautomerase (MIF-2), is a survival/anti-apoptotic signalling receptor on many haematopoietic and non-haematopoietic cells, and is itself IFN-γ-inducible. MIF is markedly elevated in sepsis and its blockade has been explored as a therapeutic strategy. The MR critical-care estimate is **OR 2.22 (IVW 1.175–4.200, P=0.014)** in the direction opposite to the expression model (`manuscript.md:159`, `:171`).

**【Why it matters】** Without acknowledging CD74's second life, the reader is left with an unexplained contradiction at the centre of the hub set — and the contradiction is informative: for an intensivist it suggests that the germline effect of CD74 may run through MIF-driven inflammation rather than through antigen presentation. Not saying this wastes the paper's one genuinely interesting genetic result and invites the suspicion that the biology was fitted to the desired story.

**【Specific fix】** After `manuscript.md:171`, insert:

> "Beyond its role as the MHC-II invariant chain, CD74 is the cell-surface receptor for macrophage migration-inhibitory factor (MIF) and for MIF-2/D-dopachrome tautomerase, is IFN-γ-inducible, and transduces pro-survival and pro-inflammatory signals largely independent of peptide loading. A genetically determined increase in CD74 could therefore act through MIF-mediated inflammation and myeloid survival rather than through antigen presentation, which offers a mechanistic reading of the discordant direction we observe; we cannot distinguish these functions with whole-blood eQTL data and do not treat the effect as evidence for CD74-directed therapy."

---

### F12 · Tier 1 — The strongest MR association in the paper has an internally incoherent standard-error structure and rests on three variants

**【Problem】** For CD74 vs critical care, MR-Egger returns a **smaller** standard error than IVW on the identical three variants, generating q≈1.5×10⁻¹¹; this is not the expected behaviour of MR-Egger and should be recomputed before publication.

**【Evidence】** Recomputed from `10_genetics_mr_outcome4982_criticalcare.csv`: same gene, same `nsnp=3` — IVW `se=0.32496`, `p=1.40×10⁻²`, OR 2.2217 (95% CI 1.175–4.200); MR-Egger `se=0.11107`, `p=6.63×10⁻¹³`, OR 2.2217 (95% CI 1.787–2.762). MR-Egger has one fewer degree of freedom than IVW and must have a **larger** SE; here it is 2.9-fold smaller, and the two point estimates agree to three decimal places. The weighted-median row reports `p=0.0` exactly (underflow) with `se=0.08849` from 2,000 bootstrap resamples. These three rows are the source of the "q≈1.5×10⁻¹¹", "q≈0" and "I²=0.00" citations at `manuscript.md:72`, `:171`, `:173` and limitation 2 (`manuscript.md:190`). Everything else in the MR layer I recomputed matched exactly (Table 3 and Table 4 IVW/Egger/median ORs, CIs, P values, Cochran-Q P, per-outcome I² including FIS1 critical-care I²=0.502, and median F statistics 35.4/168.1/45.7/36.4/75.0 from `10_genetics_mr_outcome5086_harmonised.csv`, minimum F 30.7).

**【Why it matters】** The authors already label MR Tier-3/hypothesis-generating, so the headline conclusions survive; but the largest quantitative claim in the genetics layer may be an artefact of an SE computation, and reporting a q of 10⁻¹¹ that later needs retraction is costly. Note also that if F11's biology is accepted, even a correct estimate in this direction belongs to a different pathway than the one the paper is about.

**【Specific fix】** Recompute MR-Egger for these three variants **with `TwoSampleMR::mr_egger_regression` (or an independent implementation) and verify that the reported SE accounts for the residual heterogeneity with I²_gx-scaled weights and df = n−2 = 1**; output columns `gene, outcome, method, beta, se_ivw, se_egger, ratio_se_egger_over_ivw`. If after recomputation the Egger SE remains below the IVW SE from three variants, **delete the CD74 critical-care paragraph** from §3.10, §4, limitation 2 and the abstract-facing sentence in §2.10 and state plainly: "The CD74 critical-care association did not survive recomputation of the MR-Egger standard error with three instruments and is withdrawn."

---

### F13 · Tier 1 — The external cohort is the Davenport SRS cohort, and the paper uses it only as a survival endpoint while ignoring the endotype it defines

**【Problem】** E-MTAB-4451 is the cohort in which Davenport et al. [5] defined the **sepsis response signature (SRS1/SRS2)** endotypes — SRS1 being the immunosuppressed, higher-mortality group. The manuscript cites that paper only for the external survival validation and never uses the endotype.

**【Evidence】** `manuscript.md:67` describes E-MTAB-4451 solely as "106 adult patients with severe sepsis due to community-acquired pneumonia … with 28-day survival". The paper's `09_external_validation.csv` has no endotype variable. Recomputed from the file: n=106, 52 deaths / 54 survivors, 29/30 genes mapped (HLA-DQA1 absent), external equal-weight AUC **0.638** (95% CI 0.532–0.748), locked L1 **0.585** (0.469–0.696), IRG benchmark recomputed 0.604 — all matching the text.

**【Why it matters】** This is the cheapest available external test of the paper's central biological claim. A Mars1-derived immune score that also marks SRS1 membership in an independent platform, population and endotyping framework would convert the Tier-1 finding from "reproduces its own construction" into "reproduces across endotype systems" — currently the strongest available support, and it is sitting unused in a file the authors already downloaded. It would also directly answer F1 and F4 (does the score track *immunosuppressed endotype* or merely severity?).

**【Specific fix】** Add **`09b_ext_endotype_link`**: columns `sample, signature_score_quartile, SRS_group, death_28d`. Report (a) mean/ median fixed-orientation score in SRS1 vs SRS2 with Mann–Whitney P, (b) AUC of the score for SRS1 membership, (c) the 28-day mortality odds ratio per SD of score, unadjusted and adjusted for SRS group, (d) the partial AUC contributions. Then add one sentence to §3.5:

> "Because the discovery endpoints and the validation cohort carry different published endotyping frameworks, we additionally tested whether the Mars1-derived score identifies the immunosuppressed SRS1 group of Davenport et al. [5] within E-MTAB-4451; [AUROC = …, P = …, effect on mortality after adjustment = …]."

If SRS assignment cannot be recovered from the public SDRF, say so explicitly in one sentence rather than leaving the gap unmentioned.

---

### F14 · Tier 1 — The 30-gene signature also contains a granulocyte/emergency-myelopoiesis component that is never mentioned, although it is the strongest single correlate of death

**【Problem】** The signature is presented purely as "immune-risk/immunoparalysis"; in fact its highest-absolute-correlation member is a neutrophil gene oriented towards *higher* risk.

**【Evidence】** Recomputed from `S06_signature_genes.csv`: ranked by |r| with death, the top row is **ELANE r=+0.170** (neutrophil elastase), with **MPO r=+0.152** and **S100A8 r=+0.091** also positive (3 of 30), versus 27 negative. `09_external_validation_coef.json` confirms the locked orientation, e.g. `'ELANE': 1, 'MPO': 1`. `manuscript.md:106` describes the signature as "dominated by antigen-presentation … monocytic … and T-cell genes, almost all negatively correlated with death", which is literally true but omits that the three positively-oriented genes are all granulocyte/ immature-myeloid markers.

**【Why it matters】** This matters for interpretation, not arithmetic: the score simultaneously indexes lymphoid-monocyte depletion **and** granulocytosis/emergency myelopoiesis — i.e. it straddles both poles of the well-established hyper-inflammatory/hypo-inflammatory sepsis phenotype dichotomy. Reporting only one pole over-simplifies what the score measures and wastes a natural bridge to that literature.

**【Specific fix】** Append to `manuscript.md:106`:

> "The three positively-oriented genes (ELANE r=+0.17, MPO r=+0.15, S100A8 r=+0.09) are all granulocyte / immature-myeloid markers, so the score indexes both lymphoid–monocyte depletion and granulocytosis; it therefore straddles both arms of the hyper-inflammatory/hypo-inflammatory phenotype dichotomy rather than measuring immunoparalysis alone."

---

### F15 · Tier 2 — Three pieces of must-cite literature are missing, and one cited reference is used for a claim it does not support

**【Problem】** The reference list has Sepsis-3 [3], MARS [4], SRS [5] and Hotchkiss/Monneret/Payen [17], but lacks any dedicated citation for the standardised monitoring of mHLA-DR as the clinical immunoparalysis biomarker, for the trajectory literature, or for the hyper-/hypo-inflammatory phenotype work — and reference [18] is cited for decision-curve analysis where it does not support it.

**【Evidence】** (a) `manuscript.md:106` says "Calibration and decision-curve analytics [18] for the external score are in Fig. S06", citing Schuemie et al. *Stat Med* 2013 — an empirical-calibration paper, not a decision-curve (Vickers & Elkin 2006, *Med Decis Making*) or calibration-slope paper. (b) There is no reference for quantifying mHLA-DR and standardising it across centres, although mHLA-DR is the protein-level counterpart of the whole HLA-II arm; at minimum Monneret G, Venet F et al. on immune monitoring should be cited, together with the trajectory stratification work the field now uses. (c) The discussion of endotype-guided therapy omits the hydrocortisone × endotype interaction literature, which is directly relevant to the glucocorticoid caveat in §3.9.

**【Why it matters】** These are the citations a sepsis reviewer checks for reflexively. Their absence makes the paper read as written from one database rather than from the field, and item (a) is a citation that does not say what it is cited for — the kind an editor's check flags.

**【Specific fix】** Add, and cite in the places indicated:
1. In §1 after the mHLA-DR sentence — a monitoring/immunoparalysis-biomarker reference (e.g. Monneret G, Venet F, Pachot A, Lepape A. *Monitoring immune dysfunctions in the septic patient: a new skin for the old ceremony.* Crit Care 2011;15:108, or the equivalent version the authors prefer), plus a reference for **mHLA-DR trajectory endotypes**.
2. In §3.9 after the glucocorticoid caveat — add: "This distinction is not academic: in the sepsis response-signature cohorts, hydrocortisone was associated with *increased* mortality in the SRS2 stratum, illustrating that a drug that transcriptionally mimics immune restoration can be harmful in a defined endotype."
3. Replace reference [18] at `manuscript.md:106` with **Vickers AJ, Elkin EB. Decision curve analysis. Med Decis Making. 2006;26:565–574**, retaining the empirical-calibration reference where it genuinely applies.

---

### F16 · Tier 2 — The 39% Mars1 mortality figure is Scicluna's discovery-cohort number, presented without attribution, and differs from the value in this extraction

**【Problem】** `manuscript.md:34` states Mars1 "carries a 39% 28-day mortality" as though it were a property of the analysed cohort.

**【Evidence】** Scicluna et al. ([4]) report 35/90 = **39%** 28-day mortality for Mars1 in the **discovery cohort** (HR 1.86, 95% CI 1.21–2.86, P=0.0045; Mars2 22%, Mars3 23%, Mars4 33%) — correctly recalled in the text. Recomputed here from `S02_immunoparalysis_score.csv` on the 479 patients with both endotype and outcome: **Mars1 45/132 = 34.1%**, Mars2 38/176 = 21.6%, Mars3 21/118 = 17.8%, Mars4 10/53 = 18.9%. Both are correct; they are different cohorts within GSE65682 and should be distinguished.

**【Why it matters】** Presenting the literature number as the cohort's own invites a discrepancy complaint when a reader tabulates mortality themselves.

**【Specific fix】** Replace the clause at `manuscript.md:34`:

> "Mars1, the immunosuppressed subtype, carries the highest 28-day mortality of the four endotypes (39% in the Scicluna et al. [4] discovery cohort; 34.1%, 45/132, in the GSE65682 extraction analysed here; Table S-endotype), and is defined by downregulated HLA class-II, antigen-presentation and monocytic programmes."

Add the four-row recomputed table described in F4.

---

### F17 · Tier 2 — Two remarkably informative L1000 results are reported without comment: a dry-cleaning solvent among the top skeletal-muscle-free rescuers, and named statins/HSP90 inhibitors ranked above both small-molecule candidates

**【Problem】** §3.9 reports top-ranked compounds as anonymous BRD identifiers and then lists named drug classes, but does not acknowledge what those names imply about specificity.

**【Evidence】** `S08_l1000_immuno_overlap.csv`, recomputed: rank 17 **pravastatin**, rank 25 **geldanamycin**, rank 352 **pepstatin**, rank 507 **alvespimycin**, rank 666 **tetrachloroethylene** (perchloroethylene — an industrial degreasing solvent), rank 750 **tunicamycin**, rank 953 and 1660 **mevastatin**, rank 1566 **fluvastatin**, rank 1645 **dactinomycin**, rank 935 **nystatin**. Three of ten named hits are statins and three are protein-synthesis/ER-stress toxins. Meanwhile the two candidates sit at rank 5,435 (lenalidomide) and 9,152 (azithromycin). `manuscript.md:137` does mention HDAC inhibitors and statins, but not the solvent, the pepstatin or the ER-stress agent. Also `S08_l1000_positive_control.csv` row 1 carries the label "prednisolone" against `pert_iname=prednisone`; the manuscript says prednisone (correct against the data), so the file label should be fixed. The background statistics I recomputed match the text (top rescue 0.318; 20,413 compounds).

**【Why it matters】** Two separable messages, both currently lost: (i) some plausible-looking rescues are plainly non-specific — reinforcing the authors' own necessary-but-not-sufficient caveat more strongly than the glucocorticoid example does for the 22-gene query; (ii) the existence of a coherent, reproducible **statin class** and **HSP90-inhibitor class** signal is the only *unbiased* pharmacologic finding in the paper, yet it is dismissed while an unconstrained IL-7 concordance number is promoted.

**【Specific fix】** Append to `manuscript.md:137`:

> "The composition of the high-rescue tail further limits the interpretation: among the ten named entities in the top 1,700 compounds are three statins (pravastatin, mevastatin, fluvastatin), two HSP90/ER-stress agents (geldanamycin, tunicamycin) and two compounds with no plausible immunomodulatory indication at all (tetrachloroethylene, pepstatin), consistent with a query of 22 broadly-expressed transcripts partly capturing general cellular-stress responses. The one reproducible class-level signal — HMG-CoA reductase inhibition — is notable given that statins have been tested in sepsis and is hypothesis-generating, but we do not rank it against the mechanism-anchored shortlist without a matched positive control."

Correct the "prednisolone" label in `S08_l1000_positive_control.csv` to "prednisone".

---

### F18 · Tier 1 — The power calculation in the companion protocol is wrong: n=3 donors gives 47% power, not 80%

**【Problem】** `11_validation_design.md:102` claims "n=3 donors gives 80% power to detect 1.5× MFI change at α=0.05 (paired, based on published HLA-DR tolerance SD≈0.25×mean)".

**【Evidence】** Recomputed for a paired one-sample t-test with the protocol's own assumptions (standardised effect d_z = 0.5/0.25 = 2.0), two-sided α=0.05: **n=3 → power 0.471; n=4 → 0.755; n=5 → 0.909; n=6 → 0.971.** With df=2 the two-sided critical t is 4.303, which is why three donors cannot deliver 80%.

**【Why it matters】** An under-powered confirmatory experiment that returns "no rescue" would be used to demote the hubs to biomarkers (the protocol's own no-go rule). Getting n right is cheap and prevents an irreproducible negative.

**【Specific fix】** Replace `11_validation_design.md:102`:

> "**Sample size:** under the assumptions above the standardised paired effect is d_z = 0.5/0.25 = 2.0; for a two-sided paired t-test at α=0.05 with these donor-level standard deviations, n=3 gives 47% power, n=4 76%, **n=5 91%**. We therefore specify **n=5 healthy donors for Arm A and n≥8 patients per stratum for Arm B**, with interim analysis permitted after n=5 only for futility, never for claiming rescue."

---

### F19 · Tier 2 — "Comparable to the IRG benchmark" and "excludes 0.5 by a comfortable margin" overstate what an AUC of 0.638 in 106 patients supports

**【Problem】** Two adjacent sentences soften a genuinely weak discrimination result.

**【Evidence】** Recomputed from `09_external_validation.csv`: external equal-weight AUC 0.638, 95% CI **0.532–0.748**, 52 deaths / 54 survivors; locked L1 0.585 (0.469–0.696); IRG benchmark recomputed on the same cohort 0.604. The lower confidence bound sits 0.032 above chance; with 52 events the effective width corresponds to roughly ±1 SD of chance-level AUC estimates. The paper's honesty elsewhere ("comparable rather than established as superior", `manuscript.md:106`) is good; `manuscript.md:109`'s "excludes 0.5 by a comfortable margin" undoes it in the same paragraph.

**【Why it matters】** An AUC of 0.638 with a CI reaching 0.532 does not support any prospective clinical use, and an intensivist reader will object to language implying otherwise. Overreach here invites exactly the utility objection that the rest of the paper is careful to avoid.

**【Specific fix】** Replace the relevant clause of `manuscript.md:109`:

> "… a modest separation (point estimate only 0.138 above chance, lower confidence bound 0.532, i.e. compatible with weak discrimination; 29 events would be needed per stratum to halve this interval width) that was comparable to, not superior to, the IRG benchmark recomputed on the same cohort (0.604). At this discrimination the score is not usable as a stand-alone bedside decision rule; its present value is biological — it demonstrates that the Mars1 immunosuppression programme carries outcome information across platforms — and any clinical application would require combination with existing severity scores and demonstration of net benefit by decision-curve analysis, which Fig. S06 begins to address but does not establish."

Also: the text cites `04_figures/S06_dca.png` without ever reporting what the decision curve shows. Report the threshold-probability range over which net benefit is positive, or remove the callout.

---

### F20 · Tier 3 — Small verification discrepancies and cross-file clean-ups

**【Problem】** Minor but checkable items that a copy-editor or diligent reader will find quickly.

**【Evidence】** (a) `S01_immunoparalysis_genes_in_mars1.csv` contains **HLA-DRB5** (Δ=−0.409, adj.P 0.011), which is absent from `S01_immunoparalysis_direction.csv`; the "25 consensus genes" set therefore has a 26th member in a sibling file with no explanation. (b) `08b_clinical_translation.csv` row 4 states "Rescued **4/5** antigen-presentation genes in S08 positive-control" while `08_candidates_drugs.csv` and the abstract say 5 — a third independent value for one quantity (see F7). (c) `10_genetics_mr_outcome5086_28ddeath.csv` CD14 MR-Egger reports the narrow per-file BH value 0.0766 and the text correctly gives the family q 0.058; the abstract does not mention this test at all, which is correct, but the value "0.077" appears in two places (`manuscript.md:146`, `:190`) and "0.058" elsewhere — pick one label family. (d) All three figure callouts resolve correctly to real files in `04_figures/` (`S06_dca.png`, `fig_s09_external_roc.png`, `fig_s10_l1000_rescue.png`) — this is fine. (e) The gene sets defining the immune-function score (HLA-II set, T-cell set, exhaustion set) are described at `manuscript.md:49` but are not emitted as any file in `03_results/`, so the score's membership cannot be audited from results alone.

**【Why it matters】** None change conclusions; together they suggest deaths by multiple versions of the draft, and (e) blocks audit of a construct that supplies two abstract-level numbers.

**【Specific fix】** Emit the three marker lists as **`03_results/S02_score_gene_sets.csv`** (`set, gene, rationale_source`), add one row explaining the HLA-DRB5 discrepancy or drop it from `S01_immunoparalysis_genes_in_mars1.csv`, align every written instance of the IFN-γ rescue fraction and of the CD14 q-value to the single recomputed value from F7/F20 decisions, and add a one-line "(gene sets listed in Supplementary Table S-sets)" pointer at `manuscript.md:49`.

---

## 2. Stands up — things I verified myself and the authors must NOT weaken

**S1 · The direction claims and the 23/25 / 22/25 / 21 arithmetic are exactly right.**
I recomputed from `S01_immunoparalysis_direction.csv` (25 rows): **23 down, 2 up (PDCD1, LAG3)**; **22 with adj.P<0.05**, including PDCD1; therefore **21 both down and FDR-significant**. This matches `manuscript.md:82`, the abstract, the Chinese abstract and `manuscript.md:218` precisely. Table 1's individual values also reproduce exactly: HLA-DRB1 −0.893 / 1.07×10⁻¹⁵, CD74 −0.758 / 2.08×10⁻¹⁵, CD14 −0.766 (adj.P 0.0, P underflow), FCGR3A −0.610 / 9.05×10⁻¹¹, HAVCR2 −0.349 / 2.84×10⁻¹³, HLA-DRA −0.469 / 3.77×10⁻⁷, LYZ −0.256 / 3.56×10⁻⁶, ITGAM −0.208 / 1.68×10⁻³, PDCD1 +0.162 / 3.00×10⁻¹⁰; all four headline genes have P<1×10⁻⁸. **Do not touch these numbers.**

**S2 · Every MR number in Tables 3 and 4 reproduces, including the awkward ones.**
I recomputed all three outcome files row by row: IVW/Egger/weighted-median ORs, 95% CIs, P values, Cochran-Q P, per-outcome I² (including FIS1 critical care I²=0.502 and CD14 susceptibility I²=0.379), and median instrument F (35.4 CD74, 168.1 HLA-DQA1, 45.7 CD14, 36.4 HAVCR2, 75.0 FIS1; minimum F 30.7). The 45-test BH family table is consistent with the three CD74 rows below q<0.05 (family q = 0, 1.49×10⁻¹¹, 2.47×10⁻³) and CD14 at 0.058. Except for the SE issue in F12, the MR layer reports its own results faithfully and the decision not to make a causal claim is correct.

**S3 · I suspected the compositionally-inverted reading of the score could have been fabricated; the "Mars1 lowest" point estimate is genuine and the endotype really does carry the worst outcome.**
Recomputed: Mars1 has the highest 28-day mortality of the four endotypes (**34.1%** vs 21.6 / 17.8 / 18.9%), consistent with Scicluna's published 39% discovery-cohort figure and Mars1's HR 1.86. The deficit will survive; it just needs the Mars1-vs-Mars2 test reported honestly (F4).

**S4 · The external validation is honestly reported and the numbers reproduce.**
Recomputed from `09_external_validation.csv`: 29/30 genes mapped, n=106, 52 deaths / 54 survivors, equal-weight AUC 0.638 (0.532–0.748), locked L1 0.585 (0.469–0.696), IRG benchmark 0.604; all match the text. The decision to lead with the external estimate and explicitly label the within-cohort 0.659 as optimistic is correct practice and should be preserved verbatim.

**S5 · The glucocorticoid positive-control caveat is the strongest sentence in the paper.**
`manuscript.md:139` — that prednisone (rescue 0.136, rank 651/20,413) and dexamethasone (0.032, rank 6,808) score high despite being immunosuppressive — is the single most credible piece of self-criticism in the manuscript, together with the disclosure at `manuscript.md:135` that the intended dual-direction reversal was never implemented. Keep both; they are what make the repositioning section publishable as hypothesis generation.

**S6 · The honest handling of FIS1 already goes further than most papers would.**
`manuscript.md:103` explicitly flags FIS1 as non-immune, directionally concordant but "most plausibly a co-expression passenger", reported as a marker not a target. Do not remove this in revision — extend it as in F3.

**S7 · All figure callouts resolve to real files; all 30 DOIs in `reference_doi_audit.csv` audit as OK.**
Nothing missing from `04_figures/`.

---

## 3. Questions for the authors

1. **Beautiful consequences aside — was any deconvolution or composition adjustment attempted and abandoned?** If yes, report it; if no, that is a legitimate answer but it changes how §3.1 must be worded (F1).
2. **Where is the per-gene curation provenance for the seven drug response sets?** I need one citation per gene–drug pair, specifically: what source supports "IL-7 up-regulates IL7R", given that IL-7 signalling down-regulates CD127? (F6)
3. **Which Mars1-down set does `response_gene_concordance` use: all 25 consensus genes, or only the 21 FDR-significant down ones, or only the `DEG_0.3=True` subset?** The answers differ (F7), producing 1.00 vs 0.80 for IL-7 and 0.71 vs 0.57 for IFN-γ.
4. **Can SRS1/SRS2 labels for E-MTAB-4451 be reconstructed from the public SDRF or from Davenport's supplement?** If they can, please run the analysis in F13; if they cannot, please say so in one sentence.
5. **Was the CD74 critical-care MR-Egger standard error cross-validated against an independent implementation?** (F12)
6. **Was any literature search beyond the single database used by the reference pipeline performed after the 2026-09-26 DOI audit?** ImmunoSep (JAMA 2025) and the mHLA-DR monitoring literature are the two omissions I would most expect a second source to have caught, and the "no prior study has combined…" gap claim depends on search breadth. (F5, F15)
7. **Which interferon-γ product, route and dose does the companion protocol mean at "10–100 U/mL"?** Please map it to the exposure achieved in the ImmunoSep arm so the in-vitro dose has a clinical referent. (F8)
8. **Please confirm whether the six hub genes were also tested outside the 802-sample cohort.** Limitation 10 already concedes the need; my question is whether any such test exists and was omitted, or truly none was run.
9. **Is there a reason FIS1's cell-module correlations are reported for the five immune hubs only?** If it was an authoring omission rather than a deliberate choice, the numbers are at F3.

---

## 4. What I actually checked

**Read in full:** `05_reports/manuscript.md` (all 288 lines, including the four lines that exceed 2,000 characters and are truncated by standard viewing — lines 72, 135, 181, 190 were read in full), `05_reports/review_r6/_PANEL_BRIEF.md`, `03_results/11_validation_design.md`.

**Recomputed from `03_results/` (values are mine, not the manuscript's):**

| Quantity (source file) | My recomputation | Manuscript | Verdict |
|---|---|---|---|
| Direction split, `S01_immunoparalysis_direction.csv` | 23 down / 2 up; 22 adj.P<0.05; 21 down & significant | same | matches |
| HLA-DRB1 / CD74 / CD14 / FCGR3A / HAVCR2 / HLA-DRA / LYZ / ITGAM / PDCD1 Δ & adj.P | see S1 | same | matches |
| LAG3 Δ & adj.P | +0.035, 0.552 | called part of the "up-regulated exhaustion axis" | **over-claimed (F10)** |
| Immune score medians, `S02_immunoparalysis_score.csv` | Mars1 −0.792, Mars2 −0.752, Mars3 +0.641, Mars4 −0.235, unassigned +0.238; range −3.650 to 3.862 | Mars1 −0.79; range −3.65 to 3.86 | matches; **Mars1 vs Mars2 P=0.467 unreported (F4)** |
| 28-day mortality by endotype | Mars1 34.1%, Mars2 21.6%, Mars3 17.8%, Mars4 18.9% | claims 39% from Scicluna | **attribution missing (F16)** |
| Immune score vs death AUC (negated) | 0.604 (n=479) | never reported | **promised at :100, absent (F4)** |
| Mars1 binary vs death AUC, `S06_auc_compare.csv` | 0.5782 | 0.578 | matches |
| CV / train AUC | 0.6586 / 0.7495 | 0.659 / 0.750 | matches |
| DEG counts | Mars1 3,597; sepsis-vs-ctrl 448 (of 11,519) | same | matches |
| External validation, `09_external_validation.csv` | 0.638 (0.532–0.748); L1 0.585 (0.469–0.696); IRG 0.604; 29/30 genes; 52/54 | same | matches |
| Degree ranking, `S03_hub_degree.csv` | top-25 non-immune; hub ranks CD74 595, HLA-DQA1 1102, FCGR3A 1516, CD14 1766, HAVCR2 1927; FIS1 12 | claims convergence | **contradicted (F2)** |
| Candidate set, `S04_candidate_genes.csv` | 35 = 15 immune + exactly the top-20 degree genes | not described | **undisclosed route (F2)** |
| Cell-type localisation, `07_hub_celltype.csv` | five hubs +0.298 to +0.773; **FIS1 best corr −0.438** | FIS1 omitted | **omission (F3)** |
| Axis module means, `07_axis_celltype.csv` | CD4 0.618, CD8 0.582, DC 0.459, NK 0.419, B 0.401, Neut 0.319, **Mono 0.222 (lowest)** | numbers right, "monocyte/APC" framing | **framing conflict (F1)** |
| Signature correlations, `S06_signature_genes.csv` | ELANE +0.170 top; MPO +0.152; S100A8 +0.091 | "almost all negative" | **omission (F14)** |
| Drug fractions, `08_candidates_drugs.csv` | as printed; DEG-filtered recomputation gives IL-7 0.80, GM-CSF 0.67, IFN-γ 0.57, azithromycin 0.67 | IL-7 1.00, GM-CSF 0.83, IFN-γ 0.71 | **threshold-dependent (F7)** |
| Positive control gate, `08_positive_control_check.csv` | **4/5** (HLA-DRA, HLA-DRB1, HLA-DQA1, CD74) | abstract says **5/5** | **contradiction (F7)** |
| HAVCR2 direction | Mars1_down (−0.349) | `11_validation_design.md:84` says Mars1-up | **error (F9)** |
| MR, all three outcome files + harmonised | all Table 3/4 values, I², Q, median F reproduce | see S2 | matches except F12 |
| CD74 critical-care SE structure | IVW se 0.325 vs Egger se 0.111 with n=3 | presented as q≈1.5×10⁻¹¹ | **internally incoherent (F12)** |
| L1000 named hits, `S08_l1000_immuno_overlap.csv` | pravastatin 17, geldanamycin 25, tetrachloroethylene 666, etc. | not discussed | **omission (F17)** |
| S11 power claim | n=3 → 47%; n=5 → 91% | claims n=3 gives 80% | **wrong (F18)** |

**Literature checks I performed (not data downloads):** verified Scicluna et al. 2017 Mars1 = 35/90 = 39% 28-day mortality, HR 1.86, and the explicit Mars1 description as reduced innate/adaptive programmes **plus increased heme-biosynthesis metabolism**; verified full IRIS-7 details (n=27 Phase 2b safety/lymphocyte-count endpoint, CYT107 10 µg/kg, no mortality endpoint); verified **ImmunoSep (Giamarellos-Bourboulis et al., JAMA 2025, doi:10.1001/jama.2025.24175**, NCT04990232, n=276, IFN-γ vs placebo in mHLA-DR-defined sepsis-induced immunoparalysis, primary endpoint 35.1% vs 17.9% P=0.002, no 28-day mortality difference, excess haemorrhage, 53% of screened patients unclassifiable).

**Not read (per independence discipline):** any `REVIEW_round*.md`, `review_r*/`, `review/`, `RESPONSE_*`, `REVISION_*`, `SUBMISSION_MANIFEST.md`, `author_verification_statement.md`, `GITHUB_DEPOSIT_SOP.md`, any overview/status file, or any other reviewer's output in `review_r6/`. I did **not** read any file outside `05_reports/manuscript.md`, `_PANEL_BRIEF.md`, `03_results/`, `04_figures/` and one filename listing of `02_scripts/` (used only to check whether the score's gene sets are persisted anywhere; they are not).

---

## 5. Verdict

**Major revision.**

Justification — the strongest single reason: **the paper's core biological claim is not distinguished from its principal alternative explanation.** The evidence offered for "Mars1 immunoparalysis centred on antigen presentation" — a coordinated fall in CD3D/E/G, LCK, IL7R, CD8A/B alongside CD14, LYZ and HLA-II — is exactly what falling circulating monocyte and lymphocyte content produces in bulk whole blood, and the authors' own `07_axis_celltype.csv` puts the monocyte module *dead last* (mean |r| 0.222) while CD4/CD8 T-cell modules lead (0.618/0.582), directly contradicting the abstract's "localised to monocytes/antigen-presenting cells". Nothing in the manuscript names, tests, or adjusts for this. Compounding it, the one member of the hub set contributed by the co-expression network arrives from a module whose top nodes are GATA1, EPB49 and ANK1 with FIS1 at rank 12, while the five genuine hubs sit between ranks 595 and 1,927 of 2,000 — so the "network + ML convergence" that licenses the hub list did not occur as described. Both are answerable with two specified analyses (composition adjustment; honest restatement plus an S-hub-src table), and both are the kind of defect that, once pointed out, cannot be unseen by any sepsis-aware reader or reviewer.

Secondarily but independently decisive for the clinical layer: the paper's candidate-readiness ranking omits **ImmunoSep (JAMA 2025)**, in which patients with exactly the phenotype this manuscript nominates — low monocyte HLA-DR — were randomised to subcutaneous recombinant interferon-γ, with improved day-9 organ dysfunction, no 28-day mortality benefit, and excess haemorrhage. That trial simultaneously invalidates the statement that IFN-γ has "limited sepsis-specific signals" and hands the authors their best available translational argument (over half its screened patients could not be classified at all by protein biomarkers, which is precisely the gap a transcriptomic endotype claims to fill). A revision that incorporates it becomes markedly stronger; one that does not will be judged against it.

I do not recommend rejection: the Tier-1 immunoparalysis observation reproduces, the 23/25 direction result and every front-line statistic I recomputed were exactly correct, the cytokine/repository layers are reported with unusual statistical honesty, and the authors' own caveats about transcriptional-reversal-not-equalling-functional-rescue are the right ones. But the paper currently asserts more biology than its design can support, and that must be repaired before it is defensible.
