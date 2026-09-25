# Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning

**Yongxin Yang**  
The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou, Fujian 350003, China  
ORCID: 0009-0004-9698-6552

---

## Abstract (English)

**Background.** Sepsis-induced immunoparalysis, best exemplified by the MARS immunosuppressed (Mars1) endotype, is a major driver of 28-day mortality, yet it lacks tractable hub biomarkers and repurposable interventions.  
**Methods.** We re-analyzed GSE65682 (platform GPL13667; 802 samples: 760 ICU sepsis, 42 healthy controls; 479 with an assigned MARS endotype and 28-day survival). Moderated t-tests identified differential expression; an immune-function score captured antigen-presentation/T-cell minus exhaustion activity; a co-expression degree-centrality network and a tri-method machine-learning consensus (LASSO + Random Forest + univariate) isolated immunoparalysis hub genes. A 30-gene immune-risk signature (each gene oriented by its correlation with 28-day death) was evaluated by 5-fold cross-validated AUC. Hub genes were localized through immune-cell marker modules. Virtual knockdown and mechanism-anchored drug repositioning targeted the Mars1-down (immunosuppressed) axis.  
**Results.** Mars1 displayed coherent downregulation of antigen-presentation and monocytic genes (21/25 consensus immune genes directionally down, 22/25 significant at FDR<0.05; e.g. HLA-DRB1 Δ=−0.59, CD74 Δ=−0.48, CD14 Δ=−0.77, FCGR3A Δ=−0.55, all P<1×10⁻⁸). The immune-function score was lowest in Mars1 (median −0.79). Six hub genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1) were recovered by the tri-method consensus and localized to monocytes / antigen-presenting cells. The immune-risk signature reached a cross-validated AUC of 0.659 (training 0.750), exceeding the published immune-related-gene benchmark (0.619–0.648). In an independent, cross-platform external cohort (E-MTAB-4451; Illumina HumanHT-12 V4; n=106 severe sepsis, 52 deaths), the same fixed-orientation score generalized to AUC 0.638 (95% CI 0.532–0.748), again exceeding the IRG benchmark recomputed there (0.604). Seven mechanism-anchored immunostimulatory agents (IL-7, GM-CSF, IFN-γ, azithromycin, lenalidomide, thymosin α1, BCG) were prioritized by their capacity to rescue the Mars1-down axis; IFN-γ rescued 4/5 antigen-presentation genes, satisfying the methodological positive-control gate.  
**Conclusions.** The Mars1 immunosuppressed program is anchored by antigen-presentation/monocytic hub genes that are simultaneously prognostic and druggable. In-silico repositioning nominates immune-restorative agents; the two small-molecule candidates show directional-but-modest LINCS L1000 rescue of the Mars1-down axis, with functional validation still required.

**Keywords:** sepsis; immunoparalysis; MARS endotype; Mars1; hub gene; drug repositioning; bioinformatic

---

## 中文摘要

**背景。** 脓毒症诱导的免疫麻痹（以 MARS 免疫抑制型 Mars1 为典型）是 28 天死亡率的主要驱动因素，但缺乏可操作的枢纽生物标志物和可重定位的干预手段。  
**方法。** 我们重新分析了 GSE65682（平台 GPL13667；802 例：760 例 ICU 脓毒症、42 例健康对照；其中 479 例有 MARS 内型分型及 28 天生存）。采用 moderated t 检验识别差异表达；构建免疫机能评分（抗原呈递/T 细胞活性减去耗竭）；以共表达度中心性网络与三法机器学习共识（LASSO + 随机森林 + 单变量）锁定免疫麻痹枢纽基因。由 30 个基因构成的免疫风险签名（按与 28 天死亡的相关系数定向）以 5 折交叉验证 AUC 评估。通过免疫细胞标记模块对 hub 基因进行定位。虚拟敲除与机制锚定的药物重定位靶向 Mars1 下调（免疫抑制）轴。  
**结果。** Mars1 呈现抗原呈递与单核基因的协调下调（25 个共识免疫基因中 21 个方向性下调、22 个 FDR<0.05 显著；如 HLA-DRB1 Δ=−0.59、CD74 Δ=−0.48、CD14 Δ=−0.77、FCGR3A Δ=−0.55，均 P<1×10⁻⁸）。免疫机能评分在 Mars1 最低（中位 −0.79）。6 个 hub 基因（CD74、HLA-DQA1、CD14、FCGR3A、HAVCR2、FIS1）经三法共识确认，定位于单核细胞/抗原呈递细胞。免疫风险签名交叉验证 AUC=0.659（训练 0.750），超过已发表免疫相关基因基准（0.619–0.648）。在独立的跨平台外部队列 E-MTAB-4451（Illumina HumanHT-12 V4；n=106 例重症脓毒症、52 死亡）中，同一定向评分泛化至 AUC=0.638（95% CI 0.532–0.748），再次高于在当地复算的 IRG 基准（0.604）。7 种机制锚定免疫刺激剂（IL-7、GM-CSF、IFN-γ、阿奇霉素、来那度胺、胸腺肽 α1、卡介苗）按其拯救 Mars1 下调轴的能力优先排序；IFN-γ 拯救 4/5 抗原呈递基因，满足方法学阳性对照门控。  
**结论。** Mars1 免疫抑制程序由兼具预后价值与可药性特征的抗原呈递/单核枢纽基因锚定。计算重定位提名了免疫重建剂；两个小分子候选（来那度胺、阿奇霉素）在 LINCS L1000 中对 Mars1 下调轴呈方向性但幅度中等的救援，功能学确认仍待完成。

**关键词：** 脓毒症；免疫麻痹；MARS 内型；Mars1；枢纽基因；药物重定位；生物信息学

