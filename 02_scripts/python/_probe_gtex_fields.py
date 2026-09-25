#!/usr/bin/env python
import json, urllib.request, ssl
ctx = ssl.create_default_context()
d = json.loads(urllib.request.urlopen(
    "https://gtexportal.org/api/v2/association/singleTissueEqtl?datasetId=gtex_v8&tissueSiteDetailId=Whole_Blood&gencodeId=ENSG00000196735.11",
    timeout=120, context=ctx).read().decode("utf-8","ignore"))
data = d.get("data", [])
print("count:", len(data))
if data:
    r = data[0]
    print("ALL KEYS:", list(r.keys()))
    print("sample:", json.dumps(r, indent=2))
