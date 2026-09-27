# 独立同行评审 — Reviewer A1（脓毒症 / 免疫学方向）

**稿件：** *Immunoparalysis hub genes of the MARS immunosuppressed endotype in sepsis: a multi-omics dissection and in-silico drug repositioning*
**评审立场：** 独立首次投稿评审；仅依据本人亲读稿件与源数据；未接触任何 prior review / RESPONSE / review_r7 / .workbuddy 等文件。
**总体判断：** 方法学透明度与自我批评水准高于多数单作者生信稿，但存在三处会削弱核心结论可信度的问题（FIS1 作为 hub 的定义矛盾、补充表里候选药 rescue 分数的内部不一致、临床转化主张与阴性证据的张力），以及文献覆盖的明显缺口（mHLA-DR 标志、免疫检查点阻断、更广的内型文献）。建议 **Major Revision**。

---

## 问题清单

### P1 【问题】"免疫麻痹枢纽基因"本质上是 Mars1 内型的定义性基因，生物学发现近乎对 Scicluna 2017 / Davenport 2016 的重复确认，新颖性边界未被明确声明。
【证据】稿件 intro 即引用 Scicluna 2017 (ref 4) 将 Mars1 定义为"downregulated HLA class-II, antigen-presentation and monocytic programs"。§3.3 的 6 个 hub 中 5 个免疫基因（CD74、HLA-DQA1、CD14、FCGR3A、HAVCR2/TIM-3）正是 MHC-II / 单核 / 抗原呈递基因；§3.2 自己承认免疫机能评分"partly definitional"。§3.1 的 23/25 共识免疫基因下调，是对 Mars1 定义特征的重算，而非独立发现。
【为何重要】若把"重新发现 Mars1 的抗原呈递下调"包装成 novel hub 发现，新颖性主张会被熟悉该领域的审稿人直接驳回。真正的贡献在于方法学脚手架（三法共识排序、30 基因签名 + 跨平台外部验证、LINCS 重定位、MR 阴性结果），而非生物学洞见。不声明边界会显得 overclaim。
【具体修改】在 Abstract 与 Introduction 结尾增加明确的"新颖性边界"陈述，例如：
> *"Because the Mars1 program is itself defined by suppressed HLA-class-II / antigen-presentation expression (Scicluna et al., 2017), the antigen-presentation/monocytic hub set is, by construction, a recapitulation of the endotype's defining axis. The genuine contributions of this study are therefore (i) a tri-method machine-learning ranking that isolates these genes with out-of-sample stability, (ii) an externally validated 30-gene immune-risk signature, (iii) a LINCS L1000–scored repositioning shortlist, and (iv) a null Mendelian-randomisation test of germline causality — not the biological identification of the immunoparalysis axis per se."*

---

### P2 【问题】FIS1 被同时标为"非免疫、上调、共表达乘客、非机制靶点"，却仍计入 6 个 hub 基因并进入标题/摘要/结论，削弱了"hub"这一核心概念。
【证据】`03_results/S05_hub_genes.csv` 中 FIS1 在 lasso/rf/univariate 三法均为 True；§3.3 原文："FIS1 is a mitochondrial-fission protein absent from the consensus immune gene set… it is up-regulated in Mars1 (logFC +1.26, t = +17.2) and is most plausibly a co-expression passenger… so it is reported as a marker, not a mechanistic target." 本人重算确认 FIS1 logFC = 1.2614（t = 17.16），DEG_0.3=True、方向 Mars1_up。
【为何重要】(a) 作者自己否认 FIS1 是机制靶点，却把它与 5 个免疫 hub 并列称为"6 hub genes"，造成结论自相矛盾；(b) 更深层地，三法 ML 共识在 hub 筛选中并不强制免疫学一致性——FIS1 仅因与免疫模块共表达 + 与生存统计相关而被纳入，暴露该 hub 定义是纯统计的、会把"乘客"误收为"驱动"。这直接削弱 §3.3 与 Abstract 的 hub 主张。
【具体修改】二选一：(i) 将 FIS1 移出 hub 集合，改称"5 个免疫 hub + 1 个共表达乘客基因"，相应修订标题/摘要/结论；或 (ii) 在 hub 定义中显式加入免疫注释过滤（如要求候选基因落在共识免疫基因集或经手动免疫学注释），并把 FIS1 单列。建议替换 §3.3 句：
> *"The tri-method ML consensus recovered five immune hubs — CD74, HLA-DQA1, CD14, FCGR3A and HAVCR2 — all localising to the monocyte / antigen-presenting-cell axis. A sixth consensus gene, FIS1 (mitochondrial-fission protein; Mars1 logFC +1.26), was carried by the survival-associated selection but is absent from the immune gene set and is reported separately as a co-expression passenger rather than an immune hub; accordingly the hub set is defined as the five immune genes, and FIS1 is excluded from hub-level mechanistic claims."*

