# A4 — Venue Editor / Reporting-Standard Audit

**Role:** Independent peer reviewer (journal editor + reporting-standard auditor). Single-author translational-bioinformatics manuscript, fresh first-read.
**Mandate:** STROBE-MR / TRIPOD honesty, headline-vs-caveat contradictions, abstract completeness, format hard-fails, article-type & journal fit.
**Independence statement:** I have not read any prior review, response, or panel brief for this manuscript. All judgements below are derived solely from `05_reports/manuscript.md`, the six raw `03_results/*.csv` files, and `README.md` as supplied. No prior reviewer opinion was available to me.

---

## 1. Issues

### Issue 1 — "Therapeutically addressable axis" is a disclosure≠resolution headline
**【Problem】** The Conclusion and Discussion open with a positively-causal verb that the body text itself retracts.

**【Evidence】**
- Discussion L190: *"We show that the MARS immunosuppressed endotype is anchored by a compact, prognostically informative and **therapeutically addressable** set of antigen-presentation / monocytic hub genes (in expression terms; direct-target validation still pending)."*
- §6 Conclusion L218: *"…that are both prognostically informative … and **mark a therapeutically addressable axis** (in expression terms; direct-target validation still pending)."*
- Same Discussion paragraph, later: *"None of this reaches the level of a demonstration: no primary IVW estimate is significant and the only family-significant result (CD74 critical-care weighted median) reverses the Mars1 direction, so we present the MR layer as **hypothesis-generating** rather than as either a positive or a refutation."*
- MR layer: primary outcome `ieu-b-5086` — all IVW OR 0.92–1.12, P ≥ 0.24; only family-significant test (CD74 critical-care WM, q ≈ 3×10⁻¹⁷) **reverses** direction. Repositioning: only 2/7 candidates (lenalidomide, azithromycin) have any connectivity data, both modest; glucocorticoid positive-control shows transcriptional rescue ≠ functional rescue (§3.9).

**【Why it matters】** "Therapeutically addressable" is a clinical-translational claim. The evidence supports at most *expression-level, hypothesis-generating* repositioning — not an addressable axis. The qualifier "(in expression terms; direct-target validation still pending)" softens the verb but does not neutralise it; the opening "We show… therapeutically addressable" is contradicted by the same paragraph's "hypothesis-generating / not a demonstration." This is precisely the disclosure-without-resolution pattern.

**【Specific fix】** Replace the opening verb and the conclusion phrase so the strength matches the evidence:
> *"We report that the MARS immunosuppressed endotype is anchored by a compact, prognostically informative set of antigen-presentation / monocytic hub genes whose coordinated down-regulation is, in expression terms, a **candidate** axis for future immunorestorative repositioning — pending functional validation."*
And in §6: *"…and define a **candidate, expression-level** axis for repositioning (functional validation still required)."*

---

### Issue 2 — English Abstract falsely localises all six hubs to monocytes / APC (FIS1 contradiction)
**【Problem】** The English Abstract asserts all six hub genes localised to monocytes / antigen-presenting cells; FIS1 is neither.

**【Evidence】**
- Abstract (EN) L14: *"Six hub genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1) were recovered by the tri-method consensus and **localized to monocytes / antigen-presenting cells**."*
- §3.3 L114: FIS1 is *"a mitochondrial-fission protein absent from the consensus immune gene set… up-regulated in Mars1 (logFC +1.26)… reported as a marker, not a mechanistic target."*
- §3.6 L125 localisation list (CD14 r=0.77, FCGR3A r=0.49, CD74→dendritic r=0.69, HAVCR2 r=0.30, HLA-DQA1→B-cell r=0.68) **omits FIS1 entirely** — its cellular context is never established as monocyte/APC.
- Internal inconsistency: Chinese Abstract L25 *does* carve FIS1 out ("FIS1 为线粒体分裂蛋白、属非免疫成员"), but still applies "定位于单核细胞/抗原呈递细胞" to the set — so both abstracts over-state FIS1's localisation, and the EN abstract is the worst offender.

