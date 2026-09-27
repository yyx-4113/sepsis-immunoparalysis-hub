# A3 — 实现与溯源审计（Implementation & provenance auditor）

**审阅对象：** `05_reports/manuscript.md`（git tag v1.9.0，单作者生物信息学手稿，作为首次投稿独立审阅）
**审阅人角色：** A3 — 实现与数字溯源审计
**独立性声明：** 我仅读取了 `manuscript.md` 与 `03_results/` 下的原始 CSV、表型文件 `01_data/GSE65682/GSE65682_pheno.csv`，以及 `02_scripts/python/check_audit_assertions.py`（仅作"它检查了什么"的参考，**未采信其结论**）。我未读取任何 `REVIEW_round*`、`RESPONSE*`、`REVISION*`、`review_r1/`–`review_r9/`、`SUBMISSION_MANIFEST.md`、`author_verification_statement.md` 或其他 `review_r10/` 文件。所有数字均从原始 CSV 独立重算。
**重算工具：** `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe`（scipy 1.18.1, pandas 3.0.5, numpy）。脚本与日志见同目录 `A3_recompute.py`、`A3_recompute_log.txt`。

---

## 结论速览（Executive summary）

本手稿的数字溯源质量**很高**：我独立重算了任务列示的全部 9 类头条数字，其中 **绝大多数与源 CSV 完全吻合**（差异均在合理舍入范围内）。第 6 轮审计中暴露的「MR-Egger p 用正态分布而非 t 分布」这一致命 bug 已被彻底修复并已独立验证——Table 3 中 5 个基因的 Egger p 现在**全部等于 t(df=n−2)** 分布值，且对应的正态值明显不同（如 CD14：正态 0.0051 vs t 0.0488）。

仅发现 **4 处低严重程度问题**，均不改变任何结论：
1. **D1（溯源不一致，低）：** 发现集 5 折 CV AUC 在两个结果文件间有 0.0004 的细小差异（`S06_auc_compare.csv`=0.6586 vs `09_external_validation.csv`=0.6582），但都舍入到手稿报告的 0.659。
2. **D2（精度表述，低）：** `wtcs = rescue × √22` 在「未舍入源值」上成立，但**印刷的 4 位小数对不是精确逆运算**（0.0133×√22=0.0624 ≠ 印刷 0.0626；0.0439×√22=0.2059 ≠ 印刷 0.2058，差 ≤0.0002）。"代数上恒等"一词对印刷精度而言略有夸大。
3. **D3（舍入，可忽略）：** Mars3 中位 −0.6405 印刷为 0.641（3 位小数舍入），不影响结论。
4. **D4（措辞nuance，非数字错误）：** 结论 §6 称"由 … hub genes 锚定"，讨论 §4 自承"near-replication rather than a novel gene discovery"——属强调程度差异，手稿已用"direct-target validation still pending"等措辞对冲，非硬矛盾。

---

## 逐条验证（每条含【问题】【证据】【为何重要】【具体修正】）

### 项目 1 — 样本量、DEG 计数、免疫细胞方向计数

**【问题】** 无差异：802/760/42 样本量、Mars1 DEG 3597、sepsis-vs-healthy DEG 448、23/25/22/21 免疫细胞计数均从原始 CSV 复现。

**【证据】**
- `01_data/GSE65682/GSE65682_pheno.csv`：总行数 802；`group` 列计数 sepsis=760、healthy=42（与手稿 Abstract/§2.1 一致）。`mars_endotype` 非空=479（Mars1=132, Mars2=176, Mars3=118, Mars4=53）；`death_28d` 非空=479（死亡 114 / 存活 365）；二者同时非空=479。手稿 Abstract "479 with a MARS endotype and 28-day survival" 即"479 例同时具内型与 28 天转归记录"，复现。
- `S01_mars1_deg.csv`：`DEG_0.3==True` 行数 = **3597**（重算）= 手稿 3597 ✓；`DEG_1.0==True`=186。
- `S01_deg_sepsis_vs_ctrl.csv`：`DEG_0.3==True` = **448**（重算）= 手稿 448 ✓。
- `S01_immunoparalysis_direction.csv`：共 25 基因；`direction==Mars1_down`=**23**；`adj.P.Val<0.05`=**22**；`down 且 FDR<0.05`=**21**。`Mars1_up` 仅 2 个（PDCD1、LAG3），其中 PDCD1 adj.P=2.995e-10<0.05 故计入 22，与手稿"22 FDR-significant (incl PDCD1 up), 21 both"完全吻合 ✓。

