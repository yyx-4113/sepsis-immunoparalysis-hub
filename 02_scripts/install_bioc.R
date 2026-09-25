# install_bioc.R — 修正版：用 BiocManager 安装 Bioconductor 包（首版误用 install.packages 走 CRAN 导致 GEOquery 等缺失）
# 运行： Rscript 02_scripts/install_bioc.R
options(repos = c(CRAN = "https://cloud.r-project.org"))
if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
# 确保 Bioconductor 3.19 镜像加入
bp <- BiocManager::repositories()
cat("Bioconductor repos:\n"); print(bp)
bioc_pkgs <- c("GEOquery","Biobase","annotate","genefilter","impute","preprocessCore",
               "org.Hs.eg.db","clusterProfiler","biomaRt","edgeR","WGCNA","ComplexHeatmap",
               "circlize","RColorBrewer","EnhancedVolcano")
# BiocManager 会一并处理 CRAN 依赖（caret/randomForest/pROC/survminer 已由首版装好）
for (p in bioc_pkgs) {
  if (!requireNamespace(p, quietly = TRUE)) {
    cat("BiocManager INSTALL:", p, "\n")
    BiocManager::install(p, ask = FALSE, update = FALSE, force = FALSE)
  } else cat("PRESENT:", p, "\n")
}
cat("=== BIOC INSTALL DONE ===\n")
sess <- installed.packages()
for (p in bioc_pkgs) cat(sprintf("%-16s %s\n", p, if(requireNamespace(p,quietly=TRUE)) as.character(packageVersion(p)) else "MISSING"))
