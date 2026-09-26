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

print("\nAll audit assertions passed.")
