# A3 — Implementation & Provenance Review (计算可复现性 / 数字溯源 / 数据谱系审计)

**Reviewer role:** independent computational-reproducibility / digital-provenance / data-lineage auditor
**Manuscript:** `05_reports/manuscript.md` (single-author bioinformatics; sepsis immunoparalysis Mars1 multi-omics + in-silico drug repurposing)
**Scope:** I re-ran the audit gate, then independently recomputed every headline number from the source CSVs with my own Python (pandas/scipy). I did not read any prior review, RESPONSE, review_r7, .workbuddy, or the submission manifest. All numbers below are values I derived myself, then compared to the manuscript.

---

## 1. Audit gate `check_audit_assertions.py` — does it pass, and does it actually catch errors?

**Result:** the script exits `0` ("All Round-6 + Round-7 (hardened) audit assertions passed."). I confirm the green run. It is **not a silent no-op**: the numeric stack (pandas/scipy) is imported with a hard `sys.exit(2)` if missing (lines 82–90), so an unconfigured CI cannot fake a pass.

However, on a focused reading of the 15 assertions, **the gate is strong on the MR-Egger p-value fix but has several slack points and scope limits that would let a wrong headline value through without failing.** Details below (issues A1–A6). Summary of the 15 assertions' real protective power:

| # | Assertion (script line) | Catches real error? | Gap |
|---|---|---|---|
| 1 | I² ≤ 0.50 (43–45) | Partial | tolerance 0.51; only global max, not the specific FIS1 claim |
| 2 | family size = 45 (50–58) | Yes | — |
| 3 | §7 paths exist (61–75) | Yes (metadata) | metadata only, not values |
| 4 | **Egger p = t(df=n−2)** (92–124) | **Yes, strong** | also forbids normal-based value; best assertion |
| 5 | no MR p/q = 0.0 or <1e-300 (126–145) | Yes (MR only) | DEG tables not scanned |
| 6 | Egger SE not ≪ IVW SE (147–176) | Partial | CD74-critcare exempted entirely |
| 7 | hub direction vs S01 (178–190) | Yes | hardcoded hub list, not S05 |
| 8 | Mann–Whitney P vs S02 (192–207) | Yes | loose tolerance |
| 9 | OR/CI = exp(beta±1.96·se) (215–233) | Yes | does **not** re-derive IVW/WM p |
| 10 | 23/22/21 immune counts (235–242) | Yes | — |
| 11 | Table-1 logFC/adj.P (244–256) | Yes | CD14 adj.P exempt (underflow) |
| 12 | Table-2 concordance (258–270) | Yes | — |
| 13 | external AUC/CI/n (272–287) | Yes | L1 0.585 **not** asserted |
| 14 | calibration slope/intercept/NB (289–298) | Yes | — |
| 15 | forest flag real (300–311) | Yes (CSV) | does **not** verify the PNG |

---

## 2. Issues (four-element format)

### A1 — Audit assertion #1 (I²) has a tolerance wider than the stated value and only checks the global max
【问题】 The I² guard (`check_audit_assertions.py:43`) fails only if `max_i2 > 0.51`, but the manuscript states heterogeneity reaches "up to **0.50**" (manuscript.md:157, 184). A value of 0.509 would still pass the gate while contradicting the text; the gate also never checks the specific claim that *FIS1 critical-care* I² ≈ 0.50.
【证据】 My recomputation: maximum I² across the three MR CSVs = **0.5018** (`10_genetics_mr_outcome4982_criticalcare.csv`, FIS1 IVW). 0.5018 rounds to 0.50 at 2 d.p., so the text is *currently* honest, but the gate's 0.51 ceiling is 0.01 looser than the number it is meant to protect.
【为何重要】 A CI/repro-gate whose tolerance exceeds the reported figure can mask a real drift (e.g., a future edit producing I²=0.51) and still print "OK". It also does not anchor to the specific gene/outcome the prose names.
【具体修改】 Tighten to the stated precision and assert the specific cell:
```python
# line 43-45
if max_i2 > 0.505 + 1e-9:
    fail("max I2 = %.3f exceeds stated <=0.50" % max_i2)
# add: assert FIS1 critical-care IVW I2 within rounding of 0.50
fis1_cc = ... # row gene==FIS1, method==IVW, outcome contains critcare
assert abs(float(fis1_cc["I2"]) - 0.50) <= 0.01
```

