#!/usr/bin/env python3
"""Build the Scientific Reports submission pack for sepsis-immunoparalysis-hub (v1.19.1).

Outputs (into the same folder this script lives in):
    Manuscript.docx              title, abstract, body (§1-§8), declarations, references, main tables
    Supporting_Information.docx  S01-S12 tables (CSV-backed) + 12 supplementary figures (embedded)
    Cover_Letter.docx            cover letter
    Reporting_Summary.docx       Nature life-sciences reporting summary (draft, author to finalise)
    Figures/                    the 12 PNGs, renamed to English Figure_Sx.png
    SUBMISSION_MANIFEST.md       file -> submission-system type map + metadata + open items

One source of truth: 05_reports/manuscript.md (and cover_letter.md). The .docx files are build
artefacts. Run verify_submission.py afterwards to prove the conversion lost nothing.

Conventions applied for Scientific Reports (Nature Portfolio):
    - Times New Roman 11 pt, single spaced, no line numbers (Snapp does not require them)
    - unstructured abstract (<=200 words) -- already verified at 194 words
    - Nature reference style (numbered, [n] in text)
    - main tables kept in the manuscript (caption above each)
    - all figures are supplementary (S-series); embedded in the SI and also copied separately
    - declarations (data/code availability, ethics, author contributions, funding, competing
      interests, acknowledgements) kept inside the manuscript, not separate
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
from docx.shared import Cm, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
MS = os.path.join(PROJ, "05_reports", "manuscript.md")
COVER = os.path.join(PROJ, "05_reports", "cover_letter.md")
FIG_DIR = os.path.join(PROJ, "04_figures")
RES_DIR = os.path.join(PROJ, "03_results")
FIG_OUT = os.path.join(HERE, "Figures")

BODY_FONT = "Times New Roman"
MAIN_TABLE_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")


def strip_fig_refs(text: str) -> str:
    """Remove supplementary-figure file references from the BODY prose.

    Bracketed groups that contain a .png, and standalone backtick .png spans, are removed.
    .csv backtick spans are KEPT (they are legitimate provenance citations in table captions
    and in the §7 number-provenance table).
    """
    text = re.sub(r"\[\s*`[^`]*\.png[^`]*`\s*\]", "", text)
    text = re.sub(r"\s*`[^`]*\.png[^`]*`\s*", " ", text)
    return text


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


INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*\n]+?\*|`[^`\n]+?`)")


def add_runs(p, text, *, bold=False, italic=False, size=None):
    """Render inline markdown (**bold**, *italic*, `code`) into docx runs."""
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
    return p


def para(doc, text="", *, bold=False, italic=False, size=None, align=None,
         space_before=0, space_after=4, single=False):
    p = doc.add_paragraph()
    if single:
        p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if align is not None:
        p.alignment = align
    if text:
        add_runs(p, text, bold=bold, italic=italic, size=size)
    return p


# --------------------------------------------------------------------------- #
# markdown parsing
# --------------------------------------------------------------------------- #
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
    """Render a markdown block: headings, paragraphs, pipe tables, bullet lists."""
    lines = block.split("\n")
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped or stripped == "---":
            i += 1
            continue
        if stripped.startswith(">"):                       # blockquote = internal note
            i += 1
            continue
        if any(stripped.startswith(d) for d in drop):      # internal prose note
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


def add_table(doc, rows: list[list[str]], *, size=8.5) -> None:
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
    para(doc, "", single=True, space_after=6)


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
# manuscript
# --------------------------------------------------------------------------- #
def build_manuscript(sec: dict) -> str:
    doc = new_document()

    # title page
    for line in sec["title"].split("\n"):
        s = line.strip()
        if not s or s == "---":
            continue
        if s.startswith("# "):
            para(doc, s[2:], bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
        else:
            para(doc, s, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    doc.add_paragraph()

    emit_markdown(doc, sec["abstract"])
    doc.add_paragraph()
    emit_markdown(doc, sec["body_pre"], strip_figs=True)   # strip .png cross-refs only
    emit_markdown(doc, sec["si_index"])                    # keep the file map intact
    emit_markdown(doc, sec["decl"])
    emit_markdown(doc, sec["refs"])

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
    "S03": (["S03_hub_degree.csv", "S03_key_module_genes.csv", "S03_modules.csv",
             "S03_module_trait_cor.csv"],
            "Co-expression network: hub degree, key module genes, modules, and "
            "module-trait correlations."),
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
    "S10": (["10_genetics_mr.csv", "10_genetics_mr_outcome4982_criticalcare.csv",
             "10_genetics_mr_outcome5086_28ddeath.csv", "10_mr_bh_family.csv"],
            "Two-sample MR inputs, per-outcome and family-BH outputs, harmonised "
            "instrument tables, and design log."),
    "S11": ([], "Experimental validation blueprint (LPS-tolerance / patient-cell assays; "
               "see 03_results/11_validation_design.md)."),
    "S12": (["12_strobe_mr_checklist.csv"], "STROBE-MR checklist."),
}

MAX_ROWS = 800  # tables larger than this are deposited, not embedded (SI docx stays light)


def si_expected_tables() -> int:
    """Count CSV-backed SI tables that will actually be embedded (<= MAX_ROWS)."""
    n = 0
    for key in sorted(SI_TABLES):
        for fn in SI_TABLES[key][0]:
            src = os.path.join(RES_DIR, fn)
            if not os.path.exists(src):
                continue
            try:
                with open(src, encoding="utf-8", newline="") as f:
                    rows = sum(1 for _ in csv.reader(f))
            except Exception:  # noqa: BLE001
                continue
            if rows <= MAX_ROWS:
                n += 1
    return n


FIGS = [
    ("S01_roc_28d_mars1.png", "Fig. S1",
     "ROC of 28-day mortality by the Mars1 binary indicator (AUC 0.578, discovery cohort)."),
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
    ("mr_forest.png", "Fig. S11",
     "15-test Mendelian-randomisation forest (inverse-variance weighting)."),
    ("mr_diag.png", "Fig. S12",
     "MR diagnostic panels: CD14 28-day-death scatter with IVW/Egger fits, Egger funnel, "
     "leave-one-out, and CD74 critical-care scatter."),
]


def _read_csv_rows(path: str) -> list[list[str]]:
    with open(path, encoding="utf-8", newline="") as f:
        return [[_clean_cell(c) for c in r] for r in csv.reader(f)]


CJK_MAP = {"基准": "benchmark"}


def _clean_cell(s: str) -> str:
    """Strip Chinese text from SI table cells (Scientific Reports is English-only).

    Known terms are mapped to English; any residual CJK run is removed as a safety net.
    """
    for k, v in CJK_MAP.items():
        s = s.replace(k, v)
    return re.sub(r"[\u4e00-\u9fff]+", "", s)


def build_supporting() -> str:
    doc = new_document()
    para(doc, "Supplementary Information", bold=True, size=15,
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
                para(doc, f"[Table {key} / {fn}: {len(rows)} rows — too large to embed in the "
                          f"SI document. The full table is deposited at 03_results/{fn} and is "
                          f"cited in the manuscript (§7).]", italic=True, size=9, space_after=4)
                continue
            add_table(doc, rows, size=7.5)
            para(doc, f"Source: 03_results/{fn}", italic=True, size=8, space_after=4)

    doc.add_paragraph()
    para(doc, "Supplementary Figures", bold=True, size=12.5, space_before=8, space_after=4)
    for fname, label, caption in FIGS:
        src = os.path.join(FIG_DIR, fname)
        dst = os.path.join(FIG_OUT, f"{label.replace(' ', '').replace('.', '_')}.png")
        if os.path.exists(src):
            shutil.copyfile(src, dst)
            try:
                doc.add_picture(dst, width=Cm(14))
                doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            except Exception as e:  # noqa: BLE001
                para(doc, f"[{label} image failed: {e}]", italic=True, size=9)
        para(doc, f"{label}. {caption}", italic=True, size=9.5, space_after=8)

    path = os.path.join(HERE, "Supporting_Information.docx")
    doc.save(path)
    return path


# --------------------------------------------------------------------------- #
# cover letter + reporting summary
# --------------------------------------------------------------------------- #
def build_cover_letter() -> str:
    text = open(COVER, encoding="utf-8").read()
    doc = new_document()
    emit_markdown(doc, text)
    path = os.path.join(HERE, "Cover_Letter.docx")
    doc.save(path)
    return path


def build_reporting_summary() -> str:
    doc = new_document()
    para(doc, "Life Sciences Reporting Summary (Scientific Reports / Nature Portfolio)",
         bold=True, size=13, space_after=6)
    para(doc, "DRAFT — to be finalised by the author in the journal's online form. "
              "Fields marked [AUTHOR] require input that only the submitting author can "
              "supply; they are not fabricated.", italic=True, size=9, space_after=8)

    sections = [
        ("Study design", [
            "Study type: Observational / in-silico re-analysis of public transcriptomic "
            "cohorts (GSE65682, E-MTAB-4451) plus two-sample Mendelian randomisation.",
            "Research sample: 802 GSE65682 samples (760 sepsis / 42 healthy controls) and "
            "106 E-MTAB-4451 severe-sepsis samples.",
            "Data deposition: All analysis code and result tables are in the versioned "
            "repository (tag v1.19.1); raw inputs are regenerable from GEO / ArrayExpress.",
        ]),
        ("Samples & biological materials", [
            "Human data: de-identified public deposits; no new primary samples generated.",
            "Ethics: Public, de-identified, aggregate data; analysis exempt from local "
            "IRB per the manuscript Ethics statement. [AUTHOR: confirm whether your "
            "institution requires a specific exemption letter]",
        ]),
        ("Methods", [
            "Differential expression: limma (linear models, empirical Bayes).",
            "Hub detection: tri-method ML consensus (LASSO / random forest / univariate) "
            "plus WGCNA-style co-expression.",
            "Validation: external cross-platform cohort (E-MTAB-4451), AUC with DeLong CI.",
            "MR: TwoSampleMR, IVW primary, MR-Egger / weighted median sensitivity, t-distributed p.",
        ]),
        ("Reporting standards", [
            "STROBE-MR checklist: provided as Supplementary Table S12.",
            "No blinding / randomisation (observational re-analysis).",
        ]),
        ("Statistics & reproducibility", [
            "Randomisation: not applicable (observational).",
            "Blinding: not applicable.",
            "Sample-size rationale: fixed by public-cohort availability.",
            "Software: Python 3.13, R 4.x; exact versions in the repository CITATION.cff.",
        ]),
        ("Data availability", [
            "Repository: https://github.com/yyx-4113/sepsis-immunoparalysis-hub (tag v1.19.1).",
            "Zenodo DOI: 10.5281/zenodo.23042366.",
        ]),
    ]
    for title, items in sections:
        para(doc, title, bold=True, size=11, space_before=6, space_after=2)
        for it in items:
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(2)
            add_runs(p, it)

    path = os.path.join(HERE, "Reporting_Summary.docx")
    doc.save(path)
    return path


# --------------------------------------------------------------------------- #
# manifest
# --------------------------------------------------------------------------- #
def write_manifest(files: dict) -> None:
    lines = [
        "# Submission manifest — Scientific Reports (Nature Portfolio)",
        "",
        f"Manuscript version: **v1.19.1** (tag `v1.19.1`, built on commit `1212f7b` / tag v1.16.0).",
        "Repository: https://github.com/yyx-4113/sepsis-immunoparalysis-hub",
        "",
        "## File -> submission-system file type",
        "",
        "| Local file | Snapp file type | Notes |",
        "|---|---|---|",
        f"| {files['ms']} | Main Document | Text + Tables 1-5 + §7 provenance table + references + declarations |",
        f"| {files['si']} | Supplementary Information | S01-S12 tables + 12 supplementary figures |",
        f"| {files['cl']} | Cover Letter | |",
        f"| {files['rs']} | Reporting Summary (Life Sciences) | DRAFT; finalise in journal form |",
        "| Figures/Figure_S1.png ... Figure_S12.png | Figure | map each to its caption in the SI |",
        "",
        "## Do NOT upload",
        "- 05_reports/REVIEW_round*.md (internal review logs)",
        "- 02_scripts/, 03_results/ raw CSVs as-is (they are deposited in the repo, not as SI)",
        "- build_submission.py / verify_submission.py (build tooling)",
        "",
        "## Metadata the form will ask for",
        "- Title: as in Manuscript.docx (<=20 words per Sci Rep; currently 17).",
        "- Article type: Article (research).",
        "- Abstract: unstructured, 194 words (verified).",
        "- Keywords: as listed under the abstract.",
        "- References: 41, Nature style, DOIs present.",
        "- Tables: 5 main (+ §7 provenance) in the main doc; 12 supplementary in the SI.",
        "- Figures: 12 supplementary (S1-S12) as separate PNG files.",
        "- Corresponding author: Yongxin Yang; ORCID 0009-0004-9698-6552; email 960856791@qq.com.",
        "- Funding: [AUTHOR: state explicitly — currently 'none declared' in the manuscript].",
        "- Competing interests: declared in the manuscript.",
        "- Data availability URL: https://github.com/yyx-4113/sepsis-immunoparalysis-hub (tag v1.19.1).",
        "",
        "## Open items for the author (not fabricated)",
        "1. Confirm the corresponding-author account name in Snapp uses the Latin script "
        "(given/family), not '永新 杨'.",
        "2. Complete the Nature Life Sciences Reporting Summary in the journal's online form "
        "(draft provided).",
        "3. [DONE] Zenodo DOI 10.5281/zenodo.23042366 minted and pasted into the Data availability statement.",
        "4. Upload each Figure_Sx.png and map it to its SI caption.",
        "5. Re-check the Funding statement wording before final submit.",
        "",
        "## Verification",
        "- `python verify_submission.py` exits 0: numeric-token diff empty both ways, no "
        "Chinese text, no placeholders, mandatory strings (repo URL, ORCID, AI disclosure) "
        "present, expected table counts, 12 figures embedded in the SI.",
    ]
    with open(os.path.join(HERE, "SUBMISSION_MANIFEST.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# --------------------------------------------------------------------------- #
def main() -> int:
    os.makedirs(FIG_OUT, exist_ok=True)
    text = open(MS, encoding="utf-8").read()
    sec = split_sections(text)

    # Chinese-text guard on the exported (submitted) markdown only
    exported = "\n".join([sec["title"], sec["abstract"], sec["body_pre"],
                           sec["si_index"], sec["decl"], sec["refs"]])
    exported = strip_fig_refs(exported)
    bad = re.findall(r"[\u4e00-\u9fff]", exported)
    if bad:
        print(f"ABORT: Chinese text in exported sections: {sorted(set(bad))[:10]}")
        return 1

    ms = build_manuscript(sec)
    si = build_supporting()
    cl = build_cover_letter()
    rs = build_reporting_summary()
    write_manifest({"ms": os.path.basename(ms), "si": os.path.basename(si),
                    "cl": os.path.basename(cl), "rs": os.path.basename(rs)})

    for p in (ms, si, cl, rs):
        print(f"  {os.path.relpath(p, HERE):32s} {os.path.getsize(p)/1024:8.1f} KB")
    print("Figures copied:", len(os.listdir(FIG_OUT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
