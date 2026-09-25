# ============================================================
# run_stage.R — 流水线编排器
# 用法： Rscript run_stage.R <N>   例： Rscript run_stage.R 1
# 行为：运行 02_scripts/0<N>_*.R；运行后检查 03_results 下该阶段产物是否存在
#       不存在则报 BLOCKED。这是"流水线生产"的统一入口。
# ============================================================
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) { cat("用法: Rscript run_stage.R <阶段号 1-11>\n"); quit(status = 1) }
stage <- sprintf("%02d", as.integer(args[1]))
script <- list.files("02_scripts", pattern = sprintf("^%s_.*\\.R$", stage), full.names = TRUE)
if (length(script) == 0) { cat(sprintf("阶段 %s 脚本未找到\n", stage)); quit(status = 1) }

.catf <- function(...) cat(sprintf(...), "\n", sep = "")
.catf(">>> 运行阶段 S%s : %s", stage, script)

# 设置工作目录为项目根（脚本用相对路径读 config/data）
setwd(normalizePath(".."))
source(script)

# 产物自检
res_dir <- "03_results"
stage_out <- list.files(res_dir, pattern = sprintf("^S%s_", stage), full.names = TRUE)
if (length(stage_out) == 0) {
  .catf("⚠️ BLOCKED: S%s 运行完毕但未检出 03_results/S%s_* 产物", stage, stage)
  quit(status = 2)
} else {
  .catf("✅ S%s 完成，产物 %d 个:", stage, length(stage_out))
  for (f in stage_out) .catf("   - %s", f)
}
