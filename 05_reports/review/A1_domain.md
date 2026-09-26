# A1 评审报告 — 临床 / 脓毒症免疫学领域专家（独立同行评审）

**评审稿件**：`05_reports/manuscript.md`（v1.0.2）
**评审角色**：A1 · 脓毒症 / 重症医学 / 免疫学临床领域专家
**评审立场**：首次投稿视角，未参考任何历史修订或其他专家意见；所有判断均来自稿件文本与本人亲自核对的源文件 / 文献。
**总体判断**：这是一项设计诚实、分层清晰（Tier-1/2/3）的计算重定位研究，其生物学主干（Mars1 = 抗原呈递 / 单核枢纽基因协调下调）在临床上是站得住的，且作者对自己证据强度的自述总体克制。但存在**一处会直接阻碍接收的数据溯源硬伤**（§3.1 Table 1 数值无法追到所引源文件）、**若干临床证据强度的过高表述**（IL-7/GM-CSF/IFN-γ），以及**一处从计算提名跳跃到临床处方的外推**。这些问题多为"措辞与溯源"级，可在修改轮解决；不属于结论性推翻。

---

## 一、必查数字实地核对摘要（领域相关项）

| 稿件主张 (manuscript.md) | 核对结果 | 结论 |
|---|---|---|
| §1 Mars1 28-day mortality 39% | Scicluna 2017 原文："35 (39%) of 90" Mars1 患者 28 天死亡 | ✅ 准确，归因正确 |
| §3.1 Table 1 各基因 Δ & P（HLA-DRB1 −0.59 等 5 例 + ITGAM/HLA-DRA/LYZ） | 与 `S01_immunoparalysis_direction.csv` 及 `S01_immunoparalysis_genes_in_mars1.csv` **全部不符**（见 F1） | ❌ 溯源失败 |
| §3.1 "22/25 significant (FDR<0.05)" | CSV 中 adj.P.Val<0.05 者恰为 22/25 | ✅ 准确 |
| §3.1 "21/25 directionally down" | CSV `direction` 列 23/25 为 Mars1_down（仅 PDCD1、LAG3 上调） | ⚠️ 计数不符（见 F6） |
| §3.7 Table 2 rescue_fraction（IL-7 1.00 … BCG 0.20） | 与 `08_candidates_drugs.csv` 完全一致 | ✅ 准确 |
| §3.7 "IFN-γ rescued 4/5 抗原呈递基因" | `08_positive_control_check.csv` 记 4/5；但 `08_candidates_drugs.csv` 列 IFN-γ 救援 5 个 HLA-II 基因 | ⚠️ 内部不一致（见 F7） |
| §3.8 候选药机制注释 | 与 `08b_clinical_translation.csv` 机制一致，生物学合理 | ✅ 合理（但措辞需校正，见 F2/F3） |

---

## 二、主要发现

### F1【Problem】§3.1 Table 1 引用的效应量与 P 值无法追到其所声明的源文件 `S01_immunoparalysis_direction.csv`，且与该文件及另一独立结果文件均严重不符。

【Evidence】稿件 `manuscript.md:81` 及 Table 1（`manuscript.md:87-92`）给出：
- HLA-DRB1 Δ=−0.59 (P=9.7e-09)
- CD74 Δ=−0.48 (P=8.2e-09)
- CD14 Δ=−0.77 (P=1.3e-17)
- FCGR3A Δ=−0.55 (P=1.0e-06)
- HAVCR2 Δ=−0.39 (P=1.7e-16)
- 另 Table 1 续行列：ITGAM Δ=−0.48 (P=7.0e-12)、HLA-DRA Δ=−0.18 (P=3.5e-02)、LYZ Δ=−0.21 (P=2.9e-04)

