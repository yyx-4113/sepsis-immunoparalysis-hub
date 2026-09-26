# Round 5 Independent Expert Review — v1.4.0

**Manuscript:** `05_reports/manuscript.md` (v1.4.0, commit `ddb8575`, tag `v1.4.0`)
**Date:** 2026-09-26
**Panel:** 5 blind lenses — A1 Domain/Clinical, A2 Design/Statistics/Causal, A3 Implementation/Provenance, A4 Venue/Reporting, A5 Drug-repositioning/LINCS
**Editor verification:** performed independently (see §3 cross-verification table)

---

## 1. Independence statement

The panel was briefed to ignore `REVIEW_round*.md`, `review_r2/`, `review_r3/`, `review_r4/`, and `RESPONSE_*.md`, and to treat the manuscript as a first submission. Each lens file (`review_r5/A1`–`A5`) was written without reading the others.

**Evidence independence worked:** Every lens independently converged on the same two structural themes from different angles — (a) the *reverse-direction CD74 critical-care signal is over-emphasised*, and (b) the *MR caveats need precision* (Egger-with-3-instruments, overlap-bias direction, I² range). Three independent lenses (A1, A2, A3) also independently caught the **I² 0.00–0.29 claim contradicting the source CSVs (true max 0.502)** — the diagnostic signature of genuine independence (clustered hit from different angles on a real defect). No finding was unique to a single reviewer in a way that suggested diffusion.

---

## 2. Verdict table

| Lens | Verdict | Headline |
|------|---------|----------|
| A1 Domain/Clinical | **Major (fixable)** | Reverse CD74 signal over-headlined; FIS1 uninterpreted |
| A2 Design/Stats | **Major (fixable)** | I² range wrong vs CSV; Egger-3-instrument & overlap-bias wording imprecise |
| A3 Implementation | **Minor–Major** | I² error confirmed; STROBE-MR drop-list qualitative |
| A4 Venue/Reporting | **Minor** | "addressable axis" unhedged; emphasis tone |
| A5 Drug-repositioning | **Minor** | "rescue" label muddled for an axis that rewards exhaustion up-regulation |

**Distribution:** 0 Desk-reject / 0 Tier-0 conclusion-invalidating; 4 × Tier-1 (all fixable wording/statistic precision); several Tier-2; a few Tier-3.

**This is a healthy manuscript.** The catastrophic MR fabrication of v1.3.0 is fully corrected: the MR layer now traces exactly to `10_mr_bh_family.csv` and the three raw CSVs. Round 5 is about *precision and emphasis*, not structural rescue.

---

## 3. Cross-verification table (editor-recomputed)

| # | Location | Manuscript claim | Editor-recomputed value | Source | Verdict |
|---|----------|------------------|------------------------|--------|---------|
| 1 | §2.10 / §3.10 | 3 CD74 tests q<0.05: critcare Egger q≈1.5×10⁻¹¹, WM q≈0, suscept Egger q≈0.0025 | q = 1.49×10⁻¹¹, 0, 2.47×10⁻³ | `10_mr_bh_family.csv` | ✅ correct |
| 2 | §3.10 | CD14 28d Egger OR 0.906, P=5.1×10⁻³, family q≈0.058 | OR 0.90595, P=5.11×10⁻³, q=0.0575 | `10_genetics_mr_outcome5086_28ddeath.csv` | ✅ correct |
| 3 | §3.10 | CD74 critcare Egger OR 2.222, intercept P=1.00 | OR 2.2217, intercept_p=0.99987 | `10_genetics_mr_outcome4982_criticalcare.csv` | ✅ correct |
| 4 | §3.10 | CD74 suscept Egger OR 1.118, P=1.7×10⁻⁴, intercept P=1.0×10⁻⁴ | OR 1.1179, P=1.65×10⁻⁴, intercept_p=9.98×10⁻⁵ | `10_genetics_mr.csv` | ✅ correct |
| 5 | §3.10 | CD74 critcare "only three instruments" | nsnp=3 (all 3 CD74 tests) | 3 MR CSVs | ✅ correct |
| 6 | §3.5 | External AUC 0.638 (0.532–0.748), n=106, 52 deaths | 0.6382 (0.5317–0.7475), n=106, 52 deaths | `09_external_validation.csv` | ✅ correct |
| 7 | §3.4 / §3.5 | CV AUC 0.659, train 0.750; IRG recomputed 0.604 | 0.6586, 0.7495; IRG 0.604 | `S06_auc_compare.csv`, `09_external_validation.csv` | ✅ correct |
| 8 | §3.10 | "heterogeneity was low (I² 0.00–0.29)" | **true max I² = 0.502** (FIS1 critcare); 4 tests >0.29 | 3 MR CSVs (recomputed) | ❌ **WRONG** — range only true for primary outcome |
| 9 | §3.10 | "median F 35–168" | 35.4–168.1 (Table 3) | `10_genetics_mr_outcome5086_28ddeath.csv` | ✅ correct |
| 10 | §7 / global | 31 refs, all cited, no orphan | 31 defined, 31 cited, 0 orphan | regex | ✅ correct |
| 11 | global | banned overclaim phrases absent | 0 hits (`therapeutically targetable`, `可药性`, `0.054`, `42-test`, `four of five`, …) | regex | ✅ correct |

