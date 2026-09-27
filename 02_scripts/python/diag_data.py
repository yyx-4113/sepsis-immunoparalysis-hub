"""diag_data.py — 诊断 GSE65682 重处理数据的真实信号强度，定位 Tier-1 弱结果根因。"""
import os, numpy as np, pandas as pd, scipy.stats as st
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(PROJ, "01_data", "GSE65682")
expr = pd.read_csv(os.path.join(DATA, "GSE65682_expr.csv"), index_col=0)
pheno = pd.read_csv(os.path.join(DATA, "GSE65682_pheno.csv"))
pheno["sample"] = pheno["sample"].astype(str); expr.columns = [str(c) for c in expr.columns]
common = [s for s in pheno["sample"] if s in expr.columns]
expr = expr[common]; pheno = pheno.set_index("sample").loc[common].reset_index()
pheno["death_28d"] = pd.to_numeric(pheno["death_28d"], errors="coerce")

print("=== 1) 表达值分布（确认归一化尺度/方差）===")
v = expr.values
print(f"shape={expr.shape}  min={v.min():.3f} max={v.max():.3f} mean={v.mean():.3f} median={np.median(v):.3f}")
per_gene_sd = expr.std(axis=1)
print(f"每基因 SD: min={per_gene_sd.min():.4f} median={per_gene_sd.median():.4f} max={per_gene_sd.max():.4f}")
per_gene_range = expr.max(axis=1)-expr.min(axis=1)
print(f"每基因 range: median={per_gene_range.median():.3f}")

print("\n=== 2) 关键免疫基因在 Mars1 vs Other 的真实方向（不是只看 DEG 标志）===")
genes = ["HLA-DRA","HLA-DRB1","HLA-DQA1","CD74","CIITA","PDCD1","CTLA4","LAG3","HAVCR2",
         "CD3D","CD3E","CD8A","IL7R","CD14","LYZ","ITGAM","FCGR3A","GZMK"]
m1 = pheno[pheno.mars_endotype=="Mars1"]["sample"]
oth = pheno[(pheno.mars_endotype!="Mars1") & pheno.mars_endotype.notna()]["sample"]
rows=[]
for g in genes:
    if g not in expr.index: 
        rows.append((g,"ABSENT",np.nan,np.nan,np.nan)); continue
    a = expr.loc[g, m1].values; b = expr.loc[g, oth].values
    t,p = st.ttest_ind(a,b,equal_var=False)
    rows.append((g, f"{a.mean():.3f}", f"{b.mean():.3f}", a.mean()-b.mean(), p))
print(f"{'gene':10s} {'Mars1_mean':>11s} {'Other_mean':>11s} {'diff':>8s} {'p':>10s}")
for r in rows: print(f"{r[0]:10s} {str(r[1]):>11s} {str(r[2]):>11s} {str(r[3]):>8s} {str(r[4]):>10s}")

print("\n=== 3) sepsis vs healthy 真实分离度（不同阈值下 DEG 数）===")
sep = pheno[pheno.group=="sepsis"]["sample"]; hlt = pheno[pheno.group=="healthy"]["sample"]
lfc=[]; pv=[]
for g in expr.index:
    a=expr.loc[g,sep].values; b=expr.loc[g,hlt].values
    t,p=st.ttest_ind(a,b,equal_var=False)
    lfc.append(np.mean(a)-np.mean(b)); pv.append(p)
lfc=np.array(lfc); pv=np.array(pv)
from statsmodels.stats.multitest import multipletests
_,padj,_,_=multipletests(pv,method="fdr_bh")
for fc_th,pth in [(0.585,0.05),(1.0,0.05),(1.0,0.01),(1.5,0.05),(2.0,0.05)]:
    n=((np.abs(lfc)>=fc_th)&(padj<pth)).sum()
    print(f"  |logFC|>={fc_th} & adj.P<{pth}: {n} 个基因")

print("\n=== 4) Mars1 vs Other 分离度 ===")
lfc2=[]; pv2=[]
for g in expr.index:
    a=expr.loc[g,m1].values; b=expr.loc[g,oth].values
    t,p=st.ttest_ind(a,b,equal_var=False)
    lfc2.append(np.mean(a)-np.mean(b)); pv2.append(p)
lfc2=np.array(lfc2); pv2=np.array(pv2)
_,padj2,_,_=multipletests(pv2,method="fdr_bh")
for fc_th,pth in [(0.3,0.05),(0.5,0.05),(0.585,0.05),(1.0,0.05)]:
    n=((np.abs(lfc2)>=fc_th)&(padj2<pth)).sum()
    print(f"  |logFC|>={fc_th} & adj.P<{pth}: {n} 个基因")
print("保存诊断完成")
