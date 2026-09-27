# A1 — Domain Expert Review (Sepsis Immunology / Critical-Care Clinician-Scientist)

**Manuscript:** `manuscript.md` (git tag v1.9.0)
**Reviewer role:** A1 — Domain expert (independent, treated as a fresh first submission)
**Independence note:** I did not read any prior-round review/response files, `review_r1/`–`review_r9/`, the other `review_r10/` reviewers, or the manifest/verification statements. All claims below are verified from the manuscript text and the `03_results/` files I read myself, plus the primary ImmunoSep record (JAMA, doi:10.1001/jama.2025.24175) retrieved independently.

---

## Overall assessment

The biology is, on the whole, **correctly framed**: Mars1 is an immunosuppressed endotype defined by down-regulated HLA-class-II / antigen-presentation / monocytic programs, and the re-analysis faithfully recovers that signature (23/25 consensus immune genes directionally down; 22 FDR-significant). The self-description as a "near-replication rather than novel gene discovery" is honest and commendable. However, there is **one genuinely misleading biological claim (the TIM-3/HAVCR2 direction within an "exhaustion axis")** and a **partially inaccurate citation of the ImmunoSep trial**, plus several literature-gap and endpoint issues that should be addressed before acceptance. None of these invalidate the Tier-1 biology, but two of them (A1.1, A1.2) affect how a clinician reads the "immune-checkpoint axis" and the drug-repositioning logic.

---

## Major issues (each with the four required parts)

### A1.1 — TIM-3/HAVCR2 is reported DOWN and lumped into an "antigen-presentation/monocytic" program, contradicting its canonical role as an exhaustion checkpoint up-regulated in immunoparalysis

**【Problem】** Presenting HAVCR2/TIM-3 as a down-regulated member of the antigen-presentation/immunosuppression axis is biologically incoherent with TIM-3's established role as a T-cell exhaustion marker that is *up*-regulated in sepsis immunoparalysis, and it is not reconciled with the co-occurring up-regulation of PDCD1 and LAG3.

**【Evidence】** `03_results/S01_immunoparalysis_direction.csv` line 6: HAVCR2 logFC = −0.3488, adj.P = 2.838e-13, direction `Mars1_down` (verified). Manuscript line 82 states HAVCR2/TIM-3 Δ = −0.35, adj.P 2.8e-13 and explicitly folds it into the down-regulated axis ("including TIM-3/HAVCR2"); line 116 calls the five hubs "antigen-presentation / monocytic / exhaustion-axis genes"; line 145 frames "the exhaustion markers PDCD1 and LAG3 are up-regulated in Mars1, whereas HAVCR2/TIM-3 is itself down-regulated … together they frame an immune-checkpoint axis." Meanwhile S01 line 8 PDCD1 is UP (+0.1619, adj.P 2.995e-10) and line 26 LAG3 is UP directionally (+0.0351, adj.P 0.552, not significant).

**【Why it matters】** TIM-3 (HAVCR2) is expressed on both T cells *and* monocytes/macrophages/dendritic cells. In bulk PBMC from an endotype with profoundly down-regulated monocytic/APC programs (CD14, FCGR3A, HLA-DR family all DOWN, S01), a *down*-regulated HAVCR2 most plausibly reflects **loss of APC/monocyte TIM-3 expression**, not T-cell exhaustion. Treating it as part of the "down-regulated immunosuppression axis" therefore conflates an APC-abundance correlate with a true exhaustion driver. The simultaneous "checkpoint axis" narrative (one checkpoint down, two up) is internally contradictory and will mislead clinicians who expect TIM-3 to be a targetable exhaustion marker. It also weakens the repositioning logic, which then attempts to "rescue" a gene that is arguably just a passenger of monocyte depletion.

