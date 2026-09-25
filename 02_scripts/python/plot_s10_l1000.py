"""Fig S10: LINCS L1000 rescue of the Mars1-down axis — top 25 small molecules + candidate markers."""
import pandas as pd, numpy as np, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(ROOT, "03_results"); FIG = os.path.join(ROOT, "04_figures")
os.makedirs(FIG, exist_ok=True)
df = pd.read_csv(os.path.join(RES, "S08_l1000_rescue_trtcp.csv"))

top = df.head(25).iloc[::-1]
cand_ids = ["BRD-A17883755", "BRD-K74501079"]   # lenalidomide, azithromycin
fig, ax = plt.subplots(figsize=(7.2, 8.2))
colors = ["#2c7fb8" if pid not in cand_ids else "#d95f02" for pid in top["pert_id"]]
ax.barh(range(len(top)), top["rescue_score"], color=colors)
ax.set_yticks(range(len(top)))
ax.set_yticklabels(top["pert_iname"], fontsize=7)
ax.set_xlabel("L1000 rescue score (Mars1-down axis up-regulation)\n= mean rank-percentile of 22 genes − 0.5")
ax.set_title("Top 25 LINCS L1000 rescuers of the Mars1-down\nimmunoparalysis axis (n=20,413 trt_cp; orange = S08 candidates)")
ax.axvline(0, color="k", lw=0.6)
for i, (pid, sc) in enumerate(zip(top["pert_id"], top["rescue_score"])):
    if pid in cand_ids:
        ax.text(sc + 0.003, i, f" {sc:.3f}", va="center", fontsize=7, color="#d95f02")
ax.text(0.98, 0.04, "background mean = 0.006", transform=ax.transAxes,
        ha="right", fontsize=7, style="italic", color="#555")
plt.tight_layout()
plt.savefig(os.path.join(FIG, "fig_s10_l1000_rescue.png"), dpi=150)
print("saved", os.path.join(FIG, "fig_s10_l1000_rescue.png"))
