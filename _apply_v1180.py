# -*- coding: utf-8 -*-
"""Round-17 mandatory revisions: v1.17.0 -> v1.18.0."""
import io, os, re, sys

ROOT = r"D:\2026.9\极速交付9月会员日优惠套路\05_多组学+虚拟敲除药物发现\方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位"
P = os.path.join(ROOT, "05_reports", "manuscript.md")
s = io.open(P, encoding="utf-8").read()
orig = s

report = []
fail = []

def sub(old, new, label, expect=1):
    """Replace; expect = required occurrence count (None = any)."""
    global s
    n = s.count(old)
    if n == 0:
        fail.append("%s -- PATTERN NOT FOUND" % label)
        return
    if expect is not None and n != expect:
        fail.append("%s -- expected %d occurrence(s), found %d" % (label, expect, n))
        return
    s = s.replace(old, new)
    report.append("%-26s OK (%d)" % (label, n))

# ══════════════════════════════════════════════════════════════
# STEP A — Table renumbering (T2.3): unnumbered 3.2 table -> Table 2
#          old Table 2->3, 3->4, 4->5.  Do this FIRST so later
#          replacements can cite the new numbers directly.
# ══════════════════════════════════════════════════════════════
for old, new in [("Table 4", "Table 5"), ("Table 3", "Table 4"), ("Table 2", "Table 3")]:
    n = s.count(old)
    s = s.replace(old, new)
    report.append("%-26s OK (%d)" % ("renumber %s->%s" % (old, new), n))
sub("*Table: Immune-function score by MARS endotype (median; Mann–Whitney U vs Mars1).*",
    "*Table 2. Immune-function score by MARS endotype (median; Mann–Whitney U vs Mars1).*",
    "T2.3 caption -> Table 2")

# ══════════════════════════════════════════════════════════════
# STEP B — Reference renumbering: insert new ref [20] for the
#          sepsis TIM-3 literature; old [20]..[37] -> [21]..[38].
# ══════════════════════════════════════════════════════════════
lines = s.split("\n")
rstart = next(i for i, l in enumerate(lines) if l.startswith("1. Singer"))
head, tail = "\n".join(lines[:rstart]), "\n".join(lines[rstart:])
for n in range(37, 19, -1):                      # 37 -> 38 ... 20 -> 21
    head = re.sub(r"\[%d\]" % n, "[%d]" % (n + 1), head)
    tail = re.sub(r"^%d\. " % n, "%d. " % (n + 1), tail, flags=re.M)
report.append("%-26s OK" % "B ref renumber 20-37 -> 21-38")

NEW_REF = ("20. Wang, C., Liu, J., Wu, Q. et al. The role of TIM-3 in sepsis: a promising target "
           "for immunotherapy? *Front. Immunol.* **15**, 1328667 (2024). doi:10.3389/fimmu.2024.1328667")
assert "\n21. Schuemie" in "\n" + tail
tail = tail.replace("21. Schuemie, M. J. et al.", NEW_REF + "\n21. Schuemie, M. J. et al.", 1)
report.append("%-26s OK" % "B insert ref [20]")
s = head + "\n" + tail

# ══════════════════════════════════════════════════════════════
# T1.1 — FIS1 must not be grouped as 'concordant with the
#        immunoparalysis model' (4 sites)
# ══════════════════════════════════════════════════════════════
sub("three of the five assessable hubs (HLA-DQA1, CD14, FIS1) returned protective estimates "
    "concordant across all three methods (Table 4), the direction predicted by the immunoparalysis model",
    "two of the four assessable immune hubs (HLA-DQA1, CD14) returned protective estimates "
    "concordant across all three methods (Table 4) — the direction predicted by the immunoparalysis "
    "model for the down-regulated hubs. FIS1 also returned a protective point estimate, but because "
    "FIS1 is *up*-regulated in Mars1 (logFC +1.26; \u00a73.3) that direction is opposite to its own "
    "observational association; FIS1 is therefore reported as a passenger-gene observation rather "
    "than as model-concordant, and it is not counted among the concordant hubs",
    "T1.1a s3.10")

sub("On the phenotype-matched primary outcome (28-day death), three of five assessable hubs "
    "(HLA-DQA1, CD14, FIS1) give concordant protective estimates, but no test crosses the corrected "
    "family threshold",
    "On the phenotype-matched primary outcome (28-day death), two of the four assessable immune hubs "
    "(HLA-DQA1, CD14) give concordant protective estimates, but no test crosses the corrected family "
    "threshold; FIS1 gives a protective estimate too, but as an up-regulated non-immune passenger "
    "its direction is not predicted by the immunoparalysis model and it is not counted here",
    "T1.1b s3.10 tail")

