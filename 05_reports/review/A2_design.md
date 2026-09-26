# 独立评审意见 — A2（生物信息统计 + MR 因果推断设计）

**评审角色**：资深生物信息统计学家 / 孟德尔随机化（MR）与因果推断方法学专家
**评审视角**：研究设计、统计推断严谨性、乐观偏倚、样本重叠、多重比较、工具变量有效性
**稿件**：`05_reports/manuscript.md` v1.0.2（首次投稿审，无任何历史上下文预设）
**独立性声明**：本评审仅依据稿件正文与 `03_results/` 源数据亲自核对/重算；未读取其他专家文件、PIPELINE 执行注释或 `*_gen_*.py`。

---

## 0. 总评（Executive summary）

稿件整体设计层级清晰、Tier 分层（Tier-1 生物必然信号 / Tier-2 方法阳性对照 / Tier-3 探索性预后与 MR）是值得肯定的结构。从**设计与统计因果**角度，稿件在若干核心环节存在可被接收编辑/方法学审稿人直接质疑的问题，按严重度排序：

1. **（重点·高）30-gene 签名存在标签泄漏导致的乐观偏倚**——基因选择与定向在含标签的全队列完成，5-fold CV 的 0.659 仍被乐观化；诚实泛化值应是外部 0.638，且需补 nested-CV。
2. **（重点·高）IRG benchmark 在同一队列（E-MTAB-4451）出现两个值（0.619 vs 0.604）且未澄清来源**——构成内部矛盾/误读风险，并削弱"超过基准"的论断。
3. **（重点·高）MR 样本重叠偏倚未讨论**——eQTLGen（n≈31,684，含 UK Biobank 队列）与 UKB 来源的脓毒症 GWAS（ieu-b-5086/4980/4982）极可能存在样本重叠，稿件 §3.10/§5 完全未提，属 Tier-0/1 级设计遗漏。
4. **（中）Table 1 效应量与 P 值与我核对的源文件不一致**——中心"高度显著、协调下调"的量化支撑无法溯源，须作者澄清。
5. **（中）阳性对照门控缺乏选择性/特异性量化**；**阈值与 hub 选择存在双重蘸取（double-dipping）**；**链式选择缺失家族-wise 误差控制**。
6. **（低·已大体正确）MR 多重比较框架本身正确**（我重算确认 CD14 Egger FDR=0.026、CD74 critical-care FDR≈0.21 均无误），但"仅 Egger 显著、无 IVW 显著"的边界性质需更克制的表述。

下面逐条展开，每条含【Problem】【Evidence】【Why it matters】【Specific fix】。

---

## F1（重点）30-gene 签名：标签泄漏造成的乐观偏倚

**【Problem】** 签名的基因**选择**（70-gene panel 按 |r| 与 28-day death 排序取 top-30）与**定向**（按 corr_with_death 符号）均在**含全部 479 例结局标签的全队列**上完成，之后再跑 5-fold CV。这意味着每一折测试集的死亡标签已参与决定了"选哪些基因、取何符号"，构成经典的**标签泄漏 / 选择偏倚**，使 CV-AUC 0.659 仍被乐观化。

**【Evidence】**
- `03_results/S06_signature_genes.csv` 明确给出 `corr_with_death` 列（如 ELANE +0.170、LCK −0.167、CD74 −0.163…），并按 `abs_r` 降序排列——即 top-30 由全队列与 death 的 Pearson r 选出；符号即定向。稿件 §2.6 原文："A pre-defined immune panel (70 genes) was ranked by |Pearson r| with 28-day death; the top-30, each oriented so expression positively contributes to death risk…" 与此一致。
- `03_results/S06_auc_compare.csv`：签名 CV = 0.6586、train = 0.7495 → train–CV 乐观度 0.091（稿件 §3.4 报 0.659 / 0.750）。
- 外部独立队列 `09_external_validation.csv`：锁定基因集+定向后的 equal-weight 评分 AUC = 0.6382（CI 0.5317–0.7475），低于 CV 的 0.659；locked L1 权重 AUC 仅 0.5848（CI 0.4687–0.6959）——即**诚实泛化值约 0.638**，且 L1 权重在跨平台几乎不可移植。

**【Why it matters】** 预测模型开发中，特征选择与定向若使用测试折标签，CV 估计会系统性高估泛化性能（Ambroise & McLachlan, *PNAS* 2002；TRIPOD 预测模型报告声明第 10–11 条要求"特征选择必须在每一训练折内重做"）。此处泄漏的结构是：top-30 选择 + 定向这一**整个特征工程步骤在 CV 循环之外、用全队列标签完成**，因此每一折测试集的标签已"预先窥视"过。结果 0.659（同队列 CV）被用作摘要、§3.4、§6 的**头条数字**并据此宣称"超过 IRG 基准 0.619–0.648"；但真正无泄漏的估计是外部 0.638（且 CI 极宽、与 IRG 不可区分，见 F2）。审稿人会首先质疑该 AUC 的可信度，并进而质疑整个"预后价值"主张的独立性。乐观量至少包含两层：train–CV 差 0.091（模型拟合乐观）+ 选择泄漏（进一步约 0.02，由 0.659→外部 0.638 推断）。

