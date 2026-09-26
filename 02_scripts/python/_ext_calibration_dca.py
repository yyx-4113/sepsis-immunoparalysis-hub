# -*- coding: utf-8 -*-
# T1-1: External-cohort (E-MTAB-4451) calibration + decision-curve analysis for the
# fixed-orientation equal-weight immune-risk score, replacing the stub DCA claim.
# Reads 09_ext_risk_scores.csv; writes 04_figures/S06_dca.png (calibration + DCA) and
# prints calibration slope/intercept and net-benefit summary for the manuscript.
import os
import numpy as np
import pandas as pd
from scipy import optimize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJ = "D:/2026.9/极速交付9月会员日优惠套路/05_多组学+虚拟敲除药物发现/方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位"
RES = os.path.join(PROJ, "03_results")
FIG = os.path.join(PROJ, "04_figures")

df = pd.read_csv(os.path.join(RES, "09_ext_risk_scores.csv"))
y = df["y"].astype(int).values
z = (df["risk_oriented_sum"].values - df["risk_oriented_sum"].mean()) / df["risk_oriented_sum"].std()

# --- logistic calibration fit: logit(p) = a + b*z  ---
def negll(beta, X, y):
    a, b = beta
    eta = a + b * X
    p = 1.0 / (1.0 + np.exp(-eta))
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return -np.sum(y * np.log(p) + (1 - y) * np.log(1 - p))
res = optimize.minimize(negll, [0.0, 1.0], args=(z, y), method="BFGS")
a, b = res.x
eta = a + b * z
p = 1.0 / (1.0 + np.exp(-eta))

# AUC (manual, rank-based)
def auc_manual(y, score):
    order = np.argsort(score)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(score) + 1)
    n_pos = y.sum(); n_neg = len(y) - n_pos
    # average ranks for ties
    s = pd.Series(score)
    avg_rank = s.rank(method="average").values
    return (avg_rank[y == 1].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)
auc = auc_manual(y, eta)

prev = y.mean()
print(f"n={len(y)}  deaths={int(y.sum())}  prevalence={prev:.3f}")
print(f"logistic calibration: intercept(a)={a:.4f}  slope(b)={b:.4f}  AUC={auc:.4f}")

# --- calibration plot: observed fraction per decile of predicted p ---
bins = np.linspace(0, 1, 11)
idx = np.digitize(p, bins) - 1
idx = np.clip(idx, 0, 9)
obs = np.zeros(10); pred = np.zeros(10); nbin = np.zeros(10)
for i in range(10):
    m = idx == i
    if m.sum() > 0:
        obs[i] = y[m].mean(); pred[i] = p[m].mean(); nbin[i] = m.sum()
# binomial 95% CI for observed
lo = obs - 1.96 * np.sqrt(obs * (1 - obs) / np.maximum(nbin, 1))
hi = obs + 1.96 * np.sqrt(obs * (1 - obs) / np.maximum(nbin, 1))

# --- decision curve analysis ---
thr = np.linspace(0.05, 0.95, 91)
nb_model = np.zeros_like(thr); nb_all = np.zeros_like(thr); nb_none = np.zeros_like(thr)
for k, t in enumerate(thr):
    pred_pos = p >= t
    tp = int(np.sum((pred_pos) & (y == 1)))
    fp = int(np.sum((pred_pos) & (y == 0)))
    nb_model[k] = tp / len(y) - (fp / len(y)) * (t / (1 - t))
    nb_all[k] = prev - (1 - prev) * (t / (1 - t))
    nb_none[k] = 0.0
# net benefit at a few key thresholds
for t in (0.2, 0.3, 0.5):
    nb_t = float(np.interp(t, thr, nb_model))
    print(f"  threshold={t:.2f}: model NB={nb_t:.4f}  treat-all NB={prev-(1-prev)*t/(1-t):.4f}")

# --- figure: calibration (left) + DCA (right) ---
fig, ax = plt.subplots(1, 2, figsize=(11, 4.6))
ax[0].plot([0, 1], [0, 1], "k--", lw=1, label="perfect calibration")
ax[0].errorbar(pred, obs, yerr=[obs - lo, hi - obs], fmt="o", color="#1f77b4",
               ecolor="#1f77b4", capsize=3, label="observed (binned)")
ax[0].set_xlabel("Predicted probability (external equal-weight score)")
ax[0].set_ylabel("Observed 28-day mortality")
ax[0].set_title(f"Calibration (slope={b:.2f}, intercept={a:.2f})")
ax[0].legend(loc="upper left", fontsize=8)
ax[0].set_xlim(0, 1); ax[0].set_ylim(0, 1)

ax[1].plot(thr, nb_model, color="#d62728", lw=2, label="immune-risk score")
ax[1].plot(thr, nb_all, color="#2ca02c", lw=1.5, ls="-", label="treat all")
ax[1].plot(thr, nb_none, color="gray", lw=1, label="treat none")
ax[1].axhline(0, color="gray", lw=0.8)
ax[1].set_xlabel("Threshold probability")
ax[1].set_ylabel("Net benefit")
ax[1].set_title(f"Decision curve (external, AUC={auc:.3f})")
ax[1].legend(loc="upper right", fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "S06_dca.png"), dpi=150)
print("wrote", os.path.join(FIG, "S06_dca.png"))

# also dump numbers for the manuscript
out = {
    "n": len(y), "deaths": int(y.sum()), "prevalence": round(prev, 4),
    "calib_intercept": round(a, 4), "calib_slope": round(b, 4), "auc": round(auc, 4),
    "nb_thr0.20": round(float(np.interp(0.20, thr, nb_model)), 4),
    "nb_thr0.30": round(float(np.interp(0.30, thr, nb_model)), 4),
    "nb_thr0.50": round(float(np.interp(0.50, thr, nb_model)), 4),
}
pd.DataFrame([out]).to_csv(os.path.join(RES, "09_ext_calibration_dca.csv"), index=False)
print("wrote 03_results/09_ext_calibration_dca.csv")
