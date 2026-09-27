# Independent peer review — A1 (Domain: sepsis immunology / critical-care medicine)

**Manuscript under review:** "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and validates a 30-gene sepsis prognostic signature" (Scientific Reports, Nature Portfolio)
**Reviewer role:** Domain expert (sepsis immunology / critical-care medicine), independent first-submission review.
**Scope of this report:** Domain / biological correctness only. Statistical and methodological concerns are deferred to other reviewers.

---

## Major domain concerns

### 1. HAVCR2/TIM-3 downregulation interpreted as "reduced APC abundance rather than T-cell-intrinsic exhaustion" — biologically overstated and in tension with established TIM-3 biology

【Problem】 The manuscript reads the bulk downregulation of HAVCR2/TIM-3 in Mars1 (Δ=−0.35, adj.P=2.8×10⁻¹³) as evidence of "reduced APC/monocyte abundance rather than T-cell-intrinsic exhaustion," but TIM-3 is a canonical T-cell exhaustion marker that is typically *up*-regulated on exhausted lymphocytes in sepsis, and a bulk-blood transcriptome cannot separate cell-abundance loss from lower per-cell expression.

【Evidence】 manuscript.md:71–72 (§3.1): "HAVCR2/TIM-3 Δ=−0.35 (adj.P=2.8×10⁻¹³) … consistent with reduced APC/monocyte abundance rather than T-cell-intrinsic exhaustion"; manuscript.md:14 (Abstract) lists HAVCR2 among "antigen-presentation / monocytic hub genes"; manuscript.md:135 (§3.8) repeats "HAVCR2/TIM-3 is itself down-regulated (consistent with the antigen-presentation failure described in §3.1)."

【Why it matters】 This interpretation is presented as the natural reading of the data, yet it leans against the dominant sepsis-immunoparalysis literature in which TIM-3 (alongside PD-1) is an *up*-regulated T-cell-exhaustion readout. A bulk downregulation of an immune gene in an already broadly immune-dampened endotype is equally consistent with (a) it simply being part of the general antigen-presentation/immune downregulation program, or (b) reduced per-cell TIM-3 expression. Asserting "APC abundance, not T-cell exhaustion" overstates the evidence and risks misleading readers into thinking bulk TIM-3 downregulation *refutes* T-cell exhaustion — it does not.

【Specific fix】 Replace the sentence in §3.1 ("… consistent with reduced APC/monocyte abundance rather than T-cell-intrinsic exhaustion — and a separate up-regulated T-cell exhaustion axis …") with: "HAVCR2/TIM-3, a checkpoint expressed on both antigen-presenting cells and T cells, was also down-regulated in Mars1 (Δ=−0.35, adj.P=2.8×10⁻¹³). Because this is a bulk-blood measurement, the direction cannot distinguish reduced APC/monocyte abundance from lower per-cell expression, nor can it adjudicate between an APC-abundance signal and the T-cell-intrinsic exhaustion implied by PDCD1 up-regulation; single-cell or flow-cytometric resolution is required before attributing the signal to either mechanism."

---

### 2. The "separate up-regulated T-cell exhaustion axis (PDCD1/LAG3 up)" is presented as established Mars1 biology but is the authors' interpretive addition, supported by only one significant gene

【Problem】 Mars1 is framed as carrying a "separate up-regulated T-cell exhaustion axis (PDCD1/LAG3 up)," implying this is a confirmed component of the MARS Mars1 endotype. In fact the original Scicluna/Davenport Mars1 definition is a broadly *down*-regulated immune/antigen-presentation program, and in this re-analysis only PDCD1 is significantly up (LAG3 adj.P=0.55, non-significant). The "axis" is therefore thinly supported and is an interpretation, not an established Mars1 feature.

【Evidence】 manuscript.md:22 (Introduction) defines Mars1, per Scicluna [4], solely as "downregulated HLA class-II, antigen-presentation and monocytic programs" — no up-regulated exhaustion axis is mentioned. manuscript.md:71–72 (§3.1): "the exhaustion marker PDCD1 was up-regulated (Δ=+0.16, adj.P=3.0×10⁻¹⁰) … a separate up-regulated T-cell exhaustion axis (PDCD1 significantly, adj.P=3.0×10⁻¹⁰; LAG3 directionally up but not FDR-significant, adj.P=0.55)."

