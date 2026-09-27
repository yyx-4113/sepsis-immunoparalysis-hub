# A2 — Design review (biostatistics / causal inference / epidemiology)

**Manuscript:** `05_reports/manuscript.md` (tag v1.14.0, commit 800063e)
**Role:** Independent blind reviewer — design, statistical integrity, Mendelian-randomisation / causal inference, and epidemiological validity.
**Independence statement:** This was treated as a first submission. I read only the manuscript text and the deposited `03_results/` source files listed in the panel brief. I did not consult any prior-round review, response, or other panellist's output under `05_reports/`. Every judgement below is grounded in text I read or numbers I recomputed from the deposited files.

---

## Scope and approach

My charge was to police six specific design claims the brief flagged as "corrected in this round": (i) the DCA-vs-deposited-grid reconciliation and the removal of any "converging near 0.80" language; (ii) the calibration slope/intercept point estimate with no spurious 95% CI; (iii) the MR design including overlapping instruments, the CD74 critical-care overlap-inflated reversed signal, the new MHC-II LD caveat, the 27-instrument count, and the "all IVW OR 0.92–1.12, P ≥ 0.23" summary; (iv) EPV / cross-validation independence and any label leakage; (v) the AUC comparison 0.638 vs 0.619 vs 0.529 and the honesty of "weak reference only"; and (vi) the Mars1-vs-Mars2/3/4 P-values. I recomputed each from source rather than trusting the prose.

## Independence attestation

