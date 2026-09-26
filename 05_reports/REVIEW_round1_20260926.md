# REVIEW · Round 1 (2026-09-26) — 独立多专家评审整合报告

**被评审稿件**：`05_reports/manuscript.md`（v1.0.2，复现包已 commit，未 push）
**研究**：脓毒症 MARS 免疫抑制型（Mars1）枢纽基因 + in-silico 虚拟敲除药物重定位（单作者，纯公共数据再分析）
**评审机制**：5 名独立专家（互不读取彼此输出），按 `_PANEL_BRIEF.md` 的独立性纪律评审，主编（小团）事后核对并亲自验证最严重发现后整合
**专家文件**：`05_reports/review/A1_domain.md` · `A2_design.md` · `A3_implementation.md` · `A4_venue.md` · `A5_drugrepurposing.md`

---

## 1. 独立性声明（Independence statement）

- **机制**：5 名专家在独立子代理中运行，互不可见彼此输出与历史评审文件；共享输入仅为 `_PANEL_BRIEF.md`（含禁止文件清单、输出契约、必查数字清单）。每位专家按"首次投稿"视角审查，凡可验证数字均亲自重算或核对源 CSV。
- **独立性生效的证据**：多位专家在**无互通**情况下命中同一缺陷——§3.1 Table 1 数字不符被 A1(F1)、A2(F10)、A3(F1) 三路独立指出；IRG 双值被 A2(F2)、A3(F5)、A4 共同指出；lenalidomide `wtcs` 被 A3(F3)、A5(发现8) 共同指出；MR 样本重叠被 A2(F3) 单独（设计层）指出。这种"不同角度撞同一缺陷"正是独立性有效的诊断标志。
- **主编亲自验证**：见 §3 与 §4 标注 "independently confirmed by editor"。

---

## 2. 评审团 Verdict 表

| 专家 | 专长层 | 总体 verdict | 最高危发现 |
|---|---|---|---|
| **A1** | 脓毒症/免疫学临床 | 临床claim大体合理；**核心可复现性硬伤（Table 1）须修**；证据强度措辞需校准 | F1 Table 1 不可溯源 |
| **A2** | 生物信息统计 + MR 因果 | **三大重点（F1/F2/F3）不修则方法学审稿人可合理拒稿**；加 F10 | F3 eQTLGen×UKB 样本重叠 |
| **A3** | 数字溯源/重算审计 | **F1 阻断级**（Table 1 整表不符）；另 10 项 minor 一致 | F1 Table 1 与源文件严重不符 |
| **A4** | 期刊编辑 + 报告规范 | 科学诚实性好；**报告规范与格式须返工**；JTM 偏高因 claim–evidence 失配 | F1 TRIPOD/DCA 缺失+隐藏 |
| **A5** | LINCS/L1000 药物重定位 | 框架合理诚实，但**四处方法学特异性缺陷，其中 2 处事实/定义错误须修才能送审** | 发现1 `rescue_fraction` 非真实靶点 |
| **主编** | 整合 + 亲自验证 | **需重大修订（Major Revision）**，送外审前必须修复 Tier 0/1；Table 1 数字诚信问题属 desk-reject 风险若不修 | — |

**分布**：Tier 0：3 项 · Tier 1：10 项 · Tier 2：15 项 · Tier 3：8 项（见 §4）。

---

## 3. 跨验证表（Cross-verification table — 最高价值产物）

稿件值 vs 从原始结果文件独立重算值；✅一致 / ❌不符 / ⚠️需澄清。

