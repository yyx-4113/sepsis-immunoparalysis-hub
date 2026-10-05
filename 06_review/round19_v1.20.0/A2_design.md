# A2 — Design review (statistics / ML methodology)

**Manuscript:** v1.20.0, `github.com/yyx-4113/sepsis-immunoparalysis-hub` (tag v1.20.0), target *BMC Medical Genomics*.
**Role:** Design = statistics / machine-learning methodology. MR layer assumed absent (per brief); any MR residue flagged as stale artifact only.
**Independence:** I read only `05_reports/manuscript.md`, `02_scripts/` and the `03_results/` CSVs listed as permitted; I did not open any other reviewer file, response, or memory. Every number I cite was either read from a results CSV or recomputed by me from `03_results/09_ext_risk_scores.csv` (command shown in §"What I actually checked").

---

## Executive summary

The pipeline is unusually transparent for a single-author computational paper: the optimistic within-cohort CV, the single-direction LINCS metric, and the glucocorticoid caveat are all disclosed. That honesty is a genuine strength and I have credited it (§"Stands up"). However, several design-level defects remain that a statistical gate cannot catch and that materially affect how the prognostic and repositioning claims should be read:

1. The external headline **AUC 0.638 is the equal-weight oriented-sum, not the fitted L1 model (0.585)**; the two external metrics differ by a scoring-rule choice made *after* the test labels were available, and the internal-vs-external comparison mixes scoring rules (L1 internally, equal-weight externally).
2. The reported **5-fold CV AUC 0.659 is not nested** — gene selection used the outcome labels before the split — so it is not a valid pipeline CV and should not be headlined as "cross-validated".
3. The **DCA grid shows the model is identical to treat-all below threshold 0.25 and collapses to treat-none at 0.80**; a "diverges from treat-all at 0.80" reading mistakes "flags nobody" for benefit.
4. The **LINCS positive-control panel cannot validate immune rescue**: 0/5 genuine immuno-stimulants recover, and the only strong positive (prednisone, top 3.2%) is an immunosuppressant scored in the wrong direction; the query also rewards up-regulation of the Mars1-*up* exhaustion markers PDCD1/LAG3.
5. **MR residue** (columns `observed_mr_or_ivw`, `predicted_mr_direction`) remains in a shipped results table although the MR layer was removed.

Each item below carries the four required parts.

---

## D1 — The external headline "AUC 0.638" is the equal-weight score, not the fitted model; the two external metrics differ by a post-hoc scoring-rule choice

【Problem】 The manuscript's primary external metric (0.638) and its "locked L1" metric (0.585) are two different scoring rules applied to the same 29 genes, and the higher one (equal-weight oriented-sum) is presented as *the* signature AUC even though the actual fitted model transports at only 0.585.

【Evidence】 `03_results/09_external_validation.csv`: `auc_EMTAB4451_orientedSum = 0.6382` and `auc_EMTAB4451_external_locked = 0.5848`; `manuscript.md:195` writes "External validation AUC 0.638 (CI 0.532–0.748) / locked L1 0.585"; `manuscript.md:104` states the equal-weight score "is reported as the primary external metric because it carries no cohort-specific weights." I recomputed AUC(oriented_sum)=0.6382 and AUC(locked_l1)=0.5848 directly from `09_ext_risk_scores.csv` (command in §"What I checked") — both reproduce. The 0.053 gap between the two external numbers is purely the scoring rule (orientation-sum vs L1 coefficients), and the orientation signs were fixed using GSE65682 death labels (`02_scripts/python/09_external_validation.py:73`, `run_tier1.py:224-235`).

【Why it matters】 A reader seeing "external AUC 0.638" reads it as the signature's generalization; the honest transport of the *model that was actually trained* is 0.585, whose 95% CI (0.469–0.696, `09_external_validation.csv`) includes 0.5. Presenting the higher, simpler score as primary, with the fitted model demoted to a parenthesis, is optimism-by-score-selection and overstates the prognostic signal. It also makes the internal→external comparison unfair: §3.4 compares internal **L1** CV 0.659 with external **equal-weight** 0.638, mixing rules so the apparent transport loss (0.021) is understated versus the like-for-like L1 drop of 0.074 that the manuscript itself reports two sentences later.

