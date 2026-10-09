# A2 — Design / Statistics 评审（独立同行评审，Round-22）

## 1. 独立性声明
我未读取 `06_review/` 下任何历史轮次评审、作者反驳信或"已修复说明"，本评审仅依据 `manuscript.md` v1.23.1、`03_results/*.csv`、`02_scripts/python/*.py` 与 `07_submission_bmc_v1.21.0` 产物独立得出。（透明披露：开局核对路径时误入一个陈旧镜像目录中的 `05_reports/review/A4_venue.md`（旧版 v1.0.2 评审），该文件不属于被禁的 `06_review/` 路径，我未据其得出任何结论——其数字与本版不符，本评审所有结论均来自我对源数据的独立重算。）

## 2. 裁决（Verdict）
**MAJOR。** 全部统计数字经独立重算均正确，DeLong 检验方法学成立，"主要指标 vs 敏感性指标"框架诚实且一致；唯一阻断性问题是文章以"完全可审计 / 每个数字都可追溯到脚本"为核心卖点，但提交的校准 CI / p 值列无法由已提交的分析脚本再现（Tier 1, F1）。该问题范围窄、易修复、不推翻任何结论；补齐后本文统计层面可降至 ACCEPT/MINOR。

## 3. 发现（Findings）

### [Tier 1] F1 — 校准 CI 与 p_slope_eq_1 在已提交脚本中不可再现（可审计性缺口）
- **Claim / 位置**：`manuscript.md` §3.5（L107 外部验证段落）报告"校准截距 −0.04（95% CI −0.43 至 0.35）、斜率 0.50（95% CI 0.10 至 0.90）"；`03_results/09_ext_calibration_dca.csv` 实际含 `calib_slope_ci_lo/hi`、`calib_intercept_ci_lo/hi`、`calib_slope_se`、`calib_intercept_se`、`p_slope_eq_1 = 0.01575`。文章 L1 标题与 L194（§7 溯源表）宣称"fully auditable / 每个数字都追溯到具体输出"。
- **Problem**：已提交的 `02_scripts/python/_ext_calibration_dca.py`（L102–109）只写出 7 列（`n, deaths, prevalence, calib_intercept, calib_slope, auc, nb_thr0.20/0.30/0.50`），**不计算也不写出任何 CI 或 p 值**。全仓检索（`grep -rln 09_ext_calibration_dca`）仅 `check_audit_assertions.py` 与 `_ext_calibration_dca.py` 引用该文件，前者只断言、不写。即：被引用的校准 CI / p 值**没有由任何已提交脚本生成**。若读者重跑仓库，得到的 CSV 缺失 CI/p 列，文章中报告的 CI(0.10–0.90) 不可复现——直接击穿"fully auditable"核心声明。（注：`__pycache__/_ext_calibration_dca.cpython-313.pyc` 字节码中亦无可疑 CI 代码，说明磁盘上的 `.py` 源与生成该 CSV 的版本不一致，是一处版本/提交脱节。）
- **Concrete fix**：提交能够生成 `calib_slope_ci_lo/hi`、`calib_intercept_ci_lo/hi`、`p_slope_eq_1` 的 `_ext_calibration_dca.py`（或新增命名清晰的脚本，用 bootstrap/轮廓似然给出 CI、用 Wald 检验 `H0: slope=1`），重跑使 deposited CSV 可复现。数字本身正确（见 F1 验证：slope CI = 0.5028 ± 1.96·0.2069 = 0.097–0.908；p_slope=1 的 Wald z = −2.40, p ≈ 0.016），故属**溯源缺口而非数值错误**。

### [Tier 2] F2 — 摘要命名 primary 时缺少"not significantly above chance"口吻警示
- **Claim / 位置**：Abstract（L14）报告 primary locked-L1 0.585（95% CI 0.469–0.696），但只给了 CI；明确的"not significantly above chance"口吻警示出现在 L55（§2.9）、L107（§3.5）、L157（Limitation 1），**唯独摘要缺失**——摘要是最常被阅读的部分。
- **Problem**：该 primary 是唯一非显著的外部指标，其"不显著"是全文最关键的诚实点，应在摘要即点明，而非仅由读者自行从 CI 推断包含 0.5。与文章其余部分"凡命名 primary 必附 caveat"的口径不一致。
- **Concrete fix**：在 L14 改为"…external AUC 0.585 (95% CI 0.469–0.696, which includes 0.5, so the primary estimate is not significantly above chance)…"。