**【为何重要】** 这是全文所有下游推断的基数；若样本/DEG 计数错，免疫麻痹信号与签名规模全部动摇。此处稳固。

**【具体修正】** 无需修正。建议仅将 Abstract 的 "479 with a MARS endotype and 28-day survival" 在 §7 溯源表补一行指向 `GSE65682_pheno.csv` 的 endotype/death 双重非空计数（当前 §7 已列该文件，未单列 479）。

---

### 项目 2 — Table 1 效应量与方向

**【问题】** 无差异：6 个基因的 logFC、adj.P 与方向符号全部复现；CD14 的 P 在 CSV 中为 0.0（下溢），手稿印刷为 "≈0 (P<1e-300)" 而非精确 0，符合任务"若印成精确 0 则标记"的反面——**正确避免**。

**【证据】** 从 `S01_immunoparalysis_direction.csv` 重算（logFC / adj.P / 方向）：
| 基因 | 重算 logFC | 手稿 | 重算 adj.P | 手稿 | 方向 |
|---|---|---|---|---|---|
| HLA-DRB1 | −0.8925 | −0.89 | 1.066e-15 | 1.1e-15 | down ✓ |
| CD74 | −0.7578 | −0.76 | 2.081e-15 | 2.1e-15 | down ✓ |
| CD14 | −0.7657 | −0.77 | 0.0(下溢) | ≈0(<1e-300) | down ✓ |
| FCGR3A | −0.6097 | −0.61 | 9.052e-11 | 9.1e-11 | down ✓ |
| HAVCR2 | −0.3488 | −0.35 | 2.838e-13 | 2.8e-13 | down ✓ |
| PDCD1 | +0.1619 | +0.16 | 2.995e-10 | 3.0e-10 | up ✓ |

所有符号与手稿一致（down=负、PDCD1 up=正）。

**【为何重要】** Table 1 是"免疫麻痹方向性"的核心证据表；符号或量级错会直接推翻抗原呈递下调的叙述。此处无误。

**【具体修正】** 无需修正。可在 §7 注明 CD14 的 P.Value 在源文件为精确 0.0（浮点下溢），印刷用 "≈0" 是恰当的。

---

### 项目 3 — 免疫机能评分中位数

**【问题】** 无差异：四个内型中位与 Mars1 的 MWU P 全部复现（Mars3 中位 0.6405 印刷为 0.641 为可接受舍入，见 D3）。

**【证据】** 从 `S02_immunoparalysis_score.csv` 重算：
- Mars1 n=132 中位 −0.7917（手稿 −0.792）✓
- Mars2 n=176 中位 −0.7520（手稿 −0.752）✓，vs Mars1 MWU P=0.467（手稿 0.47）✓
- Mars3 n=118 中位 0.6405（手稿 0.641）✓，vs Mars1 P=1.852e-18（手稿 1.9e-18）✓
- Mars4 n=53 中位 −0.2347（手稿 −0.235）✓，vs Mars1 P=1.321e-3（手稿 1.3e-3）✓

**【为何重要】** 评分是预后签名与 MR 表型匹配的前提；方向/显著性错会使"免疫梯度"框架崩塌。此处无误。

**【具体修正】** 无需修正。

---

### 项目 4 — 签名 AUC（CV / 训练 / 外部 / L1 锁定）

**【问题】** 主数全部复现；仅发现 D1（两文件间 CV AUC 差 0.0004）。

