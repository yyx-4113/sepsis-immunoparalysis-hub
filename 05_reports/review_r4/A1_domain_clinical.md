# A1 — Domain / Clinical Biology Lens (blind)

**Mandate:** read v1.3.0 as a first submission; judge whether the biological and clinical claims hold, whether the endpoint means what the paper says, and whether must-cite literature is missing. Verify every numeric claim I can.

## Tier 1

### A1-T1. The CD74 direction reversal is the real biology — and it is buried under a false "fails correction" claim.
【Problem】 Mars1 shows CD74 *down*-regulated (antigen presentation down, §3.1: CD74 Δ=−0.76). The MR layer, however, finds that *higher genetically-predicted CD74* associates with *worse* critical-care/death outcome (§3.10 CD74 crit-care IVW OR 2.222, 95% CI 1.175–4.200; MR-Egger OR 2.222 with null intercept). This is directionally opposite to the simple immunoparalysis model, yet it is a coherent, mechanistically plausible finding (higher baseline CD74 genotype may track a hyper-inflammatory/severity program, not protection). It is the single most robust MR signal in the study, but the manuscript hides it by asserting it "fails correction (FDR≈0.21)" — which is arithmetically false (see A2/A3).
【Evidence】 §3.10 l.146–171; `10_genetics_mr_outcome4982_criticalcare.csv` CD74 MR-Egger p=6.6e-13, p_fdr_bh=4.97e-12, egger_intercept_p=0.99987; CD74 Weighted median p=0.0, p_fdr_bh=0.0.
【Why it matters】 The paper's honest contribution is NOT "MR shows nothing." It is: "MR reveals a robust, direction-surprising CD74–critical-care association that we cannot interpret as a causal protective target because it reverses the expected direction and rests on 3 instruments." Burying it under a false correction statement wastes the strongest result and invites a reviewer to expose the arithmetic error.
【Specific fix】 Replace the "fails correction / hypothesis-generating only" framing of CD74 crit-care with: "CD74 critical-care MR-Egger reached q≈5×10⁻¹² under the 45-test family with a null Egger intercept (pleiotropy-robust) and low heterogeneity (I²=0.00); because the direction is *opposite* to the Mars1 down-regulated-CD74 program and only three instruments support it, we interpret it as a robust genotype–severity association rather than a causal target for repositioning."

### A1-T2. The 28-day-death CD14 protective signal is phenotype-coherent and supports the model — keep it, but labelled suggestive.
【Problem】 Higher predicted CD14 → *lower* 28-day death (OR 0.906, P=5.1e-3, q_45=0.058) is exactly the direction the immunoparalysis model predicts (Mars1 down-regulates CD14; restoring it should protect). This is the one phenotype-coherent MR signal.
【Evidence】 §3.10 l.146; `10_genetics_mr_outcome5086_28ddeath.csv` CD14 MR-Egger p=5.1e-3.
【Why it matters】 This is the linkage between the hub genes and the mortality endpoint; it should be foregrounded as the hypothesis the functional-validation wave (S11) will test, not diluted by the false "nothing survives" claim.
【Specific fix】 State explicitly: "Of all MR signals, only the CD14 28-day-death MR-Egger (q=0.058, just above 0.05) is both phenotype-matched and direction-coherent with the immunoparalysis model; it is reported as suggestive and is the primary hypothesis for S11."

## Tier 2

### A1-T3. "rescue-able hub" over-extends the evidence.
【Problem】 Discussion l.181 closes with "the Mars1 program is anchored by a compact, prognostically informative, rescue-able hub." The hubs are *markers* of the down-regulated axis; what is "rescue-able" is the axis via drugs, not the hubs themselves.
【Evidence】 §3.9 shows only two small molecules have any connectivity evidence; the hubs are not shown to be individually rescuable.
【Why it matters】 Minor overclaim that a careful clinician-reviewer will flag.
【Specific fix】 "anchored by a compact, prognostically informative hub that defines a therapeutically addressable axis."

## Tier 3
### A1-T4. Endpoint scope (28-day mortality) is honestly scoped; no change.

## § Stands up (verified correct)
- External AUC 0.638 (95% CI 0.532–0.748) on E-MTAB-4451 matches `09_external_validation.csv` (orientedSum 0.6382, CI 0.5317–0.7475). ✓
- §3.1 down-regulation pattern (HLA-DRB1/CD74/CD14/FCGR3A down, PDCD1 up) is biologically coherent. ✓
- IRG benchmark comparison (0.604 recomputed vs 0.619 Peng) is honestly framed as descriptive. ✓

## § Questions for the authors
1. Is the CD74 Ensembl ID in §2.10 (`eqtl-a-ENSG00000203747`) correct for FCGR3A? FCGR3A is typically ENSG00000170347; please verify the eQTL record maps to the intended gene.
2. Should CD74 critical-care be promoted from "buried caveat" to a primary, direction-surprising MR result with a mechanistic paragraph?

## § What I actually checked
Files read: `manuscript.md` (full). Values recomputed/verified: external AUC & CI (CSV); CD74 crit-care MR-Egger p, p_fdr_bh, intercept_p (CSV); CD14 28d Egger p (CSV). Discrepancy: manuscript "CD74 crit-care fails correction FDR≈0.21" vs CSV p_fdr_bh 4.97e-12 — see A2.