【Specific fix】 Either (a) make the locked L1 external AUC 0.585 (95% CI 0.469–0.696) the *primary* generalization metric, since it is the model that was trained and locked, and report the equal-weight 0.638 as a pre-registered sensitivity analysis; or (b) pre-specify in Methods (before any look at E-MTAB-4451) that the equal-weight fixed-orientation score is the signature definition and justify why equal-weight is preferred to the fitted L1. Replace the cross-rule sentence "External validation AUC 0.638 … / locked L1 0.585" with a like-for-like statement, e.g.: "The locked L1 model transported to E-MTAB-4451 at AUC 0.585 (95% CI 0.469–0.696); a pre-specified equal-weight fixed-orientation sensitivity score gave AUC 0.638 (95% CI 0.532–0.748). Both are modest and the L1 CI includes 0.5."

---

## D2 — The 5-fold CV AUC 0.659 is not nested; feature selection used the outcome before the split

【Problem】 The signature's 30 genes are selected by |correlation with 28-day death| on the full sepsis set, and *then* a 5-fold CV is run on the fixed feature matrix — so the CV estimates only the classifier fit, not the selection, and is optimistic.

【Evidence】 `02_scripts/python/run_tier1.py:224-235`: `corr_d[g]` is computed against `ysig` (all sepsis 28-day labels) and `sig30 = sImm.head(30)` is taken before the `StratifiedKFold` at `run_tier1.py:243-248`, whose loop only re-fits `m.fit(Xsig_s[tr], ysig[tr])`. Events-per-variable = 114 deaths / 30 genes = 3.8 (`manuscript.md:104`), below the conventional ≥10. The CSV `S06_auc_compare.csv` reports "Immune-risk signature (CV)" = 0.6586 and "(train)" = 0.7495; `manuscript.md:194` headlines "CV AUC 0.659 / training 0.750".

【Why it matters】 "5-fold cross-validated AUC of 0.659" is presented as the model's performance in the first sentence of §3.4 and in the §7 provenance table, yet it is an inner-loop CV after fixed feature selection. The selection-on-labels component of optimism is only visible via the external drop and is easy to miss. The headline therefore overstates pipeline performance; the honest in-cohort optimism estimate requires nested selection.

【Specific fix】 Add a nested CV on GSE65682: in each of K outer folds, select top-30-by-|r| within the training fold only, fit L1, score the held-out fold, and report the mean outer-fold AUC as the in-cohort optimism estimate (expected ≈ 0.59–0.62, not 0.659). Then demote the current 0.659 to "inner-loop CV after fixed feature selection" and keep 0.585/0.638 as the only generalization claims. Add the EPV caveat (3.8) next to the CV number, not only mid-paragraph.

---

## D3 — DCA: the model equals treat-all below 0.25 and collapses to treat-none at 0.80; "divergence at 0.80" misreads the grid

【Problem】 On the external DCA grid the model's net benefit is identical to treat-all at low thresholds and falls to treat-none (NB = 0) at 0.80, so any claim that the model "diverges from treat-all at 0.80" conflates "flags no patients" with clinical benefit.

【Evidence】 `03_results/09_ext_dca_grid.csv`: at thresholds 0.05–0.25, `nb_model == nb_treat_all` (e.g., 0.05: 0.4638 = 0.4638; 0.25: 0.3208 = 0.3208) with `n_flagged = 106` (every patient flagged = treat-all); at 0.80, `nb_model = 0.0` and `n_flagged = 0` while `nb_treat_all = -1.5472`; the model's NB exceeds treat-all only in the ≈0.30–0.75 band by <0.12 (e.g., 0.50: 0.0755 vs −0.0189; 0.65: 0.0418 vs −0.4555). Calibration used to build the DCA is `09_ext_calibration_dca.csv` slope 0.5028. I did not find the literal word "diverges" in `manuscript.md`, but the panel orientation and Fig. S6C caption rest on this grid; the grid itself is the evidence.

【Why it matters】 A decision curve is only useful where the model beats *both* defaults (treat-none and treat-all). Here the model is treat-all for thresholds ≤0.25 and treat-none for thresholds ≥0.75; in the only usable band its absolute NB is small (max 0.46 at 0.05, declining to ≈0.04 by 0.65). Stating "diverges from treat-all at 0.80" implies the model is doing something at 0.80 when it is simply recommending no treatment (NB = 0, equal to doing nothing). This mislocates where, if anywhere, the score supports a treatment decision.