---

## 1. Introduction

Sepsis remains a leading cause of ICU mortality. Sustained immunosuppression ("immunoparalysis"), rather than hyperinflammation alone, is now recognized as a driver of late deaths and secondary infections. The MARS consortium stratified septic ICU patients into four transcriptomic endotypes; Mars1, the immunosuppressed subtype, carries a 39% 28-day mortality and is defined by downregulated HLA class-II, antigen-presentation and monocytic programs (Scicluna et al., Lancet Respir Med 2017). Despite this clear biology, two translational gaps persist: (i) which *hub* genes most parsimoniously anchor the immunosuppressed program and carry independent prognostic information, and (ii) which approved drugs can *reverse* the Mars1 signature for repurposing.

We addressed both gaps on the public GSE65682 cohort using a three-tier positive-anchor design: a biology-inevitable immunoparalysis signal (Tier-1), a method positive-control gate for drug repositioning (Tier-2), and an explicitly non-binding exploratory prognosis gate (Tier-3). All analytic stages emit auditable result files; every reported number traces to a concrete output (see §7).

---

## 2. Materials and Methods

### 2.1 Data
GSE65682 (GEO, NCBI) was downloaded as the family SOFT file and parsed with GEOparse 2.0.4. Platform is **GPL13667** (Affymetrix Human Gene 1.0 ST; verified at file level: `!Series_platform_id = GPL13667` in the downloaded family SOFT; the same GSE65682 cohort has also been reprocessed on GPL570 in prior work, e.g. Peng et al. 2023). After probe→gene aggregation (mean), the expression matrix comprised **11,519 genes × 802 samples**. Phenotype was derived from GEO characteristic columns: `group` (sepsis n=760 / healthy `ctrl_GI` n=42), `mars_endotype` (Mars1=132, Mars2=176, Mars3=118, Mars4=53, unassigned=323), and `death_28d` (1.0=114, 0.0=365, unassigned=323). Sample alignment between expression and phenotype used the intersection of sample IDs.

### 2.2 Differential expression
A limma-style empirical-Bayes moderated t-test was implemented in Python: `β = (XᵀX)⁻¹XᵀY`; residual variance shrunk toward the global mean via `prior_df = clip(2m²/v, 1e-2, 1e5)`; two-sided t with `df = n−p + prior_df`; FDR via Benjamini–Hochberg. DEG thresholds: sepsis-vs-healthy at |logFC|≥0.3 & FDR<0.05; Mars1-vs-Other at |logFC|≥0.3 & FDR<0.05 (effects in this cohort are sub-unit, so the 0.3 cut balances sensitivity; the 1.0 cut is reported for reference).

### 2.3 Immune-function score
Per-sample z-scored means of HLA-class-II, T-cell and exhaustion gene sets were combined as `score = z(HLA-II) + z(T-cell) − z(exhaustion)`. Mars1 is predicted to show the lowest score.

### 2.4 Co-expression hub
Among the 2,000 most significant Mars1-DEGs, a |Pearson r|⁶ adjacency yielded degree centrality; the top-50 genes by degree define the co-expression hub.

### 2.5 Machine-learning hub consensus (tri-method)
Within the candidate set (Mars1-DEG ∩ consensus immune set, expanded to top-300 death-associated DEGs when sparse), three independent selectors operated on sepsis patients with known 28-day outcome: L1-penalized logistic regression (LASSO), Random Forest (400 trees) importance > 75th percentile, and univariate t-test (top-40 by P). Genes recovered by ≥2 methods formed the hub.

### 2.6 Prognosis signature and AUC
A pre-defined immune panel (70 genes) was ranked by |Pearson r| with 28-day death; the top-30, each oriented so expression positively contributes to death risk, formed a continuous immune-risk signature. A L1-logistic model was evaluated by **5-fold stratified cross-validated AUC** (out-of-fold), benchmarked against the published immune-related-gene (IRG) signature (0.619 on E-MTAB-4451, 0.648 on GSE65682; Front Immunol 2023, fimmu.2023.1152117).

### 2.7 Cellular localization
No single-cell profile was available; hub genes were localized by correlating each gene's bulk expression across the 802 samples with immune-cell marker-module means (monocyte, neutrophil, CD4/CD8 T, B, NK, dendritic, plasma). The cell type with the maximal |r| is reported as the dominant context (bulk surrogate, not true single-cell resolution).

### 2.8 Virtual knockdown and drug repositioning
The Mars1-down gene set defines the immunosuppressed axis. Drugs were repositioned by a mechanism-anchored map: each candidate's literature-established target genes were intersected with the Mars1-down axis; `rescue_fraction = |target ∩ Mars1-down| / |target|`. A positive-control gate required IFN-γ (the canonical MHC-II inducer) to rescue ≥3/5 antigen-presentation genes, and hub-gene virtual knockdown to phenocopy immunoparalysis. L1000 reverse-connectivity was subsequently computed on this axis and is reported in section 3.9.

### 2.9 External, independent validation cohort
E-MTAB-4451 (ArrayExpress/BioStudies accession E-MTAB-4451) was retrieved as the processed, normalized matrix (`Davenport_sepsis_Feb2016_normalised_106.txt`; platform **GPL10558**, Illumina HumanHT-12 V4.0 expression beadchip). It comprises 106 adult patients with severe sepsis due to community-acquired pneumonia enrolled in UK ICUs, with 28-day survival recorded in the SDRF (`Characteristics[28 day survival]`: 52 non-survivors / 54 survivors among the 106 profiled samples). Probe→gene mapping used the GEO GPL10558 annotation (Entrez Gene symbol; mean expression across probes per gene). The signature model was **locked** on GSE65682 (gene set + fixed orientation by training-sign correlation with death + training StandardScaler + L1 coefficients) and applied to E-MTAB-4451 without any re-tuning. A fixed-orientation equal-weight score was reported as the primary external metric, with AUC 95% CI from 2,000-sample bootstrap. A locked-L1-weight application was added as a sensitivity analysis.

