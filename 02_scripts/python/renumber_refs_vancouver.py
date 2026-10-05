#!/usr/bin/env python3
"""Renumber manuscript references to strict Vancouver first-appearance order.

The manuscript historically cited references thematically (e.g. mHLA-DR monitoring
refs at §3.2, calibration refs at §3.4), so the in-text citation numbers were not in
first-appearance order. BMC/Vancouver requires the reference list to be numbered in
the order each work is first cited. This script:
  1. finds the first appearance position of every [N] citation in the body,
  2. assigns new numbers = position in first-appearance order,
  3. rewrites every in-text [N] -> [new], and
  4. reorders + renumbers the reference list to match.
No reference *content* is changed; only numbers and ordering.
"""
import re
import sys

PATH = "05_reports/mancript.md" if False else "05_reports/manuscript.md"

with open(PATH, encoding="utf-8") as f:
    txt = f.read()

if "## References" not in txt:
    sys.exit("References section not found")

body, refs_raw = txt.split("## References", 1)

# 1) first appearance of each citation number
firstpos = {}
for m in re.finditer(r"\[(\d+)\]", body):
    n = int(m.group(1))
    firstpos.setdefault(n, m.start())

ordered = sorted(firstpos, key=lambda n: firstpos[n])   # old numbers in appearance order
remap = {old: new for new, old in enumerate(ordered, start=1)}

# 2) rewrite in-text citations in the body
def repl(m):
    n = int(m.group(1))
    return "[%d]" % remap[n] if n in remap else m.group(0)

new_body = re.sub(r"\[(\d+)\]", repl, body)

# 3) parse + reorder + renumber the reference list
ref_items = re.findall(r"^(\d+)\.\s+(.*)$", refs_raw, re.M)
if len(ref_items) != len(remap):
    sys.exit("Reference-list count (%d) != citation count (%d); aborting" % (len(ref_items), len(remap)))
by_old = {int(num): text for num, text in ref_items}
new_ref_lines = []
for new in range(1, len(remap) + 1):
    old = ordered[new - 1]
    new_ref_lines.append("%d. %s" % (new, by_old[old]))

new_txt = new_body + "## References\n" + "\n".join(new_ref_lines) + "\n"

with open(PATH, "w", encoding="utf-8") as f:
    f.write(new_txt)

# report
print("Renumbering complete: %d references." % len(remap))
print("Spot-check (new number -> first cited work):")
for new, old in enumerate(ordered, start=1):
    if new <= 3 or new >= len(ordered) - 2:
        print("  [%d] was [%d]" % (new, old))
