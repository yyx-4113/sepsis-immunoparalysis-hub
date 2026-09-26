# A4 评审报告 — 期刊/报告规范（TRIPOD · STROBE-MR · 格式 · 声明）

**评审角色**：资深学术期刊编辑 + 医学研究报告规范审计员（独立同行评审）
**稿件**：`05_reports/manuscript.md`（v1.0.2）
**研究类型**：计算多组学 + 药物重定位（单作者，纯公共数据再分析）
**独立性声明**：本人假设从未见过本稿、未参与其任何修订轮次，按首次投稿审。已读取 `_PANEL_BRIEF.md` 与 `manuscript.md` 全文；**未读取** `05_reports/review/` 下其他专家文件、`*REVIEW*`/`*RESPONSE*`、PIPELINE.md 执行注释、`*_gen_*.py`、`06_literature/` 等禁读文件。每条判断均来自本人亲读文本或亲算源数据。

---

## 总评（Overall verdict）

这是一篇在生物学层面对"Mars1 免疫抑制内型由抗原呈递/单核枢纽基因锚定"论证扎实、且外部验证已落地的计算多组学稿。作者对自己证据层级的自我认知是诚实的——§5 局限与 §8 期刊定位均明确写"MR 仅提示性""功能验证为设计稿""对接按设计未做"。

但**稿件正文（摘要结论、§4、§6）的 headline 措辞与 §5/§8 的自限不一致**，且**报告规范层面存在硬性缺口（TRIPOD 校准/DCA 缺失、STROBE-MR 协调剔除计数缺失、孤儿图选择性报告嫌疑、参考文献体例与期刊要求不符）**。这些不直接推翻结论，却是 Q1 期刊（J Transl Med 7.5）审稿人会毫不留情打回的"可报告性/规范性"问题。

一句话：**期刊层级（Q1）在学科范围上并不偏高，偏高的只是稿件当前的 claim–evidence 失配与规范完备度；正确解法是收敛 headline 并补齐规范，而非盲目降级。**

---

## 一、报告规范诚实性（TRIPOD / STROBE-MR）

### F1. 30-gene 签名未遵循 TRIPOD；且 `S06_dca.png`（决策曲线）已生成却被隐藏
【Problem】30-gene 免疫风险签名作为 28 天死亡率预测模型仅报告了 AUC，缺失校准曲线、缺失 DCA、缺失区分度表、缺失临床效用；同时 `04_figures/S06_dca.png`（决策曲线）已生成却从未在正文引用，正文亦未提及校准/DCA/临床效用。

【Evidence】
- `manuscript.md:104-105`（§3.4 仅报 CV-AUC 0.659 / 训练 0.750，无校准/DCA）
- `manuscript.md:107-110`（§3.5 仅报外部 AUC 0.638 / CI 0.532–0.748，无校准/DCA）
- `04_figures/` 目录存在 `S06_dca.png`，但全稿未引用（grep "DCA|calibration|决策曲线|calibr" 仅命中参考文献 18 的 "empirical calibration"，语境为观察性研究 p 值校正，与预测模型校准无关）；同目录 `S06_roc_cv.png`、`S06_roc_train.png` 亦未引用。

【Why it matters】TRIPOD（Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis）对"个体预后预测模型"要求同时报告**区分度**（AUC/ROC）+ **校准**（calibration plot、calibration slope/intercept）+ **临床效用**（decision-curve analysis）。一篇在 Q1 期刊声称 "prognostically informative" 的预后签名，若只报 AUC 而无校准与临床效用，审稿人会质疑其是否真具临床信息量。更关键的是：**DCA 图已经存在却被隐藏**——这触及"选择性报告（selective reporting）"红线，性质比单纯遗漏更严重，会直接引发对结果完整性的不信任。

【Specific fix】二选一，强烈建议 (i)：
- **(i) 纳入并正名**（因 DCA 已算）：在 §3.4/§3.5 增 "Calibration and clinical utility" 小节，引用 `04_figures/S06_dca.png` 并补一张校准图，另补一张区分度表（固定特异度 0.80 下的灵敏度 / 约登指数，或最佳 cutoff 下的灵敏度+特异度）；在 §7 溯源表登记。英文替换句示例：
  > "Calibration of the locked score on E-MTAB-4451 was adequate (calibration slope ≈0.9, intercept near 0; Fig. Sx); decision-curve analysis showed net benefit over the treat-all and treat-none strategies across threshold probabilities 0.20–0.60 (Fig. Sy)."
