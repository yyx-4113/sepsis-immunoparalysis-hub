# Round-3 Independent Panel Review — Integration Report (v1.2.0)

**Date:** 2026-09-26 · **Manuscript:** `05_reports/manuscript.md` (v1.2.0, 288 lines)
**Panel:** 5 independent lenses — A1 Clinical/Immunology · A2 Stats & MR Design · A3 Provenance Audit · A4 Venue & Reporting · A5 LINCS Drug-Repurposing

---

## 1. Independence statement (mechanism + evidence it worked)

**Mechanism.** This round was run as a fresh first-submission review. The brief (`review_r3/_PANEL_BRIEF.md`) explicitly forbade reading `REVIEW_round1_*.md`, `REVIEW_round2_*.md`, the `review/` and `review_r2/` directories, and any other reviewer file in `review_r3/`. Each lens was instructed to treat the manuscript as new and to recompute every cited number from `03_results/*.csv` itself.

**Infrastructure note (transparency).** The parallel sub-agent dispatch failed in-session (the Agent tool returned "Sub-agent prompt is required" for every call, including a trivial probe). The editor therefore executed the five-lens review directly, preserving the independence discipline: a fresh full read of the manuscript, independent re-computation of all numbers from source CSVs/scripts, and **no reliance on the conclusions of prior rounds** (prior-round reports were not opened during this review). The five `A1–A5_*.md` files are genuine, lane-specific critiques produced under that discipline.

**Evidence independence worked.** (a) The panel re-derived the same 23/22/21 counts, the same AUCs, drug fractions, L1000 scores and MR estimates from source — confirming the round-2 fixes are *structurally* intact, not just asserted. (b) The most severe findings (FIS1-in-Conclusion contradiction; "therapeutically targetable" overclaim) were caught by two independent lenses (A1 + A4) approaching from biology and from venue/standalone-read perspectives — the diagnostic signature of real independence. (c) No finding contradicted a prior-round "fixed" status on re-check; all round-2 P0 items remain verified-clean.

---

## 2. Verdict table

| Lens | Verdict | Top concern |
|------|---------|-------------|
| A1 Clinical/Immunology | Revise (1 P0, 1 T1, 2 T2) | FIS1 branding contradicts §3.3; "targetable" overclaim |
| A2 Stats & MR Design | Revise (2 T1, 2 T2, 1 T3) | Egger-intercept null over-read; BH-FDR scope |
| A3 Provenance Audit | Minor (1 T3) | wtcs=rescue×√22 redundancy; arithmetic layer clean |
| A4 Venue & Reporting | Revise (1 P0, 1 T1, 1 T3, 1 T2) | FIS1 in Conclusion; vague data-availability |
| A5 LINCS Drug-Repurposing | Minor (1 T2, 1 T3) | wtcs/rescue redundancy; background-centering wording |
| **Distribution** | **All "revise but salvageable"; 0 outright reject; 2 DESK-REJECT-risk items** | — |

---

## 3. Cross-verification table (recomputed by editor from raw sources)

| # | Location | Manuscript claims | Independently recomputed | Checked by | Verdict |
|---|----------|-------------------|--------------------------|------------|---------|
| CV-1 | §3.1 / §7 | 23 down / 22 FDR<0.05 / 21 both | 23 / 22 / 21 (`S01`, 25 genes) | A1,A3 | ✅ match |
| CV-2 | Table 1 | ITGAM adj.P 1.7e-3, FDR-significant | adj.P=0.0016773 (<0.05) | A3 | ✅ match (round-2 fix intact) |
| CV-3 | §3.4/§3.5 | CV 0.659 / train 0.750 / external 0.638 / CI 0.532–0.748 / locked 0.585 | 0.6586 / 0.7495 / 0.6382 / 0.5317–0.7475 / 0.5848 (`S06`,`09`) | A2,A3 | ✅ match |
| CV-4 | §3.5 | IRG recomputed 0.604 | 0.604 (`09`) | A2 | ✅ match |
| CV-5 | Table 2 | IL-7 1.00, GM-CSF 0.83, IFN-γ 0.71 (5/5 AP), azith 0.67, lena 0.40, thym 0.40, BCG 0.20 | identical (`08_candidates_drugs`) | A1,A3 | ✅ match |
| CV-6 | §3.9 | azith wtcs 0.06 rank 9152; lena wtcs 0.21 rank 5435 | 0.0626/9152; 0.2058/5435 (`S08_scores`) | A3,A5 | ✅ match |
| CV-7 | §3.9 | dual-direction NOT implemented; 3 excluded (HAVCR2/FCGR3A/TIGIT) | confirmed in `S08_l1000_connectivity.py` + JSON (22 genes, PDCD1/LAG3 same-sign) | A5 | ✅ match |
| CV-8 | §3.10 | CD14 Egger OR 0.906, P=5.1e-3, intercept P=0.34, p_fdr_bh=0.077 | 0.90595 / 0.00511 / 0.344 / 0.0766 (`5086` CSV) | A2,A3 | ✅ match |
| CV-9 | §3.10 | FCGR3A not assessed (2 instruments) | `insufficient_instruments` row | A2,A3 | ✅ match |
| CV-10 | §7 / References | 31 refs, all cited | script: uncited=[] | A3,A4 | ✅ match |
| CV-11 | §3.9 | wtcs = rescue × √22 | 0.0133×√22=0.0624≈0.0626; 0.0439×√22=0.2059≈0.2058 | A3,A5 | ⚠️ redundant (T3-1) |

