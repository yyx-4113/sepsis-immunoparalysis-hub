# -*- coding: utf-8 -*-
"""Patch: insert ref [20] correctly + compress abstract under 200 words."""
import io, os, re, sys

ROOT = r"D:\2026.9\极速交付9月会员日优惠套路\05_多组学+虚拟敲除药物发现\方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位"
P = os.path.join(ROOT, "05_reports", "manuscript.md")
s = io.open(P, encoding="utf-8").read()

# ---------- 1. insert ref [20] (previous pattern missed: author string is not "et al.") ----------
NEW_REF = ("20. Wang, C., Liu, J., Wu, Q. et al. The role of TIM-3 in sepsis: a promising target "
           "for immunotherapy? *Front. Immunol.* **15**, 1328667 (2024). doi:10.3389/fimmu.2024.1328667")
assert "20. Wang, C." not in s, "ref 20 already present"
assert "\n21. Schuemie, M. J., Ryan" in s, "anchor for insertion not found"
s = s.replace("\n21. Schuemie, M. J., Ryan", "\n" + NEW_REF + "\n21. Schuemie, M. J., Ryan", 1)
print("ref [20] inserted")

# ---------- 2. compress abstract ----------
i0 = s.find("Immunoparalysis, exemplified by the immunosuppressed Mars1 endotype,")
i1 = s.find("\n\n**Keywords:**", i0)
assert i0 > 0 and i1 > i0
NEW_ABS = (
 "Immunoparalysis, exemplified by the immunosuppressed Mars1 endotype, drives 28-day sepsis "
 "mortality, but actionable hubs and repositionable interventions remain limited. We re-analysed "
 "GSE65682 (802 samples) with an auditable multi-omics pipeline that confirms the Mars1 program and "
 "externally evaluates a prognostic signature. A consensus identified five immune hubs (CD74, "
 "HLA-DQA1, CD14, FCGR3A, HAVCR2/TIM-3) plus one non-immune passenger, FIS1 (logFC +1.26, "
 "up-regulated). A 30-gene immune-risk signature reached an external cross-platform AUC of 0.638 "
 "(95% CI 0.532\u20130.748; E-MTAB-4451, n = 106, 52 deaths); validation is independent in cohort and "
 "platform, though the score orientation was fixed on discovery 28-day outcomes. Within-cohort "
 "cross-validated AUC was 0.659 (optimistic). The external result is comparable to the published "
 "benchmark (0.619; a 3-gene proxy here, 0.529, is a weak reference). Seven immune-modulating "
 "agents were prioritised. Two-sample Mendelian randomisation gave no significant inverse-variance-"
 "weighted estimate on primary 28-day death (all OR 0.92\u20131.12, P \u2265 0.23); one sensitivity test "
 "(CD14 MR-Egger, OR 0.91, P = 0.049) was nominally significant and the single family-significant "
 "result (CD74 critical care, OR 2.19) ran opposite to the expression model. The contribution is a "
 "reproducible pipeline, an honest external validation and an experimental blueprint; repositioning "
 "and Mendelian randomisation remain hypothesis-generating."
)
old_abs = s[i0:i1]
s = s[:i0] + NEW_ABS + s[i1:]
print("abstract words: %d -> %d" % (len(old_abs.split()), len(NEW_ABS.split())))

io.open(P, "w", encoding="utf-8", newline="\n").write(s)

# ---------- post-checks ----------
print("\n--- post-checks ---")
m = re.search(r"## Abstract \(English\)\n\n(.+?)\n\n\*\*Keywords", s, re.S)
aw = len(m.group(1).split())
print("abstract words: %d -> %s" % (aw, "OK" if aw <= 200 else "FAIL"))
refs = s.split("\n1. Singer")[1]
rl = [l for l in refs.split("\n") if re.match(r"^\d+\. ", l)]
print("reference entries: %d" % len(rl))
nums = [int(re.match(r"^(\d+)\.", l).group(1)) for l in rl]
print("numbering contiguous 1..%d: %s" % (nums[-1], nums == list(range(1, len(nums) + 1))))
body = s.split("\n1. Singer")[0]
cited = sorted({int(x) for x in re.findall(r"\[(\d+)\]", body)})
print("in-text citations: %d distinct, max %d, all within range: %s"
      % (len(cited), max(cited), max(cited) <= nums[-1]))
missing = [n for n in range(1, nums[-1] + 1) if n not in cited]
print("references never cited in text: %s" % (missing if missing else "none"))
# first-appearance order
first = {}
for mm in re.finditer(r"\[(\d+)\]", body):
    first.setdefault(int(mm.group(1)), mm.start())
order = sorted(first, key=lambda n: first[n])
print("first-appearance order == numeric order: %s" % (order == sorted(order)))
print("ref[20] present: %s" % ("20. Wang, C." in s))
print("DOI trailing period in refs: %d" % len(re.findall(r"doi:\S+\.$", refs, re.M)))