本人核对 `03_results/S01_immunoparalysis_direction.csv`（第 2–26 行，logFC/P.Value/adj.P.Val/direction 列）与 `03_results/S01_immunoparalysis_genes_in_mars1.csv`（同名基因相同数值，两文件互为独立佐证），对应值为：
- HLA-DRB1 logFC **−0.8925**，P.Value **2.2e-16**（非 −0.59 / 9.7e-09）
- CD74 logFC **−0.7578**，P.Value **4.4e-16**（非 −0.48 / 8.2e-09）
- CD14 logFC **−0.7657**，P.Value 下溢为 0.0（与 −0.77 量级一致，P 极显著）
- FCGR3A logFC **−0.6097**，P.Value **3.1e-11**（非 −0.55 / 1.0e-06）
- HAVCR2 logFC **−0.3488**，P.Value **7.5e-14**（非 −0.39 / 1.7e-16）
- ITGAM logFC **−0.2084**，P.Value **1.2e-03**（非 −0.48 / 7.0e-12）
- HLA-DRA logFC **−0.4689**，P.Value **1.8e-07**（非 −0.18 / 3.5e-02）
- LYZ logFC **−0.2561**，P.Value **1.9e-06**（非 −0.21 / 2.9e-04）

方向（全部下调）在两文件中均与稿件一致，**因此"协调下调"的生物学结论未被推翻**；但稿件引用的**具体幅度与多个 P 值**（尤其 HLA-DRB1、CD74、HLA-DRA、ITGAM）与所引源文件相差数倍至数个数量级，且稿件数值系统性偏小（ITGAM 反而偏大），不符合单一归一化或缩放误差的模式，提示稿件可能转录自一次已被替换的早期运行，或指向了错误的文件。§7 数字溯源表（manuscript.md:214）将这组数直接指认给 `S01_immunoparalysis_direction.csv`，而该文件并不含这些数——这是一个可复现性阻断点。

【Why it matters】对一份以"每个报告数字都可追到具体输出（§7）"为卖点的计算生物学稿件，核心结果表的首个证据块（免疫麻痹信号）无法被读者从所引文件复现，会直接触发审稿人对全部数字可信度的质疑，并在编辑初审即可能被要求补证。结论本身（下调）稳，但"可审计"的承诺在此处落空。

【Specific fix】二选一，但必须二选一并显式声明：
> **选项 A（采用当前源文件值）**——将 Table 1 改写为当前提交文件的值，例如：
> "HLA-DRB1 Δ=−0.89 (P<2.2×10⁻¹⁶); CD74 Δ=−0.76 (P<4.4×10⁻¹⁶); CD14 Δ=−0.77 (P<1×10⁻¹⁶); FCGR3A Δ=−0.61 (P=3.1×10⁻¹¹); HAVCR2 Δ=−0.35 (P=7.5×10⁻¹⁴); HLA-DRA Δ=−0.47 (P=1.8×10⁻⁷); ITGAM Δ=−0.21 (P=1.2×10⁻³); LYZ Δ=−0.26 (P=1.9×10⁻⁶). All values recomputed from the committed file `S01_immunoparalysis_direction.csv` (Mars1−Other moderated-t logFC)."
> **选项 B（若稿件数值来自某次合法但不同的对比/运行）**——在 §7 与 Table 1 脚注中**指明产生 −0.59/−0.48 等数值的确切文件与对比定义**（如"Mars1 vs sepsis-only 子集"或某次未提交的早轮），并确保该文件进入版本库；否则不得保留这些数。
无论选哪项，§3.1 的"sub-unit but highly significant"定性判断在两套数值下都成立，无需改动。

---

### F2【Problem】§3.8 将 IL-7 与 GM-CSF 表述为"carry the strongest sepsis/immunoparalysis RCT evidence"，在脓毒症免疫治疗文献语境下夸大了证据强度与性质。

【Evidence】稿件 `manuscript.md:131`："IL-7 and GM-CSF carry the strongest sepsis/immunoparalysis RCT evidence (restoring monocyte HLA-DR and lymphocyte pools)". 本人核对外部文献：
- GM-CSF：在脓毒症中的 G-CSF/GM-CSF 合并分析（12 项 RCT、2,380 例，Crit Care 2011;15:R58）显示 28 天死亡率无显著改善（RR 0.93, 95% CI 0.79–1.11, P=0.44），院内死亡率亦无差异；GM-CSF 仅显著提高"感染逆转率"，结论为"目前无证据支持脓毒症中常规使用 G-CSF/GM-CSF"。这与稿件同段承认"mechanism-anchored"但用"strongest RCT evidence"的措辞形成张力——此处"证据"实为**生物标志物（单核细胞 HLA-DR）复苏**证据，而非**临床终点（死亡率）**证据。
- IL-7：IRIS-7（Francois 2018, JCI Insight, ref 11）为 n=27 的 II 期、双盲、安慰剂对照试验，主要终点是安全性与逆转淋巴细胞减少；CYT107 使绝对淋巴细胞计数升高 3–4 倍，**未对死亡率做效力检验**。后续更大试验（Ann Intensive Care 2023;13:17，NCT03821038）实际仅入组 21 例。故 IL-7 属**小型 pilot**，而非"最强 RCT 证据"。
- 稿件自身的 `08b_clinical_translation.csv` 其实写得更准（"Phase I/II RCTs…raises naive & central-memory T cells"；"RCTs show restored monocyte HLA-DR & cytokine production"），但 §3.8 把这份更谨慎的 CSV 折叠成了"strongest RCT evidence"的强表述。

