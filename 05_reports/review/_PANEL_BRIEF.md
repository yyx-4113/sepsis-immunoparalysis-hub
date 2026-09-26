# 共享评审简报 — 独立多专家评审面板 (Independent Review Panel)

**被评审稿件**：`05_reports/manuscript.md`
**版本**：v1.0.2（git tag；复现包已 commit，未 push）
**研究类型**：生物信息学 / 计算多组学 + 药物重定位（单作者，无新原始数据，纯公共数据再分析）
**目标期刊（作者规划）**：Journal of Translational Medicine (IF 7.5, Q1) 为首选；Frontiers in Immunology (5.7) 备选；EBioMedicine (10.8) / Critical Care (9.3) 为补功能验证后的冲刺档。
**研究主张（一句话）**：脓毒症 MARS 免疫抑制型（Mars1）由一组抗原呈递/单核枢纽基因（CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1）锚定，这组基因兼具预后价值与可药性；通过 in-silico 虚拟敲除 + LINCS L1000 反向连接度 + 文献规则层，提名 IL-7/GM-CSF/IFN-γ 等免疫重建剂；MR 遗传学为提示性（非确证）。

---

## 一、独立性纪律（强制，每位专家必读）

你作为评审专家，**假设自己从未见过这篇稿件、也从未参与过它的任何修改轮次**。本稿件已历经多轮内部修订，但**你不得**利用任何历史上下文。

**禁止阅读的文件**（读到即视为违规，你的评审作废）：
- `05_reports/review/` 目录下除本 `_PANEL_BRIEF.md` 以外的**任何**文件（包括其他专家的评审、REVIEW_*.md、RESPONSE_*.md）
- 项目根的任何 `*REVIEW*`, `*RESPONSE*`, `*REVISION*`, `*ROUND*` 文件
- `00_pipeline/PIPELINE.md`（仅允许读其中的 IO 契约与阶段定义作参考，**禁止读其"执行说明"注释**，因其含历史判断）
- `06_literature/` 与任何 `*_gen_*.py` 模拟评审脚本
- `GITHUB_DEPOSIT_SOP.md`、`author_verification_statement.md`、`.workbuddy/` 目录
- 任何任务状态文件 / 看板 / 项目概览

**你不得假设稿件"已经成熟"或"已经过前轮评审"**。把它当作首次投稿（first submission）来审。
**每一个你做出的判断，必须来自你亲自读取的稿件文本或源数据。** 稿件里任何你可以验证的数字，**你必须亲自重算或抽查**，不得直接采信。

---

## 二、输出契约（每条意见强制四段）

对每一个发现，必须包含以下四部分；缺少任一部分视为不合格：
- **【Problem】** 一句话陈述问题。
- **【Evidence】** 锚定到 `manuscript.md:行号`，或 `03_results/xxx.csv` 的表/列与精确数字；**你引用的数字必须是你亲自重算或亲自核对过的**，并注明你是"重算"还是"核对稿件与源文件一致"。
- **【Why it matters】** 对结论 / 可信度 / 接收概率的具体影响。
- **【Specific fix】** 可直接粘贴的英文替换句，或一个明确的新分析规范（变量、分层、输出列）。禁止写"建议加强讨论"这类空话。

**还必须包含**：
- **§ Stands up（≥3 条，附证据）**：明确标注你**怀疑过但核查后发现稿件是正确的**地方。这是交付物，不是填充。
- **§ Questions for the authors**：你需要作者澄清什么，不要替作者猜答案。
- **§ What I actually checked**：你读了哪些文件、运行了什么命令、重算了哪些值并与稿件比对，差异在哪里。

---

## 三、必查数字清单与源文件指针（不重算即视为评审不完整）

稿件 §7 数字溯源表列出了每个数字的源文件。请按你的专长重点核对以下项（全部位于项目根目录下）：

