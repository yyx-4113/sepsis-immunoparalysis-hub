# A1 — Domain / Biology Review (Round-22, independent)

**Independence attestation:** I did not read any file under `06_review/` (including `round21_v1.22.0/`), any author rebuttal/response letter, or git history for prior rounds; this verdict is based solely on `05_reports/manuscript.md` (v1.23.1) plus `03_results/*.csv`, `02_scripts/python/*.py`, and the cited reference landing pages.

---

## 2. Verdict: **MINOR**

The biology lane is, on the whole, **accurate, internally consistent, and unusually honestly hedged**. The central questions assigned to this lane — (a) the FIS1 "mitochondrial-fission protein / erythroid-module gene" framing, (b) the 30-gene immune-risk signature characterization, and (c) the drug-repositioning claims — all withstand scrutiny against the source data. I found **no factual error or internal contradiction** in the biology. The issues below are minor (wording/precision) rather than blocking. The drug claims in particular are exemplary in restraint: L1000 is correctly framed as *descriptive only* throughout, and the prednisone-positive-control caveat is used to *withdraw* support rather than inflate it.

---

## 3. Findings

### [Tier 2] FIS1 "mitochondrial-fission protein" label is literally correct but should be explicitly disarmed
- **Citation:** `manuscript.md:101` (§3.3), `manuscript.md:178` (Conclusion); also Abstract `manuscript.md:14`.
- **What the manuscript says:** FIS1 is repeatedly introduced as "a mitochondrial-fission protein (Yoon et al. [22])" and "a mitochondrial-fission protein up-regulated in Mars1 (logFC +1.26)".
- **Problem:** The Yoon 2003 citation ([22]) is real and apt — FIS1/hFis1 is indeed a mitochondrial fission protein. But a reader scanning the abstract/Conclusion may infer FIS1's Mars1-upregulation signals *altered mitochondrial fission in immune cells*. FIS1 is a near-ubiquitous mitochondrial housekeeping protein; its Mars1-up is a co-expression bystander of the erythroid/heme program (module 2011), not evidence of immune-cell mitophagy. The manuscript's §3.3 does reach the correct erythroid/reticulocyte reading, but the "mitochondrial-fission protein" tag appears *before* that reading in every section and is never explicitly disarmed.
- **Concrete fix:** In the Abstract and Conclusion, append one clause, e.g. "—a ubiquitously expressed mitochondrial housekeeping protein whose Mars1-upregulation is read as a co-expression bystander of the erythroid/heme program rather than an immune mitochondrial-fission signal." This preserves the accurate label while pre-empting misreading. (Verified: FIS1 logFC=1.2614, t=17.157 in `S01_mars1_deg.csv`; module 2011 = 166 genes incl. GATA1/KLF1/ALAS2/FECH/EPB49/PINK1/BNIP3L/FUNDC2 — all erythroid/reticulocyte-mitophagy genes, `S03_modules.csv`.)

### [Tier 2] §3.3 "immune-annotated" description of the ML consensus is slightly inaccurate for FIS1
- **Citation:** `manuscript.md:101` ("the tri-method ML consensus (which selects on 28-day-survival-associated, **immune-annotated genes**) rather than by the co-expression network alone").
- **What the manuscript says:** Implies the tri-method consensus selects immune-annotated genes.
- **Problem:** FIS1 is explicitly *non-immune* yet passed all three selectors (LASSO/RF/univariate = True for FIS1 in `S05_hub_genes.csv`), i.e. it was carried by the consensus despite not being immune-annotated. The "immune-annotated" qualifier is therefore imprecise and sits awkwardly next to the same sentence calling FIS1 "an erythroid-module gene co-selected with the immune hubs."
- **Concrete fix:** Reword to "the tri-method ML consensus (which, in the sparse regime, also admits top-degree-centrality non-immune genes such as FIS1) rather than by the co-expression network alone." This matches §2.5's "expanded to the top-20 degree-centrality genes when sparse" and the `S05_hub_genes.csv` evidence.

### [Tier 3] "rather than a mitophagy- or oxidative-stress-driven immune mechanism" is self-undermining
- **Citation:** `manuscript.md:101`.
- **What the manuscript says:** FIS1 up-regulation is "most likely reflecting a reticulocyte/erythroid-precursor shift in whole blood rather than a mitophagy- or oxidative-stress-driven immune mechanism."
- **Problem:** FIS1's only known molecular function *is* mitochondrial fission/mitophagy, and module 2011 explicitly contains the reticulocyte-mitophagy genes PINK1, BNIP3L, FUNDC2. So FIS1 tracking erythroid reticulocytes is *because* of its mitophagy role, not in spite of it. The parenthetical reads as if mitophagy were an alternative hypothesis when it is actually the mechanistic bridge supporting the erythroid reading.
- **Concrete fix:** Change to "…rather than a mitophagy signal originating in immune cells — its mitophagy role instead supports, rather than contradicts, the erythroid/reticulocyte interpretation."

