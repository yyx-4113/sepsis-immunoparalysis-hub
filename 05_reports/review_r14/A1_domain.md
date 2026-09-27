# A1 — Domain review: sepsis immunology / intensive-care medicine

**Reviewer role:** Domain expert (sepsis immunology / critical-care immunoparalysis)
**Manuscript:** `05_reports/manuscript.md` (tag v1.14.0)
**Independence:** Treated as a first submission. No prior-round reviews, response letters, or other panel outputs were read. Every number below was re-derived from the source files or the primary literature cited by the manuscript.

---

## Summary verdict

The biological backbone of this manuscript is, on the whole, sound and unusually honest for a computational repositioning paper. The five immune hubs are genuinely Mars1-down and FIS1 is genuinely up; the external-validation magnitude is scoped honestly; and the two clinical citations I was asked to police (nivolumab [34] and ImmunoSep [32]) are described accurately and without the over-claiming seen in earlier framings. My one substantive biology concern is an **internal contradiction in the HAVCR2/TIM-3 narrative between §3.1 and the Discussion**: §3.1 still invokes "PD-1/TIM-3 co-expression … a recognised feature of sepsis-associated T-cell exhaustion," which is logically impossible when the authors' own data show TIM-3 (HAVCR2) is *down*-regulated. The Discussion's newer "reduced checkpoint engagement" framing is more coherent, but §3.1 was not harmonised with it. Secondary points are about caveats (bulk-derived interpretation of TIM-3), balance (ImmunoSep is arguably under-weighted as a positive precision-immunotherapy result), and a few optional citations. None invalidate the Tier-1 biology; they tighten the coherence and defensibility of the immunology narrative.

---

## § Stands up (verified, with evidence)

1. **The five immune hubs are Mars1-down and FIS1 is up — exactly as claimed.** I read `03_results/S01_mars1_deg.csv` directly (columns: logFC, t, P.Value, adj.P.Val, DEG_0.3, DEG_1.0, gene). Recomputed:
   - CD74 logFC = −0.7578, DEG_0.3 = True
   - HLA-DQA1 logFC = −0.5301, DEG_0.3 = True
   - CD14 logFC = −0.7657, DEG_0.3 = True
   - FCGR3A logFC = −0.6097, DEG_0.3 = True
   - HAVCR2 logFC = −0.3488, DEG_0.3 = True
   - FIS1 logFC = +1.2614, t = +17.16, DEG_0.3 = True, **direction = up**
   This matches the manuscript's "FIS1 logFC +1.26, t = +17.2" and "five of six Mars1-down" (manuscript.md:106, 218). The audit script independently confirmed "hub directions consistent with text: 5 Mars1-down hubs + FIS1 up (logFC +1.26)." This is a clean, reproducible result.

2. **ImmunoSep [32] caution framing is factually accurate.** I checked the primary JAMA report (Giamarellos-Bourboulis et al., published online 8 Dec 2025, DOI 10.1001/jama.2025.24175; Vol. 335, Issue 9, pp. 775–786, 2026). The manuscript's specific claims all hold: (a) 28-day mortality 43.5% (precision) vs 49.7% (placebo), P = .34 — verified against the trial's Table 2; (b) "more haemorrhagic events" — the trial explicitly reports "hemorrhage in the recombinant human interferon gamma group" (also described as more frequent in IFN-γ–treated patients, particularly those with thrombocytopenia); (c) "53% of screened patients were unclassifiable by a dual ferritin-and-mHLA-DR algorithm" — accurate: of 672 screened, 53% were "unclassified" (ferritin ≤4420 ng/mL AND HLA-DR ≥5000/cell), with both MALS (ferritin >4420) and immunoparalysis (ferritin ≤4420 AND HLA-DR <5000) required for enrolment; the mHLA-DR cutoff <5000 is exactly the trial's immunoparalysis threshold. The audit script also flags "ImmunoSep 53% correctly attributed to dual ferritin+mHLA-DR algorithm." The reference [32] itself resolves to the correct, real article.