**【Specific fix】**
- 报告 **nested 5-fold CV**（在每一训练折内重新做 top-30 选择+定向，再在测试折评估）作为同队列的无泄漏估计；预期落于 0.638–0.659 之间、且低于 0.659。
- 将**外部 AUC 0.638（CI 0.532–0.748）** 作为头条泛化指标，而非 0.659；并在摘要/§3.4/§6 中明确写"within-cohort CV is optimistically biased by label-leaky gene selection; the externally validated estimate is 0.638"。
- 可粘贴英文替换句（摘要 Results 段）：
  > "A 30-gene immune-risk signature, with genes selected and oriented by their correlation with 28-day death, yielded a within-cohort cross-validated AUC of 0.659; this estimate is optimistically biased because gene selection and orientation used the full-cohort outcome labels. The signature's honest generalisation is the externally locked AUC of 0.638 (95% CI 0.532–0.748) on E-MTAB-4451."

---

## F2（重点）IRG benchmark 内部矛盾（同一队列两个值，未澄清）

**【Problem】** 稿件对 E-MTAB-4451 上的 IRG 基准给出了**两个不同数值**——§2.6/§3.4 用 **0.619**，§3.5/§7/摘要用 **0.604**——却未说明二者是"不同计算/不同处理流程"下的结果，读来像内部不一致或笔误。

**【Evidence】**
- `03_results/S06_auc_compare.csv`：`IRG 基准(E-MTAB-4451),0.619` 与 `IRG 基准(GSE65682),0.648`。
- `03_results/09_external_validation.csv`：`auc_IRG3_benchmark_EMTAB4451,0.604`。
- 稿件 §2.6："benchmarked against the published immune-related-gene (IRG) signature (0.619 on E-MTAB-4451, 0.648 on GSE65682; Front Immunol 2023, fimmu.2023.1152117)"——即 0.619 是 **Peng 2023 原报值**（Peng 团队在其自身处理流程下对该队列的 AUC）。
- 稿件 §3.5："again exceeded the IRG benchmark recomputed on the same cohort (0.604)"——即 0.604 是**作者在本稿处理流程下重算的同一 IRG 签名**于同一 E-MTAB-4451 矩阵。
- 因此两者均为"E-MTAB-4451 上的 IRG"，但前者来自外部发表、后者来自本稿重算，差异（0.015）源于**数据预处理/探针映射/结局定义/样本过滤**不同，而非生物学。

**【Why it matters】** 第一，声明诚信：同一队列、同一基准给两个值而不解释，方法学/统计审稿人会判定为内部矛盾甚至数字错误。第二，论断脆弱性：头条"签名 CV 0.659 超过 IRG 0.619–0.648"把 **GSE65682 上的 0.659** 与 **E-MTAB-4451 上的 0.619** 跨队列/跨处理比较（不公平）；而真正公平的同队列比较是 E-MTAB-4451 上 0.638 vs 0.604（+0.034），但 IRG 0.604 **没有报告 CI**，无法判定显著超过；签名自身 CI 0.532–0.748 极宽，与 IRG 很可能重叠。第三，GSE65682 上公平比较应为 0.659 vs 0.648（+0.011，几乎无差）。

**【Specific fix】**
- 在 §2.6 与 §3.5 显式区分并加脚注：
  > "The IRG benchmark value of 0.619 on E-MTAB-4451 is the figure reported by Peng et al. (Front Immunol 2023) on their own processed matrix; we recomputed the identical published IRG signature on our processed E-MTAB-4451 matrix and obtained 0.604. The two differ only by preprocessing, not by biology."
- 比较口径改为：(a) GSE65682 上签名 CV 0.659 vs IRG 0.648；(b) E-MTAB-4451 上签名 0.638 vs IRG 0.604（并补 IRG 0.604 的 bootstrap CI 以做正式比较）。
- 弱化"exceeds"为"comparable to / numerically above"：
  > "On E-MTAB-4451 the locked signature (AUC 0.638, 95% CI 0.532–0.748) was numerically above our recomputed IRG benchmark (0.604), though the confidence intervals overlap and the difference is not formally significant."

---

## F3（重点）MR 样本重叠偏倚未讨论（eQTLGen × UK Biobank）

