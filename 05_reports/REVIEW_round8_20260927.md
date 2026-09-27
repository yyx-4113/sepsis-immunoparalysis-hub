# Round-8 Independent Multi-Panel Review — v1.7.0 (consolidated editor report)

**Manuscript:** *Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning*
**Version reviewed:** v1.7.0 (commit c07cd94, tag v1.7.0)
**Date:** 2026-09-27
**Reviewers:** A1 domain/sepsis-immunology, A2 design/biostat/MR, A3 implementation/provenance, A4 venue editor/reporting — each with no knowledge of prior rounds (independence enforced; `05_reports/review_r8/_PANEL_BRIEF.md`).

---

## 1. Independence statement

Four reviewers received self-contained briefs forbidding any prior review (`REVIEW_*.md`, `RESPONSE_*.md`, `review_r7/`, `.workbuddy/`, git history). Each recomputed headline numbers from source CSVs with their own scripts. **Evidence independence worked:** the single most-repeated defect is the **FIS1-as-hub internal contradiction** (raised independently by A1 and implied by A4), and a concrete data-availability falsehood was caught by A3 and editor-verified — neither is visible to a gate that only re-checks arithmetic. Disagreements were minor and adjudicated below (§5).

---

## 2. Verdict table

| Reviewer | Verdict | One-line rationale |
|---|---|---|
| A1 domain | **Major Revision** | Methodological transparency high, but FIS1-hub contradiction, 08b/S08 inconsistency, novelty boundary & literature gaps weaken credibility. |
| A2 design/MR | **Major Revision** | All numeric assertions recompute exactly; issues are provenance/framing (DCA figure-derived numbers, IRG CI, overlap bias direction, EPV CI). |
| A3 provenance | **Major Revision** | Result-layer provenance excellent & audit gate green, but data-availability claim false (01_data gitignored) and audit gate has slack spots. |
| A4 venue | **Major Revision** | STROBE-MR checklist gaps, headline/caveat mostly balanced (good), but "intervention targets" noun slightly over-reaches, data-availability overclaim. |

**Distribution:** 4 × Major Revision; 0 desk-reject; 0 Tier-0 (conclusion-invalidating). The analytical core (Tier-1 biology, MR self-criticism, honest external validation) is sound.

---

## 3. Cross-verification table (manuscript claim vs independent recomputation)

| # | Location | Manuscript claim | Independently recomputed | Checked by | Verdict |
|---|---|---|---|---|---|
| 1 | `08b_clinical_translation.csv` | `rescue_fraction_S08` IL-7/GM-CSF/IFN-γ = 1.0 / 0.833 / 0.714 | `08_candidates_drugs.csv` (Table 2) = 0.80 / 0.667 / 0.571 (systematic +1 numerator) | A1 + **editor** | **DISCREPANCY** (internal inconsistency) |
| 2 | Data availability (§254) | "processed expression and phenotype matrices … available in the repository" | `git ls-files 01_data` = 0; `.gitignore` excludes `01_data/`; only `03_results/` (45 files) tracked | A3 + **editor** | **FALSE claim** |
| 3 | §3.4 (line 117) | DCA NB positive 0.10–0.75, →0 at ~0.77 | deposited CSV has only `nb_thr0.20/0.30/0.50` (0.36/0.28/0.08); 0.10/0.75/0.77 are figure-derived | A2 | **Provenance gap** |
| 4 | §3.4 | "their confidence intervals overlap" (signature vs IRG) | IRG 0.604 has **no CI** in CSV; only signature has CI | A2 | **Unsupported phrasing** |
| 5 | §3.10 / §7 | I² "up to 0.50" | max I² = 0.5018 (FIS1 critical-care IVW) | A3 | rounds to 0.50 (OK; gate tolerance 0.51 loose) |
| 6 | §3.10 | family q: CD74-crit WM ≈3e-17, Egger 0.79, CD14-28d-Egger 0.73 | recomputed identical (BH on 45 p) | A2 | MATCH |
| 7 | Abstract / §3.10 | min primary-outcome IVW P ≥ 0.23 | min = 0.2359 (CD14) | A2 | MATCH |
| 8 | §3.5/§7 | external AUC 0.638 (CI 0.532–0.748); L1 0.585 | 0.6382 (CI 0.5317–0.7475); locked 0.5848 | A3 | MATCH |
| 9 | §3.4/§7 | calibration slope 0.50 / intercept −0.04 | 0.5028 / −0.0382 | A3 | MATCH |
| 10 | §7 (16 sampled rows) | 802 / 3597 / 448 / 23-22-21 / −0.79 / 6 hub / 30 gene / CV 0.659·0.750 / 29-30 / L1000 20413 | all recompute from cited CSVs | A3 | MATCH |
| 11 | Audit gate | `check_audit_assertions.py` green | exit 0; 15/15 pass (not silent no-op) | A3 | MATCH (but slack — see T2-10) |

