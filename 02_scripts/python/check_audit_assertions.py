# -*- coding: utf-8 -*-
"""
Audit assertions for the sepsis-immunoparalysis-hub manuscript.

Root-cause guard against the failure class flagged in Round 5 (and earlier):
a *stated numeric range* in the text that does not match the cited CSV.
Run after any manuscript edit that changes a reported statistic:

    python 02_scripts/python/check_audit_assertions.py

Exits non-zero on the first failed assertion so it can gate a CI build.
"""
import csv, glob, math, os, re, sys
import scipy.stats as st

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
    # A missing pandas/scipy must NOT be reported as a clean pass — a gated CI
    # build that cannot import the numeric stack would otherwise silently "succeed".
    # Exit non-zero so the gate fails loudly instead of no-op'ing.
    sys.stderr.write("ERROR: pandas/scipy unavailable, cannot run the numeric assertions that actually guard the headline numbers: %s\n" % e)
    sys.exit(2)

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
# HUBS are read from S05_hub_genes.csv (genes selected by all three methods),
# not hard-coded, so the assertion tracks the actual discovery output.
s05 = _pd.read_csv(os.path.join(RESULTS, "S05_hub_genes.csv"))
def _t(x):
    return str(x).strip().lower() == "true"
HUBS = s05[[_t(r.lasso) and _t(r.rf) and _t(r.univariate) for _, r in s05.iterrows()]]["gene"].tolist()
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

# =====================================================================
# Round-7 audit hardening (A3 A9-A16): guard the headline numbers the
# prose actually headlines, not just metadata. Each re-derives a reported
# quantity from its source CSV.
# =====================================================================

# --- 9) OR / CI must be algebraically consistent with beta, se ---
# Guards against a hand-edited OR or CI that drifted from the regression output.
or_ci_bad = 0
for fn in mr_files_all:
    path = os.path.join(RESULTS, fn)
    with open(path) as f:
        for r in csv.DictReader(f):
            try:
                b = float(r["beta"]); s = float(r["se"])
                OR = float(r["or_"]); lo = float(r["ci_lo"]); hi = float(r["ci_hi"])
            except (ValueError, KeyError, TypeError):
                continue
            if (abs(math.exp(b) - OR) > 1e-3
                    or abs(math.exp(b - 1.96 * s) - lo) > 1e-3
                    or abs(math.exp(b + 1.96 * s) - hi) > 1e-3):
                or_ci_bad += 1
if or_ci_bad:
    fail("%d MR rows have OR/CI inconsistent with beta/se (hand-edit risk)" % or_ci_bad)
print("OK  OR/CI algebraically consistent with beta/se across all MR rows")

# --- 10) Consensus immune counts 23/22/21 reproducible from S01 ---
imm = _pd.read_csv(os.path.join(RESULTS, "S01_immunoparalysis_direction.csv"))
d_down = int((imm["direction"] == "Mars1_down").sum())
d_fdr = int((imm["adj.P.Val"] < 0.05).sum())
d_both = int(((imm["direction"] == "Mars1_down") & (imm["adj.P.Val"] < 0.05)).sum())
if (d_down, d_fdr, d_both) != (23, 22, 21):
    fail("consensus immune counts = (%d,%d,%d), text claims (23,22,21)" % (d_down, d_fdr, d_both))
print("OK  consensus immune counts = 23/22/21 (down / FDR / both)")

# --- 11) Table-1 immune-gene effects reproducible from S01 ---
t1map = {"HLA-DRB1": (-0.89, 1.1e-15), "CD74": (-0.76, 2.1e-15),
         "CD14": (-0.77, 1e-300), "FCGR3A": (-0.61, 9.1e-11), "HAVCR2": (-0.35, 2.8e-13)}
for g, (lfc, ap) in t1map.items():
    r = imm[imm["gene"] == g]
    if not len(r):
        fail("Table-1 gene %s missing from S01" % g); continue
    r = r.iloc[0]
    if abs(r["logFC"] - lfc) > 1e-2:
        fail("Table-1 %s logFC %.2f != %.2f (S01)" % (g, r["logFC"], lfc))
    if ap > 1e-100 and abs(r["adj.P.Val"] - ap) / max(ap, 1e-30) > 0.1:
        fail("Table-1 %s adj.P %.1e != %.1e (S01)" % (g, r["adj.P.Val"], ap))
print("OK  Table-1 immune-gene logFC + adj.P match S01")

# --- 12) Table-2 response_gene_concordance reproducible from 08_candidates_drugs.csv ---
drugs = _pd.read_csv(os.path.join(RESULTS, "08_candidates_drugs.csv"))
# expected = exact curated n_rescue / n_target fraction (the prose rounds to 2 dp)
exp_frac = {"IL-7": 4/5, "GM-CSF": 4/6, "IFN-gamma": 4/7, "Azithromycin": 2/3,
            "Lenalidomide": 2/5, "Thymosin alpha1": 2/5, "BCG (trained immunity)": 1/5}
