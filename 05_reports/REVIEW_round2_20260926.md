# Independent Expert Review — Round 2 (consolidated editor report)

**Manuscript:** *Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning* — v1.1.0
**Date:** 2026-09-26
**Editor:** WorkBuddy (consolidation only; the five expert reports are independent files in `05_reports/review_r2/`)
**Prior round:** Round 1 (`05_reports/REVIEW_round1_20260926.md`) produced Tier 0/1/2/3 = 3/10/15/8; those fixes were applied in v1.1.0. This round re-examines v1.1.0 **fresh** — experts were forbidden from reading Round-1 files.

---

## 1. Independence statement

Five independent reviewers (A1 clinical/immunology, A2 statistics+MR causal, A3 number-provenance audit, A4 journal-editor+reporting, A5 LINCS/drug-repurposing) each received a self-contained brief forbidding all prior review artefacts (`REVIEW_*.md`, the whole `05_reports/review/` dir, `RESPONSE_*.md`, `SUBMISSION_MANIFEST.md`, etc.) and were required to verify numbers against raw `03_results/*.csv` themselves.

**Evidence independence worked:** the single most-convergent finding (ITGAM FDR label) was hit independently by A1, A3 and A4 from three different angles (biology, provenance, venue). The LINCS dual-direction flaw (A5) and FIS1 incoherence (A1) were unique catches, confirming the panel is not over-diffuse. No reviewer read another's output.

**Editor verification (own script, raw sources only):** I independently re-extracted every disputed number — see §3. All four P0/P1 numeric claims below were reproduced by the editor, not forwarded from a reviewer.

---

## 2. Verdict table

| Expert | Layer | Headline verdict | Anchoring findings |
|---|---|---|---|
| A1 | Clinical / immunology | Major revision | ITGAM FDR error; FIS1 incoherence; "therapeutically targetable" overstatement |
| A2 | Statistics + MR causal | Moderate revision | CD14 BH-FDR denominator mismatch; immuno-score tautology; calibration not reported numerically |
| A3 | Number provenance | Major revision (integrity) | 2×P0 (ITGAM, §3.5 "exceeded") + 2×P1 (CD14 FDR, STROBE tally) |
| A4 | Journal editor + reporting | Major revision / **desk-reject risk if uncorrected** | 24/31 refs uncited; STROBE 9b false location; §3.5 "exceeded" |
| A5 | LINCS / drug repurposing | Moderate–Major | rescue metric cannot enforce dual-direction (HIGH); redundant scores; no null baseline |

**Distribution:** 0 outright rejects; all five say "revise" — the manuscript is salvageable at the same article type after fixes. The desk-reject risk is *conditional* on leaving the integrity items (§3) unaddressed.

---

## 3. Cross-verification table (manuscript claim vs independently recomputed)