【Why it matters】"strongest RCT evidence"在脓毒症免疫治疗领域极易被读作"疗效证据最强"，而真实情况是 GM-CSF 死亡率 RCT 多中性/阴性、IL-7 仅 pilot。这会误导临床读者对候选药成熟度的判断，削弱稿件作为"诚实分层"陈述的整体信誉，并可能在本刊（Journal of Translational Medicine）被方法学/临床审稿人直接质疑。

【Specific fix】将 `manuscript.md:131` 改写为：
> "Among the repositioned candidates, IL-7 and GM-CSF have the most direct RCT support, but this support is predominantly at the biomarker level — restoration of lymphocyte counts by IL-7 (IRIS-7, n=27) and of monocyte HLA-DR by GM-CSF (Meisel 2009, n=38) — rather than demonstrated survival benefit; meta-analyses of GM-CSF in sepsis have not shown a mortality advantage (RR 0.93, 95% CI 0.79–1.11). IFN-γ has established MHC-II–inducing biology and small historical sepsis signals. Azithromycin, lenalidomide, thymosin α1 and BCG remain hypothesis-generating (Table S2)."

---

### F3【Problem】"IFN-γ is an approved MHC-II inducer"措辞不精确，易被误解为 IFN-γ 以"MHC-II 诱导剂"身份获批用于脓毒症。

【Evidence】稿件 `manuscript.md:131`："IFN-γ is an approved MHC-II inducer with small sepsis signals". IFN-γ 的获批适应症是慢性肉芽肿病（CGD）等（稿件 `08b_clinical_translation.csv` 第 4 行亦写"Approved for chronic granulomatous disease"），并非"作为 MHC-II 诱导剂获批"。其作为 MHC-II 主诱导剂是**生物学机制事实**（Basham 1983, ref 29；Docke 1997, ref 13 在脓毒症单核细胞上去活化模型中证实），而非监管适应症。将"approved"与"MHC-II inducer"直接拼接，混淆了"获批药物"与"机制角色"。

【Why it matters】临床/药学审稿人会将其视为监管声称错误；在 Translational Medicine 类期刊，关于"已批准适应症"的措辞需精确。该问题不影响生物学正确性，但损害表述严谨性。

【Specific fix】将 `manuscript.md:131` 改写为：
> "IFN-γ, an approved immunomodulator (indicated for chronic granulomatous disease) and the canonical master inducer of MHC class II, has shown only small sepsis immunorestorative signals."

---

### F4【Problem】§4 讨论将"计算提名"直接外推为"哪类 Mars1 患者最可能从某药获益"的临床分层处方，缺乏本研究任何证据支撑。

【Evidence】稿件 `manuscript.md:182`："Mars1 patients with dominant APC suppression may benefit most from IFN-γ/GM-CSF, whereas those with T-cell exhaustion may prefer IL-7." 本句做出两条具体临床主张：(i) APC 抑制主导的 Mars1 患者最可能从 IFN-γ/GM-CSF 获益；(ii) T 细胞耗竭主导者更宜用 IL-7。然而：
- 全文无任何"按患者 APC 抑制 vs T 细胞耗竭程度分层并匹配药物反应"的分析（无亚组、无患者级轴-药物对应、无功能学数据；S11 仅为止血蓝本未执行）。
- "benefit most / prefer"是疗效与优选结论，远超本研究"in-silico 机制锚定 + 连接度评分"的能力边界。
- 这与稿件整体自诩的"honest about maturity / Tier-3 hypothesis-generating"立场自相矛盾，是简报明确警示的"从计算提名跳到有望临床获益"的典型外推。

