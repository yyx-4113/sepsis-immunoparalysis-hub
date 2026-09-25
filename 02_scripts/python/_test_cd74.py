#!/usr/bin/env python
"""End-to-end validation of S10 pipeline for CD74 only."""
import os, sys, json
import ieugwaspy, pandas as pd, numpy as np
from scipy import stats
TOK = os.environ.get("OPENGWAS_JWT")
ieugwaspy.config.env["jwt"] = TOK

import importlib.util
spec = importlib.util.spec_from_file_location("m", "02_scripts/python/10_genetics_mr_run.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

sym = "CD74"
gid = m.resolve_gencode(sym)
print("gencodeId:", gid)
eqtl = m.gtex_cis_eqtl(gid)
print("cis-eQTL rows:", len(eqtl))
if not eqtl:
    sys.exit("no cis-eQTL")

exp = m.parse_exposure(eqtl).sort_values("pval").head(50)
print("exposure instruments (top50):", len(exp))
print(exp.head(3).to_string())
rsids = exp.rsid.tolist()
print("sample rsids:", rsids[:5])

odf = m.outcome_stats("ieu-b-4980", rsids)
out = m.parse_outcome(odf)
print("outcome SNPs retrieved:", len(out))
print(out.head(3).to_string())

row, merged = m.run_mr(exp, out)
if row is None:
    print("MR FAILED:", merged)
else:
    print("MR RESULT:", json.dumps(row, indent=2))
