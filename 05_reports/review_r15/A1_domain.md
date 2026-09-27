# Round-15 Independent Blind Review — Domain (Sepsis Immunology / ICU Clinician-Scientist)

**Reviewer focus:** biological and clinical plausibility/accuracy of the immunology claims.
**Manuscript:** "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and externally evaluates a 30-gene sepsis prognostic signature" (v1.15.0).
**Reading basis:** manuscript.md, cover_letter.md, and the source CSVs listed under "What I actually checked." No prior-review or memory files were read.

---

## Headline assessment

The immunology is, on the whole, careful, internally consistent, and honestly scoped. I verified the two pivot directions that the manuscript's PD-1/TIM-3 story hinges on (PDCD1 up, HAVCR2 down) directly in the differential-expression table, confirmed all five immune hubs are Mars1-down, confirmed FIS1 is up and outside the antigen-presentation gene set, and confirmed the ImmunoSep trial is used as a *caution* rather than as support for checkpoint blockade. No biologically false claim was found. The issues below are minor, with one citation/attribution discrepancy (Mars1 28-day mortality) that is easily corrected.

---

## Issues

### ISSUE A — Mars1 "39% 28-day mortality" is not reproduced in the authors' own GSE65682 data (minor–moderate)

【Problem】 The manuscript states Mars1 "carries a 39% 28-day mortality" as an established MARS-consortium fact, but recomputing the same endpoint from the study's own GSE65682 phenotype (mars_endotype × death_28d) yields 34.1%, a ~5-point discrepancy that is left unexplained.

【Evidence】 manuscript.md §1 ("Mars1, the immunosuppressed subtype, carries a 39% 28-day mortality") citing Scicluna et al. [5]; vs my recomputation from `03_results/S02_immunoparalysis_score.csv`: Mars1 n = 132, deaths (death_28d = 1.0) = 45, survivors = 87 → 45/132 = 0.341 (34.1%). The same file reports the Mars1/Mars2/Mars3/Mars4 median immune-score values exactly as in Table in §3.2, so the endotype/death labels used here are the manuscript's own.

【Why it matters】 This is a methods-and-resources paper that is explicitly built on number-traceability. Quoting an external 39% while the identical cohort re-analysed here gives 34.1% invites a reviewer to ask whether the 39% is mis-attributed (or comes from a different denominator/definition) and undercuts the "every number traces to a source file" claim. It is not a biology error, but it is a verifiable inconsistency.

【Specific fix】 Either (i) recompute and report the value from the authors' own data — "In our re-processing of GSE65682, Mars1 (n = 132) had a 28-day mortality of 34.1% (45/132), consistent with the immunosuppressed endotype reported by Scicluna et al. (who reported ≈39% in their discovery/validation cohorts)" — or (ii) if the 39% is retained, quote it with its exact source table and denominator from Scicluna 2017 so the figure is attributable rather than asserted.

### ISSUE B — "non-immune passenger" for FIS1 slightly overstates its immunological irrelevance (minor)

【Problem】 Labeling FIS1 a "non-immune passenger" is defensible only in the narrow sense that it is absent from the curated antigen-presentation/monocytic gene set; it overstates the case that the gene is immunologically inert, because mitochondrial fission (Drp1/FIS1) actively regulates monocyte/macrophage activation, inflammasome priming, and cytokine release.

【Evidence】 `03_results/S01_mars1_deg.csv`: FIS1 logFC = +1.261, t = +17.16, up-regulated, DEG_0.3 = True; `03_results/S04_candidate_genes.csv`: FIS1 in_immune_set = False. The term "non-immune passenger" appears in the Abstract, §3.3, and §6. The manuscript does already soften this ("most plausibly a co-expression passenger… rather than an independent mitochondrial/oxidative-stress driver").

【Why it matters】 A domain reader may reasonably object that FIS1 is not "non-immune"; the absolute wording invites critique without strengthening the actual claim (which is that FIS1 is not a member of the APC/monocytic hub). It is a framing, not a factual error.