- **(ii) 若坚持定位为探索性分子签名（非临床预测工具）**：删除 `S06_dca.png` 等孤儿图，并将所有 "prognostically informative" 改为 "associated with 28-day mortality as an exploratory signal"，明确不构成临床预测模型、不提供临床效用声明。

### F2. STROBE-MR 缺失协调（harmonisation）剔除 SNP 计数与敏感性分析
【Problem】MR 部分未报告工具变量协调过程中被剔除的 SNP 数量与原因（palindromic / 链模糊 / 等位不相容），也未给出留一法（leave-one-out）或 MR-PRESSO 等敏感性分析；MR 三假设未显式列示。

【Evidence】
- `manuscript.md:71`（仅写 "palindromic SNPs resolved by allele frequency and dropped when strand could not be determined"，未给任何计数）
- `manuscript.md:143-156`（Table 3 报 n_IV、median F、Cochran Q P、I²、Egger intercept P，但无剔除计数、无留一法）
- `03_results/10_genetics_mr_harmonised.csv` 仅含最终工具变量（主结局 27 行 = CD74 3 + HLA-DQA1 4 + CD14 6 + HAVCR2 6 + FIS1 8 = 27，已核对一致），未给出进入协调前的 SNP 总数与剔除数。

【Why it matters】STROBE-MR（观察性 MR 报告规范扩展）明确要求：工具变量选取、**协调细节（含被剔除 SNP 的数量与原因）**、样本/人群重叠、敏感性分析。缺失剔除计数会使读者无法判断"FCGR3A 仅 2 个可用变异"是真实数据特性还是协调偏倚所致；缺失留一法/MR-PRESSO 则无法排除单个 SNP 驱动效应。这不直接推翻作者已自律为 Tier-3 的"提示性"结论，但会削弱方法透明度与可重复性评分，且在 Q1 期刊易被要求补正。

【Specific fix】在 §2.10 与 §3.10 补协调流水账与假设声明。英文句示例：
> "Across the six hub genes, N SNPs were extracted from the outcome and harmonised; M were dropped for palindromic/ambiguous strand and K for allele incompatibility, leaving the n_IV reported in Table 3 (FCGR3A: 2 retained → below the ≥3-instrument threshold). Mendelian randomisation rests on three assumptions: (1) relevance — instruments associate with the exposure; (2) independence — instruments are unrelated to confounders; (3) exclusion restriction — instruments affect outcome only via the exposure."
并补充 leave-one-out 与 MR-PRESSO（或显式声明未做并说明原因）。

### F3. "druggable" 与 "best published" 等 headline 与 §5 自限自相矛盾（可报告性边界）
【Problem】摘要结论、§6、§4 中的强措辞（"druggable"、"at the level of the best published sepsis mortality signatures"）与 §5 局限性及 §3.5 的 "modest" 自限直接或间接抵触。

【Evidence】
- `manuscript.md:14`（摘要 Conclusion "simultaneously prognostic and **druggable**"）
- `manuscript.md:202`（§6 "both prognostically informative ... and **druggable**"）
- `manuscript.md:178`（§4 "places the signature at the level of the **best published** sepsis mortality signatures"）
- 对比 `manuscript.md:108`（§3.5 "magnitude that is real but **modest**"）、`manuscript.md:188`（§5 "comparable to rather than better than the published IRG benchmark"）、`manuscript.md:194`（§5 对接 S09 按设计未做）。

【Why it matters】高 IF 期刊对"结论超出证据"极敏感。"**druggable**" 用于描述 HLA-II / FcγR / CD14 / TIM-3 等免疫受体与抗原呈递 machinery 本身并不准确——它们并非经典可成药小分子靶点；真正"可重定位"的是 IL-7/GM-CSF/IFN-γ 等免疫调节剂。把"hub 基因 druggable" 说成事实会招致 overclaim 拒稿。"**best published**" 与 §5 自承 "comparable to rather than better than" 直接抵触，损伤可信度。

【Specific fix】英文替换：
- 摘要与 §6 改为："The Mars1 program is anchored by antigen-presentation/monocytic hub genes that are prognostically informative and for which **repositionable immunorestorative agents can be nominated**."
- §4 改为："places the signature in the same performance band as published sepsis mortality signatures (external AUC ≈0.64), i.e. **comparable rather than superior** to the IRG benchmark."

---

## 二、目标期刊 fit 与证据层级匹配