I confirm I did not open, grep, or summarise any of the forbidden files: `05_reports/REVIEW_round12_20260927.md`, `05_reports/REVIEW_round13_20260927.md`, `05_reports/review_r12/` (any file), `05_reports/review_r13/` (any file), any `REVIEW_*.md`/`RESPONSE_*.md`/`REVISION_*.md`, `.workbuddy/memory/`, `05_reports/scirep_submission_checklist.md`, or any other panellist's output under `05_reports/review_r14/`. My judgement of the CD74/HLA-DQA1 genomic location was based on standard public gene-annotation resources (HGNC/NCBI/LOVD/Atlas of Genetics and Oncology), not on any prior reviewer's note. Every numeric claim below is traced to a file I read or a quantity I recomputed from the deposited `03_results/` data. Where I could not recompute (notably the DeLong P vs Peng's reported 0.619), I say so explicitly rather than asserting a verification I did not perform.

---

## Summary verdict

The statistical design of this revision is, on the whole, markedly improved and now *mostly honest*. The three items I was specifically asked to police — the DCA grid, the calibration point estimate (no spurious CI), and the MR primary-outcome summary — all check out exactly against the deposited numbers. The external-validation framing ("independent in cohort and platform but not in label") is an honest description of a genuine limitation, and the MR negative-causal narrative is commendably conservative.

However, one newly added sentence is **factually wrong and must be corrected before acceptance**: the claim that *CD74 and HLA-DQA1 lie within the same MHC-II region and may share linked instruments* is genomically false — CD74 is on chromosome 5q32, HLA-DQA1 on chromosome 6p21.32. They are on different chromosomes and cannot share linkage disequilibrium. The underlying motivation (the 45-test BH set is not independent) is legitimate, but the cited mechanism is wrong, which undermines rather than supports the caveat.

A second, smaller auditability gap: the "proxy CI overlaps the other benchmarks" claim is asserted in prose, but the proxy 95% CI is not deposited anywhere I can find, so the overlap is not independently verifiable from the repository.

**Three things the authors got right (worth preserving through revision):**
- They scoped the external claim to the *gene set + fixed orientation* (equal-weight score, AUC 0.638) rather than the cohort-specific L1 weights (which transported poorly at 0.585), and they said so plainly. This is the correct honesty about what actually generalises.
- They framed the MR layer as Tier-3 / hypothesis-generating and refused to let the single reversed, overlap-inflated CD74 critical-care result be read as a positive hub finding. The family-q reporting is transparent about nominal significance while the prose inverts the interpretation appropriately.
- They dropped any spurious calibration CI and presented slope 0.50 / intercept −0.04 as a point estimate, then correctly concluded the score is a *ranker* rather than a calibrated probability source. That is the right inference from a 106-patient recalibration.

**Reviewer's bottom line.** Of the six design focuses I was assigned, five are now correct and well-supported by the deposited data; the sixth (the new MHC-II LD caveat) contains a single factual error that is easy to fix and that I recommend blocking acceptance on until corrected. The manuscript's instinct toward conservatism — scoping the external claim to gene set + orientation rather than fitted weights, labelling the MR layer Tier-3/hypothesis-generating, calling the proxy a non-competing weak reference, and presenting the score as a ranker rather than a calibrated probability — is the right one and should be preserved. My only substantive demand is the genomic correction in Item D-6; the remaining points are improvements that would raise the paper from "acceptable after minor revision" to "clean and reproducible."

---

## § Stands up (verified against source files)

**S1. The DCA grid now matches the prose, and the "diverge" correction is real and complete.**
Recomputed from `03_results/09_ext_dca_grid.csv` (columns `threshold,nb_model,nb_treat_all`):
- `nb_model == nb_treat_all` at thresholds 0.05, 0.10, 0.15, 0.20, 0.25 (both 0.4638 at 0.05; both 0.3632 at 0.20).
- First threshold where `nb_model > nb_treat_all`: **0.30** (model 0.2844 vs treat-all 0.2722). This is exactly what the manuscript states ("exceeds the treat-all strategy from threshold ≈0.30 onward"; `manuscript.md:112`).
- At threshold **0.80**: `nb_model = 0.0`, `nb_treat_all = −1.5472` (rounds to −1.55). The manuscript states "at threshold 0.80 the model NB is 0.00 while treat-all NB is −1.55" (`manuscript.md:112`). Exact match.
- The prose explicitly says the advantage "widens rather than converges" (`manuscript.md:112`). No "converging near 0.80" claim against treat-all remains anywhere in the text.

**S2. Calibration reported as point estimate only, with no fabricated 95% CI.**
`03_results/09_ext_calibration_dca.csv` gives `calib_intercept = −0.0382`, `calib_slope = 0.5028`, `auc = 0.6382` — which round to −0.04 / 0.50 / 0.638, consistent with every mention (`manuscript.md:109`, `:112`, `:236`). The file has no CI columns, and I found **no** CI attached to the calibration slope/intercept anywhere in the text (§3.4, §3.5, §7). The previously problematic "calibration CI" language has been removed. This is now an honest statement of a point estimate on a 106-patient recalibration.

**S3. Mars1 vs Mars2/3/4 Mann–Whitney P-values recompute exactly.**
From `03_results/S02_immunoparalysis_score.csv` (802 per-sample immune-function scores), recomputed two-sided Mann–Whitney U:
- Mars1 (n=132) vs Mars2 (n=176): **P = 4.671×10⁻¹ (0.47)** — matches `manuscript.md:97`.
- Mars1 vs Mars3 (n=118): **P = 1.852×10⁻¹⁸ (1.9×10⁻¹⁸)** — matches `manuscript.md:98`.
- Mars1 vs Mars4 (n=53): **P = 1.321×10⁻³ (1.3×10⁻³)** — matches `manuscript.md:99`.
The conclusion — that the score does not separate Mars1 from Mars2 (P=0.47) but does separate the Mars1/Mars2 low-score cluster from Mars3/Mars4 — stands on its own numbers.

**S4. The MR instrument count (27) and per-gene split are exact and FCGR3A is correctly excluded.**
`03_results/10_genetics_mr_harmonised.csv` contains 27 data rows, 27 distinct rsIDs, 0 duplicates, split CD74 3 / HLA-DQA1 4 / CD14 6 / HAVCR2 6 / FIS1 8 = 27; FCGR3A is absent (excluded for insufficient instruments, consistent with `manuscript.md:60`, `:147`). The 45-test BH family (`10_mr_bh_family.csv`) is exactly 5 genes × 3 estimators × 3 outcomes = 45 rows. Internally consistent end to end.

**S5. The primary-outcome IVW summary ("all IVW OR 0.92–1.12, P ≥ 0.23") is accurate and correctly scoped.**
From `10_mr_bh_family.csv` (outcome 5086_28ddeath), the five IVW estimates are: CD74 1.119 (P 0.72), HLA-DQA1 0.923 (P 0.26), CD14 0.927 (P 0.24), HAVCR2 0.978 (P 0.85), FIS1 0.963 (P 0.47). All ORs fall in [0.923, 1.119] ⊂ [0.92, 1.12] and all P ≥ 0.236 ≥ 0.23. This matches the Abstract (`manuscript.md:14`) and §3.10 (`manuscript.md:147`–`159`). It is correctly scoped to the *primary* outcome (the CD74 critical-care IVW is 2.222 and is rightly excluded from this summary).

**S6. L1000 candidate rescue ranks verify to the digit.**
`03_results/S08_l1000_candidate_scores.csv`: azithromycin rescue 0.0133, wtcs 0.0626, rank **9152** of 20,413 (44.8th percentile); lenalidomide rescue 0.0439, wtcs 0.2058, rank **5435** of 20,413 (26.6th percentile). Both match `manuscript.md:140` ("lenalidomide ranked 5,435/20,413 (top 26.6%)" and "azithromycin ranked 9,152/20,413 (≈ median)"). The algebraic identity rescue = wtcs/√22 is also internally consistent (0.0439 vs 0.2058/√22 = 0.0439).

---

## Detailed items

### Item D-1 — DCA "diverge" prose is fully supported by the grid (stands up)
【Problem】 The prior-round concern was that the manuscript might still imply the model and treat-all strategies *converge* near threshold 0.80; I needed to confirm the corrected language is matched by the deposited grid, and that no contradictory "converging" sentence survives.
【Evidence】 `03_results/09_ext_dca_grid.csv` full table:
```
threshold nb_model nb_treat_all
0.05 0.4638 0.4638
0.10 0.4340 0.4340
0.15 0.4007 0.4007
0.20 0.3632 0.3632
0.25 0.3208 0.3208
0.30 0.2844 0.2722   <- first model > treat_all
0.35 0.2388 0.2163
0.40 0.1604 0.1509
0.45 0.1029 0.0738
0.50 0.0755 -0.0189
0.55 0.0346 -0.1321
0.60 0.0472 -0.2736
0.65 0.0418 -0.4555
0.70 0.0063 -0.6981
0.75 0.0094 -1.0377
0.80 0.0000 -1.5472
0.85 0.0000 -2.3962
0.90 0.0000 -4.0943
```
The model exceeds treat-all first at 0.30, and at 0.80 model = 0.00 vs treat-all = −1.5472. `manuscript.md:112` states exactly this and says the advantage "widens rather than converges." The §3.4 recalibration paragraph (`manuscript.md:109`) separately notes the model "converged to zero net benefit at high thresholds (≥ ~0.77), where treat-none is equivalent" — that statement is about the model *vs treat-none* (model NB → 0 = treat-none level), which is also true from the grid (model NB 0.0094 at 0.75, 0.00 at 0.80). The two "converge" usages refer to different comparators and are both correct. I also confirmed the `nb_treat_all` column obeys the standard treat-all net-benefit formula NB = prev − [threshold/(1−threshold)]·(1−prev) with prev = 0.4906: at 0.80 → 0.4906 − 4·0.5094 = −1.547 (matches −1.5472); at 0.50 → −0.0188 (matches −0.0189); at 0.30 → 0.2723 (matches 0.2722). So the deposited grid is internally coherent.
【Why it matters】 DCA is easily mis-read; a residual "model ≈ treat-all near 0.80" claim would have invalidated the clinical-decision-support narrative. It is absent. The remaining model-vs-treat-none convergence at high thresholds is the correct, defensible reading (the model treats no one when the calibrated probabilities are shrunk toward 0.5 by the slope-0.50 recalibration).
【Specific fix】 None required for the convergence language. Optional clarity addition to `manuscript.md:112`: "At threshold 0.80 the model NB is 0.00 (it treats no patient, i.e., it equals treat-none) while treat-all NB is −1.55; the two therefore diverge, and the model's advantage over treat-all widens with threshold."

### Item D-2 — Calibration reported as point estimate only, no fabricated CI (stands up)
【Problem】 Confirm that the calibration slope/intercept are given without a 95% CI, as required, and that the point estimate matches the source.
【Evidence】 `03_results/09_ext_calibration_dca.csv` columns are `n,deaths,prevalence,calib_intercept,calib_slope,auc,nb_thr0.20,nb_thr0.30,nb_thr0.50`. Values: n=106, deaths=52, prevalence=0.4906, calib_intercept=−0.0382, calib_slope=0.5028, auc=0.6382, nb_thr0.20=0.3632, nb_thr0.30=0.2844, nb_thr0.50=0.0755. The three NB columns equal the §3.4 stated values (0.36, 0.28, 0.08 at 0.20/0.30/0.50; `manuscript.md:109`) and equal the DCA grid model NB at those thresholds. Text `manuscript.md:109` ("calibration slope of 0.50 with intercept −0.04"), `:112` ("near-zero intercept (−0.04) but an under-fitting slope of 0.50"), `:236` (provenance, no CI). No CI column or claim anywhere.
【Why it matters】 Reporting a CI on a 106-patient logistic recalibration would be over-precise and potentially misleading; omitting it is the honest choice and removes a prior vulnerability. The slope of 0.50 (ideal = 1.0) correctly signals over-confident absolute probabilities, motivating the "ranker not probability" conclusion.
【Specific fix】 None required. Keep as is. If the authors wish to be even more precise, they may add a sentence noting the slope estimate itself is noisy at n=106 and should be re-estimated in a larger cohort (which they already say).

### Item D-3 — Mars1 vs Mars2/3/4 P-values are exact (stands up)
【Problem】 Verify the endotype-score separation statistics, which anchor the "two-cluster gradient, not Mars1-specific" claim.
【Evidence】 Recomputed from `03_results/S02_immunoparalysis_score.csv`: two-sided Mann–Whitney U gave P = 0.467 / 1.852×10⁻¹⁸ / 1.321×10⁻³ for Mars2 / Mars3 / Mars4 vs Mars1, matching `manuscript.md:97`–`99` (0.47 / 1.9×10⁻¹⁸ / 1.3×10⁻³). Sample sizes (Mars1 n=132, Mars2 n=176, Mars3 n=118, Mars4 n=53) also match the §3.2 table.
【Why it matters】 These numbers anchor the claim that the immune score indexes a Mars1/Mars2-vs-Mars3/Mars4 gradient rather than a Mars1-specific signature — a key honesty point the manuscript makes (`manuscript.md:90`). Mis-stated P-values here would over- or under-state the score's specificity.
【Specific fix】 None required.

### Item D-4 — MR instrument inventory is internally consistent (stands up)
【Problem】 Confirm 27 retained instruments and the FCGR3A exclusion against the harmonised file.
【Evidence】 `03_results/10_genetics_mr_harmonised.csv`: 27 rows, per-gene 3/4/6/6/8, 0 duplicate rsIDs. CD74 = {rs12478601, rs2305480, rs4810485}; HLA-DQA1 = {rs114293611, rs13203549, rs28383314, rs3819714}; CD14 (6); HAVCR2 (6); FIS1 (8). FCGR3A absent. `manuscript.md:60` and `:147` state the same split and the FCGR3A exclusion. The 45-test family in `10_mr_bh_family.csv` is exactly 45 rows (5×3×3). Matches.
【Why it matters】 Instrument transparency is a STROBE-MR requirement (item 9b); the count is verifiable and correct, and the per-SNP drop-list reproducibility claim is credible.
【Specific fix】 None required.

### Item D-5 — Primary MR summary stats verify (stands up)
【Problem】 Confirm "all IVW OR 0.92–1.12, P ≥ 0.23" on the primary 28-day-death outcome.
【Evidence】 `10_mr_bh_family.csv` (5086_28ddeath): CD74 IVW 1.119 (0.72), HLA-DQA1 0.923 (0.26), CD14 0.927 (0.24), HAVCR2 0.978 (0.85), FIS1 0.963 (0.47). OR range [0.923, 1.119]; minimum P 0.236. Text `manuscript.md:14` and `:147`–`159` corroborated. The CD14 MR-Egger 0.906 (P 4.9×10⁻²) and weighted-median 0.914 (P 0.065) also match the family file exactly.
【Why it matters】 This is the paper's main negative-causal claim; it is exactly supported by the data and correctly scoped to the primary outcome. The scoping matters: if a reader generalised "all IVW OR 0.92–1.12, P ≥ 0.23" to *all* MR results, they would be wrong, because the CD74 critical-care IVW is 2.222 — but the manuscript never makes that generalisation; it explicitly confines the summary to the 28-day-death primary outcome (`manuscript.md:14`, `:147`). This discipline is exactly what a careful MR reviewer looks for, and it is present. The narrow OR range (0.92–1.12) also correctly implies that germline variation in these hubs is, at most, a weak modifier of 28-day sepsis mortality — consistent with the "no causal support" conclusion and with the Tier-3/hypothesis-generating framing elsewhere.
【Specific fix】 None required.

### Item D-6 — NEW factual error: CD74 and HLA-DQA1 do NOT share an MHC-II region (must fix)
【Problem】 The manuscript now states that CD74 and HLA-DQA1 "lie within the same MHC-II region and may share linked instruments" as the rationale for why the 45-test BH correction is only a conservative approximation. This is genomically false.
【Evidence】 CD74 (ENSG00000019582) is located on **chromosome 5q32** (HGNC:1697; Entrez 972; public gene resources — Atlas of Genetics and Oncology, LOVD, NCBI Gene — all list 5q32). HLA-DQA1 (ENSG00000196735) is located in the **MHC on chromosome 6p21.32**. The two genes are on *different chromosomes* and therefore cannot share linkage disequilibrium; no instrument of one can be in LD with an instrument of the other. I also verified in `03_results/10_genetics_mr_harmonised.csv` that the CD74 rsID set {rs12478601, rs2305480, rs4810485} and the HLA-DQA1 rsID set {rs114293611, rs13203549, rs28383314, rs3819714} have **zero overlap** (no shared instrument), consistent with the absence of any genomic LD between them.
The claim appears at `manuscript.md:195` (Limitation 2): "the 45-test BH correction treats all tests as independent, but CD74 and HLA-DQA1 lie within the same MHC-II region and may share linked instruments, so the family-error control is a conservative approximation rather than a strict independence guarantee."
【Why it matters】 The independence concern is real, but the *mechanism* cited is wrong. A geneticist reviewer will immediately recognise that CD74 is not in the MHC; this single incorrect sentence discredits an otherwise careful limitations section and could trigger a blunt "factually incorrect" critique. It also misinforms the reader about where LD-based dependence could occur: only HLA-DQA1 sits in the MHC; the other five candidates are on five other chromosomes (CD14 5q31.1, FCGR3A 1q23.3, HAVCR2 3p24.3, FIS1 9q22.2) — none of which are in LD with each other or with HLA-DQA1. If the wording was meant to capture the *functional* association of CD74 (the invariant chain that chaperones MHC-II), that must be stated explicitly and not framed as genomic colocalisation. Note the distinction carefully: CD74 protein is the invariant chain (Ii) that binds nascent MHC class-II α/β dimers in the ER and is essential for antigen presentation — that is a *functional/physical* association with the MHC-II complex. But the *gene locus* CD74 is at 5q32, far from the MHC at 6p21. Conflating "CD74 associates with MHC-II proteins" with "the CD74 gene lies in the MHC-II region" is the likely source of the error, and the manuscript must not let that ambiguity stand.
【Specific fix】 Replace the sentence at `manuscript.md:195` with:
> "The 45-test Benjamini–Hochberg correction treats all tests as independent, but true independence does not hold: the three estimators (IVW, MR-Egger, weighted median) applied to a given gene and outcome reuse the same instruments and outcome, and the three outcomes share the same eQTL exposures, so the effective number of independent tests is lower than 45. Genomically, the six candidate genes lie on six distinct chromosomes (CD74 5q32, HLA-DQA1 6p21.32 within the MHC, CD14 5q31.1, FCGR3A 1q23.3, HAVCR2 3p24.3, FIS1 9q22.2) and share no LD, so the family-error control is a conservative approximation rather than a strict independence guarantee."

### Item D-7 — "Independent in cohort and platform but not in label" is honest, with one residual selection-chain caveat
【Problem】 Assess whether the external-validation independence claim is truthful and whether any label leakage remains.
【Evidence】 The locked signature (gene set + fixed orientation + StandardScaler + L1 coefficients) was trained on GSE65682 and applied to E-MTAB-4451 with no re-tuning (`manuscript.md:55`, `:112`); the two cohorts differ in platform (Affymetrix GPL13667 vs Illumina GPL10558), population (mixed sepsis vs UK CAP-sepsis), and outcome recorder. The manuscript explicitly states the validation is "independent in cohort and platform but not in label" (`manuscript.md:29` brief; echoed in §3.5). The within-cohort 5-fold CV is correctly flagged as optimistic/label-informed (`manuscript.md:109`, `:194`). One genuine, disclosed residual: gene selection and orientation used GSE65682's 28-day labels, and HLA-DQA1 was driven to a zero L1 coefficient *and* is the one gene absent from the external array (`manuscript.md:109`, `:112`) — so the external AUC is partly the product of a discovery-label-informed gene set. This is acknowledged ("the external 0.638 is driven by the gene set and orientation collectively"), so it is not hidden leakage, but it means the validation is "independent in test labels" only in the narrow sense that E-MTAB-4451's labels were not used for fitting.
【Why it matters】 The phrasing is defensible and more honest than most repositioning manuscripts, but the nuance — that gene *selection* reused the discovery label — should be stated once more plainly so a reader does not over-interpret "external" as "fully label-independent." This is the single most likely reviewer pushback on the validation claim, and pre-empting it strengthens the paper. The distinction matters epidemiologically: a signature validated on an independent cohort with an independent outcome recorder is genuinely externally validated in the cross-validation taxonomy sense (external/transportability validation), but it is not a "fully independent" signature in the stronger sense because the feature set was optimised on the discovery labels. Both truths can coexist if stated precisely; the manuscript currently leans toward the weaker ("not in label") framing, and a small clarifying sentence closes that gap without undermining the achievement. Label leakage in the strict sense — using E-MTAB-4451's own 28-day labels to fit the model — does not occur, and I found no evidence of it; the only leakage is the benign, disclosed reuse of discovery labels for feature selection, which is standard practice for locked-signature external validation.
【Specific fix】 At `manuscript.md:112` (or §5 Limitation 1, `:194`), add one sentence: "Note that 'external' here means an independent test cohort and platform; the 30-gene set and its orientation were themselves selected using GSE65682 28-day labels, so the validation is independent of the *test* labels but not of the discovery labels that defined the signature."

### Item D-8 — AUC comparison: "weak reference only" is mostly honest, but the proxy CI is not deposited (auditability gap)
【Problem】 The brief asks whether the 0.638 vs 0.619 (Peng) vs 0.529 (recomputed IRG-3 proxy) comparison and the "weak reference only" framing are honest, and whether the CIs overlap.
【Evidence】 `03_results/S06_auc_compare.csv`: CV AUC 0.6586 (→0.659), training 0.7495 (→0.750), Mars1 endotype 0.5782, IRG benchmark (E-MTAB-4451) 0.619, IRG (GSE65682) 0.648. External AUC 0.638 (CI 0.532–0.748, `manuscript.md:112`) and locked-L1 0.585 (CI 0.469–0.696). The proxy 0.529 is reported (`manuscript.md:14`, `:46`, `:109`, `:112`, `:194`) and described as "a weak reference only" / "weak lower-bound reference, not a competing benchmark" (`manuscript.md:109`). The external CI (0.532–0.748) has its lower bound *just above* the proxy point estimate 0.529; whether the two intervals overlap depends entirely on the proxy's own 95% CI upper bound, which I could **not locate in any deposited file** (only the point estimate 0.529 appears; `S06_auc_compare.csv` carries no CI; the IRG-3 value also appears as `auc_IRG3_benchmark_EMTAB4451 = 0.5288` in `09_external_validation.csv` but with no CI). So the assertion "its confidence interval overlaps the other benchmarks" (`manuscript.md:112`, `:194`) is currently unverifiable from the repository.
The "weak reference only" description itself is honest: the IRG-3 proxy is a deliberately truncated 3-gene subset of a signature whose full 30-gene form scores 0.619–0.638, and the manuscript already states it "lacks the full IRG gene set" and is "not a competing benchmark." That framing is fair and not cherry-picked.
【Why it matters】 The comparison is rhetorically balanced, but an unverifiable CI-overlap claim is a small reproducibility hole. A reviewer who tries to reproduce the "overlap" statement will fail, which weakens trust in an otherwise careful section. Conversely, over-selling the proxy as a "near-random" foil to make the signature look stronger would be the dishonest move — and the manuscript avoids that by explicitly calling it a non-competing weak reference. There is also a subtler epidemiological point worth stating for the reader: a 3-gene proxy of a 30-gene signature is not a true competitor but a deliberately weakened lower bound, so its near-random AUC (0.529) tells us only that three genes carry little standalone signal — not that the full signature is weak. The manuscript's "weak reference only / not a competing benchmark" language already captures this; depositing the proxy CI would let a reader see quantitatively that the proxy's interval straddles 0.5 while the full signature's interval (0.532–0.748) sits clearly above it, which is the honest and informative comparison.
【Specific fix】 Deposit the proxy AUC with its bootstrap 95% CI (e.g., add `auc_IRG3_CI_lo/hi` to `03_results/09_external_validation.csv`) and replace the bare claim with an explicit interval, e.g.: "the 3-gene proxy 0.529 (95% CI X.XX–X.XX) overlaps the external 0.638 CI (0.532–0.748) and, given sampling error at n=106, is not distinguishable from Peng's reported 0.619, so all three are mutually non-significant and the proxy is a disclosed weak lower bound only."

### Item D-9 — CD74 critical-care "overlap-inflated reversed signal" is honestly handled
【Problem】 Confirm the reversed, overlap-inflated CD74 critical-care signal is presented without over-claiming.
【Evidence】 `10_mr_bh_family.csv`: CD74 weighted-median critical-care OR 2.194 (P 6.6×10⁻¹⁹, family q ≈ 3×10⁻¹⁷) — the only family-significant test — but with **reversed direction** (higher predicted CD74 → worse outcome, opposite to the Mars1 expression model). The manuscript reports this as a "genotype–severity association rather than a causal hub claim" (`manuscript.md:162`, `:174`, `:184`, `:195`), notes only 3 instruments, and flags the exposure–outcome sample overlap that inflates type-I error (`manuscript.md:58`, `:174`). The CD74 critical-care MR-Egger family q = 0.79 (not significant), and the Egger SE (0.111) being smaller than its own IVW SE (0.325) is explicitly explained as an artefact of df=1 with three instruments (`manuscript.md:174`). All of this is internally consistent and conservative. The apparent method concordance (IVW/Egger/WM all ~2.2) is correctly attributed to the *same three overlapping, low-power instruments* shared across estimators (`manuscript.md:174`), so agreement is read as shared data limitation, not independent corroboration.
【Why it matters】 This is the paper's strongest MR signal and the easiest one to over-sell; the manuscript resists that temptation correctly. The reversed direction is the crucial honesty check — a naive reading would have presented it as "CD74 protects," but the authors invert the interpretation appropriately. The exposure–outcome sample overlap (eQTLGen discovery includes UK Biobank participants, who also populate the UK Biobank sepsis outcomes) is the key reason the standard errors are biased downward and the type-I error inflated; naming this explicitly (`manuscript.md:58`, `:174`) is the correct mitigation, even though no overlap-correction estimator was applied. A reviewer inclined to be harsh could still argue the CD74 critical-care result should not appear in the main Table 4 at all given the overlap and the 3-instrument fragility; my view is that it is acceptable to retain it *provided* the "genotype–severity association, not causal hub claim" framing stays as prominent as it currently is. The family-q reporting (q ≈ 3×10⁻¹⁷) is transparent about nominal significance while the prose correctly refuses to call it a positive hub finding — exactly the right balance for a Tier-3, hypothesis-generating layer.
【Specific fix】 None required. The handling is exemplary. Optional: consider moving the CD74 critical-care row to a clearly marked "caveat" position in Table 4 so the q≈3×10⁻¹⁷ value is not read as a positive hub result.

### Item D-10 — L1000 candidate ranks verify; "top 26.6%" framing is acceptable
【Problem】 Verify lenalidomide 5435 and azithromycin 9152 ranks and the single-direction caveat.
【Evidence】 `03_results/S08_l1000_candidate_scores.csv`: azithromycin rescue 0.0133, wtcs 0.0626, rank **9152** (44.8th pct); lenalidomide rescue 0.0439, wtcs 0.2058, rank **5435** (26.6th pct). Matches `manuscript.md:140` ("lenalidomide ranked 5,435/20,413 (top 26.6%)" and "azithromycin ranked 9,152/20,413 (≈ median)"). The "single-direction rescue proxy" and glucocorticoid positive-control caveats (`manuscript.md:138`–`142`) are appropriately self-critical: prednisone scores high (rank 651, 3.2nd pct) while dexamethasone does not (rank 6808), demonstrating a positive rescue score is necessary but not sufficient for functional immune restoration.
【Why it matters】 These are the only connectivity-scored candidates; accurate reporting is essential to the repositioning claim's modesty. The honest "modest, not top-tier" framing (e.g., "both are directionally positive... but the magnitude is modest") is correct and not over-stated.
【Specific fix】 None required.

### Item D-11 — DeLong P≈0.56 vs Peng's 0.619 is plausible but not independently recomputable here
【Problem】 The manuscript states the external 0.638 is "within sampling noise of 0.619 (DeLong P ≈ 0.56, not significant)" (`manuscript.md:109`).
【Evidence】 I could not recompute this DeLong test because Peng et al.'s per-sample predictions on E-MTAB-4451 are not deposited (only the reported point estimate 0.619 is cited). Given the external 95% CI (0.532–0.748) comfortably contains 0.619, a non-significant DeLong P is entirely plausible and consistent; the claim is therefore credible but should be cited as "Peng et al. reported" rather than presented as a test the authors performed. The manuscript elsewhere correctly notes Peng's 0.619 is a "reported (not recomputed) value on the same cohort" (`manuscript.md:109`), which partially mitigates this.
【Why it matters】 Presenting a DeLong P without the underlying predictions can read as a test the authors ran. It is low-risk but should be phrased as a literature comparison to avoid any appearance of an unverifiable computation.
【Specific fix】 At `manuscript.md:109`, rephrase to: "the external 0.638 falls within the sampling uncertainty of Peng et al.'s reported 0.619 on this same cohort (the two 95% CIs overlap), so the signature is comparable rather than established as superior" — dropping the unattributed "DeLong P ≈ 0.56" unless the test is actually recomputed and its inputs deposited.

### Item D-12 — EPV = 3.8 is disclosed but the "≥10 rule" threshold deserves a quantitative caveat
【Problem】 The discovery L1 model has 114 death events / 30 genes ≈ 3.8 events-per-variable, below the conventional ≥10 rule (`manuscript.md:109`).
【Evidence】 Manuscript states EPV ≈ 3.8 and correctly flags it as capping confidence. This is honest. One addition: with EPV < 4, the L1-selected non-zero coefficients are themselves unstable, which is *additional* reason the externally portable claim is scoped to the gene set + orientation (equal-weight) rather than the learned weights (locked-L1 external AUC only 0.585, `manuscript.md:112`). The fact that 7 of 29 coefficients are exactly zero and HLA-DQA1 is absent externally (`manuscript.md:109`) further shows the L1 weights did not transport — reinforcing that the portable component is the *set and orientation*, not the fitted coefficients.
【Why it matters】 Reinforces — rather than undercuts — the honesty of the external-validation scope. Stating the EPV implication explicitly pre-empts the critique that the within-cohort AUC is an over-fit artefact.
【Specific fix】 Optional: at `manuscript.md:109`, append "— at EPV < 4 the L1 coefficient estimates are themselves unstable, which is why the externally portable quantity is the fixed-orientation gene set, not the cohort-specific weights."

### Item D-13 — The real BH non-independence is method/outcome correlation, not LD (ties to D-6)
【Problem】 The manuscript's independence caveat (Limitation 2) attributes the BH set's non-independence to LD between CD74 and HLA-DQA1. As shown in D-6, that specific LD does not exist. What *does* break independence should be stated instead.
【Evidence】 In a 45-test set (5 genes × 3 estimators × 3 outcomes), the three estimators on a given (gene, outcome) cell reuse the *same* instruments and the *same* outcome, so IVW/Egger/WM p-values are mutually correlated — they are not 3 independent tests. Likewise, the three outcomes (susceptibility, 28-day death, critical care) all use the same eQTL exposures, inducing cross-outcome correlation. These are the genuine sources of non-independence. Genomic LD between candidate genes is irrelevant here because the six genes sit on six different chromosomes (D-6) and share no instruments. The BH correction therefore *does* over-state effective independence, but for the wrong reason as currently written.
【Why it matters】 Correcting the mechanism makes the limitation defensible to a methods-aware reviewer. The current wording invites a one-line rebuttal ("CD74 isn't in the MHC") that would taint the surrounding correct points. More broadly, the BH family correction's validity hinges on how many *effective* independent tests there are; over-stating independence is conservative (it makes q-values larger, harder to flag significance), so the manuscript's conclusion that only the reversed CD74 critical-care result survives is *not* overturned by fixing the mechanism — if anything, the genuine method/outcome correlation makes the set *more* interdependent than the LD story implied, so the conservative q-values remain defensible. The fix therefore strengthens, rather than weakens, the causal-inference conclusion. It also removes the only internally checkable falsehood in the MR section, which is what matters most for a clean acceptance.
【Specific fix】 Use the replacement sentence provided in Item D-6, which reframes the non-independence around estimator/outcome sharing rather than a non-existent gene-gene LD.

### Item D-14 — External prevalence 0.49 verifies and supports the DCA interpretation
【Problem】 Confirm the external prevalence used in the DCA framing.
【Evidence】 `03_results/09_ext_calibration_dca.csv`: prevalence = 0.4906 (52 deaths / 106 = 0.4906, exact). The manuscript states "external prevalence 0.49" (`manuscript.md:112`) — correct to two decimals. This prevalence is what makes treat-all increasingly harmful at higher thresholds (treating everyone when the base rate is ~49% yields negative net benefit once the threshold cost exceeds ~0.49/0.51). The grid's treat-all NB crossing zero around threshold 0.50 (NB = −0.0189 at 0.50) is exactly consistent with this prevalence.
【Why it matters】 A wrong prevalence would have broken the DCA arithmetic; it is correct, and the "treat-all becomes increasingly harmful at higher thresholds" narrative is thereby supported.
【Specific fix】 None required.

### Item D-15 — Mars1 endotype AUC 0.578 is internally consistent and correctly subordinate
【Problem】 Verify the Mars1 binary-indicator AUC cited in §3.2.
【Evidence】 `03_results/S06_auc_compare.csv`: `Mars1 endotype` AUC = 0.5782, matching `manuscript.md:90` ("Mars1 classified 28-day death at AUC 0.578"). The manuscript correctly subordinates this to the 30-gene signature (0.659 CV / 0.638 external) and notes it is a binary indicator, not the continuous signature. No discrepancy.
【Why it matters】 Minor, but confirms the §3.2 figure is not inflated relative to the deposited value.
【Specific fix】 None required.

### Item D-16 — The model NB=0 above threshold 0.80 means "treat nobody," which is correct DCA behaviour and supports the divergence claim
【Problem】 At thresholds 0.80, 0.85, and 0.90 the deposited grid shows `nb_model = 0.0` exactly, while `nb_treat_all` is increasingly negative. A reader might wonder whether model NB=0 is an artefact (e.g., a floor clamp) rather than a meaningful result.
【Evidence】 `03_results/09_ext_dca_grid.csv`: nb_model = 0.0000 at 0.80/0.85/0.90; nb_treat_all = −1.5472 / −2.3962 / −4.0943. The recalibration compresses predicted probabilities toward 0.5 (slope 0.50, `09_ext_calibration_dca.csv`), so after calibration correction almost no E-MTAB-4451 patient has a calibrated risk > 0.80; the model therefore recommends treating 0 patients, and NB = 0 by construction — identical to the treat-none strategy. This is the textbook DCA behaviour at high thresholds and is not a numerical artefact. It also explains *why* the model "diverges" from treat-all at 0.80: treat-all keeps harming more patients as the threshold rises, while the model quietly stops treating anyone and sits at the treat-none floor of 0.
【Why it matters】 Stating this explicitly prevents a reviewer from misreading the flat 0.00 as a plotting or rounding bug. It also reinforces the manuscript's own conclusion that the score functions as a *ranker* (separation of high- from low-risk patients across the 0.10–0.75 band where NB is positive) rather than as a high-threshold treatment trigger. The DCA therefore supports discrimination, not absolute-risk treatment thresholds — exactly the honest read the manuscript settles on (`manuscript.md:112`).
【Specific fix】 Optional one-sentence addition to `manuscript.md:112`: "Above threshold ~0.77 the model recommends treating no patient (calibrated risks are concentrated near 0.5), so its NB rests on the treat-none floor of 0.00 while treat-all continues to accumulate harm — the divergence from treat-all is thus genuine and reflects the model declining to act at thresholds where it has no confident high-risk cases."

---

## § Questions for the authors

1. **On the MHC-II LD claim (Item D-6):** Was the sentence "CD74 and HLA-DQA1 lie within the same MHC-II region" intended to mean *functional* association (CD74 encodes the invariant chain that chaperones MHC-II) rather than *genomic* colocalisation? If so, the wording must change, because genomically they are on different chromosomes (5q32 vs 6p21.32) and share no LD — the current text is factually incorrect as written and is the one issue I would block on.
2. **On the proxy CI (Item D-8):** Can you deposit the 3-gene IRG proxy AUC *with its bootstrap 95% CI*? Without it, the statement "its confidence interval overlaps the other benchmarks" cannot be audited from the repository, and a reviewer will likely request it.
3. **On DeLong (Item D-11):** Was the DeLong P ≈ 0.56 actually computed by you, or is it an inference from overlapping CIs? If not computed, please rephrase as a literature comparison, and consider depositing Peng's per-sample predictions (or your recomputation of Peng's signature) so the comparison is on equal preprocessing footing.
4. **On the CD74 critical-care reversal (Item D-9):** Given that this is the only family-significant MR result yet it reverses the Mars1 direction and rests on 3 overlapping instruments plus exposure–outcome overlap, would you consider moving it to a clearly marked "caveat" box rather than the main Table 4 body? The current text handles it well, but the visual prominence of a q ≈ 3×10⁻¹⁷ value may invite misreading as a positive hub finding.
5. **On external-label independence (Item D-7):** Would you agree to add one explicit sentence stating that the 30-gene *set and orientation* were selected using GSE65682 labels, so "external" refers to the test cohort/labels only? This pre-empts the most likely reviewer pushback on the validation claim.
6. **On the IRG comparison asymmetry (Item D-8/D-11):** You compare your recomputed 0.638 against Peng's *reported* 0.619 and your recomputed 0.529 proxy. To make the benchmark comparison symmetric, have you considered recomputing Peng's full IRG signature on E-MTAB-4451 in this study, rather than citing their published point estimate? The mixed (recomputed-vs-reported) comparison is disclosed but remains asymmetric.
7. **On calibration slope stability (Item D-2):** With n=106 and only 52 events, the recalibration slope 0.50 has a wide (unreported) CI. Do you agree the "ranker not probability" conclusion should be framed as provisional pending a larger external cohort, rather than as a settled property of the score?

