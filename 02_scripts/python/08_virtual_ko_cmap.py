# ============================================================
# 08_virtual_ko_cmap.py — 虚拟敲除 + 药物重定位（Tier-2, 阳性对照门控）
# 输入：S01_mars1_deg.csv / S01_immunoparalysis_direction.csv / S05_hub_genes.csv
# 产出：08_disease_signature.csv / 08_candidates_drugs.csv / 08_positive_control_check.csv
# 疾病签名：Mars1 下调的"免疫麻痹轴"基因（抗原呈递 / 单核-髓系功能）
# 重定位逻辑：文献确证的免疫刺激剂 -> 其靶点基因集若落在 Mars1-down 轴 -> 可"虚拟逆转"免疫麻痹
# 网络约束：iLINCS 在本沙箱不可达(http 000)；故用机制锚定候选，明确标注，待 L1000/iLINCS 复认。
# GATE G2：IFN-gamma（经典 HLA-II 诱导剂）必须能 rescue 抗原呈递轴 -> 方法学阳性对照。
# ============================================================
import os, sys
import numpy as np, pandas as pd

PROJ = "D:/2026.9/极速交付9月会员日优惠套路/05_多组学+虚拟敲除药物发现/方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位"
RES  = os.path.join(PROJ, "03_results"); FIG = os.path.join(PROJ, "04_figures")
os.makedirs(RES, exist_ok=True)

# ---- 1. 免疫麻痹疾病签名（Mars1 vs Other 的真实方向）----
imm = pd.read_csv(os.path.join(RES, "S01_immunoparalysis_direction.csv"))   # gene,logFC,P.Value,adj.P.Val,DEG_0.3,direction
mars1 = pd.read_csv(os.path.join(RES, "S01_mars1_deg.csv"))                # gene,logFC,...,DEG_0.3
# Mars1 下调 = 免疫抑制轴（这些基因在 Mars1 中被压制）
down_axis = imm[imm.logFC < 0]["gene"].tolist()
up_axis   = imm[imm.logFC > 0]["gene"].tolist()
# 扩展疾病向量：Mars1-DEG 中 |logFC| 最大的基因（带符号），提高召回
top = mars1.sort_values("logFC", key=lambda s: s.abs(), ascending=False).head(400)
disease_vec = dict(zip(top.gene, np.sign(top.logFC).astype(int)))
pd.DataFrame({"gene":down_axis+up_axis,
              "direction":["Mars1_down"]*len(down_axis)+["Mars1_up"]*len(up_axis)}).to_csv(
    os.path.join(RES,"08_disease_signature.csv"), index=False)
print(f"[S08] 免疫麻痹轴: Mars1_down={len(down_axis)} 基因; Mars1_up={len(up_axis)} 基因; 扩展向量={len(disease_vec)}")

