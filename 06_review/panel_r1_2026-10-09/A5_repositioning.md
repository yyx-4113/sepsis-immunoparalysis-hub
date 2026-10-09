# Independent peer review — Drug-repositioning / computational-reprioritization method layer

**Manuscript:** "A reproducible, fully auditable pipeline confirms within-cohort the MARS Mars1 immunoparalysis program and delivers an honest external validation of a 30-gene sepsis prognostic signature"
**Venue target:** BMC Bioinformatics (methodology)
**Reviewer focus:** §2.8, §3.7–3.9, §5 (limitation 8 & 10), §6, Table 3, and Supplementary S08 / S08b / S11
**Review type:** First submission, single-author, single-blind. Reviewed independently; no coordination with other referees.
**Recommendation:** Major revision (methods/statistics of the repositioning section). The biology and the external-validation framing are sound and commendably self-critical; the repositioning statistics and the LINCS subsection, as currently presented, would not survive a repurposing-methods reviewer and should be corrected or demoted before acceptance.

---

## Executive summary for the authors

The repositioning section is the weakest part of an otherwise careful, honest manuscript. Three findings drive the recommendation:

1. **The `response_gene_concordance` binomial "non-significance" is computed against a circular, self-selected null (the 0.84 within-immune rate) and the proper genome-wide null — which is already in your deposited `08_candidates_drugs.csv` as `binom_p_allgene_bg` — is not reported.** Against that proper null (genome-wide Mars1-down rate ≈ 0.225), IL-7, GM-CSF and IFN-γ are *nominally* significant. Presenting only the deflationary 0.84-based P is selective reporting and must be fixed.
2. **The single-direction LINCS aggregation is a construction defect, not merely a caveat.** It rewards up-regulation of the Mars1-*up* exhaustion markers PDCD1/LAG3, and your own glucocorticoid control (an immunosuppressant scoring the 3.2nd percentile) proves the score cannot distinguish immune restoration from immune suppression. The subsection currently carries negative/non-discriminating information dressed as "directional-but-modest rescue."
3. **The headline "7 agents annotated as candidates" is defensible only if the section is explicitly reframed as hypothesis-generating annotation plus a method + blueprint.** Five of seven have zero connectivity evidence and the two small molecules are statistically indistinguishable from random. The drug list should be demoted to illustrative examples, not a "shortlist."

Most of the LINCS arithmetic I recomputed is correct (ranks, percentiles, candidate z-scores, and the exact `wtcs = rescue × √22` identity). The defects are conceptual and statistical, not mostly arithmetic — with one genuine arithmetic slip (prednisone z). Details and paste-ready fixes follow.

---

## Issue 1 — The `response_gene_concordance` binomial null is circular and selectively reported

【Problem】 The manuscript tests `response_gene_concordance` against a 0.84 "background" that is the within-immune marginal rate of the very gene universe the curated sets were drawn from, and it reports only that deflationary null while the proper genome-wide null (also deposited) is omitted.

【Evidence】
- Manuscript §3.7: "under the internal immune-gene background established in §3.1 (21/25, 84%, of consensus immune genes are Mars1-down at FDR < 0.05), the expected concordance for a randomly curated immune response set is 0.84 … one-sided binomial P(X ≥ k) ≥ 0.82 for all seven, so no candidate's concordance exceeds the chance background."
- Source `08_candidates_drugs.csv` contains **two** binomial columns: `binom_p_immune_bg` (0.817, 0.944, 0.985, 0.931, 0.997, 0.997, 1.000) and `binom_p_allgene_bg` (0.011, 0.026, 0.050, 0.129, 0.315, 0.315, 0.720). **Only the 0.84-based column is reported in the text/Table 3.**
- I recomputed the genome-wide Mars1-down rate from `S01_mars1_deg.csv` (11,519 genes, same |logFC|≥0.3 & FDR<0.05 rule as §2.8): genes down-regulated = 2,592 / 11,519 = **0.225**. Plugging p = 0.225 into the one-sided binomial exactly reproduces the deposited `binom_p_allgene_bg` values (IL-7 4/5 → 0.011; GM-CSF 4/6 → 0.026; IFN-γ 4/7 → 0.050; azithromycin 2/3 → 0.129; lenalidomide 2/5 → 0.315; thymosin 2/5 → 0.315; BCG 1/5 → 0.720). So the genome-wide null is real and was computed by the author.

