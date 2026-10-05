#!/usr/bin/env python3
# remove_mr_discussion.py - second pass: excise the surviving MR paragraph in
# the Discussion (L149) and re-verify reference integrity correctly.
import re

ROOT = r"D:\2026.9\极速交付9月会员日优惠套路\05_多组学+虚拟敲除药物发现\方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位"
SRC = ROOT + r"\05_reports\manuscript.md"
with open(SRC, encoding="utf-8") as f:
    text = f.read()

# Excise the surviving MR block in the Discussion paragraph.
before = text
text = re.sub(r" Germline causality is now tested.*?causal hub claim\.?", "", text, flags=re.DOTALL)
print("MR discussion block removed:", before != text)

# Re-verify references: every [n] in body must be a valid NEW reference number.
idx = text.index("## References")
body = text[:idx]
refs = text[idx:]
ref_lines = refs.split("\n")
new_numbers = set()
for rl in ref_lines:
    m = re.match(r"^(\d+)\. ", rl)
    if m:
        new_numbers.add(int(m.group(1)))
cited_in_body = set(int(x) for x in re.findall(r"\[(\d+)\]", body))
bad = sorted(cited_in_body - new_numbers)
print(f"valid new ref numbers = {min(new_numbers)}..{max(new_numbers)} (count {len(new_numbers)})")
print(f"citations in body pointing to non-existent ref number = {bad}")

# Remaining MR keyword hits (excluding the false-positive 'MR' inside other words)
mr_hits = re.findall(r"\bMR\b|Mendelian|mendelian|eQTL|IVW|Egger|pleiotrop|STROBE", text)
print(f"remaining MR keyword hits = {len(mr_hits)} -> {set(mr_hits)}")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(text)
print("WROTE", SRC)