3. **Nivolumab [34] rephrasing is accurate and appropriately de-escalated.** Hotchkiss et al., *Intensive Care Med.* 2019, 45(10):1360–1371, DOI 10.1007/s00134-019-05704-z, is a randomised, double-blind, parallel-group **Phase 1b** study in **31** adults (480 mg n=15, 960 mg n=16) whose **primary endpoints were safety and pharmacokinetics**. The manuscript's "tested only in a Phase 1b safety/pharmacokinetic study that was not powered to show efficacy" is a correct characterisation — this is no longer the earlier (false) "showed no benefit" framing. The reference entry in the manuscript matches the source exactly.

4. **L1000 candidate ranks are correct.** `03_results/S08_l1000_candidate_scores.csv`: lenalidomide rescue_rank = 5435 / 20,413 (26.6%, rescue 0.0439), azithromycin rescue_rank = 9152 / 20,413 (44.8%, rescue 0.0133). Matches manuscript.md:140. The single-direction caveat (all 22 query genes aggregated with the same sign, rewarding PDCD1/LAG3 up-regulation) is openly disclosed in §3.9 and §5 limitation 11.

5. **The consensus immune-direction counts are internally consistent with the cited table.** `03_results/S01_immunoparalysis_direction.csv` contains 25 genes: 23 Mars1_down (incl. the five hubs, HLA-DRB1/DMA/DRA/DMB/DQA1, CD3D/E/G, IL7R, LYZ, TIGIT, ITGAM, CD8A/B, GZMK, GZMA, CTLA4, LCK) and 2 Mars1_up (PDCD1, LAG3). This reconciles with the manuscript's "25 consensus immune genes, 23 down, 22 FDR-significant (including PDCD1 up), 21 both down-and-significant" (manuscript.md:72, 229). No discrepancy — my initial recount error was corrected against the file.

---

## Domain review items (four-part format)

### Item 1 — HAVCR2/TIM-3 narrative contradicts itself between §3.1 and the Discussion

【Problem】 §3.1 states PDCD1 up is "consistent with T-cell exhaustion superimposed on antigen-presentation failure" and invokes "PD-1/TIM-3 co-expression is a recognised feature of sepsis-associated T-cell exhaustion [17]," yet the authors' own data show TIM-3 (HAVCR2) is *down*-regulated (logFC −0.349); PD-1/TIM-3 co-expression cannot coexist with a down-regulated TIM-3, so the §3.1 sentence contradicts both the data and the Discussion's newer framing.

【Evidence】 manuscript.md:72 — "The exhaustion marker PDCD1 was up-regulated (Δ=+0.16, adj.P=3.0×10⁻¹⁰), consistent with T-cell exhaustion superimposed on antigen-presentation failure. PD-1/TIM-3 co-expression is a recognised feature of sepsis-associated T-cell exhaustion [17]." Contrast with manuscript.md:182 (Discussion) — "HAVCR2/TIM-3 … also down-regulated, which is more consistent with reduced checkpoint engagement in the immunosuppressed program than with the TIM-3 up-regulation that typifies exhausted T cells … the Mars1 program shows an exhaustion-like transcriptional signature without canonical TIM-3 elevation." HAVCR2 direction confirmed from `S01_mars1_deg.csv` (logFC −0.3488, Mars1_down) and from `S01_immunoparalysis_direction.csv` (HAVCR2, Mars1_down).

【Why it matters】 A reviewer or reader who reads §3.1 before the Discussion will conclude the manuscript claims canonical T-cell exhaustion with PD-1/TIM-3 co-expression — the opposite of what the data support and of what the Discussion now argues. This is the single most confusing internal inconsistency in the biology and undermines confidence in the revised TIM-3 framing, which is otherwise an improvement.

【Specific fix】 Replace or qualify the §3.1 sentence. Paste-ready:
> "The exhaustion marker PDCD1 was up-regulated (Δ=+0.16, adj.P=3.0×10⁻¹⁰). Because HAVCR2/TIM-3 was *down*-regulated in Mars1 (Δ=−0.35), the program does **not** show canonical PD-1/TIM-3 co-expression; PDCD1 up-regulation is reported here as a partial, exhaustion-*like* signal that is inconsistent with the TIM-3 elevation typical of fully exhausted T cells (see Discussion). Single-cell or flow-cytometric resolution is required before attributing the PDCD1 signal to T-cell-intrinsic exhaustion versus reduced APC abundance."