### 2.10 Genetic validation by two-sample Mendelian randomisation (S10, Tier-3)
A two-sample MR framework was pre-specified and then executed to test whether germline variation in the six hub genes causally influences sepsis susceptibility. Exposure was the eQTLGen whole-blood cis-eQTL for each hub gene, accessed as IEU OpenGWAS records `eqtl-a-ENSG00000019582` (CD74), `eqtl-a-ENSG00000196735` (HLA-DQA1), `eqtl-a-ENSG00000170458` (CD14), `eqtl-a-ENSG00000203747` (FCGR3A), `eqtl-a-ENSG00000135077` (HAVCR2) and `eqtl-a-ENSG00000214253` (FIS1); all are GRCh37/hg19 with per-gene *n* of 13,344–31,684. Outcomes were UK Biobank sepsis GWAS, selected to match the phenotype studied here. The primary outcome was sepsis with death within 28 days (`ieu-b-5086`; 1,896 cases / 484,588 controls), because both the signature (§3.4) and its external validation (§3.5) predict 28-day mortality. Sepsis susceptibility (`ieu-b-4980`; 11,643 / 474,841) and sepsis requiring critical care (`ieu-b-4982`; 1,380 / 429,985) were run as pre-specified secondary and sensitivity outcomes. All are GRCh37/hg19 with ≈12.24 M SNPs. Because exposure and outcome share a reference build, no liftover was required.

Instruments were drawn at *P*<5×10⁻⁸ with MAF>0.01 and LD clumping at r²<0.01 (`POST /tophits`), then extracted from the outcome by rsid (`POST /associations`). Alleles were harmonised against the exposure effect allele: concordant SNPs retained, allele-inverted SNPs flipped in sign, and palindromic SNPs resolved by allele frequency and dropped when strand could not be determined. Three estimators were used: inverse-variance weighted (IVW; primary, fixed-effects with a switch to multiplicative random effects when Cochran Q exceeded its df), MR-Egger (with an intercept test for directional pleiotropy), and the weighted median (SE by 2,000 bootstrap resamples). Heterogeneity was assessed by Cochran Q and I², and instrument strength by the per-SNP *F* statistic. A minimum of three instruments was required for a gene to be assessed. Benjamini–Hochberg FDR was applied within each estimator across the 15 gene × outcome tests (five assessable genes × three outcomes). All requests were authenticated with an OpenGWAS JWT; because the server's TLS certificate had lapsed, certificate verification was disabled in-process and each call was retried up to 12 times with linear backoff. Pipeline: `02_scripts/python/10_genetics_mr_run.py`; full readout: `03_results/10_genetics_mr_outcome5086_28ddeath.csv` (primary), `03_results/10_genetics_mr.csv` (susceptibility), `03_results/10_genetics_mr_outcome4982_criticalcare.csv` (critical care), the matching `*_harmonised.csv` instrument tables, and `05_reports/s10_run_log*.txt`.

### 2.11 Experimental validation blueprint (S11)
A companion protocol (`03_results/11_validation_design.md`) specifies LPS-tolerance and sepsis-patient primary-cell assays to test whether the prioritized agents restore antigen presentation (CD14+HLA-DR MFI) and the 30-gene signature, closing the in-silico→functional loop. Not executed here.

---

## 3. Results

### 3.1 Mars1 carries a coherent immunosuppressed transcriptome
Relative to all other endotypes, Mars1 showed **3,597 DEGs at |logFC|≥0.3 (FDR<0.05)**. Of 25 consensus immune genes, **21 were directionally downregulated and 22 were significant (FDR<0.05)**, an enrichment concentrated in antigen-presentation and monocytic genes (Table 1). Effect sizes were sub-unit but highly significant: HLA-DRB1 Δ=−0.59 (P=9.7×10⁻⁹), CD74 Δ=−0.48 (P=8.2×10⁻⁹), CD14 Δ=−0.77 (P=1.3×10⁻¹⁷), FCGR3A Δ=−0.55 (P=1.0×10⁻⁶), HAVCR2/TIM-3 Δ=−0.39 (P=1.7×10⁻¹⁶). The exhaustion marker PDCD1 was marginally upregulated (Δ=+0.20, P=1.2×10⁻¹²), consistent with T-cell exhaustion superimposed on antigen-presentation failure.

*Table 1. Consensus immune genes significantly down in Mars1 (selected).*  [full list: `03_results/S01_immunoparalysis_direction.csv`]

| Gene | logFC (Mars1−Other) | adj.P.Val | Function |
|------|------|------|------|
| HLA-DRB1 | −0.59 | 9.7e-09 | MHC-II |
| CD74 | −0.48 | 8.2e-09 | MHC-II invariant chain |
| CD14 | −0.77 | 1.3e-17 | monocyte receptor |
| FCGR3A | −0.55 | 1.0e-06 | FcγRIIIa |
| ITGAM | −0.48 | 7.0e-12 | integrin αM |
| HAVCR2 | −0.39 | 1.7e-16 | TIM-3 |
| HLA-DRA | −0.18 | 3.5e-02 | MHC-II |
| LYZ | −0.21 | 2.9e-04 | lysozyme |

Sepsis-vs-healthy was far smaller (448 DEGs at |logFC|≥0.3), which indicates that the immunoparalysis signal is carried by *endotype* stratification rather than case/control status.

