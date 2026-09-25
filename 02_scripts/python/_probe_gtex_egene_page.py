#!/usr/bin/env python
import json, urllib.request, ssl, time
ctx = ssl.create_default_context()
def get(url, retry=4):
    for i in range(retry):
        try:
            return json.loads(urllib.request.urlopen(url, timeout=120, context=ctx).read().decode("utf-8","ignore"))
        except Exception as e:
            last = repr(e)[:160]
            if i < retry-1: time.sleep(2); continue
            return {"__ERR__": last}

HUB = ["CD74","HLA-DQA1","CD14","FCGR3A","HAVCR2","FIS1"]
# Page through egene (gtex_v8, Whole_Blood) to build symbol->storage gencodeId
symbol2gid = {}
page, size = 0, 1000
print("=== paging egene ===")
while True:
    url = (f"https://gtexportal.org/api/v2/association/egene?datasetId=gtex_v8"
           f"&tissueSiteDetailId=Whole_Blood&page={page}&itemsPerPage={size}")
    d = get(url)
    if "__ERR__" in d:
        print("  ERR paging:", d["__ERR__"]); break
    data = d.get("data", [])
    if not data:
        print(f"  page {page}: empty, stop"); break
    for g in data:
        sym = (g.get("geneSymbol") or "").upper()
        symbol2gid[sym] = g.get("gencodeId")
    print(f"  page {page}: +{len(data)} (total {len(symbol2gid)})")
    page += 1
    if page > 40:
        print("  safety stop at 40 pages"); break

print("\n=== hub genes found in egene ===")
for sym in HUB:
    gid = symbol2gid.get(sym.upper())
    if not gid:
        print(f"  {sym}: NOT in egene list"); continue
    # fetch cis-eQTL with storage gencodeId
    d2 = get(f"https://gtexportal.org/api/v2/association/singleTissueEqtl"
             f"?datasetId=gtex_v8&tissueSiteDetailId=Whole_Blood&gencodeId={gid}")
    if "__ERR__" in d2:
        print(f"  {sym} ({gid}) cis-eQTL ERR: {d2['__ERR__']}"); continue
    eqtl = d2.get("data", [])
    print(f"  {sym} ({gid}): cis-eQTL count = {len(eqtl)}")
