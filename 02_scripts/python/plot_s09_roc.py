"""S09 ROC figure: external validation of the 30-gene signature on E-MTAB-4451."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/05_多组学+虚拟敲除药物发现/方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位"
RES = f"{ROOT}/03_results"
FIG = f"{ROOT}/04_figures"

df = pd.read_csv(f"{RES}/09_ext_risk_scores.csv")
y = df["y"].values

def roc(risk, label, color, ls="-"):
    fpr, tpr, _ = roc_curve(y, risk)
    auc = roc_auc_score(y, risk)
    plt.plot(fpr, tpr, color=color, ls=ls, lw=2,
             label=f"{label} (AUC={auc:.3f})")
    return auc

plt.figure(figsize=(6.2, 5.6))
plt.plot([0, 1], [0, 1], "--", color="#888888", lw=1, label="Chance (0.500)")
roc(df["risk_oriented_sum"], "30-gene immune-risk (oriented sum)", "#1f77b4")
roc(df["risk_locked_l1"], "30-gene (locked L1 weights)", "#ff7f0e")
if "risk_irg3" in df.columns:
    roc(df["risk_irg3"], "IRG-3 benchmark (Peng 2023)", "#2ca02c", ls=":")
plt.xlim(0, 1); plt.ylim(0, 1)
plt.xlabel("1 − Specificity (False Positive Rate)")
plt.ylabel("Sensitivity (True Positive Rate)")
plt.title("External validation on E-MTAB-4451 (n=106, 52 deaths)\nIllumina HumanHT-12 V4 · independent of discovery cohort")
plt.legend(loc="lower right", fontsize=9, framealpha=0.95)
plt.tight_layout()
plt.savefig(f"{FIG}/fig_s09_external_roc.png", dpi=160)
print("saved", f"{FIG}/fig_s09_external_roc.png")
