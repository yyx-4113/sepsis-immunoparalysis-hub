# A3 · 数字溯源 / 重算审计报告（Implementation & Number-Provenance Audit）

**评审专家角色**：A3 — 数字溯源重算审计员（独立同行评审）
**被审稿件**：`05_reports/manuscript.md`（v1.0.2）
**评审性质**：首次投稿审（first submission）；严格遵守独立性纪律，未读取 `05_reports/review/` 下除 `_PANEL_BRIEF.md` 外的任何文件、未读取任何 `*REVIEW*`/`*RESPONSE*`/`06_literature`/`*_gen_*.py`/`GITHUB_DEPOSIT_SOP.md`/`author_verification_statement.md`/`.workbuddy/`。
**审计方法**：稿件每个可核对数字，逐一与其声明来源的 CSV（`01_data/`、`03_results/` 下）比对；对大型文件做精确计数与重算；不读取任何 43G 原始 `.gctx`。

---

## 0. 总体结论（Verdict）

稿件数字治理的**主体是可复现的**：样本构成、DEG 计数、hub 数、签名 AUC、外部验证 AUC/CIs、细胞定位 r 值、7 个候选药 rescue_fraction、MR 三张表的 OR/CI/P、BH-FDR、中位 F、L1000 背景统计——这些均已逐项核对，**与源文件一致**。

但存在 **1 项严重（critical）、1 项重大（major）、4 项中等（moderate）、5 项轻微（minor）** 数字问题。最严重的是：

- **§3.1 Table 1 整张表的 logFC 与 P 值与唯一声明来源的 `S01_immunoparalysis_direction.csv`（及其同源的 `S01_mars1_deg.csv`）完全不符**；其中 ITGAM 被写成"显著（P=7.0e-12）"，而源文件实际 raw P=1.2e-03 且未通过 FDR。该表连同摘要中重复出现，属必须返修级别的错误。
- **§3.9 lenalidomide 的 wtcs 写成 1.17，源文件实际为 0.2058**（约 5.7 倍偏差），主编已标注，特此独立确认。

摘要、Table 1、§3.9 的上述数字在返修前**不可接受**；其余问题为清晰度/一致性/小幅度偏差，可在 minor revision 中解决。

---

## 1. 逐项发现（Finding-by-Finding）

### [F1] CRITICAL — §3.1 Table 1（及摘要）的 logFC / P 值与声明来源严重不符

**【Problem】** Table 1 列出的 8 个共识免疫基因（HLA-DRB1、CD74、CD14、FCGR3A、ITGAM、HAVCR2、HLA-DRA、LYZ）的 `logFC(Mars1−Other)` 与 P 值，与 §7 数字溯源表声明来源 `03_results/S01_immunoparalysis_direction.csv` 完全不一致；其中 ITGAM 被错误标为"显著"。同一组数字也出现在摘要（manuscript.md:13 与 :24）。

**【Evidence】** 我读取了 `S01_immunoparalysis_direction.csv` 全表（25 行），并交叉核对了同源的 `S01_mars1_deg.csv`（两文件对这 8 个基因的 logFC/P.Value/adj.P.Val **逐位相同**）。逐基因对比如下（源值取 `S01_immunoparalysis_direction.csv`）：

| Gene | 稿件 Table 1 (manuscript.md:87–94) | 源文件实际值 | 是否一致 |
|---|---|---|---|
| HLA-DRB1 | logFC −0.59, P 9.7e-09 | logFC −0.8925, P 2.22e-16 | **不符**（logFC、P 均错） |
| CD74 | −0.48, 8.2e-09 | −0.7578, 4.44e-16 | **不符** |
| CD14 | −0.77, 1.3e-17 | −0.7657, P=0（≈0） | logFC 近似一致；**P 不符**（1.3e-17 vs 实际 0） |
| FCGR3A | −0.55, 1.0e-06 | −0.6097, 3.09e-11 | logFC 接近；**P 不符**（差 ~300×） |
| ITGAM | −0.48, 7.0e-12 | −0.2084, raw P 1.19e-03, adj.P.Val 1.68e-03 | **不符**；且 `DEG_0.3=False`、未达 FDR<0.05，**并非显著** |
| HAVCR2 | −0.39, 1.7e-16 | −0.3488, 7.55e-14 | logFC 接近；**P 不符** |
| HLA-DRA | −0.18, 3.5e-02 | −0.4689, 1.84e-07 | **不符** |
| LYZ | −0.21, 2.9e-04 | −0.2561, 1.92e-06 | logFC 接近；**P 不符**（差 ~15×） |

逐行判定：**一致/不符** —— 8 行中 0 行在 logFC 与 P 上同时与源文件一致；仅 CD14 的 logFC 量级近似（-0.77 vs -0.766），其余要么量级错、要么 P 值错、要么两者皆错。ITGAM 是最大问题：稿件给的是 −0.48 / P=7e-12（"显著"），而源文件是 −0.208（不足 0.3 阈值）/raw P=1.2e-03/未通过 FDR——方向虽同（下调）但量级被夸大 2.3 倍、显著性被错误断言。摘要（manuscript.md:13）亦写 "HLA-DRB1 Δ=−0.59, CD74 Δ=−0.48, CD14 Δ=−0.77, FCGR3A Δ=−0.55, all P<1×10⁻⁸"，同样与源文件偏差。