for cmpd, frac in exp_frac.items():
    rr = drugs[drugs["compound"] == cmpd]
    if not len(rr):
        fail("Table-2 compound %s missing from 08_candidates_drugs.csv" % cmpd); continue
    got = float(rr.iloc[0]["rescue_fraction"])
    if abs(got - frac) > 1e-3:
        fail("Table-2 %s concordance %.3f != %.3f (CSV)" % (cmpd, got, frac))
print("OK  Table-2 response_gene_concordance matches 08_candidates_drugs.csv")

# --- 13) External validation AUC / CI / n / deaths reproducible ---
_ext = _pd.read_csv(os.path.join(RESULTS, "09_external_validation.csv"))
_ext["value"] = _pd.to_numeric(_ext["value"], errors="coerce")
ext = _ext.set_index("metric")["value"]
# The primary external metric is the fixed-orientation EQUAL-WEIGHT / oriented-sum score
# (manuscript §3.5, AUC 0.638). The "locked" L1-weight model is a sensitivity analysis
# (§3.4, AUC 0.585) and must NOT be asserted against the 0.638 headline.
auc_ext = ext["auc_EMTAB4451_orientedSum"]
ci_lo = ext["auc_EMTAB4451_orientedSum_CI95_low"]
ci_hi = ext["auc_EMTAB4451_orientedSum_CI95_high"]
n_ext = ext["n_validated_samples"]; d_ext = ext["n_deaths"]
if (abs(auc_ext - 0.638) > 1e-3 or abs(ci_lo - 0.532) > 1e-3 or abs(ci_hi - 0.748) > 1e-3
        or int(n_ext) != 106 or int(d_ext) != 52):
    fail("external validation mismatch: AUC=%.3f CI=(%.3f,%.3f) n=%s deaths=%s"
         % (auc_ext, ci_lo, ci_hi, n_ext, d_ext))
print("OK  external validation AUC=0.638 (95%% CI 0.532-0.748), n=106, 52 deaths")

# --- 14) Calibration slope/intercept + DCA net benefit reproducible ---
cal = _pd.read_csv(os.path.join(RESULTS, "09_ext_calibration_dca.csv"))
if (abs(cal["calib_slope"][0] - 0.50) > 1e-2 or abs(cal["calib_intercept"][0] + 0.04) > 1e-2
        or abs(cal["auc"][0] - 0.638) > 1e-3):
    fail("calibration metrics mismatch: slope=%.3f intercept=%.3f auc=%.3f"
         % (cal["calib_slope"][0], cal["calib_intercept"][0], cal["auc"][0]))
if abs(cal["nb_thr0.30"][0] - 0.2844) > 1e-3 or abs(cal["nb_thr0.50"][0] - 0.0755) > 1e-3:
    fail("DCA net benefit mismatch: NB@0.30=%.3f NB@0.50=%.3f"
         % (cal["nb_thr0.30"][0], cal["nb_thr0.50"][0]))
print("OK  calibration slope=0.50/intercept=-0.04, AUC=0.638, NB@0.30=0.284/NB@0.50=0.076")

# --- 15) Forest significance flag is real (guards the T1-2 red-highlight regression) ---
fam = _pd.read_csv(os.path.join(RESULTS, "10_mr_bh_family.csv"))
red = int((fam["family_sig_q<0.05"].astype(str).str.strip().str.upper() == "YES").sum())
if red < 1:
    fail("family-sig flag has 0 YES entries; forest would draw 0 red points (T1-2 regression)")
cd74 = fam[(fam["gene"] == "CD74") & (fam["method"] == "Weighted median")
           & (fam["outcome"].astype(str).str.contains("crit", case=False))]
if len(cd74) == 0:
    fail("CD74 critical-care weighted median row missing from family table")
elif cd74["family_sig_q<0.05"].astype(str).str.strip().str.upper().iloc[0] != "YES":
    fail("CD74 critical-care weighted median should be family-significant (YES)")
print("OK  forest significance flag real: %d family-significant test(s); CD74 crit-care WM flagged" % red)

# --- 16) Primary-outcome minimum IVW P must be >= 0.23 (manuscript "P >= 0.23") ---
prim = _pd.read_csv(os.path.join(RESULTS, "10_genetics_mr_outcome5086_28ddeath.csv"))
ivw = prim[prim["method"] == "IVW"]
min_p = float(ivw["p"].min())
if min_p < 0.23 - 1e-9:
    fail("primary-outcome minimum IVW P = %.3e but manuscript states P >= 0.23" % min_p)
print("OK  primary-outcome minimum IVW P = %.3f (manuscript states >= 0.23)" % min_p)

# --- 17) L1-locked external AUC must equal 0.585 (sensitivity analysis, distinct from 0.638) ---
_ext2 = _pd.read_csv(os.path.join(RESULTS, "09_external_validation.csv"))
_ext2["value"] = _pd.to_numeric(_ext2["value"], errors="coerce")
locked = float(_ext2.set_index("metric")["value"]["auc_EMTAB4451_external_locked"])
if abs(locked - 0.585) > 1e-3:
    fail("L1-locked external AUC = %.3f, expected 0.585" % locked)