---

## § What I actually checked

**Files read (manuscript + source data only; no prior reviews):**

- `05_reports/manuscript.md` (full, v1.14.0) — verified all DCA, calibration, MR, AUC, score, and L1000 claims against deposited numbers; checked for residual "converging near 0.80 vs treat-all" language (none) and for any calibration CI claim (none found).
- `03_results/09_ext_dca_grid.csv` — 19-row grid; confirmed first model>treat-all at 0.30 and values at 0.80 (0.00 vs −1.5472); verified the treat-all column obeys NB = prev − [thr/(1−thr)]·(1−prev) with prev 0.4906.
- `03_results/09_ext_calibration_dca.csv` — intercept −0.0382, slope 0.5028, auc 0.6382, prevalence 0.4906, NB columns 0.3632/0.2844/0.0755; no CI columns.
- `03_results/S02_immunoparalysis_score.csv` — 802 per-sample scores; recomputed Mann–Whitney U P for Mars1 vs Mars2/Mars3/Mars4.
- `03_results/S06_auc_compare.csv` — CV 0.6586, train 0.7495, Mars1 0.5782, IRG(E-MTAB) 0.619, IRG(GSE65682) 0.648.
- `03_results/10_genetics_mr.csv` — susceptibility-outcome IVW/Egger/WM per gene (used to cross-check Table 4 susceptibility column).
- `03_results/10_mr_bh_family.csv` — all 45 tests; confirmed primary-outcome IVW OR range and P floor, CD74 WM critical-care family q ≈ 3×10⁻¹⁷, CD14 28d Egger family q = 0.73, CD74 critcare Egger family q = 0.79.
- `03_results/10_genetics_mr_harmonised.csv` — 27 instruments, per-gene 3/4/6/6/8, 0 duplicates, FCGR3A absent; confirmed zero rsID overlap between CD74 and HLA-DQA1.
- `03_results/S08_l1000_candidate_scores.csv` — azithromycin rank 9152, lenalidomide rank 5435; verified against §3.9.
- `03_results/09_external_validation.csv` — located `auc_IRG3_benchmark_EMTAB4451 = 0.5288` (no CI); external AUC 0.638 and locked-L1 0.585 present.

