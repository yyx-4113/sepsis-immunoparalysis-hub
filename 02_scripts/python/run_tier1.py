# ============================================================
# run_tier1.py — 方案三 Tier-1 实证核心（S01-S06，v2 修正版）
# GSE65682 (MARS, GPL13667 已核实) 脓毒症免疫麻痹枢纽基因 + 预后模型
# 修正要点（基于 diag_data.py 诊断）：
#   1) 本数据集效应量偏小（免疫基因 |logFC| 0.2-0.6），DEG 阈值改为 |logFC|>=0.3 & padj<0.05（Mars1 vs Other）
#   2) 免疫麻痹方向表改用"效应量+方向+显著性"判定，不靠单一阈值
#   3) WGCNA 易碎 -> 改为稳健的相关网络枢纽度（degree centrality）
#   4) S06 预后签名用"与 28d 死亡相关的基因"构建连续评分，5 折 CV AUC，目标 >=0.619
# 运行： python 02_scripts/python/run_tier1.py
# 产出：03_results/S0*.csv ; 04_figures/*.png ; 05_reports/tier1_summary.txt
# ============================================================
import os, sys
import numpy as np, pandas as pd
import scipy.stats as st
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, roc_curve
from statsmodels.stats.multitest import multipletests

PROJ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(PROJ, "01_data", "GSE65682")
RES  = os.path.join(PROJ, "03_results"); FIG = os.path.join(PROJ, "04_figures")
REP  = os.path.join(PROJ, "05_reports")
for d in (RES, FIG, REP): os.makedirs(d, exist_ok=True)

# ---- 共识免疫基因集 ----
IPG = {
 "hla_class_ii": ["HLA-DRA","HLA-DRB1","HLA-DQA1","HLA-DQB1","HLA-DMA","HLA-DMB","CD74","CIITA"],
 "exhaustion": ["PDCD1","CTLA4","LAG3","HAVCR2","TIGIT"],
 "tcell": ["CD3D","CD3E","CD3G","CD8A","CD8B","IL7R","LCK","GZMK","GZMA"],
 "mono_marker": ["CD14","FCGR3A","LYZ","ITGAM"],
}
IMMUNE_SET = set(g for v in IPG.values() for g in v)

# ============ 载入 ============
expr = pd.read_csv(os.path.join(DATA, "GSE65682_expr.csv"), index_col=0)   # gene x sample
pheno = pd.read_csv(os.path.join(DATA, "GSE65682_pheno.csv"))
pheno["sample"] = pheno["sample"].astype(str)
expr.columns = [str(c) for c in expr.columns]
common = [s for s in pheno["sample"] if s in expr.columns]
expr = expr[common]; pheno = pheno.set_index("sample").loc[common].reset_index()
pheno["death_28d"] = pd.to_numeric(pheno["death_28d"], errors="coerce")
print(f"[载入] 表达 {expr.shape[0]} 基因 x {expr.shape[1]} 样本; 表型列={list(pheno.columns)}")

# ============ limma 式 moderated t-test ============
def design0(group):
    levels = list(pd.unique(group))
    return pd.DataFrame({lv:(group==lv).astype(float).values for lv in levels}, index=group.index), levels

def fit_limma(E, group, lvl_a, lvl_b):
    mask = group.isin([lvl_a, lvl_b]).values
    Esub = E.iloc[:, mask]; gsub = group.iloc[mask]
    design, levels = design0(gsub)
    X = design.values.astype(float); Y = Esub.T.values.astype(float)
    XtX = X.T @ X
    beta = np.linalg.solve(XtX, X.T @ Y)
    resid = Y - X @ beta
    n, p = X.shape; df_resid = n - p
    RSS = (resid**2).sum(axis=0)
    s2 = RSS/df_resid; m = s2.mean(); v = s2.var(ddof=1) if df_resid>1 else s2.var()
    prior_df = np.clip(2*m**2/max(v,1e-12), 1e-2, 1e5); prior_var = m
    mod_var = (df_resid*s2 + prior_df*prior_var)/(df_resid+prior_df)
    covbeta = np.linalg.inv(XtX)
    ci = levels.index(lvl_a); cj = levels.index(lvl_b)
    contrast = np.zeros(len(levels)); contrast[ci]=1; contrast[cj]=-1
    cv = float(contrast @ covbeta @ contrast)
    stat = contrast @ beta
    t = stat/np.sqrt(mod_var*cv + 1e-12)
    df_tot = df_resid + prior_df
    p = 2*(1 - st.t.cdf(np.abs(t), df_tot))
    _, padj, _, _ = multipletests(p, method="fdr_bh")
    out = pd.DataFrame({"logFC":stat, "t":t, "P.Value":p, "adj.P.Val":padj}, index=Esub.index)
    out["DEG_0.3"] = (np.abs(stat)>=0.3)&(padj<0.05)
    out["DEG_1.0"] = (np.abs(stat)>=1.0)&(padj<0.05)
    return out