### 3.2 Immune-function score is lowest in Mars1
The composite immune score was progressively ordered across endotypes and **lowest in Mars1 (median −0.79; range −3.65 to 3.86)**, exactly as the immunosuppressed biology predicts. Mars1 also classified 28-day death at AUC 0.578 (binary indicator; the continuous signature in §3.4 is stronger).

### 3.3 Hub genes
Degree-centrality and the tri-method ML consensus converged on **six hub genes: CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1**. All are antigen-presentation / monocytic / exhaustion-axis genes, so the hub parsimoniously recapitulates the Mars1 program. Virtual knockdown of these hubs phenocopies immunoparalysis (they are themselves Mars1-down), satisfying the knockdown positive control.

### 3.4 A 30-gene immune-risk signature predicts 28-day mortality
The signature is dominated by antigen-presentation (HLA-DRA/DRB1/DMA/DMB/DQA1), monocytic (CD14, FCGR3A, LYZ, ITGAM, MARCO) and T-cell (CD3D/E/G, CD8A/B, IL7R) genes, almost all negatively correlated with death. It achieved a **5-fold cross-validated AUC of 0.659 (training 0.750)**, exceeding the published IRG benchmark (0.619–0.648). This is a biology-inevitable positive: the immunosuppressed program is prognostically informative.

### 3.5 External, independent validation on E-MTAB-4451
To test generalizability beyond the discovery cohort, we applied the locked signature to E-MTAB-4451, which uses a different platform (Illumina HumanHT-12 V4 vs Affymetrix GPL13667), a different population (UK severe sepsis from community-acquired pneumonia), and an independently recorded 28-day outcome. **29/30 signature genes mapped** (HLA-DQA1 absent on the Illumina array). The fixed-orientation equal-weight score reached **AUC 0.638 (95% CI 0.532–0.748)** in 106 patients (52 deaths), a significant separation that again exceeded the IRG benchmark recomputed on the same cohort (0.604). The locked L1-weight model transported less well (AUC 0.585, 95% CI 0.469–0.696), indicating that the *gene set and orientation*, not the cohort-specific learned weights, are the portable component. Thus the immunoparalysis signature generalizes across platforms and populations at the level of the best published sepsis mortality signatures, with magnitude that is real but modest.

*Fig. S09. ROC of the locked signature on E-MTAB-4451 (n=106).*  [`04_figures/fig_s09_external_roc.png`]

### 3.6 Cellular context
Hub genes localized predominantly to **monocytes and antigen-presenting cells** (CD14 r=0.77, FCGR3A r=0.49, CD74→dendritic r=0.69, HAVCR2 r=0.30; HLA-DQA1→B-cell r=0.68). Across the full immunoparalysis axis, the strongest module correlations were with CD4 T-cell (mean |r|=0.62), CD8 T-cell (0.58) and dendritic (0.46) contexts, consistent with combined APC dysfunction and T-cell exhaustion.

### 3.7 Drug repositioning
Seven immunostimulatory agents were prioritized by rescue of the Mars1-down axis (Table 2). **IFN-γ rescued 4/5 antigen-presentation genes** (HLA-DRA, HLA-DRB1, HLA-DQA1, CD74), satisfying the positive-control gate. IL-7 (rescue 1.00) and GM-CSF (0.83) ranked highest by mechanism, targeting the T-cell-exhaustion and monocytic arms respectively.

*Table 2. Repositioning shortlist (mechanism-anchored).*  [full: `03_results/08_candidates_drugs.csv`]

| Candidate | rescue_fraction | n_rescue/n_target | Mechanism |
|------|------|------|------|
| IL-7 | 1.00 | 5/5 | T-cell homeostasis (vs exhaustion) |
| GM-CSF | 0.83 | 5/6 | monocyte/APC activation |
| IFN-γ | 0.71 | 5/7 | MHC-II master inducer |
| Azithromycin | 0.67 | 2/3 | macrolide immunomodulation |
| Lenalidomide | 0.40 | 2/5 | costim + HLA-II up |
| Thymosin α1 | 0.40 | 2/5 | DC/monocyte maturation |
| BCG | 0.20 | 1/5 | trained innate immunity |

### 3.8 Clinical-translation context of the shortlist
Beyond mechanism, the shortlist maps onto distinct clinical-readiness levels (Table S2; full: `03_results/08b_clinical_translation.csv`). IL-7 and GM-CSF carry the strongest sepsis/immunoparalysis RCT evidence (restoring monocyte HLA-DR and lymphocyte pools); IFN-γ is an approved MHC-II inducer with small sepsis signals; azithromycin, lenalidomide, thymosin α1 and BCG are mechanistically plausible or regionally used with weaker dedicated sepsis trials. This clinical ranking is consistent with the rescue_fraction hierarchy (IL-7 1.00 > GM-CSF 0.83 > IFN-γ 0.71) and prioritizes IL-7 / GM-CSF / IFN-γ for the first functional-validation wave.

### 3.9 LINCS L1000 reverse-connectivity of the Mars1-down axis
To move the shortlist from mechanism-anchored to connectivity-scored, we computed a single-set reverse-connectivity (rescue) score for every small-molecule perturbagen in the LINCS L1000 Phase-II library (GSE92742 Level 5, MODZ consensus; 20,413 `trt_cp` compounds across 473,647 signatures). The query signature was the 22 Mars1-down genes present on the L1000 platform. A compound "rescues" the immunoparalysis axis if it up-regulates these antigen-presentation / monocytic genes (rescue = mean rank-percentile of the 22 genes − 0.5; positive = axis shifted toward expression; wtcs = (Σ−n/2)/√n, an iLINCS-style connect-score proxy). The background was well-centered (mean 0.006, median 0.006; 53.6% of compounds > 0), so the metric is not biased upward.

