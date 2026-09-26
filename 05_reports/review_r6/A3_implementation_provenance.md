# Reviewer A3 — Provenance and Recomputation Audit

**Manuscript:** `05_reports/manuscript.md` (288 lines, v1.5.0)
**Role:** implementation / provenance auditor (blinded, first-submission posture)
**Sources of truth:** `03_results/*`, `04_figures/*`, `01_data/*` (phenotype matrices only), `02_scripts/python/check_audit_assertions.py`
**Independence:** no prior-round review file, response letter, revision record, author statement, or other reviewer output was opened.

Every number below labelled "recomputed" was derived by me from the result tables; no
number was copied from the manuscript text or from any summary document.

---

## § 1. Cross-verification table — manuscript value vs recomputed value

Only rows where the manuscript value and my recomputed value **disagree** are listed.
All numbers I recomputed and found to agree are catalogued in § 3 (Stands up).

| # | Manuscript location | Manuscript claims | My recomputed value (source) | Verdict |
|---|---|---|---|---|
| V1 | §2.10, §3.10, §5.2, abstract implications | CD74 critical-care MR-Egger *q*≈1.5×10⁻¹¹; "the strongest MR association in the study" | MR-Egger *P* is computed from a **normal** deviate (z=7.187 → 6.6×10⁻¹³). With the correct *t* distribution at df = n−2 = **1** (the file itself records `Q_df = 1.0` on this row), *P* = **0.088**, family BH *q* = **0.79** (`10_genetics_mr_outcome4982_criticalcare.csv` row 2) | **WRONG — 11 orders of magnitude** |
| V2 | §2.10, §3.10, §5.2 | CD74 susceptibility MR-Egger *q*≈0.0025 | Same defect: reported *P*=1.65×10⁻⁴ is the normal *P*; *t*(df=2) *P* = **0.165**, family *q* = **0.90** | **WRONG** |
| V3 | §2.10, §3.10, §4, §5.2 | CD14 28-day-death MR-Egger *P*=5.1×10⁻³, family *q*≈0.058 | Reported *P* is the normal deviate (z=2.800 → 5.11×10⁻³); *t*(df=4) *P* = **4.88×10⁻²**, family *q* = **0.73** | **WRONG** |
| V4 | §2.10, §3.10, §5.2 | "three CD74 tests reached *q*<0.05" under the 45-test family | Re-running BH over all 45 tests with corrected Egger *P*-values: **1** test below 0.05 (CD74 critical-care weighted median, *q*≈3×10⁻¹⁷) — and that one is the direction-reversed estimate the manuscript itself discounts | **WRONG** |
| V5 | §2.10, §3.10, §5.2 | CD74 critical-care weighted median "*q*≈0" / "family *q* = 0" | The stored *P* is exactly `0.000000e+00`, a `1 − CDF` cancellation artifact. From the stored β=0.785890, SE=0.088495 (z=8.881): *P* = **6.65×10⁻¹⁹**, BH *q* = **3.0×10⁻¹⁷**, not zero | **WRONG** |
| V6 | §2.8, §3.3 | "all six hub genes are themselves down-regulated in Mars1"; FIS1 "its down-regulation is directionally concordant with the immunosuppressed program" | `S01_mars1_deg.csv`: FIS1 logFC = **+1.2614** (Mars1 **UP**), t = +17.157, recomputed *P* ≈ 2×10⁻⁵⁶. Corroborated by `08_positive_control_check.csv` row 2, which lists only **five** hubs as Mars1-down (FIS1 absent) | **WRONG — sign inverted** |
| V7 | Abstract (EN + CN), §3.7 | "IFN-γ rescued **5/5** antigen-presentation genes, satisfying the methodological positive-control gate" | `08_positive_control_check.csv` row 1: gate recorded as **4/5** (`HLA-DRA, HLA-DRB1, HLA-DQA1, CD74`); HLA-DQB1 is excluded because its Mars1 logFC (−0.203) fails the pre-specified \|logFC\|≥0.3 DEG rule (`S01_immunoparalysis_direction.csv` row 21) | **WRONG** |
| V8 | Table 1, §3.1 | CD14 adj.P "≈0 (P<1e-300)"; §3.1 "P≈0, underflow" | From the same file's own *t* column (t = −9.715, df≈800): *P* = **3.65×10⁻²¹**, BH adj.P = **2.78×10⁻²⁰**. The stored `0.0` is a `1 − CDF` cancellation artifact; "P<1e-300" is off by ~280 orders | **WRONG** |
| V9 | §2.5 | candidate set "expanded to top-300 death-associated DEGs when sparse" | The 20 non-immune genes in `S04_candidate_genes.csv` are **exactly** the intersection of the top-50 by degree (`S03_hub_degree.csv`) with Mars1 DEGs — a degree-based expansion, not a death-association expansion | **MISMATCH (methods text)** |
| V10 | §3.3 | "Degree-centrality and the tri-method ML consensus **converged** on six hub genes" | Degree ranks: FIS1 **12**, CD74 **595**, HLA-DQA1 **1102**, FCGR3A **1516**, CD14 **1766**, HAVCR2 **1927** (`S03_hub_degree.csv`, 2,000 genes). Five of six hubs are not in the top-50 that §2.4 defines as the co-expression hub | **OVERSTATED** |
| V11 | §3.4 | "Calibration and decision-curve analytics [18] for the **external** score are in Fig. S06 (`04_figures/S06_dca.png`)" | The image is a decision curve titled "Decision curve (28d death)" for the **Hub score** on the discovery cohort. It contains no calibration plot and no external-cohort curve. Its net-benefit curve lies **below the treat-none baseline** from threshold ≈0.15 to 0.9, unremarked in the text | **WRONG figure description** |
| V12 | `10_genetics_mr_design.md` §3.1 (companion supplement) | "four of five assessable hubs give protective estimates concordant across all three methods" | 28-day-death signs: CD74 IVW 1.119 / Egger 1.093 / WM 0.970 (mixed); HAVCR2 Egger 1.010 (>1). Concordant across all three: **3** (HLA-DQA1, CD14, FIS1). The manuscript's "three of five" is correct; the supplement is stale | **Supplement WRONG** |
| V13 | `10_genetics_mr_design.md` §3.1 | CD14 Egger "BH-FDR 0.026 across all 15 gene × outcome Egger tests" | `10_genetics_mr_outcome5086_28ddeath.csv` `p_fdr_bh` = **0.0766**; no file contains 0.026 | **WRONG** |
| V14 | `10_genetics_mr_design.md` §3.3 | CD74 critical-care IVW "BH-FDR ≈ 0.21 across all 15 gene × outcome tests" | `p_fdr_bh` = **0.0701** (0.0140 × 15 / rank 3). 0.21 is the rank-1 BH value | **WRONG** |
| V15 | §2.10 / §5.2 | CD74 susceptibility MR-Egger "*P*=1.7×10⁻⁴" | Stored *P* = 1.648438×10⁻⁴ → rounds to **1.6×10⁻⁴** (intercept *P* 1.0×10⁻⁴ is correct: 0.000100) | Minor rounding |
| V16 | §4 line 181 | "no primary IVW estimate is significant**,** We therefore present…" | Sentence-join typo producing an ungrammatical sentence in the Discussion | Typo |

---

## § 2. Findings

---

### F1. Every MR-Egger *P*-value in the study is computed from a normal deviate instead of a *t* distribution with df = n−2, which destroys all three headline MR signals — **Tier 0**

