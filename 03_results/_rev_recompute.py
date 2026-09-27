# -*- coding: utf-8 -*-
# Independent reviewer recomputation. Reads from absolute paths.
import numpy as np, pandas as pd
from scipy import optimize, stats
from sklearn.metrics import roc_auc_score

BASE = r"D:\2026.9\极速交付9月会员日优惠套路\05_多组学+虚拟敲除药物发现\方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位\03_results"

print("="*70)
print("RECOMP 1: External AUC (oriented-sum) vs IRG benchmark + DeLong")
print("="*70)
df = pd.read_csv(BASE + "/09_ext_risk_scores.csv")
y = df["y"].astype(int).values
print("n samples =", len(y), " deaths =", int(y.sum()), " prev =", y.mean())

auc_oriented = roc_auc_score(y, df["risk_oriented_sum"].values)
auc_irg = roc_auc_score(y, df["risk_irg3"].values)
auc_lockedl1 = roc_auc_score(y, df["risk_locked_l1"].values)
print("oriented-sum AUC =", round(auc_oriented,4))
print("IRG3 AUC        =", round(auc_irg,4))
print("locked-L1 AUC   =", round(auc_lockedl1,4))

# --- paired bootstrap difference ---
rng = np.random.default_rng(123)
B = 5000
diffs = np.empty(B)
for i in range(B):
    idx = rng.integers(0, len(y), len(y))
    if len(set(y[idx])) < 2:
        diffs[i] = np.nan; continue
    diffs[i] = roc_auc_score(y[idx], df["risk_oriented_sum"].values[idx]) - roc_auc_score(y[idx], df["risk_irg3"].values[idx])
diffs = diffs[~np.isnan(diffs)]
lo, hi = np.percentile(diffs, 2.5), np.percentile(diffs, 97.5)
p_boot = 2*min(np.mean(diffs>=0), np.mean(diffs<=0))
print("paired-bootstrap diff AUC(oriented - IRG) = %.4f  CI[%.4f, %.4f]  P(2-sided)=%.3f" % (auc_oriented-auc_irg, lo, hi, p_boot))

# --- DeLong test (Sun & Xu 2014) ---
def delong(X1, X2, y):
    # X1, X2: risk scores; y: 0/1
    y = np.asarray(y); X1=np.asarray(X1); X2=np.asarray(X2)
    n1 = np.sum(y==1); n0 = np.sum(y==0)
    def struct_k(s, y):
        # placement values for score s
        v = np.zeros_like(s, dtype=float)
        for cls in (0,1):
            s_cls = s[y==cls]; n = len(s_cls)
            order = np.argsort(s_cls)
            ranks = np.empty(n); ranks[order] = np.arange(1,n+1)
            auc = (np.sum(ranks[y[y==cls].index]) ) if False else None
        # vectorized placement
        v1 = np.array([np.sum(s[y==1] > si) + 0.5*np.sum(s[y==1]==si) for si in s])
        v0 = np.array([np.sum(s[y==0] > si) + 0.5*np.sum(s[y==0]==si) for si in s])
        return v1, v0
    # Simpler: use the standard DeLong covariance on placement values
    def place(s, y):
        # V10 (for cases): for each case i, count controls with score < s_i + 0.5 equal
        # We'll compute per-observation placement of controls w.r.t each case
        f = lambda s_i: np.sum(s[y==0] < s_i) + 0.5*np.sum(s[y==0]==s_i)
        V10 = np.array([f(si) for si in s[y==1]])
        g = lambda s_i: np.sum(s[y==1] < s_i) + 0.5*np.sum(s[y==1]==s_i)
        V01 = np.array([g(si) for si in s[y==0]])
        return V10, V01
    V10_1, V01_1 = place(X1, y)
    V10_2, V01_2 = place(X2, y)
    auc1 = V10_1.mean()/n0
    auc2 = V10_2.mean()/n0
    # covariance
    S10 = np.cov(V10_1, V10_2, ddof=1)  # 2x2
    S01 = np.cov(V01_1, V01_2, ddof=1)
    var = S10[0,0]/(n1*n0**2) + S10[1,1]/(n1**2*n0) - 2*S10[0,1]/(n1**2*n0**2)*n1*n0
    # proper DeLong var of difference
    v11 = S10[0,0]/(n1*n0**2) + S01[0,0]/(n0*n1**2)
    v22 = S10[1,1]/(n1*n0**2) + S01[1,1]/(n0*n1**2)
    v12 = S10[0,1]/(n1*n0**2) + S01[0,1]/(n0*n1**2)
    var_diff = v11 + v22 - 2*v12
    z = (auc1-auc2)/np.sqrt(var_diff)
    p = 2*(1-stats.norm.cdf(abs(z)))
    return auc1, auc2, z, p

a1,a2,z,p = delong(df["risk_oriented_sum"].values, df["risk_irg3"].values, y)
print("DeLong: AUC1=%.4f AUC2=%.4f z=%.3f P=%.4f" % (a1,a2,z,p))

print()
print("="*70)
print("RECOMP 2: Calibration slope/intercept on z-standardized score + bootstrap CI")
print("="*70)
z = (df["risk_oriented_sum"].values - df["risk_oriented_sum"].mean())/df["risk_oriented_sum"].std()
def negll(beta, X, y):
    a,b = beta
    eta = a + b*X
    p = 1.0/(1.0+np.exp(-eta)); p=np.clip(p,1e-12,1-1e-12)
    return -np.sum(y*np.log(p)+(1-y)*np.log(1-p))
