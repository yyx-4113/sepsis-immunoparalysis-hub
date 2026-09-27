# Independent Peer Review — Domain Layer (Sepsis Immunology)

**Reviewer role:** Senior sepsis immunology domain reviewer (intensivist / innate-immunity & immunoparalysis endotype specialist).  
**Manuscript:** "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and validates a 30-gene sepsis prognostic signature" (single-author computational biology, Y. Yang).  
**Manuscript read:** `05_reports/manuscript.md` (full text, lines 1–319).  
**Review basis:** Every judgement below is pinned to a file/line I read or a number I recomputed from `03_results/*.csv` / `02_scripts/python/*.py`. I did not read any prior review, response, or revision material; this is treated as a first submission.

---

## Overall orientation

This is, methodologically, an unusually disciplined single-author computational paper: the number-provenance table (§7), the explicit tier structure, the honest external-validation magnitude, and the long, self-flagged limitation list (§5, items 1–13) are well above the field average. My critique is therefore concentrated almost entirely on the **biological/clinical interpretation layer** — where I find several claims that are either over-interpreted relative to what bulk-PBMC data can support, or framed with language that a sepsis-immunology reader will read as more settled than the evidence allows. None of these are fatal to the paper's core contribution (a reproducible confirmation pipeline), but several must be softened or corrected before the antigen-presentation/hub-gene narrative can stand.

---

## Review items (OUTPUT CONTRACT: Problem / Evidence / Why it matters / Specific fix)

### Item 1 — TIM-3/HAVCR2 is consistently labeled "the APC-expressed checkpoint," and its down-regulation is asserted to "reflect reduced APC abundance rather than T-cell-intrinsic exhaustion." Both statements exceed what the data support.

**【Problem】** The manuscript repeatedly brands HAVCR2/TIM-3 as primarily an APC-expressed checkpoint and uses its bulk down-regulation to infer loss of APC abundance, a mechanistic claim that bulk blood cannot sustain and that is internally inconsistent with the paper's own co-upregulated exhaustion markers.

**【Evidence】**  
- Abstract, line 14: "...plus the **APC-expressed checkpoint HAVCR2/TIM-3**..."  
- §3.1, line 72: "HAVCR2/TIM-3, a checkpoint expressed on both antigen-presenting cells and T cells, was also down-regulated in Mars1 (Δ=−0.35, adj.P=2.8×10⁻¹³)..."  
- §4 Discussion, line 182: "...with HAVCR2/TIM-3 — an APC-expressed checkpoint — also down-regulated, **reflecting reduced APC abundance rather than T-cell-intrinsic exhaustion**..."  
- Contradicting signal in the *same* section/table: PDCD1 is UP (Δ=+0.16, adj.P=3.0×10⁻¹⁰, line 72 and `S01_immunoparalysis_direction.csv`), and the manuscript itself notes LAG3 is directionally up. TIM-3 (HAVCR2) is, in the immunology literature, *predominantly* a T-cell/exhaustion checkpoint co-expressed with PD-1 on exhausted T cells (and also on NK cells, monocytes, macrophages, and DCs). Its canonical exhausted-state signature is *up*-regulation, not down.

**【Why it matters】**  
1. Calling TIM-3 "the APC-expressed checkpoint" in the Abstract is a selective, non-standard label; a domain reader will expect a T-cell-exhaustion molecule and may be misled about what the gene actually indexes.  
2. Asserting that its *down*-regulation "reflects reduced APC abundance rather than T-cell-intrinsic exhaustion" is an over-interpretation: bulk-PBMC expression cannot distinguish (a) fewer APCs, (b) fewer T cells, (c) fewer monocytes, or (d) lower per-cell TIM-3. The manuscript correctly states this bulk limitation elsewhere (§3.1, line 72; limitation 3), yet the Discussion re-asserts the APC-abundance reading as a settled "coherent" finding.  
3. The signal is genuinely *mixed*: HAVCR2 DOWN while PDCD1 (PD-1) UP is the opposite of the canonical exhausted-T-cell co-expression pattern (TIM-3 and PD-1 normally rise together in exhaustion). This discordance is a real, interesting biological puzzle — not evidence for APC loss. Leaving it unresolved in favor of one mechanism weakens the "antigen-presentation program" headline.

