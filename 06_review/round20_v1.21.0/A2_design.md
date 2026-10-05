# 独立同行评审报告 — 设计/统计层面（A2_design）

**审稿人角色：** 设计 / 统计 / 流行病学独立审稿人（独立纪律：未读取 `06_review/` 下任何历史轮次、未读取 `REVIEW_*.md` / `RESPONSE_*.md` / `SUBMISSION_MANIFEST.md` / `CITATION.cff` / 作者核查声明 / 同轮其他审稿人文件）。本评审将稿件视为**首次投稿**处理。

**评审对象：** `05_reports/manuscript.md`（v1.21.0，commit 1212f7b）
**核对源数据：** `03_results/09_external_validation.csv`、`09_ext_calibration_dca.csv`、`09_ext_dca_grid.csv`、`S06_auc_compare.csv`、`09_ext_risk_scores.csv`、`S06_signature_genes.csv`、`08_candidates_drugs.csv`、`S08_l1000_positive_control.csv`、`S08_l1000_candidate_scores.csv`、`09_external_validation_coef.json`

**核心结论（一句话）：** 稿件在可重复性、CI 宽度、校准"作为排序器而非概率"、以及 prednisone 阳性对照失败的诚实披露上做得**对**；但其**最主要的统计设计缺陷**是 "primary / sensitivity" 标注在全文自相矛盾，且结果/摘要部分把**更低的、CI 包含 0.5 的** locked-L1（0.585）抬为 primary，把**更高的、可移植性更好的** equal-weight（0.638）贬为 sensitivity——这与 Methods §2.9 的事先规定**正好相反**，构成事后标注反转（post-hoc spin）。该矛盾必须消除。

---

## 一、设计层面问题（按严重度排序）

### 问题 1【Primary/Sensitivity 标注自相矛盾 → 事后标注反转】
**【Problem】** 稿件对 "哪个外部指标是 primary" 的标注在 Methods 与 Results/Abstract 之间直接矛盾；结果部分把**较低的** AUC（locked-L1 0.585）标为 primary，把**较高的** AUC（equal-weight 0.638）贬为 sensitivity，而 Methods 事先规定的是**相反**的安排。

**【Evidence】**（manuscript.md；行号指该文件）
- Methods §2.9（manuscript.md:55）："A fixed-orientation equal-weight score was reported as the **primary** external metric... A locked-L1-weight application was added as a **sensitivity analysis**. The equal-weight oriented sum was declared the primary external metric **before the external AUC was computed**..." → 事先规定 **equal-weight（0.638）为 primary，locked-L1（0.585）为 sensitivity**。
- Abstract（manuscript.md:14）："the locked L1 model ... gave external AUC **0.585** ... and a **pre-specified equal-weight sensitivity** score gave AUC **0.638**" → 结果把 **locked-L1（0.585）当 primary，equal-weight（0.638）当 sensitivity**，与 §2.9 相反。
- §3.4（manuscript.md:104）："this **locked-L1 estimate is reported as the primary** external transport metric ... a model-free fixed-orientation equal-weight score ... is reported as a **pre-specified sensitivity analysis**" → 与 §2.9 相反。
- §3.5（manuscript.md:107）："AUC **0.585** ... a model-free fixed-orientation equal-weight score (**a pre-specified sensitivity**) reached AUC **0.638**" → 与 §2.9 相反。
- Limitation 1（manuscript.md:157）："(n=106; AUC **0.638**, 95% CI 0.532–0.748 **for the portable fixed-orientation score**)" → 与 §2.9 一致（0.638 才是验证主结果），但与 Abstract/§3.4/§3.5 相反。

我独立复算确认 equal-weight AUC = **0.6382** > locked-L1 AUC = **0.5848**（源 `09_ext_risk_scores.csv`，n=106/52 deaths；与 `09_external_validation.csv` 完全一致）。即：较高的 0.638 才是 Methods 规定的 primary，但摘要与结果把它降为 sensitivity，把较低的 0.585 抬为 primary。

**【Why it matters】** 一个 primary endpoint 在 Methods 与 Results 之间相互打架，说明它**不是**事先规定的——这正是事后结果重标注（post-hoc outcome relabeling）的典型信号。更糟的是，被抬为 primary 的 0.585 不仅**低于**稿件自己报告的 benchmark（Peng et al. 0.619），而且其 95% CI（0.469–0.696，我复算 0.479–0.697）**包含 0.5**。于是稿件的主结论读起来像"我们没能跑赢 benchmark"，与其余位置的乐观措辞自相矛盾。把"更高的、可移植性更好（无队列特异权重）的 equal-weight"贬为 mere sensitivity，会误导读者以为 locked-L1 才是"诚实"的泛化估计——而实际上 locked-L1 应用的是**在发现队列过拟合、且在外部未迁移成功的**学习权重（AUC 反而更低）。

