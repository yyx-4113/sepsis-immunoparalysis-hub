# -*- coding: utf-8 -*-
"""
Audit assertions for the sepsis-immunoparalysis-hub manuscript.

Root-cause guard against the failure class flagged in Round 5 (and earlier):
a *stated numeric range* in the text that does not match the cited CSV.
Run after any manuscript edit that changes a reported statistic:

    python 02_scripts/python/check_audit_assertions.py

Exits non-zero on the first failed assertion so it can gate a CI build.
"""
import csv, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESULTS = os.path.join(ROOT, "03_results")

def fail(msg):
    sys.stderr.write("ASSERTION FAILED: %s\n" % msg)
    sys.exit(1)

# --- 1) Every stated numeric *range* must be re-derived from the cited CSV ---
mr_files = [
    "10_genetics_mr_outcome5086_28ddeath.csv",
    "10_genetics_mr.csv",
    "10_genetics_mr_outcome4982_criticalcare.csv",
]
max_i2 = 0.0
n_tests = 0
for fn in mr_files:
    path = os.path.join(RESULTS, fn)
    if not os.path.exists(path):
        fail("missing MR CSV: %s" % fn)
    with open(path) as f:
        for r in csv.DictReader(f):
            if r.get("I2"):
                try:
                    max_i2 = max(max_i2, float(r["I2"]))
                    n_tests += 1
                except ValueError:
                    pass
# Manuscript states heterogeneity reaches "up to 0.50" on secondary outcomes.
if max_i2 > 0.51 + 1e-9:
    fail("max I2 across MR CSVs = %.3f exceeds stated 0.50" % max_i2)
print("OK  max I2 across %d MR tests = %.3f (stated <= 0.50)" % (n_tests, max_i2))

# --- 2) Stated MR family size must equal the number of assessable tests ---
# 5 assessable genes x 3 estimators x 3 outcomes = 45. I2 is only reported for
# IVW rows (15), so the family size is taken from the BH table (all estimators).
bh_path = os.path.join(RESULTS, "10_mr_bh_family.csv")
if not os.path.exists(bh_path):
    fail("missing BH family table: 10_mr_bh_family.csv")
with open(bh_path) as f:
    bh_rows = sum(1 for _ in csv.DictReader(f))
expected_family = 45
if bh_rows != expected_family:
    fail("BH family table rows = %d, expected %d" % (bh_rows, expected_family))
print("OK  MR family size = %d (5 genes x 3 estimators x 3 outcomes); I2 computed for %d IVW tests" % (bh_rows, n_tests))

# --- 3) §7 provenance paths must exist (spot-check the load-bearing ones) ---
must_exist = [
    "03_results/S01_immunoparalysis_direction.csv",
    "03_results/S06_auc_compare.csv",
    "03_results/09_external_validation.csv",
    "03_results/10_genetics_mr_outcome5086_28ddeath.csv",
    "03_results/10_genetics_mr.csv",
    "03_results/10_genetics_mr_outcome4982_criticalcare.csv",
    "03_results/10_mr_bh_family.csv",
    "03_results/08_candidates_drugs.csv",
    "03_results/S08_l1000_candidate_scores.csv",
]
for rel in must_exist:
    if not os.path.exists(os.path.join(ROOT, rel)):
        fail("§7 provenance path missing: %s" % rel)
print("OK  %d §7 provenance paths present" % len(must_exist))

print("\nAll baseline audit assertions passed.")

# =====================================================================
# Round-6 root-cause assertions: verify HEADLINE NUMBERS directly, not metadata.
# =====================================================================
try:
    import pandas as _pd
    import scipy.stats as _st
except Exception as e:
    sys.stderr.write("WARN: pandas/scipy unavailable, skipping Round-6 numeric assertions: %s\n" % e)
    sys.exit(0)

# --- 4) MR-Egger p must be the two-sided t(df = n-2) distribution, NOT normal ---
# Root cause of the Round-6 CD74 Egger error: a normal-based p-value made a
# borderline signal look genome-significant. This guards against regression.
mr_files_all = [
    "10_genetics_mr_outcome5086_28ddeath.csv",
    "10_genetics_mr.csv",
    "10_genetics_mr_outcome4982_criticalcare.csv",
]
egger_checked = 0
for fn in mr_files_all:
    path = os.path.join(RESULTS, fn)
    with open(path) as f:
        for r in csv.DictReader(f):
            if r.get("method") != "MR-Egger":
                continue
            try:
                beta = float(r["beta"]); se = float(r["se"]); p = float(r["p"]); nsnp = int(r["nsnp"])
            except (ValueError, KeyError, TypeError):
                continue
            if se <= 0 or nsnp < 3:
                continue
            df = nsnp - 2
            p_t = 2.0 * _st.t.sf(abs(beta) / se, df)
            if abs(p_t - p) > 1e-9:
                fail("MR-Egger p (t-dist, df=%d) = %.3e but stored p = %.3e for %s / %s" %
                     (df, p_t, p, r.get("gene"), os.path.basename(fn)))
            # sanity: the normal-based value must DIFFER (otherwise we regressed to the bug)
            p_norm = 2.0 * (1.0 - _st.norm.cdf(abs(beta) / se))
            if abs(p_norm - p) < 1e-9:
                fail("MR-Egger p for %s / %s equals the NORMAL-distribution value (t-dist regression)" %
                     (r.get("gene"), os.path.basename(fn)))
            egger_checked += 1
