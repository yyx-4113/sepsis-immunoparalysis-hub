#!/usr/bin/env python
import json, urllib.request
ctx = None  # GTEx uses valid cert
def get(url):
    try:
        return json.loads(urllib.request.urlopen(url, timeout=120).read().decode("utf-8","ignore"))
    except Exception as e:
        return {"__ERR__": repr(e)[:200]}

sym = "CD74"
for url in [
    f"https://gtexportal.org/api/v2/reference/geneSearch?gene={sym}",
    f"https://gtexportal.org/api/v2/reference/gene?geneSymbol={sym}",
    f"https://gtexportal.org/api/v2/reference/gene?geneId={sym}",
    f"https://gtexportal.org/api/v2/reference/geneSearch?gene={sym}&pageSize=10",
]:
    d = get(url)
    print(f"\nURL: {url}")
    if "__ERR__" in d:
        print("  ERR:", d["__ERR__"]); continue
    # print top-level keys / structure
    if isinstance(d, dict):
        for k in d:
            v = d[k]
            if isinstance(v, list):
                print(f"  key={k} (list len {len(v)}): sample={v[:1]}")
            else:
                print(f"  key={k}: {str(v)[:120]}")
    else:
        print("  type:", type(d), str(d)[:200])