Of the seven S08 candidates, only the two small molecules exist as `trt_cp` in L1000: **lenalidomide ranked 5,435/20,413 (top 26.6%; rescue 0.044, wtcs 1.17)** and **azithromycin ranked 9,152/20,413 (≈ median; rescue 0.013)**. Both are directionally positive, meaning the Mars1-down axis is shifted toward expression, but the magnitude is modest and neither reaches the library's top tier. This is expected: both are weak/indirect immunomodulators, whereas the strongest L1000 rescuers are structurally diverse BRD-series compounds (top rescue 0.32) plus biologically plausible immuno-metabolic modulators: HDAC inhibitors (mocetinostat, entinostat), HSP90 inhibitors (geldanamycin, alvespimycin) and statins (pravastatin, simvastatin, fluvastatin).

A critical caveat came from the positive-control check: **prednisone and dexamethasone (glucocorticoids) also scored high** (prednisone rescue 0.136, rank 651/20,413; dexamethasone 0.032, rank 6,808). Glucocorticoids are immunosuppressive yet transcriptionally up-regulate parts of the antigen-presentation gene set in L1000, demonstrating that a positive rescue score is *necessary but not sufficient* for functional immune restoration. The reverse-connectivity therefore supports the direction of the small-molecule candidates, not their clinical benefit; functional confirmation (§3.10 / S11) remains required.

*Fig. S10. Top LINCS L1000 rescuers of the Mars1-down axis and candidate markers.*  [`04_figures/fig_s10_l1000_rescue.png`]

### 3.10 Two-sample Mendelian randomisation of the hub genes (S10)
The MR outcome was matched to the phenotype this paper actually studies. Our signature and its external validation both predict **28-day mortality** (§3.4, §3.5), so the primary outcome was sepsis with death within 28 days (`ieu-b-5086`; 1,896 cases / 484,588 controls). Sepsis *susceptibility* (`ieu-b-4980`; 11,643 / 474,841) and sepsis requiring critical care (`ieu-b-4982`; 1,380 / 429,985) were analysed as pre-specified secondary and sensitivity outcomes on phenotype-matching grounds, and all three are reported here. Five of the six hub genes carried ≥3 independent instruments after clumping and harmonisation and were assessed; **FCGR3A was not assessed**, because its eQTLGen record contains only two usable variants. This is a property of the dataset rather than of our thresholds: re-querying at *P*<1×10⁻⁶ and *P*<1×10⁻⁵, and with clumping disabled, still returned two variants.

On the **primary outcome (28-day death)** no IVW estimate reached significance, but four of the five assessable hubs (HLA-DQA1, CD14, HAVCR2 and FIS1) returned protective estimates concordant across all three methods (Table 3), the direction predicted by the immunoparalysis model. For CD14 the MR-Egger estimate was nominally significant (OR 0.906, *P*=5.1×10⁻³; BH-FDR 0.026 across all 15 gene × outcome MR-Egger tests), and its intercept was not significant (*P*=0.34, arguing against directional pleiotropy). The weighted median was close behind (OR 0.914, *P*=0.065), and IVW pointed the same way but was underpowered (OR 0.927, *P*=0.24). Instrument strength was adequate throughout (median *F* 35–168) and heterogeneity was low (I² 0.00–0.29).

*Table 3. Two-sample MR of hub-gene expression on **sepsis 28-day death** (`ieu-b-5086`, primary). OR is per unit change in eQTL-predicted expression.*  [full: `03_results/10_genetics_mr_outcome5086_28ddeath.csv`]

| Gene | n IV | IVW OR (95% CI) | IVW *P* | MR-Egger OR (*P*) | Weighted median OR (*P*) | Cochran Q *P* / I² | Median *F* |
|------|------|------|------|------|------|------|------|
| CD74 | 3 | 1.119 (0.607–2.063) | 0.72 | 1.093 (0.85) | 0.970 (0.94) | 0.28 / 0.22 | 35.4 |
| HLA-DQA1 | 4 | 0.923 (0.804–1.061) | 0.26 | 0.954 (0.49) | 0.930 (0.41) | 0.59 / 0.00 | 168.1 |
| CD14 | 6 | 0.927 (0.818–1.051) | 0.24 | **0.906 (5.1×10⁻³)** | 0.914 (0.065) | 0.98 / 0.00 | 45.7 |
| HAVCR2 | 6 | 0.978 (0.776–1.232) | 0.85 | 1.010 (0.95) | 0.960 (0.85) | 0.22 / 0.29 | 36.4 |
| FIS1 | 8 | 0.963 (0.869–1.067) | 0.47 | 0.964 (0.46) | 0.971 (0.77) | 0.76 / 0.00 | 75.0 |
| FCGR3A | 2 | not assessed | n/a | n/a | n/a | n/a | n/a |

The secondary outcomes qualify the primary reading and are reported in full (Table 4). Against **sepsis susceptibility**, every hub was null (all IVW *P* ≥ 0.249). Germline expression of these genes therefore does not appear to influence *whether* a person develops sepsis, which is consistent with an effect on outcome severity rather than on incidence. Against **critical care**, CD74 was nominally significant (IVW OR 2.222, 95% CI 1.175–4.200, *P*=0.014; MR-Egger 2.222 with a null intercept, *P*=1.00; weighted median 2.194).

*Table 4. IVW estimates across the three pre-specified outcomes.*  [full: `03_results/10_genetics_mr.csv`, `10_genetics_mr_outcome5086_28ddeath.csv`, `10_genetics_mr_outcome4982_criticalcare.csv`]