【Specific fix】 Replace "non-immune passenger" with: "a gene outside the antigen-presentation/monocytic immune set that behaves as a co-expression passenger of the immune hub (up-regulated, logFC +1.26); its upregulation most plausibly reflects co-regulated mitochondrial dynamics rather than a mechanistic immunoparalysis target, so it is reported as a marker, not a hub."

### ISSUE C — Umbrella term "immunostimulatory agents" includes azithromycin, which is predominantly anti-inflammatory (minor)

【Problem】 The abstract's lead sentence calls the shortlist "seven mechanism-anchored immunostimulatory agents," but azithromycin's immunomodulation is largely anti-inflammatory rather than stimulatory, so the umbrella term is a slight over-generalization.

【Evidence】 `03_results/08_candidates_drugs.csv` / `08b_clinical_translation.csv`: azithromycin mechanism = "macrolide immunomodulation (modest)"; the manuscript's own §3.7/Discussion list it under "macrolide immunomodulation." The remaining six candidates are genuinely immunostimulatory/restorative (IL-7, GM-CSF, IFN-γ, lenalidomide, thymosin α1, BCG-trained immunity).

【Why it matters】 Grouping a primarily anti-inflammatory macrolide with true immunostimulants could mislead a reader about the directionality of the proposed intervention; the manuscript's per-drug mechanism notes already soften this, but the abstract sentence does not.

【Specific fix】 In the abstract, replace "Seven mechanism-anchored immunostimulatory agents were prioritised" with "Seven mechanism-anchored immune-modulatory candidates were prioritised (predominantly immunostimulatory; azithromycin acts mainly via anti-inflammatory immunomodulation)."

### ISSUE D — The "not the canonical TIM-3-up exhaustion" contrast needs a sepsis-specific primary citation and a sharper APC-depletion caveat (minor)

【Problem】 The assertion that the Mars1 bulk HAVCR2-down state "distinguishes from the canonical TIM-3-up exhaustion signature" is anchored only to a general exhaustion review (Hotchkiss 2013, ref 3), not to sepsis-specific primary evidence on TIM-3/HAVCR2 dynamics; and the phrase "reduced checkpoint engagement" can be misread as applying to the whole checkpoint axis when PD-1 is in fact up-regulated.

【Evidence】 `03_results/S01_immunoparalysis_direction.csv`: HAVCR2 down (−0.349, adj.P 2.84×10⁻¹³) and PDCD1 up (+0.162, adj.P 3.00×10⁻¹⁰); manuscript §3.1/§4 frame PD-1-up as exhaustion but TIM-3-down as "reduced checkpoint engagement," citing only Hotchkiss 2013 for the sepsis exhaustion claim.

【Why it matters】 Several human-sepsis flow/single-cell studies report increased TIM-3 on T cells or monocytes in patient subsets, so the "this is not the canonical pattern" contrast reads as asserted rather than demonstrated. Moreover, because TIM-3 is expressed on APCs that are depleted in Mars1 (CD14/FCGR3A down), the bulk-down signal is most parsimoniously explained by reduced APC abundance — which the manuscript does acknowledge, but the "reduced checkpoint engagement" wording risks being read as contradicting the up-regulated PD-1 checkpoint.

【Specific fix】 Add one or two primary human-sepsis references on PD-1/PD-L1 and TIM-3/HAVCR2 dynamics (e.g., studies showing PD-1/PD-L1 and TIM-3 upregulation on T cells/monocytes in septic patients), and rephrase to: "HAVCR2/TIM-3 was down-regulated in bulk Mars1 (Δ = −0.35); because TIM-3 is also expressed on the APCs that are depleted in Mars1, this bulk signal most parsimoniously reflects reduced APC representation rather than T-cell-intrinsic TIM-3 engagement, and is distinct from the canonical co-upregulation of PD-1 and TIM-3 on exhausted T cells (note PD-1/PDCD1 is up-regulated here)."

### ISSUE E — "Immune-function score" conflates T-cell abundance with T-cell functional state (minor, clarity)

【Problem】 The composite immune-function score's "T-cell" component is driven by down-regulated T-cell genes (i.e., fewer T cells / lymphopenia), so the score indexes cellular composition as much as T-cell functional competence; the "immune-function" label could be over-read.

