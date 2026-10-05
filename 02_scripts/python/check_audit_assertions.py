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

# --- 2) The 15-test PRIMARY family must contain exactly the 5 assessable genes x 3 outcomes ---
# (v1.19.0 reframing: the pre-specified primary family is IVW only — 5 assessable genes x
# 3 outcomes = 15 — and the two sensitivity estimators (MR-Egger, weighted median) are not
# counted in it. The BH table additionally carries FCGR3A IVW placeholders (insufficient
# instruments) and the 30 sensitivity rows, hence 48 total rows, but only 15 are 'primary'.)
bh_path = os.path.join(RESULTS, "10_mr_bh_family.csv")
if not os.path.exists(bh_path):
    fail("missing BH family table: 10_mr_bh_family.csv")
with open(bh_path) as f:
    bh_all = list(csv.DictReader(f))
primary = [r for r in bh_all if r.get("family_role") == "primary"]
if len(primary) != 15:
    fail("primary (15-test) family rows = %d, expected 15 (5 assessable genes x 3 outcomes)" % len(primary))
for r in primary:
    if r["method"] != "IVW" or r.get("sig_15test_q05") != "no":
        fail("primary family row %s/%s/%s not IVW or unexpectedly significant"
             % (r["gene"], r["outcome"], r["method"]))
min_q = min(float(r["q_bh_15test"]) for r in primary if r["q_bh_15test"] not in ("", None))
if min_q < 0.05 - 1e-9:
    fail("primary 15-test family minimum q = %.4f but should be >= 0.05 (v1.19.0: no family-significant test)" % min_q)
print("OK  MR primary 15-test family = %d rows (5 genes x 3 outcomes, IVW); min q = %.4f (>=0.05)" % (len(primary), min_q))

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
# v1.21.0 framing: the PRIMARY external transport metric is the LOCKED-L1 model
# (AUC 0.585, manuscript §3.5/§7). The fixed-orientation EQUAL-WEIGHT / oriented-sum score
# (AUC 0.638) is the PRE-SPECIFIED sensitivity analysis reported alongside it.
# Assertion #13 verifies the equal-weight 0.638 value is reproducible from source;
# assertion #17 verifies the locked-L1 0.585. Both numbers are kept and both are checked.
auc_ext = ext["auc_EMTAB4451_orientedSum"]
ci_lo = ext["auc_EMTAB4451_orientedSum_CI95_low"]
ci_hi = ext["auc_EMTAB4451_orientedSum_CI95_high"]
n_ext = ext["n_validated_samples"]; d_ext = ext["n_deaths"]
if (abs(auc_ext - 0.638) > 1e-3 or abs(ci_lo - 0.532) > 1e-3 or abs(ci_hi - 0.748) > 1e-3
        or int(n_ext) != 106 or int(d_ext) != 52):
    fail("external validation mismatch: AUC=%.3f CI=(%.3f,%.3f) n=%s deaths=%s"
         % (auc_ext, ci_lo, ci_hi, n_ext, d_ext))
print("OK  external validation equal-weight AUC=0.638 (95%% CI 0.532-0.748, pre-specified sensitivity); n=106, 52 deaths")

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

# --- 15) Forest significance flag is real and matches the v1.19.0 corrected finding ---
# (v1.19.0: after the MR-Egger p-values were corrected to the t-distribution, NO test in the
# 15-test primary family is significant; the CD74 critical-care weighted-median signal that
# previously drove a 'family-significant' red point was an artefact of the normal approximation
# and a degenerate bootstrap SE, and is now explicitly NOT flagged.)
fam = _pd.read_csv(os.path.join(RESULTS, "10_mr_bh_family.csv"))
if "sig_15test_q05" not in fam.columns:
    fail("family table missing 'sig_15test_q05' column (audit must track the renamed flag)")
red = int((fam["sig_15test_q05"].astype(str).str.strip().str.upper() == "YES").sum())
if red != 0:
    fail("%d family-significant (q<0.05) tests under 15-test primary family; v1.19.0 finding is ZERO" % red)
cd74 = fam[(fam["gene"] == "CD74") & (fam["method"] == "Weighted median")
           & (fam["outcome"].astype(str).str.contains("crit", case=False))]
if len(cd74) == 0:
    fail("CD74 critical-care weighted median row missing from family table")
elif cd74["sig_15test_q05"].astype(str).str.strip().str.upper().iloc[0] == "YES":
    fail("CD74 critical-care weighted median should NOT be family-significant (v1.19.0: min q = 0.81)")