**【Specific fix】** Replace the exhaustion-axis framing of HAVCR2 with an APC-abundance interpretation, e.g.:
> "HAVCR2/TIM-3 was down-regulated in Mars1 (logFC −0.35, adj.P 2.8e-13). Because TIM-3 is co-expressed on monocytes and dendritic cells, this direction most likely reflects the depletion/down-regulation of antigen-presenting cells in Mars1 rather than T-cell-intrinsic exhaustion; consistent with this, the T-cell-restricted checkpoint PDCD1 was up-regulated (Δ +0.16, adj.P 3.0e-10) whereas the broadly expressed HAVCR2 tracked the APC program. HAVCR2 is therefore reported as an APC-compartment marker within the Mars1 signature, not as an independent exhaustion driver."

---

### A1.2 — The decision to *not* prioritise checkpoint blockade is unexplained, while the reported PDCD1-up signal argues the opposite; the cited nivolumab sepsis trial is never discussed

**【Problem】** The manuscript states checkpoint-blockade agents (anti–PD-1/PD-L1, anti–CTLA-4) were "not prioritised" but the rationale is truncated (manuscript line 145 ends mid-sentence "… because rele…"), and the logic is inconsistent with its own data showing PDCD1 significantly up-regulated.

**【Evidence】** S01 line 8: PDCD1 up (+0.1619, adj.P 2.995e-10) — a genuine T-cell exhaustion signal; CTLA4 is *down* (line 22: −0.0904, adj.P 0.0343, below fold-change threshold). Manuscript Reference [34] is Hotchkiss et al. *Intensive Care Medicine* 2019 (nivolumab phase 1b in sepsis), yet the repositioning discussion (§3.7–3.8) never engages it. The checkpoint-blockade non-prioritization sentence (line 145) is cut off and unrecoverable from the text provided.

**【Why it matters】** If PD-1 is up-regulated on T cells in Mars1, then PD-1/PD-L1 blockade is a *prima facie* immunorestorative strategy — and indeed it has been tested in sepsis (Hotchkiss 2019, cited but unused). Reporting PDCD1-up while silently excluding checkpoint blockade leaves a logical hole: either the up-regulation supports anti–PD-1 (contradicting the stated decision) or the decision rests on the bulk HAVCR2-down signal (which, per A1.1, is an APC correlate). Reviewers and clinicians need this reconciled; otherwise the repositioning shortlist looks arbitrarily curated.

**【Specific fix】** Either (a) add a short paragraph justifying the exclusion, e.g.:
> "Although PDCD1 was up-regulated in Mars1, we did not prioritise PD-1/PD-L1 or CTLA-4 blockade. Rationale: (i) the bulk HAVCR2 signal indicates APC loss rather than T-cell-intrinsic TIM-3 exhaustion, so the Mars1 program is dominated by antigen-presentation/monocytic failure, not a PD-1–driven T-cell exhaustion state; (ii) the single published anti–PD-1 sepsis trial (Hotchkiss et al., 2019, ref 34) is a phase 1b safety study without efficacy signal; and (iii) our repositioning metric is anchored to reversal of the Mars1-down APC axis, which cytokine/myeloid agents address more directly than checkpoint inhibitors."
Or (b) explicitly include anti–PD-1/PD-L1 as a hypothesis to be tested in the S11 blueprint. Do not leave the sentence truncated.

---

### A1.3 — "Near-replication" self-assessment is honest, but the "co-expression hub" claim is overstated and HAVCR2 is the weakest hub

**【Problem】** The five hubs are correctly characterised as a near-replication of the Mars1 antigen-presentation/monocytic program, but the manuscript over-states that they emerge from a "co-expression degree-centrality network," and lists HAVCR2 as a co-equal hub when it is the least Mars1-defining of the six.

**【Evidence】** `03_results/S05_hub_genes.csv`: all six genes (FIS1, HAVCR2, HLA-DQA1, CD14, FCGR3A, CD74) are `True` for lasso/rf/univariate — i.e., they came from the *tri-method ML consensus on 28-day survival*, not the co-expression network. Manuscript line 116 itself admits: "the degree-centrality screen of the top-2000 Mars1-DEGs surfaced a module dominated by erythroid / heme-biosynthesis genes (GATA1 degree 78.4, CGB 76.1, EPB49 72.5; FIS1 ranked 12th) … the five immune hubs … were therefore carried by the tri-method ML consensus rather than by the co-expression network alone." The title ("multi-omics dissection") and §2.4 imply network centrality produced the hubs; in fact the co-expression screen pointed elsewhere. Of the five immune hubs, CD74/HLA-DQA1/CD14/FCGR3A are textbook antigen-presentation/monocytic genes (expected); HAVCR2 is the outlier (see A1.1).

