#!/usr/bin/env python
import json, urllib.request, ssl, time
ctx = ssl.create_default_context()
def get(url, retry=3):
    for i in range(retry):
        try:
            return json.loads(urllib.request.urlopen(url, timeout=120, context=ctx).read().decode("utf-8","ignore"))
        except Exception as e:
            last = repr(e)[:160]
            if i < retry-1: time.sleep(2); continue
            return {"__ERR__": last}

# gene-endpoint gencodeIds (from reference/gene)
gene_ids = {
    "CD74": "ENSG00000019582.14",
    "HLA-DQA1": None, "CD14": None, "FCGR3A": None, "HAVCR2": None, "FIS1": None,
}
# First resolve the other 5 symbols to gencodeId via reference/gene
for sym in ["HLA-DQA1","CD14","FCGR3A","HAVCR2","FIS1"]:
    d = get(f"https://gtexportal.org/api/v2/reference/gene?geneId={sym}")
    g = (d.get("data") or [{}])[0]
    gene_ids[sym] = g.get("gencodeId")
    print(f"  {sym}: {gene_ids[sym]}")

print("\n=== egene filter per hub gene (gtex_v8, Whole_Blood) ===")
for sym, gid in gene_ids.items():
    d = get(f"https://gtexportal.org/api/v2/association/egene?datasetId=gtex_v8&tissueSiteDetailId=Whole_Blood&gencodeId={gid}")
    if "__ERR__" in d:
        print(f"  {sym} ERR: {d['__ERR__']}"); continue
    data = d.get("data", [])
    found = [g for g in data if (g.get("geneSymbol") or "").upper()==sym.upper()]
    if found:
        print(f"  {sym}: egene gencodeId={found[0].get('gencodeId')}  (eGene present)")
    else:
        print(f"  {sym}: gencodeId {gid} NOT an eGene in Whole_Blood gtex_v8")
