# Domain-layer peer review — A1 (sepsis / critical-care immunology)

**Manuscript:** "A reproducible, fully auditable pipeline confirms within-cohort the MARS Mars1 immunoparalysis program and delivers an honest external validation of a 30-gene sepsis prognostic signature"
**Target venue:** BMC Bioinformatics (Research article / Methodology)
**Reviewer role:** Independent first-submission reviewer — domain (biology / clinical immunology) layer only
**Date:** 2026-10-09

This review assesses biological coherence and clinical accuracy only. Statistical / machine-learning methodology, repository reproducibility, and reporting-interface issues are covered by other panels and are not re-litigated here except where they intersect with the biology.

---

## Summary verdict (domain)

The manuscript is unusually candid about its own limitations, and on the central biomarker-honesty questions (mHLA-DR vs mRNA proxy; honest external-validation framing; LINCS glucocorticoid caveat) it is genuinely rigorous. However, the domain layer contains one concrete citation misattribution (lenalidomide), one biologically incomplete/misleading reconciliation of the TIM-3 result, a headline mislabel of TIM-3 as an antigen-presentation/monocytic hub, a "confirmation" that is partly tautological by construction, an understated threat from the ImmunoSep trial to the paper's own repositioning logic, and a missing landmark RCT (DALI) that materially bounds the GM-CSF readiness claim. None of these invalidate the Tier-1 biology, but several should be corrected before acceptance at a methods-journal that is read by clinically literate reviewers.

---

## Issue 1 — TIM-3 bulk-down reconciliation is hand-waving and partly inverts the inference; TIM-3 is mislabeled as an AP/monocytic hub

【Problem】 The bulk-abundance explanation offered for the Mars1-down HAVCR2/TIM-3 signal does not resolve the direction of the inference and is partly backwards, and TIM-3 is inconsistently labeled as an antigen-presentation/monocytic hub when it is a T-cell/exhaustion checkpoint.

【Evidence】 §3.1: "The present Mars1 program instead shows net lower *bulk* HAVCR2/TIM-3 expression, which is compatible with, but does not by itself establish, reduced per-cell checkpoint engagement, because a bulk measurement cannot separate lower T-cell/APC abundance from lower per-cell TIM-3." Yet the same paragraph cites "PD-1/TIM-3 co-expression more broadly characterises exhausted T cells, and several sepsis studies report TIM-3 up-regulation on circulating T cells in association with severity [17]," and ref [18] (Yang 2013) on TIM-3 biology. The Abstract, Conclusion, and the headline claim then call HAVCR2 one of "5 antigen-presentation/monocytic hub genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2/TIM-3)."

【Why it matters】 In sepsis, lymphopenia from sepsis-induced T-cell apoptosis (ref [16], which the manuscript itself cites) lowers the *bulk* TIM-3 transcript denominator because there are simply fewer TIM-3-bearing T cells. That is fully compatible with *higher* per-cell TIM-3 on the surviving, exhausted T cells — the opposite of "reduced per-cell checkpoint engagement." So the manuscript's phrase "compatible with … reduced per-cell checkpoint engagement" misleads: the bulk drop most plausibly reflects T-cell loss, which is neutral-to-opposing on the exhaustion question, not reassuring. Separately, calling HAVCR2 (a co-inhibitory checkpoint expressed on T cells and some APCs) one of the "5 antigen-presentation/monocytic hub genes" overstates the coherence of that claim — only 4 of the 5 (CD74, HLA-DQA1, CD14, FCGR3A) are genuinely AP/monocytic; the 5th is a T-cell checkpoint. A domain reviewer will notice the abstract/headline/body inconsistency immediately.

【Specific fix】 Replace the §3.1 sentence with:

> "The present Mars1 program shows net lower *bulk* HAVCR2/TIM-3 transcript. Because bulk whole-blood measurements cannot separate reduced T-cell/APC abundance from reduced per-cell TIM-3, and because sepsis lymphopenia (ref. 16) itself lowers the bulk TIM-3 denominator, this finding is ambiguous: it is most parsimoniously read as reflecting T-cell loss rather than reduced per-cell checkpoint engagement, and is compatible with — not evidence against — persistent T-cell exhaustion on surviving cells (refs. 17, 18). Bulk TIM-3 down-regulation therefore neither confirms nor refutes T-cell exhaustion. HAVCR2/TIM-3 should be described consistently as a T-cell/exhaustion checkpoint co-expressed on some APCs, not as an antigen-presentation/monocytic hub."

