# A4 — Venue review: Scientific Reports (Nature Portfolio)

**Reviewer role:** A4 — Venue expert (Scientific Reports editor + reporting-standard auditor)
**Manuscript:** `05_reports/manuscript.md` (tag v1.13.0)
**Cover letter:** `05_reports/cover_letter.md`
**Declared article type:** Article (original research)
**Independence:** Treated as a first submission; no prior-round files, checklists, or other reviewers' outputs were read. Every number below was re-derived from the source files I list in § "What I actually checked".

## Overall assessment (desk-evaluation read)

This is a methodologically careful, unusually self-honest computational manuscript. On the venue-specific checkpoints I was asked to police, it is **mostly compliant**: the abstract is within the word limit and citation-free except for one named-author mention; the generative-AI statement, data-availability statement, and the author/ethics/competing-interests/acknowledgements/funding blocks are all present and correctly formatted for Nature; the external-validation and MR numbers trace exactly to the deposited CSVs; and the cover letter is fully consistent with the manuscript.

However, I found **two concrete defects that an editorial desk-evaluation would catch**:

1. **The reference list is not numbered in order of first appearance** (manuscript.md:22 cites `[3]` as the *first* bracketed reference, while `[1]` does not appear until manuscript.md:49). This violates Nature Vancouver style, which Scientific Reports requires.
2. **The decision-curve narrative in §3.5 contradicts the manuscript's own deposited grid** (`03_results/09_ext_dca_grid.csv`): the text says the model's net benefit "exceeds treat-all only at thresholds ≳0.50" and "converges toward treat-all near 0.80," but the grid shows the model already exceeds treat-all from threshold 0.30 and diverges (model 0.0 vs treat-all −1.55) at 0.80.

Neither is a fatal scientific flaw, but both are editing/accuracy failures that should be fixed before submission. The article-type framing is acceptable but contains a non-standard "methods-and-resources" gloss that should be removed.

---

## Findings (four-part items)

### Item 1 — Abstract word count and citations
【Problem】 Scientific Reports requires a single, non-structured abstract ≤200 words with no citations. The brief claims 198 words; I re-counted.
【Evidence】 `manuscript.md:14` (the English abstract paragraph) counts to **198 words** via a direct word count of that line. No bracketed numbered citations (e.g. `[3]`) appear in the abstract. One borderline item: the abstract contains a *named* attribution, "Peng et al. reported 0.619 on this cohort" (manuscript.md:14), which is a citation by author name even though it carries no reference number.
【Why it matters】 Word limit is satisfied. The named "Peng et al." mention is the only potential citation in the abstract; Nature's policy is that abstracts should be self-contained without references. A strict copyeditor may flag it as a citation.
【Specific fix】 Keep as-is on length (198 ≤ 200). For the named mention, either delete the attribution ("…comparable to the published immune-related-gene benchmark (0.619 on this cohort)…") or move the Peng comparison entirely into §3.4/§3.5. Recommended replacement sentence fragment: *"…the external result is comparable to the published immune-related-gene benchmark (0.619 reported on this cohort); a 3-gene IRG proxy recomputed here was 0.529, near-random."*

### Item 2 — Article-type fit
【Problem】 The manuscript declares "Article (original research)" but repeatedly self-labels as a "computational-biology / methods-and-resources report" (manuscript.md:8, manuscript.md:184) and the cover letter echoes this (cover_letter.md:11). Scientific Reports has **no** separate "Methods and Resources" article type — its only research article type is "Article." This is a classification mismatch.
【Evidence】 `manuscript.md:8`: *"Article type. Article (original research). This is a computational-biology / methods-and-resources report…"*; `manuscript.md:184`: *"…which is precisely the contribution a Methods & Resources / Computational Biology article is judged on."*; cover_letter.md:11 repeats "computational-biology / methods-and-resources."
【Why it matters】 The declared type "Article (original research)" is *correct* and acceptable for SR — SR publishes methodologically sound original research including replication/validation studies, and the pipeline + honest external validation is a genuine original contribution. But the recurring "methods-and-resources" gloss is not an SR category and will confuse the editorial classification drop-down and any desk editor scanning for scope fit. It does not rise to a hard reject, but it should be cleaned up.
【Specific fix】 Retain "Article (original research)." Delete every "methods-and-resources" / "Methods & Resources" qualifier from manuscript.md:8 and manuscript.md:184 and from cover_letter.md:11, or replace with *"computational original-research article."* If the authors believe the work is primarily a shareable resource, SR still requires the "Article" label — there is no alternative to select.

