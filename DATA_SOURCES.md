# Data Sources — `01_data/`

The raw multi-omics inputs for this project are **not stored in git** (the git history
was filtered to keep the repository small, ~7 MiB). The `01_data/` directory is
restored on the analyst's local disk and listed in `.gitignore`. To reproduce,
download each dataset from its public repository and place it under
`01_data/<dataset>/` using the layout below. The manuscript's Data Availability
Statement is the authoritative source for accession IDs and versions.

| Local path (under `01_data/`) | Public repository | Accession / resource |
| --- | --- | --- |
| `GSE65682/` | NCBI GEO | GSE65682 (sepsis bulk transcriptomics; `GSE65682_family.soft.gz` + `GSE65682_expr.csv` + phenotype tables) |
| `E-MTAB-4451/` | EBI ArrayExpress / BioStudies | E-MTAB-4451 (Davenport et al. sepsis; normalised matrix `Davenport_sepsis_Feb2016_normalised_106.txt`, `idf`/`sdrf`, `GPL10558` annotation) |
| `GSE317767/` | NCBI GEO | GSE317767 |
| `GSE95233/` | NCBI GEO | GSE95233 |
| `LINCS/` | LINCS L1000 (clue.io / lincsportal) | L1000 inst/sig/pert/gene info; `mars1_down_l1000_idx.json` is a derived index |
| `epigenetic/` | Epigenetic reference resource | reference tables used by the methylation / cell-type deconvolution layer |
| `gtex_egene_wholeblood_gtex_v8.json` | GTEx Analysis V8 | Whole-blood eQTL (egene) table, GTEx v8 |

## Retrieval notes

- **GEO**: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=<ACCESSION> — download the
  family SOFT archive and the series matrix; extract into `01_data/<ACCESSION>/`.
- **ArrayExpress / BioStudies**: https://www.ebi.ac.uk/biostudies/arrayexpress/studies/<ACCESSION>.
- **LINCS L1000**: https://lincsportal.lincscloud.org/ or https://clue.io/ — the level-3
  `inst_info`, `sig_info`, `pert_info`, and `gene_info` tables. The large `.gctx` matrices
  are already excluded via `.gitignore` and are not required for the manuscript's reported
  reverse-connectivity analysis (which uses the derived index).
- **GTEx v8**: https://gtexportal.org/home/datasets — whole-blood eQTL summary.

## Why raw data is excluded from git

The combined raw inputs exceed 40 GB and include multi-hundred-MB files
(`GSE65682_family.soft.gz` ~199 MB, `GSE65682_expr.csv` ~125 MB). Keeping them out of
git history keeps the repository lightweight and pushable, while every number in the
manuscript remains traceable to a re-downloadable public source. All *derived* results
under `03_results/` and the audit CSVs are committed and version-tagged.
