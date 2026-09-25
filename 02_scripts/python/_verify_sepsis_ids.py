#!/usr/bin/env python
"""Verify the real sepsis GWAS ids (ieu-b-* + finn-b-AB1_SEPSIS) resolve in THIS OpenGWAS instance."""
import os, sys
import ieugwaspy
TOK = os.environ.get("OPENGWAS_JWT")
ieugwaspy.config.env["jwt"] = TOK
cands = ["ieu-b-4980","ieu-b-4981","ieu-b-4982","ieu-b-5086","ieu-b-5088",
         "finn-b-AB1_SEPSIS","finn-b-AB1_STREPTO_SEPSIS","finn-b-AB1_OTHER_SEPSIS",
         "finn-b-SEPTICHE_PNEUMONIA","finn-b-PNEUMO_SEPTHICHE","finn-b-O15_PUERP_SEPSIS"]
print("=== verify sepsis outcome ids ===")
ok = []
for c in cands:
    try:
        r = ieugwaspy.gwasinfo([c])
        if r:
            tr = r[0].get("trait"); ncase=r[0].get("ncase"); nctrl=r[0].get("ncontrol")
            nsnp=r[0].get("nsnp"); pmid=r[0].get("pmid")
            print(f"  OK   {c:26s} trait={tr!r} ncase={ncase} nctrl={nctrl} nsnp={nsnp} pmid={pmid}")
            ok.append(c)
        else:
            print(f"  NONE {c:26s}")
    except Exception as e:
        print(f"  ERR  {c:26s} {repr(e)[:100]}")
print("\nRESOLVED:", ok)
