# ============================================================
# S09 · 对接 + ADMET（Tier-2/3）
# 输入：S08 候选药 + PDB/AlphaFold3 靶点结构
# 产出：S09_docking_scores.csv / S09_admet.csv
# ============================================================
source("02_scripts/00_utils.R")
cands <- read.csv(file.path(.dir_res, "S08_candidates_drugs.csv"))
# TODO: 对每个候选药 -> 取 hub 靶点结构(PDB/AlphaFold3) -> AutoDock Vina 对接
#       -> admetlab/ SwissADME 计算 ADMET -> 过滤
dock <- data.frame(compound = cands$compound, docking_score = NA, admet_pass = NA)
write.csv(dock, file.path(.dir_res, "S09_docking_scores.csv"), row.names = FALSE)
.catf("S09 框架就绪；候选药 %d 个待对接", nrow(cands))
dump_session("S09")