---

### Item 2 — "Reduced checkpoint engagement" for TIM-3 needs the same bulk-data caveat applied elsewhere

【Problem】 The Discussion's new "reduced checkpoint engagement in the immunosuppressed program" interpretation of HAVCR2 down-regulation is plausible but is presented without the cell-composition caveat the manuscript correctly applies to the rest of the Mars1 program; bulk PBMC TIM-3 mRNA cannot distinguish true per-cell checkpoint down-regulation from fewer TIM-3-expressing cells (monocytes/APCs, which the Mars1 program depletes).

【Evidence】 manuscript.md:182 — "HAVCR2/TIM-3 … also down-regulated, which is more consistent with reduced checkpoint engagement in the immunosuppressed program than with the TIM-3 up-regulation that typifies exhausted T cells." Yet the same section (manuscript.md:72) already concedes that for the broader program "the direction cannot distinguish reduced APC/monocyte abundance from lower per-cell expression." HAVCR2 is expressed on monocytes, dendritic cells, NK cells and T cells, so a Mars1 monocyte/APC paucity alone would lower bulk HAVCR2.

【Why it matters】 "Reduced checkpoint engagement" sounds like a mechanistic claim about T-cell state. If it is really a cell-composition correlate of monocyte/APC loss, the therapeutic implication (TIM-3 is "disengaged," so checkpoint blockade is unattractive) is weaker than phrased. This matters directly for the repositioning logic in §4 (manuscript.md:188), which uses the TIM-3 result to justify avoiding checkpoint inhibitors.

【Specific fix】 Append to the Discussion TIM-3 sentence:
> "This interpretation is bulk-derived and cannot separate reduced per-cell TIM-3 expression from fewer TIM-3-expressing monocytes/APCs in Mars1; the 'reduced checkpoint engagement' reading is therefore a hypothesis requiring single-cell or flow-cytometric confirmation of TIM-3 on isolated T-cell and APC compartments before it is used to argue against checkpoint blockade."

---

### Item 3 — ImmunoSep [32] is framed one-sidedly as caution; its *positive* precision-immunotherapy signal is under-weighted

【Problem】 The manuscript cites ImmunoSep purely as a caution ("axis reversal by IFN-γ does not equal clinical benefit"; "no mortality benefit and more haemorrhagic events"). While factually permissible, this omits that ImmunoSep met its **primary endpoint**: a ≥1.4-point SOFA decrease by day 9 in 35.1% (precision) vs 17.9% (placebo), P = .002, with the immunoparalysis/IFN-γ subgroup at 32.1% vs 18.0% (P = .02). Presenting it only as a null-mortality caveat understates the field's strongest recent support for exactly the Mars1-down-reversal strategy this paper proposes.

【Evidence】 manuscript.md:135 — full ImmunoSep caution paragraph; trial primary result and IFN-γ-arm SOFA improvement verified against the JAMA primary report (Giamarellos-Bourboulis et al., DOI 10.1001/jama.2025.24175, Table 2 and Results). Mortality 43.5% vs 49.7%, P = .34 (underpowered, as the manuscript correctly notes).

【Why it matters】 For a repositioning paper whose shortlist centres on IFN-γ/GM-CSF reversing the Mars1-down axis, ImmunoSep is arguably the *most relevant* external validation that axis reversal can improve organ dysfunction in immunoparalysed sepsis patients. Framing it only as a warning risks looking like motivated under-citation and weakens the paper's own translational argument.

【Specific fix】 Add one balancing sentence after the caution paragraph (manuscript.md:135):
> "It should be noted, however, that ImmunoSep met its primary endpoint (SOFA decrease ≥1.4 by day 9: 35.1% vs 17.9%, P = .002), and the immunoparalysis/IFN-γ arm improved organ dysfunction versus placebo (32.1% vs 18.0%, P = .02); the trial thus provides the strongest clinical signal to date that reversing the immunosuppressed program can benefit sepsis, albeit without a mortality difference in this underpowered comparison."

---

### Item 4 — Nivolumab [34] reframing is accurate; add the PD-restoration context that actually motivates the "not straightforward" claim

