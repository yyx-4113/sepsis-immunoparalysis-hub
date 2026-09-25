#!/usr/bin/env python
import json, urllib.request, ssl, time
ctx = ssl.create_default_context()
def get(url, retry=3):
    for i in range(retry):
        try:
            return json.loads(urllib.request.urlopen(url, timeout=120, context=ctx).read().decode("utf-8","ignore"))
        except Exception as e:
            last = repr(e)[:160]
            if i < retry-1:
                time.sleep(2); continue
            return {"__ERR__": last}

# 1) egene: list genes with significant cis-eQTL in Whole_Blood GTEX_v8 -> shows gencodeId format
url = "https://gtexportal.org/api/v2/association/egene?tissueSiteDetailId=Whole_Blood&datasetId=GTEX_v8&pageSize=5"
d = get(url)
print("=== egene (Whole_Blood, GTEX_v8) ===")
if "__ERR__" in d:
    print("  ERR:", d["__ERR__"])
else:
    print("  keys:", list(d.keys()))
    data = d.get("data", [])
    print("  sample:", data[:2])

# 2) retry singleTissueEqtl versioned + GTEX_v8 (transient SSL earlier)
G = "ENSG00000019582.14"
url2 = f"https://gtexportal.org/api/v2/association/singleTissueEqtl?datasetId=GTEX_v8&tissueSiteDetailId=Whole_Blood&gencodeId={G}"
d2 = get(url2, retry=4)
print("\n=== singleTissueEqtl versioned+GTEX_v8 ===")
if "__ERR__" in d2:
    print("  ERR:", d2["__ERR__"])
else:
    data2 = d2.get("data", [])
    print("  keys:", list(d2.keys()), "data len:", len(data2))
    if data2:
        print("  sample:", data2[0])
