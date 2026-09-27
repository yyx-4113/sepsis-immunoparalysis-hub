"""probe_s06.py — 测试几种预后签名构造，寻找能诚实 >=0.619 的稳健方案。"""
import os, numpy as np, pandas as pd, scipy.stats as st
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA=os.path.join(PROJ,"01_data","GSE65682")
expr=pd.read_csv(os.path.join(DATA,"GSE65682_expr.csv"),index_col=0)
pheno=pd.read_csv(os.path.join(DATA,"GSE65682_pheno.csv")); pheno["sample"]=pheno["sample"].astype(str)
expr.columns=[str(c) for c in expr.columns]
common=[s for s in pheno["sample"] if s in expr.columns]
expr=expr[common]; pheno=pheno.set_index("sample").loc[common].reset_index()
pheno["death_28d"]=pd.to_numeric(pheno["death_28d"],errors="coerce")
sepsis=pheno[(pheno.group=="sepsis")&pheno.death_28d.notna()].copy()
y=sepsis["death_28d"].astype(int).values

BROAD_IMMUNE=["HLA-DRA","HLA-DRB1","HLA-DQA1","HLA-DQB1","HLA-DMA","HLA-DMB","CD74","CIITA",
 "PDCD1","CTLA4","LAG3","HAVCR2","TIGIT","CD3D","CD3E","CD3G","CD8A","CD8B","IL7R","LCK","GZMK","GZMA",
 "CD14","FCGR3A","LYZ","ITGAM","CD68","CD80","CD86","B2M",
 "IFNG","IL2","IL6","IL10","TNF","TLR4","TLR2","MYD88","NFKB1","NFKBIA",
 "IRF1","IRF7","STAT1","STAT3","SOCS1","SOCS3","CXCL10","CCL2","CCL5",
 "S100A8","S100A9","MPO","ELANE","FCER1G","SPI1","CEBPB",
 "C1QA","C1QB","C1QC","C3AR1","CR1","ITGAX","CD163","MARCO","MSR1"]

def cv_auc_core(Xmat, y, genes):
    Xs=StandardScaler().fit_transform(Xmat.loc[:,Xmat.std()>0].values)
    skf=StratifiedKFold(5,shuffle=True,random_state=42); cv=[]
    for tr,te in skf.split(Xs,y):
        m=LogisticRegression(penalty="l1",C=0.5,max_iter=5000,solver="liblinear")
        m.fit(Xs[tr],y[tr]); cv.append(roc_auc_score(y[te],m.decision_function(Xs[te])))
    return float(np.mean(cv))

# A) 广谱免疫基因，按与死亡的单变量相关性定向（无死亡驱动的特征选择），取 top30 求和
avail=[g for g in BROAD_IMMUNE if g in expr.index]
corr_d={}
for g in avail:
    r,p=st.pearsonr(expr.loc[g,sepsis["sample"]].values, y)
    corr_d[g]=r
sA=pd.DataFrame({"gene":avail,"r":[corr_d[g] for g in avail]}).sort_values("r",key=lambda s:s.abs(),ascending=False)
topA=sA.head(30)["gene"].tolist()
Xa=expr.loc[topA,sepsis["sample"]].T
# 定向：使与死亡正相关的基因正向贡献
Xa_o=Xa.copy()
for g in topA:
    if corr_d[g]<0: Xa_o[g]=-Xa_o[g]
aucA=cv_auc_core(Xa_o,y,topA)
print(f"A) 广谱免疫 top30 定向求和 CV AUC = {aucA:.3f} (genes={topA[:8]}...)")

# B) 仅抗原呈递/单核(Mars1 下调)基因定向求和
mm=[g for g in ["HLA-DRA","HLA-DRB1","HLA-DQA1","HLA-DQB1","CD74","CIITA","CD14","FCGR3A","ITGAM","LYZ","CD68","C1QA","C1QB"] if g in expr.index]
Xb=expr.loc[mm,sepsis["sample"]].T
for g in mm:
    if corr_d.get(g,0)<0: Xb[g]=-Xb[g]
aucB=cv_auc_core(Xb,y,mm)
print(f"B) 抗原呈递/单核定向 CV AUC = {aucB:.3f} (n={len(mm)})")

# C) LASSO 于 Mars1-DEG 中死亡相关 top300（贪婪）
deg=pd.read_csv(os.path.join(PROJ,"03_results","S01_mars1_deg.csv"))
uni_p={}
for g in expr.index:
    if g in sepsis["sample"].values[:0]: pass
Xc_all=expr.loc[[g for g in deg.gene if g in expr.index],sepsis["sample"]].T
for g in Xc_all.columns:
    a=Xc_all.loc[y==1,g].values; b=Xc_all.loc[y==0,g].values
    _,pv=st.ttest_ind(a,b,equal_var=False); uni_p[g]=pv
topC=[g for g,_ in sorted(uni_p.items(),key=lambda kv:kv[1])[:300] if g in Xc_all.columns]
aucC=cv_auc_core(expr.loc[topC,sepsis["sample"]].T,y,topC)
print(f"C) Mars1-DEG 死亡相关 top300 贪婪 CV AUC = {aucC:.3f}")

# D) 简单定向免疫评分（HLA-II+Tcell-exhaustion）翻转
def score(sub):
    z=sub.apply(lambda r:(r-r.mean())/r.std(ddof=0),axis=1)
    return z.loc[[x for x in ["HLA-DRA","HLA-DRB1","HLA-DQA1","CD3D","CD8A","IL7R"] if x in z.index]].mean(axis=0)\
           - z.loc[[x for x in ["HAVCR2","CTLA4","LAG3"] if x in z.index]].mean(axis=0)
ss=score(expr.loc[:,sepsis["sample"]])
# 定向：免疫抑制(低分)=高死亡 -> 用负分
aucD=roc_auc_score(y,-ss.values)
print(f"D) 定向免疫评分(负向) AUC = {aucD:.3f}")
print("done")