**Computations performed (recomputed, not just read):**

- Mann–Whitney U (two-sided) for Mars1 vs Mars2/Mars3/Mars4 → P = 0.467 / 1.852×10⁻¹⁸ / 1.321×10⁻³.
- Instrument overlap test: CD74 rsID set ∩ HLA-DQA1 rsID set = ∅ (empty).
- Treat-all NB formula reconstruction at thresholds 0.30/0.50/0.80 using prevalence 0.4906 → matched grid values 0.2722 / −0.0189 / −1.5472.
- Spot-checked every value in manuscript Tables 3 and 4 against `10_mr_bh_family.csv` and `10_genetics_mr.csv` — all 15 primary-outcome rows and all 15 susceptibility/critical-care IVW rows matched to ≤3 significant figures.
- Verified the DCA grid monotonic relationship: model NB = treat-all NB for 0.05–0.25, model > treat-all from 0.30, and model NB pinned at 0.00 for 0.80–0.90 (treat-none level) while treat-all NB becomes increasingly negative (−1.55, −2.40, −4.09).
- Confirmed L1000 wtcs = rescue·√22 identity (lenalidomide 0.0439 vs 0.2058/√22 = 0.0439).

**Additional cross-checks performed:**

- Confirmed FCGR3A appears in no harmonised row (consistent with the "insufficient instruments" exclusion and the 27-vs-28 arithmetic).
- Confirmed the 45-test family file contains exactly 45 rows = 5 genes × 3 estimators × 3 outcomes, with FCGR3A's 3 outcome-slots absent (the 15-test per-outcome `p_fdr_bh` column in `10_genetics_mr_outcome5086_28ddeath.csv` correctly excludes FCGR3A).
- Confirmed the manuscript's "29/30 signature genes mapped" (HLA-DQA1 absent) is consistent with the L1 zeroing of HLA-DQA1 reported in §3.4 (`manuscript.md:109`).
- Confirmed calibration slope 0.50 (under-fit) is the correct mechanistic explanation for model NB collapsing to 0 at high thresholds: the recalibration logit(p_cal) = −0.04 + 0.50·logit(p_raw) compresses probabilities toward 0.5, so almost no patient exceeds a 0.80 calibrated threshold, and the model treats nobody → NB = 0 = treat-none.

