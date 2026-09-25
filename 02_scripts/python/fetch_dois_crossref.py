#!/usr/bin/env python
"""Fetch candidate DOIs from Crossref for the S08b clinical-translation table.

Purpose
-------
`03_results/08b_clinical_translation.csv` carries 7 repositioning candidates whose
`ref_status` was left as "Need DOI at submission". This script queries the Crossref
REST API (no auth, no fabrication) and prints candidate records so that a human can
pick the real, verifiable citation for each row.

Usage
-----
    python fetch_dois_crossref.py            # print candidates for all 7 compounds
    python fetch_dois_crossref.py IL-7       # print candidates for one compound

Hard rule
---------
No DOI is ever invented here. If Crossref returns nothing usable, the row keeps
"DOI unresolved - no verifiable record" in the CSV.
"""

import json
import sys
import urllib.parse
import urllib.request

ENDPOINT = "https://api.crossref.org/works"

# One or more targeted queries per compound. Wording mirrors what the manuscript
# actually claims, so the citation found will support that claim.
QUERIES = {
    "IL-7": [
        "interleukin-7 restores lymphocytes septic shock IRIS-7 randomized clinical trial",
        "recombinant human interleukin-7 CYT107 sepsis lymphopenia trial",
    ],
    "GM-CSF": [
        "granulocyte-macrophage colony-stimulating factor reverse sepsis-associated immunosuppression",
        "GM-CSF immunotherapy sepsis monocyte HLA-DR randomized trial",
    ],
    "IFN-gamma": [
        "interferon gamma treatment immunoparalysis sepsis monocyte HLA-DR",
        "interferon gamma-1b sepsis immunostimulation trial",
    ],
    "Azithromycin": [
        "azithromycin immunomodulation macrolide sepsis immune response",
        "azithromycin immunomodulatory effects clinical trial",
    ],
    "Lenalidomide": [
        "lenalidomide immunomodulatory drug upregulates antigen presentation immune",
        "lenalidomide costimulatory immune modulation mechanism",
    ],
    "Thymosin alpha1": [
        "thymosin alpha 1 sepsis immunomodulation randomized trial meta-analysis",
        "thymosin alpha1 treatment sepsis immune function",
    ],
    "BCG": [
        "BCG vaccination trained immunity innate immune reprogramming",
        "BCG trained immunity sepsis prevention infection",
    ],
}


def query(q, rows=5):
    params = urllib.parse.urlencode(
        {"query.bibliographic": q, "rows": rows, "select": "title,DOI,container-title,issued,author,type"}
    )
    url = f"{ENDPOINT}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "sepsis-immunoparalysis-hub/1.0 (mailto:960856791@qq.com)"})
    with urllib.request.urlopen(req, timeout=45) as fh:
        data = json.load(fh)
    out = []
    for it in data.get("message", {}).get("items", []):
        title = (it.get("title") or [""])[0]
        journal = (it.get("container-title") or [""])[0]
        year = None
        issued = it.get("issued", {}).get("date-parts", [[None]])
        if issued and issued[0]:
            year = issued[0][0]
        authors = it.get("author") or []
        first = authors[0].get("family", "") if authors else ""
        out.append({"doi": it.get("DOI"), "title": title, "journal": journal, "year": year, "first_author": first,
                    "type": it.get("type")})
    return out


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for compound, qs in QUERIES.items():
        if only and only != compound:
            continue
        print("=" * 100)
        print(f"### {compound}")
        for q in qs:
            print(f"\n-- query: {q}")
            try:
                items = query(q)
            except Exception as exc:  # network / API hiccup
                print(f"   [query failed: {exc}]")
                continue
            for i, it in enumerate(items, 1):
                print(f"   [{i}] {it['year']} | {it['journal']} | {it['first_author']}")
                print(f"       {it['title'][:150]}")
                print(f"       DOI: {it['doi']}  ({it['type']})")
    print("=" * 100)


if __name__ == "__main__":
    main()
