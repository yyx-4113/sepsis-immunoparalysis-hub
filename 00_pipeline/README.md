# 方案三 · 流水线工程框架（README）

把"脓毒症免疫麻痹枢纽基因 + 虚拟敲除药物重定位"做成可流水线生产的工程。

## 目录
- 00_pipeline/  config.yaml(中央配置) + PIPELINE.md(流程清单) + README.md
- 01_data/      GEO 原始数据（按数据集分子目录）
- 02_scripts/   00_utils.R(共享) / 00_geo_download.R(下载) / run_stage.R(编排) / 01~11 阶段脚本
- 03_results/   各阶段 CSV 产物（审计追踪）
- 04_figures/  各阶段图
- 05_reports/  阶段报告 + sessionInfo
- 06_literature/ 免疫基因集 / 文献

## 快速开始
1. 下载数据（联网，需 GEOquery）： Rscript 02_scripts/00_geo_download.R
2. 逐阶段跑（自动检查产物，缺失报 BLOCKED）：
   Rscript 02_scripts/run_stage.R 1   # S01 bulk DEG + Mars1（Tier-1 最小闭环）
   Rscript 02_scripts/run_stage.R 2   # S02 免疫麻痹评分
   Rscript 02_scripts/run_stage.R 3   # S03 WGCNA
   Rscript 02_scripts/run_stage.R 4   # S04 候选基因
   Rscript 02_scripts/run_stage.R 5   # S05 ML hub
   Rscript 02_scripts/run_stage.R 6   # S06 预后模型
   Rscript 02_scripts/run_stage.R 7   # S07 单细胞定位
   Rscript 02_scripts/run_stage.R 8   # S08 虚拟敲除+CMap（含阳性对照门控 G2）
   Rscript 02_scripts/run_stage.R 9   # S09 对接+ADMET
   Rscript 02_scripts/run_stage.R 10  # S10 遗传学（Tier-3）
   Rscript 02_scripts/run_stage.R 11  # S11 体外验证设计

## 流程门（gate）
- G1（S01 出口）：DEG>0 且 Mars1 关联死亡 -> 否则停。
- G2（S08 阳性对照）：PDCD1-KO 逆转签名 + 已知免疫调理药找回 -> 否则重调。
- G3（S06 出口）：AUC >= 0.619 基准（非阻塞）。

## 阳性保障
- Tier-1 生物学必然阳性（Mars1 / 共识基因 DE / 模块 / hub / ROC / 单细胞）。
- Tier-2 方法学阳性对照（PDCD1-KO 门控 + 真实 CRISPR-KO）。
- Tier-3 探索性，不纳入主结论，避免全负。

## 纪律
- 所有数字须可追溯到 03_results 产物文件。
- 期刊 IF/SCIE 投稿前联网核实并注年份。
- 复现仓：sepsis-immunoparalysis-hub（实名仓 + tag + MANIFEST 校验和）。