---

### P3 【问题】补充表 `08b_clinical_translation.csv` 的 `rescue_fraction_S08` 与 `08_candidates_drugs.csv` 对 IL-7、GM-CSF、IFN-γ 三药不一致，且膨胀恰好落在这三个被优先推荐的药上。
【证据】`08_candidates_drugs.csv`（与稿件 Table 2 一致）：IL-7 = 4/5 = 0.80、GM-CSF = 4/6 = 0.667、IFN-γ = 4/7 = 0.571。但 `08b_clinical_translation.csv` 的 `rescue_fraction_S08` 列为：IL-7 = 1.0（文本写作"S08 rescue 1.00"，并列出 CD3D/CD3E/CD8A/IL7R/LCK 5 个基因）、GM-CSF = 0.833、IFN-γ = 0.714。差异来源：08b 似按"方向性下调（不限 |logFC|≥0.3）"计数（如 IL-7 的 CD3E 方向性下调但 DEG_0.3=False，被 08b 计入、被 08_candidates 排除），而 08_candidates 用 0.3 门控。两个补充文件在同一"S08"名下使用了互不一致的指标定义。
【为何重要】这是数据溯源（provenance）不一致；且数值膨胀精确发生在被 §3.8 列为"first functional-validation wave"的三个最爱候选药上，易被解读为确认偏误。稿件正文 Table 2 用的是 0.80/0.67/0.57（正确），但该冲突会动摇补充材料的可靠性，并间接质疑优先排序的客观性。
【具体修改】统一两文件到同一指标定义，并在 §3.8 明确写出所用阈值。建议 `08b_clinical_translation.csv` 将列改名为 `rescue_fraction_directional` 或在脚注注明"counts directionally Mars1-down genes regardless of the 0.3 threshold, contrasting with Table 2's DEG_0.3-gated fraction"，并补一句：
> *"The three top-ranked candidates (IL-7, GM-CSF, IFN-γ) show identical ordering under both the DEG_0.3-gated (Table 2) and the directional (08b) concordance definitions; the absolute fractions differ only by whether sub-threshold directionally-down genes (e.g., CD3E) are counted, and this does not alter their relative priority."*

---

### P4 【问题】§3.8 一边引用 Bo 2011 荟萃（G-/GM-CSF 脓毒症无生存获益）作为"opposing evidence… tempering enthusiasm"，一边仍将 GM-CSF 列为首批功能验证的首选候选，主张与证据之间存在张力。
【证据】§3.8（稿件约 line 143）引用 Bo et al. [30] 荟萃后写"tempering the mechanistic enthusiasm"，但同段末句"prioritizes IL-7 / GM-CSF / IFN-γ as candidates for a first functional-validation wave"。`08b_clinical_translation.csv` 中 GM-CSF 的 clinical_status 仅写"RCTs show restored monocyte HLA-DR"，未体现该阴性生存荟萃。
【为何重要】对同一药物同时给出"机制热情被降温"和"优先验证"两种信号，会削弱临床转化主张的可信度。阴性生存荟萃应更重地压低 GM-CSF 的优先度，或作者需明确说明为何内型分层亚组仍值得一试。
【具体修改】在 §3.8 增加一句以调和：
> *"Although a meta-analysis of G-/GM-CSF in unselected sepsis showed no mortality benefit (Bo et al., 2011), the present endotype-stratified hypothesis is that GM-CSF may benefit only the Mars1 antigen-presentation–deficient subgroup; this remains to be tested and is offered as a hypothesis, not as support for GM-CSF in unselected sepsis."*

---

