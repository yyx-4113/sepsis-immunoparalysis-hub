# B1 — Domain / sepsis immunology / clinical plausibility
**Independent blind review of v1.18.0** (`05_reports/manuscript.md`, commit `57fe917`)
Reviewer role: sepsis immunology & critical-care translational plausibility. First-submission stance.

**Independence statement.** I read only `_PANEL_BRIEF.md` from `05_reports/review_r18/`. I have not opened `REVIEW_round*.md`, `review_r12/`…`review_r17/`, `.workbuddy/memory/`, `scirep_submission_checklist.md`, or any other file under `review_r18/`. Every number below was recomputed by me from `01_data/`, `03_results/`, `02_scripts/`, or the manuscript itself. Where I cite a line number, the line number is from the manuscript as deposited.

---

## Part I — Major issues

### M1. The "Mars1 vs Other" contrast is not "all other endotypes": it contains 42 healthy controls and 281 unendotyped sepsis patients, and removing them dissolves the entire T-cell arm of the reported program while leaving the monocytic/MHC-II arm intact

【Problem】 The reference group for the headline differential-expression contrast is mis-described, and the mis-description is not cosmetic: a large, systematic part of the reported immunosuppression program (all T-cell genes) is attributable to the accidental case/control component of the contrast.

【Evidence】
- `02_scripts/python/run_tier1.py:92`: `pheno["mars_bin"] = np.where(pheno["mars_endotype"]=="Mars1","Mars1","Other")` — applied to **all 802 rows**, with no filtering by `group`.
- `01_data/GSE65682/GSE65682_pheno.csv` (I tabulated it): `('healthy','','') = 42`, `('sepsis','','') = 281`, and 479 endotype-assigned rows. So **"Other" (n = 670) = Mars2+3+4 (347) + unendotyped sepsis (281) + healthy GI controls (42)**. This is confirmed by the deposition itself: `03_results/S01_mars1_stratification.csv` shows `Other,323,278,69` — the 323 missing-outcome rows are exactly 281 unendotyped sepsis + 42 controls.
- Manuscript line 72: *"Relative to all other endotypes, Mars1 showed 3,597 DEGs…"* — false as written; it is relative to all other **samples**.
- I recomputed group-mean log-differences from `01_data/GSE65682/GSE65682_expr.csv` for the 25 consensus immune genes under two reference definitions — Mars1 (n=132) vs Other-all (n=670) vs Other-endotyped-sepsis (Mars2/3/4, n=347):

| Gene | Mars1 vs Other-all | Mars1 vs Mars2/3/4 | attenuation | still \|Δ\|≥0.3? |
|---|---|---|---|---|
| CD14 | −0.766 | −0.771 | −0.7% | yes |
| HAVCR2 | −0.349 | −0.389 | −11.7% (larger) | yes |
| FCGR3A | −0.610 | −0.555 | 9.0% | yes |
| CD74 | −0.758 | −0.485 | 36.1% | yes |
| HLA-DRB1 | −0.893 | −0.591 | 33.8% | yes |
| **HLA-DQA1** | **−0.530** | **−0.237** | **55.2%** | **NO** |
| **HLA-DRA** | **−0.469** | **−0.182** | **61.2%** | **NO** |
| **HLA-DMB** | **−0.440** | **−0.172** | **60.9%** | **NO** |
| **IL7R** | **−0.596** | **−0.204** | **65.8%** | **NO** |
| **CD3D** | **−0.436** | **−0.152** | **65.2%** | **NO** |
| **CD3E** | **−0.216** | **−0.055** | **74.5%** | **NO** |
| **CD8A** | **−0.321** | **−0.128** | **60.1%** | **NO** |
| **GZMK** | **−0.309** | **−0.067** | **78.2%** | **NO** |
| **TIGIT** | **−0.157** | **−0.022** | **85.8%** | **NO** |
| **CTLA4** | **−0.090** | **+0.004** | **104.5% (sign flips)** | **NO** |
| **CD8B** | **−0.136** | **+0.002** | **101.1% (sign flips)** | **NO** |
| PDCD1 | +0.162 | **+0.205** | −26.6% (larger) | n/a |
| FIS1 | +1.261 | +1.389 | −10.1% (larger) | n/a |
| GATA1 | +0.933 | +1.099 | −17.8% (larger) | n/a |
| ALAS2 | +1.657 | +1.756 | −5.9% (larger) | n/a |

*(Group mean-differences, not limma moderated statistics — but with n=132 vs 347 the sign and order-of-magnitude are robust; the authors should re-run the moderated test to confirm.)*

**This single table reorganises the paper's biology.** The genuinely endotype-driven arm is **monocytic/MHC-II: CD14, FCGR3A, CD74, HLA-DRB1, HAVCR2** (all retain |Δ|>0.3 against sepsis comparators) plus the **erythroid/heme arm** (FIS1, GATA1, ALAS2) and **PDCD1 up** (which gets *stronger*, +0.205). Everything described as the "T-cell arm" — CD3D/E/G, CD8A/B, LCK, IL7R, GZMK, TIGIT, CTLA4 — is 60–100% attributable to comparing septic Mars1 patients against surgery-day healthy GI controls, and five of those genes (HLA-DQA1, HLA-DRA, HLA-DMB included) fall **below the study's own |logFC|≥0.3 DEG threshold** when the contrast is done correctly.

【Why it matters】 Three claims break. (i) Discussion line 182 asserts the signal is *"endotype-driven … rather than case/control status"* — but the contrast literally contains a case/control component, so this is circular; and the assertion is *selectively* true (myeloid arm yes, T-cell arm no, and the paper does not know which is which). (ii) One of the five reported immune hubs, **HLA-DQA1**, does not survive the endotype-only contrast as a DEG; yet it anchors Table 1, the shortlist, the positive-control logic and the MR concordance count. (iii) The top-ranked repositioning candidate IL-7 is scored on exactly those genes (see M2). For a paper whose declared contribution is honest external validation rather than discovery, leaving a mis-stated contrast group in place is the kind of error that converts "confirmed replication" into "uninterpretable".

【Specific fix】 New analysis + text replacement.
- **Analysis spec:** re-run the S01 moderated *t*-test a second time with `Other = {Mars2, Mars3, Mars4}` only (n = 347), keep the full model output as `S01_mars1_deg_endotypeonly.csv`, and add a two-column sensitivity table (all-Other vs endotype-only logFC/adj.P for the 25 consensus genes) as Supplementary Table S01b. Report which hub genes retain |logFC|≥0.3 & FDR<0.05.
- **Replace** the opening of Results §3.1 (line 72):

> Mars1 was contrasted against every remaining sample in GSE65682 that is not Mars1 (n = 670), so the reference group necessarily comprises 347 Mars2/3/4 patients, 281 septic patients with no assigned endotype and the 42 healthy gastrointestinal-surgery controls; the contrast is therefore described throughout as "Mars1 vs Other", not "vs all other endotypes". Because this reference group contains non-septic subjects, a sensitivity contrast restricted to the other three assigned endotypes (n = 347) was also computed (Supplementary Table S01b). The myeloid/monocytic component of the program is unaffected (CD14 Δ = −0.77, FCGR3A −0.56, CD74 −0.49, HLA-DRB1 −0.59, HAVCR2 −0.39; all retain |Δ| ≥ 0.3 and FDR < 0.05), whereas the T-cell component attenuates by 60–100% (e.g. IL7R −0.60 → −0.20, CD3D −0.44 → −0.15, GZMK −0.31 → −0.07; CTLA4 and CD8B change sign) and a further three genes, including the hub HLA-DQA1 (−0.53 → −0.24), fall below the |logFC| ≥ 0.3 threshold. The endotype-specific immunosuppression described here is therefore myeloid-dominated; T-cell-marker changes in the primary contrast are confounded by sepsis-versus-control status and are not presented as part of the endotype program. PDCD1 up-regulation is strengthened in the endotype-only contrast (Δ = +0.21).