**【Why it matters】** Calling these "hub genes" derived from a co-expression network over-states the network-method contribution and may lead readers to infer causal/regulatory centrality that the analysis does not establish. The honest statement already in line 116 should be elevated, not buried.

**【Specific fix】** In the Abstract/Results, rephrase to:
> "The tri-method machine-learning consensus (operating on 28-day-survival-associated, immune-annotated genes) recovered five immune hubs — CD74, HLA-DQA1, CD14, FCGR3A and HAVCR2 — that recapitulate the antigen-presentation/monocytic Mars1 program; the co-expression degree-centrality screen independently surfaced a distinct erythroid/heme module and is therefore reported separately rather than as the source of these hubs."

---

### A1.4 — The Mars1 = "immunosuppressed, 39% 28-day mortality" framing is broadly correct but needs precise citation and label-stability confirmation

**【Problem】** The Mars1 immunosuppressed characterisation matches the MARS literature, but the specific 39% mortality figure is asserted without a precise inline citation, and endotype labels are not always stable across MARS derivation/validation cohorts.

**【Evidence】** Manuscript line 34: "Mars1, the immunosuppressed subtype, carries a 39% 28-day mortality and is defined by downregulated HLA class-II, antigen-presentation and monocytic programs [4]." Reference [4] is Scicluna et al., *Lancet Resp Med* 2017 — the correct paper. S01 confirms the directional biology (23/25 immune genes down; HLA-DRB1 −0.89, CD74 −0.76, CD14 −0.77, all adj.P < 1e-15 to underflow). GSE65682 is the MARS consortium dataset on GPL13667 (Affymetrix Human Gene 1.0 ST), so the `mars_endotype` labels in the phenotype are the published MARS labels — label consistency with Scicluna is therefore likely, but the manuscript never demonstrates gene-set overlap with the published Mars1 signature.

**【Why it matters】** A clinician reviewer will accept "Mars1 = immunosuppressed" but will want the 39% tied to a specific table/figure in Scicluna 2017, and will want assurance that the authors' Mars1 is the same Mars1 the literature describes (different MARS analyses have occasionally re-ordered endotype labels). Without this, the foundational claim rests on an unverified label match.

**【Specific fix】** Add: "The Mars1 immunosuppressed characterisation and 39% 28-day mortality follow Scicluna et al. (2017), Table/Figure X. We confirmed our GSE65682 Mars1 labels reproduce the published Mars1 signature by computing the overlap between our Mars1-down gene set and the published Mars1-defining module (Jaccard/leading-edge overlap = …)."

---

### A1.5 — The ImmunoSep "53% unclassifiable by mHLA-DR" citation is inaccurate: the 53% reflects a dual ferritin + mHLA-DR algorithm, not mHLA-DR alone

**【Problem】** The manuscript attributes the 53% unclassifiability in ImmunoSep to "the monocyte HLA-DR (mHLA-DR) criterion," but ImmunoSep classified patients with a *combined* ferritin (>4420 ng/mL) **and** mHLA-DR (<5000 receptors/cell on CD45/CD14 monocytes) algorithm; "unclassified" meant normal ferritin **and** normal HLA-DR.

**【Evidence】** JAMA 2025, doi:10.1001/jama.2025.24175 (verified via PubMed/insideprecisionmedicine): of 672 screened, 53% were "unclassified," 42% met criteria (MALS 7% = 48; sepsis-induced immunoparalysis 34% = 228). Classification required ferritin ≤4420 ng/mL **and** <5000 HLA-DR receptors on CD45/CD14 monocytes for the immunoparalysis arm; unclassified = normal ferritin AND normal HLA-DR. The manuscript's other ImmunoSep claims are faithful: primary endpoint (SOFA decrease ≥1.4 by day 9) met in 35.1% vs 17.9% (P = 0.002), and in the immunoparalysis subgroup 32.1% vs 18.0% (P = 0.02); 28-day mortality 43.5% (precision) vs 49.7% (placebo), P = 0.34 (no benefit); "hemorrhage in the recombinant human interferon gamma group" / bleeding more frequent with IFN-γ (verified). Only the *attribution* of the 53% to mHLA-DR alone is imprecise.

