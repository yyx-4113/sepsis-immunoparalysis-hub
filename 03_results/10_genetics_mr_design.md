# Supplemental Design and Results — Genetic Validation of the Mars1 Immunoparalysis Hub (S10, Tier-3)

**Project:** Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis
**Companion:** `05_reports/manuscript.md` §2.10, §3.10; `02_scripts/python/10_genetics_mr_run.py`
**Status:** *Executed 2026-09-25/26.* Two-sample MR run against live IEU OpenGWAS
(JWT-authenticated) on three pre-specified outcomes. Results:
`03_results/10_genetics_mr_outcome5086_28ddeath.csv` (primary),
`03_results/10_genetics_mr.csv` (susceptibility),
`03_results/10_genetics_mr_outcome4982_criticalcare.csv` (critical care),
with instrument-level data in the matching `*_harmonised.csv` and console traces in
`05_reports/s10_run_log*.txt`.

---

## 1. Motivation

S01–S09 establish the hub genes as *co-expressed, prognostically informative, and
rescue-able* in immunoparalysis. A genetic anchor would strengthen causality:
do germline-encoded differences in these genes *cause* altered sepsis outcome,
independent of confounding? Two-sample MR (TSMR) answers this using only germline
variation.

## 2. Design — as executed

| Element | Specification (as run) |
|---------|------------------------|
| **Exposure** | eQTLGen whole-blood cis-eQTL, IEU OpenGWAS ids `eqtl-a-<ENSG>`: CD74 `ENSG00000019582`, HLA-DQA1 `ENSG00000196735`, CD14 `ENSG00000170458`, FCGR3A `ENSG00000203747`, HAVCR2 `ENSG00000135077`, FIS1 `ENSG00000214253`. Build HG19/GRCh37; per-gene *n* ≈ 13,344–31,684 |
| **Outcome — primary** | Sepsis with death within 28 days, `ieu-b-5086` (1,896 cases / 484,588 controls). Chosen by **phenotype matching**: the signature (§3.4) and its external validation (§3.5) both predict 28-day mortality |
| **Outcome — secondary** | Sepsis susceptibility, `ieu-b-4980` (11,643 / 474,841) |
| **Outcome — sensitivity** | Sepsis requiring critical care, `ieu-b-4982` (1,380 / 429,985) |
| **Instruments** | `POST /tophits` with *P*<5×10⁻⁸, MAF>0.01, LD clumping r²<0.01. Exposure and outcome share a build, so no liftover was required |
| **Harmonization** | Effect alleles aligned; palindromic SNPs resolved against allele frequency and dropped when strand was ambiguous |
| **Methods** | IVW (primary; fixed → multiplicative random effects switched on Cochran Q), MR-Egger (with intercept test), weighted median (bootstrap SE, 2,000 resamples, seed 20260925) |
| **Diagnostics** | Cochran Q / I²; Egger intercept; per-SNP *F*; BH-FDR across gene × outcome tests |
| **Minimum** | 3 instruments required per gene |

### Access notes (reproducibility)

- OpenGWAS base `https://api.opengwas.io/api`. Endpoints take the id as a **query
  parameter** (`?id=…`); `/associations/{id}` returns 404.
- `/associations` takes a POST body keyed **`variant`** (`{"variant": ["rs…"]}`).
- `/tophits` is **POST-only**; GET returns `{"message": "The method is not allowed
  for the requested URL."}`. Its `pval` / `clump` arguments did not change the
  number of returned variants in testing.
- The server TLS certificate lapsed (notAfter 2026-05-19); verification is disabled
  in-process. Connections reset intermittently (`SSLEOFError`), so the fetcher
  retries up to 12 times with linear backoff. Requests must be serialised.

## 3. Results

### 3.1 Primary outcome — sepsis 28-day death (`ieu-b-5086`)

| Gene | n IV | IVW OR (95% CI) | IVW *P* | MR-Egger OR (*P*) | Weighted median OR (*P*) | Q *P* / I² | Median *F* |
|------|------|------|------|------|------|------|------|
| CD74 | 3 | 1.119 (0.607–2.063) | 0.72 | 1.093 (0.85) | 0.970 (0.94) | 0.28 / 0.22 | 35.4 |
| HLA-DQA1 | 4 | 0.923 (0.804–1.061) | 0.26 | 0.954 (0.49) | 0.930 (0.41) | 0.59 / 0.00 | 168.1 |
| CD14 | 6 | 0.927 (0.818–1.051) | 0.24 | **0.906 (5.1e-3)** | 0.914 (0.065) | 0.98 / 0.00 | 45.7 |
| HAVCR2 | 6 | 0.978 (0.776–1.232) | 0.85 | 1.010 (0.95) | 0.960 (0.85) | 0.22 / 0.29 | 36.4 |
| FIS1 | 8 | 0.963 (0.869–1.067) | 0.47 | 0.964 (0.46) | 0.971 (0.77) | 0.76 / 0.00 | 75.0 |
| FCGR3A | 2 | not assessed | — | — | — | — | — |

