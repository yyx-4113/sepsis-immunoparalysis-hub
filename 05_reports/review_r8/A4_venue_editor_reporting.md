# A4 — Venue / Editor & Reporting-Compliance Review

**Role:** Independent peer reviewer (journal editor + reporting-standards audit)
**Manuscript:** "Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning" (single-author bioinformatics)
**Review basis:** First-submission review. Files read: `05_reports/manuscript.md` (full), `03_results/10_mr_bh_family.csv` (full), `03_results/10_genetics_mr_outcome5086_harmonised.csv` and `10_genetics_mr_harmonised.csv` (for `nsnp`/F audit). No prior reviews, response letters, or revision history consulted.

---

## Issues (four-part contract: 问题 / 证据 / 为何重要 / 具体修改)

### Issue 1 — STROBE-MR item 9b/10: variant-selection flow not reported
**【问题】** The MR instrument disclosure gives only the *final* retained count (27) and the per-gene breakdown, but never reports how many SNPs were identified at *P*<5×10⁻⁸ before LD clumping, how many were removed by clumping (r²<0.01), and how many dropped during harmonisation. STROBE-MR (Skrivankova et al., BMJ 2021) item 9b/10 expects a transparent variant-selection flow (identified → post-clump → post-harmonisation → analysed).
**【证据】** `manuscript.md:72` — "Across the six hub genes, 27 instruments were retained after harmonisation (CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8; FCGR3A excluded …)". No pre-clump or per-stage-drop counts appear anywhere in §2.10 or §3.10.
**【为何重要】** Without the flow, a reader cannot judge how aggressively instruments were filtered or whether the final set is robust to clumping/harmonisation choices — a common source of MR inflation. It is a checklist gap that most MR-methodology reviewers will flag.
**【具体修改】** Add a compact per-gene variant-selection table (or a STROBE-MR-style flow) to §2.10 / Supplementary S10, with columns: `n_identified_P5e-8`, `n_after_LDclump`, `n_after_harmonisation`, `n_analysed`. Example spec:
> For each exposure we report the number of cis-eQTL hits at *P*<5×10⁻⁸, the number surviving LD clumping (r²<0.01, kb window 10 000), and the number retained after allele harmonisation (palindromic/strand-ambiguous SNPs dropped). CD74: x→y→3; HLA-DQA1: x→y→4; CD14: x→y→6; HAVCR2: x→y→6; FIS1: x→y→8; FCGR3A: x→y→2 (excluded, <3).

### Issue 2 — STROBE-MR item 9a: Steiger directionality test not reported
**【问题】** No Steiger (or equivalent) directionality test is described or reported, so it is not demonstrated that the instruments relate to the *exposure* (gene expression) rather than to the *outcome* (sepsis) — a core MR assumption.
**【证据】** `manuscript.md:70-72` — methods describe exposure (eQTLGen cis-eQTL), outcomes, clumping, harmonisation, IVW/Egger/weighted-median, Cochran Q/I², per-SNP F; no mention of a directionality/Steiger test or "which variable the instrument is more strongly associated with."
**【为何重要】** For cis-eQTL exposures proximity usually protects against reverse causation, but STROBE-MR item 9a explicitly asks that the directionality assumption be addressed. Its absence is a checkable omission.
**【具体修改】** Either (a) add a sentence confirming a Steiger filtering test was run and passed for all 27 instruments (instruments significantly more associated with expression than with outcome), or (b) state explicitly that, because exposures are *cis*-eQTLs within ±100 kb of the target gene, reverse causation is implausible and Steiger filtering was therefore not required. Keep the wording factual:
> "Steiger directionality filtering was applied (all 27 instruments were significantly more associated with the cis-gene expression trait than with any sepsis outcome, P_Steiger<0.05), supporting the exposure→outcome orientation."

### Issue 3 — STROBE-MR item 9a: no power / minimum-detectable-effect statement
**【问题】** The manuscript never states the statistical power of the MR layer or the minimum OR detectable at the achieved instrument strength (27 SNPs; 1,896–11,643 cases).
**【证据】** `manuscript.md:70` (outcome Ns) and `manuscript.md:157-184` (results) discuss "underpowered" qualitatively but give no quantitative power/min-detectable-OR.
**【为何重要】** STROBE-MR item 9a calls for a statement on power; "underpowered" is an assertion that should be backed by the detectable effect size given the F-statistics and case counts, otherwise the null result is hard to interpret.
**【具体修改】** Add a short power note in §2.10 or §3.10, e.g.:
> "With the retained instruments (median F 35–168) and 1,896 28-day-death cases, the MR had ~80% power to detect an IVW OR of ≈1.25 per SD of predicted expression at α=0.05; smaller effects would be undetectable, so the primary-outcome null is consistent with effects below this floor rather than with no effect."

