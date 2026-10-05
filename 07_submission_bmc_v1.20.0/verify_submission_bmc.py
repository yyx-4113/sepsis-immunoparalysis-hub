#!/usr/bin/env python3
"""Verify the BMC Medical Genomics submission pack (v1.20.0) integrity.

Checks:
  1. No Chinese (CJK) characters in the built Manuscript.docx.
  2. No unfilled placeholders (TODO / TBD / Lorem / <<...>> / [file not found]).
  3. Mandatory strings present: repo URL, ORCID, Zenodo DOI, structured-abstract
     headers, BMC Declarations headings, generative-AI disclosure, version tag.
  4. Key numeric tokens preserved (no silent drift vs manuscript.md).
  5. No MR-layer residue (Mendelian / STROBE-MR / TwoSampleMR / IVW / Egger / etc.).
  6. Exactly 36 Vancouver references and 10 copied figure PNGs.
Exits non-zero on any failure.
"""
from __future__ import annotations

import os
import re

from docx import Document

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
MS_DOCX = os.path.join(HERE, "Manuscript.docx")
MS_MD = os.path.join(PROJ, "05_reports", "manuscript.md")
FIG_DIR = os.path.join(HERE, "Figures")

MANDATORY = [
    ("repo URL", "github.com/yyx-4113/sepsis-immunoparalysis-hub"),
    ("ORCID", "0009-0004-9698-6552"),
    ("Zenodo DOI", "10.5281/zenodo.23042366"),
    ("version tag", "v1.20.0"),
    ("abstract Background", "Background:"),
    ("abstract Methods", "Methods:"),
    ("abstract Results", "Results:"),
    ("abstract Conclusions", "Conclusions:"),
    ("Declarations heading", "Declarations"),
    ("Ethics+consent heading", "Ethics approval and consent to participate"),
    ("Consent for publication", "Consent for publication"),
    ("Data availability", "Data availability"),
    ("Code availability", "Code availability"),
    ("Author contributions", "Author contributions"),
    ("Funding", "Funding"),
    ("Competing interests", "Competing interests"),
    ("GenAI disclosure", "Use of generative AI"),
]

# numeric tokens that must appear verbatim in the built manuscript
KEY_NUMBERS = [
    "802", "760", "42", "0.638", "0.532", "0.748", "0.585", "0.659",
    "0.529", "0.619", "106", "52", "30", "FIS1", "1.26", "+1.26",
]

MR_RESIDUE = [
    r"(?i)mendelian", r"strobe-mr", r"twosamplemr", r"openGWAS", r"mr-base",
    r"instrumental variable", r"\bivw\b", r"\begger\b", r"genetic causality",
    r"germline", r"\bmr\b(?!\s*[-:])", r"two-sample",
]

PLACEHOLDERS = [r"\bTODO\b", r"\bTBD\b", r"\bLorem\b", r"<<[^>]+>>", r"\[file not found",
                r"\bXXX\b", r"\bplaceholder\b", r"\bFIXME\b"]


def docx_text(path: str) -> str:
    doc = Document(path)
    parts = []
    for p in doc.paragraphs:
        parts.append(p.text)
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                parts.append(c.text)
    return "\n".join(parts)


def main() -> int:
    fails = []

    text = docx_text(MS_DOCX)

    # 1. CJK
    cjk = re.findall(r"[\u4e00-\u9fff]", text)
    if cjk:
        fails.append(f"Chinese text present: {sorted(set(cjk))[:10]}")

    # 2. placeholders
    for pat in PLACEHOLDERS:
        if re.search(pat, text, flags=re.I):
            fails.append(f"placeholder matched: {pat}")

    # 3. mandatory strings
    for label, s in MANDATORY:
        if s not in text:
            fails.append(f"missing mandatory string [{label}]: {s!r}")

    # 4. key numbers
    for n in KEY_NUMBERS:
        if n not in text:
            fails.append(f"missing key number/token: {n!r}")

    # 5. MR residue
    for pat in MR_RESIDUE:
        if re.search(pat, text):
            m = re.search(pat, text)
            fails.append(f"MR residue matched: {pat} -> {m.group(0)!r}")

    # 6a. reference count (Vancouver: lines like "N. Authors. Title. Journal. Year;vol:pages.")
    ref_block = text[text.find("References"):] if "References" in text else ""
    ref_n = len(re.findall(r"^\s*\d+\.\s+\S", ref_block, flags=re.M))
    if ref_n != 36:
        fails.append(f"reference count = {ref_n}, expected 36")

    # 6b. figures copied
    figs = sorted(f for f in os.listdir(FIG_DIR) if f.lower().endswith(".png")) if os.path.isdir(FIG_DIR) else []
    if len(figs) != 10:
        fails.append(f"figure PNGs copied = {len(figs)}, expected 10 (got {figs})")

    # cross-check: manuscript.md itself has no MR residue either
    md = open(MS_MD, encoding="utf-8").read()
    for pat in MR_RESIDUE:
        if re.search(pat, md):
            fails.append(f"MR residue in source manuscript.md: {pat}")

    print("=== BMC submission verification ===")
    print(f"docx chars={len(text)} refs={ref_n} figs={len(figs)}")
    if fails:
        print("\nFAILURES:")
        for f in fails:
            print("  -", f)
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
