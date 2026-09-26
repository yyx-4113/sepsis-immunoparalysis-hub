# Round 4 — Independent Expert Panel Review (consolidated)

**Manuscript:** `05_reports/manuscript.md` **v1.3.0** (commit `fd1ce44`, tag `v1.3.0`)
**Review date:** 2026-09-26
**Panel:** 5 blind lenses (A1 Domain/Clinical, A2 Design/Statistics, A3 Implementation/Provenance, A4 Venue/Reporting, A5 Drug-repurposing)
**Mechanism of independence:** Each lens read only `manuscript.md` + raw `03_results/*.csv`; none read `REVIEW_round*.md`, `RESPONSE*.md`, prior `review_r*/`, or status files. Treated as a first submission.

---

## 1. Independence statement
The panel operated without knowledge of Rounds 1–3. The diagnostic signature of working independence appeared: **three independent lenses (A2, A3, A4) converged on the same arithmetic defect from three angles** (statistics recomputation, provenance contradiction, internal-section incoherence) — exactly the clustering-on-a-real-defect pattern the method is designed to surface. No finding was unique to a single reviewer in a way that suggested panel diffusion; the cluster validates the defect's reality.

---

## 2. Verdict table

| Lens | Verdict on current state | Headline concern |
|------|--------------------------|------------------|
| A1 Domain/Clinical | Major revision | CD74 direction-reversal (strongest MR signal) is buried under a false "fails correction" claim |
| A2 Design/Statistics | **Major / DESK-REJECT risk** | 45-test BH claim "no estimate q<0.05 (min q=0.058)" is false; min q=0.0000, 3 tests q<0.05 |
| A3 Implementation/Provenance | **Major / DESK-REJECT risk** | Manuscript text contradicts its own CSV `p_fdr_bh` (4.97e-12, 0.0) |
| A4 Venue/Reporting | Minor-to-Major | §3.10 internally incoherent on CD74 significance; STROBE-MR tally qualitative |
| A5 Drug-repurposing | Minor | Dual-direction L1000 gap admitted but verb still overstates "rescue" |

**Distribution:** 2 × DESK-REJECT-risk (A2, A3), 1 × Major (A1), 1 × Minor-Major (A4), 1 × Minor (A5).

---

## 3. Cross-verification table (numbers recomputed by the editor from raw sources)

| # | Manuscript location | Manuscript claims | Independently recomputed | Who checked | Verdict |
|---|----------------------|-------------------|--------------------------|-------------|---------|
| 1 | §2.10 / §3.10 / §5 / Disc | "45-test family: no estimate reached q<0.05 (smallest q=0.058, CD14 Egger)" | **min q = 0.0000**; 3 tests q<0.05: CD74 WM crit-care q=0, CD74 Egger crit-care q≈5e-12, CD74 Egger suscept q=0.0025 | A2 + Editor | **FALSE** |
| 2 | §3.10 l.171 | "CD74 crit-care fails correction across all 15 tests (FDR≈0.21)" | CSV `p_fdr_bh` = 0.070 (IVW), **4.97e-12 (Egger), 0.0 (WM)** | A2/A3 | **FALSE** |
| 3 | §3.10 l.146 / Disc l.181 | "four of five hubs concordant protective across all three methods" | HAVCR2 MR-Egger = 1.010 (not protective) → only 3 hubs fully concordant | A2 | **FALSE** |
| 4 | §3.5 l.109 | "95% CI only marginally excludes 0.5" | CI 0.532–0.748; lower 0.532 > 0.5 by 0.032 → CI firmly excludes 0.5 | A3 | Misleading |
| 5 | §3.10 (CD14) / §5 | CD14 28d Egger q=0.058 (45-test) | recompute q=0.0575 ≈ 0.058 — **value correct**, only its "minimum" status wrong | A2/A3 | Value OK |
| 6 | §3.5 / §7 | External AUC 0.638 (95% CI 0.532–0.748) | CSV orientedSum 0.6382, CI 0.5317–0.7475 | A1/A3 | ✅ |
| 7 | §3.9 | lenalidomide wtcs 0.21 / rescue 0.044; azith wtcs 0.06 / rescue 0.013 | 0.044×√22=0.206≈0.21; 0.013×√22=0.061≈0.06; self-consistent | A3/A5 | ✅ |
| 8 | References | 31 refs, all cited | grep audit: 31 defined, 31 cited, 0 orphans | A3/A4 | ✅ |
| 9 | §2.10 (overlap) | eQTLGen shares UKB participants → overlap | consistent with cited Burgess/Davies/Thompson 2016; inflates significance | A2 | ✅ (but under-discussed) |

