# 独立同行评审意见 — 生物统计 / 因果推断 / 孟德尔随机化方向

**稿件：** Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning
**评审角色：** 独立统计 / 因果推断审稿人（单作者生信稿，首次投稿视角）
**评审范围：** 仅基于稿件正文与 6 个指定源 CSV 的独立重算；未读取任何 prior review / RESPONSE / review_r7 / .workbuddy。

---

## 1. MR 多重检验与 Egger t 分布

### 【问题】
验证 45 检验 BH 家族校正的三项断言：(a) family_sig_q<0.05 是否仅 CD74 critical-care weighted median 一行；(b) CD74 critical-care WM family q≈3e-17、Egger family q=0.79、CD14 28d-death Egger family q=0.73 是否与稿件一致；(c) 主结局 5086 上最小 IVW P 是否真实 ≥0.23。

### 【证据】
- `10_mr_bh_family.csv` 共 **45 行数据**（header 后 45 行）；`family_sig_q<0.05` 列仅第 17 行（CD74 / Weighted median / 4982_critcare）为 `YES`。我以 Python 对 45 个 `p` 独立重算 BH q，结果 **恰好 1 个 q<0.05**，且数值与 CSV 的 `q_family_45test` 完全一致。
- CD74 crit WM：CSV `q_family_45test` = 2.9918731301280435e-17；重算 = 2.9919e-17 ✓
- CD74 crit Egger：CSV = 0.7921342799868003；重算 = 0.7921 ✓
- CD14 28d-death Egger：CSV = 0.7304566955883753；重算 = 0.7305 ✓
- 主结局 5086 的 IVW P（来自 `10_genetics_mr_outcome5086_28ddeath.csv`）：CD14 0.2359、HLA-DQA1 0.2600、FIS1 0.4727、CD74 0.7178、HAVCR2 0.8475；**最小值 = 0.236**，确 ≥0.23 ✓
- 额外核验：Egger p 值确为 **t(n−2) 分布**而非正态——CD14 28d Egger β/SE = −2.800，df=4，两尾 p=0.04881（与 CSV 0.048809 吻合）；CD74 crit Egger t=7.19，df=1，p=0.08801（与 CSV 0.088015 吻合）。故"校正到 t 分布"已正确执行。

### 【为何重要】
三项数值断言全部成立，且 Egger p 值的 t 分布校正无误——这是稿件统计严谨性的真实亮点，多重检验处理诚实、可复现，不应被削弱。

### 【具体修改】
无需数值修改。建议仅做一处措辞强化（英文替换句）：
> *"Reassuringly, the full 45-test BH read-out was independently reproduced from the deposited p-values: exactly one test (CD74 critical-care weighted median) retains family q<0.05, and the CD74 critical-care Egger family q=0.79 and CD14 28-day-death Egger family q=0.73 match the manuscript to four significant figures."*

---

## 2. Egger SE 倒挂（CD74 critical-care）

### 【问题】
稿件 §3.10（manuscript.md:182）称 CD74 critical-care MR-Egger SE(0.111) < 其 IVW SE(0.325)。从 criticalcare CSV 验证这两个 SE，并判断其合理性与对结论的含义。

### 【证据】
- `10_genetics_mr_outcome4982_criticalcare.csv` 第 3 行（CD74 MR-Egger）：`se` = 0.11107427522112252；第 2 行（CD74 IVW）：`se` = 0.3249609227470688。与稿件 0.111 / 0.325 一致 ✓
- 同一 3 个 SNP 上，Egger 斜率 SE(0.111) 小于 IVW SE(0.325)，属**异常排序**：标准 MR 预期 Egger 因解放截距、采用不同加权而 SE ≥ IVW SE。此处倒挂说明 1–2 个 SNP 在 Egger 几何中施加了高杠杆，使斜率 CI 看似偏窄。
- 更关键：Egger 用 df = n−2 = 1（仅 3 工具），t(1) 重尾使即便斜率 t=7.19，p 仍仅 0.088。即 **n=3 时 Egger 检验本质上近似无功效**——只要斜率不是极大，永远越不过 p<0.05。

### 【为何重要】
稿件已对 SE 倒挂与 overlap 偏差给出警示，方向正确。但当前表述"MR-Egger no longer does … under the corrected t-distribution"隐含"若 SE 排序正常 Egger 本会显著"的错觉。事实上 n=3 的 Egger 在 t(1) 下几乎不可能显著，SE 倒挂本身正是该估计脆弱的诊断信号，而非一个"本可显著却被 t 校正压制"的结果。