### F4. J Transl Med 7.5 Q1 是否偏高 — 明确判断与降级阶梯
【Problem】需对"JTM 7.5 Q1 首选是否偏高"给出明确判断，并给出降级建议。

【Evidence】
- `manuscript.md:235-248`（§8 自列 6 刊，JTM 首选；§8:237 已诚实写 "germline-causality layer is suggestive rather than confirmed ... functional validation is design-only ... should not be pitched to mechanism-demanding top-tier"）
- `manuscript.md:142-172`（MR 仅提示性，无 IVW 显著）、`manuscript.md:73-74`（S11 功能验证未执行）、`manuscript.md:194`（S09 对接未做）
- 外部 AUC 0.638 / CI 0.532–0.748（已核对 `03_results/09_external_validation.csv` 一致）

【Why it matters】决定投稿策略与拒稿风险。

【Specific fix】**明确判断**：
1. **学科范围上"偏高"= 否**。JTM（BMC，IF 7.5，Q1）常规发表多组学 + 药物重定位 + MR 生信文，本稿主题（免疫麻痹、翻译基因组学、医学生物信息）与其收稿范围高度契合，Q1 并非不切实际。
2. **但当前 claim–evidence 失配在 Q1 会显著抬高拒稿/大修风险**。正确解法是把 headline 收敛到 §5/§8 已承认的诚实边界（见 F3、F12），**而非降级期刊**。
3. **降级阶梯**（仅当作者拒绝收敛 claim 时采用）：JTM 7.5 → **Frontiers in Immunology 5.7**（免疫麻痹角度更贴，但仍 Q1、规范相近）→ **Scientific Reports 3.9**（多学科、审稿严但范围宽容）/ **Shock 2.9**（脓毒症专科、范围更窄）。**EBioMedicine 10.8 / Critical Care 9.3 作为"补功能验证后的冲刺档"定位正确**，当前证据（无实验验证、对接未做）不足以冲刺。
4. 一句话建议：以 JTM 为靶刊是可接受的，前提是先完成 F1–F3、F5–F12 的规范与措辞整改。

---

## 三、格式硬伤

### F5. 正文 author-year 引用 vs 期刊要求 numbered 引用（体例冲突）
【Problem】正文用"作者-年份"描述式引用，但 References 是编号 1–29（首作者字母序）；目标期刊（JTM、FiI 均 Vancouver/编号引用）要求正文用方括号编号引用。

【Evidence】
- `manuscript.md:33`（"Scicluna et al., Lancet Respir Med 2017"）、`manuscript.md:57`（"Peng et al. 2023"、"Front Immunol 2023, fimmu.2023.1152117"）
- `manuscript.md:270-298` References 为编号 1–29 字母序（Aran→Basham）

【Why it matters】BMC/JTM 与 Frontiers 均要求 Vancouver 编号引用（正文 `[n]`，参考文献按引用顺序或编号排列）。当前"author-year 正文 + 字母序编号列表"二者不匹配，投稿后需大规模返工，且易被技术初审退回。

【Specific fix】将正文所有描述式引用改为方括号编号，并令 References 按首次引用顺序重排（或保留编号但确保正文用 `[n]`）。示例：`manuscript.md:33` 改 `(4)`（Scicluna = Ref 4）；`manuscript.md:57` 改 `(16)`（Peng = Ref 16）；`manuscript.md:57` 中 "Front Immunol 2023, fimmu.2023.1152117" 改 `[16]`。投稿前统一用文献管理软件处理，避免手工编号错位。

### F6. 孤儿图（8/10 未引用）+ Figure 编号不连续
【Problem】`04_figures/` 下 10 个图，仅 2 个（Fig S09、Fig S10）被正文引用；S01/S02/S03/S06/S07 共 8 个图全部孤儿，且正文 Figure 编号跳空（直接 S09/S10，缺失 S01–S08 引用）。

【Evidence】
- `04_figures/` 含：`S01_roc_28d_mars1.png`、`S02_score_vs_endotype.png`、`S03_eigengene_trait_cor.png`、`S03_top_hub.png`、`S06_dca.png`、`S06_roc_cv.png`、`S06_roc_train.png`、`S07_celltype.png`、`fig_s09_external_roc.png`、`fig_s10_l1000_rescue.png`
- 正文中仅 `manuscript.md:110`、`manuscript.md:140` 引用 S09/S10；其余 S0x 均无引用（grep 确认）

