# ============================================================
# S03 · WGCNA 模块（Tier-1，必然有模块）
# 输入：S01 表达矩阵 + 性状(免疫麻痹评分/SOFA/死亡)
# 产出：S03_modules.csv / S03_eigengene_trait_cor.png
# ============================================================
source("02_scripts/00_utils.R")
cfg <- read_config()
dat <- load_gse_chip("GSE65682"); expr <- dat$expr; pheno <- dat$pheno
score <- read.csv(file.path(.dir_res, "S02_immunoparalysis_score.csv"))

require(WGCNA)
# 软阈功率（scale-free fit）
powers <- c(1:20)
sft <- pickSoftThreshold(t(expr), powerVector = powers, verbose = 0)
power <- if (is.character(cfg$thresholds$wgcna$soft_power)) sft$powerEstimate else cfg$thresholds$wgcna$soft_power
net <- blockwiseModules(t(expr), power = power, TOMType = "unsigned", minModuleSize = 30,
                        reassignThreshold = 0, mergeCutHeight = 0.25, numericLabels = TRUE, verbose = 0)
modules <- data.frame(gene = colnames(expr), module = net$colors)
write.csv(modules, file.path(.dir_res, "S03_modules.csv"), row.names = FALSE)

# 模块-性状相关
trait <- data.frame(immunoparalysis = score$immunoparalysis_score[match(names(net$colors), score$sample)],
                    death = pheno$death_28d)
MEs <- net$MEs
modTraitCor <- cor(MEs, trait, use = "p")
png(file.path(.dir_fig, "S03_eigengene_trait_cor.png"), width = 7, height = 5)
par(mar = c(8, 5, 3, 2)); plotMat(modTraitCor, main = "Module-trait correlation")
dev.off()
.catf("S03 模块数: %d；最大 |cor| with 免疫麻痹=%.3f", length(unique(net$colors)) - 1,
      max(abs(modTraitCor[, 1]), na.rm = TRUE))
dump_session("S03")
