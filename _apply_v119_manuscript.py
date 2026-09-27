import io, sys

P = r"D:/2026.9/极速交付9月会员日优惠套路/05_多组学+虚拟敲除药物发现/方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位/05_reports/manuscript.md"
src = open(P, encoding="utf-8").read()

reps = [
 # Abstract MR sentence (B2-1 + B2-8/9 + B2-10)
 ("no significant inverse-variance-weighted estimate on primary 28-day death (all OR 0.92–1.12, P ≥ 0.23); one sensitivity test (CD14 MR-Egger, OR 0.91, P = 0.049) was nominally significant and the single family-significant result (CD74 critical care, OR 2.19) ran opposite to the expression model.",
  "no significant inverse-variance-weighted estimate on primary 28-day death (all OR 0.92–1.12, P ≥ 0.24). The only nominally significant estimate was CD14 MR-Egger (OR 0.91, P = 0.049), uncorroborated by inverse-variance weighting or the weighted median and not surviving the pre-specified 15-test family correction (minimum q = 0.81). A reversed-direction CD74 critical-care signal (inverse-variance-weighted OR 2.22, P = 0.13 on the t(2) distribution) was observed but was not nominally significant and rested on only three instruments."),

 # §2.5 F3/F4
 ("expanded to the top-50 degree-centrality ∩ DEG genes when sparse)",
  "expanded to the top-20 degree-centrality genes when sparse"),
 ("Genes recovered by ≥2 methods formed the hub.",
  "Genes recovered by all three selectors formed the primary hub; when fewer than five genes passed all three, a frequency-based fallback (genes selected by ≥2 of the three methods) was used."),

 # §2.9 B2-2 pre-specification + B4-4 bootstrap/two-sided
 ("A locked-L1-weight application was added as a sensitivity analysis.",
  "A locked-L1-weight application was added as a sensitivity analysis. The equal-weight oriented sum was declared the primary external metric before the external AUC was computed, because it carries no cohort-specific weights and is therefore the portable component by construction; the locked-L1 result is reported alongside it as the like-for-like comparison to the within-cohort cross-validated AUC. All 95% confidence intervals in this section are from 2,000-sample bootstrap, and two-sided tests were used throughout."),

 # §2.10 B2-9 t-dist + m6 concordance rule
 ("Because exposure and outcome share a reference build, no liftover was required.",
  "Because exposure and outcome share a reference build, no liftover was required. All Mendelian-randomisation P-values are two-sided and computed on t-distributions — inverse-variance weighting and the weighted median on df = n_instruments − 1, MR-Egger slope and intercept on df = n_instruments − 2 — because the normal approximation is anti-conservative with 3–8 instruments; a result is reported as 'protective-concordant' for a Mars1-down gene only when all three point estimates are below 1.0, and this rule is sensitive near the null and stated for transparency only."),

 # §3.1 M1 opening
 ("Relative to all other endotypes, Mars1 showed **3,597 DEGs at |logFC|≥0.3 (FDR<0.05)** [`03_results/S01_mars1_deg.csv`].",
  "Mars1 was contrasted against every remaining sample in GSE65682 that is not Mars1 (n = 670), so the reference group necessarily comprises 347 Mars2/3/4 patients, 281 septic patients with no assigned endotype and the 42 healthy gastrointestinal-surgery controls; the contrast is therefore described throughout as 'Mars1 vs Other', not 'vs all other endotypes'. Because this reference group contains non-septic subjects, a sensitivity contrast restricted to the other three assigned endotypes (n = 347) was also computed (Supplementary Table S01b). Of 25 consensus immune genes, **23 were directionally down-regulated (Mars1_down) and 22 reached FDR<0.05 significance (this broader count includes the up-regulated exhaustion marker PDCD1, so 21 genes were both down-regulated and significant)**, an enrichment concentrated in antigen-presentation and monocytic genes (Table 1)."),

 # §3.1 M1 + m1 end-of-section
 ("This up-regulation is consistent with, but does not by itself establish, T-cell exhaustion in Mars1 and was not part of the original Mars1 definition of Scicluna et al. [5]; it is reported here as a hypothesis requiring single-cell confirmation.",
  "This up-regulation is consistent with, but does not by itself establish, T-cell exhaustion in Mars1 and was not part of the original Mars1 definition of Scicluna et al. [5]; it is reported here as a hypothesis requiring single-cell confirmation. Because these are bulk whole-blood measurements, every direction reported here is subject to the same limitation: a shift in the proportions of monocytes, lymphocytes and granulocytes, or the appearance of immature myeloid and erythroid precursors, will move all transcripts from one compartment coherently and cannot be separated from per-cell regulation; we therefore do not read any individual gene — including HAVCR2/TIM-3 and including the five hubs — as evidence of reduced per-cell expression, and the monocyte HLA-DR literature, which is protein-level and flow-cytometric, remains the independent corroboration for the monocytic arm. In the endotype-only sensitivity contrast (Mars1 vs Mars2/3/4; Supplementary Table S01b), the myeloid/monocytic component is unaffected (CD14 Δ = −0.77, FCGR3A −0.56, CD74 −0.49, HLA-DRB1 −0.59, HAVCR2 −0.39; all retain |Δ| ≥ 0.3 and FDR < 0.05), whereas the T-cell component attenuates by 60–100% (e.g. IL7R −0.60 → −0.20, CD3D −0.44 → −0.15, GZMK −0.31 → −0.07; CTLA4 and CD8B change sign) and a further three genes, including the hub HLA-DQA1 (−0.53 → −0.24), fall below the |logFC| ≥ 0.3 threshold. The endotype-specific immunosuppression described here is therefore myeloid-dominated; T-cell-marker changes in the primary contrast are confounded by sepsis-versus-control status and are not presented as part of the endotype program. PDCD1 up-regulation is strengthened in the endotype-only contrast (Δ = +0.21)."),

 # §3.2 m7 range
 ("(median −0.79 in Mars1; the full-cohort range across all endotypes was −3.65 to 3.86)",
  "(median −0.79 in Mars1; the score ranged from −3.65 to 3.86 across all 802 profiled samples, of which 323 carry no MARS assignment — the range across assigned endotypes alone was −3.65 to 2.95)"),

 # §3.2 m4 Table 2 ref + m2 Mars1 34.1%
 ("[*Fig. S01*].",
  "[*Fig. S01*]. The per-endotype medians and pairwise comparisons are summarised in Table 2. In this re-analysis Mars1 carried a 28-day mortality of 34.1% (45/132) versus 19.9% (69/347) for Mars2–4 combined (odds ratio 2.08); the corresponding odds are lower than the 39% reported in the original MARS derivation [5], plausibly reflecting re-processing on GPL13667 rather than the original platform and the inclusion here of unassigned patients in the comparison group. The endotype label itself is therefore a weak mortality classifier (AUC 0.578), and the prognostic signal used in §3.4–3.5 comes from the continuous signature, not from endotype membership."),

 # §3.3 M3 FIS1 parenthetical
 ("and one co-expression-linked gene, FIS1 (the degree-centrality screen pointed elsewhere — see the next sentence)",
  "and one non-immune, erythroid/heme-module gene, FIS1 (which entered the candidate pool through the top-20 degree-centrality branch of §2.5, where it ranked 12th, rather than through the immune-annotated branch)"),

 # §3.3 M3 module paragraph
 ("Five of the six are antigen-presentation / monocytic / exhaustion-axis genes and one, FIS1, is a mitochondrial-fission protein absent from the consensus immune gene set (S04); the co-expression set therefore comprises five immune genes plus one mitochondrial-fission gene, parsimoniously recapitulating the Mars1 program while flagging FIS1 as the single non-immune member; it is up-regulated in Mars1 (logFC +1.26, t = +17.2) and is most plausibly a co-expression passenger of the immune hub rather than an independent mitochondrial/oxidative-stress driver, so it is reported as a co-expression passenger / marker, not a mechanistic target.",
  "Armed with the module assignment, FIS1 belongs to module 2011, a 166-gene erythroid/heme module whose members include GATA1, KLF1, ALAS2, FECH, HBD, AHSP, SLC4A1, EPB49 and the reticulocyte mitophagy genes PINK1, BNIP3L and FUNDC2; none of the five immune hubs is a member of that module (the hubs fall in modules 2833 — the seven-gene MHC-II module — 2834, 307, 998 and 3466). FIS1 is therefore not a co-expression partner of the immune hubs. Its up-regulation in Mars1 (logFC +1.26, t = +17.2), which exceeds that of any hub gene, is most parsimoniously read as part of the same up-regulated heme/erythroid program identified above, most likely reflecting a reticulocyte/erythroid-precursor shift in whole blood rather than a mitophagy- or oxidative-stress-driven immune mechanism. FIS1 is accordingly reported as an erythroid-arm marker that is co-selected with the immune axis, is retained in MR for completeness, and is explicitly not treated as an immune hub or as a mechanistic target."),

 # §3.4 B2-2
 ("this within-cohort CV estimate (L1 model) is optimistic; the honest out-of-sample generalization is the external equal-weight AUC 0.638 (§3.5).",
  "this within-cohort CV estimate (L1 model) is optimistic; the honest out-of-sample generalization of the same locked L1 model is AUC 0.585 (95% CI 0.469–0.696), whose interval includes 0.5, whereas a model-free fixed-orientation equal-weight score on the same external cohort gave AUC 0.638 (95% CI 0.532–0.748) and is reported as the primary external metric because it carries no cohort-specific weights; the two external metrics differ by 0.053 and the like-for-like transport loss for the L1 model is 0.074 AUC units."),

 # §3.4 m3 DCA nested disclosure
 ("(NB ≈ 0.36 at 0.20, 0.28 at 0.30, 0.08 at 0.50) but converged to zero net benefit at high thresholds (≥ ~0.77), where treat-none is equivalent — so calibration (slope 0.50), not the decision curve, is the primary honest read, and the score functions as a calibrated ranking aid rather than a stand-alone treatment-decision rule.",
  "(NB ≈ 0.36 at 0.20, 0.28 at 0.30, 0.08 at 0.50); as detailed in §3.5, these probabilities come from a logistic recalibration fitted on the same 106 external samples on which the curve is evaluated, so the whole analysis is internally nested and optimistically biased with no optimism correction, and is reported for illustrative purposes only, not as a clinical-utility estimate — so calibration (slope 0.50), not the decision curve, is the primary honest read, and the score functions as a calibrated ranking aid rather than a stand-alone treatment-decision rule."),

 # §3.5 B2-4 calibration CI
 ("Calibration of the external equal-weight score showed a near-zero intercept (−0.04) but a sub-ideal slope of 0.50 (ideal = 1.0), indicating over-confident predicted probabilities;",
  "Calibration of the external equal-weight score showed a near-zero intercept (−0.04, 95% CI −0.43 to 0.35) but a sub-ideal slope of 0.50 (95% CI 0.10 to 0.91; P = 0.016 against the ideal slope of 1.0), indicating over-confident predicted probabilities whose degree of over-confidence is only weakly identified at n = 106 with 52 events;"),

 # §3.5 B2-3 + B2-5 DCA
 ("showed a positive net benefit over treat-none across the 0.10–0.75 threshold range, and exceeds the treat-all strategy from threshold ≈0.30 onward; the model's advantage over treat-all is confined to a window: net benefit is higher by only 0.01–0.09 across thresholds 0.30–0.50 and by 0.17–1.05 across 0.55–0.75, where the treat-all net benefit collapses toward −∞ as the threshold approaches 1 — an algebraic property of the treat-all strategy at this prevalence (0.49) rather than evidence of model gain. At thresholds ≥0.80 the model's own net benefit is 0.00, identical to the treat-none baseline, because no calibration-corrected predicted risk exceeds the threshold (model NB 0.00 versus treat-all −1.55 at threshold 0.80); the full per-threshold net-benefit grid is provided in `03_results/09_ext_dca_grid.csv` and the curve in Fig. S06. Because the absolute probabilities remain over-confident (slope 0.50), the DCA is read as discrimination-only support — the score ranks patients by risk — rather than as a calibrated absolute-risk benefit.",
  "showed a positive net benefit over treat-none from threshold 0.05 to 0.75 and exceeded the treat-all strategy from threshold ≈0.30 onward; the margin over treat-all was 0.01–0.09 across thresholds 0.30–0.50, 0.17–1.05 across 0.55–0.75 and 1.55–4.09 across 0.80–0.90, but the last range is vacuous because at ≥0.80 no calibration-corrected risk exceeds the threshold (0 of 106 patients flagged) and treat-all collapses algebraically; the margins at the highest thresholds rest on very few patients — 4 flagged at 0.70 and 1 at 0.75 — and are not interpretable. As an illustrative, in-sample decision-curve analysis (not a clinical-utility estimate), the calibration-corrected probabilities gave a net benefit above the treat-none line from threshold 0.05 to 0.75; because the absolute probabilities remain over-confident (slope 0.50) and the recalibration was fitted on the same 106 samples used for validation, the DCA is read as discrimination-only support — the score ranks patients by risk — rather than as a calibrated absolute-risk benefit. The full per-threshold net-benefit grid (with n_flagged, true positives and false positives) is in `03_results/09_ext_dca_grid.csv` and the curve in Fig. S06."),

 # §3.7 M2 ranking sentence
 ("IL-7 (concordance 0.80) and GM-CSF (0.67) ranked highest by mechanism, targeting the T-cell-exhaustion and monocytic arms respectively.",
  "Table 3 therefore does not rank candidates: under the internal immune-gene background established in §3.1 (21/25, 84%, of consensus immune genes are Mars1-down at FDR < 0.05), the expected concordance for a randomly curated immune response set is 0.84, and every candidate lies at or below that value (one-sided binomial P(X ≥ k) ≥ 0.82 for all seven; the two lowest are significantly below it). Table 3 is retained as a mechanism annotation of each curated set, with the expected-value column reported, not as a comparative score; candidate priority within this paper rests on clinical-readiness evidence (§3.8), not on these fractions. IL-7's four scored response genes (CD3D, CD8A, IL7R, LCK) all fall below the |logFC| ≥ 0.3 DEG threshold in the endotype-only contrast of Supplementary Table S01b, so IL-7's concordance is not maintained there."),

 # §3.7 Table 3 binomial columns
 ("| IL-7 | 0.80 | 4/5 | T-cell homeostasis (vs exhaustion) |",
  "| IL-7 | 0.80 | 4/5 (P=0.82) | T-cell homeostasis (vs exhaustion) |"),
 ("| GM-CSF | 0.67 | 4/6 | monocyte/APC activation |",
  "| GM-CSF | 0.67 | 4/6 (P=0.94) | monocyte/APC activation |"),
 ("| IFN-γ | 0.57 | 4/7 | MHC-II master inducer |",
  "| IFN-γ | 0.57 | 4/7 (P=0.99) | MHC-II master inducer |"),
 ("| Azithromycin | 0.67 | 2/3 | macrolide immunomodulation |",
  "| Azithromycin | 0.67 | 2/3 (P=0.93) | macrolide immunomodulation |"),
 ("| Lenalidomide | 0.40 | 2/5 | costim + HLA-II up |",
  "| Lenalidomide | 0.40 | 2/5 (P=1.00) | costim + HLA-II up |"),
 ("| Thymosin α1 | 0.40 | 2/5 | DC/monocyte maturation |",
  "| Thymosin α1 | 0.40 | 2/5 (P=1.00) | DC/monocyte maturation |"),
 ("| BCG | 0.20 | 1/5 | trained innate immunity |",
  "| BCG | 0.20 | 1/5 (P=1.00) | trained innate immunity |"),

 # §3.8 M5 remove BCG from list
 ("azithromycin [26], lenalidomide [27], thymosin α1 [28] and BCG [29], [30] are mechanistically plausible or regionally used with weaker dedicated sepsis trials.",
  "azithromycin [26], lenalidomide [27] and thymosin α1 [28] are mechanistically plausible or regionally used with weaker dedicated sepsis trials."),

 # §3.8 m4 Supplementary Table S2 -> S08b
 ("(to be provided as Supplementary Table S2; full: `03_results/08b_clinical_translation.csv`)",
  "(Supplementary Table S08b; full: `03_results/08b_clinical_translation.csv`)"),

 # §3.8 M4+M6 checkpoint axis
 ("Notably, the exhaustion markers PDCD1 and LAG3 are up-regulated in Mars1, whereas HAVCR2/TIM-3 is itself down-regulated (consistent with the antigen-presentation failure described in §3.1); together they frame an immune-checkpoint axis. Checkpoint-blockade agents (anti–PD-1/PD-L1, anti–CTLA-4) were nevertheless not prioritised, because releasing an already exhausted T-cell program is mechanistically contraindicated in this endotype and, in early sepsis trials, anti–PD-1 (nivolumab) showed no efficacy signal [36]. This reasoned exclusion is recorded as a deliberate scope decision rather than an oversight.",
  "Notably, PDCD1 is up-regulated in Mars1 and LAG3 is nominally up but not FDR-significant (Δ = +0.04, adj.P = 0.55), whereas HAVCR2/TIM-3 is significantly down-regulated (§3.1). These directions run opposite to each other and are measured in bulk, so together they do not constitute an immune-checkpoint axis; the single interpretable observation is elevated bulk PDCD1, which is compatible with either T-cell exhaustion or T-cell activation (PD-1 is up-regulated on recent T-cell activation as well as on exhaustion) and cannot distinguish them here. Checkpoint-blocking agents (anti–PD-1/PD-L1, anti–CTLA-4) were therefore not prioritised, but we do not regard them as mechanistically contraindicated: a randomised, placebo-controlled dose-escalation study of the anti–PD-L1 antibody BMS-936559 in participants with sepsis-associated immunosuppression (absolute lymphocyte count ≤ 1,100/µL; n = 20 treated) reported full receptor occupancy, no drug-related cytokine release, and — at the two highest doses — an apparent sustained increase in monocyte HLA-DR above 5,000 antibodies/cell persisting beyond 28 days [39]; the Phase 1b nivolumab study was a safety, tolerability, pharmacokinetic and pharmacodynamic study without an efficacy signal [36]. Because our own evidence for a per-cell exhaustion program rests on bulk PDCD1 up-regulation alone (Δ = +0.16, §3.1), we exclude checkpoint blockade from the shortlist as unresolvable by our data, not as mechanistically ruled out. This reasoned scope decision is recorded rather than an oversight."),

 # §3.8 M5 BCG sentence at end
 ("This clinical ranking is consistent with the response_gene_concordance hierarchy (IL-7 0.80 > GM-CSF 0.67 > IFN-γ 0.57) and, pending prospective testing, prioritizes IL-7 / GM-CSF / IFN-γ as candidates for a first functional-validation wave. The clinical-translation table (08b) reports a *directional* rescue fraction under a nominal down-regulation gate, which is distinct from the FDR-gated `response_gene_concordance` used in Table 3; both are descriptive and need not coincide.",
  "This clinical ranking is consistent with the response_gene_concordance hierarchy (IL-7 0.80 > GM-CSF 0.67 > IFN-γ 0.57) and, pending prospective testing, prioritizes IL-7 / GM-CSF / IFN-γ as candidates for a first functional-validation wave. The clinical-translation table (08b) reports a *directional* rescue fraction under a nominal down-regulation gate, which is distinct from the FDR-gated `response_gene_concordance` used in Table 3; both are descriptive and need not coincide. BCG is not carried as an acute rescue candidate. Its clinical signal comes from prevention trials in non-septic populations — a randomised trial in the elderly reported fewer respiratory infections with BCG versus placebo [40], whereas a randomised trial in ~2,000 elderly participants found no reduction in clinically relevant respiratory infection (subdistribution HR 1.26, 98.2% CI 0.65–2.44) [41] — its heterologous effects require months to emerge [29],[30], and it is a live attenuated vaccine with recognised risk of dissemination in immunocompromised hosts. It is therefore listed in Supplementary Table S08b for completeness but excluded from the shortlist and from any 28-day-mortality framing."),

 # §3.9 B2-6 line 140
 ("Both are directionally positive, meaning the Mars1-down axis is shifted toward expression, but the magnitude is modest and neither reaches the library's top tier.",
  "Both scores are positive but lie within the library's noise band: against the background of 20,413 compounds (mean rescue 0.006, SD 0.067) they correspond to z = +0.56 (lenalidomide) and +0.10 (azithromycin), with empirical rank P = 0.27 and 0.45, i.e. neither is distinguishable from a compound drawn at random; azithromycin sits at the library median."),

 # §3.9 B2-6 line 141
 ("The reverse-connectivity therefore supports only the direction of the small-molecule candidates, not their functional or clinical benefit; because a clinical immunosuppressant (prednisone) can score high on the same axis, the L1000 'rescue' proxy is not a validated marker of immune restoration, and functional confirmation (§3.10 / S11) remains required.",
  "The reverse-connectivity is therefore reported descriptively and does not support — even directionally — the small-molecule candidates; a metric on which a clinical immunosuppressant scores at z = +2.03 while the candidates score at z = +0.56 and +0.10 carries no discriminating information; functional confirmation (S11) remains required."),

 # §3.10 primary-outcome BH sentence
 ("Under the pre-specified full-family Benjamini–Hochberg correction (45 tests: five assessable genes × three estimators × three outcomes; FCGR3A excluded for insufficient instruments), however, this gives family *q*≈0.73 and does not cross the 0.05 threshold; the per-file `p_fdr_bh` column in `10_genetics_mr_outcome5086_28ddeath.csv` reports the narrower 15-test primary-outcome correction (0.49), shown for completeness.",
  "Under the pre-specified primary family correction (15 tests: five assessable genes × three outcomes, with inverse-variance weighting as the single primary estimator; MR-Egger and the weighted median are sensitivity analyses not counted in the family; §2.10), however, this gives minimum q = 0.81 across all 15 primary tests and does not cross the 0.05 threshold; the 45-test correction that additionally counts the two sensitivity estimators is reported in `10_mr_bh_family.csv` for completeness as a dependence-ignoring approximation."),

 # §3.10 FIS1 own death association (B2-12)
 ("FIS1 also returned a protective point estimate, but because FIS1 is *up*-regulated in Mars1 (logFC +1.26; §3.3) that direction is opposite to its own observational association; FIS1 is therefore reported as a passenger-gene observation rather than as model-concordant, and it is not counted among the concordant hubs;",
  "FIS1 also returned a protective point estimate, but FIS1 is *up*-regulated in Mars1 (logFC +1.26) and higher FIS1 expression is itself associated with worse 28-day death in the discovery cohort (OR per SD = 1.34, 95% CI 1.08–1.66, P = 0.007; §7, `S06_hub_death_association.csv`), so a protective MR estimate opposes its own observational direction; FIS1 is therefore reported as a passenger-gene observation rather than as model-concordant, and it is not counted among the concordant hubs;"),

 # §3.10 m6 concordance fragility
 ("The CD14 Egger finding therefore rests on few instruments, is not corroborated by IVW or the weighted median, and does not survive the pre-specified family-wise correction; it is reported as a suggestive signal only.",
  "The CD14 Egger finding therefore rests on few instruments, is not corroborated by IVW or the weighted median, and does not survive the pre-specified family-wise correction; it is reported as a suggestive signal only. The concordance rule is sensitive near the null: HAVCR2's MR-Egger estimate (OR 1.010, 95% CI 0.727–1.404, P = 0.95) crosses 1.0 by 1% while its IVW (0.978) and weighted median (0.960) do not, so HAVCR2 fails the criterion on numerical rather than statistical grounds; conversely no hub's estimates are distinguishable from one another, and the count of two should be read as approximate."),

 # §3.10 critical-care paragraph (B2-1 + B2-8/9)
 ("The secondary outcomes qualify the primary reading and are reported in full (Table 5). Against **sepsis susceptibility**, every hub was null (all IVW *P* ≥ 0.249). Germline expression of these genes therefore does not appear to influence *whether* a person develops sepsis, which is consistent with an effect on outcome severity rather than on incidence. Against **critical care**, CD74 returned the only estimate surviving the 45-test family correction: the weighted median (OR 2.194, p = 6.6×10⁻¹⁹, family q ≈ 3×10⁻¹⁷), corroborated by IVW (OR 2.222, 95% CI 1.175–4.200, P = 0.014) and MR-Egger (slope OR 2.222, slope P = 0.088, null intercept P = 1.00). However, this signal points in the direction opposite to the Mars1 expression model — higher genetically predicted CD74 predicts worse critical-care outcome — and rests on only three instruments plus exposure–outcome sample overlap, so it is reported as a genotype–severity association rather than a causal hub claim.",
  "The secondary outcomes qualify the primary reading and are reported in full (Table 5). Against **sepsis susceptibility**, every hub was null (all IVW *P* ≥ 0.249). Germline expression of these genes therefore does not appear to influence *whether* a person develops sepsis, which is consistent with an effect on outcome severity rather than on incidence. Against **critical care**, CD74 returned an inverse-variance-weighted OR 2.222 (95% CI 1.175–4.200, *P* = 0.13 on the t(2) distribution) in the reversed direction (higher predicted CD74 predicts worse critical-care outcome), corroborated by MR-Egger (slope OR 2.222, slope *P* = 0.088, null intercept *P* = 1.00). The weighted median also gave OR 2.194 but we do not report a *P*-value for it: with three instruments its bootstrap standard error (0.088) falls below the IVW standard error (0.325) computed from the same three variants, an ordering impossible for a median-type estimator, and no individual instrument is nominally significant (minimum *P* = 0.097). No test in the MR layer survives the pre-specified 15-test family correction (minimum q = 0.81); this CD74 critical-care signal is reported as a nominal, reversed-direction, genotype–severity association resting on three instruments and exposure–outcome overlap."),

 # §3.10 BH readout segment (first)
 ("The complete Benjamini–Hochberg readout for all 45 assessable tests — per-outcome 15-test `p_fdr_bh` and 45-test family *q* — is tabulated in `03_results/10_mr_bh_family.csv`; it shows that, after correcting the MR-Egger p-values to the t(n−2) distribution, **only one** of the 45 tests retains family *q*<0.05 — the CD74 critical-care weighted median (family *q* ≈ 3×10⁻¹⁷) — and that estimate reverses the Mars1 direction (higher predicted CD74 predicts worse critical-care outcome); the CD74 critical-care MR-Egger is family *q* = 0.79 and the CD14 28-day-death MR-Egger is family *q* = 0.73.",
  "The complete Benjamini–Hochberg readout for all 45 tests — 15-test primary-family *q* (inverse-variance weighting only) and the 45-test dependence-ignoring approximation (all three estimators) — is tabulated in `03_results/10_mr_bh_family.csv`; no test retains *q*<0.05 under either scheme after the MR-Egger p-values are corrected to the t-distribution: under the pre-specified 15-test primary family the minimum *q* is 0.81, and under the 45-test approximation the CD74 critical-care MR-Egger reaches only *q* = 0.79 (CD14 28-day-death MR-Egger *q* = 0.73)."),

 # §3.10 BH readout segment (CD74 crit panel)
 ("in mr_diag.png the CD74 critical-care panel shows the reversed-direction signal that is family-significant under the weighted median (OR 2.194), not the Egger (slope P = 0.088, family q = 0.79).",
  "in mr_diag.png the CD74 critical-care panel shows the reversed-direction signal (IVW OR 2.222, P = 0.13 on t(2); weighted median OR 2.194, P not reported)."),

 # §3.10 "45-test forest"
 ("the 45-test forest and, for the only nominally significant Egger (CD14 28-day death)",
  "the 15-test forest and, for the only nominally significant Egger (CD14 28-day death)"),

 # §4 first point (M1)
 ("First, the immunosuppressed signal is *endotype*-driven (Mars1 vs Other: 3,597 DEGs) rather than case/control status.",
  "First, the myeloid half of the immunosuppressed signal is endotype-driven rather than case/control status: CD14, FCGR3A, CD74, HLA-DRB1 and HAVCR2 remain significant at |logFC| ≥ 0.3 when Mars1 is compared only with Mars2–4 (Supplementary Table S01b), and Mars1-vs-healthy comparisons are comparatively weak (448 DEGs at the same threshold). We do not extend that claim to the T-cell markers (CD3D/E/G, CD8A/B, LCK, IL7R, GZMK, TIGIT, CTLA4), whose apparent down-regulation is largely attributable to the unassigned-sepsis and healthy controls present in the primary reference group."),

 # §4 L1 0.585 note
 ("This is not an in-sample artifact. The same fixed-orientation signature transferred to AUC 0.638 (95% CI 0.532–0.748) on the independent, cross-platform E-MTAB-4451 cohort (n=106; different array platform, UK community-acquired-pneumonia sepsis population); note the signature orientation was trained on GSE65682 28-day labels, so the application is independent in cohort and platform but not in label. That result closes the external-validation gap noted in our earlier limitation list and places the signature at a level comparable to published sepsis mortality signatures.",
  "This is not an in-sample artifact. The same fixed-orientation signature transferred to AUC 0.638 (95% CI 0.532–0.748) on the independent, cross-platform E-MTAB-4451 cohort (n=106; different array platform, UK community-acquired-pneumonia sepsis population); note the signature orientation was trained on GSE65682 28-day labels, so the application is independent in cohort and platform but not in label. The like-for-like external application of the same L1 model gave AUC 0.585 (95% CI 0.469–0.696), whose interval includes 0.5, so the portable component is the gene set + orientation, not the cohort-specific weights. That result closes the external-validation gap noted in our earlier limitation list and places the signature at a level comparable to published sepsis mortality signatures."),

 # §5 Limitation 1 SRS benchmark (M7)
 ("The within-cohort 5-fold CV AUC 0.659 is optimistic because gene selection and orientation used the same cohort's 28-day labels; the external 0.638 is the honest generalization estimate.",
  "The within-cohort 5-fold CV AUC 0.659 is optimistic because gene selection and orientation used the same cohort's 28-day labels; the external 0.638 is the honest generalization estimate. To place that figure in context we also benchmarked the locked score inside the external cohort against comparators computable from the shipped metadata: the cohort's own published sepsis-response-signature endotype (SRS group, available for all 106 profiled samples) classified 28-day mortality at AUC 0.610 (SRS1 24/37, 64.9% mortality, versus SRS2 28/69, 40.6%), and age alone classified it at AUC 0.504. The new score therefore exceeds the existing transcriptomic endotype in these same patients by ≈0.03 AUC units (locked score 0.638 vs SRS 0.610; ΔAUC +0.028, permutation P = 0.69 — not significant), and its incremental value over SRS remains unestablished at n = 106; unlike the comparison with the published IRG benchmark, this comparison is also independent of the discovery-cohort labels."),

 # §5 Limitation 2 CD14 sentence (B2-8/9 + B2-12 FIS1)
 ("CD14 was nominally significant under MR-Egger (OR 0.906, *P* = 4.9×10⁻²) but does not survive the corrected t-distribution Egger p-value or the pre-specified Benjamini–Hochberg correction across the full family of 45 tests (five genes × three estimators × three outcomes; FCGR3A excluded; family *q* = 0.73, versus the narrower per-outcome 15-test `p_fdr_bh` = 0.49 in `10_genetics_mr_outcome5086_28ddeath.csv`; the Egger intercept was non-significant, *P*=0.34, though with only six instruments this test is underpowered to detect pleiotropy), so it is reported as a suggestive signal only; **no primary IVW estimate reached significance**.",
  "CD14 was nominally significant under MR-Egger (OR 0.906, *P* = 4.9×10⁻²) but does not survive the corrected t-distribution Egger p-value or the pre-specified 15-test family correction (minimum *q* = 0.81; the 45-test approximation gives *q* = 0.73; the Egger intercept was non-significant, *P*=0.34, though with only six instruments this test is underpowered to detect pleiotropy), so it is reported as a suggestive signal only; **no primary IVW estimate reached significance**. FIS1 also gave a protective IVW estimate (OR 0.963), but higher FIS1 expression is associated with worse 28-day death in the discovery cohort (OR per SD = 1.34, 95% CI 1.08–1.66, *P* = 0.007), so the protective MR estimate opposes its observational direction and FIS1 is reported descriptively rather than as concordant."),

 # §5 Limitation 2 45-test -> 15-test primary
 ("The 45-test BH correction treats all 45 tests as independent, but each of the five genes is assessed across three estimators and three outcomes, so the family contains overlapping hypothesis structures (same gene × multiple estimators/outcomes); the correction is therefore a dependence-ignoring approximation rather than a strict independence guarantee (it does not adjust for the overlapping hypothesis structures induced by re-using the same instruments across estimators and outcomes).",
  "The pre-specified primary family is 15 tests (five assessable genes × three outcomes) with inverse-variance weighting as the single primary estimator; MR-Egger and the weighted median are sensitivity analyses and are not counted in the family. Under this correction no test reaches *q* < 0.05 (minimum *q* = 0.81). The 45-test correction that additionally counts the two sensitivity estimators as separate hypotheses is reported in `10_mr_bh_family.csv` for completeness; it treats three analyses of the same null — and, across outcomes, the same instruments — as independent, so it is a dependence-ignoring approximation and is not the basis for any claim."),

 # §5 Limitation 2 critical-care CD74 (B2-1 + B2-8/9)
 ("Against critical care, the CD74 weighted median reached family *q* ≈ 3×10⁻¹⁷ (OR 2.194, p = 6.6×10⁻¹⁹) with IVW (OR 2.222, P = 0.014) and MR-Egger (slope P = 0.088, null intercept P = 1.00) concordant; with only three instruments the Egger intercept is uninformative about pleiotropy — the only MR association surviving family correction, yet it points *opposite* to the Mars1 expression-level model (higher predicted CD74 predicts worse critical-care outcome), so we interpret it as a genotype–severity association rather than a causal repositioning target.",
  "Against critical care, CD74 gave an inverse-variance-weighted OR 2.222 (95% CI 1.175–4.200, *P* = 0.13 on the t(2) distribution) in the reversed direction (higher predicted CD74 predicts worse critical-care outcome), corroborated by MR-Egger (slope *P* = 0.088, null intercept *P* = 1.00). The weighted median also gave OR 2.194 but we do not report a *P*-value for it: with three instruments its bootstrap standard error (0.088) falls below the IVW standard error (0.325) from the same three variants, an ordering impossible for a median-type estimator, and no individual instrument is nominally significant (minimum *P* = 0.097). No test survives the pre-specified 15-test family correction (minimum *q* = 0.81); this CD74 critical-care signal is reported as a nominal, reversed-direction genotype–severity association resting on three instruments and exposure–outcome overlap, not as a causal repositioning target."),

 # Table 1 caption (B2-11)
 ("*Table 1. Consensus immune genes significantly down in Mars1 (selected).*",
  "*Table 1. Consensus immune genes significantly down-regulated in Mars1 (FDR<0.05; selected; two rows marked as failing the |logFC| ≥ 0.3 DEG rule).*"),

 # Table 1 LYZ row (B2-11)
 ("| LYZ | −0.26 | 3.6e-06 | lysozyme |",
  "| LYZ | −0.26 | 3.6e-06 | lysozyme (significant at FDR<0.05, adj.P=3.6×10⁻⁶, but below the |logFC| ≥ 0.3 DEG fold-change threshold, DEG_0.3=False) |"),

 # Table 5 CD74 crit IVW P 0.014 -> 0.13
 ("| CD74 | 1.074 (0.861–1.341), 0.53 | 1.119 (0.607–2.063), 0.72 | 2.222 (1.175–4.200), 0.014 | 0.00 / 0.22 / 0.00 |",
  "| CD74 | 1.074 (0.861–1.341), 0.53 | 1.119 (0.607–2.063), 0.72 | 2.222 (1.175–4.200), 0.13 | 0.00 / 0.22 / 0.00 |"),

 # §8 figure index relabel (B4-3) + 15-test forest
 ("**Figures (inline-captioned).** Fig. S01 (Mars1 28-d ROC), S02 (score vs endotype), S03A/B (hub genes; eigengene–trait correlation), S06A/B (CV and training ROC), S06C (decision-curve analysis), S07 (cellular context), S09 (external-cohort ROC), S10 (L1000 rescuers), and the two MR diagnostic figures — `mr_forest.png` (45-test forest) and `mr_diag.png`, a four-panel overlay comprising the CD14 28-day-death scatter with IVW/Egger fits, the CD14 Egger funnel, the CD14 leave-one-out analysis, and the CD74 critical-care scatter.",
  "**Figures (inline-captioned).** Fig. S1 (Mars1 28-d ROC), S2 (score vs endotype), S3A/B (hub genes; eigengene–trait correlation), S6A/B (CV and training ROC), S6C (decision-curve analysis), S7 (cellular context), S9 (external-cohort ROC), S10 (L1000 rescuers), and the two MR diagnostic figures — `mr_forest.png` (15-test forest) and `mr_diag.png`, a four-panel overlay comprising the CD14 28-day-death scatter with IVW/Egger fits, the CD14 Egger funnel, the CD14 leave-one-out analysis, and the CD74 critical-care scatter."),

 # Data availability v1.18.0 -> v1.19.0
 ("A citable versioned snapshot is provided as a GitHub release (tag v1.18.0); a Zenodo DOI will be minted and made public on acceptance (the current evaluated commit 1212f7b is tagged v1.16.0, and this v1.18.0 release is built on top of it).",
  "A citable versioned snapshot is provided as a GitHub release (tag v1.19.0); a Zenodo DOI will be minted and made public on acceptance (the current evaluated commit 1212f7b is tagged v1.16.0, and this v1.19.0 release is built on top of it)."),

 # Code availability v1.18.0 -> v1.19.0 + TLS note (B3-F6)
 ("Analysis code is released under the MIT licence in the versioned repository at https://github.com/yyx-4113/sepsis-immunoparalysis-hub (citable GitHub release, tag v1.18.0; CITATION.cff included).",
  "Analysis code is released under the MIT licence in the versioned repository at https://github.com/yyx-4113/sepsis-immunoparalysis-hub (citable GitHub release, tag v1.19.0; CITATION.cff included). The OpenGWAS API server certificate was expired at the time of the cited MR run, so certificate verification was disabled for that request (see `10_genetics_mr_run.py`); all MR outputs are deposited, so re-running is optional."),

 # References: add [39][40][41]
 ("38. Verbanck, M., Chen, C., Neale, B. & Do, R. Detection of widespread horizontal pleiotropy in causal relationships inferred from Mendelian randomization between complex traits and diseases. *Nat. Genet.* **50**, 693–698 (2018). doi:10.1038/s41588-018-0099-7",
  "38. Verbanck, M., Chen, C., Neale, B. & Do, R. Detection of widespread horizontal pleiotropy in causal relationships inferred from Mendelian randomization between complex traits and diseases. *Nat. Genet.* **50**, 693–698 (2018). doi:10.1038/s41588-018-0099-7\n39. Hotchkiss, R. S. et al. Immune checkpoint inhibition in sepsis: a Phase 1b randomized, placebo-controlled, single ascending dose study of anti-programmed cell death-ligand 1 antibody (BMS-936559). *Crit. Care Med.* **47**, 632–642 (2019). doi:10.1097/CCM.0000000000003685\n40. Giamarellos-Bourboulis, E. J. et al. Activate: randomized clinical trial of BCG vaccination against infection in the elderly. *Cell* **183**, 315–323 (2020). doi:10.1016/j.cell.2020.08.051\n41. Moorlag, S. J. C. F. M. et al. Efficacy of BCG vaccination against respiratory tract infections in older adults: a randomized controlled trial. *J. Infect. Dis.* **226**, 129–138 (2022). doi:10.1093/infdis/jiac182"),
]

fails = []
for old, new in reps:
    c = src.count(old)
    if c == 1:
        src = src.replace(old, new, 1)
    else:
        fails.append((c, old[:90]))

# B4-3 figure relabel: Fig. S0X -> Fig. SX (global, figures only)
before = src.count("Fig. S0")
src = src.replace("Fig. S0", "Fig. S")
after = src.count("Fig. S0")
print("Fig. S0 relabeled occurrences:", before, "-> remaining:", after)

if fails:
    print("\n*** FAILED REPLACEMENTS (count != 1) ***")
    for c, snip in fails:
        print(f"  count={c}: {snip!r}")
else:
    print("\nAll targeted replacements applied uniquely (count==1).")

open(P, "w", encoding="utf-8").write(src)
print("Wrote", P, "length", len(src))
