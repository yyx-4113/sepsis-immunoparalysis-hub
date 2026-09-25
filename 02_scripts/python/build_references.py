# ============================================================
# build_references.py
# 扩增稿件参考文献：内置 DOI 清单 -> Crossref 核实元数据 ->
# 按 Vancouver 格式排版 -> 输出 generated_references.md + audit csv
# 所有 DOI 必须命中 Crossref，禁止凭记忆写入（溯源纪律）
# ============================================================
import json, sys, time, urllib.request, urllib.error, re, html

API = "https://api.crossref.org/works/"
UA = "sepsis-immunoparalysis-hub/1.0 (mailto:960856791@qq.com)"

# 选定文献 DOI 清单（分组仅用于审计，最终按第一作者姓氏字母排序）
DOIS = [
    # --- Background / immunoparalysis ---
    "10.1038/nri3552",            # Hotchkiss 2013 Nat Rev Immunol - sepsis-induced immunosuppression review
    "10.1001/jama.2011.1829",      # Boomer 2011 JAMA - immunosuppression in sepsis deaths
    "10.1038/nri.2017.36",         # van der Poll 2017 Nat Rev Immunol - immunopathology
    "10.1001/jama.2016.0287",      # Singer 2016 JAMA - Sepsis-3 definition
    "10.1016/S2213-2600(17)30294-1",  # Scicluna 2017 Lancet Respir Med - MARS endotypes
    "10.1016/s2213-2600(16)00046-1",  # Davenport 2016 Lancet Respir Med - MARS host-response / E-MTAB-4451 source
    # --- Methods ---
    "10.1186/1471-2105-9-559",     # Langfelder 2008 BMC Bioinformatics - WGCNA
    "10.1093/nar/gkv007",          # Ritchie 2015 NAR - limma
    "10.1016/j.cell.2017.10.049",  # Subramanian 2017 Cell - LINCS L1000 connectivity
    "10.1038/nmeth.3337",          # Newman 2015 Nat Methods - CIBERSORT
    "10.1038/s41587-019-0114-2",   # Newman 2019 Nat Biotechnol - CIBERSORTx
    "10.1186/s13059-017-1349-1",   # Aran 2017 Genome Biol - xCell
    # --- MR / genetic validation ---
    "10.1093/ije/dyv080",          # Bowden 2015 IJE - MR-Egger (invalid instruments)
    "10.7554/elife.34408",         # Hemani 2018 eLife - MR-Base platform
    "10.1093/ije/dyw220",          # Bowden 2016 IJE - MR-Egger
    "10.1002/sim.5925",            # Burgess 2013 Stat Med - IVW
    "10.1038/s41588-018-0099-7",   # Verbanck 2018 Nat Genet - MR-PRESSO
    # --- Drug candidate evidence ---
    "10.1172/jci.insight.98960",   # IL-7 sepsis immunotherapy trial
    "10.1164/rccm.200903-0363OC",  # Meisel 2009 AJRCCM - GM-CSF sepsis RCT
    "10.4049/jimmunol.130.4.1492", # Basham 1983 J Immunol - IFN-gamma HLA-DR
    "10.1038/nm0697-678",          # Docke 1997 Nat Med - IFN-gamma restores monocyte function
    "10.1126/science.aaf1098",     # Netea 2016 Science - trained immunity
    "10.1016/j.chom.2011.04.006",  # Netea 2011 Cell Host Microbe - trained immunity
    "10.1016/j.pharmthera.2014.03.003",  # Parnham 2014 Pharmacol Ther - macrolide immunomodulation
    "10.1038/leu.2011.359",        # Lenalidomide immunomodulation
    "10.1016/j.ijid.2014.12.032",  # Thymosin alpha1 sepsis
    # --- Data availability / reproducibility ---
    "10.1093/nar/30.1.207",        # Edgar 2002 NAR - GEO
    "10.1093/nar/gky964",          # Athar 2019 NAR - ArrayExpress update
    "10.3389/fimmu.2023.1152117",  # Peng 2023 Front Immunol - IRG 3-gene signature
]

def initials(given):
    if not given:
        return ""
    parts = given.replace(".", " ").split()
    return "".join(p[0].upper() for p in parts if p)

def fetch(doi):
    url = API + doi
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.load(r).get("message", {})
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}"}
    except Exception as e:
        return {"_error": str(e)}

def vancouver(m):
    err = m.get("_error")
    if err:
        return None, err
    title = (m.get("title") or [""])[0].rstrip(".")
    title = html.unescape(re.sub(r"<[^>]+>", "", title))
    cont = (m.get("container-title") or [""])[0]
    cont = html.unescape(re.sub(r"<[^>]+>", "", cont))
    y = (m.get("issued") or {}).get("date-parts", [[None]])[0][0]
    vol = m.get("volume", "")
    iss = m.get("issue", "")
    page = m.get("page") or m.get("article-number") or ""
    doi = m.get("DOI", "")
    auth = m.get("author", [])
    names = []
    for a in auth[:6]:
        fam = a.get("family", "")
        ini = initials(a.get("given", ""))
        names.append(f"{fam} {ini}".strip())
    if len(auth) > 6:
        names.append("et al.")
    elif not names and auth:
        names.append("et al.")
    author_str = ", ".join(names) if names else "Anonymous"
    sep = " " if names and names[-1] == "et al." else ". "
    issue_str = f"({iss})" if iss else ""
    cit = f"{author_str}{sep}{title}. {cont}. {y};{vol}{issue_str}:{page}. doi:{doi}"
    return cit, None

def main():
    rows = []
    cites = []
    for doi in DOIS:
        m = fetch(doi)
        cit, err = vancouver(m)
        if cit:
            cites.append(cit)
            rows.append((doi, "OK", cit.split('.')[0]))
        else:
            rows.append((doi, "FAIL", err))
        time.sleep(0.12)
    # sort alphabetically by first author surname (first token of citation)
    def sortkey(c):
        return c.split(". ")[0].split()[-1].lower() if ". " in c else c.lower()
    cites.sort(key=sortkey)
    out_md = "## References (Vancouver; all DOIs verified via Crossref)\n\n"
    for i, c in enumerate(cites, 1):
        out_md += f"{i}. {c}\n"
    with open("03_results/generated_references.md", "w", encoding="utf-8") as f:
        f.write(out_md)
    audit = "doi,status,note\n"
    for d, s, n in rows:
        audit += f"{d},{s},{n}\n"
    with open("03_results/reference_doi_audit.csv", "w", encoding="utf-8") as f:
        f.write(audit)
    ok = sum(1 for _, s, _ in rows if s == "OK")
    print(f"Total: {len(DOIS)}  OK: {ok}  FAIL: {len(DOIS)-ok}")
    for d, s, n in rows:
        if s != "OK":
            print(f"  FAIL {d}: {n}")
    print(f"Wrote 03_results/generated_references.md ({len(cites)} entries) and reference_doi_audit.csv")

if __name__ == "__main__":
    main()