sub("returned directionally protective estimates concordant across IVW, MR-Egger and the weighted "
    "median for three of five assessable hubs (HLA-DQA1, CD14, FIS1)",
    "returned directionally protective estimates concordant across IVW, MR-Egger and the weighted "
    "median for two of the four assessable immune hubs (HLA-DQA1, CD14). FIS1 returned a protective "
    "estimate as well, but as an up-regulated non-immune passenger its direction is not predicted by "
    "the immunoparalysis model, so it is reported descriptively rather than as concordant",
    "T1.1c s4")

sub("three of five assessable hubs (HLA-DQA1, CD14, FIS1) gave protective estimates concordant "
    "across IVW, MR-Egger and the weighted median",
    "two of the four assessable immune hubs (HLA-DQA1, CD14) gave protective estimates concordant "
    "across IVW, MR-Egger and the weighted median; FIS1 also gave a protective estimate, but as an "
    "up-regulated non-immune passenger its direction is not predicted by the immunoparalysis model "
    "and is reported descriptively",
    "T1.1d limitation 2")

# ══════════════════════════════════════════════════════════════
# T1.2 + T1.3 — DCA: formula artefact + test-set-nested calibration
# ══════════════════════════════════════════════════════════════
sub("because treat-all becomes increasingly harmful at higher thresholds (external prevalence 0.49), "
    "the model's net-benefit advantage over treat-all widens rather than converges (at threshold 0.80 "
    "the model NB is 0.00 while treat-all NB is \u22121.55);",
    "the model's advantage over treat-all is confined to a window: net benefit is higher by only "
    "0.01\u20130.09 across thresholds 0.30\u20130.50 and by 0.17\u20131.05 across 0.55\u20130.75, where the "
    "treat-all net benefit collapses toward \u2212\u221e as the threshold approaches 1 \u2014 an algebraic "
    "property of the treat-all strategy at this prevalence (0.49) rather than evidence of model gain. "
    "At thresholds \u22650.80 the model's own net benefit is 0.00, identical to the treat-none baseline, "
    "because no calibration-corrected predicted risk exceeds the threshold (model NB 0.00 versus "
    "treat-all \u22121.55 at threshold 0.80);",
    "T1.2 DCA window")

sub("the decision-curve analysis — computed on the calibration-corrected probabilities from the "
    "external logistic fit (intercept \u22120.04, slope 0.50) —",
    "the decision-curve analysis — computed on the calibration-corrected probabilities from the "
    "external logistic fit (intercept \u22120.04, slope 0.50), which was itself fitted on the same "
    "106-sample E-MTAB-4451 set used for validation and is therefore optimistically biased and "
    "reported as illustrative (no bootstrap optimism correction was applied, and with 52 events the "
    "slope is itself imprecise) —",
    "T1.3 calibration nesting")

# ══════════════════════════════════════════════════════════════
# T1.4 — L1000: demote the two small molecules from supportive to
#        descriptive-only (prednisone refutes the axis)
# ══════════════════════════════════════════════════════════════
sub("The repositioning shortlist is now connectivity-scored on LINCS L1000 (\u00a73.9): the two small "
    "molecules, lenalidomide (top 26.6%) and azithromycin (\u2248 median), are directionally positive "
    "but modest, and the glucocorticoid positive-control caveat warns that transcriptional rescue is "
    "not functional rescue.",
    "The repositioning shortlist is now connectivity-scored on LINCS L1000 (\u00a73.9): the two small "
    "molecules, lenalidomide (top 26.6%) and azithromycin (\u2248 median), are directionally positive "
    "but modest. Because prednisone \u2014 a clinical immunosuppressant \u2014 scores in the 3.2nd percentile "
    "on the same axis, the L1000 rescue proxy is treated here as **descriptive only** for both "
    "compounds and is not counted as supportive evidence for the shortlist: a metric that ranks an "
    "immunosuppressant in the top 3% cannot simultaneously corroborate two immunomodulators.",
    "T1.4a s4 L1000")

sub("their small-molecule counterparts lenalidomide and azithromycin show directional-but-modest "
    "LINCS L1000 rescue of the Mars1-down axis, with functional validation (S11) still required.",
    "their small-molecule counterparts lenalidomide and azithromycin show directional-but-modest "
    "LINCS L1000 rescue of the Mars1-down axis; because the same axis ranks prednisone in the 3.2nd "
    "percentile, that ranking is descriptive only and not supportive evidence, and functional "
    "validation (S11) remains required.",
    "T1.4b s6 L1000")

