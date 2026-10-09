# Supplemental Protocol — Experimental Validation of the Mars1 Immunoparalysis Hub and Drug-Repositioning Candidates

**Project:** Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis
**Companion to:** `05_reports/manuscript.md` (S07–S08; S09 external validation)
**Status:** Design blueprint (in-vitro / ex-vivo). Not yet executed.
**Authored:** 2026-09-25 · Yongxin Yang (ORCID 0009-0004-9698-6552)

---

## 0. Purpose & scope

This protocol translates the *in-silico* findings (S01–S09) into an experimentally
testable plan. It is written so that an independent wet-lab group can execute it
without re-deriving the bioinformatics. Every numeric claim below traces to a file
in `03_results/` (see §7 provenance).

**Central hypothesis (H0 to falsify).** The Mars1 immunosuppressed program is a
*coherent, rescue-able* state: the six hub genes
`CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1`
are co-downregulated in immunoparalysis, and axis-specific immune-stimulatory
agents (IL-7, GM-CSF, IFN-γ prioritized by S08) restore antigen-presentation and
monocytic function *above* the non-rescued baseline.

**What this protocol is NOT.** It is not a clinical trial. It validates mechanism
at the cellular level; human-outcome claims remain anchored on the 28-day mortality
signature (S06 CV-AUC 0.659; S09 independent AUC 0.638 on E-MTAB-4451).

---

## 1. Model systems (two complementary arms)

### Arm A — LPS-tolerance (endotoxin tolerance) on human immune cells
- **Primary PBMC** from ≥5 healthy donors (IRB-approved buffy coats; gender-balanced).
- **Isolation:** negative-selection monocytes (CD14+) and CD3+ T cells (Miltenyi).
- **Tolerance induction:** 24 h pre-exposure to LPS (100 ng/mL, *E. coli* O111:B4),
  then wash, then re-stimulate (LPS 100 ng/mL, 24 h). This reproduces the
  *decreased HLA-DR / blunted TNF-α* immunoparalysis phenotype (see S01/S02:
  Mars1 immune-score median −0.79, lowest of all endotypes).

### Arm B — Sepsis patient primary cells (clinical translation)
- **Cohort:** consecutively enrolled ICU sepsis patients (Sepsis-3), n≥20, with
  stored PAXgene/frozen PBMC collected within 24 h of ICU admission.
- **Stratify by endotype** using the S06 30-gene signature (or the published
  MARS endotype classifier) into Mars1-like vs Other.
- **IRB:** protocol MUST be approved **before** any sample collection
  (see §6 ethics note — this corrects the IRB-after-data-cutoff error of the
  companion PND project).

---

## 2. Interventions (axis-specific, S08-prioritized)

| Rank | Compound | Rationale (S08 rescue_fraction) | Dose range (literature) | Vehicle |
|------|----------|--------------------------------|--------------------------|---------|
| 1 | **IL-7** | 1.00 (CD3D/CD3E/CD8A/IL7R/LCK) | 10–50 ng/mL | PBS + 0.1% HSA |
| 2 | **GM-CSF** | 0.833 (HLA-DRA/DRB1/CD14/FCGR3A/ITGAM) | 10–100 ng/mL | PBS |
| 3 | **IFN-γ** | 0.714 (HLA-DRA/DRB1/DQA1/DQB1/CD74) | 10–100 U/mL | PBS |
| 4 | Azithromycin | 0.667 (HLA-DRA/CD14) | 1–10 µg/mL | DMSO <0.1% |
| 5 | Lenalidomide | 0.40 (HLA-DRA/DRB1) | 0.1–1 µM | DMSO <0.1% |
| 6 | Thymosin α1 | 0.40 (HLA-DRA/CD14) | 10–100 µg/mL | PBS |
| 7 | BCG (trained immunity) | 0.20 (HLA-DRA) | 1–10 µg/mL | PBS |

- **Positive control:** IFN-γ rescue of antigen-presentation (S08 gate: rescued
  4/5 genes) — must reproduce *in vitro* (HLA-DR MFI recovery ≥1.5-fold).
- **Negative control:** untreated LPS-tolerance; isotype/vehicle only.
- **Each condition:** n=3 biological donors × 3 technical replicates.

---

## 3. Primary and secondary endpoints

