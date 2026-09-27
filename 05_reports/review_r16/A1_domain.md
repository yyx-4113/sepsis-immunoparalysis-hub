# Round-16 blind-domain review — biological / clinical plausibility
**Reviewer focus:** sepsis immunology; Mars1 framing vs MARS literature; hub coherence; FIS1 as non-immune passenger; PD-1(up)/TIM-3(down) distinction; drug-shortlist anchors; biologically false claims or must-cite omissions.
**Manuscript tag:** v1.16.0 · target *Scientific Reports*. Read as a first submission; every judgement traced to text or source data I recomputed.

---

## Issues

### Issue 1 — FIS1's Mendelian-randomisation direction is mis-attributed as "concordant with the immunoparalysis model"
【Problem】 The manuscript states that three of five assessable hubs (HLA-DQA1, CD14, **FIS1**) "returned protective estimates concordant across all three methods … the direction predicted by the immunoparalysis model," but FIS1's observational direction is *opposite* to that claim.

【Evidence】
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv` (primary 28-day death): FIS1 IVW OR 0.963, MR-Egger OR 0.964, Weighted-median OR 0.971 — all <1 (protective).
- `03_results/S01_mars1_deg.csv`: FIS1 logFC = **+1.261**, t = +17.16, Mars1-**UP**, adj.P ≈ 0.
- Mars1 is the high-mortality immunosuppressed endotype (39% 28-day mortality; manuscript §1, citing Scicluna 2017).
- Therefore observationally *high FIS1 ↔ high mortality* (Mars1), but MR says *high genetically-predicted FIS1 → lower mortality*. The two point in opposite directions.
- The five immune hubs are *down* in Mars1, so "low hub ↔ high mortality" is observationally consistent with MR "high hub → low mortality" (truly concordant). FIS1 is the odd one out and is explicitly framed as a passenger *outside* the immunosuppression axis (§3.3, §6).

【Why it matters】 Folding FIS1 into the "concordant with the immunoparalysis model" sentence implicitly lends the passenger gene the same biological endorsement as the antigen-presentation hubs, and inverts its true relationship to the Mars1 program. A careful reader who checks the DEG table will see the contradiction; it weakens the honestly-presented Tier-3 framing.

【Specific fix】 Restrict the concordance claim to the immune hubs and explicitly state FIS1 is discordant. Suggested replacement (§3.10 / §4):
> "Against the phenotype-matched primary outcome, the three antigen-presentation/monocytic hubs (HLA-DQA1, CD14, and the CD74 direction aside) returned protective estimates concordant across IVW, MR-Egger and the weighted median — the direction predicted by their down-regulation in the high-mortality Mars1 program. FIS1, included as a non-immune co-expression passenger, also gave protective point estimates, but these are *opposite* to its observational up-regulation in Mars1 and are not predicted by the immunoparalysis model; its MR result is reported descriptively only."

---

### Issue 2 — Mild internal tension: FIS1 is "not a mechanistic target" yet is carried as a causal MR candidate
【Problem】 FIS1 is repeatedly described as a co-expression passenger / marker "not a mechanistic target" (§3.3, §6, Conclusion), but §3.10 treats it identically to the five immune hubs as one of "six candidate genes" tested for *causal* effect on sepsis outcomes, and §5 limitation 2 lists it among the protective hubs.

【Evidence】 `03_results/S05_hub_genes.csv` carries FIS1 as True across lasso/rf/univariate (a "hub" by the ML gate); `10_genetics_mr_outcome5086_28ddeath.csv` includes FIS1 as a causal candidate. Conclusion §6: "a sixth co-expression-linked gene, FIS1 … reported as a co-expression passenger rather than an immune hub."

【Why it matters】 Not a false claim, but the narrative oscillates between "pure passenger" and "causal candidate," which a reviewer may read as hedging. The MR inclusion is defensible (all six nominated genes are tested), but the passive framing should be reconciled.

【Specific fix】 Add one sentence to §3.10 or §5: "FIS1 was retained in the MR tier because it is one of the six ML-nominated genes, but it is interpreted as a passenger whose MR estimate is hypothesis-generating only and is not read as evidence for a mitochondrial-fission target." Non-blocking.

---

### Issue 3 — PD-1(up)/TIM-3(down) result is data-true but its contrast with the canonical sepsis exhaustion literature is not cited
【Problem】 The manuscript correctly reports PDCD1 up and HAVCR2 down and uses this to argue against the canonical TIM-3-up exhaustion signature, yet it does not cite the sepsis literature that documents TIM-3 *up*-regulation / PD-1–TIM-3 co-expression on exhausted T cells — the very literature its result appears to contradict.

【Evidence】 `03_results/S01_immunoparalysis_direction.csv`: PDCD1 logFC +0.162 (Mars1_up), HAVCR2 logFC −0.349 (Mars1_down). Manuscript §3.1 / §4 discuss "PD-1/TIM-3 co-expression more broadly characterises exhausted T cells" without a primary TIM-3-in-sepsis reference; refs [3] (Hotchkiss 2013) and [35] (nivolumab) address immunosuppression/PD-1 but not TIM-3 specifically in sepsis.

【Why it matters】 A claim that contradicts an established view should engage that view directly. Citing the opposing TIM-3-up sepsis evidence strengthens the manuscript's credibility and shows the authors understand the discrepancy they are resolving (rather than merely noting a bulk-measurement caveat).

【Specific fix】 Add 1–2 citations on TIM-3/PD-1 co-expression in human sepsis (e.g., studies reporting increased TIM-3 on CD4/CD8 T cells in septic patients) to §3.1 or §4, framed as: "whereas prior reports show TIM-3 up-regulation on exhausted T cells in sepsis, the present bulk signal shows HAVCR2 down, a discrepancy most parsimoniously explained by cell-abundance loss (see bulk caveat) rather than per-cell checkpoint engagement." Non-blocking.

---

### Issue 4 — Recurring phrase "reduced checkpoint engagement" leans on a per-cell reading bulk data cannot support
【Problem】 "Reduced checkpoint engagement" (Abstract, §3.1, §4, Conclusion) implies lower per-cell TIM-3 signalling, but the authors themselves note the bulk measurement cannot separate reduced APC/T-cell abundance from lower per-cell expression.

【Evidence】 Manuscript §3.1: "Because this is a bulk-blood measurement, the direction cannot distinguish reduced APC/monocyte abundance from lower per-cell expression … single-cell or flow-cytometric resolution is required." The per-cell interpretation resurfaces uncaveated in Abstract/Conclusion.

【Why it matters】 In immunoparalysis the dominant bulk signal is leukocyte/APC loss, so "down-regulated HAVCR2" most likely reflects fewer TIM-3-bearing cells, not "disengaged" checkpoints. The phrase, unqualified in the abstract, over-interprets the data the manuscript elsewhere correctly hedges.

【Specific fix】 Soften to "lower HAVCR2/TIM-3 transcript levels, of uncertain cellular basis (cell-loss vs per-cell down-regulation)," at least in Abstract and Conclusion; keep the fuller caveat in §3.1. Non-blocking.

---

### Issue 5 — Reference year mismatch for the ImmunoSep trial (cosmetic)
【Problem】 The brief and the clinical-translation text describe Giamarellos-Bourboulis et al. as "ImmunoSep JAMA 2025," but the reference list reads "(JAMA **335**, 775–786 (**2026**))" with doi:10.1001/jama.**2025**.24175.

【Evidence】 manuscript.md ref [31]: "Giamarellos-Bourboulis, E. J. et al. … *JAMA* **335**, 775–786 (2026). doi:10.1001/jama.2025.24175." Cover letter / §3.8 call it "JAMA 2025."

【Why it matters】 Cosmetic only, but an inconsistent year between text and reference list is an easy copy-edit flag for the editorial office.

【Specific fix】 Reconcile to the published record (ahead-of-print 2025 vs issue 2026); use one year consistently in text and reference. Non-blocking / cosmetic.

---

## § Stands up (verified against source data)
1. **PD-1(up)/TIM-3(down) distinction is real and exactly as reported.** `S01_immunoparalysis_direction.csv`: PDCD1 logFC +0.162 (Mars1_up, adj.P 3.0e-10), HAVCR2 logFC −0.349 (Mars1_down, adj.P 2.8e-13). The abstract's central biological distinction is data-grounded, not asserted.
2. **Hub coherence is strong.** All five immune hubs (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) are antigen-presentation/monocytic/checkpoint genes and are *directionally down* in Mars1 (all negative in the direction file); the set parsimoniously recapitulates the established MARS Mars1 antigen-presentation program. This is a genuine near-replication, honestly framed as confirmation rather than discovery.
3. **Immune-gene directionality counts are exact.** Of 25 consensus immune genes: 23 directionally down, 22 FDR<0.05, 21 both down and significant — recomputed from the 25-row file and matches §3.1 precisely.
4. **Drug-shortlist anchors are biologically accurate and correctly calibrated.** IL-7→IRIS-7 (François 2018, lymphopenia rescue), GM-CSF→Meisel 2009 (mHLA-DR restoration) with the Bo 2011 null-mortality meta-analysis cited as caution, IFN-γ→Döcke 1997, and ImmunoSep (Giamarellos-Bourboulis) used as a *caution* (SOFA improvement but no mortality benefit, more haemorrhagic events) rather than as checkpoint-blockade support. Nivolumab (Hotchkiss 2019) is correctly cited only as a Phase-1b safety/PK study not powered for efficacy to justify avoiding checkpoint inhibitors. Every anchor maps to a real, appropriately characterised trial.
5. **L1000 rescue ranks verify.** `S08_l1000_candidate_scores.csv`: azithromycin rank 9152 (44.8th percentile, ≈ median), lenalidomide rank 5435 (26.6th percentile) — exactly as stated; the glucocorticoid positive-control caveat (prednisone high, dexamethasone not) is a sound honesty check.
6. **MR primary-outcome summary is accurate.** From `10_genetics_mr_outcome5086_28ddeath.csv`: HLA-DQA1/CD14/FIS1 all-method protective; HAVCR2 null under Egger (OR 1.010); CD74 non-protective (IVW 1.119). "No primary IVW estimate reached significance" is correct (smallest IVW P = 0.236 for CD14).

---

## § Questions for the authors
1. For FIS1, do you have any independent evidence (e.g., correlation with a mitochondrial/erythroid module, or with the GATA1/CGB/EPB49 heme cluster noted in §3.3) that supports the "passenger" vs "driver" interpretation, or is the passenger label purely statistical (ML co-expression) by design?
2. Given TIM-3 is expressed on both APCs and T cells, could you state which cell compartment you hypothesise drives the bulk HAVCR2 down-signal, and whether flow/single-cell data from a public sepsis cohort could resolve it without new experiments?
3. The 30-gene signature includes neutrophil/inflammatory genes that are *up* with death (ELANE, MPO, S100A8 in `S06_signature_genes.csv`) alongside the antigen-presentation/monocytic genes that are down. Is the net protective signal therefore partly a neutrophil-inflammation proxy, and does this affect the "immunoparalysis signature" label?
4. For the MR, since FIS1's direction opposes its observational association, would you consider dropping it from the "concordant" sentence (per Issue 1) and reporting it as a standalone descriptive result?

---

## § What I actually checked
- **Read:** `05_reports/manuscript.md`, `05_reports/cover_letter.md`, and the source CSVs `S01_mars1_deg.csv`, `S01_immunoparalysis_direction.csv`, `S05_hub_genes.csv`, `S06_signature_genes.csv`, `S02_immunoparalysis_score.csv`, `08_candidates_drugs.csv`, `S08_l1000_candidate_scores.csv`, `10_genetics_mr_outcome5086_28ddeath.csv`.
- **Recomputed / verified:** FIS1 logFC +1.26 (up); PDCD1 up (+0.162) and HAVCR2 down (−0.349) in the direction file; the 23/25-down, 22-sig, 21-down+sig counts from the 25-gene list; all five immune hubs negative (Mars1_down); L1000 ranks 9152/5435; MR CD14 IVW 0.927 (P 0.236) / Egger 0.906 (P 0.049) / WM 0.914 (P 0.065); CD74 IVW 1.119; per-outcome `p_fdr_bh` for CD14 Egger = 0.487 (matches the stated 0.49).
- **Did NOT independently recompute (outside this reviewer's biology focus, and traced in the manuscript's §7 provenance table):** the external AUC 0.638 / 95% CI, the CV AUC 0.659, the calibration slope 0.50 / intercept −0.04, and the DCA grid. These are statistical outputs; I accepted them as reported because the brief's stated values match the manuscript and the file map is internally consistent, but I did not re-run the validation script.
- **Forbidden files not opened:** all prior REVIEW_round*.md, review_r12–r15, .workbuddy/memory, scirep_submission_checklist.md, and other reviewers' r16 files.
- **No biologically false factual claim was found.** The issues above are interpretive framing (Issue 1 is the material one) and minor citations/cosmetics.

---

## VERDICT
**Minor** — The biology is sound, the Mars1 framing is an honest near-replication, hub coherence and the PD-1/TIM-3 data distinction are verified, and every drug anchor is accurate and correctly calibrated. The single material defect is the mis-attribution of FIS1's *opposite-direction* MR estimate as "concordant with the immunoparalysis model" (Issue 1), plus low-priority framing/citation items (Issues 2–5, all non-blocking). Correct the FIS1 wording and soften the "reduced checkpoint engagement" phrase; the manuscript is acceptable after a minor revision. No desk-reject and no major restructuring warranted on biological/clinical-plausibility grounds.
