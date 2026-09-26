# REVIEW — Round 7 Independent Expert Panel (manuscript.md v1.6.0)

**Manuscript:** *Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning* (single-author; `05_reports/manuscript.md`; commit `e5856b6`, tag `v1.6.0`).
**Article type under review:** computational / multi-omics translational research article.
**Panel:** 4 blinded reviewers recruited fresh, each forbidden from reading any prior round (`REVIEW_round6_20260926.md`, `review_r6/`, `RESPONSE_*/REVISION_*/review_r1–r5`, other reviewers' files, `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`).
**Reviews:** `05_reports/review_r7/A1_domain_sepsis_immunology.md`, `A2_design_biostat_mr.md`, `A3_implementation_provenance.md`, `A4_venue_editor_reporting.md`; shared brief `review_r7/_PANEL_BRIEF.md`.

---

## 1. Independence statement

Each reviewer received a self-contained brief and an explicit forbidden-file list, and was instructed to re-derive every quantitative claim from the raw `03_results/*.csv` files and `02_scripts/python/` scripts. None had access to prior rounds. **Evidence the discipline worked:** the four reviewers converged on a shared verdict (Major revision; analytical core reproducible) but hit *different* defects from different angles — A1 on biological-exhaustion wording, A2 on DCA/overlap framing, A3 on the forest-plot code bug and the audit-gate no-op, A4 on abstract headline-vs-evidence contradictions. No two reviewers re-litigated the *same* point using the *same* evidence; the overlap is on interpretation of the same disclosed facts, which is the expected signature of genuine independence (not echo-chamber repetition of prior findings).

---

## 2. Verdict table

| Reviewer | Layer | Verdict | One-line rationale |
|---|---|---|---|
| A1 | Domain (sepsis immunology) | **Major revision** | Biological/clinical over-statements (TIM-3 direction, LAG3, "converged", hub prognostics); **no numeric error**. |
| A2 | Design (biostat / MR) | **Major revision** | Every statistic reproduces exactly; issues are interpretation/framing (DCA overstated, overlap bias directional, CD74-WM fragility). |
| A3 | Implementation (provenance) | **Major revision** | No fabricated numbers; but a concrete figure code bug, an abstract numeric falsehood, a 30↔29 mismatch, and an audit-gate that can no-op. |
| A4 | Venue (editor / reporting) | **Major revision → recommend Option B (reframe/downgrade)** | Analytical core honest, but headline verbs ("therapeutically addressable", "direct-target validation pending") and the English abstract's FIS1 localisation out-run the evidence. |

**Distribution:** 0 desk-reject, 4 × Major revision (one of which recommends downgrade/reframe). No Tier-0 (conclusion-invalidating) error was found by any reviewer — the single most important outcome of this round.

---

## 3. Cross-verification table — manuscript claim vs independently recomputed value

| # | Location | Manuscript claims | Independently recomputed | Checked by | Verdict |
|---|---|---|---|---|---|
| C1 | Abstract L14 | "all IVW OR 0.92–1.12, **P ≥ 0.24**" | min primary IVW p = **0.2359** (CD14) | A3, **editor-confirmed** | ✗ **false** (derived from rounded 0.24 not stored 0.2359) |
| C2 | `mr_forest.png` title | "red = family q<0.05" | code compares `s.sig=="yes"` vs CSV `"YES"` → **0 red pixels** | A3, **editor-confirmed** | ✗ **defect** (only family-sig result not highlighted) |
| C3 | §3.4 | "positive net benefit over treat-none across the full threshold range" | 19/91 thresholds NB = 0 (tie), all ≥0.77 | A2, A3 | ✗ overstated |
| C4 | Abstract L14 (EN) | "Six hub genes … localized to monocytes / antigen-presenting cells" | FIS1 is mitochondrial-fission, up-regulated, **not** in §3.6 localisation list | A4 | ✗ **false localisation** |
| C5 | §3.7 / Abstract | "IFN-γ rescued 4/5 antigen-presentation genes" | `08_candidates_drugs.csv`: IFN-γ = **4/7** (HLA-DQB1 absent from rescued) | A4 | ✗ denominator mismatch |
| C6 | §3.4 | "exceeded treat-all above ~0.20" | equal to treat-all at 0.20 (gap +0.012 at 0.30, within noise at n=106) | A2, A3 | ⚠ overstated |
| C7 | §3.2 table | Mars3 median **0.641** | exact median = 0.64048 → 0.640 | A3 | ⚠ rounding |
| C8 | §3.1 | 3,597-DEG count sourced to `S01_roc_28d_mars1.png` | ROC cannot evidence a DEG count; correct source `S01_mars1_deg.csv` | A3 | ⚠ mis-cited figure |
| — | §3.1 / Abstract | 23/25 down, 22/25 FDR<0.05, 21 both | recomputed 23 / 22 / 21 | A1, A3 | ✓ |
| — | §3.1 | FIS1 only hub up; other 5 down | recomputed 5 down + FIS1 +1.261 | A1, A3 | ✓ |
| — | Table 2 | IL-7 0.80, GM-CSF 0.67, IFN-γ 0.57, … | matches `08_candidates_drugs.csv`; provably from `DEG_0.3` rule | A1, A3 | ✓ |
| — | §2.10/§3.10 | MR-Egger p = t(df=n−2), CD14 4.9e-2, CD74-crit Egger 0.088 | 15/15 Egger rows match t-dist; 0 match normal | A2, A3, **editor** | ✓ |
| — | §3.10 | exactly 1/45 family-sig (CD74-crit WM, q≈3e-17, reversed) | BH recompute: 1/45, q=2.99e-17, OR 2.194>1 | A2, A3 | ✓ |
| — | §3.2 / §3.5 | immune-score P 0.47 / 1.9e-18 / 1.3e-3; ext AUC 0.638 (CI 0.532–0.748); calib slope 0.50 / int −0.04 | recomputed exact match | A2, A3, A4 | ✓ |
| — | §3.9 | L1000 layer (20,413 cmpds, top 0.32, lenalidomide 26.6%) | recomputed exact match | A3 | ✓ |

**Bottom line of the table:** every headline *statistic* traces to a real CSV value at the stated precision; the discrepancies are (a) two factual errors in the English abstract (C1, C4), (b) one figure code defect (C2), (c) three overstated interpretation/framing claims (C3, C5, C6), and (d) minor citation/rounding slips (C7, C8).

---

## 4. Graded consolidated issue list

### Tier 0 — conclusion-invalidating
**None.** No reviewer found a fabricated number, a reversed headline direction, or a statistics error that changes the paper's conclusions. (This is the critical result of the round: v1.6.0's data-correcting revision held up under independent recomputation.)

