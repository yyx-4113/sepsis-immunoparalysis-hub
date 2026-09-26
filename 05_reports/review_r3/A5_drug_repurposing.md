# A5 — Pharmacoinformatics / LINCS L1000 Drug-Repurposing Review (Round 3, v1.2.0)

**Independence note:** Fresh first-submission read. No prior `REVIEW_*.md` / `review*/` consulted. Numbers verified from `03_results/*.csv` and `02_scripts/python/S08_l1000_connectivity.py`.

## Findings

### T2-1 (Tier 2) — wtcs and rescue are mathematically identical; reporting both is redundant
- **【Problem】** `wtcs = (Σ−n/2)/√n` equals `rescue × √22` (n=22). They carry identical information; presenting both as if distinct slightly inflates analytical richness.
- **【Evidence】** `S08_l1000_candidate_scores.csv`: azithromycin rescue 0.0133, wtcs 0.0626 (0.0133×√22=0.0624); lenalidomide rescue 0.0439, wtcs 0.2058 (0.0439×√22=0.2059). Source code `S08_l1000_connectivity.py` line ~91: `rescue = mean_pct.mean() - 0.5`, `wtcs = (sum - n*0.5)/sqrt(n)` → wtcs = rescue×√n.
- **【Why it matters】** Not an error, but a clarity/economy issue; reviewers may ask why two "metrics" are shown.
- **【Specific fix】** Declare one primary (e.g., rescue) and note wtcs is its z-rescaling for iLINCS comparability — or drop wtcs.

### T3-1 (Tier 3) — "Background well-centered (53.6% > 0)" is slightly skewed, not perfectly centered
- **【Problem】】** A perfectly centered metric would have ~50% of compounds > 0; 53.6% implies a mild positive skew or a small positive center.
- **【Evidence】** `manuscript.md:135` ("mean 0.006, median 0.006; 53.6% of compounds > 0"). Source background distribution not re-exported here, but the 53.6% figure is internally reported.
- **【Why it matters】** "Well-centered" overstates symmetry; the metric is mildly asymmetric. Minor.
- **【Specific fix】** Soften to "approximately centered (median 0.006; 53.6% of compounds > 0)."

## § Stands up (verified correct)
- **Dual-direction honestly stated as NOT implemented** (l.135): "the intended dual-direction requirement that PDCD1 and LAG3 also be down-regulated was not implemented… all 22 genes are aggregated with the same sign." Cross-checked against `S08_l1000_connectivity.py` — the query loads only the 22-gene down-set and aggregates with one sign; PDCD1/LAG3 are in the set but never sign-flipped. **Correct and commendably honest.** ✓
- **3 excluded genes** (HAVCR2, FCGR3A, TIGIT) consistent with `mars1_down_l1000_idx.json` (22 genes) vs the 25 consensus immune genes. ✓
- **IFN-γ 5/5 AP genes** confirmed: rescue_genes = HLA-DRA;HLA-DRB1;HLA-DQA1;HLA-DQB1;CD74 (5 AP genes) in `08_candidates_drugs.csv`. ✓
- **Glucocorticoid high-rescue caveat** (prednisone rescue 0.136, dexamethasone 0.032) correctly used to show positive score ≠ functional restoration (l.139). ✓
- **BRD- semantics** correctly stated as Broad anonymized IDs, not a BET-inhibitor class (l.137). ✓
- **2/7 connectivity-scored** honestly stated; the 5 immuno-biologics lack an unbiased `trt_cp` and rest on mechanism annotation (l.137). ✓
- **response_gene_concordance** honestly framed as curated response-gene overlap, NOT direct-target overlap (§2.8, §5 #9). ✓

## § Questions for the authors
- Could the dual-direction be actually implemented (flip PDCD1/LAG3 sign) as a sensitivity analysis, to show the single-direction proxy is not materially biased by the up-markers?

## § What I actually checked
- `manuscript.md` §2.8/§3.7/§3.9; `S08_l1000_candidate_scores.csv`; `01_data/LINCS/mars1_down_l1000_idx.json` (22 genes incl. PDCD1, LAG3); `02_scripts/python/S08_l1000_connectivity.py` (sign aggregation confirmed).
- Recomputed wtcs = rescue×√22 for both candidates — **matches** source wtcs within rounding.
- No factual error found in the LINCS section; the only issues are redundancy (T2-1) and a wording nuance (T3-1).