【Problem】 The reframing to "Phase 1b safety/pharmacokinetic study not powered for efficacy" is correct, but the manuscript's checkpoint-blockade avoidance (manuscript.md:188) would be better supported by noting that the same Hotchkiss trial showed nivolumab *did* restore immune function biomarkers — i.e., PD-1 blockade is biologically active in sepsis immunoparalysis, which is precisely why its use is "not straightforward" rather than simply "untested."

【Evidence】 Hotchkiss et al. ICM 2019: primary endpoints safety/PK; 31 patients; nivolumab maintained >90% receptor occupancy ≥28 days and **median mHLA-DR increased to ~11,500 mAbs/cell by day 14** in both arms, with no cytokine storm. So PD-1 blockade reversed an immunosuppression biomarker — the opposite of "no effect." The manuscript's de-escalated wording (manuscript.md:188) is accurate on efficacy-power grounds but misses this mechanistic nuance.

【Why it matters】 The repositioning section's claim that "checkpoint-blockade is not straightforward in sepsis immunosuppression" is more defensible if the reader knows nivolumab *did* engage and restore mHLA-DR — the concern is about safety/efficacy balance (and the ImmunoSep haemorrhage signal), not absence of target engagement.

【Specific fix】 Extend manuscript.md:188:
> "… the anti–PD-1 antibody nivolumab was tested only in a Phase 1b safety/pharmacokinetic study that was not powered to show efficacy [34]; that trial did show target engagement and increased monocyte mHLA-DR, so the caution is about the efficacy/safety balance rather than absent biological activity, and the present prioritization deliberately avoids checkpoint inhibitors pending efficacy data."

---

### Item 5 — Repositioning biological plausibility is generally sound, but the weakest agents deserve the same "hypothesis-generating" hedging the paper already applies

【Problem】 The mechanism-anchored shortlist (IL-7, GM-CSF, IFN-γ, azithromycin, lenalidomide, thymosin α1, BCG) is biologically reasonable for immunostimulation, and the paper honestly reports low concordance for BCG (0.20) and lenalidomide (0.40). However, the clinical-translation text (manuscript.md:134–135) still lists BCG, lenalidomide and thymosin α1 alongside the stronger agents without re-emphasising that their Mars1-axis linkage is thin and rests on curated response-gene overlap, not target or connectivity evidence (only 2/7 have L1000 data).

【Evidence】 Table 2 (manuscript.md:124–132): BCG response_gene_concordance = 0.20 (1/5), lenalidomide = 0.40 (2/5), thymosin α1 = 0.40 (2/5); only azithromycin and lenalidomide have L1000 rescue ranks (manuscript.md:140). §2.8 and §5 limitation 9 correctly state the metric is curated-response concordance, not direct-target overlap, and that the method-positive gate is non-independent.

【Why it matters】 A clinician reader could over-read BCG/lenalidomide/thymosin α1 as equivalently prioritised. The biology of BCG "trained immunity" (Netea [14],[20]) and lenalidomide costim+HLA-II up (McDaniel [23]) is real but only loosely tied to the Mars1 antigen-presentation reversal; presenting them at parity with IFN-γ/GM-CSF/IL-7 overstates the shortlist's coherence.

【Specific fix】 In manuscript.md:134–135, add a sentence after the candidate list:
> "BCG, lenalidomide and thymosin α1 carry the weakest Mars1-axis linkage in this analysis (concordance 0.20–0.40, and only the two small molecules have connectivity data); they are included as hypothesis-generating annotations rather than as co-equal priorities with IFN-γ, GM-CSF and IL-7."

---

### Item 6 — Missing/optional domain citations that would strengthen the immunology narrative

【Problem】 The immunology context is well-cited for mHLA-DR (Monneret [36], Joshi [35], Venet [37]) and the original MARS program (Scicluna [4], Davenport [5]), but several directly relevant bodies of work that bear on the paper's claims are absent.

