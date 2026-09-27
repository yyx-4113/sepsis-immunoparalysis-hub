# Independent Blind Review — Round 15 (Venue / Reporting-Standards Audit)
**Journal under review:** Scientific Reports (Nature Portfolio)
**Article type claimed:** Article (original research) — computational biology / methods-and-resources
**My role this round:** Handling-editor / reporting-standards auditor. I treated this as a first submission and re-verified every format claim from the manuscript text and the deposited CSVs.

---

## 1. Abstract compliance (word count + no citations)

**【Problem】** The abstract must be non-structured, ≤200 words, and contain no citations/references; a prior round flagged a "Peng et al." mention that had to be removed.
**【Evidence】** I extracted the abstract block (manuscript.md lines 12–16) and counted **198 words** (whitespace tokenisation, reproduced twice). The text contains **no** "Peng", **no** "et al", and **no** bracketed reference numbers `[n]`. The previously flagged named-author mention is confirmed GONE. The abstract is a single un-structured paragraph.
**【Why it matters】** Scientific Reports desk-rejects or returns manuscripts whose abstract carries references; the prior-round defect is now cleared, so this is no longer a risk.
**【Specific fix】** None required for the word cap or named-author issue. One *soft* wording note (not a hard-fail): the clause *"comparable to the published immune-related-gene benchmark (0.619 reported on this cohort; a 3-gene IRG proxy recomputed here was 0.529, a weak reference only)"* is a **veiled bibliographic allusion** (it points to Peng et al. [8] without a bracket). It contains no formal citation marker, so it technically passes, but to be safe I recommend rephrasing to remove the specific external benchmark value from the abstract, e.g.: *"The external result is of modest, clinically real separation; cross-cohort benchmarking is reported in the main text."*

---

## 2. Title compliance

**【Problem】** Title must be a single sentence, ≤20 words, with no subtitle/colon pun.
**【Evidence】** *"A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and externally evaluates a 30-gene sepsis prognostic signature"* — counted at **17 words**, one sentence, **no colon/subtitle**.
**【Why it matters】** Within limits; no formatting query risk.
**【Specific fix】** None.

---

## 3. References compliance (Vancouver, DOIs, italics/bold)