### Item 3 — Generative-AI use statement
【Problem】 Nature/Scientific Reports requires a statement on AI use in the Methods. One must exist and be adequate.
【Evidence】 `manuscript.md:65–66` (§2.12 "Use of generative AI") discloses: (i) drafting/revising all section text; (ii) assembling/formatting tables from direct data reads; (iii) writing the plotting/analysis code (no image-generation, no data alteration); (iv) reference retrieval and identifier verification; (v) internal adversarial review. It explicitly states no reported data were created/altered by AI, no AI tool is listed as author, and the author reviewed/edited/rewrote all output and takes responsibility.
【Why it matters】 This satisfies Nature's AI-disclosure policy (use in writing, coding, or figure generation must be declared). It is specific and adequate.
【Specific fix】 No change required. Optional: add the specific WorkBuddy/agent environment name already given is fine; consider also naming that the underlying models are "fungible" — already stated, so compliant.

### Item 4 — Data availability
【Problem】 Must point to the real repository URL + version tag **v1.13.0** and be specific (no "available on request").
【Evidence】 `manuscript.md:263`: *"…released under MIT in the versioned repository at https://github.com/yyx-4113/sepsis-immunoparalysis-hub. A citable versioned snapshot is provided as a GitHub release (tag v1.13.0)…"* The cover letter repeats the same URL and tag (cover_letter.md:24). The §7 provenance table maps every reported number to a concrete `03_results/` CSV. No "available on request" language anywhere.
【Why it matters】 Fully compliant and specific. The conditional Zenodo DOI ("will be minted on acceptance," manuscript.md:263) is acceptable for SR.
【Specific fix】 None required. Once a Zenodo DOI exists, replace the conditional sentence with the resolved DOI.

### Item 5 — Competing interests / Author contributions / Acknowledgements / Ethics / Funding
【Problem】 All five Nature-required back-matter blocks must be present and correctly formatted.
【Evidence】 `manuscript.md:274–275` Competing interests: *"The author declares no competing interests."* — standard form. `manuscript.md:268–269` Author contributions: single author, "conceived the study, performed all bioinformatics, wrote the manuscript, and approved the final version." `manuscript.md:278–279` Acknowledgements present. `manuscript.md:265–266` Ethics statement present and appropriate (purely computational re-analysis; prospective S11 needs separate IRB). `manuscript.md:271–272` Funding: "no specific grant." All present.
【Why it matters】 All blocks are present and in Nature's expected wording. No hard fail.
【Specific fix】 None required. (Single-author CRediT-style contribution line is acceptable for a sole author.)