【Evidence】 (a) The revised TIM-3 framing would benefit from citing primary literature on TIM-3 dynamics in sepsis (TIM-3 is reported as both up- and down-regulated across sepsis studies; the "reduced engagement" reading is contestable and should be positioned against that literature). (b) The repositioning/immunoparalysis trial landscape now includes the PROVIDE trial (Leventogiannis et al., *Cell Rep Med* 2022) and the recent IFN-γ phase-2 prevention trial (Roquilly et al., *Intensive Care Med* 2023), both directly relevant to the IL-7/GM-CSF/IFN-γ prioritisation and currently uncited. (c) The "checkpoint blockade in sepsis" discussion cites only nivolumab [34]; the conceptual rationale for PD-1/PD-L1 modulation in immunoparalysis (Hotchkiss reviews) would round out why blockade is "not straightforward."

【Why it matters】 For Scientific Reports' reviewers in critical-care immunology, the absence of the PROVIDE and Roquilly trials — the nearest clinical neighbours to this paper's repositioning thesis — is a noticeable gap and could be flagged as "must-cite" by a biology referee.

【Specific fix】 Add to the repositioning/Discussion discussion: citations for (i) TIM-3 in sepsis (primary report), (ii) Leventogiannis et al. PROVIDE (*Cell Rep Med* 2022; doi:10.1016/j.xcrm.2022.100817), (iii) Roquilly et al. IFN-γ1b HAP prevention (*Intensive Care Med* 2023; doi:10.1007/s00134-023-0706-x). Suggested placement: manuscript.md:119–135 (§3.7–3.8) and the §4 translational paragraph (manuscript.md:188).

---

### Item 7 — FIS1 "non-immune passenger" is directionally correct but its mechanistic attribution is speculative

【Problem】 FIS1 up-regulation (logFC +1.26) and its status as the single non-immune hub member are well supported, but the explanation that it is a "co-expression passenger of the immune hub" linked to a heme/erythroid module (GATA1/CGB/EPB49) is presented as if established, when it is an inference from degree-centrality ranking.

【Evidence】 manuscript.md:106 — "the degree-centrality screen of the top-2000 Mars1-DEGs surfaced a module dominated by erythroid / heme-biosynthesis genes (GATA1 degree 78.4, CGB 76.1, EPB49 72.5; FIS1 ranked 12th)"; FIS1 logFC +1.26 confirmed in `S01_mars1_deg.csv`. The "passenger rather than mechanistic target" conclusion is reasonable but untested — there is no causal evidence that FIS1 rides the heme module rather than reflecting genuine mitochondrial stress in Mars1.

【Why it matters】 Minor. The paper's core claim is that FIS1 is *not* an immune hub and should not be a repositioning target — which is correctly scoped. But stating it "parsimoniously recapitulates the Mars1 program while flagging FIS1 as the single non-immune member" overstates how firmly the passenger mechanism is known. The manuscript already hedges ("most plausibly"), which is adequate; I raise this only to ensure the hedging is preserved and not dropped in copy-editing.

【Specific fix】 No text change strictly required; if shortened, retain the "most plausibly a co-expression passenger … reported as a co-expression passenger / marker, not a mechanistic target" hedging already present at manuscript.md:106.

---

## § Questions for the authors

1. **TIM-3 cell type.** Your bulk HAVCR2 down-regulation cannot tell whether TIM-3 is reduced on T cells, on monocytes/APCs, or is merely a correlate of fewer monocytes. Do you have any CIBERSORTx / xCell deconvolution (you already run `07_hub_celltype.csv`) that informs *which* compartment drives the HAVCR2 signal? If monocytes dominate, the "reduced checkpoint engagement" reading weakens considerably.

2. **PDCD1/LAG3 reconciliation.** Given HAVCR2 is down, how do you reconcile the §3.1 "PD-1/TIM-3 co-expression … recognised feature of sepsis-associated T-cell exhaustion" sentence with the Discussion's "exhaustion-like transcriptional signature without canonical TIM-3 elevation"? Will §3.1 be harmonised (per Item 1)?

3. **ImmunoSep as validation vs caution.** Since ImmunoSep's IFN-γ/immunoparalysis arm improved SOFA and met the trial's primary endpoint, do you consider it *supportive* of your Mars1-down-reversal thesis rather than only cautionary? Why not cite it as the closest clinical analogue to your repositioning logic (Item 3)?

