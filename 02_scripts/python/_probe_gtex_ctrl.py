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

# (a) tissue list for gtex_v8
print("=== tissues for gtex_v8 (look for Whole_Blood) ===")
d = get("https://gtexportal.org/api/v2/dataset/tissueSiteDetail?datasetId=gtex_v8&pageSize=100")
if "__ERR__" in d:
    print("  ERR:", d["__ERR__"])
else:
    tissues = d.get("data", d.get("tissueSiteDetail", []))
    if isinstance(tissues, dict):
        tissues = tissues.get("data", [])
    names = [t.get("tissueSiteDetailId") or t.get("tissueSiteDetail") for t in tissues]
    print("  count:", len(names))
    for n in names:
        if n and ("blood" in n.lower() or "Blood" in n):
            print("   BLOOD TISSUE:", n)

# (b) control eGene WASH7P
print("\n=== control: singleTissueEqtl ENSG00000227232.5 (WASH7P) gtex_v8 Whole_Blood ===")
d2 = get("https://gtexportal.org/api/v2/association/singleTissueEqtl?datasetId=gtex_v8&tissueSiteDetailId=Whole_Blood&gencodeId=ENSG00000227232.5")
if "__ERR__" in d2:
    print("  ERR:", d2["__ERR__"])
else:
    data2 = d2.get("data", [])
    print("  data len:", len(data2))
    if data2:
        print("  sample:", json.dumps(data2[0])[:300])