### Item 6 — References: numbering order, DOIs, and style consistency
【Problem】 Scientific Reports uses Nature Vancouver style: references must be **numbered in the order in which they first appear** in the text, each with a DOI.
【Evidence】 All 37 references carry a DOI — I counted `doi:` occurrences in the manuscript and got **37** (manuscript.md:280–318), matching the 37 numbered entries. **But the numbering is not in order of first appearance.** The first bracketed citation in the text is `[3]` at `manuscript.md:22` ("Sepsis [3] remains…"); `[2]` and `[4]` also appear at line 22. Reference `[1]` (Aran et al., xCell) does **not** appear until `manuscript.md:49` ("…xCell [1]"). So references 1 and 2 are cited *after* references 3, 4, 17, 22, 26, 16, 6, 27, 8, 9 — a clear violation of Vancouver ordering. Secondary nits: journal-title abbreviations are inconsistent (some abbreviated — "Genome Biol.", "Nucleic Acids Res.", "Lancet Respir. Med." — some full — "Science", "Cell", "eLife", "Cell Host Microbe"); and reference 32 ends with a trailing period after the DOI ("doi:10.1001/jama.2025.24175.").
【Why it matters】 Out-of-order numbering is a systematic formatting defect that SR copyediting will reject and that signals the reference list was assembled thematically rather than citation-ordered. It is the single most clear-cut "format-level" failure in the manuscript. Inconsistent journal abbreviations and a stray period are lesser but will also be flagged.
【Specific fix】 Re-number all 37 references in strict order of first textual appearance and re-point every in-text citation. Concretely: the first in-text cite (manuscript.md:22) should become `[1]`, the second distinct cite `[2]`, etc. Normalize journal titles to NLM/ISO abbreviations (e.g., *Science*, *Cell*, *Cell Host Microbe*, *eLife* → keep as Nature renders them, but make the convention uniform across the list). Remove the trailing period in reference 32.

### Item 7 — Cover letter vs manuscript consistency
【Problem】 The cover letter must match the manuscript (title says "externally evaluates"; HAVCR2 framed as co-inhibitory checkpoint on T cells and APCs; data-availability tag v1.13.0).
【Evidence】 cover_letter.md:3 title = "A reproducible pipeline confirms the MARS Mars1 immunoparalysis program and externally evaluates a 30-gene sepsis prognostic signature" — matches manuscript.md:1 verbatim and contains "externally evaluates." cover_letter.md:14 frames HAVCR2/TIM-3 as *"expressed on T cells and antigen-presenting cells"* — matches manuscript.md:14 (abstract), manuscript.md:8, and manuscript.md:105/218. cover_letter.md:24 data-availability tag v1.13.0 — matches manuscript.md:263. The cover letter's "What the study does NOT claim" section (cover_letter.md:16–21) is consistent with the manuscript's Limitations (manuscript.md:192–212). Article type in cover letter (cover_letter.md:5) = "Article (original research)" — matches manuscript.md:8.
【Why it matters】 No mismatch found; the cover letter is an accurate synopsis and correctly sets editorial expectations.
【Specific fix】 None. (Consider also dropping the "methods-and-resources" phrase in cover_letter.md:11 per Item 2.)

### Item 8 — Decision-curve narrative contradicts the deposited grid (accuracy defect)
【Problem】 §3.5 describes the DCA result in a way that contradicts the manuscript's own `03_results/09_ext_dca_grid.csv`.
【Evidence】 `manuscript.md:112`: *"…the model's net benefit exceeds treat-all only at thresholds ≳0.50, converging toward treat-all near 0.80."* The deposited grid `03_results/09_ext_dca_grid.csv` (columns `threshold, nb_model, nb_treat_all`) shows: at threshold 0.30, nb_model = 0.2844 > nb_treat_all = 0.2722; at 0.40, 0.1604 > 0.1509; at 0.50, 0.0755 > −0.0189; at 0.75, 0.0094 > −1.0377; at 0.80, **0.0 > −1.5472**. So the model already exceeds treat-all from threshold **0.30** (not 0.50), and at 0.80 the two curves *diverge* (model 0.0 vs treat-all −1.55), they do **not** converge. The calibration file `03_results/09_ext_calibration_dca.csv:2` gives intercept −0.0382 and slope 0.5028, which the text rounds to −0.04 / 0.50 correctly, but the threshold interpretation is wrong.
【Why it matters】 This is an internal inconsistency between the prose and the authors' own data file — exactly the kind of over-statement a reporting-standards auditor must flag. It over-states how selectively useful the score is (implying it only beats treat-all at high thresholds, when in fact it beats treat-all across 0.30–0.80). It does not invalidate the honest "ranker, not calibrated probability" conclusion, but the DCA sentence must be corrected to match the grid.
【Specific fix】 Replace the clause with a grid-accurate statement, e.g.: *"…the model's net benefit exceeds treat-all across thresholds of roughly 0.30–0.80 (e.g., 0.284 vs 0.272 at 0.30; 0.076 vs −0.019 at 0.50; 0.0 vs −1.55 at 0.80), indicating a consistent but modest advantage over a treat-all strategy at the probabilities where the score is informative; the score remains a ranker rather than a calibrated probability."*