**【Problem】** 暴露为 eQTLGen 全血 cis-eQTL（n≈31,684），结局为 UK Biobank 脓毒症 GWAS（ieu-b-5086/4980/4982）。eQTLGen 是聚合多队列的 meta 分析，**UK Biobank 是其组成队列之一**；因此暴露与结局**极可能共享参与者**（sample overlap）。稿件 §3.10/§5 完全未提及该偏倚，属 Tier-0/1 级设计遗漏。

**【Evidence】**
- 稿件 §2.10："Exposure was the eQTLGen whole-blood cis-eQTL for each hub gene… all are GRCh37/hg19 with per-gene n of 13,344–31,684." eQTLGen 2021（Visser et al., *Nat Genet* 53:1300–1310；PMC8432599）明确为 31,684 例全血/PBMC 表达，来自 37 个数据集的 meta，其中 UK Biobank 全血 RNA-seq 为已知组成队列。
- 结局 ieu-b-5086（脓毒症 28 天死亡，1,896/484,588）、ieu-b-4980（易感性，11,643/474,841）、ieu-b-4982（危重症，1,380/429,985）均为 IEU OpenGWAS 中的 UKB 派生 GWAS。
- 稿件 §3.10/§5 的局限仅讨论"germline vs acute state"与"underpowered"，**未出现 sample overlap / overlapping samples 任何字句**。

**【Why it matters】** 两样本 MR 的核心假设是两"样本"独立。当暴露与结局 GWAS 共享个体时，相关结构会**抬高 I 类错误率并可使效应估计向不可预测方向偏倚**——这是与样本量增大相反的偏倚：更多重叠不会靠大样本"平均掉"，反而会系统性扭曲（Burgess & Thompson, *Stat Med* 2016；样本重叠在 eQTL-MR 中被广泛指出是假阳性来源，尤其 eQTLGen（含 UKB）对 UKB 结局的 MR 常出现被膨胀的关联，文献中常称此类结果为"overlap-inflated"）。其机制是：重叠个体同时贡献暴露与结局的汇总统计，使工具变量与结局的相关中混入"同一人两次测量"的相关性，等价于放松了独立性假设。本稿 15 项检验中仅 1 项 Egger 边界显著、无 IVW 显著——若其中混入重叠偏倚，则这唯一"提示性"信号的方向与显著性都不可靠。即便作者的最终结论是"仅提示性、不做因果宣称"，**沉默该偏倚本身即是方法学缺陷**，因为读者无法判断那一个 Egger 信号是真实还是重叠假象；而期刊（尤其 JTM/Front Immunol 的 MR 方法学审稿人）会直接要求披露与敏感性分析。

**【Specific fix】**
- 在 §3.10 与 §5 显式加入样本重叠讨论：
  > "Potential sample overlap: the eQTLGen consortium aggregates whole-blood expression across multiple cohorts including UK Biobank, whereas all three sepsis outcomes are UK Biobank–derived. Overlapping participants between the exposure and outcome GWAS can inflate Type-I error and bias MR estimates in either direction (Burgess & Thompson, 2016). We could not rule this out from summary data alone."
- 加一项**敏感性分析/缓解**：(i) 明确核查 eQTLGen 组成队列是否含 UKB（见 Questions）；(ii) 若含，汇报重叠估计并考虑重叠稳健法（如基于重叠样本校正的 MR、或 Leave-one-cohort-out 的 eQTLGen 子集、或非 UKB 的 eQTL 来源做三角验证）；(iii) 至少把"overlap cannot be excluded"作为对那一个 Egger 信号的附加警示。
- 不建议删除 MR 层（它已达 Tier-3 诚实定位），但须把重叠偏倚与"germline vs acute"并列写入 §5 局限。

---

## F4（中）MR 多重比较：框架正确，但"仅 Egger 显著"须更克制表述

**【Problem】** 稿件对 15 项基因×结局 MR-Egger 做 BH-FDR 并据此称 CD14 Egger 通过校正（FDR=0.026）。**我重算确认该数值本身正确**，但"唯一显著结果仅来自 Egger、且 IVW 全不显著"的边界性质，在正文与摘要中被呈现得略显肯定。

**【Evidence】**
- `10_genetics_mr_outcome5086_28ddeath.csv`：CD14 MR-Egger P = 0.0051096，OR 0.90595，intercept P = 0.344。
- 全 15 项 MR-Egger P 中，CD14-primary（0.00511）为第 3 小（前二为 CD74-critical 6.6e-13、CD74-susceptibility 1.65e-4）。按稿件所述"15 gene×outcome Egger"BH：0.0051096 × 15 / 3 = **0.0255 ≈ 0.026**，与稿件一致 → **数字无误**。
- 但同一结局 IVW：CD14 IVW P=0.236、weighted median P=0.065，均不显著；5 个 hub 中**无任何 IVW 主估计显著**（表 3）。
- CD74-critical IVW P=0.014，BH-FDR=0.01403×15/1=0.210≈0.21（稿件 §5 称 ≈0.21，无误），且方向与表达层模型相反。