【Why it matters】这是最容易被临床编辑/审稿人判为"over-interpretation"的语句，会拉低讨论的可信度，并可能成为拒稿或大修的聚焦点。其生物学"设想"本身合理，但作为本研究结论呈现则不实。

【Specific fix】将 `manuscript.md:182` 改写为（保留设想、降级为假设）：
> "Mechanistically, the shortlist spans distinct restorative strategies — IFN-γ/GM-CSF rebuild antigen presentation and myeloid function, IL-7 counters T-cell exhaustion, BCG draws on trained immunity. *A priori*, one might hypothesize that Mars1 patients with dominant APC suppression could be enriched for response to IFN-γ/GM-CSF and those with dominant T-cell exhaustion to IL-7; this stratification is a hypothesis to be tested in the S11 functional assays and in prospective trials, and is not a conclusion of the present in-silico analysis."

---

### F5【Problem】参考文献（29 条）在"脓毒症免疫治疗 RCT 证据强度"这一核心论断上遗漏了关键文献，导致 §3.8 的强弱判断缺乏对立证据支撑。

【Evidence】稿件 §3.8 断言 IL-7/GM-CSF 证据"最强"，但参考文献中：
- **缺失 GM-CSF 脓毒症死亡率 meta 分析**（如 Nouira/Crit Care 2011;15:R58，12 RCT/2380 例，中性结果；及更早的 GM-CSF 专门 meta 分析）。该文直接决定"strongest RCT evidence"是否成立，必须被引用以平衡表述。
- **缺失近期（2020–2024）脓毒症免疫治疗综述 / RCT 现状文**（如针对免疫麻痹靶向治疗的年度综述、检查点抑制剂在脓毒症中的试验），使"strongest"缺乏时间维度校准。
- **缺失 HAVCR2/TIM-3（稿件 §3.1 将 TIM-3 列为耗竭标志、§4 提 T 细胞耗竭）对应的脓毒症检查点阻断文献**（抗 PD-1/PD-L1 在脓毒症的临床前与早期临床证据）。稿件高度重视"耗竭轴"，却未引该轴最相关的在研免疫治疗文献，是领域覆盖缺口。
- Hotchkiss/Singer 免疫麻痹综述（ref 17）、van der Poll（ref 22）均已纳入，基础框架合格；但"临床证据强度"论断需要上述对立/校准文献才站得住。

【Why it matters】在评审"候选药临床证据强度"时，若只列支持性 RCT（Meisel 2009、Francois 2018）而不列中性 meta 分析与近期现状，等于让审稿人替作者补全反面证据；这会显著降低 §3.8 的可信度，也违背 Translational Medicine 对"证据层级"的期待。

【Specific fix】在 §3.8 或 Discussion 增加文献并改写论断，例如新增引用句：
> "Meta-analyses of GM-CSF (and G-CSF) across >2,000 septic patients have not demonstrated a mortality benefit, so the RCT signal for these candidates should be read as biomarker-restoration rather than efficacy evidence [add: Nouira et al., Crit Care 2011;15:R58; and a 2022–2024 sepsis immunotherapy review]."
并建议在引言/讨论补入 TIM-3/PD-1 检查点阻断在脓毒症的文献，以匹配稿件对"耗竭轴"的强调。

---

### F6【Problem】§3.1 "21/25 方向性下调"的计数与源文件 `direction` 列（23/25 Mars1_down）不符，且"directionally downregulated"定义未给出。

【Evidence】稿件 `manuscript.md:81`："Of 25 consensus immune genes, 21 were directionally downregulated and 22 were significant (FDR<0.05)". 核对 `S01_immunoparalysis_direction.csv`：25 个基因中 `direction == Mars1_down` 者为 **23**（仅 PDCD1、LAG3 为 Mars1_up）；`adj.P.Val < 0.05` 者确为 **22**（与稿件一致）。故"22 significant"准确，"21 down"与文件给出的 23 down 相差 2。若"directionally downregulated"指"下调且通过 |logFC|≥0.3"，则 CSV 中 DEG_0.3=True 且 down 者为 15，亦非 21；若指"下调且显著"则为 22。三种合理解释均不得到 21，提示该计数可能来自一份未提交的中间定义或被误算。

