# Independent peer-review — Venue / Reporting-standards audit
**Journal under review:** BMC Bioinformatics (Research article)
**Manuscript:** "A reproducible, fully auditable pipeline confirms within-cohort the MARS Mars1 immunoparalysis program and delivers an honest external validation of a 30-gene sepsis prognostic signature" (v1.24.0)
**Reviewer role:** BMC Bioinformatics handling-editor proxy + reporting-standards auditor (fresh first submission; no prior reviews read)
**Review date:** 2026-10-09
**Review file:** `06_review/panel_r1_2026-10-09/A4_venue.md`

---

## 0. Executive summary

This is a single-author, computationally intensive re-analysis of public sepsis transcriptomic cohorts (GSE65682, E-MTAB-4451, LINCS L1000). The manuscript is unusually honest about its own limitations (the primary external AUC 0.585 has a CI that includes 0.5; the drug-repositioning candidates are explicitly hypothesis-generating and none clears a significance gate; the LINCS positive-control "passes" an immunosuppressant). That honesty is an asset for BMC Bioinformatics, which evaluates on methodology and reproducibility rather than perceived interest/impact.

I found **no desk-reject-level (hard-fail) defect**. The submission is venue-appropriate, the structured abstract is well-formed, the figure/table numbering is fully internally consistent, all 40 references are cited, and a sampled subset of DOIs resolves to genuine matching records. There are, however, several **moderate-to-minor reporting/format issues** that should be corrected before submission because they bear on auditability and on BMC's disclosure expectations:

- A concrete cross-reference error (§8 points S09 to "Limitation 7" when the S09 deferral is described in Limitation 6).
- A self-contradiction about supplementary table S09 (index calls it "deferred by design"/empty, yet Data availability and the manifest list it as a deposited table).
- An ambiguous data-availability version statement (results "pinned" at commit v1.16.0 vs the released tag v1.24.0).
- A generative-AI disclosure that names the *environment* (WorkBuddy) but not the *underlying model(s)* — a gap against BMC's preference for naming the tool.
- Minor terminology drift between the structured abstract ("LINCS L1000 positive-control gate") and the manuscript (a positive-control *check*, not a gate).
- Minor inconsistencies: GitHub URL absent from the cover letter; several figures referenced by file path rather than by a formal `*Fig. Sx.*` caption.

None of these invalidate the science; all are fixable in a single revision pass.

---

## 1. Article-type fit and venue fit (BMC Bioinformatics)

**Verdict: appropriate; the non-novel framing is a strength here, not a weakness.**

BMC Bioinformatics explicitly publishes Research articles and Methodology articles covering "computational algorithms, software, models and tools for the modelling and analysis of all kinds of biological data," and it states it does **not** make editorial decisions on perceived interest or impact. The manuscript self-describes (line 8) as "a computational-biology / methods-and-resources study" whose contribution is "a reproducible, fully auditable analytical pipeline, an honest external validation… and an explicit experimental blueprint, not novel hub-gene discovery." That matches what the journal publishes.

Two framing points for the authors:
- The manuscript is submitted as **Research article** (line 8, cover letter line 3, manifest line 24). BMC Bioinformatics also offers a **Methodology article** type. Either is defensible; if the authors consider the *method* (the three-tier positive-anchor pipeline + audit trail) the primary contribution, a Methodology-article framing could be even cleaner. This is a choice, not an error.
- The methodological *novelty* should be stated in one explicit sentence in the Introduction/Discussion. As written, the novelty claim is diffuse ("auditable pipeline, honest external validation, experimental blueprint"). A reviewer will ask "what is new about this pipeline vs. existing limma/WGCNA/LASSO practice?" The answer (the three-tier positive-anchor design that pre-specifies the primary transport metric and refuses post-hoc re-labeling; the per-number provenance table) is present but buried. Surface it.

**No contradiction** between the cover letter's venue rationale and the manuscript's self-description. Both correctly position the work as a method/resource contribution.

---

## 2. Structured abstract

**Verdict: compliant with BMC's required structure; no missing required element.**