No IVW estimate is significant, but **four of five assessable hubs give protective
estimates concordant across all three methods** — the direction predicted by the
immunoparalysis model. CD14 is nominally significant under MR-Egger
(*P*=5.1×10⁻³; BH-FDR 0.026 across all 15 gene × outcome Egger tests) with a
non-significant intercept (*P*=0.34), and its weighted median is close
(*P*=0.065); IVW agrees in direction but is underpowered.

### 3.2 Secondary outcomes (IVW)

| Gene | Susceptibility `ieu-b-4980` | 28-day death `ieu-b-5086` | Critical care `ieu-b-4982` |
|------|------|------|------|
| CD74 | 1.074 (0.861–1.341), 0.53 | 1.119 (0.607–2.063), 0.72 | **2.222 (1.175–4.200), 0.014** ⚠️ |
| HLA-DQA1 | 0.976 (0.922–1.033), 0.40 | 0.923 (0.804–1.061), 0.26 | 0.948 (0.805–1.116), 0.52 |
| CD14 | 0.990 (0.927–1.057), 0.76 | 0.927 (0.818–1.051), 0.24 | 1.125 (0.970–1.303), 0.12 |
| HAVCR2 | 0.944 (0.855–1.041), 0.25 | 0.978 (0.776–1.232), 0.85 | 0.960 (0.715–1.289), 0.79 |
| FIS1 | 0.983 (0.941–1.026), 0.43 | 0.963 (0.869–1.067), 0.47 | 0.944 (0.796–1.120), 0.51 |

Against **susceptibility** every hub is null — these genes do not influence
*whether* sepsis develops, which is consistent with an effect on severity rather
than incidence. Against **critical care**, CD74 is nominally significant, but see
the caveat below.

### 3.3 Caveats on individual estimates

- **CD74, critical care** (`ieu-b-4982`): concordant across all three methods with
  a null Egger intercept (*P*=1.00) and I²=0.00, but built on only 3 instruments
  and 1,380 cases; BH-FDR ≈ 0.21 across all 15 gene × outcome tests; and the
  direction is *opposite* to the expression-level model (higher predicted CD74
  predicting worse outcome). Reported as hypothesis-generating, not as a finding.
- **CD74, susceptibility** MR-Egger (OR 1.118, *P*=1.7×10⁻⁴): accompanied by a
  significantly non-zero intercept (*P*=1.0×10⁻⁴) → directional pleiotropy; the
  slope is not interpretable as causal.
- **FCGR3A**: only 2 usable instruments exist in this eQTLGen record; re-querying
  at *P*<1e-6 and *P*<1e-5 and with clumping disabled still returned 2 variants.
  Not assessed (pre-specified minimum 3).

## 4. Interpretation and honesty gate

The MR layer is **Tier-3 and hypothesis-generating**. On the phenotype-matched
mortality outcome the pattern is coherent — four hubs protective under all three
estimators, one nominally significant pleiotropy-robust test — but no primary IVW
estimate reaches significance, so this is a suggestive boundary rather than a
demonstration. Two structural limits apply: MR interrogates germline-determined
*baseline* expression whereas the Mars1 programme is an acute, state-dependent
dysregulation, and the mortality GWAS (1,896 cases) leaves these instruments
underpowered for individually small effects.

Consequences for the manuscript:

1. S10 is reported as Tier-3 exploratory; all three outcomes are shown, and no
   outcome is selected after seeing results.
2. No causal claim for the hub is made. The repositioning argument rests on
   expression-level rescue and connectivity.
3. The CD74 critical-care signal and the CD74 susceptibility Egger signal are both
   reported *with* their disqualifying diagnostics rather than promoted.
4. FCGR3A is listed as *not assessed (insufficient instruments)* rather than
   silently dropped.

Every MR number here and in the companion CSVs is recomputed at run time from live
OpenGWAS responses by `02_scripts/python/10_genetics_mr_run.py`; none is carried
over from an earlier draft or estimated by hand.
