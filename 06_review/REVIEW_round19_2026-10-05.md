# REVIEW — Round 19 (manuscript v1.20.0, target BMC Medical Genomics)

**Manuscript:** "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and externally evaluates a 30-gene sepsis prognostic signature"
**Repo / tag:** `github.com/yyx-4113/sepsis-immunoparalysis-hub` · **v1.20.0** (annotated tag on commit `7704c9a`) · built on `v1.16.0` (`1212f7b`)
**Review date:** 2026-10-05 · **Editor:** 小团 (consolidating, independent of prior rounds)
**Panel:** 4 experts, blinded to each other and to all prior review/response/revision artifacts.

---

## 1. Independence statement

Mechanism: each expert received a self-contained brief (`06_review/round19_v1.20.0/_PANEL_BRIEF.md`) with an explicit forbidden-file list (no `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, prior `_gen_*.py`, `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, and no cross-reading of sibling reviewer files). Every expert was told to treat the manuscript as a first submission and to recompute any claim they could.

Evidence it worked — the diagnostic signature is present: experts hit the **same defects from different angles**. A1 (Domain) and A2 (Design) independently concluded the drug "prioritisation" is circular/tautological (A1 M4 ↔ A2 D4/D5/D6); A1 (Domain) and A4 (Venue) independently flagged the title/abstract "confirm" over-claim and the "methods-and-resources" article-type mismatch (A1 M1/M10 ↔ A4 F2); A2 (Design) and A3 (Implementation) independently found orphan MR artifacts (A2 D8 ↔ A3 T1-2). A3 — who read only numbers — found the arithmetic layer clean, which is the complementary (not contradictory) conclusion: the defects are in the **design/framing layer**, exactly where a gate cannot reach.

---

## 2. Verdict table

| Expert | Layer | Verdict | One-line rationale |
|---|---|---|---|
| A1 | Domain (sepsis immunology) | **Major revision** | Biology framing over-reaches: within-cohort "confirm", score not Mars1-specific, drug prioritisation circular, HAVCR2 weakest hub. |
| A2 | Design (stats / ML) | **Major revision** | Design-level honesty gaps: AUC optimism by scoring-rule, non-nested CV, L1000 positive-control failure + sign error, uncorrected hub-death p-values, MR residue in a results CSV. |
| A3 | Implementation (recompute) | **Accept numeric layer** | All 24/25 headline numbers reproduce; the lone "non-reproducing" item is a brief mis-statement, not a manuscript error. Two minor housekeeping fixes. |
| A4 | Venue (BMC editor) | **Minor revision** | Format-compliant and in scope; 4 must-fix (abstract drug list contradiction, figure-mapping hazard, commit-hash drift, article-type wording) + 1 recommended (TRIPOD note). |

**Distribution:** 2 × Major (substance), 1 × Accept (arithmetic), 1 × Minor (format). Consensus: the numeric backbone is sound; the paper is **over-claimed in framing and under-corrected in statistics**, not wrong in its numbers. Recommended handling: **restructure-and-resubmit as the same article type (Research article)** — not downgrade, and not wording-only.

---

## 3. Cross-verification table (numbers)

A3 recomputed 32 numbers directly from `03_results/` and `01_data/`. Editor re-verified the three most consequential findings flagged by A4/A2.

| # | Manuscript location | Manuscript claims | Independently recomputed | Who checked | Verdict |
|---|---|---|---|---|---|
| 1–29 | §7 provenance / Results | 802/760/42; 5 hubs down + FIS1 up +1.26; AUC 0.638/0.585/0.659/0.529; score med −0.792; DCA 0.30 crossover & 0.80 divergence; calib slope 0.50; DEG 3597/448; 23/25 down/22 sig/21 both; L1000 ranks; SRS 0.610/Δ+0.028; drug table; mortality 34.1%/19.9%; 30-gene; Zenodo DOI | All match to digit / stated rounding (`03_results/*.csv`, `01_data/GSE65682_pheno.csv`) | A3; editor spot-checked | **Reproduce** |
| 30 | Abstract (derived docx) L7 | "Seven agents prioritised, **including** positive-control glucocorticoids" | Source `manuscript.md` L14 has NO such clause; the 7 agents (IL-7/GM-CSF/IFN-γ/azi/lenali/thymosin/BCG) exclude glucocorticoids, which appear only as a disqualifying caveat (§3.9/§5.10) | A4 (docx); **editor confirmed source clean, error only in derived `BMC_structured_abstract.md` L7 + generated docx** | **Derived-artifact defect (fix the build source, not the manuscript)** |
| 31 | `S06_hub_death_association.csv` header | (MR layer removed in v1.20.0) | Header still carries `predicted_mr_direction, observed_mr_or_ivw, concordant` | A2 D8; **editor confirmed** | **Stale MR residue — strip** |
| 32 | Data availability / manifest | "evaluated commit 1212f7b tagged v1.16.0" (manuscript, correct) vs manifest "commit 7704c9a / tag v1.16.0" | `v1.16.0` = `1212f7b`; `7704c9a` = the v1.20.0 MR-removal commit (ancestor of tag `v1.20.0`, which is annotated on `7704c9a`); BMC-pack commit `15e1a20` sits *after* the tag and is untagged | A4 F4; **editor confirmed via `git rev-parse`** | **Manifest commit-drift — reconcile** |