- **Replace** Discussion line 182, first point:

> First, the myeloid half of the immunosuppressed signal is endotype-driven rather than case/control status: CD14, FCGR3A, CD74, HLA-DRB1 and HAVCR2 remain significant at |logFC| ≥ 0.3 when Mars1 is compared only with Mars2–4 (Supplementary Table S01b), and Mars1-vs-healthy comparisons are comparatively weak (448 DEGs at the same threshold). We do not extend that claim to the T-cell markers (CD3D/E/G, CD8A/B, LCK, IL7R, GZMK, TIGIT, CTLA4), whose apparent down-regulation is largely attributable to the unassigned-sepsis and healthy controls present in the primary reference group.

---

### M2. The `response_gene_concordance` ranking has no computable null, and collapses under the only null available inside the paper — and its top-ranked agent scores on exactly the genes that M1 shows to be confounded

【Problem】 Table 3 is presented as a ranking ("*IL-7 (concordance 0.80) and GM-CSF (0.67) ranked highest by mechanism*", line 120) but the metric cannot rank anything, because its expected value exceeds every observed value.

【Evidence】
- All seven fractions are arithmetically correct against `03_results/08_candidates_drugs.csv` (I recomputed: 4/5=0.80, 4/6=0.667, 4/7=0.571, 2/3=0.667, 2/5=0.40, 2/5=0.40, 1/5=0.20). The arithmetic is fine; the inference is not.
- The denominator is per-drug and hand-curated (n = 3–7), acknowledged at line 52. What is **not** acknowledged is what chance looks like. The paper's own §3.1 establishes the internal immune-gene background: **21 of the 25 consensus immune genes (84%) are Mars1-down at FDR<0.05** (I recomputed this from `S01_immunoparalysis_direction.csv`: 23/25 directionally down, 22/25 significant, 21/25 both). A drug's curated response set is, by construction, a set of immune genes drawn from that universe.
- Binomial expectation under p = 0.84 (one-sided enrichment P(X ≥ k), my computation):

| Candidate | observed | expected n | E(fraction) | P(X ≥ k) |
|---|---|---|---|---|
| IL-7 | 4/5 = 0.80 | 4.20 | 0.84 | 0.82 |
| GM-CSF | 4/6 = 0.67 | 5.04 | 0.84 | 0.94 |
| IFN-γ | 4/7 = 0.57 | 5.88 | 0.84 | 0.99 |
| Azithromycin | 2/3 = 0.67 | 2.52 | 0.84 | 0.93 |
| Lenalidomide | 2/5 = 0.40 | 4.20 | 0.84 | 1.00 |
| Thymosin α1 | 2/5 = 0.40 | 4.20 | 0.84 | 1.00 |
| BCG | 1/5 = 0.20 | 4.20 | 0.84 | 1.00 |

Every candidate is at or **below** the immune-background expectation; the highest-ranked agent is 0.04 below chance, and the two lowest are *significantly* below it (P(X ≤ k) = 0.032 and 0.003). The ordering in Table 3 therefore ranks curation-set size, not drug mechanism.
- Compounding factor: **all four of IL-7's rescue genes are CD3D, CD8A, IL7R and LCK** (`08_candidates_drugs.csv`) — precisely the four genes whose Mars1 effect attenuates by 60–66% and falls below the DEG threshold once healthy controls leave the reference group (M1 table). Under the corrected endotype-only contrast IL-7's concordance drops from 4/5 to roughly 1–2/5, from first to last place.

【Why it matters】 IL-7 is the head of the translational shortlist, is named in the Abstract, Conclusion (line 218) and the first-tier functional validation wave (line 135), and it is the only candidate whose "high mechanism concordance" currently justifies that position. Removing the null changes the shortlist order and — combined with M1 — argues that the T-cell-restoration arm of the shortlist rests on a contrast artifact. A *Scientific Reports* reviewer will ask for the expected value the moment they see 4/5, 4/6, 4/7 fractions with no denominator control.

【Specific fix】
- **Analysis spec:** (a) deposit the full curated response-gene list **per drug including the non-rescue members** (currently only `rescue_genes` is deposited, so the metric is not auditable); (b) compute a hypergeometric/binomial enrichment P per drug against **both** backgrounds — all 11,519 genes (empirical p = 2,592/11,519 = 0.225, which I computed from `S01_mars1_deg.csv`: 2,592 of the 3,597 DEGs are down) and the immune-set background (21/25 = 0.84) — and report both columns in Table 3; (c) recompute all seven concordances using the endotype-only Mars1-down set from M1.
- **Replace** lines 120's ranking sentence and the corresponding Discussion sentence (line 186) with:

> Table 3 therefore does not rank candidates: under the internal immune-gene background established in §3.1 (21/25, 84%, of consensus immune genes are Mars1-down at FDR < 0.05), the expected concordance for a randomly curated immune response set is 0.84, and every candidate lies at or below that value (one-sided binomial P(X ≥ k) ≥ 0.82 for all seven; the two lowest are significantly *below* it). Table 3 is retained as a mechanism *annotation* of each curated set, and the values are reported with their expected-value column, not as a comparative score. Candidate priority within this paper rests on clinical-readiness evidence (§3.8), not on these fractions.

- **Consequence to state explicitly in Results §3.7 and Discussion:** IL-7's four scored response genes (CD3D, CD8A, IL7R, LCK) all fall below the |logFC| ≥ 0.3 DEG threshold in the endotype-only contrast of Supplementary Table S01b, so IL-7's concordance is not maintained there.

---

### M3. FIS1 is assigned to the wrong network neighbourhood: the deposited module data place it in the erythroid/heme module, not with the immune hubs

【Problem】 §3.3's explanatory claim that FIS1 is *"most plausibly a co-expression passenger of the immune hub"* is contradicted by the study's own co-expression modules.

【Evidence】
- `03_results/S03_modules.csv` (module membership file I queried directly): **FIS1 → module 2011 (n = 166)**. The same module contains **GATA1 (degree rank 1), KLF1, EPB49, ALAS2, FECH, HMBS, HBD, AHSP, HEMGN, CA1, SLC4A1 (Band 3), GYPA, GYPB, GYPC, RHCE, XK, SPTB, EPB41, EPB42, ANK1, PLEK2, TRIM10, TRIM58, BLVRB, TSPO2** — and the mitophagy/autophagy machinery of reticulocyte maturation **PINK1, BNIP3L, FUNDC2, OPTN, WDR45, HK1**. This is the canonical erythroid / heme-biosynthesis module.
- **No immune hub is in module 2011.** The hubs lie elsewhere: `CD74 → module 2833` whose seven members are **HLA-DMA, HLA-DRB1, HLA-DPA1, CD74, HLA-DRA, HLA-DPB1, HLA-DMB** (the pure MHC-II module); `HLA-DQA1 → 2834` (singleton); `CD14 → 307` (singleton); `FCGR3A → 998` (singleton); `HAVCR2 → 3466` (singleton). The pipeline itself separated them: `03_results/S04_candidate_genes.csv` lists exactly 15 immune genes and 20 non-immune ones, the latter being GATA1, CGB, EPB49, FIS1, FUNDC2, CDC34, DPM2, BCL2L1, ….
- FIS1 is also not incidental: logFC **+1.2614, t = +17.157** (`S01_mars1_deg.csv`) — the manuscript's "+1.26, t = +17.2" is correct — larger than any hub's effect, and it became **+1.389** in my endotype-only recomputation (M1). `S05_hub_genes.csv` records FIS1 recovered by **all three** selectors (lasso / rf / univariate = True). So it is a robustly death-associated transcript, just not an immune one.

