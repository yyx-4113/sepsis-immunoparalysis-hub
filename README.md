# sepsis-immunoparalysis-hub

**Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning**

A fully computational, reproducible analysis pipeline that (i) identifies the hub genes anchoring the
MARS immunosuppressed (Mars1) endotype of sepsis from public transcriptomics, (ii) builds and
independently validates a 30-gene immune-risk prognostic signature, and (iii) reprioritizes
immune-restorative drugs by mechanism and by LINCS L1000 reverse-connectivity.

> This is the reproducibility package for the manuscript `05_reports/manuscript.md`. All numbers in the
> manuscript are traceable to files under `03_results/` (see `MANIFEST.csv` for SHA-256 checksums).

---

## Repository layout

```
00_pipeline/        Pipeline manifest (config.yaml, PIPELINE.md status table)
01_data/
  GSE65682/         Discovery cohort (MARS consortium; Affymetrix Human Gene 1.0 ST, GPL13667)
  E-MTAB-4451/      External validation cohort (Illumina HumanHT-12 V4, GPL10558; 106 sepsis samples)
  LINCS/            LINCS L1000 Phase-II Level 5 matrix (GSE92742) + metadata for reverse-connectivity
02_scripts/python/  All analysis scripts (see below)
03_results/         Every intermediate & final result table (CSV/JSON/npy)
04_figures/         Figures (PNG)
05_reports/         manuscript.md (full English + Chinese abstract), tier1_summary.txt
06_literature/      Staged references (not required to reproduce)
MANIFEST.csv        SHA-256 of every reported result/figure/report file
LICENSE             MIT
CITATION.cff        citation metadata
```

## Key scripts (run in this order)

| Script | Stage | Output |
|--------|-------|--------|
| `02_scripts/python/run_tier1.py` | S01–S06: DEG, immunoparalysis score, hub genes, 30-gene signature + 5-fold CV | `03_results/S0*.csv` |
| `02_scripts/python/07_hub_celltype.py` | S07: bulk marker-module cell-type localization of hub genes | `03_results/07_hub_celltype.csv` |
| `02_scripts/python/08_virtual_ko_cmap.py` | S08: mechanism-anchored drug repositioning + positive-control gate | `03_results/08_*.csv` |
| `02_scripts/python/09_external_validation.py` | S06 external validation on E-MTAB-4451 (locked model, no refit) | `03_results/09_*.csv`, `09_ext_risk_scores.csv` |
| `02_scripts/python/plot_s09_roc.py` | Fig: 30-gene signature external-validation ROC on E-MTAB-4451 (filename legacy `s09`; this is S06 external validation, **not** docking) | `04_figures/fig_s09_external_roc.png` |
| `02_scripts/python/S08_l1000_connectivity.py` | S08c: LINCS L1000 reverse-connectivity of Mars1-down axis (20,413 trt_cp) | `03_results/S08_l1000_rescue_trtcp.csv`, `S08_l1000_rescue_wtcs.npy` |
| `02_scripts/python/S08_l1000_postprocess.py` | S08c post-processing: candidate scores + positive controls | `03_results/S08_l1000_candidate_scores.csv`, `S08_l1000_positive_control.csv` |
| `02_scripts/python/plot_s10_l1000.py` | Fig S10 | `04_figures/fig_s10_l1000_rescue.png` |
| `02_scripts/python/10_genetics_mr_run.py` | S10: two-sample MR of hub genes (eQTLGen `eqtl-a-<ENSG>` exposure vs UKB sepsis `ieu-b-4980`; requires OpenGWAS JWT via `OPENGWAS_JWT` / `S10_JWT`) | `03_results/10_genetics_mr.csv`, `10_genetics_mr_harmonised.csv`, `05_reports/s10_run_log.txt` |

## Environment & reproduction

