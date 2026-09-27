# 独立盲审（统计 / 因果推断）第 16 轮 — 设计层评审 A2_design

以首次投稿对待本稿。所有判断均来自本人直接读取的文本与源数据，并对可核验头面数字逐一重算。

---

## 一、逐项问题（按输出契约：问题 / 证据 / 为何重要 / 具体修正）

### 问题 1 —【DCA "0.80 处背离、模型 NB 0 而 treat-all −1.55" 本质是 DCA 公式的算术产物，被头面化夸大】

【Problem】稿件将外部 DCA 在阈值 0.80 处"模型净获益 0、treat-all −1.55"的背离作为决策效用的卖点，但该背离并不反映模型增益，且模型相对 treat-all 的真实优势在可操作阈值内极小。

【Evidence】`09_ext_dca_grid.csv`：0.05–0.25 区间模型 NB 与 treat-all NB 完全相等（0.4638/0.4638、0.434/0.434、0.4007/0.4007、0.3632/0.3632、0.3208/0.3208）；0.30 时模型 0.2844 仅比 treat-all 0.2722 高 0.012；0.80 时 treat-all NB = −1.5472，恰好等于 DCA 公式 0.49 − 0.51×(0.8/0.2) = −1.55。稿件 §3.5。

【Why it matters】头面化 0.80 背离暗示强临床决策价值，而数据仅显示模型在 ≈0.30 起以不足 0.01 的 NB 微弱超过 treat-all；签名本身已被作者定性为"风险排序器而非校准概率"（§3.5），DCA 的强语气头面与该限定自相矛盾，易误导临床解读。

【Specific fix】将 DCA 表述改为："模型仅在 ≈0.30 阈值起微弱超过 treat-all（NB 差 ≤0.012 直至 0.35）；0.80 处的背离源于 treat-all NB 在 DCA 公式下随阈值陡降，并非模型新增收益。"删除或显著降级 0.80 的强调；如保留，须明确其为公式性而非模型性增益。

---

### 问题 2 —【校准参数与基于其的 DCA 均在外部测试集（n=106）上估计，属测试集内嵌套校准，偏乐观】

【Problem】稿中"过自信→已纠正"的叙事所依赖的截距/斜率，以及其上的 DCA，都是在被评估的同一外部队列上拟合的，等于用测试集校准测试集。

【Evidence】`09_ext_calibration_dca.csv` 的 slope 0.5028 / intercept −0.0382 来自 E-MTAB-4451 本身；同一 106 样本队列又直接喂给 `09_ext_dca_grid.csv` 的净获益计算。稿件 §3.5 同时给出"校准后概率"与 DCA。

【Why it matters】在测试集上估计校准会把"过自信"部分乐观地吸收进纠正，使 DCA 看似提供独立决策收益；读者可能把该 DCA 当作效用的独立验证，而它实则是测试集内回环。

【Specific fix】明确声明截距/斜率是在外部测试集上估计的，完整的独立校准需要第三队列或训练/验证分割；将 DCA 定位为"示意性、非决策级"证据，并在局限中补一条"外部队列同时承载验证与校准，校准参数无独立复算"。

---

### 问题 3 —【L1000 糖皮质激素反例（prednisone 高分）与继续把 L1000 排名当作候选药支持证据之间存在自我张力】

【Problem】稿件已证明同一 rescue 轴可被临床免疫抑制药 prednisone 推高（即该代理不能区分"免疫刺激恢复"与"免疫抑制转录扰动"），却仍在结论层把 lenalidomide / azithromycin 的 L1000 排名作为"拯救 Mars1-down 轴"的支撑。

【Evidence】稿件 §3.9（"糖皮质激素免疫抑制药 prednisone 可在同一轴上得高分……L1000 'rescue' 代理不是免疫恢复的已验证标志"）与同节及 §6（"lenalidomide（top 26.6%）和 azithromycin（≈中位），方向为正但温和"）并存；`S08_l1000_candidate_scores.csv` 确认排名 5435 / 9152。

【Why it matters】在证明指标可被免疫抑制药混淆后，仍用其排名支撑候选药，会夸大临床前依据，使"优先化"看似建立在已被证伪有效性的评分之上。

【Specific fix】显式声明：鉴于 prednisone 混淆，两小分子的 L1000 排名不计入"功能免疫恢复"证据层级，仅作弱方向性交叉验证；优先化权重应明确落到机制一致性（表 2）与文献/RCT 证据（S08b），并在 §6 相应降调。

---

### 问题 4 —【摘要"主要 28 天死亡结局无因果支持"头面准确，但弱化了实际 MR 图景，存在轻微自相矛盾】

【Problem】摘要头面"two-sample MR gave no causal support on the primary 28-day-death outcome"对 IVW 成立，但易被读作"MR 整体为零"，而数据实际包含一项 Egger 名义显著与一项 family 显著却反向。

【Evidence】`10_genetics_mr_outcome5086_28ddeath.csv`：CD14 MR-Egger P=0.0488（family q=0.73）；`10_mr_bh_family.csv`：CD74 critical-care WM q=2.99e-17（OR 2.19，方向反向于 Mars1 模型）。稿件 §3.10、抽象、结论均反复强调"无因果支持"。

【Why it matters】精确读者可能认为作者隐藏了显著 MR 结果；诚实框架应是"主 IVW 为零、一项 Egger 名义显著但未过家族校正、一项 family 显著却反向"。

【Specific fix】将摘要该句改为："主要 28 天死亡 IVW 无显著支持（最小 P=0.24）；唯一 family 显著 MR 信号反向（CD74 危重），归为基因型–严重程度关联；CD14 MR-Egger 名义显著（P=0.049）但未过 45 检验家族校正。"