No manuscript-reported number failed to reproduce. The cross-verification table therefore certifies the **arithmetic and provenance layer** (A3's scope), and isolates the genuine defects to **framing (A1/A4) and design honesty (A2)**.

---

## 4. Graded consolidated issue list

### Tier 0 — conclusion-relevant / must fix before acceptance
- **T0-1 (A1 M1 / A1 M10 / A4 F2).** Title/abstract/Conclusion sell "confirms the Mars1 immunoparalysis program," but Mars1 biology is read off the *same* GSE65682 that defined the endotype labels; there is **no independent cohort replication of Mars1 biology** (E-MTAB-4451 was used only for the mortality signature). The "methods-and-resources" self-label is not a BMC article-type option. → Reframe front matter to within-cohort "recapitulate," align article type to "Research article."
- **T0-2 (A1 M2).** The composite immune-function score is statistically identical in Mars1 and Mars2 (median −0.792 vs −0.752, P = 0.47); it indexes a *shared low-immune-activation axis*, not a Mars1-specific immunoparalysis readout. Presenting §3.2 as "lowest in Mars1" is non-discriminating; Mars1-specific immunoparalysis must rest on individual HLA-II gene directions.
- **T0-3 (A1 M4 ↔ A2 D4/D5/D6).** The "seven agents were prioritised" framing is circular: every candidate's immune-gene concordance lies at/below the paper's own 0.84 background (one-sided P ≥ 0.82); the IFN-γ gate is tautological (canonical MHC-II inducer vs an MHC-II axis); the L1000 rescue score is single-direction and **rewards up-regulating the Mars1-*up* exhaustion markers PDCD1/LAG3 (sign error)**, and an immunosuppressant (prednisone) ranks 3.2nd percentile — so 0/5 genuine immuno-stimulants recover. → Reframe §3.7/§4/abstract as **hypothesis-annotation / honest de-prioritisation**, not prioritisation.

### Tier 1 — analyses to add / reword (design honesty)
- **T1-1 (A2 D1).** External headline AUC 0.638 is the *equal-weight oriented-sum*; the fitted *locked-L1* transports at only 0.585 (95% CI 0.469–0.696, includes 0.5). The internal→external comparison mixes scoring rules (L1 internally, equal-weight externally), understating the like-for-like L1 drop (0.074). → Make locked-L1 0.585 the primary transport metric; equal-weight 0.638 a pre-specified sensitivity.
- **T1-2 (A2 D2).** The 5-fold CV AUC 0.659 is *not nested* — 30 genes selected on outcome labels before the split (EPV = 114/30 = 3.8). → Demote to "inner-loop CV after fixed feature selection"; add EPV caveat; consider nested CV.
- **T1-3 (A2 D9).** Hub 28-day-death p-values are uncorrected although the hub set was selected on the same outcome; HAVCR2 (0.0785) and HLA-DQA1 (0.0107) fail Bonferroni (0.0083). → Apply Holm across 6 hubs; report adjusted p; present HAVCR2 as exploratory.
- **T1-4 (A2 D3).** DCA: model = treat-all below 0.25 and collapses to treat-none (NB = 0) at 0.80; "diverges at 0.80" misreads "flags nobody" as benefit. → Report the usable 0.30–0.75 band with absolute NB + bootstrap CI; do not call 0.80 a divergence point.
- **T1-5 (A4 F1).** Derived abstract states glucocorticoids are *among* the prioritised agents — false (only a disqualifying positive control). → Fix `BMC_structured_abstract.md` L7 and regenerate docx.
- **T1-6 (A4 F4).** Manifest commit drift (7704c9a mis-attributed to v1.16.0). → Reconcile to "v1.20.0 (commit 7704c9a) builds on v1.16.0 (commit 1212f7b)".

### Tier 2 — wording / factual
- **T2-1 (A1 M3).** HAVCR2/TIM-3 is the weakest hub (logFC −0.35), absent from the external signature and from L1000; demote to "exploratory, bulk-down checkpoint transcript of uncertain cellular basis" or justify explicitly.
- **T2-2 (A1 M5).** Whole-blood HLA-II/CD74 *mRNA* used as immunoparalysis proxy without the explicit dissociation caveat vs monocyte membrane mHLA-DR (Monneret 2008; Venet & Monneret 2018).
- **T2-3 (A1 M6).** "IL-7's four response genes all fall below |logFC|≥0.3 in endotype-only contrast" is false for LCK (−0.404, retains). → "Three of four …; LCK retains."
- **T2-4 (A1 M9).** "Immunoparalysis/immune-risk signature" is a generic mortality signature (includes neutrophilic ELANE/MPO/S100A8 positively correlated with death). → Call it what it is; note the inflammatory arm in §3.4.
- **T2-5 (A2 D7).** Cellular-context table reports a single max-|r| "best cell type" where FIS1's strongest correlation is a *negative* −0.438 with monocytes; report full matrix with FDR threshold, or "no reliable context."
- **T2-6 (A1 M7 / M8).** Missing citations: a primary human-sepsis TIM-3/PBMC study (not just the 2024 review) where the bulk-down TIM-3 claim is made; and a FIS1 molecular-identity (mitochondrial fission 1 / DRP1-adaptor) reference.
- **T2-7 (A4 F3).** Upload PNGs named Fig1–Fig10 while captions use S-series; multi-panel mapping is non-sequential (S3A/B, S6A/B/C reversed). → Rename upload files to S-series, or supply explicit FigN→caption mapping.
- **T2-8 (A4 F5).** `manuscript.md` still has single unstructured abstract + non-standard "## Ethics statement"; the docx corrected these. → Back-port structured abstract + BMC ethics/consent headings into the source of truth.

### Tier 3 — format / repository hygiene
- **T3-1 (A4 F7).** Ref 16 trailing "?." punctuation.
- **T3-2 (A3 T1-2).** Remove/rename orphan MR files (`10_genetics_mr*.csv`, `10_mr_bh_family.csv`, `12_strobe_mr_checklist.csv`, `_mr_backup_20260927/`).
- **T3-3 (A2 D8).** Strip MR columns from `S06_hub_death_association.csv` (or delete if unused).
- **T3-4 (A3 T1-1).** Reconcile CV AUC 0.6586 (`S06_auc_compare.csv`) vs 0.6582 (`09_external_validation.csv`) — note or single-source.
- **T3-5 (A4 F6, recommended).** Add a short TRIPOD/CLIP-aligned prediction-model reporting note (model type, predictor set, validation scheme, optimism handling, calibration/DCA).

---

## 5. Consensus / complementarity / disagreement

**Consensus (all four):**
- The arithmetic and provenance layer is sound (A3) and the computational-reproducibility reporting is exemplary (A4) — §7 provenance, §2.11 AI disclosure, Zenodo, GitHub tag.
- The optimistic within-cohort CV, the single-direction LINCS metric, and the prednisone caveat are honestly disclosed — a real strength.
- No MR residue remains *in the manuscript text*; v1.20.0 is correctly carried.

**Complementarity (different layers, same conclusion):**
- A1 (biology) and A2 (design) independently conclude the drug "prioritisation" is circular/tautological and the L1000 evidence is non-discriminating — the genuine contribution is honest *de-prioritisation*, not a candidate list.
- A1 (front-matter over-claim) and A4 (article-type mismatch) independently flag the "confirm/methods-and-resources" framing.

**Disagreement (adjudicated):**
- **Severity on the numeric layer:** A3 returned "Accept" while A1/A2 returned "Major." A3's scope is arithmetic only; that does not certify the manuscript. Adopt the stricter verdict: the manuscript needs **Major-level framing + design-honesty revision**, but A3's "Accept numeric layer" is preserved as a layer-specific certificate (no number is wrong).
- **"Second external cohort AUC 0.659 (n=52)"** appeared in the *panel brief* but not in the manuscript. A3 flagged it as a brief mis-statement (T0 in A3's report). Adopted: the manuscript correctly separates within-cohort CV 0.659 from single external cohort 0.638 (n=106, 52 deaths). No manuscript change; the brief was corrected.

---

## 6. Priority must-fix list (for the author)

**Blocking acceptance (Tier 0 + the factual/derived defects):**
1. T0-1 — reframe title/abstract/Conclusion "confirm" → within-cohort "recapitulate"; article type → Research article.
2. T0-2 — §3.2 + abstract: score = shared low-immune-activation axis (Mars1≡Mars2, P=0.47); Mars1-specific immunoparalysis from HLA-II gene directions.
3. T0-3 — §3.7/§4/abstract: drug section = hypothesis-annotation / honest de-prioritisation, not prioritisation; acknowledge L1000 sign-error + positive-control failure.
4. T1-5 — fix derived abstract glucocorticoids contradiction (build source `BMC_structured_abstract.md` L7) + regenerate docx.
5. T1-6 — reconcile manifest commit drift.

**Must add / reword (Tier 1):**
6. T1-1 — locked-L1 0.585 as primary external transport; equal-weight 0.638 sensitivity.
7. T1-2 — CV 0.659 = inner-loop, not nested; EPV 3.8 caveat.
8. T1-3 — Holm-correct hub-death p-values (HAVCR2/HLA-DQA1 fail).
9. T1-4 — DCA 0.80 wording (collapse to treat-none, not divergence).

**Wording / factual (Tier 2):** T2-1..T2-8 (HAVCR2 demotion, mHLA-DR caveat, IL-7/LCK fix, generic-mortality wording, celltype table, 2 missing citations, figure mapping, back-port structured abstract).

**Hygiene (Tier 3):** T3-1..T3-5.

**No DESK-REJECT flag.** The defects are repairable by revision; the paper is in scope and format-compliant for BMC Medical Genomics.

---

## 7. What stands up (do NOT change)

Carried forward from the experts:
- Exact immunoparalysis direction counts (23/25 down, 22 sig incl. PDCD1 up, 21 both).
- FIS1 genuinely Mars1-up (+1.26, t +17.16) and honestly separated from the immune hubs.
- External validation is genuinely independent in cohort & platform (E-MTAB-4451 labels from its own SDRF; GSE65682 labels only select/orient genes; no patient overlap).
- Calibration slope 0.50 = over-confident is correctly framed (P=0.016 against slope=1).
- No residual feature/label resampling mismatch in the shipped code (historical bootstrap bug absent).
- Prednisone/dexamethasone positive-control discrepancy is a genuine, well-handled self-check.
- Endotype-only robustness of the myeloid/APC hubs (CD14/HLA-DRB1/CD74/HLA-DMA/FCGR3A/HAVCR2 retain |logFC|≥0.3 & FDR<0.05 vs Mars2–4).
- 36 Vancouver references, contiguous, all cited, all with DOI.
- DCA "diverges at 0.80" literal claim is data-true (model NB pinned at 0 while treat-all falls).

---

## 8. Recommended handling path

**A) Restructure-and-resubmit as the same article type (Research article).** The paper's strongest real contribution is an *auditable, honest computational pipeline + an external validation that is independent in cohort/platform + an experimental blueprint* — not a biological discovery. Swap the headline from "confirm/discover immune hubs" to "reproducible pipeline that recapitulates the Mars1 program and honestly evaluates a mortality signature + a drug-repositioning hypothesis set." This converts a fragile over-claim into a stable methods/validation finding. **Not B (downgrade article type)** — A1/A4 agree it is suitable for BMC Medical Genomics. **Not C (wording-only)** — the framing and statistical-honesty changes are substantive.

---

## 9. Process lessons (what the gate could not catch)

- A green audit gate verified arithmetic; it could not ask "is the composite score Mars1-specific?" (A1 M2) or "does the L1000 metric reward the wrong direction on exhaustion markers?" (A2 D5). **New gate assertions to extend coverage to the design layer:** (i) assert Mars1-vs-Mars2 score P ≥ 0.4 explicitly stated as "non-discriminating"; (ii) assert the L1000 query splits Mars1-down vs Mars1-up genes into signed directions and that no immunosuppressant ranks in the top 10%; (iii) assert hub-death p-values are Holm-adjusted and reported as such; (iv) assert the external primary metric is the *locked* model, not a post-hoc equal-weight score.
- The "confirm" front-matter over-claim is the same class of defect the project has hit before (Round-16 "fc5473b mislabeled v1.16.0"): a stale string/claim left standing while the body qualifies it. **Rule reinstated:** for every over-claim the panel flags, check whether the *headline* was retracted or merely *qualified elsewhere* — the latter is a P0 self-contradiction.

---

*Consolidated by the editor (小团) on 2026-10-05. Expert files: `06_review/round19_v1.20.0/A1_domain.md`, `A2_design.md`, `A3_implementation.md`, `A4_venue.md`. This report and all four expert files are the audit trail for the v1.21.0 revision.*