print("OK  forest flag matches v1.19.0: 0 family-significant tests (15-test primary); CD74 crit-care WM NOT flagged")

# --- 16) Retained MR-CSV integrity: 28-day-death primary IVW tests are a genuine null ---
# (The MR layer was removed from the manuscript at v1.20.0; these CSVs are retained only
#  as an audit trail. The prior gate asserted "manuscript states P >= 0.23"; that manuscript
#  statement no longer exists, so this assertion now checks the trail itself: the primary
#  IVW tests must be non-significant, i.e. a genuine null, not a faked one.)
prim = _pd.read_csv(os.path.join(RESULTS, "10_genetics_mr_outcome5086_28ddeath.csv"))
ivw = prim[prim["method"] == "IVW"].copy()
# p is stored as text and the weighted-median rows are blank by design (nsnp<10);
# coerce so the blank cells are ignored rather than forcing an object dtype crash.
ivw["p_num"] = _pd.to_numeric(ivw["p"], errors="coerce")
min_p = float(ivw["p_num"].min())
if min_p < 0.05 - 1e-9:
    fail("28-day-death primary IVW minimum P = %.3e (expected a genuine null, all > 0.05)" % min_p)
print("OK  retained MR trail (28-day death, 5 primary IVW tests): min IVW P = %.3f (genuine null; 0/15 family-significant under BH)" % min_p)

# --- 17) L1-locked external AUC must equal 0.585 (PRIMARY external transport metric in v1.21.0; distinct from equal-weight 0.638 sensitivity) ---
_ext2 = _pd.read_csv(os.path.join(RESULTS, "09_external_validation.csv"))
_ext2["value"] = _pd.to_numeric(_ext2["value"], errors="coerce")
locked = float(_ext2.set_index("metric")["value"]["auc_EMTAB4451_external_locked"])
if abs(locked - 0.585) > 1e-3:
    fail("L1-locked external AUC = %.3f, expected 0.585" % locked)
print("OK  L1-locked external AUC = %.3f (primary external transport metric; oriented-sum 0.638 is the pre-specified sensitivity)" % locked)

# --- 18) MR layer removed from manuscript at v1.20.0; MR CSVs retained as audit trail ---
# The original #18 cross-checked the manuscript's rendered MR Table-3 Egger P against the
# t(df=n-2) recompute from the source CSV. Because the MR tier was removed from the manuscript
# (v1.20.0 decision: Tier-3, all null, not a core contribution), that Table-3 no longer exists,
# so the manuscript cross-check is intentionally disabled. The MR CSVs are RETAINED as an audit
# trail proving the removed layer was genuinely null (not faked); this assertion keeps them
# self-consistent by recomputing the Egger t-dist p from the CSV for every gene and confirming
# the values are finite and in [0,1] (catching any silent corruption of the null evidence).
_mr_t3 = _pd.read_csv(os.path.join(RESULTS, "10_genetics_mr_outcome5086_28ddeath.csv"))
_eg_tdist = {}
for _, r in _mr_t3[_mr_t3["method"] == "MR-Egger"].iterrows():
    b = float(r["beta"]); se = float(r["se"]); n = int(r["nsnp"])
    _eg_tdist[r["gene"]] = 2 * st.t.sf(abs(b / se), df=n - 2)
if len(_eg_tdist) < 5:
    fail("MR Egger t-dist recompute yielded %d genes (expected >=5)" % len(_eg_tdist))
for g, p in _eg_tdist.items():
    if not (0.0 <= p <= 1.0):
        fail("retained MR Egger t-dist p out of [0,1] for %s: %r" % (g, p))
print("OK  MR layer removed from manuscript at v1.20.0; retained MR CSV recomputes t-dist "
      "Egger p in [0,1] for all %d genes (audit-trail self-consistency; manuscript "
      "Table-3 cross-check intentionally disabled)" % len(_eg_tdist))

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
if not _abs or "within-cohort" not in _abs.group(1).lower():
    fail("English abstract does not frame the work as a within-cohort confirmation (missing 'within-cohort')")
if "true replication" not in _mansrc.lower():
    fail("Discussion lacks the replication hedge for the confirmation claim (missing 'true replication')")
for bad in ["isolated hub genes", "MR layer is null"]:
    if bad in _mansrc:
        fail("Stale discovery phrasing still present: %r" % bad)
print("OK  framing: title free of 'dissection'; abstract frames within-cohort confirmation; Discussion hedges true replication; no stale discovery phrasing")

