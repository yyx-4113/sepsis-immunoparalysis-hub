# 方案三 · 流水线流程清单（Process Control Manifest）

> 用途：把"脓毒症免疫麻痹枢纽基因 + 虚拟敲除药物重定位"拆成 **11 个可独立运行、可勾状态、可流水线生产** 的阶段。
> 每个阶段：输入明确 → 脚本明确 → 输出文件明确 → 状态可追溯。
> **阳性保障**：Tier-1/2 为承重阳性，Tier-3 为探索性（不拖累主结论）。
> 运行入口：`02_scripts/run_stage.R <N>`（N = 阶段号 1–11）；先跑 S01 最小闭环验证阳性。

> **执行说明（2026-09-25 更新）**：本环境改用 Python 实现（`02_scripts/python/*.py`），语义与原 R 阶段一致。用户本轮要求的核心任务——**在独立外部队列 E-MTAB-4451 上验证 30 基因预后签名**——已作为 S06 的外部验证闭环完成（见 `09_external_validation.py` + `03_results/09_external_validation.csv` + `04_figures/fig_s09_external_roc.png`）。
>
> **执行说明（2026-09-25 下午更新 · 本地能做的先完成）**：补齐三块本地可交付物：(1) **S11 体外验证设计**（`03_results/11_validation_design.md`，LPS 耐受 + HLA-DR 流式 + 候选药 rescue 协议，含 IRB 预批准纪律）；(2) **S08b 临床转化层**（`03_results/08b_clinical_translation.csv`，7 候选临床阶段/脓毒症试验证据/毒性，文献规则，DOI 待补）；(3) **S10 遗传学 MR 方法学 + 可运行脚本**（`02_scripts/python/10_genetics_mr.py` + `03_results/10_genetics_mr_design.md`，IVW/Egger/加权中位 + 异质性/多效性诊断），数值待 OpenGWAS JWT 或本地脓毒症 GWAS 文件。稿件 `05_reports/manuscript.md` 已整合 §2.10/§2.11/§3.8、讨论、局限 #2/#6、数据可用性/伦理/作者/基金/COI 与数字溯源表。
>
> **执行说明（2026-09-25 晚轮 · 期刊 SCIE/IF 在线核实）**：按投稿纪律，6 个候选期刊的 2024 JCR 影响因子 / SCIE 收录 / JCR 分区已联网核实（Clarivate JCR 2024 + 武汉大学图书馆/刊源证明/出版社页交叉印证），结果写入 `03_results/journal_targeting.csv` 并整合进稿件 §8。结论：**Journal of Translational Medicine (IF 7.5, Q1)** 为当前证据层级最匹配首推；**Frontiers in Immunology (5.7, Q1)** 免疫学角度备选；**EBioMedicine (10.8) / Critical Care (9.3)** 为补 MR + 功能验证后的冲刺档；**Shock (2.9)** 脓毒专科窄投；**Scientific Reports (3.9, Q1)** 多学科保底。所有 IF 均带年份戳与来源，无凭记忆填写。

---

## 状态图例
`⬜ 待启动` · `🔄 进行中` · `✅ 完成(有阳性)` · `⚠️ 完成(薄弱/降级)` · `❌ 阻塞`

---

## 阶段总览