And in the Abstract, Conclusion, and the title-block headline, change "5 antigen-presentation/monocytic hub genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2/TIM-3)" to "four antigen-presentation/monocytic hubs (CD74, HLA-DQA1, CD14, FCGR3A) plus the T-cell checkpoint HAVCR2/TIM-3."

---

## Issue 2 — The hub "confirmation" is partly tautological: hubs are selected from a pre-defined immune gene set, and Mars1 labels come from the same cohort

【Problem】 Demonstrating that Mars1 is "anchored by" antigen-presentation genes is circular by construction, because the Mars1 endotype was originally defined by exactly that program and the hubs were selected from a curated immune gene list.

【Evidence】 §2.5: hubs come from "Mars1-DEG ∩ consensus immune set, expanded to the top-20 degree-centrality genes when sparse." §3.3: "five immune hub genes anchored in the antigen-presentation/monocytic program." §4: "The five immune hubs largely *confirm within-cohort* the antigen-presentation / monocytic program that defines the Mars1 endotype in the original MARS-consortium work (Scicluna et al. [5]); … (the Mars1 labels originate from the MARS consortium's own clustering of this same cohort)." The Mars1 label was itself defined by its transcriptional profile, including HLA-class-II / antigen-presentation down-regulation (ref [5], described in §1).

【Why it matters】 Because the endotype label and the antigen-presentation program are the same entity, and the hubs were then drawn from a pre-specified consensus immune gene set, showing that Mars1 "is anchored by" antigen-presentation genes restates the definition rather than confirming an independent prediction. A BMC Bioinformatics reviewer will read "confirm/anchored" as implying an external or independent test; the honest but weaker claim is "recapitulation of the defining program." This does not invalidate the pipeline, but the verb oversells the novelty/confirmation and the headline framing ("confirms within-cohort the MARS Mars1 immunoparalysis program") reads as a discovery claim it is not.

【Specific fix】 Replace the §4 sentence with:

> "The five immune hubs recapitulate within-cohort the antigen-presentation/monocytic program that defines the Mars1 endotype in the original MARS-consortium work (Scicluna et al. [5]); because the Mars1 labels originate from the consortium's own clustering of this same cohort and the hubs were selected from a curated immune gene set, this is a within-cohort recapitulation of the defining program (a within-cohort confirmation, not an independent replication), and true replication requires an independent cohort with externally assigned Mars1 labels."

Apply the same "recapitulate" framing to the Abstract and Conclusion, and consider changing the manuscript title's "confirms within-cohort" to "recapitulates within-cohort."

---

## Issue 3 — ImmunoSep is invoked as a mild "caution" then pivoted to "underscores transcriptomic endotyping," understating the threat to the paper's own repositioning logic

【Problem】 The 53% unclassifiable rate in ImmunoSep is a problem for the *bedside* biomarker the manuscript itself treats as canonical, and the paper's transcriptomic alternative shares the same weakness; the pivot "underscores the value of transcriptomic endotyping" is not supported by any evidence in the manuscript and understates the threat to clinical actionability.

【Evidence】 §3.8: "53% of screened patients were unclassifiable by a dual ferritin-and-mHLA-DR algorithm (mHLA-DR cutoff <5,000 receptors/cell on CD45/CD14 monocytes; 'unclassifiable' = normal ferritin AND normal HLA-DR)"; the trial "reported SOFA improvement in the IFN-γ/immunoparalysis arm but **no mortality benefit and more haemorrhagic events**"; "the trial was, however, underpowered to detect a mortality difference (43.5% vs 49.7% 28-day mortality; P = .34), so its null result does not refute axis-targeted immunotherapy; it instead underscores the value of transcriptomic…" Discussion §4 simultaneously calls mHLA-DR "the most validated single clinical anchor for sepsis immunoparalysis (Monneret et al. [19]; Joshi et al. [33]; Venet & Monneret [20])." Yet the manuscript's own repositioning "stratification hypothesis" (Discussion: "Mars1 patients with dominant APC suppression may benefit most from IFN-γ/GM-CSF, whereas those with T-cell exhaustion may prefer IL-7") depends on reliably identifying that population — and the transcriptomic tool the paper offers shares the defect: §3.2 shows the immune score does **not** separate Mars1 from Mars2 (P = 0.47), and Mars1 labels are not independently assigned.

