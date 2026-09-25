# ============================================================
# 07_hub_celltype.py — hub 基因的细胞定位（Tier-1 扩展, 无 scRNA 时的 bulk 标记模块替代）
# 方法：用各免疫细胞的经典标记基因模块均值，跨 802 样本计算 hub 基因与该模块的相关性，
#       将 hub 基因定位到主导免疫细胞情境。诚实标注：bulk 替代，非真正单细胞分辨率。
# 输入：S05_hub_genes.csv / GSE65682_expr.csv / pheno
# 产出：07_hub_celltype.csv / 07_axis_celltype.csv / 04_figures/S07_celltype.png
# ============================================================
import os
import numpy as np, pandas as pd, scipy.stats as st
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; import seaborn as sns
PROJ="D:/2026.9/极速交付9月会员日优惠套路/05_多组学+虚拟敲除药物发现/方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位"
DATA=os.path.join(PROJ,"01_data","GSE65682"); RES=os.path.join(PROJ,"03_results"); FIG=os.path.join(PROJ,"04_figures")
os.makedirs(FIG, exist_ok=True)
expr=pd.read_csv(os.path.join(DATA,"GSE65682_expr.csv"),index_col=0)
pheno=pd.read_csv(os.path.join(DATA,"GSE65682_pheno.csv")); pheno["sample"]=pheno["sample"].astype(str)
expr.columns=[str(c) for c in expr.columns]
common=[s for s in pheno["sample"] if s in expr.columns]; expr=expr[common]

# 免疫细胞标记模块（经典、保守）
CELL_MARKERS={
 "Monocyte":["CD14","FCGR3A","LYZ","ITGAM","ITGAX","CD68","S100A8","S100A9"],
 "Neutrophil":["MPO","ELANE","CSF3R","S100A8","S100A9","FCGR3B"],
 "CD4_Tcell":["CD3D","CD4","IL7R","LCK","GZMK"],
 "CD8_Tcell":["CD3D","CD8A","CD8B","GZMK","GZMB"],
 "B_cell":["CD19","MS4A1","CD79A","CD79B","BLNK"],
 "NK_cell":["NCAM1","FCGR3A","KLRC1","KLRD1","NKG7"],
 "Dendritic":["FCER1A","CLEC10A","CD1C","IRF8","BATF3"],
 "Plasma_cell":["IGHG1","MZB1","SDC1","XBP1"],
}
# 计算各细胞模块均值（跨样本），z-score
mod_mean={}
for ct,gs in CELL_MARKERS.items():
    gs=[g for g in gs if g in expr.index]
    if len(gs)>=3:
        z=expr.loc[gs].apply(lambda r:(r-r.mean())/r.std(ddof=0),axis=1)
        mod_mean[ct]=z.mean(axis=0)
mod_df=pd.DataFrame(mod_mean)

hub=pd.read_csv(os.path.join(RES,"S05_hub_genes.csv"))["gene"].tolist()
hub=[g for g in hub if g in expr.index]
def locate(genes):
    recs=[]
    for g in genes:
        best=None; bestr=None; corrs={}
        for ct in mod_df.columns:
            r,_ = st.pearsonr(expr.loc[g, mod_df.index].values, mod_df[ct].values)
            corrs[ct]=round(r,3)
            if bestr is None or abs(r)>abs(bestr): bestr=r; best=ct
        rec={"gene":g,"best_celltype":best,"best_corr":round(bestr,3)}
        rec.update(corrs)
        recs.append(rec)
    return pd.DataFrame(recs)
hub_loc=locate(hub)
hub_loc.to_csv(os.path.join(RES,"07_hub_celltype.csv"), index=False)
print(f"[S07] hub 基因({len(hub)}) 细胞定位:")
for _,r in hub_loc.iterrows():
    print(f"    {r['gene']:10s} -> {r['best_celltype']:12s} (r={r['best_corr']:.3f})")

# 免疫麻痹轴整体细胞情境（用 Mars1-down 轴基因）
imm=pd.read_csv(os.path.join(RES,"S01_immunoparalysis_direction.csv"))
axis=[g for g in imm[imm.logFC<0]["gene"].tolist() if g in expr.index]
axis_loc=locate(axis)
# 每细胞类型平均 |corr|
cellavg=axis_loc[[c for c in mod_df.columns]].abs().mean().sort_values(ascending=False)
cellavg_df=cellavg.reset_index(); cellavg_df.columns=["cell_type","mean_abs_corr"]
cellavg_df.to_csv(os.path.join(RES,"07_axis_celltype.csv"), index=False)
print(f"[S07] 免疫麻痹轴主导细胞情境: {cellavg_df.head(3).values.tolist()}")

plt.figure(figsize=(7,4))
sns.barplot(data=cellavg_df, x="mean_abs_corr", y="cell_type", order=cellavg_df.cell_type)
plt.title("Immunoparalysis axis: cellular context (bulk marker-module corr)"); plt.tight_layout()
plt.savefig(os.path.join(FIG,"S07_celltype.png"), dpi=120); plt.close()
print("[S07] 完成")