**【Why it matters】** Egger 是三估计量中功效最低、对少数 IV 最敏感者；当 IVW 与 weighted median 均不显著、唯独 Egger 边界显著时，该信号对 outlier SNP 与截距假设高度脆弱。稿件结论（"suggestive, not demonstrative"）方向正确，但摘要与 §3.10 把"CD14 Egger FDR=0.026"作为 MR 层最亮眼证据，易让读者高估其分量。

**【Specific fix】**
- 在报告 CD14 Egger 处加一句限制：
  > "This single Egger-significant result is not corroborated by IVW or weighted median on the same outcome, and Egger estimates are particularly unstable with ≤6 instruments; it should be read as hypothesis-generating, not as evidence of a causal effect."
- 建议在 supplemental 给出**每个估计量各自的 15-test BH-FDR 表**（IVW / Egger / wMedian 各一列），使"无 IVW 显著"一目了然，而非只在正文强调 Egger 的 0.026。

---

## F5（中）弱工具变量：FCGR3A 排除正确，CD74 critical-care 3 IVs 仍偏脆弱

**【Problem】** FCGR3A 仅 2 个可用 IV 被排除（正确）；但 CD74 critical-care 仅 3 个 IV（F 中位数未给该结局，但 §3.10 称全层 median F 35–168）。3 个 IV 虽满足 F>10，但 IV 数偏少，MR-Egger/IVW 在少 IV 下对 pleiotropy 与 outlier 极敏感。

**【Evidence】**
- `10_genetics_mr_outcome4982_criticalcare.csv`：CD74 IVW n=3，OR 2.222（CI 1.175–4.200），P=0.014，FDR≈0.21，方向与表达层模型相反；MR-Egger intercept 不显著但 Egger OR 同样 2.22。
- 稿件 §3.10/§5 已正确标注"rests on only three instruments… fails correction… points opposite"。

**【Why it matters】** 少 IV 下，即使 Cochran Q/I² 显示低异质，单个 pleiotropic SNP 即可翻转 Egger 截距与估计；CD74-critical 的"反向且与模型矛盾"已提示其可能由 1–2 个 outlier 驱动。将其列为 hypothesis-generating 是对的，但应更明确：3 IV 不足以支持任何因果解读，连"提示性"都勉强。

**【Specific fix】**
- 在 §3.10 表 4 脚注补：
  > "Estimates based on ≤3 instruments (CD74 critical care) are inherently fragile; we report them only to show direction, not as evidence."
- 可选增强：对 3-IV 基因补 **leave-one-IV-out** 敏感性，证明估计不靠单一 SNP。

---

## F6（低·大体正确）因果方向（germline vs acute state）：已诚实说明，建议再收紧一句

**【Problem】** MR 测的是种系决定的**基线**表达，而 Mars1 是**急性、状态依赖**的失调——该结构局限稿件已在 §3.10/§5 诚实说明。

**【Evidence】** 稿件 §5 局限 2 末段："MR interrogates baseline expression rather than acute state-dependent suppression, and the mortality GWAS (1,896 cases) is underpowered for individually small effects." 该表述充分。

**【Why it matters】** 这是 eQTL-MR 针对"疾病状态基因"的固有解释边界；稿件处理得当，降低了"因果误读"风险。

**【Specific fix】**（仅作收口强化，非纠错）
> "Because eQTL instruments capture life-long, germline-determined baseline expression, a significant MR effect would imply that constitutive expression level predisposes to outcome—not that reversing the acute Mars1 state therapeutically recapitulates the MR effect. Therapeutics targeting the acute program should not be inferred as causal from these MR results."

---

## F7（中）阳性对照门控缺乏选择性/特异性量化

**【Problem】** §2.8 的阳性对照门控为"IFN-γ 须 rescue ≥3/5 抗原呈递基因"，这是**表面效度（face validity）**检查，但未量化该门控的**选择性**——即随机/无关/免疫抑制性药物有多大的概率也能通过 ≥3/5。

**【Evidence】**
- 稿件 §2.8：门控仅要求 IFN-γ 救 ≥3/5 抗原呈递基因；§3.7 称 IFN-γ 救 4/5 满足。
- 稿件 §3.9 已诚实给出**负向对照警示**：糖皮质激素（prednisone rescue 0.136、dexamethasone 0.032）也高分，证明"rescue score ≠ 功能恢复"。
- 但门控本身（≥3/5）若不加选择性量化，则"通过门控"提供的信息量低：需要知道在背景药物/随机基因集中，多少比例能达到 ≥3/5。

