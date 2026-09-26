"""Editor's independent verification of the MR-Egger p-value distribution claim.

Claim under test (from the provenance auditor): every MR-Egger p-value in this
project was computed as 2*(1-Phi(|beta/se|)) -- a NORMAL distribution -- even
though the same rows record Q_df = n-2, i.e. the correct reference is a
t-distribution with n-2 degrees of freedom.

If true, the manuscript's headline causal claim (CD74 critical-care MR-Egger
q ~ 1.5e-11) collapses, because with 3 instruments df = 1 and t(1) has far
heavier tails than the normal.

This script reads ONLY the raw MR result CSVs and recomputes from scratch.
It does not read any reviewer file.
"""

import csv
import math
import os

RESULTS = os.path.join(os.path.dirname(__file__), "..", "..", "03_results")

MR_FILES = [
    "10_genetics_mr.csv",
    "10_genetics_mr_harmonised.csv",
    "10_genetics_mr_outcome5086_28ddeath.csv",
    "10_genetics_mr_outcome5086_harmonised.csv",
    "10_genetics_mr_outcome4982_criticalcare.csv",
    "10_genetics_mr_outcome4982_harmonised.csv",
]


# ---------- distribution helpers (pure python, no scipy dependency) ----------

def norm_sf(z):
    """Upper-tail survival function of the standard normal."""
    return 0.5 * math.erfc(z / math.sqrt(2.0))


def _betacf(a, b, x):
    """Continued fraction for the incomplete beta function (Numerical Recipes)."""
    MAXIT, EPS, FPMIN = 300, 3.0e-16, 1.0e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < EPS:
            break
    return h


def betai(a, b, x):
    """Regularised incomplete beta function I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
             + a * math.log(x) + b * math.log1p(-x))
    bt = math.exp(lbeta)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def t_sf(t, df):
    """Upper-tail survival function of Student's t with df degrees of freedom."""
    if df <= 0:
        return float("nan")
    x = df / (df + t * t)
    p = 0.5 * betai(df / 2.0, 0.5, x)   # one-tailed
    return p if t > 0 else 1.0 - p


def t_two_sided_p(t, df):
    """Two-sided p-value for a t statistic with df degrees of freedom."""
    return 2.0 * t_sf(abs(t), df)


def norm_two_sided_p(z):
    return 2.0 * norm_sf(abs(z))


# ---------- main ----------