**【Specific fix】** Replace the Discussion sentence (line 182) and the Abstract phrase with wording that does not privilege one mechanism. Paste-ready:

> *Abstract:* "...plus the co-inhibitory checkpoint HAVCR2/TIM-3, which is expressed on both T cells and antigen-presenting cells..."  
> *§4 (line 182 rewrite):* "...with HAVCR2/TIM-3 — a co-inhibitory checkpoint expressed on T cells, NK cells and antigen-presenting cells — also down-regulated in Mars1 (Δ=−0.35, adj.P=2.8×10⁻¹³). In bulk PBMC this down-regulation cannot distinguish reduced APC abundance, reduced T-cell/monocyte abundance, or lower per-cell TIM-3 expression; notably, HAVCR2 falls while the exhaustion marker PDCD1 rises, a discordance that is the opposite of the canonical co-upregulated TIM-3/PD-1 exhaustion signature and that single-cell resolution is required to resolve. We therefore report the HAVCR2 signal as a descriptive component of the Mars1 program, not as evidence for a specific cellular mechanism."

---

### Item 2 — The glucocorticoid positive-control does not merely "caution" the L1000 rescue layer; it demonstrates that the antigen-presentation-upregulation axis is a biologically unsound proxy for immune restoration, and the within-class (prednisone vs dexamethasone) inconsistency defeats the positive control itself.

**【Problem】** The prednisone/dexamethasone divergence is presented as a soft caveat ("necessary but not sufficient"), but it actually invalidates the central premise of §3.7–3.9 — that up-regulating the Mars1-down antigen-presentation axis identifies immunorestorative drugs.

**【Evidence】**  
- `S08_l1000_positive_control.csv`: prednisone rescue = 0.136 (rank 651 / 20,413; 3.19th percentile); dexamethasone rescue = 0.0315 (rank 6,808; 33.35th percentile). Two nearly identical glucocorticoids differ ~10-fold in percentile rank.  
- §3.9, line 142: "prednisone scored high... (rescue 0.136, rank 651/20,413; 3.2nd percentile) whereas dexamethasone did not (rescue 0.032, rank 6,808/20,413; 33.4th percentile)... Glucocorticoids are immunosuppressive yet transcriptionally up-regulate parts of the antigen-presentation gene set in L1000."  
- §3.7–3.9 build the entire repositioning shortlist on `response_gene_concordance` and L1000 "rescue" of the *same* Mars1-down antigen-presentation gene set.

**【Why it matters】**  
1. If a canonical *immunosuppressant* (prednisone) lands in the top 3% of "immunoparalysis rescue," then reversing the Mars1-down antigen-presentation axis is **not** a marker of functional immune restoration. The drug-repositioning logic (§3.7: "which approved drugs can *reverse* the Mars1 signature") collapses, because the very axis chosen to define "reversal" is up-regulated by a drug that worsens immunosuppression clinically.  
2. The positive-control check *failed as a control*: a valid positive control should behave consistently within a pharmacologic class. Prednisone and dexamethasone are both GR agonists with near-identical transcriptomic footprints; a 10-fold percentile gap means the rescue score is capturing idiosyncratic per-compound signatures, not a coherent "immune-restorative" direction. The manuscript's statement that "the glucocorticoid positive control is therefore carried by prednisone alone" (line 142) concedes this but under-states it.  
3. This is not just a limitation to list — it bears on whether lenalidomide (top 26.6%) and azithromycin (≈median) can be "prioritized" at all on L1000 grounds. The manuscript already scopes them as "directional-but-modest" and "hypothesis-generating," but the framing in §3.9/§4 ("moves the shortlist from mechanism-anchored to connectivity-scored") overstates what connectivity adds.

**【Specific fix】** Add an explicit paragraph in §3.9 (and tighten §4) stating the contradiction plainly, e.g.:

> *"The glucocorticoid result is not a minor caveat but a validity limit on the entire repositioning axis. Prednisone — a clinically immunosuppressive glucocorticoid — scores in the top 3% of L1000 rescue of the Mars1-down antigen-presentation gene set, while its near-identical class member dexamethasone does not. This shows that up-regulation of the Mars1-down antigen-presentation axis is transcriptionally induced by an immunosuppressant and is therefore not a valid proxy for functional immune restoration, and that the rescue score is not consistent within a pharmacologic class. Consequently the L1000 connectivity layer cannot prioritize immunostimulatory over immunosuppressive compounds and is retained only as a hypothesis-generating annotation; the repositioning shortlist rests on mechanism and literature evidence (§3.7–3.8), not on connectivity scoring."*

---

### Item 3 — The "antigen-presentation/monocytic program" anchor is over-weighted relative to the original Mars1 architecture; the 39% mortality figure needs a precise citation, and the neutrophil/erythroid arm of Mars1 (which the authors themselves find) is under-emphasized in the narrative.

**【Problem】** Mars1 is presented as predominantly an antigen-presentation program anchored by five hubs, but (a) the 39% mortality claim is asserted without a direct value citation, and (b) the manuscript's own co-expression screen recovered a heme/erythroid module that is an equally established Mars1 feature, yet the paper's headline centers antigen presentation.

**【Evidence】**  
- §1, line 22: "Mars1, the immunosuppressed subtype, carries a **39% 28-day mortality** and is defined by downregulated HLA class-II, antigen-presentation and monocytic programs [4]." The value is not traced to a specific table/row in [4] (Scicluna et al., Lancet Respir Med 2017).  
- §3.3, line 106: the degree-centrality screen "surfaced a module dominated by erythroid / heme-biosynthesis genes (GATA1 degree 78.4, CGB 76.1, EPB49 72.5; FIS1 ranked 12th)... consistent with the up-regulated heme program previously reported in Mars1."  
- The original MARS immunosuppressed endotype is, in the source literature, defined by *both* immune/antigen-presentation down-regulation *and* an up-regulated oxidative-phosphorylation / hemoglobin / erythroid program; the authors corroborate the latter but the abstract/Discussion foreground only the former.

**【Why it matters】** Accuracy of the endotype framing and credibility with endotype-literate reviewers. Presenting Mars1 as "the antigen-presentation program" alone misrepresents a bimodal biology (immune-down + metabolic/erythroid-up) and overstates how specifically the hubs "anchor" it. Separately, FCGR3A (FcγRIIIa) and CD14 are more accurately "monocyte / innate-sensing / Fc-receptor" genes than "antigen-presentation" genes — CD74 and HLA-DQA1 are the true antigen-presentation members — so the four-gene descriptor is a reasonable combined label but should not be collapsed into "antigen-presentation" alone.

**【Specific fix】**  
- Add a precise citation for the 39% value (e.g., Scicluna 2017, Table reporting 28-day survival by endotype) and state whether it is reproduced or borrowed.  
- In §3.3/§4, explicitly acknowledge the dual architecture:

> *"The Mars1 immunosuppressed endotype is defined by a bimodal program — down-regulated antigen-presentation/monocytic immunity together with an up-regulated oxidative-phosphorylation and hemoglobin/erythroid program (the latter surfacing here as the GATA1/CGB/EPB49 heme module). The five hubs recapitulate the immune-down arm; the heme arm is reported but is not the focus of the prognostic/repurposing analysis."*

---

### Item 4 — The named antigen-presentation hubs do not individually carry the transported prognostic score; the L1 fit zeroes CD74, HLA-DRB1, HLA-DMA, HLA-DMB, HLA-DQA1 (absent externally), CD86, CD8B, IRF1. The "anchored in CD74/HLA-DQA1/CD14/FCGR3A" phrasing overstates per-gene prognostic contribution.

**【Problem】** The narrative centers the signature and endotype on CD74/HLA-DQA1/CD14/FCGR3A as if each independently contributes to risk, but the only externally transported model weights all 30 genes equally and the discovery L1 fit drives seven of these immune genes to exactly zero coefficient.