```bash
# 1) create the managed venv (Python 3.13)
python -m venv .venv
.venv/Scripts/python -m pip install numpy pandas scipy scikit-learn h5py matplotlib ieugwaspy

# 2) run the pipeline (Windows paths; use forward slashes)
.venv/Scripts/python.exe 02_scripts/python/run_tier1.py
.venv/Scripts/python.exe 02_scripts/python/09_external_validation.py
.venv/Scripts/python.exe 02_scripts/python/S08_l1000_connectivity.py   # needs 01_data/LINCS/GSE92742_Level5_COMPZ.gctx
.venv/Scripts/python.exe 02_scripts/python/S08_l1000_postprocess.py
```

The L1000 matrix (`01_data/LINCS/GSE92742_Level5_COMPZ.gctx`, ~23 GB) is **not** committed to git;
download it from GEO GSE92742 supplement and gunzip the `.gctx.gz` before running `S08_l1000_connectivity.py`.
The computed per-perturbagen scores are checkpointed to `03_results/S08_l1000_rescue_wtcs.npy`
(~320 KB), so `S08_l1000_postprocess.py` can be re-run without re-scanning the matrix.

## Software versions (used to produce the reported results)

| Tool | Version |
|------|---------|
| Python | 3.13.14 |
| numpy | 2.4.6 |
| pandas | 2.3.3 |
| scipy | 1.18.1 |
| scikit-learn | 1.9.0 |
| h5py | 3.16.0 |
| matplotlib | 3.11.1 |
| ieugwaspy | 1.0.6 |

## Data sources & licenses

- GSE65682 — MARS consortium, GEO, platform GPL13667 (Affymetrix Human Gene 1.0 ST). CC0/CC-BY per GEO.
- E-MTAB-4451 — Davenport et al., ArrayExpress/BioStudies, platform GPL10558 (Illumina HumanHT-12 V4). CC0.
- GSE92742 — LINCS L1000 Phase-II Level 5, GEO. CC0.

This study **used and re-analyzed public research data**; no new primary data were generated.

## Headline results (all traced to `03_results/`)

- Mars1 endotype: 21/25 consensus immune genes directionally down (22/25 FDR<0.05); immunoparalysis score lowest in Mars1 (median −0.79).
- 30-gene immune-risk signature: 5-fold CV AUC 0.659 (train 0.750) on GSE65682.
- **Independent external validation on E-MTAB-4451 (cross-platform): AUC 0.638 (95% CI 0.532–0.748)** for the fixed-orientation score.
- LINCS L1000 reverse-connectivity: lenalidomide top 26.6% (rescue 0.044), azithromycin ≈ median (rescue 0.013) of 20,413 trt_cp compounds — directional but modest rescue of the Mars1-down axis.

## Stated caveats (see manuscript §5)

- External validation magnitude is real but modest (comparable to, not better than, published IRG benchmark).
- L1000 rescue supports *direction* only; glucocorticoid positive-control shows transcriptional rescue ≠ functional restoration.
- S10 two-sample MR is executed against three pre-specified outcomes; the phenotype-matched primary is sepsis 28-day death (`ieu-b-5086`, 1,896 cases). Result is **suggestive, not confirmatory**: 4/5 assessable hubs give protective estimates concordant across IVW / MR-Egger / weighted median, and CD14 is nominally significant under MR-Egger (OR 0.906, *P*=5.1×10⁻³, null intercept), but no primary IVW estimate is significant. The susceptibility outcome (`ieu-b-4980`) is null for every hub. The CD74 critical-care signal (`ieu-b-4982`, OR 2.222, *P*=0.014) uses only 3 instruments, fails correction across 15 tests and reverses direction, so it is not claimed. FCGR3A is not assessed (2 instruments). No causal claim is made.
- Experimental validation (S11) is a design blueprint, not data.
- Structure-based docking / in-silico ADMET (S09) is **intentionally not performed** (deferred by design). The ADMET / clinical-translation layer is supplied instead by the S08b literature-rule pass (`03_results/08b_clinical_translation.csv`, candidate DOIs verified 2026-09-26), and drug prioritization rests on LINCS L1000 connectivity plus literature evidence rather than docking pose — see manuscript §5 limitation #7 and `00_pipeline/PIPELINE.md` (S09). `02_scripts/09_docking_admet.R` is a non-executed scaffold only.