【Why it matters】 The 53% unclassifiable rate is a direct threat to *any* bedside-stratified immunotherapy — including the manuscript's own transcriptomic repositioning logic — not merely a "caution for the repositioning axis." If even the best-validated bedside tool (mHLA-DR + ferritin) fails to classify half of screened patients, and the transcriptomic substitute (a) is not independently replicated, (b) does not separate Mars1 from Mars2, and (c) is itself partly definitional (Issue 2), then the actionable claim "Mars1 → IFN-γ/GM-CSF" has no demonstrated way to identify the target population. Asserting that this "underscores the value of transcriptomic endotyping" is unsupported by anything in the paper showing transcriptomic assignment outperforms the ferritin+mHLA-DR algorithm that failed in half the cohort. This understates the threat to clinical actionability and should be reframed.

【Specific fix】 Replace the §3.8 pivot sentence with:

> "The 53% unclassifiable rate is a direct threat to any bedside-stratified immunotherapy, including the present transcriptomic repositioning logic: the manuscript's own immune score does not separate Mars1 from Mars2 (P = 0.47, §3.2) and the Mars1 labels are not independently assigned, so no evidence here shows transcriptomic assignment outperforms the ferritin+mHLA-DR algorithm that failed in half of screened patients. The ImmunoSep null on mortality therefore tempers — not merely 'cautions' — the clinical actionability of the IFN-γ/GM-CSF stratification hypothesis, which remains speculative until a biomarker strategy that reliably enriches immunoparalysed patients is demonstrated."

---

## Issue 4 — Lenalidomide citation (ref 29) is a misattribution; "weaker dedicated sepsis trials" is unsupported, and azithromycin lacks a sepsis RCT citation

【Problem】 Ref [29] (McDaniel et al. 2011, *Leukemia*) is a myelodysplastic-syndrome (MDS) study of lenalidomide reversing T-cell tolerance in MDS — not a sepsis trial — yet the manuscript asserts lenalidomide has "weaker dedicated sepsis trials." Azithromycin is similarly supported only by a pharmacology review with no dedicated sepsis RCT.

【Evidence】 §3.8: "lenalidomide [29] and thymosin α1 [30] are mechanistically plausible or regionally used with weaker dedicated sepsis trials." Ref [29] = McDaniel, J. M. et al. "Reversal of T-cell tolerance in myelodysplastic syndrome through lenalidomide immune modulation." *Leukemia* **26**, 1425–1429 (2011) — unambiguously an MDS paper. Ref [28] (azithromycin) = Parnham et al. pharmacology review, not a sepsis RCT.

【Why it matters】 Attributing "weaker dedicated sepsis trials" to a citation that is an MDS mechanistic paper is a misattribution any domain reviewer familiar with lenalidomide's literature will catch; it overstates the sepsis evidence base for a candidate the manuscript already labels hypothesis-generating. At minimum the citation does not support the claim and should be corrected.

【Specific fix】 Either drop the sepsis-trial claim or re-cite appropriately. Suggested replacement for the lenalidomide clause:

> "Lenalidomide [29] reverses T-cell tolerance and up-regulates HLA-class-II in myelodysplastic syndrome (a mechanistic, non-sepsis precedent); it has no dedicated sepsis RCT and is included only as a hypothesis-generating, mechanism-anchored candidate."

And for azithromycin:

> "Azithromycin [28] has described immunomodulatory mechanisms (macrolide immunomodulation) but no dedicated sepsis mortality RCT; it is included as hypothesis-generating."

Do not assert "weaker dedicated sepsis trials" without an actual sepsis trial citation for either agent.

---

## Issue 5 — MUST-CITE gap: the largest GM-CSF sepsis RCT (DALI) and other landmark immunoparalysis RCTs are missing

【Problem】 While leaning on GM-CSF as the "most clinically ready" candidate, the manuscript omits the largest GM-CSF sepsis RCT (DALI, de Jong et al. 2016) and other landmark immunostimulatory RCTs/validation literature a BMC Bioinformatics domain reviewer would expect.

