import pandas as pd, numpy as np, json, gzip, io
from scipy import stats
from scipy.stats import norm
RNG = np.random.default_rng(20261009)

# ============ T1-1: genome-wide permutation null for binomial concordance ============
deg = pd.read_csv("03_results/S01_mars1_deg.csv")
lfc, adjp = deg['logFC'].values, deg['adj.P.Val'].values
down_mask = (lfc < 0) & (adjp < 0.05) & (np.abs(lfc) >= 0.3)
Ngenes = len(deg); ndown = int(down_mask.sum())
print(f"T1-1: Ngenes={Ngenes}, Mars1-down={ndown}, base={ndown/Ngenes:.4f}")
genes_all = deg['gene'].values

cand = pd.read_csv("03_results/08_candidates_drugs.csv")
results = {}
for _, row in cand.iterrows():
    cg = [g.strip() for g in str(row['rescue_genes']).split(';') if g.strip()]
    r_obs = int(row['n_rescue_mars1down']); n = len(cg)
    cand_pos = np.array([np.where(genes_all == g)[0][0] for g in cg])
    perms = np.zeros(1000)
    for k in range(1000):
        perm_down = RNG.choice(Ngenes, size=ndown, replace=False)
        perm_set = set(perm_down.tolist())
        perms[k] = sum(1 for p in cand_pos if p in perm_set)
    permP = float(np.mean(perms >= r_obs))
    binomP = float(stats.binom.sf(r_obs - 1, n, ndown / Ngenes))
    print(f"  {row['compound'][:22]:22s} n={n} r_obs={r_obs} permP={permP:.3f} dep_binomP={binomP:.3f} dep_allgene={float(row['binom_p_allgene_bg'])}")
    results[row['compound']] = (r_obs, n, permP, binomP, float(row['binom_p_allgene_bg']))
json.dump(results, open("03_results/09b_permutation_null_concordance.json", "w"), indent=1)

# ============ T1-3: calibration slope Wald CI from deposited p ============
cal = pd.read_csv("03_results/09_ext_calibration_dca.csv")
slope = float(cal['calib_slope'].values[0]); p = float(cal['p_slope_eq_1'].values[0])
z = norm.ppf(1 - p / 2); SE = abs(1 - slope) / z
wald_lo = slope - 1.96 * SE; wald_hi = slope + 1.96 * SE
print(f"\nT1-3: slope={slope:.3f} p_slope_eq_1={p:.4f} SE={SE:.3f} WaldCI=({wald_lo:.2f},{wald_hi:.2f})")

# ============ T1-6: label-permutation negative control for external AUC ============
# Reuses the EXACT mapping + scoring of 09_external_validation.py (oriented-sum AUC = 0.638).
EMTAB = "01_data/E-MTAB-4451"

# GPL10558 annotation -> probe->symbol (proven parser)
raw = []
with gzip.open(f"{EMTAB}/GPL10558.annot.gz", "rt") as f:
    for ln in f:
        if ln[:1] in ("!", "#", "^"):
            continue
        raw.append(ln.rstrip("\n"))
ann = pd.read_csv(io.StringIO("\n".join(raw)), sep="\t")
probe2sym = {}
for pid, gs in zip(ann["ID"].astype(str), ann["Gene symbol"].fillna("").astype(str)):
    gs = gs.strip()
    if not gs or gs.lower() == "nan":
        continue
    fs = gs.split("///")[0].strip()
    if fs:
        probe2sym[pid] = fs

eme = pd.read_csv(f"{EMTAB}/Davenport_sepsis_Feb2016_normalised_106.txt", sep='\t', index_col=0)
mat_sym = eme.copy()
mat_sym["symbol"] = [probe2sym.get(p, "") for p in mat_sym.index]
mapped_only = mat_sym[mat_sym["symbol"] != ""]
expr_e = mapped_only.groupby("symbol").mean()   # gene x sample

sdrf = pd.read_csv(f"{EMTAB}/E-MTAB-4451.sdrf.txt", sep='\t')
surv = sdrf[["Source Name", "Characteristics[28 day survival]"]].copy()
surv.columns = ["sample", "survival"]
surv["y"] = (surv["survival"] == "non survivor").astype(int)
keep = [c for c in expr_e.columns if c in set(surv["sample"])]
expr_e = expr_e[keep]
y_e = surv.set_index("sample").loc[keep, "y"].values.astype(float)
print(f"\nT1-6: E-MTAB-4451 validated n={len(keep)}; deaths={int(y_e.sum())} survivors={int((1-y_e).sum())}")

