# Round-9 Independent Review — A3 (Implementation & Provenance Audit)

**Reviewer:** A3 — Implementation & provenance auditor (numbers ↔ source files; audit-assertion 1–17 fidelity; broken syntax / double-rounding)
**Manuscript:** `05_reports/manuscript.md` (v1.8.0, commit `180ecb1`)
**Verdict:** **MAJOR (revision required). No DESK-REJECT.** No fabrication and no unrecoverable defect, but the headline MR Table 3 does not trace to its source CSVs and the audit's "17/17 pass" overstates coverage. Both are fixable.

---

## Top 3 issues

### Issue 1 — Table 3 MR-Egger p-values are the *normal*-distribution values, contradicting the t-distribution source CSVs
- **【Problem】** Three of five MR-Egger p-values printed in Table 3 are the normal-distribution values, while the cited CSVs (and the audit's own assertion 4) store the t-distribution values — so the headline MR table does not trace to its source files and re-introduces the exact error the Round-6 audit was built to kill.
- **【Evidence】** `03_results/10_genetics_mr_outcome5086_28ddeath.csv` MR-Egger rows: CD74 stored p = 0.8794 (t-dist), normal = 0.8479, but manuscript Table 3 (`manuscript.md:163`) prints "1.093 **(0.85)**"; HLA-DQA1 stored p = 0.5580, normal = 0.4860, but `manuscript.md:164` prints "0.954 **(0.49)**"; FIS1 stored p = 0.4911, normal = 0.4634, but `manuscript.md:167` prints "0.964 **(0.46)**". CD14 (0.0488 → "(4.9×10⁻²)", `manuscript.md:165`) and HAVCR2 (0.9546 → "(0.95)", `manuscript.md:166`) match the t-distribution. The Egger column is therefore internally mixed — normal for 3 rows, t for 2.
- **【Why it matters】** The Round-6 audit's explicit purpose was to erase this normal-vs-t-dist bug; assertion 4 even *fails* if a stored p equals its normal value. Yet Table 3 still displays the old normal values for CD74/HLA-DQA1/FIS1, so a reader re-deriving Egger p from the committed CSV gets 0.879 / 0.558 / 0.491, not the printed 0.85 / 0.49 / 0.46. The manuscript's central "every number traces to a source file" claim is violated for a core result, and the "Egger p now uses the t-distribution" framing is internally false in the table. (Conclusion is unchanged — none are significant either way — but the auditability is broken.)
- **【Specific fix】** Regenerate Table 3's MR-Egger cells directly from `10_genetics_mr_outcome5086_28ddeath.csv`: CD74 → **0.88** (0.879), HLA-DQA1 → **0.56** (0.558), FIS1 → **0.49** (0.491); keep CD14 0.049 and HAVCR2 0.95. Best: have the table render from the CSV Egger row so it cannot drift, and add one methods sentence: "All MR-Egger p-values are two-sided t(n−2) unless stated."

### Issue 2 — The "17/17 audit passed" gives false assurance: several headline numbers are unguarded
- **【Problem】** The audit passing all 17 assertions does not verify a substantial set of headline numbers; a CI-gate "pass" can be read as full numeric certification when it is metadata/range-only for many claims.
- **【Evidence】** Recomputed by me (unguarded by any assertion): `S01_mars1_deg.csv` Mars1 DEG count = **3597** and `S01_deg_sepsis_vs_ctrl.csv` sepsis-vs-healthy = **448** (no assertion); `S06_auc_compare.csv` CV = 0.6586 / train = 0.7495 (assertion 3 only checks file *existence*); FIS1 logFC = 1.2614 (assertion 7 checks *direction* only, not +1.26); `S08_l1000_rescue_trtcp.csv` = **20,413 rows** with lenalidomide rank 5435 / azithromycin 9152 (unguarded); `07_hub_celltype.csv` CD14 r = 0.773 etc. (unguarded). Assertion 9 checks OR/CI algebra against beta/se but does **not** compare the manuscript's printed Table 3/4 ORs to the CSV (they happen to match on manual check, but the audit would not catch a typo in the printed OR).
- **【Why it matters】** Editors/reviewers treating "audit EXIT=0" as full provenance certification are misled; numbers a reviewer assumes are verified are in fact unguarded.
- **【Specific fix】** Add assertions: (a) `S01_mars1_deg` DEG(≥0.3 & FDR<0.05) == 3597 and `S01_deg_sepsis_vs_ctrl` == 448; (b) `S06_auc_compare` CV==0.659 & train==0.750 (3 dp); (c) `S01_mars1_deg` FIS1 logFC == 1.26; (d) `S08_l1000_rescue_trtcp` row count == 20413 and candidate ranks 5435/9152; (e) `07_hub_celltype` CD14 r == 0.773. This converts the audit from metadata+range to genuine headline coverage.

### Issue 3 — Residual "six hub genes" wording contradicts the FIS1-as-passenger reframing
- **【Problem】** Two sentences still call the 5+1 set "the six hub genes", implicitly counting FIS1 as a hub, contradicting the reframing that explicitly reports FIS1 as a co-expression passenger / non-immune gene, not a hub.
- **【Evidence】** `manuscript.md:64` (§2.8): "five of the **six hub genes** are themselves Mars1-down (FIS1 is Mars1-up…)"; `manuscript.md:155` (§3.10): "**Five of the six hub genes** carried ≥3 independent instruments … FCGR3A was not assessed". Both treat FIS1 as one of "six hub genes", whereas §3.3 / §6 / §7 (`manuscript.md:236`) define FIS1 as a non-immune co-expression passenger, not a hub.
- **【Why it matters】** Minor, but the dominant reframing (5 immune hubs + 1 passenger) is broken in the methods/MR sections; risks re-confusing "hub" vs "passenger" for a reader who trusts the abstract/§3.3 framing.
- **【Specific fix】** At lines 64 and 155 replace "the six hub genes" with "the six candidate genes (five immune hubs + FIS1)" (or "the six co-expression-linked genes", matching the abstract phrasing).

---

## Additional minor findings

- **A. I² "up to 0.50" vs true max 0.502.** `10_genetics_mr_outcome4982_criticalcare.csv` FIS1 IVW I² = 0.5018; assertion 1 tolerates ≤0.51 so it passes, but the prose "up to 0.50" (`manuscript.md:157`) understates the exact 0.502. Acceptable 2-dp rounding; flag only for precision.
- **B. References format spot-check (allowed — the reference list is inside `manuscript.md`).** Vancouver style is internally consistent: no "volume before a colon", no single-author "et al." (e.g. ref 30 Bo L, Wang F, Zhu J, Li J, Deng X — 5 authors, no et al.; ref 32 Giamarellos-Bourboulis EJ, Kotsaki A, Kotsamidi I, et al — 3 + et al.). MARS-consortium citations (Scicluna 2017 Lancet Respir Med 5(10):816–826; Davenport 2016 4(4):259–271) match the real papers. No impossible values found. (I did not re-verify DOIs via Crossref; the §3.8 `08b` notes claim Crossref verification on 2026-09-26.)
- **C. CD74 critical-care Egger** printed P = 0.088 (`manuscript.md:170,182`) matches the CSV t-dist value 0.0880 — consistent (unlike the primary-outcome Egger rows in Issue 1). No action.

---

## § Stands up (verified correct)

1. **23/22/21 consensus immune counts reproduce exactly.** `S01_immunoparalysis_direction.csv`: Mars1_down = 23, FDR<0.05 = 22 (LAG3 0.552, CD8B 0.110, GZMA 0.110 excluded), both = 21. Matches assertion 10 and the manuscript (§3.1, §7).
2. **Table-1 immune-gene logFC/adj.P all match source.** HLA-DRB1 −0.8925/−0.89, CD74 −0.7578/−0.76, CD14 underflow (≈0, P<1e-300, honestly disclosed), FCGR3A −0.6097/−0.61, HAVCR2 −0.3488/−0.35, ITGAM −0.2084/−0.21, HLA-DRA −0.4689/−0.47, LYZ −0.2561/−0.26 — all within rounding of `S01_immunoparalysis_direction.csv`.
3. **External AUC 0.638 (orientedSum) vs L1-locked 0.585 are correctly disambiguated.** `09_external_validation.csv`: `auc_EMTAB4451_orientedSum` = 0.6382 (assertion 13) and `auc_EMTAB4451_external_locked` = 0.5848 (assertion 17). The manuscript attributes 0.638 to the fixed-orientation score and 0.585 to the L1-locked sensitivity model (§3.5, §5) — no conflation.
4. **08b `rescue_fraction_directional` (1.0/0.833/0.714/0.667/0.4/0.4/0.2) is kept separate from Table-2 `response_gene_concordance` (0.80/0.667/0.571/0.667/0.4/0.4/0.2).** The manuscript never prints the 08b directional numbers as Table-2 values; §2.8 defines the Table-2 metric with the FDR-gated DEG rule, and §3.8 cites `08b` as a distinct supplementary table. No conflation found.
5. **Calibration/DCA figure is derived from the external cohort, not discovery.** `02_scripts/python/_ext_calibration_dca.py` reads `09_ext_risk_scores.csv` (E-MTAB-4451) and writes `09_ext_calibration_dca.csv` + `04_figures/S06_dca.png`. Reproduced: slope 0.5028 (stated 0.50), intercept −0.0382 (stated −0.04), NB@0.30 = 0.2844, NB@0.50 = 0.0755 — matches assertion 14.
6. **Phenotype and every §7 provenance path exist and counts match.** `GSE65682_pheno.csv` = 802 rows (sepsis 760 / healthy 42; Mars1 132, Mars2 176, Mars3 118, Mars4 53, unassigned 323; death 114/365/323). All 35 §7 file paths exist on disk (verified by existence scan).
7. **Hub cell-type correlations match source.** `07_hub_celltype.csv`: CD14 r = 0.773, FCGR3A 0.491, CD74→Dendritic 0.690, HAVCR2 0.298, HLA-DQA1→B-cell 0.681 — exactly the values quoted in §3.6. `07_axis_celltype.csv` CD4 0.6176 / CD8 0.5822 / Dendritic 0.4587 matches "0.62/0.58/0.46".
8. **`wtcs = rescue × √22` identity holds.** lenalidomide 0.0439 × 4.690 = 0.206 ≈ 0.2058; azithromycin 0.0133 × 4.690 = 0.0624 ≈ 0.0626 — consistent with §3.9's "algebraically identical" claim.
9. **L1000 positive-control and library size match.** `S08_l1000_rescue_trtcp.csv` = 20,413 rows; `S08_l1000_positive_control.csv`: prednisone rank 651 (rescue 0.1364), dexamethasone rank 6808 (rescue 0.0315) — matches §3.9 ("prednisone 0.136, rank 651/20,413; dexamethasone 0.032, rank 6,808"). `08_positive_control_check.csv` confirms IFN-γ rescues 4/5 antigen-presentation genes.
10. **MR Table 4 (IVW across 3 outcomes) and median-F / instrument counts match CSVs.** All 15 IVW OR/CI/p and I² values in Table 4 reproduce from `10_genetics_mr.csv` + `10_genetics_mr_outcome4982_criticalcare.csv` + `10_genetics_mr_outcome5086_28ddeath.csv`. Harmonised instrument counts 3/4/6/6/8 = 27 (FCGR3A excluded) and median F 35.4/168.1/45.7/36.4/75.0 from `10_genetics_mr_outcome5086_harmonised.csv` all match.

---

## § Questions for the authors

1. Which distribution did you intend for the Table 3 MR-Egger p-values — normal or t? The committed CSVs are t-distribution; please confirm Table 3 should be regenerated from `10_genetics_mr_outcome5086_28ddeath.csv` (Issue 1).
2. The raw large inputs (`GSE65682_expr.csv`, `E-MTAB-4451/*`, `LINCS GSE92742_Level5_COMPZ.gctx`) exist on this working copy, but the Data-availability section says they are "mirrored per DATA_SOURCES.md … excluded from the repository only for size." Confirm the deposited public repo will actually mirror (not drop) these so §7 paths resolve for readers.
3. Confirm the Table 3 median-F values are taken from the *primary-outcome* harmonised file (`10_genetics_mr_outcome5086_harmonised.csv`), since F differs by outcome (e.g. FIS1 critical-care F would differ from primary).

---

## § What I actually checked

**Files read:** `05_reports/manuscript.md` (full), `02_scripts/python/check_audit_assertions.py`, `_ext_calibration_dca.py`, `_recompute_table2.py`; all CSVs under `03_results/` (S01/S05/S06/S08*/09*/10*); `01_data/GSE65682/GSE65682_pheno.csv`; `05_reports/review_r9/_PANEL_BRIEF.md`. (Did NOT open any forbidden file: REVIEW_round*, review_r2–r8, RESPONSE/REVISION, A1/A2/A4 reviews, generated_references.md, journal_targeting.csv, reference_doi_audit.csv, author_verification_statement.md.)

**Commands run:**
- `python 02_scripts/python/check_audit_assertions.py` → **EXIT=0**. Quoted output:
  - `OK  max I2 across 15 MR tests = 0.502 (stated <= 0.50)`
  - `OK  MR family size = 45 (5 genes x 3 estimators x 3 outcomes); I2 computed for 15 IVW tests`
  - `OK  9 §7 provenance paths present`
  - `OK  15 MR-Egger p-values match t(df=n-2) distribution (normal-based values differ, as required)`
  - `OK  no MR p/q value is exactly 0.0 or < 1e-300`
  - `OK  Egger SE not substantially (<95%) below IVW SE; CD74 critical-care exempted (disclosed)`
  - `OK  hub directions consistent with text: 5 Mars1-down hubs + FIS1 up (logFC +1.26)`
  - `OK  Mars1 vs Mars2 Mann-Whitney P = 4.671e-01 (text 4.700e-01)`; `Mars1 vs Mars3 P = 1.852e-18 (text 1.900e-18)`; `Mars1 vs Mars4 P = 1.321e-03 (text 1.300e-03)`
  - `OK  OR/CI algebraically consistent with beta/se across all MR rows`
  - `OK  consensus immune counts = 23/22/21 (down / FDR / both)`
  - `OK  Table-1 immune-gene logFC + adj.P match S01`
  - `OK  Table-2 response_gene_concordance matches 08_candidates_drugs.csv`
  - `OK  external validation AUC=0.638 (95% CI 0.532-0.748), n=106, 52 deaths`
  - `OK  calibration slope=0.50/intercept=-0.04, AUC=0.638, NB@0.30=0.284/NB@0.50=0.076`
  - `OK  forest significance flag real: 1 family-significant test(s); CD74 crit-care WM flagged`
  - `OK  primary-outcome minimum IVW P = 0.236 (manuscript states >= 0.23)`
  - `OK  L1-locked external AUC = 0.585 (distinct from oriented-sum 0.638)`
  - `All Round-6 + Round-7 (hardened) audit assertions passed.`

**Recomputed vs manuscript (discrepancies flagged):**
- FIS1 logFC = 1.2614 → manuscript +1.26 ✓ (direction-checked by audit, exact value not asserted).
- Mars1 DEG = 3597; sepsis-vs-healthy = 448 → match manuscript, but **unguarded by audit** (Issue 2).
- S06 CV = 0.6586 → 0.659 ✓; train = 0.7495 → 0.750 ✓ (unguarded).
- L1000 rescue_trtcp = 20,413 rows; lenalidomide rank 5435 (rescue 0.0439), azithromycin 9152 (rescue 0.0133) → match §3.9 (unguarded).
- L1000 positive control: prednisone 651 (0.1364), dexamethasone 6808 (0.0315) → match §3.9.
- **Egger p normal-vs-t-dist for the 5 primary-outcome rows:** CD74 t 0.879 / normal 0.848 → printed 0.85 (normal); HLA-DQA1 t 0.558 / normal 0.486 → printed 0.49 (normal); CD14 t 0.0488 → printed 0.049 (t); HAVCR2 t 0.955 → printed 0.95 (ambiguous); FIS1 t 0.491 / normal 0.463 → printed 0.46 (normal). **3 of 5 rows printed the normal value** (Issue 1).
- Table 3/4 IVW OR/CI/I² and median-F (35.4/168.1/45.7/36.4/75.0) and instrument counts (3/4/6/6/8=27) → all match CSVs.
- Pheno: 802 / 760 / 42; Mars1 132; death 114/365/323 → match §2.1/§7.
- All 35 §7 provenance paths exist on disk.
- References (inside manuscript): format clean, no volume-before-colon or single-author "et al."

**Summary of discrepancies:** only one true manuscript↔CSV mismatch (Issue 1, Egger p distribution); one coverage gap (Issue 2); one wording inconsistency (Issue 3); one acceptable rounding note (I² 0.502 vs "0.50"). Everything else verified.