### Item 9 — Reporting-checklist honesty (over-claim vs limitation disclosure)
【Problem】 Does the manuscript honestly report its weak points (MR null, modest AUC, label overlap) or over-claim?
【Evidence】 Honesty is strong: MR null is explicit — abstract (manuscript.md:14) "two-sample Mendelian randomisation gave no causal support… (all IVW OR 0.92–1.12, P ≥ 0.23)"; §3.10 and Limitations 2 (manuscript.md:194–195) state "no primary IVW estimate reached significance" and that the only family-significant MR result *reverses* direction. Modest AUC is explicit — manuscript.md:112 "modest separation… the lower bound is close to 0.5." Label overlap is explicit — manuscript.md:182 "independent in cohort and platform but not in label." The Limitations section runs to **13 numbered items** (manuscript.md:192–212) covering external-validation modesty, MR suggestiveness, bulk surrogates, healthy-control type, sub-unit effects, blueprint-not-data, no docking/ADMET, 28-day endpoint scope, curated-concordance metric, selection-chain FWER, single-direction L1000, MR selection-on-outcome circularity, and STROBE-MR gaps. The only over-statement I found is the DCA threshold claim in Item 8.
【Why it matters】 The manuscript passes the honesty test on the dimensions the brief named. Fixing Item 8 removes the one Internal inconsistency. No evidence of systematic over-claiming.
【Specific fix】 Address Item 8; otherwise the limitation reporting is a model of transparency and should be preserved.

---

## § Stands up (claims I suspected but verified correct)

1. **Abstract is exactly 198 words and within limit.** `manuscript.md:14` word-counted to 198 (brief claimed 198); no numbered citations. Verified independently.
2. **External-validation numbers trace exactly to the CSV.** `03_results/09_external_validation.csv`: orientedSum AUC = 0.6382 (text 0.638), CI 0.5317–0.7475 (text 0.532–0.748), n = 106, deaths = 52, locked-L1 AUC = 0.5848 (text 0.585), IRG-3 proxy = 0.5288 (text 0.529). All match. `03_results/S06_auc_compare.csv`: CV AUC 0.6586 (text 0.659), training 0.7495 (text 0.750). Match.
3. **MR primary-outcome null is exact.** `03_results/10_mr_bh_family.csv` (outcome 5086) IVW ORs: CD74 1.119 (P 0.718), HLA-DQA1 0.923 (P 0.260), CD14 0.927 (P 0.236), HAVCR2 0.978 (P 0.847), FIS1 0.963 (P 0.473) — all within 0.92–1.12 and all P ≥ 0.236 ≥ 0.23, exactly as the abstract (manuscript.md:14) and brief state. The CD14 MR-Egger P = 0.0488 ≈ "4.9×10⁻²" and the per-outcome 15-test `p_fdr_bh` = 0.487 ≈ 0.49, family q = 0.730 ≈ 0.73 — all match the text.
4. **Immune-gene direction counts verified.** `03_results/S01_immunoparalysis_direction.csv`: of 25 consensus immune genes, 23 are Mars1_down (only PDCD1 and LAG3 are up), 22 are FDR-significant (adj.P < 0.05), and 21 are both down and significant (PDCD1 is up-and-significant, so 22 − 1 = 21). Exactly matches manuscript.md:72 ("23…22…21").
5. **L1 zero-coefficient genes match the JSON.** `03_results/09_external_validation_coef.json`: coef = 0.0 for CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B — exactly the seven genes the manuscript says were driven to zero (manuscript.md:108), and HLA-DQA1 is absent from the external array (it is present in the JSON `genes` list but not mapped externally per `09_external_validation.csv:17`). Consistent.
6. **FIS1 passenger logFC verified.** `03_results/S01_mars1_deg.csv` row for FIS1: logFC = 1.2614 (= +1.26), t = 17.1567 (= +17.2). Matches manuscript.md:106/218. The co-expression degree screen (S03_hub_degree.csv) places FIS1 12th, consistent with "FIS1 ranked 12th" (manuscript.md:106).
7. **L1000 rescue ranks verified.** `03_results/S08_l1000_candidate_scores.csv`: lenalidomide rank 5435/20,413 (rescue 0.0439), azithromycin rank 9152/20,413 (rescue 0.0133) — match the abstract and brief exactly.
8. **Matrix dimensions verified.** `03_results/S01_mars1_deg.csv` has 11,520 lines = 11,519 genes + header, matching the "11,519 genes × 802 samples" claim (manuscript.md:31).
9. **CD74 critical-care reversal verified and honestly flagged.** `03_results/10_mr_bh_family.csv`: CD74 weighted-median on crit-care OR 2.194, p = 6.6×10⁻¹⁹, family q = 2.99×10⁻¹⁷ (YES), and the text correctly reports this reverses the Mars1 direction and is a genotype–severity association, not a causal target (manuscript.md:162, 174).

