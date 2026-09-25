# ============================================================
# S08 · 虚拟敲除 + CMap 药物重定位（Tier-2，核心，含阳性对照门控）
# 输入：S04/S05；LINCS L1000 真实 CRISPR-KO + 化合物签名
# 产出：S08_candidates_drugs.csv / S08_positive_control_check.csv
# GATE G2：PDCD1-KO 必须逆转免疫麻痹上调签名 + 已知免疫调理药找回，否则重调
# 签名防空：免疫麻痹签名 = 共识免疫基因 ∩ de novo DEG（非纯 de novo）
# 阈值梯度：|score|>=90 强 / >=70 方向一致（三库交叉，必报告命中数）
# ============================================================
source("02_scripts/00_utils.R")
cfg <- read_config()

# --- 1. 免疫麻痹签名（共识 ∩ de novo）---
deg <- read.csv(file.path(.dir_res, "S01_deg_sepsis_vs_ctrl.csv"))
de_novo_up <- rownames(deg)[deg$logFC > cfg$thresholds$deg$log2fc & deg$adj.P.Val < cfg$thresholds$deg$adj_p]
de_novo_down <- rownames(deg)[deg$logFC < -cfg$thresholds$deg$log2fc & deg$adj.P.Val < cfg$thresholds$deg$adj_p]
ipg <- immunoparalysis_gene_list(cfg)
immunoparalysis_sig_up <- intersect(ipg, de_novo_up)     # 免疫麻痹中"上调"的共识基因
immunoparalysis_sig_down <- intersect(ipg, de_novo_down)
.catf("S08 免疫麻痹签名(共识∩DEG): up=%d down=%d", length(immunoparalysis_sig_up), length(immunoparalysis_sig_down))

# --- 2. hub 基因 KO 签名（真实 L1000 CRISPR-KO，经 L2S2/SigCom API）---
# TODO: 用 L2S2/SigCom LINCS API 拉取 S05 hub 的 CRISPR-KO 签名（免疫细胞系优先）
hub <- read.csv(file.path(.dir_res, "S05_hub_genes.csv"))$gene
ko_signatures <- list()  # 真实检索后填充：gene -> up/down vector

# --- 3. 化合物反向匹配（connectivity，方向取反）---
# TODO: 对 LINCS 化合物签名算与免疫麻痹签名反向的 connectivity score
#       强 |score|>=90；方向一致 |score|>=70；L2S2/SigCom/iLINCS 三库交叉取一致
cmp_scores <- data.frame(compound = character(), score = numeric(), source = character())
write.csv(cmp_scores, file.path(.dir_res, "S08_candidates_drugs.csv"), row.names = FALSE)

# --- 4. 🔒 阳性对照门控 ---
# (a) PDCD1-KO 签名须与免疫麻痹上调签名负相关（PD-1 阻断=免疫恢复）
pdcd1_ko <- ko_signatures[["PDCD1"]]
ctrl_pass <- FALSE
if (!is.null(pdcd1_ko)) {
  # PDCD1-KO 上调基因 应富集于 免疫麻痹下调(被抑制)基因 → 恢复
  ctrl_pass <- length(intersect(names(pdcd1_ko$up), immunoparalysis_sig_down)) >
               length(intersect(names(pdcd1_ko$up), immunoparalysis_sig_up))
}
# (b) 已知免疫调理药须被找回（来那度胺/IFN-γ 相关扰动）
known_drugs <- c("lenalidomide", "interferon gamma", "sargramostim(GM-CSF)", "thymosin alpha1")
known_found <- known_drugs[known_drugs %in% cmp_scores$compound]
ctrl_df <- data.frame(check = c("PDCD1_KO_reverses_signature", "known_immunostim_drug_recovered"),
                      passed = c(ctrl_pass, length(known_found) > 0),
                      detail = c(if (ctrl_pass) "PDCD1-KO 恢复免疫麻痹签名" else "FAIL",
                                 paste(known_found, collapse = ";")))
write.csv(ctrl_df, file.path(.dir_res, "S08_positive_control_check.csv"), row.names = FALSE)

.catf("S08 阳性对照: PDCD1-KO=%s, 已知药找回=%d/%d",
      if (ctrl_pass) "PASS" else "FAIL", length(known_found), length(known_drugs))
if (!ctrl_pass) {
  .catf("❌ GATE G2 FAIL: 阳性对照未通过 → 重调签名/细胞系/阈值，勿进全文")
  quit(status = 2)
}
.catf("✅ GATE G2 PASS: 方法学阳性对照通过；候选药 %d 个", nrow(cmp_scores))
dump_session("S08")