### P5 【问题】Giamarellos-Bourboulis 2025（ImmunoSep）仅被用来强化内型论证，但其对"MHC-II 重建"重定位主轴（IFN-γ/GM-CSF）的直接阴性生存结果被低估。
【证据】§3.8 引用 ref 32：IFN-γ 用于低 mHLA-DR 脓毒症患者，SOFA 改善但"no mortality benefit and more haemorrhagic events"，且 53% 筛查者不能被 mHLA-DR 标准分型——稿件据此论证"transcriptomic endotypes such as Mars1"的价值（论证方向正确、使用到位）。但同一试验恰是稿件首要重定位轴（抗原呈递 / MHC-II 重建 via IFN-γ、GM-CSF）在最匹配人群中的最直接检验，却仅以"强化内型"被引用，未作为该重定位策略的 caution。
【为何重要】把 ImmunoSep 只用作内型佐证，会让人忽略：在 precisely 免疫麻痹（低 mHLA-DR）人群里，最经典的 MHC-II 诱导剂 IFN-γ 并未改善生存。这与 §3.7–3.9 把 IFN-γ/GM-CSF 列为首选免疫重建候选形成直接张力，应在重定位章节显式承担这一 caution，而非只在 §5 泛泛带过。
【具体修改】在 §3.8 或 Discussion 增加：
> *"Notably, the only large RCT to test MHC-class-II restoration in a biologically selected immunoparalysed population (ImmunoSep; IFN-γ in low-mHLA-DR sepsis) showed SOFA improvement but no 28-day mortality benefit and increased haemorrhage (Giamarellos-Bourboulis et al., 2025). This directly tempers enthusiasm for the antigen-presentation-restoration axis (IFN-γ / GM-CSF) as a mortality-reducing strategy, and is why our repositioning shortlist is framed as hypothesis-generating rather than practice-informing."*

---

### P6 【问题】关键领域文献缺失：mHLA-DR 作为免疫麻痹金标准标志、免疫检查点阻断（PD-1/PD-L1、CTLA4）在脓毒症的重定位证据、以及更广的脓毒症内型文献。
【证据】(a) 稿件仅在 §3.8 经 ImmunoSep 顺带提到"low mHLA-DR"，未引用 mHLA-DR 阈值（如 <8000–12000 AB/C 定义免疫麻痹）的基础生物标志文献（如 Monneret & Venet 综述及 mHLA-DR 流式快速分型共识）。(b) `S01_immunoparalysis_direction.csv` 中 CTLA4 方向性下调（logFC −0.09, adj.P = 0.034），PDCD1（PD-1）上调、HAVCR2（TIM-3）为 hub；但稿件从未讨论免疫检查点生物学，也未引用脓毒症 PD-1/PD-L1 阻断的 RCT/临床试验文献。鉴于"逆转免疫麻痹"这一主旨，PD-1/PD-L1 阻断恰是最直接、且有脓毒症在研试验的免疫重建重定位候选，却被 7 药清单整体遗漏。(c) 内型文献仅引 Scicluna 2017 与 Davenport 2016，未引 Seymour 2019 的 SRS1/SRS2 表型或近年 genomic endotyping 共识，未能把 Mars1 放进更广的内型谱系。
【为何重要】遗漏 mHLA-DR 标志文献使"免疫麻痹"的量化基础显得薄弱；遗漏免疫检查点阻断既是文献缺口、也是重定位候选清单的明显空白（PDCD1-up + HAVCR2-hub 本应首选 checkpoint blockade）；遗漏更广内型文献则削弱立题 contextualization。
【具体修改】(i) 在 Introduction 或 Discussion 增加一段讨论 mHLA-DR 作为免疫麻痹标志与本研究 Mars1 转录_signature 的关系，并引用 Monneret/Venet 与 mHLA-DR 阈值文献；(ii) 在 §3.7 或 Limitations 显式讨论为何未将 anti-PD-1/PD-L1（及 CTLA4）纳入 7 药清单——若属"有意的后续扩展"应说明，若属疏忽应补入并讨论其脓毒症临床试验证据；(iii) 补充 Seymour 2019 (SRS 表型) 与近期 genomic endotyping 综述，以定位 Mars1。

---

