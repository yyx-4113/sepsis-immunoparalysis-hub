"""Recompute SHA-256 + byte size for every path in MANIFEST.csv.

- Reads MANIFEST.csv (path,bytes,sha256; Windows backslash paths).
- For each existing path, recomputes sha256 + size, updates the row, and
  reports any mismatch (audit trail for the 'number provenance' discipline).
- Appends any load-bearing files that were modified but missing from the
  manifest (e.g. pipeline status doc, deferred-stage scaffold).

Run from repo root. Idempotent: re-running yields identical output once
files stop changing.

Usage:
    python 02_scripts/python/recompute_manifest.py
"""
import hashlib
import os
import csv

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANIFEST = os.path.join(ROOT, "MANIFEST.csv")

# Files modified this session but not yet tracked by MANIFEST (decision artifacts).
ADD_PATHS = [
    "00_pipeline/PIPELINE.md",
    "02_scripts/09_docking_admet.R",
    "02_scripts/python/build_references.py",
    "02_scripts/python/insert_references.py",
    "03_results/generated_references.md",
    "03_results/reference_doi_audit.csv",
]


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if not os.path.exists(MANIFEST):
        raise SystemExit(f"MANIFEST.csv not found at {MANIFEST}")

    with open(MANIFEST, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        rows = [row for row in reader if row]

    changed, missing = [], []
    existing = {row[0] for row in rows}
    for row in rows:
        p = row[0]
        fpath = os.path.join(ROOT, p.replace("\\", "/"))
        if not os.path.exists(fpath):
            missing.append(p)
            continue
        size = os.path.getsize(fpath)
        digest = sha256_of(fpath)
        if str(size) != row[1] or digest != row[2]:
            changed.append((p, row[1], str(size), row[2], digest))
        row[1] = str(size)
        row[2] = digest

    added = []
    for p in ADD_PATHS:
        fpath = os.path.join(ROOT, p.replace("\\", "/"))
        if p not in existing and os.path.exists(fpath):
            rows.append([p, str(os.path.getsize(fpath)), sha256_of(fpath)])
            added.append(p)

    with open(MANIFEST, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        writer.writerows(rows)

    print("MISMATCHES/UPDATED (path | old_bytes old_sha -> new_bytes new_sha):")
    for c in changed:
        print(f"  {c[0]}\n    {c[1]} {c[3]}\n -> {c[2]} {c[4]}")
    print("MISSING (path in manifest but file absent):", missing or "none")
    print("ADDED:", added or "none")
    print(f"TOTAL MANIFEST ROWS: {len(rows)}")


if __name__ == "__main__":
    main()
