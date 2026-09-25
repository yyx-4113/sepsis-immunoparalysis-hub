"""
S08b/L1000 reverse-connectivity (rescue of Mars1-down immunoparalysis axis)
----------------------------------------------------------------------------
Local, reproducible implementation. No iLINCS web API needed (sandbox blocked),
uses GSE92742 Level 5 (Broad LINCS Phase-II, MODZ consensus) gctx directly.

Disease query signature = Mars1-down genes of the MARS immunosuppressed
endotype (antigen-presentation / monocytic axis suppressed in immunoparalysis).
A perturbagen "rescues" immunoparalysis if it UP-regulates these genes.

GSE92742 Level5 gctx layout (file-verified):
  matrix = (n_samples=473647, n_genes=12328)   # rows=samples, cols=genes
  /0/META/ROW/id = 12328 gene identifiers (Entrez pr_gene_id)
  /0/META/COL/id = 473647 sample/sig identifiers (sig_id)

For every small-molecule perturbagen (trt_cp, n=20,413) we compute a single-set
reverse-connectivity (rescue) score = mean rank-percentile of the Mars1-down
genes across that perturbagen's expression profile - 0.5. Positive => the
Mars1-down axis is shifted toward expression (rescue). Honestly labelled as an
iLINCS-style wtcs proxy (not the full up/down dual-KS tau).
"""
import h5py, numpy as np, pandas as pd, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LINCS = os.path.join(ROOT, "01_data", "LINCS")
RES = os.path.join(ROOT, "03_results")
GCTX = os.path.join(LINCS, "GSE92742_Level5_COMPZ.gctx")

print("loading Mars1-down gene list (L1000 membership) ...")
_meta = json.load(open(os.path.join(LINCS, "mars1_down_l1000_idx.json")))
down_sym = set(g.upper() for g in _meta["mars1_down_genes"])
print("Mars1-down genes available in L1000:", len(down_sym), "of", len(_meta["mars1_down_genes"]))

print("reading sig_info / pert_info ...")
si = pd.read_csv(os.path.join(LINCS, "sig_info.txt.gz"), sep="\t", compression="gzip", low_memory=False)
pi = pd.read_csv(os.path.join(LINCS, "pert_info.txt.gz"), sep="\t", compression="gzip", low_memory=False)
sig2pert = dict(zip(si["sig_id"].astype(str), si["pert_id"].astype(str)))
trtcp = set(pi.loc[pi["pert_type"].astype(str).str.contains("trt_cp", na=False), "pert_id"].astype(str))
all_trtcp = list(trtcp)
pert2idx = {p: i for i, p in enumerate(all_trtcp)}
n_pert = len(all_trtcp)
print("trt_cp (small-molecule) perturbagens:", n_pert)

print("opening gctx:", GCTX)
f = h5py.File(GCTX, "r")
mat = f["0/DATA/0/matrix"]
ns, ng = mat.shape                       # (samples, genes)
print("matrix shape (samples x genes):", ns, ng)
sample_ids = [x.decode() if isinstance(x, bytes) else str(x) for x in f["0/META/COL/id"][:]]   # 473647
gene_ids = [x.decode() if isinstance(x, bytes) else str(x) for x in f["0/META/ROW/id"][:]]     # 12328 (Entrez)
print("n samples (COL/id):", len(sample_ids), "| n genes (ROW/id):", len(gene_ids))

# map Entrez gene id -> symbol via gene_info, then resolve Mars1-down columns
gi = pd.read_csv(os.path.join(LINCS, "gene_info.txt.gz"), sep="\t", compression="gzip")
entrez2sym = dict(zip(gi["pr_gene_id"].astype(str), gi["pr_gene_symbol"].astype(str).str.upper()))
gene_sym = [entrez2sym.get(str(g), "") for g in gene_ids]
gene_sym_map = {s.upper(): i for i, s in enumerate(gene_sym) if s}
down_idx = np.array(sorted({gene_sym_map[g] for g in down_sym if g in gene_sym_map}), dtype=int)
print("resolved Mars1-down gene COLUMN indices in gctx:", len(down_idx), "/", len(down_sym))
assert len(down_idx) >= 10, "too few Mars1-down genes resolved in gctx"