**【Why it matters】** A factual claim in the Abstract that is contradicted by §3.3/§3.6 is a reporting hard-fail and misleads the scanning reader into thinking all six hubs are immune-cell-anchored.

**【Specific fix】** In the English Abstract, mirror the Chinese carve-out:
> *"Six hub genes were recovered by the tri-method consensus: five (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) localised to monocytes / antigen-presenting cells, and a sixth, FIS1, a mitochondrial-fission protein up-regulated in Mars1 (logFC +1.26), reported as a co-expression marker rather than an immune-localised target."*

---

### Issue 3 — "Direct-target validation still pending" mislabels the actual evidence
**【Problem】** The phrase implies a molecular target was identified and merely awaits validation. No target was identified.

**【Evidence】**
- §2.8 L64: the metric is *"a mechanism-anchored, literature-curated concordance… not an overlap with the drug's direct molecular targets (which were not retrieved from a pharmacologic database in this study)."*
- §5 limitation 9 L209: *"it is not an overlap with direct pharmacologic targets (no DGIdb/ChEMBL pull was performed)."*
- Yet Conclusion L218 and Discussion L190 repeatedly say *"direct-target validation still pending"* — presupposing a target exists.

**【Why it matters】** Framing the gap as "target validation pending" over-states maturity; the study never established a direct target–drug pair. The honest gap is "no direct target was inferred; repositioning rests on curated response-gene concordance."

**【Specific fix】** Replace "direct-target validation still pending" with "direct molecular-target inference was not performed (curated response-gene concordance only); functional validation of the reversal hypothesis is still required."

---

### Issue 4 — IFN-γ "4/5 antigen-presentation genes" contradicts the candidate CSV (4/7)
**【Problem】** Prose and Abstract count a 5-gene antigen-presentation rescue; the source table shows a 7-gene curated set with 4 rescued, and HLA-DQB1 is not in the rescued list.

**【Evidence】**
- Abstract L14 & §3.7 L128: *"IFN-γ [29] rescued **4/5 antigen-presentation genes** in its curated set (HLA-DRA, HLA-DRB1, HLA-DQA1, HLA-DQB1, CD74; HLA-DQB1 fails the paper's own |logFC|≥0.3 rule, DEG_0.3 = False)."*
- `08_candidates_drugs.csv`: IFN-gamma → `n_target_genes=7`, `n_rescue_mars1down=4`, rescue_fraction=0.571; `rescue_genes = HLA-DRA;HLA-DRB1;HLA-DQA1;CD74` (4 genes, **HLA-DQB1 absent**).
- Table 2 (L134) lists IFN-γ as 4/7, consistent with the CSV but inconsistent with the §3.7 prose "4/5".

**【Why it matters】** The method-positive gate narrative (§2.8 "≥3/5 concordance") and the §3.7 "4/5" both imply a five-gene antigen-presentation subset, while the auditable table is 4/7. A reader cannot reconcile the gate denominator. At minimum HLA-DQB1 is double-counted inconsistently (named in prose as one of the five, but not in the rescued four).

**【Specific fix】** Reconcile to the CSV: *"IFN-γ rescued 4/7 curated response genes (HLA-DRA, HLA-DRB1, HLA-DQA1, CD74), satisfying the ≥3/5 method-positive gate; HLA-DQB1 is in the curated set but fails the |logFC|≥0.3 rule and is not among the rescued four."* Apply the same 4/7 denominator in the Abstract.

---

### Issue 5 — STROBE-MR item 9b: per-SNP drop-list "available on request" is incomplete disclosure
**【Problem】** STROBE-MR 9b expects the harmonised instrument list to be fully reportable; a "available on request" drop-list is a transparency gap.