【Why it matters】孤儿图 = 选择性报告或草稿未清理的嫌疑，评审会质疑是否只展示了"好看"的结果；编号跳空（S09/S10 凭空出现）也显得章节组织未完成。

【Specific fix】将关键结果图纳入正文或补充材料并连续编号：建议 `S01`(28d ROC)、`S02`(评分 vs 内型)、`S03`(hub 网络)、`S06`(CV/train ROC + DCA)、`S07`(细胞定位) 作为 Fig S1–S7 引用；外部验证 ROC 与 L1000 作为 Fig S8–S9（或保留名称但补编号前缀）。**任一图若不引用，必须从投稿包中删除**，避免"未声明产物"引发完整性质疑。

### F7. 缺通讯作者邮箱；中文摘要对英文刊冗余
【Problem】标题块缺通讯作者标注与有效邮箱；附中文摘要对纯英文刊（JTM）属冗余。

【Evidence】
- `manuscript.md:3-5`（仅姓名/单位/ORCID，无 "Correspondence" 与邮箱）
- `manuscript.md:20-27`（中文摘要）

【Why it matters】BMC/JTM 要求明确通讯作者及有效邮箱，否则无法进入生产流程；中文摘要对纯英文刊非必需，可被视为格式不符（移至 Supplementary 或删除）。

【Specific fix】标题块加：`*Correspondence: Yongxin Yang, <email>; ORCID 0009-0004-9698-6552*`。中文摘要可保留于 Supplementary Materials 或删除。

### F8. §8 期刊定位段已标"投稿前删除"——须确认实际移除
【Problem】§8 期刊定位段虽已标 "(planning note; delete before submission)"，需确认其在投稿包中确实被移除，且其内部 IF 数值来源需可核。

【Evidence】
- `manuscript.md:235`（标题 "(planning note; delete before submission)"）
- `manuscript.md:248`（"Full source-attributed table: 03_results/journal_targeting.csv"）

【Why it matters】若误随稿提交，会被视为"作者自定期刊分级"且不专业；非常规小节也可能触发系统拒收。

【Specific fix】**投稿前从 `manuscript.md` 删除整个 §8**；保留 `journal_targeting.csv` 仅作内部决策。提交前逐项核对删除动作已完成。

---

## 四、数据可用性 / 伦理 / 声明

### F9. Data availability 写 "to be created at acceptance" — 合规风险
【Problem】Data availability 写 "to be created at acceptance"，属占位式声明，对 BMC/JTM 数据政策有合规风险。

【Evidence】
- `manuscript.md:254`（"available in the project's versioned reproducibility repository (to be created at acceptance)"）

【Why it matters】BMC 数据与材料政策要求数据在投稿时或接收前存于公共库并给可用链接/DOI；"to be created at acceptance" 等同未存放，会被要求补正甚至拒稿。

【Specific fix】改为主动存放并给 DOI。英文句：
> "Raw data: GEO GSE65682 (platform GPL13667) and ArrayExpress E-MTAB-4451 (platform GPL10558), accessions as cited. Processed expression matrices, phenotype tables and all result CSVs are deposited at Zenodo/Figshare [DOI: xxxx], released under MIT."
若暂时无法给 DOI，至少声明 "provided as Supplementary Files" 并附 GEO/ArrayExpress 登录号，删除 "to be created at acceptance"。

### F10. Ethics 对公共数据成立；Author contributions/Funding/COI 与单作者一致（基本合规，可小补强）
【Problem】伦理声明对纯公共去标识数据再分析基本成立，但可补强；作者贡献/基金/COI 与单作者一致，合规。

【Evidence】
- `manuscript.md:256-257`（Ethics：纯计算再分析公共去标识队列，无需额外 IRB）
- `manuscript.md:259-266`（Author contributions / Funding / COI 均为单作者 YY 一致表述）

【Why it matters】纯公共去标识数据再分析通常无需 IRB，但多数期刊期望注明原始队列已获伦理批准/知情同意。当前声明可接受，补强可提升严谨度。作者贡献/基金/COI 与单作者设定自洽，无矛盾。

【Specific fix】Ethics 段补一句："The original GSE65682 and E-MTAB-4451 cohorts were approved by their respective institutional review boards with participant consent (Scicluna et al., 2017 [4]; Davenport et al., 2016 [5])." 作者贡献/基金/COI 维持现状即可。

---

## 五、cover letter 一致性

### F11. 项目暂无 cover letter — 须写且与 claim 语气一致，不得夸大
【Problem】项目暂无 cover letter 文件；投稿须撰写，且语气须与 manuscript 的"提示性 MR""设计稿验证"自限一致，不得夸大。

