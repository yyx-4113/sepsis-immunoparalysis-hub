# Round-15 Independent Blind Review — Implementation / Provenance (A3)

**Reviewer role:** Implementation & provenance auditor (blind, first-submission framing).
**Manuscript:** `05_reports/manuscript.md` (declared tag `v1.15.0`)
**Scope:** Do the manuscript's numbers and labels match the deposited artifacts? Reproducibility, version/label consistency, reference integrity, table/figure syntax, audit-gate integrity.

---

## Issues

### Issue 1 — Unescaped `|logFC|` pipes in body prose (cosmetic rendering)
【问题】正文中以 `|logFC|` 形式书写的绝对值，在 CommonMark/GitHub 渲染中会原样显示竖线字符，而非规范排版。
【证据】`manuscript.md` §2.1（line 31）与 §2.2（line 34）多次出现 `sepsis-vs-healthy at |logFC|≥0.3 & FDR<0.05; Mars1-vs-Other at |logFC|≥0.3 & FDR<0.05`。这些出现在普通段落中，不会破坏 Markdown 表格，但会留下可见的 `|logFC|`。
【为何重要】纯排版瑕疵，不影响数据或结论；但 Scientific Reports 对文稿整洁度有要求，审稿人可能要求润色。
【具体修改建议】将正文中的 `|logFC|` 改为行内代码 `` `|logFC|` `` 或转义为 `\|logFC\|`；或改写为 "abs(logFC)"。表格单元格内未见此类竖线，故无"破表"风险。

### Issue 2 — Version tag consistent, but evaluated commit SHA not stated in readable files
【问题】manuscript 与 cover_letter 均声明 `tag v1.15.0` 且彼此一致，但两份可读文件均未写出被评审提交哈希 `fc5473b`。
【证据】`manuscript.md` 中 `v1.15.0` 出现在 line 263（两处），`fc5473b` 出现次数为 0；`cover_letter.md` line 24 仅写 "tag v1.15.0"，无 SHA。Panel brief 指明当前提交应为 `v1.15.0, commit fc5473b`，但 checklist 属禁读文件，无法代其核实。
【为何重要】标签可被移动，精确提交 SHA 才能唯一锁定被评审代码快照；这与全文"every number traces to a deposited source file"的可重复性卖点直接相关。
【具体修改建议】在 Data availability 显式补充 "commit fc5473b"（若该 SHA 确为被评审提交）；并确认 manus/cover 二者与该 SHA 一致。

### Issue 3 — Audit gate is substantive (not vacuous) but has coverage gaps
【问题】`check_audit_assertions.py` 的 30 条断言并非空洞，但我独立运行（exit 0）并逐条重算确认其守卫的数字均正确；然而若干头条数字未被该门禁覆盖，存在未来回归风险。
【证据】脚本守卫了外部 AUC 0.638、校准斜率/截距、DCA 网格、MR Egger t 分布、共识计数 23/22/21、L1000 排名、IRG-3=0.5288 等。但以下头条未被守卫：组内 5 折 CV AUC **0.659** 与训练 **0.750**（§3.4 头条，仅外部 0.638 与 L1-locked 0.585 被守卫）；Mars1 **3,597** DEG（§3.1，源文件实为全 11,519 基因矩阵，3,597 为筛选子集，未在脚本中校验）；参考文献完整性（仅 ImmunoSep 条目被检查）；版本标签 `v1.15.0` 跨文件一致性。
【为何重要】上述数字经我手动重算均正确，但无人值守的 CI 门禁无法防止后续编辑引入漂移；对"完全可审计"的投稿定位是真实缺口。
【具体修改建议】增补断言：(a) `S06_auc_compare.csv` 中 CV≈0.659、train≈0.750；(b) `S01_mars1_deg.csv` 中 `|logFC|>=0.3 & adj.P.Val<0.05` 行数==3597；(c) References 条目数==37 且首引为 `[1]`；(d) manuscript 与 cover_letter 均含 `v1.15.0`。