### Tier 1 — analyses/figures/abstract to fix before any resubmission
- **T1-1 (C1)** Abstract "all IVW P ≥ 0.24" is false (CD14 = 0.2359). Change to "P ≥ 0.23" or "all P ≥ 0.236". *Editor-verified.*
- **T1-2 (C2)** `mr_forest.png` does not highlight the one family-significant test ("red = q<0.05" but 0 red points). Fix `_mr_diagnostics.py:81` to `str(s.sig).strip().lower()=="yes"`, regenerate, and add a regression assertion. *Editor-verified.*
- **T1-3 (C4)** English Abstract falsely localises FIS1 to monocytes/APC. Mirror the Chinese-abstract carve-out (FIS1 = mitochondrial-fission marker, not immune-localised).
- **T1-4 (A4-1/3)** Headline verbs out-run evidence: "therapeutically addressable axis" and "direct-target validation still pending" contradict the same-paragraph "hypothesis-generating / not a demonstration" and §2.8's "no direct-target pull was performed". Replace with candidate/expression-level framing.
- **T1-5 (A3-3)** 30-gene signature vs 29-gene locked coef JSON never reconciled. State explicitly which gene is missing from the L1 design matrix and why; reconcile with the "29/30 mapped" external statement.
- **T1-6 (A3-7 / process)** `check_audit_assertions.py` exits **0 on ImportError** (`sys.exit(0)` at lines 82–87) — the gate silently no-ops without pandas/scipy. Change to `sys.exit(2)`; the manuscript's own "every number traces to a file" claim requires a non-vacuous gate.
- **T1-7 (A2-1 / A3-2)** DCA framing overstated ("positive across full range"; "exceeded treat-all above ~0.20"). Reframe around the calibration slope (0.50, under-dispersed) and state the model ties treat-none above ≈0.77 and only clears treat-all by a noise-level margin at n=106.