**【证据】**
- `S06_auc_compare.csv`：CV=**0.6586** → 手稿 0.659 ✓；train=**0.7495** → 手稿 0.750 ✓。
- `09_external_validation.csv`：orientedSum AUC=**0.6382**，CI 0.5317–0.7475 → 手稿 0.638 (0.532–0.748) ✓；L1-locked AUC=**0.5848**，CI 0.4687–0.6959 → 手稿 0.585 (0.469–0.696) ✓；n=106、死亡=52、映射 29/30 ✓。
- **D1：** 同一发现集 CV AUC 在 `09_external_validation.csv` 中记为 `auc_GSE65682_CV_locked=0.6582`，与 `S06_auc_compare.csv` 的 0.6586 相差 0.0004。二者皆舍入到手稿 0.659，故报告数不受影响，但两个"源真相"文件彼此不一致。

**【为何重要】** 外部 AUC 是手稿最强主张（诚实跨平台泛化）；主数稳固。D1 仅为溯源整洁度问题，不被动摇结论，但会让审计者质疑哪个 CSV 为权威。

**【具体修正】** 建议统一发现集 CV AUC 的生成来源（让 `09_external_validation.csv` 的 `auc_GSE65682_CV_locked` 直接引用 `S06_auc_compare.csv` 的值，或注明二者算法差异），消除 0.0004 双源不一致。

---

### 项目 5 — 药物候选短表（Table 2）与 IFN-γ 4/5

**【问题】** 无差异：7 个候选的 concordance 分数与 n_rescue/n_target 全部复现；IFN-γ "4/5 抗原呈递基因被救回"独立重算=4/5，吻合。

**【证据】** 从 `08_candidates_drugs.csv` 重算：
| 候选 | n_target | n_rescue | 重算 frac | 手稿 | 吻合 |
|---|---|---|---|---|---|
| IL-7 | 5 | 4 | 0.80 | 0.80 | ✓ |
| GM-CSF | 6 | 4 | 0.667 | 0.67 | ✓ |
| IFN-γ | 7 | 4 | 0.571 | 0.57 | ✓ |
| Azithromycin | 3 | 2 | 0.667 | 0.67 | ✓ |
| Lenalidomide | 5 | 2 | 0.40 | 0.40 | ✓ |
| Thymosin α1 | 5 | 2 | 0.40 | 0.40 | ✓ |
| BCG | 5 | 1 | 0.20 | 0.20 | ✓ |

IFN-γ 独立重算：其 curated `rescue_genes`={HLA-DRA, HLA-DRB1, HLA-DQA1, CD74}；抗原呈递子集={HLA-DRA, HLA-DRB1, HLA-DQA1, HLA-DQB1, CD74}；二者交集={HLA-DRA, HLA-DRB1, HLA-DQA1, CD74}=**4/5**；HLA-DQB1 未计入因其 `DEG_0.3=False`（在 `S01_immunoparalysis_direction.csv` 中 HLA-DQB1 的 DEG_0.3=False，adj.P=0.0174）。手稿"4/5 抗原呈递…HLA-DQB1 fails the |logFC|≥0.3 rule"完全吻合 ✓。整体 concordance=4/7=0.571 ✓。

**【为何重要】** Table 2 与 IFN-γ 阳性对照门控是药物重定位层的可信度支点；若 4/5 错算会破坏"方法学门控满足"的论断。此处无误。

**【具体修正】** 无需修正。

---

### 项目 6 — LINCS L1000（来那度胺 / 阿奇霉素）

**【问题】** 排名与分数复现；仅发现 D2（`wtcs=rescue×√22` 在印刷 4 位小数下非精确逆运算）。