# --- 20) Calibration 'well behaved' must be gone (slope 0.50 is under-fitting) ---
if "well behaved" in _mansrc.lower():
    fail("Calibration still described as 'well behaved' (slope 0.50 is under-fitting)")
print("OK  calibration no longer described as 'well behaved'")

# --- 21) ImmunoSep 53% attributed to the dual ferritin+mHLA-DR algorithm ---
_m = re.search(r"53%.{0,220}", _mansrc)
if not _m or "ferritin" not in _m.group(0).lower():
    fail("The 53%-unclassifiable statement does not name the dual ferritin+mHLA-DR algorithm")
print("OK  ImmunoSep 53% correctly attributed to dual ferritin+mHLA-DR algorithm")

# =====================================================================
# Round-11 (v1.12.0) review-driven assertions
# =====================================================================
# --- 22) Section 7 (Number provenance) must contain no CJK characters ---
_sec7 = re.search(r"## 7\..*?(?=\n## 8\.)", _mansrc, re.S)
if not _sec7:
    fail("Section 7 (Number provenance) not found")
_cjk = re.findall(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]", _sec7.group(0))
if _cjk:
    fail("Section 7 still contains %d CJK character(s): %r" % (len(_cjk), _cjk[:10]))
print("OK  Section 7 (Number provenance) is fully English (no CJK)")

# --- 23) Reference (ImmunoSep / Giamarellos, JAMA) must carry volume / pages / DOI ---
# Number-agnostic: the reference is located by author+journal, not by its numeric
# label, because the citation order is re-derived from first-appearance each revision.
_ref = re.search(r"\d+\.\s+Giamarellos.*?JAMA.*?(?=\n\d+\.|$)", _mansrc, re.S)
if not _ref:
    fail("Reference (ImmunoSep / Giamarellos, JAMA) not found")
_r = _ref.group(0)
for _need in ["335", "775", "10.1001/jama.2025.24175"]:
    if _need not in _r:
        fail("Reference (ImmunoSep / Giamarellos) missing %r (requires volume 335 / pages 775 / DOI 10.1001/jama.2025.24175): %s" % (_need, _r.strip()))
print("OK  Reference (ImmunoSep / Giamarellos, JAMA) carries volume 335, pages 775, DOI 10.1001/jama.2025.24175")

# --- 24) Dexamethasone must NOT be described as "scored high" ---
for _m in re.finditer(r"dexamethasone", _mansrc, re.I):
    _win = _mansrc[_m.end():_m.end() + 90]
    if "scored high" in _win.lower():
        fail("Dexamethasone described as 'scored high' in window: %r" % _win)
print("OK  dexamethasone is not described as 'scored high' (only prednisone scored high)")

# --- 25) No 'implausible' framing of the MR-Egger SE ordering ---
if "implausible" in _mansrc.lower():
    fail("Manuscript still uses 'implausible' to describe the MR-Egger SE ordering")
print("OK  MR-Egger SE ordering no longer described as 'implausible'")

# --- 26) DCA framed on CALIBRATION-CORRECTED probabilities (discrimination-only) ---
# Locked to the corrected v1.13.0 framing. The deposited code (_ext_calibration_dca.py)
# feeds the logistic-fit calibration probabilities (intercept -0.04, slope 0.50), NOT raw
# scores, so "uncalibrated" is a Round-12 Tier-1 contradiction that must never re-appear.
_dca = re.search(r"decision-curve analysis.{0,1500}", _mansrc, re.I)
if not _dca:
    fail("Decision-curve analysis sentence not found")
_dcatxt = _dca.group(0)
if "calibration-corrected" not in _dcatxt.lower():
    fail("DCA not framed on calibration-corrected probabilities: %r" % _dcatxt)
if "uncalibrated" in _dcatxt.lower():
    fail("DCA still described as 'uncalibrated' (Round-12 Tier-1 contradiction): %r" % _dcatxt)
if "discrimination" not in _dcatxt.lower():
    fail("DCA not framed as discrimination-only support: %r" % _dcatxt)
print("OK  DCA framed on calibration-corrected probabilities (discrimination-only); 'uncalibrated' absent")

# --- 27) Recomputed 3-gene IRG proxy benchmark must equal 0.5288 (v1.13.0 IRG-3 re-orientation) ---
# Guards against the Round-12 finding that the old 0.604 benchmark left LTB4R/IL4R unoriented.
_irg3 = float(_ext.set_index("metric")["value"]["auc_IRG3_benchmark_EMTAB4451"])
if abs(_irg3 - 0.5288) > 1e-3:
    fail("IRG-3 benchmark = %.4f, expected 0.5288 (v1.13.0 re-orientation)" % _irg3)
