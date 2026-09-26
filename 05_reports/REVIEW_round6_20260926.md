# Round 6 Independent Review — sepsis immunoparalysis hub-gene manuscript (v1.5.0)

**Date:** 2026-09-26 · **Manuscript:** `05_reports/manuscript.md` (288 lines, v1.5.0, commit `6b5a1f2`, tag `v1.5.0`)
**Panel:** A1 domain (sepsis immunology) · A2 design (biostatistics / causal inference) · A3 implementation (provenance auditor) · A4 venue (editor / reporting standards)
**Expert reports:** `05_reports/review_r6/A1_domain_sepsis_immunology.md`, `A2_design_biostatistics_causal.md`, `A3_implementation_provenance.md`, `A4_venue_editor_reporting.md`
**Shared brief:** `05_reports/review_r6/_PANEL_BRIEF.md`

---

## 1. Independence statement

Each expert was dispatched with a self-contained brief and a hard prohibition on reading
`REVIEW_round*.md`, `review_r*/`, `review/`, `RESPONSE_*`, `REVISION_*`, `SUBMISSION_MANIFEST.md`,
`author_verification_statement.md`, `GITHUB_DEPOSIT_SOP.md`, any project-overview/task-status file,
**and the other reviewers' outputs**. Each was told explicitly to treat the manuscript as a first
submission and to assume prior rounds (if any) had already removed the obvious defects, so their
value lay in finding what remained. Each was required to recompute any checkable number from
`03_results/` rather than quoting the manuscript's own figures.

**Evidence that independence actually worked.** Four defects were hit independently by reviewers
with no knowledge of one another, from different angles:

| Defect | Who found it | Angle of attack |
|---|---|---|
| Immune score does **not** separate Mars1 from Mars2 | A1 (P=0.467), A2 (P=0.47) | A1: clinical plausibility · A2: inferential validity |
| IFN-γ "reverses 5/5" is wrong (should be 4/5) | A1, A2, A3, A4 | all four, via different files |
| CD74's headline MR signal does not survive | A1 (Egger SE < IVW SE red flag), A2 (IVW q=0.126 non-significant), A3 (Egger p uses wrong distribution), A4 (direction opposite to expression model) | four independent routes to one verdict |
| Calibration / DCA claimed but does not exist | A2 (no calibration; net benefit below treat-none), A3 (`S06_dca.png` is the discovery cohort), A4 (`06_prognosis.R:27` is a `# TODO` stub; ref [18] does not support DCA) | three independent routes |

That clustering is the diagnostic signature the panel protocol looks for. It is not a diffuse panel.

**Editor verification performed.** The single most severe claim — A3's report that every MR-Egger
p-value was computed on a normal rather than a t(n−2) distribution — was **independently
reproduced by the editor** with a purpose-written script reading only the raw CSVs
(`02_scripts/python/_editor_verify_egger.py`):

- 15 MR-Egger rows located across the three outcome files.
- **14 consistent with the normal distribution; 0 consistent with t(n−2).**
- Headline CD74 critical-care: β=0.798, SE=0.111, reported p = **6.63×10⁻¹³**; correct t with
  df = 3−2 = **1** gives **p = 0.088**. Ratio ≈ **1.33×10¹¹**.
- The same rows record `Q_df` (= n−2), so the degrees of freedom were known to the pipeline and
  not used.

The editor additionally re-derived two further Tier-0 items from source:
- **FIS1** in `S01_mars1_deg.csv`: logFC = **+1.261**, t = **+17.16** (up-regulated), while the
  other five hubs are down (CD14 −0.766, CD74 −0.758, HLA-DQA1 −0.530, FCGR3A −0.610, HAVCR2 −0.349).
