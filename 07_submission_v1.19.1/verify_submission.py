#!/usr/bin/env python3
"""Verify the Scientific Reports submission pack lost nothing in conversion.

Exit 0 = pass. Checks (in order of catch-rate):
  1. numeric-token set difference (markdown -> docx), both directions
  2. no Chinese text in any submitted file
  3. mandatory strings survive (repo URL, ORCID, AI-disclosure sentence)
  4. expected table counts (manuscript = GFM tables in body; SI = CSV-backed tables)
  5. no placeholders ([[, TODO, TBD, XXX, COMPLETE BEFORE SUBMISSION)
  6. 12 supplementary figures embedded in the SI + 12 PNGs in Figures/
"""
from __future__ import annotations

import os
import re
import sys

from docx import Document

import build_submission as B

HERE = B.HERE
NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")


def tokens(text: str) -> set[str]:
    # strip commas so thousands separators / gene-list commas don't read as mismatches
    return set(t.replace(",", "") for t in NUM.findall(text.replace("`", "")))


OK, BAD = [], []


def chk(label, got, exp=True):
    (OK if got == exp else BAD).append(f"{label}: got={got!r} exp={exp!r}")


def docx_text(path: str) -> str:
    d = Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                parts.append(c.text)
    return "\n".join(parts)


def docx_table_count(path: str) -> int:
    return len(Document(path).tables)


def main() -> int:
    ms = os.path.join(HERE, "Manuscript.docx")
    si = os.path.join(HERE, "Supporting_Information.docx")
    cl = os.path.join(HERE, "Cover_Letter.docx")
    rs = os.path.join(HERE, "Reporting_Summary.docx")
    figdir = B.FIG_OUT
    for p in (ms, si, cl, rs):
        chk(f"exists {os.path.basename(p)}", os.path.exists(p))

    # exported markdown, reconstructed exactly as the build did (strip figs in body_pre only)
    text = open(B.MS, encoding="utf-8").read()
    sec = B.split_sections(text)
    md_exported = "\n".join([
        sec["title"], sec["abstract"],
        B.strip_fig_refs(sec["body_pre"]),
        sec["si_index"], sec["decl"], sec["refs"],
    ])
    ms_text = docx_text(ms)
    si_text = docx_text(si)
    cl_text = docx_text(cl)

    # 1. numeric tokens
    a, b = tokens(md_exported), tokens(ms_text)
    chk("[Manuscript] no lost numbers", sorted(a - b), [])
    chk("[Manuscript] no invented numbers", sorted(b - a), [])

    # expected SI tables = CSV-backed files small enough to embed
    si_expected = B.si_expected_tables()
    chk("[Supporting] table count matches CSVs", docx_table_count(si), si_expected)

    # manuscript tables = GFM tables in body_pre (Tables 1-5 + §7 provenance)
    body_tables = sum(
        1 for ln in sec["body_pre"].split("\n")
        if B.is_table_row(ln) and not B.is_sep(ln)
    ) // 1
    # count header+rows blocks: divide by (rows per table) is unreliable; recount blocks
    bt = 0
    lines = sec["body_pre"].split("\n")
    i = 0
    while i < len(lines):
        if B.is_table_row(lines[i]):
            while i < len(lines) and B.is_table_row(lines[i]):
                i += 1
            bt += 1
        else:
            i += 1
    chk("[Manuscript] table count matches GFM blocks", docx_table_count(ms), bt)

    # 2. no Chinese
    for label, t in [("Manuscript", ms_text), ("Supporting", si_text), ("CoverLetter", cl_text)]:
        chk(f"[{label}] no Chinese", re.findall(r"[\u4e00-\u9fff]", t), [])

    # 3. mandatory strings
    for needle in [
        "https://github.com/yyx-4113/sepsis-immunoparalysis-hub",
        "0009-0004-9698-6552",
        "Use of generative AI",
        "No reported data were created, generated, imputed or altered by generative AI",
        "tag v1.19.1",
    ]:
        chk(f"Manuscript contains 「{needle[:40]}」", needle in ms_text)
    chk("CoverLetter contains ORCID", "0009-0004-9698-6552" in cl_text)

    # 4. placeholders
    for label, t in [("Manuscript", ms_text), ("Supporting", si_text), ("CoverLetter", cl_text)]:
        left = [m for m in ["[[", "TODO", "TBD", "XXX", "COMPLETE BEFORE SUBMISSION"] if m in t]
        chk(f"[{label}] no placeholders", left, [])

    # 5. figures
    chk("SI embeds 12 figures", len(Document(si).inline_shapes), 12)
    pngs = [f for f in os.listdir(figdir) if f.lower().endswith(".png")]
    chk("Figures/ has 12 PNGs", len(pngs), 12)

    print(f"==== PASS {len(OK)} / FAIL {len(BAD)} ====")
    for b in BAD:
        print("  [X]", b)
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