**【Why it matters】** Table 1 是 §3.1"协调下调"主张的核心证据，且被摘要复述。若这些数字在返修前保留，等于稿件主体声称的"抗原呈递/单核基因强效下调"所引用的具体效应量与显著性，无法从作者自己声明的源文件复现。这对**可信度与接收概率**是致命的——审稿人会直接判定"数字不可溯源"。ITGAM 被误标为显著，会污染"22/25 显著"这一计数在读者心中的可靠性（尽管 22/25 本身正确，见 F-stands-up）。

**【Specific fix】** 用以下英文替换句重写 Table 1 主体（数值直接取自 `S01_immunoparalysis_direction.csv`，保留 3 位小数；P 用源文件 raw `P.Value`）：

> *Table 1. Consensus immune genes down in Mars1 (selected; values directly from `S01_immunoparalysis_direction.csv`).*

| Gene | logFC (Mars1−Other) | raw P | adj.P.Val | Function |
|---|---|---|---|---|
| HLA-DRB1 | −0.89 | 2.2e-16 | 1.1e-15 | MHC-II |
| CD74 | −0.76 | 4.4e-16 | 2.1e-15 | MHC-II invariant chain |
| CD14 | −0.77 | <1e-300 | 0 | monocyte receptor |
| FCGR3A | −0.61 | 3.1e-11 | 9.1e-11 | FcγRIIIa |
| ITGAM | −0.21 | 1.2e-03 | 1.7e-03 | integrin αM (not FDR-significant) |
| HAVCR2 | −0.35 | 7.5e-14 | 2.8e-13 | TIM-3 |
| HLA-DRA | −0.47 | 1.8e-07 | 3.8e-07 | MHC-II |
| LYZ | −0.26 | 1.9e-06 | 3.6e-06 | lysozyme |

并同步改正摘要（manuscript.md:13 与 :24）：将 "HLA-DRB1 Δ=−0.59, CD74 Δ=−0.48, CD14 Δ=−0.77, FCGR3A Δ=−0.55, all P<1×10⁻⁸" 改为基于源文件的 "HLA-DRB1 Δ=−0.89, CD74 Δ=−0.76, CD14 Δ=−0.77, FCGR3A Δ=−0.61, all P<1×10⁻¹⁰"（或等价表述）。务必使 Table 1、摘要、正文三处与 `S01_immunoparalysis_direction.csv` 三位一体一致。

---

### [F2] MAJOR — §3.1 "21 个方向性下调" 与源文件 23 个不符（且表述混淆两个指标）

**【Problem】** §3.1（manuscript.md:81）称"25 个共识免疫基因中 21 个方向性下调、22 个 FDR<0.05 显著"。源文件 `S01_immunoparalysis_direction.csv` 的 `direction` 列实际为 **23 个 Mars1_down、2 个 Mars1_up**（PDCD1、LAG3），并非 21。

**【Evidence】** 我读取 `S01_immunoparalysis_direction.csv`，按 `direction` 列计数：Mars1_down = 23，Mars1_up = 2（PDCD1、LAG3）。按 `adj.P.Val<0.05` 计数：显著 = 22（唯一不显著的是 CD8B 0.077、GZMA 0.11、LAG3 0.55）。因此"22 显著"**一致（正确）**；但"21 方向性下调"无法作为"方向列"的原始计数成立（应为 23）。唯一能让"21"成立的解释是"下调 **且** 显著"= 22 个显著 − 1 个上调且显著的 PDCD1 = 21——但这正是把"方向"与"显著性"两个指标混为一谈的写法。判定：**方向计数不符（23 vs 21）；显著性计数一致**。

**【Why it matters】** 读者会以为 25 个基因里有 21 个下调、4 个不上调，但源文件是 23 个下调、2 个上调。这低估了免疫麻痹信号的"协调下调"强度（23 比 21 更强，其实对作者有利），但表述与源文件对不上，违反数字溯源契约；且"21 下调 + 22 显著"的并列写法在统计上含糊（22 显著里已含 1 个上调的 PDCD1）。

**【Specific fix】** 改为明确、与源文件一致的英文句：

> "Of the 25 consensus immune genes, 23 were directionally downregulated (Mars1_down) and 2 were directionally upregulated (PDCD1, LAG3). Twenty-two of the 25 were significant at FDR<0.05 (21 of the downregulated genes plus PDCD1); PDCD1 and LAG3 were the only upregulated genes, and CD8B/GZMA/LAG3 were not FDR-significant."

---

### [F3] MAJOR — §3.9 lenalidomide 的 wtcs = 1.17 应为 0.2058

**【Problem】** §3.9（manuscript.md:136）称 lenalidomide "wtcs 1.17"，但源文件 `S08_l1000_candidate_scores.csv` 中 lenalidomide 的 `wtcs` 实际为 **0.2058**（偏差约 5.7 倍）。