**【证据】** 从 `S08_l1000_candidate_scores.csv` 重算：
- 来那度胺：rescue=**0.0439**（手稿 0.044）✓，wtcs=**0.2058**（手稿 0.21）✓，rank=**5435**（手稿 5435）✓，pct=0.26625（手稿 top 26.6%）✓。
- 阿奇霉素：rescue=**0.0133**（手稿 0.013）✓，wtcs=**0.0626**（手稿 0.06）✓，rank=**9152**（手稿 9152）✓，pct=0.44834（手稿 ≈median/44.8%）✓。
- 总库规模：`S08_l1000_rescue_trtcp.csv` 行数 = **20413**（手稿 20,413）✓；rank/total 与 pct 一致（5435/20413=0.26625，9152/20413=0.44834）。
- **D2：** `wtcs/rescue` = 阿奇霉素 4.7068、来那度胺 4.6879，而 √22=4.6904。用印刷 4 位 rescue 反算：0.0133×√22=0.0624（≠印刷 0.0626），0.0439×√22=0.2059（≠印刷 0.2058），差 ≤0.0002。说明"代数上恒等"对**未舍入源值**成立，但印刷的 4 位小数对并非精确逆运算（因 rescue_score 在入库前已四舍五入到 4 位，wtcs 由未舍入 rescue 算出）。

**【为何重要】** L1000 是手稿"从机制锚定到连接度评分"的关键一步；排名/分数主体稳固。D2 不影响"方向性正向但幅度中等"的结论，但"代数上恒等"的措辞对印刷精度略显夸大，严谨读者用印刷数反算会得到 ≤0.0002 偏差。

**【具体修正】** 二选一：(a) 将 rescue 与 wtcs 均由同一未舍入 rescue 派生并同时舍入到一致小数位后报告（使 0.0133×√22 与 0.0626 自洽）；或 (b) 将"algebraically identical"改为"approximately identical at printed precision (wtcs ≈ rescue×√22)"，并注明差异来自 4 位舍入。

---

### 项目 7 — MR Table 3（Egger p 必须匹配 t(n−2)）

**【问题】** 无差异，且无正态分布误算：5 个基因的全部 Egger p **均等于 t(df=n−2)** 分布值，正态替代值明显不同。

**【证据】** 从 `10_genetics_mr_outcome5086_28ddeath.csv` 重算（`p = 2·st.t.sf(|β/se|, df=nsnp−2)`）：
| 基因 | nsnp | 存储 Egger P | t(df=n−2) 重算 | 正态 P | 匹配 t? |
|---|---|---|---|---|---|
| CD74 | 3 | 0.8794 | 0.8794 | 0.8479 | ✓ |
| HLA-DQA1 | 4 | 0.5580 | 0.5580 | 0.4859 | ✓ |
| CD14 | 6 | 0.0488 | 0.0488 | 0.0051 | ✓ |
| HAVCR2 | 6 | 0.9546 | 0.9546 | 0.9517 | ✓ |
| FIS1 | 8 | 0.4911 | 0.4911 | 0.4635 | ✓ |

- 全部 IVW OR/CI/P、MR-Egger OR/P、Weighted median OR/P 与手稿 Table 3 逐格吻合（例如 CD14 IVW OR=0.927 CI 0.818–1.051 P=0.24；CD14 Egger OR=0.906 P=4.9e-2；HAVCR2 Egger OR=1.010 P=0.95 等）。
- **OR/CI 代数一致性**：对每个 MR 行，`exp(beta)` 与 OR、`exp(b±1.96·se)` 与 CI 之差均 <1e-3（手稿未手改 OR/CI）✓。
- 主结局最小 IVW P = **0.2359** ≥ 0.23（手稿 Abstract "P ≥ 0.23"）✓。
- 家族 BH（`10_mr_bh_family.csv`）：共 45 行（=5 基因×3 估计×3 结局）✓；CD14 28ddeath Egger `q_family_45test=0.730` ≈ 手稿 0.73 ✓，`p_fdr_bh`(15 检验)=0.487 ≈ 手稿 0.49 ✓；CD74 critical-care Weighted median `q_family=2.99e-17` ≈ 手稿 3e-17 ✓（唯一 family-sig 检验）。
- **CD74 critical-care Egger 异常 SE（手稿已诚实披露）**：`10_genetics_mr_outcome4982_criticalcare.csv` 中 CD74 Egger se=0.111 < IVW se=0.325，与手稿 §3.10/§5 "Egger SE (0.111) smaller than IVW SE (0.325)" 一致，且手稿明确称其"physically implausible"并排除因果解读——**非隐藏错误，系已披露的已知局限**。