### Issue 4 — STROBE-MR item 9a: weak-instrument exclusion threshold not explicit
**【问题】** §2.10 says instrument strength was assessed "by the per-SNP *F* statistic" but never states a numeric weak-instrument cut-off (e.g., F>10) used to drop SNPs.
**【证据】** `manuscript.md:72` — "Heterogeneity was assessed by Cochran Q and I² …, and instrument strength by the per-SNP *F* statistic. A minimum of three instruments was required for a gene to be assessed." No F>10 rule stated. (I verified from the harmonised CSVs that all 27 retained SNPs have F 30.7–2789.5, so none would have been excluded — but the rule must be declared.)
**【为何重要】** Declaring the threshold is a STROBE-MR 9a requirement; silent omission reads as incomplete methods even when the data are clean.
**【具体修改】** Add: "SNPs with per-SNP F<10 were treated as weak instruments and excluded; none of the 27 retained SNPs fell below this threshold (range F=30.7–2789.5)."

### Issue 5 — Internal clarity: dual correction framing in §2.10 is ambiguous
**【问题】** §2.10 first says BH FDR "was applied within each outcome across the 15 gene×estimator tests (the `p_fdr_bh` column …)" and then says "the pre-specified primary correction, however, was the full family of 45 tests." The ordering ("applied … however pre-specified primary") can be read as contradictory (which was the registered primary?).
**【证据】** `manuscript.md:72` — "Benjamini–Hochberg FDR was applied within each outcome across the 15 gene×estimator tests (the `p_fdr_bh` column of each MR CSV); the pre-specified primary correction, however, was the full family of 45 tests …"
**【为何重要】** Ambiguity about which correction was pre-specified vs. reported-for-completeness can be read as post-hoc flexibility in multiplicity control — exactly what a registered MR design should avoid.
**【具体修改】** Restate clearly:
> "The pre-specified primary multiplicity control was the full 45-test family BH (5 assessable genes × 3 estimators × 3 outcomes; FCGR3A excluded). For completeness we also report a narrower per-outcome 15-test BH (`p_fdr_bh`) in each MR CSV, but all primary inferences use the 45-test family q."

### Issue 6 — Wording: "intervention targets" slightly exceeds repositioning evidence (borderline)
**【问题】** Abstract, Discussion and Conclusion all state the hubs "identify candidate, expression-level intervention targets (direct-target validation still pending)." The repositioning evidence is mechanism-anchored *response-gene concordance* (not direct-target overlap) plus LINCS connectivity for only 2/7 candidates, and the glucocorticoid positive-control caveat shows a positive rescue score is not sufficient for functional restoration. Calling them "targets" — even hedged — marginally over-reaches the data.
**【证据】** `manuscript.md:15` (Abstract Conclusions), `manuscript.md:190` (Discussion), `manuscript.md:218` (Conclusion) — "… identify candidate, expression-level intervention targets (direct-target validation still pending)." Contrast with `manuscript.md:209` (Limitation 9: "Drug-repositioning metric is a curated response-gene concordance, not direct-target overlap … Unbiased connectivity evidence covers only 2/7 candidates") and `manuscript.md:150` (glucocorticoid caveat).
**【为何重要】** This is the one place where headline and caveat strength are not perfectly matched; an editor scanning the Conclusion may read "intervention targets" as stronger than the repositioning layer supports. The hedge is present, but the noun "targets" carries more weight than "candidates/hypotheses."
**【具体修改】** Soften the noun while keeping the hedge:
> "… and nominate *candidate, expression-level intervention hypotheses* (direct-target validation still pending)."
Apply the same substitution in §4 (line 190) and §6 (line 218). The Abstract already pairs it with "direct-target validation still pending," which is good; the noun change removes the residual overclaim.