**【Why it matters】** The 53% figure is used to support the manuscript's central argument that transcriptomic endotypes are superior to mHLA-DR stratification. If the unclassifiability is really a property of a hard binary dual-biomarker algorithm (with a specific <5000 cutoff) rather than mHLA-DR deficiency per se, the argument is over-stated and a reviewer (or the ImmunoSep authors) could rightly object.

**【Specific fix】** Replace:
> "53% of screened patients were unclassifiable by the monocyte HLA-DR (mHLA-DR) criterion (the canonical immunoparalysis biomarker [35]), underscoring the value of transcriptomic endotypes such as Mars1."
with:
> "In ImmunoSep, 53% of screened patients were unclassified by a dual ferritin-and-mHLA-DR algorithm (mHLA-DR cutoff <5000 receptors/cell on CD45/CD14 monocytes; unclassified = normal ferritin AND normal HLA-DR), underscoring that binary single-biomarker stratification leaves many patients unassigned and motivating richer transcriptomic endotypes such as Mars1. mHLA-DR remains the validated clinical anchor for immunoparalysis [35]."

---

### A1.6 — 28-day mortality is a reasonable but biologically imperfect endpoint for immunoparalysis; the mHLA-DR endotyping argument is over-stated

**【Problem】** Using 28-day mortality as the sole prognostic endpoint under-captures immunoparalysis biology (which drives *late* deaths and secondary/ICU-acquired infections beyond 28 days), and the claim that transcriptomic endotypes supersede mHLA-DR is stronger than the evidence supports.

**【Evidence】** Manuscript §3.4, §3.10 and Limitations #8 all anchor on 28-day mortality; the MR primary outcome is "sepsis with death within 28 days" (ieu-b-5086). Limitation #8 concedes 90-day mortality and other endpoints were unavailable. Immunoparalysis is mechanistically linked to late mortality and secondary infection (Boomer 2011, ref 2; Hotchkiss 2013, ref 17 — both cited). The mHLA-DR-low endotyping argument leans on the ImmunoSep 53% (see A1.5).

**【Why it matters】** Internal coherence (signature, external validation, and MR all use 28-day) is good, but a domain reviewer should note that the *construct validity* of 28-day death for an immunoparalysis signal is limited: immunoparalysis manifests as recurrent/secondary infection and late death, often beyond day 28. The MR "sepsis 28-day death" UK Biobank phenotype may also mix early hyperinflammatory and late immunoparalytic deaths, diluting any true signal. The mHLA-DR-vs-transcriptome argument should be framed as *complementary*, not superior.

**【Specific fix】** In Discussion/Limitations, add:
> "Because immunoparalysis primarily drives late mortality and secondary infection, 28-day death is a conservative endpoint for the Mars1 program; validation against 90-day mortality and ICU-acquired-infection/Secondary Infection-free survival would strengthen the construct. Continuous mHLA-DR trajectories, not only the binary <5000 cutoff used in ImmunoSep, remain the clinical gold standard for immunoparalysis and should be viewed as complementary to transcriptomic endotypes."

---

### A1.7 — Missing must-cite literature on (i) mHLA-DR-guided therapy, (ii) checkpoint blockade in sepsis, and (iii) non-MARS sepsis endotype frameworks

**【Problem】** The citation base is solid on MARS (Scicluna, Davenport) and on individual cytokines, but omits the canonical mHLA-DR biomarker/guided-therapy literature, the sepsis checkpoint-blockade trial already in the reference list (Hotchkiss 2019) is never discussed, and broader sepsis endotype frameworks beyond MARS are only superficially covered.