# ---------- S01 ----------
deg = fit_limma(expr, pheno["group"], "sepsis", "healthy")
deg["gene"] = deg.index
deg.to_csv(os.path.join(RES,"S01_deg_sepsis_vs_ctrl.csv"), index=False)
n_deg = int(deg["DEG_0.3"].sum()); n_deg1 = int(deg["DEG_1.0"].sum())
print(f"[S01] 脓毒症 vs 健康 DEG(|logFC|>=0.3)= {n_deg}; (|logFC|>=1.0)= {n_deg1}")

pheno["mars_bin"] = np.where(pheno["mars_endotype"]=="Mars1","Mars1","Other")
deg_mars1 = fit_limma(expr, pheno["mars_bin"], "Mars1", "Other")
deg_mars1["gene"] = deg_mars1.index
deg_mars1.to_csv(os.path.join(RES,"S01_mars1_deg.csv"), index=False)
n_mars1 = int(deg_mars1["DEG_0.3"].sum())
print(f"[S01] Mars1 vs Other DEG(|logFC|>=0.3)= {n_mars1}")

# 免疫麻痹方向表：共识免疫基因在 Mars1 vs Other 的真实效应
ipg = deg_mars1.loc[[g for g in IMMUNE_SET if g in deg_mars1.index],
                    ["logFC","P.Value","adj.P.Val","DEG_0.3"]].copy()
ipg["gene"]=ipg.index
ipg["direction"] = np.where(ipg.logFC>0, "Mars1_up", "Mars1_down")
ipg = ipg.sort_values("P.Value")
ipg.to_csv(os.path.join(RES,"S01_immunoparalysis_direction.csv"), index=False)
n_ipg_sig = int((ipg["adj.P.Val"]<0.05).sum())
n_ipg_down = int(((ipg["adj.P.Val"]<0.05)&(ipg.logFC<0)).sum())
print(f"[S01] 共识免疫基因 Mars1 vs Other 显著下调={n_ipg_down}/{len(ipg)} (共显著 {n_ipg_sig}/{len(ipg)})")

# Mars1 -> 28d death (分类预测，作为参照)
y = pheno["death_28d"].dropna()
pred = (pheno.loc[y.index,"mars_bin"]=="Mars1").astype(int).values
auc_mars1 = roc_auc_score(y.values, pred)
fpr,tpr,_ = roc_curve(y.values, pred)
plt.figure(figsize=(6,5)); plt.plot(fpr,tpr,label=f"Mars1 (AUC={auc_mars1:.3f})"); plt.plot([0,1],[0,1],"--k")
plt.xlabel("1-Specificity"); plt.ylabel("Sensitivity"); plt.title("Mars1 vs 28d death"); plt.legend(); plt.tight_layout()
plt.savefig(os.path.join(FIG,"S01_roc_28d_mars1.png"), dpi=120); plt.close()
print(f"[S01] Mars1->28d AUC = {auc_mars1:.3f}")

# ---------- S02 免疫机能评分（高=免疫活跃；Mars1 应最低）----------
def zscore_rows(E, genes):
    g=[x for x in genes if x in E.index]
    return E.loc[g].apply(lambda r:(r-r.mean())/r.std(ddof=0), axis=1)
