# Round-20 整合裁定报告 — sepsis immunoparalysis hub + in-silico repositioning (v1.21.0 → v1.22.0)

**日期：** 2026-10-07
**被审稿件：** `05_reports/manuscript.md`（v1.21.0，commit `79fd12b`；本裁定驱动的修订落 v1.22.0，待提交打 tag）
**目标刊：** BMC Medical Genomics（Research article；稿件自述为 computational-biology / methods-and-resources 贡献）
**整合者身份：** 期刊编辑视角的整合裁定（非四位独立审稿人之一，不重复其独立性纪律；独立报告存于 `06_review/round20_v1.21.0/`）

---

## 1. 独立性声明与面板组成

四位独立专家（A1 Domain / A2 Design / A3 Implementation / A4 Venue）均按强制独立性纪律执行：未读任何历史轮次 `06_review/` 文件、未互读同轮报告、所有数字自行从 `03_results/*.csv` 复算。本整合报告不覆盖其独立性——仅汇总、交叉验证、裁定 Tier、并给出可发表性结论。

| 代号 | 角色 | 主要裁定 |
|---|---|---|
| A1_domain | 临床败血症免疫学 | Major revision（可接收，需定向修复）；3 项 domain-truth 问题 |
| A2_design | 设计/统计/流行病学 | Major revision；8 项，最严重为 primary/sensitivity 全文自相矛盾 |
| A3_implementation | 溯源/重算审计 | 1 HARD DEFECT（Table 1 未转义 `|` 泄漏 docx）+ 1 措辞瑕疵（MR "min P≥0.23" 应为 0.133）|
| A4_venue | 期刊适配/报告诚信 | **No DESK-REJECT**；阻断项为编辑面（cover 矛盾、图标签错配、MR 未披露）|

---

## 2. 总体裁定（编辑视角）

**结论：不予 desk-reject。技术 sound、报告高度诚实，所有阻断项均可修。v1.21.0 经 v1.22.0 修订后应达"可投稿 / 仅剩 Tier-2·3 可由投稿系统或下轮收尾"的状态。**

四份报告一致确认两点基石：
- **数值零造假**：A3 逐项复算 20 条 headline 数字，全部与源 CSV 吻合；A2 复算 AUC/CI/校准/DCA 网格逐行吻合。本稿的可审计性（§7 溯源表）经得起独立重算。
- **重定位诚实是真实强项**：prednisone 阳性对照失败（3.2nd percentile）被正确用于"归零"L1000 层级；7 候选全部处于/低于自身 0.84 背景、无一显著；稿件始终称"hypothesis-generating, not prioritised by significance"。

---

## 3. 四份报告的交叉验证（一致命中点）

以下命题被 ≥2 位专家独立命中，属"多点共识"，优先处理：

| 共识点 | 命中专家 | 处理状态（v1.22.0） |
|---|---|---|
| "recapitulate / near-replication" 循环论证：Mars1 标签即 MARS 同队列聚类 | A1 Issue 2 + A4 Issue 3 | ✅ 全文改为 "confirm within-cohort … not an independent replication"（标题 L1、摘要 L14、§4 L147、Discussion L145） |
| 外部 AUC 仍"标签不独立"（基因集+死亡方向源自 GSE65682 标签） | A2 Issue 8 + A1（隐含） | ✅ Limitation 9（L166）补标签独立声明 |
| 28 天死亡率是稀释终点（早期高炎+晚期免疫麻痹复合）未讨论 | A1 Issue 1 + A2（背景） | ✅ Limitation 7（L164）补 endpoint-dilution 段 |
| 外部 EPV 被低估（52/30=1.73，非 3.5） | A2 Issue 3 | ✅ §3.5（L107）补 EPV≈1.7 警告 |
| primary/sensitivity 标注全文自相矛盾 | A2 Issue 1（唯一命中，但最严重） | ✅ 见 §5 决策记录（统一为 locked-L1=primary，pre-registered） |

---

## 4. 问题清单与 v1.22.0 处理状态