【Evidence】 `03_results/S01_immunoparalysis_direction.csv`: CD3D (−0.44), CD3G (−0.56), CD8A (−0.32), IL7R (−0.60), LCK (−0.64) all Mars1-down; manuscript §2.3 defines score = z(HLA-II) + z(T-cell) − z(exhaustion), and §3.2 already notes the score is "partly definitional." This is not a factual error — reduced T-cell representation is exactly the immunoparalysis phenotype — but the label invites over-interpretation as a direct measure of T-cell function.

【Why it matters】 Domain readers may mistake a lymphocyte-abundance/composition signal for a functional-competence measurement; clarifying this prevents over-claiming while preserving the (correct) observation that Mars1 shows lymphopenia + APC loss.

【Specific fix】 In §2.3/§3.2, qualify the construct as: "an immune-composition/activation score (HLA-II + T-cell-representation − exhaustion-marker signal) that indexes reduced APC and T-cell representation together with exhaustion signaling, not pure T-cell functional state."

---

## § Stands up (verified correct)

1. **PD-1 up / TIM-3 down directions are exactly as claimed.** `S01_immunoparalysis_direction.csv`: PDCD1 logFC +0.162 (adj.P 3.00×10⁻¹⁰, direction Mars1_up); HAVCR2 logFC −0.349 (adj.P 2.84×10⁻¹³, Mars1_down). The core PD-1/TIM-3 narrative is internally consistent and the bulk-tissue caveat ("cannot distinguish reduced APC abundance from lower per-cell expression") is appropriately stated.

2. **The five immune hubs are biologically coherent and all Mars1-down.** Verified logFC: CD74 −0.758, HLA-DQA1 −0.530, CD14 −0.766, FCGR3A −0.610, HAVCR2 −0.349 — a clean antigen-presentation/monocytic program, with HAVCR2/TIM-3 legitimately expressed on both APCs and T cells. This is a defensible near-replication of the established MARS Mars1 program.

3. **FIS1 is up-regulated and outside the antigen-presentation immune set.** `S01_mars1_deg.csv` FIS1 logFC +1.261, t +17.16, DEG_0.3 = True; `S04_candidate_genes.csv` in_immune_set = False. The "up-regulated co-expression passenger, not an APC/monocytic hub member" framing is supported by the data.

4. **The consensus-immune-gene direction counts are exact.** Of 25 genes: 23 directionally Mars1-down, 22 FDR-significant (adj.P<0.05), 21 both down and significant — these match the source file row-by-row, and the inclusion of PDCD1 (up but significant) in the "22 significant" count is handled correctly.

5. **Mars1 = immunosuppressed endotype framing is defensible and honestly scoped.** Scicluna 2017 (ref 5) is cited for the endotype; the manuscript repeatedly and correctly states this is a "near-replication / confirmation, not novel gene discovery," and that the honest external generalisation is the signature AUC 0.638, not the within-cohort CV. This novelty boundary is exemplary for a methods paper.

6. **ImmunoSep (ref 31) is correctly used as a caution, not as support for checkpoint blockade.** The manuscript explicitly notes SOFA improvement but no mortality benefit, more haemorrhagic events, and a large (53%) unclassifiable fraction under the dual ferritin/mHLA-DR algorithm, and uses it to temper the repositioning axis. The nivolumab reference (ref 35, Hotchkiss 2019) is correctly described as a Phase 1b safety/PK study not powered for efficacy, and the authors deliberately avoid checkpoint inhibitors.

7. **Drug anchors are accurately described.** IL-7 → IRIS-7 RCT (François 2018, JCI Insight, lymphocyte restoration in septic shock); GM-CSF → Meisel 2009 (monocyte HLA-DR restoration); IFN-γ → Döcke 1997 (Nat Med monocyte deactivation) and approved for chronic granulomatous disease — all stated correctly, with the opposing G-CSF/GM-CSF meta-analysis (Bo 2011) also noted.

---

## § Questions for the authors

