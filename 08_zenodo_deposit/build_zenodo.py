#!/usr/bin/env python3
# Build the Zenodo deposit archive (zip) for sepsis-immunoparalysis-hub v1.19.1.
# Excludes: 43 GB raw inputs (01_data/), .git, .workbuddy, .github, 06_literature,
# debug scripts, simulated-review drafts (review*/), and log/temp files.
import os, zipfile, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "08_zenodo_deposit")
os.makedirs(OUT_DIR, exist_ok=True)
PREFIX = "sepsis-immunoparalysis-hub-v1.19.1/"
ZIP_PATH = os.path.join(OUT_DIR, "sepsis-immunoparalysis-hub-v1.19.1.zip")

INCLUDE_DIRS = ["00_pipeline", "02_scripts", "03_results", "04_figures", "07_submission_v1.19.1"]
INCLUDE_ROOT = [
    "README.md", "CITATION.cff", "LICENSE", "MANIFEST.csv",
    "DATA_SOURCES.md", "GITHUB_DEPOSIT_SOP.md", "author_verification_statement.md",
]
INCLUDE_REPORTS = [
    "05_reports/manuscript.md", "05_reports/cover_letter.md",
    "05_reports/scirep_submission_checklist.md",
]

# Substring patterns (on the "/" separated relative path) to exclude anywhere
EXCLUDE = [
    ".git", ".workbuddy", ".github", "01_data", "06_literature", "__pycache__",
    "_tmp_extract", "_lines_dump", "_apply_v118", "_apply_v1180",
    "_apply_v119", "_analysis_v119", "_fix_v1180",
    "方案三_", "/review", "review_r", ".log",
    "gse65682_pdata_inspect.csv", "build.log",
]

def excluded(rel):
    return any(pat in rel for pat in EXCLUDE)

def wanted(rel):
    if rel in INCLUDE_ROOT:
        return True
    if rel in INCLUDE_REPORTS:
        return True
    if rel.startswith("05_reports/REVIEW_round") and rel.endswith(".md") and rel.count("/") == 1:
        return True
    for d in INCLUDE_DIRS:
        if rel == d or rel.startswith(d + "/"):
            return True
    return False

files = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    rel_dp = os.path.relpath(dirpath, ROOT).replace("\\", "/")
    # prune whole excluded subtrees
    dirnames[:] = [d for d in dirnames
                   if not excluded((rel_dp + "/" + d).replace("\\", "/"))]
    for fn in filenames:
        rel = (rel_dp + "/" + fn).replace("\\", "/")
        if rel_dp == ".":
            rel = fn
        if excluded(rel):
            continue
        if wanted(rel):
            files.append(rel)

files = sorted(set(files))
total = 0
with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
    for rel in files:
        full = os.path.join(ROOT, rel)
        z.write(full, PREFIX + rel)
        total += os.path.getsize(full)

desc = ("This deposition archives the reproducible analysis pipeline and outcome tables "
        "underlying the manuscript 'Immunoparalysis hub genes of the MARS immunosuppressed "
        "endotype in sepsis: multi-omics confirmation and in-silico drug repositioning' "
        "(v1.19.1). It contains: (1) the auditable Python/R pipeline (02_scripts/) that "
        "re-analyses GEO cohort GSE65682 (802 samples) to confirm the Mars1 immunoparalysis "
        "program, prioritise five antigen-presentation/monocytic hubs (CD74, HLA-DQA1, CD14, "
        "FCGR3A, HAVCR2/TIM-3) plus the non-immune passenger FIS1, build and externally validate "
        "a 30-gene immune-risk signature, and run two-sample Mendelian randomisation; (2) all "
        "derived result tables (03_results/); (3) the 12 supplementary figures (04_figures/); "
        "(4) the submission-ready manuscript, cover letter and reporting summary "
        "(07_submission_v1.19.1/); and (5) project documentation including the data-source "
        "manifest and verification statement. Raw public omics inputs (~43 GB from GEO / "
        "ArrayExpress / LINCS / GTEx) are intentionally excluded and are restored from the "
        "accessions listed in DATA_SOURCES.md. The 15-test MR primary family is null "
        "(minimum family q = 0.81); the contribution is a reproducible pipeline, an honest "
        "external validation and an experimental blueprint.")

metadata = {
    "metadata": {
        "upload_type": "software",
        "publication_date": "2026-09-28",
        "title": ("Reproducible multi-omics pipeline and in-silico drug repositioning for the "
                  "immunosuppressed Mars1 sepsis endotype (v1.19.1)"),
        "creators": [
            {
                "name": "Yang, Yongxin",
                "orcid": "0009-0004-9698-6552",
                "affiliation": ("The Second Affiliated Hospital of Fujian University of "
                                "Traditional Chinese Medicine, Fuzhou, Fujian 350003, China"),
            }
        ],
        "description": desc,
        "keywords": [
            "sepsis", "immunoparalysis", "MARS endotype", "multi-omics",
            "drug repositioning", "LINCS L1000", "transcriptomics",
            "Mendelian randomization", "reproducible research",
        ],
        "license": "mit",
        "version": "v1.19.1",
        "access_right": "open",
        "related_identifiers": [
            {
                "relation": "isSupplementTo",
                "identifier": "https://github.com/yyx-4113/sepsis-immunoparalysis-hub",
                "resource_type": "software",
                "scheme": "url",
            }
        ],
        "notes": ("Pre-reservation archive for Scientific Reports submission. After acceptance, "
                  "mint the article DOI and add a related_identifier with relation 'isCitedBy'. "
                  "Raw data are restored per DATA_SOURCES.md."),
    }
}
with open(os.path.join(OUT_DIR, "zenodo_metadata.json"), "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"ZIP: {ZIP_PATH}")
print(f"Files archived: {len(files)}")
print(f"Uncompressed total: {total/1024/1024:.2f} MiB")
print(f"Zip size: {os.path.getsize(ZIP_PATH)/1024/1024:.2f} MiB")
print("--- by top directory ---")
from collections import Counter
c = Counter(f.split("/")[0] for f in files)
for k, v in sorted(c.items()):
    print(f"  {k}: {v} files")
print("LEAK CHECK (should be empty):",
      [f for f in files if "01_data" in f or f.startswith(".git") or "review_r" in f or f.endswith(".log")])
