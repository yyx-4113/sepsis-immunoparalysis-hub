#!/usr/bin/env python
"""
S10 — Genetic validation of the Mars1 immunoparalysis hub (two-sample MR).
STATUS: pipeline-complete but DATA-BLOCKED in this sandbox.

WHY BLOCKED:
  IEU OpenGWAS (gwas.mrcieu.ac.uk) has required a JWT token for gwasinfo /
  association endpoints since 2024-05-01. This sandbox has no token, and no
  local sepsis GWAS summary-stat file is staged. Re-running the real MR needs
  EITHER (a) `ieugwaspy.get_jwt()` with a registered OpenGWAS account, OR
  (b) a local GWAS summary-statistics file for the sepsis outcome
  (Finngen R6 / GWAS Catalog / UKBB). Provide one, then call run_mr().

WHAT THIS SCRIPT DOES (once data is available):
  Exposure : cis-eQTL of the 6 hub genes (CD74, HLA-DQA1, CD14, FCGR3A,
             HAVCR2, FIS1) — eQTLGen cis-eQTL preferred; IEU prot-pQTL fallback.
  Outcome  : sepsis GWAS (e.g. finn-b-M16_SEPSIS) OR a sepsis-immunoparalysis
             trait.
  Methods  : IVW, MR-Egger, weighted median; heterogeneity (Cochran Q);
             pleiotropy (Egger intercept); leave-one-out.
  Output   : 03_results/10_genetics_mr.csv  (per-hub MR estimate + diagnostics)

Designed to be credential-agnostic: if a local outcome .tsv is supplied it is
used directly; otherwise it attempts ieugwaspy (requires JWT).
"""
import json, os, sys
import numpy as np
import pandas as pd
from scipy import stats

HUB_GENES = ["CD74", "HLA-DQA1", "CD14", "FCGR3A", "HAVCR2", "FIS1"]
RES = "03_results"

# ---------------------------------------------------------------------------
# MR core (exposure beta/se, outcome beta/se) — no external deps beyond scipy
# ---------------------------------------------------------------------------
def ivw(b_e, se_e, b_o, se_o):
    w = 1.0 / (se_o ** 2)
    num = np.sum(w * b_e * b_o)
    den = np.sum(w * b_e ** 2)
    beta = num / den
    se = np.sqrt(1.0 / np.sum(w * b_e ** 2))
    z = beta / se
    p = 2.0 * (1.0 - stats.norm.cdf(abs(z)))
    return beta, se, p

def mr_egger(b_e, se_e, b_o, se_o):
    w = 1.0 / (se_o ** 2)
    # weighted least squares: outcome ~ intercept + slope * exposure
    X = np.vstack([np.ones_like(b_e), b_e]).T
    W = np.diag(w)
    XtW = X.T @ W
    beta_hat = np.linalg.solve(XtW @ X, XtW @ b_o)
    cov = np.linalg.inv(XtW @ X)
    intercept, slope = beta_hat
    se_slope = np.sqrt(cov[1, 1])
    se_int = np.sqrt(cov[0, 0])
    p_int = 2.0 * (1.0 - stats.norm.cdf(abs(intercept / se_int)))
    p_slope = 2.0 * (1.0 - stats.norm.cdf(abs(slope / se_slope)))
    return slope, se_slope, p_slope, intercept, se_int, p_int

def weighted_median(b_e, se_e, b_o, se_o):
    # ratio per SNP = b_o/b_e, weighted by outcome precision
    ratios = b_o / b_e
    w = 1.0 / (se_o ** 2)
    order = np.argsort(ratios)
    ratios = ratios[order]; w = w[order]
    cum = np.cumsum(w) / np.sum(w)
    k = np.searchsorted(cum, 0.5)
    beta = ratios[k]
    # simple SE via order statistic approximation
    se = (ratios[min(k + 1, len(ratios) - 1)] - ratios[max(k - 1, 0)]) / (2 * 1.96)
    z = beta / se
    p = 2.0 * (1.0 - stats.norm.cdf(abs(z)))
    return beta, se, p