# 30-gene signature + fixed orientation from S06
sg = pd.read_csv("03_results/S06_signature_genes.csv")
genes30 = sg['gene'].tolist()
orient = {g: (1.0 if c >= 0 else -1.0) for g, c in zip(sg['gene'], sg['corr_with_death'])}
mapped = [g for g in genes30 if g in expr_e.index]

# GSE65682 alignment
ex = pd.read_csv("01_data/GSE65682/GSE65682_expr.csv", index_col=0)
pheno = pd.read_csv("01_data/GSE65682/GSE65682_pheno.csv")
sepsis = pheno[pheno["death_28d"].notna()]
sepsis = sepsis[sepsis["sample"].isin(ex.columns)]
y82 = sepsis["death_28d"].astype(int).values
train_genes = [g for g in mapped if g in ex.index]
print(f"  signature genes mapped to E-MTAB: {len(mapped)}/30; trainable on GSE65682: {len(train_genes)}")

# locked standardization params from oriented training data
X82 = ex.loc[train_genes, sepsis["sample"]].T            # samples x genes
for g in train_genes:
    if orient[g] == -1:
        X82[g] = -X82[g]
sc_mean = X82.mean(); sc_std = X82.std()
X82s_base = (X82 - sc_mean) / sc_std                     # standardized, un-oriented

# external standardized, un-oriented (use training params -> locked transport)
Xe_base = expr_e.loc[train_genes, keep].T
Xes_base = (Xe_base - sc_mean) / sc_std

oris = np.array([orient[g] for g in train_genes])
real_score = (oris * Xes_base).sum(1)
# AUC via rank formula
def auc_from_score(y, score):
    y = np.asarray(y, dtype=float)
    npos = y.sum(); nneg = len(y) - npos
    if npos == 0 or nneg == 0:
        return 0.5
    ranks = stats.rankdata(score)
    return (ranks[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg)
real_auc = auc_from_score(y_e, real_score)
print(f"  real external equal-weight (oriented-sum) AUC recomputed = {real_auc:.4f}  (manuscript reports 0.638)")

# Control A: permute DISCOVERY death labels -> recompute orientation, score external
K = 500; aucs = np.zeros(K)
for k in range(K):
    perm = RNG.permutation(y82)
    o_perm = np.array([np.sign(np.corrcoef(X82s_base.iloc[:, i].values, perm)[0, 1]) for i in range(len(train_genes))]).astype(float)
    aucs[k] = auc_from_score(y_e, (o_perm * Xes_base.values).sum(1))
print(f"  [Control A disc-label-perm] AUC mean={aucs.mean():.4f} median={np.median(aucs):.4f} 95%CI=({np.percentile(aucs,2.5):.3f},{np.percentile(aucs,97.5):.3f})")
print(f"  frac AUC > 0.585 = {np.mean(aucs>0.585):.3f}; > 0.638 = {np.mean(aucs>0.638):.3f}")

# Control B: permute EXTERNAL outcome labels, keep real orientation
Kb = 500; aucs_b = np.zeros(Kb)
for k in range(Kb):
    perm_ext = RNG.permutation(y_e)
    aucs_b[k] = auc_from_score(perm_ext, real_score.values)
print(f"  [Control B ext-label-perm]  AUC mean={aucs_b.mean():.4f} 95%CI=({np.percentile(aucs_b,2.5):.3f},{np.percentile(aucs_b,97.5):.3f})")
print(f"  frac ext-perm AUC > 0.638 = {np.mean(aucs_b>0.638):.3f}")

json.dump({"real_auc": real_auc, "perm_mean": float(aucs.mean()), "perm_median": float(np.median(aucs)),
           "perm_lo": float(np.percentile(aucs, 2.5)), "perm_hi": float(np.percentile(aucs, 97.5)),
           "frac_gt_0585": float(np.mean(aucs > 0.585)), "frac_gt_0638": float(np.mean(aucs > 0.638)), "K": K,
           "ext_perm_mean": float(aucs_b.mean()), "ext_perm_lo": float(np.percentile(aucs_b, 2.5)),
           "ext_perm_hi": float(np.percentile(aucs_b, 97.5)), "ext_frac_gt_0638": float(np.mean(aucs_b > 0.638)),
           "ext_K": Kb, "n_validated": int(len(keep)), "n_deaths": int(y_e.sum()),
           "n_train_genes": int(len(train_genes)), "n_mapped": int(len(mapped))},
          open("03_results/09b_label_permutation_control.json", "w"), indent=1)
print("\nSaved: 09b_permutation_null_concordance.json, 09b_label_permutation_control.json")
