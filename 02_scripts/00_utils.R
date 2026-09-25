# ============================================================
# 00_utils.R — 方案三 共享工具
# 被所有 S0x 脚本 source()。集中：路径、配置读取、基因集、读 GEO、注释、绘图 helper
# 运行环境：R-4.4.3 + limma/WGCNA/glmnet/caret(或 mlr3)/ggplot2
# ============================================================

# ---- 1. 路径（基于本脚本位置推导项目根）----
.script_dir <- tryCatch(dirname(sys.frame(1)$ofile), error = function(e) getwd())
if (.script_dir == "") .script_dir <- getwd()
.project_root <- normalizePath(file.path(.script_dir, ".."))
.dir_data   <- file.path(.project_root, "01_data")
.dir_res    <- file.path(.project_root, "03_results")
.dir_fig    <- file.path(.project_root, "04_figures")
.dir_rep    <- file.path(.project_root, "05_reports")
for (d in c(.dir_res, .dir_fig, .dir_rep)) if (!dir.exists(d)) dir.create(d, recursive = TRUE)

# ---- 2. 读 config.yaml（无 yaml 包则回退简单解析）----
read_config <- function() {
  cfg_path <- file.path(.project_root, "00_pipeline", "config.yaml")
  if (requireNamespace("yaml", quietly = TRUE)) {
    return(yaml::read_yaml(cfg_path))
  }
  # 极简回退：仅返回关键阈值（避免缺包中断）
  warning("yaml 包缺失，使用内置阈值回退")
  list(thresholds = list(deg = list(log2fc = 1, adj_p = 0.05),
                         cmap = list(strong = 90, directional = 70)),
       immunoparalysis_genes = list(
         hla_class_ii = c("HLA-DRA","HLA-DRB1","HLA-DMB","CD74","CIITA"),
         exhaustion = c("PDCD1","CTLA4","LAG3","HAVCR2"),
         positive_control_ko = c("PDCD1")))
}

# ---- 3. 免疫麻痹共识基因集（签名防空用）----
immunoparalysis_gene_list <- function(cfg = NULL) {
  if (is.null(cfg)) cfg <- read_config()
  unlist(cfg$immunoparalysis_genes, use.names = FALSE) |>
    unique() |> gsub("gene:[A-Za-z0-9]+", "", x = _)   # 去掉 "gene:XXX" 注解
}

# ---- 4. 读 GEO 表达矩阵 + 表型（GPL570 芯片示例；按需改注释包）----
# 返回 list(expr=matrix(genes x samples), pheno=data.frame)
load_gse_chip <- function(gse_id, data_dir = .dir_data, annot_pkg = NULL) {
  # 实际执行：用 GEOquery::getGSEMatrix 或本地下载的 Series Matrix
  # 此处给出契约骨架；首次运行请先 geo_download.R 把矩阵落到 data_dir
  mat_file <- file.path(data_dir, gse_id, paste0(gse_id, "_expr.csv"))
  pheno_file <- file.path(data_dir, gse_id, paste0(gse_id, "_pheno.csv"))
  if (!file.exists(mat_file)) {
    stop(sprintf("[%s] 表达矩阵缺失：请先下载到 %s", gse_id, mat_file))
  }
  expr <- as.matrix(read.csv(mat_file, row.names = 1))
  pheno <- if (file.exists(pheno_file)) read.csv(pheno_file, row.names = 1) else NULL
  list(expr = expr, pheno = pheno)
}

# ---- 5. limma DEG ----
run_limma_deg <- function(expr, group, log2fc = 1, adj_p = 0.05) {
  require(limma)
  design <- model.matrix(~ 0 + factor(group))
  colnames(design) <- levels(factor(group))
  fit <- lmFit(expr, design)
  contrast <- makeContrasts(diff = eval(parse(text = sprintf("`%s` - `%s`",
    levels(factor(group))[2], levels(factor(group))[1]))), levels = design)
  fit2 <- contrasts.fit(fit, contrast); fit2 <- eBayes(fit2)
  tt <- topTable(fit2, number = Inf, adjust.method = "BH")
  tt$DEG <- abs(tt$logFC) >= log2fc & tt$adj.P.Val < adj_p
  tt
}

# ---- 6. 绘图 helper ----
save_roc <- function(prob, label, out_png, title = "ROC") {
  require(ggplot2); require(pROC)
  roc_obj <- roc(label, prob)
  auc_val <- auc(roc_obj)
  p <- ggplot(data.frame(FPR = 1 - roc_obj$specificities, TPR = roc_obj$sensitivities),
              aes(FPR, TPR)) + geom_line() +
    labs(title = sprintf("%s (AUC=%.3f)", title, auc_val), x = "1-Specificity", y = "Sensitivity")
  ggsave(out_png, p, width = 6, height = 5)
  auc_val
}

# ---- 7. sessionInfo 落盘 ----
dump_session <- function(stage) {
  sink(file.path(.dir_rep, sprintf("sessionInfo_%s.txt", stage))); print(sessionInfo()); sink()
}

.catf <- function(...) cat(sprintf(...), "\n", sep = "")
