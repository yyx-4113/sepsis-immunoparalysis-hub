#!/usr/bin/env python
import json, urllib.request, ssl
ctx = ssl.create_default_context()
for gid in ["ENSG00000196735.11", "ENSG00000170458.13"]:
    url = (f"https://gtexportal.org/api/v2/association/dyneqtl"
           f"?datasetId=gtex_v8&tissueSiteDetailId=Whole_Blood&gencodeId={gid}")
    try:
        d = json.loads(urllib.request.urlopen(url, timeout=120, context=ctx).read().decode("utf-8","ignore"))
    except Exception as e:
        print(f"  {gid} ERR: {repr(e)[:160]}"); continue
    print(f"\n=== dyneqtl {gid} ===")
    print("  top keys:", list(d.keys()) if isinstance(d, dict) else type(d))
    # find the data list
    data = d.get("data") if isinstance(d, dict) else None
    if data is None:
        # maybe data is the whole thing
        data = d if isinstance(d, list) else []
    print("  data len:", len(data) if isinstance(data, list) else "n/a")
    if isinstance(data, list) and data:
        print("  ALL KEYS:", list(data[0].keys()))
        print("  sample:", json.dumps(data[0], indent=2)[:600])
