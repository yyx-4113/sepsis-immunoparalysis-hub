# -*- coding: utf-8 -*-
# T1-2: MR diagnostic plots from SNP-level harmonised data.
#   Fig 1: 45-test forest (all genes x estimators x outcomes), family-q coloured.
#   Fig 2: 2x2 diagnostics for the CD14 28-day-death analysis (only nominally sig Egger):
#          scatter (beta_e vs beta_o + IVW/Egger lines), Egger funnel, leave-one-out IVW,
#          and CD74 critical-care scatter (the reversed-direction family-significant signal).
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(PROJ, "03_results")
FIG = os.path.join(PROJ, "04_figures")

def ivw_egger(h):
    # h: dataframe with beta_e, se_e, beta_o, se_o
    be = h["beta_e"].values.astype(float)
    bo = h["beta_o"].values.astype(float)
    seo = h["se_o"].values.astype(float)
    ratio = bo / be
    var_ratio = (seo / be) ** 2
    w = 1.0 / var_ratio
    b_ivw = np.sum(w * ratio) / np.sum(w)
    se_ivw = 1.0 / np.sqrt(np.sum(w))
    # MR-Egger (Bowden 2015): regress beta_o on beta_e, weights 1/var(beta_o).
    #   slope  = causal effect (log OR per unit expression)
    #   intercept = horizontal pleiotropy
    x = be; y = bo; ww = 1.0 / (seo ** 2)
    W = np.diag(ww)
    X = np.vstack([np.ones_like(x), x]).T
    beta_eg = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
    resid = y - X @ beta_eg
    dof = len(x) - 2
    sigma2 = (resid @ W @ resid) / dof
    cov = sigma2 * np.linalg.inv(X.T @ W @ X)
    se_int, se_slope = np.sqrt(np.diag(cov))
    return dict(b_ivw=b_ivw, se_ivw=se_ivw, eg_int=beta_eg[0], eg_slope=beta_eg[1],
                eg_int_se=se_int, eg_slope_se=se_slope, ratio=ratio, var_ratio=var_ratio, be=be, bo=bo)

OUTMAP = {"suscept":"Sepsis susceptibility (4980)",
          "28ddeath":"28-day death (5086, primary)",
          "criticalcare":"Critical care (4982)"}
files = {"suscept":"10_genetics_mr.csv",
         "28ddeath":"10_genetics_mr_outcome5086_28ddeath.csv",
         "criticalcare":"10_genetics_mr_outcome4982_criticalcare.csv"}
fam = pd.read_csv(os.path.join(RES, "10_mr_bh_family.csv"))
fam["outcome_key"] = fam["outcome"].str.replace("_suscept","_suscept").str.replace("4980","suscept").str.replace("5086","28ddeath").str.replace("4982","criticalcare")

rows = []
for key, fn in files.items():
    d = pd.read_csv(os.path.join(RES, fn))
    for _, r in d.iterrows():
        frow = fam[(fam.gene==r.gene)&(fam.method==r.method)&(fam.outcome.str.contains(key[:4]))]
        q = frow["q_family_45test"].values[0] if len(frow) else np.nan
        sig = frow["family_sig_q<0.05"].values[0] if len(frow) else "no"
        rows.append(dict(gene=r.gene, method=r.method, outcome=OUTMAP[key],
                         orv=float(r.or_), lo=float(r.ci_lo), hi=float(r.ci_hi),
                         p=float(r.p), q=q, sig=sig))
fr = pd.DataFrame(rows)

# ---------------- Fig 1: forest ----------------
order = ["CD74","HLA-DQA1","CD14","HAVCR2","FIS1"]
methods = ["IVW","MR-Egger","Weighted median"]
outcomes = list(OUTMAP.values())
labels = []
ys = []
orv=[]; lo=[]; hi=[]; siglist=[]
yi = 0
for oc in outcomes:
    for g in order:
        for m in methods:
            sub = fr[(fr.gene==g)&(fr.outcome==oc)&(fr.method==m)]
            if len(sub)==0:
                continue
            s = sub.iloc[0]
            labels.append(f"{g} {m}")
            orv.append(s.orv); lo.append(s.lo); hi.append(s.hi)
            siglist.append(str(s.sig).strip().lower()=="yes")
            ys.append(yi); yi += 1
ys = np.array(ys); orv=np.array(orv); lo=np.array(lo); hi=np.array(hi); siglist=np.array(siglist)
fig, ax = plt.subplots(figsize=(8.5, 11))
ax.errorbar(orv, ys, xerr=[orv-lo, hi-orv], fmt="none", ecolor="#888888", capsize=2, elinewidth=0.8)
ax.scatter(orv[~siglist], ys[~siglist], color="#555555", s=14, zorder=3)
ax.scatter(orv[siglist], ys[siglist], color="#c0392b", s=16, zorder=3)
ax.axvline(1.0, color="k", lw=0.8, ls="--")
ax.set_yticks(ys); ax.set_yticklabels(labels, fontsize=6)
ax.set_xscale("log"); ax.set_xlabel("OR (per unit eQTL-predicted expression)")
ax.set_title("MR of hub-gene expression on sepsis outcomes (45 tests; red = family q<0.05)")
ax.set_xlim(0.4, 3.0)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "mr_forest.png"), dpi=140)
print("wrote mr_forest.png")

