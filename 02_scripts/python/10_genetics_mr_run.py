#!/usr/bin/env python
"""
S10 — Two-sample Mendelian randomisation for Mars1 sepsis immunoparalysis hub genes.

Exposure : eQTLGen whole-blood cis-eQTL, IEU OpenGWAS ids `eqtl-a-<ENSG>`
           (HG19/GRCh37, n ~ 31,684)
Outcome  : Sepsis GWAS `ieu-b-4980` (UK Biobank, 11,643 cases / 474,841 controls,
           HG19/GRCh37, 12,243,539 SNPs)
Methods  : IVW (fixed + multiplicative random effects), MR-Egger (+intercept test
           for directional pleiotropy), weighted median (bootstrap SE);
           Cochran Q / I2 heterogeneity; per-SNP F statistic.

Token is read from env OPENGWAS_JWT (or S10_JWT) at runtime -- NEVER hardcoded.
TLS: the OpenGWAS certificate lapsed (notAfter 2026-05-19); verification is
disabled in-process for that host only.

Usage:
  set OPENGWAS_JWT=<token>   (or S10_JWT)
  python 10_genetics_mr_run.py
Outputs:
  03_results/10_genetics_mr.csv      per-gene x per-method estimates
  03_results/10_genetics_mr_harmonised.csv   instrument-level harmonised data
  05_reports/s10_run_log.txt         run log
"""
import os, sys, json, time, urllib.request, ssl
import numpy as np, pandas as pd
from scipy import stats

# Interpreter: run with whichever Python has numpy/pandas/scipy installed
# (e.g. `python 10_genetics_mr_run.py`); no hardcoded interpreter path.

# ---------------------------------------------------------------------------
TOK = os.environ.get("OPENGWAS_JWT") or os.environ.get("S10_JWT")
if not TOK:
    sys.exit("[S10] OPENGWAS_JWT / S10_JWT not set in environment.")

BASE = "https://api.opengwas.io/api"
OUTCOME_ID = os.environ.get("S10_OUTCOME_ID", "ieu-b-4980")
PVAL = os.environ.get("S10_PVAL", "5e-8")
OUT = "03_results"
REP = "05_reports"
for d in (OUT, REP):
    os.makedirs(d, exist_ok=True)

LOG = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)

# ---------------------------------------------------------------------------
# HTTP (OpenGWAS) -- TLS verification disabled: server cert expired 2026-05-19
# ---------------------------------------------------------------------------
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def og(url, data=None, tries=12):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(
                url, data=data,
                headers={"Authorization": f"Bearer {TOK}",
                         "Content-Type": "application/json"},
                method=("POST" if data else "GET"))
            with urllib.request.urlopen(req, timeout=300, context=CTX) as r:
                return r.read().decode()
        except Exception as e:                       # flaky TLS / transient 5xx
            last = e
            time.sleep(3 + 3 * i)
    raise RuntimeError(f"OpenGWAS fetch failed: {url} :: {repr(last)[:200]}")


def og_json(url, data=None):
    t = og(url, data=data)
    try:
        return json.loads(t)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Exposure: clumped cis-eQTL instruments (tophits endpoint)
# ---------------------------------------------------------------------------
def top_hits(eid, pval=PVAL):
    """POST /tophits (the endpoint rejects GET with 'method not allowed')."""
    body = json.dumps({"id": [eid], "pval": float(pval), "clump": 1,
                       "rsq": 0.01, "maf": 0.01}).encode()
    d = og_json(f"{BASE}/tophits", data=body)
    if d is None:
        raise RuntimeError(f"tophits non-JSON for {eid}")
    if isinstance(d, dict):
        raise RuntimeError(f"tophits error {eid}: {str(d)[:200]}")
    return pd.DataFrame(d)


# ---------------------------------------------------------------------------
# Outcome: extract instrument SNPs from the sepsis GWAS
# ---------------------------------------------------------------------------
def outcome_for(rsids, oid=OUTCOME_ID, chunk=400):
    frames = []
    for i in range(0, len(rsids), chunk):
        sub = [r for r in rsids[i:i + chunk] if r]
        body = json.dumps({"variant": sub}).encode()
        d = og_json(f"{BASE}/associations?id={oid}", data=body)
        if isinstance(d, list) and d:
            frames.append(pd.DataFrame(d))
        time.sleep(0.5)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


# ---------------------------------------------------------------------------
# Allele harmonisation
# ---------------------------------------------------------------------------
PAL = {("A", "T"), ("T", "A"), ("G", "C"), ("C", "G")}


