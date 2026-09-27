# Reviewer A1 — Domain Review (Sepsis Immunology / Immunoparalysis / In-silico Repositioning)

**Manuscript:** "Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning"
**Review type:** Fresh first-submission review. I have not read any prior review round.
**Verdict:** **Major Revision** (no desk-reject flag).

---

## Summary of judgement

The analysis is unusually careful and self-auditing for a single-author bioinformatics paper: the numbers I recomputed from `03_results/` match the prose almost exactly, the external-validation claim is honestly bounded, and the positive-control logic (glucocorticoid high-rescue caveat, ImmunoSep as caution) is sound. However, three domain problems need correction before publication:

1. **(Major) The checkpoint-blockade "contraindication" reasoning is biologically inverted.** T-cell exhaustion is *defined* by over-expression of inhibitory receptors; checkpoint blockade is the standard therapy that *reverses* exhaustion. Arguing blockade is "contraindicated because the program is already exhausted" flips the core rationale of anti–PD-1/PD-L1 therapy.
2. **(Major) Title/methodology over-claim — "multi-omics" and "virtual knockout."** No proteomics/metabolomics/methylation is performed; the only non-transcriptomic layer is an eQTL MR (itself a transcriptomic proxy). No virtual knockout/knockdown simulation exists — the repositioning layer is curated concordance + LINCS L1000 reverse-connectivity.
3. **(Moderate) The "exhaustion axis" label on the hub set is internally inconsistent.** Among the five immune hubs, only HAVCR2/TIM-3 relates to exhaustion and it is *down*-regulated; the up-regulated exhaustion marker (PDCD1) is explicitly *outside* the hub set.

None of these invalidate the Tier-1 biology, which is solid and well-replicated.

---

## Issue 1 — Checkpoint-blockade "contraindication" is biologically backwards

- **【Problem】** The manuscript excludes checkpoint-blockade agents on the stated ground that "further releasing an already exhausted T-cell program is mechanistically contraindicated," which inverts established exhaustion biology.
- **【Evidence】** `manuscript.md:143` (§3.8): "we therefore did *not* prioritise checkpoint-blockade agents (anti–PD-1/PD-L1, anti–CTLA-4), because further releasing an already exhausted T-cell program is mechanistically contraindicated in this endotype and, in early sepsis trials, anti–PD-1 (nivolumab) showed no efficacy signal [34]." Contrast with the verified Mars1 expression data: the only exhaustion marker *up*-regulated is **PDCD1** (logFC +0.1619, adj.P = 2.99×10⁻¹⁰; `S01_immunoparalysis_direction.csv:8`), whereas **HAVCR2/TIM-3 is itself down** (logFC −0.3488, adj.P = 2.84×10⁻¹³; `S01_immunoparalysis_direction.csv:6`) and LAG3 is only directional (logFC +0.035, adj.P = 0.552; line 26).
- **【Why it matters】** T-cell exhaustion is *defined* by co-expression of inhibitory receptors (PD-1, TIM-3, LAG-3, CTLA-4); the entire clinical rationale for anti–PD-1/PD-L1 in cancer and chronic infection is that blockade *reinvigorates* exhausted T cells. Stating that blockade is "contraindicated because the program is already exhausted" teaches the opposite of the accepted mechanism and will be flagged immediately by any immunology reviewer. It also misreads the nivolumab evidence: Hotchkiss et al. 2019 (ref 34) is a Phase-1b *safety/PD* study that found PD-1 up-regulation on a T-cell subset and was underpowered for efficacy — an *absence* of efficacy signal, not a demonstration of harm/contraindication.
- **【Specific fix】** Replace the sentence at `manuscript.md:143` with:
  > "We therefore did not prioritise checkpoint-blockade agents (anti–PD-1/PD-L1, anti–CTLA-4). The dominant Mars1 lesion is antigen-presentation/monocytic failure (HLA-class-II, CD14 and FCGR3A all significantly down; see §3.1), i.e. an APC/innate defect more than a T-cell-intrinsic one, so APC-restorative immunotherapy (IFN-γ/GM-CSF) is more on-target than T-cell checkpoint modulation. Although PDCD1 is up-regulated, TIM-3/HAVCR2 is down-regulated and LAG3 is only directional (adj.P = 0.55), so a TIM-3–centric exhaustion axis is not established among the hubs. The single early-phase nivolumab trial in sepsis (Hotchkiss et al. [34]) was underpowered for efficacy and does not establish checkpoint blockade as beneficial; prospective stratification is required before any such strategy."