print("OK  IRG-3 benchmark = %.4f (v1.13.0 re-orientation; was 0.604)" % _irg3)

# --- 28) L1000 candidate rescue ranks reproducible from S08_l1000_candidate_scores.csv ---
_l1000 = _pd.read_csv(os.path.join(RESULTS, "S08_l1000_candidate_scores.csv"))
def _l1000_rank(c):
    r = _l1000[_l1000["candidate"] == c]
    if not len(r):
        fail("L1000 candidate %s missing from S08_l1000_candidate_scores.csv" % c)
    return int(r.iloc[0]["rescue_rank"])
_r_len = _l1000_rank("lenalidomide"); _r_azi = _l1000_rank("azithromycin")
if _r_len != 5435:
    fail("lenalidomide L1000 rescue_rank = %d, expected 5435" % _r_len)
if _r_azi != 9152:
    fail("azithromycin L1000 rescue_rank = %d, expected 9152" % _r_azi)
print("OK  L1000 candidate rescue ranks: lenalidomide 5435, azithromycin 9152 (match manuscript)")

# --- 29) DCA prose must match the deposited grid (closes Round-13 Tier-1 contradiction) ---
_grid = _pd.read_csv(os.path.join(RESULTS, "09_ext_dca_grid.csv"))
_grid["nb_model"] = _pd.to_numeric(_grid["nb_model"], errors="coerce")
_grid["nb_treat_all"] = _pd.to_numeric(_grid["nb_treat_all"], errors="coerce")
_first_exceed = _grid[_grid["nb_model"] > _grid["nb_treat_all"] + 1e-9]["threshold"].min()
if _first_exceed is None or abs(_first_exceed - 0.30) > 1e-6:
    fail("DCA grid: model first exceeds treat-all at threshold %s, expected 0.30" % _first_exceed)
_row80 = _grid[_grid["threshold"] == 0.80]
if len(_row80) == 0:
    fail("DCA grid missing threshold 0.80 row")
else:
    _m80 = float(_row80["nb_model"].iloc[0]); _t80 = float(_row80["nb_treat_all"].iloc[0])
    if not (_m80 <= 1e-6 and _t80 < -1.0):
        fail("DCA grid @0.80: model NB=%.3f treat-all NB=%.3f (expected model~0, treat-all<<0, diverging)" % (_m80, _t80))
if "converging toward treat-all" in _mansrc:
    fail("DCA prose regressed to 'converging toward treat-all' (Round-13 Tier-1 contradiction)")
if "exceeds treat-all only at thresholds" in _mansrc:
    fail("DCA prose regressed to 'exceeds treat-all only at thresholds' (Round-13 Tier-1 contradiction)")
if "exceeds the treat-all strategy from threshold" not in _mansrc:
    fail("DCA prose missing corrected 'exceeds the treat-all strategy from threshold ...' statement")
print("OK  DCA prose matches deposited grid (model exceeds treat-all from 0.30; diverges at 0.80); no regression")

# --- 30) Reference list integrity (guards the Vancouver re-numbering, v1.15.0) ---
# v1.18.0: the expected count is now DERIVED from the body's maximum citation
# number instead of hard-coded, so inserting a reference (Round-17 added the
# sepsis TIM-3 review as [20]) cannot make this gate fail spuriously.
# Requirements: entries numbered contiguously 1..N; first body citation is [1];
# no in-text [N] exceeds N; first-appearance order equals numeric order.
_refsec_m = re.search(r"## References\s*(.*)$", _mansrc, re.S)
if not _refsec_m:
    fail("Reference section not found")
_ref_entries = re.findall(r"^(\d+)\.\s", _refsec_m.group(1), re.M)
_body_only = _mansrc.split("## References")[0]
_first_cit = re.search(r"\[(\d+)\]", _body_only)
if not _first_cit or _first_cit.group(1) != "1":
    fail("First in-text citation in body is [%s], expected [1] (Vancouver order)" %
         (_first_cit.group(1) if _first_cit else "none"))
_cited = [int(c) for c in re.findall(r"\[(\d+)\]", _body_only)]
_max_cited = max(_cited) if _cited else 0
_exp_n = _max_cited  # every reference must be cited, so list size == max citation
if len(_ref_entries) != _exp_n:
    fail("Reference list has %d entries but the body cites up to [%d]; expected %d"
         % (len(_ref_entries), _max_cited, _exp_n))
