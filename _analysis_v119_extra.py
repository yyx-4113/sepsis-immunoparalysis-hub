#!/usr/bin/env python3
# v1.19.0 — Round-18 supplementary analyses (M1 / B2-3 / B2-6 / M2)
import csv, math, os
import numpy as np
import pandas as pd
from scipy import stats

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/05_多组学+虚拟敲除药物发现/方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位/"
RES = ROOT + "03_results/"
ONE = ROOT + "01_data/"

# ----------------------------------------------------------------------------
# limma-style moderated t (reused from run_tier1.py)
def fit_limma(E, group, lvl_a, lvl_b):
    mask = group.isin([lvl_a, lvl_b]).values
    Esub = E.iloc[:, mask]; gsub = group.iloc[mask]
    design = pd.DataFrame({lv:(gsub==lv).astype(float).values for lv in [lvl_a, lvl_b]}, index=gsub.index)
    X = design.values.astype(float); Y = Esub.T.values.astype(float)
    XtX = X.T @ X
    beta = np.linalg.solve(XtX, X.T @ Y)
    resid = Y - X @ beta
    n, p = X.shape; df_resid = n - p
    RSS = (resid**2).sum(axis=0)
    s2 = RSS/df_resid; m = s2.mean(); v = s2.var(ddof=1) if df_resid>1 else s2.var()
    prior_df = np.clip(2*m**2/max(v,1e-12), 1e-2, 1e5); prior_var = m
    mod_var = (df_resid*s2 + prior_df*prior_var)/(df_resid+prior_df)
    cv = 1.0/df_resid  # balanced 2-group contrast, XtX=[[n1,n12],[n12,n2]] -> contrast var
    ci = list(design.columns).index(lvl_a); cj = list(design.columns).index(lvl_b)
    contrast = np.zeros(len(design.columns)); contrast[ci]=1; contrast[cj]=-1
    cv = float(contrast @ np.linalg.inv(XtX) @ contrast)
    stat = contrast @ beta
    t = stat/np.sqrt(mod_var*cv + 1e-12)
    df_tot = df_resid + prior_df
    p = 2*(1 - stats.t.cdf(np.abs(t), df_tot))
    padj = stats.false_discovery_control(p, method="bh")
    out = pd.DataFrame({"logFC":stat, "t":t, "P.Value":p, "adj.P.Val":padj}, index=Esub.index)
    out["DEG_0.3"] = (np.abs(stat)>=0.3)&(padj<0.05)
    return out

print("Loading expression + phenotype ...")
expr = pd.read_csv(ONE+"GSE65682/GSE65682_expr.csv", index_col=0)
pheno = pd.read_csv(ONE+"GSE65682/GSE65682_pheno.csv")
pheno = pheno.set_index("sample")
common = [s for s in expr.columns if s in pheno.index]
E = expr[common]; g = pheno.loc[common, "mars_endotype"]

# ----------------------------------------------------------------------------
# M1 — endotype-only DE: Mars1 vs (Mars2+Mars3+Mars4 pooled)
endo = g.isin(["Mars1","Mars2","Mars3","Mars4"])
Ee = E.loc[:, endo]; ge = g.loc[endo].copy()
ge = ge.replace({"Mars2":"OtherEndo","Mars3":"OtherEndo","Mars4":"OtherEndo"})
deg_endo = fit_limma(Ee, ge, "Mars1", "OtherEndo")  # Other = Mars2/3/4 pool
deg_endo.to_csv(RES+"S01_mars1_deg_endotypeonly.csv")
print(f"M1: Mars1 vs (Mars2/3/4) n_Mars1={(ge=='Mars1').sum()}, n_ref={(ge!='Mars1').sum()}, DEG(0.3)={int(deg_endo['DEG_0.3'].sum())}")

# S01b sensitivity table for the 25 consensus immune genes
cons = pd.read_csv(RES+"S01_immunoparalysis_direction.csv")
allother = pd.read_csv(RES+"S01_mars1_deg.csv").set_index("gene")
rows = []
for _, r in cons.iterrows():
    gene = r["gene"]
    ao = allother.loc[gene] if gene in allother.index else None
    en = deg_endo.loc[gene] if gene in deg_endo.index else None
    lfc_ao = float(ao["logFC"]) if ao is not None else float('nan')
    ap_ao  = float(ao["adj.P.Val"]) if ao is not None else float('nan')
    lfc_en = float(en["logFC"]) if en is not None else float('nan')
    ap_en  = float(en["adj.P.Val"]) if en is not None else float('nan')
    keep = (abs(lfc_en)>=0.3 and ap_en<0.05) if en is not None else False
    rows.append([gene, f"{lfc_ao:.3f}", f"{ap_ao:.2e}", f"{lfc_en:.3f}", f"{ap_en:.2e}",
                 "yes" if keep else "no"])
