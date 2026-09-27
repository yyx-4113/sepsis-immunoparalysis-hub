# A4 — Venue & Reporting-Standard Auditor Report

**Reviewer role:** Journal editor + reporting-checklist auditor (STROBE-MR / Vancouver / format)
**Manuscript:** "Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning"
**Version reviewed:** git tag v1.9.0 (treated as a fresh first submission; no prior-round material consulted)
**Independence note:** I judged solely from `manuscript.md`, `cover_letter.md`, and `03_results/12_strobe_mr_checklist.csv`. I did not read any `REVIEW_round*.md`, `RESPONSE*.md`, `REVISION*.md`, `review_r1/`–`review_r9/`, manifest, SOP, or other reviewers' files.

---

## 〇、Bottom-line venue recommendation (decisive)

**Reframe from a Research Article (discovery framing) to a Computational Biology / Methods & Resources (or Application Note) article.** The genuine, durable contribution is *not* novel biology — the manuscript's own Discussion states the five hubs "largely recapitulate … the Mars1 endotype in the original MARS-consortium work … this is a near-replication rather than a novel gene discovery" (`manuscript.md:194`) — and the MR layer is null on the primary outcome (no primary IVW significant; the only family-significant result reverses direction: `manuscript.md:159`, `:186`). The real value is a **fully-auditable, endotype-anchored multi-omics pipeline**, an **honest external cross-platform validation** of a 30-gene signature, an **explicit experimental blueprint (S11)**, and **exemplary reporting transparency** (digital provenance table §7, STROBE-MR checklist, tiered evidence hierarchy). These are the hallmarks of a Methods/Resources article, not a discovery Research Article.

If the target venue has no Methods/Resources track, the fallback is a **headline-swap within the Research type** (recommendation 3 below). I give concrete specs for both.

---

## 一、Primary task: the ARTICLE-TYPE question (judged independently)

### 1) Is the current Research-article / discovery framing honestly supported?

- **【Problem】** The title and discovery framing ("multi-omics dissection", "hub genes") assert novel biology that the manuscript's own text retracts as a near-replication, and the causal layer it advertises is null.
- **【Evidence】** Title `manuscript.md:1`; Discussion `manuscript.md:194` ("near-replication rather than a novel gene discovery"); MR Results §3.10 `manuscript.md:159` ("no primary IVW estimate reached significance"), `:186` (only 1/45 family-corrected tests significant and it reverses direction); Limitations 2 `manuscript.md:205` ("no primary IVW estimate reached significance").
- **【Why it matters】** A discovery-framed Research Article whose headline claim is internally contradicted by its own Discussion creates a mismatch between contribution and category. Editors/referees will read the discovery title, then find confirmation + null MR, and judge it as over-claimed. This is the single largest acceptance risk and is fully within the author's control to fix.
- **【Specific fix】** Adopt the reframing in §2 below. At minimum, change the title to remove "dissection"/discovery connotations and lead with "confirmation / external validation / open pipeline." See paste-ready title options in §2.

### 2) Should it be reframed as a Computational Biology / Methods & Resources article? — YES.