def harmonise(exp, out):
    """Align outcome alleles to the exposure effect-allele orientation."""
    o = out.rename(columns={"ea": "ea_o", "nea": "nea_o", "beta": "beta_o",
                            "se": "se_o", "p": "p_o", "eaf": "eaf_o"})
    keep_cols = ["rsid", "ea_o", "nea_o", "beta_o", "se_o", "p_o"]
    for c in keep_cols:
        if c not in o.columns:
            raise KeyError(f"outcome missing column {c}: {list(o.columns)}")
    if "eaf_o" not in o.columns:
        o["eaf_o"] = np.nan
    m = exp.merge(o[keep_cols + ["eaf_o"]], on="rsid", how="inner")
    if m.empty:
        return m
    keep, flip = [], []
    for _, r in m.iterrows():
        ea_e, nea_e = str(r.ea_e).upper(), str(r.nea_e).upper()
        ea_o, nea_o = str(r.ea_o).upper(), str(r.nea_o).upper()
        if (ea_e, nea_e) in PAL or (ea_o, nea_o) in PAL:
            # palindromic: resolve with allele frequency, drop if unavailable
            if not (pd.notna(r.eaf_e) and pd.notna(r.eaf_o)):
                keep.append(False); flip.append(False); continue
            f_e, f_o = float(r.eaf_e), float(r.eaf_o)
            same_strand = abs(f_e - f_o) < 0.15
            flip_strand = abs((1 - f_e) - f_o) < 0.15
            if same_strand == flip_strand:
                keep.append(False); flip.append(False); continue
            keep.append(True); flip.append(flip_strand and not same_strand); continue
        if ea_e == ea_o and nea_e == nea_o:
            keep.append(True); flip.append(False); continue
        if ea_e == nea_o and nea_e == ea_o:
            keep.append(True); flip.append(True); continue
        keep.append(False); flip.append(False)
    m = m.assign(_keep=keep, _flip=flip)
    m = m[m._keep].copy()
    m.loc[m._flip, "beta_o"] = -m.loc[m._flip, "beta_o"]
    m.loc[m._flip, ["ea_o", "nea_o"]] = \
        m.loc[m._flip, ["nea_o", "ea_o"]].values
    return m.drop(columns=["_keep", "_flip"])


# ---------------------------------------------------------------------------
# MR estimators
# ---------------------------------------------------------------------------
def ivw(b_e, b_o, se_o):
    w = 1.0 / se_o ** 2
    beta = np.sum(w * b_e * b_o) / np.sum(w * b_e ** 2)
    se = np.sqrt(1.0 / np.sum(w * b_e ** 2))
    q = np.sum(w * (b_o - beta * b_e) ** 2)
    df = len(b_e) - 1
    q_p = 1 - stats.chi2.cdf(q, df) if df > 0 else np.nan
    i2 = max(0.0, (q - df) / q) if q > 0 else 0.0
    random = q > df and df > 0
    if random:
        se = se * np.sqrt(q / df)
    # IVW p-value on the t-distribution with df = n_snp - 1 (small-n correction;
    # the normal approximation is anti-conservative with 3-8 instruments).
    p = 2 * (1 - stats.t.cdf(abs(beta / se), df)) if df > 0 else np.nan
    return dict(beta=beta, se=se, p=p, Q=q, Q_df=df, Q_p=q_p, I2=i2,
                model=("random" if random else "fixed"))


def egger(b_e, b_o, se_o):
    """Weighted linear regression of b_o on b_e, weights 1/se_o^2."""
    w = 1.0 / se_o ** 2
    x, y = np.asarray(b_e, float), np.asarray(b_o, float)
    sw = w.sum()
    xb = np.sum(w * x) / sw
    yb = np.sum(w * y) / sw
    sxx = np.sum(w * (x - xb) ** 2)
    sxy = np.sum(w * (x - xb) * (y - yb))
    slope = sxy / sxx
    intercept = yb - slope * xb
    resid = y - (intercept + slope * x)
    phi = np.sum(w * resid ** 2) / (len(x) - 2) if len(x) > 2 else np.nan
    se_slope = np.sqrt(phi / sxx)
    se_int = np.sqrt(phi * (1.0 / sw + xb ** 2 / sxx))
    # MR-Egger slope and intercept p-values on the t-distribution with
    # df = n_snp - 2 (small-n correction; the deposited CSVs use this).
    df_eg = len(x) - 2
    p_s = 2 * (1 - stats.t.cdf(abs(slope / se_slope), df_eg))
    p_i = 2 * (1 - stats.t.cdf(abs(intercept / se_int), df_eg))
    return dict(beta=slope, se=se_slope, p=p_s,
                intercept=intercept, intercept_se=se_int, intercept_p=p_i)