【Evidence】
- `_PANEL_BRIEF.md` 明确"项目暂无 cover letter 文件"
- `manuscript.md:172`、`manuscript.md:189`（MR 仅 "suggestive / hypothesis-generating"）
- `manuscript.md:73-74`、`manuscript.md:194`（S11 设计稿、S09 对接未做）

【Why it matters】cover letter 若夸大（如称 "causally validated"、"novel druggable targets identified"）会与正文自限矛盾，损害编辑第一印象，甚至被视为学术不端信号。

【Specific fix】提供 cover letter 骨架，语气与 §5/§8 一致：
> "We report (i) an externally validated 30-gene immunoparalysis signature (independent E-MTAB-4451 AUC 0.638, 95% CI 0.532–0.748); (ii) a mechanism-anchored drug-repositioning shortlist (IL-7/GM-CSF/IFN-γ) scored by LINCS L1000 reverse-connectivity; and (iii) a two-sample MR layer that is **suggestive but not confirmatory** (no primary IVW estimate significant). Functional validation is a pre-specified prospective design not yet executed, and structure-based docking was deferred by design. We do not claim causal proof or identification of novel druggable targets, and we present the MR strictly as hypothesis-generating."

---

## 六、可报告性边界（headline 过度 vs 别处 qualify）

### F12. "Virtual knockdown ... satisfying the positive control" 缺乏实证支撑
【Problem】§3.3 声称 "Virtual knockdown of these hubs phenocopies immunoparalysis ... satisfying the knockdown positive control"，但全稿无虚拟敲除结果（图/表）支撑，疑似逻辑断言而非实证阳性对照。

【Evidence】
- `manuscript.md:102`（"Virtual knockdown of these hubs phenocopies immunoparalysis (they are themselves Mars1-down), satisfying the knockdown positive control"）
- `manuscript.md:63`（§2.8 将 virtual knockdown 列为阳性对照门控）
- `03_results/` 与 `04_figures/` 均无虚拟敲除结果文件（仅有 S03 hub 网络、S08 L1000 等）

【Why it matters】把未展示的计算结果称为"满足阳性对照"属于未被证据支持的结论，违反报告诚实性；若虚拟敲除实际未运行，则该声明失实。

【Specific fix】二选一：
- **(i)** 若确已运行，补充虚拟敲除结果（如沉默 hub 后签名/评分下降的图或表）于 §3.3 并纳入 §7 溯源表；
- **(ii)** 若仅为逻辑论证（hub 本身即 Mars1-down），改表述为："Because these hubs are themselves Mars1-down genes, their perturbation is mechanistically coherent with immunoparalysis (positive-control logic); formal in-silico knockdown validation is deferred." **不得继续称"已满足实证阳性对照"**。

---

## § Stands up（本人怀疑但核查后确认稿件正确的地方）

1. **IRG 基准 0.619 vs 0.604 矛盾**——经查实为两值并存且已调和：`03_results/S06_auc_compare.csv:5` "IRG 基准(E-MTAB-4451),0.619" 为 Peng 等（Front Immunol 2023, Ref 16）报值；`03_results/09_external_validation.csv:14` `auc_IRG3_benchmark_EMTAB4451,0.604` 为本文在 E-MTAB-4451 重算值。`manuscript.md:188`（§5）明确写 "comparable to rather than better than the published IRG benchmark (0.604 recomputed; 0.619 reported)"，摘要 `manuscript.md:12-13` 亦区分 "published benchmark 0.619–0.648" 与 "recomputed 0.604"。非错误，仅建议 §2.6 加一句说明两值来源以免混淆。

2. **CD14 MR-Egger BH-FDR = 0.026**——本人重算：跨 15 项 gene×outcome MR-Egger 检验，CD14 主结局 P=0.0051096 排名第 3，BH 调整 = (15/3)×0.0051096 = 0.0255 ≈ 0.026，与 `manuscript.md:145` 一致。

3. **CD74 critical-care BH-FDR ≈ 0.21**——本人重算：15 项 IVW 检验中 CD74 critical P=0.014028 排名第 1，BH = (15/1)×0.014028 = 0.2104 ≈ 0.21，与 `manuscript.md:170` 一致。

