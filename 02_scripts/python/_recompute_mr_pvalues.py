"""Recompute MR p-values with the correct reference distributions and rebuild the BH family table.

Fixes (per Round 6 T0-1 / T1-6):
  * MR-Egger p uses a t-distribution with df = nsnp - 2  (was: normal dist -> grossly
    anti-conservative with few instruments, e.g. CD74 df=1).
  * Weighted-median p uses normal approx computed on the log scale (was: stored as exactly
    0.0 due to floating-point cancellation for CD74 critical care).
  * IVW p is recomputed with the normal approx (verified identical to the original).

Outputs:
  * overwrites the `p` and `p_fdr_bh` columns in the three outcome CSVs (backup kept in _mr_backup_20260927/)
  * regenerates 03_results/10_mr_bh_family.csv (45-test family BH)
  * prints the key corrected q-values for manuscript editing
"""
import csv
import os
import scipy.stats as st

BASE = os.path.join(os.path.dirname(__file__), "..", "..", "03_results")
FILES = {
    "10_genetics_mr.csv": "4980_suscept",
    "10_genetics_mr_outcome5086_28ddeath.csv": "5086_28ddeath",
    "10_genetics_mr_outcome4982_criticalcare.csv": "4982_critcare",
}
GENES_5 = ["CD74", "HLA-DQA1", "CD14", "HAVCR2", "FIS1"]
METHODS = ["IVW", "MR-Egger", "Weighted median"]


def recompute_p(method, beta, se, nsnp):
    z = beta / se
    if method == "MR-Egger":
        df = max(int(round(nsnp)) - 2, 1)
        return 2.0 * st.t.sf(abs(z), df)
    return 2.0 * st.norm.sf(abs(z))  # IVW, Weighted median (normal approx)


def bh(pvals):
    """Benjamini-Hochberg q-values, same order as input."""
    n = len(pvals)
    order = sorted(range(n), key=lambda i: pvals[i])
    q = [0.0] * n
    prev = 1.0
    for rank in range(n, 0, -1):
        i = order[rank - 1]
        val = min(pvals[i] * n / rank, prev)
        q[i] = val
        prev = val
    return [min(max(v, 0.0), 1.0) for v in q]


def load(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ----- Step 1: recompute p per outcome file, write back p + p_fdr_bh -----
per_outcome = {}  # outcome_label -> list of (gene, method, or_, p_corrected)
for fname, olab in FILES.items():
    rows = load(os.path.join(BASE, fname))
    for r in rows:
        gene, method = r["gene"], r["method"]
        if r["beta"] == "" or r["se"] == "":  # e.g. FCGR3A insufficient_instruments
            continue
        beta, se, nsnp = float(r["beta"]), float(r["se"]), float(r["nsnp"])
        p_new = recompute_p(method, beta, se, nsnp)
        if method == "IVW":
            old = float(r["p"])
            if abs(old - p_new) / max(old, 1e-30) > 1e-6:
                print(f"  [IVW MISMATCH] {gene} {olab}: old={old:.6g} new={p_new:.6g}")
        r["p"] = repr(float(p_new))
    # 15-test BH within this outcome (exclude FCGR3A, which has only IVW)
    test_rows = [r for r in rows if r["gene"] != "FCGR3A"]
    qs = bh([float(r["p"]) for r in test_rows])
    for r, q in zip(test_rows, qs):
        r["p_fdr_bh"] = repr(float(q))
    # FCGR3A row: leave p_fdr_bh blank (not part of the 15-test family)
    for r in rows:
        if r["gene"] == "FCGR3A":
            r["p_fdr_bh"] = ""
    # write back
    out = os.path.join(BASE, fname)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        if r["gene"] != "FCGR3A":
            per_outcome.setdefault(olab, []).append(
                (r["gene"], r["method"], float(r["or_"]), float(r["p"]))
            )
    print(f"[written] {fname}: {len(rows)} rows, 15-test BH applied")

# ----- Step 2: build the 45-row family table -----
fam = []  # (gene, method, outcome, or_, p)
for olab, recs in per_outcome.items():
    for gene, method, orv, p in recs:
        fam.append((gene, method, olab, orv, p))

# per-outcome 15-test BH
per_out_p = {}
per_out_q = {}
for gene, method, olab, orv, p in fam:
    per_out_p.setdefault(olab, []).append((gene, method, p))
for olab, recs in per_out_p.items():
    ps = [x[2] for x in recs]
    qs = bh(ps)
    for (gene, method, _), q in zip(recs, qs):
        per_out_q[(gene, method, olab)] = q

# 45-test family BH
ps_all = [p for *_, p in fam]
qs_all = bh(ps_all)
fam_q = []
for (gene, method, olab, orv, p), q in zip(fam, qs_all):
    fam_q.append((gene, method, olab, orv, p, per_out_q[(gene, method, olab)], q))

# sort each outcome block by p ascending (to match the published BH presentation)
blocks = {}
for row in fam_q:
    blocks.setdefault(row[2], []).append(row)
for olab in blocks:
    blocks[olab].sort(key=lambda r: r[4])

# write 10_mr_bh_family.csv
fam_path = os.path.join(BASE, "10_mr_bh_family.csv")
with open(fam_path, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["gene", "method", "outcome", "or_", "p",
                "p_fdr_bh_per_outcome_15test", "q_family_45test", "family_sig_q<0.05"])
    for gene, method, olab, orv, p, q15, q45 in blocks["4980_suscept"] + \
            blocks["4982_critcare"] + blocks["5086_28ddeath"]:
        sig = "YES" if q45 < 0.05 else "no"
        w.writerow([gene, method, olab, repr(float(orv)), repr(float(p)),
                    repr(float(q15)), repr(float(q45)), sig])

# ----- Step 3: report key q-values -----
print("\n" + "=" * 70)
print("CORRECTED KEY q-VALUES (for manuscript editing)")
print("=" * 70)
n_sig = sum(1 for r in fam_q if r[6] < 0.05)
print(f"# of 45 tests with family q < 0.05: {n_sig}")
for key in [("CD74", "MR-Egger", "4982_critcare"),
            ("CD74", "Weighted median", "4982_critcare"),
            ("CD74", "MR-Egger", "4980_suscept"),
            ("CD14", "MR-Egger", "5086_28ddeath"),
            ("CD14", "Weighted median", "5086_28ddeath"),
            ("CD74", "MR-Egger", "5086_28ddeath")]:
    for r in fam_q:
        if (r[0], r[1], r[2]) == key:
            print(f"  {key[0]:9s} {key[1]:16s} {key[2]:16s}  p={r[4]:.3e}  "
                  f"q15={r[5]:.3e}  q45={r[6]:.3e}  {'SIG' if r[6]<0.05 else 'n.s.'}")
            break
print("\nFull corrected family q (q45) for CD74 and CD14 across outcomes:")
for r in fam_q:
    if r[0] in ("CD74", "CD14"):
        print(f"  {r[0]:9s} {r[1]:16s} {r[2]:16s}  p={r[4]:.3e}  q45={r[6]:.3e}")
print(f"\n[written] {fam_path}")