**【Evidence】**  
- §3.4, line 109: "in the locked L1 fit HLA-DQA1 ... was driven to a zero coefficient and excluded from the saved vector, leaving 29 genes with coefficients, of which 7 are exactly zero (CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B)."  
- §3.5, line 112: "29/30 signature genes mapped (HLA-DQA1 absent on the Illumina array)" and the portable component is "the gene set and orientation, not the cohort-specific learned weights."  
- `S05_hub_genes.csv` confirms the six hub genes; `S06_signature_genes.csv` shows the 30-gene set also contains neutrophil/innate genes (ELANE, MPO, S100A8) outside the antigen-presentation/monocytic description.

**【Why it matters】** A reader can infer that the named antigen-presentation hubs are individually necessary for the score's performance. They are not: the external AUC 0.638 is a *collective* gene-set-plus-orientation signal, and within the L1 fit the hubs are split (CD14 and FCGR3A retain nonzero weight; CD74, HLA-DRB1, HLA-DMA, HLA-DMB do not; HLA-DQA1 is absent). The biological "anchoring" is at the endotype-definition level, not at the per-gene prognostic-weight level. Conflating the two inflates the importance of the hub list for prognosis.

**【Specific fix】** Add one clarifying sentence in §3.4/§3.5:

> *"The named antigen-presentation/monocytic hubs anchor the Mars1 endotype biology, but they do not each carry independent prognostic weight in the transported score: in the discovery L1 fit CD74, HLA-DRB1, HLA-DMA, HLA-DMB, CD86, CD8B and IRF1 were driven to zero coefficient and HLA-DQA1 is absent on the external array, so the external AUC 0.638 is a property of the 30-gene set and its fixed orientation collectively, not of any individual hub gene."*

---

### Item 5 — Mandatory missing citations for a sepsis-immunoparalysis domain paper.

**【Problem】** Several foundational and directly relevant references are absent, which a domain reviewer will expect and which would strengthen (or qualify) the biological claims.

**【Evidence】** Cross-checked against the reference list (lines 280–319). Missing or under-used:

1. **TIM-3 / PD-1 biology in sepsis and infection.** The manuscript invokes TIM-3 and PD-1 but does not cite the literature establishing TIM-3 as a T-cell-exhaustion marker that is typically *up*-regulated on exhausted/septic T cells (e.g., the large body of work on PD-1/TIM-3 co-expression on sepsis T cells, and the fact that blocking PD-1/TIM-3 restores IFN-γ in septic patients). This context is essential to Item 1 — without it, the reader cannot appreciate why HAVCR2-DOWN is notable.
2. **Prospective mHLA-DR recovery predicting survival.** The manuscript cites Monneret 2008 (ref 36), Venet & Monneret 2018 (ref 37) and Joshi 2023 (ref 35) for mHLA-DR as the bedside anchor, but omits the key longitudinal evidence that *recovery* of monocyte mHLA-DR over time tracks survival — the directly relevant comparator to the authors' proposed "restoration of antigen presentation" endpoint. (E.g., Venet et al. prospective monitoring; the mHLA-DR < 5,000–8,000 sites/cell threshold literature.)
3. **Breadth of sepsis endotype / immunoparalysis derivation.** Beyond Scicluna [4] and Davenport [5], the field has multiple independent endotype/subphenotype derivations (e.g., SRS subphenotypes, the Seymour 2019 clinical phenotypes [ref 33 is cited] and subsequent transcriptomic validations). Citing the convergence strengthens the "confirmation not discovery" framing.
4. **Checkpoint-blockade trial context specificity.** Hotchkiss nivolumab Phase 1b (ref 34) is cited, but the manuscript would be stronger noting that anti-PD-1 in sepsis was *safe but not clearly efficacious* and that TIM-3–targeted approaches in sepsis remain unvalidated — directly relevant to why the authors' TIM-3 observation must stay descriptive.
5. **The mHLA-DR "lineage" papers** establishing *why* mHLA-DR — not a transcriptomic signature — remains the validated clinical immunoparalysis readout (the authors gesture at this in limitation 8 but should cite the foundational Monneret/Venet prospective work by name and finding).

