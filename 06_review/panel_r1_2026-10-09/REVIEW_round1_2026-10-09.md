# Consolidated Independent Review — Round 1 (2026-10-09)

**Manuscript:** "A reproducible, fully auditable pipeline confirms within-cohort the MARS Mars1 immunoparalysis program and delivers an honest external validation of a 30-gene sepsis prognostic signature" (v1.24.0)
**Target venue:** BMC Bioinformatics (Research article / Methodology)
**Editor:** independent consolidation of a 5-expert blind panel (A1 domain, A2 design/statistics, A3 implementation/provenance, A4 venue/reporting, A5 repositioning/LINCS methods)
**Discipline:** each expert read only the manuscript + source result files, wrote one file, and was forbidden from reading any prior review, the manifest, the SOP, or project memory.

---

## 1. Independence statement

All five experts were briefed from a shared `_PANEL_BRIEF.md` that (a) forbade reading REVIEW_*/RESPONSE_*/REVISION_*/ROUND* files, the manifest, SOPs, author-verification statement, and project memory, and (b) required every judgement to come from text or source data each expert read themselves. Each wrote to a separate file and was forbidden from reading the others'.

**Evidence the independence worked:** the findings cluster on *already-known honesty themes but from different angles* (A1 Issue 2, A2 Issue 1, A5 Issue 1 all independently concluded "the manuscript under-states the weakness of its own claims"), while each layer also caught distinct, non-overlapping defects (A3 found the only arithmetic errors, A5 found the hidden binomial column, A4 found the S09/version/AI-disclosure format issues, A2 found the calibration-slope p-value omission, A1 found the TIM-3 mislabel and lenalidomide misattribution). No finding was unique to a single reviewer in a way that signals a too-diffuse panel; no finding merely re-litigated a previous round (there was none). The panel is well-targeted.

---

## 2. Verdict table

| Expert | Layer | Verdict | DESK-REJECT? |
|---|---|---|---|
| A1 | Domain (sepsis immunology) | Minor revision (if Issues 1–4 + DALI citation fixed; Issue 6 added as limitation) | No |
| A2 | Design/statistics | **Major revision** (framing/tiering: primary/sensitivity inversion, calibration-slope p buried, "validation" overstatement; EPV; orientation-tautology) | No (blocking *framing*, not data) |
| A3 | Implementation/provenance | Numbers 11/11 MATCH; 2 minor arithmetic/prov defects (prednisone z; CV-AUC cross-file) | No |
| A4 | Venue/reporting (BMC Bioinformatics) | No desk-reject trigger; ~8 format/polish issues (S09 cross-ref, version ambiguity, AI-disclosure, figure captions, cover-letter GitHub URL) | No |
| A5 | Repositioning/LINCS methods | **Major revision** (selective binomial reporting is integrity-adjacent; LINCS single-direction defect; Table 3 overstates) | No (blocking *method honesty*, not data) |

**Distribution:** 0 desk-reject; 2 major-revision (design + method); 2 minor/polish; 1 numeric-clean. The paper is numerically faithful and honestly self-critical — the blocking items are *claim-tiering and reporting completeness*, not fabrication or arithmetic failure.

---

## 3. Cross-verification table (manuscript vs independent recomputation)

A3 recomputed all 11 mandated headline assertions from authoritative source CSVs; **11/11 match** the manuscript. Editor independently re-verified the two most consequential numeric questions. The only genuine numeric *discrepancies* are minor:

| # | Manuscript location | Manuscript claims | Independently recomputed | Who checked | Verdict |
|---|---|---|---|---|---|
| 1 | §3.9 / §6 | prednisone LINCS z = **+2.03** | **+1.93** (rescue−mean)/sd; +2.03 = rescue/sd with mean dropped | A3, A5, **Editor** | DISCREPANCY (arithmetic) |
| 2 | §7 vs `S06_auc_compare.csv` / `09_external_validation.csv` | CV AUC "0.6586 … 0.6582; rounding artifact" | 0.6585576 vs 0.6582 = two stored runs, not one rounded number | A3, **Editor** | Mislabeled provenance |
| 3 | §3.7 / Table 3 / Limitation 8 | "no candidate's concordance exceeds the chance background … none distinguishable from chance" (tests only the 0.84 internal null) | Deposited `08_candidates_drugs.csv` contains `binom_p_allgene_bg` (genome-wide null 2592/11519=0.225): IL-7 **P=0.011**, GM-CSF **P=0.026**, IFN-γ **P=0.050** nominally significant | A5, **Editor** | **Selective reporting (most severe finding)** |
| 4 | §3.9 | "3-gene IRG proxy … weak reference" | oriented vs irg3 DeLong P=0.156 (A2: 0.1556; A3: 0.148) — non-significant both ways | A2, A3 | Match (interpretation issue) |
| 5 | §3.5 / §5 | calibration slope 0.50, intercept −0.04; only intercept CI given | slope p_slope_eq_1 = **0.0156** present in CSV, omitted from text; percentile CI (0.10–0.93) crosses 1 while Wald p=0.016 | A2, **Editor** | Reporting gap |
| — | all other 11 headline numbers (802 samples, 23/22/21, hub logFC/adj.P, score medians, external AUC 0.585/0.638 + CIs, SRS/age, signature size/zero-coefs, LINCS ranks/percentiles) | as stated | reproduced exactly from source | A3 (11/11) | MATCH |