**【Evidence】**
- §2.10 L72: *"the retained-instrument details above constitute the STROBE-MR item 9b disclosure, and the full per-SNP **drop-list remains available on request**."*
- The retained-instrument `*_harmonised.csv` tables are provided (good), but the *excluded* SNPs (palindromic / strand-ambiguous / allele-incompatible) are not in the public supplement — only "on request."

**【Why it matters】** Reproducibility and the STROBE-MR disclosure standard require the exclusion trail to be published, not gated behind a request. This is a correctable, non-fatal hard-fail.

**【Specific fix】** Deposit the per-SNP drop-list (rsid, reason, alleles) as a supplementary CSV in the repository and cite it; remove "available on request."

---

### Issue 6 — TRIPOD gap: events-per-variable (EPV) not reported; overfitting risk understated
**【Problem】** The 30-gene signature is built and oriented on the same 28-day labels; EPV is never stated.

**【Evidence】**
- §2.6 / §3.4: 30-gene signature, 5-fold CV AUC 0.659 (training 0.750), discovery deaths = 114 (from `S02` / §2.1: death_28d 1.0 = 114). EPV ≈ 114/30 ≈ 3.8 — below the conventional ≥10 rule-of-thumb.
- §3.4 L117: the locked L1 model assigned **zero weight to 7 of 29** signature genes (CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B) — direct evidence the 30-gene panel is partly decorative and the effective EPV is even lower.
- §5 limitation 1 and 10 acknowledge optimism but do not quantify EPV or the zero-weight shrinkage.

**【Why it matters】** TRIPOD expects model complexity vs event count to be stated. The zero-weight finding should be foregrounded as evidence the *gene set + orientation* — not 30 individually weighted genes — is the portable unit, which actually *strengthens* the honesty of the external result but must be stated up front.

**【Specific fix】** Add to §3.4: *"With 114 discovery deaths the 30-gene panel yields EPV ≈ 3.8; consistent with this, the locked L1 model assigned zero weight to 7 of 29 signature genes, so the portable signal is the gene set and fixed orientation collectively rather than 30 independent weighted predictors."*

---

### Issue 7 — README residual over-claim vs manuscript scope (previously-flagged items now fixed)
**【Problem】** Two prior-round over-claims appear **corrected**, but a looser repo-level over-statement remains.

**【Evidence — now reconciled (credit):**
- README L89: *"immunoparalysis score lowest in the **Mars1/Mars2 cluster** (median −0.79 in Mars1)"* — matches §3.2 L100 (the old "Mars1 alone" over-claim is gone).
- README L98: *"**three of five** assessable hubs (HLA-DQA1, CD14, FIS1) give protective estimates concordant…"* — matches manuscript; the old "4/5" over-claim is gone.
- README L98 also correctly reports the MR null, the reversing CD74 critical-care signal, FCGR3A unassessed, and "No causal claim is made."

**【Evidence — residual:**
- README L5–8: *"identifies the hub genes anchoring the MARS immunosuppressed (Mars1) endotype… and (iii) reprioritizes **immune-restorative drugs**."* "Immune-restorative" is stronger than the manuscript's own "hypothesis-generating / candidate" framing; the repo sells the conclusion harder than the paper earns it.
- README "Headline results" (L89–92) omits that only 2/7 candidates have connectivity data and that the primary MR is null — a balance issue, not a falsehood.

**【Why it matters】** The reproducibility package is the first thing a reviewer/reader opens; its headline should not out-run the manuscript's hedged claims.

**【Specific fix】** In README L5–8, change "reprioritizes immune-restorative drugs" → "reprioritizes candidate immune-restorative agents (hypothesis-generating)"; add one bullet: "Only 2/7 shortlisted agents have LINCS L1000 connectivity; primary MR outcome is null."

---

