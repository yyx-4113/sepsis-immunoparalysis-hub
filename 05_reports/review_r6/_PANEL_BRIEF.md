# Round 6 Panel Brief — independent review of the sepsis immunoparalysis hub-gene manuscript (v1.5.0)

Repository root: `D:\2026.9\极速交付9月会员日优惠套路\05_多组学+虚拟敲除药物发现\方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位`
Manuscript under review: `05_reports/manuscript.md` (288 lines, v1.5.0)
Outputs: `05_reports/review_r6/A{1..4}_{role}.md`

---

## Independence discipline (mandatory)

**Forbidden to read** (these carry priors from earlier rounds and would destroy independence):
- `05_reports/REVIEW_round*.md` (any round 1–5)
- `05_reports/review_r*/` — any earlier round directory or file inside them
- `05_reports/review/` (round-1 directory)
- `RESPONSE_*.md`, `REVISION_*.md`, `SUBMISSION_MANIFEST.md`
- `author_verification_statement.md`, `GITHUB_DEPOSIT_SOP.md`
- any project-overview / task-status file
- **other reviewers' outputs in this directory** — you are blind to them

**Do not assume the manuscript is mature or has passed previous review.** Treat it as a
first submission to a journal you respect. It may have been through five prior revision
rounds; that is irrelevant to you and knowing about it must not lower your bar. If
anything, assume that obvious defects have already been fixed, soyour value lies in
finding what remains.

**Every judgement must come from text or source data you read yourself.** Any claim in
the manuscript that you *can* verify from the files in `03_results/`, you **MUST** verify
by recomputation. A point you did not check is worth less than one you did.

**Do not mention what tools you use** in your report. Write review comments only — no
"the Bash tool showed", no "I grepped", no tool names. Report findings, not process.

---

## What the manuscript is (orientation only — verify everything yourself)

Single-author computational study. Re-analysis of public bulk transcriptome
**GSE65682** (GPL13667; 802 samples: 760 ICU sepsis, 42 healthy controls; 479 with an
assigned MARS endotype and 28-day survival). The pipeline: differential expression →
immune-function score (antigen-presentation/T-cell minus exhaustion) → WGCNA-style
degree-centrality network → tri-method ML consensus (LASSO + Random Forest + univariate)
→ six hub genes (**CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1**) → cell-type localisation
→ 30-gene immune-risk signature → drug repositioning (LINCS L1000 reverse connectivity
+ mechanism-anchored candidates) → two-sample Mendelian randomisation
(eQTLGen × UKB sepsis GWAS) as causal support.

Headline numbers the manuscript asserts (all must be re-derived by the implementation
auditor; the design reviewer should judge whether each *supports the claim built on it*):

- Mars1 direction: 23/25 consensus immune genes directionally down; 22/25 significant at
  FDR<0.05 (the 22 include up-regulated PDCD1, so 21 both down *and* FDR-significant).
  HLA-DRB1 Δ=−0.89, CD74 Δ=−0.76, CD14 Δ=−0.77, FCGR3A Δ=−0.61, all P<1×10⁻⁸.
- Immune-function score lowest in Mars1 (median −0.79).
- Signature AUC: 5-fold CV 0.659; training 0.750; external 0.638; locked L1 0.585.
- MR: 5 genes × 3 estimators (IVW / MR-Egger / weighted median) × 3 outcomes = 45 tests.
  CD74 critical-care MR-Egger q≈1.5×10⁻¹¹, weighted median q=0; susceptibility Egger
  q≈0.0025. CD14 28-day-death Egger q≈0.058. Max I² 0.502 (FIS1 critical care).
  27 instruments retained after harmonisation (CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6,
  FIS1 8; FCGR3A excluded for insufficient instruments).
- Drug repositioning: IL-7 reversal score 0.422; top candidates incl. MK-2206, dinaciclib;
  "IFN-γ reverses 5/5 hub genes".
- Claimed literature gap: no prior study has *combined* MARS endotype assignment,
  consensus network + tri-method ML hub identification, cell-type localisation,
  LINCS repositioning, and MR support in one framework.

---

## Source data available to you (use these; they are the source of truth)

All under `03_results/`. Relevant files include (list is indicative, explore the directory):

- Direction / score: `S01_immunoparalysis_direction.csv`, `S01_immunoparalysis_genes_in_mars1.csv`,
  `S01_mars1_deg.csv`, `S01_deg_sepsis_vs_ctrl.csv`, `S02_immunoparalysis_score.csv`,
  `S01_mars1_stratification.csv`
- Network / hubs: `S03_hub_degree.csv`, `S03_modules.csv`, `S03_module_trait_cor.csv`,
  `S03_key_module_genes.csv`, `S04_candidate_genes.csv`, `S05_hub_genes.csv`
- Signature / validation: `S06_signature_genes.csv`, `S06_auc_compare.csv`,
  `09_external_validation.csv`, `09_external_validation_coef.json`, `09_ext_risk_scores.csv`
