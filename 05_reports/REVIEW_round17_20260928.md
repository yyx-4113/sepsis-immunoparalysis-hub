# Round-17 consolidated independent blind review — v1.17.0

**Date:** 2026-09-28 · **Manuscript:** `05_reports/manuscript.md` (tag v1.17.0, commit 5e1af29) · **Target venue:** *Scientific Reports* (Nature Portfolio)
**Panel:** A1 domain (sepsis immunology) · A2 design (statistics / causal inference) · A3 implementation (provenance / recompute) · A4 venue (Sci Rep compliance / desk-reject)

---

## 1. Independence statement

Each expert received a shared brief (`05_reports/review_r17/_PANEL_BRIEF.md`) forbidding, by explicit filename, all prior-round material: `REVIEW_round*.md`, `review_r2/`–`review_r16/`, `.workbuddy/memory/*`, `scirep_submission_checklist.md`, and every other `review_r17/*` file besides the brief. Each was instructed to treat the manuscript as a **first submission** and to verify independently any claim it could verify. All four experts restated the forbidden-file list in their own reports and confirmed non-access.

**Evidence that independence actually worked** — findings that clustered across experts who could not see each other:

| Defect | A1 | A2 | A3 | A4 | independent hits |
|---|---|---|---|---|---|
| FIS1 folded into "concordant with the immunoparalysis model" | (a) | Issue 6 | Q1 | — | **3** |
| §8 MR diagnostic figure index | (e) | Issue 7 | Issue 2 | Q4 | **3** (see §5 adjudication) |
| Reference [31] trailing period after DOI | — | Issue 8 | Issue 3 | Item 2 | **3** |
| MR "no causal support" headline understates results | — | Issue 4 | Q4 | Item 5 | **2** |
| DCA threshold-0.80 framing | — | Issue 1 | Issue 6 | — | **2** |
| "Reduced checkpoint engagement" over-read | (b) | Issue 8 | — | — | **2** |
| Missing standalone Code availability heading | — | Issue 8 | Issue 4 | Item 4 | **2** |

Two clusters are notable: the FIS1 mis-framing was hit by three experts from three different angles (biological incoherence, causal-direction logic, provenance question), and the §8 figure index by three. That convergence from disjoint starting points is the signature of real independence.

---

## 2. Verdict table

| Expert | Layer | Verdict | Desk-reject? | Central question |
|---|---|---|---|---|
| A1 | Domain | **Major** | no | Is the biology coherent and clinically plausible? |
| A2 | Design | **Major** | no | Is the statistical / causal reasoning sound? |
| A3 | Implementation | **Minor** | no | Does every headline number trace to a deposited source? |
| A4 | Venue | **Minor** | **none** | Is it Sci Rep compliant / desk-reject free? |

**Distribution: 2 Major, 2 Minor, 0 desk-reject.** Consolidated recommendation: **Major revision (Path A — revise and resubmit as the same article type)**.

**Adjudication of the split (not averaged).** A3's Minor is explicitly self-limited — "does every headline number trace to a deposited source file" — and it answers that question **yes**, with ten independently recomputed values all matching. A4's Minor is likewise scoped to format compliance. A self-limited scope is an honest reason for a lenient verdict, but it certifies a *layer*, not the manuscript. A1 and A2 were asked unrestricted questions and each found defects that change how a reader should interpret the Discussion's stated contributions. **The stricter verdict is adopted.**

---

## 3. Cross-verification table

Every value below was recomputed by at least one expert from source CSVs. Rows marked **[editor]** were additionally re-derived by me directly from raw files, independently of any reviewer intermediate.