- **【Problem】** The dominant intellectual product is a reproducible, source-traceable analytical workflow plus an honest validation, not a new biological finding; the current article type miscategorizes that product.
- **【Evidence】** §7 数字溯源表 (`manuscript.md:230–258`) maps every number to a deposited file; §2.10 pre-specifies MR (`manuscript.md:70`); §2.11 S11 experimental blueprint (`manuscript.md:74–75`); Discussion `manuscript.md:194` self-declares near-replication; external validation AUC 0.638 is "comparable to, not better than" the IRG benchmark (`manuscript.md:122`, `:192`). Code released under MIT (`manuscript.md:263`).
- **【Why it matters】** Methods/Resources and Application-Note article types (e.g., *Bioinformatics* Application Note, *PLOS Computational Biology* "Methods", *BMC Bioinformatics* Methodology) are evaluated on pipeline rigor, reusability, validation honesty, and reporting quality — exactly where this manuscript is strong. Recategorized, its candid self-limiting caveats become a *strength* (exemplary transparency) rather than a *weakness* (failed discovery).
- **【Specific fix】** Concrete reframing spec:

  **New title (Methods/Resources):** "An endotype-anchored, fully-auditable multi-omics pipeline confirms the sepsis MARS Mars1 immunoparalysis program and externally validates a 30-gene prognostic signature: a computational biology study with an experimental blueprint"

  **Alternative shorter title:** "Replicating and externally validating the sepsis Mars1 immunoparalysis signature: an endotype-anchored multi-omics pipeline and reproducible workflow"

  **Abstract skeleton (structured, ~250 words), paste-ready:**
  - **Background.** The Mars1 immunosuppressed endotype of sepsis is a well-established biology (Scicluna/Davenport). What remains valuable is a reproducible, auditable pipeline that *confirms* the program and provides an honestly validated prognostic signature plus a clear path to experimentation.
  - **Methods.** We built an endotype-anchored multi-omics pipeline on GSE65682 (802 samples): moderated-t moderated DE, immune-function score, co-expression degree-centrality + tri-method ML consensus, a 30-gene signature (5-fold CV), **locked** external validation on E-MTAB-4451, mechanism-anchored repositioning, and a **pre-specified** two-sample MR (eQTLGen × UK Biobank). Every reported number traces to a deposited CSV (§7).
  - **Results.** We *confirm* (not discover) that Mars1 is anchored by antigen-presentation/monocytic hubs (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) plus a non-immune co-expression passenger (FIS1, up-regulated, reported as a marker). The signature reached CV AUC 0.659 (optimistic, label-informed) and **external** AUC 0.638 (95% CI 0.532–0.748), **comparable to, not superior to** the published IRG benchmark. MR was null on the primary 28-day-death outcome (no IVW significant; the sole family-significant result reverses direction and rests on 3 instruments + uncorrected sample overlap) → hypothesis-generating. Repositioning shortlist is mechanism-anchored and hypothesis-generating.
  - **Conclusions.** The contribution is the **pipeline, the honest external validation, and the experimental blueprint (S11)** — not novel hub-gene biology. We release a reusable, fully-traceable workflow for endotype-anchored sepsis immunoparalysis analysis.

  **Section-structure change (emphasis moves to method + validation + blueprint):**
  1. Intro → "Why a reproducible confirmation/validation pipeline matters" (cite MARS as established).
  2. **Methods (elevate to §2, already strong)** → rename "Implementation / Pipeline."
  3. Results → "Reproducible results (source-traced)" — keep but lead each sub-result with *what was confirmed* vs *what is new*.
  4. Add a prominent **"Reproducibility & provenance"** subsection drawing from §7.
  5. Discussion → "What this pipeline adds" + "Honest boundaries" (near-replication; null MR).
  6. Elevate **S11 Experimental blueprint** to a main-section or co-equal "Translation blueprint" section.
  7. Keep Limitations, Data availability, STROBE-MR checklist as core (these are theMethods/Resources selling points).

### 3) Or is a headline-swap within the Research type sufficient?

- **【Problem】** If the venue only accepts Research Articles, the discovery title/abstract must be swapped to a confirmation/validation/replication framing without changing the article type.
- **【Evidence】** Same as §1–§2. The biology is confirmatory (`manuscript.md:194`); the signature validation is real but modest and non-superior (`manuscript.md:122`).
- **【Why it matters】** A within-type headline-swap preserves the Research-Article slot while removing the over-claim. It is the *minimum* acceptable fix; the Methods/Resources reframing (§2) is preferred because it better matches the actual contribution.
- **【Specific fix】** If staying as Research Article: (a) title → "Confirmation and external validation of the MARS Mars1 immunoparalysis program in sepsis: an endotype-anchored multi-omics analysis and in-silico repositioning blueprint"; (b) abstract Background/Conclusions must state "confirm/replicate" and "null MR / hypothesis-generating" in the lead sentences, not buried; (c) Keywords keep "bioinformatic" but add "replication" / "external validation". Do **not** keep "dissection" as a discovery verb.

**Decision:** Recommendation **2 (reframe to Methods/Resources)** is primary; **3 (headline-swap)** is the acceptable fallback. Both are decisively better than the current framing.

---

## 二、Secondary task: STROBE-MR checklist