【Specific fix】 Report the threshold band where `model NB > max(treat-all NB, treat-none NB)` with the absolute NB and its bootstrap CI (e.g., resample patients 2000×, recompute NB at each threshold), and state explicitly: "Below threshold ≈0.25 the score is equivalent to treat-all (flags all 106); above ≈0.75 it collapses to treat-none (flags 0); in the 0.30–0.75 band it marginally exceeds treat-all by <0.12 NB, which is weak decision support at n = 106." Do not describe 0.80 as a point of divergence.

---

## D4 — LINCS positive-control set cannot validate immune rescue; 0/5 immuno-stimulants recover and the only strong positive is an immunosuppressant

【Problem】 The reverse-connectivity positive-control panel contains no correctly-directed immuno-stimulant that recovers, while the single strong positive (prednisone) is a glucocorticoid that should *not* rescue immunoparalysis, so the metric has no demonstrated face validity for its stated purpose.

【Evidence】 `03_results/S08_l1000_positive_control.csv`: prednisone rescue_score 0.1364, rank 651/20,413 (3.2nd percentile); dexamethasone 0.0315, rank 6,808 (33.4th, below median); entinostat 0.05, rank 4,821 (23.6th); lenalidomide 0.0439, rank 5,435 (26.6th); vorinostat 0.0172, rank 8,647 (42.4th); azithromycin 0.0133, rank 9,152 (44.8th); interferon-gamma and romidepsin are "absent from trt_cp." `manuscript.md:137` itself notes "prednisone scored high … dexamethasone did not … the glucocorticoid positive control is therefore carried by prednisone alone" and that a metric on which an immunosuppressant scores z = +2.03 "carries no discriminating information."

【Why it matters】 A reverse-connectivity score whose only strong positive is an immunosuppressant, and on which every genuine immuno-stimulant (lenalidomide, entinostat, vorinostat, azithromycin) sits at or below the library median, has not been shown to detect immune rescue. The §2.8 "positive-control gate" therefore did not pass for the intended biological question, yet the Methods still frames it as a gate; the manuscript's correct retreat to "descriptive only" (§3.9, Limitation 8/10) is undermined by the gate language.

【Specific fix】 Add at least one immuno-stimulant perturbagen actually present in `trt_cp` (an IFN-γ or GM-CSF L1000 signature) and pre-specify a recovery threshold (e.g., top 10% of 20,413). If none recovers, relabel §2.8/§3.9 as "exploratory reverse-connectivity with no passing positive control" and remove the word "gate." State plainly: "No correctly-directed immuno-stimulant positive control recovered; the L1000 rescue score is therefore unrevalidated for immune rescue."

---

## D5 — The L1000 rescue query is sign-errorneous on exhaustion markers and single-direction

【Problem】 All 22 query genes are aggregated with the same sign, so the metric rewards *up*-regulation of PDCD1 and LAG3 (Mars1-*up* exhaustion markers) as if that were rescue, although rescue of immunoparalysis requires those markers to be *down*-regulated.

【Evidence】 `02_scripts/python/S08_l1000_connectivity.py:91-93`: `rescue = mean_pct.mean(axis=0) - 0.5` and `wtcs = (mean_pct.sum(axis=0) - n*0.5)/sqrt(n)` over the 22 genes with one sign; `manuscript.md:133` states PDCD1/LAG3 are "aggregated with the same sign" and that the dual-direction requirement "was not implemented," and Limitation 10 repeats this. The query set (`manuscript.md:133`) explicitly includes the Mars1-*up* markers PDCD1 and LAG3.

【Why it matters】 "Rescue" is partially the opposite of the biology: a drug that suitably *down*-regulates exhaustion markers scores *worse* on this metric, while a drug that further activates PDCD1/LAG3 scores *better*. The reverse-connectivity therefore measures Mars1-down-axis reversal only, and even there it is contaminated by exhaustion-marker up-regulation — exactly the component that should move the other way.

【Specific fix】 Split the 22-gene query into Mars1-down (should be up-regulated: positive contribution) and Mars1-up exhaustion (PDCD1/LAG3; should be down-regulated: negative contribution) and compute a signed dual-direction score, e.g. `score = mean(up_gene_percentile) − mean(down_gene_percentile) − 0.5` (or the standard LINCS WTCS with signed query). Alternatively, restrict the query to the Mars1-down antigen-presentation/monocytic genes only and state the metric no longer addresses exhaustion reversal.

---