**【Evidence】** 读取 `S03_... ` 实际文件 `03_results/S08_l1000_candidate_scores.csv`：lenalidomide 行 `rescue_score=0.0439, wtcs=0.2058, rescue_rank=5435, rescue_pct_rank=0.26625`；azithromycin 行 `rescue_score=0.0133, wtcs=0.0626, rescue_rank=9152, rescue_pct_rank=0.44834`。稿件中 rank 5435、pct 26.6%、rescue 0.044 均与源文件一致（一致），**唯独 wtcs 1.17 与源文件 0.2058 不符**。判定：**wtcs 不符（1.17 vs 0.2058）**；其余 lenalidomide/azithromycin 字段一致。azithromycin 的 wtcs 稿件未单列（仅给 rescue 0.013，与 0.0133 一致）。

**【Why it matters】** wtcs 被定义为"iLINCS 式 connect-score 代理"。在稿件叙述里它本用于佐证"两个小分子呈方向性但幅度中等的救援"；若 wtcs 被写成 1.17（远大于 1），会暗示信号相当强，与"modest"的定性自相矛盾，也与同一行的 rescue=0.044（弱）冲突。正确的 0.2058 才支持"modest"结论。错误数值会削弱 §3.9 自洽性。

**【Specific fix】** 将 manuscript.md:136 中 "wtcs 1.17" 改为 "wtcs 0.21"（或保留三位 "0.206"）。建议句：

> "lenalidomide ranked 5,435/20,413 (top 26.6%; rescue 0.044, wtcs 0.21) and azithromycin ranked 9,152/20,413 (≈ median; rescue 0.013, wtcs 0.06)"

---

### [F4] MODERATE — §3.7 / §2.8 的 IFN-γ "4/5 抗原呈递基因" 与 `08_candidates_drugs.csv` 的 5/5 矛盾

**【Problem】** §3.7（manuscript.md:116）与 §2.8 阳性对照门控均称"IFN-γ 救回 4/5 抗原呈递基因（HLA-DRA、HLA-DRB1、HLA-DQA1、CD74）"，但 `03_results/08_candidates_drugs.csv` 中 IFN-γ 的 `rescue_genes` 实为 **5 个**（HLA-DRA;HLA-DRB1;HLA-DQA1;**HLA-DQB1**;CD74），即在其自身 7 个靶基因中的 5 个抗原呈递基因**全部**被救回。

**【Evidence】** 读取 `08_candidates_drugs.csv`：IFN-gamma 行 `n_target_genes=7, n_rescue_mars1down=5, rescue_fraction=0.714, rescue_genes=HLA-DRA;HLA-DRB1;HLA-DQA1;HLA-DQB1;CD74`。而 `08_positive_control_check.csv` 写 "救回 4/5 抗原呈递基因: ['HLA-DRA','HLA-DRB1','HLA-DQA1','CD74']"（缺 HLA-DQB1）。稿件 §3.7 与阳性对照文件一致（4/5），但与候选药文件（5/5，含 HLA-DQB1）**内部矛盾**。判定：**两源文件对 IFN-γ 救回的抗原呈递基因数不一致（4 vs 5），稿件取了 4/5 一侧**。

**【Why it matters】** 这是同一复现包内两个结果文件的直接冲突。若读者核对 `08_candidates_drugs.csv` 会发现IFN-γ 实际救回 5 个（含 HLA-DQB1），与正文的"4/5"不符，动摇"阳性对照门控满足"这一 Tier-2 证据的可溯源性。

**【Specific fix】** 二选一，但必须一致：
(1) 若以候选药表的 7-靶基因为准，则改为 "IFN-γ rescued 5/5 antigen-presentation genes among its 7 targets (HLA-DRA, HLA-DRB1, HLA-DQA1, HLA-DQB1, CD74)"；
(2) 若阳性对照门控定义的是另一个固定的 5-基因集合（不含 HLA-DQB1、含第 5 个非 HLA-DQB1 基因），则必须在 §2.8/§3.7 显式列出该 5 基因集合名称并说明与候选药表的差异。
切勿让两个 CSV 与正文三处给出不同计数。

---

### [F5] MODERATE — 同一队列 E-MTAB-4451 出现两个 IRG 基准（0.619 与 0.604），需澄清"公平比较"口径

**【Problem】** §2.6 / §3.4（manuscript.md:57, :105）称 IRG 基准在 E-MTAB-4451 = **0.619**、在 GSE65682 = 0.648（来自文献 Peng 2023）；而 §3.5 / 摘要 / §7（manuscript.md:108, :13, :219）称"recomputed on the same cohort (0.604)"。同一外部队列给出两个不同 IRG 值，稿件未明确二者关系。

**【Evidence】** 读取 `S06_auc_compare.csv`：`IRG 基准(E-MTAB-4451)=0.619`、`IRG 基准(GSE65682)=0.648`。读取 `09_external_validation.csv`：`auc_IRG3_benchmark_EMTAB4451=0.604`。两者均为真实存在的数字，但**分别来自两个文件、两种口径**：0.619 是文献报道值（标签 "(E-MTAB-4451)"），0.604 是作者在同一队列上重新计算的基准。稿件 §3.5 用 0.604 作为"超越基准"的比较对象（0.638 > 0.604），而 §2.6/§3.4 用 0.619/0.648 作为"已发表基准"的定性参照。判定：**两个数字各自可溯源，但稿件未解释其差异，易让读者误以为同一基准自相矛盾**。