with open(RES+"S01b_endotypeonly_sensitivity.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["gene","logFC_allOther","adj.P_allOther","logFC_endotypeOnly","adj.P_endotypeOnly","retains_0.3_FDR05"])
    w.writerows(rows)
print("M1: wrote S01b_endotypeonly_sensitivity.csv")
for r in rows:
    print("   ", r)

# ----------------------------------------------------------------------------
# B2-3 — DCA grid patient counts (n_flagged, TP, FP)
risk = pd.read_csv(RES+"09_ext_risk_scores.csv")
y = risk["y"].values.astype(float)
z = (risk["risk_oriented_sum"].values - risk["risk_oriented_sum"].values.mean())/risk["risk_oriented_sum"].values.std()
a, b = -0.0382, 0.5028
calib = 1/(1+np.exp(-(a + b*z)))
grid = pd.read_csv(RES+"09_ext_dca_grid.csv")
nfl=[]; tp=[]; fp=[]
for th in grid["threshold"]:
    flagged = calib >= th
    nfl.append(int(flagged.sum())); tp.append(int((flagged&(y==1)).sum())); fp.append(int((flagged&(y==0)).sum()))
grid["n_flagged"]=nfl; grid["TP"]=tp; grid["FP"]=fp
grid.to_csv(RES+"09_ext_dca_grid.csv", index=False)
print("B2-3: DCA grid augmented with n_flagged/TP/FP")

# ----------------------------------------------------------------------------
# B2-6 — L1000 z vs library background
lib = pd.read_csv(RES+"S08_l1000_rescue_trtcp.csv")
# find rescue column
rcol = [c for c in lib.columns if "rescue" in c.lower() and "rank" not in c.lower()][0]
bg = lib[rcol].values.astype(float)
mu, sd = bg.mean(), bg.std()
cand = pd.read_csv(RES+"S08_l1000_candidate_scores.csv")
rscores = cand["rescue_score"].values.astype(float)
zs = (rscores-mu)/sd
empP = np.array([(bg >= r).mean() for r in rscores])
cand["rescue_z_vs_background"]=zs
cand["rank_empirical_p"]=empP
cand["background_mean"]=mu
cand["background_sd"]=sd
cand.to_csv(RES+"S08_l1000_candidate_scores.csv", index=False)
print(f"B2-6: library background mean={mu:.5f} sd={sd:.5f}")
for _, r in cand.iterrows():
    print(f"   {r['candidate']:14s} rescue={r['rescue_score']:.4f} z={r['rescue_z_vs_background']:+.2f} empP={r['rank_empirical_p']:.2f}")

# ----------------------------------------------------------------------------
# M2 — binomial null for concordance metric
# immune background: 21/25 consensus immune genes both Mars1-down & FDR<0.05
immune_genes = cons["gene"].tolist()
imm_down = sum(1 for _,r in cons.iterrows() if r["direction"]=="Mars1_down" and float(r["adj.P.Val"])<0.05)
p_bg_immune = imm_down/len(immune_genes)   # 21/25 = 0.84
# all-gene background: 2592 down of 3597 DEGs -> fraction down = 2592/11519
p_bg_all = 2592/11519
print(f"\nM2: immune background p={p_bg_immune:.3f} ({imm_down}/{len(immune_genes)}); all-gene background p={p_bg_all:.3f}")
drugs = list(csv.DictReader(open(RES+"08_candidates_drugs.csv", encoding='utf-8')))
out=[]
for d in drugs:
    k=int(d["n_rescue_mars1down"]); n=int(d["n_target_genes"])
    P_immune=sum(math.comb(n,i)*(p_bg_immune**i)*((1-p_bg_immune)**(n-i)) for i in range(k,n+1))
    P_all   =sum(math.comb(n,i)*(p_bg_all**i)*((1-p_bg_all)**(n-i)) for i in range(k,n+1))
    out.append((d["compound"], k, n, f"{float(d['rescue_fraction']):.3f}", f"{P_immune:.3f}", f"{P_all:.3f}"))
    print(f"   {d['compound']:22s} {k}/{n} frac={float(d['rescue_fraction']):.3f} Pimmune={P_immune:.3f} Pall={P_all:.3f}")
# append columns to 08_candidates_drugs.csv
cols = list(drugs[0].keys()) + ["binom_p_immune_bg","binom_p_allgene_bg"]
with open(RES+"08_candidates_drugs.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for d,o in zip(drugs,out):
        d["binom_p_immune_bg"]=o[4]; d["binom_p_allgene_bg"]=o[5]; w.writerow(d)
print("\nDONE v1.19.0 extra analyses.")
