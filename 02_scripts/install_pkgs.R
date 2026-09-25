options(repos = c(CRAN = "https://cloud.r-project.org"),
        BioC_mirror = "https://bioconductor.org")
if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
BiocManager::install(version = "3.19", ask = FALSE, update = FALSE)
pkgs_bioc <- c("GEOquery","WGCNA","Biobase","annotate","genefilter","impute",
               "org.Hs.eg.db","clusterProfiler","biomaRt","preprocessCore","edgeR")
pkgs_cran <- c("caret","randomForest","pROC","survminer","RColorBrewer","circlize",
               "qs","data.table","glmnet","reshape2","ggplot2","tibble","readr",
               "jsonlite","Matrix","foreach","doParallel","e1071","sva")
for (p in c(pkgs_bioc, pkgs_cran)) {
  if (!requireNamespace(p, quietly = TRUE)) {
    cat("INSTALLING:", p, "\n")
    ok <- tryCatch({ install.packages(p, ask = FALSE, quiet = TRUE); TRUE },
                   error = function(e){ cat("FAIL", p, ":", conditionMessage(e), "\n"); FALSE })
    cat("  ->", if(ok && requireNamespace(p, quietly=TRUE)) "OK" else "STILL_MISSING", "\n")
  } else cat("PRESENT:", p, "\n")
}
cat("=== DONE ===\n")
