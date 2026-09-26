# A4 — Independent peer review (Venue + Reporting Standards layer)

**Manuscript:** *Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning* (v1.1.0)
**Review layer:** Venue fit + reporting-standard audit (STROBE-MR, TRIPOD, abstract/cover-letter consistency, formatting hard-fails, reporting honesty).
**Independence:** Read only `manuscript.md`, `coverletter.md`, `PANEL_BRIEF.md`, and the `03_results/*.csv` source tables. No prior-round files consulted.

---

## Issues

### Issue 1 — 【Problem】 24 of 31 listed references are never cited anywhere in the text (dangling bibliography).
**【Evidence】** `manuscript.md` inline citations (grep `\[[0-9]+\]`): only the numbers **4, 11, 12, 13, 16, 30, 31** appear (with [16]×5, [31]×3). The References section nonetheless lists **1–31**. Uncited entries include methods-critical items: [6] Ritchie/limma, [7] Subramanian/L1000, [8][9] Newman/CIBERSORT, [10] Hemani/MR-Base, [26] Edgar/GEO, [27] Langfelder/WGCNA, [21][28] Bowden/MR-Egger, [24] Verbanck/horizontal-pleiotropy, [5][15] Davenport & ArrayExpress (the external cohort!), [25] Parnham/azithromycin, [23] McDaniel/lenalidomide, [14][20] Netea/trained-immunity, [17] Hotchkiss, [22] van der Poll, [29] Basham/IFN-γ, [2] Boomer, [3] Singer/Sepsis-3, [1] Aran/xCell, [18] Schuemie, [19] Li/thymosin.
**【Why it matters】** A reference list where ~77% of entries are uncited is a hard desk-reject/major-revision point at essentially every computational/translational journal. It also signals that foundational methods (limma, L1000, CIBERSORT, MR-Egger, the validation-cohort sources) are asserted without attribution, weakening methodological traceability.
**【Fix】** Either (a) insert the citations where the method/cohort/drug is introduced — minimally: [6] in §2.2, [7] in §3.9, [8]/[9] in §2.7, [10]/[21]/[28]/[24] in §2.10, [5]/[15]/[26] when E-MTAB-4451/GEO are described, [27] in §2.4, [25]/[23]/[14]/[20] in §3.7–3.8, [17]/[22] in Discussion, [29] for IFN-γ mechanism, [2]/[3] in Introduction; or (b) delete every entry that is not actually used. Do not ship a 31-item list with 7 citations.

### Issue 2 — 【Problem】 Both abstracts present the label-informed, optimistic within-cohort CV AUC 0.659 as "comparable to the published benchmark" without the optimism caveat the body explicitly applies.
**【Evidence】** EN abstract: *"reached a cross-validated AUC of 0.659 (training 0.750), comparable to the published immune-related-gene benchmark (0.619–0.648)"* (`manuscript.md:14`). ZH abstract: *"免疫风险签名交叉验证 AUC=0.659（训练 0.750），与已发表免疫相关基因基准（0.619–0.648）相当"* (`manuscript.md:25`). The body contradicts the framing: §3.4 *"this within-cohort CV estimate is optimistic; the honest out-of-sample generalization is the external AUC 0.638"* (`manuscript.md:106`) and §5 limitation 1 restates it (`manuscript.md:189`).
**【Why it matters】** Editors and most readers read only the abstract. Leading with 0.659 as "comparable to benchmarks" lets the optimistic, label-informed number stand as the signature's headline performance, while the body disowns it in favour of the honest external 0.638 (which is only marginally above the recomputed 0.604 benchmark). This is an abstract/body inconsistency that several journals treat as a correctness defect, and it is the exact trap flagged in the panel brief.
**【Fix】** In both abstracts, attach the optimism qualifier, e.g.: *"the within-cohort 5-fold CV AUC of 0.659 is label-informed and optimistic; the honest, cross-platform external AUC was 0.638 (95% CI 0.532–0.748), comparable to — not better than — the recomputed IRG benchmark (0.604)."* Do not delete the 0.659 number (it is real), but stop presenting it as the benchmark-comparable headline.

### Issue 3 — 【Problem】 STROBE-MR item 9b claim is not satisfied by the supplied data: the "harmonisation exclusion tallies" are asserted but absent from the harmonised tables.
**【Evidence】** Text: *"Per-gene exclusion tallies from harmonisation (palindromic, strand-ambiguous, allele-incompatible) are itemised in the accompanying `*_harmonised.csv` tables (STROBE-MR item 9b)"* (`manuscript.md:72`). Actual file `03_results/10_genetics_mr_harmonised.csv` header = `rsid,ea_e,nea_e,beta_e,se_e,p_e,eaf_e,ea_o,nea_o,beta_o,se_o,p_o,eaf_o,gene,F` and contains only **27 retained** instruments (no exclusion-reason or removed-count column). The same holds for the outcome-specific harmonised CSVs.
**【Why it matters】** STROBE-MR requires reporting how many SNPs were retained after harmonisation and how many were dropped, with reasons. A reader cannot verify instrument pruning from the provided tables, and the manuscript's own claim that the tallies are "itemised" is false.
**【Fix】** Either add an exclusion-reason/status column (e.g., `drop_reason: palindromic | strand_ambiguous | allele_incompatible | retained`) to each `*_harmonised.csv`, or add a short results sentence/table giving per-gene extracted→retained→dropped counts (the GI tally the brief asks for). Until then, soften the §2.10 sentence to "available in the supplementary harmonised tables" without claiming the exclusion reasons are itemised.