- **Mars1 vs Mars2** immune score (Mann–Whitney, tie-corrected, n=132 vs 176): medians −0.7917 vs
  −0.7520, **P = 0.52** (reviewers' independent estimates 0.467 / 0.47 — same conclusion). Mars1 vs
  Mars3 P = 6.5×10⁻¹⁹; Mars1 vs Mars4 P = 6.4×10⁻⁴.

Items below marked **[editor-verified]** were reproduced by the editor directly; all others are as
reported by the named reviewer.

---

## 2. Verdict table

| Reviewer | Lens | Verdict | Single strongest reason given |
|---|---|---|---|
| A1 | Domain — sepsis immunology | **Major revision** | "Mars1-down axis" is inseparable from the erythroid/heme module that actually dominates the network; monocyte localisation contradicted by the authors' own data |
| A2 | Design — biostatistics / causal inference | **Major revision** | The most citable MR finding is non-significant under the paper's declared primary estimator (IVW) and under any corrected family |
| A3 | Implementation — provenance | **Major revision** | MR-Egger p-values used the wrong reference distribution; the repo's own audit script passes green anyway |
| A4 | Venue — editor / reporting standards | **Major revision** | Abstract omits the MR layer while claiming a three-tier design, and claims calibration/DCA that does not exist |

**Distribution: 4 / 4 Major revision. No reviewer returned Accept or Minor.**

---

## 3. Cross-verification table

Every row where the manuscript's stated value differs from an independently recomputed value.

| # | Manuscript location | Manuscript claims | Independently recomputed | Checked by | Verdict |
|---|---|---|---|---|---|
| 1 | §3.x MR (headline); Table 3/4 | CD74 critical-care MR-Egger **q ≈ 1.5×10⁻¹¹** | p = 6.63×10⁻¹³ (normal) → **p = 0.088** with t(df=1); q ≈ 0.79 after BH | A3 + **[editor-verified]** | **FAIL — Tier 0** |
| 2 | §3.x MR | CD74 susceptibility Egger q ≈ 0.0025 | → **q ≈ 0.90** with correct t | A3 | **FAIL — Tier 0** |
| 3 | §3.x MR | CD14 28-day-death Egger q ≈ 0.058 | p 0.00511 → **0.0488** with t(df=4); q → 0.73 | A3 | **FAIL — Tier 0** |
| 4 | §3.x MR | 3 tests in the 45-test family reach q<0.05 | **1** survives, and it is a sign-reversal estimator | A3 | **FAIL — Tier 0** |
| 5 | §3.x MR | CD74 weighted-median "q = 0" | p stored as exactly 0.0 (floating-point cancellation); true q ≈ **3×10⁻¹⁷** | A2, A3 | **FAIL — Tier 1** |
| 6 | §3.x MR | CD14 "P < 1×10⁻³⁰⁰" | recomputing from the file's own `t` column gives adj.P ≈ **2.8×10⁻²⁰** — a 280-order-of-magnitude discrepancy | A3 | **FAIL — Tier 1** |
| 7 | §2.8, §3.3, S11 | "all six hub genes down-regulated" in Mars1 | **FIS1 logFC = +1.261, t = +17.16 (up)** | A3 + **[editor-verified]** | **FAIL — Tier 0** |
| 8 | §3.2 / Abstract | immune score "lowest in Mars1" implying Mars1-specific immunoparalysis | Mars1 vs **Mars2 P = 0.52** (−0.7917 vs −0.7520). Separation exists vs Mars3/Mars4 only | A1, A2 + **[editor-verified]** | **FAIL — Tier 0** |
| 9 | Abstract Methods/Results/Conclusions | three-tier design incl. MR | **no mention of MR, eQTL, or GWAS anywhere in the abstract**; MR on the primary outcome null for all 5 genes (OR 0.92–1.12, P≥0.24) | A4 | **FAIL — Tier 0** |
| 10 | Abstract; §3.9 | IFN-γ "reverses **5/5** hub genes" | `08_positive_control_check.csv` = **4/5**; `08_candidates_drugs.csv` = 5/7. HLA-DQB1 fails (logFC −0.203, DEG_0.3=False) under the paper's own rule | A1, A2, A3, A4 | **FAIL — Tier 2** |
| 11 | Table 2 (reversal scores) | IL-7 1.00, IFN-γ 0.71 | under the paper's own \|logFC\|≥0.3 rule: **IL-7 0.80, IFN-γ 0.57** — scores change and the shortlist reorders | A1 | **FAIL — Tier 2** |
| 12 | §2.5 | candidate set expanded from "top-300 death-associated DEG" | actually **top-50 degree-centrality ∩ DEG** | A3 | **FAIL — Tier 2** |
| 13 | §3.4 / Fig. S06 | calibration + decision-curve analysis performed (ref [18]) | **does not exist**; `02_scripts/06_prognosis.R:27` is a `# TODO: dca 图` stub; `S06_dca.png` is the discovery cohort, not external; ref [18] (Schuemie, p-value calibration) does not support DCA | A2, A3, A4 | **FAIL — Tier 1** |
| 14 | Abstract | hubs "localized to monocytes / antigen-presenting cells" | `07_axis_celltype.csv` ranks the **monocyte module last** (mean \|r\| 0.222); CD4/CD8 T lead (0.618 / 0.582) | A1 | **FAIL — Tier 1** |
| 15 | §3.1 network | "network + ML converged" on the six hubs | top nodes are **erythroid/heme**: GATA1 78.4, CGB 76.1, EPB49 72.5, ANK1, EIF2AK1; FIS1 rank 12; the five real hubs rank **595–1927 of 2000** | A1 | **FAIL — Tier 1** |
| 16 | Conclusion §6 | 30-gene signature AUC attributed to the hub genes | **HAVCR2 and FIS1 are not in the signature**; 7 L1 coefficients are 0 and 5 have sign opposite to the stated orientation (incl. CD14) | A2, A4 | **FAIL — Tier 1** |
| 17 | §2.10 | palindromic SNPs excluded | **two retained**, one affecting CD14's only nominally significant test | A2 | **FAIL — Tier 1** |
| 18 | README.md | 23/25; 3/5; CD74 "did not pass 15-test correction" | manuscript says **23/25** (README says 21/25); **3/5** (README says 4/5); CD74 statement now outdated | A4 | **FAIL — Tier 3** |
| 19 | Table 4 / §3.x | CD74 Egger SE 0.111 | **smaller than its own IVW SE (0.325) on the same 3 SNPs** — physically implausible, should be flagged not headline | A1 | **FAIL — Tier 2** |

Rows 1, 7, 8 were re-derived by the editor from source.

---

## 4. Graded consolidated issue list

### Tier 0 — conclusion-invalidating

**T0-1 · The entire MR causal-support layer is computed on the wrong reference distribution.**
All MR-Egger p-values use 2·(1−Φ(|β/SE|)) instead of t(n−2), despite `Q_df` = n−2 being recorded
in the same rows. Consequences: CD74 critical-care q 1.5×10⁻¹¹ → **~0.79**; CD74 susceptibility
0.0025 → **~0.90**; CD14 death 0.058 → **~0.73**; of 45 tests only **1** retains q<0.05 and it is a
sign-reversal estimator. **[editor-verified]** *(A3, corroborated A2)*
**Fix:** recompute all MR-Egger p-values with `2*pt(-abs(beta/se), df=n-2)` (R) or
`2*stats.t.sf(abs(t), df)` (Python); regenerate `10_mr_bh_family.csv`; rewrite every MR statement.
Because CD74 has 3 instruments (df=1), the Egger test is essentially uninformative regardless —
state that plainly rather than substituting another estimator's p-value.

**T0-2 · The headline MR signal is not supported by the declared primary estimator and points the
wrong way.** Under IVW — the estimator the paper nominates as primary — CD74 critical-care is not
significant (family q = 0.126; per-outcome q = 0.070). The one signal that did reach significance
has β = +0.798 (higher CD74 expression → *more* critical care), the **opposite** direction to the
expression model in which CD74 is *down* in the immunosuppressed endotype. *(A2, A4, corroborated A1)*
**Fix:** report the IVW result as the primary MR result; present Egger/weighted-median as sensitivity
analyses only; state explicitly that the significant sensitivity result is directionally
inconsistent with the transcriptome model and therefore does not support the causal claim.

**T0-3 · FIS1 is up-regulated in Mars1, not down.** logFC = +1.261, t = +17.16. The manuscript
asserts "all six hub genes down-regulated" in §2.8, §3.3 and S11; the pipeline's own positive-control
file lists only five down hubs. **[editor-verified]** *(A3)*
**Fix:** replace with "five of the six hub genes were down-regulated in Mars1
(CD14 −0.77, CD74 −0.76, FCGR3A −0.61, HLA-DQA1 −0.53, HAVCR2 −0.35); FIS1 was up-regulated
(logFC +1.26, t = +17.2) and is therefore reported as a co-expression marker rather than a member
of the down-regulated immunosuppression axis."

**T0-4 · The immune-function score does not distinguish Mars1 from Mars2.** P = 0.52
(−0.7917 vs −0.7520). The score separates the Mars1/Mars2 pair from Mars3 (P = 6.5×10⁻¹⁹) and
Mars4 (P = 6.4×10⁻⁴) — i.e. it is a two-cluster score, not a Mars1-specific one. Since Mars1 vs
Mars2 28-day mortality differs (34.1% vs 21.6%), the score does not track the outcome difference
that motivates the paper. **[editor-verified]** *(A1, A2)*
**Fix:** replace "the immune-function score was lowest in Mars1" with "the immune-function score
separated Mars1/Mars2 from Mars3/Mars4 (P<10⁻¹⁸ vs Mars3) but did not distinguish Mars1 from Mars2
(P=0.52); it therefore indexes a two-cluster immune gradient common to both low-score endotypes
rather than a Mars1-specific signature." Add the Mars1-vs-Mars2 test to the results table.

**T0-5 · The abstract reports the design selectively.** It claims a three-tier design but contains
no mention of MR, eQTL or GWAS, while the MR layer is null on the primary outcome for all five genes
(OR 0.92–1.12, P ≥ 0.24). The conclusion nonetheless asserts the genes "mark a therapeutically
addressable axis." *(A4)*
**Fix:** add to Abstract Methods "…and two-sample Mendelian randomisation (eQTLGen × UKB sepsis
GWAS) as causal support" and to Abstract Results "Mendelian randomisation did not support a causal
effect of any hub gene on the primary outcome (OR 0.92–1.12, P≥0.24)." Abstract is already 350
words including labels, so this must be a **swap**, not an addition — remove one lower-value Methods
clause to make room.

