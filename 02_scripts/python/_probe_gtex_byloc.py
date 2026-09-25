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

# CD74 coords from gene endpoint: chr5, 150401637-150412929
CHR, START, END = "chr5", 150401637, 150412929
url = (f"https://gtexportal.org/api/v2/association/singleTissueEqtlByLocation"
       f"?datasetId=gtex_v8&tissueSiteDetailId=Whole_Blood&chromosome={CHR}"
       f"&start={START}&end={END}")
d = get(url)
print("=== ByLocation CD74 ===")
if "__ERR__" in d:
    print("  ERR:", d["__ERR__"])
else:
    data = d.get("data", [])
    print("  keys:", list(d.keys()), "data len:", len(data))
    if data:
        print("  sample:", data[0])
        print("  variantIds:", [x.get("variantId") for x in data[:5]])
        print("  rsids:", [x.get("rsid") for x in data[:5]])