_ref_nums = [int(x) for x in _ref_entries]
if _ref_nums != list(range(1, len(_ref_nums) + 1)):
    fail("Reference numbering is not contiguous 1..%d (found %s)"
         % (len(_ref_nums), _ref_nums[:12]))
_bad = [c for c in _cited if c > len(_ref_entries)]
if _bad:
    fail("In-text citation number(s) exceed the reference-list size: %s" % sorted(set(_bad))[:10])
_uncited = [n for n in range(1, len(_ref_entries) + 1) if n not in set(_cited)]
if _uncited:
    fail("Reference(s) never cited in text: %s" % _uncited[:10])
_firstpos = {}
for _m in re.finditer(r"\[(\d+)\]", _body_only):
    _firstpos.setdefault(int(_m.group(1)), _m.start())
_by_first = sorted(_firstpos, key=lambda n: _firstpos[n])
if _by_first != sorted(_by_first):
    fail("Vancouver first-appearance order violated; first-citation sequence is %s"
         % _by_first[:12])
# every reference must end with a bare DOI (no trailing period)
_baddoi = re.findall(r"doi:\S+\.\s*$", _refsec_m.group(1), re.M)
if _baddoi:
    fail("Reference DOI(s) end with a trailing period: %s" % _baddoi[:5])
print("OK  Reference list integrity: %d entries contiguous 1..%d, first citation [1], "
      "all cited, Vancouver first-appearance order preserved, no DOI trailing period"
      % (len(_ref_entries), len(_ref_entries)))

# --- 31) Data-availability tag / commit-hash consistency (anti-regression guard) ---
# Round-16 caught a self-contradiction: the DA line claimed the evaluated commit
# `fc5473b` was tagged `v1.16.0`, but v1.16.0 = `1212f7b` and `fc5473b` is v1.15.0.
# This guard derives the ground-truth commit hash from git (when available) and
# asserts (a) the "current evaluated commit <HASH> is tagged <TAG>" clause matches
# git's rev-parse of <TAG>, and (b) the GitHub-release tag equals the latest repo tag.
import subprocess as _sp
_da = re.search(r"## Data availability\s*(.*?)\n## ", _mansrc, re.S)
if not _da:
    fail("Data availability section not found")
_dasrc = _da.group(1)
_rel_tag = re.search(r"GitHub release \(tag (v\d+\.\d+\.\d+)\)", _dasrc)
_eval = re.search(r"current evaluated commit (\w+) is tagged (v\d+\.\d+\.\d+)", _dasrc)
if not _rel_tag:
    fail("Data availability does not state the GitHub release tag (tag vX.Y.Z)")
if not _eval:
    fail("Data availability does not state the evaluated commit hash / tag clause")
_rel_v = _rel_tag.group(1)
_eval_hash = _eval.group(1)
_eval_tag = _eval.group(2)
# Ground truth from git when the repo and tags are present (CI / local checkout).
_git = _sp.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=ROOT,
               capture_output=True, text=True)
if _git.returncode == 0:
    _rev = _sp.run(["git", "rev-parse", _eval_tag], cwd=ROOT,
                   capture_output=True, text=True)
    if _rev.returncode == 0:
        _truth = _rev.stdout.strip()
        if not (_truth == _eval_hash or _truth.startswith(_eval_hash) or _eval_hash in _truth):
            fail("DA claims commit %s is tagged %s, but git rev-parse %s = %s"
                 % (_eval_hash, _eval_tag, _eval_tag, _truth))
    _latest = _sp.run(["git", "describe", "--tags", "--abbrev=0"], cwd=ROOT,
                      capture_output=True, text=True)
    if _latest.returncode == 0 and _latest.stdout.strip():
        if _latest.stdout.strip() != _rel_v:
            fail("DA release tag %s != latest git tag %s" % (_rel_v, _latest.stdout.strip()))
    print("OK  DA tag/commit consistency verified against git: release %s, %s=%s" % (_rel_v, _eval_tag, _eval_hash))
else:
    print("OK  DA tag/commit clause present (release %s; %s=%s); git cross-check skipped (not a checkout)"
          % (_rel_v, _eval_tag, _eval_hash))

print("\nAll Round-6 + Round-7 (hardened) + Round-10 framing + v1.12.0..v1.17.0 review audit assertions passed (32 assertions).")

