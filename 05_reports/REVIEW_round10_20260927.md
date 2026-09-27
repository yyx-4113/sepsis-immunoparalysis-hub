# Round-10 Independent Panel Review of v1.9.0

**Manuscript:** `05_reports/manuscript.md` (git tag **v1.9.0**, commit `96f43eb`)
**Repository:** https://github.com/yyx-4113/sepsis-immunoparalysis-hub
**Date:** 2026-09-27
**Editor:** consolidated by the coordinating editor (this report)

---

## 1. Independence statement

Four blind reviewers (A1 domain, A2 design/stats, A3 implementation/provenance, A4 venue/reporting) were convened with a **firewall forbidding any reading of REVIEW_round*.md, RESPONSE*.md, REVISION*.md, review_r1/–review_r9/, SUBMISSION_MANIFEST.md, GITHUB_DEPOSIT_SOP.md, author_verification_statement.md, or each other's outputs.** Each treated v1.9.0 as a first submission and recomputed numbers from raw `03_results/` CSVs.

**Evidence independence worked:** the panel converged on the same structural defect from three angles — A3 (provenance) flagged that the Conclusion says "anchored by hub genes" while the Discussion concedes "near-replication" (D4); A2 (stats) flagged the overstated calibration and imprecise "MR is null" wording; A4 (venue) flagged that the discovery title is contradicted by the manuscript's own "near-replication" admission. None had read the others. The single numeric cluster (calibration slope, MR all-null, IRG label collision) was caught independently by A2 and A3.

The editor personally reproduced the two empirical anchors of the article-type decision: the MR family-BH readout (exactly **1/45** family-significant, direction-reversed; **0/5** primary-outcome IVW significant) and the calibration slope (**0.5028**, intercept −0.0382) — both from source CSVs, confirming A2/A4's empirical claims. The ImmunoSep "53% unclassifiable" citation was verified against the JAMA 2025 primary (doi:10.1001/jama.2025.24175) via web: it was a **dual ferritin + mHLA-DR** algorithm, confirming A1.5.

---

## 2. Verdict table

| Reviewer | Layer | Verdict | One-line rationale |
|---|---|---|---|
| A1 | Domain (sepsis immunology) | **Major** | Core biology sound; HAVCR2 interpretation, truncated checkpoint sentence, ImmunoSep citation, and missing literature need fixing |
| A2 | Design & statistics | **Major** | Numbers verified correct; calibration "well behaved" and "MR is null" overstated; IRG comparison asserted without CI/formal test |
| A3 | Implementation & provenance | **Minor** | All headline numbers reproduce exactly; Egger p correctly t-distributed; 4 trivial provenance/rounding items |
| A4 | Venue & reporting | **Major** | Discovery framing contradicted by manuscript's own admissions; reframe to Methods/Resources (or decisive headline-swap) + STROBE-MR/abstract/reference fixes |

**Distribution:** 3 Major / 1 Minor → overall **Major Revision**.

---

## 3. Cross-verification table (manuscript claim vs independent recomputation)

| # | Manuscript location | Manuscript claim | Independently recomputed value | Who checked | Verdict |
|---|---|---|---|---|---|
| 1 | §2.1 / Abstract | 802 samples (760 sepsis / 42 healthy) | 802 / 760 / 42 (`GSE65682_pheno.csv`) | A3 | ✓ |
| 2 | §3.1 | Mars1 DEG 3,597; sepsis-vs-healthy 448 | 3,597 / 448 | A3 | ✓ |
| 3 | §3.1 | 23/25 down, 22 FDR-sig, 21 both | 23 / 22 / 21 (`S01_immunoparalysis_direction.csv`) | A1, A3 | ✓ |
| 4 | Table 1 | 6-gene logFC/adj.P + signs | exact match | A1, A3 | ✓ |
| 5 | §3.2 | Mars1 score median −0.792; vs Mars2 P=0.47 | −0.7917; P=0.467 | A3 | ✓ |
| 6 | §3.4 / §3.5 | CV 0.659 / train 0.750 / external 0.638 (CI 0.532–0.748) / L1 0.585 | 0.6586/0.7495/0.6382 (0.5317–0.7475)/0.5848 | A2, A3 | ✓ |
| 7 | §3.7 / Table 2 | 7-drug concordance + IFN-γ 4/5 | exact match; IFN-γ 4/5 recomputed | A1, A3 | ✓ |
| 8 | §3.9 | lenalidomide 5,435/20,413; azithromycin 9,152/20,413 | exact match | A3 | ✓ |
| 9 | Table 3 | MR-Egger p (t-distributed) | `2·st.t.sf(|β/se|, df=n−2)` for all 5 genes; normal alternative differs | A2, A3, **editor** | ✓ |
| 10 | §3.10 / Lim 2 | MR all-null on primary; 1/45 family-sig, reversed | 45 tests; 1 family-sig (CD74 crit-care WM, q=3.0e-17, OR 2.19 reversed); 0/5 primary IVW sig | **editor** | ✓ |
| 11 | §3.5 | Calibration "well behaved (slope 0.50, intercept −0.04)" | slope **0.5028**, intercept −0.0382 | **editor** | ✗ overstated (slope 0.50 = over-confident) |
| 12 | §3.5 / A2.5 | IRG "comparable" (0.604 vs 0.638) | IRG recomputed = 0.604 (no CI); `S06` also stores 0.619 (Peng reported) → label collision | A2, A3 | ⚠ needs relabel |
| 13 | §3.8 (cited) | ImmunoSep "53% unclassifiable by mHLA-DR" | dual ferritin + mHLA-DR algorithm; unclassified = normal ferritin AND normal HLA-DR | **editor (web)** | ✗ mis-attributed |