**【Why it matters】** 这是"超越已发表基准"这一核心卖点的统计诚信边界。公平的 apples-to-apples 比较应当是作者自己的签名（0.638）vs 作者自己在同队列重算的 IRG（0.604）——稿件 §3.5 正是这样做的，因此结论成立；但 §2.6/§3.4 引用的 0.619 是文献报告值，若不与 0.604 区分，会被误读为"作者自己复算的基准前后不一致"。

**【Specific fix】** 在 §3.4 与 §3.5 之间增加一句澄清（英文）：

> "The published IRG benchmark is reported as 0.619 (E-MTAB-4451) and 0.648 (GSE65682) by Peng et al. (2023). When we re-derived the same IRG signature on the E-MTAB-4451 processing used here, the benchmark was 0.604; we therefore compare our locked signature against this re-derived, cohort-matched value (0.604) rather than the literature-reported 0.619, to keep the comparison on identical preprocessing."

---

### [F6] MODERATE — §3.2 "中位 −0.79；range −3.65~3.86" 混用亚组与全队列口径；"progressively ordered" 夸大

**【Problem】** §3.2（manuscript.md:99）写"lowest in Mars1 (median −0.79; range −3.65 to 3.86)"，但 −0.79 是 **Mars1 亚组**（n=132）的中位数，而 range −3.65~3.86 是 **全 802 样本**的范围。句法上二者并置，易误读为"Mars1 的中位与范围"。此外"progressively ordered across endotypes"与数据不符。

**【Evidence】** 读取 `S02_immunoparalysis_score.csv`（802 行，含 `immune_function_score` 与 `mars_endotype`）。全队列中位 = −0.0965（非 −0.79），min/max = −3.6496 / 3.8616（即 −3.65~3.86，与稿件 range 一致）。分内型中位：Mars1 = **−0.7917**（与稿件 −0.79 一致）、Mars2 = −0.7527、Mars3 = +0.6405、Mars4 = −0.2347、unassigned = +0.2381。判定：**−0.79 与 Mars1 亚组中位一致（正确）；range 与全队列一致（正确）；但两句并置未标注口径**。且 Mars1(−0.792) 与 Mars2(−0.753) 几乎并列，"progressively ordered"不成立（顺序实为 Mars1<Mars2<Mars4<Mars3，非单调"渐进"）。

**【Why it matters】** 数字本身正确，但口径混淆会误导读者以为 Mars1 的范围是 −3.65~3.86（实际那是全队列）。"progressively ordered"则是对数据的过度陈述，细心的审稿人会用分位数表反驳。

**【Specific fix】** 改为（英文）：

> "The immune-function score was lowest in Mars1 (subgroup median −0.79; the cohort-wide range across all 802 samples was −3.65 to 3.86). Mars1 and Mars2 showed similarly low medians (−0.79 and −0.75), Mars4 was intermediate (−0.23), and Mars3 was highest (+0.64)."

---

### [F7] MINOR — `S06_auc_compare.csv` 与 `09_external_validation.csv` 的 CV-AUC 微差（0.65856 vs 0.6582）

**【Problem】** 同一"GSE65682 交叉验证 AUC"在两个结果文件中数值略有差异。

**【Evidence】** `S06_auc_compare.csv`：`Immune-risk signature (CV)=0.65855758`。`09_external_validation.csv`：`auc_GSE65682_CV_locked=0.6582`。差异约 0.0004，二者四舍五入均为稿件所报的 0.659。判定：**两者都"约等于 0.659"，但与源文件两处不完全一致（微差）**。

**【Why it matters】** 不影响结论（均≈0.659），但同一指标在不同结果文件中应完全一致，否则显得复现包未最终锁定。属低优先级一致性问题。

**【Specific fix】** 在 PIPELINE/复现说明中注明两文件应由同一锁定脚本产出，或将 `09_external_validation.csv` 的 `auc_GSE65682_CV_locked` 改为与 `S06_auc_compare.csv` 完全一致的 0.65856；稿件维持 0.659 即可。

---

### [F8] MINOR — MR 的 GWAS 病例/对照计数（1896/484588 等）不在结果 CSV，需 run-log 佐证

**【Problem】** §2.10 / §3.10（manuscript.md:69, :143, :158）给出的 GWAS 样本量（ieu-b-5086: 1896/484588；ieu-b-4980: 11643/474841；ieu-b-4982: 1380/429985）未出现在任何 `*_mr*.csv` 结果文件中，属于 OpenGWAS 元数据。

**【Evidence】** 我核对的 `10_genetics_mr_outcome5086_28ddeath.csv`、`10_genetics_mr.csv`、`10_genetics_mr_outcome4982_criticalcare.csv` 及其 `*_harmonised.csv` 均不含这些总样本量计数，仅含每个基因的 SNP 级 harmonised 数据（含每 SNP 的 F 统计量，见 Stands-up）。判定：**这些计数无法从所给结果文件核实（无法核实）**，但稿件明确声称，且 `05_reports/s10_run_log*.txt` 与 `02_scripts/python/10_genetics_mr_run.py` 据 §2.10 应留存 API 响应证据。

**【Why it matters】** 样本量是 MR 效力讨论的基础（§5 限性 2 称"1,896 cases underpowered"）。若这些数字无法溯源，会削弱局限性的可信度。