res = optimize.minimize(negll,[0.0,1.0],args=(z,y),method="BFGS")
a,b = res.x
print("point estimate: intercept=%.4f slope=%.4f" % (a,b))
# bootstrap
rng = np.random.default_rng(7)
Bs=2000; slopes=np.empty(Bs); intercepts=np.empty(Bs)
for i in range(Bs):
    idx = rng.integers(0,len(y),len(y))
    if len(set(y[idx]))<2:
        slopes[i]=np.nan; intercepts[i]=np.nan; continue
    r = optimize.minimize(negll,[0.0,1.0],args=(z[idx],y[idx]),method="BFGS")
    intercepts[i],slopes[i]=r.x
slopes=slopes[~np.isnan(slopes)]; intercepts=intercepts[~np.isnan(intercepts)]
print("bootstrap slope  95%% CI = [%.3f, %.3f]" % (np.percentile(slopes,2.5), np.percentile(slopes,97.5)))
print("bootstrap slope  mean=%.3f median=%.3f" % (slopes.mean(), np.median(slopes)))
print("bootstrap intercept 95%% CI = [%.3f, %.3f]" % (np.percentile(intercepts,2.5), np.percentile(intercepts,97.5)))
print("CI crosses 1.0?", np.percentile(slopes,2.5)<1.0 and np.percentile(slopes,97.5)>1.0)

print()
print("="*70)
print("RECOMP 3: DCA net benefit grid (verify zero-crossing & uncalibrated-prob)")
print("="*70)
eta = a + b*z
p = 1.0/(1.0+np.exp(-eta))   # probabilities from the calibration fit
# ALSO raw uncalibrated: plogis(z) with slope1 intercept0
p_raw = 1.0/(1.0+np.exp(-z))
thr = np.linspace(0.05,0.95,91)
prev = y.mean()
nb_fit=np.zeros_like(thr); nb_raw=np.zeros_like(thr); nb_all=np.zeros_like(thr)
for k,t in enumerate(thr):
    nb_fit[k] = np.mean((p>=t)&(y==1))/len(y) - np.mean((p>=t)&(y==0))/len(y)*t/(1-t)
    nb_raw[k] = np.mean((p_raw>=t)&(y==1))/len(y) - np.mean((p_raw>=t)&(y==0))/len(y)*t/(1-t)
    nb_all[k] = prev - (1-prev)*t/(1-t)
# find zero crossings
zc_fit = thr[np.where(np.diff(np.sign(nb_fit))!=0)[0]]
zc_raw = thr[np.where(np.diff(np.sign(nb_raw))!=0)[0]]
print("DCA using CALIBRATION-FIT probs: zero-crossing threshold ~", [round(float(x),2) for x in zc_fit])
print("DCA using RAW plogis(z) probs:   zero-crossing threshold ~", [round(float(x),2) for x in zc_raw])
print("At thr=0.80: nb_fit=%.4f nb_raw=%.4f nb_treat_all=%.4f" % (float(np.interp(0.8,thr,nb_fit)), float(np.interp(0.8,thr,nb_raw)), float(np.interp(0.8,thr,nb_all))))
print("At thr=0.10: nb_fit=%.4f nb_treat_all=%.4f" % (float(np.interp(0.1,thr,nb_fit)), float(np.interp(0.1,thr,nb_all))))
print("Model NB exceeds treat-all NB for thr in:",
      [round(float(thr[k]),2) for k in range(len(thr)) if nb_fit[k]>nb_all[k]+1e-9])
print("Are probs from code = calibration-fit probs (slope<1)? ->", b<1)

print()
print("="*70)
print("RECOMP 4: MR Egger vs IVW SEs + '1/45' family significance")
print("="*70)
for fn in ["10_genetics_mr_outcome5086_28ddeath.csv",
           "10_genetics_mr_outcome4982_criticalcare.csv",
           "10_genetics_mr.csv"]:
    d = pd.read_csv(BASE+"/"+fn)
    print("--", fn)
    for _,row in d[d['gene']=='CD74'].iterrows():
        if row['method'] in ('IVW','MR-Egger'):
            print("   CD74 %s: nsnp=%s beta=%.4f se=%.4f OR=%.4f p=%.3e" % (row['method'], row['nsnp'], row['beta'], row['se'], row['or_'], row['p']))
# family file
fam = pd.read_csv(BASE+"/10_mr_bh_family.csv")
sig = fam[fam['family_sig_q<0.05']=='YES']
print("Family-significant tests (q_family<0.05):", len(sig))
print(sig[['gene','method','outcome','or_','p','q_family_45test']].to_string(index=False))
print("Total tests in family file:", len(fam))

print()
print("="*70)
print("RECOMP 5: EPV for 30-gene L1 model")
print("="*70)
# death events in GSE65682 sepsis with known outcome
# from manuscript: 114 deaths / 30 genes = 3.8
print("Manuscript EPV: 114 death events / 30 genes = 3.8")
print("Mapped genes (EMTAB): 29 ; trainable genes after orientation:", 
      "see 09_external_validation.csv n_signature_genes_mapped_EMTAB4451")
ext = pd.read_csv(BASE+"/09_external_validation.csv")
print(ext.to_string(index=False))
