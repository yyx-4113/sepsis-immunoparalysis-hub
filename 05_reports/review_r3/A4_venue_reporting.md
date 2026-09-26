# A4 — Journal Editor & Reporting-Standards Review (Round 3, v1.2.0)

**Independence note:** Fresh first-submission read of `manuscript.md` and `cover_letter.md`. No prior `REVIEW_*.md` / `review*/` consulted.

## Findings

### T0 (DESK-REJECT-risk if Conclusion read standalone) — FIS1 branded as antigen-presentation/monocytic hub in Conclusion
- **【Problem】** Conclusion l.207 writes "antigen-presentation/monocytic hub genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2, **FIS1**)" — a biological falsehood the paper itself retracts in §3.3.
- **【Evidence】** `manuscript.md:207` vs `:103`.
- **【Why it matters】** Many editors skim Abstract + Conclusion. A standalone read yields "mitochondrial-fission protein is an antigen-presentation hub" → immediate credibility hit / possible desk reject.
- **【Specific fix】** See A1 T0-1 paste-ready sentence; re-list FIS1 outside the immune-hub parenthetical.

### T1 — "Therapeutically targetable" in Conclusion over-reaches the evidence
- **【Problem】** The conclusion asserts the hub genes are "therapeutically targetable," but the study provides no direct-target evidence (§2.8, §5 #9: curated response-gene concordance only, no DGIdb/ChEMBL).
- **【Evidence】** `manuscript.md:15, :179, :207`; ZH `:25` "可药性". Cover letter is clean (no such claim) — good.
- **【Why it matters】** Overclaim in the conclusion is the most visible spot for an editor; it invites a "claims exceed evidence" rejection.
- **【Specific fix】** Use "therapeutically addressable axis" / "marker of a reversible, pharmacologically actionable state."

### T3-1 — Data availability is too vague to be actionable
- **【Problem】** "GitHub: https://github.com/yyx-4113" does not name the specific repository; a reader cannot locate the exact artifact.
- **【Evidence】** `manuscript.md:242`.
- **【Why it matters】** Data-availability statements should point to the exact repo (and, per §7, a persistent DOI). Vagueness fails reproducibility-checklist expectations.
- **【Specific fix】** "…versioned reproducibility repository (GitHub: https://github.com/yyx-4113/<repo-name>; persistent DOI to be issued on acceptance)."

### T2-1 — Abstract EN/FH count ambiguity (see A1 T2-1)
- **【Evidence】** `manuscript.md:14`.
- **【Specific fix】** Add the PDCD1-up clarification to the abstract.

## § Stands up (verified correct)
- STROBE-MR item 9b now honestly scoped: harmonised CSVs hold retained instruments; exact exclusion tally explicitly NOT itemised (l.72) — transparent, not misleading. ✓
- TRIPOD: calibration + DCA referenced for the external score (l.106, Fig S06). ✓
- Abstract vs body: IRG "comparable" framing is internally consistent (EN l.14, body l.109/179). The only abstract/body gap is the PDCD1 count nuance (T2-1). ✓
- Cover letter evidence-tier framing (Tier-1 robust / MR hypothesis-generating / drug metric = curated concordance / functional validation = blueprint) **matches** the manuscript — no over-statement in the letter. ✓
- Single-author declaration, corresponding-author email, ethics statement, funding/COI all present and correct. ✓
- References numbered 1–31 sequential; all 31 cited in body (verified). ✓

## § Questions for the authors
- Will you name the exact repository in Data availability before submission? (Required for most computational-biology journals.)

## § What I actually checked
- `manuscript.md` (full) + `cover_letter.md`.
- Grepped cover letter for "targetable/druggable/therapeutically" → none (clean).
- Verified reference sequence 1–31 and citation coverage via script (uncited=[]).
- Spot-checked STROBE-MR / TRIPOD wording against §2.10/§3.10/§3.4.
- Discrepancy: FIS1 branding (T0) and "targetable" framing (T1) are real; everything else consistent.