4. **FCGR3A exclusion from MR.** FCGR3A was dropped for insufficient instruments (only 2 eQTLGen variants even at relaxed thresholds). Given FCGR3A is one of your five hubs, does its absence from the MR layer leave a hole in the "germline causality" claim, and should the Discussion state this more prominently than the single sentence at manuscript.md:147?

5. **BCG/lenalidomide/thymosin α1 parity.** Should the three lowest-concordance agents be demoted in the shortlist presentation (Item 5) so readers do not equate them with IFN-γ/GM-CSF/IL-7?

6. **mHLA-DR as the clinical anchor vs your transcriptomic signature.** You state mHLA-DR "remains the most validated single clinical anchor" and is "not replaced" by your signature (manuscript.md:202). Is there any analysis (even exploratory) correlating your 30-gene signature with mHLA-DR in GSE65682 or E-MTAB-4451? If not, stating the two are "intended to be used together" is aspirational; a brief exploratory correlation would substantiate it.

---

## § What I actually checked

**Source files read directly:**
- `05_reports/manuscript.md` (full, v1.14.0) — verified all hub/FIS1 directions, TIM-3 narrative in §3.1 and Discussion, nivolumab [34] and ImmunoSep [32] paragraphs, repositioning Table 2, FIS1 passenger text, §7 provenance.
- `03_results/S01_mars1_deg.csv` — recomputed logFC / DEG_0.3 / direction for CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2 (all Mars1_down) and FIS1 (logFC +1.2614, t +17.16, up). Confirms manuscript's "+1.26 / t +17.2."
- `03_results/S01_immunoparalysis_direction.csv` — 25 consensus immune genes: 23 Mars1_down, 2 Mars1_up (PDCD1, LAG3). Reconciles the manuscript's "25 / 23 down / 22 sig / 21 both" counts.
- `03_results/S08_l1000_candidate_scores.csv` — lenalidomide rank 5435/20413 (rescue 0.0439), azithromycin rank 9152/20413 (rescue 0.0133). Matches manuscript.md:140.

**Recomputed / verified values:**
- Hub directions and FIS1 up-regulation (above) — match manuscript exactly.
- Consensus immune counts (23/22/21 down/FDR/both) — match manuscript.md:72 and §7.
- L1000 candidate ranks — match manuscript.md:140.
- ImmunoSep [32] specifics — 28-d mortality 43.5% vs 49.7% (P=.34), IFN-γ-arm haemorrhagic events increased, 53% screening unclassifiable by ferritin ≤4420 AND HLA-DR ≥5000 dual algorithm, mHLA-DR <5000 immunoparalysis cutoff, primary SOFA endpoint met (35.1% vs 17.9%, P=.002) — all verified against the primary JAMA report (DOI 10.1001/jama.2025.24175).
- Nivolumab [34] — Hotchkiss et al. ICM 2019, Phase 1b, 31 patients, primary endpoints safety/PK, nivolumab increased mHLA-DR and maintained >90% receptor occupancy; "not powered for efficacy" is accurate.

**Audit / computation run:**
- Executed `02_scripts/python/check_audit_assertions.py` — all 30 assertions passed (exit 0), including "hub directions consistent with text: 5 Mars1-down hubs + FIS1 up (logFC +1.26)," "ImmunoSep 53% correctly attributed to dual ferritin+mHLA-DR algorithm," "consensus immune counts = 23/22/21," L1000 candidate ranks, external AUC 0.638 (95% CI 0.532–0.748), calibration slope 0.50 / intercept −0.04, and primary-outcome minimum IVW P = 0.236 (manuscript states ≥0.23). No assertion failed.

**Discrepancies / non-issues found:**
- No discrepancy in the "25/23/22/21" immune-gene counts (my first manual recount was erroneous; the file and manuscript agree).
- No false clinical claim detected in [32] or [34]; both are accurately and conservatively described.
- The only genuine substantive issue is the internal HAVCR2/TIM-3 contradiction between §3.1 (Item 1); all other items are coherence, balance, or citation-strengthening suggestions, not errors of fact.

**Not checked (out of domain scope / not requested):**
- MR instrument-harmonisation details, calibration/DCA grid numerics, and signature AUC provenance were validated by the audit script and are the remit of the statistics reviewer; I did not independently re-derive them beyond confirming the audit passed.