**【Problem】** The MR-Egger *P*-values (and their BH *q*-values) reported in §2.10, §3.10, §5.2 and Table 3 assume a standard normal sampling distribution, but MR-Egger with *n* instruments has n−2 residual degrees of freedom, so every Egger significance claim — and the entire "three CD74 tests reach *q*<0.05" statement — is quantitatively false.

**【Evidence】** Recomputed from the repository's own files:
- All 30 IVW and 15 Egger *P*-values in the three MR CSVs reproduce `2·(1−Φ(|β/SE|))` to within 1.6×10⁻¹⁵, i.e. they are z-test *P*-values.
- `10_genetics_mr_outcome4982_criticalcare.csv` row 2 (CD74, MR-Egger, nsnp=3): β=0.798285, SE=0.111074, reported *P*=6.6258×10⁻¹³ = normal two-sided *P* at z=7.187. The same row records `Q_df = 1.0`, i.e. the pipeline itself knows the residual df is n−2 = 1. Correct *P* = 2·sf_t(7.187, df=1) = **8.80×10⁻²**.
- `10_genetics_mr_outcome5086_28ddeath.csv` row 7 (CD14, MR-Egger, nsnp=6): reported *P* = 5.1096×10⁻³ (normal); correct *t*(4) *P* = **4.88×10⁻²**.
- `10_genetics_mr.csv` row 1 (CD74 susceptibility, MR-Egger, nsnp=3): reported 1.648×10⁻⁴ (normal); correct *t*(2) *P* = **0.165**.
- Recomputing the pre-specified 45-test BH family with corrected Egger *P*-values: **1** test survives *q*<0.05 (CD74 critical-care weighted median, *q*≈3.0×10⁻¹⁷) instead of the reported **3**; CD74 critical-care Egger *q*: 1.49×10⁻¹¹ → **0.79**; CD74 susceptibility Egger *q*: 2.47×10⁻³ → **0.90**; CD14 28-day-death Egger *q*: 5.75×10⁻² → **0.73**.
- Note this is not the reference behaviour: the standard MR-Egger implementation returns the OLS *t*-test *P*-value at df = n−2, and the manuscript's own `Q_df` column already carries n−2.

**【Why it matters】** This is the single most consequential defect in the paper. §3.10, §5.2 and the Discussion all build on "CD74 reaches *q*<10⁻¹¹ … the strongest MR association in the study" and on a nominally significant, pleiotropy-robust CD14 mortality signal. After correction, **no MR-Egger result is significant at all**, the only surviving family-corrected test is the CD74 critical-care weighted-median estimate that the manuscript itself argues is direction-reversed and instrument-starved, and the honest summary of the MR layer becomes "uniformly null after correction". The paper's framing ("hypothesis-generating") survives, but every number in the MR section is wrong, and a reviewer who recomputes them will conclude the analysis was not understood by its own author.

**【Specific fix】** Recompute all Egger (and, for completeness, IVW) *P*-values as two-sided *t* with df = n−2 and df = n−1 respectively, regenerate `10_mr_bh_family.csv`, and replace the affected sentences. Paste-ready replacements:
- §2.10: "Under the pre-specified full family of 45 tests (five assessable genes × three estimators × three outcomes; FCGR3A was not assessed for insufficient instruments), with MR-Egger *P*-values computed from the *t* distribution at n−2 degrees of freedom, **no test reached q<0.05**; the smallest family-corrected value was the CD74 critical-care weighted median (*q*≈3×10⁻¹⁷), an estimate that rests on three instruments and points opposite to the expression-level model."
- §3.10, first sentence of the MR-Egger discussion: "For CD14 the MR-Egger estimate was directionally protective (OR 0.906, *t*(4) *P*=0.049) but did not approach significance under the pre-specified 45-test family correction (*q*≈0.73)."
- §3.10 / §5.2: "Against critical care, the CD74 association (IVW OR 2.222, *P*=0.014) did not survive family correction for any estimator once Egger *P*-values were computed at their correct degrees of freedom (Egger *t*(1) *P*=0.088, family *q*=0.79; weighted median *q*≈3×10⁻¹⁷), and it points opposite to the Mars1 expression-level model; we therefore report the MR layer as uniformly null after correction."

---

### F2. FIS1 — one of the six hub genes — is strongly **up**-regulated in Mars1, contradicting the directionality check asserted in three places — **Tier 0**

**【Problem】** The manuscript states in §2.8, §3.3 (twice) and in the S11 protocol's central hypothesis that all six hub genes are down-regulated in Mars1, but the repository's own differential-expression table shows FIS1 is the most strongly *up*-regulated gene of the six.

**【Evidence】** `S01_mars1_deg.csv`: FIS1 logFC = **+1.2614** (Mars1 vs Other), t = +17.157, stored P = 0.0 (artifact; recomputed *P* ≈ 2.0×10⁻⁵⁶ at df≈800). For comparison the five immune hubs are −0.35 to −0.89. Independent corroboration inside the repository: `08_positive_control_check.csv` row 2 (`hub_KO_phenocopies_immunoparalysis = True`) lists only `['HAVCR2','HLA-DQA1','CD14','FCGR3A','CD74']` as "hub 在 Mars1 下调" — FIS1 is absent from the pipeline's own directionality list, and FIS1 appears in none of the 25 rows of `S01_immunoparalysis_direction.csv`, so the §3.1 citation in "all six hub genes are themselves down-regulated in Mars1 (§3.1)" cannot even be sourced. The false claim appears at: §2.8 ("a directionality check confirmed the six hub genes are themselves Mars1-down"), §3.3 ("all six hub genes are themselves down-regulated in Mars1 (§3.1)" and "its down-regulation is directionally concordant with the immunosuppressed program"), and `03_results/11_validation_design.md` line 18–20 ("the six hub genes … are co-downregulated in immunoparalysis").

**【Why it matters】** The directionality check is the only "sanity" evidence offered that the hub set is internally coherent with the immunoparalysis program, and it is offered as justification for the virtual-knockdown framing of the whole project. For one of six hubs the sign is not merely unconcordant — it is strongly inverted (|logFC| = 1.26, the largest of any hub). §3.3 itself concedes FIS1 is "most plausibly a co-expression passenger", yet the surrounding sentences still claim its down-regulation supports the program. This is exactly the kind of internal contradiction that, once found, makes a reviewer distrust every other directional claim.

**【Specific fix】** Replace §3.3's directionality sentences with: "Directionality check: five of the six hub genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) are down-regulated in Mars1 (§3.1), so their loss-of-function is directionally concordant with the immunosuppressed program; the sixth, FIS1, is **up**-regulated in Mars1 (logFC = +1.26, adj.P ≈ 3×10⁻⁵⁴), consistent with its interpretation as a co-expression passenger rather than a participant in the down-regulated immunosuppressed axis. This is a consistency check, not an independent perturbation control, and is not used to validate the repositioning pipeline." Make the matching edits in §2.8 ("a directionality check confirmed that five of the six hub genes are Mars1-down and flagged FIS1 as directionally discordant") and in `11_validation_design.md` line 18 ("five of the six hub genes are co-downregulated in immunoparalysis; FIS1 is up-regulated and serves as a negative-directionality control").

---

### F3. The IFN-γ positive-control gate is reported as 5/5 but the repository's own gate record says 4/5 — **Tier 1**

**【Problem】** The abstract (English and Chinese) and §3.7 report that IFN-γ rescued 5/5 antigen-presentation genes, while the checkpoint file that implements the gate records 4/5, because HLA-DQB1 fails the study's own \|logFC\|≥0.3 DEG rule.

