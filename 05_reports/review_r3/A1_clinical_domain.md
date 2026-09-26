# A1 — Clinical / Immunology Domain Review (Round 3, v1.2.0)

**Independence note:** Fresh first-submission read of `manuscript.md` (v1.2.0, 288 lines). I did not consult any prior `REVIEW_*.md`, `review/`, or `review_r2/` files. All numbers below were recomputed by me from `03_results/*.csv`.

## Findings

### T0-1 (P0, self-contradiction) — FIS1 is branded as an "antigen-presentation/monocytic hub gene" in the Conclusion, contradicting §3.3
- **【Problem】** The Conclusion lists FIS1 inside "antigen-presentation/monocytic hub genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, **FIS1**)," directly contradicting §3.3, which states FIS1 is "a mitochondrial-fission protein absent from the consensus immune gene set … the single non-immune member."
- **【Evidence】** `manuscript.md:207` vs `manuscript.md:103`. §3.3 literally says "the hub therefore comprises five immune genes plus one mitochondrial-fission gene." The Conclusion erases that distinction.
- **【Why it matters】** If an editor reads the Conclusion alone (common), the paper asserts a mitochondrial-fission protein is an antigen-presentation hub — a biological falsehood that undermines credibility and is a desk-reject-level internal contradiction.
- **【Specific fix】** Rewrite l.207: "The Mars1 immunosuppressed program is anchored by six hub genes — five antigen-presentation/monocytic genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) plus the mitochondrial-fission protein FIS1 — that are both prognostically informative (CV-AUC 0.659; independent external AUC 0.638) and mark a therapeutically addressable axis."

### T1-1 (Tier 1) — "Therapeutically targetable" over-claims the hub genes
- **【Problem】** The six hub genes are *down-regulated* disease markers; the pharmacologically actionable entities are the *drugs* (ranked by curated response-gene concordance, not direct targets). Calling the genes themselves "therapeutically targetable" conflates biomarker with drug target.
- **【Evidence】** `manuscript.md:15` (Abstract EN), `:179` (Discussion), `:207` (Conclusion); ZH Abstract `:25` says "兼具预后价值与**可药性**特征" ("druggable"). §2.8 itself states the metric is *not* direct-target overlap.
- **【Why it matters】** "Targetable/druggable" is a strong mechanistic claim with no direct-target evidence in this study (no DGIdb/ChEMBL pull, admitted in §5 #9). It inflates the translational claim and invites reviewer pushback.
- **【Specific fix】** Replace "therapeutically targetable" with "mark a therapeutically addressable axis" (the axis is addressable via the repositioned immune-stimulatory agents, not the genes themselves). Apply to l.15, l.179, l.207 and ZH l.25 ("可药性" → "可被治疗性干预的轴").

### T2-1 (Tier 2) — Abstract EN count omits the PDCD1-up nuance
- **【Problem】** Abstract EN l.14 states "23/25 … directionally down, 22/25 significant at FDR<0.05" without noting the 22 significant *include the up-regulated exhaustion marker PDCD1* (which §3.1 clarifies).
- **【Evidence】** `manuscript.md:14` vs `:82` (§3.1: "22 reached FDR<0.05 significance (this broader count includes the up-regulated exhaustion marker PDCD1…)").
- **【Why it matters】** A reader may infer 22 of the 23 down-genes are significant, overstating the down-regulation signal in the abstract.
- **【Specific fix】** Add to l.14: "22/25 significant at FDR<0.05 (the 22 include the up-regulated exhaustion marker PDCD1, so 21 were both down-regulated and significant)."

### T2-2 (Tier 2) — "First functional-validation wave" reads as a recommendation
- **【Problem】** §3.8 ends by "prioritizes IL-7 / GM-CSF / IFN-γ for the first functional-validation wave," phrased as a recommendation rather than a hypothesis.
- **【Evidence】** `manuscript.md:132`.
- **【Why it matters】** Minor, but the Discussion (l.183) correctly calls this "a hypothesis requiring prospective testing" — the §3.8 phrasing slightly outruns that hedge.
- **【Specific fix】** Reword to "suggests IL-7 / GM-CSF / IFN-γ as priority candidates for a first functional-validation wave, pending prospective testing."

## § Stands up (verified correct)
- Mars1 biology is coherent: 23/25 down, 22 sig, 21 both — recomputed from `S01_immunoparalysis_direction.csv` (23 Mars1_down, 22 adj.P<0.05, 21 both). ✓
- Drug shortlist is clinically plausible; IL-7 (Francois 2018) and GM-CSF (Meisel 2009) RCT signals are real; the Bo 2011 G-CSF/GM-CSF null meta is correctly cited as a counterweight (l.132). ✓
- IFN-γ positive-control logic is sound: 5/5 AP genes (HLA-DRA/DRB1/DQA1/DQB1/CD74) confirmed in `08_candidates_drugs.csv`. ✓
- Glucocorticoid high-rescue caveat (prednisone/dexamethasone) is correctly used to temper the L1000 interpretation (l.139). ✓

## § Questions for the authors
- Was FIS1 retained in the hub purely on statistical convergence, or is there a biological hypothesis for mitochondrial dynamics in immunoparalysis? (Affects how prominently it should appear.)
- Do you intend "targetable" to mean the *axis/program* (addressable by immune-stimulatory drugs) rather than the *genes*? The text currently implies the latter.

## § What I actually checked
- Read `manuscript.md` (full, 288 lines).
- Recomputed Table 1 counts from `S01_immunoparalysis_direction.csv`: 23 down / 22 FDR<0.05 / 21 both — **no discrepancy**.
- Cross-checked drug fractions in `08_candidates_drugs.csv`: IL-7 5/5, GM-CSF 5/6, IFN-γ 5/7, azith 2/3, lena 2/5, thym 2/5, BCG 1/5 — **matches manuscript**.
- Checked `08b_clinical_translation.csv` for RCT citations — present and plausible.
- Discrepancy noted: FIS1 branding (T0-1) and "targetable" framing (T1-1) are real defects.
