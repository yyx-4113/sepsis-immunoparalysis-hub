# -*- coding: utf-8 -*-
"""A3 independent recomputation of every headline number in the manuscript.
Does NOT trust check_audit_assertions.py; re-derives each number from raw CSVs.
"""
import os, math, csv
import numpy as np
import pandas as pd
import scipy.stats as st

ROOT = r"D:/2026.9/极速交付9月会员日优惠套路/05_多组学+虚拟敲除药物发现/方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位"
RES = os.path.join(ROOT, "03_results")
OUT = []
def log(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s)

# ---------------------------------------------------------------
# 1) SAMPLE COUNTS + DEG COUNTS
# ---------------------------------------------------------------
# 802/760/42 from phenotype
pheno = os.path.join(ROOT, "01_data", "GSE65682", "GSE65682_pheno.csv")
if os.path.exists(pheno):
    ph = pd.read_csv(pheno)
    log("PHENO cols:", list(ph.columns)[:12])
    # try to count sepsis/healthy
    for col in ph.columns:
        if ph[col].astype(str).str.lower().str.contains("group|sepsis|ctrl|healthy|endotype").any():
            pass
    # heuristic
    n_total = len(ph)
    log("PHENO total rows:", n_total)
    # count by group column
    grpcol = [c for c in ph.columns if c.lower() in ("group","gse65682_group","characteristics_ch1.1","sample_type") or "group" in c.lower()]
    log("group-like cols:", grpcol)
    for c in grpcol:
        vc = ph[c].astype(str).str.lower().value_counts()
        log("  ", c, dict(vc))
else:
    log("PHENO file NOT FOUND at", pheno)

# Mars1 DEG count from S01_mars1_deg.csv
deg = pd.read_csv(os.path.join(RES, "S01_mars1_deg.csv"))
n_deg03 = int((deg["DEG_0.3"] == True).sum())
n_deg10 = int((deg["DEG_1.0"] == True).sum())
log("\n[S01_mars1_deg] rows:", len(deg), "| DEG_0.3=True:", n_deg03, "| DEG_1.0=True:", n_deg10)
log("  manuscript claims Mars1 DEG = 3597 (>=0.3). Recomputed:", n_deg03)

# sepsis vs healthy
svc = pd.read_csv(os.path.join(RES, "S01_deg_sepsis_vs_ctrl.csv"))
n_svc = int((svc["DEG_0.3"] == True).sum())
log("  [S01_deg_sepsis_vs_ctrl] DEG_0.3=True:", n_svc, "(manuscript claims 448)")

# consensus immune direction
imm = pd.read_csv(os.path.join(RES, "S01_immunoparalysis_direction.csv"))
n_down = int((imm["direction"] == "Mars1_down").sum())
n_up = int((imm["direction"] == "Mars1_up").sum())
n_fdr = int((imm["adj.P.Val"] < 0.05).sum())
n_both = int(((imm["direction"] == "Mars1_down") & (imm["adj.P.Val"] < 0.05)).sum())
log("\n[S01_immunoparalysis_direction] total genes:", len(imm))
log("  Mars1_down:", n_down, "| Mars1_up:", n_up)
log("  FDR<0.05 (any direction):", n_fdr)
log("  both down & FDR<0.05:", n_both)
log("  manuscript claims 23/25 down, 22/25 FDR-sig (incl PDCD1 up), 21 both-down+significant")

# ---------------------------------------------------------------
# 2) TABLE 1 effect sizes & signs
# ---------------------------------------------------------------
log("\n=== TABLE 1 effect sizes (recomputed vs manuscript) ===")
t1 = {
 "HLA-DRB1":(-0.89,1.1e-15), "CD74":(-0.76,2.1e-15),
 "CD14":(-0.77,1e-300), "FCGR3A":(-0.61,9.1e-11),
 "HAVCR2":(-0.35,2.8e-13), "PDCD1":(0.16,3.0e-10),
}
for g,(mlfc,map_) in t1.items():
    r = imm[imm["gene"]==g]
    if len(r)==0:
        log("  MISSING", g); continue
    r=r.iloc[0]
    log(f"  {g}: logFC={r['logFC']:.4f} (ms -0.? -> {mlfc}) adj.P={r['adj.P.Val']:.3e} (ms {map_:.1e}) dir={r['direction']} DEG_0.3={r['DEG_0.3']}")

