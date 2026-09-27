# Round-11 independent review — Scientific Reports submission readiness (v1.11.0)

**Manuscript:** `05_reports/manuscript.md` (v1.11.0, commit `e49ccb5`, tag `v1.11.0`, pushed)
**Target venue:** *Scientific Reports* (Nature Portfolio), article type = **Article**
**Review date:** 2026-09-27
**Panel:** 4 blind experts, convened with enforced independence (firewall against all prior `REVIEW_*.md` / `RESPONSE_*.md` / `review_r*/` / memory artifacts). Each expert read only the manuscript (+ `cover_letter.md` for the venue reviewer) and, where applicable, recomputed from deposited `03_results/*.csv`.
**Review artifacts:** `05_reports/review_r11/_PANEL_BRIEF.md`, `A1_domain.md`, `A2_design.md`, `A3_implementation.md`, `A4_venue.md`.

---

## 1. Independence statement

Mechanism: experts were given a self-contained brief forbidding any read of prior review/response/revision files, memory, overview, submission manifest, deposit SOP, or other reviewers' outputs. They were told to treat the manuscript as a first submission and to verify every checkable claim themselves.

Evidence independence worked:
- **Cross-cluster on a genuine defect.** A2 (design) and A1 (domain) independently converged on the HAVCR2/TIM-3 over-interpretation and on the MR-overlap caveat from different angles — the diagnostic signature of real independence (not re-litigation of known points).
- **No leakage from prior rounds.** No expert reproduced the Round-9/Round-10 "discovery-verb" or "truncation" debates; all findings are derived from the *current* v1.11.0 text.
- **Complementarity.** A3 (provenance) found the numbers *fully reconcile* while A4 (venue) and A1 (domain) found *presentation/language/citation* defects — the two layers (arithmetic vs framing) are cleanly separated, exactly what independence is meant to expose.

---

## 2. Verdict table

| Reviewer | Layer | Verdict | Basis |
|---|---|---|---|
| A1 — Domain (sepsis immunology) | Domain | **Major revision** | 5 domain concerns, all Tier-2/3 (interpretation softening + missing foundational citations); core Mars1 confirmation intact |
| A2 — Design (stats / MR) | Design | **Major revision** | uncorrected MR overlap; dexamethasone factual error; DCA-on-uncalibrated-probabilities overstatement |
| A3 — Implementation (provenance) | Implementation | **Accept (provenance sound)** | every headline number reconciles exactly from CSVs; 1 minor wording |
| A4 — Venue (Sci Rep compliance) | Venue | **Major revision** | 1 hard-fail (ref [32] incomplete) + Chinese text in §7 + competing-interests wording |

**Distribution:** 0 desk-reject, 0 minor-only, 3 major, 1 accept. **Overall editorial verdict: MAJOR REVISION — not desk-reject, not minor.** The science is sound and reproducible; the required changes are mechanical/copy-edit plus judicious softening of two over-stated biological/statistical claims.

---

## 3. Cross-verification table (editor-verified)

| Manuscript location | Manuscript claims | Independently recomputed | Checked by | Verdict |
|---|---|---|---|---|
| §3.1 Mars1-vs-Other DEG | 3,597 at \|logFC\|≥0.3 & FDR<0.05 | 3,597 (exact); sepsis-vs-healthy 448 | A3 | ✓ |
| §3.1 immune genes | 23/25 down; 22 FDR-sig (incl. PDCD1 up); 21 both | exact; non-sig = CD8B, GZMA (down), LAG3 (up) | A3 | ✓ |
| §3.5 external AUC | 0.638 (95% CI 0.532–0.748), n=106, 52 deaths, 29/30 mapped | AUC 0.6382; bootstrap CI 0.531–0.742; HLA-DQA1 absent | A3 + editor | ✓ |
| §3.10 / §5 "1 of 45 q<0.05" | CD74 crit-care weighted median, q≈3×10⁻¹⁷ | only that test significant (present in both 45-test and 15-test q-columns = same test) | A2 + A3 + **editor** | ✓ |
| §3.10 CD14 28-d Egger P | 4.9×10⁻² | t(4) two-sided = 4.88×10⁻² (normal-approx would be 5.11×10⁻³) | A2 | ✓ (t-correction real) |
| §3.9 L1000 library | 20,413 compounds | exact | A3 | ✓ |
| §3.9 "prednisone and dexamethasone … scored high" | both high | **dexamethasone rescue 0.0315, rank 6,808/20,413 = 33.35th pct (below median); only prednisone high** | **editor** | ✗ **FALSE** |
| §3.10 CD74 crit-care "Egger SE 0.111 < IVW SE 0.325 is physically implausible" | implausible ordering | SEs reconstruct exactly; ordering is routine MR-Egger math (Σwᵢ(xᵢ−x̄)² > σ²Σwᵢ); real caveat is df=1 | A2 | ✗ **mischaracterised** |

