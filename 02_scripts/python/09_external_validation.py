"""
S09 — External, independent validation of the 30-gene immune-risk signature
on E-MTAB-4451 (Illumina HumanHT-12 V4; 106 severe-sepsis patients, 28-day survival).

Locked pipeline (no re-tuning on test set):
  1. Train L1-logistic signature model on GSE65682 sepsis samples, orienting each
     gene by its training-set sign of correlation with 28-day death (fixed orientation).
  2. Apply the LOCKED coefficients + training StandardScaler to E-MTAB-4451.
  3. Report external-validation AUC with bootstrap 95% CI.

All numbers are traced to real downloaded files. No fabrication.
"""
import io, gzip, json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/05_多组学+虚拟敲除药物发现/方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位"
EMTAB = f"{ROOT}/01_data/E-MTAB-4451"
RES = f"{ROOT}/03_results"

# ----------------------------------------------------------------------
# 1. GPL10558 (Illumina HT-12 V4) probe -> gene symbol
# ----------------------------------------------------------------------
print("[1] parsing GPL10558 annotation ...")
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
print(f"    probes with symbol: {len(probe2sym)}")

# ----------------------------------------------------------------------
# 2. E-MTAB-4451 matrix (probes x samples) -> gene x sample
# ----------------------------------------------------------------------
print("[2] loading E-MTAB-4451 matrix ...")
mat = pd.read_csv(f"{EMTAB}/Davenport_sepsis_Feb2016_normalised_106.txt", sep="\t", index_col=0)
mat_sym = mat.copy()
mat_sym["symbol"] = [probe2sym.get(p, "") for p in mat_sym.index]
mapped_only = mat_sym[mat_sym["symbol"] != ""]
expr_e = mapped_only.groupby("symbol").mean()          # gene x sample (mean over probes)
print(f"    matrix {mat.shape[0]} probes -> {expr_e.shape[0]} genes; samples={expr_e.shape[1]}")

# ----------------------------------------------------------------------
# 3. E-MTAB-4451 survival outcome (SDRF)
# ----------------------------------------------------------------------
sdrf = pd.read_csv(f"{EMTAB}/E-MTAB-4451.sdrf.txt", sep="\t")
surv = sdrf[["Source Name", "Characteristics[28 day survival]"]].copy()
surv.columns = ["sample", "survival"]
surv["y"] = (surv["survival"] == "non survivor").astype(int)
keep = [c for c in expr_e.columns if c in set(surv["sample"])]
expr_e = expr_e[keep]
y_e = surv.set_index("sample").loc[keep, "y"].values
print(f"    E-MTAB-4451 validated samples n={len(keep)}; deaths={int(y_e.sum())} survivors={int((1-y_e).sum())}")

# ----------------------------------------------------------------------
# 4. 30-gene signature + fixed orientation from S06
# ----------------------------------------------------------------------
sig = pd.read_csv(f"{RES}/S06_signature_genes.csv")
genes30 = sig["gene"].tolist()
orient = {g: (1 if c >= 0 else -1) for g, c in zip(sig["gene"], sig["corr_with_death"])}

# genes present on BOTH platforms
mapped = [g for g in genes30 if g in expr_e.index]

# ----------------------------------------------------------------------
# 5. Lock model on GSE65682 using the intersection genes
# ----------------------------------------------------------------------
print("[5] locking signature model on GSE65682 ...")
e82 = pd.read_csv(f"{ROOT}/01_data/GSE65682/GSE65682_expr.csv", index_col=0)
pheno = pd.read_csv(f"{ROOT}/01_data/GSE65682/GSE65682_pheno.csv")
sepsis = pheno[pheno["death_28d"].notna()]
sepsis = sepsis[sepsis["sample"].isin(e82.columns)]
y82 = sepsis["death_28d"].astype(int).values

train_genes = [g for g in mapped if g in e82.index]
print(f"    signature genes mapped to E-MTAB-4451: {len(mapped)}/30; trainable on GSE65682: {len(train_genes)}")
X82 = e82.loc[train_genes, sepsis["sample"]].T
for g in train_genes:
    if orient[g] == -1:
        X82[g] = -X82[g]
sc = StandardScaler().fit(X82.values)
X82s = sc.transform(X82.values)
lr = LogisticRegression(penalty="l1", C=0.5, max_iter=5000, solver="liblinear")
lr.fit(X82s, y82)
coef = dict(zip(train_genes, lr.coef_[0]))
intercept = float(lr.intercept_[0])

# training CV AUC (locked model, 5-fold) for comparison
from sklearn.model_selection import StratifiedKFold
skf = StratifiedKFold(5, shuffle=True, random_state=42)
cv = []
for tr, te in skf.split(X82s, y82):
    m = LogisticRegression(penalty="l1", C=0.5, max_iter=5000, solver="liblinear")
    m.fit(X82s[tr], y82[tr])
    cv.append(roc_auc_score(y82[te], m.decision_function(X82s[te])))
auc_cv82 = float(np.mean(cv))