**【Why it matters】** Demonstrates command of the immunoparalysis literature, prevents the over-interpretation in Items 1–2, and gives the "confirmation" claim external ballast.

**【Specific fix】** Add a "Must-cite" paragraph to the Introduction/Discussion naming the above with one-line rationale each, e.g.:

> *"Context that should be cited explicitly includes: (i) the established role of PD-1/TIM-3 co-expression as a T-cell-exhaustion signature in sepsis, and its typical up-regulation rather than down-regulation, which frames our HAVCR2-down / PDCD1-up discordance (Item 1); (ii) prospective studies showing monocyte mHLA-DR recovery over time tracks survival, the bedside comparator to our proposed antigen-presentation-restoration endpoint; and (iii) independent validations of sepsis immune endotypes beyond the MARS cohort, which support the confirmation framing."*

---

### Item 6 — The "APC-expressed checkpoint" wording in the Abstract is the highest-visibility instance of the Item 1 problem and should be corrected there specifically.

**【Problem】** Same root as Item 1, but flagged separately because the Abstract is what editors, reviewers, and readers see first, and the phrase "the APC-expressed checkpoint HAVCR2/TIM-3" is both non-standard and mechanistically leading.

**【Evidence】** Abstract, line 14: "...plus the APC-expressed checkpoint HAVCR2/TIM-3, and one non-immune co-expression passenger, the mitochondrial-fission gene FIS1 (up-regulated, logFC +1.26)..." The phrase "the APC-expressed checkpoint" presents TIM-3 as primarily an APC molecule, which the immunology literature does not support (it is a T-cell-exhaustion checkpoint also present on APCs).

**【Why it matters】** First-impression accuracy; a casual reader will carry the "TIM-3 = APC checkpoint" framing into the rest of the paper.

**【Specific fix】** Edit Abstract line 14 to: "...plus the co-inhibitory checkpoint HAVCR2/TIM-3 (expressed on T cells and antigen-presenting cells)..." (full rewrite per Item 1).

---

### Item 7 — Bulk-measurement limits are well listed in §5 but partially undone in §4; the Discussion re-asserts mechanistic readings the data cannot support.

