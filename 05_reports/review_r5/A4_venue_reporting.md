# A4 — Venue / Reporting-standard lens

I reviewed v1.4.0 for reporting-checklist honesty (STROBE-MR, TRIPOD-adjacent) and for title/abstract/conclusion consistency. The paper is now honest about the MR layer; remaining issues are wording-level and emphasis.

## Findings

### Tier 2 — A4-1: "therapeutically addressable axis" unhedged in headline positions
【Problem】 The phrase appears in Abstract, Discussion, and Conclusion without a caveat that no direct target validation exists and MR is null/opposite.
【Evidence】 Abstract (line 15) "mark a therapeutically addressable axis"; Discussion (line 179) "therapeutically addressable set"; Conclusion (line 207) "therapeutically addressable axis."
【Why it matters】 Venue editors (e.g., Scientific Reports, BMC) run consistency/claim checks; an unhedged "addressable" next to a null MR layer invites a minor-revision flag.
【Specific fix】 Add "(in expression terms; direct target validation pending)" at least in the Conclusion, and keep Abstract wording but pair with the §5 limitation.

### Tier 2 — A4-2: "strongest MR association" emphasis (see A1-1)
【Problem】 Headlining a reverse, 3-instrument, overlap-affected signal three times.
【Evidence】 §3.10 ×2, §5 ×1.
【Why it matters】 Editorial tone: over-claiming the weakest (most fragile) signal undermines the strong, honest external-validation story.
【Specific fix】 Reduce to one mention in the secondary-outcome/limitations context (per A1-1).

### Tier 3 — A4-3: Data-availability "to be made public upon acceptance"
【Problem】 "to be made public upon acceptance, with a persistent DOI to be minted, e.g., via Zenodo" — fine, but confirm the GitHub URL is live and the repo actually contains the cited files.
【Evidence】 §Data availability (line 242), URL github.com/yyx-4113/sepsis-immunoparalysis-hub.
【Why it matters】 Some venues verify the repo; a 404 or empty repo is a hard check failure.
【Specific fix】 Before submission, confirm the repo is populated with `03_results/`, `02_scripts/`, and `10_mr_bh_family.csv`; consider minting the Zenodo DOI pre-acceptance as a preprint companion.

### Tier 3 — A4-4: IRB statement consistency
【Problem】 Ethics statement correctly separates bioinformatics (no IRB) from S11 (needs IRB). Consistent.
【Evidence】 §Ethics statement (line 245).
【Why it matters】 No change; noted as compliant.

## § Stands up (verified)
- No "smallest q=0.058 / all-null" fabrication (the prior fatal error) — the MR layer now correctly reports 3 surviving CD74 tests.
- STROBE-MR item 9b retained-instrument disclosure present (§2.10).
- TRIPOD-adjacent calibration/DCA referenced (§3.4, Fig. S06).
- Title/abstract/conclusion all now separate FIS1 as non-immune (no self-contradiction).

## § Questions for the authors
- Target venue decided? (Specifies which reporting checklist to audit against — STROBE-MR for the MR layer is already partially addressed.)

## § What I actually checked
- Read full manuscript; checked Abstract/Discussion/Conclusion for "addressable"/"targetable" consistency.
- Verified the FIS1 non-immune separation is present in all three headline sections.
- Confirmed no re-emergence of banned phrases (per A3 scan).