**【Specific fix】**（粘贴即用）
统一采用 Methods §2.9 的安排，并将 Abstract / §3.4 / §3.5 改写到一致：
> "The pre-specified **primary** external metric was the portable fixed-orientation equal-weight score (AUC 0.638, 95% CI 0.532–0.748); the **locked L1-weight** application (AUC 0.585, 95% CI 0.469–0.696) was the pre-specified **sensitivity** analysis."

并在 §7 编号溯源表（manuscript.md:195）维持 "equal-weight 0.638 = primary, locked-L1 0.585 = sensitivity" 的措辞，删除所有把 0.585 称为 primary、把 0.638 称为 sensitivity 的反向句子（Abstract:14、§3.4:104、§3.5:107）。

---

### 问题 2【以 CI 包含 0.5 的指标作为 primary，并 headline 一个低于 benchmark 的数字】
**【Problem】** 无论最终选定哪个为 primary，稿件在摘要层面对"显著性"的措辞偏离数据：被抬为 primary 的 locked-L1（0.585）其 CI 包含 0.5（非显著），且低于稿件自己报告的 benchmark 0.619；而更高的 equal-weight（0.638）仅比 benchmark 高 **+0.019**，二者 CI 重叠，无法区分。

**【Evidence】** `09_external_validation.csv`：locked-L1 AUC 0.5848，CI 0.4687–0.6959（含 0.5）；equal-weight 0.6382，CI 0.5317–0.7475（不含 0.5 但下界贴近 0.5）。我的 2000 次 bootstrap 复算：locked 0.479–0.697、equal-weight 0.538–0.745（与报告一致，差异仅来自 bootstrap 随机种子）。benchmark 0.619 出自 `S06_auc_compare.csv`（"IRG 基准(E-MTAB-4451),0.619"）。3-gene IRG proxy 本稿复算 = 0.5288（`09_external_validation.csv`），CI 与 0.5 邻近重叠。

**【Why it matters】** "可比于 benchmark（comparable to）" 是诚实的天花板；但若把 locked-L1 标为 primary 并暗示它"迁移成功"，则是过度宣称。反之，若按 §2.9 把 equal-weight 标为 primary，则诚实结论是"可移植评分略高于已发表 IRG benchmark，但统计上无法区分"。两种情形都应明确写出"非显著优于 chance / 非显著优于 benchmark"，不能让摘要读成干净的成功。

**【Specific fix】**（粘贴即用，置于 §3.5 末或 Abstract）
> "The locked-L1 external AUC (0.585) is not significantly above chance (95% CI includes 0.5); the portable equal-weight score (0.638) is modestly above the published IRG benchmark (0.619) but the two are not statistically distinguishable (overlapping 95% CIs). The honest conclusion is a real-but-modest, uncertain generalization, not a validated prognostic test."

---

### 问题 3【EPV 口径被低估：外部队列实际 EPV=1.73，而非 3.5】
**【Problem】** 稿件只引用了发现队列的 EPV（114/30≈3.8，manuscript.md:104），但外部测试集仅有 52 例事件（deaths）对应 30 基因签名，按事件数计 **EPV = 52/30 = 1.73**，远低于 ≥10 经验阈值；评审简报中 "EPV≈3.5（106/30）" 用样本量而非事件数作分母，同样低估。

**【Evidence】** `09_external_validation.csv`：n_validated_samples=106, n_deaths=52。复算 EPV_by_events = 52/30 = **1.73**；EPV_by_n = 106/30 = 3.53；discovery EPV = 114/30 = 3.80（manuscript.md:104）。`09_external_validation_coef.json`：locked-L1 30 基因中仅 22 个非零系数、8 个为零（CD74/HLA-DRB1/IRF1/HLA-DMA/HLA-DMB/CD86/CD8B 等被 L1 压到 0），说明发现阶段系数已高度稀疏/过拟合。