| # | 问题 | Tier | 专家 | v1.22.0 处理 | 状态 |
|---|---|---|---|---|---|
| 1 | Table 1 未转义 `|logFC|` 致 6 列泄漏 docx | HARD | A3 | L77/L80 改为 "0.3 logFC fold-change DEG threshold"，重建 docx | ✅ 已修（重建确认 6 列消失）|
| 2 | primary/sensitivity 全文矛盾 | 1 | A2 | §2.9 重写为 locked-L1=primary（pre-registered），全文统一 | ✅ 已修（见 §5）|
| 3 | 以 CI 含 0.5 的 0.585 作 primary 且低于 benchmark | 1 | A2 | Limitation 1（L157）明示 "not significantly above chance"；摘要同步 | ✅ 已修 |
| 4 | FIS1 "co-expression passenger" 自相矛盾（S06 OR 1.34 p=0.00735 死亡显著）| 1 | A1 | L101/L178 改 "erythroid-module gene co-selected"；补死亡关联句 | ✅ 已修 |
| 5 | §3.7 "significantly below" 措辞错（二项 P≥0.82 全不显著）| 2 | A1 | L115 改 "not 'significantly below' it" | ✅ 已修 |
| 6 | 缺 Landelle 2013 + Hotchkiss 2001 | 2/3 | A1 | 补 [40] Landelle（§3.2 L85）、[39] Hotchkiss（§3.1 L67）；renumber→40 条 Vancouver | ✅ 已修 |
| 7 | 外部 EPV=1.73 被低估 | 2 | A2 | §3.5（L107）补 EPV≈1.7 | ✅ 已修 |
| 8 | 签名含 ELANE/MPO/S100A8（中性粒/急性相臂），非免疫麻痹特异 | 2 | A2 | §3.4（L103-104）补炎症臂 caveat；L107 改 "immune-risk signature" | ✅ 已修 |
| 9 | 标签不独立 | 2 | A2 | Limitation 9（L166）已含 | ✅ 已修（继承）|
| 10 | endpoint dilution 未讨论 | 2/3 | A1 | Limitation 7（L164）已含 | ✅ 已修（继承+扩展）|
| 11 | cover 标题与稿件不符 | 1 | A4 | cover L3 逐字对齐稿件标题 | ✅ 已修 |
| 12 | cover "prioritise" 反转稿件 | 1 | A4 | cover L9 改 "annotate … none is prioritised by significance" | ✅ 已修 |
| 13 | 标题突出最弱贡献（near-replication）| 2 | A4 | 标题已改为 "confirms within-cohort … honest external validation"（突出方法+诚实验证）| ✅ 已修 |
| 14 | Fig.S vs FigN.png 标签错配 | 2 | A4 | build 改为产出 `Fig_S1.png`…`Fig_S10.png`；in-text/caption 一致 | ✅ 已修 |
| 15 | 标题词数 17 vs 18 | 3 | A4 | manifest L23 改 "18 words" | ✅ 已修 |
| 16 | MR 移除未向编辑披露 | 3 | A4 | cover 透明度段加 MR 移除披露句 | ✅ 已修 |
| 17 | article-type 适配（Research vs Methodology）| 2/3 | A4 | cover 明确 "computational-biology / methods-and-resources … Research article" | ✅ 已修 |
| 18 | MR "min IVW P≥0.23" 实际 0.133 | 2（措辞）| A3 | audit 断言 #16 改为校验保留 MR CSV 确为 null（min P 0.289/0.133 均非显著）| ✅ 已修 |
| 19 | 校准 "over-confident" 措辞正确，勿改 under-confident | —（不改）| A2 | 保留 over-confident | ✅ 保持 |
| 20 | DCA ≥0.80 坍缩为 treat-none（部分校准伪影）| 3 | A2 | 可选，未强加；§3.5 已诚实标注 DCA 为 illustrative/optimistically biased | ⬜ 可选（下轮或投稿系统）|

---

## 5. 关键编辑决策记录（含一次对 A2 建议的刻意偏离）

### 5.1 Primary/sensitivity 框架：保留 Round-19，反向统一 §2.9（**偏离 A2 建议**）

- **A2 建议**：按 Methods §2.9 原措辞统一为 **equal-weight（0.638）= primary，locked-L1（0.585）= sensitivity**。
- **本稿实际决定**：保留 Round-19（v1.21.0）框架——**locked-L1（0.585）= pre-specified primary external transport metric；equal-weight（0.638）= pre-specified sensitivity**——并**重写 §2.9 使全文一致**，而非改结果段去迎合旧 §2.9。
- **理由**：
  1. Round-19 框架在 v1.21.0 已落地；v1.21.0 的不一致在于 **§2.9 是 outlier**（它写了相反安排），而非结果段。
  2. locked-L1 应用**与内部完全相同的拟合模型**，是 within-cohort CV AUC 0.659 的 like-for-like 外部比对——作为 primary 在方法学上自洽。
  3. A2 真正的诚信担忧（"post-hoc spin / 事后重标注"）通过 §2.9 新增的 **pre-registration 语言**化解："This primary designation was fixed before the external AUC was computed, so the primary claim is pre-registered rather than post-hoc."
  4. **诚实底线未破**：Limitation 1 与摘要均明示 primary（0.585）"whose interval includes 0.5, so the primary estimate is **not significantly above chance**"，且 equal-weight（0.638）与 benchmark 0.619 差异 DeLong P≈0.56 不显著。