**Editor's independent confirmation of the worst finding (#3):** I read `08_candidates_drugs.csv` directly; it contains both `binom_p_immune_bg` (0.817–1.000, the only column the manuscript reports) and `binom_p_allgene_bg` (0.011–0.720). I recomputed the genome-wide Mars1-down rate from `S01_mars1_deg.csv` as 2592/11519 = 0.225, which exactly reproduces the deposited hidden column. The manuscript's "none distinguishable from chance" claim is therefore **false under the proper null** and the proper null was already computed and deposited but suppressed. This is the single most serious issue and is a reporting-integrity defect, not a rounding slip.

---

## 4. Graded consolidated issue list

### Tier 1 — must fix before acceptance (reword + ≥1 new analysis)

- **T1-1 (reporting integrity, worst).** Selective binomial reporting in §3.7 / Table 3 / Limitation 8. Report the genome-wide null (`binom_p_allgene_bg`) alongside or instead of the circular 0.84 internal null; reframe concordance as descriptive; add a **genome-wide permutation null** (shuffle Mars1-down label across 11,519 genes ×1,000 iters, empirical P per candidate). *Must add analysis + reword.*
- **T1-2 (design/framing, spin).** Inverted primary/sensitivity hierarchy (A2-1): the CI-includes-0.5 locked-L1 is called "primary," the CI-excludes-0.5 equal-weight (the portable quantity) is demoted to "sensitivity." Re-tier: equal-weight = **primary transportability metric**; locked-L1 = sensitivity. *Reword only.*
- **T1-3 (design, miscalibration under-reported).** §3.5 reports near-zero intercept but buries slope 0.50 with p=0.0156. Report slope CI + p; reframe as over-confident (under-shrunk). Use BCa or Wald CI for the slope. *Rword + recompute CI.*
- **T1-4 (design, title overstatement).** "honest external validation" in title/abstract for a label-tied transport. Retitle to "label-tied external transport"; one abstract sentence "transport, not label-independent validation." *Reword only.*
- **T1-5 (design, EPV).** 30-gene signature at 52 external events (EPV≈1.7) cannot be "validated." Either pre-specify a parsimonious sub-signature sized to EPV, or explicitly frame the external step as **hypothesis-generating** and add an EPV table. *Reword + (optional) sub-signature.*
- **T1-6 (design, orientation tautology).** Add a **label-permutation negative control**: re-orient on shuffled 28-d labels, transport to E-MTAB-4451, show AUC collapses → 0.5; quantifies how much of 0.638 is orientation-tautology vs genuine transport. *Must add analysis.*
- **T1-7 (biology, tautology).** "confirm/anchored" overstates; hubs drawn from a predefined immune set and labels from same cohort. Switch to "recapitulate" in Abstract/§4/Conclusion/title. *Reword only.*
- **T1-8 (biology, TIM-3).** §3.1 reconciliation is partly backwards (sepsis lymphopenia lowers the bulk TIM-3 denominator, compatible with *more* per-cell exhaustion). Relabel HAVCR2 as a T-cell/exhaustion checkpoint (not "antigen-presentation/monocytic hub") in Abstract/Conclusion/title-block. *Reword only.*
- **T1-9 (biology, ImmunoSep).** §3.8 pivot "underscores transcriptomic endotyping" is unsupported; the 53% unclassifiable rate threatens the paper's own transcriptomic logic. Reword to "tempers, not merely cautions." *Reword only.*
- **T1-10 (repositioning, LINCS specificity).** Single-direction LINCS aggregation (rewards PDCD1/LAG3 up-regulation) is a construction defect; glucocorticoid control proves non-specificity. Re-label §3.9 control as a **specificity/negative control** and state the LINCS score gives **no** supporting evidence for either small molecule. Optionally recompute a dual-direction score. *Reword + (optional) recompute.*
- **T1-11 (repositioning, Table 3).** "Repositioning shortlist" + binomial P column overstates; 5/7 have no connectivity evidence. Rename to "Mechanism-anchored hypothesis annotation (illustrative)"; add "L1000 connectivity evidence: yes(2)/none(5)" column; report genome-wide null P (T1-1). *Reword + table edit.*