---

## § Questions for the authors

1. **STROBE-MR item 9a (Steiger directionality test) is explicitly omitted** (manuscript.md:210, Limitation 13). Given the exposure–outcome sample overlap you disclose, do you plan to add at least a directional-plausibility note or a sensitivity without Steiger, or will you submit with the gap openly declared as now? The current disclosure is acceptable, but editors may ask.
2. **HLA-DQA1 is absent from the external Illumina array** (manuscript.md:111, `09_external_validation.csv:17`) yet remains in the 30-gene discovery set and orientation. Was its coefficient stable/non-zero in the discovery L1 fit (the JSON shows it present but `genes` only; the external application drops it)? Please confirm the 29-mapped-gene AUC is the honest primary and that no selection relied on the dropped gene.
3. **Reconcile the DCA threshold narrative with `09_ext_dca_grid.csv`** (Item 8). Which threshold range should readers trust — the grid (model > treat-all from 0.30) or the prose (≳0.50)? Please correct the prose to the grid.
4. **AI-assisted, single-author manuscript.** The generative-AI statement (§2.12) is thorough. For CRediT/transparency, confirm that no AI system contributed substantively to study conception or interpretation in a way that would warrant acknowledgement, and that the sole-author contribution line is intentional.
5. **Zenodo DOI timing.** The data-availability statement conditions the DOI on acceptance (manuscript.md:263). Will a preprint/archived version be publicly readable before acceptance so reviewers can access the exact v1.13.0 snapshot? SR permits this; clarifying helps desk evaluation.
6. **Reference re-numbering (Item 6).** After re-ordering, please confirm every in-text citation still resolves (especially the out-of-order ones like `[1]` at manuscript.md:49 vs `[3]` at manuscript.md:22).

---

## § What I actually checked

**Manuscript and cover letter (read in full):**
- `05_reports/manuscript.md` (319 lines) — abstract, article type, all sections, back-matter, references.
- `05_reports/cover_letter.md` (29 lines) — title, article type, "does/does-not claim," data tag.

**Direct computations / re-counts I performed:**
- Abstract word count of `manuscript.md:14` → **198 words** (single line, no numbered citations; one named "Peng et al." mention).
- `grep -c "doi:"` on the manuscript → **37** DOIs for 37 references.