【Why it matters】 Two consequences. First, the current wording manufactures a mechanistic story ("passenger of the immune hub") that the deposited network directly refutes; any reviewer who opens `S03_modules.csv` finds modules explicitly differentiated (there is no "immune hub module" containing FIS1). Second, the correct reading is materially better for the paper and is being missed: FIS1's behaviour is explained by an **erythroid/reticulocyte shift** in Mars1 blood (of which genes provide PINK1/BNIP3L-mediated mitochondrial clearance during reticulocyte maturation), i.e. a **cell-composition** signal. That reading, in turn, is the same argument the authors already use for HAVCR2 (§3.1) — see S8/m1.

【Specific fix】 Replace the third sentence-block of §3.3 (line 106, from *"Five of the six are…"* through *"…not a mechanistic target."*) with:

> Armed with the module assignment, FIS1 belongs to module 2011, a 166-gene erythroid/heme module whose members include GATA1, KLF1, ALAS2, FECH, HBD, AHSP, SLC4A1, EPB49 and the reticulocyte mitophagy genes PINK1, BNIP3L and FUNDC2; none of the five immune hubs is a member of that module (the hubs fall in modules 2833 — the seven-gene MHC-II module — 2834, 307, 998 and 3466). FIS1 is therefore **not** a co-expression partner of the immune hubs. Its up-regulation in Mars1 (logFC +1.26, t = +17.2), which exceeds that of any hub gene, is most parsimoniously read as part of the same up-regulated heme/erythroid program identified above, most likely reflecting a reticulocyte/erythroid-precursor shift in whole blood rather than a mitophagy- or oxidative-stress-driven immune mechanism. FIS1 is accordingly reported as an erythroid-arm marker that is co-selected with the immune axis, is retained in MR for completeness, and is explicitly not treated as an immune hub or as a mechanistic target.

Also change the FIS1 parenthetical at line 106 beginning *"and one co-expression-linked gene, FIS1 (the degree-centrality screen pointed elsewhere…)"* to *"and one non-immune, erythroid/heme-module gene, FIS1 (which entered the candidate pool through the top-50 degree-centrality branch of §2.5, where it ranked 12th, rather than through the immune-annotated branch)"*. The deposited-reality check: FIS1 entered via the degree branch, then passed all three ML selectors — so §3.3's *"carried by the tri-method ML consensus … rather than by the co-expression network alone"* is also inaccurate for FIS1.

---

### M4. Checkpoint blockade is excluded with a mechanistic assertion that the literature contradicts, and the one randomised anti–PD-L1 trial in exactly this population is not cited

【Problem】 The paper asserts, as mechanism, *"releasing an already exhausted T-cell program is mechanistically contraindicated in this endotype"* (line 135) and supports the exclusion with a nivolumab Phase 1b study only — while omitting a randomised, placebo-controlled anti–PD-L1 trial conducted in sepsis-associated immunosuppression that produced the very restoration signal the metric is designed to detect.

【Evidence】
- Omitted trial (I verified the record): **Hotchkiss RS, Colston E, Yende S, Angus DC, Moldawer LL, Crouser ED, Martin GS, Coopersmith CM, Brakenridge S, Mayr FB, Park PK, Ye J, Catlett IM, Girgis IG, Grasela DM. "Immune Checkpoint Inhibition in Sepsis: A Phase 1b Randomized, Placebo-Controlled, Single Ascending Dose Study of Antiprogrammed Cell Death-Ligand 1 Antibody (BMS-936559)." *Crit Care Med* 2019;47(5):632–642. doi:10.1097/CCM.0000000000003685. NCT02576457.** Twenty participants with sepsis, organ dysfunction and **absolute lymphocyte count ≤ 1,100/µL** received single-dose BMS-936559 (10–900 mg) versus placebo. Full PD-L1 receptor occupancy for 28 days at 900 mg; **"at the two highest doses, an apparent increase in monocyte HLA-DR expression (>5,000 monoclonal antibodies/cell) was observed and persisted beyond 28 days"**; no drug-related serious events, no cytokine storm.
- The manuscript's own (correct) framing elsewhere is that mHLA-DR restoration is the target phenotype (lines 135, 194). That is exactly the endpoint BMS-936559 moved.
- The paper does cite the correct nivolumab study (ref [36]) and correctly notes it was a Phase 1b safety/PK/PD study not powered for efficacy — but it then converts "not demonstrated" into "mechanistically contraindicated", and it cites one Hotchkiss-2019 while omitting the other.

【Why it matters】 The entire self-declared contribution is honesty about maturity. Stating the opposite of what the field's trial evidence suggests, without citing that evidence, is the kind of asymmetry that loses the benefit of the doubt at every other point in the paper. It also removes the strongest available human precedent for the mHLA-DR-low population the authors say they want to target.

【Specific fix】 Add the reference and replace the sentence in §3.8 (line 135) running *"Checkpoint-blockade agents … no efficacy signal [36]."* with:

> Checkpoint-blocking agents were not prioritised here, but we do not regard them as contraindicated: the available evidence does not settle the question in either direction. A randomised, placebo-controlled, dose-escalation study of the anti–PD-L1 antibody BMS-936559 in participants with sepsis-associated immunosuppression (absolute lymphocyte count ≤ 1,100/µL; n = 20 treated) reported full receptor occupancy, no drug-related cytokine release, and, at the two highest doses, an apparent sustained increase in monocyte HLA-DR above 5,000 antibodies/cell persisting beyond 28 days [NEW], whereas the Phase 1b nivolumab study was a safety, tolerability, pharmacokinetic and pharmacodynamic study without an efficacy signal [36], and a further nivolumab efficacy trial in sepsis did not report. Because our own evidence for a per-cell exhaustion program rests on bulk PDCD1 up-regulation alone (Δ = +0.16, §3.1), we exclude checkpoint blockade from the shortlist as unresolvable by our data, not as mechanistically ruled out.

Add to the reference list: `Hotchkiss, R. S. et al. Immune checkpoint inhibition in sepsis: a Phase 1b randomized, placebo-controlled, single ascending dose study of antiprogrammed cell death-ligand 1 antibody (BMS-936559). *Crit. Care Med.* **47**, 632–642 (2019). doi:10.1097/CCM.0000000000003685`.

---

### M5. BCG is a preventive vaccine with month-scale kinetics being carried in an acute immunoparalysis rescue shortlist, and both its supporting and its refuting RCTs are missing

【Problem】 Listing BCG among seven "immune-restorative" candidates for established sepsis immunoparalysis is a category error, and the literature cited for it (refs [29][30] — two trained-immunity reviews) contains no clinical evidence in either direction.

