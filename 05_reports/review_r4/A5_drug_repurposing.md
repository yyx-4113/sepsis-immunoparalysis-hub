# A5 — Drug-Repurposing Specialist Lens (blind)

**Mandate:** judge whether the repositioning logic is sound, whether the metric means what the paper says, and whether the downstream biology claims are supported.

## Tier 2

### A5-T2-1. The L1000 dual-direction requirement is admitted as not implemented — good, but it weakens the candidate ranking more than stated.
【Problem】 §3.9 now correctly states the intended dual-direction requirement (PDCD1/LAG3 also down-regulated) was NOT implemented; all 22 genes are aggregated with the same sign, so the score rewards up-regulation of the exhaustion markers too. This is honestly disclosed. However, the text still calls lenalidomide/azithromycin "directionally positive" and a "rescue" — but because the metric cannot penalise exhaustion-marker up-regulation, "rescue of the Mars1-down axis" overstates what the single-sign score measures.
【Evidence】 §3.9 l.135 ("the intended dual-direction requirement … was not implemented … so it rewards up-regulation of PDCD1/LAG3 as well").
【Why it matters】 The admitted limitation should be reflected in the verb: the score is a "Mars1-down-axis reversal proxy," not a verified "rescue."
【Specific fix】 Consistently call it a "single-direction Mars1-down reversal proxy" in §3.9, §3.7/§3.8 context, and the Abstract/Conclusion summary.

### A5-T2-2. Glucocorticoid positive-control caveat is well handled.
【Problem】 None — the prednisone/dexamethasone high-rescue caveat (§3.9 l.139) is a genuine, honest safeguard showing a positive L1000 score is necessary but not sufficient for functional immune restoration. This is a strength.
【Specific fix】 None; consider citing it once in the Limitations to reinforce the repositioning caveat (limitation 9 already covers the metric, so no change needed).

## Tier 3

### A5-T3-1. wtcs = rescue × √22 redundancy correctly disclosed.
【Problem】 None. §3.9 explicitly states the two are algebraically identical and not independent evidence. Good.
【Specific fix】 None.

### A5-T3-2. response_gene_concordance is curated, not direct-target — correctly scoped.
【Problem】 None. §2.8 and Limitation 9 make clear the metric uses curated downstream response genes, not DGIdb/ChEMBL direct targets. No overclaim.
【Specific fix】 None.

### A5-T3-3. Clinical-translation hierarchy matches the concordance ranking.
【Problem】 None. §3.8 IL-7 (1.00) > GM-CSF (0.83) > IFN-γ (0.71) ordering is consistent with Table 2 and with the cited RCT signals. The opposing G-CSF/GM-CSF meta-analysis (Bo 2011) is correctly noted as a tempering counterpoint.
【Specific fix】 None.

## § Stands up (verified correct)
- IFN-γ 5/5 antigen-presentation rescue satisfies the method-positive gate and is a real consistency check. ✓
- L1000 candidate scores self-consistent: lenalidomide rescue 0.044 ↔ wtcs 0.21; azithromycin rescue 0.013 ↔ wtcs 0.06. ✓
- Five immunobiologic/vaccine candidates correctly flagged as lacking unbiased L1000 perturbagen. ✓

## § Questions for the authors
1. Given the dual-direction gap (A5-T2-1), would a post-hoc re-score that also down-weights PDCD1/LAG3 up-regulation materially change lenalidomide/azithromycin ranking? If cheap to compute, it would close the acknowledged gap.

## § What I actually checked
- Read `manuscript.md` §2.8, §3.7, §3.8, §3.9, Limitation 9.
- Verified L1000 score self-consistency (rescue × √22 = wtcs).
- Cross-checked Table 2 concordance ordering vs §3.8 narrative.