### A2 — Audit does NOT re-derive IVW / Weighted-median p-values (only Egger); mitigated but unguarded
【问题】 The gate re-derives MR-Egger p from t(df=n−2) (assertion 4) and checks OR/CI internal consistency (assertion 9), but it never independently recomputes the **IVW** or **Weighted-median** p-values. The manuscript's central negative claim — "no primary IVW estimate reached significance" — rests entirely on IVW p-values that the gate does not verify.
【证据】 I added my own Wald check: for all IVW and Weighted-median rows across the three MR CSVs, `p_wald = 2·(1−Φ(|beta|/se))` matched the stored `p` with **0 mismatches** (tolerance 1e-6). So the values are currently consistent — but the *audit gate itself* would not catch a hand-edited IVW p.
【为何重要】 The most-cited result of §3.10 (no significant primary IVW) is the one quantity the gate cannot defend. A regression there would print green.
【具体修改】 Add to the gate:
```python
for r in all_ivw_wm_rows:
    p_wald = 2*(1-scipy.stats.norm.cdf(abs(float(r['beta']))/float(r['se'])))
    if abs(p_wald - float(r['p'])) > 1e-6:
        fail("IVW/WM p mismatch for %s/%s" % (r['gene'], outcome))
```

### A3 — Audit assertion #6 (Egger SE) exempts the exact cell the manuscript flags as suspicious
【问题】 The Egger-SE guard (`check_audit_assertions.py:152`) hardcodes `EXEMPT_EGGER_SE = {("CD74","criticalcare")}` and tolerates Egger SE down to 95% of IVW SE. The exempted CD74 critical-care cell has Egger SE 0.111 vs IVW SE 0.325 (ratio 0.34) — the precise "physically implausible ordering" the manuscript itself warns about (manuscript.md:182). The guard therefore provides **zero protection for the one cell it should be most suspicious of**.
【证据】 Recomputed from `10_genetics_mr_outcome4982_criticalcare.csv`: CD74 IVW se=0.3250, Egger se=0.1111 (ratio 0.342). The exemption (line 152) plus 95% tolerance means any *new* gene with Egger SE < 95% of IVW SE is caught, but the disclosed anomaly is carved out.
【为何重要】 The exemption is defensible because the anomaly is disclosed in text, but the guard gives a false sense of coverage: a reviewer reading "Egger SE not substantially below IVW SE" might assume the CD74 case is also bounded, when it is not.
【具体修改】 Keep the exemption but make it auditable: assert the exempted cell's SE ratio is *recorded* (not silently skipped), e.g. print the ratio and require it to be ≥ the disclosed 0.34; and add a comment in the gate noting the exemption is a known disclosure, not a clean pass.

### A4 — Audit assertion #7 reads a hardcoded hub list instead of the authoritative `S05_hub_genes.csv`
【问题】 Hub-direction check (`check_audit_assertions.py:181`) hardcodes `HUBS = ["CD74","HLA-DQA1","CD14","FCGR3A","HAVCR2","FIS1"]`. If the consensus output `S05_hub_genes.csv` changed (a hub dropped/added), the gate would still assert the old list and would not notice the divergence between prose and the actual consensus file.
【证据】 `S05_hub_genes.csv` does contain exactly those 6 genes (verified: 6 rows, all three methods True), so it currently matches — but the gate is coupled to a literal list, not to the source of truth.
【为何重要】 The hub set is the paper's central object; a gate that trusts a hardcoded list cannot detect drift between `S05` and the manuscript.
【具体修改】
```python
HUBS = list(pd.read_csv(os.path.join(RESULTS,"S05_hub_genes.csv"))["gene"])
```