- **【Problem】** The checklist covers STROBE-MR items 9a/9b/10/11–17, but item **10_counts** is only "PARTIAL" (intermediate variant counts not tabulated) and two 9a sub-items (directionality, which-variable) are "PARTIAL" because Steiger was not run — none of these gaps are surfaced in the manuscript's Limitations section.
- **【Evidence】** `12_strobe_mr_checklist.csv`: rows `10_counts` (status PARTIAL, "Final retained counts given; identified/post-clump intermediate counts reproducible from deposited script (not tabulated in text)"), `9a_directionality` (PARTIAL, "Not performed"), `9a_which_var` (PARTIAL). Manuscript §2.10 `manuscript.md:72` discloses non-performance of Steiger and non-correction of sample overlap; FCGR3A exclusion stated `manuscript.md:71`, `:157`; 27 retained instruments (3+4+6+6+8=27) consistent with Table 3 `manuscript.md:165–170`.
- **【Why it matters】** STROBE-MR compliance is only as good as its visibility to the reader. A PARTIAL item that is silently "reproducible from script" still leaves the *manuscript* non-compliant at the point of reading; editors using the checklist as a gate will flag this. The math (27 instruments) and FCGR3A exclusion and sample-overlap non-correction ARE honestly disclosed in the body — good — but the omitted Steiger and untabulated intermediate counts should be explicitly named as limitations, not only buried in a supplementary CSV.
- **【Specific fix】**
  - Add to Limitations a line: "We did not perform a Steiger directionality test (STROBE-MR 9a), so reverse-causation between cis-eQTL baseline whole-blood expression and acute sepsis outcome is not formally excluded; and we tabulated only final retained instrument counts, with per-SNP drop-lists reproducible from the deposited TwoSampleMR script (STROBE-MR 10_counts)."
  - Optionally add a one-line summary table of variant flow per gene: identified → post-clump → harmonised-retained (even if sourced from the script) to lift `10_counts` from PARTIAL to Present.

---

## 三、Abstract vs body consistency

- **【Problem】** The English abstract uses discovery-leaning verbs ("isolated hub genes", "evaluated") and does **not** state the near-replication nature in its lead, slightly over-claiming relative to the body; it *does* honestly convey the all-null MR and the reversed family-significant result.
- **【Evidence】** Abstract `manuscript.md:13` ("…consensus … isolated hub genes"); `manuscript.md:14` ("Two-sample MR did not support a causal effect of any hub gene … the only family-significant result, the CD74 critical-care weighted median, reversed the Mars1 direction") — this MR sentence is honest and good. But the abstract never says "confirm/replicate"; the "near-replication" caveat appears only in Discussion `manuscript.md:194`. Conclusions `manuscript.md:15` do say "the MR layer is null and hypothesis-generating" — acceptable.
- **【Why it matters】** Readers (and editors skimming the abstract) will take "isolated hub genes … multi-omics dissection" as a novelty claim that the body contradicts. The abstract is ~80% honest but the missing "confirmation" framing is the same discovery-overclaim as the title.
- **【Specific fix】** In the abstract Methods/Results, replace "isolated hub genes" with "recapitulated/confirmed five immune hubs" and add one clause: "consistent with a near-replication of the original MARS Mars1 program rather than novel gene discovery." Keep the existing honest MR sentence verbatim.

---

## 四、Cover letter vs manuscript

- **【Problem】** The cover letter is commendably honest about non-claims, but it **mislabels FIS1 as a "hub gene"** whereas the manuscript carefully distinguishes FIS1 as a non-immune co-expression *passenger/marker*, not a hub.
- **【Evidence】** Cover letter `cover_letter.md:12`: "(CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1)" listed among "hub genes." Manuscript `manuscript.md:116` ("FIS1 … reported as a co-expression passenger / marker, not a mechanistic target"), `:226` ("a sixth co-expression-linked gene, FIS1 … reported as a co-expression passenger rather than an immune hub"), §7 `manuscript.md:240` ("5 免疫 hub + FIS1 乘客").
- **【Why it matters】** A cover-letter/manuscript terminology mismatch is a small but real inconsistency editors notice; it undercuts the manuscript's otherwise careful FIS1 boundary. The cover letter's "What the study does NOT claim" section (`cover_letter.md:14–18`) is exemplary and does **not** contradict the manuscript's caveats — good.
- **【Specific fix】** In `cover_letter.md:12`, change "(CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, FIS1)" to "(CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) plus a non-immune co-expression passenger, FIS1," matching the manuscript's terminology.