### [Tier 3] "antigen-presentation/monocytic core + neutrophilic/acute-phase arm" — verify the uncategorized genes are not mislabeled
- **Citation:** `manuscript.md:104` (§3.4).
- **What the manuscript says:** The signature is dominated by antigen-presentation/monocytic/T-cell genes plus a neutrophilic/acute-phase arm (ELANE, MPO, S100A8).
- **Check (passed):** `S06_signature_genes.csv` confirms the 30 genes; ELANE (r=+0.170), MPO (+0.152), S100A8 (+0.091) are the only three *positively* correlated with death; all HLA/monocytic/T-cell genes are negative. The characterization is biologically coherent and accurate. The remaining genes (CCL5, MYD88, NFKB1, TNF, CR1, SPI1, IRF1, IRF7) are left uncategorized — acceptable, but note they are all negative and mostly myeloid/inflammatory, so the "antigen-presentation/monocytic core" label is if anything *under*-stated, not overstated. No fix required; informational only.

### [Tier 3] Drug candidates correctly framed as hypothesis-generating — no overstatement found
- **Citation:** `manuscript.md:114-137` (§3.7–3.9), `manuscript.md:149` (Discussion), `manuscript.md:178` (Conclusion).
- **Assessment (positive):** The repositioning evidence is consistently and correctly bounded. Table 3 concordance fractions are explicitly *not* a ranking (all ≤ the 0.84 background; binomial P ≥ 0.82 for all seven). L1000 is declared "descriptive only" because prednisone (an immunosuppressant) ranks 3.2nd percentile — a genuine, well-used negative-control argument. The conclusion's "because the same axis ranks prednisone in the 3.2nd percentile, that ranking is descriptive only and not supportive evidence" is the correct inference. No drug is claimed to "reverse" Mars1 on the basis of the L1000 evidence. This lane found **no overstated drug claim**. The only caveat worth a sentence: the manuscript states the two small molecules "show directional-but-modest LINCS L1000 rescue" — "rescue" here is the single-direction Mars1-down proxy explicitly acknowledged in §3.9/§5(10), so the word is fine, but it is already correctly qualified as "directional-but-modest" and "descriptive only." No change needed.

---

## 4. Cross-validation note (3 numbers recomputed/verified from source)

1. **FIS1 Mars1 logFC +1.26 / t +17.2** — recomputed from `03_results/S01_mars1_deg.csv`: logFC = 1.2614, t = 17.157. **MATCH** (manuscript rounding correct).
2. **23/25 immune genes down; 22 significant; 21 both down+significant** — recomputed from `03_results/S01_immunoparalysis_direction.csv` (25 genes; PDCD1 + LAG3 up → 23 down; adj.P<0.05 in 22 rows; of those 22, PDCD1 is the sole up gene → 21 down+significant). **MATCH**.
3. **FIS1 ∈ erythroid module 2011 (166 genes), separated from the 5 immune hubs** — verified in `03_results/S03_modules.csv`: FIS1=2011; hubs in 2833/998/2834/307/3466 (exactly as stated); module 2011 size = 166; FIS1 degree-centrality rank = 12 (degree 64.26, `S03_hub_degree.csv`), matching "ranked 12th". **MATCH**. (Also confirmed the neutrophilic arm ELANE/MPO/S100A8 are the only positively death-correlated signature genes — supports §3.4.)

**Reference spot-checks (real & apt):** Ref [22] Yoon et al. *Mol. Cell. Biol.* 2003 (FIS1/hFis1 mitochondrial fission) — real and apt. Ref [32] Giamarellos-Bourboulis et al. "Precision Immunotherapy to Improve Sepsis Outcomes: The ImmunoSep Randomized Clinical Trial," *JAMA*, published online 2025-12-08 — confirmed real, authored by the stated group, describes the IFN-γ (immunoparalysis arm) / anakinra (MALS arm) RCT; the manuscript's use of it as a *caution* (no mortality benefit, more hemorrhagic events, ~53% unclassifiable by ferritin+mHLA-DR) is appropriate. Ref [5] Scicluna et al. *Lancet Respir. Med.* 2017 (MARS endotype derivation, 39% Mars1 mortality) — real and apt. No fabricated/irrelevant citations detected in this lane.

---

## 5. One-line integrator summary
A1 finds the biology lane **accurate and internally consistent** — the FIS1 erythroid-co-expression framing, the 30-gene signature's antigen-presentation/neutrophilic characterization, and the drug-repositioning "descriptive-only" restraint all verify against source data with **no Tier-0 errors**; only three minor wording/clarity fixes (Tier 2–3) are recommended, so the manuscript is **acceptable for biology after MINOR revisions**.