**【Specific fix】** 在 Data availability / 方法补充中注明这些计数取自 OpenGWAS API（`ieu-b-5086` 等）的响应头，并保留 `s10_run_log*.txt` 作为可复核证据；或在脚注写明检索日期与 API 版本。

---

### [F9] MINOR — 参考文献 1–29 连续且作者-年份引用可对应，但建议自动化核对映射

**【Problem】** 编号 1–29 连续无缺；正文多为作者-年份引用。需确认每个正文引用都能映射到列表条目、且列表条目均被引用。

**【Evidence】** 我通读 manuscript.md 参考文献段（manuscript.md:270–298）与正文引用：编号 1–29 连续。关键支撑性引用均能对应——Scicluna 2017=L4（§1）、Peng 2023 fimmu.1152117=L16（§2.6 IRG 基准）、Docke 1997=L13（IFN-γ）、Meisel 2009=L12（GM-CSF）、Francois 2018=L11（IL-7）、McDaniel 2011=L23（lenalidomide）、Netea 2016/2011=L14/L20（BCG/trained immunity）、Li 2015=L19（thymosin）、Parnham 2014=L25（azithromycin）、Ritchie 2015=L6（limma）、Hemani 2018=L10（MR-Base）、Bowden 2015/2016=L28/L21（MR-Egger）、Verbanck 2018=L24（pleiotropy）、Newman 2015/2019=L8/L9（deconvolution）、Langfelder 2008=L27（WGCNA）、Subramanian 2017=L7（L1000）、Davenport 2016=L5（E-MTAB-4451）、ArrayExpress=L15、GEO=L26、Hotchkiss 2013=L17、van der Poll 2017=L22、Schuemie 2013=L18、Aran 2017=L1、Boomer 2011=L2、Singer 2016=L3、Basham 1983=L29。判定：**编号连续、主要引用均能映射（一致）**；但作者-年份式引用未使用方括号编号，未做逐条自动化映射核对（无法核实每一条无遗漏/无错配）。

**【Why it matters】** 低优先级；若某条正文引用张冠李戴（如把 L16 的 IRG 基准误归于其他作者），会影响方法可信度。

**【Specific fix】** 提交前用脚本将正文作者-年份与 29 条参考条目做一次自动匹配校验，确保无悬空引用、无错配；或改用方括号编号引用以便机械核对。

---

### [F10] MINOR — §3.8 引用 "Table S2" 但未作为补充表呈现

**【Problem】** §3.8（manuscript.md:131）写"Table S2; full: `03_results/08b_clinical_translation.csv`"，但稿件正文中并未呈现任何名为 Table S2 的表格，仅给出 CSV 指针。

**【Evidence】** 通读 manuscript.md：除 Table 1、Table 2、Table 3、Table 4 外，仅在 §3.8 出现"Table S2"字样，无对应表格实体。判定：**Table S2 被引用但未呈现（一致地指向了存在的 CSV，但补充表未随稿提供）**。

**【Why it matters】** 多数期刊要求补充表随稿提交；仅给 CSV 指针而不附可读补充表，会在技术审查阶段被要求补件。

**【Specific fix】** 在投稿包中加入可读的 Table S2（由 `08b_clinical_translation.csv` 渲染），或在正文改为"clinical-readiness details in `08b_clinical_translation.csv` (provided as Supplementary Table S2)"并确保该补充文件随稿上传。

---

### [F11] OK-NOTE — §8 已正确标注"delete before submission"

**【Problem】** 无问题，记录以备完整性。

**【Evidence】** manuscript.md:235 标题为 "Pre-submission journal targeting (planning note; delete before submission)"，且 §8 全段为内部选刊规划（含 IF/ quartile 与"mechanism-demanding top-tier"等编辑性判断）。判定：**已正确标注删除标记（一致）**。

**【Why it matters】** 确认作者未把内部选刊/竞争力评估误带入正式稿件；该节内容若随稿提交会显得不专业，现已妥善标记。

**【Specific fix】** 投稿前确实删除 §8 整节即可；无需修改。

---

## 2. § Stands up（经我独立核查后确认稿件正确的项）

以下为我**曾怀疑但核对后确认稿件与源文件一致**的项；每条附源文件证据。共 18 条，远超下限 10 条。