**Editor note:** rows 1 and 2 were independently reproduced by the editor from raw sources; both hold. No headline *numeric* contradiction with source CSVs was found — the defects are (a) an internal file-vs-file inconsistency, (b) a false repository claim, and (c) design/framing issues a gate cannot catch.

---

## 4. Graded consolidated issue list

### Tier 1 — headline / central-concept defects (must fix before any submission)
- **T1-1. FIS1 is called a "hub" while simultaneously described as "non-immune, up-regulated, co-expression passenger, not a mechanistic target."** (A1-P2; reinforced by A4-Issue6 framing). The tri-method ML consensus selected FIS1 purely on survival-association + co-expression, not immune biology; presenting it as one of "six hub genes" in title/abstract (line 14)/§3.3 (114)/§6 (218) contradicts the manuscript's own caveat and weakens the hub concept. **Fix (editor-adopted, less disruptive than removal):** reframe as **"five immune hubs (CD74/HLA-DQA1/CD14/FCGR3A/HAVCR2) + one co-expression passenger (FIS1, mitochondrial-fission, Mars1 logFC +1.26)"**; exclude FIS1 from hub-level mechanistic claims; optionally add an immune-annotation filter to the hub definition. Update title/abstract/§3.3/§6 accordingly.

### Tier 2 — analyses to add, reconcile, or reword (substantive)
- **T2-1. Reconcile `08b_clinical_translation.csv` vs `08_candidates_drugs.csv` rescue fractions.** (A1-P3; editor-verified). IL-7/GM-CSF/IFN-γ read 1.0/0.833/0.714 in 08b but 0.80/0.667/0.571 in Table 2/S08 (a +1-numerator inflation landing exactly on the three top-recommended drugs). Define one canonical concordance (keep Table 2's DEG_0.3-gated fraction as primary), relabel the 08b column (e.g. `rescue_fraction_directional`), and add a sentence that ordering is unchanged under both definitions.
- **T2-2. Correct the data-availability claim.** (A3-A7/A8; editor-verified). "Processed expression and phenotype matrices … available in the repository" is false because `01_data/` is gitignored. Either (a) commit `GSE65682_pheno.csv` (with `group`) + the expression matrix so 760/42 and 802 are reproducible, or (b) rewrite: matrices are regenerated by provided scripts from public GEO/ArrayExpress and are **not committed** (see `.gitignore`); only result tables/figures/scripts are versioned. At minimum fix the wording.
- **T2-3. Use ImmunoSep as a *caution* for the repositioning axis, not only as endotype support.** (A1-P5). IFN-γ in low-mHLA-DR sepsis (ImmunoSep) showed SOFA improvement but no 28-day mortality benefit and more haemorrhage, 53% unclassifiable — directly tempers the antigen-presentation-restoration axis (IFN-γ/GM-CSF). Add to §3.8/Discussion.
- **T2-4. State MR sample-overlap bias direction explicitly.** (A2-#3). "Hypothesis-generating" alone is insufficient: overlap biases the ratio estimate *away from null, inflating OR and shrinking SE* — the single family-significant result (CD74 critical-care WM) is the most vulnerable, not a robust finding.
- **T2-5. Reframe the CD74 critical-care Egger SE inversion.** (A2-#2). With n=3, Egger df=1 is effectively uninformative; the SE<IVW-SE inversion is a fragility signal, *not* a "would-have-been-significant" result. Reword so it is not read as a lost significance.
- **T2-6. Quantify CV-AUC optimism.** (A2-#5). EPV≈3.8; add a 95% CI / bootstrap optimism for the within-cohort CV AUC 0.659 (the 0.021 gap to external 0.638 may understate selection-stage optimism).
- **T2-7. Fix the IRG "CI overlap" phrasing.** (A2-#6). IRG 0.604 has no CI; rephrase to "IRG point estimate falls within our signature's 95% CI" and/or report a DeLong paired test on the 106 shared samples.
- **T2-8. State the novelty boundary.** (A1-P1). Mars1 immunoparalysis = Scicluna 2017's defining axis; the 5 immune hubs recapitulate known biology. Explicitly declare the genuine contributions are methodological (tri-method ranking, externally validated signature, LINCS-scored shortlist, null MR) — not biological discovery.
- **T2-9. Close literature gaps.** (A1-P6). (i) mHLA-DR as immunoparalysis biomarker + threshold literature; (ii) immune-checkpoint blockade — PDCD1 (PD-1) is up-regulated and HAVCR2 (TIM-3) is a hub, yet anti-PD-1/PD-L1/CTLA4 are absent from the 7-drug list and undiscussed; (iii) broader endotype literature (Seymour SRS phenotypes). At minimum discuss why checkpoint blockade was excluded or add it.
- **T2-10. Harden the audit gate.** (A3-A1,A2,A4,A5,A10). Add: (a) IVW/WM p re-derivation (Wald), not only Egger; (b) assert L1-locked external AUC 0.585; (c) read `HUBS` from `S05_hub_genes.csv` (not hardcoded); (d) tighten I² tolerance to ≤0.505 and assert the specific FIS1-critical-care cell; (e) extend the "no exact-0 p" scan to DEG tables (CD14 adj.P=0.0 underflow is disclosed but ungated).
- **T2-11. Upgrade the LINCS single-sign defect to Limitations.** (A1-P7). The rescue metric aggregates all 22 genes with one sign, co-rewarding PDCD1/LAG3 up-regulation and glucocorticoid MHC-II induction; state explicitly that LINCS evidence ranks hypotheses only.
- **T2-12. Soften "intervention targets" → "intervention hypotheses".** (A4-Issue6). Headline/caveat balance is mostly good; change the noun in Abstract/§4/§6 to remove residual over-reach while keeping "direct-target validation still pending."
- **T2-13. Reconcile GM-CSF opposing evidence.** (A1-P4). §3.8 cites Bo 2011 (no mortality benefit for G-/GM-CSF in unselected sepsis) yet still prioritises GM-CSF; add the endotype-stratified hypothesis caveat.
- **T2-14. Clarify §2.10 dual-correction framing.** (A4-Issue5). State the 45-test family BH was the pre-specified primary; the per-outcome 15-test `p_fdr_bh` is reported for completeness only.
- **T2-15. STROBE-MR items 9a/9b.** (A4-Issues1–4). Add variant-selection flow (identified→post-clump→post-harmonisation→analysed per gene); state Steiger directionality handling (cis-eQTL proximity or a test); add a power/min-detectable-OR statement; declare the F>10 weak-instrument rule (all 27 retained SNPs F=30.7–2789.5).

### Tier 3 — format / checklist (low risk)
- **T3-1.** Deposit a full DCA threshold table (NB at 0.05/0.10/0.20/0.30/0.50/0.75/0.77) so "0.10–0.75 positive, 0.77→0" is numerically traceable (A2-#4).
- **T3-2.** References 21 (missing volume) and 32 (single author + "et al.", no vol/issue/pages) — fix Vancouver uniformity (A4-Issue7).
- **T3-3.** Trim abstract to target journal's word limit; move 23/25 detail and per-estimator OR ranges into body (A4-Issue8).
- **T3-4.** Add a Supplementary File Inventory mapping every in-text S01–S11 / figure / CSV citation to a deposited file (A4-Issue11).
- **T3-5.** Replace the hardcoded `PROJ` path in `_mr_diagnostics.py` with a relative path for portability; note the figure is generated deterministically from `10_mr_bh_family.csv` (A3-A6).
- **T3-6.** Add an Ethics clause noting source cohorts (GSE65682, E-MTAB-4451) carried their own IRB approval/consent, supporting the re-analysis exemption (A4-Issue9).

---

## 5. Consensus / complementarity / disagreement

**Consensus (all 4):** (i) the result-layer provenance and the MR-Egger t-distribution fix are genuine strengths; (ii) external validation is honestly scoped ("comparable to, not better than"); (iii) the glucocorticoid positive-control caveat is a real safeguard; (iv) the manuscript is *not* desk-rejectable and *not* a discovery paper — it is a computational re-analysis; (v) FIS1 framing and data-availability wording must change.

**Complementarity:** A1 (biology/novelty) + A4 (article-type) jointly establish the re-analysis positioning; A2 (stats) + A3 (provenance) jointly establish that numbers are correct but provenance claims over-reach; A3's audit-gate slack (#10) is the actionable bridge to make gates catch future drift.

**Disagreements (adjudicated):**
- *FIS1: remove vs reframe.* A1 offers removal as an option; editor adopts **reframe as passenger** (less disruptive, retains the co-expression finding, edits agree) rather than dropping it — but the headline "6 hub genes" must become "5 immune hubs + 1 passenger."
- *Severity of data-availability.* A3 rates it a real false claim (Tier-2); A4 folds it into deposition/ethics. Editor adopts **Tier-2** because a reproducibility reviewer cloning the repo cannot obtain the processed matrices.
- *"Intervention targets" noun.* A4 flags slight over-reach; A1/A2 silent. Editor adopts the soft-touch change (T2-12).
- *Article type.* Unanimous: position as **computational re-analysis / bioinformatics research article**; explicitly avoid "discovery." No downgrade to a brief note is required.

---

## 6. Priority must-fix list

**DESK-REJECT flags:** none.

**Must change (substantive, before submission):**
1. T1-1 FIS1 hub→passenger reframing (title/abstract/§3.3/§6).
2. T2-2 data-availability false claim → rewrite or commit pheno/expression subset.
3. T2-1 reconcile 08b vs S08 rescue fractions.
4. T2-3 ImmunoSep as repositioning caution.
5. T2-4 MR overlap bias direction.
6. T2-8 novelty boundary statement.

**Must reword / add (strengthens, not blocking):** T2-5, T2-6, T2-7, T2-9, T2-10, T2-11, T2-12, T2-13, T2-14, T2-15.
**Format (do at copy-edit):** T3-1…T3-6.

**Must-add-analysis vs must-reword split:** Only T2-6 (CV-AUC CI/bootstrap) and T2-15/STROBE-MR items (variant-flow, Steiger, power, F>10) and T3-1 (DCA table) require *new analysis/artefacts*; everything else is rephrasing or reconciliation.

---

## 7. What stands up (do NOT change)

1. Cross-platform external validation is disciplined and honest (locked model, fixed orientation, L1-weights-don't-transport 0.585 correctly scoped). 
2. MR layer self-criticism is exemplary: phenotype-matched primary outcome, pre-specified 45-test BH, sample-overlap disclosed, single family-significant result correctly read as genotype–severity (reversed direction) not causal. 
3. MR-Egger p-values are genuinely t(n−2)-corrected and the audit assertion #4 protects this (the strongest gate assertion). 
4. §7 number-provenance table is reproducible from cited CSVs (16 sampled rows all match). 
5. Glucocorticoid positive-control caveat is a real, non-routine honesty check. 
6. Headline/caveat balance in the Abstract is honest after v1.7.0 ("addressable axis" fully removed; "direct-target validation still pending" retained).

---

## 8. Recommended handling path

**Option A — restructure & resubmit as the same article type (RECOMMENDED).** The analytical core is sound; the required changes are (a) one central-concept reframing (FIS1), (b) one false repository claim, (c) several provenance/framing reconciliations, and (d) STROBE-MR completeness. None require new experiments. Position as a **computational re-analysis / bioinformatics research article**; avoid "discovery/novel target" language.
**Option B (downgrade to brief note)** — not needed; the work has enough analytic substance for a full research article.
**Option C (wording-only)** — **insufficient**: T1-1 and T2-2 are substantive, not cosmetic.

---

## 9. Process lessons (what gates could not catch, and how to extend them)

1. **A green audit gate verifies arithmetic and single-file provenance, not design-layer or cross-file consistency.** The two concrete defects (FIS1 self-contradiction; 08b vs S08 rescue inflation) are *consistency* problems a number-checking gate cannot see. **New assertion proposal:** a "claim-vs-self-description" check — assert that no gene described in §3.3 as "passenger / non-mechanistic / non-immune" is simultaneously named a "hub" in the title/abstract; and a "cross-file concordance" check that `08b.rescue_fraction_S08` equals `08_candidates_drugs.rescue_fraction` (or that the column is explicitly relabelled directional).
2. **Repository-claim assertion.** The data-availability sentence should be gated: assert the files it names are actually `git ls-files`-tracked, or the sentence must say "regenerated by script, not committed."
3. **Figure-derived numbers.** DCA thresholds 0.10/0.75/0.77 lived only in a PNG. Any numeric claim traced to a figure should also be deposited as CSV (T3-1).
4. **IVW/WM p-values were ungated.** The central negative claim ("no primary IVW significant") rested on p-values the gate never re-derived (T2-10a).
5. **Single-direction LINCS metric** is a structural limitation that should sit in Limitations, not only mid-text (T2-11).

---

*Panel files:* `05_reports/review_r8/A1_domain_sepsis_immunology.md`, `…/A2_design_biostat_mr.md`, `…/A3_implementation_provenance.md`, `…/A4_venue_editor_reporting.md`, `…/_PANEL_BRIEF.md`.