### Issue 4 — 【Problem】 Table 1 mislabels ITGAM as "not significant at FDR<0.05" — it is in fact FDR-significant.
**【Evidence】** `manuscript.md:92` Table 1: *"ITGAM | −0.21 | 1.7e-03 | integrin αM (not significant at FDR<0.05)"*. Source `03_results/S01_immunoparalysis_direction.csv` row ITGAM: `adj.P.Val = 0.001677362` (< 0.05, i.e. FDR-significant) with `DEG_0.3 = False` only because `|logFC| = 0.208 < 0.3`.
**【Why it matters】** The parenthetical is factually wrong about FDR status and quietly contradicts the paper's own "22/25 significant at FDR<0.05" tally (ITGAM would actually count as one of the significant genes). It erodes confidence in Table 1 and the §3.1 count.
**【Fix】** Reword to: *"ITGAM | −0.21 | 1.7e-03 | integrin αM (FDR-significant but did not meet the |logFC|≥0.3 DEG threshold)"*. Confirm the §3.1 "22/25 significant" enumeration still holds with ITGAM included as significant-but-sub-threshold.

### Issue 5 — 【Problem】 TRIPOD: headline performance should be the optimism-corrected external AUC, which the body already does, but the abstract (Issue 2) undercuts it.
**【Evidence】** Body §3.4/§5 clearly separates within-cohort CV (0.659, optimistic) from external locked-orientation (0.638, honest) and reports calibration/DCA for the external score in Fig. S06 (`manuscript.md:106`). The model is a simple fixed-orientation 30-gene score, so full TRIPOD prediction-model reporting is not strictly required; what is required is that the abstract not blur the two.
**【Why it matters】** If aimed at a clinical-prediction/translational venue, reviewers will check that the external, optimism-corrected AUC is the headline and that calibration is shown — both are present in the body. The only leak is the abstract framing.
**【Fix】** Adopt the Issue-2 rewording so the abstract's headline is 0.638, not 0.659. No further TRIPOD item needed unless the target journal mandates a TRIPOD flow diagram (then add one for the E-MTAB-4451 application).

---

## § Stands up (verified correct — what I checked and found sound)

1. **LINCS L1000 numbers are exact and honestly framed.** `03_results/S08_l1000_candidate_scores.csv`: azithromycin rescue_score 0.0133 / wtcs 0.0626 / rank 9152 (pct 0.448 ≈ median); lenalidomide 0.0439 / 0.2058 / rank 5435 (pct 0.266 = top 26.6%). These match §3.9 verbatim (azithromycin "≈ median", lenalidomide "top 26.6%"). HAVCR2/FCGR3A are correctly stated as absent from L1000 and excluded by design (`manuscript.md:135`), and BRD-prefixed IDs are correctly described as anonymized Broad identifiers, *not* a pharmacologic class (`manuscript.md:137`). The glucocorticoid positive-control caveat (prednisone/dexamethasone also score high) is present and properly used to caution that transcriptional rescue ≠ functional rescue — good reporting honesty.

2. **Drug-repositioning concordance table is fully consistent with source.** `03_results/08_candidates_drugs.csv`: IL-7 1.0 (5/5), GM-CSF 0.833 (5/6), IFN-γ 0.714 (5/7), Azithromycin 0.667 (2/3), Lenalidomide 0.40 (2/5), Thymosin α1 0.40 (2/5), BCG 0.20 (1/5) — all match Table 2 (`manuscript.md:121-129`). The abstract/§3.7 claim "IFN-γ rescued 5/5 antigen-presentation genes" maps exactly to the five AP genes in its `rescue_genes` list (HLA-DRA/DRB1/DQA1/DQB1/CD74) — verified, not overstated. The metric is correctly defined as curated *response-gene* concordance, explicitly **not** direct-target overlap (§2.8, §5 limitation 9).

3. **MR Table 3 is byte-for-byte consistent with the primary-outcome CSV.** `03_results/10_genetics_mr_outcome5086_28ddeath.csv`: CD74 IVW 1.119 (0.607–2.063); HLA-DQA1 0.923 (0.804–1.061); CD14 IVW 0.927, MR-Egger 0.906 (P=5.1e-3, null intercept), weighted median 0.914; HAVCR2 0.978; FIS1 0.963; FCGR3A `insufficient_instruments`. All match §3.10/Table 3. Exposure–outcome sample overlap is disclosed and the no-correction decision is flagged as a limitation (§2.10, §5 limitation 2). The MR layer is correctly tiered as hypothesis-generating — honest.