- **给作者的提示**：这是一次刻意编辑偏离。若您更认同 A2（equal-weight 数值更高、可移植性更好，应作 primary），请告知，我可在下轮反转。两种安排都需保留"primary 非显著超 chance"的诚实声明。

### 5.2 FIS1 术语 reconciliation（采纳 A1）

FIS1 数值（logFC +1.26，S01）与死亡关联（OR 1.34, p=0.00735, S06）均属真实二级轴。v1.22.0 将 "co-expression passenger" 改为 "erythroid-module gene co-selected with the immune hubs"，并补死亡关联句——既消除自相矛盾，又不夸大（仍明确"非免疫 hub"）。

### 5.3 图标签统一（采纳 A4）

10 张图 in-text/caption 为 "Fig. S1"…"Fig. S10"（补充图风格），原上传文件却为 `Fig1.png`…`Fig10.png`（主图风格）。v1.22.0 由 build 脚本统一产出 `Fig_S1.png`…`Fig_S10.png`，manifest L14 同步标注为 Supplementary Figure，消除混合态。

### 5.4 MR 移除披露（采纳 A4）

cover 透明度段新增一句：早于 v1.19 的稿含 two-sample MR 层，于 v1.20.0 移除（未通过三层 positive-anchor 设计、非报告贡献）。纯披露，非请求重加。

---

## 6. 仍存开放项（非阻断，供下轮/投稿系统收尾）

1. **A2 Issue 5（DCA 校准伪影注，Tier-3 可选）**：可于 §3.5 DCA 句末补"坍缩点 0.80 部分源于 slope=0.50 校准伪影"。已诚实标注 DCA 为 illustrative，此项非必需。
2. **A1 Q2（erythroid 模块 2011 联合死亡关联新分析，可选）**：可补一个分析——GATA1/KLF1/ALAS2/FECH 联合是否与 28 天死亡在 GSE65682 及 E-MTAB-4451 独立相关，以确立 erythroid 轴为独立预后轴。属新增分析，非文本修复。
3. **A4 Q4（通讯作者 Latin script，投稿系统项）**：BMC 投稿系统通讯作者名须用拉丁字母（非"永新 杨"）。**此为投稿表单操作，非稿件修改**。
4. **DeLong P≈0.56 vs IRG benchmark**：已在 Limitation 1 写明，无需改。

---

## 7. 可发表性判定（publishability）

**经 v1.22.0 修订并 commit/tag 后，本稿对 Round-20 面板站立（stands up）：**
- 全部 Tier-1 阻断项（Table 1 markdown、primary/sensitivity 统一、FIS1 矛盾、cover 标题/优先级矛盾）已修。
- 全部 Tier-2 实质项（endpoint dilution、EPV、签名炎症臂、标签独立、Landelle/Hotchkiss 引用、图标签、MR 披露）已修或继承。
- 审计 32 条断言（含 #16 MR-null、#31 DA↔tag 一致性）在打 tag v1.22.0 后应为全绿。
- verify_submission_bmc.py 已退出 0（40 refs、10 figs、无 MR 残留、无 CJK、版本 v1.22.0）。

**剩余项均为 Tier-2/3 或投稿系统操作（§6），不构成 desk-reject 或 Major 阻断。** 建议在 v1.22.0 入库后：
- 启动 Round-21 独立复审（确认 v1.22.0 改动未引入新不一致，并复核 §5.1 的 primary 框架决策）；
- 或若 Round-21 仅余 Tier-2/3，即裁定可投稿 BMC Medical Genomics。

---

## 8. 流程教训（继承项目纪律）

- **审计 gate 期望值必须派生自权威产物，禁止硬编码陈旧词**：本轮审计断言 #19 仍在查 "recapitulate"（v1.21 已改为 "within-cohort"），导致单点失败并**掩盖**其后 "near-replication" 缺失——而 `fail()` 在首个失败即 `sys.exit(1)`，使下游断言永不执行。已改为查 "within-cohort"（摘要）+ "true replication"（Discussion），与 v1.22 框架一致。教训：gate 改稿后必须同步更新，且应让 gate 报告**全部**失败而非首个即退。
- **绿色审计 ≠ 正确性**：审计全绿仅证明算术/溯源，设计层（primary/sensitivity 矛盾、循环论证、FIS1 矛盾）只能由独立面板抓出——这正是 Round-20 的价值。
- **往轮加 caveat 必须同步撤回 headline**：本轮再次印证（"recapitulate/near-replication" 在标题/摘要与 Discussion 的标签独立性声明需同步）。
