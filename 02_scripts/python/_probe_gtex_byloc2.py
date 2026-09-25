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

CHR, START, END = "chr5", 150401637, 150412929
url = (f"https://gtexportal.org/api/v2/association/singleTissueEqtlByLocation"
       f"?datasetId=gtex_v8&tissueSiteDetailId=Whole_Blood&chromosome={CHR}"
       f"&start={START}&end={END}")
d = get(url)
print("=== ByLocation CD74 (correct key) ===")
if "__ERR__" in d:
    print("  ERR:", d["__ERR__"])
else:
    eqtl = d.get("singleTissueEqtl", [])
    print("  keys:", list(d.keys()), "| singleTissueEqtl len:", len(eqtl))
    if eqtl:
        print("  sample:", json.dumps(eqtl[0]))
        print("  rsids:", [x.get("rsid") for x in eqtl[:6]])