**Independently confirmed by the editor:** items 1–7, 9–11 reproduce exactly; item 8 is a genuine error (the "0.00–0.29" range is only valid for the primary outcome — secondary outcomes reach I²=0.502). This is the one NEW factual defect and is Tier-1 (word-change + scope, not a re-analysis).

---

## 4. Graded consolidated issue list

### Tier 0 (conclusion-invalidating) — NONE
The MR fabrication is fixed; no claim invalidates the manuscript.

### Tier 1 (must fix — precision / one wrong statistic)
- **T1-1 (A2-1/A3-1): I² range error.** §3.10 "heterogeneity was low (I² 0.00–0.29)" is false for the full MR set (true 0.00–0.502). *Fix:* scope to primary outcome + disclose secondary I² (up to 0.50 for FIS1 critical care). [Paste-ready in A2-1.]
- **T1-2 (A2-2): Egger intercept with 3 instruments.** Do not cite the null CD74-critical-care Egger intercept (P=1.00) as reassurance — with 3 SNPs the intercept is uninformative about pleiotropy. *Fix:* append "although with only three instruments the Egger intercept is uninformative about pleiotropy, so its null cannot be read as evidence against it." [A2-2.]
- **T1-3 (A2-3): Sample-overlap bias direction.** "inflated by exposure–outcome sample overlap" implies magnitude exaggeration; overlap primarily biases SEs downward (inflated type-1-error). *Fix:* "overlap biases standard errors downward (inflating type-1-error risk); the true association may be weaker or null." [A2-3.]
- **T1-4 (A1-1): Over-emphasis of the reverse CD74 signal.** "the strongest MR association in the study" ×3 over-weights a reverse, 3-instrument, overlap-affected, explicitly-non-causal result. *Fix:* one mention in secondary/limitations context; delete the other two and the Table 4 ⚠️. [A1-1.]

### Tier 2 (wording / framing)
- **T2-1 (A4-1): "therapeutically addressable axis" unhedged** in Abstract/Discussion/Conclusion. *Fix:* add "(in expression terms; direct target validation pending)". [A4-1.]
- **T2-2 (A5-1): L1000 "rescue" label muddled.** The merged score rewards up-regulation of PDCD1/LAG3 (exhaustion markers pathologically UP in Mars1). *Fix:* relabel as "Mars1-down-axis reversal proxy (single-direction; co-rewards exhaustion-marker up-regulation)"; reserve "rescue" for the AP/monocytic subset. [A5-1.]
- **T2-3 (A1-2): FIS1 biological interpretation missing.** *Fix:* one clause linking FIS1 downregulation to mitochondrial/oxidative-stress coupling (or state it is a co-expression passenger). [A1-2.]
- **T2-4 (A2-4/A3-3): Secondary-outcome I² not in Table 4; STROBE-MR drop-list "on request".** *Fix:* add I² column to Table 4; report exact harmonisation drop counts in §2.10. [A2-4, A3-3.]

### Tier 3 (format / process)
- **T3-1 (A3-2):** Split the long §2.10 BH paragraph for edit-safety. No content change.
- **T3-2 (A4-3):** Pre-submission, confirm the GitHub repo is populated and consider minting the Zenodo DOI alongside.
- **T3-3 (A3-4):** Optional CI assertion that every §7 provenance path exists.

---

## 5. Consensus / Complementarity / Disagreement

**Consensus (all 5 lenses):**
- v1.4.0's MR numerical layer is correct and the BH table is a genuine improvement.
- The reverse-direction CD74 critical-care signal should NOT be headlined as "strongest."
- The I² 0.00–0.29 claim is wrong against the data (A1/A2/A3 converged independently).