### [Tier 3] F3 — §7 将两次 CV AUC 差异误称"rounding artifact"
- **Claim / 位置**：`manuscript.md` L194 称 `S06_auc_compare.csv` 的 0.6586 与 `09_external_validation.csv` 的 0.6582 之差为"rounding artifact"。
- **Problem**：两者是两次不同的 5 折 CV 运行（不同随机种子/实现），相差 0.0004，并非同一数值的四舍五入。
- **Concrete fix**：改为"两次 CV 种子分别得 0.6586（S06）与 0.6582（09），均四舍五入为 0.659"。

## 4. 交叉验证注记（从 `09_ext_risk_scores.csv` 用 numpy/scipy 独立重算）
重算基于 106 样本 / 52 死亡 / 54 存活；DeLong 用配对 V 分量法；bootstrap 用 `np.random.default_rng(42)`、2000 次重采样，并严格复刻脚本中 rng 的先后消费顺序（先 locked 后 oriented-sum）。

1. **DeLong P（equal-weight 0.638 vs IRG3 0.529）= 0.1556 → 文章 0.16**：**MATCH**。✓
2. **Bootstrap 95% CI – locked-L1 = 0.4687–0.6959 → 文章 0.469–0.696**：**MATCH（精确复刻）**。✓
3. **Bootstrap 95% CI – oriented-sum = 0.5317–0.7475 → 文章 0.532–0.748**：**MATCH（精确复刻）**。✓
4. **AUC 点估计（CSV 重算）：oriented-sum 0.6382 / locked-L1 0.5848 / IRG3 0.5288 → 文章 0.638 / 0.585 / 0.529**：**MATCH**。✓
5. **校准点估计：slope 0.5028→0.50、intercept −0.0382→−0.04**（与 CSV 一致）；slope 显著 <1（p≈0.016）被文章正确解读为"sub-ideal"。**MATCH**。✓
6. **DCA 网格 `09_ext_dca_grid.csv` 与文章所报 NB 值及"≥0.80 塌缩为 treat-none"claim 完全一致**：在 ≥0.80 阈值 n_flagged=0/106、NB=0，文章已诚实标注"vacuous / not interpretable"。**MATCH**。✓
7. **SRS/age 基准 AUC（0.6104 / 0.5043）与 permutation P（0.694）与 `09_ext_benchmark_vs_srs.csv` 及文章一致**。✓

## 5. 站得住的结论（经核查无误，予以肯定）
- **Primary/Sensitivity 框架诚实且一致**：locked-L1 0.585 = 预指定 PRIMARY，equal-weight 0.638 = 预指定 SENSITIVITY，CV 0.659 始终标注 optimistic；"CI 含 0.5 / 不显著优于机会"的 caveat 在 §2.9、§3.5、Limitation 1、Conclusion 均出现（仅摘要缺口见 F2）。
- **DeLong 检验成立且方法学正确**：equal-weight 与 IRG3 两者在 `09_ext_risk_scores.csv` 中均有逐样本向量（`risk_oriented_sum`、`risk_irg3`），配对 DeLong 合法，重算 P=0.156≈0.16。
- **不存在"不可能的 DeLong"**：文章**没有**对 Peng 已发表的 0.619 点估计做 DeLong/H0 检验；Limitation 1 正确说明其无逐样本分数/CI，"no formal significance test is possible"。评审担心的"对 0.619 做不可能 DeLong"**未发生**。
- **EPV、终点稀释、选择链 FWER 均已诚实披露**：外部 EPV≈1.7、CV≈3.8（Limitation 1/§3.4）、终点稀释（Limitation 7）、选择链族误控（Limitation 9）均明示；药物候选的二项式 P 均在自身背景内、未主张显著性。无被掩盖的虚假显著。

## 6. 给整合者的一句话摘要
统计层面基本干净、DeLong(0.16) 与全部 AUC/CI/DCA 经重算均吻合且框架诚实，唯一阻断项是"已提交校准脚本不能再现文章所报 CI/p 值"这一可审计性缺口（F1），补上脚本并给摘要加一句非显著警示（F2）即可放行。