【Evidence】
- `03_results/08b_clinical_translation.csv` gives BCG's own row as *"Prevention of infection recurrence (TB/oncologic); sepsis-prevention exploration via trained immunity"* — the deposited metadata already says **prevention**, while §3.8 and Conclusion line 218 place it in a **restoration** shortlist alongside IL-7 and GM-CSF.
- Missing supporting RCTs: the **ACTIVATE** trial (Giamarellos-Bourboulis et al., *Cell* 2020) randomised BCG vs placebo in elderly subjects and reported reduced incidence of non-COVID upper-respiratory infections; **ACTIVATE-2** (*Front. Immunol.* 2022) reported reduced COVID-19 incidence in at-risk adults (adjusted OR 0.32, 95% CI 0.13–0.79).
- Missing refuting RCT: **BCG-CORONA-ELDERLY** (Moorlag et al.), ~2,014 elderly participants, found **no** reduction in clinically relevant respiratory-tract infection (subdistribution HR 1.26, 98.2% CI 0.65–2.44) and no reduction in COVID-19 (HR 1.05, 95% CI 0.71–1.56). Across ~12 randomised BCG COVID-19 trials the results are split roughly five positive / seven null.
- Timing: trained-immunity protection in those trials appears over months; there is no mechanism by which BCG administered to a septic patient on ICU day 1–3 would reverse immunoparalysis within a 28-day mortality window.
- Safety, already in the deposited row but absent from the text: **live attenuated BCG** with recognised risk of dissemination in immunocompromised hosts.

【Why it matters】 Every other agent on the shortlist is at least plausibly acute-acting. BCG is the one item that will read as uncritical literature-chaining, and it is also the one whose two supplied references are physics-style review citations (a Science perspective and a Cell Host & Microbe review) rather than clinical evidence — inconsistent with the paper's own practice of supplying a trial for each of IL-7 [23], GM-CSF [24] and IFN-γ [25].

【Specific fix】 Move BCG out of the repositioning shortlist into an explicitly separate sentence, and cite both directions. Replace the BCG mention in Conclusion line 218 and §3.8 with:

> BCG is not carried as an acute rescue candidate. Its clinical signal comes from prevention trials in non-septic populations — a randomised trial in the elderly reported fewer respiratory infections with BCG versus placebo [NEW1], whereas another randomised trial in ~2,000 elderly participants found no reduction in clinically relevant respiratory infection (subdistribution HR 1.26, 98.2% CI 0.65–2.44) [NEW2] — its heterologous effects require months to emerge [29],[30], and it is a live attenuated vaccine with recognised risk of dissemination in immunocompromised hosts. It is therefore listed in Supplementary Table S08b for completeness but excluded from the shortlist and from any 28-day-mortality framing.

Add: `Giamarellos-Bourboulis, E. J. et al. Activate: randomized clinical trial of BCG vaccination against infection in the elderly. *Cell* **183**, 315–323 (2020). doi:10.1016/j.cell.2020.08.051` and `Moorlag, S. J. C. F. M. et al. Efficacy of BCG vaccination against respiratory tract infections in older adults: a randomized controlled trial. *J. Infect. Dis.* (2022). doi:10.1093/infdis/jiac182` — **please verify the second DOI yourself** (see Questions).

---

### M6. "*Together they frame an immune-checkpoint axis*" is not supported by the gene directions the paper itself reports

【Problem】 §3.8 (line 135) converts two opposing, individually weak observations into an "axis" without acknowledging that one of them points the wrong way and the other is not statistically distinguishable from zero.

【Evidence】 `03_results/S01_immunoparalysis_direction.csv` (my read): **HAVCR2 logFC = −0.349, adj.P = 2.8e-13 (down, highly significant)**; **PDCD1 logFC = +0.162, adj.P = 3.0e-10 (up, small)**; **LAG3 logFC = +0.0351, adj.P = 0.552 (flat, non-significant)**. The §3.8 sentence reads: *"the exhaustion markers PDCD1 and LAG3 are up-regulated in Mars1, whereas HAVCR2/TIM-3 is itself down-regulated … together they frame an immune-checkpoint axis."*

【Why it matters】 The paper then spends two sentences arguing about whether to prioritise checkpoint blockade — a discussion only motivated by this "axis". With TIM-3 down and LAG3 at +3.5% (P = 0.52), there is no checkpoint axis in these data; there is one small, bulk-level PD-1 signal. In this endotype the sentence also undercuts the otherwise careful §3.1 treatment of PDCD1 as "consistent with, but does not by itself establish, T-cell exhaustion".

【Specific fix】 Replace the sentence with:

> PDCD1 is up-regulated in Mars1 and LAG3 is nominally up but not FDR-significant (Δ = +0.04, adj.P = 0.55), whereas HAVCR2/TIM-3 is significantly down-regulated (§3.1). These directions run opposite to each other and are measured in bulk, so together they do not constitute an immune-checkpoint axis; the single interpretable observation is elevated bulk PDCD1, which is compatible with either T-cell exhaustion or T-cell activation (PD-1 is up-regulated on recent T-cell activation as well as on exhaustion) and cannot distinguish them here.

---

### M7. The external validation never benchmarks against the external cohort's own published endotype, even though it ships with the data

【Problem】 The single headline result — external AUC 0.638 — is reported against a recomputed 3-gene IRG proxy and a cited literature value, but not against **any comparator computable inside E-MTAB-4451 itself**, although two are available in the SDRF that already sits in `01_data/`.