【Why it matters】 The authors explicitly position this work as *confirmation, not discovery* (Abstract line 14; Discussion line 184). Overstating a T-cell-exhaustion axis as a confirmed Mars1 attribute misrepresents the MARS literature and inflates the novelty of a re-analysis. Reviewers at Scientific Reports will expect precise attribution of what is established versus interpreted, especially given the internal inconsistency with the HAVCR2 reading (Item 1): if T cells are exhausted, TIM-3 on those T cells should also be up, yet the manuscript argues it is down — the two claims cannot both be cleanly true without explicit cell-type resolution the study lacks.

【Specific fix】 Replace "and a separate up-regulated T-cell exhaustion axis (PDCD1 significantly, adj.P=3.0×10⁻¹⁰; LAG3 directionally up but not FDR-significant, adj.P=0.55)" with: "and a candidate, incompletely supported T-cell-exhaustion signal: only PDCD1 was significantly up-regulated (Δ=+0.16, adj.P=3.0×10⁻¹⁰), whereas LAG3 was directionally but not significantly up (adj.P=0.55). This up-regulation is consistent with, but does not by itself establish, T-cell exhaustion in Mars1 and was not part of the original Mars1 definition of Scicluna et al. [4]; it is reported here as a hypothesis requiring single-cell confirmation."

---

### 3. HAVCR2 is mislabeled an "antigen-presentation / monocytic hub gene" in the Abstract and §3.3, contradicting the manuscript's own APC-checkpoint framing

【Problem】 The Abstract and Results classify HAVCR2/TIM-3 as one of "five antigen-presentation / monocytic hub genes," but the manuscript elsewhere treats HAVCR2 as an APC-expressed exhaustion checkpoint that is down-regulated as an abundance marker. TIM-3 is not an antigen-presentation or monocytic gene, so the label is both imprecise and internally inconsistent.

【Evidence】 manuscript.md:14 (Abstract): "five antigen-presentation / monocytic hub genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2)"; manuscript.md:105 (§3.3): "five immune hub genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2)"; contrasted with manuscript.md:71–72 and :135, which explicitly define HAVCR2 as "an APC-expressed checkpoint."

【Why it matters】 The Abstract must accurately summarize the results; an inconsistent hub definition (antigen-presentation gene vs. APC checkpoint) undermines credibility and confuses what the Mars1 hub actually represents. A Nature-Portfolio editor/reviewer will flag an abstract that does not match the body.

【Specific fix】 Replace "five antigen-presentation / monocytic hub genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2)" (Abstract) with: "five immune hub genes anchored in the antigen-presentation/monocytic program (CD74, HLA-DQA1, CD14, FCGR3A) plus the APC-expressed checkpoint HAVCR2/TIM-3."

---

### 4. Glaring omission of foundational immunoparalysis literature (Monneret on mHLA-DR dynamics; Venet) despite mHLA-DR being repeatedly invoked as "the validated clinical anchor"

【Problem】 The manuscript repeatedly asserts that monocyte mHLA-DR is "the validated clinical anchor" of immunoparalysis (§3.8 line 135; Limitation 8 line 202) yet never cites the foundational body of work that *established* longitudinal mHLA-DR monitoring as the bedside immunoparalysis biomarker (Monneret and colleagues), nor the Venet line of work on lymphocyte/T-cell exhaustion and apoptosis in sepsis. Hotchkiss is cited (refs 17, 34) and Joshi (ref 35), but Monneret and Venet are absent.

【Evidence】 manuscript.md:135 ("mHLA-DR remains the validated clinical anchor [35]") and manuscript.md:202 (Limitation 8: "Monocyte mHLA-DR remains the canonical, complementary bedside immunoparalysis biomarker"); the reference list (manuscript.md:284–318) contains no Monneret and no Venet entry.

【Why it matters】 The entire clinical-anchor argument and the authors' caution about ImmunoSep rest on mHLA-DR biology that was defined by Monneret's group (e.g., the <5,000–8,000 mAb/cell threshold and its prognostic value). Omitting it makes the biomarker context look ungrounded and weakens the paper's authority on its core topic (immunoparalysis). For a journal whose scope includes biological mechanisms, this is a conspicuous gap.