**Discrepancies / unresolved items stated plainly:**
1. **Confirmed error (must fix):** "CD74 and HLA-DQA1 lie within the same MHC-II region" is false — CD74 is chr5q32, HLA-DQA1 is chr6p21.32; they share no LD (verified by both public gene annotation and the empty rsID overlap in the harmonised file). See Item D-6 / D-13.
2. **Auditability gap (should fix):** The proxy (0.529) 95% CI is asserted to overlap but is not deposited; the overlap claim is therefore not reproducible from the repository. See Item D-8.
3. **Unverifiable as-stated:** DeLong P ≈ 0.56 vs Peng 0.619 — plausible from overlapping CIs but not recomputable here because Peng's per-sample predictions are not deposited. See Item D-11.
4. **Minor asymmetry:** The benchmark comparison mixes the authors' recomputed 0.638/0.529 against Peng's *reported* 0.619; disclosed but asymmetric. See Item D-8 / Q6.
5. **No discrepancy found** on: DCA grid vs prose (incl. removal of "converge vs treat-all" language); calibration point estimate and absence of CI; Mars1 score P-values; MR instrument count (27) and per-gene split; primary-outcome IVW summary; L1000 candidate ranks; external prevalence 0.49; Mars1 endotype AUC 0.578.

**Overall assessment:** The design and statistics are, with the single exception of the CD74/HLA-DQA1 genomic claim, honest and well-audited. The CD74/HLA-DQA1 sentence is a factual error that is easy to fix and should block acceptance until corrected; the proxy-CI deposit and DeLong phrasing are minor reproducibility improvements. The MR and external-validation narratives are commendably conservative, and the "weak reference only" / "ranker not probability" framings are appropriate. After the D-6 correction and the two minor deposits/phrasings, this manuscript's statistical design would be suitable for Scientific Reports.