| # | Manuscript location | Manuscript claims | Independently recomputed value | Checked by | Verdict |
|---|---|---|---|---|---|
| CV-1 | §3.1 / Table 1 (ITGAM) | "not significant at FDR<0.05" | `S01_immunoparalysis_direction.csv`: ITGAM adj.P.Val = **0.0016773 (<0.05) → FDR-significant**; only `DEG_0.3=False` (|logFC|=0.21<0.30) | Editor (script) + A1+A3+A4 | **WRONG** — factual error |
| CV-2 | §3.1 counts | 23 down / 22 sig / 21 down&sig | Source: down=23, up=2, sig=22, down&sig=21 | Editor (script) + A3 | Correct |
| CV-3 | §3.5 line 109 | "again **exceeded** the IRG benchmark (0.604)" | §3.4 (l.106) "comparable rather than superior"; Discussion (l.179) "comparable to, not better than" | Editor (grep) + A3 | **Self-contradiction (P0)** |
| CV-4 | §3.10 line 146 / §5 line 190 | "BH-FDR 0.026 across all 15 gene × outcome Egger tests" | `10_genetics_mr_outcome5086_28ddeath.csv` CD14 Egger `p_fdr_bh` = **0.0766** across 15 tests; 0.026 = within-5-test BH only | Editor (script) + A2+A3+A4 | **Mismatch** — value≠denominator |
| CV-5 | §2.10 line 72 | harmonisation exclusion tallies "itemised in `*_harmonised.csv`" | harmonised CSVs contain **only retained-SNP columns** (rsid…F); no palindrome/strand/allele-incompat tally; absent from `s10_run_log*.txt` too | Editor (grep/script) + A2+A3+A4 | **False claim** |
| CV-6 | §3.9 L1000 wtcs | azithromycin 0.0626; lenalidomide 0.2058 | `S08_l1000_candidate_scores.csv`: azith wtcs 0.0626, lena wtcs 0.2058 | A3+A5 | Correct (1.17 trap avoided) |
| CV-7 | §3.7 / Table 2 concordance | IL-7 5/5, GM-CSF 5/6, IFN-γ 5/7, azi 2/3, lena 2/5, thym 2/5, BCG 1/5 | `08_candidates_drugs.csv` matches exactly; IFN-γ 5/5 AP genes resolve to its rescue_genes | A3+A5 | Correct |
| CV-8 | §3.4 / §3.5 AUC | CV 0.659, train 0.750, external 0.638 (L1 0.585), IRG 0.619/0.648/0.604 | `S06_auc_compare.csv` + `09_external_validation.csv` match; L1 0.585 already disclosed in §3.5 | Editor + A2 | Correct |
| CV-9 | §3.10 CD14 Egger | OR 0.906, P=5.1e-3, null intercept | `10_genetics_mr_outcome5086_harmonised.csv` reproduces; correctly flagged suggestive-only | A2+A3 | Correct |
| CV-10 | References | 31 entries | Body cites only **[4][11][12][13][16][30][31]** = 7 unique → **24 uncited** | Editor (grep) + A4 | **Gap (real)** |
| CV-11 | §3.9 rescue formula | dual-direction (PDCD1/LAG3 required down) enforced | `rescue = mean(rank-percentile of 22) − 0.5` is unsigned; proved `wtcs = rescue×√22` → **no sign term, up-markers not enforced** | A5 (editor concurs) | **Method not implemented as stated** |

---

## 4. Graded consolidated issue list

### Tier 0 — conclusion-invalidating / integrity / self-contradiction
- **T0-1 (ITGAM, Table 1 l.92).** "integrin αM (not significant at FDR<0.05)" is factually false: source adj.P = 0.0016773 < 0.05, so ITGAM *is* FDR-significant. The `DEG_0.3=False` flag only means |logFC|=0.21 < 0.30 fold-change cutoff. **Fix:** change to "significant at FDR<0.05 (adj.P = 1.7×10⁻³) but below the |logFC|≥0.3 DEG fold-change threshold (DEG_0.3 = False)". The aggregate "21 down&significant" count is unaffected (ITGAM remains in it).
- **T0-2 (§3.5 l.109 "exceeded").** The sentence "a significant separation that again **exceeded** the IRG benchmark recomputed on the same cohort (0.604)" contradicts the manuscript's own invariant framing — §3.4 "comparable rather than superior", §5/Discussion "comparable to, not better than". 0.638 vs 0.604–0.619 are numerically close with overlapping CIs; the honest word is *comparable*. **Fix:** "a significant separation that was **comparable to** the IRG benchmark recomputed on the same cohort (0.604; Peng et al. [16] reported 0.619)".
- **T0-3 (§3.9 L1000 dual-direction not enforced, A5 HIGH).** The query text claims 22 genes "comprising 20 Mars1-down … and 2 Mars1-up exhaustion markers (PDCD1, LAG3; required to be down-regulated)". But `rescue_score = mean(rank-percentile of 22 genes) − 0.5` is an *unsigned* mean; `wtcs = rescue_score × √22`, so there is no sign term and the up-marker requirement is never implemented. The connectivity scores therefore do not actually test exhaustion-marker down-regulation. **Fix (pick one):** (a) honestly restate that the connectivity score captures Mars1-*down* rescue only and the up-marker requirement is a *design intention not enforced in the metric*; or (b) correct the formula to subtract the up-marker percentile contributions so dual-direction is real. Option (a) is lower-risk given only modest small-molecule scores are reported; either way the current text overstates what the metric does.