**【Why it matters】** 外部 AUC 的**点估计**不依赖重拟合，但其**精度**受 52 事件强烈限制——这一点稿件用宽 CI（locked 跨 0.227、equal-weight 跨 0.208）诚实地表达了，我复算 CI 与之吻合，**这一点应予肯定**。但稿件从未说明"外部测试本身只有 52 事件"，读者会误以为"EPV 问题只存在于发现阶段 CV"。实际上外部点估计同样**不精确**，宽 CI 正是由此而来，点估计不应被过度解读。

**【Specific fix】**（粘贴即用，加于 §3.5）
> "The external test set contains only 52 events for a 30-gene signature (effective EPV ≈ 1.7), so the AUC point estimate is imprecise; the wide 95% CI (0.469–0.696 / 0.532–0.748) reflects this small-event constraint, and the point estimate should not be over-read."

---

### 问题 4【校准斜率 0.50（<1）= 概率不迁移，已诚实降为"排序器"；但"over-confident"措辞正确，须勿误改为 under-confident】
**【Problem】** 外部 equal-weight 评分校准斜率为 0.50（95% CI 0.10–0.91，P=0.016 vs 理想斜率 1.0），说明预测概率在外部队列**未校准**；稿件据此把评分降为"risk ranker 而非校准概率"，处理正确。但评审简报称稿件"正确地称 0.50 为 under-confident"，而稿件实际正文（manuscript.md:107）写的是 **"over-confident predicted probabilities"**——这与标准校准斜率约定一致，应为**正确**，不应被"修正"成 under-confident。

**【Evidence】** `09_ext_calibration_dca.csv`：calib_slope=0.5028, calib_intercept=−0.0382, p_slope_eq_1=0.01575。我以标准化 oriented_sum 做 logistic 再拟合：slope=0.5005, intercept=−0.0381, bootstrap p(slope=1)=0.024（与源文件吻合）。manuscript.md:107 原文："a sub-ideal slope of 0.50 ... indicating **over-confident** predicted probabilities whose degree of over-confidence is only weakly identified at n=106 with 52 events; the score is therefore presented as a risk *ranker* rather than a calibrated probability"。

**【Why it matters】** 在预测模型迁移文献（van Calster 2019; Steyerberg）中，外部验证斜率 **<1** 的标准解读正是"预测概率过于极端 / over-confident（需要向均值收缩）"。稿件用 "over-confident" 是**标准且正确**的。若按简报的 "under-confident" 去改，反而会变成非标准表述。真正要点是：斜率 0.50 且其 95% CI 极宽（0.10–0.91，含接近 0.5 的值），所以"弱识别"的措辞是诚实的；加上 locked-L1 的 CI 含 0.5，**概率输出双重不可用，仅排序信息保留**——这正确地限定了可迁移性声明的边界。

**【Specific fix】** 保持 "over-confident"（标准约定），不要改为 under-confident。若作者坚持用 under-confident，必须显式定义为"predicted risks are too shrunken toward the mean"。同时在 §3.5 补一句："With slope 0.50 and a CI spanning 0.10–0.91, the calibration correction itself is imprecise; only the ranking—not any threshold probability—should be transported."

---

### 问题 5【DCA "≥0.80 坍缩为 treat-none" 的解读正确；但 DCA 建立在样本内校准概率上，可操作区间偏窄部分源于校准伪影】
**【Problem】** 稿件称 DCA "从阈值 ≈0.30 起超过 treat-all，在 ≥0.80 坍缩（treat-none）"。我核验该解读**正确**（NB 在阈值 0.80 处 = 0，即 treat-none 参考线），但 DCA 所用概率是对同一 106 例做的**样本内校准**（slope 0.50），而 slope 本身 CI 极宽，故"可操作区间窄"部分来自过度收缩的校准，非纯生物学。

**【Evidence】** `09_ext_dca_grid.csv`：threshold 0.80 → nb_model=0.0、nb_treat_all=−1.5472、n_flagged=0；0.85/0.90 同样 nb_model=0.0。manuscript.md:107 后半段原文："decision-curve analysis — computed on the calibration-corrected probabilities from the external logistic fit (intercept −0.04, slope 0.50), which was itself fitted on the same 106-sample E-MTAB-4451 set used for validation and is therefore optimistically biased and reported as illustrative ... showed a positive net benefit over treat-none from threshold 0.05 to 0.75 and exceeds the treat-all strategy from threshold ≈0.30 onward ... but the last range is vacuous because at ≥0.80 no calibration-corrected risk exceeds the threshold (0 of 106 patients flagged)". 我用校准后 logit 概率复算 DCA 网格**逐行吻合**（0.30: 0.2844 vs 0.2722；0.50: 0.0755 vs −0.0189；0.80: 0.0000；最大概率 0.7607，故无人 >0.80）。模型在 0.25 与 treat-all 持平、0.30 起超出，与"≈0.30"一致。

