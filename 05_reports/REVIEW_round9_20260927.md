# Round-9 Independent Review — Consolidated Editor Report

**Manuscript:** `05_reports/manuscript.md` (v1.8.0, commit `180ecb1`)
**Title (working):** "Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning"
**Review date:** 2026-09-27
**Panel:** 4 blind reviewers (A1 domain / A2 design-stats-MR / A3 implementation-provenance / A4 venue-reporting), each forbidden from any prior round (`REVIEW_round*`, `review_r*`, `RESPONSE*`, and each other's outputs).
**Deliverables:** `05_reports/review_r9/A1_domain.md`, `A2_design_stats.md`, `A3_implementation.md`, `A4_venue_reporting.md`, `_PANEL_BRIEF.md`, this report.

---

## 1. Independence statement

The firewall was enforced per `_PANEL_BRIEF.md`: every reviewer was told it was a first submission and was given an explicit forbidden-file list. No reviewer was permitted to read `REVIEW_round1–8.*`, `review/`, `review_r2–r8/`, `RESPONSE*`, or sibling `A*_*.md` files.

**Evidence the firewall worked:** Round-8 (and 6/7) reviewers had verified the MR-Egger *CSV* values and the 17-assertion audit, and concluded the Egger layer was fixed. Round-9's **A3 independently re-derived the Egger p-values from the CSVs and then audited the manuscript *table prose*** — finding that Table 3 still prints the *normal-distribution* Egger p-values (0.85 / 0.49 / 0.46) while the CSVs correctly store the *t-distribution* values (0.8794 / 0.5580 / 0.4911). This table↔CSV gap was invisible to every prior round because those rounds checked the CSV/audit, not the rendered table. **A1 independently caught a biological mislabel** (HAVCR2/TIM-3 called an "up-regulated exhaustion marker" at line 143) that no prior round had flagged at the prose level. Two defects surfaced that the previous "clean" rounds had missed — the signature of genuine independent review, not delta-grading.

---

## 2. Verdict table

| Reviewer | Layer | Verdict | Desk-reject |
|---|---|---|---|
| A1 | Domain (sepsis immunology / repositioning biology) | **Major Revision** | No |
| A2 | Design / statistics / MR causal | Minor Revision *(statistics layer)* | No |
| A3 | Implementation / provenance audit | **Major Revision** | No |
| A4 | Venue / editorial / reporting | **Major Revision** | No |

**Adjudicated manuscript verdict: MAJOR REVISION (0 desk-reject).** A2's "Minor" certifies the *statistics layer* (all its recomputations matched the manuscript) but does not cover design-layer and prose-layer defects; per panel-adjudication rules the stricter verdict is adopted for the manuscript as a whole. No Tier-0 (conclusion-invalidating) error was found by any reviewer or by the editor's own re-derivation.

---

## 3. Cross-verification table (editor-verified)

| # | Manuscript location | Manuscript claims | Independently recomputed (editor, raw sources) | Checked by | Verdict |
|---|---|---|---|---|---|
| C1 | Table 3 MR-Egger P (28-d death) | CD74 0.85, HLA-DQA1 0.49, FIS1 0.46 | From `10_genetics_mr_outcome5086_28ddeath.csv` MR-Egger rows: t-dist p = 0.8794 / 0.5580 / 0.4911; **normal-dist p = 0.8479 / 0.4860 / 0.4634** → table shows the normal values | Editor + A3 | **MISMATCH (Tier-1)** |
| C2 | Table 3 MR-Egger P | CD14 4.9×10⁻², HAVCR2 0.95 | CD14 t-dist 0.0488 (=4.9e-2 ✓); HAVCR2 0.9546 (both dist ≈0.95 ✓) | Editor | correct |
| C3 | Line 143 "up-regulated exhaustion markers PDCD1, **HAVCR2/TIM-3** and LAG3" | HAVCR2/TIM-3 up-regulated | `S01_immunoparalysis_direction.csv`: HAVCR2 logFC −0.349, adj.P 2.8e-13, **Mars1_down**; PDCD1 +0.162 up; LAG3 +0.035 up (ns). Manuscript's own line 93 & §3.9 call HAVCR2 down. | Editor + A1 | **FACTUAL + INTERNAL CONTRADICTION (Tier-1)** |
| C4 | Audit 17/17 green | headline numbers guarded | Re-ran `check_audit_assertions.py`: EXIT=0, all 17 pass | Editor + A3 | correct (but does NOT guard the table prose — see C1) |
| C5 | Egger p in CSVs = t(df=n−2) | corrected in R6 | Confirmed: stored p = t-dist for all 15 MR-Egger rows | Editor | correct |
| C6 | 23/22/21 consensus | down/FDR/both | Matches `S01_immunoparalysis_direction.csv` | A3 + A2 | correct |
| C7 | External AUC 0.638 (CI 0.532–0.748, n=106, 52 deaths) vs L1 0.585 | disambiguated | `09_external_validation.csv` holds both keys, not conflated | A2 + A3 | correct |
| C8 | IRG 0.604 within signature 95% CI | honest framing | IRG single point estimate, no CI; correct framing | A2 | correct |
| C9 | Data-availability truthful | repo holds results+code, raw regenerable | `git ls-files`: 03_results/ + 02_scripts/ tracked; force-added `GSE65682_pheno.csv` present (802/760/42 verifiable); ~43 GB correctly excluded | Editor + A4 | **now correct** |
| C10 | CD74 critical-care WM q≈3e-17, reversed direction, 3 instruments | demoted to genotype–severity | Recomputed: OR 2.194, p 6.6e-19, Egger slope p 0.088 (df=1), IVW SE 0.325 > Egger SE 0.111 | A2 + A3 | correct & well-caveated |

---

## 4. Graded consolidated issue list

### Tier 1 — must fix before resubmission (no conclusion change, but citable defects)
- **T1 (C1).** Table 3 MR-Egger p-values for CD74, HLA-DQA1, FIS1 are the *normal-distribution* values (0.85 / 0.49 / 0.46); the source CSVs correctly store the *t-distribution* values (0.88 / 0.56 / 0.49). Correct the three cells. (CD14 0.049 and HAVCR2 0.95 are already correct.) Add a gate assertion that the **manuscript table** Egger p equals the CSV t-dist p, OR auto-generate Table 3 from the MR CSV, to close the "second occurrence goes stale" gap.
- **T2 (C3).** Line 143 calls **HAVCR2/TIM-3 an "up-regulated exhaustion marker"** — it is *down*-regulated in Mars1 (logFC −0.35, adj.P 2.8e-13; also stated correctly at line 93 and §3.9). This is both factually wrong and internally contradictory with §3.9 (which names PDCD1/LAG3 as the up markers). Re-frame the checkpoint-blockade decision on accurate biology: the elevated exhaustion marker is PDCD1 (and LAG3 directionally), not HAVCR2. Either drop the false "HAVCR2 up" premise or state the contraindication rationale without it. Reconcile §3.8 and §3.9.
- **T3 (A4).** No STROBE-MR compliance artifact. Add a STROBE-MR item table (9a/9b/10/11–17) as a supplementary file or inline; specifically report the **variant-selection flow** (identified at P<5e-8 → post-LD-clump → post-harmonisation → analysed) — currently only the final retained counts (27) are given.

### Tier 2 — wording / revision (needed for acceptance at most journals)
- **T4 (A4).** Structured abstract ≈463 words (lines 10–17); exceeds typical 250–350 caps (BMC 350, PLOS 300, Frontiers 200–250). Trim: move 23/25 immune-gene detail and per-estimator OR ranges into the body; keep the four top-line results.
- **T5 (A3).** Residual "six hub genes" loose phrasing at lines 64, 114, 155 ("the six immune hubs … FIS1 …"; "five of the six hub genes"). The reframing substance in §3.3/§4/§6/§7 is correct, but these residues call FIS1 an immune hub. Standardise to "six candidate genes (five immune hubs + FIS1 passenger)".
- **T6 (A2).** **Circularity of gene selection.** The 6 MR genes were chosen because they were expression-associated with the sepsis endotype / 28-day death, then tested for *causal* effect on sepsis outcomes — selection is built on the outcome. The 45-test BH does not correct this. Add one sentence acknowledging the selection-on-outcome circularity as a design limitation.
- **T7 (A2).** **Min-detectable-OR understated for key genes.** The single "MDO ≈1.25 at 80% power" is too low for CD74 (recomputed critical-care MDO ≈2.49; CD74 observed OR 2.22 is *below* its own MDO). Report per-gene MDO, or soften the single-number claim.
- **T8 (A4).** Orphan figure `04_figures/S01_roc_28d_mars1.png` is committed but never cited in text (grep-confirmed by A4). Cite it or remove it; verify every `04_figures/*.png` is referenced.

### Tier 3 — format
- **T9 (A4).** Vancouver journal-name inconsistency: refs 34 ("Intensive Care Med") and 35 ("Front Immunol") use abbreviations while the other ~33 use full forms. Standardise to NLM abbreviations or full spellings throughout.
- **T10 (A4).** Refs 2/3 page ranges appear truncated to a single page; verify full ranges (e.g., 2594–2603 / 801–810).
- **T11 (A2).** DCA reports only 3 thresholds (NB@0.20/0.30/0.50); add the threshold grid so the "NB>0 over 0.10–0.75, converges to 0 near 0.77" claim is auditable.

---

## 5. Consensus / complementarity / disagreement

**Consensus (all 4):** (a) the analytical core is reproducible and the MR null is honestly reported — a genuine strength; (b) the 5-immune-hub + FIS1-passenger reframing and the data-availability rewrite are now correct; (c) the contribution is *methodological* (near-replication of the known MARS antigen-presentation program + honest external validation + transparent, self-critical MR), not a novel biological or therapeutic discovery; (d) no desk-reject; Major Revision.

**Complementarity:** A3 (provenance) found the table↔CSV Egger mismatch; A1 (domain) found the HAVCR2 direction error; A2 (stats) confirmed all CSV/audit numbers and added the circularity + MDO caveats; A4 (reporting) added STROBE-MR/abstract/Vancouver gaps. Each caught defects in a different layer — the panel spanned the four required layers and they did not overlap.

**Disagreement:** A2 returned "Minor" while A1/A3/A4 returned "Major". Adjudicated: A2's Minor scopes to the *statistics layer* (which is solid); it does not certify the prose/biology/reporting layers. Adopted stricter verdict = Major Revision for the manuscript. Severity on T1/T2 is not in dispute (both are concrete mismatches); A2 did not contest them.

---

## 6. Priority must-fix list

| Priority | Item | Type | Desk-reject? |
|---|---|---|---|
| P1 | T1 — correct Table 3 Egger p (CD74/HLA-DQA1/FIS1) to t-dist; add table↔CSV gate | fix numbers | No |
| P1 | T2 — fix HAVCR2 "up-regulated exhaustion marker" at line 143; reconcile §3.8/§3.9 | fix biology + contradiction | No |
| P2 | T3 — add STROBE-MR checklist + variant-selection flow | add analysis/artifact | No |
| P2 | T4 — trim abstract to ≤350 words | reword | No |
| P2 | T5 — "six hub" → "six candidate genes (5 hubs + FIS1)" | reword | No |
| P3 | T6/T7 — circularity + per-gene MDO caveat | add caveat | No |
| P3 | T8–T11 — figure citation, Vancouver, page ranges, DCA grid | format | No |

**No DESK-REJECT flag on any item.**

---

## 7. What stands up (do NOT change)

- FIS1 correctly a non-immune, up-regulated (logFC +1.26) mitochondrial-fission **passenger**, not a mechanistic hub.
- 23/22/21 consensus counts exact (down / FDR / both).
- External AUC 0.638 (95% CI 0.532–0.748, n=106, 52 deaths) vs L1-locked 0.585 correctly disambiguated; IRG 0.604 point estimate honestly framed as within the CI (no formal test possible).
- MR-Egger p-values in the **CSVs** correctly use the t(df=n−2) distribution (17/17 audit green).
- `08b_clinical_translation.csv` `rescue_fraction_directional` kept distinct from Table-2 `response_gene_concordance`.
- Calibration slope/intercept 0.50/−0.04 and DCA NB from the external cohort; no "positive NB across all thresholds" over-claim.
- Data-availability statement now **truthful** (git-verified: 03_results + 02_scripts tracked; pheno force-added; ~43 GB correctly excluded).
- Primary-outcome MR null reported prominently; CD74 critical-care reversed-direction, 3-instrument signal correctly demoted to a genotype–severity association.
- 11 balanced limitations; celltype localizations and phenotype counts (802/760/42; Mars1=132) exact.

---

## 8. Recommended handling path

**Path A (recommended):** Restructure-and-resubmit as the same **Research** article type after T1–T3 (and preferably T4–T5). The analytical core, honest null MR, and portable external signature satisfy a methods-transparent Research paper.

**Path B (fallback):** Downgrade to **Computational Biology / Methods & Resources / Hypothesis-generating** if the author prefers to foreground the methodological contribution and the near-replication explicitly. A4 independently recommended this; it is defensible and removes the tension between the "Research/Novel" framing and the near-replication reality.

Do **not** choose C (wording-only) — T1 and T2 are numerical/factual fixes, not cosmetic.

---

## 9. Process lessons (what gates could not catch)

1. **The "second occurrence goes stale" trap is real and recurring.** The Round-6 bug (Egger p normal vs t) was fixed in the CSV and guarded by assertion 4, but the *manuscript table prose* still carried the old normal values through v1.7.0 → v1.8.0. A gate that checks `strings must match` only checks the enumerated first occurrence; the rendered table is a second, unguarded occurrence. **Fix:** generate Table 3 programmatically from the MR CSV, or add an assertion comparing the table's Egger p to the CSV t-dist p.
2. **17/17 green ≠ correct.** The audit verifies arithmetic and CSV↔CSV provenance. It cannot see (a) design-layer defects (T6 circularity, T7 MDO understatement) or (b) prose-layer defects (T1 stale table numbers, T2 mislabeled biology, T5 residual "hub" wording). These require human-style, assumption-challenging review.
3. **Independence buys exactly what automation cannot:** each reviewer read the *current state* without the author's memory of "we already handled that." T1 and T2 are defects that prior rounds' "clean" verdicts had papered over because those rounds trusted the CSV/audit and stopped at the data layer.
4. New gate assertions recommended: (i) manuscript Table-3 Egger p == CSV t-dist p (per gene); (ii) every `04_figures/*.png` referenced in text; (iii) every "up/down" biological claim about a hub maps to `S01_immunoparalysis_direction.csv` direction; (iv) abstract word count ≤ 350.

---

## 10. Editor's reframe note to the author

- **Strongest claim that does not fully hold:** the MR layer is essentially null (only a *reversed-direction*, 3-instrument CD74 signal survives family correction, and it is explicitly demoted). The manuscript nonetheless headlines "candidate, expression-level intervention hypotheses" and an "immunoparalysis axis" that reads as therapeutically addressable. The honest contribution is the **methodological triangulation + honest independent cross-platform external validation + transparent self-critical MR + hypothesis-generating repositioning shortlist** — not a causal or therapeutic demonstration.
- **Buried finding that IS the contribution:** the portable external AUC 0.638 on an independent platform, the candid MR self-criticism, and the *near-replication* of the MARS antigen-presentation program. Swapping the emphasis — lead with "methodological near-replication of a known endotype + portable signature + honest null MR" — converts the paper from a fragile signal-chaser into a solid methods/resource contribution, and pre-empts the "downgrade?" question A4 raised.
- **Why the failures are not your fault:** the Table-3 Egger mismatch is a rendering/auditing pipeline gap (CSV fixed, table not regenerated); the HAVCR2 mislabel is a single prose sentence that contradicts your own correct Table 2/§3.9. Both are fixable in hours, not months.