def wmedian(ratios, weights, boot=2000, seed=20260925):
    order = np.argsort(ratios)
    r, w = np.asarray(ratios)[order], np.asarray(weights)[order]
    cw = np.cumsum(w) - 0.5 * w
    tot = w.sum()
    med = np.interp(0.5 * tot, cw, r)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(r), size=(boot, len(r)))
    bs = []
    for k in range(boot):
        rr, ww = r[idx[k]], w[idx[k]]
        o = np.argsort(rr)
        rr, ww = rr[o], ww[o]
        c = np.cumsum(ww) - 0.5 * ww
        bs.append(np.interp(0.5 * ww.sum(), c, rr))
    se = np.std(bs, ddof=1)
    # Weighted-median p-value on the t-distribution with df = n_snp - 1.
    p = 2 * (1 - stats.t.cdf(abs(med / se), len(r) - 1)) if se > 0 else np.nan
    return dict(beta=med, se=se, p=p)


# ---------------------------------------------------------------------------
HUB = {
    "CD74":     "ENSG00000019582",
    "HLA-DQA1": "ENSG00000196735",
    "CD14":     "ENSG00000170458",
    "FCGR3A":   "ENSG00000203747",
    "HAVCR2":   "ENSG00000135077",
    "FIS1":     "ENSG00000214253",
}

rows, harm_all = [], []

log("=" * 78)
log("S10 two-sample MR -- sepsis immunoparalysis hub genes")
log("exposure = eQTLGen whole-blood cis-eQTL (eqtl-a-<ENSG>, HG19)")
log(f"outcome  = {OUTCOME_ID} (sepsis, UK Biobank)")
log(f"instrument p-value threshold = {PVAL}, LD clumping r2<0.01")
log("=" * 78)

