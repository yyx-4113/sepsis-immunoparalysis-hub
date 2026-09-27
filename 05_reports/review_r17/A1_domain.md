# Round-17 blind-domain review — A1 (sepsis immunology / clinical plausibility)

- **Tag:** v1.17.0
- **Read as:** first submission (no prior-round material consulted)
- **Manuscript:** `05_reports/manuscript.md`, cover letter `05_reports/cover_letter.md`
- **Role:** Domain reviewer — sepsis immunology, Mars1 endotype framing, hub-gene biological coherence, checkpoint-exhaustion logic, and drug-shortlist mechanism anchors.

---

## Issues

### (a) FIS1 is folded into "concordant with the immunoparalysis model" although it is an up-regulated, non-immune passenger — biologically incoherent

【Problem】 §3.10 and §4 group FIS1 with the five immune hubs as a protective MR estimate "the direction predicted by the immunoparalysis model," but FIS1 is explicitly a non-immune (mitochondrial-fission) passenger that is *up*-regulated, so the immunoparalysis model predicts no direction for it.

【Evidence】 `S01_mars1_deg.csv` FIS1 row: `1.2614331467372244, 17.156684530047006, 0.0, 0.0, True, True, FIS1` → logFC = +1.26 (up), t = +17.2, DEG_0.3 = True — i.e. observ­ationally *up*-regulated, matching the manuscript's own "logFC +1.26" and the §3.3 classification as "a co-expression passenger / marker, not a mechanistic target." `10_genetics_mr_outcome5086_28ddeath.csv` FIS1: IVW OR 0.963 (P=0.47), MR-Egger OR 0.964 (P=0.49), weighted median OR 0.971 (P=0.77) — all OR<1 (protective) but all non-significant. The culprit sentence is `manuscript.md:149` ("three of the five assessable hubs (HLA-DQA1, CD14, FIS1) returned protective estimates concordant across all three methods … the direction predicted by the immunoparalysis model") and `manuscript.md:186` (same grouping in §4).

【Why it matters】 For the five *down*-regulated immune hubs, a protective MR (higher expression → lower death) is genuinely concordant with the observed Mars1 down-regulation being deleterious. For FIS1, which is *up*-regulated and flagged as non-immune, calling its protective MR "predicted by the immunoparalysis model" is the opposite logic — the up-regulation would have to be read as a protective response, which contradicts the manuscript's own passenger framing. This is a real biological incoherence, not a cosmetic slip, and it weakens the second "reliable" pillar of the Discussion.

【Specific fix】 Replace `manuscript.md:149` with: "On the primary outcome (28-day death) no IVW estimate reached significance; the five immune hubs stratified into directionally mixed MR signals (HLA-DQA1 and CD14 protective, HAVCR2 null, CD74 non-protective), whereas FIS1 — an up-regulated, non-immune co-expression passenger — returned a non-significant protective point estimate that is *not* interpretable under the immunoparalysis model and is reported only for completeness." Mirror this in `manuscript.md:186`.

### (b) "Reduced checkpoint engagement" over-reads bulk blood data that cannot separate cell-loss from per-cell down-regulation

【Problem】 The manuscript repeatedly concludes HAVCR2/TIM-3 down-regulation means "reduced checkpoint engagement," but bulk whole-blood expression cannot distinguish fewer TIM-3-bearing cells from lower per-cell TIM-3, so the conclusion is not supported by the data it cites.

【Evidence】 `manuscript.md:72` ("the present Mars1 program shows down-regulated HAVCR2/TIM-3 (reduced checkpoint engagement) rather than the canonical TIM-3-up exhaustion signature") and `manuscript.md:182` ("also down-regulated, which is more consistent with reduced checkpoint engagement in the immunosuppressed program"). A partial caveat is buried in the same §3.1 paragraph ("Because this is a bulk-blood measurement, the direction cannot distinguish reduced APC/monocyte abundance from lower per-cell expression … single-cell or flow-cytometric resolution is required"), but the headline "reduced checkpoint engagement" in Abstract/§3.1/§4 is stated as a positive mechanistic read-out, not as a bulk net-expression observation.

【Why it matters】 "Reduced checkpoint engagement" implies a per-cell functional state (less inhibitory signalling). Bulk down-regulation is equally consistent with fewer exhausted T cells / fewer APCs (cell-abundance signal) — which would mean the program is *not* showing reduced per-cell engagement. The conclusion is therefore over-reached and sits on one of the three "reliable" pillars in §4.