| # | 稿件位置 | 稿件声称 | 源文件重算/实测值 | 检查者 | 判定 |
|---|---|---|---|---|---|
| CV-1 | §3.1 Table 1 · HLA-DRB1 | Δ=−0.59, P=9.7e-09 | −0.8925, adj.P=1.07e-15 | A1/A2/A3/**主编** | ❌ |
| CV-2 | §3.1 Table 1 · CD74 | −0.48, 8.2e-09 | −0.7578, 2.08e-15 | A1/A2/A3 | ❌ |
| CV-3 | §3.1 Table 1 · CD14 | −0.77, 1.3e-17 | −0.7657, P≈0（下溢） | A1/A2/A3 | logFC✓ / P量级异 |
| CV-4 | §3.1 Table 1 · ITGAM | −0.48, 7.0e-12 "显著" | −0.2084, adj.P=1.68e-3（**不显著**） | A1/A2/A3 | ❌且"显著"误标 |
| CV-5 | §3.1 Table 1 · HAVCR2 | −0.39, 1.7e-16 | −0.3488, 2.84e-13 | A2/A3 | ❌ |
| CV-6 | §3.1 Table 1 · HLA-DRA | −0.18, 3.5e-02 | −0.4689, 3.77e-07 | A2/A3 | ❌ |
| CV-7 | §3.1 Table 1 · LYZ | −0.21, 2.9e-04 | −0.2561, 3.56e-06 | A2/A3 | ❌ |
| CV-8 | §3.1 "21 directionally down" | 21 | **23**（Mars1_down；22 显著；21 为"下调且显著"子集） | A1/A3/**主编** | ❌应为23 |
| CV-9 | §3.9 lenalidomide `wtcs` | 1.17 | **0.2058**（`S08_l1000_candidate_scores.csv`） | A3/A5/**主编** | ❌ |
| CV-10 | §2.6/§3.4 vs §3.5 IRG bench (E-MTAB-4451) | 0.619 与 0.604 并存 | 0.619=Peng 2023 原报；0.604=本稿重算，**均真实** | A2/A3/A4 | ⚠️需显式区分 |
| CV-11 | §3.4 / §7 CV AUC | 0.659 | 0.6586（`S06_auc_compare.csv`） | A3 | ✅四舍五入一致 |
| CV-12 | §3.5 外部 AUC | 0.638 (0.532–0.748) | 0.6382 (0.5317–0.7475) | A3 | ✅一致 |
| CV-13 | §3.5 锁定 L1 AUC | 0.585 (0.469–0.696) | 0.5848 (0.4687–0.6959) | A3 | ✅一致 |
| CV-14 | §3.7 Table 2 · 7 候选 rescue | IL-7 1.00 … BCG 0.20 | 与 `08_candidates_drugs.csv` 完全一致 | A3 | ✅一致 |
| CV-15 | §3.6 细胞定位 r 值 | CD14 0.77 等 | 与 `07_hub_celltype.csv` 一致 | A3 | ✅一致 |
| CV-16 | §3.10 MR Table 3/4 OR/CI/P | 见正文 | 与 `10_genetics_mr*.csv` 全部一致 | A3 | ✅一致 |
| CV-17 | §2.1 样本构成 | 802/760/42/479 | 与 `GSE65682_pheno.csv` 一致 | A3 | ✅一致 |
| CV-18 | §3.1 DEG 计数 | 3597 / 448 | 与 `S01_mars1_deg.csv` / `S01_deg_sepsis_vs_ctrl.csv` 行数一致 | A2/A3 | ✅一致 |

**主编亲自验证结论（independently confirmed by editor）**：用脚本直接读取 `S01_immunoparalysis_direction.csv` 与 `S01_mars1_deg.csv`（二者该 8 基因数值彼此一致），确认 CV-1~CV-7 中 **7/8 基因的 logFC 与 P 值与稿件 Table 1 严重不符**（仅 CD14 的 logFC 对得上）；CV-8 的"21 方向性下调"实为 23；CV-9 的 `wtcs` 实测 0.2058。CV-10 两值均真实、属口径未澄清而非计算错误。**Table 1 数字并非"引用错源文件"——两个候选源文件都不含稿件中的数值，属数字本身错误（疑似早期草稿/不同预处理版本遗留）。**

---

## 4. 分级整合问题清单（Graded consolidated issue list）

去重后按严重度分级；每条附证据（manuscript.md:行号 + 源文件）与指向专家文件的修正。

### Tier 0 — 结论无效化 / 阻断级（送审前必须修复，否则 desk-reject 风险）

**T0-1 · §3.1 Table 1 整表数字与源文件不符（含摘要复述）**
- 证据：manuscript.md:85-94（Table 1）、:13/:24（摘要复述）；源 `S03_results/S01_immunoparalysis_direction.csv` 与 `S01_mars1_deg.csv`（两文件一致，但与稿件不符，见 CV-1~CV-7）。主编亲自验证确认。
- 影响：稿件核心卖点即"每个数字可溯源（§7）"。Table 1 是免疫麻痹主效应的唯一展示表，数字不可溯源直接击穿可信度；若编辑/审稿人核对即触发拒稿。
- 修正：以 `S01_immunoparalysis_direction.csv` 的真实值重写 Table 1（HLA-DRB1 −0.89/2.2e-16、CD74 −0.76/2.1e-15、CD14 −0.77/≈0、FCGR3A −0.61/9.1e-11、ITGAM −0.21/1.7e-3、HAVCR2 −0.35/2.8e-13、HLA-DRA −0.47/3.8e-7、LYZ −0.26/3.6e-6），并同步修正 §7 溯源表与摘要中的复述值；ITGAM 不可再标"显著"。详见 A1 F1 / A2 F10 / A3 F1。

**T0-2 · 药物重定位方法学的"靶点"定义失真 + 阳性对照循环验证 + 虚拟敲除名不副实**
- 证据：manuscript.md:63（§2.8）、:116（§3.7）、:102（§3.3）；`02_scripts/python/08_virtual_ko_cmap.py:34-56` 的 `DRUG_MAP` 显示 IL-7 的"target"实为 CD3D/E/CD8A/IL7R/LCK（下游响应基因，真实受体是 IL7R/JAK3），GM-CSF 的"target"是髓系响应基因（真实受体 CSF2RA/CSF2RB）；§3.3 承认"virtual knockdown"等价于"hub 本身下调"。详见 A5 发现1/6/7、A4 F12。
- 影响：`rescue_fraction` 用"下游响应基因集"代替"真实分子靶点"，使任何 broadly 上调免疫基因的药都得高分，把"重定位证据"降级为"机制注释"；IFN-γ 阳性对照因靶列表手工填入那 5 个抗原呈递基因而按构造必过（循环验证）；"虚拟敲除满足阳性对照"无真实 CRISPR-KO 签名支撑。三者叠加，S08 药物重定位层可信度受损。
- 修正：用 DGIdb/ChEMBL 拉取真实直接靶点重算 `rescue_fraction`（更名 `target-overlap concordance`）并加 Fisher/超几何检验；IFN-γ 改为独立阳性 + 非免疫阴性双向对照；§3.3 的"virtual knockdown positive control"若无实证产物须降级为"逻辑自洽性论证"并显式声明。详见 A5 发现1（含可粘贴英文 fix）。

**T0-3 · MR 暴露–结局样本重叠（eQTLGen × UK Biobank）未讨论**
- 证据：manuscript.md:68-71（§2.10）；eQTLGen（Visser et al. 2021, Nat Genet；31,684 例，含 UK Biobank 队列）与结局 `ieu-b-5086/4980/4982`（UK Biobank 脓毒症 GWAS）极可能共享样本。详见 A2 F3。
- 影响：暴露与结局样本重叠会产生相关性偏倚与弱工具假象，是 eQTL-MR 经典陷阱。稿件将 S10 标为 Tier-3 提示性，故非结论无效化，但**遗漏此披露属方法学硬伤**，审稿人会据此质疑 MR 层全部估计。
- 修正：披露重叠规模（若可量化），说明是否/如何校正（如留一法、或引用同队列 eQTL 偏倚文献），并将"提示性"框定收紧。详见 A2 F3。

### Tier 1 — 须补分析 / 重大（重大修订，强烈建议修）

- **T1-1 · 30-gene 签名乐观偏倚**：基因选择与定向在含全部 death 标签的全队列完成，5-fold CV 0.659 仍泄漏标签；诚实泛化值是外部 0.638。补 nested CV 或将外部 0.638 作为头条。详见 A2 F1。
- **T1-2 · IRG 基准同队列双值澄清**：§2.6/§3.4 写 0.619、§3.5/摘要/§7 写 0.604（均真实，前者 Peng 原报、后者本稿重算）。每处显式标注来源并补 0.604 的 CI，避免"超过基准"论断脆弱（跨队列 + IRG 无 CI）。详见 A2 F2 / A3 F5。
- **T1-3 · `rescue_fraction` 重定义为真实靶点 + 统计检验**（同 T0-2 的方法学修复）。
- **T1-4 · §3.9 L1000 query 集合定义错误**：真实 query 是"25 共识免疫基因中可测的 22 个"，混入 PDCD1、LAG3 两个 Mars1-up 耗竭基因，且漏掉 HAVCR2、FCGR3A 两个 hub。须 signed 重定义。详见 A5 发现2。
- **T1-5 · lenalidomide `wtcs` 1.17 → 0.2058**（CV-9，主编验证）。
- **T1-6 · §3.1 "21 方向性下调" → 23**（CV-8，主编验证）；并区分"方向性下调总数(23)"与"下调且显著(21)"。
- **T1-7 · §3.9 把 LINCS "BRD-" 前缀误当"BET 抑制剂"**：Top 救援剂是 BRD- 匿名 Broad ID，须逐一解析真实药理身份后再下结论。详见 A5 发现3。
- **T1-8 · 孤儿图 / TRIPOD 缺失 + DCA 已生成却未引用**：`04_figures/S06_dca.png` 已存在但未纳入正文；预测模型缺校准曲线与决策曲线。详见 A4 F1/F6。
- **T1-9 · STROBE-MR 缺失协调剔除计数**：harmonised 表无 palindromic/链模糊/等位不相容各自剔除列；须补。详见 A4 F2。
- **T1-10 · L1000 仅覆盖 2/7 候选（小分子）**：IL-7/GM-CSF/IFN-γ/胸腺肽α1/BCG 不在 `trt_cp`，连接度证据只覆盖小分子；claim 须显式限定。详见 A5 发现5。

### Tier 2 — 措辞 / 中等（修订轮处理）

- **T2-1** IL-7/GM-CSF "carry the strongest sepsis RCT evidence" 夸大（GM-CSF RCT 多中性/阴性，IL-7 仅 pilot）。A1 F2。
- **T2-2** "IFN-γ is an approved MHC-II inducer" 措辞不精确，易误读为以该身份获批用于脓毒症。A1 F3。
- **T2-3** §4 把"计算提名"外推为"哪类 Mars1 患者最可能从某药获益"的临床分层处方，缺本研究证据支撑。A1 F4。
- **T2-4** headline 与 §5 自相矛盾：§3.4"predicts"、§6"druggable"、§4"best published" 与 modest/对接未做的自限冲突。A4 F3。
- **T2-5** 参考文献遗漏脓毒症免疫治疗 RCT 对立证据（核心强弱判断缺反证）。A1 F5。
- **T2-6** 28-day mortality 作为唯一主终点，未提 90-day mortality 趋势。A1 F8。
- **T2-7** IFN-γ "4/5 抗原呈递基因"与 `08_candidates_drugs.csv` 的 5/5 内部矛盾。A3 F4。
- **T2-8** §3.2 "中位 −0.79；range −3.65~3.86" 混用 Mars1 亚组中位与全队列范围；"progressively ordered" 夸大。A3 F6。
- **T2-9** 正文 author-year 引用 vs 目标期刊要求的 numbered 引用体例冲突。A4 F5。
- **T2-10** MR "仅 Egger 显著"表述须更克制（虽 FDR 框架正确，A2 重算确认 CD14 Egger FDR=0.026 无误）。A2 F4。
- **T2-11** 弱工具：CD74 critical-care 仅 3 IVs 仍偏脆弱。A2 F5。
- **T2-12** 阳性对照门控缺选择性/特异性量化（在随机药物集上的通过率=假阳性率）。A2 F7 / A5 发现6。
- **T2-13** 阈值 |logFC|≥0.3 与 top-2000 hub 选择的双重蘸取。A2 F8。
- **T2-14** 链式选择缺失家族-wise 误差控制（需独立队列复现 hub 共表达结构）。A2 F9。
- **T2-15** §3.8 引用 "Table S2" 但未作为补充表呈现。A3 F10。

### Tier 3 — 格式 / 小（排版或投稿准备）

- **T3-1** 参考文献 1–29 映射建议自动化核对。A3 F9。
- **T3-2** §8 "delete before submission" 须确认投稿包中实际移除。A3 F11 / A4 F8。
- **T3-3** Data availability "to be created at acceptance" 合规风险，建议投稿时即提供预注册仓库或实时 DOI。A4 F9。
- **T3-4** 缺通讯作者邮箱；中文摘要对英文刊冗余。A4 F7。
- **T3-5** 缺 cover letter，须写且与"提示性 MR/设计稿验证"语气一致、不夸大。A4 F11。
- **T3-6** CV-AUC 在两文件微差 0.65856 vs 0.6582，统一口径。A3 F7。
- **T3-7** GWAS 病例/对照计数不在结果 CSV，需 run-log 佐证。A3 F8。
- **T3-8** Ethics/Author contributions/Funding/COI 与单作者基本一致（可小补强）。A4 F10。

---

## 5. 共识 / 互补 / 分歧

**Consensus（共识）**
- 稿件科学诚实性**总体良好**：MR 一致框定为 Tier-3 提示性、功能验证明确标注设计稿、外部验证真实落地、S09 对接未做已诚实声明。
- §3.1 Table 1 数字诚信是**头号阻断问题**（A1+A2+A3+主编四路一致）。
- IRG 双值、lenalidomide wtcs、21/23 计数为明确数字错误（多路一致）。

**Complementarity（互补）**
- A1 提供临床/文献维度，A2 提供统计/因果维度，A3 提供逐数字审计，A4 提供期刊/规范维度，A5 提供重定位方法学维度——五层恰好覆盖 design/implementation/venue/domain 全谱，无重大遗漏层。

**Disagreement（分歧，保留并裁决）**
- **JTM 7.5 Q1 是否偏高**：A4 认为"学科范围不偏高，偏高的是 claim–evidence 失配与规范完备度，应修规范而非降级期刊"；A2 倾向降档到 Front Immunol/Scientific Reports/Shock。裁决：**采纳 A4 的"先收敛 headline + 补规范，再投 JTM"路径**；但若 T0/T1 修复周期长，可暂以 Scientific Reports（3.9 Q1，已核实 SCIE）作为稳妥首投，JTM 作为补功能验证后的冲刺档。两专家均不反对"JTM 为靶刊可接受，前提是先完成规范整改"。
- **Table 1 是否"引用错源文件"**：A3 初判"与两个源文件均不符"，主编验证确认两候选源文件（direction 与 mars1deg）数值彼此一致且都不含稿件值 → 属**数字本身错误**而非引用错文件。采纳主编验证结论（更高置信）。

---

## 6. 优先 Must-fix 清单（含 DESK-REJECT 标记）

| 优先级 | 项 | 标记 | 动作 |
|---|---|---|---|
| P0 | T0-1 Table 1 数字重写（含摘要/§7 复述） | 🔴 **DESK-REJECT 风险** | 修数字源 + 同步摘要/溯源表 |
| P0 | T0-2 rescue_fraction 真实靶点 + 循环验证 + 虚拟敲除降级 | 🔴 | 重算 + 改 §2.8/§3.3/§3.7 |
| P0 | T0-3 MR 样本重叠披露 | 🟠 高危 | 补 §2.10/§3.10 披露 |
| P1 | T1-1 nested CV / 外部 0.638 头条 | 🟠 | 补分析 |
| P1 | T1-2 IRG 双值显式区分 + CI | 🟠 | 改表述 |
| P1 | T1-4 L1000 query signed 重定义 | 🟠 | 改脚本+正文 |
| P1 | T1-5 wtcs 1.17→0.2058 | 🟠 | 改数字 |
| P1 | T1-6 21→23 计数 | 🟠 | 改数字 |
| P1 | T1-7 BRD- 误为 BET 抑制剂 | 🟠 | 改表述 |
| P1 | T1-8 DCA/TRIPOD 纳入 | 🟠 | 补图+文 |
| P1 | T1-9 STROBE-MR 剔除计数 | 🟠 | 补表 |
| P1 | T1-10 L1000 仅 2/7 限定 | 🟡 | 改 claim 限定 |
| P2 | T2-1~T2-15 措辞/统计表述 | 🟡 | 修订轮 |
| P3 | T3-1~T3-8 格式/投稿准备 | 🟢 | 投稿前 |

**must add analysis vs must reword 拆分**：
- 须补分析：T1-1(nested CV)、T0-3(重叠量化)、T1-9(剔除计数)、T0-2(真实靶点重算)、T1-4(query 重定义)。
- 仅须改数字/措辞：T1-5、T1-6、T1-2、T2 全组、T3 全组（不改数字，只改表述/格式）。

---

## 7. What stands up（核查后稿件正确的部分 — 勿动）

以下经多位专家独立核对**正确**，修订时不应改动（A3 列 18 条 Stands-up，节选关键）：
- 样本构成 802/760/42/479（A3 F17）
- DEG 计数 3597（Mars1-vs-Other）/ 448（sepsis-vs-healthy）正确（A2/A3）
- 22/25 共识免疫基因 FDR<0.05 显著 正确（A3；注 23 个方向性下调）
- 6 hub 基因（CD74/HLA-DQA1/CD14/FCGR3A/HAVCR2/FIS1）正确（A3）
- 30-gene CV AUC 0.659 / 训练 0.750 正确（A3）
- 外部验证 AUC 0.638 (0.532–0.748) / 锁定 L1 0.585 正确（A3）
- 29/30 基因映射、E-MTAB-4451 数据口径正确（A3）
- 细胞定位 r 值正确（A3）
- 7 候选 rescue_fraction 计算正确（A3；仅"target"语义有误）
- MR Table 3/4 全部 OR/CI/P 与源 CSV 一致；CD14 Egger FDR=0.026、CD74 critical-care FDR≈0.21 重算无误；median F 正确（A2/A3）
- L1000 背景统计（mean/median 0.006、53.6%>0、20,413 化合物）正确（A5）
- FCGR3A 仅 2 IVs 排除正确（A2/A3）
- 糖皮质激素反向对照 caveats 充分（A2/A5）
- §8 "delete before submission" 标注正确存在（A3）
- 科学诚实性框架（Tier-1/2/3 正锚、MR 提示性、S09 不执行）获全体认可

---

## 8. 处理路径建议（Recommended handling paths）

- **路径 A（推荐）· 重构后重投同类型**：完成 P0+P1（修 Table 1 数字、rescue_fraction 真实靶点、MR 重叠披露、nested CV、IRG 澄清、L1000 query 修正、wtcs/计数修正、DCA/STROBE-MR 补规范），收敛 headline 到诚实边界，投 **Journal of Translational Medicine (7.5 Q1)**。A4 明确：JTM 学科范围不偏高，偏高的是规范完备度，修规范即可。
- **路径 B（稳妥首投）· 降档**：若 P0/P1 修复周期长，先投 **Scientific Reports (3.9 Q1, SCIE 已核实)** 或 **Frontiers in Immunology (5.7 Q1)**，JTM/EBioMedicine/Critical Care 留作补功能验证（S11 实际执行）后的冲刺档。
- **路径 C（仅措辞，不可行）· wording-only**：❌ 不可行。T0-1/T0-2/T0-3 与方法学核心相关，仅靠改措辞无法解决；必须改数字或补分析。

**最关键的 reframing（给作者）**：稿件最强的真实贡献是"Mars1 免疫麻痹程序由一套抗原呈递/单核枢纽基因锚定，且这套基因在独立外部队列可泛化（AUC 0.638，与最佳已发表基准持平）"——这是**生物学必然且可溯源的阳性**（Tier-1）。当前稿件把"脆弱的 MR 提示性信号"和"机制注释式药物重定位分数"与这个稳固核心并列头条，反而稀释了它。把头条换成 Tier-1 生物学阳性、把 MR 与重定位明确降级为"假设生成"，稿件会从"脆弱信号"转为"稳健结构发现"。

---

## 9. 流程教训（Process lessons）

- **自动门只能验证算术，验证不了设计**：本项目 git 门禁（一致性/数字溯源）全绿，但 Table 1 数字仍错——因为门禁枚举的是"字符串是否匹配"，而本次错误是"源文件本身数值与稿件不符"且 §7 溯源表声称的源文件根本不含那些值。需增加一道**独立重算脚本**（`audit_numbers.py`）从 03_results 重算关键数字并与稿件正则抽取值比对，作为 CI 门禁。
- **"target genes"术语陷阱**：方法学层最易被审稿人一眼识破的是"用下游响应基因代替真实分子靶点"——任何药物重定位稿应在方法段显式区分 direct target 与 downstream response，并引用 pharmacologic DB。
- **源文件即唯一真相**：§7 溯源表指向的文件中若数值与稿件不符，门禁应失败。本次 §7 声明 `S01_immunoparalysis_direction.csv` 为 Table 1 来源，但该文件无稿件值 → 门禁应捕获。建议溯源表改为"脚本自动抽取+写入"，而非人工填值。
- **跨队列基准比较需同口径**：IRG 0.619（文献）vs 0.604（重算）的混淆本可避免——凡"与文献基准比较"，必须注明基准来源与预处理，并附 CI。
- **专家独立性价值**：A2 单独提出的 MR 样本重叠（设计层）是自动门与单专家都难发现的缺陷，印证"门禁绿 ≠ 设计无误"。

---

*整合报告完。各专家完整四段式意见、英文 fix 句、§ Stands up / Questions / What I checked 见 `05_reports/review/A1_domain.md` … `A5_drugrepurposing.md`。*