### Tier 1 — analyses to add

- **T1-1** Calibration and decision-curve analysis are claimed (manuscript:106, Fig S06, ref [18])
  but do not exist. Either implement them on the **external** cohort (report calibration slope,
  intercept, observed/expected ratio; DCA net benefit vs treat-none across thresholds 0–1) or
  delete the claim, the figure reference, and ref [18]. Note the existing DCA curve falls below the
  treat-none baseline across most thresholds — if that is the true result, report it. *(A2, A3, A4)*
- **T1-2** No MR diagnostic plots exist (scatter, forest, leave-one-out, funnel). STROBE-MR expects
  them. Generate all four per exposure–outcome pair. *(A4)*
- **T1-3** The co-expression network is an erythroid/heme module, not an immune module. Either
  re-derive it restricted to immune-relevant genes, or report honestly that degree centrality on
  whole blood recovers a heme module (consistent with Scicluna's own report of up-regulated heme
  biosynthesis in Mars1) and that the hubs came from the ML consensus, not the network. *(A1)*
- **T1-4** Reconcile the cell-type localisation with `07_axis_celltype.csv`, which ranks monocytes
  last. *(A1)*
- **T1-5** Fix the 30-gene signature: report which L1 coefficients are zero and which have reversed
  sign (incl. CD14), and stop attributing the signature's AUC to hub genes that are not in it. *(A2, A4)*