---

## Issue 2 — "multi-omics" and "virtual knockout" are not substantiated

- **【Problem】** The title and abstract claim a "multi-omics dissection" and "virtual knockout drug repositioning," but the analysis is single-transcriptomics plus a genetics MR layer, and no gene knockout/knockdown perturbation is performed.
- **【Evidence】** `manuscript.md:1` (title): "… a multi-omics dissection and in-silico drug repositioning"; `manuscript.md:14` (abstract): "the virtual-KO / LINCS rescue logic." Methods (§2.1–2.10) use only GSE65682 bulk microarray + E-MTAB-4451 bulk microarray + eQTL MR. A targeted grep of the manuscript for `methylat|epigenet|proteom|metabolom` returns only the title (line 1) and the discussion "multi-omics triangulation" (line 192); no methylation/proteomics/metabolomics step is described. `DATA_SOURCES.md` lists epigenetic/GTEx references, but they are never used in the methods. The repositioning layer is (a) curated `response_gene_concordance` (§2.8) and (b) **LINCS L1000 reverse-connectivity** (§3.9, `S08_l1000_rescue_trtcp.csv`) — a standard connectivity-map gene-set enrichment, i.e. an *axis-reversal proxy*, not a virtual knockout.
- **【Why it matters】** "Virtual knockout" implies an in-silico gene-perturbation step (e.g., simulating hub-gene knockdown and observing axis rescue) that does not exist here. The claim over-states both the breadth of the omic evidence and the novelty of the method, and invites a methods-accuracy objection at copy-editing or reviewer stage.
- **【Specific fix】** (a) Retitle / relabel: drop "multi-omics" → "a transcriptomic dissection with genetic triangulation," and replace "virtual knockout drug repositioning" with "in-silico expression-axis rescue / LINCS reverse-connectivity drug repositioning" throughout (title line 1, abstract line 14, §4 line 192, and the repository/folder naming). (b) If a genuine second omic layer (methylation/deconvolution) was intended, either add it or remove the claim. (c) In §2.8/§3.9, state explicitly: "No in-silico gene-knockout/knockdown simulation was performed; 'rescue' denotes LINCS L1000 reverse-connectivity of the Mars1-down gene set."

---

## Issue 3 — The hub set's "exhaustion axis" is mislabeled

- **【Problem】** The five immune hubs are repeatedly called "antigen-presentation / monocytic / exhaustion-axis genes," but the only exhaustion-related hub (HAVCR2/TIM-3) is *down*-regulated, while the up-regulated exhaustion marker (PDCD1) is not a hub.
- **【Evidence】** `manuscript.md:14` (abstract) and `manuscript.md:114` (§3.3) describe the five as "antigen-presentation / monocytic / exhaustion-axis genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2)." Verified directions: HAVCR2 logFC −0.3488 (down, FDR-sig) `S01_immunoparalysis_direction.csv:6`; PDCD1 logFC +0.1619 (up, FDR-sig) line 8 — and PDCD1 is **not** in `S05_hub_genes.csv` (the six hubs are FIS1, HAVCR2, HLA-DQA1, CD14, FCGR3A, CD74). So the hub set contains no up-regulated exhaustion marker.
- **【Why it matters】** A hallmark of T-cell exhaustion is *up*-regulated TIM-3; here TIM-3/HAVCR2 is down, so folding it into an "exhaustion axis" within the hubs is inaccurate and muddles the otherwise clean "MARS = antigen-presentation/monocytic suppression" story. It also undercuts the checkpoint argument in Issue 1 (there is no TIM-3–up exhaustion signature to block).
- **【Specific fix】** In §3.3 and the abstract, re-label the five as "antigen-presentation/monocytic hubs, with HAVCR2/TIM-3 co-down-regulated," and add: "The up-regulated exhaustion marker in Mars1 is PDCD1, which lies outside the hub set; LAG3 was only directionally up (adj.P = 0.55). The Mars1 program is therefore best characterized as antigen-presentation/monocytic suppression with a weak, partial T-cell exhaustion signal, not a TIM-3–driven exhaustion axis."

---

## Issue 4 — Two discordant "concordance" metrics for the same drugs