【Why it matters】 A "randomly curated immune-response set" is not a random subset of all transcripts; it is a non-random subset of immune-response genes, which are themselves enriched for Mars1-down by biology. Testing it against the 0.84 within-immune rate asks "is this immune gene set more Mars1-down than the average immune gene?" — a question that is trivially answered "no" for any curated immune set and therefore provides *no* information. It manufactures the appearance of a significance test while being constructed to be uninformative. Omitting the genome-wide null that would show nominal significance for three candidates is selective reporting and will be flagged by any statistics-aware repurposing reviewer; at BMC Bioinformatics this is a correctness issue, not a styling one.

【Specific fix】 Either (a) drop the binomial "non-significance" claim entirely and present the concordance as explicitly descriptive, or (b) replace the circular null with a **genome-wide permutation null** and report it transparently. Minimal acceptable change — replace the relevant sentences in §3.7 with:

> "The curated concordance fractions are descriptive. The appropriate null is the genome-wide Mars1-down base rate (2,592/11,519 = 0.225 under the same |logFC|≥0.3 & FDR<0.05 rule), not the 0.84 within-immune marginal rate, because the curated genes are a non-random subset of the immune universe and cannot be tested against that universe's own marginal rate. Against the genome-wide null, IL-7 (4/5, permutation/binom P≈0.011), GM-CSF (4/6, P≈0.026) and IFN-γ (4/7, P≈0.050) are nominally enriched, but this remains a literature-curation overlap rather than a pharmacologic-target or connectivity validation, and no multiplicity correction across the seven candidates was applied; the fractions therefore rank hypotheses, not significance."

And add a genome-wide permutation (shuffle the Mars1-down label across all 11,519 genes ×1,000 iterations, recompute the empirical P per candidate) as the definitive null, reporting both observed concordance and permutation P in Table 3. The deposited `binom_p_allgene_bg` column should be cited, not hidden.

---

## Issue 2 — Single-direction LINCS aggregation is a construction defect; the glucocorticoid control cannot rescue it

【Problem】 The LINCS rescue score aggregates all 22 query genes with the same sign, so it rewards up-regulation of the Mars1-*up* exhaustion markers PDCD1 and LAG3; the author's mitigation (explicit caveat + glucocorticoid control) is honest but does not make the score informative about immune restoration, and the glucocorticoid result positively demonstrates the score's lack of specificity.

【Evidence】
- Manuscript §3.9 (admitted): "the intended dual-direction requirement that PDCD1 and LAG3 also be down-regulated was **not implemented** in the metric (all 22 genes are aggregated with the same sign), so it rewards up-regulation of PDCD1/LAG3 as well."
- Query composition: 22 genes = 20 Mars1-down antigen-presentation/monocytic genes + 2 Mars1-*up* markers (PDCD1, LAG3), confirmed by the §3.9 description. The 2 up-genes therefore contribute ~9% of the score with the *wrong* sign relative to the intended biology.
- Glucocorticoid control (§3.9, `S08_l1000_positive_control.csv`): prednisone rescue 0.136, rank 651/20,413 (3.2nd percentile); dexamethasone rescue 0.0315, rank 6,808 (33.4th percentile). The manuscript correctly concludes a positive rescue score is "necessary but not sufficient," but the more damaging inference is that an *immunosuppressant* scores in the top 3% — i.e., the metric cannot tell a restorative from a suppressor.