- Cell type: `07_hub_celltype.csv`, `07_axis_celltype.csv`
- Repositioning: `08_candidates_drugs.csv`, `08_positive_control_check.csv`,
  `08_disease_signature.csv`, `08b_clinical_translation.csv`,
  `S08_l1000_rescue_trtcp.csv`, `S08_l1000_candidate_scores.csv`,
  `S08_l1000_positive_control.csv`, `S08_l1000_immuno_overlap.csv`
- MR: `10_genetics_mr.csv`, `10_genetics_mr_harmonised.csv`,
  `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr_outcome5086_harmonised.csv`,
  `10_genetics_mr_outcome4982_criticalcare.csv`, `10_genetics_mr_outcome4982_harmonised.csv`,
  `10_mr_bh_family.csv`, `10_genetics_mr_design.md`
- Reporting: `11_validation_design.md`, `journal_targeting.csv`,
  `reference_doi_audit.csv`, `generated_references.md`

Also present but **deliberately NOT tracked in git** (do not rely on, do not try to
re-download): `01_data/` holds ~43 GB of raw public data (GSE65682 matrices, LINCS
`.gctx`, GTEx eQTL, Davenport cohort). It exists on disk but the reproducible claims
must be checkable from `03_results/` alone. Do not attempt network downloads.

Figures live in `04_figures/` (10 files). Check that the manuscript's figure callouts
resolve to real files.

---

## Environment / trap list (do not burn your budget rediscovering these)

1. **Self-contained markers**: the immune-function score is computed from
   user-specified marker lists, so a "significant" score separation is partly by
   construction. Judge whether the manuscript is honest about this.
2. **Optimistic AUC**: the manuscript itself concedes the CV AUC is optimistic because
   marker curation used prior knowledge and gene selection reused the cohort. The
   *external* estimate is the honest one. Check the manuscript keeps this distinction
   intact everywhere and never lets the training/CV number carry a clinical claim.
3. **MR sample overlap**: eQTLGen and the UKB sepsis GWAS share participants, which
   biases standard errors downward. Check whether this is stated wherever the MR result
   is used, or only in the limitations.
4. **"Reversal" is a transcriptional proxy, not a functional rescue.** Check whether any
   sentence still implies functional rescue, and whether the co-rewarding of
   exhaustion-marker up-regulation is disclosed at the point of claim.
5. **Single-database literature search** and a claimed "no prior study" gap — check
   whether the gap claim is stated with appropriate hedging given only one database was
   searched.
6. **MR instrument counts are small** (CD74 has 3). An MR-Egger intercept from 3
   instruments is essentially uninformative about pleiotropy. Check that the manuscript
   does not read a null intercept as evidence *against* pleiotropy.
7. **I² varies by outcome** — a single range stated without saying which outcome it
   covers is imprecise. Check per-test tabulation exists.
8. **Consistency traps**: a value that appears in more than one place (title, abstract,
   methods, cover letter) can go stale in the second location. Grep for the *value*, not
   the expected location.
9. **Prior-round residue**: a previous round may have added a caveat in one section while
   leaving the original over-claim standing in another. Read the whole text; if a
   headline claim was merely *qualified elsewhere* rather than retracted, that internal
   contradiction is a Tier-0 finding. Quote both locations side by side.

---

## Output contract (mandatory for every item)

For every issue you raise, four parts — no exceptions:

- **【Problem】** one sentence, stating the defect.
- **【Evidence】** pinned to `file:line`, or table/section, **with exact numbers** — and
  the numbers you cite must be ones **you recomputed yourself** from `03_results/`,
  not numbers copied from the manuscript text.
- **【Why it matters】** concrete effect on conclusions / credibility / acceptance.
- **【Specific fix】** a **paste-ready English replacement sentence**, or an explicit spec
  for a new analysis (variables, strata, output columns).

Banned: "consider strengthening the discussion", "the authors should clarify",
"this could be improved", and any fix that is not paste-ready or fully specified.

Grade every item: **Tier 0** (conclusion-invalidating) · **Tier 1** (analysis to add) ·
**Tier 2** (wording) · **Tier 3** (format/reference/consistency).

## Also required in every report

1. **§ Stands up** — at least **3** items, with evidence. Explicitly mark things you
   *suspected were wrong* but verified as **correct**. This is a deliverable, not filler:
   it tells the author what must NOT be changed in the next revision.
2. **§ Questions for the authors** — state what you need to know; do not guess the answer.
3. **§ What I actually checked** — files read, commands run, values you recomputed vs the
   manuscript's stated value, with any discrepancy stated explicitly.

Close with your **verdict**: Accept / Minor revision / Major revision / Reject, and a
one-paragraph justification naming the single strongest reason.

## Deliverable

Write your report to `05_reports/review_r6/A{N}_{role}.md` using the Write tool.
Aim for 300–650 lines. Write the file; do not try to end the whole task.