- **【Problem】** Table 2 (`08_candidates_drugs.csv`) and `08b_clinical_translation.csv` report different concordance fractions for the same agents under similarly named columns, with no stated reconciliation.
- **【Evidence】** `08_candidates_drugs.csv`: IL-7 0.80 (4/5), GM-CSF 0.67 (4/6), IFN-γ 0.57 (4/7). `08b_clinical_translation.csv`: IL-7 `rescue_fraction_directional` 1.0, GM-CSF 0.833, IFN-γ 0.714 — a different scoring/denominator. The manuscript text (§3.7, Table 2) uses the S08 numbers; the 08b "directional" column is an undocumented redefinition.
- **【Why it matters】** A reader comparing the two tables sees conflicting rankings for the same drug and cannot tell which is the primary metric; this weakens the repositioning transparency the paper otherwise does well.
- **【Specific fix】** Either harmonize the metric (use one definition) or explicitly label `08b_clinical_translation.csv`'s `rescue_fraction_directional` as a *secondary, differently-scored annotation* and state that Table 2's ranking uses `08_candidates_drugs.csv`. Add one sentence in §3.7 clarifying the two columns are not interchangeable.

---

## Issue 5 — MR outcome provenance / must-cite gap (Minor)

- **【Problem】** The UK Biobank sepsis GWAS outcomes (`ieu-b-4980/5086/4982`) are used but their originating GWAS publication is not cited; the foundational Connectivity Map (Lamb et al.) is also absent.
- **【Evidence】** `manuscript.md:70` (§2.10) cites only the IEU/MR-Base platform (Hemani 2018, ref 10) for the outcome IDs, not the source sepsis GWAS. `ref 7` is Subramanian 2017 (L1000) but the original CMAP method (Lamb et al., *Science* 2006) is not cited.
- **【Why it matters】** Outcome-source provenance is a STROBE-MR expectation; omitting the originating GWAS and the CMAP progenitor slightly weakens methodological citation completeness.
- **【Specific fix】** Add the originating UK Biobank sepsis GWAS citation that produced `ieu-b-4980/5086/4982`, and cite Lamb et al., *Science* 2006 (The Connectivity Map) alongside Subramanian 2017.

---

## § Stands up (verified correct despite my suspicion)

1. **FIS1 is genuinely a non-immune, up-regulated mitochondrial-fission passenger.** I suspected the author had mislabeled FIS1 as immune. Verified: FIS1 logFC **+1.2614**, t = +17.16, `DEG_1.0 = True` (`S01_mars1_deg.csv`, FIS1 row); it is absent from the consensus immune set (`S05_hub_genes.csv` only marks it via ML, not immune annotation). Framing it as a co-expression passenger rather than an immune hub is correct and honest.
2. **Mars1 antigen-presentation/monocytic suppression is real and directionally coherent.** Verified: CD74 −0.7578, CD14 −0.7657, FCGR3A −0.6097, HLA-DQA1 −0.5301, HAVCR2 −0.3488 — all significantly down (`S01_immunoparalysis_direction.csv`). Of 25 consensus immune genes, **23 down**, **22 FDR-significant**, **21 down+FDR-sig** with PDCD1 the single up member (line 8) — exactly as stated. This matches the established Mars1 biology.
3. **External validation is honestly bounded.** Verified `09_external_validation.csv`: oriented-sum (equal-weight) AUC **0.6382** (95% CI 0.5317–0.7475); L1-locked AUC **0.5848** (CI 0.4687–0.6959). The manuscript correctly reports 0.638 as primary and 0.585 as the (weaker) transported L1 model, and notes L1 weights did not generalize — a rare, commendable honesty about optimism.
4. **Cellular localization claims are accurate.** Verified `07_hub_celltype.csv`: CD14→Monocyte r = 0.773, FCGR3A→Monocyte 0.491, CD74→Dendritic 0.690, HAVCR2→Monocyte 0.298, HLA-DQA1→B-cell 0.681 — all match §3.6.
5. **Positive-control logic is sound and candid.** Verified `S08_l1000_positive_control.csv`: prednisone rescue 0.136 (rank 651/20413), dexamethasone 0.0315 (rank 6808) — both high despite being immunosuppressive, correctly flagged as "necessary but not sufficient." IFN-γ 4/5 rescue verified (`08_candidates_drugs.csv`, IFN-gamma row). ImmunoSep (ref 32) is used as *caution* (SOFA benefit, no mortality benefit, more haemorrhage) — correctly, not as support.
6. **Phenotype provenance is exact.** Verified `GSE65682_pheno.csv`: 802 rows; sepsis 760 / healthy 42; Mars1 132, Mars2 176, Mars3 118, Mars4 53, unassigned 323; death 114/365/323. Matches every count in §2.1 and the provenance table (§7).