### P7 【问题】LINCS L1000 阳性对照（糖皮质激素）呈现是充分且诚实的，但 rescue 指标更深层的"符号缺陷"（把 PDCD1/LAG3 上调也计为 rescue）应在 Limitations 中升级强调；且源 CSV 的"expect LOW rescue"注释已被数据推翻。
【证据】§3.9 明确给出 prednisone rescue 0.136 / rank 651、dexamethasone 0.032 / rank 6808，并指出"a positive rescue score is necessary but not sufficient for functional immune restoration"——本人从 `S08_l1000_positive_control.csv` 核实这两个数值（prednisone 0.1364/651、dexamethasone 0.0315/6808）一致，呈现到位、未被轻描淡写。但 §3.9 也承认 rescue 把 22 个基因（含 Mars1-up 的耗竭标志 PDCD1、LAG3）以同一符号聚合，因此"也 co-rewards exhaustion-marker up-regulation"。这意味着该指标在结构上无法区分"抗原呈递上调（好）"与"耗竭标志上调（坏）"，更无法区分功能免疫重建与单纯转录上调（糖皮质激素即为证）。此外 `S08_l1000_positive_control.csv` 把 dexamethasone 标注为"anti-inflammatory control, expect LOW rescue"，但实测 rescue 0.032（库内前 33%），该期望注释已被数据否定，应清理或改写为"contrary to the a-priori expectation, glucocorticoids showed modest positive rescue, reinforcing the caveat"。
【为何重要】糖皮质激素阳性对照用得好，但 rescue 指标双重（甚至三重）混淆的事实，使 lenalidomide / azithromycin 的"方向性但幅度中等"信号证据力更弱。应在 Limitations 把这一结构性缺陷与糖皮质激素警示并列，明确 LINCS 层仅能筛 hypothesis、不能支持功能结论。
【具体修改】在 §5 增加一条：
> *"The LINCS rescue metric aggregates all 22 query genes with a single sign, so it simultaneously rewards (i) up-regulation of Mars1-down antigen-presentation genes (intended), (ii) up-regulation of the Mars1-up exhaustion markers PDCD1/LAG3 (counter-intended, since true rescue should suppress exhaustion), and (iii) transcriptional MHC-class-II induction by immunosuppressive glucocorticoids (non-functional). The metric is therefore a single-direction Mars1-down proxy and cannot, by construction, certify immunorestorative reversal; LINCS evidence is restricted to hypothesis ranking for the two small-molecule candidates."*

---

## § 站得住的（经本人核实，可保留）

1. **跨平台外部验证设计严谨且诚实。** §3.5 锁定签名、跨平台（Affymetrix → Illumina）、跨人群（荷兰 MARS → 英国 CAP 重症）应用到 E-MTAB-4451，AUC 0.638 (95% CI 0.532–0.748)；并诚实说明 L1 权重未迁移（0.585），结论仅限"基因集+方向"。这是单作者生信稿中少见的 honest generalization 处理。
2. **MR 层的方法学自我批评到位。** §3.10/§5 明确表型匹配（28 天死亡）、预先设定 45 检验家族 BH 校正、主动披露 eQTLGen–UKB 样本重叠且未做重叠校正、将唯一家族显著结果（CD74 critical-care，方向却相反）正确解读为"基因型–严重度关联而非因果 hub 主张"。未把阴性/反向结果包装成阳性，可信度高。
3. **三层级 positive-anchor 设计与 Limitations 透明度突出。** Tier-1/2/3 分级、§7 数字溯源表、以及 10 条 Limitations（含选择链族系误差未控制、亚单位效应量、端点限于 28 天）使几乎所有主张可追溯，远超同类稿件。
4. **关键数字本人重算一致。** 25 共识免疫基因中 23 方向性下调、22 FDR<0.05 显著、21 既下调又显著、PDCD1 上调且显著（全部核实）；Mars1 DEG = 3597（|logFC|≥0.3）；FIS1 logFC = 1.261（t = 17.16）；Table 2 与 `08_candidates_drugs.csv` 一致；糖皮质激素阳性对照数值与源文件一致。
5. **糖皮质激素阳性对照使用正确。** 作为"必要非充分"警示被显式呈现，论证方向合理，未轻描淡写。

---

## § 向作者提问

1. **FIS1：** tri-method ML 共识在 hub 定义阶段是否考虑过加免疫学注释过滤？既然您自己判定 FIS1 为"共表达乘客、非机制靶点"，保留其"hub"身份的理由是什么——还是同意将其移出 hub 集合？
2. **检查点阻断：** 鉴于 PDCD1（PD-1）在 Mars1 中上调、HAVCR2（TIM-3）为 hub，为何 7 药重定位清单未纳入 anti-PD-1/PD-L1（及 CTLA4）？是设计性排除还是文献遗漏？近年脓毒症 PD-1/PD-L1 阻断临床试验是否应被讨论？
3. **签名稳健性：** 30 基因签名的基因选择与方向均复用同一队列 28 天标签（局限性第 1、10 条已承认乐观），除 GSE65682→E-MTAB-4451 外，是否有第三种独立队列或交叉验证策略进一步约束乐观偏差？
4. **08b 分数定义：** `08b_clinical_translation.csv` 的 `rescue_fraction_S08` 与 `08_candidates_drugs.csv` 对 IL-7/GM-CSF/IFN-γ 不一致，以哪个阈值（0.3 门控 vs 方向性）为权威？是否同意统一并加脚注？
5. **MR 重叠敏感性：** eQTLGen 暴露含 UKB 参与者导致暴露–结局重叠，除在 Limitations 声明外，是否尝试用非重叠仪器子集或 mrSampleOverlap 偏倚估计做敏感性分析？
6. **mHLA-DR 关联：** 本研究 Mars1 转录_signature 与经典 mHLA-DR 流式标志的相关性是否在某个队列中实证过？还是仅以 ImmunoSep 的"53% 不可分型"作间接论证？

