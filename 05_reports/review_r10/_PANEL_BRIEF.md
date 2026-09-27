# Round-10 Independent Panel — Panel Brief (editor's reference)

**Manuscript under review:** `05_reports/manuscript.md`, evaluated at git tag **v1.9.0** (commit `96f43eb`).
**Repository:** https://github.com/yyx-4113/sepsis-immunoparalysis-hub
**Study type:** Single-author bioinformatics re-analysis. Re-analysis of GSE65682 (sepsis MARS transcriptomic endotypes, n=802) to triangulate "immunoparalysis hub genes" of the Mars1 (immunosuppressed) endotype, plus an honest independent external validation (E-MTAB-4451, n=106), a mechanism-anchored drug-repositioning shortlist (LINCS L1000 connectivity), and a two-sample MR layer (eQTLGen × UK Biobank sepsis GWAS, 45 tests).

---

## Independence discipline (mandatory)

**Forbidden to read (for every reviewer):**
- `05_reports/REVIEW_round*.md` (rounds 1–9 consolidated reports)
- `05_reports/RESPONSE*.md`, `05_reports/REVISION*.md`, any `*_response*.md`
- Every prior review sub-directory: `05_reports/review_r1/`, `review_r2/`, … `review_r9/`
- Any file that summarizes prior review rounds, the task status, or the project overview
- `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`
- **Other reviewers' outputs in `05_reports/review_r10/`** (written by A1–A4) — do not read them.

**Treat `05_reports/manuscript.md` (v1.9.0) as a first submission.** Do not assume it is mature or has passed previous review. Every judgement must come from text or source data you read yourself. Any claim in the manuscript that you CAN verify, you MUST verify.

---

## The article-type question (open item for the panel, esp. A4)

The manuscript positions itself as a **Research Article** with a discovery framing ("immunoparalysis hub genes … multi-omics dissection and in-silico drug repositioning"). However, **the manuscript's own text** states:
- The five immune hubs "largely recapitulate the antigen-presentation / monocytic program that defines the Mars1 endotype in the original MARS-consortium work … this is a near-replication rather than a novel gene discovery" (Discussion).
- The MR layer is entirely null on the primary outcome: exactly 1/45 family-corrected tests is significant and it reverses direction; "no primary IVW estimate reached significance" (Results §3.10, Limitations 2).

The panel must evaluate, **independently and from the manuscript + source data alone** (not from any prior review's conclusion):
1. Is the current Research-article / discovery framing honestly supported by the evidence, or is the genuine contribution methodological transparency + an honest external validation + an explicit experimental blueprint?
2. Should the article be **reframed as a Computational Biology / Methods & Resources** article (or otherwise retitled/restructured)? If so, specify the concrete title / abstract / structure / emphasis changes.
3. Or is a **headline-swap within the Research type** sufficient (lead with the method/transparency contribution, demote the discovery claims)?

---

## Source data the reviewers MUST recompute from

| File | What to verify |
|------|----------------|
| `03_results/10_mr_bh_family.csv` | 45-test BH; column `q_family_45test`, flag `family_sig_q<0.05`. Confirm only 1/45 significant and it reverses direction. |
| `03_results/10_genetics_mr_outcome5086_28ddeath.csv` | Table 3 MR-Egger p-values. **These are t(n−2)-distributed, NOT normal** — recompute with `2*st.t.sf(\|β/se\|, df=n_snp−2)`. |
| `03_results/09_external_validation.csv` | External AUC orientedSum 0.6382 (CI 0.5317–0.7475), IRG 0.604, L1-locked 0.5848. |
| `03_results/S01_immunoparalysis_direction.csv` | HAVCR2/TIM-3 direction (claimed down, logFC −0.35, adj.P 2.8e-13); PDCD1/LAG3 up. |
| `03_results/S05_hub_genes.csv` | 6 co-expression-associated genes (5 immune hubs + FIS1). |
| `03_results/S02_immunoparalysis_score.csv` | Mars1 median immune score −0.792. |
| `03_results/08_candidates_drugs.csv`, `03_results/S08_l1000_candidate_scores.csv` | Drug shortlist concordance fractions; LINCS rescue ranks. |
| `02_scripts/python/check_audit_assertions.py` | 18 audit assertions (read, do not trust blindly). |

---

## Environment traps (learned the hard way)

- **MR-Egger p is t-distributed.** The CSV stores `2*st.t.sf(|β/se|, df=nsnp−2)`. If the manuscript Table 3 Egger p differs from the CSV, that is a stale (normal-distribution) value — flag it.
- **Sample overlap** eQTLGen ↔ UK Biobank not corrected by the authors (they state this). MR is hypothesis-generating only.
- **External AUC 0.638** is the orientedSum (fixed-orientation equal-weight) score; **0.585** is the L1-locked model. Both are real; do not conflate.
- **Selection-on-outcome circularity** (Limitation 12): the 6 candidate genes were selected from the same cohort, then MR-tested. The MR null = "no evidence for causality in these specific candidates," not a refutation of the expression association.
- **No tool talk** in review outputs: write review comments only, do not describe what tools you used.

---

## Output contract (every item needs all four)

- **【Problem】** one sentence.
- **【Evidence】** pinned to file:line, or table/section + exact numbers; numbers you cite must be ones you recomputed yourself.
- **【Why it matters】** concrete effect on conclusions / credibility / acceptance.
- **【Specific fix】** a paste-ready English replacement sentence, or an explicit spec for a new analysis.

Also required: § Stands up (≥3, with evidence — things you suspected but found correct); § Questions for the authors; § What I actually checked (files read, commands run, values recomputed vs manuscript, with discrepancy stated).

---

## Panel

- **A1 — Domain (sepsis immunology / critical-care clinician-scientist)**
- **A2 — Design & statistics (causal inference / biostats)**
- **A3 — Implementation & provenance (recompute auditor)**
- **A4 — Venue & reporting-standard auditor (incl. article-type question)**
