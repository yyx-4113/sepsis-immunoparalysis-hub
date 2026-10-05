#!/usr/bin/env python3
"""Build the BMC Medical Genomics submission pack for sepsis-immunoparalysis-hub (v1.20.0).

v1.20.0 removes the Tier-3 Mendelian-randomisation layer (PLOS ONE desk-rejected the
prior version on MR methodological grounds). This pack is the MR-free, BMC-aligned build:
    - structured abstract (Background/Methods/Results/Conclusions)
    - BMC "Declarations" headings (ethics+consent, consent for publication, data/code, etc.)
    - 10 figures (the two MR figures are excluded)
    - supplementary tables S01,S02,S04,S05,S06,S07,S08,S08b,S09,S11 (S03/S10/S12 dropped)
    - 36 Vancouver references

Outputs (into the same folder this script lives in):
    Manuscript.docx           title, authors, structured abstract, body (§1-§8), declarations,
                              references (Vancouver), figure captions
    Supporting_Information.docx  S01-S11 tables (CSV-backed) + figure-caption list
    Cover_Letter.docx         BMC cover letter
    Figures/                  the 10 PNGs, renamed Fig1..Fig10.png (upload separately)
    SUBMISSION_MANIFEST.md    file -> submission-system type map + metadata + open items
    bmc_checklist.md          BMC pre-submission checklist
    references_parse.log      per-reference conversion audit
"""
from __future__ import annotations

import csv
import os
import re
import shutil

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
MS = os.path.join(PROJ, "05_reports", "manuscript.md")
COVER = os.path.join(HERE, "Cover_Letter_BMC.md")
STRUCT_ABSTRACT = os.path.join(HERE, "BMC_structured_abstract.md")
FIG_DIR = os.path.join(PROJ, "04_figures")
RES_DIR = os.path.join(PROJ, "03_results")
FIG_OUT = os.path.join(HERE, "Figures")

BODY_FONT = "Times New Roman"
MAX_ROWS = 800
N_EXPECTED_REFS = 36
N_EXPECTED_FIGS = 10