### A5 — Audit assertion #13 does not assert the L1-locked external AUC 0.585 (cited in §3.5/§7)
【问题】 The external-validation assertion (`check_audit_assertions.py:272–287`) checks only the fixed-orientation `orientedSum` AUC 0.638 and its CI/n/deaths. The locked-L1-weight sensitivity AUC **0.585** (manuscript.md:120, 235; `09_external_validation.csv` `auc_EMTAB4451_external_locked` = 0.5848) is never asserted.
【证据】 My recomputation: `auc_EMTAB4451_external_locked` = 0.5848 (≈0.585, CI 0.4687–0.6959). Correct, but ungated.
【为何重要】 The 0.585 vs 0.638 gap is the basis for the "gene set + orientation, not learned weights, are portable" conclusion (manuscript.md:120). An unguarded number underpinning a key interpretation claim is a provenance hole.
【具体修改】 Extend assertion 13:
```python
if abs(ext["auc_EMTAB4451_external_locked"] - 0.585) > 1e-3:
    fail("locked-L1 external AUC mismatch")
```

### A6 — Forest significance is verified at the CSV level, not at the figure (PNG) level
【问题】 Assertion #15 (`check_audit_assertions.py:300–311`) confirms the family table has exactly one `family_sig_q<0.05 = YES` (CD74 critical-care Weighted median) and that the CSV flag is real. It does **not** verify `04_figures/mr_forest.png` actually draws that point red. A stale or hand-edited figure would still pass the gate.
【证据】 I read the generator `02_scripts/python/_mr_diagnostics.py:49–93`: the plot *does* read `family_sig_q<0.05` from `10_mr_bh_family.csv` to color points (`siglist`, line 81/87), so re-running reproduces the single red point. `mr_forest.png` mtime (2026-09-27 08:12) is newer than the CSV (06:46), consistent with regeneration. **But** a reviewer cannot pixel-verify the PNG, and the script hardcodes an absolute `PROJ` path (line 14), so it is not portable.
【为何重要】 The "only CD74 critical-care WM is red" claim is the visual centerpiece of §3.10; the gate proves the data supports it but not that the artifact reflects the data.
【具体修改】 (a) Add a programmatic PNG sanity check (e.g., assert the figure embeds the expected number of red pixels / or regenerate in CI and diff), or (b) at minimum state in §3.10 that the figure is generated deterministically from `10_mr_bh_family.csv` via `02_scripts/python/_mr_diagnostics.py`, and replace the absolute `PROJ` path with `os.path.dirname(...)` for portability.

### A7 — Data-availability statement is literally false as written: processed matrices are NOT in the committed repository
【问题】 The Data availability section (manuscript.md:254) states "Processed expression and phenotype matrices, and all result tables, are available in the project's versioned reproducibility repository." But `01_data/` (which holds `GSE65682_expr.csv`, `GSE65682_pheno.csv`, `E-MTAB-4451/...`, `LINCS/...` — the very files the §7 provenance table cites) is **gitignored and untracked**: `git ls-files 01_data` → 0 files. Only `03_results/` (45 files), `04_figures/` (12), `02_scripts/` (53) are tracked.
【证据】 `.gitignore` explicitly excludes `01_data/` ("Intentionally kept OUT of git history"). `git ls-files 01_data | wc -l` = 0. The §7 table (manuscript.md:226, 237, 245) points the "802 samples / GPL13667" and "E-MTAB-4451 data" and "L1000 main library" claims at `01_data/...` paths that will **not** exist in the deposited repo.
【为何重要】 A reproducibility reviewer cloning the repo cannot obtain the processed matrices; the headline sample count (802) and the 760/42 split are therefore not independently re-derivable from the deposited artifact. The statement overclaims what the repo contains.
【具体修改】 Either (a) commit a slim processed phenotype/expression matrix (or at least `GSE65682_pheno.csv` and the expression matrix) so the provenance paths resolve, or (b) rewrite the sentence to match reality:
> "Processed expression and phenotype matrices are regenerated by the provided download and processing scripts (`02_scripts/python/00_geo_download.py` and the GSE65682 processing step) from public GEO GSE65682 (GPL13667) and ArrayExpress E-MTAB-4451 (GPL10558) inputs; **the raw and intermediate matrices are not committed** (see `.gitignore`) and the result tables, figures, and scripts are versioned in this repository."