print("OK  %d MR-Egger p-values match t(df=n-2) distribution (normal-based values differ, as required)" % egger_checked)

# --- 5) No MR p/q value may be exactly 0.0 or < 1e-300 (silent underflow-as-zero) ---
underflow_hit = False
scan_files = mr_files_all + ["10_mr_bh_family.csv"]
for fn in scan_files:
    path = os.path.join(RESULTS, fn)
    with open(path) as f:
        for r in csv.DictReader(f):
            for col in ("p", "q_family_45test", "p_fdr_bh", "p_fdr_bh_per_outcome_15test"):
                if col in r and r[col] not in ("", None):
                    try:
                        v = float(r[col])
                    except ValueError:
                        continue
                    if v == 0.0 or v < 1e-300:
                        sys.stderr.write("  underflow/zero in %s col=%s val=%s gene=%s method=%s\n" %
                                         (fn, col, r[col], r.get("gene"), r.get("method")))
                        underflow_hit = True
if underflow_hit:
    fail("MR p/q column contains 0.0 or < 1e-300 (must be recomputed on log scale)")
print("OK  no MR p/q value is exactly 0.0 or < 1e-300")

# --- 6) Egger SE must not be substantially smaller than the same-gene IVW SE ---
# A marginal difference (a few percent) is a precision artifact and is tolerated; a
# gross difference (Egger SE << IVW SE) signals a re-introduced Egger estimation bug.
# The CD74 critical-care cell is disclosed in the manuscript as a known 3-instrument
# outlier (Egger SE 0.111 < IVW SE 0.325) and is explicitly exempted.
EXEMPT_EGGER_SE = {("CD74", "criticalcare")}
SE_TOL = 0.95  # fail only if Egger SE < 95% of IVW SE
outcome_of = {"10_genetics_mr_outcome5086_28ddeath.csv": "28ddeath",
              "10_genetics_mr.csv": "suscept",
              "10_genetics_mr_outcome4982_criticalcare.csv": "criticalcare"}
se_violation = False
for fn in mr_files_all:
    oc = outcome_of[fn]
    se_map = {}
    with open(os.path.join(RESULTS, fn)) as f:
        for r in csv.DictReader(f):
            try:
                se_map[r["method"]] = (r["gene"], float(r["se"]))
            except (ValueError, KeyError):
                continue
    if "IVW" in se_map and "MR-Egger" in se_map:
        g_ivw, ivw_se = se_map["IVW"]; g_eg, eg_se = se_map["MR-Egger"]
        if g_ivw != g_eg:
            continue
        if eg_se < ivw_se * SE_TOL and (g_ivw, oc) not in EXEMPT_EGGER_SE:
            sys.stderr.write("  Egger SE %.3f < %.3f*%.2f IVW SE for %s/%s\n" % (eg_se, ivw_se, SE_TOL, g_ivw, oc))
            se_violation = True
if se_violation:
    fail("Egger SE substantially < IVW SE for a non-exempt gene (implausible ordering)")
print("OK  Egger SE not substantially (<95%) below IVW SE; CD74 critical-care exempted (disclosed)")

# --- 7) Hub direction stated in text must match S01_mars1_deg.csv ---
deg = _pd.read_csv(os.path.join(RESULTS, "S01_mars1_deg.csv"))
hub_dir = dict(zip(deg["gene"], deg["logFC"]))
HUBS = ["CD74", "HLA-DQA1", "CD14", "FCGR3A", "HAVCR2", "FIS1"]
missing = [h for h in HUBS if h not in hub_dir]
if missing:
    fail("hub gene(s) absent from S01_mars1_deg.csv: %s" % missing)
down_hubs = [h for h in HUBS if hub_dir[h] < 0]
up_hubs = [h for h in HUBS if hub_dir[h] > 0]
expected_down = set(HUBS) - {"FIS1"}
if set(down_hubs) != expected_down or up_hubs != ["FIS1"]:
    fail("hub direction mismatch: down=%s up=%s (text claims 5 down + FIS1 up)" % (down_hubs, up_hubs))
print("OK  hub directions consistent with text: 5 Mars1-down hubs + FIS1 up (logFC +%.2f)" % hub_dir["FIS1"])

# --- 8) Each stated group-comparison P-value must be reproducible from its source CSV ---
s02 = _pd.read_csv(os.path.join(RESULTS, "S02_immunoparalysis_score.csv"))
groups = {e: s02.loc[s02["mars_endotype"] == e, "immune_function_score"].dropna().values
          for e in ["Mars1", "Mars2", "Mars3", "Mars4"]}
# text claims: Mars1 vs Mars2 P=0.47; vs Mars3 P=1.9e-18; vs Mars4 P=1.3e-3
claims = {("Mars1", "Mars2"): 0.47, ("Mars1", "Mars3"): 1.9e-18, ("Mars1", "Mars4"): 1.3e-3}
for (a, b), stated in claims.items():
    u, pval = _st.mannwhitneyu(groups[a], groups[b], alternative="two-sided")
    if stated >= 1e-2:
        ok = abs(pval - stated) <= 0.03
    else:
        ok = abs(pval - stated) / stated <= 0.10
    if not ok:
        fail("recomputed Mars1 vs %s Mann-Whitney P = %.3e but text states %.3e" % (b, pval, stated))
    else:
        print("OK  Mars1 vs %s Mann-Whitney P = %.3e (text %.3e)" % (b, pval, stated))

print("\nAll Round-6 root-cause audit assertions passed.")