# ══════════════════════════════════════════════════════════════
# T1.5 + T1.6 + T2.7 — Abstract rewritten (MR nuance, label
#        dependence, word count kept safely under 200)
# ══════════════════════════════════════════════════════════════
OLD_ABS_START = "Immunoparalysis, exemplified by the immunosuppressed Mars1 endotype,"
i0 = s.find(OLD_ABS_START)
i1 = s.find("\n\n**Keywords:**", i0)
assert i0 > 0 and i1 > i0, "abstract bounds not found"
NEW_ABS = (
 "Immunoparalysis, exemplified by the immunosuppressed Mars1 endotype, drives 28-day sepsis "
 "mortality, but actionable hubs and repositionable interventions remain limited. We re-analysed the "
 "public GSE65682 cohort (802 samples) and built an auditable multi-omics pipeline that confirms the "
 "Mars1 program and externally evaluates a prognostic signature. A consensus identified five immune "
 "hubs (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2/TIM-3) plus one non-immune passenger, FIS1 (logFC "
 "+1.26, up-regulated). A 30-gene immune-risk signature reached an external, cross-platform AUC of "
 "0.638 (95% CI 0.532\u20130.748; E-MTAB-4451, n = 106, 52 deaths); this validation is independent in "
 "cohort and platform but not in label, the score orientation having been fixed on the discovery "
 "cohort's 28-day outcomes. The within-cohort cross-validated AUC was 0.659 (optimistic). The "
 "external result is comparable to the published benchmark (0.619; a 3-gene proxy recomputed here, "
 "0.529, is a weak reference). Seven immune-modulating agents were prioritised. Two-sample Mendelian "
 "randomisation gave no significant inverse-variance-weighted estimate on primary 28-day death (all "
 "OR 0.92\u20131.12, P \u2265 0.23); one pleiotropy-robust sensitivity test (CD14 MR-Egger, OR 0.91, "
 "P = 0.049) was nominally significant and the single family-significant result (CD74 critical care, "
 "OR 2.19) ran opposite to the expression model. The contribution is a reproducible pipeline, an "
 "honest external validation and an experimental blueprint; the repositioning and Mendelian-"
 "randomisation layers remain hypothesis-generating."
)
s = s[:i0] + NEW_ABS + s[i1:]
report.append("%-26s OK (%d words)" % ("T1.5/1.6/2.7 abstract", len(NEW_ABS.split())))

# ══════════════════════════════════════════════════════════════
# T1.6 — qualify 'independent' at the remaining headline sites
# ══════════════════════════════════════════════════════════════
sub("an honest independent external validation",
    "an honest external validation that is independent in cohort and platform but not in label "
    "(the score orientation was fixed on the discovery cohort's 28-day outcomes)",
    "T1.6a article type")
sub("### 3.5 External, independent validation on E-MTAB-4451",
    "### 3.5 External validation on E-MTAB-4451 (independent in cohort and platform, not in label)",
    "T1.6b s3.5 heading")
sub("an honest independent cross-platform external validation",
    "an honest external validation on a cross-platform cohort that is independent in cohort and "
    "platform but not in label",
    "T1.6c s4")

# ══════════════════════════════════════════════════════════════
# T1.7 + T1.8 — checkpoint engagement downgraded; sepsis TIM-3
#        literature cited and reconciled (new ref [20])
# ══════════════════════════════════════════════════════════════
sub("PD-1/TIM-3 co-expression more broadly characterises exhausted T cells, whereas the present "
    "Mars1 program shows down-regulated HAVCR2/TIM-3 (reduced checkpoint engagement) rather than the "
    "canonical TIM-3-up exhaustion signature.",
    "PD-1/TIM-3 co-expression more broadly characterises exhausted T cells, and several sepsis "
    "studies report TIM-3 up-regulation on circulating T cells in association with severity [20]. "
    "The present Mars1 program instead shows net lower *bulk* HAVCR2/TIM-3 expression, which is "
    "compatible with \u2014 but does not by itself establish \u2014 reduced per-cell checkpoint engagement, "
    "because a bulk measurement cannot separate lower T-cell/APC abundance from lower per-cell "
    "TIM-3. Bulk TIM-3 down-regulation is not unprecedented in sepsis: lower TIM-3 mRNA in peripheral "
    "blood mononuclear cells has been reported in severe sepsis relative to sepsis [20]. The present "
    "result is therefore a cohort-specific net-expression observation, not a refutation of the "
    "TIM-3-up exhaustion literature [20].",
    "T1.7a s3.1 checkpoint")