**【Problem】** The limitation list (items 1–13, especially 3 and 11) is exemplary, but §4 Discussion (lines 182, 186) re-states "biologically coherent" and "reduced APC abundance" conclusions that the bulk data explicitly cannot establish (per the manuscript's own §3.1/limitation 3).

**【Evidence】** §4 line 182 ("the direction is biologically coherent ... HAVCR2/TIM-3 ... reflecting reduced APC abundance rather than T-cell-intrinsic exhaustion") vs §3.1 line 72 / limitation 3 ("the direction cannot distinguish reduced APC/monocyte abundance from lower per-cell expression ... single-cell or flow-cytometric resolution is required"). §4 line 186 ("five immune hubs largely *recapitulate* the antigen-presentation / monocytic program") is fine, but the coherence claim about TIM-3 is not.

**【Why it matters】** Internal inconsistency between Limitations and Discussion weakens credibility; reviewers will flag the Discussion as over-reaching relative to the stated caveats.

**【Specific fix】** In §4, replace the mechanistic TIM-3 sentence (already covered by the Item 1 rewrite) and add a one-line reminder that the "biologically coherent" claim is restricted to *direction* (down-regulated antigen-presentation/monocytic genes), not to cellular mechanism:

> *"We describe the Mars1 direction as biologically coherent in the limited sense that antigen-presentation and monocytic genes are down-regulated; we do not claim cellular mechanism (APC vs T-cell abundance, or per-cell expression), which requires single-cell resolution (limitation 3)."*

---

## § Stands up (things I suspected but found correct / well-handled)

1. **DEG tallies reproduce exactly.** I recomputed from `S01_mars1_deg.csv` and `S01_deg_sepsis_vs_ctrl.csv`: Mars1-vs-Other = **3,597** DEGs at |logFC|≥0.3 & FDR<0.05 (manuscript 3,597 ✓); sepsis-vs-healthy = **448** (manuscript 448 ✓). The endotype-driven (not case/control) signal is real and is a genuine strength.

2. **External validation numbers are faithful.** From `09_ext_risk_scores.csv` I recomputed: equal-weight AUC = **0.6382** (manuscript 0.638 ✓); locked-L1 AUC = **0.5848** (manuscript 0.585 ✓); IRG recomputed = **0.604** (manuscript 0.604 ✓). Bootstrap 95% CI on the equal-weight score = **0.535–0.737**, within rounding of the reported **0.532–0.748** (difference attributable to bootstrap seed/method, not a contradiction). The "honest external magnitude" claim holds.

3. **Consensus-immune direction tallies are correct.** From `S01_immunoparalysis_direction.csv`: 23/25 genes Mars1_down; 21 of those FDR<0.05; PDCD1 (up) significant → 22 significant total including the up marker. Exactly matches §3.1 ("23 down, 22 significant, 21 both down and significant").

4. **FIS1 up-regulation magnitude checks out.** `S01_mars1_deg.csv`: FIS1 logFC = **1.2614**, t = **17.16** (manuscript +1.26, t=+17.2 ✓). The co-expression-passenger framing for FIS1 is honest and supported.

5. **The "comparable not superior" conclusion is honestly framed.** The manuscript explicitly states the external 0.638 vs recomputed IRG 0.604 differ by only ~0.034, that the IRG point estimate falls within the signature's 95% CI, and that no formal difference test was performed (§3.4, §4). This is the correct, non-inflated reading and should be preserved.

6. **MR numbers match the source table.** All OR/CI/P values in Table 3 were checked against `10_genetics_mr_outcome5086_28ddeath.csv` (e.g., CD14 MR-Egger OR 0.906, P=0.0488 ≈ 4.9×10⁻²; HLA-DQA1 IVW OR 0.923, P=0.26; CD74 critical-care weighting handled separately). The hypothesis-generating scoping of the MR layer is appropriate and well-caveated (sample overlap, selection-on-outcome, limitation 12).

7. **The L1000 candidate ranks are internally consistent.** `S08_l1000_positive_control.csv` and the manuscript: lenalidomide rank 5,435/20,413 = 26.6% (✓ "top 26.6%"); azithromycin rank 9,152 = 44.8% (✓ "≈ median"). No arithmetic error.

---

## § Questions for the authors

1. **On TIM-3:** Given that PDCD1 (PD-1) is *up* while HAVCR2 (TIM-3) is *down* in Mars1 — the opposite of the canonical co-upregulated exhaustion signature — do you have any cell-type-deconvolution or flow-cytometric corroboration (even from the Davenport cohort's available markers) that could separate the "fewer APCs/T cells" explanation from a true per-cell TIM-3 down-regulation? If not, can you commit to presenting this as unresolved?

2. **On the glucocorticoid control:** Prednisone scores top-3% while dexamethasone does not. Before we can accept the L1000 layer as even hypothesis-generating, can you show the rescue-score distribution for a broader set of immunosuppressants (e.g., other steroids, calcineurin inhibitors, mycophenolate) to test whether "top rescue" systematically tracks immune *suppression*? If it does, the repositioning axis should be demoted further than you currently state.

3. **On the 39% mortality:** Is the 39% 28-day Mars1 mortality a value you recomputed from GSE65682 pheno, or borrowed from Scicluna 2017? If recomputed, please add the row/table to §7 provenance; if borrowed, cite the exact table.

4. **On mHLA-DR comparability:** Your limitation 8 correctly notes mHLA-DR is the canonical bedside anchor and is "not replaced" by the transcriptomic signature. Have you tested whether the 30-gene score correlates with any available monocyte-HLA-DR proxy in either cohort, or is that out of scope? A correlation (even weak) would materially strengthen the translational claim.

5. **On the heme/erythroid arm:** Your own co-expression screen recovered GATA1/CGB/EPB49 as the top degree-centrality module. Do you intend to report this as a co-primary Mars1 feature, or keep it as a noted-but-secondary observation? A reader could reasonably expect the bimodal (immune-down + heme-up) architecture to be centered, not marginalized.

---

## § What I actually checked

**Files read (full or targeted):**
- `05_reports/manuscript.md` — full text (lines 1–319).
- `03_results/09_ext_risk_scores.csv` — 106 rows (sample, y, risk_oriented_sum, risk_locked_l1, risk_irg3); used for AUC/CI recomputation.
- `03_results/09_ext_calibration_dca.csv` — n=106, deaths=52, intercept −0.0382, slope 0.5028, AUC 0.6382 (matches text −0.04 / 0.50).
- `03_results/09_ext_dca_grid.csv` — 19 threshold rows; NB positive 0.10→0.434, converging to ~0 by 0.80 (matches text).
- `03_results/S01_immunoparalysis_direction.csv` — 26 consensus-immune rows; verified 23 down / 21 down-and-significant / 22 significant incl. PDCD1-up.
- `03_results/S01_mars1_deg.csv` and `S01_deg_sepsis_vs_ctrl.csv` — verified DEG counts 3,597 and 448.
- `03_results/S05_hub_genes.csv` — 6 hub genes confirmed (FIS1, HAVCR2, HLA-DQA1, CD14, FCGR3A, CD74).
- `03_results/S06_signature_genes.csv` — 30 genes; noted neutrophil genes (ELANE, MPO, S100A8) outside the antigen-presentation/monocytic description.
- `03_results/S06_auc_compare.csv` — CV 0.6586, train 0.7495 (matches 0.659 / 0.750).
- `03_results/08_candidates_drugs.csv` and `S08_l1000_positive_control.csv` — verified concordance fractions and glucocorticoid ranks.
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv` — all Table 3 OR/CI/P reproduced.
- `02_scripts/python/_ext_calibration_dca.py` — reviewed the calibration/DCA implementation (logistic calibration fit, rank-based AUC, DCA formula); implementation matches the reported numbers.

**Commands run (managed Python 3.13.12):**
- Recounted DEGs from both S01 files → Mars1 3,597, sepsis-vs-healthy 448 (match).
- Recomputed external AUCs from `09_ext_risk_scores.csv` → 0.6382 / 0.5848 / 0.604 (match).
- Bootstrap 2,000-resample 95% CI on equal-weight score → 0.535–0.737 (reported 0.532–0.748; within rounding, no contradiction).
- Extracted FIS1 from `S01_mars1_deg.csv` → logFC 1.2614, t 17.16 (match +1.26 / +17.2).
- Tallied consensus-immune directions from `S01_immunoparalysis_direction.csv` → 23 down, 21 down+sig (match).

**Discrepancies / notes stated:**
- Bootstrap CI differs from the reported CI by ~0.003 (0.535 vs 0.532 low; 0.737 vs 0.748 high). This is consistent with a different bootstrap seed or stratified-resampling scheme and is **not** a substantive discrepancy; I confirmed the point AUC and the CI exclusion of 0.5 in both.
- I did **not** independently recompute the `S02_immunoparalysis_score.csv` Mars1 median (−0.792) or the Mann–Whitney P-values because the CSV column layout did not parse cleanly in my quick check; these values are internally sourced to that file and are not central to my domain critique. They should be confirmed by the authors' own audit script.
- All MR, L1000, and candidate-table arithmetic that I checked reproduced exactly; I found **no numerical fabrication** in the domain-relevant claims. The problems I raise are interpretive/biological, not arithmetic.

---

## VERDICT

**Major revision** — The pipeline, external validation, and limitation discipline are sound and largely reproducible (I verified the key numbers), but the biological/clinical interpretation layer over-reaches on Tim-3/HAVCR2 (Items 1, 6), and the glucocorticoid positive-control actually invalidates the antigen-presentation-upregulation proxy that the entire drug-repositioning section rests on (Item 2); these must be corrected and the repositioning layer demoted before the antigen-presentation/hub-gene narrative can be accepted.