## D6 — One-sided mean-rank statistic with no negative control can be driven by global expression inflation

【Problem】 `rescue = mean rank-percentile − 0.5` is a one-sided enrichment of the 22 genes with no down-component and no negative-control drug set, so any broadly transcriptionally activating perturbagen scores positive regardless of specific axis reversal.

【Evidence】 `S08_l1000_connectivity.py:91-93`; `manuscript.md:133` reports background "mean 0.006, median 0.006; 53.6% of compounds > 0," i.e. just over half of all 20,413 compounds already score positive by construction. The candidate small molecules lenalidomide (z = +0.56) and azithromycin (z = +0.10) sit inside this noise band (`manuscript.md:135`).

【Why it matters】 With 53.6% of *all* compounds already positive and no signed query, a positive rescue score is nearly uninformative; the "rescue" can reflect general expression-level inflation rather than specific reversal of the immunoparalysis axis. This compounds D4/D5: the metric is both sign-indefensible and low-signal.

【Specific fix】 Use the canonical signed LINCS connectivity (query genes up vs down; cosine/WTCS against the perturbagen's signed z-score profile), or at minimum add a negative-control drug set expected to score ≈0 (e.g., non-immune cytotoxic agents) and report their score distribution; require candidate rescuers to exceed the negative-control 95th percentile, not merely to be >0.

---

## D7 — Cellular-localization is a bulk-marker max-|r| call with weak/rare-cell correlations; FIS1's assignment is an artifact

【Problem】 The "single-cell" cellular context (§3.6) is a bulk-marker correlation reporting only the max-|r| cell type, with modest correlations and sparse markers for rare populations, so assignments are low-confidence and FIS1's "Monocyte" call is a max-|r| artifact on a mitochondrial/erythroid gene.

【Evidence】 `03_results/07_hub_celltype.csv`: FIS1 best Monocyte r = −0.438 (negative); NK max r = −0.191; dendritic 0.69 (CD74); B-cell 0.68 (HLA-DQA1); CD14 0.773; only 7–8 marker genes per cell type. `manuscript.md:49` is transparent that this is "marker-module correlation across bulk samples … bulk surrogate, not true single-cell resolution," and §3.6 repeats both views are bulk surrogates. The manuscript also states FIS1 entered via the degree-centrality branch, not the immune-annotated branch (`manuscript.md:100`).

【Why it matters】 Reporting a single "dominant context" from few markers, where the strongest correlation for FIS1 is a *negative* −0.438 with monocytes, invites over-reading of cellular specificity that the data cannot support; rare cell types (NK, dendritic) are sparsely represented and their correlations are unstable. This is a limitation the manuscript names but the table presentation (one "best_celltype" column) understates.

【Specific fix】 Report the full correlation matrix (already in the file) with 95% CIs and a pre-specified significance threshold (e.g., |r| with FDR < 0.05 across cell types); state "no reliable cellular context" when no cell type meets it. For FIS1, replace "Monocyte (r = −0.438)" with "no cell type reached the significance threshold; assignment unreliable." Keep the explicit bulk-surrogate caveat in the caption of Fig. S7.

---

## D8 — MR residue remains in a shipped results table after the MR layer was removed

【Problem】 `S06_hub_death_association.csv` still carries Mendelian-randomisation columns (`predicted_mr_direction`, `observed_mr_or_ivw`, `concordant`), contradicting the v1.20.0 removal of the MR layer.

【Evidence】 `03_results/S06_hub_death_association.csv` columns: `gene, mars1_logFC, corr_with_death, or_per_sd, ci, p, predicted_mr_direction, observed_mr_or_ivw, concordant`. The MR layer is gone from v1.20.0 per the brief; the file also is not listed in the §7 number-provenance table (which lists only `S05_hub_genes.csv` for hubs), so it is an orphaned MR-bearing artifact.

【Why it matters】 Although the manuscript text does not cite these columns, shipping an MR-table alongside a "MR-removed" manuscript risks accidental reinclusion or reviewer confusion about whether MR evidence still underpins the hub claims (e.g., the `concordant` column implies an MR concordance check that no longer exists in the paper).

【Specific fix】 Strip the MR columns (`predicted_mr_direction`, `observed_mr_or_ivw`, `concordant`) from `S06_hub_death_association.csv` (or delete the file if unused), retaining only `gene, mars1_logFC, corr_with_death, or_per_sd, ci, p`. Confirm no other `03_results/` CSV references MR (the `10_*` MR files may remain only as the removed-layer backup).

---

## D9 — Hub-death associations are not family-wise corrected; two of six hubs fail Bonferroni

【Problem】 The six hub 28-day-death associations are reported with uncorrected p-values although the hub set was selected on the same outcome, so the per-hub significance is overstated.

【Evidence】 `03_results/S06_hub_death_association.csv` p-values: FIS1 0.00735, CD74 0.000458, HLA-DQA1 0.0107, CD14 0.00252, FCGR3A 0.000648, HAVCR2 0.0785. Bonferroni across 6 tests = 0.05/6 = 0.0083; HAVCR2 (0.0785) and HLA-DQA1 (0.0107) do not survive. `manuscript.md:166` (Limitation 9) acknowledges the *selection chain* FWER is uncontrolled for hub discovery but does not extend correction to this hub-death table.

【Why it matters】 The hubs were chosen by a tri-method ML consensus that already reused the 28-day labels (`run_tier1.py:174-210`), so the hub-death p-values are not independent of selection. Reporting them uncorrected lets HAVCR2 (p = 0.08, CI 0.65–1.02 includes 1.0) appear as a significant mortality-associated hub when it is not.

【Specific fix】 Apply Holm/Bonferroni across the 6 hubs and report adjusted p-values; where a hub fails (HAVCR2, and note HLA-DQA1 is marginal), present it as exploratory. Add one sentence: "Because the hub set was selected on the same 28-day outcome, hub-death p-values are selection-dependent and reported Holm-adjusted; HAVCR2 (adj. p = X) does not reach significance."

---

## § Stands up (verified correct)

1. **External validation is genuinely independent in cohort and platform, and not label-leaked from GSE65682.** `09_external_validation.py:59-66` reads 28-day survival from `E-MTAB-4451.sdrf.txt` (different study, different platform GPL10558 vs GPL13667); GSE65682 death labels are used only to select/orient the 30 genes and fit the scaler/coefficients (`09_external_validation.py:73,94`). The only information shared with the test set is the gene set + orientation, which is standard, and the external AUC is computed solely on E-MTAB labels. No patient overlap is possible between MARS (GSE65682) and Davenport (E-MTAB-4451). I verified n = 106, deaths = 52, prevalence 0.4906 by recompute.

2. **Calibration slope 0.50 = over-confident is correctly framed.** Recompute from `09_ext_risk_scores.csv`: intercept −0.0382, slope 0.5028, P = 0.0157 vs ideal 1 (`09_ext_calibration_dca.csv`), matching the manuscript's "slope 0.50 / intercept −0.04." The manuscript correctly reads this as over-confident and explicitly presents the score as a ranker, not a calibrated probability (`manuscript.md:107`).

3. **No residual feature/label resampling mismatch in the current code.** I checked every fit/predict/bootstrap site: `09_external_validation.py:124-132` bootstrap indexes `y_e[idx]` and `risk[idx]` together (aligned); `run_tier1.py:243-248` and `probe_s06.py:29-31` split `Xsig_s`/`y` (or `Xs`/`y`) jointly; the L1000 streaming (`S08_l1000_connectivity.py:75-86`) maps samples→perturbagen via `col2pert` with no resampling. The historical bootstrap-index bug is not present in the shipped scripts.

4. **The optimistic within-cohort CV and the single-direction LINCS metric are disclosed, not hidden.** Limitation 9 ("selection-chain FWER not controlled"; within-cohort CV optimistic) and Limitation 10 ("LINCS single-direction") plus the glucocorticoid caveat (`manuscript.md:137`) are explicit. The incremental-value claim over the existing SRS endotype is honestly reported as non-significant (ΔAUC +0.028, permutation P = 0.69; `09_ext_benchmark_vs_srs.csv`, `manuscript.md:157`).

5. **DEG calling uses BH FDR.** `run_tier1.py:79` applies `multipletests(method="fdr_bh")`; the manuscript reports "|logFC|≥0.3 & FDR<0.05" consistently (`manuscript.md:34,189`).

---

## § Questions for the authors

1. The panel orientation mentioned a "second external cohort AUC 0.659 (n = 52)." I found no second cohort in the manuscript — 0.659 is the *internal* GSE65682 CV AUC and n = 52 is the death count in E-MTAB-4451, not a sample size. Is there in fact a second independent cohort (n ≈ 52), or was 0.659/0.659 a mislabel of the internal CV? Please confirm the only external cohort is E-MTAB-4451 (n = 106).
2. For D1/D2: was the equal-weight fixed-orientation score pre-specified *before* reading E-MTAB-4451 outcomes, or chosen because it gave the higher AUC? If the latter, will you switch the primary external metric to the locked L1 (0.585)?
3. For D4: is an IFN-γ or GM-CSF `trt_cp` signature present anywhere in GSE92742, and if so, what is its rescue rank? This determines whether a correctly-directed positive control can be added at all.
4. For D7: were the 7–8 marker genes per cell type chosen a-priori, and do any hub–celltype correlations survive an FDR correction across the cell-type panel?

---

## § What I actually checked

**Scripts read (implementation vs text):**
- `02_scripts/python/run_tier1.py` (full) — S06 signature build (`run_tier1.py:212-261`): 30 genes = top-30 |pearsonr(gene, death)| over a hand-picked `BROAD_IMMUNE` list, selected on full-cohort `ysig` *before* the `StratifiedKFold` at `:243`; EPV 114/30 = 3.8. S05 hub ML consensus (`:174-210`). S01 limma + BH (`:79`).
- `02_scripts/python/09_external_validation.py` (full) — lock (`lr.fit` on GSE65682, `:97`), orientation fixed from training labels (`:73`), external apply (`:114-122`), bootstrap CI (`:124-143`, indices aligned). Confirmed no feature/label mismatch.
- `02_scripts/python/_ext_calibration_dca.py` (full) — calibration logistic fit on z-standardized oriented-sum; DCA thresholds 0.05–0.95; grid dump.
- `02_scripts/python/S08_l1000_connectivity.py` (full) — `rescue = mean rank-percentile − 0.5` over 22 same-signed genes (`:91-93`); single-direction; background ~53.6% positive.
- `02_scripts/python/S08_l1000_postprocess.py` (full) — positive-control table assembly; prednisone/dexamethasone/entinostat/lenalidomide/vorinostat/azithromycin ranks.
- `02_scripts/08_virtual_ko_cmap.R`, `02_scripts/python/08_virtual_ko_cmap.py` (full) — mechanism-anchored candidate map (not L1000 connectivity); `08_positive_control_check.csv` is the *mechanism* gate, distinct from the L1000 positive control.
- `02_scripts/python/probe_s06.py` (full) — CV alignment correct (`:29-31`).
- `02_scripts/06_prognosis.R` — confirmed it is a stub (hub 5-gene z-sum, `auc_val = NA`); the 30-gene signature is built in `run_tier1.py`, not here.

**Values recomputed (command: `python` reading `03_results/09_ext_risk_scores.csv`):**
- AUC(risk_oriented_sum) = 0.6382; AUC(risk_locked_l1) = 0.5848; AUC(risk_irg3) = 0.5288 — reproduce `09_external_validation.csv` (0.6382 / 0.5848 / IRG3 0.5288).
- Calibration intercept = −0.0382, slope = 0.5028, P = 0.0157 — reproduces `09_ext_calibration_dca.csv` (slope 0.5028, intercept −0.0382).
- Oriented-sum bootstrap CI95 = 0.5326–0.7394 (script reports 0.5317–0.7475; same to rounding/rng).
- n = 106, deaths = 52, prevalence = 0.4906 — matches `09_external_validation.csv`.

**Discrepancies found:** none between the manuscript's stated numbers and the CSVs I recomputed. The only mismatch is the panel orientation's "second cohort 0.659 (n=52)," which I trace to the internal CV (0.659) and the external death count (52), not a second cohort (see Questions).

**Secondary checks (read, not recomputed):** `S08_l1000_positive_control.csv` (ranks above); `07_hub_celltype.csv` (correlations above); `S06_hub_death_association.csv` (uncorrected p-values + MR residue); `08_candidates_drugs.csv` (rescue_fraction ≤ 0.8, binomial P ≥ 0.82 — consistent with the manuscript's "no candidate beats the immune background" point); `S06_auc_compare.csv` (CV 0.6586, train 0.7495, IRG baselines 0.619/0.648); `09_ext_benchmark_vs_srs.csv` (SRS dir-corrected AUC 0.6104, locked 0.6382, Δ +0.0278, perm P 0.694 — matches `manuscript.md:157`).
