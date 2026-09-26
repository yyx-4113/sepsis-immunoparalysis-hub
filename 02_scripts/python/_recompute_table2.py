# -*- coding: utf-8 -*-
# Recompute Table 2 response_gene_concordance with the paper's OWN DEG definition
# (|logFC|>=0.3 & FDR<0.05; i.e. DEG_0.3==True) instead of mere direction (logFC<0).
# This makes the repositioning metric internally consistent with S01/S03 thresholds.
import os
import pandas as pd

PROJ = "D:/2026.9/极速交付9月会员日优惠套路/05_多组学+虚拟敲除药物发现/方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位"
RES = os.path.join(PROJ, "03_results")

imm = pd.read_csv(os.path.join(RES, "S01_immunoparalysis_direction.csv"))
# Original basis: merely directionally down
down_dir = set(imm[imm.logFC < 0]["gene"])
# Corrected basis: down AND DEG_0.3 (|logFC|>=0.3 & FDR<0.05) -- the paper's own DEG rule
down_strict = set(imm[(imm.logFC < 0) & (imm["DEG_0.3"] == True)]["gene"])

# Mirror the script's curated target sets
DRUG_MAP = {
 "IFN-gamma":      ["HLA-DRA","HLA-DRB1","HLA-DQA1","HLA-DQB1","CD74","CIITA","B2M","TAP1","TAP2"],
 "GM-CSF":         ["HLA-DRA","HLA-DRB1","CD14","FCGR3A","ITGAM","CD86","CD80"],
 "Lenalidomide":   ["CD80","CD86","HLA-DRA","HLA-DRB1","ICAM1","TLR4"],
 "Thymosin alpha1":["HLA-DRA","CD14","TLR4","TLR2","CD80","CD86"],
 "IL-7":           ["CD3D","CD3E","CD8A","IL7R","LCK"],
 "BCG (trained immunity)":["HLA-DRA","CD80","CD86","TLR4","TLR2","NOD2"],
 "Azithromycin":   ["HLA-DRA","CD14","IL10"],
}
mars1 = pd.read_csv(os.path.join(RES, "S01_mars1_deg.csv"))
present = set(mars1["gene"].tolist()) | set(imm["gene"].tolist())
cands = pd.read_csv(os.path.join(RES, "08_candidates_drugs.csv"))

print(f"{'drug':24s} {'old':>6s} {'new':>6s}   old -> new (of n_target in present)")
for drug, targets in DRUG_MAP.items():
    tg = [g for g in targets if g in present]
    old_rescue = [g for g in tg if g in down_dir]
    new_rescue = [g for g in tg if g in down_strict]
    old_f = len(old_rescue)/len(tg) if tg else 0
    new_f = len(new_rescue)/len(tg) if tg else 0
    label = drug if drug in set(cands["compound"]) else None
    print(f"{drug:24s} {old_f:6.2f} {new_f:6.2f}   {len(old_rescue)}/{len(tg)} -> {len(new_rescue)}/{len(tg)}  {new_rescue}")

# --- rewrite 08_candidates_drugs.csv (only the three rescued columns change) ---
out_rows = []
for _, r in cands.iterrows():
    comp = r["compound"]
    targets = DRUG_MAP.get(comp)
    if targets is None:
        out_rows.append(r)
        continue
    tg = [g for g in targets if g in present]
    new_rescue = [g for g in tg if g in down_strict]
    r["n_rescue_mars1down"] = len(new_rescue)
    r["rescue_fraction"] = round(len(new_rescue)/len(tg), 3) if tg else 0.0
    r["rescue_genes"] = ";".join(new_rescue)
    out_rows.append(r)
new_df = pd.DataFrame(out_rows)
new_df.to_csv(os.path.join(RES, "08_candidates_drugs.csv"), index=False)
print("\nWrote updated 08_candidates_drugs.csv:")
print(new_df[["compound","n_target_genes","n_rescue_mars1down","rescue_fraction"]].to_string(index=False))