【Specific fix】 Add to the reference list, e.g.: "Monneret, G. et al. Monitoring immune dysfunctions in the septic patient: a new skin for the old ceremony. *J. Biomed. Biotechnol.* **2010**, 314549" and "Venet, F. & Monneret, G. Advances in the understanding and treatment of sepsis-induced immunosuppression. *Nat. Rev. Nephrol.* **14**, 121–137 (2018)." Then in §3.8 replace "mHLA-DR remains the validated clinical anchor [35]" with "mHLA-DR remains the most validated single clinical anchor of immunoparalysis (Monneret et al.; Joshi et al. [35])."

---

### 5. The ImmunoSep (Giamarellos-Bourboulis 2025 JAMA) "53% unclassifiable / dual ferritin+mHLA-DR" quantitative claim is unverifiable from the manuscript and should be confirmed against the publication; the "no mortality benefit" caveat needs the underpowered framing

【Problem】 The paragraph states that "53% of screened patients were unclassifiable by a dual ferritin-and-mHLA-DR algorithm (mHLA-DR cutoff <5,000 receptors/cell on CD45/CD14 monocytes; 'unclassifiable' = normal ferritin AND normal HLA-DR)." This is a precise factual assertion that cannot be verified from the manuscript text and may not match the published ImmunoSep report; moreover, presenting it as a flat 53% unclassifiability and a definitive "no mortality benefit" overstates the maturity of the dual algorithm and the trial's power for the mortality endpoint. The general caution (more hemorrhagic events with IFN-γ; mHLA-DR remains anchor) is fair.

【Evidence】 manuscript.md:135 (§3.8): "53% of screened patients were unclassifiable by a dual ferritin-and-mHLA-DR algorithm (mHLA-DR cutoff <5,000 receptors/cell on CD45/CD14 monocytes; 'unclassifiable' = normal ferritin AND normal HLA-DR)"; ref 32 (manuscript.md:315) is the ImmunoSep JAMA 2025 citation, listed only as "JAMA (2025)" without volume/issue/pages.

【Why it matters】 If the exact percentage, the algorithm definition, or the cutoff does not match the published trial, it is a factual error in a high-visibility clinical-translation paragraph. Even if approximately correct, the ImmunoSep mortality comparison was underpowered (and the trial was not powered for a mortality claim in the IFN-γ arm), so "no mortality benefit" should be framed as underpowered rather than as a refutation of IFN-γ.

【Specific fix】 Replace "53% of screened patients were unclassifiable by a dual ferritin-and-mHLA-DR algorithm (mHLA-DR cutoff <5,000 receptors/cell on CD45/CD14 monocytes; 'unclassifiable' = normal ferritin AND normal HLA-DR); mHLA-DR remains the validated clinical anchor [35]" with: "In ImmunoSep, a substantial proportion of screened patients could not be assigned to the immunoparalysis or MALS stratum by the ferritin-plus-mHLA-DR algorithm [insert the exact reported percentage and algorithm definition from Giamarellos-Bourboulis et al. [32]]; this underscores that mHLA-DR remains the most validated single clinical anchor of immunoparalysis (Monneret et al.; Joshi et al. [35]). The trial's null mortality result and excess hemorrhagic events in the IFN-γ arm were underpowered for mortality and should be read as a caution, not as definitive evidence against IFN-γ." (Also supply full JAMA citation details for ref 32.)

---

## Minor domain notes

- **Internal contradiction between PDCD1-up and HAVCR2-down narratives (Items 1–2 combined):** The same §3.1 paragraph argues PDCD1/LAG3 up = T-cell exhaustion is *present*, while HAVCR2 down = T-cell exhaustion is *absent* (APC abundance). These two readings coexist only by asserting TIM-3 is APC-specific here, which bulk data cannot support. The manuscript is commendably honest about the tension, but it should state plainly that the bulk profile cannot resolve it rather than implying the APC-abundance reading is established.
- **Reference formatting for ref 32:** Giamarellos-Bourboulis et al. is listed as "*JAMA* (2025)" with no volume/issue/pages/DOI. For a 2025 Nature-Portfolio submission this should be completed to full bibliographic standard.

---

## § Stands up (strengths, with evidence)