1. **802 样本构成**（manuscript.md:42）：`GSE65682_pheno.csv` 行数 = 802；`group` 计数 sepsis=760 / healthy=42（一致）；`mars_endotype` 中 Mars1=132、Mars2=176、Mars3=118、Mars4=53、unassigned=323（一致）；`death_28d` 1.0=114、0.0=365、unassigned=323（一致）。
2. **"479 有内型 AND 28d 生存"**：端型已赋值 479、死亡已赋值 479；二者交集（同时非 unassigned）= **479**（一致）——确证 323 个未赋值样本在两列上完全重合，数字精确。
3. **Sepsis-vs-healthy DEG 448**（manuscript.md:96）：`S01_deg_sepsis_vs_ctrl.csv` 中 `DEG_0.3==True` 计数 = **448**（一致；注意该文件含全部 11,519 基因，448 是 flagged 子集）。
4. **Mars1-vs-Other DEG 3597**（manuscript.md:81）：`S01_mars1_deg.csv` 中 `DEG_0.3==True` 计数 = **3,597**（一致）。
5. **25 共识免疫基因中 22 个 FDR<0.05 显著**（manuscript.md:81）：`S01_immunoparalysis_direction.csv` 中 `adj.P.Val<0.05` 计数 = **22**（一致；唯一不显著为 CD8B 0.077、GZMA 0.11、LAG3 0.55）。
6. **6 个 hub 基因**（manuscript.md:102）：`S05_hub_genes.csv` 列出 FIS1、HAVCR2、HLA-DQA1、CD14、FCGR3A、CD74，三法（lasso/rf/univariate）均为 True（一致）。
7. **CV AUC 0.659 / 训练 0.750**（manuscript.md:105）：`S06_auc_compare.csv` 中 `Immune-risk signature (CV)=0.65856`（→0.659）、`(train)=0.74951`（→0.750）（一致）。
8. **Mars1 二元分类 AUC 0.578**（manuscript.md:99）：`S06_auc_compare.csv` 中 `Mars1 endotype=0.57819`（一致）。
9. **外部验证 AUC 0.638（CI 0.532–0.748）**（manuscript.md:108）：`09_external_validation.csv` 中 `auc_EMTAB4451_orientedSum=0.6382`、`_CI95_low=0.5317`、`_CI95_high=0.7475`（一致）。
10. **锁定 L1 权重 AUC 0.585（CI 0.469–0.696）**（manuscript.md:108）：`09_external_validation.csv` 中 `auc_EMTAB4451_external_locked=0.5848`、`_CI95_low=0.4687`、`_CI95_high=0.6959`（一致）。
11. **29/30 基因映射、52 死/54 活、HLA-DQA1 缺失**（manuscript.md:108）：`09_external_validation.csv` 中 `n_signature_genes_mapped_EMTAB4451=29`、`n_deaths=52`、`n_survivors=54`、`genes_missing_in_test=HLA-DQA1`（一致）。
12. **细胞定位 r 值**（manuscript.md:113）：`07_hub_celltype.csv` 给出 CD14 0.773、FCGR3A 0.491、CD74→Dendritic 0.690、HAVCR2 0.298、HLA-DQA1→B_cell 0.681（与稿件 0.77/0.49/0.69/0.30/0.68 一致）；`07_axis_celltype.csv` 给出 CD4_Tcell 0.6176、CD8_Tcell 0.5822、Dendritic 0.4587（与稿件 0.62/0.58/0.46 一致）。
13. **7 候选药 rescue_fraction**（manuscript.md:122–128，Table 2）：`08_candidates_drugs.csv` 给出 IL-7 1.0(5/5)、GM-CSF 0.833(5/6)、IFN-γ 0.714(5/7)、Azithromycin 0.667(2/3)、Lenalidomide 0.4(2/5)、Thymosin α1 0.4(2/5)、BCG 0.2(1/5)（与 Table 2 全一致）。
14. **L1000 背景统计**（manuscript.md:134）：`S08_l1000_rescue_trtcp.csv`（20,413 行）中 rescue_score 均值 0.0064、中位数 0.0055、>0 比例 0.5362、最大值 0.3182（与稿件 mean/median 0.006、53.6%>0、top rescue 0.32 一致）；化合物总数 20,413（与稿件一致）。
15. **MR Table 3 全部 OR/CI/P**（manuscript.md:151–156）：`10_genetics_mr_outcome5086_28ddeath.csv` 中 CD74/HLA-DQA1/CD14/HAVCR2/FIS1 的 IVW、MR-Egger、Weighted median 的 or_/ci_lo/ci_hi/p、Cochran Q_p、I² 与稿件 Table 3 逐位一致；FCGR3A `status=insufficient_instruments`（与"not assessed"一致）；CD14 Egger p=0.00511（=5.1e-3，一致）。
16. **MR Table 4 三结局 IVW**（manuscript.md:164–168）：`10_genetics_mr.csv`（易感性 ieu-b-4980）、`10_genetics_mr_outcome5086_28ddeath.csv`（28d）、`10_genetics_mr_outcome4982_criticalcare.csv`（危重）三文件的 IVW or_/ci/p 与稿件 Table 4 逐位一致；CD74 危重 IVW 2.2217(1.175–4.200)p=0.014（一致）。
17. **中位 F 统计量与 BH-FDR 0.026 可复现**：由 `10_genetics_mr_outcome5086_harmonised.csv` 逐基因 per-SNP `F` 取中位数，得 CD74 35.4、HLA-DQA1 168.1、CD14 45.7、HAVCR2 36.4、FIS1 75.0（与 Table 3 "Median F" 一致）。将三结局文件共 15 个 MR-Egger p 做 BH 校正，CD14（primary）p=0.00511 排第 3，BH-FDR = 0.00511×15/3 = 0.0255 ≈ **0.026**（与稿件声称一致）。
18. **CD74 危重 Egger "null intercept, P=1.00" 与 CD74 易感 Egger "intercept P=1.0e-4"**：`10_genetics_mr_outcome4982_criticalcare.csv` CD74 Egger `egger_intercept_p=0.99987`（→1.00，一致）；`10_genetics_mr.csv` CD74 Egger `egger_intercept_p=9.98e-05`（→1.0e-4，一致）且其 Egger or_=1.118、p=1.65e-4（与稿件 OR 1.118、P=1.7e-4 一致）。