---

## 4. Graded consolidated issue list

### Tier 0 — conclusion-invalidating
None. The core biology (Mars1 immunoparalysis signal, honest external validation, near-replication admission) and every headline number hold.

### Tier 1 — must fix (substantive)
- **T1. Article-type / headline reframe (mandatory).** The discovery title ("multi-omics dissection and in-silico drug repositioning", "isolated hub genes") is internally contradicted by the manuscript's own "near-replication rather than a novel gene discovery" (Discussion) and the all-null MR. *Fix:* swap the headline to confirmation/validation/replication language; demote discovery claims. See §8 for the two handling paths (downgrade vs within-type swap). (A4 primary; A2, A3-D4, editor.)
- **T2. Calibration "well behaved" overstated (A2.6; editor-verified).** Slope 0.5028 (ideal = 1.0) means over-confident predicted probabilities. *Fix:* "acceptable calibration intercept (−0.04) but slope 0.50 → over-confident; present as ranker, not calibrated probabilities" (or add logistic recalibration).
- **T3. HAVCR2 interpretation (A1.1).** Data confirm HAVCR2 is genuinely DOWN (logFC −0.35, adj.P 2.8e-13), but folding it into an "exhaustion axis" contradicts its canonical role as an up-regulated checkpoint. *Fix:* reinterpret HAVCR2-down as an APC/monocyte-abundance correlate, not T-cell-intrinsic exhaustion.
- **T4. Checkpoint-blockade sentence truncated + logic gap (A1.2).** Line 145 ends mid-word ("because rele…") and excludes PD-1/PD-L1 despite PDCD1 being significantly up. *Fix:* complete the sentence with an explicit, citable rationale (Hotchkiss 2019, ref 34, is in the list but undiscussed).
- **T5. "MR layer is null" imprecise (A2.3).** *Fix:* "no significant evidence supporting the expression-level causal hypothesis — the only family-significant result reverses direction and is reported as a genotype–severity association; the primary outcome shows a consistent but non-significant protective direction across three hubs — and is therefore hypothesis-generating."
- **T6. ImmunoSep 53% mis-attribution (A1.5; editor-verified).** *Fix:* "53% unclassified by a dual ferritin-and-mHLA-DR algorithm (mHLA-DR cutoff <5000 receptors/cell on CD45/CD14 monocytes; unclassified = normal ferritin AND normal HLA-DR)"; mHLA-DR remains the validated clinical anchor.
- **T7. STROBE-MR gaps not surfaced in Limitations (A4).** Steiger not done (9a PARTIAL) and intermediate variant counts untabulated (10_counts PARTIAL). *Fix:* add a Limitation line naming both, paralleling the existing sample-overlap and selection-circularity limitations.

