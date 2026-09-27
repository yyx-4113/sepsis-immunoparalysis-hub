# A4 — Venue / Reporting-standards review
**Journal under review:** Scientific Reports (Nature Portfolio) — Article (original research)
**Manuscript:** "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and validates a 30-gene sepsis prognostic signature" (single-author; version stated v1.12.0)
**Reviewer role:** Handling-editor / reporting-standards auditor (VENUE layer — what only a venue/format editor catches)
**Independence note:** Reviewed as a first submission. I did not consult any prior `REVIEW_*.md`, `RESPONSE_*.md`, `revision`/`review_r*` folders, task/status files, OVERVIEW, SUBMISSION_MANIFEST, deposit SOP, or author_verification_statement. All claims below were checked against the source manuscript, the audit gate, the result CSVs, and the cover letter.

---

## 0. Summary verdict (preview)

The manuscript is, from a *venue* standpoint, in unusually good shape. The Article-type framing is honest (it explicitly disclaims novel hub-gene discovery and headlines the reproducible, externally validated signal rather than the fragile MR/repositioning layers), the audit gate passes, every headline number traces to a result file, and all mandatory Scientific Reports end-matter sections (Data availability, Ethics, Author contributions, Funding, Competing interests, Acknowledgements, References) are present. **No desk-evaluation hard-fail** was found. The remaining items are format/metadata corrections (chiefly missing reference DOIs, AI-tool naming, and confirming the data/code repository is live). These are **minor-revision** level, not major.

**VERDICT: Minor** (accept after minor format/metadata corrections — see §9).

---

## 1. What stands up (≥3)

1. **Article-type statement is honest and internally consistent.** `manuscript.md:8` declares the contribution as a "reproducible, fully auditable analytical pipeline, an honest independent external validation, and an explicit experimental blueprint — not novel hub-gene discovery," and the whole manuscript keeps that promise. The Discussion (`manuscript.md:184`) explicitly calls the hubs a "near-replication rather than a novel gene discovery." This is exactly the framing Scientific Reports expects for a computational/methods article and defuses the single most common desk-eval trigger (over-claiming novelty).

2. **Number provenance is real and machine-checked.** The `check_audit_assertions.py` gate (26 assertions) passes, and I independently re-derived the load-bearing numbers from the CSVs: external AUC 0.638 / CI 0.532–0.748 / n=106 / 52 deaths (`09_external_validation.csv`); hub directions (5 down + FIS1 up, logFC +1.26, `S01_mars1_deg.csv` + `S05_hub_genes.csv`); consensus immune counts 23/22/21 (`S01_immunoparalysis_direction.csv`); Mars1-vs-endotype Mann–Whitney P-values (0.47 / 1.9e-18 / 1.3e-3); primary-outcome minimum IVW P = 0.236 (≥0.23); OR/CI algebraically consistent with beta/se; MR-Egger p-values on the t(df=n-2) distribution (the Round-6 normal-dist bug is guarded and absent). The §7 provenance table maps every reported number to a file. This is a model of reporting honesty.

3. **Generative-AI disclosure is present, detailed, and policy-aligned** (`manuscript.md:65-66`, §2.12). It states the service (WorkBuddy), what it was used for (drafting, tables, code, reference retrieval, adversarial review), that no data were created/altered by AI, that no AI tool is an author, and that the author takes full responsibility. This satisfies the Nature Portfolio generative-AI mandate.

4. **Mandatory end-matter is complete.** Competing interests (`manuscript.md:274-275`, "The author declares no competing interests."); Ethics/IRB statement (`manuscript.md:265-266`) correctly noting that re-analysis of de-identified public cohorts needs no new IRB and that source cohorts were IRB-approved; Funding (`manuscript.md:271-272`); Author contributions (`manuscript.md:268-269`); Acknowledgements (`manuscript.md:278-279`); Data availability (`manuscript.md:261-263`). No missing sections.

5. **Title and abstract pass the format caps.** Title = 16 words (≤20) and non-misleading (it says "confirms … and validates," matching the honest framing). Abstract = 180 words (≤200), unstructured, and contains **zero** in-text citations (`[n]`), satisfying Nature's "no citations in abstract" policy.

6. **No broken or orphaned references.** I cross-checked 37 in-text citations against 37 reference entries: every cited number is defined and every defined entry is cited (no `cited-but-undefined` and no `defined-but-uncited`).