- **T1-6** Eliminate floating-point artifacts: recompute weighted-median p via `2*pnorm(-|z|)` on
  the log scale or via `pchisq(z², 1, lower.tail=FALSE)`; never store or report "p = 0" or
  "P < 1×10⁻³⁰⁰". *(A3)*
- **T1-7** Apply the stated palindromic-SNP exclusion policy consistently; report the sensitivity of
  CD14's result to it. *(A2)*
- **T1-8** Cite **ImmunoSep** (Giamarellos-Bourboulis et al., *JAMA* 2025, doi:10.1001/jama.2025.24175),
  which randomised IFN-γ in exactly this mHLA-DR-low population: SOFA benefit, **no mortality
  benefit**, more haemorrhage, and **53% of screened patients unclassifiable**. This materially
  changes the clinical-translation section — and its 53% unclassifiable rate actually *strengthens*
  the paper's endotyping argument, so it should be used, not avoided. *(A1)*

### Tier 2 — wording

- **T2-1** IFN-γ 5/5 → **4/5** (three places). All four reviewers caught this independently. *(A1–A4)*
- **T2-2** Recompute Table 2 under the stated |logFC|≥0.3 rule (IL-7 1.00→0.80; IFN-γ 0.71→0.57);
  the shortlist reorders. *(A1)*
- **T2-3** §2.5 candidate-set description: "top-300 death-associated DEG" → "top-50
  degree-centrality ∩ DEG". *(A3)*
- **T2-4** Flag that CD74's Egger SE (0.111) is smaller than its IVW SE (0.325) on the same 3 SNPs. *(A1)*
- **T2-5** "therapeutically addressable axis" must be withdrawn or hedged to expression-level
  addressability given the null MR on the primary outcome. *(A4)*