**【Evidence】** `08_positive_control_check.csv` row 1: `IFN_gamma_rescues_antigen_presentation_axis = True`, detail "救回 **4/5** 抗原呈递基因: ['HLA-DRA','HLA-DRB1','HLA-DQA1','CD74']". `S01_immunoparalysis_direction.csv` row 21: HLA-DQB1 logFC = −0.2027, adj.P = 0.0174, `DEG_0.3 = False` — it is FDR-significant but below the fold-change threshold that defines the Mars1-down axis elsewhere in the paper. `08_candidates_drugs.csv` row 3 lists IFN-γ's five rescue genes as HLA-DRA;HLA-DRB1;HLA-DQA1;HLA-DQB1;CD74 out of 7 curated targets (rescue_fraction 0.714), which is where the manuscript's "5/5" comes from; the two files therefore use different denominators and the manuscript picked the more favourable one. The string "4/5" appears nowhere in the manuscript.

**【Why it matters】** The positive-control gate is one of the paper's three "positive anchors" (§1). A headline number in the abstract that contradicts the study's own checkpoint file is the kind of inconsistency that triggers a data-integrity query rather than a revision request. The gate still passes at 4/5 ≥ 3/5, so no conclusion changes — but the number must be corrected, and the two differing definitions (response-gene overlap vs DEG-thresholded axis) must be stated explicitly, because at present the reader cannot tell which denominator the "≥3/5" threshold applies to.

**【Specific fix】** Abstract (EN): "IFN-γ rescued 4/5 antigen-presentation genes passing the Mars1 DEG threshold in its curated set (HLA-DQB1 is FDR-significant but below the |logFC|≥0.3 axis threshold), satisfying the pre-specified ≥3/5 method-positive gate." §3.7: "IFN-γ [29] rescued 4/5 antigen-presentation genes in its curated set against the Mars1-down DEG axis (HLA-DRA, HLA-DRB1, HLA-DQA1, CD74; HLA-DQB1 is FDR-significant at adj.P = 0.017 but fails the |logFC|≥0.3 threshold), satisfying the method-positive gate (≥3/5)." Chinese abstract: "IFN-γ 逆转 4/5 个通过 Mars1 DEG 阈值的抗原呈递基因，满足预设的 ≥3/5 方法学阳性对照门控。"

---

### F4. CD74 critical-care weighted-median *P* is stored as exactly 0.0 and reported as "q≈0" — a floating-point cancellation artifact, not a probability — **Tier 1**

**【Problem】** The manuscript reports a family-corrected *q* of "≈0" (and "family *q* = 0" in §3.10) for the CD74 critical-care weighted-median test, but the stored *P* of exactly `0.000000e+00` is a `1 − CDF` underflow, and the probability recomputable from the same row's β and SE is 6.6×10⁻¹⁹ (family *q* ≈ 3×10⁻¹⁷).

**【Evidence】** `10_genetics_mr_outcome4982_criticalcare.csv` row 3: β=0.785890, SE=0.088495 → z=8.881 → *P* = 6.65×10⁻¹⁹ by the survival function; the stored `p` is `0.000000e+00` because Φ(8.881) rounds to 1.0 in double precision and `1 − 1.0 = 0`. The same artifact class produces the exact zeros in `S01_mars1_deg.csv` (CD14, FIS1) and the exact powers of two 2.2204×10⁻¹⁶ = 2⁻⁵² (HLA-DRB1) and 4.4409×10⁻¹⁶ = 2⁻⁵¹ (CD74, HLA-DMA), which are machine-epsilon quantizations, not computed probabilities. No *q*-value in a scientific paper should be printed as 0.

**【Why it matters】** A reader sees "q = 0" and reads it as infinite evidence; the true value, while still small, is finite and rests on three instruments whose weighted-median SE (0.088) is 3.7× smaller than the IVW SE (0.325) on the *same* three SNPs — itself a sign that the bootstrap SE is unstable at n=3. Reporting an impossible number invites the suspicion that the pipeline was not validated.

**【Specific fix】** Replace the *P*-value computation throughout with survival-function calls (`2*sf(|z|)` / `2*sf(|t|, df)`), regenerate the MR and DEG tables, and rewrite: "the CD74 critical-care weighted-median test had *P* = 6.6×10⁻¹⁹ and family *q* = 3×10⁻¹⁷ (the smallest family-corrected value in the study), although with three instruments its bootstrap SE is unstable and the estimate points opposite to the expression-level model."

---

### F5. Table 1's "CD14 adj.P ≈ 0 (P<1e-300)" is an artifact; the value recomputable from the file's own t column is adj.P ≈ 2.8×10⁻²⁰ — **Tier 1**

**【Problem】** The manuscript converts a floating-point zero into a substantive claim ("P<1e-300", "P≈0, underflow") that is off by roughly 280 orders of magnitude and is not supported by any file.

**【Evidence】** `S01_mars1_deg.csv` row for CD14: t = −9.7145. With the df ≈ 800 implied by §2.2 (n = 802), *P* = 3.65×10⁻²¹ and BH adj.P = 2.78×10⁻²⁰ (recomputed over all 11,519 genes). The stored `P.Value`/`adj.P.Val` of `0.0` is the `1 − CDF` artifact described in F4; the neighbouring stored values 2.2204×10⁻¹⁶ (HLA-DRB1) and 4.4409×10⁻¹⁶ (CD74) are exact powers of two, confirming saturation. Recomputing the whole table from the *t* column leaves the DEG count at 3,597 — so the correction changes no call, only the printed numbers.

**【Why it matters】** "P<1e-300" is not a rounding choice; it is a fabricated-appearing magnitude that any statistical reviewer will flag immediately, and it is repeated in the abstract-adjacent Table 1. The corrected value is still highly significant, so there is nothing to protect by keeping the artifact.

**【Specific fix】** Table 1 CD14 row: `| CD14 | −0.77 | 2.8×10⁻²⁰ | monocyte receptor |`. §3.1 sentence: "CD14 Δ=−0.77 (adj.P=2.8×10⁻²⁰)". Additionally regenerate all *P*/adj.P columns in `S01_mars1_deg.csv`, `S01_deg_sepsis_vs_ctrl.csv` and `S01_immunoparalysis_direction.csv` using survival-function tail probabilities so that no value is stored as exactly 0.

---

### F6. The methods text misdescribes how the candidate set was expanded, and §3.3 overstates network/ML "convergence" — **Tier 2**

**【Problem】** §2.5 says the candidate set was "expanded to top-300 death-associated DEGs when sparse", but the actual expansion visible in the output is the top-50 by co-expression degree intersected with Mars1 DEGs; and §3.3's claim that degree centrality and the tri-method consensus "converged on six hub genes" is not supported, since five of the six hubs are not in the top-50 degree list at all.

**【Evidence】** `S03_hub_degree.csv` (2,000 genes) degree ranks: FIS1 12, CD74 595, HLA-DQA1 1102, FCGR3A 1516, CD14 1766, HAVCR2 1927. `S04_candidate_genes.csv` (35 genes) contains exactly 20 non-immune-set genes, and those 20 are exactly `top50(degree) ∩ Mars1-DEG` (GATA1, CGB, DPM2, EPB49, BCL2L1, CDC34, KRTAP5-2, ELOF1, FIS1, DES, GMPR, BAT3, C2orf24, DUX4, FKBP8, FOXO4, FUNDC2, GLYATL1, HPS1, MAF1) — a degree-based, not death-association-based, expansion. `S05_hub_genes.csv` records only the three ML selectors and no degree column.

