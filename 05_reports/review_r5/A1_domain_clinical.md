# A1 — Domain / Clinical lens (sepsis immunology & translational relevance)

I reviewed `manuscript.md` v1.4.0 as a first submission, with no access to prior review rounds. I focused on whether the biological and clinical claims are sound and whether emphasis is placed where the evidence actually is.

## Findings

### Tier 1 — A1-1: Reverse-direction CD74 signal is over-emphasised as a "strongest MR association"
【Problem】 The CD74 critical-care MR signal (OR 2.22, reverse direction, 3 instruments) is repeatedly headlined as "the strongest MR association in the study," which over-weights a non-causal, reverse, underpowered result.
【Evidence】 §3.10 (lines 159, 171–173) and §5 (line 190) use "the strongest MR association in this study" / "the strongest MR association in the study" three times; the signal reverses the Mars1 model (higher predicted CD74 → worse outcome) and rests on only 3 instruments with exposure–outcome overlap.
【Why it matters】 A fresh clinician-reader will remember the "strongest association" and miss that it is explicitly non-causal; this is the kind of emphasis that triggers reviewer pushback and dilutes the genuine contribution.
【Specific fix】 Keep ONE mention, placed in the secondary-outcome/limitations context, e.g. in §3.10 secondary paragraph: "CD74 reached the only family-surviving signal (critical-care, reverse direction, 3 instruments), reported here as a genotype–severity association rather than a hub claim." Delete the two other "strongest MR association" phrasings and the ⚠️ emphasis on Table 4 CD74 row.

### Tier 2 — A1-2: FIS1 biological interpretation is missing
【Problem】 FIS1 is flagged as the single non-immune hub but its mechanistic relevance to immunoparalysis is never interpreted.
【Evidence】 §3.3 (line 103) and §6 (line 207) note FIS1 is "a mitochondrial-fission protein outside the immune set" but give no link to immune dysfunction.
【Why it matters】 Without interpretation, a reviewer may read FIS1 as a co-expression passenger that inflates the hub set's biological coherence.
【Specific fix】 Add one clause in §3.3: "FIS1 downregulation may couple mitochondrial dynamics / oxidative-stress signalling to immune-cell dysfunction, though its causal role in immunoparalysis is not established; it is retained as a co-expression member rather than an immune anchor."

### Tier 2 — A1-3: "therapeutically addressable axis" is unhedged
【Problem】 The conclusion/abstract claim that the hubs "mark a therapeutically addressable axis" is stated without the caveat that no direct target validation exists.
【Evidence】 Abstract (line 15), Discussion (line 179), Conclusion (line 207); MR shows null/opposite effects (§3.10), and repositioning rests on expression-level rescue + L1000 (§3.9).
【Why it matters】 A strict venue editor may flag "addressable" as implying target-level tractability not demonstrated.
【Specific fix】 Soften to "mark a therapeutically addressable axis in expression terms (direct target validation pending)" or add a one-line §5 limitation.

### Tier 2 — A1-4: IFN-γ clinical evidence is old/small (honesty already good, minor)
【Problem】 IL-7/GM-CSF/IFN-γ are presented as the top candidates; IFN-γ's human sepsis signal is the 1997 Döcke study (ref 13), small.
【Evidence】 §3.8 (line 132) cites Döcke 1997 for IFN-γ; the paper already notes weak dedicated sepsis trials.
【Why it matters】 Low risk — the paper is already honest here; only a precision note.
【Specific fix】 No change required; optionally add "IFN-γ's human sepsis evidence remains limited to small early trials" in §3.8.

## § Stands up (verified correct)
- External AUC 0.638 (CI 0.532–0.748) on E-MTAB-4451, n=106, 52 deaths — matches `09_external_validation.csv` (`auc_EMTAB4451_orientedSum`=0.6382, CI 0.5317–0.7475). Excellent honest generalization.
- 29/30 signature genes mapped (HLA-DQA1 absent on Illumina) — matches `09_external_validation.csv` (`n_signature_genes_mapped_EMTAB4451`=29).
- Glucocorticoid positive-control caveat (prednisone/dexamethasone score high) in §3.9 — methodologically strong, correctly interpreted as "necessary not sufficient."
- FIS1 correctly separated as non-immune in both §3.3 and §6 — fixes the earlier self-contradiction.

## § Questions for the authors
- Do the 3 CD74 critical-care instruments correspond to known CD74 cis-eQTLs, or could they be proximal to HLA region pleiotropy given CD74 sits in the MHC? This matters for the "genotype–severity" interpretation.
- Was any sensitivity MR run excluding the HLA-region LD-clumped instruments for CD74 (given MHC proximity)?

## § What I actually checked
- Read `manuscript.md` v1.4.0 in full.
- Cross-checked `03_results/09_external_validation.csv` (AUC, CI, n, mapped genes) — all match.
- Spot-checked `03_results/10_mr_bh_family.csv` for the CD74 critical-care q values cited in text — match.
- Did NOT re-run BH (delegated to editor/implementation lens); relied on the table the authors generated.
