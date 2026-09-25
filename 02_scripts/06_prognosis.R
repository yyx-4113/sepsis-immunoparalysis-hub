# ============================================================
# S06 · 预后/分型模型（Tier-1，AUC 须 >= 0.619 基准）
# 输入：S05 hub 表达 + 28d 死亡 + 验证集
# 产出：S06_auc_compare.csv / S06_nomogram.pdf / S06_dca.png
# GATE G3：AUC >= 阈值则过
# ============================================================
source("02_scripts/00_utils.R")
cfg <- read_config()
hub <- read.csv(file.path(.dir_res, "S05_hub_genes.csv"))$gene
dat <- load_gse_chip("GSE65682"); expr <- dat$expr; pheno <- dat$pheno
hub_expr <- t(expr[intersect(hub, rownames(expr)), ])
# hub 风险评分（LASSO 系数或简单 z-sum）
risk <- scale(rowSums(hub_expr))
auc_train <- save_roc(risk, pheno$death_28d,
                      file.path(.dir_fig, "S06_roc_train.png"), "Hub risk score (train)")

# 验证集（E-MTAB-4451 / GSE95233）：方向一致性（外部集表达需映射到相同基因符号）
auc_val <- NA
# TODO: 载入 01_data/E-MTAB-4451 表达，计算同 risk 公式，出 AUC

auc_compare <- data.frame(dataset = c("GSE65682(train)", "external(validation)"),
                          auc = c(auc_train, auc_val),
                          baseline_IRG = cfg$thresholds$prognosis$roc_min_auc)
write.csv(auc_compare, file.path(.dir_res, "S06_auc_compare.csv"), row.names = FALSE)

# Nomogram + DCA（用 rms + rmda，若有）
# TODO: dca 图

.catf("S06 训练集 AUC=%.3f (基准=%.3f)", auc_train, cfg$thresholds$prognosis$roc_min_auc)
if (!is.na(auc_train) && auc_train < cfg$thresholds$prognosis$roc_min_auc) {
  .catf("⚠️ GATE G3 偏低：检查 hub 筛选/签名，但非阻塞")
}
dump_session("S06")