**【Why it matters】** 解读本身无误，且稿件已诚实标注 DCA 为"illustrative / optimistically biased"。但须指出：因校准斜率 0.50 把概率拉向 0.5，才有"无人在 0.80 以上被标记"——若真实斜率为 1.0，更多患者会越过 0.80，DCA 可操作区间会更宽。因此 DCA 的窄带**部分是校准伪影**，不应被读作"生物学上该评分在高风险处无用"。

**【Specific fix】**（可选，非强制）在 §3.5 DCA 句末补："Because the DCA threshold axis uses the in-sample calibration-corrected (slope 0.50) probabilities, the exact collapse point at 0.80 is partly a calibration artifact; the qualitative conclusion—modest, narrow net-benefit band, no support for treat-all—is unchanged. A DCA after external/slope=1 recalibration is recommended."

---

### 问题 6【签名是"泛化的 28 天死亡率/脓毒症严重度"签名，而非免疫麻痹特异签名 → 削弱"immunoparalysis-specific"声称】
**【Problem】** 30 基因签名并非纯免疫麻痹锚定：它包含一个**中性粒/炎症臂**（ELANE、MPO、S100A8 与死亡**正相关**），因此更宜描述为泛化死亡率/严重度签名，而非免疫麻痹特异签名。

**【Evidence】** `S06_signature_genes.csv`：ELANE corr +0.170、MPO +0.152、S100A8 +0.091（均为正 → 表达越高死亡越高，属高炎症/中性粒急性相臂）；而抗原呈递/单核臂为负（CD74 −0.163、HLA-DRB1 −0.162、FCGR3A −0.161、HLA-DRA −0.144、CD14 −0.141 等）。manuscript.md:112 也自承该轴与 CD4/CD8 T 细胞及炎症上下文相关。稿件标题/摘要/§3.4/结论多次称其为 "immunoparalysis signature"（如 Abstract:14、§3.4 标题行 103、Conclusion:178）。

**【Why it matters】** 把含 ELANE/MPO/S100A8（经典中性粒/钙卫蛋白急性相）的签名称为"免疫麻痹签名"夸大了特异性；评审会指出正相关臂是随严重度上升的经典中性粒/急性相反应，与免疫抑制状态无关。这**不推翻**论文，但要求题目/摘要改为"富集于 Mars1 抗原呈递/单核程序"的免疫风险/死亡率签名。

**【Specific fix】**（粘贴即用，替换 Abstract:14、§3.4 标题行 103、Conclusion:178 中的 "immunoparalysis signature"）
> "an immune-risk (28-day mortality) signature enriched for the Mars1 antigen-presentation / monocytic program (and also containing a neutrophilic/acute-phase arm, e.g., ELANE, MPO, S100A8)"

---

### 问题 7【药物重定位：prednisone 阴性对照失败将 L1000 层级"归零"——这限定（bounds）而非推翻结论；但全部重定位证据均非显著，声明须保持"假设生成"】
**【Problem】** prednisone 阳性对照失败意味着 L1000 rescue 层级**不可区分**；稿件正确地把它降为"仅描述性、不作为支持证据"。但这使整个重定位结论完全落在"策展一致性"之上，而稿件自承该一致性处于或低于自身 0.84 背景且无一显著。诚实，但**措辞重心**有漂移风险。

**【Evidence】** `S08_l1000_positive_control.csv`：prednisone rescue 0.136、rank 651/20413（**3.2nd percentile**）、z≈+2.03；dexamethasone 0.032（33.4th pct）。`S08_l1000_candidate_scores.csv`：lenalidomide z=+0.56（rank 5435，26.6th pct，empirical P 0.266）、azithromycin z=+0.10（rank 9152，44.8th pct，empirical P 0.449）——均在噪声带内。manuscript.md:137：明确"a metric on which a clinical immunosuppressant scores at z=+2.03 while the candidates score at z=+0.56 and +0.10 carries no discriminating information"。`08_candidates_drugs.csv`：7 个候选的 binom_p_immune_bg 均 ≥0.82（即处于或低于 0.84 背景）；manuscript.md:115："every candidate lies at or below that value (one-sided binomial P(X ≥ k) ≥ 0.82 for all seven)"。

