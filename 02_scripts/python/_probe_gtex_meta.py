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

print("=== metadata/dataset ===")
d = get("https://gtexportal.org/api/v2/metadata/dataset")
if "__ERR__" in d:
    print("  ERR:", d["__ERR__"])
else:
    print(json.dumps(d, indent=2)[:1500])

print("\n=== egene without datasetId (find CD74 gencodeId) ===")
d2 = get("https://gtexportal.org/api/v2/association/egene?tissueSiteDetailId=Whole_Blood&pageSize=500")
if "__ERR__" in d2:
    print("  ERR:", d2["__ERR__"])
else:
    data = d2.get("data", [])
    print("  total egenes returned (capped 500):", len(data))
    for g in data:
        if (g.get("geneSymbol") or "").upper() == "CD74":
            print("  CD74 egene entry:", json.dumps(g))
    # show a sample gencodeId format
    if data:
        print("  sample gencodeId:", data[0].get("gencodeId"), data[0].get("geneSymbol"))