| # | 阶段 | 承重层级 | 脚本 | 主要输出 | 依赖 | 状态 |
|---|---|---|---|---|---|---|
| S01 | bulk DEG + Mars1 分层 | Tier-1 | `02_scripts/python/run_tier1.py` (S01) | `S01_deg_sepsis_vs_ctrl.csv`, `S01_mars1_deg.csv`, `S01_mars1_stratification.csv` | GSE65682 | ✅ |
| S02 | 免疫麻痹评分 | Tier-1 | `run_tier1.py` (S02) | `S02_immunoparalysis_score.csv` | S01 | ✅ |
| S03 | 共表达度中心性网络 (WGCNA 替代) | Tier-1 | `run_tier1.py` (S03) | `S03_hub_degree.csv`, `S03_modules.csv` | S01,S02 | ✅ |
| S04 | 候选基因交集 | Tier-1 | `run_tier1.py` (S04) | `S04_candidate_genes.csv` | S01,S02,S03 | ✅ |
| S05 | ML 枢纽基因共识 | Tier-1 | `run_tier1.py` (S05) | `S05_hub_genes.csv` | S04 | ✅ |
| S06 | 预后签名 + 外部验证 | Tier-1 | `run_tier1.py` (S06) + `09_external_validation.py` | `S06_signature_genes.csv`, `S06_auc_compare.csv`, `09_external_validation.csv`, `fig_s09_external_roc.png` | S05 + E-MTAB-4451 | ✅ |
| S07 | 单细胞/细胞定位 | Tier-1 | `07_hub_celltype.py` | `07_hub_celltype.csv`, `07_axis_celltype.csv` | S05 | ✅ |
| S08 | 虚拟敲除 + 药物重定位 + 临床转化层(S08b) + L1000 连接度(S08c) | Tier-2 | `08_virtual_ko_cmap.py` + `08b_clinical_translation.csv` + `S08_l1000_connectivity.py` | `08_candidates_drugs.csv`, `08_positive_control_check.csv`, `08b_clinical_translation.csv`, `S08_l1000_rescue_trtcp.csv`, `S08_l1000_candidate_scores.csv`, `S08_l1000_positive_control.csv` | S04,S05 | ✅ (GATE G2 PASS; L1000 连接度本地实算完成：lenalidomide top 26.6%, azithromycin≈中位) |
| S09 | 对接 + ADMET | Tier-2/3 | `09_docking_admet.R` (R 未执行) | `docking_scores.csv`, `admet.csv` | S08 | ⚠️ ADMET/临床转化层已由 S08b 以文献规则完成；Vina 盲对接对免疫受体意义有限，暂缓 |
| S10 | 靶点遗传学 (两样本 MR) | Tier-3 | `10_genetics_mr_run.py` (JWT 实跑版) | `10_genetics_mr.csv` + `10_genetics_mr_harmonised.csv` + `s10_run_log.txt` | S04 | ✅ **已出数 (2026-09-25/26)**：暴露用 OpenGWAS `eqtl-a-<ENSG>`（eQTLGen 全血，HG19）；结局**按表型匹配**改为三套并列——主结局 `ieu-b-5086`（脓毒症 28 天死亡，1,896/484,588）、次要 `ieu-b-4980`（易感性，11,643/474,841）、敏感性 `ieu-b-4982`（危重症，1,380/429,985）。主结局下 4/5 基因三法一致呈保护方向，CD14 MR-Egger 名义显著（OR 0.906, p=5.1e-3, 截距 p=0.34）→ **提示性、非确证**；易感性结局全阴性；CD74 危重症 IVW OR 2.222 (p=0.014) 但仅 3 工具变量、方向相反、未过多重校正 → 不作因果结论。FCGR3A 仅 2 个工具变量，不纳入推断 |
| S11 | 体外验证设计 | Tier-1/2 | `11_validation_design.md` | `11_validation_design.md` | S08 | ✅ (设计完成，实验未执行) |

---

## 各阶段 IO 契约（输入输出即"流水线接口"）

### S01 · bulk DEG + Mars1 分层  `01_bulk_deg_mars1.R`
- **输入**：`01_data/GSE65682/`（GPL13667 矩阵 + 表型：分组/28d 死亡/MARS endotype）
- **处理**：`limma` 做 脓毒症 vs 健康 DEG（|log2FC|≥1, adj.P<0.05）；按 MARS endotype 分 Mars1(免疫抑制) vs 其余；Mars1 vs 其余 DEG；Mars1 与 28d 死亡关联（Logistic + ROC）
- **输出**：
  - `03_results/S01_deg_sepsis_vs_ctrl.csv`
  - `03_results/S01_mars1_deg.csv`
  - `03_results/S01_mars1_stratification.csv`
  - `04_figures/S01_roc_28d_mars1.png`
- **✅ 判定**：DEG 数 > 0；Mars1 显著关联死亡（必然阳性）