4. **各 hub median F 值**——CD74 35.4 / HLA-DQA1 168.1 / CD14 45.7 / HAVCR2 36.4 / FIS1 75.0，与 `03_results/10_genetics_mr_harmonised.csv` 逐 SNP F 中位数核对一致（例：CD74 三 SNP F = 37.6/35.4/30.7 → 中位 35.4；CD14 六 SNP F = 1382.2/586.2/46.5/44.8/43.0/31.2 → 中位 45.7）。

5. **外部验证数值全链核对**——`09_external_validation.csv` 中 `orientedSum 0.6382` / `CI 0.5317–0.7475` / `locked 0.5848` / `CI 0.4687–0.6959` / `IRG 0.604`，与 `manuscript.md:108`、`manuscript.md:219` 完全一致；`S06_auc_compare.csv` 中 CV 0.6586 / train 0.7495 与 `manuscript.md:105`（0.659/0.750）一致。

6. **§8 自评估诚实**——`manuscript.md:237` 明确写 "germline-causality layer is suggestive rather than confirmed ... functional validation is design-only ... should not be pitched to mechanism-demanding top-tier"，与 §5 自限自洽。说明作者自知之明，body 的 overclaim 属措辞问题，非故意造假。

7. **Table 3 OR/CI/P 与源文件一致**——CD74 IVW OR 1.119 (0.607–2.063) P0.72、CD14 MR-Egger 0.906 P5.1e-3、CD14 median 0.914 P0.065 等，均与 `10_genetics_mr_outcome5086_28ddeath.csv` 逐行核对一致。

---

## § Questions for the authors

1. **虚拟敲除是否实际运行？** §3.3 称 "satisfying the knockdown positive control"，但 `03_results/` 与 `04_figures/` 中无对应结果文件。请确认：是已运行待补图/表（F12-i），还是仅为逻辑论证（F12-ii）？
2. **协调阶段具体剔除多少 SNP？** 请分别给出 palindromic、链模糊、等位不相容各自剔除计数，以补 STROBE-MR（F2）。
3. **是否运行 leave-one-out / MR-PRESSO？** 若未运行，是否计划补充或显式声明？
4. **`S06_dca.png` 与校准图的处理意向？** 拟纳入正文满足 TRIPOD（F1-i），还是坚持探索性签名定位并删除之（F1-ii）？
5. **通讯作者邮箱与 Data availability 的实时 DOI 何时落实？**（F7、F9）
6. **参考文献编号化返工是否已由文献管理软件完成？** 请确认正文 `[n]` 与列表顺序一致（F5）。
7. **§8 在投稿包中是否已实际删除？**（F8）

---

## § What I actually checked

- 读取 `_PANEL_BRIEF.md` 与 `manuscript.md` 全文（v1.0.2）；**未读取**其他专家评审、`*REVIEW*`/`*RESPONSE*`、PIPELINE.md 执行注释、`*_gen_*.py` 等禁读文件，遵守独立性纪律。
- 列 `04_figures/`（10 文件）与 `03_results/`（全量），确认 `S06_dca.png` 等 8 图孤儿、仅 `fig_s09_external_roc.png`(Fig S09)、`fig_s10_l1000_rescue.png`(Fig S10) 被引。
- 读取并核对 `S06_auc_compare.csv`、`09_external_validation.csv`、`10_genetics_mr_outcome5086_28ddeath.csv`、`10_genetics_mr.csv`、`10_genetics_mr_outcome4982_criticalcare.csv`、`10_genetics_mr_harmonised.csv`：
  - IRG 0.619（已发表）vs 0.604（本文重算）来源区分；
  - 外部验证 orientedSum 0.6382 / CI 0.5317–0.7475 / locked 0.5848 / CI 0.4687–0.6959 / IRG 0.604 与稿件一致；
  - 重算 BH-FDR：CD14 MR-Egger (15/3)×0.0051096≈0.026、CD74 critical IVW (15/1)×0.014028≈0.21，与稿件一致；
  - 逐 SNP 核对 median F 与 Table 3 OR/CI/P 一致；
  - 确认 FCGR3A 主结局 nsnp=2（insufficient_instruments），与稿件"仅 2 个可用变异"一致。
- 确认 References 1–29 为字母序编号列表、正文 author-year 引用（F5）；确认 §8 标 "delete before submission"（F8）；确认 Data availability "to be created at acceptance"（F9）。
- 未运行 git push；未读其他专家输出。

---

*评审人：A4（期刊编辑 + 报告规范审计）| 独立、首次投稿视角 | 聚焦 TRIPOD / STROBE-MR / 格式 / 声明一致性*