### A8 — The 760-sepsis / 42-ctrl split is not verifiable from the committed repository
【问题】 §2.1 (manuscript.md:43) claims "802 samples: 760 ICU sepsis, 42 healthy controls" and "group (sepsis n=760 / healthy ctrl_GI n=42)". The only committed file carrying phenotype is `S02_immunoparalysis_score.csv`, which has `mars_endotype` and `death_28d` but **no `group` column**, so the 760/42 split cannot be checked from the deposited artifacts; it lives only in gitignored `01_data/GSE65682_pheno.csv`.
【证据】 From `S02`: 802 samples total; endotype Mars1=132 / Mars2=176 / Mars3=118 / Mars4=53 / unassigned=323; death_28d 1.0=114 / 0.0=365 / unassigned=323; 479 with both endotype and death — all match the manuscript. But `group` (sepsis/ctrl) is absent, so 760/42 is unconfirmed.
【为何重要】 The sepsis-vs-healthy DEG count (448, verified) depends on the 760/42 split; if that split were wrong the downstream 448 would be wrong too, yet it is not reproducible from the repo.
【具体修改】 Add the `group` column (or a tiny committed `GSE65682_pheno.csv` subset) to the repo, or point the §7 provenance row for "802 samples" at a committed file that actually contains the 760/42 split.

### A9 — "Zenodo DOI to be minted" is a not-yet-fulfilled declaration; reproducibility is currently unverifiable
【问题】 Data availability (manuscript.md:254) promises a "persistent DOI to be minted … upon acceptance" and a GitHub repo "to be made public upon acceptance." Both are forward commitments, not current artifacts. The GitHub URL `https://github.com/yyx-4113/sepsis-immunoparalysis-hub` and any Zenodo deposit cannot be verified at review time.
【证据】 The repo is described as private-until-acceptance; no DOI exists yet. This is standard for under-review deposits, but it means a reviewer cannot independently re-run anything today.
【为何重要】 Honesty: the claim is acceptable *if* the author commits to depositing on acceptance, but it should not be presented as if the data/code are already accessible. The §7 provenance table implies all cited files ship with the manuscript, yet several (the `01_data/` paths) do not.
【具体修改】 Soften to a clearly conditional statement and, if possible, deposit a private reviewer copy (e.g., a Zenodo "under review" DOI or a GitHub private link shared with the editor) so the audit is actually runnable during review.

### A10 — Audit assertion #5 scopes "no exact-0 p" to MR only; DEG-table underflow (CD14 adj.P = 0.0) is unguarded (disclosed, low risk)
【问题】 Assertion #5 (`check_audit_assertions.py:126–145`) scans only the MR CSVs for `p == 0.0` or `< 1e-300`. The differential-expression table `S01_immunoparalysis_direction.csv` contains `CD14` with `P.Value = 0.0` and `adj.P.Val = 0.0` (true underflow). The manuscript discloses this honestly ("CD14 Δ=−0.77 (P≈0, underflow)", manuscript.md:90, 92), so it is not an error — but the audit's own "no p exactly 0.0" guarantee does not cover the DEG layer.
【证据】 `S01_immunoparalysis_direction.csv` row CD14: `logFC=-0.7657, P.Value=0.0, adj.P.Val=0.0, direction=Mars1_down`. Manuscript Table 1 lists CD14 P "≈0 (P<1e-300)" — consistent.
【为何重要】 Low risk because disclosed; but if a *different* gene's p underflowed and were mis-reported as a finite value, the gate would not catch it. The audit's protective claim is narrower than a reader might assume.
【具体修改】 Extend assertion 5 to also scan `S01_immunoparalysis_direction.csv` / `S01_mars1_deg.csv` `adj.P.Val`/`P.Value` columns and require any 0.0 to be *explicitly* labelled "underflow" in the manuscript (or stored as a sub-normal, not literal 0.0).