### Issue 7 — References: two formatting inconsistencies (Vancouver)
**【问题】** (a) Reference 21 is missing its journal volume; (b) Reference 32 lists a single author + "et al." and omits volume/issue/pages, inconsistent with the rest of the list (which gives 3–7 authors and full pagination).
**【证据】** `manuscript.md:290` — "21. Bowden J, Del Greco M. F, … International Journal of Epidemiology. 2016;:dyw220. doi:10.1093/ije/dyw220" (no volume before the colon). `manuscript.md:301` — "32. Giamarellos-Bourboulis EJ, et al. Randomized trial of interferon-γ … JAMA. 2025. doi:10.1001/jama.2025.24175" (single author + et al.; no vol/issue/pages).
**【为何重要】** Vancouver uniformity is a copy-editing gate at most journals; the missing volume (ref 21) is a factual gap that can block proofing, and ref 32's single-author "et al." diverges from the house style used elsewhere.
**【具体修改】** (a) Ref 21 → "Int J Epidemiol. 2016;45(6):dyw220." (b) Ref 32 → list first 6 authors then "et al." and add volume/issue/pages if available, e.g. "JAMA. 2025;333(1):xx–xx." or, if not yet in an issue, keep the advance-access DOI but list ≥6 authors.

### Issue 8 — Abstract: word count / structured-format fit for target journal
**【问题】** The English structured abstract is long (Background/Methods/Results/Conclusions, ≈500–600 words) and embeds many numbers (23/25, AUC 0.659/0.638, OR ranges, 45-test family, etc.).
**【证据】** `manuscript.md:12-15` — full structured abstract.
**【为何重要】** Many bioinformatics/methods journals cap structured abstracts at 250–350 words (e.g., BMC series 350; PLOS 300; Frontiers 200–250). An over-length abstract will force a revision regardless of scientific merit.
**【具体修改】** Before submission, confirm the target journal's abstract limit and trim: move the 23/25 immune-gene detail and the per-estimator OR ranges into the Methods/Results body, keep the abstract to the four top-line results (endotype-driven immunosuppression; 6 hubs; external AUC 0.638 comparable to benchmark; MR null on primary outcome with one reversed family-significant signal). Keep the honest hedging in Conclusions.

### Issue 9 — Ethics/Data-availability mapping to EM "research data" question
**【问题】** Data availability states "used and re-analyzed public research data" and Ethics states "purely computational re-analysis … no additional IRB approval required." This is correct for de-identified public re-analysis, and the S11 experimental blueprint is correctly separated as needing independent IRB.
**【证据】** `manuscript.md:254` (Data availability) and `manuscript.md:257` (Ethics).
**【为何重要】** For the Editorial Manager question "Did you use or generate research data?" the honest answer is **Yes (used)** / No (generated) — and the statement already supports it. But the Ethics paragraph could be strengthened by noting the *source* studies (GSE65682, E-MTAB-4451) obtained their own ethics approval/consent, which is the usual basis for the re-analysis exemption.
**【具体修改】** Add one clause to Ethics:
> "The source cohorts (GSE65682; E-MTAB-4451) were approved by their originating institutions with participant consent/de-identification; re-analysis of these public datasets therefore falls under standard exempt-reanalysis policy. The companion S11 experimental validation is a prospective design requiring independent IRB approval before any sample collection and was not executed here."

### Issue 10 — Article-type & "discovery" positioning (venue fit)
**【问题】** Given the evidence tier — Tier-1 biology is robust and expected, MR is essentially null on the phenotype-matched primary outcome (the only family-significant result reverses direction and rests on 3 instruments + sample overlap), external AUC 0.638 is *comparable to* (not better than) the published benchmark, and drug repositioning is mechanism-anchored concordance rather than direct-target validation — the manuscript should be positioned as a **computational reanalysis / bioinformatics methodology note**, not as a target-discovery paper.
**【证据】** `manuscript.md:154-184` (MR null/one-reversed), `manuscript.md:120` ("comparable to … not better than"), `manuscript.md:209` (repositioning = concordance, 2/7 connectivity).
**【为何重要】** Framing a re-analysis of canonical antigen-presentation genes (CD74, HLA-DQA1, CD14) as "novel target discovery" would over-promise and attract reviewer pushback; the current title already avoids "discovery" (uses "dissection" + "in-silico repositioning"), which is appropriate.
**【具体修改】** Recommended article type: **"Research Article"** at a bioinformatics/methods journal (e.g., BMC Bioinformatics, PLOS Computational Biology, Briefings in Bioinformatics, Frontiers in Genetics/Immunology — Methods) **or** an "Application/Brief Note" if the journal offers it. Explicitly avoid titles/abstracts containing "novel biomarker/target discovery." Keep the honest "reanalysis + hypothesis-generating repositioning" framing already present.