【Evidence】 §3.8 supports GM-CSF readiness via Meisel 2009 [26] and the Bo 2011 meta [31]; it does not cite the DALI phase-2 RCT (de Jong, H. F. et al., "Efficacy and safety of granulocyte-macrophage colony-stimulating factor in patients with severe sepsis," *Lancet Infect. Dis.* 2016/2017), which — consistent with the broader G-CSF/GM-CSF null evidence — found no improvement in ventilator-free or ICU-free days. Also absent is a recent systematic review/meta-analysis of immunostimulatory RCTs in sepsis (GM-CSF / IFN-γ / IL-7) to situate the readiness claims, and the multi-centre mHLA-DR prognostic-validation literature beyond the single-centre papers already cited (refs 19–21).

【Why it matters】 The "GM-CSF most clinically ready" framing is materially bounded by the DALI negative trial. Citing only the positive/older Meisel 2009 and a 2011 meta while omitting the definitive GM-CSF RCT makes the readiness claim look selectively cited. BMC Bioinformatics frequently consults clinically literate reviewers for translational computational papers; the DALI omission is the single most likely "missing landmark reference" critique. It also bears directly on the repositioning shortlist's headline ranking of GM-CSF.

【Specific fix】 Add to §3.8 / References:

> "The optimism for GM-CSF is also bounded by the DALI phase-2 RCT (de Jong et al., [NEW]), the largest GM-CSF sepsis trial, which showed no improvement in ventilator-free or ICU-free days, consistent with the null G-CSF/GM-CSF meta-analysis [31]."

Add the DALI citation and, ideally, a recent (2020s) systematic review of immunostimulatory immunotherapy RCTs in sepsis to anchor the readiness ladder for all seven candidates.

---

## Issue 6 — Translational logic gap: no evidence that transcriptomic Mars1 predicts mHLA-DR-low status or IFN-γ/GM-CSF responsivity

【Problem】 The repositioning "stratification hypothesis" (Mars1 APC suppression → IFN-γ/GM-CSF; Mars1 T-cell exhaustion → IL-7) is asserted biologically but never demonstrated, because the cohort lacks measured mHLA-DR and no analysis links Mars1 status to cytokine inducibility.

【Evidence】 Discussion §4: "Mars1 patients with dominant APC suppression may benefit most from IFN-γ/GM-CSF, whereas those with T-cell exhaustion may prefer IL-7. This is a hypothesis requiring prospective testing, not a treatment recommendation." No analysis correlates Mars1 assignment or the 5 hubs with measured mHLA-DR (acknowledged unavailable in GSE65682) or with IFN-γ-inducible HLA-DR rescue. Limitation 7 correctly states mHLA-DR is the canonical biomarker "not replaced by the transcriptomic signature," but the manuscript does not operationalise that caveat into the stratification claim.

【Why it matters】 Without showing that Mars1 transcriptomic status tracks the validated mHLA-DR bedside phenotype or predicts response to the proposed agents, the stratification hypothesis remains plausible but unsupported. The manuscript's own caveat that mHLA-DR is canonical is not acted upon. This is the central translational gap and should be stated as a limitation rather than implied as established — otherwise the "which axis each rescues" mapping reads as more actionable than the data permit.

【Specific fix】 Add to Limitations:

> "The repositioning stratification hypothesis (Mars1 → IFN-γ/GM-CSF for APC suppression; Mars1 → IL-7 for T-cell exhaustion) is asserted biologically but not demonstrated: GSE65682 lacks measured mHLA-DR, and no analysis here shows that Mars1 transcriptomic status predicts mHLA-DR-low immunoparalysis or IFN-γ/GM-CSF inducibility. The hypothesis requires prospective correlation of Mars1 assignment with mHLA-DR and with ex-vivo cytokine responsiveness (S11) before any patient-selection logic can be proposed."

---

## § Stands up (claims I suspected were wrong but found CORRECT)

1. **mHLA-DR vs the transcriptomic immune-function score — rigorously distinguished, not blurred.** I expected the manuscript to conflate the mRNA HLA-II/CD74 proxy with monocyte membrane mHLA-DR. It does the opposite, explicitly: §3.2 states "the HLA-class-II / CD74 *mRNA* down-regulation reported here is a transcript-level immunoparalysis proxy and should not be equated with monocyte membrane mHLA-DR, the validated bedside immunoparalysis biomarker (Monneret et al. [19]; Venet & Monneret [20]; Landelle et al. [21]); the two are complementary, not interchangeable," and Limitation 7 reiterates "Monocyte mHLA-DR remains the canonical, complementary bedside immunoparalysis biomarker and is not replaced by the transcriptomic signature." This is exactly the rigor a domain reviewer wants.