---

## § Appendix — claim-by-claim reconciliation table

The following table lists every numerical claim I was asked to police, the value stated in the manuscript, the value I recomputed or read from the deposited source, and the verdict. "Verified" means exact or ≤3-significant-figure agreement; "Error" means the claim is factually wrong; "Gap" means the claim is asserted but not auditable from deposited files.

| # | Claim (brief focus) | Manuscript value | Recomputed / source value | Verdict | Location |
|---|---------------------|------------------|---------------------------|---------|----------|
| 1 | First threshold where model NB > treat-all NB | ≈0.30 | 0.30 (grid: 0.2844 vs 0.2722) | Verified | `09_ext_dca_grid.csv`; `manuscript.md:112` |
| 2 | Model NB at 0.80 | 0.00 | 0.0000 | Verified | `09_ext_dca_grid.csv`; `manuscript.md:112` |
| 3 | Treat-all NB at 0.80 | −1.55 | −1.5472 | Verified | `09_ext_dca_grid.csv`; `manuscript.md:112` |
| 4 | "Diverge not converge" vs treat-all | stated | grid confirms divergence | Verified | `manuscript.md:112` |
| 5 | No residual "converge near 0.80 vs treat-all" | required | none found (only model-vs-treat-none convergence, which is correct) | Verified | `manuscript.md:109` |
| 6 | Calibration slope / intercept | 0.50 / −0.04 | 0.5028 / −0.0382 | Verified | `09_ext_calibration_dca.csv`; `manuscript.md:109,112` |
| 7 | No 95% CI claimed for calibration | required | none found anywhere | Verified | `manuscript.md:109,112,236` |
| 8 | Mars1 vs Mars2 P | 0.47 | 0.467 | Verified | `S02_immunoparalysis_score.csv`; `manuscript.md:97` |
| 9 | Mars1 vs Mars3 P | 1.9×10⁻¹⁸ | 1.852×10⁻¹⁸ | Verified | `S02_immunoparalysis_score.csv`; `manuscript.md:98` |
| 10 | Mars1 vs Mars4 P | 1.3×10⁻³ | 1.321×10⁻³ | Verified | `S02_immunoparalysis_score.csv`; `manuscript.md:99` |
| 11 | MR instruments retained | 27 (3/4/6/6/8) | 27 (3/4/6/6/8), 0 dups | Verified | `10_genetics_mr_harmonised.csv`; `manuscript.md:60,147` |
| 12 | FCGR3A excluded | stated | absent from harmonised (2 variants) | Verified | `10_genetics_mr_harmonised.csv`; `manuscript.md:147` |
| 13 | Primary IVW OR range | 0.92–1.12 | [0.923, 1.119] | Verified | `10_mr_bh_family.csv`; `manuscript.md:14` |
| 14 | Primary IVW min P | ≥0.23 | 0.236 | Verified | `10_mr_bh_family.csv`; `manuscript.md:14` |
| 15 | CD74 critical-care reversed/overlap-inflated | stated | OR 2.194 reversed, 3 instruments, overlap flagged | Verified | `10_mr_bh_family.csv`; `manuscript.md:162,174` |
| 16 | MHC-II LD caveat (CD74 & HLA-DQA1 same region) | stated | **FALSE** — chr5q32 vs chr6p21.32, 0 rsID overlap | **Error** | `manuscript.md:195`; `10_genetics_mr_harmonised.csv` |
| 17 | External AUC 0.638 (CI 0.532–0.748) | stated | 0.6382 in calibration file; CI from `09_external_validation.csv` | Verified | `09_ext_calibration_dca.csv`; `manuscript.md:112` |
| 18 | Locked-L1 external AUC 0.585 (CI 0.469–0.696) | stated | consistent with §3.5 text | Verified | `manuscript.md:112` |
| 19 | CV AUC 0.659 / train 0.750 | stated | 0.6586 / 0.7495 | Verified | `S06_auc_compare.csv`; `manuscript.md:109` |
| 20 | Peng benchmark 0.619 (reported) | stated | present in `S06_auc_compare.csv` | Verified | `S06_auc_compare.csv`; `manuscript.md:109` |
| 21 | IRG-3 proxy 0.529 | stated | 0.5288 in `09_external_validation.csv` | Verified (point) | `09_external_validation.csv`; `manuscript.md:14` |
| 22 | Proxy CI "overlaps the other benchmarks" | stated | proxy CI **not deposited** | **Gap** | `manuscript.md:112,194` |
| 23 | DeLong P≈0.56 vs Peng 0.619 | stated | not recomputable (Peng predictions not deposited) | **Gap** | `manuscript.md:109` |
| 24 | L1000 lenalidomide rank 5435 (top 26.6%) | stated | 5435 / 20413 = 26.6% | Verified | `S08_l1000_candidate_scores.csv`; `manuscript.md:140` |
| 25 | L1000 azithromycin rank 9152 (≈median) | stated | 9152 / 20413 = 44.8% | Verified | `S08_l1000_candidate_scores.csv`; `manuscript.md:140` |
| 26 | External prevalence 0.49 | stated | 0.4906 (52/106) | Verified | `09_ext_calibration_dca.csv`; `manuscript.md:112` |
| 27 | Mars1 endotype AUC 0.578 | stated | 0.5782 | Verified | `S06_auc_compare.csv`; `manuscript.md:90` |
| 28 | EPV ≈ 3.8 (114/30) | stated | 114 death events / 30 genes = 3.8 | Verified | `manuscript.md:109` |