### Issue 11 — Supplementary-file completeness (figures & tables must be packaged)
**【问题】** The text cites many supplementary files (S01–S11 tables, multiple `04_figures/*.png`, harmonised CSVs). As reviewer I cannot confirm all are present in the submission package.
**【证据】** Citations include `S01_mars1_deg.csv`, `S02_immunoparalysis_score.csv`, `S03_*`, `S04`, `S05_hub_genes.csv`, `S06_*`, `07_axis_celltype.csv`, `08_candidates_drugs.csv`, `08b_clinical_translation.csv`, `S08_l1000_*`, `*_harmonised.csv`, `10_mr_bh_family.csv`, `04_figures/S02/S03/S06/S07/S09/S10/mr_forest/mr_diag`, and `11_validation_design.md`.
**【为何重要】** Missing any cited supplementary file is a mechanical desk-reject/return risk.
**【具体修改】** Provide a consolidated "Supplementary File Inventory" table at submission mapping every in-text citation (S01–S11, every figure, every CSV) to a deposited file, confirming none are orphaned.

---

## § 站得住的（holds up — ≥3）

1. **MR instrument counts are internally consistent and independently verified.** §2.10 states 27 retained (CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8; FCGR3A excluded). I counted the same from `10_genetics_mr_outcome5086_harmonised.csv` / `10_genetics_mr_harmonised.csv` (3+4+6+6+8 = 27; FCGR3A absent) and confirmed every retained SNP has F = 30.7–2789.5 (>10). Table 3 `n IV` (3/4/6/6/8) agrees. Strong.
2. **The 45-test family BH readout is real and matches the narrative.** `10_mr_bh_family.csv` contains exactly 45 rows (5 genes × 3 estimators × 3 outcomes). Only CD74 critical-care weighted median has `q_family_45test` ≈ 2.99×10⁻¹⁷ (YES), and the text correctly reports it reverses the Mars1 direction. No primary-outcome IVW is significant; CD14 28-day-death Egger `q` = 0.73. Fully consistent with §3.10/§5.
3. **Headline/caveat balance in the Abstract is honest.** Abstract Conclusions already carries "direct-target validation still pending" and "functional validation still required" (line 15), matching Limitations #6 (experimental blueprint only) and #7 (no docking). No residual overheat detected — grep for `druggable`, `addressable`, `we identify`, `therapeutic target` (author claim) returned only a *reference title* (ref 291). The v1.7.0 cleanup of "addressable axis" → "candidate, expression-level intervention targets" is confirmed complete.
4. **External validation is presented with honest magnitude.** AUC 0.638 (95% CI 0.532–0.748) is repeatedly framed as "comparable to, not better than" the IRG benchmark (0.604/0.619), and the optimistic within-cohort CV (0.659) is explicitly scoped as label-informed. This is exemplary calibration language.
5. **The glucocorticoid positive-control caveat is a genuine safeguard.** Prednisone/dexamethasone scoring high on the LINCS rescue metric while being immunosuppressive is used correctly to show a positive rescue score is necessary-but-not-sufficient — a strong, non-routine honesty check.
6. **Ethics/IRB separation of S11 is correct.** Public de-identified re-analysis exempt; prospective experimental validation correctly flagged as needing independent IRB.

---

## § 向作者提问

1. **Variant-selection flow:** What were the per-gene SNP counts *before* LD clumping and *after* clumping (i.e., the two intermediate stages) for each of the six hub genes? (Needed to satisfy STROBE-MR item 9b/10 — see Issue 1.) I only have the final 27.
2. **Steiger test:** Was a Steiger directionality test actually run? If yes, were all 27 instruments directionally valid? If no, is the cis-eQTL proximity argument the intended justification? (Issue 2.)
3. **Power:** Can you supply the minimum detectable OR (≈80% power) for the primary 28-day-death outcome given the retained instrument strengths? (Issue 3.)
4. **Deposition:** Are the `*_harmonised.csv` files (with per-SNP effect allele + beta + F for all 27) actually deposited in the versioned repo referenced in Data availability, or only present locally? I verified them locally but the reviewer cannot assume public availability.
5. **Target journal:** Which journal and article type are you targeting, and what is its abstract word limit? This determines whether Issue 8 (trim) and Issue 10 (positioning) need action before submission.
6. **IRB basis:** Do you rely on the originating cohorts' own ethics approvals for the re-analysis exemption, or did you obtain a specific exemption determination? (Informs the Issue 9 wording.)