| 稿件主张 (manuscript.md) | 声称值 | 必须核对源文件 |
|---|---|---|
| 802 样本构成（760 脓毒症 / 42 对照；479 有内型+28d 生存） | §2.1 | `01_data/GSE65682/GSE65682_pheno.csv`, `GSE65682_expr.csv` |
| sepsis-vs-healthy DEG 448；Mars1-vs-Other DEG 3597（\|logFC\|≥0.3） | §3.1, §7 | `03_results/S01_deg_sepsis_vs_ctrl.csv`, `S01_mars1_deg.csv` |
| 25 共识免疫基因中 21 个方向性下调、22 个 FDR<0.05 显著 | §3.1 | `03_results/S01_immunoparalysis_direction.csv` |
| HLA-DRB1 Δ=−0.59 (P=9.7e-09); CD74 −0.48 (8.2e-09); CD14 −0.77 (1.3e-17); FCGR3A −0.55 (1.0e-06); HAVCR2 −0.39 (1.7e-16) | §3.1 Table 1 | `03_results/S01_immunoparalysis_direction.csv` |
| Mars1 免疫评分中位 −0.79（range −3.65 to 3.86） | §3.2 | `03_results/S02_immunoparalysis_score.csv` |
| 6 hub 基因（CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1） | §3.3 | `03_results/S05_hub_genes.csv` |
| 30-gene 签名 5-fold CV AUC 0.659（训练 0.750） | §3.4, §6, §7 | `03_results/S06_auc_compare.csv` |
| 外部 E-MTAB-4451：定向和评分 AUC 0.638 (CI 0.532–0.748)；锁定 L1 权重 AUC 0.585 (CI 0.469–0.696)；IRG 基准重算 0.604 | §3.5, §7 | `03_results/09_external_validation.csv` |
| IRG benchmark 0.619 (E-MTAB-4451) / 0.648 (GSE65682) | §2.6, §3.4 | `03_results/S06_auc_compare.csv` |
| **注意**：§2.6/§3.4 说 IRG 在 E-MTAB-4451 上是 **0.619**，但 §3.5/§7/摘要说"IRG benchmark recomputed on the same cohort (0.604)"。**两处同一队列给出不同值——必须查清这两个数字各自来自哪个文件、是否同一基准、是否需要澄清。** | ⚠️ | `S06_auc_compare.csv` 与 `09_external_validation.csv` 两个文件对比 |
| 细胞定位：CD14 r=0.77, FCGR3A r=0.49, CD74→dendritic r=0.69, HAVCR2 r=0.30, HLA-DQA1→B r=0.68；CD4 mean\|r\|=0.62, CD8 0.58, dendritic 0.46 | §3.6 | `03_results/07_hub_celltype.csv`, `07_axis_celltype.csv` |
| 7 候选药 rescue_fraction：IL-7 1.00, GM-CSF 0.83, IFN-γ 0.71, Azithromycin 0.67, Lenalidomide 0.40, Thymosin α1 0.40, BCG 0.20 | §3.7 Table 2 | `03_results/08_candidates_drugs.csv`, `08_positive_control_check.csv` |
| L1000：lenalidomide rank 5435/20413 (top 26.6%, rescue 0.044, wtcs 1.17); azithromycin 9152/20413 (rescue 0.013); 背景 mean/median 0.006, 53.6% compounds >0 | §3.9 | `03_results/S08_l1000_candidate_scores.csv`, `S08_l1000_rescue_trtcp.csv`, `S08_l1000_positive_control.csv` |
| MR：CD14 MR-Egger OR 0.906 (P=5.1e-3, BH-FDR 0.026, intercept P=0.34); 主结局 ieu-b-5086 (1896/484588)；易感性 ieu-b-4980 (11643/474841)；危重症 ieu-b-4982 (1380/429985)；CD74 critical-care OR 2.222 (P=0.014, 3 IVs, FDR≈0.21) | §3.10, §5 | `03_results/10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`, 对应 `*_harmonised.csv` |

---

## 四、环境与数据陷阱（避免重复踩坑）

- **数据规模**：`01_data/` 含约 43G 原始 GEO/LINCS 文件（.gctx 等），**不要尝试完整读取**；用摘要 CSV（`03_results/*`）核对数字即可。LINCS 主库 `GSE92742_Level5_COMPZ.gctx` 已被 `.gitignore` 排除，仅 `03_results/S08_l1000_*.csv` 内含聚合结果。
- **执行环境**：实际分析用 Python（`02_scripts/python/*.py`）实现；PIPELINE.md 旧版写的是 R 阶段名（`01_bulk_deg_mars1.R` 等），**稿件方法部分明确说"limma-style ... implemented in Python"**——核对时不要被 R 文件名误导，以 `02_scripts/python/` 与 `03_results/` 为准。
- **git 已初始化**（v1.0.0/v1.0.1/v1.0.2 三个 tag），但**未 push**。你只需读文件，不要运行 git push。
- **S09 对接按设计不执行**（`09_docking_admet.R` 是桩，输出 NA）。稿件 §3.9 的 `fig_s09_external_roc.png` 实为 S06 外部验证 ROC（非对接图）。勿误判为"伪造对接结果"。
- **Crossref/PubMed 可用性**：若需查证参考文献 DOI 是否真实，可用 `curl https://api.crossref.org/works/<DOI>` 核实（项目 `02_scripts/python/build_references.py` 已用此法核实 29 条）。当前参考文献 29 条，均为 Crossref 核实过的真实 DOI。

---

## 五、禁止事项

- **禁止提及你使用什么工具**（不写"我用 Python 读了…"、"grep 显示…"）。只写评审意见本身。
- **禁止读取其他专家的输出**或历史评审文件（见第一节）。
- **禁止替作者做主**；无法判断处写入 "§ Questions for the authors"。
- 不得给出"建议加强讨论/未来可探索"类空泛意见；每条必须有【Problem/Evidence/Why/Specific fix】。

---

## 六、你的专长聚焦点（每个专家不同，见各自派发任务）

A1 = 脓毒症/免疫学临床领域专家（临床 claim 真假、必须引用文献、终点含义）
A2 = 生物信息统计 + MR 因果推断设计专家（稀疏细胞、多重检验、工具变量有效性、阴性对照、样本重叠、乐观偏倚）
A3 = 数字溯源 / 重算审计员（数字匹配源文件、双舍入、表格语法、不可复现 claim）
A4 = 期刊编辑 + 报告标准审计员（TRIPOD/STROBE/STROBE-MR 诚实性、格式硬伤、cover letter 一致性）
A5 = LINCS/L1000 计算药物重定位方法学专家（reverse-connectivity、阳性对照、假阳性、target 定义特异性）

请按你被指派的专长深度审查，但**任何专家**发现跨层问题都应记录（例如 A3 发现设计层偏倚也照常写）。