【Specific fix】 Reword `manuscript.md:72` and `manuscript.md:182` to: "the Mars1 program shows net lower bulk HAVCR2/TIM-3 expression, which is compatible with — but does not by itself establish — reduced per-cell checkpoint engagement, since bulk signal cannot separate lower T-cell/APC abundance from lower per-cell TIM-3; single-cell or flow resolution is required before attributing the signal to either mechanism."

### (c) The PD-1(up)/TIM-3(down) contrast with "the canonical TIM-3-up exhaustion signature" is asserted but the opposing sepsis TIM-3-up literature is not cited

【Problem】 The manuscript presents its TIM-3-down result as a contrast against a "canonical TIM-3-up exhaustion signature" without citing any sepsis study showing TIM-3 up-regulation on exhausted T cells, and does not reconcile the two.

【Evidence】 `manuscript.md:72` and `manuscript.md:182` invoke "the canonical TIM-3-up exhaustion signature" / "the TIM-3 up-regulation that typifies exhausted T cells," yet the only exhaustion citation in that passage is Hotchkiss et al. [3] (referenced for PD-1 up, not TIM-3). The §3.1 immune-gene table (`S01_immunoparalysis_direction.csv`) shows PDCD1 up (logFC +0.16, adj.P=3.0e-10) and HAVCR2 down (logFC −0.35, adj.P=2.8e-13); LAG3 is directionally up but not significant (adj.P=0.55). A substantial sepsis body of work reports TIM-3 *up*-regulation on circulating exhausted T cells correlating with severity — none of it is cited.

【Why it matters】 Without citing the opposing literature and reconciling it, the TIM-3-down "contrast" reads as a discovery rather than a cohort-specific net-expression observation, and the bulk caveat from (b) applies with equal force to this contrast. This is a missing-context gap that a domain reader will immediately flag.

【Specific fix】 Add a citation to sepsis TIM-3-up studies (e.g. the established literature on TIM-3/PD-1 co-upregulation on CD4+/CD8+ T cells in septic patients) and rewrite the contrast as: "whereas prior sepsis studies report TIM-3 *up*-regulation on exhausted T cells, the present bulk Mars1 signal shows net lower HAVCR2/TIM-3 expression — a difference most parsimoniously explained by altered T-cell/APC abundance in bulk rather than reduced per-cell engagement, pending single-cell validation."

### (d) No biologically false drug-mechanism claim found, but two mechanism anchors need either a sepsis-specific caveat or a missing citation

【Problem】 The seven mechanism-anchored agents are biologically plausible and correctly hedged; I found no false mechanism claim, but (i) the BCG/lenalidomide sepsis evidence is weakest and should be explicitly caveated in the mechanism sentence, and (ii) the "canonical MHC-II inducer" IFN-γ anchor is sound but the manuscript should not imply its immunoparalysis benefit is established given the ImmunoSep null.

【Evidence】 `08_candidates_drugs.csv` concordance values (IL-7 0.80, GM-CSF 0.667, IFN-γ 0.571, azithromycin 0.667, lenalidomide 0.40, thymosin α1 0.40, BCG 0.20) all match Table 2 (`manuscript.md:122-132`). The anchors themselves (IL-7 → François 2018 [22]; GM-CSF → Meisel 2009 [23], with the Bo meta-analysis [30] caveat; IFN-γ → Basham 1983 [21]/Döcke 1997 [24]; azithromycin → Parnham 2014 [25]; lenalidomide → McDaniel 2011 [26, MDS context]; thymosin α1 → Li 2015 [27]; BCG → Netea 2016/2011 [28][29]) are biologically defensible. The ImmunoSep caution [31] (`manuscript.md:135`) is used correctly (no mortality benefit, more hemorrhagic events). I did not find a biologically false claim.

【Why it matters】 Not a defect, but the Discussion's claim that "IFN-γ/GM-CSF rebuild antigen presentation" could be read as established benefit; the manuscript already carries the ImmunoSep null, so the fix is purely a wording tightening to keep the causal-therapy language clearly hypothesis-generating.

【Specific fix】 At `manuscript.md:188` reword to: "These agents are mechanistically distinct immune-restorative *candidates*; their sepsis benefit remains unproven (the ImmunoSep trial [31] showed no mortality benefit for axis-reversing IFN-γ), and BCG/lenalidomide in particular rest on trained-immunity/IMiD precedent rather than dedicated sepsis trials."

### (e) §8 claims a four-plot MR diagnostic set that does not exist in `04_figures/`