1. On the Mars1 28-day mortality: which Scicluna 2017 table/denominator yields 39%? Our recomputation from your own GSE65682 labels is 34.1% (45/132) — do the endotype labels or death definitions differ from the original consortium assignment in a way that explains the gap?
2. For the HAVCR2-down / PDCD1-up dissociation: have you considered reporting the per-cell interpretation explicitly as "APC-depletion-driven TIM-3 signal" and citing sepsis-specific TIM-3 primary data? Would you agree the "reduced checkpoint engagement" wording should be scoped to TIM-3 only?
3. The immune-function score mixes HLA-II (APC), T-cell-abundance, and an exhaustion term. Did you test whether the score's prognostic signal survives when the T-cell-abundance component is removed, to separate composition from exhaustion? (Not required for acceptance, but would strengthen §3.2.)
4. BCG and lenalidomide rest on trained-immunity / IMiD mechanism with no sepsis RCT; the manuscript already flags this as hypothesis-generating — do you have a plan to down-weight them in any prospective ranker, or is the flat shortlist intentional for hypothesis generation?

---

## § What I actually checked

**Files read:** `05_reports/manuscript.md`, `05_reports/cover_letter.md`, `03_results/S01_immunoparalysis_direction.csv`, `03_results/S01_mars1_deg.csv` (FIS1 row), `03_results/S04_candidate_genes.csv`, `03_results/S05_hub_genes.csv`, `03_results/08_candidates_drugs.csv`, `03_results/08b_clinical_translation.csv`, `03_results/09_external_validation.csv`, `03_results/09_ext_calibration_dca.csv`, `03_results/09_ext_dca_grid.csv`, `03_results/S02_immunoparalysis_score.csv`.

**Values recomputed / verified against the manuscript:**
- PDCD1 logFC +0.162, adj.P 3.00×10⁻¹⁰ (up) — matches §3.1.
- HAVCR2 logFC −0.349, adj.P 2.84×10⁻¹³ (down) — matches §3.1.
- CD74 −0.758, HLA-DQA1 −0.530, CD14 −0.766, FCGR3A −0.610 — all down, match §3.1/Table 1.
- FIS1 logFC +1.261, t +17.16, up — matches §3.3 ("logFC +1.26, t = +17.2").
- 25-gene direction counts: 23 down / 22 significant / 21 down-and-significant — match §3.1.
- External AUC: orientedSum 0.6382, CI 0.5317–0.7475; locked-L1 0.5848; IRG3 proxy 0.5288; n=106, 52 deaths, HLA-DQA1 missing — match §3.5/Abstract.
- Calibration: intercept −0.0382, slope 0.5028, no CI claimed — match §3.5 ("−0.04 / 0.50").
- DCA grid: at threshold 0.30 model NB 0.2844 vs treat-all 0.2722 (model just exceeds); at 0.80 model NB 0.00 vs treat-all −1.5472 (diverge) — match the brief's "diverge, not converge" claim.
- Mars1 28-day mortality recomputed from S02: 45 deaths / 132 = 34.1% (manuscript cites 39% from Scicluna — discrepancy flagged as ISSUE A).

**Discrepancies found:** only the Mars1 mortality figure (ISSUE A). All other checked numbers were exact or within rounding.

**Not independently verifiable here (flagged, not asserted wrong):** the precise ImmunoSep trial sub-numbers (53% unclassifiable; "more haemorrhagic events") and the exact Scicluna 39% denominator — these are external citations; the cautious *framing* of ImmunoSep is correct regardless, but the authors should confirm the exact percentages against the published tables.

---

## VERDICT: Minor

Justification: the core sepsis-immunology claims (Mars1 immunosuppressed endotype, the five-hub APC/monocytic program, the PD-1-up/TIM-3-down dissociation with its bulk-tissue caveat, FIS1 as an up-regulated non-hub passenger, and the cautious use of ImmunoSep as a warning) are accurate, internally consistent, and directly verified in the source tables; no biologically false claim was found. The required changes are minor — correct one external mortality attribution, soften two umbrella/wording phrases ("non-immune," "immunostimulatory"), and add a sepsis-specific primary citation plus a sharper APC-depletion caveat for the TIM-3 contrast.