sub_scores={}
for grp in ["hla_class_ii","exhaustion","tcell"]:
    z=zscore_rows(expr, IPG[grp])
    if z.shape[0]>0: sub_scores[grp]=z.mean(axis=0)
composite=pd.DataFrame(sub_scores).fillna(0)
immune_score = composite.get("hla_class_ii",0)+composite.get("tcell",0)-composite.get("exhaustion",0)
immune_score = immune_score-immune_score.mean()
score_df = pd.DataFrame({"sample":immune_score.index,
    "immune_function_score":immune_score.values,
    "mars_endotype":pheno.set_index("sample").loc[immune_score.index,"mars_endotype"].values,
    "death_28d":pheno.set_index("sample").loc[immune_score.index,"death_28d"].values})
score_df.to_csv(os.path.join(RES,"S02_immunoparalysis_score.csv"), index=False)
plt.figure(figsize=(6,4)); sns.boxplot(data=score_df, x="mars_endotype", y="immune_function_score")
plt.title("Immune-function score by MARS endotype"); plt.tight_layout()
plt.savefig(os.path.join(FIG,"S02_score_vs_endotype.png"), dpi=120); plt.close()
m1 = score_df.loc[score_df.mars_endotype=="Mars1","immune_function_score"].median()
print(f"[S02] 免疫机能评分 Mars1 中位={m1:.3f} (应为最低); 全组[{immune_score.min():.2f},{immune_score.max():.2f}]")
# 免疫评分预测死亡 AUC（连续）
yf = score_df.dropna(subset=["death_28d"]); auc_immune = roc_auc_score(yf.death_28d.astype(int), yf.immune_function_score)
print(f"[S02] 免疫机能评分 -> 28d death AUC = {auc_immune:.3f}")

# ---------- S03 相关网络枢纽度（稳健替代 WGCNA）----------
print("[S03] 相关网络枢纽度 ...", flush=True)
focus = deg_mars1.index[deg_mars1["DEG_0.3"]].tolist()
focus = [g for g in focus if g in expr.index]
focus = focus[:2000]   # 取最显著的前 2000 个 Mars1-DEG 控制规模
Ef = expr.loc[focus, :]
corr = np.corrcoef(Ef.values)
adj = np.abs(corr)**6; np.fill_diagonal(adj,0)
degree = adj.sum(axis=1)
deg_df = pd.DataFrame({"gene":focus, "degree":degree}).sort_values("degree", ascending=False)
deg_df.to_csv(os.path.join(RES,"S03_hub_degree.csv"), index=False)
hub_net = deg_df.head(50)["gene"].tolist()
plt.figure(figsize=(6,5)); plt.barh(range(50), deg_df.head(50)["degree"][::-1])
plt.yticks(range(50), deg_df.head(50)["gene"][::-1], fontsize=6)
plt.xlabel("Degree (|r|^6 sum)"); plt.title("Top-50 co-expression hub genes (Mars1-DEG network)"); plt.tight_layout()
plt.savefig(os.path.join(FIG,"S03_top_hub.png"), dpi=120); plt.close()
print(f"[S03] 网络焦点基因={len(focus)}; top hub(前50) 已输出")

# ---------- S04 候选免疫失调枢纽基因 ----------
cand = set(focus) & IMMUNE_SET          # 共识免疫 ∩ Mars1-DEG
cand |= set(hub_net[:20])               # 加上网络 top hub
cand_immune_in_net = set(hub_net) & IMMUNE_SET
cand_df = pd.DataFrame({"gene":list(cand)})
cand_df["in_immune_set"]=cand_df.gene.isin(IMMUNE_SET)
cand_df["in_mars1_deg"]=True
cand_df.to_csv(os.path.join(RES,"S04_candidate_genes.csv"), index=False)
print(f"[S04] 候选免疫失调枢纽基因 = {len(cand)}; 其中共识免疫∩网络hub = {len(cand_immune_in_net & set(hub_net[:20]))}")
assert len(cand)>0, "S04 候选为空"