---

## 五、Format hard-fails for a typical bioinformatics journal

The manuscript **passes** the standard structural requirements; I verified each:

- **Dataset accession verification — PASS.** GPL13667 verified at file level `manuscript.md:43`; E-MTAB-4451 (ArrayExpress, GPL10558) `manuscript.md:67`; LINCS GSE92742 `manuscript.md:253`; GEO/ArrayExpress cited.
- **Conflict of interest — PASS.** `manuscript.md:274–275` ("declares no conflict of interest").
- **Data availability — PASS (minor caveat).** `manuscript.md:261–263` gives repo, Zenodo DOI-upon-acceptance, GEO/ArrayExpress sources. *Caveat:* "will be made public upon acceptance" may not satisfy journals requiring immediate availability (e.g., PLOS/BMC want a live private repo+token at submission). Recommend depositing a private Zenodo/figshare DOI now and citing it.
- **Ethics / Author contributions / Funding — PASS.** `manuscript.md:265–272`.
- **Figure legends — WEAK (not a hard fail, but should be fixed).** Figures are referenced inline as one-line captions (e.g., `*Fig. S01. ROC of 28-day mortality by the Mars1 binary indicator (AUC 0.578, discovery cohort).*` `manuscript.md:111`) with a source-file path but no consolidated "Figure Legends" section and minimal method/statistic description. For a Methods/Resources article this is acceptable; for a Research Article some editors require full legends. **Fix:** add a consolidated "Figure/Table Legends" appendix with purpose, data source, statistical method, and n for each S01–S12.
- **Supplementary listing — WEAK.** S01–S12 are enumerated in §7 but there is no single "Supplementary Materials" index with filenames+legends. **Fix:** add a short Supplementary index table.

No format *hard-fail* (rejection-level) was found; the above are polish items, except the data-availability "upon acceptance" caveat which some journals treat as a submission requirement.

---

## 六、Vancouver references (spot-check)

I spot-checked refs 2, 3, 5, 16, 32, 34, 35 (including the four the audit may have fixed: 2, 3, 34, 35) plus format.

- **【Problem】** References are internally consistent (all in-text citations 1–35 resolve; list is complete) and the four audited refs (2, 3, 34, 35) are correct. The main deviation is **full journal names instead of NLM-abbreviated titles**, which is the standard Vancouver expectation.
- **【Evidence】**
  - Ref 2 `manuscript.md:280` Boomer JS … JAMA. 2011;306(23):2594-2603 — correct, real paper. ✓
  - Ref 3 `manuscript.md:281` Singer M … Sepsis-3, JAMA 2016;315(8):801-810 — correct. ✓
  - Ref 34 `manuscript.md:312` Hotchkiss RS … nivolumab sepsis Phase 1b, Intensive Care Medicine 2019;45(10):1360-1371, doi:10.1007/s00134-019-05704-z — correct, real paper. ✓
  - Ref 35 `manuscript.md:313` Joshi I … mHLA-DR utility, Frontiers in Immunology 2023;14:1130214 — plausible/correct. ✓
  - Ref 5 `manuscript.md:283` Davenport … Lancet Respir Med 2016;4(4):259-271 — correct. ✓
  - Ref 16 `manuscript.md:294` Peng Y … Frontiers in Immunology 2023;14:1152117 (IRG benchmark) — plausible. ✓
  - Ref 32 `manuscript.md:310` Giamarellos-Bourboulis … ImmunoSep RCT, JAMA online Dec 8 2025, doi:10.1001/jama.2025.24175 — format with "et al; ImmunoSep Study Group" acceptable. ✓
- **【Why it matters】** Full journal titles (e.g., "The Lancet Respiratory Medicine", "Intensive Care Medicine", "Frontiers in Immunology") deviate from Vancouver/NLM abbreviation convention; many target journals will request reformatting during copy-edit, causing avoidable rework. No factual errors found in the sampled set.
- **【Specific fix】** Abbreviate journal names to NLM style: *Lancet Respir Med.*, *Intensive Care Med.*, *Front Immunol.*, *JAMA*, *Nat Med.*, *Nat Genet.*, *Nat Biotechnol.*, *Genome Biol.*, *Nucleic Acids Res.*, *BMC Bioinformatics*, *Cell Host Microbe*, *Cell*, *eLife*, *Sci Rep.* (if used), *Crit Care*, *Am J Respir Crit Care Med.*, etc. Verify every DOI resolves (spot-checked ones do). Also confirm ref 21 (Bowden 2016, I²/MR-Egger) is actually cited where I² heterogeneity is discussed in §3.10 — if not, add the citation at `manuscript.md:159`.

