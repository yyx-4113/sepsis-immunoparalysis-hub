import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from scipy import stats

np.random.seed(20260905)

df = pd.read_csv("03_results/09_ext_risk_scores.csv")
y = df["y"].values.astype(int)
n = len(y)
n_death = int(y.sum())
n_surv = n - n_death
print(f"n={n} deaths={n_death} survivors={n_surv} prevalence={n_death/n:.4f}")

def auc(a,b):
    return roc_auc_score(a,b)

r_orient = df["risk_oriented_sum"].values.astype(float)
r_lock   = df["risk_locked_l1"].values.astype(float)
r_irg3   = df["risk_irg3"].values.astype(float)

auc_orient = roc_auc_score(y, -r_orient)   # oriented sum: higher expression -> higher risk? verify orientation
auc_lock   = roc_auc_score(y, -r_lock)
auc_irg3   = roc_auc_score(y, -r_irg3)
print(f"AUC oriented_sum (raw): {roc_auc_score(y, r_orient):.4f}")
print(f"AUC oriented_sum (-sign): {auc_orient:.4f}")
print(f"AUC locked_l1 (raw): {roc_auc_score(y, r_lock):.4f}")
print(f"AUC locked_l1 (-sign): {auc_lock:.4f}")
print(f"AUC irg3 (-sign): {auc_irg3:.4f}")

# bootstrap CI 2000 samples
B = 2000
def boot_ci(risk):
    rng = np.random.default_rng(20260905)
    aucs = np.empty(B)
    for i in range(B):
        idx = rng.integers(0, n, n)
        # need both classes present
        yy = y[idx]; rr = risk[idx]
        if yy.sum()==0 or yy.sum()==n:
            aucs[i] = np.nan; continue
        aucs[i] = roc_auc_score(yy, -rr)
    aucs = aucs[~np.isnan(aucs)]
    lo, hi = np.percentile(aucs, [2.5, 97.5])
    return aucs.mean(), lo, hi, len(aucs)

m_o, lo_o, hi_o, k_o = boot_ci(r_orient)
m_l, lo_l, hi_l, k_l = boot_ci(r_lock)
print(f"\n[Bootstrap B={B}, usable={k_o}]")
print(f"oriented_sum AUC={m_o:.4f} CI=({lo_o:.4f}, {hi_o:.4f})  span={hi_o-lo_o:.4f}")
print(f"locked_l1   AUC={m_l:.4f} CI=({lo_l:.4f}, {hi_l:.4f})  span={hi_l-lo_l:.4f}")

# Calibration: standardize oriented sum, logistic regression y ~ z
from sklearn.linear_model import LogisticRegression
z = (r_orient - r_orient.mean())/r_orient.std()
lr = LogisticRegression(C=1e9, fit_intercept=True, solver="lbfgs")
lr.fit(z.reshape(-1,1), y)
slope = lr.coef_[0][0]
intercept = lr.intercept_[0]
print(f"\n[Calibration on standardized oriented_sum]")
print(f"intercept={intercept:.4f} slope={slope:.4f}")
# CI + p for slope==1 via statsmodels-style: use bootstrap of slope
rng = np.random.default_rng(20260905)
slopes = np.empty(B); ints=np.empty(B)
for i in range(B):
    idx = rng.integers(0, n, n)
    yy = y[idx]; zz = z[idx]
    if yy.sum()==0 or yy.sum()==n:
        slopes[i]=np.nan; ints[i]=np.nan; continue
    l2 = LogisticRegression(C=1e9, fit_intercept=True, solver="lbfgs")
    l2.fit(zz.reshape(-1,1), yy)
    slopes[i]=l2.coef_[0][0]; ints[i]=l2.intercept_[0]
slopes=slopes[~np.isnan(slopes)]; ints=ints[~np.isnan(ints)]
s_lo, s_hi = np.percentile(slopes,[2.5,97.5])
i_lo, i_hi = np.percentile(ints,[2.5,97.5])
# p slope==1: two-sided
p_slope = 2*min((slopes<1).mean(), (slopes>=1).mean())
print(f"slope CI=({s_lo:.4f},{s_hi:.4f})  intercept CI=({i_lo:.4f},{i_hi:.4f})  p(slope==1)={p_slope:.5f}")

# DCA recompute from probability derived from calibrated logit of oriented sum
# Use logistic transform: p = 1/(1+exp(-(a + b*z))) with fitted a,b
p = 1.0/(1.0+np.exp(-(intercept + slope*z)))
print(f"\n[DCA] probability range: min={p.min():.4f} max={p.max():.4f}")
# DCA grid
print("thr  n_flagged  TP  FP  NB_model  NB_treat_all")
for thr in [0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
    flagged = p >= thr
    TP = int((flagged & (y==1)).sum())
    FP = int((flagged & (y==0)).sum())
    nb = TP/n - (FP/n)*(thr/(1-thr))
    nb_all = n_death/n - (n_surv/n)*(thr/(1-thr))
    print(f"{thr:.2f}  {int(flagged.sum()):3d}      {TP:3d} {FP:3d}   {nb:.4f}    {nb_all:.4f}")