The `BMC_structured_abstract.md` provides the four headings **Background / Methods / Results / Conclusions**. BMC Bioinformatics requires a structured abstract with at least Background, Results, Conclusions; the inclusion of a Methods heading is accepted and is appropriate here. Keywords are present (manuscript line 16; identical in the abstract file). No unsupported numerical claim appears in the abstract that is not also in the manuscript body (AUC 0.585/0.638/0.659, prednisone 3.2nd percentile, 0.84 background — all match §3.4–§3.9).

One terminology drift (also reported as Issue I-5 below): the abstract Results line says "no agent cleared the LINCS L1000 positive-control gate," whereas the manuscript describes a positive-control *check* (§3.9, prednisone ranks high) without defining a pass/fail *gate* for candidates. The abstract wording slightly over-structures the manuscript's descriptive finding. Minor, but worth aligning.

Word count is within BMC's ~350-word limit (≈270 words).

---

## 3. Figure / table consistency (manuscript ↔ pack ↔ manifest)

**Verdict: fully consistent. No missing figure, no uncited pack figure, no pack figure left uncited.**

Cross-check of what the manuscript cites, what §8 indexes, what the manifest lists, and what the 10 PNGs provide:

| Item | Inline cited | §8 index | Manifest (figures) | PNG provided |
|------|--------------|----------|--------------------|--------------|
| S1 (Mars1 28-d ROC) | §3.2 | yes | Fig_S1 | Fig_S1.png |
| S2 (score vs endotype) | §3.2 | yes | Fig_S2 | Fig_S2.png |
| S3A (hub genes) | §3.3 | yes | Fig_S3A | Fig_S3A.png |
| S3B (eigengene–trait) | §3.3 | yes | Fig_S3B | Fig_S3B.png |
| S6A (CV ROC) | §3.4 | yes | Fig_S6A | Fig_S6A.png |
| S6B (training ROC) | §3.4 | yes | Fig_S6B | Fig_S6B.png |
| S6C (decision-curve) | §7/§8 | yes | Fig_S6C | Fig_S6C.png |
| S7 (cellular context) | §3.6 | yes | Fig_S7 | Fig_S7.png |
| S9 (external ROC) | §3.5 | yes | Fig_S9 | Fig_S9.png |
| S10 (L1000 rescuers) | §3.9 | yes | Fig_S10 | Fig_S10.png |

All 10 PNGs map 1:1 to cited figures; numbering is non-contiguous (S4/S5/S8 intentionally absent), which the manifest and checklist both acknowledge. Tables: manuscript cites Tables 1–3 (main) and supplementary S01, S02, S04, S05, S06, S07, S08, S08b, S09, S11; the manifest's Supporting_Information.docx lists exactly the same ten supplementary tables. **No discrepancy.**

Caveat (reported as Issue I-6 and I-2): S09 is listed as a deposited supplementary table everywhere, yet §8 calls it "(deferred by design)" and Limitation 6 says it was withheld. See Issue I-2.

Minor captioning inconsistency (Issue I-6): figures S1, S2, S3A/B, S9, S10 carry formal `*Fig. Sx.*` captions in the Results body, whereas S6A/B, S6C and S7 are referenced only by raw file path (`04_figures/S06_*.png`, `04_figures/S07_celltype.png`) without a parallel formal caption in the body. The §8 consolidated index supplies captions for all, so BMC's "caption required" rule is technically met, but the body should be uniform.

---

## 4. Cover letter vs manuscript

**Verdict: accurate and honest; one minor omission (GitHub URL).**

