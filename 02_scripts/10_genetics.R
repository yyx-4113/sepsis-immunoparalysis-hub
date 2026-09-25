# ============================================================
# S10 · 靶点遗传学 eQTL/pQTL 共定位（Tier-3 探索性，不纳入主结论）
# 输入：S04 hub；免疫细胞计数 GWAS / 脓毒症 GWAS
# 产出：S10_colocalization.csv
# 注：共定位为概率事件，标探索性
# ============================================================
source("02_scripts/00_utils.R")
cand <- read.csv(file.path(.dir_res, "S04_candidate_genes.csv"))$gene
# TODO: 用 Open Targets / IEU OpenGWAS 拉 hub 的 eQTL/pQTL
#       + 免疫细胞计数 GWAS / 脓毒症 GWAS -> SMR / coloc (PP.H4)
coloc <- data.frame(gene = cand, coloc_pph4 = NA, note = "exploratory-Tier3")
write.csv(coloc, file.path(.dir_res, "S10_colocalization.csv"), row.names = FALSE)
.catf("S10 框架就绪（Tier-3 探索性）；hub %d 个待共定位", length(cand))
dump_session("S10")
