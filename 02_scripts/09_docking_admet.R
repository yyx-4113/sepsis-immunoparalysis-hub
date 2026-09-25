# ============================================================
# S09 · 对接 + ADMET（Tier-2/3）
# ⛔ 按设计【不执行 / NOT EXECUTED — deferred by design】
#    本脚本仅作为脚手架保留；输出 S09_docking_scores.csv 仅含 NA 占位，
#    不代表任何真实对接 / ADMET 结果。
#    决策依据：ADMET/临床转化层已由 S08b 文献规则层替代（08b_clinical_translation.csv，
#    DOI 已 2026-09-26 核实）；hub 靶点为免疫受体/抗原呈递机器（HLA-II、FcγR、CD14、
#    TIM-3）与细胞因子，多为 PPI/细胞因子-受体界面，盲对接得分低信息量。
#    详见 PIPELINE.md S09 节与 manuscript.md §5 局限 #7。
# 输入：S08 候选药 + PDB/AlphaFold3 靶点结构
# 产出（规划，本稿不生成）：S09_docking_scores.csv / S09_admet.csv
# ============================================================
source("02_scripts/00_utils.R")
cands <- read.csv(file.path(.dir_res, "S08_candidates_drugs.csv"))
# TODO: 对每个候选药 -> 取 hub 靶点结构(PDB/AlphaFold3) -> AutoDock Vina 对接
#       -> admetlab/ SwissADME 计算 ADMET -> 过滤
dock <- data.frame(compound = cands$compound, docking_score = NA, admet_pass = NA)
write.csv(dock, file.path(.dir_res, "S09_docking_scores.csv"), row.names = FALSE)
.catf("S09 框架就绪；候选药 %d 个待对接", nrow(cands))
dump_session("S09")