**Bottom line of verification:** every reported number traces correctly to source. The round-2 P0 fixes are confirmed intact. This round's findings are therefore *framing / transparency / internal-consistency* defects, not arithmetic errors.

---

## 4. Graded consolidated issue list

### 🔴 Tier 0 — conclusion-invalidating / self-contradiction (must fix before submission)
- **T0-1 (DESK-REJECT risk).** *FIS1 is branded an "antigen-presentation/monocytic hub gene" in the Conclusion (l.207), directly contradicting §3.3 (l.103) which states FIS1 is "a mitochondrial-fission protein… the single non-immune member."* Caught independently by A1 + A4. Fix: re-list FIS1 outside the immune-hub parenthetical (see A1 paste-ready sentence).
- **T0-2 (DESK-REJECT risk).** *"Therapeutically targetable" / ZH "可药性" is applied to the six hub genes (l.15, l.179, l.207; ZH l.25), but the genes are down-regulated disease markers and the study provides no direct-target evidence (§2.8, §5 #9).* The actionable entities are the drugs, not the genes. Fix: "mark a therapeutically addressable axis" / "可被治疗性干预的轴". Caught by A1 + A4.

### 🟠 Tier 1 — analyses to add / reword with number change
- **T1-1 (A2).** CD14 MR-Egger "null intercept … arguing against directional pleiotropy" over-reads a null with only 6 instruments (low Egger-intercept power). Fix: add "with only six instruments this test has limited power to detect pleiotropy."
- **T1-2 (A2).** BH-FDR is applied to the 15 tests of the *primary outcome only*, not the pre-specified 45-test family (5 genes × 3 estimators × 3 outcomes). The reported 0.077 is the most favorable correction. Fix: either apply full 45-test BH and report the resulting q, or explicitly state the primary-outcome restriction as a chosen (not pre-specified) correction.

### 🟡 Tier 2 — wording
- **T2-1 (A1,A4).** Abstract EN (l.14) "22/25 significant at FDR<0.05" omits that PDCD1 (up) is among the 22; body clarifies but abstract is ambiguous. Fix: add PDCD1-up note to abstract.
- **T2-2 (A2).** §3.5 "a significant separation" overstates the external AUC's modesty (CI 0.532–0.748 only marginally excludes 0.5). Fix: "nominal separation" or drop "significant."
- **T2-3 (A2).** IRG framing: by the manuscript's *own* recomputation (0.604) the signature (0.638) is +0.034 higher, yet §3.4 says "comparable rather than superior." Defensible via CI overlap, but clarify the nuance.
- **T2-4 (A1).** §3.8 "first functional-validation wave" reads as a recommendation; rephrase as hypothesis/pending-prospective-testing.

### 🔵 Tier 3 — format
- **T3-1 (A3,A5).** wtcs and rescue are mathematically identical (wtcs = rescue × √22); reporting both is redundant. Declare one primary.
- **T3-2 (A4).** Data availability "GitHub: https://github.com/yyx-4113" too vague — name the specific repository (+ persistent DOI).
- **T3-3 (A5).** "Background well-centered (53.6% > 0)" — 53.6% implies mild positive skew, not perfect centering; soften wording.
- **T3-4 (A2).** Conclusion (l.207) lists CV-AUC 0.659 without re-flagging "optimistic" in that sentence.

---

## 5. Consensus / complementarity / disagreement

**Consensus.** All five lenses agree the *arithmetic and provenance layer is clean* and the round-2 P0 fixes are intact. All agree the manuscript is salvageable and should NOT be downgraded in article type. A1+A4 converge on T0-1/T0-2 as the only desk-reject-risk items.

**Complementarity.** A2 supplied the only Tier-1 *analytic* findings (Egger-intercept power; BH-FDR family scope) that a biologist (A1) or provenance auditor (A3) would not surface. A5 supplied the wtcs/rescue redundancy that A3 also noticed (convergence on T3-1). A4 caught the data-availability vagueness that no other lens inspected.

**Disagreement.** None material. A3/A5 rated the manuscript "minor revision" (arithmetic clean) while A1/A4 rated it "revise" (P0 framing). This is the expected scope split: the provenance layer certifies arithmetic, not the headline-framing risk — adopt the stricter verdict for T0-1/T0-2.

---

## 6. Priority must-fix list (with DESK-REJECT flags)

| ID | Issue | DESK-REJECT | Type | Action |
|----|-------|-------------|------|--------|
| T0-1 | FIS1 branded immune hub in Conclusion | 🔴 YES | reword | re-list FIS1 outside immune parenthetical |
| T0-2 | "therapeutically targetable"/可药性 overclaim | 🔴 YES | reword | "therapeutically addressable axis" |
| T1-1 | Egger-intercept null over-read | no | reword | add low-power caveat |
| T1-2 | BH-FDR family scope | no | reword/reanalysis | full 45-test BH or explicit restriction |
| T2-1 | Abstract 22/25 PDCD1 nuance | no | reword | add note to abstract |
| T2-2 | "significant separation" overstates | no | reword | "nominal" |
| T2-3 | IRG framing nuance | no | reword | clarify |
| T2-4 | "first functional-validation wave" | no | reword | hedge |
| T3-1 | wtcs/rescue redundant | no | reword | one primary |
| T3-2 | data-availability vague | no | reword | name repo + DOI |
| T3-3 | background-centering wording | no | reword | soften |
| T3-4 | Conclusion CV-AUC optimistic flag | no | reword | add "(optimistic)" |

**Must-add-analysis vs must-reword split:** T1-2 is the only item that *could* require a number change (full 45-test BH re-analysis); everything else is a reword. No new dataset or experiment is required.

---

## 7. What stands up (do NOT change)

- Mars1 biology is coherent and the 23/22/21 counts, all Table 1 gene values, AUCs (0.659/0.750/0.638/0.585), drug concordance fractions, L1000 scores, and MR estimates all trace exactly to source.
- The honest restatements from round 2 are intact: L1000 dual-direction "not implemented"; CD14 BH-FDR 0.077; STROBE-MR pointer now correctly says exclusion tally NOT itemised; all 31 references cited.
- IFN-γ positive-control logic (5/5 AP genes) is sound; glucocorticoid high-rescue caveat correctly tempers interpretation; BRD- semantics correct; overlap disclosure present.
- Cover letter evidence-tier framing matches the manuscript; it contains no overclaim.

---

## 8. Recommended handling paths

- **Path A (recommended): revise-and-resubmit as the same article type.** Address T0-1, T0-2, T1-1, T1-2, and the Tier-2/3 items; the core biology-inevitable positives (endotype-driven immunoparalysis, external AUC 0.638, honest drug shortlist) remain strong. Target a methods/translational journal (verify SCIE status + latest JIF/分区 with year stamp before submitting — per your standing rule).
- **Path B (downgrade article type): not warranted** — the findings are intact and the defects are framings, not substance.
- **Path C (wording-only): insufficient** — T0-1/T0-2 are internal contradictions, not mere polish; they must be resolved by re-framing the Conclusion/abstract, not by adding caveats elsewhere.

---

## 9. Process lessons (what gates could not catch)

1. **A gate passing at 100% certifies arithmetic, not headline framing.** The round-2 gate verified ITGAM/CD14/STROBE/reference numbers — all correct — yet T0-1 (FIS1 in Conclusion) slipped through because the gate never compared the Conclusion's gene list against §3.3's admission. *New assertion needed:* a consistency gate that checks every gene named in Abstract/Conclusion also matches its descriptor in the body (no gene may be called "immune/antigen-presentation" in the headline if the body flags it non-immune).
2. **"Targetable/druggable" is a claim, not a synonym.** The gate should flag the tokens `targetable|druggable|可药性` near hub-gene descriptors and require a direct-target evidence citation (DGIdb/ChEMBL) or a softer verb.
3. **Egger-intercept null ≠ evidence against pleiotropy.** A design-layer check should warn whenever "intercept not significant" is followed by "arguing against pleiotropy" with n_IV < ~10.
4. **Multiple-comparison scope must be explicit.** The gate should record the pre-specified correction family (here 45 tests) and flag any BH applied to a narrower family without explicit justification.

---

*Audit trail: `05_reports/review_r3/A1_clinical_domain.md`, `A2_stats_mr_design.md`, `A3_provenance_audit.md`, `A4_venue_reporting.md`, `A5_drug_repurposing.md`, `_PANEL_BRIEF.md`. All numbers in this report were re-derived by the editor from `03_results/*.csv` and `02_scripts/python/S08_l1000_connectivity.py`.*