---

## 4. Graded consolidated issue list

### Tier 0 — conclusion-invalidating (must fix before any submission)
**T0-1 (A2-T0-1 / A3-T0-1).** The manuscript's central MR verdict — "under the full 45-test family no estimate reached q<0.05 (smallest q=0.058)" — is arithmetically false. Independent recomputation over all 45 gene×estimator tests gives **minimum q = 0.0000** with three tests below 0.05 (all CD74: critical-care MR-Egger q≈5×10⁻¹² and weighted median q=0; susceptibility MR-Egger q=0.0025). The manuscript's own result CSV already carries `p_fdr_bh` = 4.97e-12 and 0.0, so the prose and data directly contradict. This is visible to any reviewer who opens the CSV, and it inverts the paper's entire "MR is null / hypothesis-generating only" narrative. **Appears in 4 locations: §2.10 l.72, §3.10 l.146 & l.173, §5 lim-2 l.190, Discussion l.181.** Fix: replace with the correct statement (see A2-T0-1 Specific fix); the honest framing is that CD74 critical-care is *highly* significant under BH but direction-reversed and 3-instrument-limited, hence not a causal-target claim.

**T0-2 (A3-T0-1).** Provenance break: the artefact contradicts itself (text vs its own `p_fdr_bh` column). Resolved by the same fix as T0-1.

### Tier 1 — analyses to reword / reconcile
**T1-1 (A2-T1-1).** "Four of five hubs concordant protective across all three methods" is false — HAVCR2 MR-Egger = 1.010 (null, not protective). Correct to "three of five (HLA-DQA1, CD14, FIS1); HAVCR2 two-protective/one-null; CD74 discordant." (§3.10 l.146, Discussion l.181)

**T1-2 (A2-T1-2).** "CD74 crit-care fails correction (FDR≈0.21)" false — file shows 4.97e-12 (Egger), 0.0 (WM). Replace with correct q + biological-caution rationale. (§3.10 l.171)

**T1-3 (A2-T1-3).** Sample overlap (eQTLGen ⊋ UKB) *inflates* the CD74 significance; manuscript acknowledges overlap but not its inflation direction. Add one sentence. (§2.10 / §5)

### Tier 2 — wording
**T2-1 (A3-T2-1).** §3.5 "95% CI only marginally excludes 0.5" understates — CI 0.532–0.748 firmly excludes 0.5. Reword to "excludes 0.5, though point estimate is only 0.138 above chance."
**T2-2 (A4-T2-1).** §3.10 internally incoherent (reports CD74 crit-care OR 2.222/P=0.014 yet claims it "fails correction / nothing survives"). Reconcile once via T0-1 fix.
**T2-3 (A4-T2-2).** STROBE-MR item 9.1.2 per-SNP exclusion tally only qualitative. Add a supplementary table or point to the column in `*_harmonised.csv`.
**T2-4 (A1-T3).** Discussion l.181 "rescue-able hub" → "therapeutically addressable axis" (hubs are markers, not individually rescuable).
**T2-5 (A5-T2-1).** L1000 score verb: consistently call it a "single-direction Mars1-down reversal proxy" given the unimplemented dual-direction requirement.

### Tier 3 — format / hygiene
**T3-1 (A4-T3).** Data-availability, references (31/31), ethics/COI statements, wtcs redundancy disclosure — all clean; no action.
**T3-2 (A5-T3).** Clinical-translation hierarchy matches concordance ranking; opposing GM-CSF meta-analysis correctly noted — no action.

---

## 5. Consensus / complementarity / disagreement

**Consensus.** All five lenses agree the MR multiple-testing narrative (T0-1) is wrong and must be corrected; A2/A3/A4 reached it independently. All agree the CD74 critical-care signal is the study's strongest MR result and is currently mis-handled.

**Complementarity.** A1 supplied the biological reading (direction reversal = coherent severity signal, not noise); A2 supplied the arithmetic; A3 supplied the provenance contradiction; A4 supplied the intra-section incoherence; A5 confirmed the repositioning section is otherwise sound and that the L1000 dual-direction gap should modestly soften the "rescue" verb.

**Disagreement.** A5 graded the repositioning section "Minor" while A1 graded the CD74-MR handling "Major." This is a *scope*, not a *substance* disagreement: A5's lens is the drug-repositioning section (which is fine); A1's lens is the MR interpretation (which is broken). Adopt the stricter verdict for the MR layer (Major) and the lenient one for the repositioning section (Minor). No contradiction in recommendations.