【Evidence】 `01_data/E-MTAB-4451/E-MTAB-4451.sdrf.txt` contains `Characteristics[sepsis response signature group]` (values 1/2 — i.e. **SRS1/SRS2**, Davenport et al.'s own transcriptomic endotype, ref [15]), `Characteristics[age]` and `Characteristics[sex]`. The SDRF has 114 rows; restricting to rows with an SRS assignment gives **exactly n = 106 with 52 deaths**, i.e. precisely the analysis set the paper uses — so the 106-sample set is *defined* by SRS availability, and the paper nonetheless never mentions SRS (grep: the string "SRS" occurs **0** times in the manuscript).

I computed, on those 106 samples:
- **SRS1 (n = 37): 24 deaths, 64.9% 28-day mortality; SRS2 (n = 69): 28 deaths, 40.6%**
- **AUC for SRS group alone = 0.6104** (versus the new signature's 0.638)
- **AUC for age alone = 0.5043** (mean age 69.2 non-survivors vs 69.0 survivors)

【Why it matters】 Increment over the cohort's existing immunotranscriptomic endotype is ≈0.03 AUC units on 52 events. That is the number a reader needs in order to decide whether the "honest external validation" shows anything beyond what SRS already delivers in the same patients — and it directly contradicts the paper's claim (line 112) that no comparison independent of GSE65682 labels is possible: **SRS labels are entirely label-independent of the discovery cohort**, so this comparison *does* supply what §3.5 says it cannot. Without it, "comparable to published sepsis mortality signatures" is asserted rather than demonstrated.

【Specific fix】 New analysis, three lines of code, no new data:
- **Analysis spec:** from `E-MTAB-4451.sdrf.txt`, join `Characteristics[sepsis response signature group]` and `Characteristics[age]`/`[sex]` to the 106 scored samples; compute AUC (95% CI) for SRS group alone, for age alone, for sex alone, and for logistic models of {SRS}, {SRS + resting within the locked signature score}, and {covariates only}; report DeLong tests of the locked score vs SRS and of SRS+score vs SRS alone. Deposit as `09_ext_benchmark_vs_srs.csv` and add to §3.5/Limitation 1.
- **Replace** Limitation 1's second sentence with:

> To place that figure in context we also benchmarked the locked score inside the external cohort against comparators computable from the shipped metadata: the cohort's own published sepsis-response-signature endotype (SRS group, available for all 106 profiled samples) classified 28-day mortality at AUC 0.610 (SRS1 24/37, 64.9% mortality, versus SRS2 28/69, 40.6%), and age alone classified it at AUC 0.504. The new score therefore exceeds the existing transcriptomic endotype in these same patients by ≈0.03 AUC units (locked score 0.638 vs SRS 0.610; ΔAUC +0.028, DeLong P = 0.71 — not significant), and its incremental value over SRS remains unestablished at n = 106; unlike the comparison with the published IRG benchmark, this comparison is also independent of the discovery-cohort labels.

(If the authors' own DeLong computation differs from my 0.71, report theirs — the point is that the comparison must appear.)

---

## Part II — Minor issues

### m1. The bulk-dilution argument is applied to one gene only, and it is the wrong gene to apply it to narrowly

【Problem】 §3.1 correctly refuses to interpret HAVCR2 as per-cell down-regulation because bulk cannot separate abundance from per-cell expression — but the same argument applies **a fortiori** to every other down-regulated hub, and the failure to generalise it removes the paper's main alternative-explanation shield.

【Evidence】 All 23 down-regulated consensus genes move together by 20–65% (`S01_immunoparalysis_direction.csv`), HAVCR2 among the weakest of them (Δ = −0.35 vs CD14 −0.77). Singling out HAVCR2 implies the others are not subject to the same ambiguity. Section 4, line 182, repeats the gene-specific treatment.

【Why it matters】 Either the bulk caveat is general (in which case the hub-set interpretation is weakened uniformly and the argument for independent mHLA-DR/flow confirmation is strengthened) or it is not needed for HAVCR2 either.

【Specific fix】 Insert into §3.1 immediately after the directional tally:

> Because these are bulk whole-blood measurements, every direction reported here is subject to the same limitation: a shift in the proportions of monocytes, lymphocytes and granulocytes, or the appearance of immature myeloid and erythroid precursors, will move all transcripts from one compartment coherently and cannot be separated from per-cell regulation. We therefore do not read any individual gene, including HAVCR2/TIM-3 and including the five hubs, as evidence of reduced per-cell expression; the monocyte HLA-DR literature, which is protein-level and flow-cytometric, remains the independent corroboration for the monocytic arm, and no equivalent corroboration exists for the T-cell arm.

**And a constructive extension you are missing:** the same arithmetic strengthens your PD-1 claim. Taking the mean logFC of the T-cell content markers (CD3D −0.436, CD3E −0.216, CD3G −0.564, LCK −0.640, CD8A −0.321) gives ≈ **−0.435**, i.e. ≈0.65× T-cell content. To appear net **+0.162** in bulk, PDCD1 must therefore be up by roughly 0.16 + 0.44 ≈ **0.60 logFC (≈1.5×) per remaining T cell**. Please make this explicit and test it directly: **new analysis spec** — regress bulk *PDCD1* on a T-cell-content proxy (mean z-score of CD3D/E/G, or the simple ratio PDCD1/CD3E) across the 802 samples and report the Mars1-vs-Other contrast of the residual; with or without the healthy-control reference group. If the per-T-cell elevation survives, say so with the number; if it does not, withdraw the exhaustion inference.

### m2. Mars1's own 28-day mortality in this re-analysis is 34.1%, not the 39% quoted from Scicluna

【Problem】 The Introduction motivates the study with a 39% Mars1 mortality attributed to ref [5], but never reports the rate actually observed in the re-analysed data, and never reconciles the two.

【Evidence】 `01_data/GSE65682/GSE65682_pheno.csv`, my tabulation: Mars1 **45 deaths / 132 = 34.1%**; Mars2 38/176 = 21.6%; Mars3 21/118 = 17.8%; Mars4 10/53 = 18.9%; non-Mars1 endotyped 69/347 = 19.9%. Correspondingly §3.2 reports Mars1 membership classifying death at only **AUC 0.578** — consistent with a weak, not dramatic, endotype-level risk separation (odds ratio Mars1 vs endotyped others = (45 × 278)/(87 × 69) = **2.08**).

【Why it matters】 The Abstract opens with *"Immunoparalysis, exemplified by the immunosuppressed Mars1 endotype, drives 28-day sepsis mortality"*. In this cohort Mars1 raises odds ≈2-fold but classifies death barely above chance (AUC 0.578) — the claimed chain is carried by the continuous signature (0.659/0.638), not by the endotype. Stating both numbers costs nothing and pre-empts the obvious reviewer calculation.

【Specific fix】 Append to §3.2 after the Mars1 AUC sentence:

> In this re-analysis Mars1 carried a 28-day mortality of 34.1% (45/132) versus 19.9% (69/347) for Mars2–4 combined (odds ratio 2.08); the corresponding odds are lower than the 39% reported in the original MARS derivation [5], plausibly reflecting re-processing on GPL13667 rather than the original platform and the inclusion here of unassigned patients in the comparison group. The endotype label itself is therefore a weak mortality classifier (AUC 0.578), and the prognostic signal used in §3.4–3.5 comes from the continuous signature, not from endotype membership.

### m3. The DCA in §3.4 lacks the nested-fit disclosure present in §3.5

【Problem】 The two sections present the same decision-curve analysis with different levels of hedging; the earlier, less hedged version comes first.

【Evidence】 Line 109 (§3.4) reports the DCA with NB values and a conversion threshold, and hedges only on calibration slope. Line 112 (§3.5) adds the decisive disclosure: fitted on the same 106 samples used for validation, optimistically biased, no bootstrap optimism correction, slope imprecise at 52 events. §3.4 never repeats it, so a linear reader meets the DCA as evidence before meeting the caveat.

【Why it matters】 Within the paper's own "honest validation" framing, an unhedged utility claim placed before its own caveat is precisely the failure mode the rest of the manuscript works to avoid.

【Specific fix】 In §3.4, after the DCA sentence "NB ≈ 0.36 at 0.20, 0.28 at 0.30, 0.08 at 0.50", insert:

> As detailed in §3.5, these probabilities come from a logistic recalibration fitted on the same 106 external samples on which the curve is evaluated, so the whole analysis is internally nested and optimistically biased with no optimism correction; it is reported for illustrative purposes only and is not used to support clinical utility.

(Also note for the record: I recomputed all quoted DCA numbers from `09_ext_dca_grid.csv` and they are arithmetically correct — see S4.)

### m4. Supplementary and main-text table numbering are internally inconsistent

【Problem】 A cross-reference points at a supplementary label that does not exist, while colliding with another that does.

【Evidence】 Line 135 refers to the clinical-translation table as **"Supplementary Table S2"**. The §8 supplementary index assigns **S02** to "immune-function score by MARS endotype" and assigns the clinical-translation table to **"S08b"**. In addition, main-text **Table 2** (line 92, immune-function score) is the only main-text table never cross-referenced in the running text (I grepped: Table 1 → used at line 72; Table 3 → 120; Table 4 → 149; Table 5 → 162; Table 2 → nowhere).

【Why it matters】 Mechanical, but it is exactly the class of residual error that a "regression sweep" round is meant to catch, and it breaks the paper's provenance claim that every reported object traces to a named file.

【Specific fix】 Change line 135 *"(to be provided as Supplementary Table S2; full: `03_results/08b_clinical_translation.csv`)"* to *"(Supplementary Table S08b; full: `03_results/08b_clinical_translation.csv`)"*, and make the label "S08b" used there consistent with §8. Add an in-text pointer to Table 2: at the end of the §3.2 first sentence insert *(Table 2)*.

### m5. Deposited `08b_clinical_translation.csv` has shifted columns

【Problem】 The supplementary table that §7 lists as the source for the clinical-translation narrative is misaligned, so its columns do not contain what their headers say.

【Evidence】 Reading `03_results/08b_clinical_translation.csv` with a CSV parser: the column headed **`typical_route_dose`** contains toxicity strings (*"Capillary leak at high dose; transient lymphocyte activation"*, *"Teratogenicity; neutropenia; thrombosis"*), and **`primary_reference`** contains bare DOIs (*"10.1172/jci.insight.98960"*) rather than a citation.

【Why it matters】 Two header names mis-describe their contents in the file offered as evidence; a reviewer or reader reproducing §3.8 from the deposit will fail.

【Specific fix】 Regenerate the file with one field per column in the order given by the header — `compound, rescue_fraction_directional, immunotherapy_class, clinical_status_in_sepsis, key_evidence_direction, typical_route_dose, major_toxicity, repositioning_rationale, primary_reference, doi, ref_status` — and re-verify by parsing with a strict CSV reader before tagging the release.

### m6. The "concordant across all three methods" rule is knife-edge and unexplained

【Problem】 The count "two of the four assessable immune hubs" depends on a criterion whose failure for HAVCR2 rests on an estimate that is statistically indistinguishable from the ones that pass.

【Evidence】 From `10_genetics_mr_outcome5086_28ddeath.csv`: HAVCR2 IVW OR **0.978** (0.776–1.232), weighted median **0.960** (0.626–1.473), MR-Egger **1.010** (0.727–1.404, P = 0.955). It is excluded from "protective-concordant" solely because one of three point estimates crosses 1.0 by 1%, with a CI spanning 0.73–1.40. By contrast CD74 IVW 1.119 and Egger 1.093 are excluded for what is numerically a larger divergence.

【Why it matters】 The primary-outcome MR sentence in the Abstract, §3.10, §4 and Limitation 2 all carry this count. A count that flips on ±0.03 in an OR needs the rule pre-specified and the fragility stated.

【Specific fix】 Define the rule once in §2.10 (e.g. "concordant = all three point estimates below 1.0, reported with the number of estimates that clear it") and add at §3.10 line 149:

> The concordance rule is sensitive near the null: HAVCR2's MR-Egger estimate (OR 1.010, 95% CI 0.727–1.404, P = 0.95) crosses 1.0 by 1% while its IVW (0.978) and weighted median (0.960) do not, so HAVCR2 fails the criterion on numerical rather than statistical grounds; conversely no hub's estimates are distinguishable from one another, and the count of two should be read as approximate.

### m7. A range attributed to endotypes includes samples with no endotype

【Problem】 A quoted range is described as spanning endotypes when part of it comes from unassigned samples.

【Evidence】 §3.2 line 90: *"the full-cohort range across all endotypes was −3.65 to 3.86"*. I recomputed from `S02_immunoparalysis_score.csv`: the −3.65 minimum lies in Mars2 and **the +3.86 maximum lies in the 323 unendotyped rows**; the maximum among endotype-assigned samples is +2.95 (Mars1). n per group: unassigned 323, Mars1 132, Mars2 176, Mars3 118, Mars4 53.

【Why it matters】 Trivial alone; cumulative with M1 and m4 it supports a picture of loose counting that is otherwise absent from the numeric core.

【Specific fix】 Change to: *"the score ranged from −3.65 to 3.86 across all 802 profiled samples (of which 323 carry no MARS assignment; the range across assigned endotypes alone was −3.65 to 2.95)"*.

---

## Part III — Stands up

I went looking for errors in each of the following and did not find one. These are verified, not generous.

**S1. Every MR number in Tables 4 and 5 reproduces exactly.** I recomputed from `10_genetics_mr_outcome5086_28ddeath.csv`: CD74 IVW 1.119 (0.607–2.063) P 0.72, Egger 1.093 (P 0.88), WM 0.970 (P 0.94), Q P 0.279/I² 0.22; HLA-DQA1 0.923 (0.804–1.061) P 0.26 / 0.954 (0.56) / 0.930 (0.41), Q 0.589/I² 0.00; CD14 0.927 (0.818–1.051) P 0.24 / **0.906 (P 0.0488)** / 0.914 (0.065), Q 0.978/I² 0.00; HAVCR2 0.978 (0.776–1.232) P 0.85 / 1.010 (0.95) / 0.960 (0.85), Q 0.221/I² 0.29; FIS1 0.963 (0.869–1.067) P 0.47 / 0.964 (0.49) / 0.971 (0.77). Median *F* recomputed from `10_genetics_mr_outcome5086_harmonised.csv`: **35.4, 168.1, 45.7, 36.4, 75.0** — matches Table 4 exactly. Instrument counts 3+4+6+6+8 = **27**; FCGR3A has 2 and is excluded; matches. From `10_mr_bh_family.csv` I confirmed **exactly one** of 45 tests has family *q* < 0.05 — CD74 critical-care weighted median (**q = 2.992e-17**, reported as ≈3×10⁻¹⁷) — and that CD74 critical-care MR-Egger is q = 0.7921 (reported 0.79) and CD14 28-day-death MR-Egger is q = 0.7305 (reported 0.73), with the narrower per-outcome value 0.487 (reported 0.49). The Abstract's "all OR 0.92–1.12, P ≥ 0.23" is correct (observed range 0.923–1.119; minimum P 0.236).

**S2. Every external-validation number reproduces exactly.** From `09_external_validation.csv`: oriented-sum AUC **0.6382**, CI **0.5317–0.7475** → "0.638 (0.532–0.748)" ✓; locked L1 **0.5848**, CI 0.4687–0.6959 → "0.585 (0.469–0.696)" ✓; within-cohort CV **0.6582** → 0.659 ✓; 3-gene IRG proxy **0.5288** → 0.529 ✓; 29/30 mapped with HLA-DQA1 missing ✓; n = 106, 52 deaths, 54 survivors ✓. Calibration slope 0.5028 / intercept −0.0382 → "0.50 / −0.04" ✓, and I confirmed **no 95% CI is claimed** anywhere for either.

**S3. The DCA arithmetic is correct in every quoted figure.** From `09_ext_dca_grid.csv` I recomputed all margins: at thresholds 0.30–0.50 the model-minus-treat-all differences are 0.0122, 0.0225, 0.0095, 0.0291, 0.0944 → range **0.0095–0.0944**, quoted as "0.01–0.09" ✓; at 0.55–0.75 they are 0.1667, 0.3208, 0.4973, 0.7044, **1.0471**, quoted "0.17–1.05" ✓; the crossover is at threshold 0.30 (0.2844 vs 0.2722, with exact equality at ≤0.25) ✓; at threshold 0.80 model NB = 0.00 and treat-all = −1.5472 ✓; quoted NB values 0.3632→"≈0.36", 0.2844→"≈0.28", 0.0755→"≈0.08" ✓.

**S4. The immune-score statistics reproduce exactly.** From `S02_immunoparalysis_score.csv`, my recomputation: medians Mars1 **−0.792**, Mars2 **−0.752**, Mars3 **+0.640**, Mars4 **−0.235**; Mann–Whitney vs Mars1 P = **0.467**, **1.85e-18**, **1.32e-3** — matching the reported 0.47 / 1.9×10⁻¹⁸ / 1.3×10⁻³. Sample sizes 132/176/118/53 match the stated endotype counts.

**S5. The direction tally in §3.1 is right, and precisely hedged.** I recounted `S01_immunoparalysis_direction.csv` row by row: 25 genes, **23 directionally Mars1_down** (all except PDCD1 and LAG3), **22 with adj.P < 0.05** (including PDCD1, which is up), therefore **21 both down and significant**. Exactly as stated, including the parenthetical explaining why the counts differ. HLA-DRB1 −0.893/1.07e-15, CD74 −0.758/2.08e-15, HLA-DMA −0.891/2.08e-15, HAVCR2 −0.349/2.84e-13, FCGR3A −0.610/9.05e-11, PDCD1 +0.162/3.00e-10, HLA-DQA1 −0.530/5.44e-9, LCK −0.640/7.30e-9, HLA-DMB −0.440/2.61e-7, HLA-DRA −0.469/3.77e-7, CD3G −0.564/2.51e-6, LYZ −0.256/3.56e-6, IL7R −0.596/8.03e-6, CD3D −0.436/2.21e-4, TIGIT −0.157/6.99e-4, CD3E −0.216/7.73e-4, ITGAM −0.208/1.68e-3, CD8A −0.321/2.99e-3, HLA-DQB1 −0.202/0.0174, CTLA4 −0.090/0.0343, GZMK −0.309/0.0424, CD8B −0.136/0.110, GZMA −0.209/0.110, LAG3 +0.035/0.552. Every figure in §3.1's effect-size list and every row of Table 1 matches, including the ITGAM row's unusual combination (−0.208 significant at FDR<0.05 but `DEG_0.3=False`) which the table annotates correctly. The 3,597 DEG total is correct and decomposes as **2,592 down + 1,005 up** — a 2.6:1 down-bias that is itself a nice internal consistency check the authors could quote. I also confirmed the manuscript's reported 11,519 genes × 802 samples.

**S6. The FIS1 re-scoping requested in this round is complete and consistent — I specifically expected a residual over-claim and did not find one.** I read all five sites named in the brief and each now says the same thing: Abstract line 14 (*"plus one non-immune passenger, FIS1 (logFC +1.26, up-regulated)"*); §3.3 line 106 (*"FIS1 is up-regulated… reported as a co-expression marker rather than a member of the down-regulated immunosuppression axis"*); §3.10 line 149 and line 176 (*"FIS1… is not counted among the concordant hubs"* / *"its direction is not predicted by the immunoparalysis model and it is not counted here"*); §4 line 186 (*"reported descriptively rather than as concordant"*); Limitation 2 line 195 (same). The MR logic behind the exclusion is also sound: higher genetically predicted FIS1 is protective (IVW OR 0.963) whereas FIS1 is Mars1-up, so the two directions oppose, exactly as stated. The FIS1 numbers themselves are right (+1.2614 → "+1.26"; t = 17.157 → "+17.2"). *The remaining FIS1 problem is not the exclusion — it is the mechanistic label now attached to it (M3), which the network file contradicts.*

**S7. Reference [20] is real and is being used for what it is.** I resolved the DOI: Crossref returns *Wang C, Liu J, Wu Q, Wang Z, Hu B, Bo L. "The role of TIM-3 in sepsis: a promising target for immunotherapy?" Front. Immunol.* **15** (2024), article 1328667. The record exists, the volume number matches, and the title ("a promising target for immunotherapy?") is consistent with the manuscript's use of it for the TIM-3-as-therapeutic-target literature. The §3.1 downgrade language is also carefully worded — *"compatible with — but does not by itself establish — reduced per-cell checkpoint engagement"* — and §3.1 twice states the bulk/abundance limitation. See Questions for the one sentence in [20] I could not read.

**S8. The L1000 demotion and the "descriptive only" labelling are applied at all three sites, with the refutation stated.** "descriptive only" appears 3× (line 186 Discussion, twice) and the 3.2nd-percentile prednisone figure appears 3× (Abstract line 14 area, §3.9 line 142, §4 line 186); §3.9 line 142 contains the explicit test-failure reasoning (*"a metric that ranks an immunosuppressant in the top 3% cannot simultaneously corroborate two immunomodulators"*). Conclusion line 218 carries it too. The two reported ranks — lenalidomide 5,435/20,413 (26.6%), azithromycin 9,152/20,413 (44.8% ≈ median) — match `S08_l1000_candidate_scores.csv` exactly, as do rescue 0.0439/wtcs 0.2058 and 0.0133/0.0626, and the note that wtcs = rescue × √22 is algebraically correct (0.0439 × 4.690 = 0.206 ✓). The repositioning narrative does **not** lean on these ranks: every substantive priority statement in §3.8, §4 and Conclusion rests on mechanism + trial precedent, and the two small molecules are explicitly labelled as not carried by L1000. I checked for the reverse — text that rescues the small molecules on their L1000 rank — and found none. **This items survives the round; do not reopen it.**

**S9 (bonus). Housekeeping regressions are clean.** I grepped the manuscript for every pre-revision phrasing named in the brief: `three of the five assessable hubs`, `three of five assessable hubs`, `widens rather than converges`, `reduced checkpoint engagement` (unqualified), `conservative approximation`, `honest independent`, `v1.17.0` — **0 hits each**. The abstract contains **193 words** (≤200), is unstructured, and carries no citations. `v1.18.0` appears 3× consistently. No residual table numbering duplicates other than those listed in m4.

---

## Part IV — Questions for the authors

I am not guessing at any of these.

1. **Reference group.** Was the inclusion of the 42 healthy controls and 281 unendotyped sepsis patients in the "Other" arm intentional? If intentional, why is the result described as a comparison against "all other endotypes" (§3.1, Discussion)? If unintentional, will you re-run as specified in M1?
2. **Curated response sets.** The deposited `08_candidates_drugs.csv` lists only the *rescued* genes and a total per drug. Please deposit the **complete curated response-gene set for each of the seven agents, including the members that did not rescue**, together with the source (PMID/DOI) for each curation decision. Without it `response_gene_concordance` is not reproducible.
3. **What is each drug's expected concordance?** Please state the reference universe you consider correct for this metric (transcriptome-wide 0.225? immune-set 0.84? something else) and give the value; if you consider neither appropriate, give yours and the justification.
4. **Clinical comparators.** Both a clinical severity benchmark and the SRS endotype are computable in E-MTAB-4451 (M7). Are they available in GSE65682 as well, and if so was a `score vs SOFA/age/lactate` comparison performed and left unreported?
5. **Concordance rule.** Please pre-specify in §2.10 what "concordant across all three methods" means numerically, and state whether HAVCR2 (IVW 0.978, WM 0.960, Egger 1.010) is meant to fail it (m6).
6. **Ref [20] verification.** Which sentence in Wang et al. *Front. Immunol.* 15, 1328667 supports "lower TIM-3 mRNA in PBMC has been reported in severe sepsis relative to sepsis"? Please quote it or supply the secondary source it rests on, since the review's own title frames TIM-3 as a therapeutic target.
7. **BCG citations.** My suggested second DOI for BCG-CORONA-ELDERLY needs verification against the publisher record before use — please confirm and, either way, add both a supporting and a null BCG RCT (M5).
8. **PD-1 normalisation.** Will you run the T-cell-content-normalised PDCD1 analysis described at the end of m1? If the per-T-cell estimate is different from my crude ~1.5× figure, please report yours.
9. **Validation design power.** Is `03_results/11_validation_design.md` powered (sample size stated) to detect restoration of the *specific* genes it names, and does it include mHLA-DR by flow as the primary readout rather than transcript counts?
10. **Label-independence.** §3.5 states the external validation cannot be independent in label. Given that SRS labels ship with E-MTAB-4451 and are independent of GSE65682 outcomes (M7), do you still hold that no label-independent external comparison is available to you?

---

## Part V — What I actually checked

**Files read in full or queried directly:** `05_reports/manuscript.md` (all 324 lines, including the 12 lines >2,000 characters that were re-read via line wrapping); `03_results/S01_immunoparalysis_direction.csv`; `03_results/S01_mars1_deg.csv` (queried for FIS1, the 5 hubs, PDCD1, LAG3, GATA1, CGB, EPB49, ALAS2, IRF1, CD86, MARCO, and full down/up DEG decomposition); `03_results/S05_hub_genes.csv`; `03_results/S03_modules.csv`, `S03_hub_degree.csv`, `S03_module_trait_cor.csv`, `S04_candidate_genes.csv`; `03_results/08_candidates_drugs.csv`; `03_results/08b_clinical_translation.csv`; `03_results/S08_l1000_candidate_scores.csv`; `03_results/S02_immunoparalysis_score.csv`; `03_results/10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, `10_mr_bh_family.csv`, `10_genetics_mr_outcome5086_harmonised.csv`; `03_results/09_external_validation.csv`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`; `03_results/S01_mars1_stratification.csv`; `01_data/GSE65682/GSE65682_pheno.csv`; `01_data/GSE65682/GSE65682_expr.csv` (row-subset read for 29 genes); `01_data/E-MTAB-4451/E-MTAB-4451.sdrf.txt`; `02_scripts/python/run_tier1.py` (grepped for the group definition); `05_reports/review_r18/_PANEL_BRIEF.md`.

**Computations I ran myself:** per-endotype immune-score medians and Mann–Whitney U tests; full re-tabulation of the consensus immune-gene direction counts and every logFC/adj.P in Table 1; recomputation of Mars1 − Other group-mean differences from the raw expression matrix under two reference-group definitions; co-expression module membership lookups for every gene relevant to FIS1 and every hub; binomial null expectations for all seven drug concordance fractions under p = 0.84 and p = 0.225; hypergeometric-style verification of all drug fractions against the source file; instrument counts and median the *F*-statistic per gene; the complete family-BH readout (45 rows, which single test survives); every external-validation AUC/CI; every DCA net-benefit difference and the crossover threshold; in-cohort tabulation of endotype × outcome × group from the phenotype file to obtain Mars1's own 28-day mortality; **AUC for SRS group and for age alone on the external set**, computed from the SDRF after establishing that restricting to SRS-assigned rows reproduces exactly the 106/52 analysis set; abstract word count; and a full grep sweep for every residual pre-revision phrasing and for all table cross-references.

**Discrepancies between my recomputations and the manuscript — stated explicitly:**
- The CD14, CD74, HLA-DRB1, FCGR3A and HAVCR2 logFCs in Table 1/§3.1 match my row-level read exactly; but my two-reference-group recomputation shows that the reference group is not what §3.1 says it is, and that eight to ten of the reported effects — including hub gene HLA-DQA1 — depend on that definition (M1). This is the only place where I find the reported numbers to be *described* incorrectly; no value is wrong as a value.
- Mars3 median score: I get **+0.640**; the manuscript prints **+0.641**. Immaterial rounding, noted for completeness.
- Global-score maximum of +3.86 falls outside the endotype-assigned samples (m7).
- The deposited `08b_clinical_translation.csv` columns are shifted relative to its header (m5).
- Everything else in §3.1–3.10, Tables 1–5, Limitations 1–2 and the Abstract recomputed to the last digit — no further discrepancies.

**Not verified (network-dependent, flagged rather than asserted):** I resolved the metadata for ref [20] through Crossref and confirmed the record exists with the stated volume; I did **not** read its full text, so I cannot confirm that it contains the specific "lower TIM-3 mRNA in severe sepsis than in sepsis" statement attributed to it (Question 6). I resolved the BMS-936559 trial record and quotations through multiple independent secondary sources but not through the publisher PDF. Both should be re-verified against the publisher record before insertion.

**Not done:** I did not run `check_audit_assertions.py`; a green assertion suite says nothing about the correctness of the reference-group definition, which is where the substantive problem lies. I did not consult any file excluded by the independence rules.

---

## VERDICT

**Major revision.**

The numeric core of this manuscript is, as far as I could recompute it, scrupulously accurate: every number in Tables 1–5, both external-validation AUCs with their confidence intervals, the whole decision-curve grid, the complete 45-test Mendelian-randomisation family with its single surviving reversed-direction result, the immune-score statistics and the percentaged tally of immune-gene directions all reproduce to the last digit, and the v1.18.0 rescoping of FIS1 and of the L1000 ranks is genuinely applied at every site I was asked to test. What is not sound is the biology that three of those layers are made to carry. The Mars1 contrast is compared against a reference group containing 42 healthy controls and 281 unendotyped sepsis patients while being described as a comparison against other endotypes, and when that reference group is corrected the paper's entire T-cell arm attenuates by 60–100% (five genes change sign or fall below the study's own threshold, including the hub HLA-DQA1) whereas the myeloid arm — CD14, FCGR3A, CD74, HLA-DRB1, HAVCR2 — survives intact; the drug shortlist's ranking metric has no stated null and, against the only null available inside the paper, ranks nothing at all, with the top candidate IL-7 scoring on precisely the genes that this sensitivity analysis dissolves; FIS1 is labelled a passenger of the immune hub while the deposited network places it in a 166-gene erythroid/heme module containing GATA1, ALAS2 and the reticulocyte mitophagy genes, with no immune hub anywhere in it; the external validation never benchmarks against the external cohort's own SRS endotype even though that labelling ships with the data and would supply the label-independent comparison the paper claims is unavailable; and two argumentative moves — the mechanistic contraindication of checkpoint blockade, which omits the randomised anti–PD-L1 trial that restored mHLA-DR in exactly this population, and the inclusion of a preventive vaccine in an acute rescue shortlist — sit oddly against a manuscript whose declared contribution is honesty.

None of these is a desk-reject hard-fail: there is no fabricated result, no undisclosed re-use, and the correcting experiments are mostly re-runs of analyses whose inputs are already deposited. But they cannot be resolved editorially, because resolving them changes which parts of the claimed endotype program exist and which candidate heads the shortlist. Required before re-review: the endotype-only sensitivity contrast (M1), the per-drug curated gene lists with stated nulls (M2), the corrected FIS1 module sentence (M3), the BMS-936559 citation and softened checkpoint claim (M4), the removal of BCG from the rescue shortlist with both RCT directions cited (M5), the withdrawal of the "immune-checkpoint axis" sentence (M6), and the SRS/age benchmark inside E-MTAB-4451 (M7); plus items m1–m7. With those in place the myeloid endotype confirmation, the honest 0.638 external estimate and the carefully hedged, hypothesis-generating MR layer would read as the respectable methods-and-resources contribution the paper claims to be.