---

## § 我实际核查了什么

**读取的文件**（按评审契约，未触碰任何 REVIEW_*/RESPONSE_*/review_r7/.workbuddy/SUBMISSION_MANIFEST）：
- `05_reports/manuscript.md`（全文，含被截断尾部，但涉及评审点的章节 §1–§3.10、§5、§7、References 均已读到）
- `03_results/S01_mars1_deg.csv`（11,519 行，全基因矩阵）
- `03_results/S01_immunoparalysis_direction.csv`（25 基因）
- `03_results/S05_hub_genes.csv`（6 hub × 3 方法）
- `03_results/08_candidates_drugs.csv`（7 候选药）
- `03_results/08_positive_control_check.csv`（3 行方法学门控）
- `03_results/08b_clinical_translation.csv`（7 候选药临床转化）
- 额外读取 `03_results/S08_l1000_positive_control.csv`（用于核实糖皮质激素数值，源自稿件 §7 溯源表列出的文件名）

**重算与核对（Python）vs 稿件值：**
| 项 | 稿件值 | 本人重算 | 一致？ |
|---|---|---|---|
| 共识免疫基因总数 | 25 | 25 | ✓ |
| 方向性下调 | 23 | 23（PDCD1、LAG3 上调） | ✓ |
| FDR<0.05 显著 | 22 | 22 | ✓ |
| 既下调又显著 | 21 | 21（22 显著中剔除 PDCD1 上调） | ✓ |
| PDCD1 上调且显著 | 是 | adj.P=2.99e-10，方向 Mars1_up | ✓ |
| Mars1 DEG（|logFC|≥0.3 & FDR<0.05） | 3,597 | 3,597 | ✓ |
| FIS1 logFC / t | +1.26 / +17.2 | +1.2614 / +17.16，DEG_0.3=True | ✓ |
| Table 2 rescue（IL-7/GM-CSF/IFN-γ/阿奇/来那/胸腺/BCG） | 0.80/0.67/0.57/0.67/0.40/0.40/0.20 | 与 `08_candidates_drugs.csv` 完全一致 | ✓ |
| 糖皮质激素阳性对照 | prednisone 0.136/651；dexamethasone 0.032/6808 | `S08_l1000_positive_control.csv`：0.1364/651；0.0315/6808 | ✓ |

**发现的不一致（未见于稿件正文、属源数据层面）：**
- `08b_clinical_translation.csv` 的 `rescue_fraction_S08` 对 IL-7=1.0、GM-CSF=0.833、IFN-γ=0.714，与 `08_candidates_drugs.csv` / Table 2 的 0.80/0.667/0.571 冲突（见 P3）。
- `S08_l1000_positive_control.csv` 将 dexamethasone 标注"expect LOW rescue"，但实测 rescue 0.032（库内前 33%），期望注释被数据否定（见 P7）。

**未核实（说明边界）：**
- sepsis-vs-healthy 448 DEG 数（来自 `S01_deg_sepsis_vs_ctrl.csv`，不在本次提供的必读清单内，未读取）；该数为次要旁证，不影响核心结论。
- 外部验证 AUC 0.638 的原始 `09_external_validation.csv`、LINCS 全库 20,413 化合物排名文件（体积过大，未全读）；糖皮质激素两项数值已通过 `S08_l1000_positive_control.csv` 直接核实，其余 L1000 排名未见矛盾。
- MR 各 OR/CI 数字来自稿件 Table 3/4 与所引 CSV 文件名，未逐行打开 `10_*.csv` 复核（属本次评审范围外，但稿件内部自洽、且 MR 结论为"阴性/反向"，与本文重点的生物学与转化主张无直接冲突）。