4. **External validation AUC is traceable and correct.** `03_results/09_external_validation.csv`: `auc_EMTAB4451_orientedSum = 0.6382` (CI 0.5317–0.7475) = manuscript 0.638 (0.532–0.748); `auc_EMTAB4451_external_locked = 0.5848` (CI 0.4687–0.6959) = manuscript locked-L1 0.585 (0.469–0.696); `auc_IRG3_benchmark_EMTAB4451 = 0.604`; missing gene HLA-DQA1. All consistent with §3.5.

5. **Cover letter is appropriately conservative and matches the manuscript's tiered evidence framing — no over-statement detected.** The letter leads with the honest external AUC 0.638 ("comparable to, not better than" the benchmark) and never touts the 0.659 CV number; it explicitly states the MR layer is "hypothesis-generating only," discloses the sample overlap with no correction, and states the drug layer uses curated response-gene concordance "not direct pharmacologic-target overlap." This is fully consistent with the manuscript's limitations and answers the brief's cover-letter-vs-manuscript check in the authors' favour.

6. **Formatting hard-fails that PASS:** corresponding-author email present (`manuscript.md:6` and cover letter); data-availability statement present (§Data availability, GitHub + DOI-upon-acceptance); ethics statement present (§Ethics statement); no leftover "delete before submission"/placeholder/editorial notes found (the only grep hit, `manuscript.md:195`, is the legitimate ADMET limitation paragraph — "interfaces", not an instruction).

---

## § Questions for the authors

1. Of the 24 uncited references, which did you intend to cite (methods/cohort/drug attributions) versus which should be deleted? Please confirm the intended final reference count.
2. Will you accept the abstract rewording in Issue 2 (optimism caveat on the 0.659 CV AUC) for both EN and ZH abstracts, or do you prefer to drop the 0.659 from the abstract entirely and lead with the external 0.638?
3. Can you supply the per-gene harmonisation drop-counts (palindromic / strand-ambiguous / allele-incompatible) for STROBE-MR item 9b, or should the §2.10 sentence be softened until they exist?
4. Do you agree ITGAM should be re-labeled FDR-significant-but-sub-threshold (Issue 4), and does that change the "22/25 significant" count in §3.1?

---

## § What I actually checked

**Files read:** `05_reports/manuscript.md`, `05_reports/coverletter.md`, `05_reports/review_r2/_PANEL_BRIEF.md` (brief only; no other review_r2 file), and the following source CSVs in `03_results/`:
- `S01_immunoparalysis_direction.csv` — verified Table 1 logFC/adj.P for HLA-DRB1, CD74, CD14, FCGR3A, ITGAM, HAVCR2, HLA-DRA, LYZ; confirmed ITGAM adj.P=0.0017 (FDR-significant).
- `S06_auc_compare.csv` — CV 0.6586 / train 0.7495 (≈0.659/0.750); IRG 0.619/0.648.
- `08_candidates_drugs.csv` — all 7 drug concordance fractions match Table 2.
- `S08_l1000_candidate_scores.csv` — azithromycin & lenalidomide rescue/wtcs/rank verified.
- `10_genetics_mr_outcome5086_28ddeath.csv` — all Table 3 ORs/CIs/P verified; FCGR3A insufficient_instruments.
- `09_external_validation.csv` — orientedSum 0.6382 / locked 0.5848 / IRG 0.604 verified.
- `10_genetics_mr_harmonised.csv` — confirmed only 27 retained instruments, no exclusion-reason column (Issue 3).

**Commands run:** `grep -oE '\[[0-9]+\]'` on `manuscript.md` to enumerate cited reference numbers (result: only 4, 11, 12, 13, 16, 30, 31 → 24 uncited); directory listing to locate the real manuscript path (`05_reports/manuscript.md`, not a root-level `manuscript.md`).

**Values recomputed/compared myself:** cited-reference set (counted from text); ITGAM FDR status (read adj.P from CSV); external-AUC provenance (read from CSV, matched to manuscript to 3 decimals); L1000 ranks/percentiles (read from CSV, matched to manuscript); MR ORs (read from CSV, matched to Table 3).

**Not re-run (by design):** the full bioinformatics pipeline; I relied on the already-computed CSVs as the panel brief instructed. I did not independently recompute the bootstrap CIs or the MR estimators.

**Conclusion for this layer:** The numerical substance of the MR, LINCS, drug, and external-validation claims is accurate and honestly tiered, and the cover letter is conservative and consistent. The blocking problems are **editorial/standards**, not analytical: the 24-uncited-reference list (Issue 1, hard fail), the abstract's omission of the optimism caveat on the 0.659 AUC (Issue 2), the unmet STROBE-MR harmonisation-tally claim (Issue 3), and the ITGAM FDR mislabel (Issue 4). Resolve Issues 1–4 before any submission.