---

## § Stands up (strengths — keep these)

1. **Exemplary digital provenance (§7).** Every reported number traces to a deposited CSV (`manuscript.md:230–258`). This is rare and is the strongest argument for a Methods/Resources framing.
2. **Honest, tiered evidence hierarchy.** Tier-1 biology-inevitable → Tier-2 method-positive gate → Tier-3 non-binding MR (`manuscript.md:36`); MR consistently presented as hypothesis-generating (`manuscript.md:186`, `:205`).
3. **Pre-specified, family-corrected MR.** 45-test Benjamini–Hochberg (`manuscript.md:159`, `10_mr_bh_family.csv`), with the reversed-direction result explicitly demoted (`manuscript.md:172`, `:184`) — methodologically disciplined.
4. **Genuinely honest external validation.** Locked signature, cross-platform, n=106, AUC 0.638 with 95% CI, explicitly "comparable not superior" (`manuscript.md:122`) — avoids the usual inflated within-cohort AUC claim.
5. **Complete reporting blocks.** Conflict of interest, data availability, ethics, author contributions, funding, and STROBE-MR checklist are all present and mostly complete.

---

## § Questions for the authors

1. Given exposure–outcome sample overlap (eQTLGen ⊃ UK Biobank) biases SEs *downward* (inflating Type-I risk) and you applied **no** overlap correction (`manuscript.md:70`), is the "hypothesis-generating" reading itself over-generous for the CD14 MR-Egger (family q=0.73) and the reversed CD74 critical-care signal? Should the MR layer be presented even more conservatively?
2. Why was the **Steiger** directionality test (STROBE-MR 9a) omitted when it is cheap to run and would address reverse-causation between baseline cis-eQTL and acute sepsis? Will you add it, or explicitly list it as a limitation (recommendation §二)?
3. Can you tabulate the **per-gene variant flow** (identified → post-clump → harmonised-retained) to lift STROBE-MR `10_counts` from PARTIAL to Present (recommendation §二)?
4. The abstract/title discovery framing contradicts your own "near-replication" Discussion — do you accept the Methods/Resources reframing (recommendation §2) or at minimum the headline-swap (recommendation §3)?
5. Will you deposit a **live (private) data/code DOI now** rather than "upon acceptance" to satisfy immediate-availability policies (recommendation §五)?
6. Please reconcile the **FIS1 "hub" (cover letter) vs "passenger" (manuscript)** terminology (recommendation §四).

---

## § What I actually checked

- Read `manuscript.md` in full (all 314 lines, including truncated §2.10, §3.4, §3.8, §3.9, §3.10, §4, §5).
- Read `cover_letter.md` in full.
- Read `03_results/12_strobe_mr_checklist.csv` in full and cross-checked every item (9a×6, 9b, 10×4, 11, 12×3, 13, 14, 15, 16, 17) against the manuscript body and tables.
- Verified the 27-instrument arithmetic (3+4+6+6+8) against Table 3 (`manuscript.md:165–170`).
- Verified no prior-round/forbidden files were opened (independence maintained).
- Spot-checked 7 references (2, 3, 5, 16, 32, 34, 35) for correctness/format and assessed Vancouver journal-abbreviation convention.
- Verified presence/completeness of: dataset accession verification, conflict of interest, data availability, ethics, author contributions, funding, figure references, §7 provenance.
- Confirmed the FIS1 hub/passenger terminology mismatch between cover letter and manuscript via targeted grep.

**Final verdict:** The science is competently executed and commendably honest in its caveats, but it is **mis-categorized as a discovery Research Article**. Reframe to **Computational Biology / Methods & Resources** (preferred) or perform a decisive **headline-swap within Research** (fallback). With that reframing plus the minor STROBE-MR/reference/terminology fixes above, this is a solid, publishable Methods/Resources contribution.