### 【具体修改】
英文替换句（manuscript.md:182 相关句）：
> *"The CD74 critical-care MR-Egger standard error (0.111) is smaller than its own IVW standard error (0.325) on the same three SNPs — an inversion that is itself diagnostic of an Egger slope leveraged by a single outlying instrument, so its narrow CI is not credible. With only three instruments the Egger test has df = 1 and is effectively uninformative (any slope would require an extreme t to reach p<0.05); the family q = 0.79 therefore reflects a structurally untestable estimate rather than a 'lost significance'."*

---

## 3. 样本重叠（eQTLGen × UK Biobank）

### 【问题】
eQTLGen 与 UKB 结局共享样本，稿件未做 overlap 校正；评估该省略对点估计/SE 偏差方向的影响，以及"hypothesis-generating"措辞是否足够。

### 【证据】
- 稿件 §2.10（manuscript.md:70）与 §3.10（:182、:201）明确承认 eQTLGen 发现样本含 UKB 受试者，构成 exposure–outcome 样本重叠，并引用 Burgess, Davies & Thompson (2016) 作为未执行的校正方案，结论整体以"hypothesis-generating"表述。
- 唯一 family-significant 结果（CD74 crit WM，OR 2.19，q≈3e-17）恰恰是**重叠最易放大的那类结果**：overlap 使暴露与结局效应相关，比率估计被推向"观察性（非因果）关联"方向——即**偏离零、放大 OR 并缩小 SE**，提高假阳性而非保守。

### 【为何重要】
"hypothesis-generating"是必要的，但**不够**：它未点明偏差方向。读者可能误以为 overlap 只会稀释信号；实际相反——重叠最易把本不显著的关联"做"显著，而稿件中唯一的 family 显著结果正是最脆弱者。

### 【具体修改】
建议强化 limitation（manuscript.md:201 附近）的英文替换句：
> *"Because eQTLGen and the UK Biobank sepsis outcomes share participants, the overlap biases the ratio estimates toward the observational (non-causal) association — inflating effect size and shrinking standard errors rather than conservatively attenuating them. The single family-significant result (CD74 critical-care weighted median) is therefore the estimate most vulnerable to overlap-induced inflation, and is reported as hypothesis-generating only."*

并补充分析 spec：在可用时运行 `mrSampleOverlap` 偏差估计器，至少报告 CD74 crit WM 校正后的 OR/SE，或在正文定性写出"偏差方向为偏离零"。

---

## 4. DCA / 校准

### 【问题】
验证 `09_ext_calibration_dca.csv` 中 calib_slope=0.50、intercept=−0.04、auc=0.638、nb_thr0.20=0.3632 / 0.30=0.2844 / 0.50=0.0755 与稿件一致；指出 CSV 仅 3 个阈值点，"0.10/0.75/0.77"来自图而非数值产物，是否构成溯源缺口；slope<1 的准确解释是否被恰当说明。

### 【证据】
- `09_ext_calibration_dca.csv` 第 2 行：`calib_slope`=0.5028≈0.50、`calib_intercept`=−0.0382≈−0.04、`auc`=0.6382≈0.638、`nb_thr0.20`=0.3632、`nb_thr0.30`=0.2844、`nb_thr0.50`=0.0755。全部与稿件 §3.4（manuscript.md:117）及溯源表（:236）吻合 ✓
- **溯源缺口**：CSV 的阈值列仅有 `nb_thr0.20 / nb_thr0.30 / nb_thr0.50` 三列。稿件 §3.4 称"DCA NB 在 0.10–0.75 阈值范围为正、~0.77 收敛到 0"中的 **0.10、0.75、0.77 均不在 CSV 中**，只能来自 `04_figures/S06_dca.png`。即该数值断言是图派生产物，无 deposited 数值溯源。
- slope<1 解释：slope=0.50 意为外部预测**过度极端（过度自信）**——校准需将 log-odds 收缩约 50%；intercept≈−0.04 仅说明平均校准尚可（calibration-in-the-large OK），但斜率<1 表明高风险的预测偏高、低风险的预测偏低。稿件称其为"primary honest read"正确，但未把方向讲透。

### 【为何重要】
(1) 溯源缺口违反稿件自诩的"每个数字可溯源到具体产物"原则（§7 溯源表把 DCA 同时列在 CSV 与 png，但 0.10/0.75/0.77 实际只属 png）。(2) slope=0.50 直接关系到"绝对风险是否可用于临床决策"：AUC 0.638 说明**排序能力尚可，但绝对风险估计不可信**——这对任何临床适用性宣称是硬约束，必须明说。