**【Why it matters】** "Converged" implies two independent lines of evidence selected the same six genes; in fact one line (degree) contributed exactly one hub, and the other five entered through the immune-set branch of the candidate pool. A methods section that does not match its own outputs is an independent reproducibility defect even when the result is defensible.

**【Specific fix】** §2.5: "Within the candidate set (Mars1-DEG ∩ consensus immune set, 15 genes), expanded with the top-50 co-expression-degree genes that are also Mars1 DEGs (20 genes; 35 candidates in total), three independent selectors operated…". §3.3 first sentence: "The tri-method ML consensus recovered six hub genes: CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2 and FIS1; five entered through the immune-set branch of the candidate pool and one (FIS1, degree rank 12 of 2,000) through the co-expression-degree expansion."

---

### F7. A palindromic SNP is retained in all three harmonised instrument tables despite a stated drop policy — **Tier 1**

**【Problem】** §2.10 states that "Palindromic, strand-ambiguous and allele-incompatible SNPs were dropped during harmonisation", yet rs6084653 (effect allele G / other C — a strand-ambiguous A/T–G/C palindromic pair) is present as a FIS1 instrument in all three `*_harmonised.csv` files, and no column flags palindromic status or allele-frequency-based resolution.

**【Evidence】** `10_genetics_mr_harmonised.csv`, `10_genetics_mr_outcome5086_harmonised.csv`, `10_genetics_mr_outcome4982_harmonised.csv`, row 25: rsid rs6084653, ea_e = G, nea_e = C, eaf_e = 0.3664, eaf_o = 0.3873. I checked all 27 retained instruments across the three files; rs6084653 is the only palindromic pair. The two sentences in §2.10 also contradict each other ("resolved by allele frequency and dropped when strand could not be determined" vs "were dropped … per TwoSampleMR defaults").

**【Why it matters】** Retention may be defensible — both allele frequencies are far from 0.5, so the strand is in principle resolvable — but the manuscript asserts a policy the data contradict, and a reader cannot verify the resolution because no flag column exists. STROBE-MR item 9b is explicitly invoked in this section, so the disclosure must be exact.

**【Specific fix】** Add a `palindromic` and `af_resolved` column to each harmonised table, and replace the two §2.10 sentences with: "Palindromic (strand-ambiguous) SNPs were resolved by allele frequency and retained when the reported EAF was >0.05 away from 0.5 and consistent between exposure and outcome; SNPs that could not be resolved were dropped. One retained instrument (rs6084653, FIS1) is palindromic and was resolved by allele frequency (EAF 0.366 exposure vs 0.387 outcome); it is flagged in the harmonised tables."

---

### F8. The decision-curve figure is misdescribed, contains no calibration analysis, and shows the score is clinically useless — unremarked — **Tier 2**

**【Problem】** §3.4 states that "Calibration and decision-curve analytics [18] for the external score are in Fig. S06", but the referenced image is a decision curve for the **hub score on the discovery cohort**, contains no calibration plot, and shows the model's net benefit falling **below the treat-none baseline** over nearly the entire threshold range — a negative result the text never mentions. Reference [18] is an empirical-calibration paper, not a decision-curve reference.

**【Evidence】** `04_figures/S06_dca.png`: title "Decision curve (28d death)", single series "Hub score", plotted against "None" and "All" references; the blue curve crosses below the dashed treat-none line at threshold ≈0.15 and reaches net benefit ≈−2.2 at threshold 0.9. No calibration curve exists anywhere in `04_figures/` (10 files enumerated). Reference [18] = Schuemie et al., *Statistics in Medicine* 2013 (empirical calibration of *P*-values). The three figure files actually called out (`S06_dca.png`, `fig_s09_external_roc.png`, `fig_s10_l1000_rescue.png`) all exist; the other seven (`S01_roc_28d_mars1.png`, `S02_score_vs_endotype.png`, `S03_eigengene_trait_cor.png`, `S03_top_hub.png`, `S06_roc_cv.png`, `S06_roc_train.png`, `S07_celltype.png`) are never referenced, and the label "Fig. S06" is ambiguous across three S06 files.

**【Why it matters】** Citing a decision-curve figure that contradicts the prognostic claim, attributed to the wrong cohort and the wrong method, is the kind of detail that costs credibility disproportionately. Either the DCA is reported honestly (it is negative) or it is removed; it cannot be cited as supporting analytics.

**【Specific fix】** Either delete the sentence, or replace it with: "Decision-curve analysis of the hub score for 28-day death on the discovery cohort (`04_figures/S06_dca.png`, decision-curve analysis per Vickers & Elkin) shows net benefit below the treat-all and treat-none strategies at nearly all threshold probabilities above 0.15, so the score supports risk stratification but not treatment-selection decisions; no calibration plot was generated." If kept, correct the citation: [18] should be replaced by a DCA reference (e.g., Vickers AJ, Elkin EB. Decision curve analysis: a novel method for evaluating prediction models. Med Decis Making. 2006;26(6):565-575, doi:10.1177/0272989X06295361) and Schuemie et al. should either be cited where empirical calibration is actually discussed or removed.

---

### F9. Reference-list defects — **Tier 3**

**【Problem】** Two of 31 references are absent from the project's DOI audit file, two bibliographic fields contradict the project's own verified source table, one reference lacks volume/pages, and reference [18] is cited for a method it does not describe.

**【Evidence】** (a) `reference_doi_audit.csv` contains 29 DOIs, all "OK"; refs [30] (Bo L, doi:10.1186/cc10031) and [31] (Burgess, doi:10.1002/gepi.21998) are missing — [31] is load-bearing for the sample-overlap caveat in §2.10/§3.10/§5.2. (b) Ref [11]: manuscript "JCI Insight. 2018;**3(5)**:e98960" vs `08b_clinical_translation.csv` "JCI Insight. 2018;**3(14)**:e98960" — the project's own Crossref-verified table says 3(14). (c) Ref [23]: manuscript "Leukemia. **2011**;26(6):1425-1429" vs `08b_clinical_translation.csv` "Leukemia. **2012**;26(6):1425-1429" (the DOI 10.1038/leu.2011.359 is a 2012 print issue). (d) Ref [21]: "International Journal of Epidemiology. 2016;:dyw220" — no volume/page. (e) Ref [18] cited at §3.4 for decision-curve analytics (see F8). (f) DOI case inconsistencies vs the audit file: [4] `10.1016/s2213-2600(17)30294-1` vs audit `…/S2213-2600…`; [12] `10.1164/rccm.200903-0363oc` vs audit `…0363OC`. All 31 references are cited in the text and all 31 text citations resolve — no orphan or missing reference.

**【Why it matters】** Minor individually, but a submission that advertises a DOI-verification pass (§5.7: "DOIs verified 2026-09-26") while two references bypass that pass and two fields contradict the verification table undermines the audit claim itself.

**【Specific fix】** Add rows for 10.1186/cc10031 and 10.1002/gepi.21998 to `reference_doi_audit.csv` with Crossref confirmation; change ref [11] to "2018;3(14):e98960", ref [23] to "2012;26(6):1425-1429", ref [21] to "Int J Epidemiol. 2017;46(2):461-468. doi:10.1093/ije/dyw220" (confirm against Crossref before resubmission); normalise DOI case to the audit file's form.

---

### F10. Stale numbers in companion files that would ship as supplements — **Tier 3**

**【Problem】** `10_genetics_mr_design.md` and `journal_targeting.csv` carry pre-final-round values that now contradict the manuscript and the result files.

