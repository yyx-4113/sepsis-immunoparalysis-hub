#!/usr/bin/env python3
# remove_mr_layer.py
# One-shot transformation for sepsis-immunoparalysis-hub v1.19.1 -> v1.20.0.
# PLOS ONE desk-rejected the MR layer on methodological grounds; MR was Tier-3,
# fully null, not in the title, and not a core contribution, so it is removed
# entirely and the paper is reframed as a computational methods + signature
# validation + drug-repositioning blueprint report.
import re, sys

ROOT = r"D:\2026.9\极速交付9月会员日优惠套路\05_多组学+虚拟敲除药物发现\方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位"
SRC = ROOT + r"\05_reports\manuscript.md"

with open(SRC, encoding="utf-8") as f:
    text = f.read()
orig = text

# ---- 1. small prose replacements ----
text = re.sub(r", and the Mendelian-randomisation layer is hypothesis-generating\.?", ".", text)
text = re.sub(r"Two-sample Mendelian randomisation showed no significant.*?and an experimental blueprint\.",
              "The contribution is a reproducible pipeline, an honest external validation and an experimental blueprint.",
              text, flags=re.DOTALL)
text = text.replace(
    "is retained in MR for completeness, and is explicitly not treated as an immune hub or as a mechanistic target.",
    "and is explicitly not treated as an immune hub or as a mechanistic target.")
text = text.replace("(tag v1.19.1)", "(tag v1.20.0)").replace("this v1.19.1 release", "this v1.20.0 release")
text = re.sub(r" The OpenGWAS API server certificate was expired at the time of the cited MR run, so certificate verification was disabled for that request \(see `10_genetics_mr_run\.py`\); all MR outputs are deposited, so re-running is optional\.", "", text)
text = text.replace("(citable GitHub release, tag v1.19.1;", "(citable GitHub release, tag v1.20.0;")
text = text.replace("GEOparse, limma, TwoSampleMR, the IEU OpenGWAS platform and the LINCS L1000 resource",
                    "GEOparse, limma and the LINCS L1000 resource")

# ---- 2. structural deletions + renumbering (line based) ----
lines = text.split("\n")
out = []
skip = None
in5 = False
counter = 0
for ln in lines:
    if ln.startswith("### 2.10 Genetic validation"):
        skip = "mr2"; continue
    if skip == "mr2":
        if ln.startswith("### 2.11 Experimental validation blueprint"):
            out.append("### 2.10 Experimental validation blueprint (S11)"); skip = None; continue
        continue
    if ln.startswith("### 2.12 Use of generative AI"):
        out.append("### 2.11 Use of generative AI"); continue
    if ln.startswith("### 3.10 Two-sample Mendelian"):
        skip = "mr3"; continue
    if skip == "mr3":
        if ln.startswith("## 4. Discussion"):
            out.append("---"); out.append(""); out.append(ln); skip = None; continue
        continue
    if ln.startswith("## 5. Limitations"):
        in5 = True; counter = 0; out.append(ln); continue
    if ln.startswith("## 6. Conclusion"):
        in5 = False; out.append(ln); continue
    if in5:
        if ln.startswith("2. **Genetic causality") or ln.startswith("12. **Mendelian-randomisation") or ln.startswith("13. **STROBE-MR"):
            continue
        m = re.match(r"^(\d+)\. ", ln)
        if m:
            counter += 1
            out.append(re.sub(r"^\d+\. ", f"{counter}. ", ln, count=1)); continue
        out.append(ln); continue
    out.append(ln)
text = "\n".join(out)

# ---- 3. §7 MR rows + §8 MR mentions ----
text = "\n".join(l for l in text.split("\n") if ("S10 genetic MR" not in l) and ("| S12 STROBE-MR" not in l))
text = text.replace(
    " S10 — two-sample MR inputs, per-outcome and family-BH outputs, harmonised instrument tables, and design log. S11 — experimental validation blueprint (LPS-tolerance / patient-cell assays). S12 — STROBE-MR checklist.",
    " S11 — experimental validation blueprint (LPS-tolerance / patient-cell assays).")
text = text.replace(
    ", and the two MR diagnostic figures — `mr_forest.png` (15-test forest) and `mr_diag.png`, a four-panel overlay comprising the CD14 28-day-death scatter with IVW/Egger fits, the CD14 Egger funnel, the CD14 leave-one-out analysis, and the CD74 critical-care scatter.",
    "")

# ---- 4. reference cleanup: drop uncited, renumber ----
idx = text.index("## References")
body = text[:idx]
refs = text[idx:]
cited = set(int(x) for x in re.findall(r"\[(\d+)\]", body))
ref_lines = refs.split("\n")
entries = {}
order = []
for rl in ref_lines:
    mm = re.match(r"^(\d+)\. ", rl)
    if mm:
        num = int(mm.group(1)); entries[num] = rl; order.append(num)
kept = sorted(n for n in order if n in cited)
newnum = {old: i + 1 for i, old in enumerate(kept)}

def repl(m):
    n = int(m.group(1))
    return f"[{newnum[n]}]" if n in newnum else m.group(0)
body2 = re.sub(r"\[(\d+)\]", repl, body)

newref_lines = []
for rl in ref_lines:
    mm = re.match(r"^(\d+)\. ", rl)
    if mm:
        num = int(mm.group(1))
        if num in newnum:
            rest = rl[rl.index(". ") + 2:]
            newref_lines.append(f"{newnum[num]}. {rest}")
    else:
        newref_lines.append(rl)
text = body2 + "\n".join(newref_lines)

# ---- 5. verification ----
dropped = [n for n in order if n not in kept]
remaining_mr = len(re.findall(r"\bMR\b|Mendelian|mendelian|eQTL|IVW|Egger|pleiotrop|STROBE", text))
dangling = re.findall(r"\[(\d+)\]", body2)
dangling_bad = [d for d in set(int(x) for x in dangling) if d not in newnum]
print(f"refs before={len(order)} after={len(kept)} dropped={dropped}")
print(f"remaining MR keyword hits in full text = {remaining_mr}")
print(f"dangling citations (cited number not in new ref map) = {sorted(dangling_bad)}")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(text)
print("WROTE", SRC)