### Tier 1 — must fix (reword-with-numbers or add analysis)
- **T1-1 (CD14 BH-FDR l.146/190).** "BH-FDR 0.026 across all 15 gene × outcome Egger tests" is internally inconsistent: the 15-test BH for CD14 is **0.0766** (source `p_fdr_bh`); 0.026 is the *within-5-test* BH inside the 28-day-death outcome. **Fix:** "BH-FDR 0.026 within the five hub-gene Egger tests of the 28-day-death outcome (0.077 across all 15 gene×outcome Egger tests)" — or report 0.0766 consistently with "across 15". State one canonical number.
- **T1-2 (STROBE-MR 9b l.72).** The claim that exclusion tallies are "itemised in `*_harmonised.csv`" is false (those files hold only retained, allele-aligned SNPs + F). The run logs also lack the tally. **Fix:** either (a) re-extract the harmonisation drop counts from TwoSampleMR and write `10_genetics_mr_harmonisation_exclusions.csv`, then cite it; or (b) correct the sentence to state the harmonised tables provide retained instruments per gene (with F) and that palindromic/strand-ambiguous/non-biallelic SNPs were dropped per TwoSampleMR defaults, with per-gene retained counts shown — and remove the false "itemised in" pointer.
- **T1-3 (References 24/31 uncited, A4).** Only 7 of 31 references are cited in the body ([4][11][12][13][16][30][31]). Methods are never cited where used: WGCNA [27] (§2.4), limma [6] (§2.2), L1000/iLINCS [7] (§2.9), CIBERSORT(x) [8][9] (§2.7), MR-Base [10] (§2.10), GEO [26]/ArrayExpress [5][15] (§2.1/§2.9), Bowden MR-Egger [21][28] & Verbanck [24] (§2.10/§3.10), drug RCTs [23][25] (§3.7/§3.8). **Fix:** add in-text citations at each method/claim. Mechanical but mandatory for any journal.
- **T1-4 (External AUC model consistency, A2).** §3.4 compares the optimistic *L1* CV (0.659) against the honest *equal-weight* external (0.638); §3.5 already discloses L1 external = 0.585. The optimism gap is correctly scoped, but ensure §3.4 does not imply 0.659 and 0.638 come from the same model. Minor tightening: "the within-cohort CV AUC 0.659 (L1 model) is optimistic; the honest generalization is the external equal-weight AUC 0.638".
- **T1-5 (L1000 25→22 map, A5).** 25 consensus − 2 named L1000-absent hubs (HAVCR2, FCGR3A) = 23, yet the query is 22. The **third** excluded gene is unnamed. **Fix:** state all three L1000-absent genes explicitly.
- **T1-6 (response_gene_concordance null baseline, A5).** No shuffle/null distribution; tiny curated sets (n=3–7) cannot distinguish true rescue from chance overlap with the large Mars1-down set. **Fix:** add a permutation null or explicitly caveat that the metric is a curation-consistency check, not a statistical significance.