---

## 3. § Questions for the authors（需作者澄清，不替作者作答）

1. **Table 1 的 −0.59/−0.48/−0.55/−0.39/−0.18/−0.21 等数值来自哪次分析？** 我核对了 `S01_immunoparalysis_direction.csv` 与同源的 `S01_mars1_deg.csv`，两文件对这 8 个基因的 logFC/P 完全一致（如 HLA-DRB1 −0.893/2.2e-16），均与稿件不符。请说明稿件 Table 1 数值的生成来源；若确为旧版/另一归一化产出，请提供对应文件或重新从 `S01_immunoparalysis_direction.csv` 生成。
2. **ITGAM 在稿件中被标为显著（P=7.0e-12），但源文件 raw P=1.2e-03、adj.P.Val=1.7e-03 且 `DEG_0.3=False`。** 这是数据错误还是另有显著性定义？请解释。
3. **§3.1 "21 方向性下调" 的精确定义是什么？** 源文件 direction 列为 23 个 Mars1_down。若意指"下调且显著"，应为 21（22 显著 − PDCD1 上调），请确认并改写以避免与"22 显著"混淆。
4. **lenalidomide 的 wtcs 1.17 与源文件 0.2058 的差异来源？** 请确认应以 `S08_l1000_candidate_scores.csv` 的 0.2058 为准并修订稿件。
5. **IFN-γ 救回 4/5 还是 5/5 抗原呈递基因？** `08_positive_control_check.csv` 给 4/5（不含 HLA-DQB1），`08_candidates_drugs.csv` 给 5/5（含 HLA-DQB1）。请明确两个文件的"抗原呈递基因"集合定义并统一正文。
6. **IRG 基准 0.619 与 0.604 的关系**：0.619 是否为 Peng 2023 文献报道值、0.604 是否为作者在同队列重算？请在 §3.4–§3.5 显式区分，避免读者误读为同一基准前后矛盾。
7. **MR 的 GWAS 样本量（1896/484588 等）** 是否已在 `05_reports/s10_run_log*.txt` 留存 API 响应证据？请确认可在返修时提交该 run log 作为溯源。
8. **§3.2 的"中位 −0.79"是否确为 Mars1 亚组中位（全队列中位实为 −0.10）？** 请确认并区分亚组与全队列口径；同时"progressively ordered"是否应改为"Mars1 与 Mars2 同为最低、Mars3 最高"的更精确描述。

---

## 4. § What I actually checked（读的文件、运行的核对、重算差异逐条）