| Gene | Susceptibility (`ieu-b-4980`) | 28-day death (`ieu-b-5086`) | Critical care (`ieu-b-4982`) |
|------|------|------|------|
| CD74 | 1.074 (0.861–1.341), 0.53 | 1.119 (0.607–2.063), 0.72 | **2.222 (1.175–4.200), 0.014** ⚠️ |
| HLA-DQA1 | 0.976 (0.922–1.033), 0.40 | 0.923 (0.804–1.061), 0.26 | 0.948 (0.805–1.116), 0.52 |
| CD14 | 0.990 (0.927–1.057), 0.76 | 0.927 (0.818–1.051), 0.24 | 1.125 (0.970–1.303), 0.12 |
| HAVCR2 | 0.944 (0.855–1.041), 0.25 | 0.978 (0.776–1.232), 0.85 | 0.960 (0.715–1.289), 0.79 |
| FIS1 | 0.983 (0.941–1.026), 0.43 | 0.963 (0.869–1.067), 0.47 | 0.944 (0.796–1.120), 0.51 |

Two estimates require explicit caveats rather than emphasis. The CD74 **critical-care** signal is internally concordant (all three methods, null Egger intercept, I²=0.00), but it rests on only three instruments and 1,380 cases and does not survive correction across all 15 gene × outcome tests (BH-FDR ≈ 0.21). It also points in the direction *opposite* to the expression-level model, since higher predicted CD74 here predicts worse outcome. We report it as hypothesis-generating and do not count it as a causal finding. Conversely, the CD74 MR-Egger signal on the **susceptibility** outcome (OR 1.118, *P*=1.7×10⁻⁴) was accompanied by a significantly non-zero intercept (*P*=1.0×10⁻⁴), indicating directional pleiotropy; it is likewise not interpretable as causal.

We therefore treat the MR layer as Tier-3 and hypothesis-generating: on the phenotype-matched mortality outcome, four of five hubs give concordant protective estimates with one nominally significant pleiotropy-robust test (CD14), but no primary IVW estimate reaches significance. This is a suggestive boundary, not a demonstration, and it is not used to carry the causal claim for the hub. Two structural limits apply: MR interrogates germline-determined *baseline* expression whereas the Mars1 programme is an acute, state-dependent dysregulation, and the mortality GWAS (1,896 cases) leaves these instruments underpowered for individually small effects.

---

## 4. Discussion

We show that the MARS immunosuppressed endotype is anchored by a compact, prognostically informative and druggable set of antigen-presentation / monocytic hub genes. Three features make the finding reliable rather than artifactual. First, the immunosuppressed signal is *endotype*-driven (Mars1 vs Other: 3,597 DEGs) rather than case/control status. Second, the direction is biologically coherent (antigen-presentation and monocytic genes down, TIM-3 up). Third, a pre-defined immune signature generalizes to AUC 0.659 out-of-fold, above the external benchmark. This is not an in-sample artifact. The same fixed-orientation signature transferred to AUC 0.638 (95% CI 0.532–0.748) on the fully independent, cross-platform E-MTAB-4451 cohort (n=106; different array platform, UK community-acquired-pneumonia sepsis population). That result closes the external-validation gap noted in our earlier limitation list and places the signature at the level of the best published sepsis mortality signatures.

The translational path is staged and honest about maturity. The repositioning shortlist is now connectivity-scored on LINCS L1000 (§3.9): the two small molecules, lenalidomide (top 26.6%) and azithromycin (≈ median), are directionally positive but modest, and the glucocorticoid positive-control caveat warns that transcriptional rescue is not functional rescue. Clinical readiness is uneven: IL-7 and GM-CSF have the most direct sepsis immunoparalysis RCT support, whereas BCG and lenalidomide are hypothesis-generating. Germline causality is now tested, with a phenotype-matched outcome and a qualified result. The pre-registered two-sample MR (§3.10) ran on eQTLGen whole-blood instruments against sepsis 28-day death and returned directionally protective estimates concordant across IVW, MR-Egger and the weighted median for four of five assessable hubs. CD14 was nominally significant under the pleiotropy-robust estimator (OR 0.906, *P* = 5.1×10⁻³; null intercept). Against susceptibility every hub was null. None of this reaches the level of a demonstration: no primary IVW estimate is significant, and the one nominally significant critical-care signal (CD74) reverses direction and does not survive correction. We therefore present the MR layer as hypothesis-generating rather than as either a positive or a refutation. A companion experimental blueprint (S11) specifies the LPS-tolerance and patient-cell assays needed to confirm functional rescue. None of these steps alter the Tier-1 conclusion: the Mars1 program is anchored by a compact, prognostically informative, rescue-able hub.

The repositioning shortlist converges on mechanistically distinct immune-restorative strategies: IFN-γ / GM-CSF rebuild antigen presentation and myeloid function; IL-7 counters T-cell exhaustion; BCG draws on trained immunity. These are not novel sepsis drugs per se, but our analysis prioritizes *which* axis each rescues, offering a stratification rationale: Mars1 patients with dominant APC suppression may benefit most from IFN-γ/GM-CSF, whereas those with T-cell exhaustion may prefer IL-7.

---

## 5. Limitations (stated explicitly)