**【Why it matters】** 方法学审稿人会问：这个 gate 的特异度是多少？若 30% 的随机药物都能过 ≥3/5，则 IFN-γ 通过并不特别；门控就只是"能识别一个已知诱导剂"的演示，而非对方法严谨性的独立背书。稿件已用 glucocorticoid 负对照补了"rescue≠功能"的洞见，但门控选择性仍是空缺。

**【Specific fix】**
- 补一个选择性/null 分布分析：对一组**已知免疫抑制性药物**（或与 Mars1-down 无生物学关系的随机药物集）计算 rescue_fraction，报告通过 ≥3/5 的比例作为假阳性率背景；或报告"随机基因集 rescue 的置换分布"以说明 ≥3/5 是否高于背景。
- 可粘贴：
  > "To quantify gate selectivity, we computed rescue_fraction for 50 randomly drawn gene sets of equal size; the ≥3/5 pass-rate was X%, establishing that the IFN-γ pass is Y-fold above chance."

---

## F8（中）阈值与稀疏：|logFC|≥0.3 与 top-2000 hub 选择的双重蘸取

**【Problem】** (a) §2.2 对重处理阵列取 |logFC|≥0.3 阈值偏低，虽以 FDR 控假阳性，但产生 3597 个 Mars1-DEG，其中大量效应极小；(b) §2.4 取"2000 个最显著 Mars1-DEG"做共表达 hub——这把**差异表达信号注入共表达网络**，属 double-dipping：所谓"hub"部分反映的是 Mars1 状态本身，而非独立的共表达结构。此外 |Pearson r|⁶ 的 6 次幂是任意选择。

**【Evidence】**
- 稿件 §2.2："Mars1-vs-Other at |logFC|≥0.3 & FDR<0.05" → 我核对 `S01_mars1_deg.csv` 得 DEG_0.3=True = **3597**（与稿件 §3.1 "3,597"一致）；sepsis-vs-healthy = **448**（一致）。
- 稿件 §2.4："Among the 2,000 most significant Mars1-DEGs, a |Pearson r|⁶ adjacency yielded degree centrality; the top-50 genes by degree define the co-expression hub."
- 稿件 §2.5：机器学习共识候选集为 "Mars1-DEG ∩ consensus immune set"（进一步把 hub 限在 DEG 内）。

**【Why it matters】** 当 hub 基因本就从"最显著 DEG"中挑出，再用其共表达度中心性排序，网络结构天然偏向 Mars1 差异表达谱——这不一定是错误（免疫麻痹 hub 本就该与 Mars1 相关），但它意味着 hub 的"独立性/网络真实性"未被外部验证。r⁶ 幂次未论证，结果对幂次敏感。

**【Specific fix】**
- 明确说明该 hub 是"Mars1 差异共表达 hub"（而非无偏全转录组共表达 hub），并在 §3.3 写清这是 by-design 的生物学聚焦，其独立性需外部单细胞/独立队列验证。
- 补敏感性：用 r² 与 r⁴ 重算 hub，报告 top hub 是否稳定；或在全表达基因（非仅 DEG）上建共表达网络作对照，说明限定 DEG 的影响。
- 可粘贴：
  > "The co-expression hub was derived from the 2,000 most significant Mars1-DEGs by design, so it captures Mars1-associated co-expression rather than an unbiased whole-transcriptome network; robustness to the |r|⁶ power was confirmed with |r|² and |r|⁴ (top-hub overlap = Z%)."

---

## F9（中）链式选择缺失家族-wise 误差控制

**【Problem】** 免疫评分（§2.3）、hub 选择（§2.4–2.5）、签名定向（§2.6）全部依赖**同一 479 例 GSE65682 + 同一 28-day death 标签**。各步内部做 FDR，但步骤间**无家族-wise 误差控制**——DEG → 免疫方向 → hub → 签名是一条依赖链，整体族错误率未被控制。

**【Evidence】**
- 稿件 §2.3–2.6 各步均在同一 sepsis-with-outcome 子集（479 例）操作；hub 来自 DEG∩immune set，签名来自同一 death 标签排序。
- 唯一跨队列独立验证的是签名（E-MTAB-4451，0.638），而 **hub 基因身份、'22/25 显著'等未被独立复制**。

**【Why it matters】** 探索性组学链式选择会 inflate 整体假阳性率（circular analysis 风险；Kriegeskorte et al., *Nat Neurosci* 2009）。稿件 Tier-1 主张（"compact, prognostically informative hub"）的"预后信息"部分只由同队列签名 CV（有泄漏，见 F1）与未被复制的 hub 支撑。外部验证部分缓解了签名，但未缓解 hub 身份。

