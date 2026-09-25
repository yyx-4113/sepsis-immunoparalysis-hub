# ============================================================
# 00_geo_download.py — 解析本地 GSE65682_family.soft.gz（curl 已下载）
# 运行： python 02_scripts/python/00_geo_download.py
# 前置： 01_data/GSE65682/GSE65682_family.soft.gz
# 产出： GSE65682_expr.csv(基因x样本) / GSE65682_pheno.csv / gse65682_pdata_inspect.csv
# 注：真实平台 GPL13667，802 样本(760 ICU + 42 健康)；GEOparse 自带下载器本机坏掉，故 curl+本地解析
# ============================================================
import os, re
import numpy as np, pandas as pd
import GEOparse

PROJ = "D:/2026.9/极速交付9月会员日优惠套路/05_多组学+虚拟敲除药物发现/方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位"
DATA = os.path.join(PROJ, "01_data", "GSE65682")
REP  = os.path.join(PROJ, "05_reports")
os.makedirs(REP, exist_ok=True)
FAM = os.path.join(DATA, "GSE65682_family.soft.gz")
assert os.path.exists(FAM), f"缺少 {FAM}"

print(">>> 本地解析 ...", flush=True)
gse = GEOparse.get_GEO(filepath=FAM, annotate_gpl=False)
print("样本数:", len(gse.gsms), flush=True)

# 表达矩阵：pivot_samples 返回 探针 x 样本（index=probe, columns=sample）
expr = gse.pivot_samples("VALUE")
if set(expr.index) <= set(gse.gsms.keys()):   # index 是样本 -> 需要转置
    expr = expr.T
print("原始表达矩阵:", expr.shape, flush=True)

# 探针 -> 基因符号（family soft 含 GPL 注释）
gpl_id = list(gse.gpls.keys())[0]
gpl = gse.gpls[gpl_id]
gpl_tbl = gpl.table
sym_col = [c for c in gpl_tbl.columns if re.search("symbol", c, re.I)][0]
print("GPL:", gpl_id, "| 注释列:", sym_col, flush=True)
probe2sym = dict(zip(gpl_tbl["ID"].astype(str), gpl_tbl[sym_col].astype(str)))
def first_sym(s):
    if not isinstance(s, str) or s.strip() in ("", "---", "NA"): return None
    return s.split(";")[0].split("/")[0].strip()
expr.index = [first_sym(probe2sym.get(str(p), "")) for p in expr.index]
expr = expr[expr.index.notna()]; expr.index.name = "gene"
expr = expr.groupby(level=0).mean()
print("基因级表达矩阵:", expr.shape, flush=True)
expr.to_csv(os.path.join(DATA, "GSE65682_expr.csv"))

# 表型
pheno = gse.phenotype_data.copy()
pheno.insert(0, "sample", pheno.index)
insp = [{"variable":c, "n_unique":pheno[c].astype(str).nunique(),
         "example":" | ".join(list(pheno[c].astype(str).unique()[:3]))} for c in pheno.columns]
pd.DataFrame(insp).to_csv(os.path.join(REP,"gse65682_pdata_inspect.csv"), index=False)
pheno.to_csv(os.path.join(DATA,"GSE65682_pheno_raw.csv"), index=False)
print("pData 列:", list(pheno.columns), flush=True)

# 打印关键列取值（核对真实编码）
for col in pheno.columns:
    if any(k in col.lower() for k in ["endotype","mortal","gender","age","source_name","abdominal","cohort","pneumonia","control"]):
        vals = pheno[col].astype(str)
        print(f"  [{col}] unique({vals.nunique()}): {list(vals.unique()[:8])}", flush=True)

end_col = "characteristics_ch1.5.endotype_class"
mort_col = "characteristics_ch1.6.mortality_event_28days"
abdo_col = "characteristics_ch1.11.abdominal_sepsis_and_controls"

out = pd.DataFrame({"sample":pheno["sample"]})
if end_col in pheno.columns:
    ec = pheno[end_col].astype(str).str.strip()
    out["mars_endotype"] = ec.where(ec.str.contains("Mars[1-4]", case=False, na=False), other="")
    out["mars_endotype"] = out["mars_endotype"].replace({"":np.nan})
if mort_col in pheno.columns:
    mv = pheno[mort_col].astype(str).str.strip()
    out["death_28d"] = np.where(mv.str.startswith("1"), "1", np.where(mv.str.startswith("0"), "0", ""))
    out["death_28d"] = out["death_28d"].replace({"":np.nan})
# group: 健康对照 = ctrl_GI（42 例）；其余为脓毒症（760 例）
if abdo_col in pheno.columns:
    is_healthy = pheno[abdo_col].astype(str).str.strip().eq("ctrl_GI")
else:
    is_healthy = pd.Series(False, index=pheno.index)
out["group"] = np.where(is_healthy, "healthy", "sepsis")
# 保留其它临床列
for c in pheno.columns:
    cl = c.lower()
    if any(k in cl for k in ["age","gender","sex","diabet","infection","thromb","apa","sofa","saps","follow","pneumonia","endotype_cohort"]):
        out[c.replace(" ","_").replace(",","")] = pheno[c].astype(str).str.strip()
out.to_csv(os.path.join(DATA,"GSE65682_pheno.csv"), index=False)
print("派生表型列:", list(out.columns), flush=True)
for c in ["group","mars_endotype","death_28d"]:
    if c in out:
        vc = out[c].value_counts(dropna=False)
        print("  ", c, ":", ", ".join(f"{k}={v}" for k,v in vc.items()), flush=True)
print(">>> 解析完成")