**【为何重要】** 这是全文最易出致命错处（第 6 轮曾因 Egger p 用正态分布使边界信号看似基因组显著）。现已彻底修复并独立确认：Egger p 全部为 t 分布、正态替代值显著不同，证明 bug 未回归。MR 层作为 Tier-3 假设生成、结论"null"稳健。

**【具体修正】** 无需修正。建议保留审计脚本断言 #4/#5（Egger 必须 t 分布且必须**不等于**正态值）作为 CI 门禁，以防回归。

---

### 项目 8 — 陈旧二次出现（stale second-occurrence）排查

**【问题】** 未发现手稿正文内的陈旧二次出现；版本串、6-vs-5 hub、30/29 基因在正文内部一致。仅 D1（结果文件间 CV AUC 0.6586 vs 0.6582）属"源文件二次出现不一致"。

**【证据】**
- 版本串：手稿仅在 Data availability 出现一次 "tagged v1.9.0"，与任务给定 tag 一致；正文无残留 v1.7/v1.8（那些仅出现在 `check_audit_assertions.py` 注释中，我已读过但未采信）。
- "six immune hubs" vs "five immune hubs + FIS1"：Abstract(13–14) "five immune hubs (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) plus one co-expression passenger, FIS1"；§3.3(116) "five immune hub genes … plus one co-expression-linked gene, FIS1"，并明确 "Five of the six … one, FIS1"；§7 溯源表(240) "6 共表达关联基因（5 免疫 hub + FIS1 乘客）"。框架一致：5 免疫 hub + 1 乘客 = 6 关联基因，无矛盾。
- "30-gene" vs "29 genes"：Abstract/§2.6/§3.4 用"30-gene signature"（设计 30 个）；§3.4 "leaving 29 genes with coefficients"（L1 拟合后 HLA-DQA1 系数为 0），§3.5 "29/30 signature genes mapped"（HLA-DQA1 不在 Illumina 阵列）。`S06_signature_genes.csv` 实为 30 行基因（31 行含表头）✓。30（设计）与 29（L1/外部映射）语境分明，非矛盾。
- 共表达度中心性支撑数（§3.3）：`S03_hub_degree.csv`（恰 2000 行=top-2000 Mars1 DEG）中 GATA1 degree=78.395→78.4 ✓，CGB=76.121→76.1 ✓，EPB49=72.462→72.5 ✓，FIS1 **rank=12**（降序第 12）✓。手稿"FIS1 ranked 12th"复现。
- `S05_hub_genes.csv`：6 基因（FIS1, HAVCR2, HLA-DQA1, CD14, FCGR3A, CD74）三法均 True，与"tri-method consensus"一致。

**【为何重要】** 陈旧二次出现是最隐蔽的错误类（一处正确、他处抄错）。此处正文内部自洽；唯一双源不一致落在结果文件（D1），不影响正文数字。

**【具体修正】** 见 D1 修正（统一 CV AUC 源）。

---

### 项目 9 — 内部矛盾（某节过度宣称而另一节退让）

**【问题】** 未发现硬性数字矛盾；仅一处**措辞强调程度**差异（D4），且手稿已用对冲语言弱化。