---

## 4. Graded consolidated issue list

### Tier 1 — conclusion-relevant / submission hard-fail (must fix before submit)
- **T1-1 (Venue hard-fail).** Ref [32] Giamarellos-Bourboulis *JAMA* (2025) has **no volume, pages, or DOI** (`manuscript.md:315`). Nature/Sci Rep cannot typeset it. *Fix:* complete to `*JAMA* **[VOL]**, [PAGES] (2025). https://doi.org/[DOI]` from PubMed/publisher record. This is a copy-edit blocker, not a scientific defect.
- **T1-2 (Factual error).** "prednisone and dexamethasone … scored high" (`manuscript.md:142`) is **false for dexamethasone** (33.35th percentile, below median). *Fix:* "prednisone scored high (rank 651/20,413, 3.2nd percentile); dexamethasone was below median (rank 6,808/20,413, 33.4th percentile)." The glucocorticoid caveat logic survives (prednisone alone suffices), but the example must be corrected. *(Editor-verified.)*

### Tier 2 — interpretation / credibility (fix by rewording + citations)
- **T2-1 (Domain).** HAVCR2/TIM-3 down-regulation read as "reduced APC abundance rather than T-cell-intrinsic exhaustion" over-states the evidence; TIM-3 is canonically an *up*-regulated exhaustion marker, and bulk blood cannot separate cell-abundance from per-cell expression. *Fix:* state the direction cannot adjudicate mechanism without single-cell/flow resolution (paste-ready sentence in A1 #1).
- **T2-2 (Domain).** "separate up-regulated T-cell exhaustion axis (PDCD1/LAG3 up)" presented as established Mars1 biology, but only PDCD1 is significant (LAG3 adj.P=0.55) and it is *not* in the original Scicluna/Davenport Mars1 definition. *Fix:* reframe as candidate, incompletely supported signal (A1 #2).
- **T2-3 (Domain).** HAVCR2 mislabelled "antigen-presentation/monocytic hub gene" in Abstract/§3.3 while body calls it "APC-expressed checkpoint" — internal inconsistency. *Fix:* "five immune hubs anchored in the antigen-presentation/monocytic program (CD74, HLA-DQA1, CD14, FCGR3A) plus the APC-expressed checkpoint HAVCR2/TIM-3" (A1 #3).
- **T2-4 (Domain).** Foundational immunoparalysis literature (Monneret on mHLA-DR dynamics; Venet) omitted although mHLA-DR is repeatedly invoked as "validated clinical anchor." *Fix:* add Monneret & Venet citations (A1 #4).
- **T2-5 (Domain).** ImmunoSep "53% unclassifiable" is unverifiable from the manuscript and "no mortality benefit" should be framed as underpowered. *Fix:* insert exact reported percentage from the publication + underpowered framing (A1 #5).
- **T2-6 (Design).** MR exposure–outcome sample overlap (eQTLGen∩UK-Biobank) flagged but never corrected; "hypothesis-generating" does not neutralise the downward-biased SE on the one crossing-threshold test. *Fix:* explicitly state all q-values are overlap-biased and the CD74 crit-care q≈3×10⁻¹⁷ "may not survive overlap correction; must not be read as evidence for CD74-directed therapy" (A2 #1). Optionally run `mrSampleOverlap`.
- **T2-7 (Design).** "CD74 crit-care Egger SE < IVW SE is physically implausible" is **incorrect** (A2 #4). *Fix:* replace with the real caveat — Egger has df=1, null intercept, contributes no independent information beyond IVW, and both SEs remain overlap-biased.
- **T2-8 (Design).** Decision-curve "positive net benefit" is built on miscalibrated probabilities (slope 0.50). *Fix:* recalibrate and re-run DCA, or drop the DCA utility claim and state discrimination-only; report bootstrap CI for the slope (A2 #5).
- **T2-9 (Venue).** Chinese text in main body §7 heading ("数字溯源表") and provenance table cells (`manuscript.md:222, 229–249`). Sci Rep requires English. *Fix:* translate §7 heading + all table cells to English.

### Tier 3 — format / wording (mechanical)
- **T3-1 (Venue).** "Competing interests" sentence body says "no conflict of interest" → "no competing interests" (house template). (`manuscript.md:277`)
- **T3-2 (Design wording).** "after correcting the MR-Egger p-values … only one of 45" misattributes the survivor to the Egger correction; the survivor is the weighted median (normal-approx). Rephrase (A2 #2).
- **T3-3 (Implementation wording).** DCA "converging to zero near 0.77" → "by 0.80" (grid `09_ext_dca_grid.csv` shows 0.0 at 0.80). (`manuscript.md:112`)
- **T3-4 (Venue).** Body word count ≈6,000–6,500 vs ~4,500 guideline — condense Limitations/Discussion (recommendation, not blocker).
- **T3-5 (Venue).** §2.12 AI disclosure could name the specific commercial model(s) for full clarity.
- **T3-6 (Design, optional).** Add DeLong paired test of signature vs IRG AUC on the 106 E-MTAB-4451 samples; state EPV=3.8 explicitly in §3.4; state bootstrap spec for external CI.

---

## 5. Consensus / complementarity / disagreement

**Consensus.** All four agree: (i) the core Mars1 confirmation and the independent external validation (AUC 0.638) are sound and reproducible; (ii) the MR and L1000 layers are appropriately scoped as hypothesis-generating; (iii) no desk-reject is warranted; (iv) the manuscript is honest about limitations. A1/A2/A4 all independently flag the HAVCR2/TIM-3 handling as over-stated.

**Complementarity.** A3's "numbers all reconcile" liberates the other three to focus on *framing* defects — the panel cleanly separated the arithmetic layer (sound) from the presentation layer (needs work). A2's statistical re-computation and A1's biological re-reading converged on the same two soft spots from opposite directions.

**Disagreement (adjudicated).**
- *Severity of the MR overlap (A2 #1).* A3 (provenance) did not grade it because it only recomputed numbers; A2 grades it Major. **Adjudication:** adopt A2's stricter read — the manuscript already discloses the overlap and scopes MR as hypothesis-generating, so it is not conclusion-invalidating, but the "one surviving signal" must be explicitly flagged as potentially overlap-biased (T2-6). The lenient provenance verdict certifies the *layer*, not the manuscript.
- *Dexamethasone.* Only A2 caught it; editor independently confirmed it is a **false statement** (T1-2), upgrading it from A2's Tier-2 to a Tier-1 factual error.

---

## 6. Priority must-fix list

| # | Issue | Tier | DESK-REJECT? | Type |
|---|---|---|---|---|
| 1 | Ref [32] complete (volume/pages/DOI) | 1 | No (copy-edit) | must reword/add |
| 2 | Dexamethasone "scored high" → correct to below-median | 1 | No | must reword (factual) |
| 3 | §7 Chinese → English | 2 | No | must reword |
| 4 | HAVCR2/TIM-3 over-interpretation softened (T2-1/2/3) | 2 | No | must reword |
| 5 | Add Monneret/Venet; verify ImmunoSep % (T2-4/5) | 2 | No | must add citation/verify |
| 6 | MR overlap explicitly framed as bias (T2-6/7) | 2 | No | must reword |
| 7 | DCA on calibrated probs only or drop (T2-8) | 2 | No | must reword/reanalysis |
| 8 | Competing-interests wording (T3-1); DCA 0.77→0.80 (T3-3); Egger misdesc (T2-7/T3-2) | 3 | No | must reword |

No DESK-REJECT flag raised. All items are achievable without new experiments.

---

## 7. What stands up (do NOT change)

- Mars1 antigen-presentation/monocytic down-regulation (CD74, HLA-DQA1, CD14, FCGR3A) recapitulated with strong statistics — biologically faithful to MARS literature (A1 §Stands up #1).
- External validation AUC 0.638 (95% CI 0.532–0.748) on independent cross-platform cohort — genuinely honest, recomputed exactly (A3 #3).
- MR-Egger t(n−2) correction correctly implemented (A2 #3).
- 45-test BH arithmetic correct: exactly 1 family-significant test, and it reverses Mars1 direction (A2 #2, A3 #4, editor-verified).
- All 12 cited figures and 29 §7 provenance files exist; references [1]–[35] complete and consistent (A3 #5/6).
- Unusual, commendable transparency about selection-chain FWER, outcome-driven MR gene selection, and single-direction L1000 (A2 §Stands up #5).

---

## 8. Recommended handling path

**A) Revise and resubmit as the same article type (Article, *Scientific Reports*) — RECOMMENDED.** No downgrade is needed (it is already "Article"); no new data are required. The fixes are: complete ref [32] + translate §7 (submission blockers), correct the dexamethasone statement (factual), soften the HAVCR2/TIM-3 and MR-overlap framings, add Monneret/Venet, and tighten DCA/competing-interests wording. Estimated effort: copy-edit + targeted rewording, ~0.5–1 day. Consider adding `mrSampleOverlap` and a DeLong test as optional robustness (T2-6, T3-6) to pre-empt reviewer pushback.

**B) Downgrade article type — NOT indicated.** Already "Article"; the issue is presentation, not article-type mismatch (the Round-10 Path-B reframing already resolved the type question).

**C) Wording-only — NOT viable.** Two items (ref [32] completion, §7 translation) are substantive submission blockers, not mere wording.

---

## 9. Process lessons (what the automated gates could not catch)

The audit (`check_audit_assertions.py`, 21 assertions) verifies arithmetic and provenance *strings* but is blind to the design/framing layer. This panel caught five classes of defect a gate cannot:
1. **Domain over-interpretation** (TIM-3 as APC-abundance; "T-cell exhaustion axis" from one significant gene) — requires biological judgement, not string matching.
2. **Factual misstatement of a recomputed number** (dexamethasone "high") — the number in the CSV was correct; the *prose* inverted its meaning. A gate checks the CSV value, not whether the sentence describes it correctly.
3. **Reference completeness** (ref [32] missing volume/pages/DOI) — outside any numeric gate.
4. **Language compliance** (Chinese in §7 body) — the v1.11.0 adaptation removed the Chinese *abstract* but missed the Chinese §7; a gate keyed on "abstract" missed it.
5. **Conceptual statistical issue** (DCA net-benefit on miscalibrated probabilities) — a logic error, not an arithmetic one.

**Suggested new gate assertions (for v1.12.0):**
- `§7` and all §7 table cells contain no CJK characters.
- Ref [32] matches a regex requiring volume + pages + DOI.
- `dexamethasone` does not co-occur with "scored high" / "high rescue" in §3.9.
- `Egger SE` claim does not contain "implausible".
- DCA sentence references calibrated probabilities OR states "discrimination-only".

---

*Consolidated by the editor (小团). The single worst factual claim (dexamethasone "scored high") was independently re-verified by the editor from `03_results/S08_l1000_positive_control.csv` and confirmed false. The central MR "1 of 45" claim was independently re-verified and confirmed correct.*