### Tier 2 — wording / internal contradictions
- **T2-1 (A1-1)** Discussion says "TIM-3 up" but HAVCR2/TIM-3 is Mars1-down (Δ=−0.35, FDR 2.8e-13). Delete "TIM-3 up"; restrict exhaustion-axis claim to PDCD1.
- **T2-2 (A1-2)** LAG3 presented as up-regulated exhaustion marker but not FDR-significant (adj.P 0.55). Downgrade.
- **T2-3 (A1-3)** "Degree-centrality and ML consensus *converged*" is contradicted in the same paragraph (co-expression network surfaced erythroid/heme genes). Rephrase to "ML consensus identified …; degree-centrality pointed elsewhere."
- **T2-4 (A1-4)** "Hub genes prognostically informative" over-claims; AUC is a set/orientation property (7 hubs got zero L1 weight). Scope to the axis.
- **T2-5 (A4-4 / C5)** IFN-γ "4/5 antigen-presentation" (§3.7) vs CSV 4/7. Reconcile denominator to 4/7 across §3.7 + Abstract.
- **T2-6 (A2-4)** CD74 critical-care MR-Egger SE (0.111) < IVW SE (0.325) on identical slopes is unresolved; re-derive against a reference closed form and disclose.
- **T2-7 (A3-9)** `mr_diag.png` panel (d) title attributes family-significance to the IVW/Egger panel while the surviving estimator is the weighted median (not plotted). Retitle/add WM.
- **T2-8 (A4-5)** STROBE-MR 9b per-SNP drop-list "available on request" → deposit as supplementary CSV.
- **T2-9 (A4-6)** EPV (≈3.8, 114 deaths / 30 genes; 7 of 29 zero-weighted) not reported — add to §3.4 (strengthens honesty).
- **T2-10 (A3-5)** §3.1 cites a ROC figure for the 3,597-DEG count — re-point to `S01_mars1_deg.csv`.
- **T2-11 (A1-7 / A4-7)** Stratified-treatment language ("may benefit most / may prefer IL-7") reads as recommendation without subgroup evidence — recast as testable hypothesis. README residual "immune-restorative" over-claim → "candidate … hypothesis-generating."

### Tier 3 — format
- **T3-1 (A4-8)** Expand MODZ at first use; add one-line captions for cited figures; append "(two-sided)" to Mann–Whitney P; state "df = n_instruments − 2 = 4" at the CD14 Egger claim; confirm §3.10 is not truncated mid-word in the submitted file.
- **T3-2 (A3-8a)** Mars3 median 0.641 → 0.640; adopt one rounding rule and emit in-text constants from a script.

---

## 5. Consensus / Complementarity / Disagreement

**Consensus (all four):** (i) the analytical core is reproducible and the MR null is honestly disclosed — a genuine strength; (ii) the *headline verbs* ("anchored", "therapeutically addressable", "direct-target validation pending") exceed the evidence; (iii) the audit gate is a good start but does not guard most headline numbers and can no-op.

**Complementarity:** A1 supplied the biological nuance (TIM-3, LAG3, FIS1 biology, 28-day endpoint mismatch); A2 supplied the design-layer critique (DCA/overlap bias direction, CD74-WM fragility); A3 supplied the forensic code/figure defects (forest red bug, gate exit(0), 30↔29, abstract P≥0.24); A4 supplied the reporting-layer contradictions (abstract localisation falsehood, headline-vs-caveat). The four layers caught disjoint defect classes — confirming the panel composition.

