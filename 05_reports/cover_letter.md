# Cover letter

**Manuscript title:** A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and externally evaluates a 30-gene sepsis prognostic signature

**Article type:** Article (original research)

**Corresponding author:** Yongxin Yang, The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou, Fujian 350003, China. Email: 960856791@qq.com

**Dear Editor,**

Please find enclosed our manuscript for consideration as an Article in *Scientific Reports*. This is a single-author, purely computational re-analysis of two public transcriptomic cohorts (GSE65682; E-MTAB-4451), with no new primary data generated. *Scientific Reports* evaluates submissions on methodological rigour and scientific validity rather than perceived novelty; our contribution is precisely a reproducible, fully auditable analytical pipeline, an honest independent external validation, and an explicit experimental blueprint — not novel hub-gene discovery.

**What the study does.**
We confirm and externally evaluate the MARS immunosuppressed (Mars1) endotype of sepsis and show that its immunoparalysis program is anchored by a compact set of antigen-presentation / monocytic hub genes (CD74, HLA-DQA1, CD14, FCGR3A) plus the co-inhibitory checkpoint HAVCR2/TIM-3 (expressed on T cells and antigen-presenting cells), and a non-immune co-expression passenger, FIS1. Two findings are robust and source-traceable: (i) the Mars1 program shows coherent downregulation of antigen-presentation and monocytic genes (a near-replication of the published MARS program), and (ii) a 30-gene immune-risk signature generalised to AUC 0.638 (95% CI 0.532–0.748) on an independent, cross-platform external cohort — comparable to, not better than, the published immune-related-gene benchmark.

**What the study does NOT claim.**
We wish to be explicit about the evidence hierarchy, because it bounds our claims:
- The two-sample Mendelian randomisation layer (germline eQTL of the hub genes on UK Biobank sepsis outcomes) is **hypothesis-generating only**. No primary IVW estimate reached significance; the one nominally significant MR-Egger signal (CD14) is uncorroborated by IVW or the weighted median and rests on few instruments. We further disclose that the eQTLGen exposure and the UK Biobank sepsis outcomes share participants (exposure–outcome sample overlap), for which we applied no correction.
- The drug-repositioning layer uses a **curated downstream response-gene concordance**, not direct pharmacologic-target overlap (no DGIdb/ChEMBL pull was performed), and its method-positive gate verifies a curated prior rather than independently discriminating true from false positives. Unbiased LINCS L1000 connectivity evidence covers only the two small-molecule candidates; the five immunobiologic/vaccine candidates rest on mechanism-anchored annotation.
- Functional validation of immune restoration is a **prospective design blueprint (S11)**, not data.

We believe the manuscript fits *Scientific Reports* because it combines a biologically inevitable, externally validated signal with an honest, tiered presentation of the weaker repositioning and genetic-causality layers — a framing we hope is useful to readers navigating computational sepsis immunotherapy.

**Conflicts of interest:** none declared. **Funding:** none. **Ethics:** purely computational re-analysis of public de-identified cohorts; no IRB approval required for the bioinformatics. **Data/code availability:** all result tables and analysis code are released under MIT at https://github.com/yyx-4113/sepsis-immunoparalysis-hub (citable GitHub release, tag v1.18.0; Zenodo DOI on acceptance).

Thank you for your consideration.

Yongxin Yang