| # | Manuscript location | Manuscript claims | Independently recomputed | Who | Verdict |
|---|---|---|---|---|---|
| 1 | §3.5, §4, Abstract | External AUC 0.638 (95% CI 0.532–0.748; n=106; 52 deaths) | 0.6382; CI 0.5317–0.7475; n=106, deaths=52 | A2, A3, A4 **[editor]** | ✅ match |
| 2 | §3.1 | 23/25 down, 22 significant, 21 both | 23 down; 22 adj.P<0.05; 21 both | A1, A3 | ✅ match |
| 3 | §3.2 | Mars1 vs M2/M3/M4 P = 0.47 / 1.9e-18 / 1.3e-3 | 0.467 / 1.85e-18 / 1.32e-3 | A2, A3 | ✅ match |
| 4 | §3.3, §4 | FIS1 logFC +1.26 (t ≈ 17.2), up-regulated | 1.2614; t = 17.16 | A1, A2, A3 **[editor]** | ✅ match — **but conclusion drawn from it is wrong** (see #8) |
| 5 | §3.9 | lenalidomide rank 5,435 (26.6%); azithromycin 9,152 (≈median) | 5435/20413 = 26.6%; 9152/20413 = 44.8% | A1, A2, A3, A4 | ✅ match — **but used as support despite #6** |
| 6 | §3.9 | prednisone 3.2nd percentile; dexamethasone 33.4th | rescue 0.136 rank 651; 0.032 rank 6808 | A2 **[editor]** | ✅ match — **invalidates axis as support metric** |
| 7 | §3.10 | MR IVW OR 0.92–1.12, all P ≥ 0.23 | CD74 1.119, HLA-DQA1 0.923, CD14 0.927, HAVCR2 0.978, FIS1 0.963; min P 0.2359 | A1, A2, A4 **[editor]** | ✅ match |
| 8 | §3.10, §4, Lim. 2 | "three of five (HLA-DQA1, CD14, **FIS1**) … concordant … the direction predicted by the immunoparalysis model" | FIS1 IVW OR 0.9635 (P=0.473); Egger 0.9638 (P=0.491); WM 0.9712 (P=0.768) — protective but **opposite** to FIS1's observational up-regulation | A1, A2, A3 **[editor]** | ❌ **logical error** — FIS1 not model-concordant |
| 9 | §3.5 | DCA at thr 0.80: model NB 0.00 vs treat-all −1.55, "widens rather than converges" | grid: 0.80 → 0.0 / −1.5472; treat-all NB = 0.4906 − 0.5094·t/(1−t) = −1.547 (pure algebra); model NB = 0 also at 0.85, 0.90 | A2, A3 **[editor]** | ⚠️ **numbers right, framing wrong** |
| 10 | §3.5 | Calibration slope 0.50 / intercept −0.04 | 0.5028 / −0.0382, n=106, no CI column | A2, A3, A4 | ✅ match — **but test-set-nested, undisclosed** |
| 11 | §3.10 | CD14 MR-Egger OR 0.906, P = 0.049 | 0.90595; P = 0.048809 | A2, A4 **[editor]** | ✅ match — **omitted from Abstract** |
| 12 | §3.10 | CD74 critical-care WM OR 2.194, family q ≈ 3e-17, reversed | 2.194; q_family = 2.99e-17 | A2, A4 | ✅ match — **omitted from Abstract** |
| 13 | §3.10 | 27 instruments: 3/4/6/6/8 | 27 rows; CD74 3, HLA-DQA1 4, CD14 6, HAVCR2 6, FIS1 8 | A3 | ✅ match |
| 14 | §7 / Data avail. | commit 1212f7b is tagged v1.16.0; v1.17.0 built on top | `git rev-parse v1.16.0` = 1212f7be…; `v1.17.0` = 5e1af29, direct descendant | A3 **[editor]** | ✅ match |
| 15 | §8 | "MR diagnostic set (forest, scatter, funnel, leave-one-out)" | `04_figures/`: only `mr_forest.png`, `mr_diag.png` | A1, A2, A3 **[editor]** | ⚠️ **figures exist — as panels inside `mr_diag.png`; index wording is ambiguous, not a phantom** |

**No arithmetic discrepancy was found anywhere.** Every numeric defect is an *interpretation or framing* defect built on correct numbers — which is exactly the class a green audit gate cannot catch.

---

## 4. Editor's independent verification of the most severe findings

Per panel discipline, I did not forward the most severe findings unexamined.

### (i) §8 "phantom MR figures" — **demoted: the figures exist; the wording is at fault**

Three experts independently reported that §8 names four MR diagnostic plots while `04_figures/` holds only two PNGs. Before accepting this, I read the generating script `02_scripts/python/_mr_diagnostics.py`:

- L93 → `fig.savefig(..., "mr_forest.png")` — the 45-test forest.
- L103 → `plt.subplots(2, 2, ...)`, and L144 → `fig.savefig(..., "mr_diag.png")`, with panels built at:
  - `ax[0,0]` (L106–111) — **CD14 28-day-death scatter** with IVW and Egger fits
  - `ax[0,1]` (L115–120) — **CD14 Egger funnel**
  - `ax[1,0]` (L130–134) — **CD14 leave-one-out IVW**
  - `ax[1,1]` (L137–142) — **CD74 critical-care scatter**

So the scatter, funnel and leave-one-out plots **do exist** — as three panels of the single composite `mr_diag.png`, consistent with the body text at L176. The experts' finding is therefore a **false positive on file existence**, produced by an index that reads as a list of separate files. It nonetheless exposes a real defect: the §8 index is ambiguous, and three qualified readers all mis-read it. Fix = disambiguate §8 (Tier 2), no file generation needed. **Not a Major item, and not a desk-reject risk.**

### (ii) FIS1 "concordant with the immunoparalysis model" — **confirmed genuine**

I re-read the FIS1 row of `S01_mars1_deg.csv` directly: `1.2614331467372244, 17.156684530047006, 0.0, 0.0, True, True, FIS1` → logFC **+1.261** (up). And `10_genetics_mr_outcome5086_28ddeath.csv`: FIS1 IVW OR 0.9635 (P = 0.473), Egger 0.9638 (P = 0.491), WM 0.9712 (P = 0.768) — all protective, all non-significant.

The logic in the manuscript is therefore inverted: for the four **down**-regulated immune hubs, "higher expression → lower death" is coherent with the immunoparalysis model; for FIS1, which is **up**-regulated in the high-mortality Mars1 endotype, the same protective direction *contradicts* its observational association. Calling it "the direction predicted by the immunoparalysis model" is a stated-result error, not a wording preference. **Confirmed; Tier 1.**

### (iii) DCA threshold-0.80 — **confirmed genuine**

Recomputed from `09_ext_dca_grid.csv` (read directly): 0.80 → `nb_model = 0.0`, `nb_treat_all = −1.5472`; and `nb_model` is **also 0.0 at 0.85 and 0.90**. So above 0.80 the model recommends treatment for nobody and is numerically identical to the treat-none baseline. A2's algebra holds: with prevalence 52/106 = 0.4906, treat-all NB = 0.4906 − 0.5094·(0.80/0.20) = −1.547, i.e. the −1.55 is a property of the formula and the prevalence, not of the model. The genuine model advantage is the 0.30–0.75 band, where margins are ≤0.04 NB in the 0.30–0.50 range. **Confirmed; Tier 1.**

---

## 5. Graded consolidated issue list

### Tier 0 — conclusion-invalidating
*None.* No expert found a fabricated number, a false headline, or a desk-reject trigger.

### Tier 1 — must fix before acceptance (analyses restated or claims re-scoped)

| ID | Location | Problem | Evidence | Fix |
|---|---|---|---|---|
| **T1.1** | §3.10 L149, §3.10 L176, §4 L186, Lim. 2 L195 | FIS1 — an **up**-regulated non-immune passenger — is counted among hubs "concordant … the direction predicted by the immunoparalysis model" | logFC +1.261; MR OR 0.9635/0.9638/0.9712 (protective, opposite to observational direction) | Re-scope to "two of the four assessable immune hubs (HLA-DQA1, CD14)"; report FIS1 separately as a passenger-gene observation whose direction is **not** predicted by the model. Apply at **all four** sites. |
| **T1.2** | §3.5 L112 | DCA "widens rather than converges" at thr 0.80 presents a formula artefact as a model win | grid 0.80 → 0.0 / −1.5472; treat-all NB = prevalence − (1−prev)·t/(1−t); model NB = 0 also at 0.85/0.90 | Restrict the advantage claim to the 0.30–0.75 band (margins ≤0.04 NB at 0.30–0.50); state that at ≥0.80 the model ties treat-none because no calibrated risk exceeds the threshold. |
| **T1.3** | §3.5 L112 | Calibration slope/intercept fitted **on the same external test set** (n=106/52) that the DCA is computed on; optimism undisclosed | `09_ext_calibration_dca.csv` single row, n=106, deaths=52, no CI | Disclose explicitly: calibration-corrected DCA is optimistically biased and illustrative; slope on n=106 is itself noisy. |
| **T1.4** | §3.9 L142 vs §4 L186 / §6 L218 | Internal contradiction: prednisone (a clinical immunosuppressant) scores 3.2nd percentile on the rescue axis, refuting the axis — yet lenalidomide/azithromycin ranks are still cited as **supportive** | prednisone rescue 0.136 rank 651; lenalidomide 5435 (26.6%), azithromycin 9152 (44.8%) | Demote the two small-molecule L1000 ranks from supportive to **descriptive only**, wherever cited, and say why: the same metric that ranks an immunosuppressant in the top 3% cannot support compounds on the same axis. |
| **T1.5** | Abstract L14 | "no causal support on the primary 28-day-death outcome" understates two surviving results | CD14 Egger OR 0.906 P = 0.0488; CD74 critical-care WM OR 2.194 q = 2.99e-17 (reversed) | Restate: no significant **IVW** estimate on the primary outcome (OR 0.92–1.12, P ≥ 0.23); one Egger nominally significant; one family-significant result reversed → hypothesis-generating. |
| **T1.6** | Article-type L8, Abstract L14, §3.5 heading L111, §4 L184 | "honest **independent** external validation" — independence is only in cohort and platform, not in label | §3.5: "orientation was trained on GSE65682 28-day labels" | Qualify every headline occurrence: "independent in cohort and platform; orientation fixed on discovery 28-day labels, so not label-independent". |
| **T1.7** | §3.1 L72, §4 L182 | "reduced checkpoint engagement" is a per-cell functional claim drawn from bulk data that cannot separate cell-loss from per-cell down-regulation | bulk caveat exists in §3.1 but the headline is stated as a positive read-out; §4 states it more firmly | Downgrade to "net lower bulk HAVCR2/TIM-3 expression, compatible with — not establishing — reduced per-cell engagement", and carry the §3.1 caveat into §4. |
| **T1.8** | §3.1 L72, §4 L182 | The TIM-3-down vs "canonical TIM-3-up exhaustion" contrast cites **no** opposing sepsis literature and does not reconcile it | only citation in the passage is Hotchkiss [3] (for PD-1, not TIM-3) | Cite the sepsis TIM-3 literature and reconcile explicitly — including the sepsis studies reporting TIM-3 **down**-regulation in PBMC, which is directionally consistent with this bulk result. |

### Tier 2 — wording / reporting precision

| ID | Location | Problem | Fix |
|---|---|---|---|
| T2.1 | Ref [31] (L312) | Stray trailing period after the DOI — the only one of 37 entries | Remove |
| T2.2 | after §Data availability | No standalone `## Code availability` heading (Sci Rep expects one) | Add, naming tag v1.18.0 and the MIT licence |
| T2.3 | §3.2 L92 | "Table:" is unnumbered while four siblings are numbered | Renumber → Table 2; shift 2→3, 3→4, 4→5; update all in-text cross-references |
| T2.4 | Lim. 2 L195 | 45-test BH called a "conservative approximation" despite overlapping hypothesis structures | "a dependence-ignoring approximation" |
| T2.5 | §8 L257 | MR figure index reads as four separate files but they are panels of `mr_diag.png` | Name the files and enumerate the panels |
| T2.6 | Table 1 L82 | Escaped-pipe token `\|logFC\|` inside a table cell | Render as `\|logFC\| ≥ 0.3` in code formatting |
| T2.7 | Abstract L14 | 196 words — only 4 below the 200 cap; T1.5 adds words | Compress elsewhere to keep a safe margin (target ≤190) |

### Tier 3 — deferred
None carried forward.

---

## 6. Consensus / complementarity / disagreement

**Consensus (all four agree).** No fabricated or unverifiable number; the external-validation magnitude is reported without inflation; the MR layer is honestly self-labelled hypothesis-generating; provenance and commit/version self-consistency hold; no desk-reject hard-fail. A1: "unusually honest and well-scoped". A3: "every headline number traces exactly to a real deposited source file". A4: "no desk-reject hard-fail".

**Complementarity.** A3 and A4 independently certified the *substrate* (numbers, provenance, format) while A1 and A2 attacked the *interpretation* built on it. Neither pair's findings would have been found by the other: A4's format screen cannot ask whether FIS1's direction makes biological sense, and A1's biology screen cannot check whether treat-all NB at thr 0.80 is pure algebra.

**Disagreement 1 — severity of the §8 figure item.** A3 called it the single most severe finding and flagged that it becomes Major if Sci Rep enforces deposited-figure completeness; A1 and A2 listed it as minor. **Ruling: A3 is right about the risk but wrong about the fact.** I read the generating script (§4.i): the panels exist inside `mr_diag.png`. The item is demoted to Tier 2 wording. The disagreement is preserved because it documents a real reader-comprehension failure that must be fixed even though no file is missing.

**Disagreement 2 — is the MR headline an understatement (A2, A4) or acceptable (A3, A1)?** A1 explicitly noted it had *suspected* understatement and found the manuscript clean; A3 recommended keeping the wording as accurate for primary IVW. A2 and A4 said it omits the CD14 Egger and CD74 reversed results. **Ruling: adopt the stricter reading (A2/A4).** "No causal support" is true of IVW only, and the Abstract is the one place a reader will not see the body-text nuance. Cost of compliance is one clause. This is a rare case where the fix makes the claim *more* informative rather than weaker — it is the mirror image of T1.2, and fixing both is what makes the paper internally consistent.

**Disagreement 3 — Table 1 `\|logFC\|`.** Round-15 (prior panel) judged the inline escaped pipe acceptable because markdown prose renders it literally; A3 raises rendering fragility. **Ruling: adopt the conservative reading.** Compliance cost is near zero and the cell is central to the provenance story.

---

## 7. Priority must-fix list

**Must restate (no new analysis required):** T1.1 (4 sites), T1.2, T1.3, T1.4 (3 sites), T1.5, T1.6 (4 sites), T1.7 (2 sites), T1.8 (2 sites + 1 new reference).
**Must reword (Tier 2):** T2.1–T2.7.
**Must add analysis:** none. No expert required new data, new computation, or a new cohort.
**DESK-REJECT flags:** none.

**Single-source-of-truth requirement.** T1.1 appears at four sites and T1.6 at four; they must all change together. The last round's lesson applies: a caveat added in one place while the headline stands elsewhere is a fresh P0.

---

## 8. What stands up — do not change these

1. **Every recomputed number matches its source** (13 independent recomputations in §3, plus 10 by A3). No data-integrity defect.
2. **Commit/version provenance reconciles:** v1.16.0 == 1212f7b; v1.17.0 (5e1af29) is its direct descendant.
3. **The MR "no primary IVW significance" result is honest**, and the CD74 critical-care reversal plus CD74/Egger SE ordering are disclosed in the body — A1 specifically suspected over- or under-statement here and cleared it.
4. **The L1000 glucocorticoid caveat is genuinely constraining** and correctly used to bound the evidence; only its *downstream* reuse as support is inconsistent (T1.4).
5. **Drug-shortlist concordance fractions and mechanism anchors are faithful to source**, with ImmunoSep used correctly as a caution (no mortality benefit, more haemorrhagic events).
6. **Format compliance:** title 17 words, abstract non-structured and citation-free, all eight mandatory statements present, 5 main-text tables ≤ 8 budget, 37 references all with DOIs.

---

## 9. Recommended handling path

**Path A — revise and resubmit as the same article type.** No path change is warranted: the article-type downgrade (v1.10.0) already matched the claim to the evidence, and nothing in this round suggests the framing is still inflated. What remains is a **consistency** problem, not a scope problem: the body text is more careful than the Abstract and Discussion headlines, and one stated result (FIS1) has inverted logic.

---

## 10. Process lessons

- **The gate's blind spot is interpretation, not arithmetic.** All 32 audit assertions were green at v1.17.0 and every number in the manuscript is correct — yet the round found eight Tier-1 items. The defect class is "true numbers, wrong conclusion", which only hypothesis-generating review catches.
- **Three experts can be wrong in the same direction.** The §8 finding looked overwhelming (3/4 experts) and was still a false positive. Multi-expert convergence raises confidence but does not replace reading the generating artefact.
- **New guard-worthy assertions suggested by this round:** (a) FIS1 must never co-occur with "concordant"/"predicted by the immunoparalysis model"; (b) the DCA text must state the 0.30–0.75 window and must not claim advantage at ≥0.80 without tying to treat-none; (c) "independent" must not appear unqualified next to "external validation"; (d) any L1000 rank cited as support must be accompanied by the prednisone refutation; (e) §8's figure index must name the two PNG files.

---

## 11. Note to the author

The strongest claim that does not hold is the **FIS1 concordance** — and its failure is not really your fault: it is what happens when a passenger gene is carried along inside a hub set and then inherits the hub set's interpretive language. The gene is correctly measured and correctly labelled everywhere else in the paper; only this one sentence borrows a direction that belongs to the down-regulated hubs.

The finding you buried is the **DCA/calibration honesty problem**. Your calibration slope of 0.50 is *already* disclosed, and your DCA grid is deposited — but the headline "widens rather than converges" sells an algebraic artefact. Correcting it to "positive net benefit only in the 0.30–0.75 band; tied with treat-none above 0.80; calibration fitted on the test set, therefore illustrative" converts a weak, defensible result into an unattackable one. This is the same move that fixed the MR Egger p-value: the honest version is more citable than the flattering one.

Swapping those two — dropping the borrowed FIS1 direction, and owning the DCA window — is what turns the Discussion from "three fragile signals" into "one stable methodological contribution with correctly bounded clinical utility".