# ---------------------------------------------------------------
# 3) IMMUNE SCORE MEDIANS
# ---------------------------------------------------------------
log("\n=== IMMUNE SCORE (S02) ===")
s02 = pd.read_csv(os.path.join(RES, "S02_immunoparalysis_score.csv"))
for e in ["Mars1","Mars2","Mars3","Mars4"]:
    sub = s02.loc[s02["mars_endotype"]==e,"immune_function_score"].dropna()
    log(f"  {e}: n={len(sub)} median={sub.median():.4f}")
# Mann-Whitney vs Mars1
g1 = s02.loc[s02["mars_endotype"]=="Mars1","immune_function_score"].dropna().values
claims = {"Mars2":0.47,"Mars3":1.9e-18,"Mars4":1.3e-3}
for e,pstated in claims.items():
    gx = s02.loc[s02["mars_endotype"]==e,"immune_function_score"].dropna().values
    u,p = st.mannwhitneyu(g1,gx,alternative="two-sided")
    log(f"  Mars1 vs {e}: MWU P={p:.4e} (manuscript {pstated})")

# ---------------------------------------------------------------
# 4) SIGNATURE AUC
# ---------------------------------------------------------------
log("\n=== SIGNATURE AUC ===")
s06 = pd.read_csv(os.path.join(RES,"S06_auc_compare.csv"))
for _,r in s06.iterrows():
    log(f"  {r['model']}: {r['auc']:.4f}")
ext = pd.read_csv(os.path.join(RES,"09_external_validation.csv"))
ext_idx = ext.set_index("metric")["value"]
def ev(k):
    return float(ext_idx[k])
log("  external orientedSum AUC:", round(ev("auc_EMTAB4451_orientedSum"),4),
    "CI", round(ev("auc_EMTAB4451_orientedSum_CI95_low"),4),"-",round(ev("auc_EMTAB4451_orientedSum_CI95_high"),4))
log("  external L1-locked AUC:", round(ev("auc_EMTAB4451_external_locked"),4),
    "CI", round(ev("auc_EMTAB4451_external_CI95_low"),4),"-",round(ev("auc_EMTAB4451_external_CI95_high"),4))
log("  discovery CV locked (09 csv):", round(ev("auc_GSE65682_CV_locked"),4))
log("  n_validated_samples:", int(ev("n_validated_samples")), "n_deaths:", int(ev("n_deaths")), "mapped:", int(ev("n_signature_genes_mapped_EMTAB4451")),"/",int(ev("n_signature_genes_total")))

# ---------------------------------------------------------------
# 5) DRUG SHORTLIST (Table 2) + IFN-gamma 4/5
# ---------------------------------------------------------------
log("\n=== DRUG SHORTLIST (Table 2) ===")
drugs = pd.read_csv(os.path.join(RES,"08_candidates_drugs.csv"))
for _,r in drugs.iterrows():
    log(f"  {r['compound']}: n_target={r['n_target_genes']} n_rescue={r['n_rescue_mars1down']} frac={r['rescue_fraction']} genes={r['rescue_genes']}")
# IFN-gamma 4/5 antigen-presentation recompute
ifng = drugs[drugs["compound"]=="IFN-gamma"].iloc[0]
ap_set = {"HLA-DRA","HLA-DRB1","HLA-DQA1","HLA-DQB1","CD74"}  # antigen-presentation subset
rescued = set(str(ifng["rescue_genes"]).split(";"))
ap_rescued = ap_set & rescued
log(f"  IFN-gamma antigen-presentation set={ap_set}")
log(f"  IFN-gamma rescued genes={rescued}")
log(f"  IFN-gamma AP rescued = {ap_rescued} -> {len(ap_rescued)}/5")
log(f"  HLA-DQB1 DEG_0.3 in S01? {bool((imm[imm['gene']=='HLA-DQB1']['DEG_0.3']==True).any())}")
log(f"  IFN-gamma overall concordance = {ifng['n_rescue_mars1down']}/{ifng['n_target_genes']} = {ifng['rescue_fraction']}")

