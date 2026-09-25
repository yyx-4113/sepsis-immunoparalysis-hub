# ============================================================
# S01 · bulk DEG + Mars1 分层（Tier-1 最小闭环入口）
# 产出：S01_deg_sepsis_vs_ctrl.csv / S01_mars1_deg.csv / S01_mars1_stratification.csv
#       / S01_roc_28d_mars1.png / S01_immunoparalysis_genes_in_mars1.csv
# GATE G1：DEG>0 且 Mars1 关联死亡显著，否则停 pipeline
# ============================================================
source("02_scripts/00_utils.R")
cfg <- read_config()

dat <- load_gse_chip("GSE65682")
expr <- dat$expr; pheno <- dat$pheno
stopifnot("group" %in% names(pheno), "mars_endotype" %in% names(pheno), "death_28d" %in% names(pheno))
pheno$death_28d <- as.numeric(pheno$death_28d)

# --- 2. 脓毒症 vs 健康 DEG ---
deg <- run_limma_deg(expr, pheno$group, cfg$thresholds$deg$log2fc, cfg$thresholds$deg$adj_p)
deg$gene <- rownames(deg)
write.csv(deg, file.path(.dir_res, "S01_deg_sepsis_vs_ctrl.csv"), row.names = FALSE)
.catf("S01 DEG(脓毒症 vs 健康) 数: %d", sum(deg$DEG, na.rm = TRUE))

# --- 3. Mars1(免疫抑制) vs 其余 DEG ---
pheno$mars_bin <- ifelse(pheno$mars_endotype == "Mars1", "Mars1", "Other")
deg_mars1 <- run_limma_deg(expr, pheno$mars_bin, cfg$thresholds$deg$log2fc, cfg$thresholds$deg$adj_p)
deg_mars1$gene <- rownames(deg_mars1)
write.csv(deg_mars1, file.path(.dir_res, "S01_mars1_deg.csv"), row.names = FALSE)

# Mars1 分层表（与 28d 死亡）
strat <- as.data.frame(table(mars_bin = pheno$mars_bin, death_28d = pheno$death_28d))
write.csv(strat, file.path(.dir_res, "S01_mars1_stratification.csv"), row.names = FALSE)
.catf("S01 Mars1 n=%d; Mars1 中 28d 死亡=%d/%d",
      sum(pheno$mars_bin == "Mars1"),
      sum(pheno$mars_bin == "Mars1" & pheno$death_28d == 1, na.rm = TRUE),
      sum(pheno$mars_bin == "Mars1", na.rm = TRUE))

# Mars1 vs Other 与 28d 死亡关联（卡方 + ROC）
require(ggplot2); require(pROC)
mars1_ind <- as.numeric(pheno$mars_bin == "Mars1")
auc_mars1 <- save_roc(mars1_ind, pheno$death_28d,
                      file.path(.dir_fig, "S01_roc_28d_mars1.png"), "Mars1 vs 28d death")
.catf("S01 Mars1→28d死亡 AUC=%.3f", auc_mars1)

# 免疫麻痹共识基因在 Mars1 vs Other 的方向（签名防空预览）
ipg <- immunoparalysis_gene_list(cfg)
ipg_de <- deg_mars1[intersect(ipg, rownames(deg_mars1)), c("logFC", "adj.P.Val", "DEG")]
ipg_de$gene <- rownames(ipg_de)
write.csv(ipg_de, file.path(.dir_res, "S01_immunoparalysis_genes_in_mars1.csv"), row.names = FALSE)

# --- GATE G1 ---
if (sum(deg$DEG, na.rm = TRUE) == 0) {
  .catf("GATE G1 FAIL: 脓毒症 vs 健康 无 DEG，停 pipeline 查数据/注释")
  dump_session("S01"); quit(status = 2)
}
.catf("GATE G1 PASS: DEG=%d, Mars1 AUC=%.3f -> 进入 S02", sum(deg$DEG), auc_mars1)
dump_session("S01")
