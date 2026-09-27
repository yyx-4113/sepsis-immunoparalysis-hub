#!/usr/bin/env python3
# v1.19.0 — Round-18 evidence regeneration
# Produces corrected MR CSVs, recomputed BH family, calibration CI,
# SRS/age/sex benchmark, FIS1+hub death association, concordance binomial null.
import csv, math, os, json
import numpy as np
from scipy import stats

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/05_多组学+虚拟敲除药物发现/方案三_脓毒症免疫失调枢纽基因与虚拟敲除药物重定位/"
RES = ROOT + "03_results/"
ONE = "01_data/"

def tp(t, df):
    return 2.0 * stats.t.sf(abs(t), df)

# ---------------------------------------------------------------- 1) MR P-correction
mr_files = [("10_genetics_mr.csv","4980_suscept"),
            ("10_genetics_mr_outcome5086_28ddeath.csv","5086_28ddeath"),
            ("10_genetics_mr_outcome4982_criticalcare.csv","4982_criticalcare")]
mr_summary = []
for fn, outc in mr_files:
    path = RES + fn
    rows = list(csv.DictReader(open(path, encoding='utf-8')))
    for r in rows:
        if r['beta']=='' or r['se']=='':
            mr_summary.append((fn, r.get('gene',''), r.get('method',''), outc, float(r['or_']) if r['or_'] else float('nan'), r['p'], ''))
            continue
        ns = int(r['nsnp'])
        b = float(r['beta']); s = float(r['se'])
        method = r['method']
        if method == 'MR-Egger':
            p_new = tp(b/s, ns-2)          # already t in deposited CSV; confirm
            ref = f"t({ns-2})"
        else:  # IVW or Weighted median
            if method == 'Weighted median' and ns < 10:
                p_new = ""                 # degenerate bootstrap -> no P
            else:
                p_new = tp(b/s, ns-1)
            ref = f"t({ns-1})"
        r['p'] = f"{p_new:.6g}" if p_new != "" else ""
        r['p_refdist'] = ref
        r['outcome'] = outc
        if r['gene'] == 'CD74' and outc=='4982_criticalcare' and method == 'IVW':
            r['model'] = 'fixed'           # B2-13: Q<df so fixed, not random
        mr_summary.append((fn, r['gene'], method, outc, float(r['or_']),
                           r['p'], ref))
    # write back
    cols = list(rows[0].keys())
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    print("updated", fn, "rows", len(rows))

print("\n=== MR corrected P (IVW primary; WM blanked for nsnp<10) ===")
for item in mr_summary:
    if item[2] in ('IVW', 'Weighted median'):
        print(f"  {item[1]:9s} {item[2]:15s} {item[3]:16s} OR={item[4]:.3f} P={item[5]} ({item[6]})")

# ---------------------------------------------------------------- 2) BH family (15-test IVW primary)
# gather all rows across all outcome files, tag with outcome
allrows = []
for fn, outc in mr_files:
    for r in csv.DictReader(open(RES+fn, encoding='utf-8')):
        r['outcome'] = outc
        allrows.append(r)
# primary = IVW only (drop rows with insufficient instruments / empty p, e.g. FCGR3A)
prim = [r for r in allrows if r['method'] == 'IVW']
n_before = len(prim)
prim = [r for r in prim if r['p'] != '' and r['p'] is not None]
print(f"\nBH primary family: {len(prim)} IVW rows (dropped {n_before-len(prim)} with empty p)")
pv = np.array([float(r['p']) for r in prim])
q_bh = stats.false_discovery_control(pv, method='bh')
for r, q in zip(prim, q_bh):
    r['q_bh_15test'] = f"{q:.4g}"
    r['family_role'] = 'primary'
    r['sig_15test_q05'] = 'yes' if q < 0.05 else 'no'
# sensitivities = Egger / WM
for r in allrows:
    if r['method'] != 'IVW':
        r['family_role'] = 'sensitivity'
        r['q_bh_15test'] = ''
        r['sig_15test_q05'] = ''
# build family file fresh
fam_cols = ['gene','method','outcome','or_','p','p_refdist','family_role',
            'q_bh_15test','sig_15test_q05']