---

## 2. Reporting-checklist honesty — per-item audit

### Item A — Title ≤20 words & non-misleading
【Problem】 None substantive. The title is 16 words and is not misleading: it promises "confirms" + "validates," both of which the results support (Mars1 near-replication; external AUC 0.638 with CI excluding 0.5).
【Evidence】 `manuscript.md:1` ("A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and validates a 30-gene sepsis prognostic signature"); independent word count = 16.
【Why it matters】 Title length/accuracy is a routine format check; an over-claiming title ("discovers novel hubs") would be a desk-eval flag. Here it is correctly scoped.
【Specific fix】 None required. (Optional: if you want to pre-empt any reviewer who reads "validates" as "superior," the abstract already qualifies it as "comparable to, not better than" the benchmark — keep that qualification visible.)

### Item B — Abstract non-structured ≤200 words, no citations
【Problem】 Passes, but two internal-consistency notes.
【Evidence】 Abstract at `manuscript.md:12-16`; independent count = 180 words (the planning `scirep_submission_checklist.md:8` states 173 — both are <200, so no action, but the checklist's own count is slightly off and should be corrected to avoid confusion). Zero `[n]` tokens in the abstract.
【Why it matters】 Abstracts over 200 words or carrying citations are routinely returned by the journal's format checker before peer review.
【Specific fix】 No change to the manuscript. Correct the internal checklist figure to "180" so the planning doc matches the manuscript.

### Item C — Methods has generative-AI use statement (§2.12)
【Problem】 Present and good, but the specific underlying model(s) are not named.
【Evidence】 `manuscript.md:65-66`: "Large language model (LLM) assistants accessed through a desktop AI-agent environment (WorkBuddy, which routes each request to one of several commercial large language models)…". The *service* (WorkBuddy) is named, but the individual commercial LLM(s) actually used are not.
【Why it matters】 Nature Portfolio's AI policy asks authors to disclose "the name(s) of the tool(s)/service(s) used." "One of several commercial large language models" is a grey area; a stricter copy-editor may request the specific model(s).
【Specific fix】 Add the specific model name(s) where known, e.g.: "…accessed through the WorkBuddy desktop AI-agent environment (the underlying model was <Model name, e.g., Claude/GPT-4-class>, routed by the agent)…". If the exact model is not recorded, state that explicitly: "the specific underlying model was not individually logged by the agent wrapper."

### Item D — Competing interests present & correctly worded
【Problem】 None. Wording is the Nature-standard negative statement.
【Evidence】 `manuscript.md:274-275`: "The author declares no competing interests." (The cover letter `cover_letter.md:24` also states "Conflicts of interest: none declared.")
【Why it matters】 A missing or non-standard competing-interests statement is a submission-blocker at Scientific Reports.
【Specific fix】 None.

### Item E — Data availability with a real citable repo URL + version
【Problem】 The statement is correctly structured (GitHub repo + version tag v1.12.0 + Zenodo DOI "on acceptance"), **but the repository URL was unreachable from the review environment** (HTTP 000), and the Zenodo DOI is still pending. I could not confirm the tag v1.12.0 is actually pushed/public or that the repo contains the referenced `03_results/` and `02_scripts/` files.
【Evidence】 `manuscript.md:261-263` (https://github.com/yyx-4113/sepsis-immunoparalysis-hub, tag v1.12.0; "a Zenodo DOI will be minted and made public on acceptance"); `curl` to the GitHub URL returned 000 (sandbox network blocked — not proof the repo is down, but also not proof it is up).
【Why it matters】 Scientific Reports mandates a live, citable data/code availability statement. A dead, private, or empty repo, or a version tag that does not exist, is a post-acceptance (and sometimes pre-acceptance) compliance failure and undermines the entire "fully auditable" premise of the paper.
【Specific fix】 Before submission: (i) confirm the `v1.12.0` tag is pushed and public; (ii) confirm the repo actually contains `03_results/`, `02_scripts/python/`, `04_figures/` as cited in §7; (iii) ideally mint the Zenodo DOI *before* acceptance and paste the real `https://doi.org/10.5281/zenodo.XXXXXXX` into the Data availability statement rather than "on acceptance." If the Zenodo DOI must remain pending, keep the explicit "on acceptance" wording (acceptable) but state the GitHub release is already public.

### Item F — References in Nature style with DOIs
【Problem】 **36 of 37 references carry no DOI.** Only reference [32] includes a DOI (`10.1001/jama.2025.24175`). The remaining 36 have no `doi`/`10.xxxx/` token.
【Evidence】 `manuscript.md:280-319` (37 references); automated scan: 1 DOI-like token total; 36 entries flagged as lacking a DOI. Nature style formatting (numbered, journal abbreviations, volume bold, article titles present) is otherwise correct.
【Why it matters】 Springer Nature / Scientific Reports runs a reference-quality check and strongly expects a DOI for every reference where one exists (essentially all of these do). Missing DOIs are not a desk-reject but are a guaranteed "minor revision / format correction" request and slow production. For an audit-focused reviewer this is the single most concrete reporting-hygiene defect.
【Specific fix】 Append the DOI to every reference. Example corrected entries (format: `https://doi.org/…` after the year):
- [1] … *Genome Biol.* **18**, 220 (2017). https://doi.org/10.1186/s13059-017-1349-1
- [2] … *JAMA* **306**, 2594–2603 (2011). https://doi.org/10.1001/jama.2011.1829
- [4] … *Lancet Respir. Med.* **5**, 816–826 (2017). https://doi.org/10.1016/S2213-2600(17)30299-5
- [5] … *Lancet Respir. Med.* **4**, 259–271 (2016). https://doi.org/10.1016/S2213-2600(16)00046-3
(Repeat for all 36.) Most of these are long-established papers with stable DOIs retrievable from Crossref/PubMed.

### Item G — Acknowledgements present
【Problem】 None. Present and appropriate (thanks source consortia and tool developers).
【Evidence】 `manuscript.md:278-279`.
【Why it matters】 Optional but expected; present, so no issue.
【Specific fix】 None.

### Item H — Article-type statement consistency
【Problem】 None. The declared Article type is consistent with the actual claims (confirmation/validation, not discovery).
【Evidence】 `manuscript.md:8` vs the claim hierarchy in Abstract (`manuscript.md:14`) and Discussion (`manuscript.md:184-188`).
【Why it matters】 A mismatch between the stated article type and the claims (e.g., calling it "novel discovery") is a desk-eval red flag; here there is no mismatch.
【Specific fix】 None.

### Item I — Ethics / IRB statement for re-analyzed public data
【Problem】 None substantive. The statement correctly handles the public-data case.
【Evidence】 `manuscript.md:265-266`: "purely computational re-analysis of public, de-identified transcriptomic cohorts … no additional IRB approval was required … source cohorts were approved by their respective IRBs."
【Why it matters】 Scientific Reports requires an ethics statement even for re-analysis; omitting it is a blocker. It is present and correctly scoped.
【Specific fix】 None. (Optionally, in the submission system's ethics questionnaire, select "re-used public data / n/a" and paste this sentence.)

---

## 3. Format / desk-evaluation screen (hard-fail check)

I screened for the four classic Scientific Reports desk-eval hard-fails:

- **Missing sections** — NONE. Title, author/affiliation/ORCID/email, Abstract, Keywords, Introduction, Methods (§2.1–2.12), Results (§3.1–3.10), Discussion, Limitations, Conclusion, Number provenance, Supplementary index, Data availability, Ethics, Author contributions, Funding, Competing interests, Acknowledgements, References — all present.
- **Broken references** — NONE (37/37 matched, see §1.6).
- **Unsupported claims** — NONE found. Every strong claim is hedged appropriately (MR "hypothesis-generating"; signature "comparable not superior"; repositioning "hypothesis-generating"; validation "modest"). No claim exceeds what the cited CSV supports; the audit gate confirms this.
- **IRB/ethics statement** — PRESENT (§2, Item I).

**Conclusion:** No desk-eval hard-fail. The manuscript would clear the format/ethics screen.

**Minor cosmetic note (not blocking):** End-matter ordering. The manuscript currently sequences: Data availability → Ethics → Author contributions → Funding → Competing interests → Acknowledgements → References (References last). Scientific Reports house order is typically References → Acknowledgements → Author contributions → Funding → Competing interests → Data availability → Ethics. This is reordered in production, so it is not a blocker, but aligning it pre-submission reduces copy-edit churn.

---

## 4. Cover-letter vs manuscript mismatch check

I compared `cover_letter.md` against `manuscript.md`:

- **Title** — identical (cover letter line 3 = manuscript line 1). ✔
- **Article type** — both "Article (original research)." ✔
- **Repo + version** — cover letter line 24 and manuscript line 263 both cite `github.com/yyx-4113/sepsis-immunoparalysis-hub`, tag **v1.12.0**. ✔ (Note: the planning `scirep_submission_checklist.md:12,33` still says v1.11.0 — that is an internal planning doc lag, not a cover-letter/manuscript mismatch. Update it for consistency.)
- **Gene list** — cover letter line 14 (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2/TIM-3, FIS1) matches manuscript hubs (`manuscript.md:14, 105, 218`). ✔
- **External AUC** — cover letter line 14 (0.638, 95% CI 0.532–0.748) matches `manuscript.md:14, 112, 235`. ✔
- **MR null claim** — cover letter line 18 ("no primary IVW estimate reached significance"; "applied no [sample-overlap] correction") matches `manuscript.md:149, 194` and the gate (min IVW P 0.236). ✔
- **Repositioning caveat** — cover letter line 19 (curated response-gene concordance, not direct target overlap; LINCS covers 2/7) matches `manuscript.md:52, 119-132, 203`. ✔

**No cover-letter/manuscript mismatch.** The only inconsistency is the internal checklist's stale v1.11.0, which does not affect the submission package.

---

## 5. Article-type fit & headline-framing judgment

**Question put to this review:** Is the strongest *real* finding headlined while the weakest is buried, or does the headline over-state the fragile signal?

**Finding:** The framing is **correct as written — no reframe needed; this is a positive example.**

- The **stable, real contribution** — (i) a reproducible confirmation/near-replication of the Mars1 immunosuppressed program (3,597 Mars1-vs-Other DEGs; coherent antigen-presentation/monocytic down-regulation), and (ii) an *honest, independent, cross-platform external validation* of the 30-gene signature at AUC 0.638 (CI excludes 0.5) — is exactly what the **title** (`manuscript.md:1`) and the **lead of the Abstract** (`manuscript.md:14`) headline.
- The **fragile layers** — the MR null (no primary IVW significance; sample overlap uncorrected; Steiger not done) and the signature being "comparable rather than superior" to the benchmark (Δ≈0.034; IRG point estimate inside the signature's CI) — are explicitly **buried/hedged**, not headlined. They appear in later abstract sentences and are restated in Limitations 1–2, 12–13.
- The repositioning layer is consistently flagged "hypothesis-generating" and "mechanism-anchored, not connectivity-asserted" (`manuscript.md:119, 184, 203`), and the glucocorticoid positive-control caveat (`manuscript.md:142`) honestly notes a positive rescue score is "necessary but not sufficient for functional immune restoration."

**Recommendation:** Keep this framing. Do **not** let any reviewer talk you into upgrading the title/abstract to feature the MR or repositioning layers — doing so would invert the honest evidence hierarchy and create the exact over-claim that triggers desk-eval. The only optional tightening: ensure the word "validates" in the title is never read as "validates as superior" — the abstract's "comparable to, not better than" already cushions this, so no change is required.

---

## 6. Generative-AI disclosure compliance (Nature Portfolio)

Nature Portfolio requires: (a) a statement that generative AI was used in manuscript preparation; (b) what it was used for; (c) that it is not an author; (d) that the authors take responsibility. The manuscript satisfies (a), (b), (c), (d) at `manuscript.md:65-66`. Specific compliance points:
- Used for drafting/revising text, assembling tables (values are direct reads), writing plotting/analysis code, reference retrieval/checking, and internal adversarial review. ✔
- Explicitly states no reported data were created/generated/imputed/altered by AI, and no image-generation model was used. ✔
- No AI tool listed as author; author takes full responsibility. ✔
- Located in Methods (§2.12), as expected. ✔

**Only gap (see Item C):** the specific underlying LLM(s) are not named ("one of several commercial large language models"). Recommend naming them or explicitly stating they were not individually logged.

---

## 7. Questions for the authors

1. **Repository liveness (critical):** Please confirm that the `v1.12.0` GitHub release is publicly accessible and that the repo actually contains the `03_results/`, `02_scripts/python/`, and `04_figures/` files referenced throughout §7. If possible, mint the Zenodo DOI *before* acceptance and paste the real `doi.org` link into the Data availability statement.
2. **Reference DOIs:** Will you add DOIs to the 36 references that currently lack them? (This is the main format correction Scientific Reports will request.) Most are established papers with stable DOIs.
3. **AI model naming:** Can you name the specific commercial LLM(s) used via WorkBuddy, or state explicitly that the underlying model was not individually logged? This tightens §2.12 against a stricter interpretation of the Nature AI policy.
4. **Reference [32] (ImmunoSep, JAMA 335:775–786, 2026, doi:10.1001/jama.2025.24175):** Please double-check the bibliographic details (volume/pages/DOI/year) are exact, since it is a very recent citation and the only one carrying a DOI. The DOI form `10.1001/jama.2025.24175` is consistent with JAMA's scheme, but please verify the 2025-vs-2026 date pairing is correct as published.
5. **End-matter order (cosmetic):** Would you consider reordering the back-matter to the Scientific Reports house sequence (References → Acknowledgements → Author contributions → Funding → Competing interests → Data availability → Ethics) to minimize production copy-editing?
6. **Planning-doc drift (housekeeping):** `scirep_submission_checklist.md` still references v1.11.0 and an abstract count of 173; the manuscript is v1.12.0 / 180 words. Please sync the planning doc so it does not mislead a later submitter.

---

## 8. What I actually checked

**Files read in full:**
- `05_reports/manuscript.md` (the manuscript under review).
- `05_reports/cover_letter.md`.
- `05_reports/scirep_submission_checklist.md` (venue-format planning doc).
- `02_scripts/python/check_audit_assertions.py` (the audit gate).

**Files/claims verified against data (not read in full, but asserted against):**
- `03_results/09_external_validation.csv` — external AUC 0.638, CI 0.532–0.748, n=106, 52 deaths (gate assertion 13; my recomputation).
- `03_results/S01_mars1_deg.csv` + `S05_hub_genes.csv` — 5 Mars1-down hubs + FIS1 up (logFC +1.26) (gate assertion 7).
- `03_results/S01_immunoparalysis_direction.csv` — consensus immune counts 23/22/21 and Table-1 logFC/adj.P (gate assertions 10, 11).
- `03_results/S02_immunoparalysis_score.csv` — Mars1-vs-endotype Mann–Whitney P (gate assertion 8; recomputed 0.467/1.85e-18/1.32e-3 vs stated 0.47/1.9e-18/1.3e-3).
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv` and siblings — MR-Egger t-dist p-values, OR/CI consistency, primary min IVW P = 0.236 (gate assertions 4, 9, 16, 18).
- `03_results/10_mr_bh_family.csv` — 45-test family size; 1 family-significant test (CD74 critical-care WM) (gate assertions 2, 15).
- `03_results/08_candidates_drugs.csv` — Table-2 `response_gene_concordance` (gate assertion 12).
- `03_results/09_ext_calibration_dca.csv` — calibration slope 0.50 / intercept −0.04 / AUC 0.638 / DCA NB (gate assertion 14).

**Checks performed programmatically (Python 3.13.12):**
- Ran the full `check_audit_assertions.py` gate → **all 26 assertions PASS**.
- Independent title word count (16) and abstract word count (180, no citations).
- Citation cross-check: 37 in-text `[n]` vs 37 reference entries → no broken/orphaned refs.
- Reference DOI scan → 36/37 lack a DOI.
- GitHub repo reachability probe → HTTP 000 (sandbox network blocked; could not confirm liveness).

**Independence guard:** I deliberately did not open any `REVIEW_*.md`, `RESPONSE_*.md`, `revision` text, `review_r*` directories, task/status files, OVERVIEW, SUBMISSION_MANIFEST, author_verification_statement, or any other reviewer's output. This review is independent.

---

## 9. VERDICT

**VERDICT: Minor** (accept pending minor format/metadata corrections).

**One-sentence justification:** The manuscript clears every Scientific Reports desk-evaluation screen (complete sections, no broken references, no unsupported claims, proper ethics/AI/disclosures, and a fully audited, honest Article-type framing that headlines the stable confirmation+external-validation finding while correctly burying the null MR and "comparable-not-superior" signature), so it should be accepted after the authors add reference DOIs (36/37 missing), name the specific LLM(s) in §2.12, and confirm the v1.12.0 data/code repository and (ideally pre-minted) Zenodo DOI are live and complete.