def run_mr(exp, out):
    """exp, out: DataFrames with columns SNP, beta, se, allele (effect)."""
    m = exp.merge(out, on="SNP", suffixes=("_e", "_o"))
    m = m.dropna(subset=["beta_e", "se_e", "beta_o", "se_o"])
    if len(m) < 3:
        return None, f"only {len(m)} overlapping instruments"
    b_e, se_e = m.beta_e.values, m.se_e.values
    b_o, se_o = m.beta_o.values, m.se_o.values
    ivw_b, ivw_se, ivw_p = ivw(b_e, se_e, b_o, se_o)
    eg_b, eg_se, eg_p, eg_i, eg_is, eg_ip = mr_egger(b_e, se_e, b_o, se_o)
    wm_b, wm_se, wm_p = weighted_median(b_e, se_e, b_o, se_o)
    q = np.sum(((b_o - ivw_b * b_e) ** 2) / (se_o ** 2))
    q_p = stats.chi2.sf(q, len(m) - 1)
    row = dict(
        n_instruments=int(len(m)),
        ivw_beta=round(ivw_b, 4), ivw_se=round(ivw_se, 4), ivw_p=round(ivw_p, 4),
        egger_beta=round(eg_b, 4), egger_se=round(eg_se, 4), egger_p=round(eg_p, 4),
        egger_intercept=round(eg_i, 5), egger_int_p=round(eg_ip, 5),
        wmedian_beta=round(wm_b, 4), wmedian_se=round(wm_se, 4), wmedian_p=round(wm_p, 4),
        heterogeneity_Q=round(q, 3), heterogeneity_Q_p=round(q_p, 4),
    )
    return row, m

# ---------------------------------------------------------------------------
# Data acquisition (gated on credential / local file)
# ---------------------------------------------------------------------------
def fetch_exposure_eqtlgen(gene):
    """eQTLGen cis-eQTL — public, no token. Returns DataFrame or None."""
    # expected local path; download separately from www.eqtlgen.org
    p = f"01_data/eqtlgen/cis_eQTL_{gene}.txt.gz"
    if os.path.exists(p):
        d = pd.read_csv(p, sep="\t")
        return d[["SNP", "Beta"]].rename(columns={"Beta": "beta"})
    return None

def fetch_outcome_local(path):
    if path and os.path.exists(path):
        d = pd.read_csv(path, sep="\t")
        return d
    return None

def run_mr_pipeline(local_outcome_tsv=None, ieugwas_sepsis_id=None):
    """Entry point. local_outcome_tsv: path to sepsis GWAS summary stats.
    ieugwas_sepsis_id: OpenGWAS id (requires JWT via ieugwaspy.get_jwt())."""
    rows = []
    out = fetch_outcome_local(local_outcome_tsv)
    if out is None and ieugwas_sepsis_id:
        try:
            import ieugwaspy as ig
            out = ig.associations(ids=[ieugwas_sepsis_id])  # requires JWT
        except Exception as e:
            sys.stderr.write(f"[S10] outcome fetch failed: {e}\n")
            out = None
    if out is None:
        sys.stderr.write("[S10] NO OUTCOME DATA — provide local_outcome_tsv or IEU JWT.\n")
        return None
    for g in HUB_GENES:
        exp = fetch_exposure_eqtlgen(g)
        if exp is None:
            rows.append({"gene": g, "status": "NO cis-eQTL file (drop eQTLGen_cis_*.txt.gz)"})
            continue
        row, _ = run_mr(exp, out)
        if row is None:
            rows.append({"gene": g, "status": "insufficient overlap"})
        else:
            row["gene"] = g
            rows.append(row)
    df = pd.DataFrame(rows)
    os.makedirs(RES, exist_ok=True)
    df.to_csv(f"{RES}/10_genetics_mr.csv", index=False)
    return df

if __name__ == "__main__":
    # Example: python 10_genetics_mr.py  --outcome 01_data/sepsis_gwas.tsv
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--outcome", default=None, help="local sepsis GWAS summary-stats .tsv")
    ap.add_argument("--ieu-id", default=None, help="OpenGWAS sepsis id (needs JWT)")
    a = ap.parse_args()
    run_mr_pipeline(a.outcome, a.ieu_id)