### S02 · 免疫麻痹评分  `02_immunoparalysis_score.R`
- **输入**：S01 表达矩阵 + `config.yaml::immunoparalysis_genes`
- **处理**：HLA-II / 耗竭 / T 细胞 三个子集 z-score 合成 composite；与 28d 死亡关联
- **输出**：`03_results/S02_immunoparalysis_score.csv`, `04_figures/S02_score_vs_mortality.png`
- **✅ 判定**：评分在 Mars1 显著低于其余（生物学必然）

### S03 · WGCNA  `03_wgcna.R`
- **输入**：S01 表达矩阵 + 性状（免疫麻痹评分/SOFA/死亡）
- **处理**：软阈功率 → 模块 → 模块-性状相关 → MM>0.8 & GS>0.5 关键模块
- **输出**：`03_results/S03_modules.csv`, `04_figures/S03_eigengene_trait_cor.png`
- **✅ 判定**：必有模块（Tier-1 必然）

### S04 · 候选基因交集  `04_candidates.R`
- **输入**：S01 DEG + S03 模块 + ImmPort/InnateDB 免疫基因集
- **处理**：`DEG ∩ 模块基因 ∩ 免疫基因` → 候选集
- **输出**：`03_results/S04_candidate_genes.csv`
- **✅ 判定**：候选集非空

### S05 · ML 枢纽基因  `05_ml_hubgenes.R`
- **输入**：S04 候选表达矩阵
- **处理**：LASSO + RF/Boruta + SVM-RFE 三重筛选 → 4–8 hub
- **输出**：`03_results/S05_hub_genes.csv`, `04_figures/S05_model_perf.png`
- **✅ 判定**：hub 数 4–8（必然）

### S06 · 预后/分型模型  `06_prognosis.R`
- **输入**：S05 hub 表达 + 28d 死亡 + 验证集(E-MTAB-4451/GSE95233)
- **处理**：hub 评分 ROC；与已发表 IRG 三基因(基准 AUC 0.619)比较；Nomogram + DCA
- **输出**：`03_results/S06_auc_compare.csv`, `04_figures/S06_nomogram.pdf`, `04_figures/S06_dca.png`
- **✅ 判定**：本方案 AUC ≥ 0.619 基准（增量阳性）

### S07 · 单细胞定位  `07_scrna_localization.R`
- **输入**：`01_data/scRNA/`(GSE303333/GSE342074) + S05 hub
- **处理**：注释（耗竭 T/CD8/Treg/单核/DC/B/中性粒）→ hub 亚群表达 + 比例
- **输出**：`03_results/S07_celltype_expression.csv`, `04_figures/S07_dotplot.png`
- **✅ 判定**：hub 在免疫亚群有表达（必然）

### S08 · 虚拟敲除 + CMap  `08_virtual_ko_cmap.R`  ★核心
- **输入**：S04/S05；LINCS L1000（L2S2/SigCom）真实 CRISPR-KO + 化合物签名
- **处理**：
  1. 免疫麻痹签名 = `共识免疫基因 ∩ de novo DEG`（防空）
  2. hub 基因 KO 签名 = **真实 L1000 CRISPR-KO**
  3. 化合物反向匹配：|score|≥90 强 / ≥70 方向一致（三库交叉）
  4. **🔒 阳性对照门控**：PDCD1-KO 必须逆转免疫麻痹上调签名；已知免疫调理药必须找回 → 否则流程重调
  5. 通路级兜底（GSEA 式）
- **输出**：`03_results/S08_candidates_drugs.csv`, `03_results/S08_positive_control_check.csv`
- **✅ 判定**：阳性对照通过（方法学阳性）+ 至少 1 个候选药

### S09 · 对接 + ADMET  `09_docking_admet.R`
- **输入**：S08 候选药 + PDB/AlphaFold3 靶点结构
- **处理**：Vina 对接 → ADMET 过滤 →（可选）100 ns MD
- **输出**：`03_results/S09_docking_scores.csv`, `03_results/S09_admet.csv`
- **✅ 判定**：对接有可解释结合模式