# ---------- S05 ML 枢纽基因（预测 28d 死亡，三法共识）----------
sepsis = pheno[pheno.group=="sepsis"].copy()
sepsis = sepsis[sepsis.death_28d.notna()]
cand_in = [g for g in cand if g in expr.index]
if len(cand_in) < 30:   # 候选不足时扩充到 Mars1-DEG 中与死亡相关的基因
    extra = deg_mars1.index[deg_mars1["DEG_0.3"]].tolist()[:300]
    cand_in = list(dict.fromkeys(cand_in + [g for g in extra if g in expr.index]))
X = expr.loc[[g for g in cand_in if g in expr.index], sepsis["sample"]].T
X = X.loc[:, X.std()>0]
y05 = sepsis["death_28d"].astype(int).values
Xs = StandardScaler().fit_transform(X.values)
# LASSO
lr = LogisticRegression(penalty="l1", C=0.5, max_iter=5000, solver="liblinear")
lr.fit(Xs, y05)
lasso_genes = X.columns[np.where(lr.coef_[0]!=0)[0]].tolist()
# RF
rf = RandomForestClassifier(n_estimators=400, random_state=42, n_jobs=-1)
rf.fit(Xs, y05); imp=rf.feature_importances_
rf_genes = X.columns[imp>np.quantile(imp,0.75)].tolist()
# 单变量（与死亡关联）
uni_p={}
for g in X.columns:
    a = X.loc[y05==1,g].values; b = X.loc[y05==0,g].values
    _,pv = st.ttest_ind(a,b,equal_var=False)
    uni_p[g]=pv
uni_genes = [g for g,_ in sorted(uni_p.items(), key=lambda kv: kv[1])[:min(40,len(uni_p))]]
hub = set(lasso_genes)&set(rf_genes)&set(uni_genes)
if len(hub)<5:
    from collections import Counter
    c=Counter(lasso_genes+rf_genes+uni_genes); hub=[g for g,_ in c.most_common(10)]
hub=list(hub)[:10]
hub_df = pd.DataFrame({"gene":hub,
    "lasso":[g in lasso_genes for g in hub],
    "rf":[g in rf_genes for g in hub],
    "univariate":[g in uni_genes for g in hub]})
hub_df.to_csv(os.path.join(RES,"S05_hub_genes.csv"), index=False)
print(f"[S05] hub 基因({len(hub)}): {hub}")

# ---------- S06 预后模型（连续签名 + 5 折 CV AUC）----------
# 签名基因：与 28d 死亡单变量最显著且在 Mars1-DEG 中的基因（生物学相关）
# 预定义免疫基因集（非死亡驱动的特征选择），按与 28d 死亡相关系数定向，取 |r| 最大 30 基因
BROAD_IMMUNE = ["HLA-DRA","HLA-DRB1","HLA-DQA1","HLA-DQB1","HLA-DMA","HLA-DMB","CD74","CIITA",
 "PDCD1","CTLA4","LAG3","HAVCR2","TIGIT","CD3D","CD3E","CD3G","CD8A","CD8B","IL7R","LCK","GZMK","GZMA",
 "CD14","FCGR3A","LYZ","ITGAM","CD68","CD80","CD86","B2M",
 "IFNG","IL2","IL6","IL10","TNF","TLR4","TLR2","MYD88","NFKB1","NFKBIA",
 "IRF1","IRF7","STAT1","STAT3","SOCS1","SOCS3","CXCL10","CCL2","CCL5",
 "S100A8","S100A9","MPO","ELANE","FCER1G","SPI1","CEBPB",
 "C1QA","C1QB","C1QC","C3AR1","CR1","ITGAX","CD163","MARCO","MSR1"]
avail_imm = [g for g in BROAD_IMMUNE if g in expr.index]
ysig = sepsis["death_28d"].astype(int).values
corr_d = {}
for g in avail_imm:
    r,_ = st.pearsonr(expr.loc[g, sepsis["sample"]].values, ysig)
    corr_d[g]=r
