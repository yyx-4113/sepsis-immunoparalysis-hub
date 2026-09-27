# A1 — Domain review (sepsis immunology / intensive‑care medicine)

**Manuscript:** `05_reports/manuscript.md` (tag v1.13.0)
**Journal target:** Scientific Reports (Nature Portfolio)
**Reviewer role:** Domain expert — sepsis immunology / intensive‑care medicine
**Independence note:** This review was written without access to any prior‑round review, response, or revision files, and without any other r13 reviewer's output. Every judgement below is anchored to a file/line I read directly or a value I recomputed.

---

## Overall assessment

The biological core of this manuscript is sound and, importantly, **well hedged**. The central claim — that the Mars1 immunosuppressed endotype is anchored by an antigen‑presentation / monocytic gene program that is coherent and externally reproducible — is supported by the differential‑expression source tables I inspected. The drug‑repositioning and Mendelian‑randomisation layers are correctly scoped as hypothesis‑generating, and the glucocorticoid positive‑control caveat is a genuine strength. However, two clinical/biological statements in the Discussion over‑read their citations: (i) the anti‑PD‑1 nivolumab trial is described as having "shown no benefit," which mischaracterises a Phase‑1b safety/pharmacokinetic study; and (ii) the down‑regulation of HAVCR2/TIM‑3 is framed as "consistent with … T‑cell exhaustion," which the direction of the data actually complicates rather than supports. Both are fixable with tighter wording. Details and evidence below.

---

## Detailed items

### Item 1 — The nivolumab "showed no benefit" statement misreads a Phase‑1b safety/PK trial

【Problem】The Discussion asserts that checkpoint blockade is avoided in the prioritization because "the anti–PD‑1 nivolumab trial showed no benefit [34]," but reference [34] (Hotchkiss et al., *Intensive Care Med.* 2019) was explicitly a Phase‑1b safety, tolerability, pharmacokinetic (PK) and pharmacodynamic (PD) study, not an efficacy trial, and it did not demonstrate "no benefit."

【Evidence】Manuscript `manuscript.md:188` ("Checkpoint‑blockade is not straightforward in sepsis immunosuppression — the anti–PD‑1 nivolumab trial showed no benefit [34]"). Reference [34] in `manuscript.md:315`: Hotchkiss, R. S. et al., *Intensive Care Med.* **45**, 1360–1371 (2019), doi:10.1007/s00134‑019‑05704‑z. The published title is itself "Immune checkpoint inhibition in sepsis: a Phase 1b randomized study to **evaluate the safety, tolerability, pharmacokinetics, and pharmacodynamics** of nivolumab." The study enrolled 31 adults (nivolumab 480 mg n=15, 960 mg n=16), with **primary endpoints = safety and PK**; both arms showed ~40% 90‑day mortality (40% and 37.5%), and the authors' conclusion was "nivolumab administration did not result in unexpected safety findings or indicate any 'cytokine storm' … Further efficacy and safety studies are warranted." There is no powered between‑group efficacy comparison and no statement of "no benefit" in the source.

【Why it matters】Characterising a safety/PK dose‑finding study as a negative efficacy trial is a factual over‑reading that a clinical reader will immediately catch. It also weakens the manuscript's own careful, otherwise commendable, calibration of evidence tiers: the same paragraph correctly calls the MR and repositioning layers hypothesis‑generating, yet here it asserts a definitive negative that the cited paper does not support. This is the single most likely point for a clinician‑reviewer to reject.