【Why it matters】虽不影响"多数下调"的定性，但与同句"22 significant"并列时，21 vs 22 的并列关系本身在读者看来应互为子集而实际不自洽，构成小但可被挑出的内部不一致，且再次指向 §3.1 数字与源文件的对齐问题（与 F1 同源）。

【Specific fix】将 `manuscript.md:81` 改为与源文件一致的陈述，并显式定义标准：
> "Of 25 consensus immune genes, 23 were directionally downregulated (Mars1_down) and 22 were significant at FDR<0.05; 21 were both downregulated and passed the |logFC|≥0.3 threshold."
（或作者确认其"consensus immune genes"集合的精确定义后，采用该定义下真实的 down 计数，并在 §7 标注该集合来源文件。）

---

### F7【Problem】IFN-γ 抗原呈递救援在两份结果文件中计数不一致（阳性对照文件记 4/5，候选药文件列 5 个 HLA-II 基因）。

【Evidence】稿件 `manuscript.md:116`："IFN-γ rescued 4/5 antigen-presentation genes (HLA-DRA, HLA-DRB1, HLA-DQA1, CD74)". 核对 `03_results/08_positive_control_check.csv` 第 2 行：`detail = "救回 4/5 抗原呈递基因: ['HLA-DRA', 'HLA-DRB1', 'HLA-DQA1', 'CD74']"`（4 个，无 HLA-DQB1）。但 `03_results/08_candidates_drugs.csv` 第 4 行 IFN-γ 的 `rescue_genes = HLA-DRA;HLA-DRB1;HLA-DQA1;HLA-DQB1;CD74`（5 个，均为 HLA-II 基因）。即同一候选在两份提交文件中的救援基因列表不一致：候选药文件含 HLA-DQB1，阳性对照文件不含。两处均满足"≥3/5"阳性对照门槛，故**不影响 Tier-2 门控结论**，但内部不一致需在修改中统一。

【Why it matters】方法学审稿人会要求阳性对照的"分子清单"与候选药表的"分子清单"一致；当前差异虽小，却暴露了结果文件间未交叉校验，与 F1 的溯源问题同源，宜一并清理。

【Specific fix】统一两份文件对 IFN-γ 的抗原呈递救援基因列表，并在 `manuscript.md:116` 据统一后的清单改写，例如：
> "IFN-γ rescued 5/5 queried antigen-presentation genes (HLA-DRA, HLA-DRB1, HLA-DQA1, HLA-DQB1, CD74), satisfying the positive-control gate (≥3/5)."
或若有意排除 HLA-DQB1，须在 `08_positive_control_check.csv` 与 `08_candidates_drugs.csv` 同时注明排除理由（如"不在 22-gene Mars1-down 轴内"）。

---

### F8【Problem】将 28-day mortality 作为唯一主终点时，未说明现代脓毒症 RCT 日益采用 90-day mortality 的趋势，可能被视为终点选择的时效盲区。

【Evidence】稿件 §2.6、§3.4、§3.5、§3.10 及摘要均以 28-day mortality 为主终点，并与 MARS 原队列（Scicluna 2017 用 28 天）、E-MTAB-4451（28-day survival）、MR 主结局 ieu-b-5086（"death within 28 days"）对齐——**内部一致性良好，且 28 天是脓毒症文献中的标准终点之一**，故此项并非错误。但 2020 年后的脓毒症 RCT 与很多观察性研究已将 90-day mortality 作为优先主终点（更敏感捕捉免疫麻痹驱动的"迟发死亡/继发感染"），稿件 Limitations 未提此点。

【Why it matters】属次要时效说明缺口。不影响结论，但补充后可 preempt 临床审稿人"为何不用 90 天"的追问，并强化"终点对齐"的方法论自觉。

【Specific fix】在 §5 Limitations 增一句：
> "We used 28-day mortality to align with the MARS endotype derivation and the E-MTAB-4451 and UK Biobank sepsis phenotypes; 90-day mortality is increasingly adopted as the primary endpoint in modern sepsis RCTs and may capture additional late immunoparalysis-related deaths, so our signature's performance at 90 days remains to be established."

---

## 三、§ Stands up（本人怀疑、但核查后认为稿件正确的地方）

