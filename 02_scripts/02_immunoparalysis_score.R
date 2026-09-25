# ============================================================
# S02 · 免疫麻痹评分（Tier-1）
# 输入：S01 表达矩阵 + config$immunoparalysis_genes
# 产出：S02_immunoparalysis_score.csv / S02_score_vs_mortality.png
# ============================================================
source("02_scripts/00_utils.R")
cfg <- read_config()
dat <- load_gse_chip("GSE65682"); expr <- dat$expr; pheno <- dat$pheno

ipg_list <- cfg$immunoparalysis_genes
# 分三个子集 z-score 合成 composite（HLA-II / 耗竭 / T细胞）
sub_scores <- list()
for (grp in c("hla_class_ii", "exhaustion", "tcell")) {
  genes <- gsub("gene:[A-Za-z0-9]+", "", ipg_list[[grp]])
  genes <- intersect(genes, rownames(expr))
  if (length(genes) > 0) sub_scores[[grp]] <- colMeans(t(scale(t(expr[genes, ]))), na.rm = TRUE)
}
# composite = mean of available subscores（HLA-II 取负向：低表达=麻痹）
composite <- Reduce(`+`, lapply(names(sub_scores), function(n)
  if (n == "hla_class_ii") -sub_scores[[n]] else sub_scores[[n]])) / length(sub_scores)
score_df <- data.frame(sample = names(composite), immunoparalysis_score = composite,
                       mars = pheno$mars_endotype, death_28d = pheno$death_28d)
write.csv(score_df, file.path(.dir_res, "S02_immunoparalysis_score.csv"), row.names = FALSE)

# Mars1 应显著低于其余（生物学必然）
require(ggplot2)
p <- ggplot(score_df, aes(mars, immunoparalysis_score)) + geom_boxplot() +
  labs(title = "Immunoparalysis score by MARS endotype")
ggsave(file.path(.dir_fig, "S02_score_vs_mortality.png"), p, width = 6, height = 4)
.catf("S02 评分完成；Mars1 中位评分=%.3f", median(composite[pheno$mars_endotype == "Mars1"]))
dump_session("S02")