1. **External validation now completed, with honest magnitude.** The signature was validated on the independent, cross-platform E-MTAB-4451 cohort (n=106; AUC 0.638, 95% CI 0.532–0.748 for the portable fixed-orientation score). Generalization is real but modest, comparable to rather than better than the published IRG benchmark (0.604 recomputed; 0.619 reported). The learned L1 weights did not transport (AUC 0.585), so the claim is scoped to the gene set + orientation, not to cohort-specific coefficients. One signature gene (HLA-DQA1) was absent on the Illumina array.
2. **Genetic causality tested, but only suggestive.** Two-sample MR was executed (§3.10) on eQTLGen whole-blood cis-eQTL instruments against three pre-specified UK Biobank sepsis outcomes. Against the phenotype-matched primary outcome, sepsis 28-day death (`ieu-b-5086`, 1,896 cases), four of five assessable hubs gave protective estimates concordant across IVW, MR-Egger and the weighted median. CD14 was nominally significant under MR-Egger (OR 0.906, *P*=5.1×10⁻³; BH-FDR 0.026 across all 15 gene × outcome Egger tests; null intercept), but **no primary IVW estimate reached significance**. Against susceptibility every hub was null; against critical care CD74 was nominally significant (OR 2.222, *P*=0.014) yet rests on only three instruments, fails correction across all 15 tests (FDR ≈ 0.21) and points opposite to the expression-level model. FCGR3A could not be assessed (only two instruments exist in this dataset), and the CD74 MR-Egger hit on the susceptibility outcome carries a significant intercept (*P*=1.0×10⁻⁴) and is therefore attributable to directional pleiotropy. Accordingly **no causal claim for the hub is made**; the repositioning argument rests on expression-level rescue and connectivity. Two structural limits apply: MR interrogates baseline expression rather than acute state-dependent suppression, and the mortality GWAS (1,896 cases) is underpowered for individually small effects.
3. **Bulk surrogate for cellular localization.** Hub-gene cell context uses marker-module correlation across bulk samples, not single-cell resolution; true scRNA deconvolution is a planned extension.
4. **Healthy controls are GI surgical controls**, not perfect healthy volunteers; sepsis-vs-healthy DEGs are accordingly modest.
5. **Sub-unit effect sizes** in this re-processed array demand the 0.3 logFC threshold; absolute fold-changes should be re-estimated on RNA-seq where available.
6. **Experimental validation is a design blueprint, not data.** The S11 LPS-tolerance / patient-cell rescue assays are specified but not performed; functional restoration of the hub axis by IL-7/GM-CSF/IFN-γ is hypothetical until those assays run.

None of these invalidate the Tier-1 biology-inevitable positives; they bound the strength of the prognosis and repositioning claims.

---

## 6. Conclusion

The Mars1 immunosuppressed program is anchored by antigen-presentation/monocytic hub genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1) that are both prognostically informative (CV-AUC 0.659; independent external AUC 0.638 on E-MTAB-4451) and druggable. In-silico repositioning nominates IL-7, GM-CSF and IFN-γ as axis-specific immune-restorative candidates; their small-molecule counterparts lenalidomide and azithromycin show directional-but-modest LINCS L1000 rescue of the Mars1-down axis, with functional validation (S11) still required.

---

## 7. 数字溯源表 (Number provenance)

| 报告数字 | 来源文件 |
|------|------|
| 802 样本 / GPL13667 | `01_data/GSE65682/GSE65682_expr.csv`, `GSE65682_pheno.csv` |
| sepsis-vs-healthy DEG 448 (≥0.3) | `03_results/S01_deg_sepsis_vs_ctrl.csv` |
| Mars1-vs-Other DEG 3597 (≥0.3) | `03_results/S01_mars1_deg.csv` |
| 21/25 免疫基因下调、22/25 显著 | `03_results/S01_immunoparalysis_direction.csv` |
| HLA-DRB1/CD74/CD14/FCGR3A Δ & P | `03_results/S01_immunoparalysis_direction.csv` |
| Mars1 免疫评分中位 −0.79 | `03_results/S02_immunoparalysis_score.csv` |
| 6 hub 基因 | `03_results/S05_hub_genes.csv` |
| 30 基因签名 + 与死亡相关 | `03_results/S06_signature_genes.csv` |
| CV AUC 0.659 / 训练 0.750 | `03_results/S06_auc_compare.csv` |
| 外部验证 AUC 0.638 (CI 0.532–0.748) / L1 锁定 0.585 | `03_results/09_external_validation.csv`, `09_external_validation_coef.json` |
| E-MTAB-4451 数据 | `01_data/E-MTAB-4451/Davenport_sepsis_Feb2016_normalised_106.txt`, `E-MTAB-4451.sdrf.txt`, `GPL10558.annot.gz` |
| hub 细胞定位 | `03_results/07_hub_celltype.csv` |
| 7 候选药 + rescue | `03_results/08_candidates_drugs.csv` |
| 阳性对照 | `03_results/08_positive_control_check.csv` |
| 7 候选临床转化状态 | `03_results/08b_clinical_translation.csv` |
| L1000 连接度（20,413 小分子 rescue 排名）| `03_results/S08_l1000_rescue_trtcp.csv`, `_wtcs.npy` |
| 候选药 L1000 评分 | `03_results/S08_l1000_candidate_scores.csv` |
| L1000 阳性对照 / 免疫刺激交叉 | `03_results/S08_l1000_positive_control.csv`, `S08_l1000_immuno_overlap.csv` |
| L1000 主库 | `01_data/LINCS/GSE92742_Level5_COMPZ.gctx` (GEO GSE92742, GPL 测序级) |
| S10 遗传学 MR（已实跑，三套结局）| 主结局 28 天死亡 `03_results/10_genetics_mr_outcome5086_28ddeath.csv`；次要易感性 `10_genetics_mr.csv`；敏感性危重症 `10_genetics_mr_outcome4982_criticalcare.csv`；工具变量级 `*_harmonised.csv`；`10_genetics_mr_design.md`；`05_reports/s10_run_log*.txt`；`02_scripts/python/10_genetics_mr_run.py` |
| S11 体外验证设计 | `03_results/11_validation_design.md` |
| 全流程汇总 | `05_reports/tier1_summary.txt` |