### Tier 2 — wording / specific corrections

- **T2-1.** Lenalidomide misattribution: ref 29 (McDaniel 2011, *Leukemia*) is an MDS paper, not a sepsis trial; drop "weaker dedicated sepsis trials" or re-cite. *Reword + citation.*
- **T2-2.** Missing landmark GM-CSF RCT (DALI, de Jong 2016) — add reference; bounds the "most clinically ready" claim. *Add citation + caveat.*
- **T2-3.** Add limitation: Mars1 transcriptomic status never demonstrated to predict mHLA-DR-low or cytokine inducibility. *Add limitation.*
- **T2-4.** DeLong vs 3-gene: state non-inferiority, not superiority ("incremental discrimination unestablished"). *Reword.*
- **T2-5.** SRS benchmark: flag post-hoc direction flip (max(AUC,1−AUC)); incremental value non-significant (ΔAUC +0.028, P=0.69). *Reword.*
- **T2-6.** Bootstrap slope percentile CI unreliable vs Wald p=0.016 → use BCa/Wald. *Reword + recompute.*
- **T2-7.** prednisone z **+2.03 → +1.93** in §3.9 and §6. *Arithmetic fix.*
- **T2-8.** CV-AUC "rounding artifact" mislabel → reword §7 or regenerate `09_external_validation.csv`. *Reword.*
- **T2-9.** §7 "positive control" row mis-targeted (`08_positive_control_check.csv` vs `S08_l1000_positive_control.csv`). *Fix citation.*
- **T2-10.** §7 GPL13667 not in CSV → cite the family SOFT as authoritative source for the token. *Housekeeping.*
- **T2-11.** A4 I-1/I-2: §8 S09 points to "Limitation 7" but deferred in Limitation 6; S09 simultaneously "deferred" and "deposited." Fix cross-ref; resolve deferred-vs-deposited. *Fix.*
- **T2-12.** A4 I-3: version ambiguity v1.16.0 vs v1.24.0 → clarify cited result files are frozen at tag v1.24.0. *Reword.*
- **T2-13.** A4 I-4: AI disclosure name the LLM class ("OpenAI/Anthropic-class"), not just "fungible." *Reword.*
- **T2-14.** A4 I-5: structured abstract "positive-control gate" → "positive-control check." *Reword.*
- **T2-15.** A4 I-6: add formal `*Fig. S6A/B/C*` and `*Fig. S7*` captions in body. *Add captions.*
- **T2-16.** A4 I-7: add GitHub URL + tag to cover letter. *Edit cover letter.*
- **T2-17.** A4 I-8: add one sentence foregrounding methodological novelty (three-tier positive-anchor design + §7 provenance table). *Add sentence.*
- **T2-18.** A5-5: S11 monocyte-only primary endpoint misclassifies IL-7 (T-cell candidate); make endpoint axis-specific; add multiplicity note; raise donor target to n≥5. *Reword blueprint.*

### Tier 3 — format / housekeeping

- T3-1: consistent z-centring formula across all three LINCS numbers (prednisone +1.93 under same formula).
- T3-2: ensure all §7 cited files exist (A3 confirmed all present — no action).
- T3-3: confirm Frontiers DOIs (refs 8/17/33) via PubMed/CrossRef before final submit (A4: bot-wall, not 404).

---

## 5. Consensus / complementarity / disagreement

**Consensus (all 5):** the manuscript is numerically faithful (A3 11/11), genuinely and commendably self-critical about its own null/modest results, venue-appropriate for BMC Bioinformatics, and carries no desk-reject trigger. The strongest shared message: *the manuscript's honesty must be extended to its claim-tiering and to the repositioning statistics* — A1-2, A2-1, A5-1 independently arrived at this from biology, design, and method angles respectively.

**Complementarity:** each layer caught distinct defects with no overlap — A3 the only arithmetic errors; A5 the hidden binomial column; A4 the S09/version/AI/figure-caption format issues; A2 the calibration-slope p-value and EPV; A1 the TIM-3 mislabel and lenalidomide misattribution. The independence discipline produced additive coverage, exactly as intended.

**Disagreement:** **severity**. A4 (venue) rated the paper minor-revision / no desk-reject; A2 (design) and A5 (method) rated major-revision. Adjudication: adopt the stricter verdict for the design/method items (T1-2, T1-3, T1-6, T1-10, T1-1) because A4's lenient "minor" scope is explicitly limited to format/hard-fail, which does not certify the manuscript against design-layer or method-integrity objections. The paper is **Major Revision**, not rejection: every blocking item is a reword or a small, feasible new analysis, and the core biology (Mars1 program recapitulated; external transport real-but-modest) is sound.