1. **Mars1 39% 28-day mortality 准确且归因正确。** 本人核对 Scicluna et al., Lancet Respir Med 2017 原文："at 28 days, 35 (39%) of 90 people with a Mars1 endotype had died (HR 1.86 … p=0.0045)"。稿件 `manuscript.md:33` 的引用与数值完全吻合，且"immunosuppressed subtype defined by downregulated HLA class-II / antigen-presentation / monocytic programs"亦符合该文对 Mars1 的定义。原怀疑其可能混淆了发现队列与验证队列死亡率，核查后确认无误。

2. **"22/25 significant at FDR<0.05"准确。** 核对 `S01_immunoparalysis_direction.csv`，adj.P.Val<0.05 者恰为 22/25（PDCD1 虽上调但显著，计入 22）。本人原怀疑"25 共识基因"集合可能含非显著基因导致计数偏差，核查后确认 22 无误。

3. **候选药机制注释生物学可信， rescue_fraction 与 `08_candidates_drugs.csv` 完全一致。** IL-7（T 细胞稳态/抗耗竭）、GM-CSF（髓系/单核激活）、IFN-γ（MHC-II 主诱导剂）、阿奇霉素（大环内酯免疫调节）、来那度胺（共刺激+HLA-II 上调）、胸腺肽 α1（DC/单核成熟）、BCG（训练免疫）的机制 claim 均有文献支撑且与 `08b_clinical_translation.csv` 一致。本人原怀疑"rescue_fraction"可能混入了疗效含义，核查后确认其仅为"靶基因∩Mars1-down / 靶基因"的词汇重叠指标，稿件在 §2.8 已明确定义，未越界。

4. **IFN-γ 作为 MHC-II 主诱导剂、IL-7 抗 T 细胞耗竭、GM-CSF 髓系激活的生物学 claim 正确。** 这三条是免疫学共识（Basham 1983 ref 29；Docke 1997 ref 13；IRIS-7 ref 11；Meisel 2009 ref 12），稿件未将其错误表述为"临床已验证有效"，仅在机制层使用，符合领域事实。

5. **28-day mortality 作为主终点的内部一致性成立。** 签名（§3.4/§3.5）、外部验证（E-MTAB-4451 28-day survival）、MR 主结局（ieu-b-5086 "death within 28 days"）三者终点定义对齐，且均与 MARS 原队列一致；未发现 28 天 vs 院内 vs 90 天的混淆。本人原怀疑 MR 结局可能用了不同时间窗，核查后确认对齐。

6. **"immunoparalysis"定义与临床文献一致。** 稿件将免疫麻痹表述为"迟发死亡与继发感染驱动、抗原呈递/T 细胞耗竭"，与 Hotchkiss 2013（ref 17）、Boomer 2011（ref 2）、van der Poll 2017（ref 22）的界定吻合，未见定义性偏差。

---

## 四、§ Questions for the authors（需作者澄清，不代答）

1. **§3.1 Table 1 的 −0.59/−0.48/−0.18 等数值来自哪次运行 / 哪个文件？** 当前提交的 `S01_immunoparalysis_direction.csv` 与 `S01_immunoparalysis_genes_in_mars1.csv` 均给出大得多的幅度（HLA-DRB1 −0.89、CD74 −0.76、HLA-DRA −0.47）。请指明产生稿件数值的权威文件与对比定义；若已被替换，请说明为何 §7 仍指向旧值。

2. **"21/25 directionally downregulated"中"directionally downregulated"的操作定义是什么？** 源文件 `direction` 列 23/25 为 Mars1_down；若采用"下调且 |logFC|≥0.3"则为 15；若"下调且显著"则为 22。请给该集合的精确定义与对应文件。

3. **IFN-γ 抗原呈递救援应记为 4/5 还是 5/5？** `08_positive_control_check.csv` 列 4 个（无 HLA-DQB1），`08_candidates_drugs.csv` 列 5 个 HLA-II 基因（含 HLA-DQB1）。两份文件以哪份为准？HLA-DQB1 是否应计入抗原呈递轴？

4. **§3.8 "strongest RCT evidence"是否仅指生物标志物（mHLA-DR、淋巴细胞计数）层面的 RCT，而非死亡率疗效？** 请确认修订时是否接受 F2 的降级表述；若作者坚持"strongest"包含疗效含义，请提供支持 GM-CSF/IL-7 死亡率获益的 RCT 证据。