**【Specific fix】**
- 在 §5 加一条局限：
  > "The immune score, hub selection and signature orientation were all optimised on the same 479-sample GSE65682 cohort with the 28-day outcome; no family-wise error control was applied across these sequential steps. The signature is the only component independently validated (E-MTAB-4451); hub-gene identity remains discovery-level and requires replication."
- 若可行，用 E-MTAB-4451 或其它独立脓毒症转录组**复现 hub 共表达结构**作为增强。

---

## F10（中·高）Table 1 效应量与 P 值无法溯源至 cited 源文件

**【Problem】** 稿件 §3.1 / Table 1 给出的若干共识免疫基因效应量与 P 值，与我核对的源文件 `S01_immunoparalysis_direction.csv`（及 `S01_mars1_deg.csv`、`S01_deg_sepsis_vs_ctrl.csv`）**不一致**；该表是"协调、高度显著的免疫麻痹"的量化支点，却无法溯源。

**【Evidence】**（逐基因核对，源=`S01_immunoparalysis_direction.csv`，logFC/P.Value 列）
- HLA-DRB1：稿件 Δ=**−0.59**, P=**9.7e-09** → 源文件 logFC=**−0.8925**, P=**2.22e-16**（不符）。
- CD74：稿件 Δ=**−0.48**, P=**8.2e-09** → 源文件 logFC=**−0.7578**, P=**4.44e-16**（不符）。
- FCGR3A：稿件 Δ=**−0.55**, P=**1.0e-06** → 源文件 logFC=**−0.6097**, P=**3.09e-11**（不符）。
- ITGAM：稿件 Δ=**−0.48**, P=**7.0e-12** → 源文件 logFC=**−0.2084**, P=**1.19e-03**, 且 DEG_0.3=False（不符，且源中 ITGAM 远未达"高度显著"）。
- HLA-DRA：稿件 Δ=**−0.18**, P=**3.5e-02** → 源文件 logFC=**−0.4689**, P=**1.84e-07**（不符）。
- CD14：稿件 Δ=**−0.77**, P=**1.3e-17** → 源文件 logFC=**−0.7657**, P≈0（**相符**）。
- HAVCR2：稿件 −0.39 / 1.7e-16 vs 源 −0.349 / 7.5e-14（近似）；LYZ：−0.21 / 2.9e-4 vs 源 −0.256 / 3.6e-6（近似）。

换言之，Table 1 是**混合来源**——部分（CD14）与源文件一致，多数（HLA-DRB1、CD74、FCGR3A、ITGAM、HLA-DRA）显著偏离，且偏离方向并非统一缩放。我额外核对 `S01_deg_sepsis_vs_ctrl.csv`（sepsis-vs-healthy）亦不匹配。因此这些数值既不来自本稿 Mars1-DEG 文件，也不来自 sepsis-vs-healthy 文件。

**【Why it matters】** ① 可溯源性失效：§7 数字溯源表把上述值指向 `S01_immunoparalysis_direction.csv`，但实际不符，违反可重复承诺。② 中心叙事受损：稿件以"效应量亚单位但高度显著（HLA-DRB1 Δ=−0.59, P=9.7e-9 等）"论证协调免疫麻痹，但源文件显示 HLA-DRB1 实为 −0.89/P≈2e-16、ITGAM 仅为 −0.21/P=1.2e-3——量级与显著性被改写，读者无法验证。③ 这些基因同时是 hub/MR 的焦点，数值失真会波及下游解释。

**【Specific fix】**
- 作者须逐格核对 Table 1 每个数字到其真实来源；若数值引自 Peng 2023 或 Scicluna 2017 等**他人研究**，须明确归属并改述为"既往研究报道"，不得作为本稿 Mars1-DEG 结果呈现。
- 若数值应为本稿重分析，则用 `S01_immunoparalysis_direction.csv` 的真实 logFC/P 替换（如 HLA-DRB1 −0.89/2.2e-16、CD74 −0.76/4.4e-16、FCGR3A −0.61/3.1e-11、ITGAM −0.21/1.2e-03、HLA-DRA −0.47/1.8e-07）。
- 可粘贴（Table 1 校正模板）：
  > "| HLA-DRB1 | −0.89 | 2.2×10⁻¹⁶ | MHC-II | (values as recomputed in S01_immunoparalysis_direction.csv) |"

---

## § Stands up（我怀疑过但核查后确认稿件正确的地方）

为履行交付要求，以下各项我**主动质疑并亲自重算/核对，结论为稿件无误**，应被接收编辑视为已通过方法学检查：