### Issue 8 — Minor format / reporting hard-fails
**【Problem】** Small but citable defects.
1. **Undefined abbreviation:** §3.9 L146 "**MODZ** consensus" is never expanded (LINCS z-score, moderated z-score).
2. **Figure legends:** figures are cited inline (`[04_figures/S01_*.png]`, `fig_s09_external_roc.png`, etc.) but there is no consolidated figure/table legend list; several references (e.g., §3.1 S01 ROC, §3.4 S06 DCA) point to files without a caption in the text.
3. **Statistical reporting:** Mann–Whitney P values (§3.2 L100, L109) are given without stating two-sided; CD14 MR-Egger P = 4.9×10⁻² is reported as "nominally significant" but the t-distribution df (= n_instruments − 2 = 4) is not shown at the point of claim (it is mentioned later in §2.10, not at the result).
4. **§3.10 closure sentence** L184: *"no causal claim for the hub i… [truncated]"* — the manuscript text as supplied ends mid-word ("i…"), indicating a truncation/copy artefact in the source I received. Confirm the published version is complete.

**【Specific fix】** Expand MODZ at first use; add a one-line caption per cited figure; append "(two-sided)" to Mann–Whitney P values; state "df = 4" beside the CD14 Egger P; verify §3.10 is not truncated in the submitted file.

---

### Issue 9 — Article-type & journal fit: recommend downgrade/reframe (Option B)
**【Problem】** Framed as an original translational research article with causal-sounding conclusions, but the evidence is in-silico, null-MR, modest-external-AUC, zero functional rescue.

**【Evidence】** All of Issues 1–3; external AUC 0.638 (95% CI 0.532–0.748, excluding 0.5 by a thin margin); MR null on the phenotype-matched primary outcome; repositioning is curated-concordance + 2/7 connectivity.

**【Why it matters】** A "Research Article" in a clinical-translational venue implies a demonstrated or at least robustly-supported causal/translational claim. This manuscript is, by its own limitations, a hypothesis-generating resource.

**【Specific fix — recommended path B (downgrade/reframe):**
- Reframe as a **"Hypothesis / Computational Biology" brief** or a **"Methods & Resource"** article, OR
- If keeping "Research," strip every causal/therapeutically-addressable verb (per Issue 1/3) and rename to e.g. *"…a multi-omics dissection and in-silico candidate repositioning (hypothesis-generating)."*
- **Option C (wording-only) is NOT viable**: the gap is between evidence level and claim strength, not merely phrasing — but wording fixes (Issues 1–3) are necessary regardless of path.

---

## 2. Stands up (strengths — evidence-pinned)

