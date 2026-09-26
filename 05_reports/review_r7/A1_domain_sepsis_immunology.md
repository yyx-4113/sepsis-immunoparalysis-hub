# A1 — Independent peer review (Domain: sepsis immunology / immunoparalysis)

**Reviewer:** A1 (sepsis immunology / immunoparalysis domain expert)
**Manuscript:** "Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning"
**Role:** Independent first-submission reviewer of biological / clinical plausibility, endpoint validity, must-cite literature, and over-reaching clinical claims.

## Independence statement

I have **not** read any prior review round, response, or revision document for this manuscript. I read only the raw sources specified for this task:
`05_reports/manuscript.md` (full text), `03_results/S01_immunoparalysis_direction.csv`, `03_results/S01_mars1_deg.csv`, `03_results/08_candidates_drugs.csv`, `03_results/08_positive_control_check.csv`, and `02_scripts/python/check_audit_assertions.py` (read only to see what the authors claim to guard). All numeric checks below were recomputed by me from the raw CSVs; I did not take any reported figure on trust. My assessment is therefore independent of any earlier round's conclusions.

---

## Numbered issues

### Issue 1 — Internal contradiction: TIM-3 / HAVCR2 direction
**【Problem】** The Discussion (and the Abstract's biological-coherence claim) state the Mars1 program carries "an up-regulated T-cell exhaustion axis … TIM-3 up" (Discussion line 190: "antigen-presentation and monocytic genes down, TIM-3 up"). This directly contradicts the manuscript's own Results and data, where HAVCR2/TIM-3 is **down-regulated** in Mars1.
**【Evidence】** §3.1 line 82 explicitly lists "down-regulated antigen-presentation axis (including TIM-3/HAVCR2)"; Table 1 gives HAVCR2 Δ=−0.35, adj.P=2.8×10⁻¹³; `S01_immunoparalysis_direction.csv` row for HAVCR2: `logFC=−0.3488`, `adj.P.Val=2.84e-13`, `DEG_0.3=True`, `direction=Mars1_down`. The gene is unambiguously Mars1-down and FDR-significant.
**【Why it matters】** A reader trusting the Discussion would conclude TIM-3 is up-regulated in immunosuppression, which the authors' own analysis refutes. It also weakens the "directionally coherent" claim in the Abstract and Discussion, since one of the two "exhaustion" anchors is actually down.
**【Specific fix】** In Discussion line 190 and the Abstract biological-coherence sentence, delete "TIM-3 up". Replace with a coherent statement such as: "antigen-presentation/monocytic genes down (including TIM-3/HAVCR2) and PDCD1 up-regulated." Restrict the "exhaustion axis is up" claim to PDCD1 only (see Issue 2).

### Issue 2 — "Up-regulated T-cell exhaustion axis (PDCD1, LAG3)" overstates LAG3
**【Problem】** LAG3 is presented as part of an up-regulated exhaustion axis, but in the Mars1 comparison it is only nominally up and **not** FDR-significant.
**【Evidence】** `S01_immunoparalysis_direction.csv`: LAG3 `logFC=+0.035`, `adj.P.Val=0.552`, `DEG_0.3=False`, `direction=Mars1_up`. PDCD1 is genuinely up (logFC +0.162, adj.P 3.0×10⁻¹⁰, FDR-significant) but also fails the |logFC|≥0.3 DEG rule. So among the two named exhaustion markers, only PDCD1 is statistically supported, and even that is sub-threshold for the DEG rule.
**【Why it matters】** Presenting LAG3 as a confirmed up-regulated exhaustion marker overstates the exhaustion signal and is inconsistent with the conservatism the authors show elsewhere.
**【Specific fix】** State: "PDCD1 was up-regulated and FDR-significant (Δ=+0.16, adj.P=3.0×10⁻¹⁰), whereas LAG3 was nominally up but not significant (adj.P=0.55); the exhaustion-axis claim therefore rests on PDCD1 alone." Drop LAG3 from the "up-regulated exhaustion axis" phrasing in §3.1, §3.3, and the Abstract.

### Issue 3 — "Degree-centrality and the tri-method ML consensus converged on six hub genes" is contradicted in the same paragraph
**【Problem】** The opening sentence of §3.3 claims convergence between the co-expression network and the ML consensus, but the very next sentences show the co-expression degree-centrality screen surfaced an erythroid/heme module (GATA1 deg 78.4, CGB 76.1, EPB49 72.5), and that the six immune hubs were carried **only** by the tri-method ML consensus, with FIS1 ranking only 12th by degree.
**【Evidence】** §3.3 line 114: "Degree-centrality and the tri-method ML consensus converged on six hub genes …" immediately followed by "the degree-centrality screen of the top-2000 Mars1-DEGs surfaced a module dominated by erythroid / heme-biosynthesis genes … the six immune hubs were therefore carried by the tri-method ML consensus … rather than by the co-expression network alone."
**【Why it matters】** The two methods did not converge; the co-expression network pointed elsewhere. The "converged" wording implies independent corroboration that did not occur, inflating confidence in the hub set.
**【Specific fix】** Rephrase to: "The tri-method ML consensus identified six hub genes. The independent degree-centrality screen instead highlighted an erythroid/heme module (GATA1, CGB, EPB49), indicating the immune hubs are ML-selected on survival-associated, immune-annotated genes rather than co-expression-derived; FIS1 appeared at rank 12 by degree and was retained via the ML consensus."

### Issue 4 — Hub-gene "prognostic informativeness" overstated at the gene level
**【Problem】** The Abstract and Conclusion call the hub genes "prognostically informative," but the locked L1 signature model assigned zero weight to 7 of 29 signature genes, including hubs CD74 and HLA-DRB1 (§3.4). The mortality AUC is therefore a gene-set/orientation property, not evidence that each hub gene individually carries prognostic signal.
**【Evidence】** §3.4 line 117: "the locked L1 model shows it assigned zero weight to 7 of the 29 signature genes (CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B)." Abstract line 14 / Conclusion line 218: hubs "both prognostically informative … and mark a therapeutically addressable axis."
**【Why it matters】** An endotype-association (hubs mark Mars1) is being merged with a mortality-prognosis claim. The hubs are markers of the immunosuppressed endotype; their individual causal/contributory role in 28-day death is not established by the AUC.
**【Specific fix】** Soften to: "the hub genes mark the immunosuppressed endotype, and the aggregated 30-gene Mars1-oriented axis is prognostically informative (external AUC 0.638); hub genes were not individually required for the signature AUC (several received zero L1 weight)." Remove "prognostically informative" as a standalone attribution to the hub genes.

### Issue 5 — FIS1 dismissed as a "pure passenger" may be biologically premature
**【Problem】** FIS1 (mitochondrial fission receptor for Drp1) is the single largest hub effect (logFC +1.26, t=+17.2) yet is reported only as a non-immune co-expression passenger with no mechanistic role. Mitochondrial dynamics are mechanistically linked to monocyte metabolic reprogramming, Drp1-mediated fission, and suppression of trained-immunity / myeloid function — i.e., plausibly central to immunoparalysis, not incidental.
**【Evidence】** §3.3 line 114: "it is up-regulated in Mars1 (logFC +1.26 …) and is most plausibly a co-expression passenger … so it is reported as a marker, not a mechanistic target." (Domain reasoning: monocyte immunoparalysis involves oxidative-phosphorylation suppression and mitochondrial remodeling; see e.g. Cheng et al., Nature 2016 on metabolic reprogramming in sepsis; the authors cite none of this.)
**【Why it matters】** Dismissing the strongest single hub effect as a passenger forecloses a biologically credible axis (mitochondrial fission as a driver or amplifier of monocyte paralysis). The caution is defensible, but the text should not imply FIS1 is irrelevant.
**【Specific fix】** Add one sentence: "Although annotated as non-immune, the magnitude of FIS1 up-regulation and its link to Drp1-mediated mitochondrial fission raise the possibility that monocyte mitochondrial remodeling contributes to the paralytic phenotype; FIS1 warrants functional probing rather than dismissal as a passive passenger." Keep the honest "reported as marker" qualifier.

### Issue 6 — 28-day mortality is a partially mismatched anchor endpoint for an immunoparalysis signature
**【Problem】** The whole prognostic and MR program is anchored to 28-day death. Immunoparalysis manifests as late mortality and secondary infection (typically 60–90 days), whereas 28-day death also captures early hyperinflammatory deaths, diluting the immunosuppression signal. This likely contributes to the null MR on the primary outcome.
**【Evidence】** Abstract line 12 ("28-day mortality, yet it lacks tractable hub biomarkers"); §2.10 primary outcome `ieu-b-5086` (28-day death). Limitation 8 acknowledges the endpoint is limited to 28-day but does not note the directional attenuation. The canonical mHLA-DR / IFN-γ immunotherapy literature (Monneret & Venet; Döcke 1997) ties restoration to infection-related and longer-term outcomes, not purely 28-day.
**【Why it matters】** Choosing 28-day death as the "phenotype-matched primary outcome" is defensible as a proxy, but the mismatch with immunoparalysis biology is itself a plausible explanation for the weak/non-significant MR — a point the Discussion should own rather than defer to "underpowering" alone.
**【Specific fix】** In Discussion §4 and Limitation 8, add: "immunoparalysis is more strongly indexed by 60–90-day mortality and secondary-infection endpoints; the 28-day choice captures early hyperinflammatory deaths and plausibly attenuates both the signature and the MR." Cite Monneret/Venet mHLA-DR work to ground the immunoparalysis-endotype claim beyond the MARS paper.

### Issue 7 — Stratified-treatment language for IL-7/GM-CSF/IFN-γ reads as a recommendation without subgroup evidence
**【Problem】** Most of the repositioning framing is appropriately cautious ("hypothesis-generating", "not a treatment recommendation"), but §4 line 194 states "Mars1 patients with dominant APC suppression may benefit most from IFN-γ/GM-CSF, whereas those with T-cell exhaustion may prefer IL-7" — treatment-assignment language unsupported by any patient-level subgroup or interaction analysis.
**【Evidence】** §4 line 194. Contrast with the otherwise careful §3.8 / §5 framing.
**【Why it matters】** "May benefit most / may prefer" implies a validated stratification that the in-silico pipeline cannot support; it could be read as a clinical recommendation.
**【Specific fix】** Recast as a future-hypothesis: "these axes suggest a testable stratification hypothesis — APC-dominant Mars1 for IFN-γ/GM-CSF, exhaustion-dominant for IL-7 — to be examined in prospective subgroup analyses; it is not a treatment recommendation."

---

## § Stands up (things I suspected were wrong but found correct)

1. **The 23/25 / 22/25 / 21 headline numbers are exactly correct.** I recomputed from `S01_immunoparalysis_direction.csv` (25 rows): 23 Mars1_down, 2 Mars1_up; 22 FDR<0.05-significant; 21 both down and significant. The three non-significant genes are CD8B (adj.P 0.077), GZMA (0.110), LAG3 (0.552) — exactly consistent with the "22 includes PDCD1 (up) and 21 both down+sig" decomposition. No rounding or definition error.

2. **FIS1 is the sole up-regulated hub; the other five are genuinely down.** From `S01_mars1_deg.csv`: CD14 −0.766, CD74 −0.758, FCGR3A −0.610, HAVCR2 −0.349, HLA-DQA1 −0.530 (all down), FIS1 +1.261 (up). The authors' "5 down + FIS1 up" claim and their honest "passenger/marker, not mechanistic target" framing are data-supported.

3. **The repositioning metric's distinction (curated response-gene concordance vs direct-target overlap) is honestly maintained throughout.** §2.8, §3.7, §3.9 and Limitation 9 all state the metric is *not* a direct pharmacologic-target overlap and that the method-positive gate is non-independent. There is no conflation of "curated response-gene concordance" with "direct target overlap" — the distinction the brief asked me to police is preserved.

4. **The IFN-γ positive-control gate is honestly reported as 4/5, not 5/5.** `08_positive_control_check.csv` confirms "救回 4/5 抗原呈递基因: [HLA-DRA, HLA-DRB1, HLA-DQA1, CD74]." The exclusion of HLA-DQB1 because it fails the |logFC|≥0.3 rule (`DEG_0.3=False` in the direction CSV, adj.P 0.017 but logFC −0.203) is correctly handled and disclosed in §3.7.

5. **Every `rescue_genes` entry is a genuine Mars1-down DEG_0.3 gene — no leakage of FDR-insignificant or up-regulated genes.** I verified all 23 listed rescue genes across IL-7, GM-CSF, IFN-γ, Azithromycin, Lenalidomide, Thymosin α1, BCG: each has `DEG_0.3=True` and `logFC<0` in `S01_mars1_deg.csv`. The concordance fractions are internally consistent with the DEG rule used everywhere else.

6. **The Giamarellos-Bourboulis (JAMA 2025, ImmunoSep) citation is present [32] and its findings are represented honestly.** The manuscript reports SOFA improvement, no mortality benefit, more hemorrhagic events, and 53% unclassifiable by the mHLA-DR criterion — a fair summary that is used to *support* (not distort) the endotyping argument. The authors do not over-claim from it.

7. **The glucocorticoid positive-control caveat (§3.9) is a strong, honest guard against over-reading transcriptional rescue.** Prednisone/dexamethasone scoring high despite being immunosuppressive is surfaced as evidence that a positive L1000 rescue score is necessary-but-not-sufficient for functional immune restoration. This is exactly the kind of self-skepticism a domain reviewer wants.

---

## § Questions for the authors

1. **Hub-selection provenance for FIS1.** `S05_hub_genes.csv` is not in my read set. Can you show that FIS1 was recovered by ≥2 of the three ML selectors (LASSO/RF/univariate) on 28-day-survival-associated genes, rather than merely present in the candidate set? Which of the three methods selected it, and was its selection driven by survival association or co-expression?
2. **Endpoint choice for MR.** Given that immunoparalysis is better indexed by 60–90-day / secondary-infection outcomes, why was 28-day death fixed as the primary MR outcome, and did you run (or could you report) a sensitivity MR on a longer or infection-related sepsis phenotype to test whether the null is endpoint-driven?
3. **HAVCR2 re-classification.** Since HAVCR2/TIM-3 is Mars1-down (FDR-significant), do you intend to re-label it as antigen-presentation/monocytic rather than "exhaustion-axis," and to drop the "TIM-3 up" Discussion claim (Issue 1)?
4. **FIS1 biology.** Will you add the mitochondrial-dynamics caveat (Issue 5) or keep FIS1 strictly as a non-mechanistic marker? If the latter, please justify why a logFC +1.26, t=+17.2 signal should be treated as passive.
5. **Prognosis vs endotype.** The hubs mark Mars1; the AUC is a set-level property (several hubs get zero L1 weight). Do you agree the "prognostically informative" attribution should be scoped to the axis, not the individual hub genes (Issue 4)?

---

## § What I actually checked

**Files read (raw sources only):**
- `05_reports/manuscript.md` — full text (Abstract EN/ZH, Intro, Methods §2.1–2.11, Results §3.1–3.10, Discussion §4, Limitations §5, Conclusion §6, §7 provenance, References).
- `03_results/S01_immunoparalysis_direction.csv` — 25 consensus immune genes (direction, logFC, adj.P.Val, DEG_0.3).
- `03_results/S01_mars1_deg.csv` — full Mars1 DEG table (1 MB); queried for the 6 hubs and all rescue genes.
- `03_results/08_candidates_drugs.csv` — 7 candidates, `rescue_genes`, `n_target_genes`, `n_rescue_mars1down`, `rescue_fraction`.
- `03_results/08_positive_control_check.csv` — IFN-γ 4/5 gate, hub-KO, candidate recovery.
- `02_scripts/python/check_audit_assertions.py` — read to see what the authors claim to guard (treated as claims, not verified truth).

**Commands / code run** (managed Python `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe` with pandas):
- Check 1 — loaded `S01_immunoparalysis_direction.csv`; counted `direction=="Mars1_down"` (23), `direction=="Mars1_up"` (2), `adj.P.Val<0.05` (22), and `(Mars1_down & FDR<0.05)` (21). Listed non-significant genes (CD8B 0.0767, GZMA 0.110, LAG3 0.552) and up genes (PDCD1, LAG3).
- Check 2 — loaded `S01_mars1_deg.csv`; extracted logFC for HUBS=[CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1]; confirmed 5 negative, FIS1 +1.261 positive.
- Check 3 — for each candidate's `rescue_genes`, looked up each gene in `S01_mars1_deg.csv` and asserted `DEG_0.3==True` and `logFC<0`. All 23 genes passed (CD3D −0.436, CD8A −0.321, IL7R −0.596, LCK −0.640, HLA-DRA −0.469, HLA-DRB1 −0.893, CD14 −0.766, FCGR3A −0.610, HLA-DQA1 −0.530, HLA-DQB1 absent from rescue list, etc.).

**Values recomputed vs manuscript — discrepancies:**
- 23/25 down: recomputed 23 → **matches** manuscript.
- 22/25 FDR-significant: recomputed 22 → **matches** manuscript.
- 21 both down & significant: recomputed 21 → **matches** manuscript.
- FIS1 only up-regulated hub: recomputed True → **matches** manuscript.
- Other five hubs down: recomputed True → **matches** manuscript.
- IFN-γ positive-control 4/5 (not 5/5): recomputed/confirmed via `08_positive_control_check.csv` and HLA-DQB1 `DEG_0.3=False` → **matches** manuscript.
- All `rescue_genes` are Mars1-down DEG_0.3: recomputed all-pass → **matches** manuscript (no leakage found).
- **No numeric discrepancy found in the mandatory checks.** The discrepancies I raise are *interpretive/biological* (Issues 1–7), not arithmetic: (a) TIM-3/HAVCR2 stated "up" in Discussion but data show "down" (internal contradiction, not a CSV error); (b) LAG3 presented as up-regulated exhaustion marker but not FDR-significant; (c) "converged" wording vs co-expression network pointing to erythroid genes; (d) hub prognostic attribution vs zero L1 weight on CD74/HLA-DRB1; (e) FIS1 passenger framing; (f) 28-day endpoint mismatch; (g) stratified-treatment language.

**Note on the audit script:** `check_audit_assertions.py` guards hub direction (assertion 7) and would have caught a FIS1-direction flip, but it does **not** check the TIM-3/LAG3 Discussion wording, the "converged" claim, or the L1-zero-weight point — those are prose inconsistencies a CI assertion cannot catch, which is why manual review is required.

---

*End of A1 review.*