### Tier 2 — wording
- **T2-1 (FIS1 incoherence, A1).** FIS1 is a mitochondrial-fission protein and is *absent* from the consensus immune gene set (`S04 in_immune_set=False`), yet §3.1/§3.4 call all six hubs "antigen-presentation / monocytic / exhaustion-axis genes". **Fix:** acknowledge FIS1 as the one non-immune hub member, or reframe the "parsimoniously recapitulates the Mars1 program" claim to "five immune hubs + one mitochondrial-fission gene".
- **T2-2 ("therapeutically targetable", A1).** Abstract/Conclusion use "therapeutically targetable set" while only modest L1000 rescue exists. Borderline; acceptable if paired with the existing "hypothesis-generating" hedges — keep but do not strengthen.
- **T2-3 ("best published", l.109/179).** Residual over-claim vs the established "comparable" framing. **Fix:** "comparable to published sepsis mortality signatures" (drop "best").
- **T2-4 (Abstract optimism qualifier, A4).** EN/ZH abstract says 0.659 "comparable to the published benchmark" but omits the "optimistic" caveat present in §3.4/§5. Low severity (abstract is already restrained); optionally add "optimistic within-cohort" qualifier.
- **T2-5 (Immuno-function score tautology, A2).** The score is built from the same gene set that defines Mars1, so "lowest in Mars1" is partly definitional. **Fix:** acknowledge this and note the score is still used prognostically across the whole cohort, not only within Mars1.

### Tier 3 — format
- **T3-1 (wtcs vs rescue_score redundant, A5).** Mathematically identical (linear); presenting both implies two independent scores. **Fix:** keep one primary (recommend `wtcs`) and drop or footnote the other.
- **T3-2 (HAVCR2/TIM-3 direction vs exhaustion, A1).** §3.4 says "antigen-presentation and monocytic genes down, TIM-3 up" — fine, but the hub contains HAVCR2 (TIM-3, down-regulated) while the exhaustion narrative cites PDCD1/LAG3 (up). Clarify this is the Mars1 *program* carrying both a down AP axis and an up exhaustion axis.

---

## 5. Consensus / complementarity / disagreement

**Consensus (≥2 independent experts):**
- ITGAM FDR label is wrong (A1, A3, A4).
- CD14 BH-FDR value/denominator mismatch (A2, A3, A4).
- STROBE-MR 9b tally falsely located (A2, A3, A4).
- "exceeded" self-contradiction in §3.5 (A3; editor confirms).
- References overwhelmingly uncited (A4, editor confirms).

**Complementarity (unique catches):**
- A5 alone: L1000 rescue metric cannot enforce dual-direction (HIGH); redundant wtcs/rescue; no null baseline; 25→22 unmapped third gene.
- A1 alone: FIS1 biological incoherence; "therapeutically targetable" overstatement.
- A2 alone: immuno-function score tautology; calibration not reported numerically (TRIPOD).

**Disagreement & adjudication:**
- A4's "Issue 2" implies the *abstract* over-claims 0.659 vs benchmark. **Adjudication:** the abstract actually says "comparable to the published benchmark (0.619–0.648)" — it is restrained. The real "exceeded" is in §3.5 body (T0-2), not the abstract. Adopt the stricter reading for §3.5; the abstract needs only the optional T2-4 tweak. No contradiction between experts once the locus is corrected.
- Severity on the LINCS sign flaw: A5 rates HIGH (method not implemented as stated); A3 did not flag it (scope-limited to numbers). **Adopt A5's stricter verdict** (T0-3) because it is a stated-method-not-implemented integrity issue, not merely wording.

---

## 6. Priority must-fix list (before any submission)

`DESK-REJECT` flags mark items that, if left unaddressed, would justify a desk reject at a methods-honest journal.

| # | Item | Type | DESK-REJECT risk |
|---|---|---|---|
| 1 | T0-1 ITGAM FDR label | reword (number) | **YES** (Table-1 factual error) |
| 2 | T0-2 §3.5 "exceeded" | reword | **YES** (self-contradiction) |
| 3 | T0-3 L1000 dual-direction not enforced | reword-or-fix-metric | **YES** (method misstated) |
| 4 | T1-2 STROBE 9b false location | reword-or-add-CSV | **YES** (false reporting claim) |
| 5 | T1-3 24/31 refs uncited | add citations | **YES** (near-certain major-revision/desk query) |
| 6 | T1-1 CD14 BH-FDR denominator | reword (number) | No (minor but must fix) |
| 7 | T1-4/5/6 L1000/MR clarity + null baseline | reword/add | No |

