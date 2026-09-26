# A5 — Drug-repositioning / LINCS lens

I reviewed the repositioning pipeline (§2.8, §3.7–3.9) and the L1000 connectivity as a first submission. The method-positive gate and glucocorticoid caveat are genuinely strong; the main issue is the "rescue" label for an axis that also rewards exhaustion-marker up-regulation.

## Findings

### Tier 2 — A5-1: L1000 "rescue" label is conceptually muddled
【Problem】 The reverse-connectivity score is called a "rescue" of the Mars1-down axis, but the 22-gene query includes PDCD1 and LAG3 (Mars1-UP exhaustion markers), so up-regulating them is scored as rescue even though exhaustion-marker up-regulation is pathologic in Mars1.
【Evidence】 §3.9 (line 135): the metric aggregates all 22 genes with the same sign; "it rewards up-regulation of PDCD1/LAG3 as well and must be read as a single-direction Mars1-down rescue proxy." The paper discloses this, but the *label* "rescue" applied to the merged axis is still misleading.
【Why it matters】 A pharmacologist reviewer will object that up-regulating TIM-3/PD-1-pathway exhaustion markers is the opposite of immune restoration; the disclosed caveat does not fully neutralise the misleading frame.
【Specific fix】 Relabel the composite metric as "Mars1-down-axis reversal proxy (single-direction; co-rewards exhaustion-marker up-regulation)" and reserve "rescue" for the antigen-presentation/monocytic subset explicitly. The conclusion (line 207) "directional-but-modest LINCS L1000 rescue" should say "directional-but-modest LINCS L1000 reversal of the Mars1-down axis."

### Tier 2 — A5-2: response_gene_concordance ranking is descriptive — already hedged (minor)
【Problem】 The candidate hierarchy (IL-7 1.00 > GM-CSF 0.83 > IFN-γ 0.71) rests on 3–7-gene curated sets with no permutation null.
【Evidence】 §2.8 (line 64) and §3.7 (line 117) state this is descriptive and hypothesis-generating.
【Why it matters】 Already honestly scoped; no change required. Listed for completeness.
【Specific fix】 None.

### Tier 3 — A5-3: Five biologics lack L1000 perturbation (stated)
【Problem】 IL-7/GM-CSF/IFN-γ/thymosin/BCG have no `trt_cp` in L1000; their evidence is mechanism-anchored only.
【Evidence】 §3.9 (line 137).
【Why it matters】 Honestly stated; acceptable. A prospective S11 assay is the right remedy (already specified).
【Specific fix】 None.

## § Stands up (verified)
- IFN-γ positive control: 5/5 antigen-presentation genes rescued (`08_positive_control_check.csv` referenced; §3.7 line 117) — a real, honest method gate.
- Glucocorticoid positive-control caveat (prednisone rescue 0.136, dexamethasone 0.032) — correctly interpreted as "necessary not sufficient" (§3.9 line 139). This is a methodological strength.
- wtcs = rescue × √22 redundancy disclosed (§3.9 line 135) — no double-counting of evidence.
- Dual-direction requirement not implemented — disclosed, not hidden (§3.9).

## § Questions for the authors
- Could the L1000 query be split into a Mars1-down (AP/monocytic) subset and a Mars1-up (exhaustion) subset, reporting two separate rescue scores? This would remove the conceptual muddle without new data.

## § What I actually checked
- Read §2.8, §3.7–3.9, §3.10 drug context.
- Cross-checked the disclosed caveats (wtcs redundancy, dual-direction not implemented, glucocorticoid control) against the text.
- Verified IFN-γ 5/5 claim is presented as a positive-control gate, not a significance claim.