---

## 3. §7 数字溯源表 — sampled verification (≥10 numbers, all re-derived by me)

I recomputed each cited number directly from the named CSV. Results (manuscript value → my recomputed value → status):

| §7 row | Manuscript | My recomputation (source) | Status |
|---|---|---|---|
| 802 samples / GPL13667 | 802 | `S02` sample nunique = **802**; genes = 11,519 (S01 rows) | ✅ (802 OK; 760/42 unverifiable — see A8) |
| sepsis-vs-healthy DEG 448 | 448 | `S01_deg_sepsis_vs_ctrl.csv` `DEG_0.3`.sum() = **448** | ✅ |
| Mars1 DEG 3597 | 3597 | `S01_mars1_deg.csv` `DEG_0.3`.sum() = **3597** | ✅ |
| 23/25 down, 22/25 FDR, 21 both | 23/22/21 | `S01_immunoparalysis_direction.csv`: down=**23**, fdr<0.05=**22**, both=**21** | ✅ |
| HLA-DRB1/CD74/CD14/FCGR3A Δ & P | −0.89/1.1e-15; −0.76/2.1e-15; −0.77/underflow; −0.61/9.1e-11 | S01: −0.8925/1.07e-15; −0.7578/2.08e-15; −0.7657/**0.0(underflow)**; −0.61/9.1e-11 | ✅ (CD14 adj.P=0.0 = underflow, disclosed) |
| Mars1 免疫评分中位 −0.79 | −0.79 | `S02` median = **−0.7917** (Mars2 −0.752, Mars3 0.640, Mars4 −0.235; range −3.65 to 3.86) | ✅ |
| 6 hub 基因 | 6 | `S05_hub_genes.csv` rows = **6** | ✅ |
| 30 基因签名 | 30 | `S06_signature_genes.csv` rows = **30** | ✅ |
| CV AUC 0.659 / 训练 0.750 | 0.659 / 0.750 | `S06_auc_compare.csv`: CV = **0.6586**, train = **0.7495** | ✅ |
| 外部 AUC 0.638 (CI 0.532–0.748) / L1 0.585 | 0.638 / 0.585 | `09_external_validation.csv`: orientedSum = **0.6382**, CI 0.5317–0.7475; locked = **0.5848** | ✅ |
| 校准斜率 0.50 / 截距 −0.04 | 0.50 / −0.04 | `09_ext_calibration_dca.csv`: slope = **0.5028**, intercept = **−0.0382**; NB@0.30=0.2844, NB@0.50=0.0755 | ✅ |
| 29/30 映射 (HLA-DQA1 缺失) | 29/30 | `09_external_validation.csv`: n_mapped=**29**, genes_missing=**HLA-DQA1** | ✅ |
| L1000 20,413 排名 | lenalidomide 5435/20413; azithromycin 9152/20413 | `S08_l1000_rescue_trtcp.csv` rows = **20413**; `S08_l1000_candidate_scores.csv`: lenalidomide rank **5435** (0.2663 → top 26.6%), azithromycin rank **9152** (0.4483 ≈ median) | ✅ |
| 7 候选药 + rescue | Table 2 | `08_candidates_drugs.csv`: 7 compounds; concordance 0.80/0.667/0.571/0.667/0.40/0.40/0.20 = prose | ✅ |
| 阳性对照 | IFN-γ 4/5 | `08_positive_control_check.csv`: IFN_gamma_rescues_antigen_presentation_axis = True (4/5 genes) | ✅ |
| S10 MR 45 检验家族 | 1 family-sig | `10_mr_bh_family.csv`: 45 rows, **1 YES** (CD74 crit-care Weighted median, q=2.99e-17) | ✅ |

**Conclusion on §7:** every sampled number traces to its cited CSV and matches. The only provenance-table weakness is that several cited *paths* (`01_data/...`) are not in the committed repo (A7/A8).

---

## 4. 文件级声明 (§2.1) — what I could and could not verify

Verifiable from committed `03_results/S02_immunoparalysis_score.csv` (a phenotype-side proxy):
- 802 total samples ✅
- endotype counts Mars1=132, Mars2=176, Mars3=118, Mars4=53, unassigned=323 ✅
- death_28d 114 / 365 / 323 ✅
- 479 samples with both endotype and 28-day survival ✅ (manuscript "479 with an assigned MARS endotype and 28-day survival")
- gene count 11,519 ✅ (from `S01_mars1_deg.csv` row count)

NOT verifiable from the committed repository:
- **760 sepsis / 42 ctrl** split — no `group` column in any committed file; only in gitignored `01_data/GSE65682_pheno.csv` (A8).
- **GPL13667** platform identity and the `!Series_platform_id = GPL13667` SOFT claim — cannot be re-checked without the raw SOFT (gitignored).
- The expression matrix "11,519 genes × 802 samples" sample alignment — only the gene count and the phenotype-side 802 are confirmable; the matrix itself is gitignored.

---

## 5. 森林图 (mr_forest.png) — can the "only CD74 critical-care WM is red" claim be verified?

- **From the data:** Yes. `10_mr_bh_family.csv` has exactly one `family_sig_q<0.05 = YES` row — `CD74 / Weighted median / 4982_critcare` (OR 2.194, p=6.65e-19, q=2.99e-17). Assertion #15 confirms this; my own count confirms 1/45.
- **From the figure:** Partially. The generator `02_scripts/python/_mr_diagnostics.py:49–93` reads the `family_sig_q<0.05` flag and colors `siglist` points red, so the artifact is *deterministically reproducible* from the CSV. The PNG mtime (08:12) post-dates the CSV (06:46). **However**, the gate (and I) cannot pixel-verify the PNG content, and the script uses a hardcoded absolute `PROJ` path (line 14) that breaks portability. This is a visualization-layer, non-fatal gap (see A6).

---

## 6. 数据可用性 / 可及性 — is the statement honest?

- "GitHub repo … to be made public upon acceptance" — forward commitment; repo currently unverifiable (A9).
- "persistent DOI to be minted" — explicitly pending; **not an extant artifact**, so a reviewer cannot confirm existence. Acceptable only as a stated future action, not as current availability (A9).
- "Processed expression and phenotype matrices … available in the repository" — **literally false** because `01_data/` is gitignored/untracked; the repo ships only `03_results/`, `04_figures/`, `02_scripts/` (A7).
- All **result tables and figures** cited in §7 *are* present and tracked (45 + 12 files), so the analytic provenance is genuinely reproducible from those. The gap is the raw/processed *inputs*, which must be re-downloaded via the provided scripts.

**Recommendation:** either commit the processed matrices (or a phenotype subset containing the 760/42 split and the expression matrix) or rewrite the Data-availability paragraph to state they are regenerated by script from public sources and are not committed (A7/A8/A9).

---

## 7. § 站得住的 (what is solid — with evidence)

1. **The MR-Egger t(df=n−2) fix is real and well-guarded (assertion 4).** I re-derived all 15 MR-Egger p-values from `beta`, `se`, `nsnp` and every one matches the stored `p` to <1e-9; the assertion also *forbids* the normal-based value, preventing regression to the Round-6 bug. This is the strongest, most purposeful assertion in the gate.
2. **The headline MR readout is internally consistent.** IVW/WM p-values are Wald-consistent with their beta/se (0 mismatches in my check); OR/CI = exp(beta±1.96·se) holds for every MR row (assertion 9). CD74 critical-care WM (OR 2.194, p=6.65e-19, family q=2.99e-17) is the sole family-significant test and reverses Mars1 direction — exactly as the prose states (manuscript.md:170, 182, 184).
3. **Every §7 number I sampled (16 rows) traces to its CSV and matches** — including the tricky ones: 23/22/21 immune counts, Mars1 score median −0.7917, CV 0.6586 / train 0.7495, external 0.6382 (CI 0.5317–0.7475), calibration slope 0.5028 / intercept −0.0382, L1000 20413 compounds, lenalidomide 5435 / azithromycin 9152. The digital provenance of the *result layer* is excellent.
4. **The 479 / 802 / endotype / death counts are reproducible** from a committed file (`S02`), not just asserted — a genuine strength for a single-author submission.
5. **The forest figure is data-driven**, not hand-colored: `_mr_diagnostics.py` binds the red point to the `family_sig_q<0.05` column, so re-running from `10_mr_bh_family.csv` reproduces the single highlighted test.

---

## 8. 向作者提问 (questions to the author)

1. Can you commit `GSE65682_pheno.csv` (or at least its `group`/`mars_endotype`/`death_28d` columns) so the 760/42 split and the 802-sample count are reproducible from the deposited repo, not only from the gitignored `01_data/`? (A8)
2. Will the processed expression matrix and the LINCS/E-MTAB-4451 intermediates actually be deposited, or only regenerated by script? The current Data-availability sentence implies they ship with the repo — please align wording with `.gitignore`. (A7)
3. Is a reviewer-copy DOI (Zenodo "under review") or a private GitHub link available so the audit is runnable during peer review, given the public repo and minted DOI are both post-acceptance? (A9)
4. For the CD74 critical-care Egger SE anomaly (0.111 vs IVW 0.325), do you have a sensitivity (e.g., a different Egger implementation or a leave-one-out) showing the point estimate is stable, given the gate exempts this exact cell? (A3)
5. The L1000 rescue score aggregates all 22 genes with the same sign, co-rewarding PDCD1/LAG3 up-regulation (manuscript.md:146). Have you computed the *dual-direction* version (PDCD1/LAG3 required down) as a sensitivity, to bound how much of the candidate ranking rests on the single-direction proxy? (not a provenance error, but a robustness question the audit cannot answer)

---

## 9. 我实际核查了什么 (auditor's work log)

**Files read (manuscript + scripts + CSVs, no prior reviews):**
- `05_reports/manuscript.md` (full)
- `02_scripts/python/check_audit_assertions.py` (full, 315 lines)
- `02_scripts/python/_mr_diagnostics.py` (forest/diag generator)
- CSVs: `S01_mars1_deg.csv`, `S01_deg_sepsis_vs_ctrl.csv`, `S01_immunoparalysis_direction.csv`, `S02_immunoparalysis_score.csv`, `S05_hub_genes.csv`, `S06_signature_genes.csv`, `S06_auc_compare.csv`, `09_external_validation.csv`, `09_ext_calibration_dca.csv`, `10_mr_bh_family.csv`, `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, `08_candidates_drugs.csv`, `08_positive_control_check.csv`, `S08_l1000_candidate_scores.csv`, `S08_l1000_rescue_trtcp.csv`
- `01_data/` existence + `.gitignore` (to assess what is/ isn't committed)
- `git ls-files` for `01_data`, `03_results`, `04_figures`, `02_scripts`

**Commands run (Python 3.13.12, pandas/scipy):**
1. `python 02_scripts/python/check_audit_assertions.py` → **exit 0**, all 15 assertions "passed".
2. DEG counts: `S01_mars1_deg['DEG_0.3'].sum()` = 3597; `S01_deg_sepsis_vs_ctrl['DEG_0.3'].sum()` = 448; gene rows = 11,519.
3. Immune direction: `S01_immunoparalysis_direction`: down=23, fdr<0.05=22, both=21; CD14 `P.Value=adj.P.Val=0.0` (underflow).
4. Score medians: `S02.groupby('mars_endotype')['immune_function_score'].median()` → Mars1 −0.7917, Mars2 −0.7520, Mars3 0.6405, Mars4 −0.2347; range −3.65 to 3.86.
5. Counts from `S02`: 802 samples; endotype 132/176/118/53/323; death 114/365/323; both=479.
6. AUC/calibration/external: `S06_auc_compare` CV 0.6586 / train 0.7495; `09_external_validation` orientedSum 0.6382 (CI 0.5317–0.7475), locked 0.5848, n=106, deaths=52, mapped=29, missing=HLA-DQA1; `09_ext_calibration_dca` slope 0.5028 / intercept −0.0382 / NB@0.30 0.2844 / NB@0.50 0.0755.
7. MR family: `10_mr_bh_family.csv` 45 rows, 1 YES (CD74 crit-care WM, q=2.99e-17). CD74 crit-care IVW OR 2.222 CI(1.175,4.200) p=0.014; Egger slope OR 2.222 p=0.088 intercept_p=0.9999; WM OR 2.194 p=6.65e-19. CD14 28ddeath Egger OR 0.906 p=0.0488 family q=0.730.
8. **IVW/WM Wald re-derivation (my own, not in the gate):** `2·(1−Φ(|beta|/se))` vs stored `p` → **0 mismatches** across all IVW + Weighted-median rows.
9. **Full Egger t-dist sweep (my own):** all 15 MR-Egger rows satisfy `p == 2·t.sf(|beta|/se, nsnp−2)` to <1e-9.
10. I² max = 0.5018 (FIS1 critical-care IVW).
11. L1000: `S08_l1000_rescue_trtcp.csv` = 20,413 rows; candidate scores lenalidomide rank 5435 (0.2663), azithromycin rank 9152 (0.4483).
12. Drugs: `08_candidates_drugs.csv` 7 rows, concordance = prose; `08_positive_control_check.csv` IFN-γ 4/5 True.

**Differences found (manuscript vs recomputed):** none that contradict the text. Minor rounding only: I² 0.5018 vs "0.50" (2-d.p. equal); CD14 adj.P stored as literal 0.0 while text says "underflow" (honest); CD74 crit-care Egger SE 0.111 < IVW 0.325 (disclosed). All other numbers match to ≤1e-3 or better.

**Audit script output (verbatim, exit 0):** "OK max I2 … = 0.502 (stated <= 0.50)"; "OK MR family size = 45"; "OK 9 §7 provenance paths present"; "OK 15 MR-Egger p-values match t(df=n-2)"; "OK no MR p/q value is exactly 0.0 or < 1e-300"; "OK Egger SE not substantially (<95%) below IVW SE; CD74 critical-care exempted"; "OK hub directions consistent … 5 Mars1-down hubs + FIS1 up"; Mann–Whitney P 0.467/1.85e-18/1.32e-3 (text 0.47/1.9e-18/1.3e-3); "OK OR/CI algebraically consistent"; "OK consensus immune counts = 23/22/21"; "OK Table-1 … match S01"; "OK Table-2 … matches"; "OK external validation AUC=0.638 …"; "OK calibration slope=0.50/intercept=−0.04 …"; "OK forest significance flag real: 1 family-significant test(s); CD74 crit-care WM flagged".

**Bottom line:** The result-layer digital provenance is strong and the audit gate (especially the MR-Egger t-dist assertion) genuinely protects the headline numbers. Remaining issues are (i) audit-gate slack/exemptions (A1–A6), and (ii) data-availability overclaim + unverifiable 760/42 split because `01_data/` is gitignored (A7–A9). None invalidate the Tier-1 biology; they bound the strength of the reproducibility claim and should be fixed before acceptance.