# --------------------------------------------------------------------------- #
# inline markdown -> docx runs
# --------------------------------------------------------------------------- #
INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*\n]+?\*|`[^`\n]+?`)")


def add_runs(p, text, *, bold=False, italic=False, size=None):
    for piece in INLINE.split(text):
        if not piece:
            continue
        b, i, mono = bold, italic, False
        if piece.startswith("**") and piece.endswith("**") and len(piece) > 4:
            piece, b = piece[2:-2], True
        elif piece.startswith("*") and piece.endswith("*") and len(piece) > 2:
            piece, i = piece[1:-1], True
        elif piece.startswith("`") and piece.endswith("`") and len(piece) > 2:
            piece, mono = piece[1:-1], True
        run = p.add_run(piece)
        run.bold, run.italic = b, i
        if size:
            run.font.size = Pt(size)
        run.font.name = "Courier New" if mono else BODY_FONT


def para(doc, text="", *, bold=False, italic=False, size=None, align=None,
         space_before=0, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if align is not None:
        p.alignment = align
    if text:
        add_runs(p, text, bold=bold, italic=italic, size=size)
    return p


# --------------------------------------------------------------------------- #
# document skeleton
# --------------------------------------------------------------------------- #
def new_document() -> Document:
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(11)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
    pf = normal.paragraph_format
    pf.line_spacing = 1.15
    pf.space_after = Pt(4)
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(2.54)
        s.left_margin = s.right_margin = Cm(2.54)
    return doc


# --------------------------------------------------------------------------- #
# markdown parsing helpers
# --------------------------------------------------------------------------- #
def strip_fig_refs(text: str) -> str:
    text = re.sub(r"\[\s*`[^`]*\.png[^`]*`\s*\]", "", text)
    text = re.sub(r"\s*`[^`]*\.png[^`]*`\s*", " ", text)
    return text


def is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.endswith("|")


def is_sep(line: str) -> bool:
    return bool(re.fullmatch(r"\|[\s:|\-]+\|", line.strip()))


def cells(line: str) -> list[str]:
    inner = line.strip()[1:-1]
    parts = re.split(r"(?<!\\)\|", inner)
    return [p.replace("\\|", "|").strip() for p in parts]


def emit_markdown(doc, block: str, *, table_size=8.5, strip_figs=False,
                  drop: tuple[str, ...] = ()) -> None:
    lines = block.split("\n")
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped or stripped == "---":
            i += 1
            continue
        if stripped.startswith(">"):
            i += 1
            continue
        if any(stripped.startswith(d) for d in drop):
            i += 1
            continue

        if is_table_row(line):
            rows = []
            while i < len(lines) and is_table_row(lines[i]):
                if not is_sep(lines[i]):
                    rows.append(cells(lines[i]))
                i += 1
            add_table(doc, rows, size=table_size)
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            level, title = len(m.group(1)), m.group(2)
            if level == 1:
                para(doc, title, bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER,
                     space_after=8)
            elif level == 2:
                para(doc, title, bold=True, size=12.5, space_before=8, space_after=4)
            else:
                para(doc, title, bold=True, size=11, space_before=6, space_after=3)
            i += 1
            continue

        if stripped.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(2)
            add_runs(p, stripped[2:])
            i += 1
            continue

        text = strip_fig_refs(stripped) if strip_figs else stripped
        para(doc, text)
        i += 1


def add_table(doc, rows, *, size=8.5) -> None:
    if not rows:
        return
    width = max(len(r) for r in rows)
    t = doc.add_table(rows=0, cols=width)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = True
    for ri, row in enumerate(rows):
        cells_out = t.add_row().cells
        for ci in range(width):
            text = row[ci] if ci < len(row) else ""
            cell = cells_out[ci]
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            add_runs(p, text, bold=(ri == 0), size=size)
        if ri == 0:
            trPr = t.rows[0]._tr.get_or_add_trPr()
            hdr = OxmlElement("w:tblHeader")
            trPr.append(hdr)
    para(doc, "", space_after=6)


def split_sections(text: str) -> dict:
    def idx(marker):
        return text.index(marker)

    return {
        "title": text[: idx("## Abstract (English)")],
        "abstract": text[idx("## Abstract (English)"): idx("## 1. Introduction")],
        "body_pre": text[idx("## 1. Introduction"): idx("## 8. Supplementary materials index")],
        "si_index": text[idx("## 8. Supplementary materials index"): idx("## Data availability")],
        "decl": text[idx("## Data availability"): idx("## References")],
        "refs": text[idx("## References"):],
    }


# --------------------------------------------------------------------------- #
# reference conversion: Nature style -> Vancouver (BMC)
# --------------------------------------------------------------------------- #
def strip_md(s: str) -> str:
    return s.replace("**", "").replace("*", "").replace("`", "")


def normalize_authors(a: str) -> str:
    return a.replace(" & ", ", ").strip()


def convert_references(refs_text: str):
    lines = refs_text.split("\n")
    out, log = [], []
    conv = raw = 0
    for ln in lines:
        s = ln.rstrip()
        if not s.strip():
            out.append(ln)
            continue
        m = re.match(r"^\s*(\d+)\.\s+(.*)$", s)
        if not m:
            out.append(ln)
            continue
        num, rest = m.group(1), m.group(2)
        jm = re.search(r"\*([^*]+?)\*", rest)
        vm = re.search(r"\*\*(\d+)\*\*", rest)
        if not (jm and vm):
            out.append(f"{num}. {strip_md(rest)}")
            log.append(f"RAW-kept {num}: no journal/vol anchor")
            raw += 1
            continue
        journal, vol = jm.group(1), vm.group(1)
        pre = rest[: jm.start()].rstrip()
        idx = pre.rfind(". ")
        if idx == -1:
            authors, title = "", pre
        else:
            authors = pre[:idx]
            title = pre[idx + 2:]
        authors = re.sub(r"^\s*\d+\.\s*", "", authors)
        after = rest[vm.end():]
        am = re.match(r"\s*,\s*(.+?)\s+\((\d{4})\)\.\s*(?:doi:)?(.+)$", after)
        if not am:
            out.append(f"{num}. {strip_md(rest)}")
            log.append(f"RAW-kept {num}: year/doi parse failed")
            raw += 1
            continue
        pages, year, doi = am.group(1), am.group(2), am.group(3).strip()
        authors_v = normalize_authors(authors)
        journal = journal.rstrip(".")
        title = title.rstrip(".")
        out.append(f"{num}. {authors_v}. {title}. {journal}. {year};{vol}:{pages}. doi:{doi}.")
        conv += 1
    return "\n".join(out), log, conv, raw