with open(RES+"10_mr_bh_family.csv",'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=fam_cols, extrasaction='ignore'); w.writeheader()
    for r in allrows: w.writerow(r)
minq = min(float(r['q_bh_15test']) for r in prim)
print(f"\n15-test IVW family: min q = {minq:.4g} -> family_sig = {'YES' if minq<0.05 else 'NO'}")
print("CD74 critical-care IVW corrected P =", [r['p'] for r in prim if r['gene']=='CD74' and 'crit' in r['outcome']][0])

# ---------------------------------------------------------------- 3) Calibration CI (IRLS logistic)
rs = list(csv.DictReader(open(RES+"09_ext_risk_scores.csv")))
y = np.array([int(r['y']) for r in rs], float)
z = (np.array([float(r['risk_oriented_sum']) for r in rs]) - np.mean([float(r['risk_oriented_sum']) for r in rs])) / np.std([float(r['risk_oriented_sum']) for r in rs])
# IRLS
b = np.zeros(2); X = np.column_stack([np.ones_like(y), z])
for _ in range(50):
    eta = X@b; pr = 1/(1+np.exp(-eta)); W = pr*(1-pr)
    grad = X.T@(y-pr); H = (X.T*(W@np.ones(1)) if False else X.T@(X*W[:,None]))
    b = b + np.linalg.solve(H+1e-9*np.eye(2), grad)
eta = X@b; pr = 1/(1+np.exp(-eta)); W = pr*(1-pr)
cov = np.linalg.inv(X.T@(X*W[:,None]))
se = np.sqrt(np.diag(cov))
a, bs = b[0], b[1]
se_a, se_b = se[0], se[1]
ci_a = (a-1.96*se_a, a+1.96*se_a); ci_b=(bs-1.96*se_b, bs+1.96*se_b)
p_slope1 = 2.0*(1-stats.norm.cdf(abs(bs-1)/se_b))  # Wald z-test slope=1
print(f"\nCalibration: intercept={a:.4f} SE={se_a:.4f} CI={ci_a}; slope={bs:.4f} SE={se_b:.4f} CI={ci_b}; P(slope=1)={p_slope1:.4g}")
# append columns to 09_ext_calibration_dca.csv
cal = list(csv.DictReader(open(RES+"09_ext_calibration_dca.csv")))
ccols = list(cal[0].keys())
for c in ['calib_intercept_se','calib_intercept_ci_lo','calib_intercept_ci_hi',
          'calib_slope_se','calib_slope_ci_lo','calib_slope_ci_hi','p_slope_eq_1']:
    if c not in ccols: ccols.append(c)
cal[0].update({'calib_intercept_se':f"{se_a:.4f}",'calib_intercept_ci_lo':f"{ci_a[0]:.3f}",
               'calib_intercept_ci_hi':f"{ci_a[1]:.3f}",'calib_slope_se':f"{se_b:.4f}",
               'calib_slope_ci_lo':f"{ci_b[0]:.3f}",'calib_slope_ci_hi':f"{ci_b[1]:.3f}",
               'p_slope_eq_1':f"{p_slope1:.4g}"})
with open(RES+"09_ext_calibration_dca.csv",'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=ccols); w.writeheader(); w.writerows(cal)

# ---------------------------------------------------------------- 4) SRS / age / sex benchmark
sdrf = ROOT+"01_data/E-MTAB-4451/E-MTAB-4451.sdrf.txt"
hr = open(sdrf,encoding='utf-8').readline().rstrip('\n').split('\t')
idx = {k:hr.index(k) for k in ['Source Name','Characteristics[28 day survival]',
      'Characteristics[sepsis response signature group]','Characteristics[sex]','Characteristics[age]']}
meta = {}
for line in open(sdrf,encoding='utf-8'):
    c=line.rstrip('\n').split('\t')
    if len(c)<=max(idx.values()): continue
    src=c[idx['Source Name']]
    is_dead = 1 if c[idx['Characteristics[28 day survival]']]=='non survivor' else 0
    srsg = c[idx['Characteristics[sepsis response signature group]']]
    sx = c[idx['Characteristics[sex]']]
    ag = c[idx['Characteristics[age]']]
    meta[src]={'death':is_dead,'srs':srsg,'sex':sx,'age':ag}
def auc_mw(scores, labels):
    # Mann-Whitney U based AUC with tie handling
    order=np.argsort(scores,kind='mergesort'); ranks=np.empty(len(scores)); 
    s_sorted=scores[order]
    r=1; i=0
    while i<len(scores):
        j=i
        while j+1<len(scores) and s_sorted[j+1]==s_sorted[i]: j+=1
        avg=(r+r+(j-i))/2.0; ranks[order[i:j+1]]=avg; r+= (j-i+1); i=j+1
    pos=labels==1; n1=pos.sum(); n0=len(labels)-n1
    Rpos=ranks[pos].sum()
    return (Rpos - n1*(n1+1)/2.0)/(n1*n0)
# join
samples=[]; ys=[]; srsv=[]; ages=[]; sexv=[]
for r in rs:
    m=meta.get(r['sample'])
    if not m or m['srs'] in ('NA',''): continue
    samples.append(r['sample']); ys.append(int(r['y']))
    srsv.append(int(m['srs'])); ages.append(float(m['age'])); sexv.append(m['sex'])
Ys=np.array(ys); SRS=np.array(srsv); AGE=np.array(ages); SEX=np.array([1 if s=='male' else 0 for s in sexv])
score=np.array([float(r['risk_oriented_sum']) for r in rs if meta.get(r['sample']) and meta[r['sample']]['srs'] not in ('NA','')])
# AUCs
auc_srs=auc_mw(SRS, Ys); auc_age=auc_mw(AGE, Ys); auc_sex=auc_mw(SEX, Ys); auc_score=auc_mw(score, Ys)
auc_srs_dir=max(auc_srs, 1-auc_srs)   # fair discriminant capacity (label orientation-agnostic)
print(f"\nBenchmark AUCs (n={len(Ys)}, deaths={Ys.sum()}):")
print(f"  SRS group : {auc_srs:.4f} (ordinal) / {auc_srs_dir:.4f} (direction-corrected)")
print(f"  age       : {auc_age:.4f}")
print(f"  sex       : {auc_sex:.4f}")
print(f"  score     : {auc_score:.4f}")
# permutation test score vs direction-corrected SRS (fair)
rng=np.random.default_rng(7); nperm=2000; obs=auc_score-auc_srs_dir; cnt=0
for _ in range(nperm):
    perm=np.random.permutation(Ys)
    a_s=auc_mw(score,perm); a_r=max(auc_mw(SRS,perm),1-auc_mw(SRS,perm))
    if abs(a_s-a_r)>=abs(obs): cnt+=1
p_perm=(cnt+1)/(nperm+1)
print(f"  ΔAUC(score - SRS_dir)={obs:+.4f}; permutation P={p_perm:.3g}")
# write benchmark csv
with open(RES+"09_ext_benchmark_vs_srs.csv",'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['comparator','n','deaths','auc','note'])
    w.writerow(['SRS group (Davenport endotype, ordinal)',len(Ys),int(Ys.sum()),f"{auc_srs:.4f}",f"SRS1 mortality {Ys[SRS==1].mean():.3f} ({int(Ys[SRS==1].sum())}/{int((SRS==1).sum())})"])
    w.writerow(['SRS group (direction-corrected)',len(Ys),int(Ys.sum()),f"{auc_srs_dir:.4f}",'max(AUC,1-AUC)'])
    w.writerow(['age',len(Ys),int(Ys.sum()),f"{auc_age:.4f}",''])
    w.writerow(['sex',len(Ys),int(Ys.sum()),f"{auc_sex:.4f}",''])
    w.writerow(['locked score (oriented sum)',len(Ys),int(Ys.sum()),f"{auc_score:.4f}",f"ΔAUC vs SRS_dir {obs:+.4f}, perm P {p_perm:.3g}"])

# ---------------------------------------------------------------- 5) FIS1 + 5 hubs death association (GSE65682)
pheno={}
for r in csv.DictReader(open(ONE+"GSE65682/GSE65682_pheno.csv",encoding='utf-8')):
    pheno[r['sample']]=r
# expr as dict gene->dict(sample->value)
hdr=None
exprmap={}
with open(ONE+"GSE65682/GSE65682_expr.csv",encoding='utf-8') as f:
    hdr=f.readline().strip().split(',')[1:]
    for line in f:
        parts=line.rstrip('\n').split(',')
        exprmap[parts[0]]=dict(zip(hdr,[float(x) for x in parts[1:]]))
samples=list(pheno.keys())
avail=[s for s in samples if pheno[s]['death_28d'] not in ('','NA','NaN')]
print(f"\nFIS1/hub death assoc: {len(avail)} samples with death_28d")
def logit_or_per_sd(vec, lab):
    vec=(vec-vec.mean())/vec.std()
    X=np.column_stack([np.ones(len(vec)),vec]); b=np.zeros(2)
    for _ in range(50):
        eta=X@b; pr=1/(1+np.exp(-eta)); W=pr*(1-pr)
        b=b+np.linalg.solve(X.T@(X*W[:,None])+1e-9*np.eye(2), X.T@(lab-pr))
    eta=X@b; pr=1/(1+np.exp(-eta)); W=pr*(1-pr); cov=np.linalg.inv(X.T@(X*W[:,None]))
    se=np.sqrt(np.diag(cov)); orr=math.exp(b[1]); ci=(math.exp(b[1]-1.96*se[1]),math.exp(b[1]+1.96*se[1])); p=tp(b[1]/se[1],len(vec)-2)
    rval=np.corrcoef(vec,lab)[0,1]
    return rval, orr, ci, p
# direction table
deg={}
for r in csv.DictReader(open(RES+"S01_mars1_deg.csv",encoding='utf-8')):
    deg[r['gene']]=float(r['logFC'])
mr28={}
for r in csv.DictReader(open(RES+"10_genetics_mr_outcome5086_28ddeath.csv",encoding='utf-8')):
    if r['method']=='IVW' and r['or_']!='': mr28[r['gene']]=float(r['or_'])
genes=['FIS1','CD74','HLA-DQA1','CD14','FCGR3A','HAVCR2']
out=[]
for g in genes:
    if g not in exprmap: continue
    lab=np.array([int(float(pheno[s]['death_28d'])) for s in avail])
    vec=np.array([exprmap[g][s] for s in avail])
    rv,orr,ci,p=logit_or_per_sd(vec,lab)
    pred = 'harmful' if deg.get(g,0)>0 else 'protective'
    mv = mr28.get(g)  # None if insufficient instruments
    if mv is None:
        obs='NA'; obs_or='NA'; concord='NA'
    else:
        obs = 'protective' if mv<1 else 'harmful'; obs_or=f"{mv:.3f}"
        concord='YES' if (pred=='protective' and obs=='protective') else 'no'
    out.append((g, f"{deg.get(g,0):.3f}", f"{rv:.3f}", f"{orr:.2f}", f"[{ci[0]:.2f},{ci[1]:.2f}]", f"{p:.3g}", pred, obs_or, concord))
with open(RES+"S06_hub_death_association.csv",'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['gene','mars1_logFC','corr_with_death','or_per_sd','ci','p','predicted_mr_direction','observed_mr_or_ivw','concordant'])
    for o in out: w.writerow(o)
for o in out: print("  ",o)

# ---------------------------------------------------------------- 6) Concordance binomial null (M2)
imm=np.array([(r['gene'],float(r['logFC']),float(r['adj.P.Val'])) for r in csv.DictReader(open(RES+"S01_immunoparalysis_direction.csv",encoding='utf-8'))]) if os.path.exists(RES+"S01_immunoparalysis_direction.csv") else None
# compute immune background p from S01_mars1_deg
deg_all=list(csv.DictReader(open(RES+"S01_mars1_deg.csv",encoding='utf-8')))
n_down=sum(1 for r in deg_all if float(r['logFC'])<0 and float(r['adj.P.Val'])<0.05)
n_sig=sum(1 for r in deg_all if float(r['adj.P.Val'])<0.05)
immune_genes=['CD74','HLA-DQA1','HLA-DRB1','HLA-DRA','HLA-DMB','HLA-DPB1','HLA-DPA1','HLA-DMA','CD14','FCGR3A','CD68','CD86','ITGAM','LYZ','TLR2','TLR4','IRF1','STAT1','STAT3','NFKB1','RELA','IL1B','TNF','IL6','IL10']
imm_down=sum(1 for r in deg_all if r['gene'] in immune_genes and float(r['logFC'])<0 and float(r['adj.P.Val'])<0.05)
print(f"\nImmune background: {imm_down}/{len(immune_genes)} consensus immune genes Mars1-down at FDR<0.05 = {imm_down/len(immune_genes):.2f}")
p_bg=imm_down/len(immune_genes)
drugs=list(csv.DictReader(open(RES+"08_candidates_drugs.csv",encoding='utf-8')))
print("Concordance vs immune-background p=%.2f:"%p_bg)
for d in drugs:
    k=int(d['n_rescue_mars1down']); n=int(d['n_target_genes'])
    # binomial P(X>=k) under p_bg
    P=sum(math.comb(n,i)*(p_bg**i)*((1-p_bg)**(n-i)) for i in range(k,n+1))
    print(f"  {d['compound']:14s} {k}/{n}={float(d['rescue_fraction']):.3f}  E={n*p_bg:.2f}  P(X>=k)={P:.3f}")

print("\nDONE v1.19.0 analysis regeneration.")