---

### 问题 5（轻微）—【"独立 / 诚实外部验证"头面与"标签不独立"披露并存，头面略夸独立性】

【Problem】标题与摘要反复用 "honest / independent external validation"，而正文 §3.5 与局限 1 披露"独立于队列与平台但不独立于标签"，头面未带此限定。

【Evidence】稿件摘要第 14 行、§3.5 第 112 行、局限 1 第 194 行。

【Why it matters】独立性的头面表述若不带"方向由发现队列标签训练"的限定，会略夸验证的独立性，尽管正文已诚实披露。

【Specific fix】在摘要首句及结论相应处加限定语"跨队列、跨平台，但方向性由发现队列 28 天标签训练（标签不独立）"。

---

## 二、§ Stands up（≥3，附证据）

1. **所有可核验头面数字本人重算一致。** 外部 AUC 0.638（CI 0.532–0.748，n=106，52 deaths）与 `09_external_validation.csv` 逐字一致；校准 slope 0.5028 / intercept −0.0382，且该表无 CI 列（与"未声明 CI"一致）；DCA 0.30 首超、0.80 模型 0 / treat-all −1.55 与 `09_ext_dca_grid.csv` 一致；Mars1 vs Mars2/3/4 本人以 Mann–Whitney U（正态近似+结校正）基于 `S02` 全量重算得 P=0.467 / ≈1.9e-18（z=−8.77）/ 1.3e-3，与稿中 0.47 / 1.9e-18 / 1.3e-3 吻合；`S01_mars1_deg.csv` 中 DEG_0.3=True 计数 = 3597，与稿中 3597 一致；MR 主要 IVW OR 0.923–1.119、最小 P=0.236；27 工具（3/4/6/6/8）构成正确；L1000 排名 5435 / 9152 正确。

2. **校准术语已修正为正确方向。** slope<1 被解释为"过自信"（over-confident）而非"欠拟合"，与临床预测校准惯例（校准斜率<1 = 预测过于极端）一致，稿中 §3.5 表述无误。

3. **CD74 critical-care 反向信号被正确降级。** §3.10、表 4、局限 2 一致地把它归为"基因型–严重程度关联而非因果枢纽主张"，并披露其仅 3 工具且存在样本重叠——反向结果未被包装成支持证据，处理诚实。

4. **样本重叠偏倚方向陈述正确。** 稿中"SE 下偏、一类错误风险上升"与 Burgess 2016 的样本重叠结论一致，方向无误。

5. **45 检验 BH 框架建立在"重叠假设结构"而非 LD 上，属正确表述。** CD74（chr5q32）与 HLA-DQA1（chr6p21.32）不同染色体，稿件未做 LD 主张，仅以"同基因×多估计量×多结局"的重叠结构立论；且 45>15 使 BH 阈值更严，方向保守。此点正确，可作为站得住的项。

---

## 三、§ Questions for the authors

- 能否提供第三队列或训练/验证分割下的校准（截距/斜率），以支撑 DCA 的临床解读，而不仅是在测试集内拟合？
- 鉴于 prednisone 混淆已证伪该代理的"免疫恢复"含义，是否愿意把两小分子的 L1000 排名明确移出"功能恢复"证据层级？
- DCA 在 0.10–0.25 与 treat-all 完全重合，是否考虑报告"模型相对 treat-all 的净增益（模型 NB − treat-all NB）曲线"而非绝对 NB，以更诚实地呈现边际收益？
- CD74 critical-care WM 反向且在 3 工具 + 样本重叠下"显著"，是否计划在独立 eQTL / 独立结局中复制后再作任何主张？

---

## 四、§ What I actually checked

- **读取文件**：`_PANEL_BRIEF.md`、`manuscript.md`，以及 `09_external_validation.csv`、`09_ext_calibration_dca.csv`、`09_ext_dca_grid.csv`、`S02_immunoparalysis_score.csv`、`S01_mars1_deg.csv`、`S08_l1000_candidate_scores.csv`、`08_candidates_drugs.csv`、`10_genetics_mr_outcome5086_28ddeath.csv`、`10_mr_bh_family.csv`、`10_genetics_mr.csv`。
- **重算**：基于 `S02` 全量（按 endotype 分组）以 Mann–Whitney U（正态近似 + 结校正）重算 Mars1 vs Mars2/3/4 → 0.467 / ≈1.9e-18 / 1.3e-3；基于 `S01_mars1_deg.csv` 计数 DEG_0.3=True → 3597。
- **核对一致性**：外部 AUC / CI / n / deaths；校准 slope / intercept 且无 CI；DCA 网格首超阈值与 0.80 值；MR 主要 IVW OR 区间与最小 P；27 工具构成；L1000 两排名——均与源文件逐字一致，**未发现任何数值冲突**。
- **依独立性纪律未读**：`REVIEW_round*`、`review_r12`–`review_r15`、`.workbuddy/memory`、`scirep_submission_checklist.md`、其他 `review_r16` 文件。
- **结论**：本稿无算错或数值造假；问题集中在设计层表述与框架（DCA 头面化、测试集聚类校准、L1000 反例张力、MR 头面弱化、独立性措辞），均为可经文字修订解决的项，无方法学硬伤。

---

## 五、VERDICT

**Minor** — 所有可核验头面数字本人重算一致，校准术语与 MR 框架正确且诚实；剩余问题均为设计层框架/表述夸大与一处测试集聚类校准，可在不补实验前提下以文字修正解决，无数值错误或方法学硬伤，不足以构成 Major 或 Desk-reject。