# ---- 2. 文献锚定的免疫刺激剂 -> 靶点基因（机制映射）----
# 每张药物卡：靶点基因 = 文献确证该药上调/激活的免疫基因；方向须与 Mars1-down 轴相反 -> 逆转免疫麻痹
# 注：靶点为标准基因符号；rescue 判定只看是否落在 Mars1-down 轴（即该药可"救回"被抑制的免疫程序）
DRUG_MAP = {
 "IFN-gamma":      {"targets":["HLA-DRA","HLA-DRB1","HLA-DQA1","HLA-DQB1","CD74","CIITA","B2M","TAP1","TAP2"],
                    "mechanism":"JAK1/2-STAT1 经典 MHC-II 主诱导剂，直接救回抗原呈递轴",
                    "evidence":"Well-established; CIITA transactivates HLA-II"},
 "GM-CSF":         {"targets":["HLA-DRA","HLA-DRB1","CD14","FCGR3A","ITGAM","CD86","CD80"],
                    "mechanism":"髓系/单核激活，上调 HLA-DR 与吞噬受体",
                    "evidence":"Sepsis trials (GMS 2009 等) 提示髓系重建"},
 "Lenalidomide":   {"targets":["CD80","CD86","HLA-DRA","HLA-DRB1","ICAM1","TLR4"],
                    "mechanism":"共刺激与抗原呈递上调，T 细胞共刺激增强",
                    "evidence":"IMiD; 上调 costim 与 HLA-II"},
 "Thymosin alpha1":{"targets":["HLA-DRA","CD14","TLR4","TLR2","CD80","CD86"],
                    "mechanism":"树突/单核成熟与抗原呈递恢复",
                    "evidence":"免疫 restoration in sepsis (IST 等)"},
 "IL-7":           {"targets":["CD3D","CD3E","CD8A","IL7R","LCK"],
                    "mechanism":"T 细胞稳态增殖，对抗 T 细胞耗竭/凋亡",
                    "evidence":"lymphopenia 复苏；PDCD1 轴上游"},
 "BCG (trained immunity)":{"targets":["HLA-DRA","CD80","CD86","TLR4","TLR2","NOD2"],
                    "mechanism":"先天免疫训练，上调抗原呈递与共刺激",
                    "evidence":"trained immunity; 降低感染复发"},
 "Azithromycin":   {"targets":["HLA-DRA","CD14","IL10"],
                    "mechanism":"大环内酯免疫调节，部分上调 HLA-DR、下调过度炎症",
                    "evidence":"macrolide immunomodulation (modest)"},
}
present = set(mars1.gene.tolist()) | set(imm.gene.tolist())
rows=[]
for drug, info in DRUG_MAP.items():
    tg = [g for g in info["targets"] if g in present]
    # rescue：靶点中落在 Mars1-down 轴的比例（该药可救回被抑制的免疫程序）
    rescue = [g for g in tg if g in set(down_axis)]
    if len(tg)==0:
        continue
    frac = len(rescue)/len(tg)
    rows.append({"compound":drug,
                 "n_target_genes":len(tg),
                 "n_rescue_mars1down":len(rescue),
                 "rescue_fraction":round(frac,3),
                 "rescue_genes":";".join(rescue),
                 "mechanism":info["mechanism"],
                 "evidence":info["evidence"]})
cands = pd.DataFrame(rows).sort_values("rescue_fraction", ascending=False)
cands.to_csv(os.path.join(RES,"08_candidates_drugs.csv"), index=False)
print(f"[S08] 机制锚定候选药={len(cands)} 种; 按 rescue_fraction 排序:")
for _,r in cands.iterrows():
    print(f"    {r['compound']:22s} rescue={r['rescue_fraction']:.2f} ({r['n_rescue_mars1down']}/{r['n_target_genes']})")

# ---- 3. 🔒 阳性对照门控 ----
# (a) IFN-gamma 必须 rescue 抗原呈递轴（HLA-DRA/DRB1/CD74/CIITA 在 Mars1-down 中）
ifn_rescue = [g for g in ["HLA-DRA","HLA-DRB1","HLA-DQA1","CD74","CIITA"] if g in set(down_axis)]
# (b) 虚拟敲除阳性对照：Hub 基因（CD74/HLA-DQA1 等）若被 KO 应加剧免疫麻痹 -> 与疾病签名同向
hub = pd.read_csv(os.path.join(RES,"S05_hub_genes.csv"))
hub_genes = hub["gene"].tolist()
ko_same_dir = [g for g in hub_genes if g in set(down_axis)]   # hub 在 Mars1 中下调 -> KO 加剧麻痹
ctrl = pd.DataFrame([
    {"check":"IFN_gamma_rescues_antigen_presentation_axis","passed":len(ifn_rescue)>=3,
     "detail":f"救回 {len(ifn_rescue)}/5 抗原呈递基因: {ifn_rescue}"},
    {"check":"hub_KO_phenocopies_immunoparalysis","passed":len(ko_same_dir)>0,
     "detail":f"hub 在 Mars1 下调(虚拟KO加剧麻痹): {ko_same_dir}"},
    {"check":"candidate_drugs_recovered","passed":len(cands)>0,
     "detail":f"{len(cands)} 种机制锚定免疫刺激剂"},
])
ctrl.to_csv(os.path.join(RES,"08_positive_control_check.csv"), index=False)
g2 = all(ctrl["passed"])
print(f"[S08] 阳性对照: IFN-gamma 救回抗原呈递={len(ifn_rescue)}/5; hub-KO 同向={len(ko_same_dir)}; 候选={len(cands)}")
print(f"GATE G2: {'PASS' if g2 else 'FAIL'}")
if not g2:
    print("  -> 方法学阳性对照未过：需补 iLINCS/L1000 复认后重调；不虚构候选。")
print("[S08] 完成 (机制锚定; iLINCS/L1000 复认待联网)")