**【Evidence】** `10_genetics_mr_design.md` line 62: "**four of five** assessable hubs give protective estimates concordant across all three methods" (correct count: **3**; the manuscript is right, the supplement is wrong — see V12). Line 65: CD14 Egger "BH-FDR **0.026**" (file value 0.0766). Line 88: CD74 critical care "BH-FDR ≈ **0.21**" (file value 0.0701). `journal_targeting.csv` row 1 fit_rationale: "本稿缺功能验证+**MR未跑**" — the MR has since been run and is reported in §3.10. These are precisely the "consistency-gate residue" pattern: values updated in the manuscript but not in the second location.

**【Why it matters】** If the supplement and the journal-targeting memo accompany submission, a reviewer will see the manuscript and its own supplement disagreeing about the central MR result count.

**【Specific fix】** Update `10_genetics_mr_design.md` §3.1 to "three of five assessable hubs give protective estimates concordant across all three methods", correct the two BH values to 0.077 and 0.070 (and, after F1 is fixed, regenerate them entirely), and refresh `journal_targeting.csv` row 1 to "本稿已完成外部验证与 MR（Tier-3），仍缺功能验证" — or drop the internal memo from the submission package.

---

### F11. The repository's audit script passes while checking almost none of the numbers the manuscript headlines — **Tier 2**

**【Problem】** `02_scripts/python/check_audit_assertions.py` exits green ("All audit assertions passed") but contains only three assertions: max I² ≤ 0.51, BH table row count = 45, and existence of nine file paths. It checks **zero** of the DEG counts, gene counts, Δ values, AUCs, concordance fractions, instrument counts, or MR *P*/q values that the manuscript headlines.

**【Evidence】** Script content (77 lines): assertion 1 recomputes max I² across the three MR CSVs (passes at 0.502); assertion 2 counts rows in `10_mr_bh_family.csv` (45); assertion 3 checks path existence for nine files. It does not recompute the 3,597/448 DEG counts, the 23/25/22/21 immune-gene counts, the −0.79 median, any AUC, the IFN-γ gate fraction (F3 would have caught it), the FIS1 direction (F2 would have caught it), or the MR *P*-value distribution (F1 would have caught it). The script's own docstring says its purpose is to guard against "a *stated numeric range* in the text that does not match the cited CSV".

**【Why it matters】** The green pass creates false assurance for exactly the class of defect this round contains. Two of the three most serious findings (F1, F3) are mechanically detectable and would have been caught by a dozen lines of assertion code.

**【Specific fix】** Extend the script with: (i) recount `DEG_0.3` in both DEG CSVs and assert 3597/448; (ii) recount the direction file's down / FDR<0.05 / down∧significant counts and assert 23/22/21; (iii) assert FIS1 logFC > 0 in `S01_mars1_deg.csv` so the directionality claim can never silently rot; (iv) assert `rescue_fraction` for the IFN-γ gate equals the value in `08_positive_control_check.csv`; (v) for every MR row, recompute `2*sf(|β/SE|, df)` with df = n−2 (Egger) / n−1 (IVW) and fail if the stored *P* differs by more than 1e-9, and fail if any stored *P* equals exactly 0; (vi) assert per-gene instrument counts in `*_harmonised.csv` equal (3,4,6,6,8) with FCGR3A absent.

---

### F12. Smaller wording, consistency and format items — **Tier 3**

**【Problem】** (a) A sentence-join typo in the Discussion; (b) the in-cohort Mars1 mortality is not the quoted 39%; (c) LAG3 is described as part of an "up-regulated exhaustion axis" although it is nowhere near significance; (d) the 22-gene L1000 query set is not enumerable from any shipped file.

**【Evidence】** (a) Line 181: "no primary IVW estimate is significant**,** We therefore present…" — two sentences fused. (b) §1 quotes "Mars1 … carries a 39% 28-day mortality" from Scicluna et al. [4]; recomputed from this cohort (`S02_immunoparalysis_score.csv`): 45/132 = **34.1%**. The citation is legitimate but the juxtaposition invites the reading that the re-analysed cohort reproduces 39%. (c) §3.1: "an up-regulated T-cell exhaustion axis (PDCD1, LAG3)" — LAG3 logFC = +0.035, adj.P = 0.552 (`S01_immunoparalysis_direction.csv` row 26); only PDCD1 is significant. (d) §3.9 states the L1000 query was "the 22 consensus immune genes measurable on the L1000 platform" (25 minus HAVCR2, FCGR3A, TIGIT), but no file in `03_results/` enumerates those 22 symbols, so the query set cannot be audited.

**【Why it matters】** Each is small; together they are the residue pattern that suggests the text and the outputs are drifting apart, which is the specific risk this manuscript's §7 provenance table is designed to counter.

**【Specific fix】** (a) Replace with: "None of this reaches the level of a demonstration: no primary IVW estimate is significant. We therefore present the MR layer as hypothesis-generating rather than as either a positive or a refutation." (b) Add after the 39% clause: "(34% in the GSE65682 re-analysis used here: 45/132 deaths)". (c) Replace with: "an up-regulated T-cell exhaustion marker (PDCD1, Δ=+0.16, adj.P=3.0×10⁻¹⁰; LAG3 shows a non-significant trend in the same direction, adj.P=0.55)". (d) Ship a `S08_l1000_query_genes.csv` with the 22 symbols and their Mars1 directions, and add it to the §7 provenance table.

---

## § 3. Stands up (verified correct — do not change)