sub("also down-regulated, which is more consistent with reduced checkpoint engagement in the "
    "immunosuppressed program than with the TIM-3 up-regulation that typifies exhausted T cells;",
    "also down-regulated \u2014 more consistent with net lower bulk TIM-3 transcript levels, of "
    "uncertain cellular basis (reduced cell abundance versus lower per-cell expression, \u00a73.1), "
    "than with the TIM-3 up-regulation that typifies exhausted T cells [20]; the two are reconciled "
    "by the bulk-abundance explanation above rather than by a claim of reduced per-cell engagement;",
    "T1.7b s4 checkpoint")

# ══════════════════════════════════════════════════════════════
# Tier-2 wording / format items
# ══════════════════════════════════════════════════════════════
sub("doi:10.1001/jama.2025.24175.", "doi:10.1001/jama.2025.24175", "T2.1 ref trailing period")

sub("the correction is therefore a conservative approximation rather than a strict independence guarantee.",
    "the correction is therefore a dependence-ignoring approximation rather than a strict independence "
    "guarantee (it does not adjust for the overlapping hypothesis structures induced by re-using the "
    "same instruments across estimators and outcomes).",
    "T2.4 BH wording")

sub("and the MR diagnostic set (forest, scatter, funnel, leave-one-out).",
    "and the two MR diagnostic figures \u2014 `mr_forest.png` (45-test forest) and `mr_diag.png`, a "
    "four-panel overlay comprising the CD14 28-day-death scatter with IVW/Egger fits, the CD14 Egger "
    "funnel, the CD14 leave-one-out analysis, and the CD74 critical-care scatter.",
    "T2.5 s8 figure index")

sub("below the \\|logFC\\|\u22650.3 DEG fold-change threshold, DEG_0.3=False",
    "below the `|logFC| \u2265 0.3` DEG fold-change threshold, DEG_0.3=False",
    "T2.6 Table 1 escaped pipe")

# Data availability: version tag -> v1.18.0
sub("(tag v1.17.0)", "(tag v1.18.0)", "version tag DA")
sub("and this v1.17.0 release is built on top of it",
    "and this v1.18.0 release is built on top of it", "version tag DA-2")

# T2.2 — standalone Code availability heading (Sci Rep expects one)
sub("## Ethics statement",
    "## Code availability\n\nAnalysis code is released under the MIT licence in the versioned "
    "repository at https://github.com/yyx-4113/sepsis-immunoparalysis-hub (citable GitHub release, "
    "tag v1.18.0; CITATION.cff included).\n\n## Ethics statement",
    "T2.2 Code availability")

# ══════════════════════════════════════════════════════════════
# Write + self-checks
# ══════════════════════════════════════════════════════════════
if fail:
    print("FAILED ITEMS:")
    for f in fail:
        print("  -", f)
    print("\nAborting; nothing written.")
    sys.exit(1)

io.open(P, "w", encoding="utf-8", newline="\n").write(s)

print("Applied %d replacement groups:" % len([r for r in report]))
for r in report:
    print("  ", r)

# --- post-conditions ---
print("\n--- post-checks ---")
abs_m = re.search(r"## Abstract \(English\)\n\n(.+?)\n\n\*\*Keywords", s, re.S)
aw = len(abs_m.group(1).split()) if abs_m else -1
print("abstract words: %d (cap 200) -> %s" % (aw, "OK" if 0 < aw <= 200 else "FAIL"))
print("refs in list:", len(re.findall(r"^\d+\. ", s, re.M)))
print("max in-text citation:", max(int(x) for x in re.findall(r"\[(\d+)\]", s.split("\n1. Singer")[0])))
print("'reduced checkpoint engagement' (bare claim) count:",
      s.count("reduced checkpoint engagement") - s.count("reduced per-cell checkpoint engagement"))
for bad in ["three of the five assessable hubs", "three of five assessable hubs",
            "widens rather than converges", "v1.17.0"]:
    print("residual %-38s : %d" % (bad, s.count(bad)))
print("new ref [20] present:", "20. Wang, C." in s)
print("code availability heading:", s.count("\n## Code availability"))
print("bytes: %d -> %d" % (len(orig), len(s)))