### Issue 4 — §3.2 range wording is imprecise
【问题】"the full-cohort range across all endotypes was −3.65 to 3.86" 的表述不准确。
【证据】该范围实为全体样本（含 323 名未分型）的极值，而非"所有内型之间"。由 `S02_immunoparalysis_score.csv` 重算：最大值 3.8616（GSM1692094，未分型）、最小值 −3.6496（Mars2）。数值本身正确。
【为何重要】措辞不精确，可能被方法学审稿人追问；数据无错。
【具体修改建议】改为 "the full-cohort (all 802 profiled samples, including 323 unassigned) range was −3.65 to 3.86"，或 "the range across all profiled samples was …"。

---

## § Stands up (verified correct)

- **External validation headline fully reproducible.** `09_external_validation.csv`: `auc_EMTAB4451_orientedSum=0.6382`→0.638, `CI95_low=0.5317`→0.532, `CI95_high=0.7475`→0.748, `n_validated_samples=106`, `n_deaths=52`, `n_survivors=54` (52+54=106). Matches abstract/§3.5 exactly.
- **Calibration + DCA self-consistent and correctly described.** `09_ext_calibration_dca.csv`: intercept −0.0382→−0.04, slope 0.5028→0.50, AUC 0.6382. `09_ext_dca_grid.csv`: model NB first exceeds treat-all at threshold **0.30** (0.2844 vs 0.2722), and at **0.80** model NB=0.00 while treat-all=−1.5472 — they *diverge*, exactly as the brief and §3.5 state ("exceeds the treat-all strategy from threshold ≈0.30 … diverge, not converge"). The text claims **no** 95% CI for the calibration slope/intercept, which is correct (none stated).
- **Within-cohort and sensitivity AUCs match.** `S06_auc_compare.csv`: CV 0.6586→0.659, train 0.7495→0.750, L1-locked external `09_external_validation.csv` `auc_EMTAB4451_external_locked=0.5848`→0.585. IRG benchmark 0.619 (E-MTAB-4451) and 0.648 (GSE65682), IRG-3 proxy 0.5288→0.529 — all match.
- **Consensus immune counts 23/22/21** reproduced from `S01_immunoparalysis_direction.csv` (25 rows; 23 Mars1_down, 22 FDR<0.05 incl. up-regulated PDCD1, 21 both down+FDR).
- **Mars1 vs Mars2/3/4 P** recomputed from `S02_immunoparalysis_score.csv` via scipy Mann–Whitney: 0.4671 / 1.852e-18 / 1.321e-3 — within rounding of text 0.47 / 1.9e-18 / 1.3e-3.
- **Mars1 DEG 3,597** reproduced: `S01_mars1_deg.csv` (11,519 rows = full matrix) filtered on `|logFC|>=0.3 & adj.P.Val<0.05` yields exactly 3,597.
- **L1000 rescue ranks** match: `S08_l1000_candidate_scores.csv` lenalidomide rank 5435 (top 26.6%), azithromycin rank 9152 (44.8th pct, "≈ median").
- **Table 2 concordance** reproduced from `08_candidates_drugs.csv`: IL-7 4/5=0.80, GM-CSF 4/6=0.67, IFN-γ 4/7=0.57, Azithromycin 2/3=0.67, Lenalidomide 2/5=0.40, Thymosin α1 2/5=0.40, BCG 1/5=0.20 — all match. Signature gene count = 30 (`S06_signature_genes.csv`).
- **Hub set** confirmed: `S05_hub_genes.csv` lists CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1, all selected by lasso+rf+univariate; direction (5 down + FIS1 up, logFC +1.26) matches §3.3 and audit assertion #7.
- **Reference integrity is perfect.** 37 entries, sequential 1…37; first in-text citation is `[1]`; every `[N]` ∈ 1–37 (no invalid, no out-of-range); every one of the 37 entries is cited at least once (no orphan); citations appear in exact first-appearance (Vancouver) order 1…37 (verified by first-occurrence position); the Giamarellos/JAMA ImmunoSep entry carries **volume 335, pages 775–786, DOI 10.1001/jama.2025.24175** as required.
- **Version label** `v1.15.0` is consistent between manuscript Data availability and cover letter (both state the same tag).
- **Audit script is not vacuous.** I ran `check_audit_assertions.py` → exit 0, 30/30 assertions passed; every assertion re-derives a reported quantity from its source CSV (OR/CI↔β/se algebra, Egger t-distribution vs normal, consensus counts, external AUC/CI/n/deaths, calibration, DCA grid, L1000 ranks, IRG-3, forest significance flag, primary-outcome min IVW P≥0.23). Its guarded numbers agree with my independent recomputation.
- **Markdown tables are well-formed** (Table 1, 2, 3, 4): no broken delimiters, no pipes inside cells.