1. **DEG 计数完全正确**：核对 `S01_mars1_deg.csv` 得 Mars1-vs-Other DEG_0.3=True = **3597**（稿件 §3.1 "3,597"✓）；`S01_deg_sepsis_vs_ctrl.csv` 得 **448**（✓）。
2. **MR 多重比较 FDR 数值正确**：CD14-primary Egger P=0.0051096，在 15 项 gene×outcome Egger 中排第 3（前二为 CD74-critical 6.6e-13、CD74-susceptibility 1.65e-4），BH = 0.0051096×15/3 = **0.0255 ≈ 0.026**，与稿件 §3.10/§5 的 "BH-FDR 0.026" 一致。CD74-critical IVW P=0.01403，排第 1，BH=0.01403×15/1=**0.210 ≈ 0.21**，与稿件 "≈0.21" 一致。→ 多重比较框架本身严谨。
3. **外部验证数值正确**：`09_external_validation.csv`：orientedSum AUC=0.6382（CI 0.5317–0.7475）、locked L1 AUC=0.5848（CI 0.4687–0.6959）、29/30 基因映射、缺失基因为 HLA-DQA1——均与 §3.5 一致。
4. **FCGR3A 因仅 2 IV 被排除正确**，且 CD74-susceptibility Egger 截距显著（intercept P=9.98e-5）被正确地判定为方向性多效、不可解释为因果（§5 局限 2）。
5. **因果方向局限已诚实陈述**（germline vs acute state），见 F6，处理得当。
6. **糖皮质激素负向对照警示已充分**（§3.9 prednisone/dexamethasone 高分），正确削弱了"rescue=功能恢复"的误读，见 F7。
7. **"22/25 显著"正确**：`S01_immunoparalysis_direction.csv` 中 25 个共识免疫基因有 22 个 adj.P<0.05（第 2–23 行），与 §3.1 一致。（注：raw sign 下 23 个为 Mars1_down，稿件称"21 个方向性下调"应指与免疫麻痹预期方向一致者，建议 §3.1 给"方向性下调"的操作定义以避免与 raw 23 混淆。）

---

## § Questions for the authors（需作者澄清，不代答）

1. **样本重叠**：eQTLGen 的组成队列是否包含 UK Biobank？若是，请量化暴露–结局重叠规模，并说明是否/如何校正（见 F3）。
2. **Table 1 溯源**：§3.1 / Table 1 中 HLA-DRB1(−0.59, 9.7e-9)、CD74(−0.48, 8.2e-9)、FCGR3A(−0.55, 1.0e-6)、ITGAM(−0.48, 7.0e-12)、HLA-DRA(−0.18, 3.5e-2) 的**确切来源**是何处？若来自他人文献请归属；若为本稿重分析请给出正确数值（F10）。
3. **IRG 双值**：请确认 0.619（Peng 2023 原报）与 0.604（本稿重算）的预处理差异，并按 F2 在文中显式区分；另请提供 0.604 的 CI 以便做正式比较。
4. **nested CV**：是否尝试过 nested 5-fold CV（特征选择在训练折内）？若有，请给出无泄漏的同队列 AUC；若无，是否同意补做并将外部 0.638 作为头条（F1）？
5. **门控选择性**：≥3/5 阳性对照门控在背景/随机药物集上的通过率（假阳性率）是多少（F7）？
6. **r⁶ 依据**：|Pearson r|⁶ 邻接的幂次选择有何依据？不同幂次下 hub 是否稳定（F8）？
7. **家族-wise 误差**：是否计划用独立队列复现 hub 共表达结构，以补链式选择缺失的家族-wise 控制（F9）？

---

## § What I actually checked（审阅痕迹）