1. **Sample and endotype accounting.** 802 samples; 760 sepsis / 42 healthy; Mars1 = 132, Mars2 = 176, Mars3 = 118, Mars4 = 53, unassigned = 323; death_28d 1.0 = 114, 0.0 = 365, unassigned = 323; 479 with endotype + outcome. All recomputed from `01_data/GSE65682/GSE65682_pheno.csv` and `S02_immunoparalysis_score.csv` and all match §2.1 exactly. External cohort: 106 samples, 52 deaths, 54 survivors, 29/30 genes mapped, HLA-DQA1 missing — all match `09_external_validation.csv` and `09_ext_risk_scores.csv`.
2. **The immunoparalysis count claims.** 23/25 directionally down, 22/25 FDR<0.05, 21 both down and significant — I recounted all three from `S01_immunoparalysis_direction.csv` (25 rows; 23 `Mars1_down`; 22 with adj.P<0.05; 21 in both sets). Suspected an off-by-one in the "21" figure; it is exactly right. The DEG totals 3,597 (Mars1, |logFC|≥0.3) and 448 (sepsis-vs-healthy) both recount exactly, and 3,597 is stable even when the BH adjustment is fully recomputed from the *t* column (F5), so the count does not depend on the *P*-value artifact.
3. **Table 1 effect sizes and *P*-values (except CD14).** HLA-DRB1 −0.8925/1.07×10⁻¹⁵, CD74 −0.7578/2.08×10⁻¹⁵, FCGR3A −0.6097/9.05×10⁻¹¹, HAVCR2 −0.3488/2.84×10⁻¹³, PDCD1 +0.1619/3.00×10⁻¹⁰, ITGAM −0.2084/1.68×10⁻³, LYZ −0.2561/3.56×10⁻⁶, HLA-DRA −0.4689/3.77×10⁻⁷ — every Δ and every adj.P in Table 1 matches to the printed precision. Only the CD14 row (F5) is wrong.
4. **Immune-function score.** Mars1 median −0.7917 → "−0.79"; full-cohort range −3.6496 to 3.8616 → "−3.65 to 3.86"; Mars1 endotype AUC for 28-day death 0.5782 → "0.578". All match. (Note for the design reviewer: the Mars2 median is −0.7520, only 0.04 below Mars1 — the "lowest in Mars1" statement is true but the margin is thin; see Questions.)
5. **Signature and external validation numbers.** CV AUC 0.65856 → 0.659; training 0.74951 → 0.750; external oriented-sum 0.6382 (CI 0.5317–0.7475) → 0.638 (0.532–0.748); locked L1 0.5848 (CI 0.4687–0.6959) → 0.585 (0.469–0.696); IRG benchmark 0.604; the "0.034 above the benchmark" gap (0.6382−0.604=0.0342) and the "0.138 above chance" gap are both arithmetically right. `fig_s09_external_roc.png` depicts exactly these values (n=106, 52 deaths; 0.638 / 0.585 / 0.604). I looked for inflation of the external number and found none.
6. **Cell-type localisation and repositioning tables.** CD14 r=0.773, FCGR3A 0.491, CD74→dendritic 0.690, HAVCR2 0.298, HLA-DQA1→B-cell 0.681; axis means CD4 0.618 / CD8 0.582 / dendritic 0.459 — all match §3.6. All seven Table 2 concordance values and n_rescue/n_target ratios match `08_candidates_drugs.csv` (the IFN-γ gate fraction is the one exception, F3).
7. **LINCS L1000 layer.** 20,413 compounds; wtcs = rescue × √22 verified exactly across all 20,413 rows (ratio 4.690416 = √22 to 7 figures); lenalidomide rescue 0.0439, rank 5,435, top 26.6%; azithromycin 0.0133, rank 9,152; prednisone 0.1364/rank 651; dexamethasone 0.0315/rank 6,808; top rescue 0.3182 → "0.32"; background mean 0.0064 / median 0.0055 / 53.6% > 0 — the §3.9 text is accurate on every one of these, including the algebraic-identity caveat that I suspected was hiding a second independent metric (it is not). All seven named plausible modulators (mocetinostat, entinostat, geldanamycin, alvespimycin, pravastatin, simvastatin, fluvastatin) are present in `S08_l1000_immuno_overlap.csv`.
8. **MR instruments and Table 3/Table 4 cells.** 27 instruments retained (CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8; FCGR3A not assessed) — counted in all three harmonised files. Median F per gene: 35.39, 168.12, 45.65, 36.44, 75.01 — matches Table 3's 35.4/168.1/45.7/36.4/75.0. All 15 IVW ORs, CIs and *P*-values in Table 4, all 12 per-outcome I² values, the max I² 0.5018 (FIS1 critical care) and the primary-outcome I² range 0.00–0.29 all match. The BH family table has exactly 45 rows and, *as currently computed*, contains exactly the three *q*<0.05 tests and the *q* values 1.49×10⁻¹¹ / 0 / 2.47×10⁻³ / 0.0575 that the manuscript quotes — the defect is upstream of the BH arithmetic (F1, F4), not in it.
9. **Provenance and reference plumbing.** All §7 file paths exist, including the three `01_data/` raw inputs, `S08_l1000_rescue_wtcs.npy`, the three `s10_run_log*.txt` files and `05_reports/tier1_summary.txt`. All 10 figure files exist. All 31 references are cited in the text and all 31 text citations resolve to list entries; the 29 audited DOIs match the list (F9 covers the exceptions).

---

## § 4. Questions for the authors

1. Which *t* degrees of freedom were used for the MR-Egger *P*-values, and why does the reported *P* for CD74 critical care reproduce a standard normal deviate to 15 decimal places while the same row records `Q_df = 1.0`? If a normal approximation was deliberate, please provide the justification for using it at n = 3 instruments.
2. Was the weighted-median SE for CD74 critical care bootstrapped from three SNPs with 2,000 resamples (as stated in `10_genetics_mr_design.md`)? Please provide the bootstrap distribution or the resampling seed, because the resulting SE (0.088) is 3.7× smaller than the fixed-effect IVW SE (0.325) on the same three SNPs.
3. Was the §2.5 candidate expansion computed from the top-300 death-associated DEGs or from the top-50 co-expression-degree genes? The 20 non-immune genes in `S04_candidate_genes.csv` match the latter exactly; if both were applied, which produced the 20?
4. Was rs6084653 (FIS1, G/C palindromic) retained by allele-frequency resolution, and can you confirm no other palindromic SNP was dropped silently? Please provide the per-SNP drop-list that §2.10 says "remains available on request".
5. The 39% Mars1 28-day mortality in the Introduction is cited to Scicluna et al.; the GSE65682 re-analysis gives 45/132 = 34.1%. Is the 39% intended as a literature figure only, and should the two be distinguished explicitly?
6. Is there a reason the 22-gene L1000 query set and the 70-gene pre-defined immune panel of §2.6 are not present as files in `03_results/`? Both are inputs to headline analyses and neither is auditable from the shipped tables.
7. Does `S06_dca.png` correspond to a current or a superseded analysis? Its series label ("Hub score") and cohort (discovery) do not match the §3.4 sentence that cites it.

---

## § 5. What I actually checked