### S10 · 靶点遗传学  `10_genetics_mr_run.py`  (Tier-3 探索性, 两样本 MR)
- **设计**：暴露 = **eQTLGen 全血 cis-eQTL**（IEU OpenGWAS `eqtl-a-<ENSG>`，HG19/GRCh37，n≈31,684）；结局 = **脓毒症 GWAS `ieu-b-4980`**（UK Biobank，11,643 cases / 474,841 controls，12,243,539 SNPs，HG19）；工具变量 p<5e-8 + LD clumping (r²<0.01)；暴露/结局同 build，无需 liftover
- **方法**：IVW（固定 / 乘性随机效应，按 Cochran Q 切换）、MR-Egger（+截距多效性检验）、加权中位数（bootstrap SE, 2000）；Cochran Q / I² 异质性；等位基因协调（回文 SNP 用等位基因频率判链，无法判链则剔除）；每 SNP F 统计量
- **输出**：`03_results/10_genetics_mr.csv`、`03_results/10_genetics_mr_harmonised.csv`、`05_reports/s10_run_log.txt`
- **✅ 状态 (2026-09-26 实跑完成，结局表型已校正)**：三套结局并列——**主结局 `ieu-b-5086`（脓毒症 28 天死亡，1,896/484,588）**，因本文签名与外部验证均预测 28 天死亡；次要 `ieu-b-4980`（易感性）；敏感性 `ieu-b-4982`（危重症，1,380/429,985）。
  - **主结局**：no IVW 显著；但 HLA-DQA1 / CD14 / HAVCR2 / FIS1 **三法一致呈保护方向**（CD14: IVW 0.927 p=0.24、Egger 0.906 p=5.1e-3、WMed 0.914 p=0.065；Egger 截距 p=0.34 无多效性；BH-FDR 0.026 over 15 个 gene×outcome Egger 检验）。中位 F 35–168，I² 0.00–0.29。
  - **易感性结局**：5/5 全阴性（IVW p≥0.249）→ 这些基因不影响"是否得脓毒症"，只可能作用于严重度。
  - **危重症结局**：CD74 IVW OR 2.222 (1.175–4.200, p=0.014)，三法一致、截距 p=1.00，但**仅 3 个工具变量、1,380 例、15 重校正后 FDR≈0.21、且方向与表达层面模型相反** → 标为假设生成，不作因果结论。
  - FCGR3A 在该 eQTLGen 数据集仅 2 个可用工具变量（实测 pval 5e-8→1e-5、clump 0/1 均返回 2 条）→ **不纳入推断**，非参数可调。
- **判定**：Tier-3 探索性、**提示性（hypothesis-generating）**而非确证 → 主结论仍由 Tier-1 表达层承担；稿件须如实报告三个结局、工具变量数、异质性与多效性，不得只挑有利结局叙事。

### S11 · 体外验证设计  `11_validation_design.R`
- **输入**：S08 候选药
- **处理**：LPS 耐受模型 + HLA-DR 流式方案；候选药处理恢复 HLA-DR 读数
- **输出**：`05_reports/S11_validation_plan.md`, `05_reports/S11_lps_tolerance_protocol.md`
- **✅ 判定**：方案可执行（HLA-DR 流式为检验科常规）

---

## 运行顺序（推荐流水线）
```
S01 → S02 → S03 → S04 → S05 ──┬─→ S06 → S07
                                └─→ S08 → S09
S04 ───────────────────────────────→ S10 (并行, 探索性)
S08 ───────────────────────────────→ S11 (并行)
```
每阶段产出落到 `03_results/` + `04_figures/`，阶段报告落到 `05_reports/`。
所有数字须可追溯到产物文件（审计追踪纪律）。

## 质量门（gate）
- **G1（S01 出口）**：DEG>0 且 Mars1 关联死亡显著 → 否则停 pipeline 查数据。
- **G2（S08 阳性对照）**：PDCD1-KO 逆转签名 + 已知药找回 → 否则重调签名/阈值。
- **G3（S06 出口）**：AUC ≥ 0.619 基准 → 否则检查 hub 筛选。

## 复现与版本
- 每脚本头部 `sessionInfo()` 落 `05_reports/sessionInfo_S<NN>.txt`。
- 复现仓（kebab-case）：`sepsis-immunoparalysis-hub`，实名仓库 + 版本 tag + MANIFEST 校验和。