**【Why it matters】** 重定位结论仅是假设生成，且**没有任何层级达到显著性**。这在 Limitation 8（manuscript.md:165）与 10（manuscript.md:168）中已诚实声明，Abstract（manuscript.md:14）也称"annotated as hypothesis-generating ... rather than prioritised by significance"——这是正确的。风险仅在结论段（manuscript.md:178）若漂移为"identifies candidate interventions"而未加"hypothesis-generating"限定。

**【Specific fix】**（粘贴即用，加于 §3.9 末或 Conclusion）
> "No repositioning candidate reached significance on any tier; the L1000 screen failed its glucocorticoid positive control and therefore provides no supporting evidence (only a non-refutation). The shortlist rests entirely on curated immune-response concordance at/below the 0.84 background and on literature precedent (§3.8), and remains strictly hypothesis-generating pending the S11 functional assays."

---

### 问题 8【选择链族系误差（Limitation 9）已披露，但外部 AUC 仍"不独立于标签"；其乐观程度未量化】
**【Problem】** Limitation 9（manuscript.md:166）正确指出 hub 发现与签名选择复用了同一队列的 28 天标签，使内部 CV AUC（0.659）乐观。但外部验证的**基因集 + 死亡方向**同样是在 GSE65682 的 28 天标签上确定的，因此该"外部"AUC 是"队列与平台独立、但标签不独立"的迁移检验——稿件已说明（manuscript.md:106），但未量化标签复用对外部点估计的乐观贡献。

**【Evidence】** manuscript.md:106："The fixed orientation was trained on GSE65682 28-day labels, so the external application is independent in cohort and platform but not in label." manuscript.md:166（Limitation 9）。`S06_auc_compare.csv`：CV AUC 0.6586、train 0.7495（内部乐观已承认）。`09_external_validation.csv`：auc_GSE65682_CV_locked=0.6582（与 CV 一致）。

**【Why it matters】** 外部 AUC（0.585/0.638）仍可能被**标签定义**乐观偏倚：基因选择 + 方向利用了发现标签，真正"标签独立"的验证应先用外部准则固定基因集（如已发表 IRG 基因）再应用。内部 CV 是被夸大的那个；外部是真实但**标签绑定**的迁移。这通过披露被诚实界定，但应作为局限明确写出。

**【Specific fix】**（粘贴即用，加于 Limitation 9）
> "Because the 30-gene set and its death-orientation were both derived from GSE65682 28-day labels, the external AUC is a transport test that remains tied to the discovery label definition; a fully label-independent confirmation (gene set fixed a priori, e.g., from the published IRG panel, or a second independent held-out cohort) is required before the signature can be called validated."

---

## 二、§ Stands up（稿件做得对、应予保留之处，附证据）

1. **内部 CV 的乐观被公开承认**（manuscript.md:104 "an inner-loop estimate ... optimistic"；Limitation 1:157）。复算确认 CV AUC 0.659 / train 0.750（`S06_auc_compare.csv`），并正确将其与"诚实的外部泛化"区分。
2. **校准斜率 <1 被诚实报告为宽 CI 并降为"排序器"**（manuscript.md:107；`09_ext_calibration_dca.csv` slope 0.5028 / intercept −0.0382 / p=0.01575，我复算吻合）。这是正确且克制的处理。
3. **prednisone L1000 阳性对照失败被正确地用来"归零"该层级**（manuscript.md:137；`S08_l1000_positive_control.csv` rank 651/20413, 3.2nd pct）。对阴性结果的处理诚实——没有把 lenalidomide/azithromycin（z=+0.56/+0.10，噪声带内）包装成支持证据。
4. **外部 CI 宽度正确且诚实**：我 2000 次 bootstrap 复算 locked 0.479–0.697、equal-weight 0.538–0.745，与报告 0.469–0.696 / 0.532–0.748 一致（差异仅 bootstrap 种子）。CI 包含 0.5 这一事实被明确写出，未掩盖不确定性。
5. **可重复性可审计**：我复算的每一个数值（AUC、CI、校准、DCA 网格）均与 deposited CSV 吻合，说明分析管线确实可复现、每数可溯源（符合 §7 承诺）。
6. **"标签不独立"在 §3.5 显式声明**（manuscript.md:106），没有把外部验证伪装成完全独立验证。

---

## 三、§ Questions for the authors（请作者回答）