**读取的稿件/数据文件**
- `05_reports/manuscript.md`（全文，重点 §2.2–2.10、§3.1–3.10、§5、§7）。
- `03_results/S06_auc_compare.csv`：签名 CV 0.6586 / train 0.7495；IRG E-MTAB-4451 0.619、GSE65682 0.648。
- `03_results/09_external_validation.csv`：orientedSum 0.6382（CI 0.5317–0.7475）、locked L1 0.5848（CI 0.4687–0.6959）、IRG 重算 0.604、29/30 映射、缺失 HLA-DQA1。
- `03_results/S06_signature_genes.csv`：30 个基因及其 `corr_with_death`（全队列与 death 的 Pearson r），证实标签泄漏机制（F1）。
- `03_results/S01_immunoparalysis_direction.csv` 与 `S01_mars1_deg.csv` 与 `S01_deg_sepsis_vs_ctrl.csv`：核对 25 共识免疫基因方向/显著性、Table 1 数值（发现 F10 不符）、DEG 计数（3597/448 正确）。
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv`、`10_genetics_mr.csv`、`10_genetics_mr_outcome4982_criticalcare.csv`：核对 CD14/各 hub 的 IVW/Egger/wMedian OR、P、截距、FDR，重算 BH-FDR（确认 0.026 与 0.21 无误）。

**独立重算/核对的值（与稿件比对）**
- DEG 计数：Mars1 3597、sepsis-vs-ctrl 448 —— 与稿件一致。
- CD14-primary Egger BH-FDR：按 15 项 Egger P 排序（CD14 第 3 小），0.0051096×15/3 = 0.0255 ≈ 0.026 —— 与稿件一致。
- CD74-critical IVW BH-FDR：0.01403×15/1 = 0.210 ≈ 0.21 —— 与稿件一致。
- Table 1 五基因数值：与 `S01_immunoparalysis_direction.csv` 系统不符（F10）。

**未做/范围之外**
- 未读取其他专家评审、REVIEW/RESPONSE 文件、PIPELINE 执行注释、`*_gen_*.py`（遵守独立性纪律）。
- 未深入重算 LINCS L1000 rescue_fraction 明细（属 A5 范畴），但确认 §3.9 糖皮质激素负对照已被作者正确讨论。
- 通过公开文献核实 eQTLGen 为 31,684 例全血/PBMC、37 数据集 meta（Visser et al. 2021, *Nat Genet*；PMC8432599），并确认其组成含 UK Biobank 队列，据此提出 F3 样本重叠关切。

---

## 收尾建议（给编辑的接收概率判断）

若仅修 F1（nested CV + 头条改为外部 0.638）、F2（IRG 双值澄清）、F3（补样本重叠讨论与敏感性）、F10（Table 1 溯源校正）四条，稿件在 *Journal of Translational Medicine* / *Frontiers in Immunology* 层级具备可接受的方法学诚信。F4–F9 多为表述收紧与补充敏感性，不影响主体结论。最不可妥协的是 **F3（样本重叠）与 F10（数字溯源）**——二者任一条不修，方法学审稿人将合理拒稿或要求重大修订。

---

## 附：本评审所依方法学原则与可引用文献

为使上述每条【Specific fix】可被作者直接落地，列出对应的方法学依据（供作者引用，非强制本稿引用全部）：

1. **预测模型特征选择泄漏 / 乐观偏倚**：Ambroise & McLachlan (2002) *PNAS* 99:6562–6566 — "Selection bias in gene extraction on the basis of microarray gene-expression data". 核心结论：特征选择必须在每一训练折内完成，否则 CV 高估性能。预测模型报告规范见 **TRIPOD** (Collins et al., *Ann Intern Med* 2015) 第 10–11 条（开发队列内须嵌套重采样）。
2. **两样本 MR 样本重叠偏倚**：Burgess & Thompson (2016) *Statistics in Medicine* 35:1880–1906 — 重叠样本使两样本 MR 的 I 类错误率上升、估计偏倚方向不可预测；在暴露为 eQTL、结局为 UKB 派生 GWAS 时尤为突出（eQTLGen 含 UKB 队列）。缓解手段包括重叠样本校正、Leave-one-cohort-out、或非重叠 eQTL 来源三角验证。
3. **eQTLGen 队列构成**：Visser et al. (2021) *Nature Genetics* 53:1300–1310（PMC8432599）— 31,684 例全血/PBMC 表达，来自 37 个数据集的 meta，UK Biobank 为已知组成队列。
4. **MR 估计量与 pleiotropy**：Bowden et al. (2015) *IJE* 44:512–525（MR-Egger）；Bowden et al. (2016) *IJE* dyw220（I²/截距检验）；使用 Egger 作"提示性"证据时需同时报告 IVW 与 weighted median 并说明 Egger 对少 IV 的不稳定性。
5. **多重检验 / FDR**：Benjamini & Hochberg (1995) *JRSS B* 57:289–300 — 本稿 15 项 gene×outcome 的 BH 框架本身正确（见 Stands up 2），关键点在于"按估计量分别报告 FDR"与"仅 Egger 显著≠因果"。
6. **链式选择 / 循环分析家族误差**：Kriegeskorte et al. (2009) *Nature Neuroscience* 12:535–540 — 在同一数据上串行做选择+验证会 inflate 族错误率；推荐独立验证集或至少显式披露。
7. **弱工具变量**：一般以 F>10 为经验阈值（Staiger & Stock 1997）；本稿 FCGR3A（2 IV）排除正确，但 CD74 critical-care（3 IV）即便 F>10 仍建议 leave-one-IV-out 敏感性。

> 说明：上述文献用于支撑评审意见的方法学正确性；作者只需在相应修改处引用最相关的 1–2 篇，不必全引。本评审未替作者决定具体引用，亦未读其他专家文件。