2. **The external-validation framing is genuinely honest.** The pre-specified primary metric (locked-L1 AUC 0.585, 95% CI 0.469–0.696) is reported with an interval that includes 0.5 and is explicitly labelled "not significantly above chance," with the equal-weight sensitivity (0.638, CI 0.532–0.748) correctly carrying the portable claim. The "independent in cohort and platform, not in label" framing is precise and not oversold.

3. **The LINCS glucocorticoid caveat is self-critical and correct.** The observation that prednisone (a clinical immunosuppressant) ranks in the 3.2nd percentile on the same Mars1-down rescue axis is used to declare the L1000 rescue score "descriptive only" and explicitly *not* counted as supportive evidence for lenalidomide/azithromycin (§3.9, Discussion §4, Conclusion). This is a rare and commendable refusal to over-read a connectivity metric, and "a metric that ranks an immunosuppressant in the top 3% cannot simultaneously corroborate two immunomodulators" is correct logic.

4. **FIS1 is correctly *not* called an immune hub.** Despite being co-selected by the tri-method ML consensus, the manuscript consistently frames FIS1 as a non-immune erythroid/heme-module gene up-regulated in Mars1 (logFC +1.26), situates it in module 2011 (GATA1/KLF1/ALAS2…), and states it is "not a co-expression partner of the immune hubs." The headline and Conclusion both separate it from the 5 immune hubs. Honest.

5. **Mars1 vs Mars2 non-separability is openly stated.** §3.2 reports the immune score does not distinguish Mars1 from Mars2 (median −0.79 vs −0.75, P = 0.47) and correctly notes the score "indexes a two-cluster immune gradient common to both low-score endotypes rather than a Mars1-specific signature." This candidly bounds the score's specificity.