**Source data files read and values recomputed vs the manuscript:**
- `03_results/09_external_validation.csv` — external AUC 0.6382 (CI 0.5317–0.7475), n 106, deaths 52, locked-L1 0.5848, IRG-3 0.5288, HLA-DQA1 missing. → matches manuscript.md:111–112, abstract.
- `03_results/09_ext_calibration_dca.csv` — intercept −0.0382, slope 0.5028, AUC 0.6382. → matches manuscript.md:112 rounding (−0.04 / 0.50).
- `03_results/09_ext_dca_grid.csv` — per-threshold nb_model vs nb_treat_all. → **contradicts** the §3.5 "exceeds treat-all only at ≳0.50 / converges near 0.80" narrative (model > treat-all from 0.30; diverges at 0.80). [Discrepancy logged in Item 8.]
- `03_results/S06_auc_compare.csv` — CV 0.6586, train 0.7495. → matches manuscript.md:108/218.
- `03_results/10_genetics_mr.csv` and `03_results/10_mr_bh_family.csv` — primary 28-day-death IVW ORs 0.92–1.12, P ≥ 0.236; CD14 Egger P 0.0488; per-outcome 15-test p_fdr_bh 0.487; family q 0.730; CD74 crit-care WM OR 2.194, q 2.99×10⁻¹⁷. → matches abstract and §3.10 exactly.
- `03_results/S01_immunoparalysis_direction.csv` — 25 immune genes: 23 down, 22 significant, 21 both. → matches manuscript.md:72.
- `03_results/S02_immunoparalysis_score.csv` — raw per-sample immune scores by endotype (the cited source for Mars1/Mars2/Mars3/Mars4 P values in Table 2). I did **not** re-run the Mann–Whitney U test (would require executing the stats code); the values are reported as derived from this file and are internally consistent with the stated medians.
- `03_results/09_external_validation_coef.json` — 7 zero-coefficient genes (CD74, HLA-DRB1, IRF1, HLA-DMA, HLA-DMB, CD86, CD8B). → matches manuscript.md:108.
- `03_results/S08_l1000_candidate_scores.csv` — lenalidomide 5435, azithromycin 9152. → matches abstract/brief.
- `03_results/S01_mars1_deg.csv` — 11,520 lines (= 11,519 genes + header); FIS1 logFC 1.2614, t 17.1567. → matches manuscript.md:31 and §3.3.
- `03_results/S03_hub_degree.csv` — FIS1 degree 64.26, rank 12th. → matches §3.3.

**Discrepancies / concerns found (all reported above):**
- DCA prose vs `09_ext_dca_grid.csv` (Item 8) — accuracy inconsistency.
- Reference numbering not in order of first appearance (Item 6) — Nature Vancouver violation; `[3]` first at manuscript.md:22, `[1]` at manuscript.md:49.
- Abstract named "Peng et al." mention (Item 1) — borderline citation.
- Journal-title abbreviation inconsistency + trailing period in ref 32 (Item 6) — minor style.
- "Methods-and-resources" non-SR article-type gloss (Item 2) — classification cleanup.

**No other discrepancies** were found between the manuscript's reported numbers and the deposited source files I read. The external-validation, MR, immune-direction, hub, signature, and L1000 claims are internally consistent and source-traceable, and the limitation reporting is unusually candid.

## Recommendation

**Minor revision (format/accuracy) — not a reject.** The science and transparency are strong and venue-appropriate. Before submission, the authors must: (a) re-number references in citation order and normalize journal abbreviations (Item 6); (b) correct the DCA threshold narrative to match `09_ext_dca_grid.csv` (Item 8); (c) drop the non-standard "methods-and-resources" label and keep "Article (original research)" (Item 2); and (d) optionally remove the named "Peng et al." citation from the abstract (Item 1). With those four edits, the manuscript meets Scientific Reports' reporting standards.