- **T2-6** README contradictions: 23/25 (written 21/25), 3/5 (written 4/5), CD74 correction status
  now outdated. *(A4)*

### Tier 3 — format / references

- **T3-1** 7 of 10 figures are never cited in text. Cite or remove. *(A4)*
- **T3-2** References 30 and 31 — which carry the two most important caveats — have unverified DOIs.
  Verify before submission. *(A4)*
- **T3-3** Abstract is 350 words including labels; check the target venue's cap. *(A4)*
- **T3-4** Complete the STROBE-MR and TRIPOD item-by-item gaps enumerated in A4 §Findings.

---

## 5. Consensus · complementarity · disagreement

**Consensus (all four, or three of four).** The MR layer does not support the causal claim (T0-1,
T0-2); the IFN-γ count is wrong (T2-1); the immune score does not separate Mars1 from Mars2 (T0-4);
calibration/DCA is claimed but absent (T1-1); the manuscript's data layer is largely *correct* —
see §7.

**Complementarity — findings only one reviewer could have produced.**
- A1 only: the network is a heme module; ImmunoSep supersedes the clinical ranking.
- A2 only: IVW nullity, palindromic-SNP retention, TRIPOD calibration gap.
- A3 only: the t-distribution defect, FIS1 direction, floating-point artifacts.
- A4 only: abstract omits MR, `# TODO` stub, 7 uncited figures, L1 coefficient signs.

**Disagreement and adjudication.**
- *Severity of the MR defect.* A3 graded the Egger distribution error Tier 0; A1 treated the same
  region as Tier 1 (flagging the SE anomaly without recomputing the distribution). **I adopt the
  stricter verdict (Tier 0).** A1's self-limited scope ("I flagged the SE, I did not recompute the
  p-values") is an honest reason for leniency about *its own* findings, but it cannot set the
  manuscript's fate when another reviewer demonstrates the numbers are wrong. **[editor-verified]**
- *Exact P for Mars1 vs Mars2.* A1 0.467, A2 0.47, editor 0.52 (tie-corrected normal approximation,
  n=132/176). All three agree on the substantive point (P ≫ 0.05). I adopt the conservative value
  **P = 0.52** and require the authors to publish one canonical test with the method named.
- *Calibration/DCA: "must add" vs "must retract".* A2 and A4 want the analysis added; A3 notes the
  existing artefact is the wrong cohort. **Ruling: must add, on the external cohort** — a prediction
  model paper without calibration is incomplete under TRIPOD — and if the honest result is net
  benefit below treat-none, report that rather than the figure currently shipped.
- *Article type.* A4 recommends path A (restructure, same article type) and explicitly rules out
  C (wording-only). I concur; see §8.

---

## 6. Priority must-fix list

**Must fix before this can be sent anywhere (all Tier 0):**

1. **T0-1** Recompute every MR-Egger p-value with t(n−2) and regenerate the BH family. 🚩 *This is a
   DESK-REJECT-level defect as it stands: the paper's most prominent causal claim is an artefact of
   the wrong reference distribution.*
2. **T0-2** Report IVW as primary; move Egger/weighted-median to sensitivity; state the directional
   inconsistency.
3. **T0-3** Correct FIS1's direction (up, not down) in §2.8, §3.3, S11.
4. **T0-4** Add the Mars1-vs-Mars2 test and reword the score claim.
5. **T0-5** Put the MR null into the abstract.

**Split — must add analysis vs must reword:**

| Must add analysis (cannot be fixed by rewording) | Must reword (numbers already correct) |
|---|---|
| T1-1 calibration + DCA on the external cohort | T2-1 IFN-γ 5/5 → 4/5 |
| T1-2 MR diagnostic plots (scatter/forest/LOO/funnel) | T2-3 §2.5 candidate-set description |
| T0-1 MR-Egger recomputation | T2-5 "therapeutically addressable axis" |
| T0-4 Mars1 vs Mars2 test | T2-6/README contradictions |
| T1-3 network re-derivation or honest reframing | T0-3 FIS1 direction (text only — data are right) |
| T1-6 floating-point p-value recomputation | T3-1–T3-4 format |
| T1-8 ImmunoSep citation | |

---

## 7. What stands up — do NOT change these

Carried forward from the reviewers' verification sections. Each was suspected of being wrong and
confirmed correct. **Protect these in the next revision.**

