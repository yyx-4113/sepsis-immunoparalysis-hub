# A3 — Implementation / provenance-recompute review (independent blind panel, Round 13)

**Reviewer role:** A3 — Implementation / provenance-recompute auditor.
**Manuscript:** `05_reports/manuscript.md` (tag `v1.13.0`).
**Mandate:** Treat the manuscript as a first submission; recompute/verify every headline number against the deposited source CSVs and scripts; do not trust any stated claim. I did not open any prior-round review, response, or revision file, nor the prior submission-checklist or memory.

## Headline-number verification ledger

For each headline quantity the manuscript reports, the table gives the manuscript value, the value I read/computed from the source, and whether they match. File:line pins every source.

| # | Manuscript claim | Source file:value I read | Match? |
|---|---|---|---|
| 1 | External AUC 0.638 (95% CI 0.532–0.748), n=106, 52 deaths | `09_external_validation.csv:11` orientedSum=0.6382; `:12-13` CI 0.5317–0.7475; `:4-5` n=106, deaths=52 | ✅ exact (rounds to stated) |
| 2 | L1-locked external AUC 0.585 (95% CI 0.469–0.696) | `09_external_validation.csv:8`=0.5848; `:9-10` CI 0.4687–0.6959 | ✅ exact |
| 3 | L1 set 7 zero-coef genes: CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B | `09_external_validation_coef.json:6,7,14,15,21,24,31` all `0.0`; no other gene is `0.0` (FCGR3A=0.00166) | ✅ exact |
| 4 | HLA-DQA1 absent from external array | `09_external_validation.csv:17` `genes_missing_in_test=HLA-DQA1`; coef `genes` list has 29 entries, no DQA1 | ✅ exact |
| 5 | IRG-3 proxy recomputed 0.529 | `09_external_validation.csv:14` `auc_IRG3_benchmark_EMTAB4451=0.5288` | ✅ exact (rounds to 0.529) |
| 6 | Peng et al. IRG benchmark 0.619 on E-MTAB-4451 | `S06_auc_compare.csv:5` `IRG 基准(E-MTAB-4451)=0.619` | ✅ (literature value, stored) |
| 7 | Calibration slope 0.50 / intercept −0.04 | `09_ext_calibration_dca.csv:2` slope=0.5028, intercept=−0.0382 | ✅ exact point estimates |
| 8 | Calibration slope **95% CI 0.11–0.95** | Not present in `09_ext_calibration_dca.csv` (point estimate only) nor produced by `_ext_calibration_dca.py` | ❌ **untraceable — provenance gap** |
| 9 | Mars1 vs Mars2/3/4 Mann–Whitney P = 0.47 / 1.9e-18 / 1.3e-3 | Recomputed from `S02_immunoparalysis_score.csv`: 0.467 / 1.85e-18 / 1.32e-3 (audit #8 identical) | ✅ within rounding |
| 10 | Mars1/Mars2/Mars3/Mars4 medians −0.792/−0.752/0.641/−0.235 | Recomputed: −0.792/−0.752/0.640/−0.235 (Mars3 0.640 vs 0.641) | ✅ rounding-level |
| 11 | 5 Mars1-down hubs + FIS1 up (logFC +1.26, t=+17.2) | `S01_mars1_deg.csv` FIS1 logFC=1.2614, t=17.16; `S01_immunoparalysis_direction.csv` CD74/HLA-DQA1/CD14/FCGR3A/HAVCR2 all `Mars1_down`; audit #7 | ✅ exact |
| 12 | MR primary (28-day death) IVW OR 0.92–1.12, P ≥ 0.23 | `10_genetics_mr_outcome5086_28ddeath.csv` IVW OR 0.923–1.119, P 0.236–0.848; min P=0.2359 (audit #16) | ✅ exact |
| 13 | 27 retained instruments (CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8; FCGR3A excluded) | nsnp in `10_genetics_mr_outcome5086_28ddeath.csv` / `10_genetics_mr.csv`: 3+4+6+6+8 = 27; FCGR3A nsnp=2 (insufficient) | ✅ exact |
| 14 | Consensus immune counts 23 down / 22 FDR<0.05 / 21 both | `S01_immunoparalysis_direction.csv`: 23 `Mars1_down`, 22 `adj.P.Val<0.05`, 21 both (audit #10) | ✅ exact |
| 15 | L1000 rescue ranks: lenalidomide 5435, azithromycin 9152 | `S08_l1000_candidate_scores.csv:3` 5435; `:2` 9152; pct-rank 0.266 / 0.448 | ✅ exact |
| 16 | Tag v1.13.0 in manuscript + cover letter; no v1.12.0/v1.11.0 leftovers | manuscript line 263 (+1) and cover_letter line 24 = v1.13.0; zero `v1.12.0`/`v1.11.0` in either file | ✅ exact |
| 17 | Audit gate runs 29 assertions and passes | `02_scripts/python/check_audit_assertions.py` executed: 29 OK lines, exit code 0 | ✅ exact |
| 18 | 37 references all carry real DOIs (spot-checked [32],[16],[4],[5]) | DOI resolver: [32]=10.1001/jama.2025.24175 → ImmunoSep RCT (JAMA); [16]=10.3389/fimmu.2023.1152117 → Peng Front Immunol 14:1152117; [4]=10.1016/S2213-2600(17)30294-1 → Scicluna Lancet Resp Med 2017; [5]=10.1016/s2213-2600(16)00046-1 → Davenport Lancet Resp Med 2016 | ✅ all resolve to correct papers |

**Bottom line of the ledger:** 16/18 headline checks match the source exactly or within rounding. The only true failures are #8 (calibration-slope CI untraceable) and a table-syntax defect (Finding 2 below). One minor cross-file inconsistency (#1 vs `S06_auc_compare.csv`) is noted under Minor notes.

---

## Findings (four-part items)

### Finding 1 — Calibration-slope 95% CI (0.11–0.95) is not reproducible from any deposited artifact

【Problem】 The 95% confidence interval quoted for the external calibration slope (0.11–0.95) cannot be regenerated from the deposited result CSV or the deposited analysis script.

【Evidence】 `03_results/09_ext_calibration_dca.csv:2` stores only `calib_slope=0.5028` and `calib_intercept=-0.0382` (point estimates) — no slope CI column. The producing script `02_scripts/python/_ext_calibration_dca.py` fits a single logistic model `logit(p)=a+b·z` by BFGS (`_ext_calibration_dca.py:22-30`) and never bootstraps, never derives a standard error for `b`, and writes only the point estimate to CSV (`:102-109`). The §7 provenance table maps "External-cohort calibration slope 0.50 / intercept −0.04" to `09_ext_calibration_dca.csv`, but the CI is absent from that file. So the number 0.11–0.95 has no traceable origin in the repository.

【Why it matters】 This manuscript's entire premise (Article type = methods-and-resources; "every reported number traces to a concrete output", manuscript §7) is auditable provenance. An untraceable CI is precisely the failure class the study exists to preclude. The point estimate 0.50 is the load-bearing claim (under-fitting relative to ideal 1.0) and is fully sourced; the CI only softens it — but a reviewer or reader cannot regenerate, defend, or challenge a number that nowhere exists in the deposited pipeline. It also invites the suspicion that the CI was hand-computed elsewhere and not version-controlled.

【Specific fix】 Pick one of:
- (a) Add a bootstrap to `_ext_calibration_dca.py` (e.g., 2,000 resamples of the logistic calibration fit on the 106 E-MTAB-4451 samples), write `calib_slope_CI95_low` / `calib_slope_CI95_high` to `09_ext_calibration_dca.csv`, and cite that column in §3.5 / §7; or
- (b) Drop the CI from the text and report only "slope 0.50 (point estimate; under-fits relative to ideal 1.0)", so the prose matches what the repository can regenerate. Either way the §7 provenance line must name the exact source of every digit it quotes.

### Finding 2 — Table 1 contains an unescaped vertical bar that breaks Markdown table parsing

【Problem】 The ITGAM row of Table 1 (§3.1) embeds a literal `|logFC|` inside a cell, introducing extra pipe characters and corrupting the table under strict Markdown renderers.

【Evidence】 `05_reports/manuscript.md:82` reads: `| ITGAM | −0.21 | 1.7e-03 | integrin αM (significant at FDR<0.05, adj.P=1.7×10⁻³, but below the |logFC|≥0.3 DEG fold-change threshold, DEG_0.3=False) |`. The cell text `|logFC|≥0.3` contributes two unescaped pipes, so the row has 7 pipe characters versus the 5-pipe header (`:76`) and the 5-pipe sibling rows (`:83` HAVCR2, `:84` HLA-DRA, …). A line-aware cell-count lint flags exactly rows 82/83 as inconsistent (row 82 = 7 pipes, header = 5); the break originates at the embedded `|`.

【Why it matters】 Scientific Reports renders tables from the submitted Markdown/XML. A row with a stray pipe is parsed by CommonMark/GitHub as extra columns; downstream of ITGAM the table mis-aligns or the ITGAM line is dropped, and any automated table extraction (and the audit's own "every number traces to a file" ethos) fails on that row. It is a concrete, fixable defect, not cosmetic.

【Specific fix】 Escape or rephrase the bar, e.g. change `below the |logFC|≥0.3 DEG fold-change threshold` to `below the \|logFC\|≥0.3 DEG fold-change threshold` (escaped), or simply `below the logFC≥0.3 threshold`. Then re-lint the manuscript so every `|`-delimited row has exactly 5 pipes. (A one-line table-lint check, or the existing audit script, can guard this against re-introduction.)

---

## Minor notes (not four-part; discrepancies stated, no action strictly required)

- **CV AUC cross-file inconsistency (0.0004).** `09_external_validation.csv:7` `auc_GSE65682_CV_locked=0.6582` whereas `S06_auc_compare.csv:2` `Immune-risk signature (CV)=0.6586`. Both round to the reported 0.659, so the manuscript text is correct, but the same quantity is stored with two slightly different values in two result files. Recommend one authoritative source (or a comment in the CSV noting they are the same metric recomputed in two scripts) to keep the "single source of truth" promise. Not a manuscript-vs-source error.
- **Mars1 vs Mars3 P rounding.** Recomputed 1.85e-18 vs text 1.9e-18 (2.6% relative); Mars1 vs Mars4 1.32e-3 vs 1.3e-3. Both within normal rounding; no change needed. The audit gate (#8) tolerates ±10% on small P and passes.
- **Mars3 median.** Recomputed 0.640 vs text 0.641 (difference 0.001, even-n interpolation). Negligible.
- **DCA is genuinely on calibration-corrected probabilities.** The DCA script (`_ext_calibration_dca.py:31,67-72`) computes net benefit from `p = logistic(a+b·z)` with a=−0.04, b=0.50, i.e. the calibration-corrected probabilities. This matches the manuscript's §3.5 wording and the audit #26 guard. No discrepancy.

---

## § Stands up (claims I suspected were wrong but found correct)

1. **External validation numbers are exactly sourced.** I expected at least one of AUC/CI/n/deaths to have drifted from rounding, but `09_external_validation.csv` gives 0.6382 / 0.5317–0.7475 / 106 / 52, matching the text to the third decimal. The honest-external-validation centerpiece is real.
2. **The L1 zero-coefficient list is precise.** All seven genes the manuscript names as zero (CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B) are exactly `0.0` in `09_external_validation_coef.json`, no others are zero, and HLA-DQA1 is correctly absent. The §3.4 prose about the coefficient structure is faithful, not hand-waved.
3. **The audit gate is real, not aspirational.** `check_audit_assertions.py` actually runs and prints 29 OK lines with exit code 0, including re-derivation of the Mars1 Mann–Whitney Ps, the 23/22/21 consensus counts, the OR/CI algebra, the IRG-3 0.5288, and the L1000 ranks. The reproducibility claim is substantiated by code, not assertion.
4. **MR primary-outcome framing is accurate.** IVW ORs span 0.923–1.119 (→ "0.92–1.12") and the minimum IVW P is 0.236 (≥0.23); the 27-instrument total sums exactly from per-gene nsnp. The "no primary IVW significance" claim is correctly bounded.
5. **L1000 candidate ranks are exact.** lenalidomide 5435 / azithromycin 9152 read verbatim from `S08_l1000_candidate_scores.csv`, with pct-rank 0.266 / 0.448 matching the "top 26.6%" / "≈ median" prose.
6. **Load-bearing reference DOIs resolve to the correct papers.** [32] (ImmunoSep/JAMA), [16] (Peng/Front Immunol), [4] (Scicluna/Lancet Resp Med), [5] (Davenport/Lancet Resp Med) all resolve via their DOIs to the cited articles, with correct volume/pages where stated. No fabricated or mismatched DOI in the sampled set.
7. **Version labels are consistent.** Both manuscript and cover letter say `v1.13.0`; grep finds zero `v1.12.0` or `v1.11.0` leftovers in either file. The stale-version-string risk the brief flagged does not materialise.

---

## § Questions for the authors

1. **Calibration-slope CI provenance.** Where does 0.11–0.95 come from? Can you add the bootstrap (or drop the CI) so §3.5/§7 are regenerable? (See Finding 1.)
2. **Single source of truth for CV AUC.** `09_external_validation.csv` (0.6582) and `S06_auc_compare.csv` (0.6586) disagree by 0.0004 for the same metric — which is authoritative, and should the other be annotated?
3. **Full DOI batch resolution.** I verified 4 of 37 DOIs (the load-bearing ones) resolve correctly. Have you run a complete 37-DOI automated resolution (e.g., against Crossref/doi.org) to catch any that do not resolve? I recommend it as a pre-acceptance check, even though the sampled set is clean.
4. **Mars1-vs-Mars3 P.** My recompute is 1.85e-18 vs your 1.9e-18. Is 1.9e-18 from a different tie-handling in `scipy`/`mannwhitneyu`? Purely rounding, but worth confirming the exact call so the audit's tolerance band is the intended one.
5. **FCGR3A exclusion robustness.** You state FCGR3A has only two usable eQTLGen variants even at relaxed thresholds. Could you show the relaxed-threshold query results in a supplementary line so the "excluded for insufficient instruments" statement is itself auditable?

---

## § What I actually checked

**Files read (full unless noted):**
- `05_reports/manuscript.md` — full read (all sections, tables, 37 references).
- `03_results/09_external_validation.csv` — external AUC/CI/n/deaths, L1-locked AUC, IRG-3 proxy, missing gene (items 1,2,5,15-source).
- `03_results/09_external_validation_coef.json` — L1 coefficients; verified the 7 zero-coef genes and HLA-DQA1 absence (item 3,4).
- `03_results/09_ext_calibration_dca.csv` — calibration slope/intercept point estimates + DCA net benefit (item 7; absence of slope CI → Finding 1).
- `02_scripts/python/_ext_calibration_dca.py` — full read; confirmed slope CI is never computed (Finding 1 evidence).
- `03_results/S02_immunoparalysis_score.csv` — full 804-row read; basis for Mann–Whitney recompute and medians (items 9,10).
- `03_results/S01_immunoparalysis_direction.csv` — 25 consensus immune genes; direction + adj.P.Val; basis for 23/22/21 (item 14) and hub-direction cross-check (item 11).
- `03_results/S01_mars1_deg.csv` — grepped FIS1 row → logFC 1.2614, t 17.16 (item 11).
- `03_results/S06_auc_compare.csv` — CV/train AUC, Peng IRG 0.619/0.648 (items 6, minor CV note).
- `03_results/10_genetics_mr.csv` — susceptibility outcome; nsnp/or/p per gene (item 13).
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv` — primary 28-day-death outcome; IVW OR/P range and minimum P (item 12).
- `03_results/10_mr_bh_family.csv` — 45-test family BH; confirmed one family-significant row (CD74 crit-care WM) and others not (cross-check of MR layer).
- `03_results/S08_l1000_candidate_scores.csv` — lenalidomide/azithromycin rescue_rank (item 15).
- `05_reports/cover_letter.md` — full read; confirmed v1.13.0, AUC 0.638 framing, no hub-discovery claim (item 16).
- `02_scripts/python/check_audit_assertions.py` — full read (29 assertions) and executed (item 17).

**External reference resolution (DOI resolver):**
- [32] 10.1001/jama.2025.24175 → ImmunoSep RCT, Giamarellos-Bourboulis, JAMA (online Dec 2025; vol 335 per text).
- [16] 10.3389/fimmu.2023.1152117 → Peng et al., Front. Immunol. 14:1152117 (2023).
- [4] 10.1016/S2213-2600(17)30294-1 → Scicluna et al., Lancet Resp Med 5, 816–826 (2017).
- [5] 10.1016/s2213-2600(16)00046-1 → Davenport et al., Lancet Resp Med 4, 259–271 (2016).
All four resolve to the correct articles (item 18).

**Computations I ran (values recomputed vs manuscript, discrepancies stated):**
1. Executed the audit gate: 29 assertions, all OK, exit code 0. This re-derived externally: Mars1 Mann–Whitney Ps (0.467 / 1.85e-18 / 1.32e-3) — matches text within rounding; consensus counts 23/22/21 — exact; OR/CI algebra across all MR rows — consistent; IRG-3 0.5288 — exact; L1000 ranks 5435/9152 — exact; external AUC 0.638/CI/106/52 — exact; calibration 0.50/−0.04 — exact; primary-min IVW P 0.236 ≥ 0.23 — exact; L1-locked 0.585 — exact; Table-3 Egger P matches t-dist CSV — exact; Reference [32] carries 335/775/10.1001/jama.2025.24175 — exact.
2. Independent Mann–Whitney recompute from `S02_immunoparalysis_score.csv` (separate from the audit script): Mars1 vs Mars2 P=0.467, vs Mars3 P=1.85e-18, vs Mars4 P=1.32e-3; medians −0.792 / −0.752 / 0.640 / −0.235. Discrepancy vs text: Mars3 P 1.85e-18 vs 1.9e-18 (rounding, 2.6%), Mars3 median 0.640 vs 0.641 (0.001) — both immaterial.
3. Independent consensus-count recompute from `S01_immunoparalysis_direction.csv`: 23 `Mars1_down`, 22 `adj.P.Val<0.05`, 21 both — exact match to text and audit.
4. Independent MR primary-outcome scan from `10_genetics_mr_outcome5086_28ddeath.csv`: IVW OR min 0.923, max 1.119 (→ "0.92–1.12"); min IVW P 0.2359 (≥0.23) — exact.
5. Instrument tally: 3+4+6+6+8 = 27; FCGR3A = 2 (insufficient) — exact.
6. Table-syntax lint + reference/DOI count + version-string grep on `manuscript.md` and `cover_letter.md`: found the ITGAM unescaped-pipe defect (Finding 2); 37 references, 37 DOIs, none missing; v1.13.0 present in both, zero v1.12.0/v1.11.0.

**Discrepancies stated explicitly:**
- **Finding 1 (real):** calibration-slope 95% CI 0.11–0.95 is not present in `09_ext_calibration_dca.csv` and is not produced by `_ext_calibration_dca.py` — untraceable provenance.
- **Finding 2 (real):** Table 1 ITGAM row (`manuscript.md:82`) has an unescaped `|logFC|` that breaks Markdown table parsing (7 pipes vs 5-pipe header).
- **Minor (immaterial):** CV AUC 0.6582 (`09_external_validation.csv`) vs 0.6586 (`S06_auc_compare.csv`) — cross-file 0.0004, both round to reported 0.659.
- **Rounding-only:** Mars1-vs-Mars3 P 1.85e-18 vs 1.9e-18; Mars3 median 0.640 vs 0.641 — no manuscript change required.

**Everything else matched exactly** (items 1–7, 11–17, 18). No headline number in the manuscript contradicts its cited source file, apart from the two findings above.