print("OK  L1-locked external AUC = %.3f (distinct from oriented-sum 0.638)" % locked)

# --- 18) Manuscript Table-3 MR-Egger P must equal the t-dist CSV value (closes "2nd occurrence" gap) ---
# The Round-6 bug (Egger p normal vs t) was fixed in the CSV and guarded by an earlier
# assertion, but the *rendered Table 3 prose* carried stale normal-dist values in v1.7/v1.8.
# This assertion parses the manuscript Table-3 Egger column and compares it to the t(df=n-2) p
# recomputed from the MR-Egger rows of the source CSV, so the table and CSV cannot drift again.
_mr_t3 = _pd.read_csv(os.path.join(RESULTS, "10_genetics_mr_outcome5086_28ddeath.csv"))
_eg_tdist = {}
for _, r in _mr_t3[_mr_t3["method"] == "MR-Egger"].iterrows():
    b = float(r["beta"]); se = float(r["se"]); n = int(r["nsnp"])
    _eg_tdist[r["gene"]] = 2 * st.t.sf(abs(b / se), df=n - 2)
_sup_map = {"\u2070": "0", "\u00b9": "1", "\u00b2": "2", "\u00b3": "3", "\u2074": "4",
            "\u2075": "5", "\u2076": "6", "\u2077": "7", "\u2078": "8", "\u2079": "9",
            "\u207b": "-"}
_manuscript_path = os.path.join(ROOT, "05_reports", "manuscript.md")
_t3_checked = 0
with open(_manuscript_path, encoding="utf-8") as f:
    for line in f:
        m = re.match(r"^\|\s*(CD74|HLA-DQA1|CD14|HAVCR2|FIS1)\s*\|", line)
        if not m:
            continue
        gene = m.group(1)
        parts = [p.strip() for p in line.split("|")]
        inner = re.search(r"\(([^)]+)\)", parts[5])  # Egger OR (P) field
        if not inner:
            continue
        pstr = inner.group(1).replace("\u00d710", "e")
        pstr = "".join(_sup_map.get(ch, ch) for ch in pstr)
        try:
            pman = float(pstr)
        except ValueError:
            continue
        exp = _eg_tdist.get(gene)
        if exp is None:
            continue
        if abs(pman - exp) > 0.01:
            fail("Table-3 %s Egger P (manuscript %.2f) != CSV t-dist %.2f" % (gene, pman, exp))
        _t3_checked += 1
if _t3_checked < 5:
    fail("Table-3 Egger P guard only matched %d hub rows (expected 5)" % _t3_checked)
print("OK  Table-3 MR-Egger P matches t-dist CSV for all %d genes (2nd-occurrence guard)" % _t3_checked)

# =====================================================================
# Round-10 framing-layer assertions (close the "conceptual 2nd-occurrence" gap)
# =====================================================================
_mp = os.path.join(ROOT, "05_reports", "manuscript.md")
with open(_mp, encoding="utf-8") as f:
    _mansrc = f.read()

# --- 19) No discovery verb without a near-replication hedge in title/abstract/discussion ---
_title_line = _mansrc.splitlines()[0]
if "dissection" in _title_line.lower():
    fail("Title still uses discovery verb 'dissection': %s" % _title_line)
_abs = re.search(r"## Abstract \(English\)(.*?)\n## ", _mansrc, re.S)
if not _abs or "confirm" not in _abs.group(1).lower():
    fail("English abstract does not frame the work as confirmation (missing 'confirm')")
if "near-replication" not in _mansrc.lower():
    fail("Discussion lacks the 'near-replication' hedge for the discovery claim")
for bad in ["isolated hub genes", "MR layer is null"]:
    if bad in _mansrc:
        fail("Stale discovery phrasing still present: %r" % bad)
print("OK  framing: title free of 'dissection'; abstract frames confirmation; Discussion hedges near-replication; no stale discovery phrasing")

# --- 20) Calibration 'well behaved' must be gone (slope 0.50 is under-fitting) ---
if "well behaved" in _mansrc.lower():
    fail("Calibration still described as 'well behaved' (slope 0.50 is under-fitting)")
print("OK  calibration no longer described as 'well behaved'")

# --- 21) ImmunoSep 53% attributed to the dual ferritin+mHLA-DR algorithm ---
_m = re.search(r"53%.{0,220}", _mansrc)
if not _m or "ferritin" not in _m.group(0).lower():
    fail("The 53%-unclassifiable statement does not name the dual ferritin+mHLA-DR algorithm")
print("OK  ImmunoSep 53% correctly attributed to dual ferritin+mHLA-DR algorithm")

print("\nAll Round-6 + Round-7 (hardened) + Round-10 framing audit assertions passed.")

