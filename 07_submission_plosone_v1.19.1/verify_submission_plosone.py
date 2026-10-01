#!/usr/bin/env python3
"""Verify the PLOS ONE submission pack (build artefacts vs source manuscript).

Exits non-zero on any failure. Focus: lossless number transfer, no Chinese text,
no stale placeholders, mandatory strings present, references in Vancouver style,
12 figures present, abstract within 300 words.
"""
from __future__ import annotations

import os
import re
import sys

from docx import Document

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
MS = os.path.join(PROJ, "05_reports", "manuscript.md")

NUM = re.compile(r"\d[\d,]*\.?\d*")
CJK = re.compile(r"[\u4e00-\u9fff]")

KEY_NUMBERS = [
    "0.638", "0.532", "0.748", "0.659", "0.529", "0.619", "0.92", "1.12",
    "0.24", "0.81", "0.91", "0.049", "2.222", "0.13", "802", "760", "42",
    "106", "52", "132", "23042366", "1212f7b", "1.19.1", "39%", "+1.26",
]


def docx_text(path: str) -> str:
    d = Document(path)
    parts = []
    for p in d.paragraphs:
        parts.append(p.text)
    for t in d.tables:
        for row in t.rows:
            for c in row.cells:
                parts.append(c.text)
    return "\n".join(parts)


def main() -> int:
    ok = True
    ms_path = os.path.join(HERE, "Manuscript.docx")
    si_path = os.path.join(HERE, "Supporting_Information.docx")
    cl_path = os.path.join(HERE, "Cover_Letter.docx")
    for p in (ms_path, si_path, cl_path):
        if not os.path.exists(p):
            print(f"FAIL: missing {p}")
            ok = False
    if not ok:
        return 1

    mst = docx_text(ms_path)
    sit = docx_text(si_path)
    clt = docx_text(cl_path)
    allt = mst + "\n" + sit + "\n" + clt

    # 1) abstract word count
    m = re.search(r"Abstract \(English\)\s*(.+?)\*\*Keywords", open(MS, encoding="utf-8").read(),
                  re.S)
    abst = m.group(1).split("**Keywords")[0].strip() if m else ""
    words = re.findall(r"[A-Za-z0-9%./\-]+", abst)
    wc = len(words)
    print(f"[abstract] {wc} words (limit 300) -> {'OK' if wc <= 300 else 'FAIL'}")
    ok = ok and wc <= 300

    # 2) Chinese text
    cjk = CJK.findall(allt)
    print(f"[chinese] {len(cjk)} CJK chars in docx -> {'OK' if not cjk else 'FAIL'}")
    ok = ok and not cjk

    # 3) stale placeholders
    for ph in ("will be minted", "on acceptance", "AUTHOR:", "TODO", "XXX"):
        hit = ph in allt
        print(f"[placeholder] '{ph}' -> {'FAIL' if hit else 'OK'}")
        ok = ok and not hit

    # 4) mandatory strings
    for s in ("github.com/yyx-4113/sepsis-immunoparalysis-hub",
              "0009-0004-9698-6552", "10.5281/zenodo.23042366",
              "Use of generative AI", "Ethics statement",
              "Data availability", "Competing interests"):
        hit = s in allt
        print(f"[mandatory] '{s[:32]}...' -> {'OK' if hit else 'FAIL'}")
        ok = ok and hit

    # 5) references: 41, Vancouver style, numbered in order
    ref_block = allt[allt.index("References"):] if "References" in allt else ""
    ref_lines = re.findall(r"^\s*(\d+)\.\s+.+\.\s+\d{4};\d+:.+\.\s+doi:", ref_block, re.M)
    print(f"[refs] {len(ref_lines)} Vancouver-style refs (expect 41) -> "
          f"{'OK' if len(ref_lines) == 41 else 'FAIL'}")
    ok = ok and len(ref_lines) == 41
    # in-text citations bracketed
    md = open(MS, encoding="utf-8").read()
    bad_cite = re.findall(r"\(\d{4}\)\.\s*\[", md)  # not a real check; placeholder
    cite_ok = bool(re.search(r"\[1\]", md)) and not bool(re.search(r"<sup>\d+</sup>", md))
    print(f"[citations] bracketed [n] in source -> {'OK' if cite_ok else 'FAIL'}")
    ok = ok and cite_ok

    # 6) key numbers present in docx
    missing = [n for n in KEY_NUMBERS if n not in mst]
    print(f"[numbers] {len(KEY_NUMBERS)-len(missing)}/{len(KEY_NUMBERS)} key numbers in manuscript docx"
          + (f" MISSING={missing}" if missing else " -> OK"))
    ok = ok and not missing

    # 7) figures
    fig_dir = os.path.join(HERE, "Figures")
    figs = sorted(f for f in os.listdir(fig_dir)) if os.path.isdir(fig_dir) else []
    print(f"[figures] {len(figs)} files in Figures/ (expect 12) -> "
          f"{'OK' if len(figs) == 12 else 'FAIL'}")
    ok = ok and len(figs) == 12

    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