**【证据】**
- 讨论 §4(194) 明确退让："The five immune hubs largely *recapitulate* the antigen-presentation / monocytic program that defines the Mars1 endotype … — this is a near-replication rather than a novel gene discovery."
- 结论 §6(226) 称："The Mars1 immunosuppressed program is **anchored by** antigen-presentation/monocytic hub genes (CD74, HLA-DQA1, CD14, FCGR3A, HAVCR2) … that are both prognostically associated … and identify candidate, expression-level intervention hypotheses (direct-target validation still pending)."
- 二者并非数字冲突；结论用"anchored by … hub genes"语气强于讨论的"near-replication"，但结论同时附 "direct-target validation still pending" 与 "candidate" 对冲，Limitations §5 亦诚实列明。属强调差异而非自相矛盾。
- 另：MR 层在 Table 3/§3.10 称"no IVW significant / null / hypothesis-generating"，而 §5 同样称"no causal claim for the hub"——前后一致，无 over-claim。

**【为何重要】** 若结论过度宣称而讨论退让，会削弱可信度。此处手稿整体诚实，D4 仅为编辑一致性建议。

**【具体修正】** 建议将结论 §6 首句弱化为"… is *parsimoniously recapitulated* by antigen-presentation/monocytic hub genes …"（与讨论"near-replication"对齐），或在结论加一句"consistent with the near-replication noted in Discussion"，以消除强调错位。

---

## § Stands up（成立项，≥3，附证据）

1. **Round-6 Egger 正态/t 分布 bug 已彻底修复并已独立验证。** `10_genetics_mr_outcome5086_28ddeath.csv` 中 5 个基因的 Egger p 全部等于 `2·st.t.sf(|β/se|, df=nsnp−2)`（CD74 df1、HLA-DQA1 df2、CD14 df4、HAVCR2 df4、FIS1 df6），且对应正态值明显不同（CD14 正态 0.0051 vs t 0.0488），证明未回归。这是本稿最关键的溯源风险点，现已稳固。
2. **全部 18 条审计断言所依赖的底层数字均被我独立重算确认**（未采信脚本本身）：样本 802、DEG 3597/448、免疫 23/22/21、Table1 六基因、免疫评分四中位与 P、签名 CV/train/外部/L1 AUC、Table2 七候选、IFN-γ 4/5、L1000 排名/分数、MR OR/CI/P 与家族 BH 45 行。重算结果全部吻合。
3. **手稿对已知局限诚实披露**：CD74 critical-care Egger SE(0.111) < IVW SE(0.325) 的"物理上不可能"排序在 §3.10/§5 明确点出并排除因果解读；MR 全程定性为 Tier-3 假设生成；药物重定位的 curated-response 而非 direct-target 局限、L1000 单方向 rescue、样本重叠未校正等均在 Limitations 列明。
4. **核心生物学叙述（免疫麻痹方向性、外部泛化、共表达度中心性 FIS1 rank 12）全部可被原始 CSV 复现**，无一处手写数字与源文件漂移。

---

## § Questions（待作者澄清）

1. 发现集 5 折 CV AUC 在 `S06_auc_compare.csv`(0.6586) 与 `09_external_validation.csv`(0.6582) 间差 0.0004，哪个为权威？二者算法是否不同步？（见 D1）
2. `wtcs = rescue × √22` 是否意图为"精确恒等"？若否，建议在正文将"algebraically identical"改为"approximately identical at printed precision"，并使印刷的 rescue/wtcs 由同一未舍入值派生（见 D2）。
3. Abstract 的 "479 with a MARS endotype and 28-day survival" 建议明确为"479 例同时具内型分型与 28 天转归记录（114 死亡）"，避免被读作"479 例存活"。
4. 结论 §6 的 "anchored by … hub genes" 与讨论 §4 的 "near-replication" 强调错位，是否同意按 D4 对齐措辞？

---

## § What I actually checked（实际检查清单）