【Why it matters】 A drug that is a pure T-cell-exhaustion driver (up-regulating PDCD1/LAG3) would score positively on this metric even while doing nothing for antigen presentation. Combined with the glucocorticoid result, the score has no demonstrated specificity for the intended "immune restoration" axis. Presenting lenalidomide ("top 26.6%") and azithromycin ("≈ median") as "directionally positive but modest" rescue still lends a veneer of supporting evidence that the author's own caveat says is invalid. As written, the LINCS subsection is a negative/non-discriminating result; it should not be presented alongside the candidate list as partial support.

【Specific fix】 Two acceptable paths:
- **(Recommended, minimal)** Recompute a proper dual-direction score by flipping the contribution of the two Mars1-up genes: `rescue_dual = mean_over_20_down(percentile − 0.5) + mean_over_2_up(0.5 − percentile)`, re-rank lenalidomide and azithromycin, and report both the old and new scores. Then keep the glucocorticoid pair explicitly as a **specificity/negative control** (the metric must *not* light up an immunosuppressant), and state plainly that even after correction the two small molecules remain within the noise band (z = +0.56 and +0.10; rank P = 0.27 and 0.45).
- **(Alternative)** Demote the entire §3.9 LINCS block to a clearly-labelled "negative exploratory control" demonstrating that single-direction L1000 rescue cannot separate restoratives from immunosuppressants, and remove any candidate-ranking language. Replace the §3.9 closing sentence ("the L1000 rescue proxy is treated here as descriptive only … not counted as supportive evidence") with an explicit statement that the LINCS score provides **no** supporting evidence for either small molecule.

Paste-ready replacement for the misleading "directionally positive" phrasing in §6/Discussion:
> "Both small molecules lie within the library noise band (lenalidomide z = +0.56, rank P = 0.27; azithromycin z = +0.10, rank P = 0.45) and the single-direction LINCS score provides no supporting evidence for either, because it is non-discriminating (an immunosuppressant, prednisone, scores in the 3.2nd percentile on the same axis)."

---

## Issue 3 — The glucocorticoid positive-control design has the wrong polarity and is non-reproducible

【Problem】 A positive control for an *immune-restoration* metric should be a known restorative agent; instead the only available `trt_cp` "control" is an immunosuppressant, and the two glucocorticoids disagree (one high, one not), so the control fails as a validation gate and should be re-framed as a specificity falsification.