**Files read in full:** `05_reports/manuscript.md` (all 288 lines, including the four long lines the display truncates), `03_results/S01_immunoparalysis_direction.csv`, `S01_immunoparalysis_genes_in_mars1.csv`, `S01_mars1_deg.csv` (11,519 rows), `S01_deg_sepsis_vs_ctrl.csv` (11,519 rows), `S01_mars1_stratification.csv`, `S02_immunoparalysis_score.csv` (802 rows), `S03_hub_degree.csv` (2,000 rows), `S03_modules.csv`, `S03_module_trait_cor.csv`, `S03_key_module_genes.csv`, `S04_candidate_genes.csv`, `S05_hub_genes.csv`, `S06_signature_genes.csv`, `S06_auc_compare.csv`, `07_hub_celltype.csv`, `07_axis_celltype.csv`, `08_candidates_drugs.csv`, `08_positive_control_check.csv`, `08_disease_signature.csv`, `08b_clinical_translation.csv`, `S08_l1000_candidate_scores.csv`, `S08_l1000_positive_control.csv`, `S08_l1000_immuno_overlap.csv` (40 rows), `S08_l1000_rescue_trtcp.csv` (20,413 rows), `09_external_validation.csv`, `09_external_validation_coef.json`, `09_ext_risk_scores.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, `10_mr_bh_family.csv` (45 rows), the three `10_genetics_mr*_harmonised.csv` (27 rows each), `10_genetics_mr_design.md`, `11_validation_design.md`, `reference_doi_audit.csv`, `journal_targeting.csv`, `generated_references.md`, `02_scripts/python/check_audit_assertions.py`, `01_data/GSE65682/GSE65682_pheno.csv`.

**Figures opened:** `S06_dca.png`, `fig_s09_external_roc.png` (image content inspected against the manuscript descriptions); the remaining eight files confirmed present.

**Recomputation performed:** DEG counts under both thresholds in both contrasts; all down/significant/down∧significant counts in the direction file; per-endotype score medians, full range and per-endotype 28-day mortality; every Δ and adj.P in Table 1; per-gene Mars1 logFC for all six hubs (including FIS1's sign); degree ranks of the six hubs and the exact composition of `S04_candidate_genes.csv` against the top-50 degree list; all AUCs and CIs against `S06_auc_compare.csv` and `09_external_validation.csv`; all cell-type correlations; all seven repositioning concordances and the gate fraction; all L1000 ranks, scores, the √22 algebraic identity, background moments and the named-compound lookups; MR instrument counts and per-SNP F statistics; median F per gene; every OR, CI, *P*, Q, I² and intercept *P* in Tables 3 and 4; max I² and the primary-outcome I² range; the BH family arithmetic; and — the load-bearing recomputation — the *P*-value distribution of all 45 MR tests against both normal and *t*(n−1/n−2) references, with the 45-test BH family re-run under corrected Egger *P*-values. Exact-zero and powers-of-two *P*-values were identified in both the MR tables and the DEG tables, and the CD14/FIS1 *P*-values were recomputed from the stored *t* statistics at df ≈ 800.

**Discrepancies found:** the 16 rows of §1, of which V1–V8 are substantive (four MR *q*-values, one MR family-count claim, one hub-gene direction, one positive-control fraction, one DEG *P*-value) and V9–V16 are methods-text, supplement-staleness, figure-description and format defects. The repository's own audit script passes but covers none of these.

---

## § Appendix A. Full recomputation of all 15 MR-Egger tests (basis of F1)

Reported *P* is the value stored in the MR CSVs; it reproduces the two-sided normal
deviate `2·(1−Φ(|β/SE|))` to ≤1.6×10⁻¹⁵ in every row. Correct *P* uses *t* at df = n−2.
Family *q* is the BH correction over the full pre-specified 45-test family.

| Outcome | Gene | n | β | SE | Reported *P* | Correct *t* *P* | Reported family *q* | Correct family *q* |
|---|---|---|---|---|---|---|---|---|
| 4982 crit care | CD74 | 3 | 0.798285 | 0.111074 | 6.63×10⁻¹³ | **8.80×10⁻²** | 1.49×10⁻¹¹ | **0.79** |
| 4980 suscept | CD74 | 3 | 0.111478 | 0.029589 | 1.65×10⁻⁴ | **0.165** | 2.47×10⁻³ | **0.90** |
| 5086 28d death | CD14 | 6 | −0.098770 | 0.035275 | 5.11×10⁻³ | **4.88×10⁻²** | 5.75×10⁻² | **0.73** |
| 4982 crit care | CD14 | 6 | 0.143341 | 0.082076 | 8.07×10⁻² | 0.156 | 0.52 | 0.90 |
| 4980 suscept | HAVCR2 | 6 | −0.101002 | 0.064040 | 0.115 | 0.190 | 0.60 | 0.94 |
| 5086 28d death | HLA-DQA1 | 4 | −0.047094 | 0.067591 | 0.486 | 0.558 | 0.94 | 0.97 |
| 4982 crit care | HLA-DQA1 | 4 | −0.029841 | 0.057664 | 0.605 | 0.656 | 0.94 | 0.97 |
| 4980 suscept | HLA-DQA1 | 4 | −0.015479 | 0.037840 | 0.683 | 0.722 | 0.94 | 0.97 |
| 5086 28d death | FIS1 | 8 | −0.036918 | 0.050354 | 0.463 | 0.491 | 0.94 | 0.97 |
| 4982 crit care | FIS1 | 8 | −0.056822 | 0.108468 | 0.600 | 0.619 | 0.94 | 0.97 |
| 4980 suscept | FIS1 | 8 | −0.004823 | 0.025359 | 0.849 | 0.855 | 0.94 | 0.97 |
| 4982 crit care | HAVCR2 | 6 | −0.091232 | 0.212549 | 0.668 | 0.690 | 0.94 | 0.97 |
| 5086 28d death | CD74 | 3 | 0.089231 | 0.465259 | 0.848 | 0.879 | 0.94 | 0.97 |
| 5086 28d death | HAVCR2 | 6 | 0.010169 | 0.167904 | 0.952 | 0.955 | 0.97 | 0.97 |
| 4980 suscept | CD14 | 6 | −0.044339 | 0.044688 | 0.321 | 0.377 | 0.94 | 0.97 |

Net effect: under the corrected *P*-values the 45-test family contains **one** test at
*q*<0.05 (CD74 critical-care weighted median, *q* = 3.0×10⁻¹⁷, after replacing its
stored *P* = 0.0 by 6.65×10⁻¹⁹), versus the **three** the manuscript reports — and that
one survivor is the estimate the manuscript itself argues is direction-reversed,
instrument-starved and overlap-biased.

---

## § Appendix B. Full recomputation of the 25 consensus immune genes (Table 1 basis)

All values from `S01_immunoparalysis_direction.csv`; "recomputed adj.P" is the BH
adjustment recomputed from the *t* column of `S01_mars1_deg.csv` at df ≈ 800.

| Gene | logFC | Stored adj.P | Recomputed adj.P | DEG_0.3 | Direction | Table 1 value | Match |
|---|---|---|---|---|---|---|---|
| CD14 | −0.7657 | 0.0 (artifact) | 2.78×10⁻²⁰ | True | down | "≈0 (P<1e-300)" | **NO (V8)** |
| HLA-DRB1 | −0.8925 | 1.066×10⁻¹⁵ | 1.05×10⁻¹⁵ | True | down | 1.1×10⁻¹⁵ | yes |
| CD74 | −0.7578 | 2.081×10⁻¹⁵ | 2.21×10⁻¹⁵ | True | down | 2.1×10⁻¹⁵ | yes |
| HLA-DMA | −0.8911 | 2.081×10⁻¹⁵ | — | True | down | (not in Table 1) | — |
| HAVCR2 | −0.3488 | 2.838×10⁻¹³ | 2.84×10⁻¹³ | True | down | 2.8×10⁻¹³ | yes |
| FCGR3A | −0.6097 | 9.052×10⁻¹¹ | 9.06×10⁻¹¹ | True | down | 9.1×10⁻¹¹ | yes |
| PDCD1 | +0.1619 | 2.995×10⁻¹⁰ | 3.00×10⁻¹⁰ | False | up | 3.0×10⁻¹⁰ | yes |
| HLA-DQA1 | −0.5301 | 5.439×10⁻⁹ | 5.44×10⁻⁹ | True | down | (not in Table 1) | — |
| LCK | −0.6398 | 7.297×10⁻⁹ | — | True | down | (not in Table 1) | — |
| HLA-DMB | −0.4400 | 2.608×10⁻⁷ | — | True | down | (not in Table 1) | — |
| HLA-DRA | −0.4689 | 3.772×10⁻⁷ | — | True | down | 3.8×10⁻⁷ | yes |
| CD3G | −0.5643 | 2.514×10⁻⁶ | — | True | down | (not in Table 1) | — |
| LYZ | −0.2561 | 3.563×10⁻⁶ | — | False | down | 3.6×10⁻⁶ | yes |
| IL7R | −0.5962 | 8.033×10⁻⁶ | — | True | down | (not in Table 1) | — |
| CD3D | −0.4356 | 2.207×10⁻⁴ | — | True | down | (not in Table 1) | — |
| TIGIT | −0.1570 | 6.989×10⁻⁴ | — | False | down | (not in Table 1) | — |
| CD3E | −0.2164 | 7.735×10⁻⁴ | — | False | down | (not in Table 1) | — |
| ITGAM | −0.2084 | 1.677×10⁻³ | — | False | down | 1.7×10⁻³ | yes |
| CD8A | −0.3206 | 2.986×10⁻³ | — | True | down | (not in Table 1) | — |
| HLA-DQB1 | −0.2027 | 1.738×10⁻² | — | False | down | (not in Table 1) | — |
| CTLA4 | −0.0904 | 3.426×10⁻² | — | False | down | (not in Table 1) | — |
| GZMK | −0.3090 | 4.241×10⁻² | — | True | down | (not in Table 1) | — |
| CD8B | −0.1359 | 7.668×10⁻² | — | False | down | (not in Table 1) | — |
| GZMA | −0.2093 | 0.1100 | — | False | down | (not in Table 1) | — |
| LAG3 | +0.0351 | 0.5521 | — | False | up | (not in Table 1) | — |

Counts recomputed from this table: 25 genes, 23 `Mars1_down`, 22 with adj.P<0.05,
21 both down and significant — matching the manuscript's 23/25, 22/25 and 21 exactly.
Note FIS1 does **not** appear in this file at all, which is why the §3.3 citation
"(§3.1)" for the "all six hubs down" claim cannot be sourced.

---

## § Appendix C. Key numbers verified as matching (manuscript value = recomputed value)

| Quantity | Manuscript | Recomputed | Source |
|---|---|---|---|
| Total samples | 802 | 802 | `GSE65682_pheno.csv`, `S02_immunoparalysis_score.csv` |
| Sepsis / healthy | 760 / 42 | 760 / 42 | `GSE65682_pheno.csv` |
| Endotypes Mars1–4 / unassigned | 132/176/118/53 / 323 | identical | `GSE65682_pheno.csv` |
| 28-day deaths / survivors | 114 / 365 (479 typed) | identical | `S02_immunoparalysis_score.csv` |
| Genes after aggregation | 11,519 | 11,519 | `S01_mars1_deg.csv` |
| Mars1 DEGs \|logFC\|≥0.3 | 3,597 | 3,597 (stable under recomputed BH) | `S01_mars1_deg.csv` |
| Sepsis-vs-healthy DEGs ≥0.3 | 448 | 448 | `S01_deg_sepsis_vs_ctrl.csv` |
| Immune-score Mars1 median | −0.79 | −0.7917 | `S02_immunoparalysis_score.csv` |
| Score full-cohort range | −3.65 to 3.86 | −3.6496 to 3.8616 | `S02_immunoparalysis_score.csv` |
| Mars1 endotype AUC | 0.578 | 0.5782 | `S06_auc_compare.csv` |
| CV AUC / train AUC | 0.659 / 0.750 | 0.65856 / 0.74951 | `S06_auc_compare.csv` |
| External AUC (oriented sum) | 0.638 (0.532–0.748) | 0.6382 (0.5317–0.7475) | `09_external_validation.csv` |
| Locked L1 external AUC | 0.585 (0.469–0.696) | 0.5848 (0.4687–0.6959) | `09_external_validation.csv` |
| IRG benchmark recomputed | 0.604 | 0.604 | `09_external_validation.csv` |
| External cohort | n=106, 52 deaths, 29/30 mapped | identical | `09_ext_risk_scores.csv`, `09_external_validation.csv` |
| Hub genes (6) | CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1 | identical, all 3/3 selectors | `S05_hub_genes.csv` |
| Cell-type r values (5 genes) | 0.77 / 0.49 / 0.69 / 0.30 / 0.68 | 0.773/0.491/0.690/0.298/0.681 | `07_hub_celltype.csv` |
| Axis mean \|r\| | 0.62 / 0.58 / 0.46 | 0.618/0.582/0.459 | `07_axis_celltype.csv` |
| Table 2 concordances | 1.00/0.83/0.71/0.67/0.40/0.40/0.20 | identical | `08_candidates_drugs.csv` |
| L1000 compounds | 20,413 | 20,413 | `S08_l1000_rescue_trtcp.csv` |
| wtcs = rescue × √22 | asserted | exact, ratio 4.690416 over all rows | `S08_l1000_rescue_trtcp.csv` |
| Lenalidomide | rank 5,435, top 26.6%, 0.044, wtcs 0.21 | identical (0.0439, 0.2058) | `S08_l1000_candidate_scores.csv` |
| Azithromycin | rank 9,152, ≈median, 0.013, wtcs 0.06 | identical (0.0133, 0.0626, pct 0.448) | `S08_l1000_candidate_scores.csv` |
| Prednisone / dexamethasone | 0.136/651 ; 0.032/6,808 | 0.1364/651 ; 0.0315/6,808 | `S08_l1000_positive_control.csv` |
| Background mean/median/%>0 | 0.006 / 0.006 / 53.6% | 0.0064 / 0.0055 / 53.62% | `S08_l1000_rescue_trtcp.csv` |
| Top rescue | 0.32 | 0.3182 | `S08_l1000_rescue_trtcp.csv` |
| MR instruments | 27 (3/4/6/6/8; FCGR3A excluded) | identical | `*_harmonised.csv` |
| Median F per gene | 35.4/168.1/45.7/36.4/75.0 | 35.39/168.12/45.65/36.44/75.01 | `*_harmonised.csv` |
| Table 3 & Table 4 cells | all OR, CI, P, Q, I² | all match to printed precision | three MR CSVs |
| Max I² | 0.502 (FIS1 crit care) | 0.5018 | `10_genetics_mr_outcome4982_criticalcare.csv` |
| Primary-outcome I² range | 0.00–0.29 | 0.000–0.2855 | `10_genetics_mr_outcome5086_28ddeath.csv` |
| CD14 15-test / 45-test q | 0.077 / 0.058 | 0.07664 / 0.05748 | MR CSV / `10_mr_bh_family.csv` |
| CD74 susceptibility Egger q | ≈0.0025 | 2.4727×10⁻³ (as computed) | `10_mr_bh_family.csv` |
| Egger intercept P (CD14 / CD74 crit / CD74 susc) | 0.34 / 1.00 / 1.0×10⁻⁴ | 0.3440 / 0.99987 / 1.00×10⁻⁴ | MR CSVs |
| §7 provenance paths | 20+ listed | all exist | repository tree |
| Figures | 3 called out | all 3 exist; 10 files total | `04_figures/` |
| References | 31 cited / 31 listed | identical; no orphans | manuscript |
| DOI audit coverage | — | 29 of 31 audited, all "OK" | `reference_doi_audit.csv` |

---

## § 6. Verdict

**Major revision.**

The single strongest reason is V1/F1: every MR-Egger *P*-value in the study was computed from a standard normal deviate rather than a *t* distribution at n−2 degrees of freedom, and once the correct distribution is used — the degrees of freedom are already recorded in the author's own output files — the CD74 critical-care signal moves from *q*≈1.5×10⁻¹¹ to *q*≈0.79, the CD74 susceptibility signal from *q*≈0.0025 to *q*≈0.90, the CD14 mortality signal from *q*≈0.058 to *q*≈0.73, and the claim "three CD74 tests reached *q*<0.05" collapses to a single surviving test that is the direction-reversed estimate the manuscript itself discounts. Layered on top of this are a hub gene whose Mars1 direction is inverted relative to what the text asserts in three places (FIS1, +1.26 logFC), a positive-control fraction contradicted by the study's own gate record (5/5 vs 4/5), and *P*-values printed as exact zeros or "P<1e-300" that are floating-point artifacts. What keeps this short of rejection is that the manuscript's core — the 23/25/22/21 immunoparalysis counts, every Table 1 effect size except CD14's *P*, the score medians, all four AUCs, the cell-type and L1000 layers, the instrument counts and every Table 3/4 point estimate — recomputes exactly from the shipped files, and the MR layer is already framed as Tier-3 and non-load-bearing; the corrections required are numerical and surgical, not structural. But a manuscript whose §1 promises that "every reported number traces to a concrete output" cannot ship with four headline statistics that its own outputs contradict, and the audit script that is supposed to prevent exactly this passed green throughout. The MR section must be recomputed and rewritten, the FIS1 and IFN-γ claims corrected in all locations including the S11 protocol and the design supplement, and the audit script extended so that these assertions are machine-checked before the next round.