def main():
    print("=" * 78)
    print("EDITOR VERIFICATION: MR-Egger p-value reference distribution")
    print("=" * 78)

    rows_checked = 0
    matches_normal = 0
    matches_t = 0
    unresolved = 0
    worst = []   # (file, gene, outcome, reported, p_norm, p_t, df)

    for fname in MR_FILES:
        path = os.path.join(RESULTS, fname)
        if not os.path.exists(path):
            print(f"\n[skip] {fname} not found")
            continue

        with open(path, newline="", encoding="utf-8", errors="replace") as fh:
            reader = csv.DictReader(fh)
            cols = reader.fieldnames or []
            print(f"\n--- {fname} ---")
            print(f"    columns: {cols}")

            for row in reader:
                method = " ".join(
                    str(row.get(k, "")) for k in cols
                    if any(s in k.lower() for s in ("method", "estimator", "estimand"))
                ).strip().lower()

                # locate the MR-Egger rows
                is_egger = "egger" in method
                if not is_egger:
                    # fall back: scan the whole row text
                    blob = " ".join(str(v) for v in row.values()).lower()
                    is_egger = "egger" in blob
                if not is_egger:
                    continue

                # --- pull beta / se / reported p / df ---
                def g(*names):
                    for n in names:
                        for k in cols:
                            if k.lower() == n.lower():
                                v = row.get(k)
                                if v not in (None, "", "NA", "NaN"):
                                    return v
                    return None

                beta = g("beta", "b", "estimate", "beta_egger")
                se = g("se", "std_err", "stderr", "se_egger", "SE")
                p_rep = g("pval", "p", "p_value", "pvalue", "Pval", "p.value")
                q_df = g("Q_df", "q_df", "df", "df_Q", "Q_df_egger")
                nsnp = g("nsnp", "n_snp", "nSNP", "n_instruments", "nsnps")

                try:
                    beta = float(beta)
                    se = float(se)
                    p_rep = float(p_rep)
                except (TypeError, ValueError):
                    unresolved += 1
                    continue

                if se == 0:
                    unresolved += 1
                    continue

                z = beta / se
                p_norm = norm_two_sided_p(z)

                # degrees of freedom for the Egger test = n_instruments - 2
                df = None
                for cand in (q_df, nsnp):
                    if cand is None:
                        continue
                    try:
                        cv = float(cand)
                    except (TypeError, ValueError):
                        continue
                    # Q_df is already n-2; nsnp needs -2 applied
                    if cand == q_df:
                        df = cv
                    else:
                        df = cv - 2.0
                    break

                if df is None or df <= 0:
                    p_t = float("nan")
                else:
                    p_t = t_two_sided_p(z, df)

                rows_checked += 1

                tol = 1e-9
                # compare on the log scale so tiny p-values are handled fairly
                def close(a, b):
                    if a <= 0 or b <= 0:
                        return abs(a - b) <= tol
                    return abs(math.log10(a) - math.log10(b)) <= 1e-6

                ok_norm = close(p_rep, p_norm)
                ok_t = (not math.isnan(p_t)) and close(p_rep, p_t)

                if ok_norm and not ok_t:
                    matches_normal += 1
                elif ok_t and not ok_norm:
                    matches_t += 1
                elif ok_norm and ok_t:
                    matches_normal += 1   # indistinguishable (df large)
                else:
                    unresolved += 1

                worst.append((fname, str(row.get(cols[0], "")), beta, se,
                              p_rep, p_norm, p_t, df))

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"MR-Egger rows checked      : {rows_checked}")
    print(f"consistent with NORMAL     : {matches_normal}")
    print(f"consistent with t(df=n-2)  : {matches_t}")
    print(f"neither / unresolved       : {unresolved}")
    print()

    if rows_checked == 0:
        print("No MR-Egger rows located -- cannot adjudicate.")
        return

    if matches_normal > 0 and matches_t == 0:
        print(">>> VERDICT: CONFIRMED. Egger p-values were computed on the")
        print(">>>          NORMAL distribution, not t(n-2). The claim holds.")
    elif matches_t > 0 and matches_normal == 0:
        print(">>> VERDICT: REFUTED. Egger p-values already use t(n-2).")
    else:
        print(">>> VERDICT: MIXED/AMBIGUOUS -- inspect the table below.")

    print("\n--- Egger rows: reported vs recomputed ---")
    print(f"{'file':<44}{'beta':>9}{'se':>9}{'reported':>13}"
          f"{'p_norm':>13}{'p_t':>12}{'df':>6}")
    for fname, key, beta, se, p_rep, p_norm, p_t, df in worst:
        ptxt = f"{p_t:.3g}" if not math.isnan(p_t) else "n/a"
        dft = f"{df:.0f}" if df is not None else "n/a"
        print(f"{fname[:43]:<44}{beta:>9.3f}{se:>9.3f}{p_rep:>13.3g}"
              f"{p_norm:>13.3g}{ptxt:>12}{dft:>6}")

    # spotlight the headline CD74 critical-care test
    print("\n--- headline CD74 critical-care Egger test ---")
    for fname, key, beta, se, p_rep, p_norm, p_t, df in worst:
        if "criticalcare" in fname.lower() and "cd74" in str(key).lower():
            print(f"  file={fname}  key={key}")
            print(f"  beta={beta}  se={se}  df={df}")
            print(f"  reported p = {p_rep:.6g}")
            print(f"  p (normal) = {p_norm:.6g}")
            print(f"  p (t, df={df}) = {p_t:.6g}")
            print(f"  --> ratio p_t / p_reported = {p_t / p_rep:.3g}")


if __name__ == "__main__":
    main()