6. **The "within-cohort confirmation, not independent replication" disclosure is present and repeated** in the Abstract, §1, §4, and the article-type statement. The disclosure itself is correct (the Mars1 labels originate from the same cohort's own clustering); my Issue 2 concern is about the *verb* ("confirm/anchored") overselling what the disclosure already qualifies, not about the disclosure being absent.

---

## § Questions for the authors (clarification required; I am not guessing the answers)

1. **ImmunoSep primary endpoint.** The manuscript gives 28-day mortality 43.5% vs 49.7% (P = .34) and "SOFA improvement" in the IFN-γ/immunoparalysis arm, but does not state whether that SOFA/organ-dysfunction benefit was statistically significant, nor the trial's stated primary endpoint. Please clarify, and confirm these numbers are taken verbatim from the published JAMA 2025 paper (ref 32), which I could not independently access. Was the trial stopped early or under-enrolled relative to its powering calculation?

2. **Source of the "consensus immune gene set" (25 genes).** Is this set defined *a priori* from external literature, or was it derived/refined from this cohort? This single fact determines whether the hub selection (Issue 2) is genuinely confirmatory versus circular. Please state the provenance (e.g., a published immune-gene panel or GO/Reactome curation) and cite it.

3. **HLA-DQA1 handling in the external model.** §3.4 says HLA-DQA1 was "driven to a zero coefficient and excluded from the saved vector" (it is also absent from the Illumina array, §3.5). Please confirm the locked external model therefore uses 29 genes with non-zero coefficients and reconcile this with the persistent "30-gene signature" label — consider renaming to "30-gene (29-measurable) signature" or similar.

4. **Sepsis trials for lenalidomide and azithromycin.** If a dedicated sepsis RCT exists for either agent, please cite it; otherwise the "weaker dedicated sepsis trials" phrasing (Issue 4) must be dropped in favour of a mechanism-only statement.

5. **Mars1 ↔ mHLA-DR enrichment.** Does any cohort (including E-MTAB-4451 or the MARS extension) provide both transcriptomic endotype and measured mHLA-DR, allowing the manuscript to test whether Mars1 enriches for mHLA-DR-low immunoparalysis? If so, reporting that correlation would substantially strengthen the translational claim; if not, please state so explicitly.

6. **TIM-3 directionality across references.** The manuscript cites refs 17/18 for TIM-3 *up*-regulation on T cells in sepsis, then reports bulk TIM-3 *down* in Mars1. Please confirm whether the cited "TIM-3 up-regulation" literature is specifically on *cell-surface protein* (flow cytometry) versus bulk mRNA, to avoid mixing protein- and transcript-level evidence in the reconciliation.

---

## § What I actually checked

**Files read:**
- `05_reports/manuscript.md` — read in full (283 lines). This is the only manuscript file reviewed.

**Files NOT read (per the forbidden-list contract):** any `REVIEW_*.md` / `RESPONSE_*.md` / `REVISION_*.md` / `ROUND*.md`; the `06_review/` directory except this output file; `SUBMISSION_MANIFEST.md`; any `*_SOP.md`; `author_verification_statement.md`; `MEMORY.md`; `.workbuddy/memory/`. I did not open, grep, or list any of these.

**Biological claims verified against the cited references (within the manuscript text):**
- TIM-3 / exhaustion literature (refs 17 Wang 2024, 18 Yang 2013) — accurately represented as describing TIM-3 up-regulation / homeostasis role in sepsis; the internal tension with the bulk-down finding is real and is the basis of Issue 1.
- mHLA-DR biomarker canon (refs 19 Monneret 2008, 20 Venet & Monneret 2018, 21 Landelle 2013, 33 Joshi 2023) — accurately cited as the validated bedside immunoparalysis biomarker; the manuscript's distinction from mRNA is correct.
- Hotchkiss immunosuppression / lymphocyte apoptosis (refs 2, 3, 16) — accurately represented; ref 16 (T/B apoptosis 2001) is correctly invoked for lymphopenia.
- MARS endotype (ref 5 Scicluna 2017) and Davenport SRS (ref 15) — accurately described; Mars1 39% mortality figure correctly attributed to the original derivation.
- IRIS-7 IL-7 RCT (ref 25 François 2018) — accurately represented as a septic-shock lymphocyte-restoration RCT.
- Meisel GM-CSF RCT (ref 26, 2009) — accurately represented as a placebo-controlled monocyte-HLA-DR restoration trial.
- Döcke IFN-γ (ref 27, 1997 Nat Med) — accurately represented as a small mechanistic monocyte-deactivation study; the manuscript's "limited sepsis-specific signals" qualifier is fair.
- Thymosin α1 meta (ref 30 Li 2015) — accurately represented.
- BCG trained immunity (refs 36 ACTIVATE Cell 2020, 37 Moorlag JID 2022) — accurately represented as infection-prevention RCTs in older adults; consistent with the "trained immunity" framing.
- Nivolumab sepsis Phase 1b (ref 35 Hotchkiss 2019) — accurately represented as a safety/PK study not powered for efficacy; the manuscript's avoidance of checkpoint inhibitors is consistent.

**Citations I could NOT independently access:** I did not retrieve the primary PDFs/PubMed records for refs 25–32, 36–37, nor the DALI trial, during this review (and was instructed not to read the author's verification statement or any prior review). My assessments therefore rely on recognition of these landmark studies rather than re-opening the source documents. Two points are flagged with explicit access-caveats:
- The lenalidomide misattribution (Issue 4) is **high confidence**: McDaniel et al. 2011 *Leukemia* is unambiguously an MDS paper, not a sepsis trial, regardless of the primary record.
- The exact ImmunoSep numbers (43.5% vs 49.7%, P = .34; "SOFA improvement") and the DALI trial details should be **verified by the authors against the primary JAMA 2025 (ref 32) and Lancet/other (DALI) sources**; my Issue 3 critique stands on the manuscript's own stated 53% unclassifiable rate and does not depend on the exact mortality figures.

**Biological claims NOT verifiable from the manuscript alone:** (a) whether the 25-gene consensus immune set is a priori or cohort-derived (Issue 2, Question 2); (b) whether Mars1 transcriptomic status enriches for mHLA-DR-low immunoparalysis in any overlapping cohort (Issue 6, Question 5); (c) the protein- vs mRNA-level basis of the cited TIM-3-up literature (Issue 1, Question 6). These require author clarification, not assumption.

---

## Recommendation (domain layer)

**Minor revision** is appropriate *if* Issues 1, 2, 3, and 4 are corrected with the paste-ready text above and Issue 5 (DALI citation) is added. The biology is internally coherent on the points that matter most (mHLA-DR honesty, external-validation candour, LINCS caveat), and the within-cohort-confirmation disclosure is present. The required changes are predominantly wording/labeling and one citation correction plus one missing-landmark addition — none require new analyses. Issue 6 should be added as an explicit limitation. I do **not** recommend rejection on domain grounds; the paper's honesty posture is a strength worth preserving through the revisions.