# ---------------- Fig 2: diagnostics ----------------
h14 = pd.read_csv(os.path.join(RES, "10_genetics_mr_outcome5086_harmonised.csv"))
h74 = pd.read_csv(os.path.join(RES, "10_genetics_mr_outcome4982_harmonised.csv"))
g14 = h14[h14.gene=="CD14"].reset_index(drop=True)
g74 = h74[h74.gene=="CD74"].reset_index(drop=True)
s14 = ivw_egger(g14); s74 = ivw_egger(g74)

fig, ax = plt.subplots(2, 2, figsize=(11, 9))

# (a) CD14 scatter beta_e vs beta_o with IVW & Egger lines
ax[0,0].scatter(s14["be"], s14["bo"], color="#1f77b4")
xe = np.linspace(s14["be"].min(), s14["be"].max(), 50)
ax[0,0].plot(xe, s14["b_ivw"]*xe, "r-", label=f"IVW slope={s14['b_ivw']:.3f}")
ax[0,0].plot(xe, s14["eg_int"]+s14["eg_slope"]*xe, "g--", label=f"Egger slope={s14['eg_slope']:.3f} (int={s14['eg_int']:.3f})")
ax[0,0].set_xlabel("eQTL effect on expression (beta_e)"); ax[0,0].set_ylabel("GWAS effect on 28-d death (beta_o)")
ax[0,0].set_title("CD14 — 28-day death: exposure vs outcome"); ax[0,0].legend(fontsize=7)

# (b) CD14 Egger funnel
prec = 1.0/np.sqrt(s14["var_ratio"])
ax[0,1].scatter(prec, s14["ratio"], color="#1f77b4")
xs = np.linspace(0, prec.max(), 50)
ax[0,1].plot(xs, s14["eg_int"]+s14["eg_slope"]*xs, "g--", lw=1)
ax[0,1].axhline(0, color="k", lw=0.8, ls=":")
ax[0,1].set_xlabel("precision (1/SE of ratio)"); ax[0,1].set_ylabel("ratio estimate (beta_o/beta_e)")
ax[0,1].set_title("CD14 — Egger funnel (no-pleiotropy line at 0)")

# (c) CD14 leave-one-out IVW
loo_or=[]; loo_lo=[]; loo_hi=[]
for i in range(len(g14)):
    hh = g14.drop(index=i).reset_index(drop=True)
    ss = ivw_egger(hh)
    loo_or.append(np.exp(ss["b_ivw"]))
    loo_lo.append(np.exp(ss["b_ivw"]-1.96*ss["se_ivw"]))
    loo_hi.append(np.exp(ss["b_ivw"]+1.96*ss["se_ivw"]))
ax[1,0].errorbar(range(len(loo_or)), loo_or, yerr=[np.array(loo_or)-np.array(loo_lo), np.array(loo_hi)-np.array(loo_or)],
                 fmt="o", color="#c0392b", capsize=2, ms=3)
ax[1,0].axhline(1.0, color="k", lw=0.8, ls="--")
ax[1,0].set_xticks(range(len(loo_or))); ax[1,0].set_xticklabels(g14["rsid"], rotation=90, fontsize=5)
ax[1,0].set_ylabel("IVW OR (omit-one-SNP)"); ax[1,0].set_title("CD14 — leave-one-out IVW")

# (d) CD74 critical-care scatter (reversed direction)
ax[1,1].scatter(s74["be"], s74["bo"], color="#9467bd")
xe2 = np.linspace(s74["be"].min(), s74["be"].max(), 50)
ax[1,1].plot(xe2, s74["b_ivw"]*xe2, "r-", label=f"IVW slope={s74['b_ivw']:.3f} (OR={np.exp(s74['b_ivw']):.2f})")
ax[1,1].plot(xe2, s74["eg_int"]+s74["eg_slope"]*xe2, "g--", label=f"Egger slope={s74['eg_slope']:.3f}")
ax[1,1].set_xlabel("eQTL effect on expression (beta_e)"); ax[1,1].set_ylabel("GWAS effect on critical care (beta_o)")
ax[1,1].set_title("CD74 — critical care (reversed direction, family-q<0.05)"); ax[1,1].legend(fontsize=7)

fig.tight_layout(); fig.savefig(os.path.join(FIG, "mr_diag.png"), dpi=140)
print("wrote mr_diag.png")
print(f"CD14 IVW slope={s14['b_ivw']:.4f} OR={np.exp(s14['b_ivw']):.3f}; Egger slope={s14['eg_slope']:.4f} int={s14['eg_int']:.4f}")
print(f"CD74 crit IVW slope={s74['b_ivw']:.4f} OR={np.exp(s74['b_ivw']):.3f}; Egger slope={s74['eg_slope']:.4f} int={s74['eg_int']:.4f}")