---

## § 我实际核查了什么

**文件读取**
- `05_reports/manuscript.md` — 通读全文（行 1–302），重点 §2.10、§3.1/3.4/3.5/3.10、§4、§5、§6、§7、References、Data availability、Ethics。
- `03_results/10_mr_bh_family.csv` — 47 行（1 表头 + 45 数据行）。逐行核对：5 基因 × 3 估计量 × 3 结局 = 45 行；仅 CD74 critical-care weighted median 为 `q_family_45test` ≈ 2.99e-17（YES），方向反转；CD14 28-day-death Egger `q`=0.73；其余均为 no。与正文一致。
- `03_results/10_genetics_mr_outcome5086_harmonised.csv` 与 `10_genetics_mr_harmonised.csv` — 逐 SNP 计数：CD74 3（rs2305480/rs4810485/rs12478601）、HLA-DQA1 4（rs28383314/rs114293611/rs13203549/rs3819714）、CD14 6（rs57599368/rs149007767/rs148008812/rs6782228/rs424971/rs34856868）、HAVCR2 6（rs6891966/rs7911264/rs116560088/rs2617170/rs13401811/rs9266629）、FIS1 8（rs114756165/rs62482549/rs9399137/rs28361887/rs875741/rs6084653/rs7789679/rs9944715）= 27；FCGR3A 缺失。所有 F = 30.7–2789.5（>10）。与 §2.10 完全一致。两个 harmonised 文件的 eQTL 列相同，说明跨结局 harmonisation 一致。
- 确认 `01_data` 之外的相关 MR CSV 路径存在（glob 命中 7 个 `*mr*.csv`）。

**Grep 结果**
- 检索 `druggable|addressable|novel (target|biomarker|discovery)|we identify|therapeutic target|druggable axis|druggable target`（不区分大小写）：唯一命中为 `manuscript.md:291`（参考文献 van der Poll 标题 "potential therapeutic targets"），作者正文无未加 hedge 的 "druggable"/"addressable"/"we identify"。确认 v1.7.0 已将 "addressable axis" 清理为 "candidate, expression-level intervention targets"。
- 检索 `addressable|druggable|therapeutic target|therapeutic|discovery|candidate, expression-level|intervention target|direct-target validation`：命中行 15/70/117/120/190/201/210/218/291，均为已加 hedge 的 "candidate, expression-level intervention targets (direct-target validation still pending)" 或参考文献标题，无过热残留。

**数值一致性核对（已亲自验证）**
- Abstract MR："all IVW OR 0.92–1.12, P ≥ 0.23" ↔ Table 3 主结局 IVW：1.119/0.923/0.927/0.978/0.963（范围 0.92–1.12 ✓），P：0.72/0.26/0.24/0.85/0.47（均 ≥0.23 ✓）。
- Abstract："across the 45-test family only the CD74 critical-care weighted median survived correction, and it pointed opposite" ↔ §3.10 与 CSV 一致 ✓。
- 23/25、22/25、21 三处（Abstract、§3.1、§7）一致 ✓。
- 外部 AUC 0.638（CI 0.532–0.748）、CV AUC 0.659（训练 0.750）在 Abstract/§3.4/§3.5/§4/§5/§6/§7 完全一致 ✓。
- LINCS：lenalidomide 5435/20413 = 26.6% ✓；azithromycin 9152/20413 ≈ 44.8%（≈中位）✓；prednisone/dexamethasone 作为 caveat 呈现 ✓。
- 参考文献：除 ref 21（缺卷号）、ref 32（单作者 + et al. 且缺卷期页）外，编号引用 [n] 连贯、doi 完整。

**未核对（声明）**：未读取任何 REVIEW_*.md / RESPONSE_*.md / review_r7 / .workbuddy / SUBMISSION_MANIFEST / git 历史；未修改稿件、未执行 git。所有被核对数字均源于稿件正文与所提供的 CSV。
