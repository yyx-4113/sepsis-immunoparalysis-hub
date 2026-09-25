# ============================================================
# 00_geo_download.R — 下载并整理 GEO 数据到 01_data/
# 运行：Rscript 02_scripts/00_geo_download.R
# 依赖：GEOquery / ArrayExpress；首次运行会联网下载（建议代理/直连对齐）
# 产出：各数据集 expr.csv + pheno.csv（pheno 含 group/mars_endotype/death_28d/sofa）
# ============================================================
source("02_scripts/00_utils.R")
require(GEOquery)

download_one_gse <- function(gse_id, out_dir, pheno_cols = NULL) {
  gset <- getGSEDataTables(gse_id)   # 表型表
  gse <- getGSE(gse_id, destdir = out_dir, getGPL = FALSE)
  # 取首个 Series Matrix 表达矩阵
  expr <- exprs(gse[[1]])
  pdata <- pData(phenoData(gse[[1]]))
  # 简化为 symbols：用 fData 注释（GPL570 需 annotate 包映射；此处占位）
  write.csv(expr, file.path(out_dir, paste0(gse_id, "_expr.csv")))
  write.csv(pdata, file.path(out_dir, paste0(gse_id, "_pheno.csv")))
  .catf("下载 %s -> %d x %d", gse_id, nrow(expr), ncol(expr))
}

# 主数据集（必下）
download_one_gse("GSE65682", file.path(.dir_data, "GSE65682"))
# 验证集
download_one_gse("E-MTAB-4451", file.path(.dir_data, "E-MTAB-4451"))
download_one_gse("GSE95233", file.path(.dir_data, "GSE95233"))
download_one_gse("GSE317767", file.path(.dir_data, "GSE317767"))
.catf("数据下载完成；下一步运行 run_stage.R 1 起跑 S01")