- **Prior BMC Medical Genomics desk-reject: honestly disclosed.** Cover letter line 15 states a prior version "was assessed by *BMC Medical Genomics* and not sent to peer review under that journal's standing policy excluding purely computational studies without independent experimental validation." This is the required honesty disclosure and is correctly framed (BMC Bioinformatics does accept computational studies; the distinction is legitimate). No contradiction with the manuscript.
- **No overclaiming.** The cover letter's summary (five immune hubs confirm within-cohort the Mars1 program; seven agents are hypothesis-generating; concordance ≤ 0.84 background; LINCS non-discriminating) matches §3.3, §3.7, §3.9 exactly.
- **MR-layer removal: consistent.** Cover letter line 16 ("two-sample Mendelian-randomisation layer… removed in v1.20.0") matches Data availability (line 221: "MR layer was removed at commit 7704c9a (v1.20.0)") and manifest line 3.
- **Minor omission (Issue I-7):** the cover letter cites the Zenodo DOI (10.5281/zenodo.23042366) but does **not** state the GitHub repository URL or the `v1.24.0` tag, both of which appear in the manuscript (§219, §225) and the manifest (lines 4–5). For consistency of the data/code-availability statement across the submission packet, the cover letter should name the repo + tag.

---

## 5. Generative-AI disclosure (manuscript §2.11)

**Verdict: meets BMC's core policy; one gap (model identity not named).**

BMC's generative-AI policy requires: (i) disclosure of use; (ii) no AI listed as author; (iii) no AI generation/alteration of data/figures; (iv) authors take responsibility and verify outputs. §2.11 satisfies (i), (ii), (iii), (iv):
- Use disclosed across drafting, table assembly, code writing, reference retrieval, adversarial review.
- "No AI tool is listed as an author or contributor" — explicit.
- "No reported data were created, generated, imputed or altered by generative AI… no image was altered in a way that changes the data" — explicit.
- "All AI-assisted output was reviewed, edited and… rewritten by the author, who takes full responsibility" — explicit.

**Gap (Issue I-4):** the disclosure names the *environment* ("a desktop AI-agent environment (WorkBuddy…)") but states "the specific underlying model identities are not individually logged and are treated as fungible." BMC's guidance prefers that the tool/model be named where known. Even a statement such as "routing to several commercial LLMs (e.g., OpenAI/Anthropic-class models) via the WorkBuddy agent" would be stronger than "fungible/unlogged." This is a disclosure-completeness item, not a compliance failure, but BMC editors increasingly expect it.

---

## 6. Data / code availability consistency

**Verdict: Zenodo DOI consistent across all three artefacts; GitHub URL consistent in manuscript + manifest but missing from cover letter; version statement internally ambiguous.**

| Field | Manuscript | Cover letter | Manifest |
|-------|-----------|-------------|----------|
| Zenodo DOI 10.5281/zenodo.23042366 | line 221 | line 17 | line 5 |
| GitHub URL …/sepsis-immunoparalysis-hub | line 221, 225 | **absent** | line 4 |
| Tag v1.24.0 | line 221, 225 | absent | line 3 |
| MIT licence / CITATION.cff | §225 | — | line 14 |

The Zenodo DOI is identical in all three places — no inconsistency. The GitHub URL + tag are present in manuscript and manifest but not the cover letter (Issue I-7, minor).

**Version ambiguity (Issue I-3):** Data availability (line 221) says "The current evaluated commit `1212f7b` is tagged `v1.16.0` (the results-pinned base); the MR layer was removed at commit `7704c9a` (`v1.20.0`)… this `v1.24.0` release is built on top of both." A reproducibility auditor cannot tell at a glance whether the *exact* result files cited in §7 (the CSVs backing every number) live at tag `v1.24.0` or at `v1.16.0`. For an "auditable pipeline" paper this ambiguity undercuts the central selling point. Clarify that the cited result files are frozen at (or re-exported under) tag `v1.24.0`, or state explicitly that `v1.24.0` is the citable snapshot containing the §7 artefacts.

---

## 7. References

**Verdict: all 40 cited; Vancouver style; sampled DOIs resolve to genuine records. No fabrication detected in the sampled set.**

- Citation coverage: a programmatic extraction of every `[n]` token in the manuscript shows all integers 1–40 are cited at least once (no orphan references; no cited number > 40). Vancouver (numbered, author–title–journal–year–volume–pages–DOI) format is correctly applied.
- DOI spot-checks performed (6): results below.