**Reading of the table:** 26 of 28 rows verify exactly; 2 rows are gaps (proxy CI and DeLong P not auditable from the repository, though both are plausible); and 1 of the 28 (row 16, the MHC-II LD caveat) is a factual error. The error is concentrated in a single sentence and is readily corrected with the replacement text supplied in Item D-6. The two gaps are minor reproducibility improvements (deposit the proxy CI; rephrase or recompute the DeLong comparison). No other claimed number in the design-focused scope was found to be wrong, mis-stated, or mismatched to its source file. This is a strong statistical-design baseline that is let down only by the one genomic mis-statement.

**Negative results — what I specifically looked for and did NOT find (worth recording for the editors):**
- No residual "model and treat-all converge near 0.80" language remains; the prose now says the opposite (diverge/widen). Verified by full-text search of `manuscript.md`.
- No 95% CI is claimed for the calibration slope or intercept anywhere in the text, the tables, or the §7 provenance map. The earlier-round vulnerability (a fabricated-looking CI) has been removed.
- No label leakage in the strict sense (E-MTAB-4451's own 28-day labels used to fit the model) — the external labels were untouched; only the discovery-label feature selection is reused, which is disclosed.
- No duplication of instruments within any gene in `10_genetics_mr_harmonised.csv` (0 duplicate rsIDs across all 27 rows).
- No contradiction between the susceptibility/critical-care IVW values in `10_genetics_mr.csv` and the same values reported in `10_mr_bh_family.csv` (the two files agree to all shown digits).
- No over-statement of the MR primary outcome: the "all IVW OR 0.92–1.12, P ≥ 0.23" summary is correctly confined to the 28-day-death outcome and does not leak into the critical-care or susceptibility results.

---

## § Minor wording suggestions (non-blocking)

- `manuscript.md:109` — the phrase "calibration-in-the-large adequate" for an intercept of −0.04 is reasonable, but consider "calibration-in-the-large acceptable" since −0.04 with no CI is a single noisy point; "adequate" may over-state.
- `manuscript.md:140` — "top 26.6%" for lenalidomide could be misread as "top quartile of rescuers"; consider "26.6th percentile (i.e., 73.4% of compounds score higher)" to prevent over-interpretation of a modest signal.
- `manuscript.md:162` — the critical-care Table 4 row for CD74 currently sits among the other (null) rows; a thin horizontal rule or "(reversed direction — see caveat)" tag would reduce the risk a skimming reader treats q≈3×10⁻¹⁷ as a positive hub result.
- `manuscript.md:55` — "without any re-tuning" is correct for the equal-weight score; consider adding "the locked L1 model was also applied without re-tuning (AUC 0.585)" inline so the reader sees both transportability results in the methods, not only in results.

These four are cosmetic and do not affect the acceptability of the design; they are offered to tighten an already improved manuscript.