---

## 6. Priority must-fix list (with DESK-REJECT flags)

| # | Fix | DESK-REJECT? | Type |
|---|-----|--------------|------|
| 1 | Correct the 45-test BH claim in all 4 locations (§2.10, §3.10×2, §5, Discussion); state min q=0.0000, 3 CD74 tests q<0.05, direction-reversal rationale | **YES** | reword + reframe |
| 2 | Fix "CD74 crit-care fails correction FDR≈0.21" → correct q values + biological caution | **YES** | reword |
| 3 | Fix "four of five hubs concordant protective" → three (HAVCR2 Egger=1.010 not protective) | No | reword |
| 4 | Add sample-overlap inflation sentence | No | add analysis note |
| 5 | §3.5 CI-exclusion reword | No | wording |
| 6 | §3.10 internal coherence pass | No | wording |
| 7 | STROBE-MR per-SNP tally (supp table or pointer) | No | add artefact |
| 8 | "rescue-able hub" → "therapeutically addressable axis"; L1000 "rescue" → "single-direction reversal proxy" | No | wording |

Items 1–2 are DESK-REJECT-risk because a reviewer recomputing from the supplied CSV will find the paper asserting the opposite of its own data — a credibility failure that can override otherwise-acceptable science.

---

## 7. What stands up (do NOT change)
- External validation AUC 0.638 (95% CI 0.532–0.748) — real, modest, comparable to benchmark. ✅
- Tier-1 biology-inevitable immunoparalysis signal (endotype-driven 3,597 DEGs, coherent down-regulation). ✅
- IFN-γ method-positive gate (5/5 antigen-presentation rescue). ✅
- L1000 score self-consistency + glucocorticoid caveat + dual-direction non-implementation disclosure. ✅
- Reference integrity (31/31, 0 orphans). ✅
- §7 number-provenance table (makes every number auditable — the reason T0-1 is catchable). ✅
- CD14 28-day-death MR-Egger q=0.058 is correctly computed (only its "minimum" status is wrong). ✅
- Data-availability names the real repo; ethics/COI statements complete. ✅

---

## 8. Recommended handling path
**B) Downgrade-the-claim, not the article type.** The science is sound; the defect is a false "null MR" narrative that the data refute. Recommended path:
- Keep the article type (computational multi-omics + repositioning).
- **Reframe the MR layer from "nothing survives correction" to "CD74 critical-care is a robust, direction-surprising association (q≈5×10⁻¹², null Egger intercept) that we interpret as genotype–severity rather than a causal repositioning target, because it reverses the Mars1 down-regulated-CD74 direction and rests on 3 instruments + exposure–outcome overlap."**
- This *strengthens* the paper: it converts a fabricated "all-null" into a genuine, honestly-bounded finding, and it directly motivates the S11 functional-validation wave (test whether raising CD74/CD14 restores antigen presentation).
Do **not** take path A (restructure) — no structural change needed. Do not take path C (wording-only) for items 1–2 — those require the numerical reframe, not cosmetic edits.

---

## 9. Process lessons
- **"Disclosure ≠ resolution" trap fired again.** Round 3 "fixed" the MR by recomputing the 45-test BH, but the recomputation (or the narrative built on it) was wrong — it reported 0.058 as the family minimum and pasted "nothing survives" into four places. The subsequent round's fresh panel caught it instantly because it read the data, not the author's memory. **Rule reinforced:** any multiple-testing claim must be re-derived from the raw p-values in the current CSVs every round, never carried forward from a prior round's prose.
- **Gates cannot catch cross-file semantic contradiction.** The arithmetic gate checks string matching; it did not notice the manuscript says "no q<0.05" while its own `p_fdr_bh` column says 4.97e-12. A new gate artefact is warranted: a script that reads every `*_harmonised.csv` / MR CSV `p_fdr_bh` and asserts the manuscript's stated minimum/maximum q is consistent with the file. This extends gate coverage to the design layer.
- **A single authoritative BH table (all 45 tests, per-outcome + family q) as a supplementary CSV would pre-empt reviewer recomputation** and remove the temptation to assert q-values in prose.

---

*Panel files: `review_r4/_PANEL_BRIEF.md`, `A1_domain_clinical.md`, `A2_design_stats.md`, `A3_implementation.md`, `A4_venue_reporting.md`, `A5_drug_repurposing.md`. Editor verification of T0-1 performed directly from `03_results/10_genetics_mr_*.csv`.*