| Ref | DOI | Result |
|-----|-----|--------|
| 5 Scicluna *Lancet Respir Med* 2017 | 10.1016/S2213-2600(17)30294-1 | **Resolves** — real MARS endotype paper; title/authors match citation |
| 32 Giamarellos-Bourboulis *JAMA* 2025 | 10.1001/jama.2025.24175 | **Resolves** — "Precision Immunotherapy to Improve Sepsis Outcomes: The ImmunoSep Randomized Clinical Trial"; matches citation |
| 36 Giamarellos-Bourboulis *Cell* 2020 | 10.1016/j.cell.2020.08.051 | **Resolves** (title "Activate: Randomized Clinical Trial of BCG Vaccination against Infection in the Elderly" returned) — matches citation |
| 8 Peng *Front Immunol* 2023 | 10.3389/fimmu.2023.1152117 | **Inconclusive** — Frontiers returned a bot-wall/empty page, not a 404; plausible, not verified |
| 17 Wang *Front Immunol* 2024 | 10.3389/fimmu.2024.1328667 | **Inconclusive** — same Frontiers bot-wall; not a 404 |
| 33 Joshi *Front Immunol* 2023 | 10.3389/fimmu.2023.1130214 | **Inconclusive** — same Frontiers bot-wall; not a 404 |

The three Frontiers DOIs could not be machine-verified because the publisher blocked automated retrieval; this is a fetch limitation, **not** evidence of fabrication. The authors' §2.11 statement ("any candidate that did not resolve to a real record being discarded, with all cited references verified by identifier") is consistent with the citations I could resolve. I recommend the authors re-confirm the three Frontiers DOIs via PubMed/CrossRef before final submit as a belt-and-braces step, but I am not flagging them as fabricated.

---

## 8. Reporting-checklist honesty (Methods vs claims)

**Verdict: the methods genuinely support the claims; the manuscript is careful not to over-read its own results. Two format-level mismatches remain (S09).**

The study's honesty is its strongest feature:
- The primary external claim (locked-L1 AUC 0.585, CI includes 0.5) is presented as *not* significantly above chance (§3.5, §5 Limitation 1). The abstract repeats this. No inflated claim.
- The drug-repositioning candidates are explicitly "hypothesis-generating… not prioritised by significance" (abstract; §3.7; §4) and the LINCS rescue is called "descriptive only" because an immunosuppressant (prednisone) scores in the 3.2nd percentile (§3.9, §4, §6). This is methodologically scrupulous.
- The selection-chain family-wise error and the label-dependence of the external transport are openly disclosed (Limitation 9).

Format-level mismatch found:
- **S09 (Issue I-2):** §8 indexes "S09, (deferred by design; see Limitation 7)" while Limitation 6 states "No structure-based docking / in-silico ADMET layer (S09 deferred by design)." Two problems: (a) the cross-reference points to the wrong limitation (7, which is about the 28-day endpoint); (b) an "empty/deferred" table is simultaneously listed in Data availability (line 221) and the manifest's Supporting_Information.docx as a *deposited* supplementary table. A reader/auditor cannot reconcile "deferred/empty" with "deposited CSV." Either drop S09 from the deposited-tables list or add a one-line note that S09 is intentionally an empty placeholder. The cross-reference number must be corrected regardless.

---

## 9. Hard-fail / desk-reject checks

I checked each common BMC Bioinformatics technical-rejection trigger:

- Article type allowed (Research article) — **pass**.
- Structured abstract present with required headings + keywords — **pass**.
- Declarations block present (ethics, consent, data, code, competing interests, funding, author contributions) — **pass** (§219–237).
- References numbered, Vancouver, DOIs present, all cited — **pass**; no fabricated ref in sampled set.
- Figures supplied as separate PNG files with captions — **pass** (10 PNGs; captions in §8/index).
- No Chinese/placeholder text in the manuscript body (the manifest's verify script asserts this; my read found none) — **pass**.
- Generative-AI disclosure present and policy-compatible — **pass** (minor model-name gap, Issue I-4).
- Data + code availability statements present with a citable DOI + repo — **pass** (version ambiguity, Issue I-3).

**Conclusion: no desk-reject or technical-rejection trigger identified.** The issues below are pre-submission polish, not blockers.

---

# 10. Issues (mandatory 4-part contract)

---

### Issue I-1 — Wrong limitation cited for the deferred S09 table
【Problem】 The supplementary-materials index points the deferred table S09 to "Limitation 7," but the S09 deferral is actually described in Limitation 6.
【Evidence】 Manuscript §8 line 213: "S09, (deferred by design; see Limitation 7)." Limitation 6 (line 162) reads: "No structure-based docking / in-silico ADMET layer (S09 deferred by design)." Limitation 7 (line 164) is about 28-day endpoint scope and never mentions S09.
【Why it matters】 A wrong cross-reference breaks the audit trail in a manuscript whose entire premise is traceability; a careful reviewer will read it as an editing slip that undermines confidence in the provenance claims.
【Specific fix】 In §8, change "S09, (deferred by design; see Limitation 7)." to "S09, (deferred by design; see Limitation 6)."

---

### Issue I-2 — S09 listed as a deposited table despite being "deferred by design" (empty)
【Problem】 Supplementary table S09 is indexed as "deferred by design" (i.e., not produced) yet is simultaneously listed among the deposited supplementary tables in the Data availability statement and the submission manifest.
【Evidence】 §8 line 213 calls S09 "deferred by design"; Data availability line 221 lists "The supplementary tables (S01, S02, S04, S05, S06, S07, S08, S08b, S09, S11) … accompany the manuscript as deposited CSV"; manifest line 12 includes S09 in the Supporting_Information.docx table list. Limitation 6 confirms S09 was withheld.
【Why it matters】 Claiming an empty/withheld table "accompanies the manuscript as a deposited CSV" is a format-level mismatch between the index and the deposit; it invites a reviewer query about a missing file and weakens the "everything traces to a file" claim.
【Specific fix】 Either (a) remove "S09" from the Data-availability table list (line 221) and from the manifest's Supporting_Information.docx table enumeration, and keep only the §8 note "S09 deferred by design (see Limitation 6)"; or (b) if a placeholder CSV was intentionally deposited, add to §8: "S09: intentionally empty (ADMET/docking layer deferred by design; see Limitation 6)." Do not leave the two statements contradictory.

---

### Issue I-3 — Ambiguous version/commit for the citable results snapshot
【Problem】 The data-availability statement does not make clear whether the exact result files cited in §7 are frozen at tag v1.24.0 or at the earlier results-pinned commit v1.16.0.
【Evidence】 Data availability line 221: "The current evaluated commit `1212f7b` is tagged `v1.16.0` (the results-pinned base); the MR layer was removed at commit `7704c9a` (`v1.20.0`)… this `v1.24.0` release is built on top of both." Zenodo DOI and GitHub release are both tagged v1.24.0 (lines 221, 225).
【Why it matters】 For a paper whose headline contribution is auditability, a reviewer must be able to reproduce every number from the *cited* tag. The phrasing lets "evaluated" (v1.16.0) and "released" (v1.24.0) diverge, creating doubt about which snapshot actually contains the §7 artefacts.
【Specific fix】 Add one explicit sentence, e.g.: "All result files cited in §7 and the deposited CSVs backing every reported number are frozen in, and re-exported under, the citable release tag v1.24.0 (Zenodo 10.5281/zenodo.23042366); commit 1212f7b (v1.16.0) is the results-pinned analytical base on which v1.24.0 was built."

---

### Issue I-4 — Generative-AI disclosure does not name the underlying model(s)
【Problem】 The §2.11 AI-disclosure names the host environment (WorkBuddy) but states the specific LLM identities are "not individually logged and treated as fungible," leaving the tool/model unnamed.
【Evidence】 §2.11 line 61: "Large language model (LLM) assistants accessed through a desktop AI-agent environment (WorkBuddy, which routes each request to one of several commercial large language models; the specific underlying model identities are not individually logged and are treated as fungible writing/analysis assistants)…"
【Why it matters】 BMC's generative-AI policy prefers that the tool/model be identified where known; an editor may request the model class. "Fungible/unlogged" is defensible but weaker than naming the vendor/class, and could prompt a query.
【Specific fix】 Replace the parenthetical with something like: "(WorkBuddy, a desktop agent that routes requests to one or more commercial large language models, e.g. OpenAI/Anthropic-class instruction-tuned LLMs; the specific model version per request was not individually logged)."

---

### Issue I-5 — Structured abstract says "LINCS L1000 positive-control gate" but the manuscript defines no such gate
【Problem】 The structured abstract describes a "LINCS L1000 positive-control gate" that candidate agents pass or fail, whereas the manuscript describes only a positive-control *check* (prednisone scores high) and treats the LINCS result as descriptive.
【Evidence】 `BMC_structured_abstract.md` Results line: "no agent cleared the LINCS L1000 positive-control gate (the immunosuppressant prednisone ranked in the 3.2nd percentile)." Manuscript §3.9 line 137: "A critical caveat came from the positive-control check: prednisone scored high… The glucocorticoid positive control is therefore carried by prednisone alone… The reverse-connectivity is therefore reported descriptively and does not support, even directionally, the small-molecule candidates." No pass/fail gate is defined for candidates.
【Why it matters】 "Gate" implies a binary accept/reject criterion the manuscript does not implement; it slightly over-structures a descriptive finding and could be read as overclaiming.
【Specific fix】 Change the abstract sentence to: "the LINCS L1000 positive-control check was non-discriminating (the immunosuppressant prednisone ranked in the 3.2nd percentile), so the connectivity screen does not support, even directionally, any candidate."

---

### Issue I-6 — Inconsistent formal figure captions in the Results body
【Problem】 Some supplementary figures are introduced with formal `*Fig. Sx.*` captions while others are referenced only by raw file path, producing uneven captioning in the body.
【Evidence】 Formal captions present for S1 (§3.2), S2 (§3.2), S3A/B (§3.3), S9 (§3.5), S10 (§3.9). By contrast §3.4 references "Cross-validated and training ROC: [`04_figures/S06_roc_cv.png`, `04_figures/S06_roc_train.png`]" with no `*Fig. S6A/S6B.*` caption, §3.6 references "`04_figures/S07_celltype.png`" inline without a `*Fig. S7.*` caption, and S6C appears only in §7/§8.
【Why it matters】 BMC requires each figure to carry a caption; although §8 supplies a consolidated index, inconsistent in-body captioning looks unpolished and can confuse the typesetter about which PNG maps to which result.
【Specific fix】 Add parallel formal captions in the body, e.g. in §3.4: "*Fig. S6A. Cross-validated ROC of the 30-gene signature (discovery cohort).* [`04_figures/S06_roc_cv.png`]; *Fig. S6B. Training ROC.* [`04_figures/S06_roc_train.png`]; *Fig. S6C. Decision-curve analysis.* [`04_figures/S06_dca.png`]" and in §3.6: "*Fig. S7. Hub-gene cellular context (bulk surrogate).* [`04_figures/S07_celltype.png`]."

---

### Issue I-7 — GitHub repository URL + tag omitted from the cover letter
【Problem】 The cover letter cites the Zenodo DOI but does not state the GitHub repository URL or the v1.24.0 tag, both of which appear in the manuscript and manifest.
【Evidence】 Cover letter line 17: "the repository carries 32 audit assertions and a citable Zenodo snapshot (DOI 10.5281/zenodo.23042366)" — no GitHub URL/tag. Manuscript lines 221/225 and manifest lines 4–5 give `https://github.com/yyx-4113/sepsis-immunoparalysis-hub` (tag v1.24.0).
【Why it matters】 The data/code-availability statement should be consistent across all submission artefacts; an editor cross-checking the cover letter against the manuscript will note the repo URL is missing from the letter.
【Specific fix】 In the cover letter Transparency paragraph, add: "Code and frozen result files are released at https://github.com/yyx-4113/sepsis-immunoparalysis-hub (citable release tag v1.24.0; Zenodo DOI 10.5281/zenodo.23042366)."

---

### Issue I-8 — Methodological novelty is under-stated relative to the "methods-and-resources" framing
【Problem】 The manuscript claims method contribution diffusely and does not state in one sentence what is *new* about the pipeline versus standard limma/WGCNA/LASSO practice, which a BMC Bioinformatics reviewer will probe.
【Evidence】 Line 8 and §4 (lines 147, 149) describe the contribution as "auditable pipeline, honest external validation, experimental blueprint" without isolating the novel methodological device; the genuine novelty (three-tier positive-anchor design that pre-specifies the primary transport metric and refuses post-hoc relabeling; the §7 per-number provenance table) is present but distributed across §1, §2.8–§2.9, §7.
【Why it matters】 BMC Bioinformatics evaluates method articles on whether the method is non-trivial and reusable; failing to foreground the novelty weakens the "Research/Methodology article" case even though the venue fit is otherwise correct.
【Specific fix】 Add to the end of §1 (or the start of §4) one sentence such as: "The methodological advance over standard limma/WGCNA/LASSO re-analysis is the three-tier positive-anchor design — a biology-inevitable Tier-1 signal, a method-positive-control Tier-2 gate, and a pre-specified, non-binding prognostic Tier-3 — together with a per-number provenance table (§7) that pins every reported value to a deposited output, making the confirmation/validation auditable rather than asserted."

---

# 11. § Stands up (elements checked and found compliant)

1. **Structured abstract conforms to BMC requirements.** `BMC_structured_abstract.md` carries Background/Methods/Results/Conclusions, includes Keywords, and contains no numerical claim absent from the manuscript body (AUC 0.585/0.638/0.659, prednisone 3.2nd percentile, 0.84 background all match §3.4–§3.9). Within the ~350-word limit.

2. **Figure/table numbering is fully internally consistent.** Every figure cited inline (S1, S2, S3A/B, S6A/B/C, S7, S9, S10) appears in the §8 index, the manifest, and the 10 supplied PNGs; every supplied PNG is cited; non-contiguous gaps (S4/S5/S8) are intentional and acknowledged in the checklist. Every supplementary table (S01, S02, S04, S05, S06, S07, S08, S08b, S09, S11) cited in §8/manuscript matches the manifest's SI enumeration.

3. **All 40 references are cited and in valid Vancouver style; sampled DOIs resolve to genuine records.** Programmatic extraction confirms integers 1–40 are each cited ≥1×; format is ICMJE/Vancouver. Spot-checked DOIs 5 (Lancet Respir Med 2017 MARS), 32 (JAMA 2025 ImmunoSep), and 36 (Cell 2020 ACTIVATE BCG) all resolve to real articles whose titles/authors match the citations exactly — strong evidence the reference list is authentic, not fabricated.

4. **Prior BMC Medical Genomics desk-reject is honestly disclosed.** Cover letter line 15 discloses the earlier assessment and its policy basis; this honesty is required and present, with no contradiction to the manuscript's computational-study framing (which is in-scope for BMC Bioinformatics).

5. **Generative-AI disclosure meets BMC's core policy.** §2.11 explicitly states no AI authorship, no AI-generated/altered data or figures, and full author responsibility/verification — satisfying BMC's three non-negotiable requirements (disclose use; no AI as author; no AI-generated data).

6. **Declarations block is complete.** Ethics/consent, data availability, code availability, competing interests (none), funding (none), author contributions, and acknowledgements are all present (§219–241), matching the bmc_checklist declarations section.

---

# 12. § Questions for the authors

1. **Reproducibility snapshot:** Are the exact CSV files behind every §7 number present at tag **v1.24.0**, or only at the results-pinned base **v1.16.0**? Please state this explicitly so a reviewer can re-run from the cited tag (see Issue I-3).
2. **S09 status:** Is S09 an intentionally empty placeholder that was nevertheless deposited, or should it be removed from the deposited-tables list? The index ("deferred by design") and the Data-availability list ("deposited CSV") currently conflict (Issue I-2).
3. **Generative-AI model:** Can you name the commercial LLM class(es) routed through WorkBuddy, even at the vendor level, to strengthen the §2.11 disclosure (Issue I-4)?
4. **Frontiers references:** Refs 8, 17, 33 are Frontiers Immunology DOIs I could not machine-verify (publisher bot-wall, not a 404). Can you confirm they resolve via PubMed/CrossRef and that the volume/issue/pages match?
5. **External-validation interpretation:** Given the pre-specified primary metric (locked-L1 AUC 0.585, CI includes 0.5) is not significantly above chance, do you want the abstract's lead framing to foreground the equal-weight sensitivity (0.638) or keep the deliberately honest "real but modest" primary statement? The current honest framing is appropriate for BMC Bioinformatics, but confirm it is your intended emphasis.
6. **Article type:** Have you considered submitting as a **Methodology article** rather than a **Research article**, given the contribution is primarily the auditable pipeline + validation framework? Either is acceptable; we only ask you to confirm the chosen type matches your emphasis.

---

# 13. § What I actually checked

**Files read (submission artefacts only; no prior reviews):**
- `05_reports/manuscript.md` (full, 283 lines) — primary manuscript.
- `07_submission_bmcbio_v1.24.0/Cover_Letter_BMC.md` (full).
- `07_submission_bmcbio_v1.24.0/BMC_structured_abstract.md` (full).
- `07_submission_bmcbio_v1.24.0/bmc_checklist.md` (full).
- `07_submission_bmcbio_v1.24.0/SUBMISSION_MANIFEST.md` (full).

**Checks performed:**
- Article-type / venue fit against BMC Bioinformatics scope (Research & Methodology articles; no impact-based editorial rule).
- Structured-abstract heading structure (Background/Methods/Results/Conclusions) + keyword presence + claim cross-check vs body.
- Figure/table cross-consistency: manuscript inline citations ↔ §8 index ↔ manifest ↔ 10 supplied PNG filenames (manual table, see §3).
- Cover-letter-vs-manuscript consistency (prior-rejection disclosure, MR removal, summary accuracy) and cover-letter data/code statement vs manuscript/manifest.
- Generative-AI disclosure (§2.11) against BMC policy (disclose / no-authorship / no-data-generation / responsibility).
- Data/code-availability consistency of Zenodo DOI and GitHub URL across the three artefacts; version/commit ambiguity.
- Reference audit: programmatic extraction of all `[n]` tokens (confirmed 1–40 each cited ≥1×); Vancouver format check; DOI spot-checks (see below).
- Reporting-checklist honesty: Methods vs claimed results (AUC significance framing, drug-repositioning "hypothesis-generating" framing, FWER/label-dependence disclosures).
- Hard-fail/desk-reject trigger sweep (article type, structured abstract, declarations, references, figures, AI disclosure, data/code availability).

**DOI spot-checks performed (6 of 40) with results:**
- ✅ Ref 5 — 10.1016/S2213-2600(17)30294-1 → real (Scicluna *Lancet Respir Med* 2017, MARS endotype). Title/authors match.
- ✅ Ref 32 — 10.1001/jama.2025.24175 → real (Giamarellos-Bourboulis *JAMA* 2025, ImmunoSep RCT). Title matches.
- ✅ Ref 36 — 10.1016/j.cell.2020.08.051 → real (Giamarellos-Bourboulis *Cell* 2020, ACTIVATE BCG RCT). Title matches.
- ⚠️ Ref 8 — 10.3389/fimmu.2023.1152117 → Frontiers bot-wall returned empty page (NOT a 404); inconclusive, plausible, not flagged as fabricated.
- ⚠️ Ref 17 — 10.3389/fimmu.2024.1328667 → same Frontiers bot-wall; inconclusive.
- ⚠️ Ref 33 — 10.3389/fimmu.2023.1130214 → same Frontiers bot-wall; inconclusive.

**Not read (per instructions):** any REVIEW_*.md / RESPONSE_*.md / REVISION_*.md / ROUND*.md; `06_review/` except this output; `*_SOP.md`; author_verification_statement.md; MEMORY.md; `.workbuddy/memory/`.

**Bottom line:** Venue-appropriate; no desk-reject trigger. Resolve Issues I-1 through I-7 (mostly one-line edits) and consider I-8 before submitting. The manuscript's honesty about its own null/modest results is a genuine strength for BMC Bioinformatics and should be preserved.