**【Evidence】** Reference list: mHLA-DR is represented only by Joshi 2023 (ref 35). Foundational mHLA-DR work (Monneret et al. on HLA-DR as diagnosis/prognosis of sepsis immunosuppression; the established <8000 AB/cell or <5000 receptors/cell cutoffs; prospective GM-CSF trials guided by mHLA-DR, e.g., the controlled trials showing restored monocyte HLA-DR and fewer infections) is absent. Reference [34] Hotchkiss 2019 (nivolumab phase 1b) is listed but never engaged in the repositioning text (see A1.2). Other sepsis endotype frameworks cited only by Seymour 2019 (ref 33, clinical phenotypes); missing are the transcriptomic "sepsis response signature" (SRS1/SRS2; Wong/Stortz), the molecular degree of pathogenesis score (MDPS; Sweeney), more recent immunoparalysis-specific endotypes (e.g., Moreno-Bautista / pediatric sepsis endotypes), and the interferon endotype work (e.g., Shakoory/ESCI). Wider immunostimulant RCTs beyond Döcke 1997 and Meisel 2009 (e.g., recent GM-CSF and IFN-γ sepsis trials, and the BCG trained-immunity sepsis trials) are likewise thin.

**【Why it matters】** A domain reviewer expects the immunoparalysis biomarker canon and the competing endotype frameworks to be cited; their absence makes the "Mars1 is the immunosuppressed endotype" claim look孤立 (isolated) and weakens the "transcriptomic endotypes beat mHLA-DR" argument, which needs the mHLA-DR-guided-therapy literature as counterweight.

**【Specific fix】** Add a paragraph in Introduction/Discussion citing: (a) mHLA-DR as the canonical immunoparalysis biomarker and mHLA-DR-guided GM-CSF trials; (b) Hotchkiss 2019 (already in refs) discussed in the context of checkpoint blockade; (c) at least two non-MARS endotype frameworks (SRS and MDPS, plus a recent immunoparalysis endotype study) to situate Mars1; (d) the broader immunostimulant RCT landscape (recent GM-CSF/IFN-γ/BCG trials) so the drug shortlist is placed in context.

---

### A1.8 — Drug clinical characterisations of IL-7 / GM-CSF / IFN-γ are accurate; minor over-statement on GM-CSF "restored monocyte HLA-DR"

**【Problem】** The three cytokine citations are correctly identified and characterised, but the GM-CSF claim "restored monocyte HLA-DR" is presented as established whereas Meisel 2009 is a single small (n≈30) double-blind RCT and the broader meta-analysis the manuscript itself cites (Bo et al., ref 30) found *no* mortality benefit for G-CSF/GM-CSF — a tension that should be stated alongside the mechanism claim.

**【Evidence】** Manuscript line 144–145: "IL-7 restored lymphocytes in septic shock (Francois et al. [11]), GM-CSF restored monocyte HLA-DR (Meisel et al. [12]) … IFN-γ … canonical MHC-II inducer with limited sepsis-specific signals (Döcke et al. [13])." All three papers are real and correctly described (Francois JCI Insight 2018 IRIS-7; Meisel AJRCCM 2009; Döcke Nat Med 1997). Manuscript line 145 also cites Bo et al. (ref 30) meta-analysis finding no mortality benefit for G-CSF/GM-CSF — yet the GM-CSF mechanism claim is stated without this caveat in the same breath. `03_results/08b_clinical_translation.csv` correctly tags GM-CSF as "RCTs show restored monocyte HLA-DR & cytokine production" but also notes "Edema; mild ARDS risk; leukocytosis" toxicity.