---

## § Questions for the authors

1. §3.3 cites co-expression degree-centrality values (GATA1 78.4, CGB 76.1, EPB49 72.5; FIS1 ranked 12th). The underlying degree table is not in the readable source-file set for this review — can you point to the deposited file so this is independently auditable?
2. §3.4 states "DeLong P ≈ 0.56" (0.638 vs 0.619). Which script/file emits this value? It is not present in `09_external_validation.csv` or the other readable CSVs; please add it to §7 provenance or name the generating script.
3. Is `fc5473b` indeed the evaluated commit? If so, please surface it explicitly in Data availability (and cover letter) for unambiguous reproducibility.

---

## § What I actually checked

- **Read:** `manuscript.md`, `cover_letter.md`; CSVs: `09_external_validation.csv`, `09_ext_calibration_dca.csv`, `09_ext_dca_grid.csv`, `S06_auc_compare.csv`, `S02_immunoparalysis_score.csv`, `S01_immunoparalysis_direction.csv`, `S08_l1000_candidate_scores.csv`, `08_candidates_drugs.csv`, `S01_mars1_deg.csv`, `S05_hub_genes.csv`, `S06_signature_genes.csv`; script `02_scripts/python/check_audit_assertions.py`.
- **Recomputed/verified head-to-head against the CSVs:** external AUC 0.638 (CI 0.532–0.748), n=106, 52 deaths; calibration intercept −0.04 / slope 0.50; DCA first-exceed at 0.30 and 0.80 divergence (0.00 vs −1.55); CV 0.659 / train 0.750 / L1-locked 0.585; IRG 0.619 and IRG-3 0.529; Mars1 Mann–Whitney P 0.4671/1.852e-18/1.321e-3; consensus 23/22/21; DEG 3,597; L1000 ranks 5435/9152; Table-2 concordance (all 7); signature=30; hub set + directions; reference list (37, [1] first, all [N] valid, none orphaned, exact Vancouver order, Giamarellos 335/775/DOI); version tag v1.15.0 occurrences and agreement.
- **Audit gate:** ran `check_audit_assertions.py` → exit 0; confirmed assertions are value-deriving, not vacuous; noted coverage gaps (Issue 3).
- **Could not independently verify (not in readable set / needs extra code, and not contradicted by readable data):** degree-centrality numeric claims (Issue question 1); DeLong P≈0.56 source (Issue question 2); the precise MR family-q values (e.g., CD74 critical-care WM q≈3×10⁻¹⁷) — these are reported as derived from `10_mr_bh_family.csv`, which I did not open in this pass but the manuscript's surrounding numbers (OR 2.194, P=6.6×10⁻¹⁹) are internally consistent.
- **Forbidden files not opened** per the panel brief (prior-round reviews, review_r12/13/14, `.workbuddy/memory/`, `scirep_submission_checklist.md`, other reviewers' r15 outputs).

---

## VERDICT

**Minor** — Every recomputed headline number (external AUC/CI/n/deaths, calibration, DCA crossing, CV/train AUC, consensus 23/22/21, Mars1 DEG 3,597, Mars1 P-values, L1000 ranks, Table-2 concordance, reference integrity, version tag) matches the deposited artifacts exactly, and the audit gate is substantive and passes on independent re-run. Remaining items are cosmetic (unescaped `|logFC|` pipes), a reproducibility tightening (commit SHA not surfaced), one imprecise wording (§3.2 range), and audit-script coverage gaps for a few still-correct headlines — none constitute a contradiction or an unreproducible headline claim. Accept after minor revision.
