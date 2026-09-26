# A4 — Venue & Reporting-Standard Lens (blind)

**Mandate:** audit reporting-checklist honesty (TRIPOD / STROBE-MR), format hard-fails, cover-letter vs manuscript mismatches, internal coherence of the revision.

## Tier 2

### A4-T2-1. §3.10 is internally incoherent about CD74 critical-care significance.
【Problem】 Within the same section, the manuscript both (a) reports CD74 critical-care in detail (IVW OR 2.222, P=0.014; MR-Egger 2.222 null intercept; WM 2.194) and (b) asserts it "fails correction across all 15 tests (FDR≈0.21)" and that "no estimate reached q<0.05" under the 45-test family. A reader cannot reconcile "we report OR 2.222, P=0.014, null intercept" with "it fails correction / nothing survives." The data file shows it strongly *survives* correction (p_fdr_bh 4.97e-12). This internal contradiction is visible without opening the CSV.
【Evidence】 §3.10 l.159 ("Against critical care, CD74 was nominally significant … P=0.014") vs l.171 ("fails correction across all 15 tests (FDR ≈ 0.21)") vs l.146/173 ("no estimate reached q<0.05").
【Why it matters】 Reviewers read top-to-bottom; the contradiction signals the authors do not trust their own numbers, which undermines the whole MR section.
【Specific fix】 Reconcile to the data: CD74 critical-care is highly significant under BH but direction-reversed and 3-instrument-limited; state this once, consistently, and drop the "fails correction" sentence.

### A4-T2-2. STROBE-MR item 9.1.2 (per-SNP exclusion tally) is only qualitative.
【Problem】 §2.10 states the exact per-SNP exclusion tally is "not itemised in those tables and is reported qualitatively here." STROBE-MR expects the harmonisation/exclusion step to be itemised.
【Evidence】 §2.10 l.72 ("the exact per-SNP exclusion tally is not itemised … reported qualitatively").
【Why it matters】 A methods-strict journal (e.g., a genetic-epidemiology outlet) may flag this as incomplete reporting.
【Specific fix】 Either add a supplementary per-SNP harmonisation table, or soften the claim to "summary-level exclusions are provided in the `*_harmonised.csv` files" and point to the column that records dropped SNPs.

## Tier 3

### A4-T3-1. Data availability now names the repository — good.
【Problem】 None. The §Data availability section correctly names `github.com/yyx-4113/sepsis-immunoparalysis-hub` and the data-used statement is consistent with EM submission rules.
【Specific fix】 None.

### A4-T3-2. References integrity verified clean.
【Problem】 None. 31 references defined, 31 cited, zero orphans (grep audit). All 31 refs appear in the body.
【Specific fix】 None.

### A4-T3-3. Abstract / Conclusion "therapeutically addressable" — acceptable hedging.
【Problem】 The v1.3.0 change from "targetable" to "addressable" is appropriate; it frames the axis (not the hubs) as actionable. Keep.
【Specific fix】 Keep; only tidy "rescue-able hub" → "therapeutically addressable axis" (see A1-T3).

## § Stands up (verified correct)
- TRIPOD: calibration + decision-curve analytics cited (Fig S06) for the external score. ✓
- §7 number-provenance table is comprehensive and points to the exact files that expose T0-1 — a strength that makes the error fully auditable. ✓
- Ethics / funding / COI / author-contributions statements present and consistent. ✓

## § Questions for the authors
1. Which target journal? If a genetic-epidemiology venue, the STROBE-MR per-SNP table (A4-T2-2) becomes mandatory, not optional.
2. Will the GitHub repo be public at submission, or only "upon acceptance"? Some journals require public at submission.

## § What I actually checked
- Read `manuscript.md` §2.10, §3.10, §5, Discussion, Data availability, References.
- Grep-audited all `[N]` citations vs the 31-item reference list.
- Cross-read §3.10 internal logic for coherence.