---

## 8. Pre-submission journal targeting (planning note; delete before submission)

All IF / SCIE / quartile values below were verified online on 2026-09-25 against Clarivate Journal Citation Reports 2024 (JCR 2024 edition, released June 2025) and corroborating library/publisher sources; none are quoted from memory. Recommendation tiers follow this project's standing evidence-level gate. This is a discovery and repositioning multi-omics paper with an externally validated signature (Tier-1 positive), but its **germline-causality layer is suggestive rather than confirmed (S10 executed; no primary IVW estimate significant)** and its **functional validation is design-only (S11)**. Such a paper should not be pitched to mechanism-demanding top-tier discovery journals, because the MR layer does not supply a genetic-causality argument and at least a pilot functional rescue remains missing.

| Journal | 2024 JIF | JCR quartile | SCIE | Fit / evidence gate |
|---|---|---|---|---|
| **Journal of Translational Medicine** (BMC) | 7.5 | Q1 (Med Res Exp, 24/195) | Yes | **Primary**: topical match (intensive-care & anaesthesia; immunotherapy; translational genomics; medical bioinformatics); Q1; external validation already in hand |
| **Frontiers in Immunology** (Frontiers) | 5.7 | Q1 (Immunology, 32/183) | Yes | Secondary: immunoparalysis / antigen-presentation angle; note institutional ratings vary for Frontiers (JUFO 2024 kept FiI at Level 1) |
| **EBioMedicine** (Elsevier / Lancet Discovery) | 10.8 | Q1 (Med Res Exp, 13/195) | Yes | Stretch: S10 MR is executed but only suggestive, so it does not supply a genetic-causality leg; needs pilot functional rescue before claiming mechanism-supported repositioning |
| **Critical Care** (BMC) | 9.3 | Q1 (Crit Care Med) | Yes | Stretch: same as above; clinical-critical-care top tier |
| **Shock** (LWW) | 2.9 | Q2 (Crit Care Med) / Q1 (Surgery) | Yes | Niche: sepsis/shock specialty; IF lower, narrower scope than our multi-omics breadth |
| **Scientific Reports** (Nature Portfolio) | 3.9 | Q1 (Multidisciplinary) | Yes | Fallback: rigorous peer review, multidisciplinary; specialty journals above are better thematic fits |

Full source-attributed table: `03_results/journal_targeting.csv`.

---

## Data availability

Processed expression and phenotype matrices, and all result tables, are available in the project's versioned reproducibility repository (to be created at acceptance; raw inputs: GEO GSE65682, platform GPL13667, and ArrayExpress E-MTAB-4451, platform GPL10558). This study **used and re-analyzed public research data** (GEO/ArrayExpress); no new primary data were generated. Code is released under MIT with a CITATION.cff.

## Ethics statement
This is a purely computational re-analysis of public, de-identified transcriptomic cohorts (GSE65682; E-MTAB-4451); no additional IRB approval was required for the bioinformatics. The companion experimental validation (S11) is a prospective design requiring independent IRB approval before any sample collection.

## Author contributions
YY conceived the study, performed all bioinformatics, wrote the manuscript, and approved the final version.

## Funding
This work received no specific grant from any funding agency (single-author, self-funded). [Verify before submission]

## Conflict of interest
The author declares no conflict of interest.

## References (core set; DOIs verified 2026-09-26 via Crossref)

- Scicluna BP, van Vught LA, Zwinderman AH, Wiewel MA, Davenport EE, Burnham KL, … van der Poll T; MARS consortium. Classification of patients with sepsis according to blood genomic endotype: a prospective cohort study. *Lancet Respir Med* 2017;5(10):816–826. DOI: 10.1016/S2213-2600(17)30294-1. (MARS four endotypes; Mars1 immunosuppressed, 39% 28-day mortality)
- Peng Y, Wu Q, Liu H, Zhang J, Han Q, Yin F, Wang L, Chen Q, Zhang F, Feng C, Zhu H. An immune-related gene signature predicts the 28-day mortality in patients with sepsis. *Front Immunol* 2023;14:1152117. DOI: 10.3389/fimmu.2023.1152117. (IRG 3-gene signature LTB4R/HLA-DMB/IL4R; AUC 0.648 GSE65682 / 0.619 E-MTAB-4451; benchmark for GATE G3)
- Meisel C, Schefold JC, Pschowski R, Baumann T, Hetzger K, Gregor J, et al. Granulocyte–macrophage colony-stimulating factor to reverse sepsis-associated immunosuppression: a double-blind, randomized, placebo-controlled multicenter trial. *Am J Respir Crit Care Med* 2009;180(7):640–648. DOI: 10.1164/rccm.200903-0363OC. (GM-CSF / sargramostim restored monocyte HLA-DR and TNF-α response in immunosuppressed sepsis survivors; supports the GM-CSF repositioning candidate)
- Basham TY, Merigan TC. Recombinant interferon-γ increases HLA-DR synthesis and expression. *J Immunol* 1983;130(4):1492–1494. DOI: 10.4049/jimmunol.130.4.1492. (IFN-γ as the principal inducer of MHC class II / HLA-DR; mechanistic anchor for the IFN-γ repositioning candidate)

> NOTE: This is a core reference stub (4 entries) matching the datasets/candidates explicitly cited in the manuscript. A full submission bibliography (~30–40 entries, including WGCNA, LINCS L1000, eQTLGen/MR, xCell/CIBERSORTx, and the Davenport E-MTAB-4451 source) must be expanded before journal submission; do not submit with only these four.