# map each SAMPLE -> global pert idx (None if not trt_cp)
col2pert = np.full(ns, -1, dtype=np.int64)
for i, sid in enumerate(sample_ids):
    pp = sig2pert.get(sid)
    if pp is not None and pp in pert2idx:
        col2pert[i] = pert2idx[pp]

# Memory-safe streaming over samples; accumulate ONLY the 22 down-gene
# rank-percentile values into a (22 x n_pert) buffer.
acc = np.zeros((len(down_idx), n_pert), dtype=np.float32)
cnt = np.zeros(n_pert, dtype=np.int32)
CH = 2000
n_valid = 0
for c0 in range(0, ns, CH):
    c1 = min(c0 + CH, ns)
    chunk = mat[c0:c1, :].astype(np.float32)                       # (CH, G)
    ranks = np.argsort(np.argsort(chunk, axis=1), axis=1).astype(np.float32)  # (CH, G)
    pct = (ranks + 1.0) / ng                                       # percentile 0..1
    idx_local = col2pert[c0:c1]
    mask = idx_local >= 0
    if mask.any():
        sub = pct[np.ix_(mask, down_idx)]          # (n_valid, 22)
        acc[:, idx_local[mask]] += sub.T
        cnt[idx_local[mask]] += 1
        n_valid += int(mask.sum())
    if (c0 // CH) % 50 == 0:
        print(f"  ..processed samples {c1}/{ns}, valid sigs so far {n_valid}")
print("valid small-molecule sig columns accumulated:", n_valid)

mean_pct = acc / np.clip(cnt, 1, None)[None, :]     # (22, n_pert) mean percentile
rescue = mean_pct.mean(axis=0) - 0.5
wtcs = (mean_pct.sum(axis=0) - len(down_idx) * 0.5) / np.sqrt(len(down_idx))

# checkpoint the expensive per-pert scores immediately (durable across reruns)
np.save(os.path.join(RES, "S08_l1000_rescue_wtcs.npy"),
        np.vstack([rescue, wtcs]).T)   # (n_pert, 2)

out = pd.DataFrame({
    "pert_id": all_trtcp,
    "rescue_score": rescue,
    "wtcs": wtcs,
})
# annotate with columns that actually exist in pert_info
piname = dict(zip(pi["pert_id"].astype(str), pi["pert_iname"]))
if "canonical_smiles" in pi.columns:
    out["canonical_smiles"] = out["pert_id"].map(dict(zip(pi["pert_id"].astype(str), pi["canonical_smiles"])))
if "pubchem_cid" in pi.columns:
    out["pubchem_cid"] = out["pert_id"].map(dict(zip(pi["pert_id"].astype(str), pi["pubchem_cid"])))
out["pert_iname"] = out["pert_id"].map(piname)
out = out.sort_values("rescue_score", ascending=False).reset_index(drop=True)
out.to_csv(os.path.join(RES, "S08_l1000_rescue_trtcp.csv"), index=False)
print("\n=== TOP 25 rescue (reverse-connectivity) small molecules ===")
print(out.head(25).to_string())

# cross with S08 mechanism-anchored candidates (target/mechanism keyword match)
cand = pd.read_csv(os.path.join(RES, "08_candidates_drugs.csv"))
print("\n=== S08 mechanism-anchored candidates ===")
print(cand.to_string())
kws = ["interferon", "ifn", "il-7", "il7", "gm-csf", "granulocyte", "bcg", "lenalidomide",
       "azithromycin", "thymosin", "tlr", "il2", "il15", "cd40", "stat", "jak"]
hit = out[out["pert_iname"].astype(str).str.lower().str.contains("|".join(kws), na=False) |
          out["pert_target"].astype(str).str.lower().str.contains("|".join(kws), na=False)].head(30)
print("\n=== L1000 rescue hits overlapping immunostimulatory keywords ===")
print(hit.to_string())
hit.to_csv(os.path.join(RES, "S08_l1000_immuno_overlap.csv"), index=False)
print("\nDONE -> 03_results/S08_l1000_rescue_trtcp.csv")