【Problem】 §8 advertises an MR diagnostic set of four plots (forest, scatter, funnel, leave-one-out), but the figure directory contains only two MR PNGs.

【Evidence】 `04_figures/` listing returns only `mr_diag.png` and `mr_forest.png`. `manuscript.md:257` states "the MR diagnostic set (forest, scatter, funnel, leave-one-out)," while the §7 provenance table (`manuscript.md:246`) lists only `mr_forest.png` and `mr_diag.png`. The two sections contradict each other.

【Why it matters】 Either the three missing plots were never generated or the §8 description over-states the supplementary material; both are citable inaccuracies that a reviewer/editor will catch at proof stage.

【Specific fix】 Either generate `mr_scatter.png`, `mr_funnel.png`, `mr_loo.png` and deposit them, or correct `manuscript.md:257` to "the MR diagnostic set (forest and diagnostic scatter; see `mr_forest.png`, `mr_diag.png`)."

---

## § Stands up (verified)

1. **Mars1 immune-gene directionality is internally coherent and matches the cited immunoparalysis model.** Recomputed from `S01_immunoparalysis_direction.csv`: of 25 consensus immune genes, 23 are Mars1_down and 22 reach FDR<0.05 (PDCD1 is the sole up-regulated significant gene; CD8B, GZMA, LAG3 are non-significant) — exactly the "23/25 down, 22 significant, 21 both down-and-significant" reported at `manuscript.md:72`. No discrepancy.

2. **The MR "no primary IVW significance" headline is accurate, and the manuscript does *not* understate the suggestive signals.** From `10_genetics_mr_outcome5086_28ddeath.csv`: all primary IVW P ≥ 0.23 (CD74 0.72, HLA-DQA1 0.26, CD14 0.24, HAVCR2 0.85, FIS1 0.47). The CD14 MR-Egger nominal P=0.0488 (`manuscript.md:157`) and the CD74 critical-care reversed family-significant signal (`manuscript.md:162,174`) are both explicitly disclosed in §3.10/§5 — so the "hypothesis-generating only" framing is honest, not understated. (I had suspected understatement; the manuscript is clean on this point.)

3. **LINCS L1000 candidate ranks match the manuscript exactly.** `S08_l1000_candidate_scores.csv`: lenalidomide rank 5,435 / 20,413 (rescue 0.0439, pct 0.26625 = "top 26.6%") and azithromycin rank 9,152 / 20,413 (rescue 0.0133, pct 0.44834 ≈ median) — identical to `manuscript.md:140`. The glucocorticoid positive-control caveat (prednisone rescues, dexamethasone does not) is acknowledged at `manuscript.md:142` and correctly used to bound the L1000 evidence rather than over-claim it.

4. **Drug-shortlist concordance fractions are faithful to source.** `08_candidates_drugs.csv` values reproduce Table 2 verbatim (`manuscript.md:122-132`); the IFN-γ method-positive gate (4/5 antigen-presentation subset) and the 4/7 overall (`manuscript.md:120`) are correctly described. I suspected the concordance metric might be mis-computed; it is not.

5. **FIS1 logFC +1.26 is genuinely up-regulated (not a transcription error).** Verified from `S01_mars1_deg.csv` (logFC = 1.2614, t = 17.16). The "up-regulated, non-immune passenger" classification at `manuscript.md:106,218` is therefore internally consistent — which is precisely what makes issue (a) a real framing error rather than a data error.

---

## § Questions for the authors

1. Given FIS1 is an *up*-regulated, non-immune mitochondrial-fission passenger, do you agree it should be removed from the "concordant with the immunoparalysis model" sentence in §3.10/§4, and reported only as a non-significant, direction-agnostic observation?
2. Can you supply a citation for the "canonical TIM-3-up exhaustion signature" in sepsis and reconcile your bulk TIM-3-down with the body of literature reporting TIM-3 up-regulation on exhausted circulating T cells? Is the discrepancy not more parsimoniously explained by altered T-cell/APC abundance in bulk blood?
3. Your bulk-surrogate cell-localisation (§3.6, `S07_axis_celltype.csv`) reports T-cell-module correlations at the aggregate level. Has any deconvolution been able to separate whether the HAVCR2/TIM-3 down-signal is cell-abundance vs per-cell? If not, should the "reduced checkpoint engagement" language be downgraded to "net lower bulk expression"?
4. The MARS consortium's original endotype derivation (Scicluna et al. [5]) was data-driven, not pre-specified on antigen-presentation. Can you clarify the basis for the "near-replication" claim and the source of the "39% 28-day mortality" figure for Mars1, and confirm it is a reproduction of the original rather than a re-derivation on GSE65682?
5. §8 lists four MR diagnostic plots but only two exist in `04_figures/`. Please reconcile — generate the missing plots or correct the text.