1. **Faithful recapitulation of the core Mars1 antigen-presentation/monocytic program.** The downregulation of CD74, HLA-DQA1, CD14 and FCGR3A with strong statistics is exactly what the MARS consortium described: HLA-DRB1 Δ=−0.89 (adj.P=1.1×10⁻¹⁵), CD74 Δ=−0.76 (adj.P=2.1×10⁻¹⁵), CD14 Δ=−0.77, FCGR3A Δ=−0.61 (adj.P=9.1×10⁻¹¹) (manuscript.md:72, Table 1). This is a defensible confirmation of Mars1 and the strongest biological claim in the paper.
2. **Clinical-readiness claims for IL-7, GM-CSF, IFN-γ and the Bo meta-analysis are accurately represented.** IL-7 "restored lymphocytes in septic shock (Francois et al. [11])" (IRIS-7, JCI Insight 2018), GM-CSF "restored monocyte HLA-DR (Meisel et al. [12])" (AJRCCM 2009), IFN-γ "restored monocyte HLA-DR (Döcke et al. [13])" (Nat Med 1997), and "a meta-analysis found no mortality benefit for G-CSF/GM-CSF in sepsis (Bo et al. [30])" (Crit Care 2011) all match the cited primary literature (manuscript.md:120, 134–135; refs 11–13, 30).
3. **Appropriate biological caution on the MR and reverse-connectivity layers.** The manuscript correctly scopes the two-sample MR as hypothesis-generating (no primary IVW significant; explicit eQTLGen–UK-Biobank sample overlap; no Steiger test) (manuscript.md:147–176, 210), and the glucocorticoid reverse-connectivity caveat — prednisone/dexamethasone score high on the L1000 Mars1-down rescue despite being immunosuppressive (manuscript.md:142) — is a sound biological sanity check that honestly bounds the repositioning claim.
4. **mHLA-DR positioned as a complementary bedside anchor, not a competitor.** Limitation 8 (manuscript.md:202) correctly states the transcriptomic signature is intended to be used *with* monocyte mHLA-DR, not to replace it — biologically appropriate.

---

## § Questions for the authors (answers not assumed)

1. Please confirm the exact ImmunoSep (Giamarellos-Bourboulis 2025) reported percentage of patients unclassifiable by the ferritin+mHLA-DR algorithm, the precise algorithm definition, and the cutoffs used in that trial. Does "unclassifiable = normal ferritin AND normal HLA-DR" match the publication, and is the <5,000 receptors/cell mHLA-DR cutoff the one ImmunoSep actually applied?
2. In the original MARS Mars1 characterization (Scicluna 2017; Davenport 2016), were PDCD1, HAVCR2/TIM-3 and LAG3 expression examined, and if so what were the reported directions? Does your "T-cell exhaustion axis" reading reproduce a published MARS-subtype finding, or is it a novel re-interpretation of the re-analyzed GSE65682 cohort?
3. Given that HAVCR2 is measured in bulk blood, what evidence beyond direction supports attributing its downregulation to APC/monocyte abundance loss rather than lower per-cell TIM-3 expression on residual cells? Have you examined cell-type-specific expression (e.g., monocytes vs CD4/CD8 T) in any subset, or is the APC-abundance reading purely inferential?
4. Were Monneret's and Venet's foundational immunoparalysis works considered for citation? If omitted deliberately, on what basis, given that mHLA-DR is invoked as "the validated clinical anchor" throughout?

---

## § What I actually checked

- **File read:** the complete `manuscript.md` (lines 1–319) — Abstract, Introduction, Materials & Methods (§2.1–2.12), Results (§3.1–3.10), Discussion, Limitations (1–13), Conclusion, Data availability, Ethics, and the full References list (lines 282–319).
- **Biological framings verified against:** the cited MARS references (Scicluna 2017 = ref 4; Davenport 2016 = ref 5), the clinical RCT/meta-analysis citations (François IRIS-7 = ref 11; Meisel GM-CSF = ref 12; Döcke IFN-γ = ref 13; Bo G-CSF/GM-CSF meta = ref 30; Giamarellos-Bourboulis ImmunoSep = ref 32), and domain knowledge of TIM-3/HAVCR2 expression biology, the mHLA-DR immunoparalysis biomarker literature, and T-cell exhaustion in sepsis.
- **Reference-list audit:** confirmed the presence of Hotchkiss (refs 17, 34) and Joshi (ref 35) and the **absence** of Monneret and Venet.
- **Independence:** I did **not** open any `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `review_r*/` outputs, `cover_letter.md`, `scirep_submission_checklist.md`, `journal_recommendation.md`, any `MEMORY.md`, project overview, or other reviewer artifacts. Every judgement above is derived solely from the manuscript text I read and from established domain literature.