### 4.1 读取并逐项比对的源文件
- `01_data/GSE65682/GSE65682_pheno.csv`（802 行；group / mars_endotype / death_28d 计数与交集）
- `03_results/S01_deg_sepsis_vs_ctrl.csv`（11,519 行；`DEG_0.3` 计数）
- `03_results/S01_mars1_deg.csv`（11,519 行；`DEG_0.3` 计数；8 个 Table 1 基因取值）
- `03_results/S01_immunoparalysis_direction.csv`（25 行；down/sig 计数；8 个 Table 1 基因取值；与 S01_mars1_deg 同源核对）
- `03_results/S02_immunoparalysis_score.csv`（802 行；全队列与分内型 median/range）
- `03_results/S05_hub_genes.csv`（6 hub）
- `03_results/S06_auc_compare.csv`（CV/train/Mars1/IRG 基准）
- `03_results/S06_signature_genes.csv`（30 基因）
- `03_results/09_external_validation.csv`（外部验证全指标）
- `03_results/07_hub_celltype.csv`、`07_axis_celltype.csv`（r 值）
- `03_results/08_candidates_drugs.csv`、`08_positive_control_check.csv`（候选药与 IFN-γ 门控）
- `03_results/S08_l1000_candidate_scores.csv`、`S08_l1000_positive_control.csv`、`S08_l1000_rescue_trtcp.csv`（L1000 候选分、阳性对照、背景统计 20,413 化合物）
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv`、`10_genetics_mr.csv`、`10_genetics_mr_outcome4982_criticalcare.csv`、`10_genetics_mr_outcome5086_harmonised.csv`（MR 三结局 + 工具变量 F）
- `04_figures/` 目录（确认 `fig_s09_external_roc.png`、`fig_s10_l1000_rescue.png` 均存在，非伪造对接图）
- 稿件 `manuscript.md` 全文（重点 §2.1/§3.1/§3.2/§3.3/§3.4/§3.5/§3.6/§3.7/§3.9/§3.10/§7/§8）

### 4.2 运行的数字核对 / 重算（与稿件差异逐条）

| # | 稿件主张 | 源文件实际 | 判定 |
|---|---|---|---|
| 1 | 802 样本；760/42；479 有内型+28d | pheno 802；sepsis 760/healthy 42；交集 479 | 一致 |
| 2 | sepsis-vs-healthy DEG 448 | S01_deg_sepsis `DEG_0.3`=448 | 一致 |
| 3 | Mars1-vs-Other DEG 3597 | S01_mars1 `DEG_0.3`=3597 | 一致 |
| 4 | 21 方向性下调 / 22 显著 | direction 列 23 down / 22 sig(adj<0.05) | **down 不符(23 vs 21)；sig 一致** |
| 5 | Table1 HLA-DRB1 −0.59/9.7e-09 | −0.893/2.2e-16 | **不符** |
| 6 | Table1 CD74 −0.48/8.2e-09 | −0.758/4.4e-16 | **不符** |
| 7 | Table1 CD14 −0.77/1.3e-17 | −0.766/P=0 | logFC 近似；**P 不符** |
| 8 | Table1 FCGR3A −0.55/1.0e-06 | −0.610/3.1e-11 | logFC 近似；**P 不符** |
| 9 | Table1 ITGAM −0.48/7.0e-12 | −0.208/raw 1.2e-03(不显著) | **不符（含错误标显著）** |
| 10 | Table1 HAVCR2 −0.39/1.7e-16 | −0.349/7.5e-14 | logFC 近似；**P 不符** |
| 11 | Table1 HLA-DRA −0.18/3.5e-02 | −0.469/1.8e-07 | **不符** |
| 12 | Table1 LYZ −0.21/2.9e-04 | −0.256/1.9e-06 | logFC 近似；**P 不符** |
| 13 | 免疫评分中位 −0.79；range −3.65~3.86 | Mars1 亚组中位 −0.792；全队列 −3.65~3.86 | 数值一致；**口径混淆** |
| 14 | 6 hub | S05 6 基因 | 一致 |
| 15 | CV AUC 0.659 / 训练 0.750 | 0.65856 / 0.74951 | 一致（四舍五入） |
| 16 | Mars1 AUC 0.578 | 0.57819 | 一致 |
| 17 | 外部 0.638 (0.532–0.748) | 0.6382 (0.5317–0.7475) | 一致 |
| 18 | 锁定 L1 0.585 (0.469–0.696) | 0.5848 (0.4687–0.6959) | 一致 |
| 19 | IRG 重算 0.604 | 09 文件 0.604 | 一致；但与 S06 0.619 并存（见 F5） |
| 20 | 29/30 映射；52 死/54 活 | 09 文件 29/30；52/54 | 一致 |
| 21 | 细胞 r：CD14 0.77/FCGR3A 0.49/CD74 0.69/HAVCR2 0.30/HLA-DQA1 0.68；轴 CD4 0.62/CD8 0.58/Dendritic 0.46 | 07 文件全对应 | 一致 |
| 22 | 7 候选 rescue：1.00/0.83/0.71/0.67/0.40/0.40/0.20 | 08 文件全对应 | 一致 |
| 23 | IFN-γ 4/5 AP 基因 | 08_positive 4/5；08_candidates 5/5(含 DQB1) | **内部矛盾** |
| 24 | lenalidomide wtcs 1.17 | 0.2058 | **不符** |
| 25 | L1000 背景 mean/median 0.006；53.6%>0；top 0.32；20,413 化合物 | 0.0064/0.0055；53.6%；0.318；20,413 | 一致 |
| 26 | MR Table3 OR/CI/P（5 基因×3 法） | 5086 文件逐位 | 一致 |
| 27 | MR Table4 IVW 三结局 | 三文件逐位 | 一致 |
| 28 | CD14 Egger P=5.1e-3；intercept P=0.34 | 0.00511；0.344 | 一致 |
| 29 | BH-FDR 0.026（15 检验） | 重算 0.0255≈0.026 | 一致 |
| 30 | 中位 F 35.4/168.1/45.7/36.4/75.0 | harmonised 中位 | 一致 |
| 31 | CD74 危重 IVW 2.222(1.175–4.200)p0.014 | 2.2217(1.175–4.200)0.014 | 一致 |
| 32 | CD74 危重 Egger "null intercept P=1.00" | intercept_p 0.99987 | 一致 |
| 33 | CD74 易感 Egger OR 1.118/P1.7e-4/intercept P1.0e-4 | 1.118/1.65e-4/9.98e-5 | 一致 |
| 34 | IRG 基准 0.619(S06)/0.648(S06) | S06 0.619/0.648 | 一致；与 09 的 0.604 并存（F5） |
| 35 | S06 CV 0.65856 vs 09 CV 0.6582 | 微差 0.0004 | **微不一致（F7）** |
| 36 | MR 样本量 1896/484588 等 | 不在结果 CSV | 无法核实（F8） |
| 37 | 参考文献 1–29 连续 | 列表连续；主要作者-年份可映射 | 一致（建议自动核对） |
| 38 | Table S2 引用 | 仅 CSV 指针，无表实体 | 轻微（F10） |
| 39 | §8 "delete before submission" | 已标注 | 一致（F11） |

### 4.3 结论性说明
- **无需读取 43G 原始 `.gctx`**：所有可核数字均已通过 `03_results/*` 聚合 CSV 完整复核。
- **未违反独立性纪律**：未读取 `05_reports/review/` 下除 `_PANEL_BRIEF.md` 外的任何文件、未读历史评审/`06_literature`/`*_gen_*.py`。
- **优先级排序**：F1（Table 1 整表）/ F3（wtcs）为返修阻断项；F2/F4/F5/F6 为重大/中等需在修回中解决；F7–F11 为 minor。

---

**审计完成。** 报告已写入 `05_reports/review/A3_implementation.md`。
