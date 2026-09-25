# ============================================================
# S07 · 单细胞定位（Tier-1，hub 必有表达）
# 输入：01_data/scRNA (GSE303333/GSE342074) + S05 hub
# 产出：S07_celltype_expression.csv / S07_dotplot.png
# ============================================================
source("02_scripts/00_utils.R")
hub <- read.csv(file.path(.dir_res, "S05_hub_genes.csv"))$gene
# 单细胞读取（Seurat 优先；若无则用 sparse 直接读）
# TODO: Read10x / ReadH5AD -> 注释 CD4 T(naive/effector/memory/exhausted:PDCD1/HAVCR2/LAG3),
#       CD8 T, Treg, NK, 单核(CD14+/CD16+), DC, B, 中性粒/LDN
# 计算 hub 在各亚群平均表达 + 亚群比例变化
cell_expr <- data.frame(gene = hub, placeholder_avg = NA)  # 占位，真实运行填充
write.csv(cell_expr, file.path(.dir_res, "S07_celltype_expression.csv"), row.names = FALSE)
.catf("S07 框架就绪；运行前请补全 scRNA 读取与注释逻辑")
dump_session("S07")