### Tier 2 — should fix
- **T8. "Co-expression hub" overstated (A1.3).** Hubs came from tri-method ML on 28-day survival, not the co-expression network (which surfaced erythroid genes). Elevate the honest line already at §3.3.
- **T9. 28-day mortality imperfection (A1.6).** Immunoparalysis drives late death/secondary infection beyond day 28; mHLA-DR should be framed as complementary, not inferior.
- **T10. Missing must-cite literature (A1.7).** mHLA-DR-guided therapy; SRS1/SRS2 and MDPS endotype frameworks; broader immunostimulant RCT landscape. Also tighten the 39% Mars1 mortality citation (A1.4).
- **T11. GM-CSF overstatement (A1.8).** Add the "no mortality benefit" meta-analysis caveat (Bo et al., ref 30) alongside the monocyte HLA-DR recovery claim.
- **T12. MR sensitivity pledge (A2.2).** Pledge a sample-overlap bias-corrected sensitivity (mr_sampleoverlap) and a Steiger test before any claim beyond hypothesis generation.
- **T13. IRG comparison + EPV (A2.5).** Relabel `S06` 0.619 vs `09` 0.604 to avoid collision; soften "comparable" (IRG has no CI, so equivalence untested); state the signature is a biological ranker, not a calibrated predictor, given EPV ≈ 3.8.
- **T14. Abstract "isolated hub genes" (A4).** Replace with "recapitulated/confirmed five immune hubs" + one clause on near-replication; keep the honest MR sentence.

### Tier 3 — polish
- **T15.** Unify CV-AUC source (D1: `S06` 0.6586 vs `09` 0.6582).
- **T16.** Reword "algebraically identical" for wtcs = rescue×√22 (printed 4-dp not exact; D2).
- **T17.** Cover letter mislabels FIS1 as a "hub" — make it "co-expression passenger" (A4).
- **T18.** Add consolidated Figure/Table-legend appendix + Supplementary index (A4).
- **T19.** Abbreviate journal names to NLM style in References (A4).
- **T20.** Deposit a live (private) data/code DOI now rather than "upon acceptance" (A4).

---

## 5. Consensus / complementarity / disagreement

**Consensus.** (a) The manuscript's numbers are trustworthy — A3 reproduced every headline value and confirmed the Egger t-distribution fix from Round-6/9 is stable; A2 independently confirmed. (b) The MR layer is correctly presented as hypothesis-generating; the all-null-on-primary claim is accurate. (c) The external validation is honestly scoped ("comparable not superior"). (d) The discovery framing over-claims relative to the manuscript's own near-replication admission.

**Complementarity.** A1 supplied the biological mechanism fixes (HAVCR2, checkpoint, ImmunoSep, citations) that A2/A3/A4 could not; A2 supplied the statistical framing fixes (calibration, "null" wording, IRG); A3 supplied the provenance assurance that makes the rest actionable; A4 supplied the article-type and reporting-standards synthesis.

**Disagreement — article type (A2 vs A4), adjudicated.** A4 recommends **reframing to Computational Biology / Methods & Resources**; A2 argues the design flaws don't *force* a downgrade and notes the study introduces "no new method, no new resource, no new primary data," so it is not strictly a Methods/Resource article. **Editor's adjudication (per the panel skill: judge whether the strongest finding is buried while the weakest is headlined; if so, usually swap, not downgrade):** The genuine contribution — a fully-auditable, endotype-anchored pipeline; an honest external validation; an explicit experimental blueprint; and exemplary provenance/transparency — is real and valuable, but it is a *reuse-and-confirmation* contribution, not a novel-method or novel-resource contribution. Therefore:
- The **minimum required fix is a mandatory headline-swap** (title + abstract lead + emphasis moved to confirmation/validation/replication; demote discovery claims). This resolves the internal contradiction regardless of article type.
- **Downgrading to Computational Biology / Methods & Resources is the preferred option if the target journal offers that category** (it converts the candid self-limiting caveats into strengths). A2's caveat is noted: without a genuinely new method/resource, the strict definition of a Methods/Resource article may not fit every journal, so the within-type headline-swap is the universal safe fix and the downgrade is an option tied to journal choice.

---

## 6. Priority must-fix list

No DESK-REJECT flags. All issues are fixable by rewording or modest addition; none invalidate the Tier-1 biology or the provenance.

**Must reword (no new analysis):** T1 (title/abstract/emphasis), T2 (calibration), T3 (HAVCR2), T4 (checkpoint sentence), T5 (MR "null"), T6 (ImmunoSep), T7 (STROBE-MR limitation), T8, T9, T11, T14, T16, T17, T19, T20.

**Must add (small analysis/text):** T10 (citations), T12 (sensitivity pledge), T13 (IRG relabel + EPV note), T18 (legends/index), T15 (provenance unify), T21 (live DOI).

---

## 7. What stands up (do NOT change)

