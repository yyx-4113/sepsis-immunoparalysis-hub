# ============================================================
# S04 · 候选基因交集（Tier-1）
# 输入：S01 DEG ∩ S03 模块 ∩ 免疫基因集(ImmPort/InnateDB)
# 产出：S04_candidate_genes.csv
# ============================================================
source("02_scripts/00_utils.R")
cfg <- read_config()

deg <- read.csv(file.path(.dir_res, "S01_deg_sepsis_vs_ctrl.csv"))
deg_genes <- rownames(deg)[deg$DEG]
modules <- read.csv(file.path(.dir_res, "S03_modules.csv"))
key_mod <- modules$gene[modules$module != 0]   # 非灰模块
# 免疫基因集：共识 + 可选 ImmPort/InnateDB 下载列表（06_literature 提供）
ipg <- immunoparalysis_gene_list(cfg)
immune_extra <- tryCatch(readLines(file.path(.project_root, "06_literature", "immune_genes.txt")),
                          error = function(e) character(0))
immune_set <- union(ipg, immune_extra)

cand <- intersect(intersect(deg_genes, key_mod), immune_set)
cand_df <- data.frame(gene = cand,
                      in_DEG = cand %in% deg_genes,
                      in_module = cand %in% key_mod,
                      in_immune = cand %in% immune_set)
write.csv(cand_df, file.path(.dir_res, "S04_candidate_genes.csv"), row.names = FALSE)
.catf("S04 候选基因数: %d (DEG∩module∩immune)", length(cand))
stopifnot(length(cand) > 0)   # Tier-1 必然非空
dump_session("S04")