No disagreement on article type: A4 notes Methodology article is an equally valid framing; no expert objects to Research article.

---

## 6. Priority must-fix list

**Must add analysis (new computations):**
1. T1-1 genome-wide permutation null for the binomial concordance (shuffle Mars1-down ×1,000; empirical P per candidate) + report `binom_p_allgene_bg`.
2. T1-3 BCa (or Wald) CI for calibration slope + report p_slope_eq_1.
3. T1-6 label-permutation negative control (orientation shuffle → external AUC collapses to ~0.5).
4. T1-10 (optional) dual-direction LINCS score (flip PDCD1/LAG3 sign) — recompute candidate ranks.

**Must reword (no new numbers):**
- T1-2 re-tier primary/sensitivity; T1-4 title "transport" not "validation"; T1-7 "recapitulate"; T1-8 TIM-3 relabel; T1-9 ImmunoSep pivot; T1-5 EPV/hypothesis-generating; T1-10 LINCS specificity reframe; T1-11 Table 3 rename + connectivity column; T2-1 lenalidomide; T2-2 DALI; T2-3 mHLA-DR limitation; T2-4 DeLong; T2-5 SRS; T2-6 slope CI; T2-7 prednisone z; T2-8 CV-AUC; T2-11/12 S09 + version; T2-13 AI model; T2-14 abstract gate; T2-15 captions; T2-17 novelty sentence; T2-18 S11 endpoint; A4 I-7 cover-letter GitHub URL.

**DESK-REJECT flags:** None. (No T0 that invalidates the whole manuscript; T1-1 is integrity-adjacent but fixable by reporting + permutation null.)

---

## 7. What stands up (do NOT change)

1. mHLA-DR vs transcriptomic mRNA proxy — rigorously distinguished (A1, A4).
2. External-validation candour — primary CI includes 0.5, honestly labelled (A1, A2, A4).
3. LINCS glucocorticoid caveat — self-critical, correct logic (A1, A5).
4. FIS1 correctly NOT called an immune hub (A1).
5. Mars1 vs Mars2 non-separability openly stated (A1).
6. Within-cohort-confirmation disclosure present (A1).
7. DCA "≥0.80 collapses to treat-none" — factually correct (A2).
8. All headline AUC/DeLong reproduce exactly; no fabrication (A3).
9. wtcs = rescue × √22 exact; LINCS ranks/percentiles/background correct (A5).
10. Figure/table numbering 1:1 consistent; all 40 refs cited, sampled DOIs real; structured abstract compliant; BMC declarations complete (A4).
11. Prior BMC Medical Genomics desk-reject honestly disclosed (A4).

---

## 8. Recommended handling path

**A) Restructure & resubmit as the same article type (Research article).** This is the correct path. The blocking items are claim-tiering and reporting completeness, not data failure. Required moves: (i) swap the headline emphasis so the *portable equal-weight* result carries the external claim and the locked-L1 is the sensitivity (T1-2); (ii) stop calling a label-tied transport a "validation" in the title (T1-4); (iii) report the suppressed genome-wide binomial null + add a permutation null, reframing the drug list as hypothesis annotation (T1-1, T1-11); (iv) report the calibration-slope p-value and re-label the LINCS control as a specificity/negative control (T1-3, T1-10); (v) add the label-permutation negative control (T1-6).

**B) Downgrade article type to Methodology** — not required; the auditable-pipeline + honest-transport contribution is real and the strongest finding. If anything, foreground the methodology (T2-17) rather than downgrade.

**C) Wording-only** — not viable; T1-1, T1-2, T1-6 require either new analysis or structural re-tiering, not just phrasing.

---

## 9. Process lessons (what gates could not have caught)

- The automated `verify_submission_bmcbio.py` gate checks arithmetic self-consistency and presence of strings; it **cannot** ask "is the reported null the right null?" The hidden `binom_p_allgene_bg` column passed the gate because the gate only checks the *manuscript* text, not the *deposited CSV columns the manuscript omitted*. **New gate recommendation:** a provenance gate should diff every column of every cited CSV against what the manuscript actually reports, and flag columns that exist in source but are never cited. This would have caught T1-1 automatically.
- A gate cannot detect "primary/sensitivity inverted" (T1-2) or "validation vs transport" (T1-4) — these are design-layer semantic defects. Only human design review catches them.
- "Confirm/anchored" vs "recapitulate" (T1-7) is a framing tell a domain reviewer catches; a gate cannot.
- Lesson for the author's general workflow: when a null hypothesis is computed two ways (internal 0.84 vs genome-wide 0.225), **both must be reported**; selective reporting of the favorable null is the single biggest avoidable risk in an honesty-postured paper.