- The **23/25 / 22/25 / 21** triple count (directionally down / FDR-significant / both) — verified. *(A1, A4)*
- All **Table 1 effect sizes and P values** (HLA-DRB1 −0.89, CD14 −0.77, CD74 −0.76, FCGR3A −0.61,
  all P<1×10⁻⁸) — verified. *(A1, A3)*
- **MR point estimates** — all betas, ORs, CIs and I² in Tables 3–4 are correct as computed; only
  the *p-values* are wrong. *(A3)*
- The **45-test BH family structure** and its bookkeeping — verified. *(A2)*
- **27 instruments** accounting (CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8) and median F per gene
  (all > 30) — verified. *(A2, A4)*
- **External validation** AUC 0.638 / locked L1 0.585 and n = 106 / 52 — verified. *(A2, A4)*
- **Mars1 immune-score median −0.7917** and range — verified. *(A4)*
- **DEG counts, cell-type localisation values, L1000 numbers** — verified. *(A3)*
- The **glucocorticoid self-caveat** — appropriately stated, keep. *(A1)*
- The three figure callouts that do resolve — verified. *(A1)*

---

## 8. Recommended handling paths

**A) Restructure and resubmit as the same article type — RECOMMENDED.**
C) **Wording-only is NOT viable.** Three deliverables cannot be supplied by rewording: the MR
recomputation, calibration/DCA on the external cohort, and MR diagnostic plots. *(A4 concurs.)*
B) Downgrading the article type is unnecessary — the study design is sound; the execution defects
are fixable.

---

## 9. Process lessons

- **A green audit script is evidence about arithmetic, not about correctness.**
  `check_audit_assertions.py` passed 100% while the MR-Egger p-values used the wrong distribution,
  FIS1's direction was inverted in three places, and the Mars1/Mars2 comparison was never made. The
  script asserts only three things (max I², family size, provenance paths) — none of which touch
  the numbers the manuscript headlines. **New assertions needed:** (i) every Egger p must equal
  `2*pt(-|β/SE|, df=n−2)` to 1e-9; (ii) no p-value column may contain exactly 0.0 or any value
  below 1e-300; (iii) Egger SE must not be less than IVW SE on the same instruments; (iv) the
  direction sign of every hub gene in the text must match `S01_mars1_deg.csv`; (v) every
  between-group claim in the text must have a corresponding test row in a results CSV.
- **A previous round added caveats without retracting headlines.** The MR caveats from earlier
  rounds (sample overlap, small instrument counts) were added to Methods and Limitations while the
  headline claim in Results and the abstract was left standing. A fresh panel caught this instantly.
  **Rule: when a caveat is added, check whether the headline itself was retracted or merely
  qualified elsewhere.**
- **Floating-point underflow silently became a claim.** "p = 0" and "P < 1×10⁻³⁰⁰" entered the
  manuscript as if they were findings. Any p-value at the representation limit must be recomputed
  on the log scale, never reported literally.
- **Cross-reviewer convergence is the quality signal.** Four independent hits on the IFN-γ count and
  three on the MR/CD74 defect indicate real defects; single-reviewer findings deserve independent
  confirmation before they drive a rewrite.

---

## 10. A direct note to the author

The claim that fails is the **causal layer**: the CD74 MR signal you have been treating as your
strongest genetic support does not survive, and it fails in a way that is not your fault — it is a
reference-distribution error buried in the MR routine, invisible in every diagnostic you had, and
it passed a green audit script. Once corrected with t(n−2), CD74's critical-care result is p ≈ 0.088
with three instruments, and the honest statement is that MR does not support causality for any hub
gene on the primary outcome.

But you buried the finding that is genuinely yours, and it is a better one. Your data show that
**whole-blood degree centrality does not recover an immune module at all** — it recovers an
erythroid/heme module (GATA1, CGB, EPB49, ANK1), with your five real hubs ranked 595–1927 of 2000;
that **the immune score separates Mars1/Mars2 from Mars3/Mars4 but not Mars1 from Mars2**; and that
**ImmunoSep could not classify 53% of screened patients** into the very endotype framework this
field relies on. Those three facts, taken together, are a coherent and publishable argument that
endotype-driven hub discovery in whole blood is structurally limited — a methodological finding
with real consequences, not a negative result to apologise for.

Swapping them converts the paper from a fragile causal signal into a stable structural finding:
**lead with what the network and the score can and cannot recover, and report the MR layer as the
null it is.** That reframing is why path A is viable and path C is not.