1. **Provenance quality is exceptional for a single-author paper** — every number traces to a deposited CSV; A3 reproduced all headline values. (A3, A4)
2. **Egger p-values are correctly t-distributed** — the Round-6 normal-distribution bug is fixed and stable. (A2, A3, editor)
3. **MR family correction is exactly as reported** — 1/45 significant, direction-reversed; 0/5 primary IVW significant. (A2, editor)
4. **External validation is honestly scoped** — AUC 0.638 with CI, explicitly "comparable not superior," L1 weights did not transport. (A1, A2, A3)
5. **Methodological honesty about limitations** — selection circularity, sample overlap, glucocorticoid positive-control caveat, reversed CD74 signal all disclosed. (A2, A4)
6. **Mars1 immunosuppressed biology is accurately recovered** — 23/25 immune genes down; antigen-presentation/monocytic program matches the published MARS picture. (A1, A3)
7. **ImmunoSep specifics (SOFA, no mortality benefit, hemorrhage) are faithful** except the 53% attribution (T6). (A1, editor)

---

## 8. Recommended handling paths

- **Path B (preferred) — downgrade to Computational Biology / Methods & Resources (or Application Note).** Recategorize the contribution as a reproducible, auditable pipeline + honest external validation + experimental blueprint. A4 supplies a paste-ready title, ~250-word abstract skeleton, and section-structure plan. This converts the manuscript's transparency assets into the selling point and removes the discovery-overclaim risk. *Viable only if the target journal has such a category.*
- **Path A (fallback, universal) — headline-swap within the Research type.** Keep the article type; change title to "Confirmation and external validation of the MARS Mars1 immunoparalysis program …"; lead the abstract with "confirm/replicate" and "null MR / hypothesis-generating"; add "replication"/"external validation" to keywords; drop "dissection" as a discovery verb. Removes the internal contradiction without reclassification.
- **Path C — wording-only without reframing — NOT viable.** Leaving the discovery title while the Discussion concedes near-replication is the exact self-contradiction the panel's firewall is designed to catch; it would persist the largest acceptance risk.

**Editor's synthesis (reframe, don't just criticise):** The manuscript's *strongest* real finding — an endotype-anchored, fully-traceable analytical pipeline that honestly confirms a known program and validates a signature out-of-sample — is currently buried under its *weakest* headlined claim (novel hub-gene discovery + drug repositioning). Swapping the two (Path A or B) converts the paper from a fragile discovery into a stable methodological/transparency contribution. This is not the author's fault: aggregate-layer opacity and the structural near-duplication of the published MARS program are properties of the evidence base, not errors in execution.

---

## 9. Process lessons

- **A gate passing at 100% is evidence about arithmetic, not about framing.** The 18/18 audit was green, yet the panel's most important finding (T1) is a *framing* defect the gates cannot see. This is the recurring lesson: gates verify provenance; they do not verify whether the headline matches the contribution.
- **The "second-occurrence goes stale" rule now extends to conceptual second-occurrences.** Round-9's assertion #18 closed the numeric Egger-staleness gap; Round-10 shows the *conceptual* staleness remains — Conclusion says "anchored by hub genes" while Discussion says "near-replication." A new assertion should check that the headline/Conclusion discovery强度 matches the Discussion's own concession (e.g., grep for "novel"/"discovery"/"isolated" in title+abstract+conclusion and require a "near-replication"/"confirmation" hedge within N words).
- **Article-type is a design-layer judgement the panel must make fresh.** Re-feeding a prior round's downgrade suggestion would have biased A4; by posing it from the manuscript's own text, A4 reached the reframe recommendation independently and consistently with A3's D4 and A2's framing items.
- **New assertions to extend gate coverage to the design/framing layer:** (i) title/abstract/Conclusion must not use discovery verbs ("dissection", "novel", "isolated") without a near-replication hedge; (ii) calibration slope reported as "well behaved" only if |slope−1| < 0.1; (iii) "MR is null" only if zero family-significant AND no direction-reversed family-significant signal; (iv) any cited trial percentage attributed to the correct algorithm (ferritin + mHLA-DR, not mHLA-DR alone).

---

*Panel files:* `review_r10/_PANEL_BRIEF.md`, `review_r10/A1_domain.md`, `review_r10/A2_design_stats.md`, `review_r10/A3_implementation.md` (+ `A3_recompute.py`, `A3_recompute_log.txt`), `review_r10/A4_venue_reporting.md`.