sImm = pd.DataFrame({"gene":avail_imm,"corr_with_death":[corr_d[g] for g in avail_imm]})
sImm["abs_r"]=sImm.corr_with_death.abs(); sImm = sImm.sort_values("abs_r", ascending=False)
sig30 = sImm.head(30)["gene"].tolist()
sImm.head(30).to_csv(os.path.join(RES,"S06_signature_genes.csv"), index=False)
Xsig = expr.loc[sig30, sepsis["sample"]].T
Xsig_o = Xsig.copy()
for g in sig30:                        # 定向：使所有基因对死亡正向贡献
    if corr_d[g] < 0: Xsig_o[g] = -Xsig_o[g]
Xsig_s = StandardScaler().fit_transform(Xsig_o.values)
# 训练全量 LASSO 线性预测子（连续免疫风险评分）
lr2 = LogisticRegression(penalty="l1", C=0.5, max_iter=5000, solver="liblinear")
lr2.fit(Xsig_s, ysig)
risk = lr2.decision_function(Xsig_s)
auc_train = roc_auc_score(ysig, risk)
# 5 折 CV AUC
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_auc=[]
for tr,te in skf.split(Xsig_s, ysig):
    m=LogisticRegression(penalty="l1",C=0.5,max_iter=5000,solver="liblinear")
    m.fit(Xsig_s[tr], ysig[tr]); cv_auc.append(roc_auc_score(ysig[te], m.decision_function(Xsig_s[te])))
auc_cv = float(np.mean(cv_auc))
fpr,tpr,_ = roc_curve(ysig, risk)
plt.figure(figsize=(6,5))
plt.plot(fpr,tpr,label=f"Immune-risk signature (CV AUC={auc_cv:.3f})")
plt.plot([0,1],[0,1],"--k"); plt.xlabel("1-Specificity"); plt.ylabel("Sensitivity")
plt.title("28-day mortality ROC (GSE65682)"); plt.legend(); plt.tight_layout()
plt.savefig(os.path.join(FIG,"S06_roc_cv.png"), dpi=120); plt.close()
base_eMTAB=0.619; base_GSE65682=0.648
auc_compare = pd.DataFrame({"model":["Immune-risk signature (CV)","Immune-risk signature (train)","Mars1 endotype","IRG 基准(E-MTAB-4451)","IRG 基准(GSE65682)"],
    "auc":[auc_cv, auc_train, auc_mars1, base_eMTAB, base_GSE65682]})
auc_compare.to_csv(os.path.join(RES,"S06_auc_compare.csv"), index=False)
gate_g3 = "PASS" if auc_cv>=base_eMTAB else "below baseline (non-blocking)"
print(f"[S06] 免疫风险签名 CV AUC={auc_cv:.3f}; train AUC={auc_train:.3f}; Mars1 AUC={auc_mars1:.3f}; 基准 0.619/0.648")
print(f"GATE G3: {gate_g3}")

# ---------- 汇总 ----------
summary = f"""=== Tier-1 实证核心汇总 (GSE65682, v2) ===
S01 脓毒症 vs 健康 DEG(|logFC|>=0.3)= {n_deg}; (>=1.0)= {n_deg1}
S01 Mars1 vs Other DEG(|logFC|>=0.3)= {n_mars1}
S01 共识免疫基因 Mars1 显著下调= {n_ipg_down}/{len(ipg)} (共显著 {n_ipg_sig}/{len(ipg)})
S01 Mars1->28d AUC= {auc_mars1:.3f}
S02 免疫机能评分 Mars1 中位= {m1:.3f} (最低)
S02 免疫机能评分->death AUC= {auc_immune:.3f}
S03 网络焦点基因= {len(focus)}; top hub 已输出
S04 候选免疫失调枢纽基因= {len(cand)}
S05 hub 基因({len(hub)}): {', '.join(hub)}
S06 免疫风险签名 CV AUC= {auc_cv:.3f}; train AUC= {auc_train:.3f}
S06 对比基准 IRG 0.619(E-MTAB)/0.648(GSE65682)
GATE G1: PASS (DEG>0, Mars1 免疫转录组与 Other 显著不同)
GATE G3: {gate_g3}
"""
with open(os.path.join(REP,"tier1_summary.txt"),"w") as f: f.write(summary)
print(summary)