**Complementarity:**
- A1 (clinical) and A4 (venue) both landed on "addressable axis" hedging from different angles (biological tractability vs reporting-checklist).
- A5 (drug) supplied the conceptual "rescue ≠ restoration" critique that A2/A3 did not reach.
- A3 (implementation) provided the recomputation that confirmed A2's I² finding as a real data-vs-text mismatch, not a reader misinterpretation.

**Disagreement:** None material. A3 rated the I² error "Minor–Major" while A2 rated it "Major"; the editor adopts **Major (Tier-1)** because, although the fix is a word-change, the error is a stated statistic contradicting the manuscript's own CSV — the exact failure class that previously caused a desk-risk. Severity is adopted from the stricter lens per the skill's adjudication rule.

---

## 6. Priority must-fix list

| Priority | Item | Type | DESK-REJECT? |
|----------|------|------|--------------|
| 1 | T1-1 I² range 0.00–0.29 → 0.00–0.502 (scope + disclose) | reword + 1 number | No |
| 2 | T1-2 Egger-3-instrument caveat | reword | No |
| 3 | T1-3 overlap-bias direction precision | reword | No |
| 4 | T1-4 demote "strongest MR association" ×3 → ×1 | reword | No |
| 5 | T2-1 "addressable axis" hedge | reword | No |
| 6 | T2-2 L1000 "rescue" relabel | reword | No |
| 7 | T2-3 FIS1 interpretation | add 1 clause | No |
| 8 | T2-4 Table 4 I² column + drop counts | add data | No |

No DESK-REJECT flags. Everything is must-reword or must-add-a-number; nothing requires a new analysis except the optional I² column (already computable from existing CSVs).

---

## 7. What stands up (do NOT change)

- External validation AUC 0.638 (CI 0.532–0.748) on E-MTAB-4451 — honest, real, comparable to IRG 0.604.
- Within-cohort CV 0.659 / train 0.750, correctly flagged as optimistic.
- MR family-BH: 3 CD74 tests q<0.05 (critcare WM q=0, critcare Egger q=1.5×10⁻¹¹, suscept Egger q=0.0025); CD14 28d Egger q≈0.058 (not <0.05). All trace to `10_mr_bh_family.csv`.
- FIS1 correctly separated as non-immune in Abstract/§3.3/§6 (the v1.3.0 self-contradiction is gone).
- IFN-γ 5/5 positive-control gate and the glucocorticoid "rescue ≠ restoration" caveat — methodological strengths.
- wtcs = rescue × √22 redundancy disclosed; dual-direction requirement not implemented, disclosed.
- 31/31 references cited; banned overclaim phrases eliminated.

---

## 8. Recommended handling path

**Path A — wording + precision revision (recommended).** This is NOT a restructure and NOT a downgrade. v1.4.0's strongest real finding (endotype-driven immunosuppressed transcriptome + honest external AUC 0.638 + a transparent MR layer that now correctly reports a reverse, family-surviving CD74 signal as a genotype–severity association) is intact. The 8 must-fix items are all rewordings or one disclosed number; apply them as a v1.5.0 pass.

Do **not** take Path B (downgrade article type) — the contribution is a solid multi-omics + repositioning + honest MR dissection, appropriate for a bioinformatics/sepsis-methodology venue.

---

## 9. Process lessons

- **The I² error is the same genus as the v1.3.0 fabrication:** a stated statistic that does not match the file. v1.4.0 fixed the MR *claim* but a copy-paste "I² 0.00–0.29" survived from an earlier draft where only the primary outcome was in view. **Lesson for the gate:** add an assertion that every *stated numeric range* in the text (I², F, OR CI bounds, AUC CI) is re-derived from the cited CSV at build time, not just key headline numbers. A one-line CI check `assert max(I2 across 10_*.csv) <= stated_max` would have caught T1-1.
- **"Disclosure ≠ resolution" still bites:** the Egger-intercept and overlap caveats were *present* but the *framing* still leaned on them as reassurance. The panel's job is to read whether the headline or the caveat carries the reader — here the headline ("strongest MR association") out-weighed the caveats.
- **New artefact that worked:** `10_mr_bh_family.csv` (per-outcome 15-test + 45-test family q) materially reduced re-litigation risk. Recommend keeping it and adding an I² column to Table 4 so secondary heterogeneity is visible without re-running.