### 【具体修改】
- 溯源修正（英文替换句，manuscript.md:117 末段）：
> *"As plotted in Fig. S06 (04_figures/S06_dca.png), the decision-curve net benefit is positive across the depicted threshold range (≈0.10–0.75) and converges to ~0 near threshold 0.77; the three deposited numeric anchors are nb at threshold 0.20 = 0.3632, 0.30 = 0.2844, 0.50 = 0.0755 (03_results/09_ext_calibration_dca.csv)."*
- 并补充分析 spec：将完整 DCA 阈值表（0.05/0.10/0.20/0.30/0.50/0.75/0.77 的 NB）作为 CSV 沉积，使"0.10–0.75 为正、0.77→0"成为数值可溯源断言。
- slope 解释强化（英文替换句）：
> *"the calibration slope of 0.50 (intercept −0.04) indicates the score is over-confident externally — predicted risks are too extreme and would require ~50% shrinkage of the log-odds for perfect calibration; ranking is preserved (AUC 0.638) but absolute risk estimates are not trustworthy for clinical decision use."*

---

## 5. EPV≈3.8 与 selection-chain 家族误差

### 【问题】
评估 EPV≈3.8 与 selection-chain 家族误差未控制，对"CV AUC 乐观度"论证的充分性。

### 【证据】
- `10_genetics_mr_outcome5086_28ddeath.csv` 之外，EPV 计算在 §3.4（manuscript.md:117）：114 死亡事件 / 30 基因 = **3.8**，重算 = 3.8 ✓
- 稿件已承认 (a) 基因选择与定向复用了同一队列的 28 天标签，故 0.659 为乐观估计；(b) limitation 10（:210）明确 selection-chain 家族误差未控制、需独立队列复现。
- 但**乐观度论证不充分处**：within-cohort CV AUC 0.659 与 external 0.638 仅差 0.021。对 EPV 3.8 且标签复用而言，这一小落差可能有两种解释——(i) 信号由少数强基因主导、确较稳健；或 (ii) "乐观"已体现在基因选择阶段而非 CV 拟合阶段，故 CV 落差被低估。且 0.659 **未报告 CI**；5 折 CV 每折仅约 23 个事件用于评估，CV AUC 本身精度有限。

### 【为何重要】
EPV 3.8 远低于常规 ≥10 规则，无论乐观落差大小，都**直接封顶了 within-cohort AUC 的可信度**。稿件笼统说"optimistic"不够，应给出量化乐观度（bootstrap / Harrell .632 或层内再拆分）并明确 EPV 对 CV AUC 置信度的硬约束。

### 【具体修改】
英文替换句（manuscript.md:117 附近）：
> *"With EPV ≈ 3.8 (114 events / 30 genes), well below the conventional ≥10 rule, the within-cohort CV AUC of 0.659 is credible only as an upper-bound ranking signal; a bootstrap optimism estimate (or .632) and a 95% CI for the CV AUC should accompany this figure, since the small 0.021 gap to the external 0.638 may understate selection-stage optimism."*
分析 spec：补充 `S06_auc_compare.csv` 中 CV AUC 的 bootstrap CI，或报告 1000 次 bootstrap 乐观校正 AUC。

---

## 6. 外部 AUC 0.638 vs IRG 基准 0.604

### 【问题】
外部 AUC 0.638 (95% CI 0.532–0.748) 与 IRG 基准 0.604 的差异是否真"无统计确立"（CI 重叠）。

### 【证据】
- `09_external_validation.csv`：orientedSum AUC = 0.6382，CI = [0.5317, 0.7475]≈[0.532, 0.748] ✓；`auc_IRG3_benchmark_EMTAB4451` = **0.604**（无 CI 列）。
- 稿件 §3.4（manuscript.md:117）称"their confidence intervals overlap, so the difference is not statistically established"。
- **问题**：IRG 基准 0.604 在稿件与 CSV 中**均只给点估计、无 CI**。因此"their CIs overlap"在已报告数字下**无法成立**——只有 signature 有 CI。真实可证的是：IRG 点估计 0.604 **落于** signature 的 95% CI [0.532, 0.748] 之内，故不能拒绝相等。这是一个更弱但有效的陈述。
- 更恰当检验：两 AUC 均在**同一 106 例** E-MTAB-4451 上计算，应做 **DeLong 配对检验**而非 CI 重叠判断。

### 【为何重要】
"CI 重叠"是比"点估计落入对方 CI"更强的断言，稿件用它支撑"差异无统计确立"属于措辞过度。读者会误以为已做过 IRG 的 CI 比较。正确做法要么补 IRG CI，要么降格陈述，最好直接用 DeLong 配对检验。

### 【具体修改】
英文替换句（manuscript.md:117 "their confidence intervals overlap…" 句）：
> *"The IRG benchmark point estimate (0.604, recomputed on the same cohort) falls within our signature's 95% CI (0.532–0.748), so the apparent +0.034 advantage is not statistically distinguishable from zero; a paired DeLong test on the 106 shared samples (AUC_signature vs AUC_IRG) should be reported to formalise this."*
分析 spec：在 `09_external_validation.csv` 增补 IRG 基准的 bootstrap 95% CI，或在正文补一行 DeLong 检验 p 值。

---