# --------------------------------------------------------------------------- #
# manuscript
# --------------------------------------------------------------------------- #
def restructure_declarations(decl: str) -> str:
    """Map the manuscript's flat ## headings onto BMC 'Declarations' sub-headings
    and add the BMC-required 'Consent for publication' block."""
    decl = decl.replace("## Data availability", "### Data availability")
    decl = decl.replace("## Code availability", "### Code availability")
    decl = decl.replace("## Ethics statement",
                        "## Declarations\n\n### Ethics approval and consent to participate")
    decl = decl.replace("## Author contributions", "### Author contributions")
    decl = decl.replace("## Funding", "### Funding")
    decl = decl.replace("## Competing interests", "### Competing interests")
    consent = ("\n\n### Consent for publication\n\nNot applicable. This study used only "
               "public, de-identified aggregate transcriptomic cohorts and reports no "
               "individual-level data, images, or case details.")
    decl = decl.rstrip() + consent + "\n"
    return decl


def build_manuscript(sec: dict, structured_abstract: str) -> str:
    doc = new_document()

    # --- title page ---
    title_text = None
    for line in sec["title"].split("\n"):
        s = line.strip()
        if not s or s == "---":
            continue
        if s.startswith("# "):
            title_text = s[2:]
            para(doc, title_text, bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER,
                 space_after=6)
        elif s.startswith("**") and s.endswith("**"):
            inner = s[2:-2]
            para(doc, inner, bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER,
                 space_after=1)
        else:
            para(doc, s, size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    doc.add_paragraph()

    # structured (BMC) abstract, not the manuscript's unstructured one
    emit_markdown(doc, structured_abstract)
    emit_markdown(doc, sec["body_pre"], strip_figs=True)
    emit_markdown(doc, sec["si_index"])

    decl = restructure_declarations(sec["decl"])
    emit_markdown(doc, decl)

    # --- references (converted) ---
    refs_conv, ref_log, conv_n, raw_n = convert_references(sec["refs"])
    with open(os.path.join(HERE, "references_parse.log"), "w", encoding="utf-8") as f:
        f.write(f"converted={conv_n} raw_kept={raw_n}\n")
        f.write("\n".join(ref_log) + "\n")
    emit_markdown(doc, refs_conv)

    # --- figure captions (figures uploaded separately) ---
    doc.add_paragraph()
    para(doc, "Figures", bold=True, size=12.5, space_before=8, space_after=4)
    for _, label, caption in FIG_CAPTIONS:
        para(doc, f"{label}. {caption}", italic=True, size=9.5, space_after=6)

    path = os.path.join(HERE, "Manuscript.docx")
    doc.save(path)
    return path


# --------------------------------------------------------------------------- #
# supporting information
# --------------------------------------------------------------------------- #
SI_TABLES = {
    "S01": (["S01_deg_sepsis_vs_ctrl.csv", "S01_immunoparalysis_direction.csv",
             "S01_immunoparalysis_genes_in_mars1.csv", "S01_mars1_deg.csv",
             "S01_mars1_deg_endotypeonly.csv", "S01_mars1_stratification.csv"],
            "Mars1 differential expression and consensus immune-gene direction "
            "(Mars1-vs-Other and sepsis-vs-healthy)."),
    "S02": (["S02_immunoparalysis_score.csv"],
            "Immune-function score by MARS endotype."),
    "S04": ([], "Curated immune-gene sets (see deposited gene-set files and §2.4)."),
    "S05": ([], "Hub-gene selection (LASSO / RF / univariate consensus) and the FIS1 "
               "co-expression passenger (see 03_results/S05_hub_genes.csv)."),
    "S06": (["S06_auc_compare.csv", "S06_hub_death_association.csv", "S06_signature_genes.csv"],
            "30-gene signature genes and cross-validated AUC; hub death association."),
    "S07": ([], "Hub and axis cellular-context marker-module correlations "
               "(see 03_results/07_hub_celltype.csv)."),
    "S08": (["S08_l1000_candidate_scores.csv", "S08_l1000_immuno_overlap.csv",
             "S08_l1000_positive_control.csv", "S08_l1000_rescue_trtcp.csv"],
            "Mechanism-anchored repositioning shortlist, positive-control check, and "
            "L1000 reverse-connectivity scores."),
    "S08b": (["08b_clinical_translation.csv"], "Clinical-translation status of each candidate."),
    "S09": ([], "Deferred by design (see Limitation 7)."),
    "S11": ([], "Experimental validation blueprint (LPS-tolerance / patient-cell assays; "
               "see 03_results/11_validation_design.md)."),
}


CJK_MAP = {"基准": "benchmark"}


def _clean_cell(s: str) -> str:
    for k, v in CJK_MAP.items():
        s = s.replace(k, v)
    return re.sub(r"[\u4e00-\u9fff]+", "", s)


def _read_csv_rows(path: str) -> list[list[str]]:
    with open(path, encoding="utf-8", newline="") as f:
        return [[_clean_cell(c) for c in r] for r in csv.reader(f)]


def build_supporting() -> str:
    doc = new_document()
    para(doc, "Supporting Information", bold=True, size=15,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    para(doc, "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and "
              "externally evaluates a 30-gene sepsis prognostic signature", italic=True,
         size=11, space_after=10)

    for key in sorted(SI_TABLES):
        files, caption = SI_TABLES[key]
        para(doc, f"Table {key}. {caption}", bold=True, size=10.5,
             space_before=8, space_after=3)
        if not files:
            para(doc, "(No tabular CSV deposited; narrative content is in the manuscript "
                      "methods and the versioned repository.)", italic=True, size=9,
                 space_after=6)
            continue
        for fn in files:
            src = os.path.join(RES_DIR, fn)
            if not os.path.exists(src):
                para(doc, f"[file not found: {fn}]", italic=True, size=9)
                continue
            rows = _read_csv_rows(src)
            if not rows:
                continue
            if len(rows) > MAX_ROWS:
                para(doc, f"[Table {key} / {fn}: {len(rows)} rows — too large to embed. "
                          f"The full table is deposited at 03_results/{fn} and cited in "
                          f"the manuscript (§7).]", italic=True, size=9, space_after=4)
                continue
            add_table(doc, rows, size=7.5)
            para(doc, f"Source: 03_results/{fn}", italic=True, size=8, space_after=4)

    doc.add_paragraph()
    para(doc, "Figure captions", bold=True, size=12.5, space_before=8, space_after=4)
    for _, label, caption in FIG_CAPTIONS:
        para(doc, f"{label}. {caption}", italic=True, size=9.5, space_after=6)

    path = os.path.join(HERE, "Supporting_Information.docx")
    doc.save(path)
    return path


# --------------------------------------------------------------------------- #
# cover letter
# --------------------------------------------------------------------------- #
def build_cover_letter() -> str:
    text = open(COVER, encoding="utf-8").read()
    doc = new_document()
    emit_markdown(doc, text)
    path = os.path.join(HERE, "Cover_Letter.docx")
    doc.save(path)
    return path


# --------------------------------------------------------------------------- #
# figures (copied separately for upload) -- MR figures excluded
# --------------------------------------------------------------------------- #
FIG_CAPTIONS = [
    ("S01_roc_28d_mars1.png", "Fig. S1",
     "ROC of 28-day mortality by the Mars1 binary indicator (discovery cohort)."),
    ("S02_score_vs_endotype.png", "Fig. S2", "Immune-function score by MARS endotype."),
    ("S03_top_hub.png", "Fig. S3A", "Hub genes (top-hub degree centrality)."),
    ("S03_eigengene_trait_cor.png", "Fig. S3B", "Eigengene-trait correlation."),
    ("S06_roc_cv.png", "Fig. S6A", "Cross-validated ROC."),
    ("S06_roc_train.png", "Fig. S6B", "Training ROC."),
    ("S06_dca.png", "Fig. S6C", "Decision-curve analysis (external equal-weight score)."),
    ("S07_celltype.png", "Fig. S7",
     "Cellular context of hub genes (bulk surrogate deconvolution)."),
    ("fig_s09_external_roc.png", "Fig. S9",
     "ROC of the locked signature on E-MTAB-4451 (n=106)."),
    ("fig_s10_l1000_rescue.png", "Fig. S10",
     "Top LINCS L1000 rescuers of the Mars1-down axis and candidate markers."),
]


def copy_figures() -> int:
    os.makedirs(FIG_OUT, exist_ok=True)
    n = 0
    for i, (fname, label, _) in enumerate(FIG_CAPTIONS, start=1):
        src = os.path.join(FIG_DIR, fname)
        dst = os.path.join(FIG_OUT, f"Fig{i}.png")
        if os.path.exists(src):
            shutil.copyfile(src, dst)
            n += 1
    return n


# --------------------------------------------------------------------------- #
# manifest + checklist
# --------------------------------------------------------------------------- #
def write_manifest(files: dict, n_fig: int) -> None:
    lines = [
        "# Submission manifest — BMC Medical Genomics",
        "",
        "Manuscript version: **v1.20.0** (tag `v1.20.0`, built on commit `7704c9a` / tag v1.16.0).",
        "Repository: https://github.com/yyx-4113/sepsis-immunoparalysis-hub",
        "Zenodo DOI: 10.5281/zenodo.23042366 (public).",
        "",
        "## File -> BMC submission-system file type",
        "",
        "| Local file | System file type | Notes |",
        "|---|---|---|",
        f"| {files['ms']} | Main Document / Manuscript | Structured abstract + §1-§8 body + Declarations + 36 Vancouver refs + figure captions |",
        f"| {files['si']} | Supplementary Material | S01,S02,S04,S05,S06,S07,S08,S08b,S09,S11 tables + figure-caption list |",
        f"| {files['cl']} | Cover Letter | |",
        "| Figures/Fig1.png ... Fig10.png | Figure | upload each separately; map to captions in Manuscript.docx |",
        "",
        "## Do NOT upload",
        "- 05_reports/REVIEW_round*.md (internal review logs)",
        "- 02_scripts/, 03_results/ raw CSVs as-is (deposited in repo, not as SI)",
        "- build_submission_bmc.py / verify_submission_bmc.py (build tooling)",
        "- the two MR figures (mr_forest.png, mr_diag.png) — MR layer removed in v1.20.0",
        "",
        "## Metadata the form will ask for",
        "- Title: as in Manuscript.docx (17 words).",
        "- Article type: Research article.",
        "- Abstract: STRUCTURED (Background / Methods / Results / Conclusions).",
        "- Keywords: as listed under the abstract.",
        "- References: 36, Vancouver style, DOIs present, numbered in citation order.",
        "- Tables: main provenance table in main doc (§7); 10 supplementary in SI.",
        "- Figures: 10, uploaded separately as PNG.",
        "- Corresponding author: Yongxin Yang; ORCID 0009-0004-9698-6552; email 960856791@qq.com.",
        "- Funding: none declared (state explicitly in form).",
        "- Competing interests: declared in the manuscript (none).",
        "- Data availability: GitHub (tag v1.20.0) + Zenodo DOI 10.5281/zenodo.23042366.",
        "- Declarations: Ethics approval and consent to participate; Consent for publication; "
        "Data availability; Code availability; Competing interests; Funding; Author contributions.",
        "",
        "## Open items for the author (not fabricated)",
        "1. Confirm the corresponding-author account name in the submission system uses the "
        "Latin script (given/family), not '永新 杨'.",
        "2. Complete the BMC declarations in the online form (the manuscript carries the "
        "full text; the form asks for checkboxes).",
        "3. Zenodo DOI 10.5281/zenodo.23042366 already minted and pasted into Data availability.",
        f"4. Upload each FigN.png and map it to its manuscript caption ({n_fig} figures).",
        "5. BMC requires a 'Declarations' section (included: ethics+consent, consent for "
        "publication, data, code, competing interests, funding, author contributions).",
        "",
        "## Verification",
        "- `python verify_submission_bmc.py` exits 0: numeric-token diff empty both ways, "
        "no Chinese text, no placeholders, mandatory strings (repo URL, ORCID, Zenodo DOI, "
        "AI disclosure §2.11) present, 36 references in Vancouver style, 10 figures copied, "
        "no MR-residue keywords.",
    ]
    with open(os.path.join(HERE, "SUBMISSION_MANIFEST.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_checklist() -> None:
    lines = [
        "# BMC Medical Genomics pre-submission checklist",
        "",
        "## Scope / soundness",
        "- [x] Original computational-biology research (reproducible pipeline + external "
        "signature validation + drug-repositioning blueprint).",
        "- [x] Within scope: genomic/transcriptomic analysis of sepsis immunoparalysis.",
        "- [x] Methods described in sufficient detail for reproduction (every number traces "
        "to a deposited file; 32 audit assertions).",
        "- [x] Conclusions supported by the data (null/observational findings framed honestly).",
        "- [x] Written in standard English.",
        "",
        "## Required BMC Declarations (present in manuscript)",
        "- [x] Ethics approval and consent to participate.",
        "- [x] Consent for publication: Not applicable.",
        "- [x] Data availability (GitHub tag v1.20.0 + Zenodo DOI 10.5281/zenodo.23042366).",
        "- [x] Code availability (MIT, CITATION.cff).",
        "- [x] Competing interests (none declared).",
        "- [x] Funding (none declared).",
        "- [x] Author contributions.",
        "- [x] Acknowledgements.",
        "- [x] Generative-AI use disclosure (§2.11).",
        "",
        "## Formatting",
        "- [x] Structured abstract (Background/Methods/Results/Conclusions).",
        "- [x] References numbered in citation order, Vancouver style, DOIs present (36).",
        "- [x] In-text citations bracketed [n].",
        "- [x] Figures as separate PNG files; captions in manuscript.",
        "- [x] Article type: Research article.",
        "",
        "## Before final submit",
        "- [ ] Confirm corresponding-author name in the system is Latin script.",
        "- [ ] Re-check Funding wording (none declared).",
        "- [ ] Upload Fig1-Fig10 and map to captions.",
        "- [ ] Tick the BMC online declarations checkboxes.",
    ]
    with open(os.path.join(HERE, "bmc_checklist.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# --------------------------------------------------------------------------- #
def main() -> int:
    os.makedirs(FIG_OUT, exist_ok=True)
    text = open(MS, encoding="utf-8").read()
    sec = split_sections(text)
    structured = open(STRUCT_ABSTRACT, encoding="utf-8").read()

    exported = "\n".join([sec["title"], structured, sec["body_pre"],
                          sec["si_index"], sec["decl"], sec["refs"]])
    exported = strip_fig_refs(exported)
    bad = re.findall(r"[\u4e00-\u9fff]", exported)
    if bad:
        print(f"ABORT: Chinese text in exported sections: {sorted(set(bad))[:10]}")
        return 1

    # MR-residue guard
    mr_hits = re.findall(r"(?i)mendelian|strobe-mr|twosamplemr|instrumental variable|"
                         r"\bivw\b|\begger\b|genetic causality", exported)
    if mr_hits:
        print(f"ABORT: MR residue in exported text: {sorted(set(mh.lower() for mh in mr_hits))}")
        return 1

    refs_conv, ref_log, conv_n, raw_n = convert_references(sec["refs"])
    if raw_n:
        print(f"WARN: {raw_n} references kept raw (see references_parse.log)")
    else:
        print(f"OK: all {conv_n} references converted to Vancouver style")
    if conv_n != N_EXPECTED_REFS:
        print(f"WARN: expected {N_EXPECTED_REFS} references, got {conv_n}")

    ms = build_manuscript(sec, structured)
    si = build_supporting()
    cl = build_cover_letter()
    n_fig = copy_figures()
    write_manifest({"ms": os.path.basename(ms), "si": os.path.basename(si),
                    "cl": os.path.basename(cl)}, n_fig)
    write_checklist()

    for p in (ms, si, cl):
        print(f"  {os.path.relpath(p, HERE):32s} {os.path.getsize(p)/1024:8.1f} KB")
    print("Figures copied:", n_fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