5. **（可选）28-day vs 90-day：** 作者是否拥有 90-day mortality 的可用表型以做敏感性分析？若没有，是否同意在 Limitations 显式说明该终点局限（见 F8）？

---

## 五、§ What I actually checked（本人实际核对范围）

- **读取并通读** `05_reports/manuscript.md` 全文（§1–§8、参考文献 1–29）。
- **核对 `03_results/S01_immunoparalysis_direction.csv`**（25 行基因 × logFC/P.Value/adj.P.Val/DEG_0.3/direction）：确认 (a) 方向全部下调（23/25 Mars1_down，仅 PDCD1、LAG3 上调）；(b) 22/25 adj.P.Val<0.05；(c) 稿件 Table 1 的 8 个示例 Δ/P 与该文件**全部不符**（F1）。
- **交叉核对 `03_results/S01_immunoparalysis_genes_in_mars1.csv`**：同名基因 logFC 与上一文件完全一致（如 HLA-DRB1 −0.8925），证实稿件 Table 1 数值不来自这两份已提交文件。
- **核对 `03_results/08_candidates_drugs.csv`**：Table 2 的 7 个 rescue_fraction（1.00/0.833/0.714/0.667/0.40/0.40/0.20）与机制注释与稿件 `manuscript.md:120-128` 完全一致。
- **核对 `03_results/08b_clinical_translation.csv`**：发现其 `clinical_status_in_sepsis` 字段比 §3.8 更谨慎（IL-7 "Phase I/II RCTs"、GM-CSF "RCTs show restored monocyte HLA-DR"、IFN-γ "Approved for chronic granulomatous disease"），证实 §3.8 把更谨慎的底层 CSV 折叠成了过强表述（F2/F3 依据）。
- **核对 `03_results/08_positive_control_check.csv`**：IFN-γ 记 4/5（无 HLA-DQB1），与 `08_candidates_drugs.csv` 的 5 个 HLA-II 基因不一致（F7）。
- **外部文献核对（Web）**：
  - Scicluna 2017 原文确认 Mars1 28-day mortality = 35/90 = 39%（HR 1.86, p=0.0045）→ §1 准确（Stands up #1）。
  - GM-CSF/G-CSF 脓毒症 meta 分析（Crit Care 2011;15:R58，12 RCT/2380 例）：28-day mortality RR 0.93 (95% CI 0.79–1.11, P=0.44)，院内死亡率无差异 → 支撑 F2（"strongest RCT evidence"夸大）。
  - IL-7 IRIS-7（JCI Insight 2018;3:e98960）：n=27，II 期，主要终点安全性+逆转淋巴细胞减少，3–4 倍淋巴细胞升高，未做死亡率效力检验；后续 NCT03821038 仅入组 21 例 → 支撑 F2（IL-7 仅 pilot）。
- **未读取**（遵守简报禁止清单）：`05_reports/review/` 下除 `_PANEL_BRIEF.md` 外的任何文件、PIPELINE.md 执行说明、`06_literature/`、`*_gen_*.py`、`GITHUB_DEPOSIT_SOP.md`、`author_verification_statement.md`、`.workbuddy/`。
- **未运行**任何重算脚本或 git 操作；所有数值比对均基于直接读取提交的结果 CSV 与文献原文。

---

## 六、给作者的修订优先级建议（领域视角）

- **阻断级（必须修，否则可退修/拒）**：F1（§3.1 Table 1 溯源硬伤，含 F6 计数）。
- **重要级（强烈建议修，影响接收概率）**：F2（GM-CSF/IL-7 证据强度）、F4（§4 临床外推）、F3（IFN-γ 措辞）、F5（补齐对立文献）。
- **次要级（ polish）**：F7（IFN-γ 计数一致性）、F8（90-day 终点说明）。
- 整体：生物学主干（Mars1 = 抗原呈递/单核枢纽协调下调、可预后、可药）经核查成立，作者自述的证据层级（Tier-1 正、Tier-3 假设生成）在绝大多数位置是诚实的；论文价值在于"外部验证签名 + 机制锚定重定位 + 显式阴性 MR"的组合，而非任何单点的强因果 claim。修正上述表述与溯源后，具备在 Journal of Translational Medicine（Q1）送外审的资格。