## § 站得住的（reviewer 认为可靠、不必改的部分）

1. **内型驱动而非病例/对照驱动**（§3.1）：Mars1-vs-Other 3597 DEGs vs sepsis-vs-healthy 448 DEGs，构成强内部对照，生物学信号稳健。
2. **MR 多重检验处理诚实且可复现**（§3.10 / `10_mr_bh_family.csv`）：45 检验 BH 我独立重算，恰好 1 个 q<0.05，且 q 值与 Egger 的 t 分布 p 值全部吻合——统计执行质量高。
3. **外部验证的纪律性**（§3.5）：锁定模型、固定定向、零再调参；明确 L1 权重不移植（0.585）；校准斜率 0.50 被诚实报告为过拟合信号。
4. **方向相反结果的正确处理**：CD74 critical-care WM（OR 2.19）虽 family 显著但方向**反转**于 Mars1 表达模型，稿件正确地将其解读为基因型–严重程度关联而非因果重定位证据。
5. **药物重定位的诚实框架**（§2.8、§3.9）：metrics 明确标注为假设生成；糖皮质激素阳性对照"高分"的警示是真实的方法学优点，避免了"转录救援=功能救援"的错误推论。

---

## § 向作者提问（questions to author）

1. 能否将完整 DCA 阈值表（NB at 0.05/0.10/0.20/0.30/0.50/0.75/0.77）作为 CSV 沉积，使"0.10–0.75 为正、0.77→0"成为数值可溯源断言，而非仅图派生？
2. 对样本重叠，您是否尝试过 Burgess–Davies–Thompson `mrSampleOverlap` 偏差估计器？若已运行，请提供 CD74 crit WM 校正后的 OR/SE；若未运行，能否至少定性写出偏差方向（偏离零、放大 OR、缩小 SE）？
3. 能否为 within-cohort CV AUC（0.659）补一个 95% CI 和/或 bootstrap 乐观度估计（EPV 3.8 下）？
4. 能否补 IRG 基准在 E-MTAB-4451 上的 95% CI，或直接做 DeLong 配对检验（signature vs IRG，同 106 样本）以正式化"无统计确立"？
5. 对 CD74 critical-care，能否报告哪个/哪几个 SNP 驱动了 Egger 杠杆，并附 leave-one-out，以证明 SE 倒挂由单一工具驱动还是稳健？

---

## § 我实际核查了什么（audit trail）

**读取的文件（仅指定源，未触碰任何 prior review）：**
- `05_reports/manuscript.md`
- `03_results/10_mr_bh_family.csv`
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv`
- `03_results/10_genetics_mr_outcome4982_criticalcare.csv`
- `03_results/10_genetics_mr.csv`
- `03_results/09_ext_calibration_dca.csv`
- `03_results/09_external_validation.csv`
- `03_results/S06_auc_compare.csv`

**运行的 Python 重算：**
1. 对 `10_mr_bh_family.csv` 的 45 个 `p` 独立重算 BH q（自写 BH 函数）——验证恰好 1 个 q<0.05，且 q 值与 CSV `q_family_45test` 一致（CD74 crit WM = 2.9919e-17；CD74 crit Egger = 0.7921；CD14 28d Egger = 0.7305）。
2. 用 scipy 核验 Egger p 值确为 t(n−2) 分布：CD14 28d Egger t=−2.800 df=4 → p=0.04881（CSV 0.048809）；CD74 crit Egger t=7.19 df=1 → p=0.08801（CSV 0.088015）。
3. 提取 5086 主结局全部 IVW P，确认最小值为 0.2359（≥0.23）。
4. 核对 criticalcare CSV 中 CD74 Egger SE=0.11107、IVW SE=0.32496。
5. 核对 DCA：slope=0.5028、intercept=−0.0382、auc=0.6382、nb 0.20/0.30/0.50 = 0.3632/0.2844/0.0755；确认阈值列仅 3 列（0.20/0.30/0.50），0.10/0.75/0.77 不在 CSV。
6. 核对外部 AUC：orientedSum CI [0.5317, 0.7475]≈[0.532,0.748]；IRG 基准 = 0.604（无 CI 列）。
7. 核对 EPV：114/30 = 3.8。

**重算值 vs 稿件值：差异汇总**
- 全部核对数值（MR 家族 q、Egger SE、DCA 全部字段、外部 AUC CI、EPV）**与稿件一致，无数值矛盾**。
- **两处非数值但需纠正的断言**：(i) DCA "0.10–0.75 为正、0.77→0" 的 0.10/0.75/0.77 仅存在于图、不在 deposited CSV（溯源缺口）；(ii) "IRG 与 signature 的 CI 重叠" 不成立——IRG 仅有点估计 0.604、无 CI，仅能说其点估计落于 signature CI 内，应补 IRG CI 或改做 DeLong 配对检验。