**【Why it matters】** For a clinician reader, "GM-CSF restored monocyte HLA-DR" reads as a proven clinical benefit; the honest position is that monocyte HLA-DR recovery is demonstrated but *mortality* benefit is unproven (the manuscript's own cited meta-analysis agrees). Stating this avoids over-selling the repositioning shortlist.

**【Specific fix】** Amend to:
> "GM-CSF restored monocyte HLA-DR and cytokine production in a randomised trial (Meisel et al., 2009, ref 12), though a meta-analysis of colony-stimulating factors in sepsis found no mortality benefit (Bo et al., ref 30), tempering enthusiasm for GM-CSF as a mortality-reducing immunorestorative."

---

## § Stands up (things I suspected but found correct)

1. **Mars1 immunosuppressed framing is accurate.** I expected possible over-statement, but S01 confirms 23/25 consensus immune genes directionally down, 22 FDR-significant, 21 both down-and-significant (verified by counting all 26 rows of `S01_immunoparalysis_direction.csv`); HLA-class-II/AP genes (HLA-DRB1 −0.89, CD74 −0.76, HLA-DQA1 −0.53, HLA-DRA −0.47) and monocytic genes (CD14 −0.77, FCGR3A −0.61) are all down with adj.P in the 1e-15–1e-7 range — exactly the published Mars1 picture (Scicluna 2017, Davenport 2016).

2. **HAVCR2 is genuinely DOWN in the data (not a typo).** Given canonical TIM-3 exhaustion biology, I initially suspected a sign error. `S01` line 6 verifies logFC = −0.3488, adj.P = 2.838e-13, `Mars1_down`. The signal is real; the issue is *interpretation* (A1.1), not data integrity.

3. **External-validation magnitude is honestly scoped.** I expected spin ("novel superior signature"). Instead the manuscript reports AUC 0.638 (95% CI 0.532–0.748) and explicitly states it is *comparable to, not better than*, the IRG benchmark (recomputed 0.604; Peng 0.619), and that the learned L1 weights did not transport (0.585). The 12 numbered limitations are unusually candid (e.g., selection-chain FWER uncontrolled, MR selection-on-outcome circularity, single-direction L1000 proxy, glucocorticoid positive-control caveat). This is genuine methodological honesty.

4. **Drug citations are real and correctly characterised.** Francois IRIS-7 (JCI Insight 2018), Meisel GM-CSF (AJRCCM 2009), Döcke IFN-γ (Nat Med 1997) all verified as real papers matching the described findings. The IL-7/GM-CSF "most direct RCT signal" ranking in `08b_clinical_translation.csv` is appropriately graded (Phase I/II vs mechanism-only).

5. **ImmunoSep specifics are faithful (except A1.5 attribution).** Independent verification of JAMA 2025 doi:10.1001/jama.2025.24175 confirms: SOFA improvement in the IFN-γ/immunoparalysis arm (primary 35.1% vs 17.9%, P = 0.002; immunoparalysis subgroup 32.1% vs 18.0%, P = 0.02), *no* 28-day mortality benefit (43.5% vs 49.7%, P = 0.34), and *more* haemorrhagic events in the IFN-γ group. The manuscript reports all three correctly.

6. **Five hubs are internally consistent.** `S05_hub_genes.csv` shows all six genes `True` for lasso/rf/univariate; `S08` concordance values (IL-7 0.80, GM-CSF 0.667, IFN-γ 0.571, azithromycin 0.667, lenalidomide 0.40, thymosin 0.40, BCG 0.20) exactly match Table 2 in §3.7. No fabrication of hub/concordance numbers.

---

## § Questions for the authors

1. **HAVCR2 biology:** Given TIM-3 is canonically an *up*-regulated exhaustion marker, what is your preferred biological explanation for its *down*-regulation in Mars1? Did your cell-type deconvolution (you have `07_hub_celltype.csv` / `07_axis_celltype.csv`) show HAVCR2 tracking monocyte/DC loss rather than a T-cell signal? If so, should HAVCR2 be re-labelled an APC-compartment marker rather than an exhaustion hub?

2. **Checkpoint blockade:** PDCD1 is significantly up-regulated in Mars1 (S01). Why, then, exclude anti–PD-1/PD-L1 (and CTLA-4) from serious consideration? The Hotchkiss 2019 nivolumab phase 1b trial is in your references but undiscussed. Was the exclusion a deliberate biological decision or an oversight?

3. **Mars1 label validity:** Did you confirm that your `mars_endotype` labels in GSE65682 reproduce the *published* Mars1 signature (gene-set/leading-edge overlap)? Endotype labels have occasionally been re-ordered across MARS derivation vs validation cohorts.

4. **39% mortality source:** Please cite the exact Scicluna 2017 table/figure for the 39% Mars1 28-day mortality.

5. **Two concordance tables:** `08_candidates_drugs.csv` (rescue_fraction: IL-7 0.80, GM-CSF 0.667, IFN-γ 0.571) and `08b_clinical_translation.csv` (rescue_fraction_directional: IL-7 1.0, GM-CSF 0.833, IFN-γ 0.714) report different values, and S08b's IL-7 = 1.0 is inconsistent even with its own 4/5 rescue. Which metric populates Table 2, and how are the two reconciled?

6. **FIS1 magnitude:** The +1.26 logFC for FIS1 is stated repeatedly but I could not verify it from the files I was asked to read (`S05` lists only the consensus flags, not logFC). Please confirm the source file/row.

---

## § What I actually checked

**Files read in full:** `manuscript.md`; `03_results/S01_immunoparalysis_direction.csv` (26 data rows); `03_results/S05_hub_genes.csv` (6 genes); `03_results/S02_immunoparalysis_score.csv` (802 rows); `03_results/08_candidates_drugs.csv`; `03_results/08b_clinical_translation.csv`; `03_results/11_validation_design.md`.

**Values verified by direct recomputation from S01:**
- Count of `Mars1_down` = 23 of 25 (PDCD1 and LAG3 are the 2 `Mars1_up`). ✓ matches manuscript "23/25 … directionally down."
- FDR-significant (adj.P < 0.05) = 22 of 25; both-down-and-significant = 21 (22 sig minus PDCD1-up). ✓ matches "22 reached FDR<0.05 … 21 both."
- HAVCR2: logFC −0.3488, adj.P 2.838e-13 → DOWN. ✓ matches text Δ −0.35 / 2.8e-13.
- CD74: −0.7578 / 2.081e-15; CD14: −0.7657 / 0.0; FCGR3A: −0.6097 / 9.052e-11; HLA-DRB1: −0.8925 / 1.066e-15; HLA-DQA1: −0.5301 / 5.439e-09; HLA-DRA: −0.4689 / 3.772e-07. ✓ all match Table 1 / §3.1.
- PDCD1: +0.1619 / 2.995e-10 → UP (significant). ✓ matches "PDCD1 was up-regulated (Δ=+0.16, adj.P=3.0e-10)."
- LAG3: +0.0351 / 0.552 → UP, not significant. ✓ matches "LAG3 directionally up but not FDR-significant."
- CTLA4: −0.0904 / 0.0343 → DOWN (sub-threshold). ✓
- `S05`: all six genes `True` for lasso/rf/univariate. ✓
- `S08` vs Table 2 concordance values identical. ✓

**Discrepancies / things I could not clear:**
- `08b_clinical_translation.csv` uses a *different* concordance metric (`rescue_fraction_directional`: IL-7 1.0, GM-CSF 0.833, IFN-γ 0.714) that conflicts with `S08` (0.80 / 0.667 / 0.571) and is internally inconsistent (IL-7 lists 4/5 rescued yet scores 1.0). Not resolved from provided files — see Question 5.
- ImmunoSep "53% unclassifiable by mHLA-DR" is imprecise: the 53% reflects a dual ferritin + mHLA-DR algorithm (see A1.5). Verified the rest of the ImmunoSep claims against the primary JAMA record (SOFA, mortality, hemorrhage all correct).
- Could **not** verify from the provided files: FIS1 logFC +1.26 (stated consistently but not in the files I read); the 39% Mars1 mortality figure (not in provided files); IRIS-7/Meisel/Döcke specifics (verified via domain knowledge +, for ImmunoSep, live PubMed/JAMA retrieval on 2026-09-27).
- I did **not** independently recompute the Mars1 immune-score median (−0.792) or the Mars1-vs-Mars2 non-significance (P = 0.47); the `S02` values fall within the stated full-cohort range (−3.65 to 3.86) and the file structure is consistent, but the medians themselves were not re-derived.

**Verdict:** Biologically sound core; one misleading exhaustion-axis claim (A1.1) and one inaccurate citation attribution (A1.5) should be corrected, and the checkpoint-blockade logic (A1.2) and literature gaps (A1.7) should be addressed. With those fixes the manuscript is suitable for the domain layer.
