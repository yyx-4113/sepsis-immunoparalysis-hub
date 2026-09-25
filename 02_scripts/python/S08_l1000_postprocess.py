"""
S08b post-processing: candidate cross + sanity checks (NO gctx re-scan).
Reads the checkpointed rescue/wtcs arrays produced by S08_l100100_connectivity.py
and annotates the 7 mechanism-anchored candidates that are LINCS small molecules,
plus runs method-positive-control checks against known immunostimulatory drugs.
"""
import numpy as np, pandas as pd, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LINCS = os.path.join(ROOT, "01_data", "LINCS")
RES = os.path.join(ROOT, "03_results")

df = pd.read_csv(os.path.join(RES, "S08_l1000_rescue_trtcp.csv"))
n = len(df)
print("loaded rescue table:", n, "small-molecule perturbagens")

# percentile rank of rescue_score (higher = more rescue); 1.0 = best
df = df.sort_values("rescue_score", ascending=False).reset_index(drop=True)
df["rescue_pct_rank"] = (np.arange(1, n + 1) / n)   # top=1.0
# also express as rank position
df["rescue_rank"] = np.arange(1, n + 1)

pi = pd.read_csv(os.path.join(LINCS, "pert_info.txt.gz"), sep="\t", compression="gzip", low_memory=False)
id2iname = dict(zip(pi["pert_id"].astype(str), pi["pert_iname"]))

# ---- 1) the two small-molecule candidates from S08 ----
cand_sm = {"azithromycin": ["BRD-K74501079"],
           "lenalidomide": ["BRD-A17883755", "BRD-K05926469"]}
print("\n=== S08 small-molecule candidates in L1000 (reverse-connectivity) ===")
rows = []
for name, pids in cand_sm.items():
    sub = df[df["pert_id"].isin(pids)]
    if len(sub):
        best = sub.iloc[0]
        rows.append({"candidate": name, "pert_id": best["pert_id"],
                     "rescue_score": round(best["rescue_score"], 4),
                     "wtcs": round(best["wtcs"], 4),
                     "rescue_rank": int(best["rescue_rank"]),
                     "rescue_pct_rank": round(best["rescue_pct_rank"], 5)})
cand_l1000 = pd.DataFrame(rows)
print(cand_l1000.to_string())
cand_l1000.to_csv(os.path.join(RES, "S08_l1000_candidate_scores.csv"), index=False)

# ---- 2) method positive-control: known immunostimulatory small molecules ----
# (HLA-II / antigen-presentation / Th1 inducers well established in literature)
known = {
    "vorinostat (HDACi, upregulates HLA-II)": ["vorinostat"],
    "romidepsin (HDACi)": ["romidepsin"],
    "entinostat (HDACi)": ["entinostat"],
    "lenalidomide (IMiD)": ["lenalidomide"],
    "azithromycin (macrolide immunomod)": ["azithromycin"],
    " interferon-gamma (biologic, not trt_cp)": ["interferon gamma", "ifn-gamma"],
    "dexamethasone (anti-inflammatory control, expect LOW rescue)": ["dexamethasone"],
    "prednisolone (glucocorticoid control)": ["prednisolone", "prednisone"],
}
print("\n=== Method positive-control: known immunomodulators ===")
pc = []
for label, keys in known.items():
    sub = df[df["pert_iname"].astype(str).str.lower().isin([k.lower() for k in keys])]
    if len(sub):
        b = sub.iloc[0]
        pc.append({"drug": label, "pert_iname": b["pert_iname"],
                   "rescue_score": round(b["rescue_score"], 4),
                   "rescue_pct_rank": round(b["rescue_pct_rank"], 5),
                   "rescue_rank": int(b["rescue_rank"])})
    else:
        pc.append({"drug": label, "pert_iname": "N/A (absent from trt_cp)",
                   "rescue_score": np.nan, "rescue_pct_rank": np.nan, "rescue_rank": np.nan})
pc = pd.DataFrame(pc).sort_values("rescue_score", ascending=False)
print(pc.to_string())
pc.to_csv(os.path.join(RES, "S08_l1000_positive_control.csv"), index=False)

# ---- 3) immunostimulatory-keyword rescue hits (discovery) ----
kws = ["interferon", "ifn", "il-7", "il7", "gm-csf", "granulocyte", "bcg", "lenalidomide",
       "azithromycin", "thymosin", "tlr", "il2", "il15", "cd40", "stat", "jak",
       "vorinostat", "romidepsin", "entinostat", "hdac", "imidazole", "asco", "len", "myc"]
hit = df[df["pert_iname"].astype(str).str.lower().str.contains("|".join(kws), na=False)].head(40)
print("\n=== Immunostimulatory-keyword rescue hits (top 40) ===")
print(hit[["pert_id", "pert_iname", "rescue_score", "wtcs", "rescue_rank"]].to_string())
hit.to_csv(os.path.join(RES, "S08_l1000_immuno_overlap.csv"), index=False)

# ---- 4) summary stats for manuscript ----
print("\n=== Summary ===")
print("mean rescue_score:", round(df["rescue_score"].mean(), 4),
      "| median:", round(df["rescue_score"].median(), 4))
print("fraction with rescue_score>0 (axis-shifted-up):", round((df["rescue_score"] > 0).mean(), 4))
print("DONE -> candidate_scores / positive_control / immuno_overlap CSVs")