# ---------------------------------------------------------------
# 6) LINCS L1000
# ---------------------------------------------------------------
log("\n=== LINCS L1000 (S08_l1000_candidate_scores) ===")
l1 = pd.read_csv(os.path.join(RES,"S08_l1000_candidate_scores.csv"))
for _,r in l1.iterrows():
    rescue=float(r["rescue_score"]); wtcs=float(r["wtcs"]); rank=int(r["rescue_rank"]); pct=float(r["rescue_pct_rank"])
    sq22 = rescue*math.sqrt(22)
    log(f"  {r['candidate']}: rescue={rescue} wtcs={wtcs} rank={rank} pct={pct}")
    log(f"     wtcs/rescue = {wtcs/rescue:.4f} ; sqrt(22)={math.sqrt(22):.4f} ; rescue*sqrt22={sq22:.4f}")
    log(f"     rank/total check: if total=20413 -> {rank/20413:.5f} (csv pct={pct})")

# total trt_cp compounds
trtcp = os.path.join(RES,"S08_l1000_rescue_trtcp.csv")
if os.path.exists(trtcp):
    with open(trtcp) as f:
        nrows = sum(1 for _ in f) - 1
    log(f"  S08_l1000_rescue_trtcp.csv rows (compounds): {nrows}")

# ---------------------------------------------------------------
# 7) MR TABLE 3 Egger p (t-dist) + OR/CI + IVW
# ---------------------------------------------------------------
log("\n=== MR Table 3 (28d death) recompute ===")
mr = pd.read_csv(os.path.join(RES,"10_genetics_mr_outcome5086_28ddeath.csv"))
for _,r in mr.iterrows():
    if r["method"] not in ("IVW","MR-Egger","Weighted median"): continue
    if pd.isna(r["beta"]):
        log(f"  {r['gene']} {r['method']}: not assessed (nsnp={r['nsnp']})")
        continue
    b=float(r["beta"]); s=float(r["se"]); nsnp=int(r["nsnp"]); p=float(r["p"])
    OR=float(r["or_"]); lo=float(r["ci_lo"]); hi=float(r["ci_hi"])
    if r["method"]=="MR-Egger":
        df=nsnp-2
        p_t = 2*st.t.sf(abs(b)/s, df)
        p_norm = 2*(1-st.norm.cdf(abs(b)/s))
        log(f"  {r['gene']} Egger: stored P={p:.4e} | t-dist(df={df}) P={p_t:.4e} | normal P={p_norm:.4e} | match_t={abs(p_t-p)<1e-9}")
    or_ok = abs(math.exp(b)-OR)<1e-3 and abs(math.exp(b-1.96*s)-lo)<1e-3 and abs(math.exp(b+1.96*s)-hi)<1e-3
    log(f"  {r['gene']} {r['method']}: OR={OR:.4f} CI=({lo:.3f},{hi:.3f}) P={p:.4e} | exp(b)={math.exp(b):.4f} OR/CI-consistent={or_ok}")

# min primary IVW P
ivw = mr[mr["method"]=="IVW"]
log("  primary-outcome min IVW P =", float(ivw["p"].min()), "(ms claims >=0.23)")

# BH family
fam = pd.read_csv(os.path.join(RES,"10_mr_bh_family.csv"))
log("\n  BH family rows:", len(fam), "(expected 45)")
red = int((fam["family_sig_q<0.05"].astype(str).str.upper()=="YES").sum())
log("  family-sig YES:", red)
cd74 = fam[(fam["gene"]=="CD74")&(fam["method"]=="Weighted median")&(fam["outcome"].astype(str).str.contains("crit",case=False))]
if len(cd74):
    log("  CD74 crit-care WM q_family:", float(cd74["q_family_45test"].iloc[0]))

# critical care file CD74 Egger SE ordering
cc = pd.read_csv(os.path.join(RES,"10_genetics_mr_outcome4982_criticalcare.csv"))
cd74cc = cc[(cc["gene"]=="CD74")]
log("\n  === CD74 critical-care MR ===")
for _,r in cd74cc.iterrows():
    if pd.isna(r["se"]): continue
    log(f"    {r['method']}: beta={r['beta']:.4f} se={float(r['se']):.4f} OR={float(r['or_']):.4f} P={float(r['p']):.4e} nsnp={int(r['nsnp'])}")

# ---------------------------------------------------------------
# WRITE LOG
# ---------------------------------------------------------------
with open(os.path.join(ROOT,"05_reports","review_r10","A3_recompute_log.txt"),"w",encoding="utf-8") as f:
    f.write("\n".join(OUT))
log("\n[written A3_recompute_log.txt]")