**must-add-analysis vs must-reword split:**
- *Must reword (numbers):* T0-1, T0-2, T1-1.
- *Must reword (honesty):* T0-3, T1-2, T1-3, T1-5, T1-6, T2-1…T2-5, T3-1/2.
- *Must add:* T1-3 (citations), T1-2 (exclusion CSV or corrected text), T1-6 (null baseline — optional but recommended).

---

## 7. What stands up (do NOT change)

Carried from the experts — these were suspected but verified correct:
- §3.1 directionality counts (23/2, 22 sig, 21 down&sig) and the 8 named-gene logFC/adj.P (except ITGAM's significance label).
- All 7 drug `response_gene_concordance` fractions and Table 2; IFN-γ 5/5 AP-gene resolution.
- LINCS wtcs azithromycin 0.0626 / lenalidomide 0.2058 (the 1.17 trap is correctly avoided).
- External AUC 0.638 (95% CI 0.532–0.748) and L1 0.585, both honestly disclosed in §3.5.
- IRG benchmark 0.619 / 0.648 / 0.604 (dual-value口径 correctly distinguished).
- MR CD14 Egger OR 0.906 / P=5.1e-3 reproduced and correctly flagged suggestive-only; IV counts & median F match source.
- Sample-overlap limitation (eQTLGen×UKB) disclosed in §2.10/§5.
- Virtual-knockdown correctly downgraded to a directionality consistency check (§3.3).
- Cover letter is conservative and consistent with the tiered-evidence framing (does not over-state; cites honest 0.638, not 0.659).
- Forbidden strings removed: `rescue_fraction`, `druggable`, `Virtual knockdown`, `progressively ordered`, `4/5`. References 1–31 sequential, no gaps.

---

## 8. Recommended handling path

**Path A — restructure-and-resubmit at the same article type (RECOMMENDED).** Every Tier 0/1 item is fixable by rewording + 2 number corrections (ITGAM, CD14 BH-FDR) + adding ~24 citations + correcting the L1000 dual-direction statement. No new experiment or large analysis is required. After fixes the manuscript is suitable for a methods-honest translational/computational-biology journal (e.g. *Journal of Translational Medicine*, *Scientific Reports*, *Frontiers in Immunology* — verify SCIE status and JIF at submission time per the user's verification discipline).

Path B (downgrade article type) is **not** warranted — the core finding (endotype-anchored, externally validated, modest but real immunosuppressed signature) is intact.

Path C (wording-only) is **not viable** — T0-1/T0-2/T0-3/T1-2 are factual/honesty fixes, not cosmetics.

---

## 9. Process lessons (for the CI gate)

- **A green consistency gate did not catch a per-gene significance error.** The v1.1.0 gate checked aggregate counts (21/22/23) but not the *per-gene significance label* vs the `DEG_0.3` fold-change flag. Add an audit that, for every gene named in Table 1, asserts `significance_label ⇔ (adj.P.Val < 0.05)` and separately reports `DEG_0.3`.
- **Cross-section contradiction gate.** Add a grep-gate: if the body uses "exceeded/superior/better than" for the AUC anywhere, it must co-occur with the "comparable rather than superior" framing — flag any lone "exceeded".
- **Method-claim ↔ metric gate.** For every metric named in §2/§3, assert the formula in the text mathematically implements what the query text claims (the L1000 dual-direction gap would have been caught).
- **Reference-citation gate.** Assert every reference in the list is cited at least once in the body; fail the build on any uncited entry (would have caught the 24/31 gap).
- **STROBE/TRIPOD pointer gate.** Any claim of the form "itemised in <file>" must be verified by grepping <file> for the claimed columns; the false harmonised-CSV pointer would have been caught.

---

*Expert files: `05_reports/review_r2/A1_clinical_domain.md`, `A2_stats_mr_design.md`, `A3_provenance_audit.md`, `A4_venue_reporting.md`, `A5_drug_repurposing.md`. Editor verification scripts read only `03_results/*.csv` and `manuscript.md`; no prior-review file was opened.*