1. **The Abstract honestly reports the MR null.** Abstract (EN) L14: *"Two-sample Mendelian randomisation did not support a causal effect of any hub gene on the phenotype-matched primary outcome (sepsis 28-day death: all IVW OR 0.92–1.12, P ≥ 0.24); across the pre-specified 45-test family only the CD74 critical-care weighted median survived correction, and it pointed opposite to the Mars1 expression model."* Cross-checked against `10_genetics_mr_outcome5086_28ddeath.csv` (all IVW P ≥ 0.235) and `10_mr_bh_family.csv` (CD74 crit-care WM q ≈ 2.99×10⁻¹⁷, `family_sig_q<0.05 = YES`, OR 2.194 > 1 = reversed). This is genuine reporting maturity — the negative finding is not buried.
2. **External validation is real and honestly scoped.** `09_external_validation.csv`: orientedSum AUC 0.6382 (CI 0.5317–0.7475 ≈ "0.638, 95% CI 0.532–0.748"); locked-L1 AUC 0.5848 (manuscript's 0.585); IRG benchmark 0.604. §3.5 and §5 limitation 1 correctly state the L1 weights did *not* transport and the gene-set+orientation is the portable unit. Calibration slope 0.50 / intercept −0.04 is reported (TRIPOD-positive).
3. **STROBE-MR methods & assumptions are thorough.** §2.10 discloses exposure/outcome sources, instrument thresholds, harmonisation, three estimators, pleiotropy (Egger intercept) and heterogeneity (Cochran Q / I²), and the sample-overlap limitation with a named correction it chose not to apply. The 45-test family BH is pre-specified and correctly applied in `10_mr_bh_family.csv`.
4. **Exemplary number provenance (§7).** Every reported figure is traced to a concrete `03_results/` file — a model of reproducibility that most submissions lack.
5. **Previously-flagged README over-claims are corrected** (Issue 7) — the Mars1-only score claim and the "4/5 hubs" claim now match the manuscript.

---

## 3. Questions for the authors

1. FIS1: given §3.3 labels it a mitochondrial-fission *marker* (not immune-localised), why does the English Abstract state all six hubs localised to monocytes/APC? Will you apply the Chinese-abstract carve-out to the English text?
2. The locked L1 model zero-weights 7/29 signature genes (§3.4). Should the "30-gene signature" be re-described as a "fixed-orientation 30-gene set" to avoid implying 30 independent weighted predictors?
3. For IFN-γ, please reconcile the §3.7 "4/5 antigen-presentation genes" prose with `08_candidates_drugs.csv` (4/7; HLA-DQB1 not in rescued list). Which denominator is correct?
4. The repositioning metric is explicitly *not* a direct-target overlap (§2.8, §5.9). Why then use "direct-target validation still pending" in the Conclusions? What, specifically, is the "target" awaiting validation?
5. STROBE-MR 9b: will you publish the per-SNP drop-list as a supplementary CSV rather than "available on request"?
6. Confirm §3.10 in the submitted file is not truncated (the source I received ends mid-word at "no causal claim for the hub i…").

---

## 4. What I actually checked

- **Abstract (EN + CN) vs body:** verified the MR null is reported in the Abstract (not buried); flagged the EN-abstract FIS1 localisation over-statement (Issue 2) and the "therapeutically addressable" verb (Issue 1).
- **`10_genetics_mr_outcome5086_28ddeath.csv`:** confirmed all IVW OR 0.92–1.12, P ≥ 0.235; CD14 Egger P = 0.0488 (df = 4), `p_fdr_bh` = 0.487; FCGR3A "insufficient_instruments."
- **`10_mr_bh_family.csv`:** confirmed only one family-significant test (CD74 crit-care WM, q ≈ 2.99×10⁻¹⁷, reversed direction); CD14 28d-death Egger family q = 0.730; susceptibility entirely null.
- **`09_external_validation.csv`:** confirmed AUC 0.6382 (CI 0.5317–0.7475), locked-L1 0.5848, IRG 0.604, HLA-DQA1 missing in test set — all match manuscript.
- **`08_candidates_drugs.csv`:** confirmed Table 2 fractions; detected IFN-γ 4/7 vs §3.7 prose 4/5 mismatch (Issue 4).
- **`S02_immunoparalysis_score.csv`:** confirmed Mars1 median ≈ −0.79, Mars2 ≈ −0.75 (README "Mars1/Mars2 cluster" claim now correct).
- **`README.md`:** confirmed the two prior-round over-claims (Mars1-only; 4/5 hubs) are corrected; flagged residual "immune-restorative" repo phrasing (Issue 7).
- **STROBE-MR / TRIPOD scan:** methods/assumptions largely complete; 9b drop-list gated "on request" (Issue 5); EPV not stated (Issue 6).
- **Format scan:** MODZ undefined, inline-only figure refs, Mann–Whitney two-sided not stated, possible §3.10 truncation (Issue 8).

**Bottom line:** The analytical core is reproducible and the MR null is honestly disclosed — a real strength. But the manuscript's *headline verbs* ("anchored," "therapeutically addressable," "direct-target validation pending") out-run the evidence, the English Abstract makes a factually false localisation claim for FIS1, and the repositioning denominator is internally inconsistent. These are fixable by rewording + one table correction, but the evidence level argues for **Option B: downgrade/reframe the article type** rather than present as a standard translational Research Article.