1. **primary 究竟事先规定为哪一个——equal-weight（§2.9）还是 locked-L1（Abstract/§3.4）？** 二者直接矛盾。请提供在生成 `09_external_validation.csv` **之前**的、带日期的分析脚本或 commit，证明 primary/sensitivity 决定先于结果计算。
2. **能否给出时间戳/commit，证明 primary/sensitivity 的指定早于外部 AUC 计算？** 若不能，则默认按 Methods §2.9（equal-weight=primary）统一全文，并删除结果段的反向标注。
3. **为何不对发现集做 Harrell 式 optimism bootstrap，以量化从 0.659（CV）→0.585（外部 locked）的收缩量？** 这将把"乐观"从定性陈述变为定量估计。
4. **对重定位：7 个候选全部处于或低于 0.84 背景、L1000 层级阳性对照失败，那么支持任一候选进入实验随访的"最强单一证据"是什么？** 是否是 §3.8 的临床 RCT 文献（而非任何 in-silico 层级）？请在结论中明确。
5. **签名含 ELANE/MPO/S100A8（中性粒/急性相，与死亡正相关）。是否做过剔除炎症臂的敏感性分析，确认仅抗原呈递臂仍能迁移？** 若有请补充；若无，请在该局限中明确"签名是泛化死亡率签名，非免疫麻痹特异"。
6. **外部 AUC 的"标签不独立"：是否有计划用已发表 IRG 基因集（外部固定）或第二个独立队列做一次标签独立验证？** 若无，请在 Limitation 9 写清这是未决验证。

---

## 四、§ What I actually checked（独立核验清单）

- **AUC（源 `09_ext_risk_scores.csv`，n=106，52 deaths）**：复算 oriented_sum AUC=0.6382、locked-L1 AUC=0.5848（与 `09_external_validation.csv` 完全一致）。
- **Bootstrap 2000 样本 CI（非取负向、与稿件一致的方向）**：oriented 0.538–0.745；locked 0.479–0.697（与报告 0.532–0.748 / 0.469–0.696 在 bootstrap 种子误差内吻合）。确认 CI=2000 次 bootstrap 已正确实现。
- **校准（对标准化 oriented_sum 做 logistic 再拟合）**：slope=0.5005、intercept=−0.0381、bootstrap p(slope=1)=0.024（与 `09_ext_calibration_dca.csv` 0.5028/−0.0382/0.01575 吻合）。
- **DCA（用校准后 logit 概率复算）**：逐行复现 `09_ext_dca_grid.csv`（0.30: 0.2844 vs 0.2722；0.50: 0.0755 vs −0.0189；0.80: 0.0000）；确认阈值 ≥0.80 时 NB=0（=treat-none 参考线），模型自 ≈0.30 起超出 treat-all——与稿件解读一致。
- **prednisone 阳性对照**：`S08_l1000_positive_control.csv` rank 651/20413（3.2nd pct），dexamethasone 33.4th pct；候选 lenalidomide z=+0.56、azithromycin z=+0.10（均在噪声带，empirical P 0.27/0.45）。
- **策展一致性背景**：`08_candidates_drugs.csv` 7 候选 binom_p_immune_bg 均 ≥0.82（处于/低于 0.84 背景）。
- **EPV**：外部 52/30=1.73；发现 114/30=3.80；locked-L1 30 基因中 8 个系数被 L1 压至 0（源 `09_external_validation_coef.json`）。
- **签名构成**：`S06_signature_genes.csv` 确认 ELANE/MPO/S100A8 与死亡正相关（炎症/中性粒臂），其余为抗原呈递/单核/ T 细胞臂。
- **完整性**：通读 `manuscript.md` 全文；**未**打开 `06_review/` 下任何历史文件、未读 `REVIEW_*.md`/`RESPONSE_*.md`/`SUBMISSION_MANIFEST.md`/`CITATION.cff`/作者核查声明/同轮其他审稿人文件。

---

## 五、给编辑的处置建议（一句话）
**修回（Major Revision）**。最严重缺陷是问题 1（primary/sensitivity 全文自相矛盾、结果段事后把较低且 CI 含 0.5 的 locked-L1 抬为 primary），必须按 Methods §2.9 统一；问题 6（特异性措辞）与问题 8（标签独立验证）须补局限。问题 2–5、7 的诚实披露本身基本到位，仅需措辞对齐。复算未发现任何数值造假——所有报告数字均可从源 CSV 复现。