【Evidence】
- `S08_l1000_positive_control.csv`: prednisone (high), dexamethasone (not high). Dexamethasone appears **7 times** in the full `S08_l1000_rescue_trtcp.csv` (7 distinct signatures, varying rescue), so the single chosen signature (rank 6,808) is an arbitrary pick and the glucocorticoid "class" signal is unstable.
- The genuinely appropriate restorative positive control, IFN-γ, is listed in the positive-control file as "interferon-gamma (biologic, not trt_cp), N/A (absent from trt_cp)" — i.e., it is structurally unavailable as an unbiased L1000 perturbagen, so no true restorative control exists. romidepsin is also absent.
- Recomputed z: prednisone 1.93 (see Issue 6 for the text's erroneous +2.03), dexamethasone 0.37 (mid-pack). Only 1 of 2 glucocorticoids lights up.

【Why it matters】 You cannot validate that a metric identifies immune *restoratives* by showing it lights up an immune *suppressant*; at best that demonstrates the metric is non-specific. The fact that the two glucocorticoids disagree means the "positive control" is not reproducible and fails its gate. The current text turns this into a cautionary point (which is honest), but the *design* of the control is defective and should be labelled as such rather than presented as a partially-successful validation. This is exactly the kind of control-design flaw a methods reviewer blocks on.

【Specific fix】 Re-label §3.9's control paragraph from a "positive-control check" to a **"specificity / negative-control check."** Paste-ready:
> "No unbiased L1000 perturbagen exists for a true restorative positive control (IFN-γ, the canonical MHC-II inducer, is absent from trt_cp). We therefore used glucocorticoids as a specificity probe: if the score measured immune restoration specifically, an immunosuppressant should *not* score highly. Prednisone instead ranked 651/20,413 (3.2nd percentile; dexamethasone, present in 7 signatures, was mid-pack at rank 6,808), so the single-direction score lacks specificity for restoration and is reported as a non-discriminating, descriptive control only. The positive-control gate for repositioning therefore remains unmet by LINCS connectivity."

---

## Issue 4 — Table 3's quantitative sheen overstates the five non-LINCS candidates; "shortlist" framing should be softened

【Problem】 Table 3 presents mechanism-anchored fractions and a binomial P column that look like scoring statistics, sorting candidates by concordance, even though 5/7 have zero connectivity evidence and the text concedes "Table 3 does not rank candidates" — the visual design contradicts the prose.

【Evidence】
- `08_candidates_drugs.csv` + `S08_l1000_candidate_scores.csv`: only lenalidomide and azithromycin exist as `trt_cp` (2/7 with connectivity). The five biologics/vaccines (IL-7, GM-CSF, IFN-γ, thymosin α1, BCG) "lack an unbiased L1000 perturbagen (trt_cp) and rest on mechanism-anchored annotation only" (§3.9).
- Table 3 is ordered IL-7 (0.80) → GM-CSF (0.67) → IFN-γ (0.57) → azithromycin → lenalidomide → thymosin → BCG, implicitly ranking by concordance, and shows a "n_rescue/n_target (P=…)" column whose P is the circular 0.84-based value (Issue 1).
- The abstract and §3.7 call these "hypothesis-generating," which is the correct stance, but the table's ordinal layout and P column undermine that stance.

【Why it matters】 For a methods audience, a table that sorts candidates by a non-significant descriptive fraction and attaches a P-value reads as a prioritization, inviting over-interpretation by clinicians/librarians who scan tables. The honest contribution is the *annotation workflow*, not the specific seven drugs.

【Specific fix】 (a) Rename the table from "Repositioning shortlist" to "Mechanism-anchored hypothesis annotation (illustrative)." (b) Add a column "L1000 connectivity evidence: yes (2) / none (5)." (c) Relabel the P column "Descriptive vs genome-wide null — not a significance test" and, per Issue 1, report the genome-wide null P (and permutation P) rather than the 0.84-based one. (d) State at the top of §3.7: "Five of seven candidates have no unbiased connectivity evidence; the table annotates mechanistic plausibility, not prioritization." (e) Remove the descending sort or add an explicit "ordering is alphabetical, not by rank" note.

---

## Issue 5 — The S11 experimental blueprint is adequately detailed but has an axis-specificity bias, underpowering, and no multiplicity control

【Problem】 S11 is a genuinely useful blueprint (not vague), but its primary endpoint (CD14+HLA-DR MFI ≥1.5×) is a monocyte readout that will misclassify the T-cell-axis candidate IL-7, and the power/multiplicity planning is thin.

【Evidence】
- S11 §2 intervention table ranks IL-7 #1 (rationale: CD3D/CD3E/CD8A/IL7R/LCK — a T-cell-homeostasis axis), yet §3 primary readout is "CD14+ HLA-DR+ MFI" with go/no-go (§8) requiring "IL-7 or GM-CSF restores HLA-DR MFI ≥1.5× **and** ≥15/30 signature genes up-regulated **and** MLR recovery significant."
- IL-7's mechanism is lymphocyte homeostasis, not monocyte HLA-DR; it could fully rescue its annotated T-cell axis and still fail the monocyte-HLA-DR primary endpoint → false "no-go."
- §5 statistics: "n=3 donors gives 80% power to detect 1.5× MFI change at α=0.05 (paired)" — primary-cell MFI SDs are often larger than the assumed 0.25×mean, and n=3 biological donors is below typical; the "3 technical replicates" do not add independent power.
- Seven candidates × multiple endpoints are tested with no α-adjustment; "stratify patients by the 30-gene signature" whose external AUC is 0.585 (CI includes 0.5, §3.5) — a non-validated stratifier.

【Why it matters】 A blueprint that closes the in-silico→functional loop is the manuscript's strongest translational asset, so getting its design right matters. The monocyte-only primary endpoint would systematically disadvantage the T-cell candidate you rank first, risking a misleading negative. The underpowering and missing multiplicity correction would not survive a wet-lab methods reviewer if the experiment were later submitted.

【Specific fix】 Make the primary endpoint **axis-specific**: each drug is tested against its own annotated gene set (IL-7 → CD3/CD8/IL7R/LCK surface or transcript; GM-CSF/IFN-γ → HLA-DR/MHC-II), with a shared secondary of the 30-gene signature. In §8, change the go-rule to "restores its annotated axis (≥1.5× on the drug's own primary readout) AND demonstrates specificity (no concomitant PDCD1/LAG3 up-regulation beyond baseline)." Add a multiplicity note (e.g., Bonferroni/Holm across the 7 candidates for the primary endpoint) and raise the donor target to n≥5 with a realistic MFI SD (cite a pilot SD rather than assuming 0.25×mean). Soften the stratification claim to "exploratory stratification by the 30-gene signature (external AUC 0.585, descriptive)."

---

## Issue 6 — Arithmetic slip: prednisone z is +1.93 (recomputed), not +2.03 as written

【Problem】 The manuscript states prednisone scores "at z = +2.03," but the recomputed z against the deposited background is +1.93.

【Evidence】
- From `S08_l1000_rescue_trtcp.csv` (20,413 compounds): background mean rescue = 0.0063973, SD = 0.0672452.
- prednisone rescue = 0.1364 → z = (0.1364 − 0.0063973) / 0.0672452 = **1.9337**.
- The candidate and positive-control z-values I recomputed all match the manuscript except this one: lenalidomide z = 0.5572 (text +0.56 ✓), azithromycin z = 0.1034 (text +0.10 ✓), dexamethasone z = 0.3728. Only the prednisone +2.03 is inconsistent (it would require SD ≈ 0.0640, not the library 0.0672).

【Why it matters】 Minor, but BMC Bioinformatics copy-editing/statistics checkers will recompute; a wrong z in the single most-cited "cautionary" number slightly undercuts the otherwise careful numeracy of the paper.

【Specific fix】 Replace "z = +2.03" with "z = +1.93" in §3.9 (and the parallel sentence in the Discussion/§6). The percentile (3.2nd) and rank (651/20,413) are correct and need no change.

---

## Issue 7 (lower severity) — The LINCS query omits two of the five immune hubs, so it is not the hub axis

【Problem】 The 22-gene LINCS query excludes HAVCR2 and FCGR3A (two of the five immune hubs) plus TIGIT, so "reverse-connectivity of the Mars1-down axis" is only a partial axis.

【Evidence】 §3.9: "Of the 25 consensus immune genes … three are absent from L1000 and were excluded by platform design: the two hubs HAVCR2 and FCGR3A, and TIGIT." The query is therefore the 22 measurable genes, not the hub-anchored axis.

【Why it matters】 Not blocking, but it should be stated explicitly that the connectivity screen did not test the hub genes HAVCR2/FCGR3A at all, so any claim that LINCS "rescues the Mars1-down axis" is narrower than the hub-anchored claim in §3.3.

【Specific fix】 Add one sentence in §3.9: "Note that two of the five immune hubs (HAVCR2, FCGR3A) are absent from the L1000 platform and were therefore not part of the connectivity query; the screen tests the measurable immune-axis genes, not the hub set per se."

---

## § Stands up — methodology points I checked and found sound or defensible

1. **`wtcs = rescue × √22` is algebraically exact.** I verified against all 20,413 rows of `S08_l1000_rescue_trtcp.csv`: max |wtcs − rescue·√22| = 6.9×10⁻¹⁶. The claimed identity is correct, and presenting wtcs as "not independent evidence" (§3.9) is the right call.
2. **Candidate LINCS ranks, percentiles and z-scores are correct.** lenalidomide: rank 5,435/20,413, percentile-rank 0.266 (top 26.6%), z = +0.557 (text +0.56 ✓), rank P = 0.27 ✓. azithromycin: rank 9,152/20,413, percentile-rank 0.448 (≈ median), z = +0.103 (text +0.10 ✓), rank P = 0.45 ✓. Prednisone/dexamethasone ranks and percentiles match the source files (651 → 3.19%; 6,808 → 33.35%).
3. **Library background statistics are accurate.** Recomputed from the full file: n = 20,413; mean rescue = 0.00640 (text "0.006" ✓); SD = 0.06725 (text "0.067" ✓); 53.6% of compounds > 0 (text "53.6%" ✓); max rescue 0.318 (text "0.32" ✓).
4. **The author's self-critical framing of the repositioning section is methodologically honest and commendable** — the explicit admission of the single-direction flaw (Limitation 10), the glucocorticoid caveat (Limitation 8 / §3.9), and the "hypothesis-generating, not prioritised by significance" stance in the abstract are exactly what a repurposing reviewer wants to see. My critiques are about *extending* that honesty (e.g., the hidden null, the control polarity), not about a cover-up.
5. **The IFN-γ method-positive gate is correctly implemented as a consistency/sanity check, not an independent perturbation control** (§2.8, §3.7), and this scoping is stated. The 4/5 antigen-presentation subset satisfying the gate is internally consistent with the deposited `S01_immunoparalysis_direction.csv` logic.
6. **The genome-wide null (`binom_p_allgene_bg`) was correctly computed and deposited** even though it is not reported in the text — credit to the author for having done the right calculation; the fix for Issue 1 is to *report* it, not to recompute it.

---

## § Questions for the authors

1. Why was only the 0.84 within-immune binomial P reported in Table 3 / §3.7 when `binom_p_allgene_bg` (the genome-wide null) was already in `08_candidates_drugs.csv`? Was the omission intentional, and do you agree it should be reported (with a permutation null) per Issue 1?
2. Can you recompute the dual-direction rescue score (flipping the sign of PDCD1/LAG3) and report whether lenalidomide/azithromycin change rank materially? If the glucocorticoid control *still* lights up prednisone under the dual-direction score, do you agree §3.9 should be demoted to a non-discriminating negative control?
3. For the S11 go/no-go rule: do you accept that a monocyte-HLA-DR-only primary endpoint would misclassify IL-7 (a T-cell-axis candidate ranked #1 in the blueprint), and will you make the primary endpoint axis-specific as suggested?
4. The dexamethasone control appears 7 times in the L1000 library with varying rescue — which signature was chosen for the 6,808 rank, and does the choice affect the "glucocorticoid control carried by prednisone alone" conclusion?
5. BRD-prefixed anonymized IDs are listed for the top rescuers (e.g., top rescue 0.32). Before any claim, will you resolve these to pharmacologic class/name, and do any of them correspond to known immune modulators that would change the interpretation?
6. The LINCS query excludes HAVCR2 and FCGR3A (two of five hubs). Do you consider the connectivity screen's omission of the hub genes a limitation worth stating explicitly (Issue 7), or do you treat the 22-gene axis as a sufficient proxy?

---

## § What I actually checked

**Files read (full or targeted):**
- `05_reports/manuscript.md` — full.
- `03_results/08_candidates_drugs.csv` — full (7 candidates; both binomial columns).
- `03_results/08b_clinical_translation.csv` — full (clinical-readiness tiers).
- `03_results/S08_l1000_candidate_scores.csv` — full (lenalidomide, azithromycin rows).
- `03_results/S08_l1000_positive_control.csv` — full (prednisone, dexamethasone, entinostat, vorinostat, romidepsin, IFN-γ).
- `03_results/S08_l1000_rescue_trtcp.csv` — full (20,413 rows) via Python; header + statistics recomputed.
- `03_results/11_validation_design.md` — full (S11 blueprint).
- `03_results/S01_mars1_deg.csv` — full (11,519 genes; genome-wide Mars1-down rate).
- `03_results/S01_immunoparalysis_direction.csv` — full (25 consensus immune genes; confirms 21/25 down).

**Recomputations (Python, venv `C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe`, numpy/pandas/scipy):**

1. **Library background (from all 20,413 trt_cp):** mean rescue = 0.0063973, median = 0.0055130, SD = 0.0672452, fraction > 0 = 0.5362, max rescue = 0.3182. → Matches manuscript "mean 0.006, SD 0.067, 53.6% > 0, top 0.32." ✓
2. **`wtcs = rescue × √22` identity:** verified across all 20,413 rows; max absolute deviation 6.9×10⁻¹⁶. ✓
3. **Candidate z / rank / percentile:**
   - lenalidomide: rescue 0.0439, rank 5,435, top-fraction 0.26625, z = +0.5572 (manuscript +0.56 ✓), rank P = 0.27 ✓.
   - azithromycin: rescue 0.0133, rank 9,152, top-fraction 0.44834, z = +0.1034 (manuscript +0.10 ✓), rank P = 0.45 ✓.
   - prednisone: rescue 0.1364, rank 651, top-fraction 0.03189, **z = +1.9337 (manuscript claims +2.03 — DISCREPANCY, Issue 6).**
   - dexamethasone: rescue 0.0315 (one of 7 signatures), rank 6,808, top-fraction 0.33351, z = +0.3728 (manuscript "not high" ✓).
   - entinostat: rescue 0.0500, rank 4,821, top-fraction 0.23617 ✓. vorinostat: rescue 0.0172, rank 8,647, top-fraction 0.4236 ✓.
4. **Genome-wide Mars1-down base rate (from `S01_mars1_deg.csv`, same |logFC|≥0.3 & FDR<0.05 rule as §2.8):** 2,592 / 11,519 = **0.2247**. Plugging p = 0.2247 into the one-sided binomial exactly reproduces the deposited `binom_p_allgene_bg` column (IL-7 0.011, GM-CSF 0.026, IFN-γ 0.050, azithromycin 0.129, lenalidomide 0.315, thymosin 0.315, BCG 0.720). This confirms the hidden proper null and underpins Issue 1.
5. **Circular null check:** the 0.84 figure = 21/25 consensus immune genes Mars1-down (confirmed in `S01_immunoparalysis_direction.csv`). Testing curated immune-gene subsets against this marginal rate is circular (Issue 1).

**Discrepancies found:**
- (a) prednisone z: text +2.03 vs recomputed +1.93 — arithmetic error (Issue 6).
- (b) The 0.84-based binomial P is reported while the genome-wide null P (already deposited) is omitted — selective reporting (Issue 1).
- (c) dexamethasone appears 7× in the library; the chosen signature is arbitrary and the glucocorticoid class signal is unstable (Issue 3).
- (d) No discrepancy in wtcs, candidate ranks/percentiles/z (except prednisone), or library background stats — those are correct.

**Not recomputed (out of scope / unavailable):** the L1000 Level-5 MODZ parsing that produced `rescue_score` (source `.gctx` not opened; I treated `S08_l1000_rescue_trtcp.csv` as ground truth per the manuscript's number-provenance table), and the per-gene rank-percentile construction. If the reviewers wish, I can independently rebuild `rescue_score` from `GSE92742_Level5_COMPZ.gctx` to confirm the query-gene selection (22 genes, PDCD1/LAG3 sign handling) — but the construction flaw in Issue 2 is evident from the manuscript's own description without that.

---

*End of review — method/statistics layer only. Biology, external validation (§3.5), and pipeline-auditability aspects were not the focus of this review and are treated as sound based on the manuscript's self-reporting and the checks above.*
