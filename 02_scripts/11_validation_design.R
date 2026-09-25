# ============================================================
# S11 · 体外验证设计（Tier-1/2，HLA-DR 流式为金标准读数）
# 输入：S08 候选药
# 产出：S11_validation_plan.md / S11_lps_tolerance_protocol.md
# ============================================================
source("02_scripts/00_utils.R")
cands <- read.csv(file.path(.dir_res, "S08_candidates_drugs.csv"))

plan <- c(
  "# 体外验证计划（S11）",
  "",
  "## 模型：LPS 耐受（免疫麻痹体外模型）",
  "1. 健康志愿者/PBMC 或患者 PBMC，低剂量 LPS(10 ng/mL) 预处理 24h → 再高剂量 LPS(100 ng/mL) 刺激 24h",
  "2. 分组：对照 / LPS耐受 / LPS耐受+候选药(各候选 1-3 个浓度)",
  "3. 读数：",
  "   - 流式 HLA-DR（单核/DC 表面，免疫麻痹金标准）：候选药应恢复 HLA-DR 表达 = 阳性",
  "   - qPCR：hub 基因 + TNF/IL10/HLA-DRA",
  "   - ELISA：TNF-α、IL-10、IL-6",
  "",
  "## 候选药",
  paste("   -", cands$compound, collapse = "\n   - "),
  "",
  "## 判定：候选药处理组 HLA-DR 表达高于 LPS 耐受组 = 逆转免疫麻痹（阳性）"
)
writeLines(plan, file.path(.dir_rep, "S11_validation_plan.md"))

proto <- c(
  "# LPS 耐受实验 Protocol",
  "- Day0: 分离 PBMC，培养于 RPMI+10% FBS",
  "- Day1: LPS 10 ng/mL 预处理 24h",
  "- Day2: 换液，候选药处理 2h 后加 LPS 100 ng/mL 24h",
  "- Day3: 收样：流式(HLA-DR/CD14/CD16)、qPCR、ELISA"
)
writeLines(proto, file.path(.dir_rep, "S11_lps_tolerance_protocol.md"))
.catf("S11 验证方案已生成；候选药 %d 个", nrow(cands))
dump_session("S11")