### Primary readout — axis-specific immunoparalysis restoration (endpoint matched to candidate mechanism)
- **Monocyte / antigen-presentation axis (primary for GM-CSF, IFN-γ):** CD14+ HLA-DR+ MFI (clinical gold-standard marker of
  monocyte immunoparalysis). Rescue = MFI ≥1.5× tolerance baseline, *P*<0.05. HLA-DR / HLA-DQA1 / CD74 surface & transcript (S05 hub genes).
- **T-cell / lymphoid axis (primary for IL-7):** because IL-7 is a T-cell homeostasis factor rather than a monocyte stimulator, its primary readout is CD3+/CD8+ T-cell count and activation (CD25/CD69) and IL-7-induced lymphocyte recovery, not monocyte HLA-DR; a monocyte-only primary endpoint would misclassify IL-7 as inert.
- **Multiplicity:** three candidate agents × two axis-specific primary endpoints are tested; family-wise error is controlled by the hierarchical go/no-go rule (§8) and, where parallel agents are compared, Dunnett correction against the tolerance control. The confirmatory patient-arm cohort uses n≥5 donors per condition to support the corrected threshold.

### Secondary readouts
1. **Cytokine rebound** — TNF-α, IL-6, IL-12p70 in supernatant after re-stimulation
   (LegendPlex / Luminex). Blunted in tolerance; restored by rescue.
2. **Antigen-presentation function** — Mixed Lymphocyte Reaction (MLR): patient/
   tolerated monocytes as stimulators, allogeneic CFSE-labeled T cells; proliferation
   = rescue of T-cell activation (links to CD3D/CD3E/LCK/IL7R axis).
3. **Phagocytosis** — pHrodo-*E. coli* uptake by CD14+ (FCGR3A/ITGAM axis).
4. **Checkpoint axis** — TIM-3 (HAVCR2) surface (S01: Mars1-up); expected to
   *decrease* under IL-7/IFN-γ rescue.

---

## 4. Transcriptomic confirmation (links to S06/S07)

- **qPCR panel (30-gene signature, `S06_signature_genes.csv`):** ΔΔCt rescue score
  per gene; report % of 30 genes significantly up-regulated post-intervention.
- **RNA-seq (optional, Arm B):** bulk + scRNA-seq of recovered cells to map
  restoration back to the S07 cell-type map (monocyte / dendritic / T-cell modules).
  Pre-register GEO/SRA upload.

---

## 5. Statistics & power

- **Primary endpoint:** one-way ANOVA + Dunnett vs tolerance control, FDR<0.05.
- **Sample size:** n=3 donors gives 80% power to detect 1.5× MFI change at α=0.05
  (paired, based on published HLA-DR tolerance SD≈0.25×mean). Expand to n≥5 donors
  for the patient-arm confirmatory cohort.
- **Rescue score:** mean oriented change of the 30-gene signature; 95% CI by
  bootstrap (10⁴ resamples), mirroring S09 bootstrap CI method.

---

## 6. Ethics & governance (mandatory)

- IRB / Ethics Committee approval **obtained before** any human sample work.
- Informed consent (or waiver for de-identified banked PBMC per local policy).
- Data deposited to a public repository with a versioned tag + MANIFEST checksum
  (per lab data-availability policy; no "available on request").
- Pre-registration of the primary endpoint (HLA-DR MFI rescue) recommended.

---

## 7. Provenance (every claim traces to a file)

| Claim | Source file |
|-------|-------------|
| 6 hub genes (tri-method consensus) | `03_results/S05_hub_genes.csv` |
| Mars1 immune-score lowest (median −0.79) | `03_results/S02_immunoparalysis_score.csv` |
| 30-gene signature & orientation | `03_results/S06_signature_genes.csv` |
| 7 repositioned candidates + rescue_fraction | `03_results/08_candidates_drugs.csv` |
| IFN-γ positive-control (4/5 genes) | `03_results/S08_l1000_positive_control.csv` |
| Hub cell-type localization | `03_results/07_hub_celltype.csv` |
| Independent external AUC 0.638 | `03_results/09_external_validation.csv` |

---

## 8. Go / No-go decision rule

- **GO (advance candidate to in-vivo/preclinical):** IL-7 or GM-CSF restores
  HLA-DR MFI ≥1.5× *and* ≥15/30 signature genes up-regulated *and* MLR recovery
  significant.
- **Partial:** single readout restored → report as hypothesis-generating.
- **No-go:** no candidate restores primary endpoint → reframe hub genes as
  *biomarkers* rather than *druggable nodes* (honest negative, pre-specified).