【Specific fix】Replace the sentence in `manuscript.md:188` with a wording that matches the source: *"Checkpoint blockade is not yet established for sepsis immunosuppression: the anti–PD‑1 antibody nivolumab was tested in a Phase‑1b safety, pharmacokinetic and pharmacodynamic study in septic ICU patients, where it was well tolerated, maintained >90% PD‑1 receptor occupancy and increased monocytic mHLA‑DR, but was not powered to assess clinical benefit [34]; the present prioritization therefore deliberately avoids checkpoint inhibitors pending efficacy data."* (Optionally add that no Phase‑2/3 sepsis anti–PD‑1 efficacy trial has, to the authors' knowledge, reported a mortality benefit, citing a broader basis rather than [34] alone.)

---

### Item 2 — HAVCR2/TIM‑3 down‑regulation sits uneasily with the "T‑cell exhaustion" framing

【Problem】The manuscript counts HAVCR2/TIM‑3 among the Mars1 hubs and repeatedly describes it as a "co‑inhibitory checkpoint … consistent with, but not by itself establishing, T‑cell exhaustion," yet the very same gene is **down‑regulated** in Mars1, which is mechanistically the opposite of what an exhausted‑T‑cell signature would predict for a checkpoint receptor.

【Evidence】`manuscript.md:72` and `:105` and `:182` and `:218` all describe HAVCR2 as part of the down‑regulated immunosuppressed program (Δ=−0.35, adj.P=2.8×10⁻¹³). I confirmed in `03_results/S01_immunoparalysis_direction.csv` (line 6): `HAVCR2,Mars1_down,logFC −0.3488,adj.P 2.84e‑13`. The "T‑cell exhaustion" narrative in the manuscript (`manuscript.md:72`) rests on PDCD1/**up** (line 8 of the same file: `PDCD1,Mars1_up,logFC +0.162,adj.P 3.0e‑10`) and LAG3 directionally up but **not** significant (line 26: `LAG3,Mars1_up,logFC +0.035,P 0.524,adj.P 0.552`). So the only *significant* exhaustion marker is up‑regulated, while the checkpoint the manuscript highlights as a hub is down‑regulated.

【Why it matters】A co‑inhibitory checkpoint being *down* in bulk blood is more parsimoniously explained by **immune‑cell paucity** — fewer T cells and antigen‑presenting cells — which is the canonical cellular correlate of immunoparalysis, than by T‑cell‑intrinsic exhaustion (which would be expected to *up‑regulate* TIM‑3 on the remaining T cells). The manuscript does acknowledge the bulk‑abundance ambiguity (`manuscript.md:72`), which saves it from being wrong, but the recurrent "checkpoint … consistent with T‑cell exhaustion" phrasing oversells the directional evidence. A reader could reasonably infer that TIM‑3 down‑regulation *supports* exhaustion, when the data are equivocal at best.

【Specific fix】In `manuscript.md:182` and `:105`/`72`, sharpen the causal logic: *"HAVCR2/TIM‑3, a co‑inhibitory checkpoint expressed on T cells and antigen‑presenting cells, was also down‑regulated in Mars1 (Δ=−0.35). Because a checkpoint receptor is down‑regulated here, this signal is more consistent with reduced APC/T‑cell abundance — a hallmark of immunoparalysis — than with T‑cell‑intrinsic exhaustion, which would be expected to up‑regulate TIM‑3. The only significant exhaustion marker was PDCD1 (up); LAG3 was directionally but non‑significantly up (adj.P=0.55). The T‑cell‑exhaustion signal is therefore tentative and requires single‑cell or flow‑cytometric confirmation."*

---

### Item 3 — ImmunoSep (ref [32]) framing is largely accurate; two minor attributions need tightening

【Problem】The ImmunoSep caution citation is mostly correct and well used, but (a) the SOFA benefit is attributed to "the IFN‑γ/immunoparalysis arm" whereas the published primary endpoint was reported for the combined precision‑immunotherapy group, and (b) the "53% unclassifiable" figure is approximately right but its denominator is ambiguously stated.

【Evidence】Manuscript `manuscript.md:134‑135` (§3.8): "Giamarellos‑Bourboulis et al. [32] randomised a precision‑immunotherapy strategy (recombinant IFN‑γ for the immunoparalysed arm, anakinra for the MALS arm) … reported SOFA improvement in the IFN‑γ/immunoparalysis arm but no mortality benefit and more haemorrhagic events … 53% of screened patients were unclassifiable … mHLA‑DR cutoff <5,000 receptors/cell … 43.5% vs 49.7% 28‑day mortality; P = .34." Reference [32] (`manuscript.md:313`) is real and correctly cited: *JAMA* **335**(9), 775–786 (2026), doi:10.1001/jama.2025.24175 (online 2025‑12‑08). Independent summaries confirm: Phase‑IIb, 672 screened → 281 randomised → 276 analysed; SIP = ferritin ≤4420 **and** <5000 HLA‑DR receptors/monocyte; primary endpoint SOFA improvement ≥1.4 by day 9 was 35.1% vs 17.9% (combined immunotherapy vs placebo); 28‑day mortality 43.5% vs 49.7%, P=.34; more bleeding with IFN‑γ. The 28‑day mortality, bleeding, under‑powering, and mHLA‑DR cutoff all check out exactly.

【Why it matters】The citation is used appropriately as a *caution* (axis reversal ≠ clinical benefit) and the numbers are essentially faithful, so this is not a substantive error. But attributing the SOFA benefit specifically to "the IFN‑γ/immunoparalysis arm" implies a per‑arm primary result the paper did not report (the day‑9 SOFA result was for the combined immunotherapy group). Small imprecisions like this erode trust in an otherwise careful manuscript.

【Specific fix】(a) Reword `manuscript.md:135` "SOFA improvement in the IFN‑γ/immunoparalysis arm" → "SOFA improvement in the combined precision‑immunotherapy group (driven by both arms), with the IFN‑γ/immunoparalysis stratum contributing the antigen‑presentation‑restoring signal." (b) Clarify the 53% denominator: "≈53% of screened patients were unclassifiable by the dual ferritin‑and‑mHLA‑DR algorithm (i.e., normal ferritin AND normal HLA‑DR), so only a minority qualified for the stratified immunotherapy."

---

### Item 4 — The glucocorticoid positive‑control caveat is correctly reasoned and well supported

【Problem】No problem — this is a strength, flagged here so the editors know it was checked.

【Evidence】Manuscript `manuscript.md:142` and `03_results/S08_l1000_positive_control.csv`: prednisone rescue 0.1364 (rank 651/20,413; 3.2nd percentile) scores high, whereas dexamethasone rescue 0.0315 (rank 6808; 33.4th percentile) does not. The interpretation — a positive L1000 "rescue" score is *necessary but not sufficient* for functional immune restoration because an immunosuppressant (prednisone) can transcriptionally up‑regulate parts of the antigen‑presentation set — is biologically correct and appropriately non‑overstated.

【Why it matters】This caveat is the single most important guard against over‑reading the LINCS L1000 repositioning layer, and the manuscript states it correctly. It materially strengthens the paper's credibility.

【Specific fix】None required. Optionally, note in §3.9 that the prednisone/dexamethasone discrepancy itself is informative (glucocorticoid‑inducible MHC‑II genes such as HLA‑DR are cell‑type‑ and ligand‑specific), but this is editorial, not a correction.

---

### Item 5 — The five immune hubs are genuinely Mars1‑down; FIS1 up‑regulation is verified

【Problem】No problem with the directional claim — verified.

【Evidence】Manuscript `manuscript.md:14,72,105,182,218` lists CD74, HLA‑DQA1, CD14, FCGR3A and HAVCR2 as Mars1‑down immune hubs plus FIS1 as a non‑immune up‑regulated passenger (logFC +1.26). I confirmed every value in `03_results/S01_immunoparalysis_direction.csv`: CD74 Δ=−0.758 (adj.P 2.08e‑15), HLA‑DQA1 Δ=−0.530 (5.44e‑9), CD14 Δ=−0.766 (0.0), FCGR3A Δ=−0.610 (9.05e‑11), HAVCR2 Δ=−0.349 (2.84e‑13) — all `Mars1_down`, all DEG_0.3 True. FIS1 in `03_results/S01_mars1_deg.csv` (line 3716): `logFC 1.2614, t 17.157, P 0.0, adj.P 0.0, DEG_0.3 True, DEG_1.0 True`. The consensus‑immune directionality counts also check: 23/25 directionally down and 22/25 FDR‑significant including the up‑regulated PDCD1, hence 21 both down‑and‑significant (`manuscript.md:72`; file lines 1–26 of `S01_immunoparalysis_direction.csv`).

【Why it matters】These are the biological load‑bearing claims of the paper, and they are reproducible from the deposited tables. This is what makes the confirmation credible rather than assertion.

【Specific fix】None. One minor clarification worth adding: the term "hub" is used for two distinct notions — co‑expression degree centrality (§2.4) and tri‑method ML prognostic selection (§2.5). §3.3 acknowledges HLA‑DQA1 was driven to a zero L1 coefficient and is absent from the external array (`manuscript.md:108`); stating explicitly that "hub" here means "anchors the Mars1 program and the prognostic signature collectively, not that each individually contributes to the locked external score" would pre‑empt an obvious methodological question.

---

### Item 6 — Decision‑curve "exceeds treat‑all only at ≳0.50" is imprecise versus the grid

【Problem】The Discussion states the model's net benefit "exceeds treat‑all only at thresholds ≳0.50," but the supplied DCA grid shows the model already exceeds treat‑all from ≈0.25 onward.

【Evidence】Manuscript `manuscript.md:112` and `03_results/09_ext_dca_grid.csv`: at threshold 0.25, nb_model 0.3208 vs nb_treat_all 0.2163 (model already higher); 0.30 → 0.2844 vs 0.2722; 0.20 → 0.3632 = 0.3632 (equal); 0.10–0.15 → equal to treat‑all. So the crossover from "equal" to "model better" occurs near 0.25, not 0.50. The "converging toward treat‑all near 0.80" part is correct (at 0.80 both = 0.0 because prevalence ≈0.49 caps treat‑all).

【Why it matters】This is a small quantitative slip, but DCA is a nuanced plot and imprecise threshold language can mislead clinicians about where the signature adds value. The substantive claim (positive net benefit over treat‑none; modest advantage over treat‑all) is correct.

【Specific fix】In `manuscript.md:112`, change "exceeds treat‑all only at thresholds ≳0.50" to "exceeds the treat‑all strategy from roughly the 0.25 threshold upward, while converging toward treat‑all near 0.80, reflecting the 0.49 external prevalence."

---

### Item 7 — The Mars1 ↔ 28‑day‑mortality link is cited, not re‑derived, in this cohort

【Problem】The manuscript presents Mars1 as the immunosuppressed endotype with a 39% 28‑day mortality and links the program to death, but the GSE65682 re‑analysis does not directly recompute endotype‑stratified 28‑day mortality; it only shows the immune‑score and a binary Mars1 indicator at AUC 0.578.

【Evidence】`manuscript.md:22` states Mars1 "carries a 39% 28‑day mortality" (cited to Scicluna [4], not computed here). `manuscript.md:90` and `03_results/S06_auc_compare.csv` (line 4): "Mars1 endotype" AUC for 28‑day death = 0.5782. The manuscript never reports a Mars1‑vs‑other mortality table from GSE65682 itself. The externally validated 30‑gene signature does predict 28‑day mortality (AUC 0.638, `09_external_validation.csv`), which is the real, source‑traceable mortality link.

【Why it matters】Clinically, the Mars1→mortality association is well established by the MARS consortium and citing it is legitimate for a confirmation study. But the endpoint framing would be cleaner if the manuscript stated explicitly that the *within‑cohort* mortality association is taken from the founding literature rather than re‑estimated, so readers do not assume a new mortality stratification was performed.

【Specific fix】Add one sentence in §3.2 or Limitations: *"The Mars1–28‑day‑mortality association quoted here (39%) is taken from the original MARS consortium report [4]; the present re‑analysis confirms the immunosuppressed *transcriptomic* program and its prognostic signature (AUC 0.578 binary indicator; external 0.638) but does not re‑derive endotype‑specific mortality within GSE65682."*

---

### Item 8 — "FIS1 as a non‑immune co‑expression passenger" is a reasonable interpretation, not a proven fact

【Problem】Calling FIS1 a "passenger" is supported circumstantially but is an interpretation that single‑cell data would be needed to prove; the manuscript presents it confidently.

【Evidence】`manuscript.md:106,218` and `03_results/S01_mars1_deg.csv` line 3716 (FIS1 logFC +1.26, t +17.16, strongly up). `03_results/07_hub_celltype.csv` line 2 shows FIS1's strongest module correlation is with Monocyte at **r = −0.438** (negative), consistent with a non‑immune/erythroid‑associated signal rather than an immune‑cell‑driven one; §3.3 also notes the degree‑centrality screen surfaced an erythroid/heme module (GATA1, CGB, EPB49) with FIS1 ranking 12th. So the "non‑immune passenger" reading is well motivated.

【Why it matters】The interpretation is defensible and the data point the right way, so this is not an error. But "passenger" implies a causal claim about mechanism (correlated but not driving). Stating it as "most plausibly a co‑expression passenger" (which the manuscript already does at `manuscript.md:106`) is the right level; I only caution against any stronger phrasing elsewhere.

【Specific fix】No change required; retain the "most plausibly …" hedging already present. Ensure the Abstract (`manuscript.md:14`) "non‑immune co‑expression passenger" is read alongside §3.3's caveat.

---

### Item 9 — Missing / weakly anchored citations in the immunological narrative

【Problem】A few domain claims would be stronger with more specific primary citations, and one review‑only citation is doing primary‑study work.

【Evidence】
- `manuscript.md:72`: "PD‑1/TIM‑3 co‑expression is a recognised feature of sepsis‑associated T‑cell exhaustion [17]" — [17] is Hotchkiss 2013, a *review*. A primary human study demonstrating PD‑1/TIM‑3 co‑expression on T cells in septic patients (e.g., the bodies of work by Monneret/Venet on PD‑1⁺ T cells in sepsis, or specific cytometry studies) would better support the claim. Not blocking, but should‑cite.
- `manuscript.md:72,105,182`: "HAVCR2/TIM‑3 … expressed on T cells and antigen‑presenting cells" is asserted without a citation anchoring TIM‑3 expression on human monocytes/macrophages/dendritic cells specifically. A primary reference for TIM‑3 on human APC would tighten it.
- `manuscript.md:188` checkpoint‑blockade avoidance: as Item 1 shows, [34] cannot carry "no benefit." If the authors wish to assert that checkpoint inhibitors are unproven in sepsis, the appropriate support is the absence of a positive Phase‑2/3 trial; consider citing the broader immunotherapy‑trial landscape (including the anakinra/IL‑1 and IFN‑γ experience) rather than leaning on the nivolumab Phase‑1b paper for a negative efficacy claim.

【Why it matters】Scientific Reports weighs citation accuracy; review‑only citations standing in for primary evidence, and mis‑mapped citations (Item 1), are the kind of issues that draw "must revise references" requests and, if unaddressed, reduce confidence in the clinical framing.

【Specific fix】Add 1–2 primary citations for PD‑1/TIM‑3 co‑expression on T cells in human sepsis and for TIM‑3 expression on human APCs; re‑anchor the checkpoint‑blockade sentence per Item 1's fix rather than [34] as a "no benefit" proof.

---

### Item 10 — "Immunoparalysis endotype" endpoint framing is clinically valid

【Problem】No problem — the endpoint framing is clinically sound; recorded here as verified for the editors.

【Evidence】Mars1 as the immunosuppressed (low HLA‑II / antigen‑presentation) endotype with the highest mortality is the established MARS consortium finding (Scicluna 2017 [4], Davenport 2016 [5]), correctly cited at `manuscript.md:22,184`. The manuscript's own re‑analysis confirms the *direction* of the program (Item 5) and shows the immune‑score is lowest in Mars1/Mars2 (`manuscript.md:90`, `S02_immunoparalysis_score.csv`: Mars1 median −0.792 vs Mars2 −0.752, P=0.47; vs Mars3 P=1.9e‑18; vs Mars4 P=1.3e‑3 — all match the brief's stated claims and the source table). The 30‑gene signature's honest external AUC 0.638 is modest but real and comparable to the published benchmark (Peng et al. 0.619, `S06_auc_compare.csv` line 5; IRG3 proxy 0.5288, `09_external_validation.csv`).

【Why it matters】This is the clinically meaningful backbone: the Mars1 immunoparalysis endotype is a legitimate, validated construct, and tying the signature to 28‑day mortality (the endpoint ICUs actually use) is appropriate. The modest magnitude is honestly reported.

【Specific fix】None.

---

## § Stands up (claims I suspected but found correct)

1. **The five immune hubs are genuinely Mars1‑down, and FIS1 is genuinely up‑regulated.** I expected the "hub" label to be a soft claim, but `S01_immunoparalysis_direction.csv` confirms CD74/HLA‑DQA1/CD14/FCGR3A/HAVCR2 all `Mars1_down` with strong adj.P values, and `S01_mars1_deg.csv` line 3716 gives FIS1 logFC +1.2614, t +17.16. The directional biology is reproducible, not asserted.

2. **The glucocorticoid positive‑control caveat is correct and well‑reasoned.** I wondered whether prednisone "scoring high" was a cherry‑picked positive control; `S08_l1000_positive_control.csv` shows prednisone rescue 0.1364 (rank 651, 3.2nd percentile) versus dexamethasone 0.0315 (rank 6808, 33.4th percentile), and the inference that a transcriptional rescue score is not a validated marker of immune restoration is biologically sound. This is a real strength.

3. **The external‑validation numbers are exactly as reported and honestly scoped.** `09_external_validation.csv`: oriented‑sum AUC 0.6382 (CI 0.5317–0.7475), n=106, 52 deaths; locked‑L1 AUC 0.5848; IRG3 benchmark 0.5288 — all match the manuscript text. The calibration slope 0.5028 / intercept −0.0382 (`09_ext_calibration_dca.csv`) also matches. The authors did not round‑up or hide the modest magnitude.

4. **The MR layer is honestly null and correctly family‑corrected.** I checked `10_mr_bh_family.csv` and `10_genetics_mr_outcome5086_28ddeath.csv`: all primary‑outcome IVW ORs are 0.92–1.12 with P ≥ 0.23 (e.g., CD74 1.119 P=0.72; HLA‑DQA1 0.923 P=0.26; CD14 0.927 P=0.24; HAVCR2 0.978 P=0.85; FIS1 0.963 P=0.47), and the only family‑significant result is CD74 critical‑care weighted median, which *reverses* direction and is flagged as a genotype–severity association. The Brief's claim that "no primary IVW estimate reached significance" is verified.

---

## § Questions for the authors

1. **On the nivolumab citation (Item 1):** Given that Hotchkiss 2019 was a Phase‑1b safety/PK study with both arms at ~40% mortality and no powered efficacy comparison, how would you re‑phrase the checkpoint‑blockade‑avoidance sentence so it does not imply a negative efficacy trial? Do you know of any later sepsis anti–PD‑1/PD‑L1 efficacy study that would better support "unproven"?

2. **On HAVCR2 direction (Item 2):** Since HAVCR2/TIM‑3 is *down*‑regulated in Mars1, do you agree this is more consistent with immune‑cell paucity than with T‑cell‑intrinsic exhaustion, and would you reframe the "consistent with T‑cell exhaustion" clause to foreground PDCD1 (the only significantly up‑regulated exhaustion marker)?

3. **On ImmunoSep per‑arm results (Item 3):** The day‑9 SOFA improvement (35.1% vs 17.9%) was reported for the *combined* precision‑immunotherapy group. Do you have a per‑arm (IFN‑γ/SIP vs anakinra/MALS) SOFA or 28‑day‑mortality breakdown that justifies attributing the SOFA benefit specifically to the IFN‑γ/immunoparalysis arm, or should the text be generalised?

4. **On endotype mortality (Item 7):** Did you attempt a direct Mars1‑vs‑other 28‑day‑mortality comparison within GSE65682, or is the 39% figure solely from Scicluna 2017? If computed, please report it; if not, please state so explicitly to avoid implying a new stratification.

5. **On "hub" semantics (Item 5/8):** Given HLA‑DQA1 was zeroed in the L1 fit and is absent from the external array, would you clarify that "hub" denotes program‑level anchoring rather than an individually portable external predictor?

6. **On TIM‑3/APC expression (Item 9):** Can you add a primary citation for TIM‑3 expression on human monocytes/macrophages/dendritic cells and for PD‑1/TIM‑3 co‑expression on T cells in human sepsis, to replace or supplement the review‑only [17]?

---

## § What I actually checked

**Files read (directly):**
- `05_reports/manuscript.md` — full text, all sections and references [1]–[37].
- `03_results/S01_immunoparalysis_direction.csv` — 25 consensus immune genes; verified 23/25 directionally `Mars1_down`, 22/25 FDR‑significant (incl. PDCD1 up), 21 both down‑and‑significant; confirmed CD74/HLA‑DQA1/CD14/FCGR3A/HAVCR2 down and PDCD1/LAG3 up.
- `03_results/S01_mars1_deg.csv` — confirmed FIS1 logFC +1.2614, t +17.157, P/adj.P = 0.0, DEG_0.3 & DEG_1.0 True (line 3716).
- `03_results/09_external_validation.csv` — AUC 0.6382 (CI 0.5317–0.7475), n=106, 52 deaths, locked‑L1 0.5848, IRG3 0.5288; all match text.
- `03_results/09_ext_calibration_dca.csv` — intercept −0.0382, slope 0.5028, AUC 0.6382.
- `03_results/09_ext_dca_grid.csv` — net‑benefit grid; used to check the treat‑all crossover (Item 6).
- `03_results/S08_l1000_candidate_scores.csv` — azithromycin rescue 0.0133/rank 9152; lenalidomide 0.0439/rank 5435; match text.
- `03_results/S08_l1000_positive_control.csv` — prednisone 0.1364/rank 651; dexamethasone 0.0315/rank 6808; match text.
- `03_results/08_positive_control_check.csv` — IFN‑γ rescues 4/5 antigen‑presentation genes; hub down‑regulation sanity check True.
- `03_results/S06_auc_compare.csv` — CV 0.6586, train 0.7495, Mars1 indicator 0.5782, IRG benchmark 0.619/0.648; all match.
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv` and `10_mr_bh_family.csv` — verified all primary IVW OR 0.92–1.12, P ≥ 0.23; CD74 critical‑care weighted median reverses direction; FCGR3A absent (excluded for insufficient instruments).
- `03_results/S02_immunoparalysis_score.csv` (via manuscript Table §3.2) — Mars1 −0.792, Mars2 −0.752 (P=0.47), Mars3 P=1.9e‑18, Mars4 P=1.3e‑3.
- `03_results/07_hub_celltype.csv` (line 2) — FIS1 Monocyte r = −0.438, supporting non‑immune/erythroid association.
- `05_reports/cover_letter.md` — confirmed consistent with manuscript; the nivolumab overstatement is confined to the Discussion, not the cover letter.

**External literature verification (independent of the manuscript):**
- Reference [32] Giamarellos‑Bourboulis et al., *JAMA* 2026;335(9):775–786, doi:10.1001/jama.2025.24175 — confirmed real; 672 screened → 281 randomised → 276 analysed; SIP defined by ferritin ≤4420 AND <5000 HLA‑DR receptors/monocyte; day‑9 SOFA improvement 35.1% vs 17.9% (combined group); 28‑day mortality 43.5% vs 49.7% (P=.34); more bleeding with IFN‑γ. Manuscript's numbers are faithful; minor attribution nuance in Item 3.
- Reference [34] Hotchkiss et al., *Intensive Care Med.* 2019;45(10):1360–1371, doi:10.1007/s00134‑019‑05704‑z — confirmed real bibliographic record, but confirmed it is a **Phase‑1b safety/PK/PD study** (31 patients, primary endpoints safety + PK), not an efficacy trial; conclusion calls for "further efficacy and safety studies." This substantiates Item 1.

**Discrepancies / mismatches found:**
- DCA "exceeds treat‑all only at ≳0.50" vs grid showing model > treat‑all from ≈0.25 (Item 6) — minor quantitative imprecision.
- ImmunoSep SOFA benefit attributed to "IFN‑γ/immunoparalysis arm" whereas source reports it for the combined group (Item 3a) — minor attribution.
- Nivolumab "showed no benefit" vs source being a safety/PK Phase‑1b study (Item 1) — substantive over‑reading.
- HAVCR2 down‑regulation framed as supporting T‑cell exhaustion, whereas direction is opposite to the exhaustion expectation (Item 2) — framing over‑reach, hedged but improvable.

No forbidden files (prior‑round reviews, response/revision docs, memory, other r13 reviewers) were opened.