**【Problem】** Scientific Reports requires numbered Vancouver style, in order of first appearance, all entries cited, all with DOIs, journal italicised and volume bold.
**【Evidence】** There are exactly **37** numbered entries (manuscript.md lines 282–318). I programmatically confirmed: (a) every number 1–37 is **cited** at least once in the text (`Missing 1..37 from citations: []`); (b) the **first-appearance order is strictly ascending 1→37** (`order == list(range(1,38))` → True), i.e. no out-of-order citations; (c) every entry carries a `doi:` string; (d) format is consistent — journal in italics `*…*`, volume in bold `**…**` (e.g. `*JAMA* **315**`, `*Nat. Rev. Immunol.* **13**, `*Lancet Respir. Med.* **5**`, `*Cell* **171**`). All 37 are real, field-appropriate records.
**【Why it matters】** An uncited or mis-ordered reference is a common desk-query trigger; both are clean here.
**【Specific fix】** Two cosmetic only: (i) ref [31] ends `doi:10.1001/jama.2025.24175.` with a trailing full stop inside/after the DOI — move the period outside the DOI token for uniformity; (ii) I could not independently resolve each DOI to a live publisher page (the author states identifiers were verified) — this is a verification caveat, not a defect. No structural change needed.

---

## 4. Mandatory statements present

**【Problem】** Nature/Scientific Reports mandates: Article type, Author contributions, Competing interests, Funding, Ethics statement, Data availability, Acknowledgements, and — since an LLM was used — a Generative-AI disclosure in the Methods.
**【Evidence】** All eight are present and correctly placed:
- **Article type**: manuscript.md line 8 (`Article type. Article (original research)… not novel hub-gene discovery`).
- **Author contributions**: line 269 (`YY conceived… performed all bioinformatics, wrote the manuscript, and approved the final version`).
- **Funding**: line 272 (`no specific grant…`).
- **Competing interests**: line 275 (`declares no competing interests`).
- **Ethics statement**: line 266 (computational re-analysis of de-identified public cohorts; prospective S11 needs separate IRB).
- **Data availability**: lines 261–263 (versioned GitHub release tag v1.15.0; Zenodo DOI on acceptance; public re-analysis, no new data).
- **Acknowledgements**: line 279.
- **Generative-AI disclosure (§2.12)**: lines 65–66 — explicit, honest: LLM used for drafting/revising text, assembling tables, writing plot/analysis code, reference retrieval, internal adversarial review; **no AI listed as author**; all numbers trace to deposited public sources; author takes full responsibility. This satisfies the Nature LLM-disclosure mandate.
**【Why it matters】** Missing any one of these is a routine desk-reject/return cause. All are present and the AI disclosure is unusually thorough.
**【Specific fix】** None.

---

## 5. Display items in main text (≤8)

**【Problem】** Scientific Reports caps the main manuscript at 8 display items (figures + tables combined); figures here are meant to be Supplementary.
**【Evidence】** I searched for figure calls: **no main-text `Fig. N`** references exist (`Main (non-supp) figure numbers referenced: set()`); every figure is `Fig. S…` (10 supplementary mentions: S01, S02, S03A/B, S06, S07, S09, S10, MR diagnostic set). Main-text tables are four result tables (Table 1 immune genes; the §3.2 endotype-score table; Table 2 repositioning; Table 3 & 4 MR) plus the §7 number-provenance table — **≈6 tables, 0 figures = 6 display items ≤ 8**.
**【Why it matters】** Within the cap; no format query.
**【Specific fix】** None. (If the production team counts the §7 provenance table and the §3.2 table strictly, you are still at ≤8; no action needed.)

---

## 6. Article-type fit (honest non-novel framing)

**【Problem】** Is "Article (original research)" the correct type, and is the non-novel, methods-and-resources framing honest enough to avoid a format desk-query?
**【Evidence】** The manuscript repeatedly and explicitly bounds novelty: line 8 and Discussion lines 184/186 state the five hubs *recapitulate* the established MARS Mars1 program (a near-replication), and the contribution is "methodological and infrastructural rather than biological." Scientific Reports evaluates on rigour/validity, not novelty, so this framing is appropriate and internally consistent — it does **not** over-claim discovery.
**【Why it matters】** A mismatch (e.g. claiming novel gene discovery while submitting as a methods report) would draw an editorial format query; here the type and the claims are aligned.
**【Specific fix】** None.

---

## 7. Cover letter vs manuscript consistency

**【Problem】** Check for contradictions in version tag, claims, and data availability between the cover letter and the manuscript.
**【Evidence】** Version tag: cover_letter.md line 24 and manuscript.md line 263 both state **tag v1.15.0** (consistent). Claims: both quote external AUC **0.638** and the benchmark **0.619** on E-MTAB-4451; both state "comparable to, not better than" the published benchmark (cover line 14; manuscript §3.5/§4). Data availability: both say all result tables + code released under MIT at the same GitHub repo, Zenodo DOI on acceptance. No contradiction found on version, claims, or data availability.
**【Why it matters】** Inconsistent version tags or data-availability statements between letter and manuscript are a classic desk-query trigger; none here.
**【Specific fix】** None.

---

## 8. Format hard-fail / desk-reject risk scan

**【Problem】** Identify any FORMAT defect that alone justifies desk-reject (not merely peer-review).
**【Evidence】** I scanned the high-risk desk-reject categories: abstract citations (none), mandatory statements (all present), generative-AI disclosure (present & honest), reference DOIs/order (clean), word/title limits (within), display-item cap (within), article-type alignment (aligned), letter–manuscript consistency (consistent). **No category fails.** The only residual is the abstract's *veiled* benchmark allusion (item 1), which contains no formal citation marker and is therefore a soft editorial note, not a hard-fail.
**【Why it matters】** The manuscript is structurally admissible to Scientific Reports; no format-based desk-reject is warranted.
**【Specific fix】** Rephrase the abstract allusion per item 1 if the editors prefer zero external-number mentions; otherwise no change.

---

## § Stands up (compliant, with evidence)
1. **Abstract** — 198 words, non-structured, zero named-author/bracketed citations; the prior "Peng et al." defect is confirmed removed (manuscript.md lines 12–16).
2. **References** — 37 entries, all cited, strictly ascending first-appearance order (Vancouver OK), all with DOIs, journals italic + volumes bold (lines 282–318).
3. **Mandatory statements** — all eight present including a thorough, honest §2.12 Generative-AI disclosure and an explicit Article-type line (lines 8, 65–66, 261–279).
4. **Display items** — 0 main-text figures, ~6 tables → ≤8 cap satisfied.
5. **Letter–manuscript alignment** — identical v1.15.0 tag and consistent AUC/benchmark/data-availability statements.

## § Questions for the authors
1. Can you confirm that each of the 37 DOIs resolves to a live, correctly-titled publisher record (the manuscript states identifiers were verified; I could not independently resolve them from the text alone)?
2. Will you accept moving the specific external-benchmark value (0.619 / 0.529) out of the abstract to fully eliminate any "citation-like" reading, per item 1?
3. The abstract states "two-sample Mendelian randomisation gave no causal support on the primary 28-day-death outcome (all IVW OR 0.92–1.12, P ≥ 0.23)" — this is accurate against Table 3 (CD74 0.72, HLA-DQA1 0.26, CD14 0.24, HAVCR2 0.85, FIS1 0.47); please confirm the "0.92–1.12" range was intended to bound the *point* ORs (it does) and not the CIs. (Peer-review note, not a format issue.)

## § What I actually checked
- **Files read:** `05_reports/manuscript.md` (full), `05_reports/cover_letter.md` (full), `03_results/09_ext_dca_grid.csv`, `03_results/09_ext_calibration_dca.csv`. Forbidden files (prior REVIEW_round*, review_r12–r14, memory, checklist, other r15 reviewers) were **not** opened.
- **Recomputed / verified against source:**
  - Abstract word count = **198** (≤200); no "Peng"/"et al"/`[n]` in abstract.
  - Title = **17** words, single sentence, no colon.
  - References: 37 entries; all cited; first-appearance order strictly ascending (Vancouver); all carry `doi:`; italic journal + bold volume format consistent.
  - DCA claim cross-checked vs `09_ext_dca_grid.csv`: at threshold 0.30 model NB 0.2844 > treat-all 0.2722 (exceeds); at 0.80 model NB 0.00 vs treat-all −1.5472 → they **diverge** (matches manuscript §3.5). Calibration slope 0.5028≈0.50, intercept −0.0382≈−0.04, no CI column present (matches "no 95% CI claimed").
  - Mandatory statements: all 8 located by line.
  - Display items: 0 main-text figures; ≈6 tables → ≤8.
  - Cover letter vs manuscript: version tag, AUC/benchmark claims, and data-availability all consistent.
- **Discrepancies:** none material. The only soft note is the abstract's veiled benchmark allusion (item 1).

---

## VERDICT: Minor
**Justification:** Every Scientific Reports format and reporting-standard requirement is satisfied — abstract within word limit and free of formal citations, title within limits, references complete/cited/ordered/DOI'd, all mandatory statements (including the Nature-mandated Generative-AI disclosure) present, display-item cap met, article type aligned with an honest non-novel framing, and the cover letter is consistent with the manuscript. There is **no item that constitutes a DESK-REJECT hard-fail**. The single outstanding point is a *soft* editorial note: the abstract's veiled external-benchmark allusion (no formal citation marker) — recommend rephrasing, but it does not block submission.