**读取的源文件（独立重算来源）：**
- `01_data/GSE65682/GSE65682_pheno.csv`（样本/内型/死亡计数）
- `03_results/S01_mars1_deg.csv`、`S01_deg_sepsis_vs_ctrl.csv`、`S01_immunoparalysis_direction.csv`
- `03_results/S02_immunoparalysis_score.csv`
- `03_results/S06_auc_compare.csv`、`09_external_validation.csv`
- `03_results/08_candidates_drugs.csv`
- `03_results/S08_l1000_candidate_scores.csv`、`S08_l1000_rescue_trtcp.csv`（20413 行）
- `03_results/10_genetics_mr_outcome5086_28ddeath.csv`、`10_mr_bh_family.csv`、`10_genetics_mr_outcome4982_criticalcare.csv`
- `03_results/S03_hub_degree.csv`、`S05_hub_genes.csv`、`S06_signature_genes.csv`
- `02_scripts/python/check_audit_assertions.py`（仅作"它检查了什么"的参考，未采信其结论）

**运行命令（节选）：** 见 `A3_recompute.py`（由 `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe` 执行），及 pandas/scipy 的 `mannwhitneyu`、`st.t.sf`、`2·st.t.sf(|β/se|,df)` 等。完整输出见 `A3_recompute_log.txt`。

**重算关键值汇总（重算 vs 手稿）：**
- 802/760/42 ✓；479(endotype∩death) ✓；Mars1 DEG 3597 ✓；sepsis-vs-healthy 448 ✓
- 免疫 23 down / 22 FDR / 21 both ✓
- Table1 六基因 logFC+adj.P+方向 ✓（CD14 P 源=0.0 下溢，印刷≈0 正确）
- 免疫评分中位 −0.792/−0.752/0.641/−0.235，MWU P 0.47/1.9e-18/1.3e-3 ✓
- 签名 CV 0.659 / train 0.750 / 外部 0.638(CI 0.532–0.748) / L1 0.585(CI 0.469–0.696) / n106·死52·映射29/30 ✓（D1：S06 0.6586 vs 09 0.6582）
- Table2 七候选 concordance 0.80/0.67/0.57/0.67/0.40/0.40/0.20 + n_rescue/n_target 全 ✓；IFN-γ 4/5 抗原呈递 ✓
- L1000 来那度胺 5435/20413·26.6%·rescue0.044·wtcs0.21 ✓；阿奇霉素 9152/20413·rescue0.013·wtcs0.06 ✓（D2：印刷 4 位非精确逆运算）
- MR Table3 五基因 IVW/Egger/WM 的 OR/CI/P 全 ✓；Egger p 全 t(df=n−2) ✓（无正态误算）；最小 IVW P 0.236≥0.23 ✓；CD14 Egger q_family 0.73·p_fdr_bh 0.49 ✓；CD74 crit-care WM q 3e-17 ✓；CD74 crit-care Egger SE 0.111<IVW 0.325（已披露）✓
- 共表达度中心性 GATA1 78.4/CGB 76.1/EPB49 72.5/FIS1 rank 12 ✓；S05 六 hub ✓；S06 三十基因 ✓

**发现的差异（均低严重度，不影响结论）：**
- D1：发现集 CV AUC 在 S06(0.6586) 与 09(0.6582) 间 0.0004 双源不一致 → 统一来源。
- D2：`wtcs=rescue×√22` 在印刷 4 位小数下非精确逆运算（差 ≤0.0002）→ 改措辞或由同源派生。
- D3：Mars3 中位 0.6405 印刷 0.641（可忽略舍入）。
- D4：结论"anchored by hub genes" vs 讨论"near-replication" 措辞错位 → 对齐。

**未发现问题（none of the following reproduced a discrepancy）：** 任何手写数字与源 CSV 漂移；任何 Egger p 用正态分布；任何"stale second-occurrence"正文内抄错；任何样本/DEG/免疫/评分/签名/药物/L1000/MR 头条数字不可复现。

---

**总体判断：** 作为首次投稿的独立实现审计，本手稿的数字溯源质量在单作者生信稿中属于上乘——所有头条数字均可从原始 CSV 复现，历史致命 bug（Egger 正态误算）已修复且我独立确认。剩余 4 项均为低严重度的溯源整洁度/措辞/精度问题，不改变任何科学结论，可在修回时一并清理。建议**小修（minor revision）**级别接收，无需因数字问题退稿。
