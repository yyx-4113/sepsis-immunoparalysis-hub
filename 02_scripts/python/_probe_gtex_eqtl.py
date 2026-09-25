#!/usr/bin/env python
import json, urllib.request
def get(url):
    try:
        d = json.loads(urllib.request.urlopen(url, timeout=120).read().decode("utf-8","ignore"))
        return d
    except Exception as e:
        return {"__ERR__": repr(e)[:160]}

G = "ENSG00000019582.14"
GU = "ENSG00000019582"
base = "https://gtexportal.org/api/v2/association/singleTissueEqtl"
combos = [
    f"{base}?datasetId=GTEX_v8&tissueSiteDetailId=Whole_Blood&gencodeId={G}",
    f"{base}?tissueSiteDetailId=Whole_Blood&gencodeId={G}",
    f"{base}?datasetId=GTEX_v8&tissueSiteDetailId=Whole_Blood&gencodeId={GU}",
    f"{base}?tissueSiteDetailId=Whole_Blood&gencodeId={GU}",
    f"{base}?datasetId=GTEX_v8&tissueSiteDetailId=Whole_Blood&geneId={G}",
    f"{base}?tissueSiteDetailId=Whole_Blood&geneId={G}",
]
for url in combos:
    d = get(url)
    print(f"\nURL: {url}")
    if "__ERR__" in d:
        print("  ERR:", d["__ERR__"]); continue
    if isinstance(d, dict):
        data = d.get("data")
        print("  keys:", list(d.keys()))
        if isinstance(data, list):
            print(f"  data len: {len(data)}; sample: {data[:1]}")
        else:
            print("  data:", str(data)[:200])