**Disagreement:** A4 recommends **Option B (downgrade/reframe to Hypothesis/Computational-Biology or Methods & Resource)**, while A1/A2/A3 frame it as Major revision with rewording + figure fixes and keep the Research-Article type. **Editor's adjudication:** adopt the *stricter* interpretation for the substance — the gap is evidence-level vs claim-strength, exactly A4's point — but the fix is primarily **re-wording + the T1 concrete fixes**, not a structural rebuild. A full downgrade is not required *if* T1-1…T1-7 are applied; however, if the author retains causal/therapeutically-addressable framing after T1-4, then Option B becomes mandatory. The recommended path is therefore: apply all T1 fixes (which neutralise A4's downgrade trigger) and keep Research-Article type; if the author resists T1-4, switch to Option B.

---

## 6. Priority must-fix list

**DESK-REJECT flags:** none.

**Must-fix before resubmission (blocking):**
1. T1-1 Abstract "P ≥ 0.24" → "P ≥ 0.23" (factual error).
2. T1-2 Regenerate `mr_forest.png` with the red-highlight bug fixed + add regression assertion.
3. T1-3 English-abstract FIS1 localisation corrected.
4. T1-4 Soften "therapeutically addressable" / "direct-target validation pending" to candidate/expression-level framing.
5. T1-5 Reconcile 30↔29 signature/coef.
6. T1-6 Make the audit gate non-vacuous (`sys.exit(2)` on ImportError).
7. T1-7 Re-frame DCA around calibration slope; drop "positive across full range."

**Must-add-analysis vs must-reword split:**
- *Must reword only:* T1-1, T1-3, T1-4, T2-1…T2-5, T2-9, T2-10, T2-11, T3-1/2.
- *Must re-run code/figure:* T1-2 (regenerate forest), T1-5 (coef JSON regeneration if incomplete), T1-6 (gate fix), T2-6 (Egger SE re-derivation), T2-7 (diag retitle/WM).
- *No new dataset required*: every fix is achievable from existing `03_results/` artefacts.

---

## 7. What stands up (do NOT change)

Carried from the reviewers' "§ Stands up":
1. **23/25 · 22/25 · 21/25 consensus counts** — exact (A1, A3).
2. **Hub directions** — 5 down + FIS1 up (+1.26); honestly framed as a marker (A1, A3).
3. **Table 2 concordance provably derives from the `DEG_0.3` rule** (not bare direction) — re-running `_recompute_table2.py` reproduces the CSV byte-identically (A1, A3).
4. **MR-Egger p-values use the correct t(df=n−2) distribution** — 15/15 match, 0 match normal; the v1.6.0 data correction is real (backup-vs-current diff confirms stored p-values changed, not just prose) (A2, A3, editor).
5. **Exactly one 45-test family-significant result, direction-reversed** — BH recompute q=2.99e-17, OR 2.194>1 (A2, A3).
6. **External AUC 0.638 (CI 0.532–0.748), calibration slope 0.50 / intercept −0.04, DCA values** — all trace and reproduce; `S06_dca.png` is genuinely the external cohort (A2, A3, A4).
7. **ImmunoSep (Giamarellos-Bourboulis, JAMA 2025) cited and represented fairly** (A1).
8. **Glucocorticoid positive-control caveat and the curated-vs-direct-target distinction are honestly maintained** (A1).
9. **§7 number-provenance table is exemplary** (A4) — the model other submissions lack.

---

## 8. Recommended handling path

**Recommended: Option A (restructure-and-resubmit as the same article type), conditional on applying T1-1…T1-7.** The analytical core is sound and reproducible; the defects are (a) two factual abstract errors, (b) one figure code bug, (c) headline-strength-vs-evidence, and (d) a non-vacuous audit gate. None requires new data. If the author retains causal/"therapeutically-addressable" framing after T1-4, switch to **Option B (downgrade/reframe to Hypothesis / Computational-Biology or Methods & Resource)** per A4.

Option C (wording-only) is **not viable as a standalone path** — but note that most of the required changes *are* wording; the only true code/figure re-runs are T1-2, T1-5, T1-6, T2-6, T2-7, all cheap.

---

## 9. Process lessons (what gates could not catch, and how to extend them)

- **A green gate proves arithmetic, not design — and can even be vacuous.** The single most important lesson this round: `check_audit_assertions.py` passed at exit 0 yet (i) the forest figure it implicitly certifies drew 0 red points (C2), and (ii) the script `sys.exit(0)`s on missing pandas, so a degraded CI runner would report green while checking almost nothing (T1-6). **A gate that can no-op is worse than no gate** — it manufactures false confidence. Fix: `sys.exit(2)` on ImportError; and every figure must be regression-tested (pixel/value assertion), not just the CSVs it reads.
- **Headline-vs-caveat contradiction is invisible to a consistency gate.** A4's T1-4 ("therapeutically addressable" in the Conclusion vs "hypothesis-generating" two sentences later) is a self-contradiction no numeric assertion detects. **Rule:** grep the manuscript for each strong verb ("addressable", "demonstrate", "validate") and require a matching strength in the Limitations; quote both locations.
- **Concrete new assertions to extend gate coverage to the design/figure layer (from A3):** A9 (MR OR/CI/p algebraic consistency), A10 (per-gene I² value guard), A11 (Table-1 effect sizes), A12 (23/22/21), A13 (Table-2 concordance), A14 (validation AUC/calibration/DCA NB), A15 (BH internal consistency), A16 (forest significance + gate non-vacuous). Adopt A9–A16 before repository deposit.
- **The "disclosure ≠ resolution" trap recurred.** v1.6.0 correctly added caveats (MR null, immune-score non-specificity) but left stronger verbs standing in the Abstract/Conclusion — the exact failure class that sank prior rounds. The fix is to **retract the headline verb, not merely qualify it elsewhere.** This must be a standing gate rule.
- **Endpoint-biology mismatch is a design-level bias a gate cannot see.** A1's T1-equivalent point (28-day death dilutes the immunoparalysis signal, plausibly driving the null MR) is a hypothesis about *why* the MR is null — only a domain reviewer raised it; neither recompute nor gate would. Preserve the human panel for design-layer questions.

---

*End of Round-7 consolidated review. Review artifacts: `05_reports/review_r7/` (4 expert files + brief) and this report. No code was modified by the panel; all fixes are the author's next step (Round-7 revision → v1.7.0).*