---

## § Questions for the authors

1. The ImmunoSep "53% unclassifiable by mHLA-DR" figure (§3.8) — is this the per-screened-patient rate reported in Giamarellos-Bourboulis 2025, and was the mHLA-DR threshold the trial's own cut-off? (I could not verify the exact percentage from the source.)
2. For the LINCS rescue, you aggregate all 22 query genes with one sign, so PDCD1/LAG3 *up*-regulation is rewarded. Given PDCD1 is the one genuinely up exhaustion marker, did you explore a dual-direction metric (down antigen-presentation + down exhaustion) as a sensitivity analysis, and did it change lenalidomide/azithromycin ranking?
3. FCGR3A was dropped from MR for having only 2 instruments. Was a proxy/colocalization or a surrogate cis-eQTL (e.g., a nearby tag SNP or a different eQTL source) considered, given FCGR3A is a core monocytic hub?
4. The degree-centrality co-expression screen surfaced an erythroid/heme module (GATA1, CGB, EPB49) with FIS1 12th — is the heme program in Mars1 something you considered as a biologically interesting secondary finding rather than only a "passenger" caveat?

---

## § What I actually checked

**Files read in full / part:**
- `05_reports/manuscript.md` (full) — all numbers below traced to source.
- `03_results/S01_mars1_deg.csv` — verified FIS1 (+1.2614, t 17.16, DEG_1.0 True), CD74/CD14/FCGR3A/HAVCR2/HLA-DQA1/PDCD1/LAG3 directions.
- `03_results/S01_immunoparalysis_direction.csv` — verified 23 down / 22 FDR-sig / 21 down+sig + PDCD1 up; recomputed the 22-significant count by hand (all except CD8B 0.077, GZMA 0.110, LAG3 0.552).
- `03_results/S05_hub_genes.csv` — 6 hubs confirmed (all three ML methods True).
- `03_results/08_candidates_drugs.csv` and `08b_clinical_translation.csv` — verified concordance values and the S08-vs-S08b discrepancy.
- `03_results/S08_l1000_candidate_scores.csv` — lenalidomide rank 5435/20413 (rescue 0.0439), azithromycin 9152/20413 (rescue 0.0133). Matches text.
- `03_results/S08_l1000_positive_control.csv` — prednisone 0.136/rank 651, dexamethasone 0.0315/rank 6808. Matches text.
- `03_results/S06_auc_compare.csv` — CV AUC 0.6586, train 0.7495, IRG 0.619/0.648. Matches abstract.
- `03_results/09_external_validation.csv` — oriented-sum AUC 0.6382 (CI 0.5317–0.7475), L1-locked 0.5848 (CI 0.4687–0.6959), IRG recomputed 0.604. Matches §3.5.
- `03_results/07_hub_celltype.csv` — all five localization r-values match §3.6.
- `01_data/GSE65682/GSE65682_pheno.csv` — 802/760/42, endotype and death counts match §2.1 exactly.
- `DATA_SOURCES.md` — confirmed no methylation/proteomics actually used by the manuscript methods.

**Recomputed vs manuscript (no discrepancies found except the conceptual/labeling issues above):**
- Hub gene logFC/P: exact match.
- 23/25, 22-sig, 21 down+sig: exact match.
- AUC 0.659/0.750, external 0.638 (0.585 L1): exact match.
- LINCS ranks and glucocorticoid controls: exact match.
- Phenotype counts: exact match.

**Discrepancies / concerns stated:**
- No "virtual knockout" step exists (terminology only).
- "multi-omics" unsupported by methods.
- Checkpoint "contraindication" reasoning inverted (Issue 1).
- "exhaustion axis" label on hubs inconsistent with HAVCR2-down / PDCD1-not-a-hub (Issue 3).
- S08 vs S08b concordance metrics discordant/unreconciled (Issue 4).
- MR outcome GWAS source and CMAP progenitor not cited (Issue 5).

**Not verified (out of scope / no access):** the exact 53% ImmunoSep unclassifiability rate; the internal content of `04_figures/` (figures not opened, only the CSVs they report); the eQTLGen instrument-level `*_harmonised.csv` files (MR table values taken as reported and internally consistent with the manuscript's caveats).