---

## § What I actually checked

**Files read:** `05_reports/manuscript.md`, `05_reports/cover_letter.md`, `03_results/S01_immunoparalysis_direction.csv`, `03_results/S05_hub_genes.csv`, `03_results/10_genetics_mr_outcome5086_28ddeath.csv`, `03_results/S02_immunoparalysis_score.csv`, `03_results/08_candidates_drugs.csv`, `03_results/S08_l1000_candidate_scores.csv`, `03_results/S06_signature_genes.csv`, and a targeted grep of `03_results/S01_mars1_deg.csv` (FIS1 row; file is 1 MB and was not read line-by-line, so the full 3,597-DEG count was not independently recomputed — it is traceable and I accept it as stated).

**Computations / recomputations performed:**
- Re-derived immune-gene direction/significance tallies from `S01_immunoparalysis_direction.csv` (23/25 down; 22 FDR-significant; 21 down-and-significant) → matches `manuscript.md:72`.
- Re-derived FIS1 logFC (+1.2614) and t (+17.16) from `S01_mars1_deg.csv` → matches "logFC +1.26, t = +17.2".
- Re-derived all primary MR OR/P from `10_genetics_mr_outcome5086_28ddeath.csv` → all IVW P ≥ 0.23; FIS1 protective but non-significant; CD14 MR-Egger P=0.0488 disclosed → matches §3.10.
- Re-derived L1000 candidate ranks/percentiles from `S08_l1000_candidate_scores.csv` → matches §3.9.
- Re-derived drug concordance fractions from `08_candidates_drugs.csv` → matches Table 2.
- Enumerated `04_figures/` for MR plots → only `mr_forest.png` + `mr_diag.png` present, contradicting the four-plot claim at `manuscript.md:257`.

**Discrepancies found (stated):**
- (a) FIS1 grouped as "concordant with the immunoparalysis model" despite being an up-regulated non-immune passenger — genuine framing error.
- (b) "Reduced checkpoint engagement" over-reads bulk data — partially mitigated by a buried caveat but headline framing still over-reached.
- (c) "Canonical TIM-3-up exhaustion signature" asserted without citing the opposing sepsis TIM-3-up literature.
- (e) §8 four-plot MR diagnostic claim vs only two deposited PNGs.
- No data-arithmetic discrepancies found in the verified numbers (MR, direction file, L1000, drug table).

**Forbidden files NOT opened (per panel brief):** any `05_reports/REVIEW_round*.md`; `05_reports/review_r12/`–`review_r16/`; `.workbuddy/memory/` (all); `05_reports/scirep_submission_checklist.md`; and every other `05_reports/review_r17/*` file besides `_PANEL_BRIEF.md`. The manuscript was treated as a first submission.

---

## VERDICT: Major

The manuscript is, on the whole, unusually honest and well-scoped: the external-validation magnitude is reported without inflation, the MR layer is correctly self-labelled hypothesis-generating, the L1000 glucocorticoid caveat is genuinely constraining, and every number I recomputed (MR, immune-gene directions, L1000 ranks, drug concordance) is faithful to source. These are real strengths.

However, three findings are genuine *scientific/framing* defects — not cosmetic — and they touch the manuscript's conceptual core:
1. **FIS1 folded into "concordant with the immunoparalysis model"** (a) is biologically incoherent because an up-regulated non-immune passenger has no predicted direction under that model; correcting it requires re-framing §3.10 and §4.
2. **"Reduced checkpoint engagement"** (b) over-reads bulk blood data that cannot separate cell-loss from per-cell down-regulation — this is one of the three "reliable" pillars of the Discussion and should be downgraded to a net-expression observation.
3. **The TIM-3-down "contrast"** (c) cites no opposing sepsis TIM-3-up literature and is vulnerable to the same bulk-abundance confound.

None of these requires new experiments; all are fixable by re-wording and one added citation, and the underlying biology (Mars1 immunosuppression, external AUC 0.638) remains sound. The §8 figure discrepancy (e) is a straightforward textual fix. Because the defects are substantive enough to alter how a reader should interpret the Discussion's "reliable" claims yet fully remediable in revision, I recommend **Major revision** rather than Minor or Desk-reject.