for gene, ensg in HUB.items():
    time.sleep(1.0)
    eid = f"eqtl-a-{ensg}"
    log(f"\n[{gene}] exposure {eid}")
    try:
        exp = top_hits(eid)
    except Exception as e:
        log(f"  EXPOSURE FAIL: {repr(e)[:160]}")
        rows.append(dict(gene=gene, ensg=ensg, method="IVW", nsnp=0,
                         status="exposure_unavailable"))
        continue
    if exp.empty:
        log("  no instruments at threshold")
        rows.append(dict(gene=gene, ensg=ensg, method="IVW", nsnp=0,
                         status="no_instruments"))
        continue

    cols = {c.lower(): c for c in exp.columns}
    ren = {}
    for want, opts in [("rsid", ["rsid", "rs_id", "snp"]),
                       ("ea_e", ["ea", "effect_allele", "alt"]),
                       ("nea_e", ["nea", "other_allele", "ref"]),
                       ("beta_e", ["beta", "effect_size"]),
                       ("se_e", ["se", "standard_error"]),
                       ("p_e", ["p", "pval", "p_value"]),
                       ("eaf_e", ["eaf", "freq", "maf"])]:
        for o in opts:
            if o in cols:
                ren[cols[o]] = want
                break
    exp = exp.rename(columns=ren)
    need = ["rsid", "ea_e", "nea_e", "beta_e", "se_e", "p_e"]
    if any(c not in exp.columns for c in need):
        log(f"  exposure columns missing: {list(exp.columns)}")
        continue
    if "eaf_e" not in exp.columns:
        exp["eaf_e"] = np.nan
    exp = exp[need + ["eaf_e"]].dropna(subset=need)
    exp = exp[exp.p_e.astype(float) < float(PVAL)]
    n_raw = len(exp)
    log(f"  clumped instruments: {n_raw}")

    try:
        out = outcome_for(exp.rsid.tolist())
    except Exception as e:
        log(f"  OUTCOME FAIL: {repr(e)[:160]}")
        continue
    if out.empty:
        log("  outcome returned no rows for these SNPs")
        continue
    log(f"  outcome rows matched: {len(out)}")

    h = harmonise(exp, out)
    log(f"  after harmonisation: {len(h)}")
    if len(h) < 3:
        log("  too few instruments (<3) -- MR not attempted")
        rows.append(dict(gene=gene, ensg=ensg, method="IVW", nsnp=len(h),
                         status="insufficient_instruments"))
        continue

    h = h.copy()
    h["gene"] = gene
    h["F"] = (h.beta_e.astype(float) / h.se_e.astype(float)) ** 2
    harm_all.append(h)

    b_e = h.beta_e.astype(float).values
    b_o = h.beta_o.astype(float).values
    se_o = h.se_o.astype(float).values
    n = len(h)
    log(f"  median F = {np.median(h.F):.1f}; weak-instrument risk:"
        f" {'YES' if np.median(h.F) < 10 else 'no'}")

    # IVW (primary)
    r = ivw(b_e, b_o, se_o)
    or_, lo, hi = (np.exp(r["beta"]),
                   np.exp(r["beta"] - 1.96 * r["se"]),
                   np.exp(r["beta"] + 1.96 * r["se"]))
    rows.append(dict(gene=gene, ensg=ensg, method="IVW", nsnp=n,
                     beta=r["beta"], se=r["se"], or_=or_, ci_lo=lo, ci_hi=hi,
                     p=r["p"], model=r["model"], Q=r["Q"], Q_df=r["Q_df"],
                     Q_p=r["Q_p"], I2=r["I2"],
                     egger_intercept=np.nan, egger_intercept_p=np.nan,
                     status="ok"))
    log(f"  IVW      beta={r['beta']:+.4f} se={r['se']:.4f} "
        f"OR={or_:.3f} [{lo:.3f}-{hi:.3f}] p={r['p']:.3g} ({r['model']}), "
        f"Q={r['Q']:.1f} p_het={r['Q_p']:.3g} I2={r['I2']:.2f}")

    # MR-Egger
    e = egger(b_e, b_o, se_o)
    or_e = np.exp(e["beta"])
    rows.append(dict(gene=gene, ensg=ensg, method="MR-Egger", nsnp=n,
                     beta=e["beta"], se=e["se"], or_=or_e,
                     ci_lo=np.exp(e["beta"] - 1.96 * e["se"]),
                     ci_hi=np.exp(e["beta"] + 1.96 * e["se"]),
                     p=e["p"], model="egger", Q=np.nan, Q_df=n - 2, Q_p=np.nan,
                     I2=np.nan, egger_intercept=e["intercept"],
                     egger_intercept_p=e["intercept_p"], status="ok"))
    log(f"  MR-Egger beta={e['beta']:+.4f} se={e['se']:.4f} "
        f"OR={or_e:.3f} p={e['p']:.3g}; intercept={e['intercept']:+.4f} "
        f"p_pleio={e['intercept_p']:.3g}")

    # Weighted median
    wm = wmedian(b_o / b_e, 1.0 / (se_o / np.abs(b_e)) ** 2)
    rows.append(dict(gene=gene, ensg=ensg, method="Weighted median", nsnp=n,
                     beta=wm["beta"], se=wm["se"], or_=np.exp(wm["beta"]),
                     ci_lo=np.exp(wm["beta"] - 1.96 * wm["se"]),
                     ci_hi=np.exp(wm["beta"] + 1.96 * wm["se"]),
                     p=wm["p"], model="wmedian", Q=np.nan, Q_df=np.nan,
                     Q_p=np.nan, I2=np.nan,
                     egger_intercept=np.nan, egger_intercept_p=np.nan,
                     status="ok"))
    log(f"  WMed     beta={wm['beta']:+.4f} se={wm['se']:.4f} "
        f"OR={np.exp(wm['beta']):.3f} p={wm['p']:.3g}")

# ---------------------------------------------------------------------------
res = pd.DataFrame(rows)
if not res.empty:
    ok = res[res.status == "ok"]
    if len(ok):
        pv = ok.p.values
        order = np.argsort(pv)
        m = len(pv)
        q = np.empty(m)
        prev = 1.0
        for i in range(m - 1, -1, -1):
            prev = min(prev, pv[order[i]] * m / (i + 1))
            q[order[i]] = prev
        res.loc[ok.index, "p_fdr_bh"] = q
res.to_csv(f"{OUT}/10_genetics_mr.csv", index=False)
if harm_all:
    pd.concat(harm_all, ignore_index=True).to_csv(
        f"{OUT}/10_genetics_mr_harmonised.csv", index=False)

log("\n" + "=" * 78)
log("Wrote 03_results/10_genetics_mr.csv")
if harm_all:
    log("Wrote 03_results/10_genetics_mr_harmonised.csv")
log("=" * 78)

with open(f"{REP}/s10_run_log.txt", "w", encoding="utf-8") as fh:
    fh.write("\n".join(LOG) + "\n")