# ----------------------------------------------------------------------
# 6. Apply LOCKED model to E-MTAB-4451
# ----------------------------------------------------------------------
print("[6] applying locked model to E-MTAB-4451 ...")
Xe = expr_e.loc[train_genes, keep].T
for g in train_genes:
    if orient[g] == -1:
        Xe[g] = -Xe[g]
Xes = sc.transform(Xe.values)
coef_arr = np.array([coef[g] for g in train_genes])
risk = Xes @ coef_arr + intercept
auc_ext = float(roc_auc_score(y_e, risk))

# bootstrap 95% CI
rng = np.random.default_rng(42)
bs = []
for _ in range(2000):
    idx = rng.integers(0, len(y_e), len(y_e))
    if len(set(y_e[idx])) < 2:
        continue
    bs.append(roc_auc_score(y_e[idx], risk[idx]))
ci_lo, ci_hi = float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))

# model-free oriented-sum AUC (equal weight)
risk_sum = Xes.sum(axis=1)
auc_sum = float(roc_auc_score(y_e, risk_sum))
bs_sum = []
for _ in range(2000):
    idx = rng.integers(0, len(y_e), len(y_e))
    if len(set(y_e[idx])) < 2:
        continue
    bs_sum.append(roc_auc_score(y_e[idx], risk_sum[idx]))
ci_sum_lo, ci_sum_hi = float(np.percentile(bs_sum, 2.5)), float(np.percentile(bs_sum, 97.5))
missing_genes = [g for g in genes30 if g not in expr_e.index]

# ----------------------------------------------------------------------
# 7. Benchmark IRG (Peng 2023) 3-gene on E-MTAB-4451 for context
# ----------------------------------------------------------------------
irg = ["LTB4R", "HLA-DMB", "IL4R"]
irg_present = [g for g in irg if g in expr_e.index]
if len(irg_present) == 3:
    Xi = expr_e.loc[irg_present, keep].T
    # orient by GSE65682 sign if available else keep
    for g in irg_present:
        if g in orient and orient[g] == -1:
            Xi[g] = -Xi[g]
    Xi = StandardScaler().fit_transform(Xi.values)
    auc_irg = float(roc_auc_score(y_e, Xi.sum(axis=1)))
else:
    auc_irg = None

# ----------------------------------------------------------------------
# 8. Save
# ----------------------------------------------------------------------
out = pd.DataFrame({
    "metric": [
        "n_signature_genes_total", "n_signature_genes_mapped_EMTAB4451",
        "n_validated_samples", "n_deaths", "n_survivors",
        "auc_GSE65682_CV_locked", "auc_EMTAB4451_external_locked",
        "auc_EMTAB4451_external_CI95_low", "auc_EMTAB4451_external_CI95_high",
        "auc_EMTAB4451_orientedSum", "auc_EMTAB4451_orientedSum_CI95_low",
        "auc_EMTAB4451_orientedSum_CI95_high", "auc_IRG3_benchmark_EMTAB4451",
        "platform_train", "platform_test", "genes_missing_in_test",
    ],
    "value": [
        30, len(mapped), len(keep), int(y_e.sum()), int((1 - y_e).sum()),
        round(auc_cv82, 4), round(auc_ext, 4),
        round(ci_lo, 4), round(ci_hi, 4),
        round(auc_sum, 4), round(ci_sum_lo, 4), round(ci_sum_hi, 4),
        (round(auc_irg, 4) if auc_irg is not None else "NA"),
        "GPL13667 (Affymetrix Human Gene 1.0 ST)",
        "GPL10558 (Illumina HumanHT-12 V4)",
        ",".join(missing_genes) if missing_genes else "none",
    ],
})
out.to_csv(f"{RES}/09_external_validation.csv", index=False)
with open(f"{RES}/09_external_validation_coef.json", "w") as f:
    json.dump({"intercept": intercept, "coef": coef, "genes": train_genes,
               "orientation": {g: orient[g] for g in train_genes}}, f, indent=2)

# per-sample risk scores for plotting
risk_df = pd.DataFrame({
    "sample": keep,
    "y": y_e,
    "risk_oriented_sum": risk_sum,
    "risk_locked_l1": risk,
})
if auc_irg is not None:
    risk_df["risk_irg3"] = Xi.sum(axis=1)
risk_df.to_csv(f"{RES}/09_ext_risk_scores.csv", index=False)

print("\n================ RESULT ================")
print(out.to_string(index=False))
print(f"External-validation AUC = {auc_ext:.3f} (95% CI {ci_lo:.3f}-{ci_hi:.3f})")
print(f"  vs GSE65682 locked CV AUC = {auc_cv82:.3f}")
print(f"  oriented-sum AUC = {auc_sum:.3f} (95% CI {ci_sum_lo:.3f}-{ci_sum_hi:.3f}); IRG-3 benchmark = {auc_irg}")
print(f"  genes missing in test cohort: {missing_genes if missing_genes else 'none'}")
print("========================================")
