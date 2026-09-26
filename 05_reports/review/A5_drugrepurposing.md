# A5 · 计算药物重定位 / LINCS L1000 连接度方法学评审

**评审角色**：独立同行评审专家（计算药物重定位 / 转录组连接度 reverse-connectivity 方法学）
**评审对象**：`05_reports/manuscript.md`（v1.0.2，首次投稿视角）
**评审纪律**：假设此前未见过该稿件，所有判断均来自亲自读取的稿件文本或源数据；凡可验证数字均亲自重算或核对源文件（见末尾 § What I actually checked）。未读取其他专家文件、PIPELINE 执行注释或 `*_gen_*.py`。

---

## 总体评价（先给结论）

稿件把"脓毒症免疫麻痹枢纽基因"与"in-silico 虚拟敲除 + LINCS L1000 反向连接度 + 文献规则层"三个层次串成一条 drug-repositioning 证据链，框架设计（Tier-1/2/3 正锚）是合理且诚实的，§5 局限也确实列出了 S09 对接与 S11 功能验证的缺口。但是，**作为一篇以"计算药物重定位"为卖点的稿件，其重定位方法学核心环节存在四处会直接影响接收概率的特异性 / 严谨性缺陷**，集中在：(i) `rescue_fraction` 的"target"定义并非真实药物靶点；(ii) §3.9 的 L1000 query 集合与正文"22 Mars1-down genes"描述不一致且混入了方向相反的 exhaustion 基因；(iii) 把 LINCS 的 "BRD-" 前缀误当成"BET 抑制剂"药理类别；(iv) "虚拟敲除"阳性对照名不副实，是循环验证。其中 (ii) 与 (iii) 属于可被审稿人一眼识破的事实性 / 定义性错误，必须修正后才能送外审。

下面按四段式（【Problem】【Evidence】【Why it matters】【Specific fix】）逐条给出。

---

## 发现 1 — `rescue_fraction` 用"机制相关基因集"代替"真实药物靶点"，特异性不足（专长聚焦点 1）

### 【Problem】
`rescue_fraction = |target ∩ Mars1-down| / |target|` 中的 `target` 并非药物在 ChEMBL / DGIdb 意义上的**直接分子靶点**，而是作者手工整理的"该药文献确证会上调 / 激活的免疫基因"（下游响应基因）。这把"重定位证据"降级为"机制注释"，特异性被严重稀释。

### 【Evidence】
- 稿件 §2.8（manuscript.md:63）明确写："each candidate's literature-established **target genes** were intersected with the Mars1-down axis"。
- 源脚本 `02_scripts/python/08_virtual_ko_cmap.py:34-56` 的 `DRUG_MAP` 显示：
  - IL-7 的 `targets = ["CD3D","CD3E","CD8A","IL7R","LCK"]` —— 这些是 T 细胞受体 / 细胞因子下游响应基因，**不是 IL-7 的真实靶点**。IL-7 的真实受体是 IL7R（CD127），信号经 JAK1/JAK3–STAT5；CD3D/E、LCK 是 T 细胞增殖后被动上调的下游标志。
  - GM-CSF 的 `targets = ["HLA-DRA","HLA-DRB1","CD14","FCGR3A","ITGAM",...]` —— 这些是髓系 / APC 响应基因，真实受体是 CSF2RA/CSF2RB，根本不在该列表里。
- `03_results/08_candidates_drugs.csv` 第 2–8 行确认：IL-7 救回的 5 个基因全部是 T 细胞标志，GM-CSF 救回的 5 个全部是髓系 / APC 标志。
- 我核对了 `rescue_fraction` 的计数本身（IL-7 5/5=1.00、GM-CSF 5/6=0.833 等）与 CSV 一致，**数字计算无误，但"target"的语义定义有误**。

### 【Why it matters】
这直接触及本专长的核心质疑。把"下游响应基因集"当作"药物靶点"来计算重叠比例，意味着**任何会 broadly 上调免疫基因的药物都会得高分**，而真正"药物结合并作用于枢纽基因"的证据为零。更关键的是：该指标没有统计检验——IL-7 得 1.00 仅因作者塞进去的 5 个 T 细胞基因恰好都落在 Mars1-down 轴里（按构造必然如此），它验证的是"整理者先验"，不是"方法能发现真实重定位"。在 J Transl Med / Front Immunol 这类期刊，方法学审稿人会要求靶点来自**可溯源的 pharmacologic 数据库**而非作者手工 curated 的响应基因。

### 【Specific fix】
1. 重命名指标并更换数据源。建议：
   > "We redefined `rescue_fraction` using **experimentally verified direct targets** retrieved from DGIdb v4.2 and ChEMBL (max_phase≥4), replacing the curated downstream-response gene sets. The metric is now reported as `target-overlap concordance` and is accompanied by a two-sided Fisher exact test (or hypergeometric enrichment) against the Mars1-down gene set, with the odds ratio and BH-FDR reported for each candidate."
2. 对现有 7 个候选，重新用 DGIdb/ChEMBL 拉取真实靶点（如 IL-7→IL7R/JAK3；GM-CSF→CSF2RA/CSF2RB；IFN-γ→IFNGR1/IFNGR2；lenalidomide→CRBN；azithromycin→无明确单一靶点，应如实标注），再与 Mars1-down 轴做超几何富集。若真实靶点大多不在 Mars1-down 基因里，应**如实报告**这一负向发现，而不是维持一个基于响应基因的虚高分数。
3. 在 §2.8 明确区分"direct target"与"downstream response gene"，避免把机制注释包装成重定位证据。

---

## 发现 2 — §3.9 "22 Mars1-down genes" 与真实 L1000 query 集合不一致，且混入了方向相反的 exhaustion 基因（专长聚焦点 2）

### 【Problem】
稿件 §3.9 声称 query signature 是"22 Mars1-down genes present on the L1000 platform"，但**真实的 query 集合是"25 个共识免疫基因中存在于 L1000 平台的 22 个"**，其中包含 2 个在 Mars1 中**方向性上调**的 exhaustion 基因（PDCD1、LAG3），同时**排除了 3 个不在平台上的基因，其中 2 个是 hub 基因（HAVCR2、FCGR3A）**。这与"Mars1-down"的语义相悖，也使 L1000 救援查询实际上漏掉了 2/6 个枢纽基因。

### 【Evidence】
- 真实 query 集合来自 `01_data/LINCS/mars1_down_l1000_idx.json` 的 `mars1_down_genes`（22 个）：CD14, HLA-DMB, LCK, CD3E, GZMA, CD8A, ITGAM, IL7R, **LAG3**, GZMK, CD3G, **PDCD1**, CD8B, HLA-DRB1, HLA-DRA, CD74, HLA-DQB1, CD3D, HLA-DQA1, LYZ, HLA-DMA, CTLA4。
- 我用 `S01_immunoparalysis_direction.csv` 逐一比对方向，确认 **LAG3 = Mars1_up（logFC +0.035）**、**PDCD1 = Mars1_up（logFC +0.162）**（json 中二者被标作"down"但源数据方向为 up）。即 22 个里有 2 个是 Mars1 上调的耗竭标志。
- 与 §3.1 的 25 基因比对：缺失的 3 个是 **HAVCR2、FCGR3A、TIGIT**（均不在 L1000 平台解析到）。其中 **HAVCR2 与 FCGR3A 正是 §3.3 的 6 个 hub 基因之二**（manuscript.md:102, `S05_hub_genes.csv`）。
- 因此 §3.9（manuscript.md:134）"the 22 Mars1-down genes present on the L1000 platform" 是不准确的：准确说法是"22 of the 25 consensus immune genes that are measurable on L1000, of which 2 are Mars1-up exhaustion markers"。

### 【Why it matters】
两重后果：(a) **概念错误**——rescue 评分 `rescue = mean rank-percentile − 0.5` 对全部 22 个基因**同等奖励"表达上调"**。但对 PDCD1、LAG3（疾病中已上调的耗竭标志），"救援免疫麻痹"本应要求它们被**下调**，而当前单向度量会把"进一步上调 PDCD1/LAG3"误记为"救援"。这污染了 rescue 分数的语义。(b) **枢纽基因覆盖缺口**——一篇标题主打"hub genes"的稿件，其 L1000 反向连接度查询却丢掉了 2/6 个 hub（HAVCR2、FCGR3A），但未在正文声明，读者会误以为 rescue 分数覆盖了全部 hub 轴。

### 【Specific fix】
1. 对 query 集合做方向感知（signed）重定义。建议：
   > "The reverse-connectivity query was redefined as a **signed** set: the 20 Mars1-down consensus immune genes measurable on L1000 were required to be up-regulated by a rescuing perturbagen, while the 2 Mars1-up exhaustion markers (PDCD1, LAG3) were required to be down-regulated (iLINCS-style dual-direction τ). The two hubs absent from the L1000 platform (HAVCR2, FCGR3A) were excluded from the connectivity query by design and are listed explicitly in §3.9; a sensitivity analysis treating their proxies is provided."
2. 在 §3.9 给出 22 个基因的**显式清单与各自方向**，并说明 HAVCR2/FCGR3A 因平台缺失被排除。
3. 若坚持用单集度量，至少把 PDCD1/LAG3 从"want-up"集移到"want-down"集，并重新报告 lenalidomide / azithromycin 的 rescue（方向修正后分数可能变化，需重算）。

---

## 发现 3 — 把 LINCS "BRD-" 前缀误标为"BET 抑制剂"，属事实性错误（专长聚焦点 3）

### 【Problem】
稿件 §3.9（manuscript.md:136）将最强的 L1000 救援剂写作"structurally diverse **BRD-series compounds (top rescue 0.32)** plus biologically plausible immuno-metabolic modulators: **HDAC inhibitors**..."。这里的"BRD-series (BET inhibitors)"是**错误标识**：在 LINCS L1000 中，"BRD-" 是 Broad Institute 贡献化合物的 **ID 前缀**，覆盖所有药理类别，并不特指 BET 溴结构域抑制剂。

### 【Evidence】
- 我直接对 `03_results/S08_l1000_rescue_trtcp.csv`（20,413 行）按 rescue_score 排序，Top 8 为：BRD-K89995901 (0.318)、BRD-K47094330 (0.293)、BRD-K20793945 (0.287)、BRD-K22451143 (0.284)、BRD-K46284961 (0.275)、BRD-K87311987 (0.275)、BRD-K14228330 (0.270)、BRD-K84405221 (0.266)——**全部是 BRD- 开头的匿名 Broad ID**。
- "BRD-" 前缀在 LINCS `pert_id` 体系里是 Broad 的命名空间（如 BRD-Kxxxxxxxxx 为小分子、BRD-Axxxxxxxxx 为探针），与"BET 抑制剂"药理类无等价关系。真正是 BET 抑制剂的化合物（如 JQ1、OTX015）确实也带 BRD- 前缀，但**不能反推所有 BRD- 都是 BET 抑制剂**。稿件随后又把"HDAC inhibitors / HSP90 inhibitors / statins"作为**独立类别**列出，更说明作者知道 BRD- ≠ 这些类，却在括号里把它等同于"BET inhibitors"。
- 稿件未给出这些 Top 化合物的 canonical name 或 pharmacologic class，仅以"BRD-series (BET inhibitors)"一带而过。

### 【Why it matters】
这是方法学审稿人最容易一眼看穿的低级错误，会直接损害整段 L1000 结果的可信度——因为读者会质疑作者是否真正理解所用数据库的结构。把匿名 ID 前缀当成药理机制类别，削弱了"最强救援剂与免疫麻痹恢复机制联系牵强"这一本应被认真讨论的论证。

### 【Specific fix】
1. 删除"BET inhibitors"的括号断言，改为逐化合物解析真实身份。建议：
   > "The highest-scoring perturbagens were Broad-Institute LINCS identifiers (BRD-prefixed); we resolved each top compound to its canonical name and pharmacologic class via `pert_iname`/PubChem CID. The leading rescuers comprised [e.g., JQ1/OTX015 if BET inhibitors; otherwise state actual classes], distinct from the separately enumerated HDAC-, HSP90-inhibitors and statins. We report the resolved identities in Table S__ and refrain from implying a uniform mechanism."
2. 用 `pert_iname` + `canonical_smiles`/`pubchem_cid`（已在 `S08_l1000_rescue_trtcp.csv` 中）把 Top 25 救援剂逐一映射为化合物名与类，替换"BRD-series (BET inhibitors)"这一笼统说法。在结论里讨论"最强救援剂机制联系是否牵强"时，必须建立在**真实化合物身份**之上。

---

## 发现 4 — LINCS 单集反向连接度能否表征"功能免疫恢复"：概念边界与证据强度不足（专长聚焦点 3）

### 【Problem】
§3.9 用单集反向连接度（`rescue = mean rank-percentile − 0.5`、`wtcs = (Σ−n/2)/√n`）度量"免疫麻痹逆转"，但 (a) 该度量只捕获"22 个基因被转录本上调"，不等于功能免疫恢复；(b) L1000 仅直接测 ~978 个 landmark 基因，22 个查询基因多为**推断值**，抗原呈递基因的恢复保真度未被讨论；(c) 糖皮质激素"也高分"的 caveat 已诚实给出，但仍有更粗暴的非特异性高分化合物（转录抑制剂、线粒体毒物、溶剂）未被列为反面证据；(d) 度量本身缺乏显著性检验。

### 【Evidence】
- 稿件 §3.9（manuscript.md:134-138）已诚实标注：prednisone rescue 0.136（rank 651）、dexamethasone 0.032（rank 6808），"a positive rescue score is necessary but not sufficient"。
- 但 `S08_l1000_immuno_overlap.csv`（按免疫刺激关键词过滤的 Top 救援剂）里还出现 **tetrachloroethylene（四氯乙烯，工业溶剂，rescue 0.136，rank 666）、nystatin（抗真菌多烯，0.046）、kanamycin / dihydrostreptomycin（氨基糖苷抗生素）、dactinomycin / chromomycin-a3（转录抑制剂）、antimycin-a / oligomycin（线粒体电子传递抑制剂）** 等高 rescue 化合物。这些显然不是"免疫麻痹功能恢复剂"，却与 pravastatin、geldanamycin 同列 Top 救援——说明该度量大量捕获**非特异性转录应激 / 全局表达扰动**，而非抗原呈递轴的定向恢复。
- 背景：我重算 `S08_l1000_rescue_trtcp.csv` 全 20,413 个 trt_cp 的 rescue 分布：mean 0.0064、median 0.0055、53.62% > 0（与稿件 §3.9 的 "0.006 / 0.006 / 53.6%" 一致，✓ 数字正确）。度量居中、偏正略多，但**没有给定显著性阈值**（如 top-k% 或 z>2），lenalidomide 仅 top 26.6%、azithromycin 中位附近，缺乏"显著救援"的统计学判据。
- L1000 landmark 覆盖：稿件未说明 22 个查询基因中有多少是 ~978 个直接测量的 landmark、多少是被线性模型推断的。抗原呈递基因（HLA-DRA/DRB1、CD74）多为推断值，其 rescue 信号经推断链衰减，保真度需明示。

### 【Why it matters】
这关系到 §3.9 结论"supports the direction of the small-molecule candidates, not their clinical benefit"是否成立，以及标题级 claim 的强度。当前证据只能支持"方向性一致"，且因非特异性高分化合物普遍，方向性一致的信号很弱。若不把这些反面证据摆出来并给出显著性框架，审稿人会认为该连接度分析"噪声大、不可信"。

### 【Specific fix】
1. 扩充 caveat，显式列出非特异性高分化合物作为反面证据。建议：
   > "Beyond glucocorticoids, several high-rescue perturbagens are clearly non-immune (e.g., tetrachloroethylene, nystatin, kanamycin, dactinomycin, antimycin-a, oligomycin), confirming that the single-set percentile rescue captures generic transcriptional perturbation rather than antigen-presentation-specific restoration. We therefore report rescue as **hypothesis-generating only** and require functional validation (S11)."
2. 增加显著性框架：报告每化合物的 rescue z-score（基于 20,413 背景）或 rank-percentile 阈值（如 top 5%/1%），并明确 lenalidomide/azithromycin 是否越过该阈值（目前仅 top 26.6% / ~50%，应如实标注"未达严格显著"）。
3. 补充 L1000 landmark 成员说明：列出 22 查询基因中 landmark vs inferred 的数量，并讨论抗原呈递基因推断保真度对 rescue 的影响（或换用 iLINCS 的官方签名级连接度复算）。

---

## 发现 5 — 仅 2/7 候选进入 L1000 `trt_cp`，削弱"in-silico drug repositioning"整体主张（专长聚焦点 4）

### 【Problem】
7 个候选中只有 azithromycin 与 lenalidomide 是小分子且存在于 L1000 `trt_cp`；IL-7、GM-CSF、IFN-γ、胸腺肽α1、BCG 是生物制剂 / 疫苗 / 多肽，**没有 unbiased 连接度证据**。整篇"计算重定位"对 5/7 候选实质上只依赖文献规则层（S08b）与手工 `rescue_fraction`，而非 in-silico 连接度。

### 【Evidence】
- `03_results/S08_l1000_candidate_scores.csv` 仅 2 行：azithromycin（BRD-K74501079, rescue 0.0133, rank 9152）、lenalidomide（BRD-A17883755, rescue 0.0439, rank 5435）。
- 稿件 §3.9（manuscript.md:136）确实写了"only the two small molecules exist as trt_cp"，但摘要（manuscript.md:14）与结论（manuscript.md:202）仍表述为"in-silico repositioning nominates immune-restorative agents; the two small-molecule candidates show ... LINCS L1000 rescue"，对 5 个非小分子候选缺少连接度支持这一事实被弱化处理。
- `S08_l1000_positive_control.csv` 第 9 行明确："interferon-gamma (biologic, not trt_cp): N/A (absent from trt_cp)"——印证 IFN-γ 无法进 L1000 验证。

### 【Why it matters】
对以"计算药物重定位"为标题卖点的稿件，若 5/7 候选无连接度证据，则"in-silico repositioning"对多数候选只是"文献机制注释 + 手工重叠"。这会触发方法学审稿人质疑标题与内容不匹配。稿件需要诚实地把"连接度验证"范围限定到小分子，并说明其余候选的证据层级。

### 【Specific fix】
1. 在摘要与结论中明确限定。建议（结论句替换）：
   > "Connectivity-scored LINCS L1000 rescue was attainable for only the two small-molecule candidates (lenalidomide, azithromycin); the remaining five immunobiologics/vaccine candidates (IL-7, GM-CSF, IFN-γ, thymosin α1, BCG) rest on mechanism-anchored annotation (S08b literature-rule layer) without unbiased transcriptomic connectivity and should be regarded as hypothesis-generating."
2. 为非小分子候选提供替代 in-silico 证据（若可行）：例如用 INDRA / DrugBank / 已知靶点-基因调控网络验证其靶基因是否落在 Mars1-down 轴，或明确声明"these lack any in-silico connectivity evidence by design"。

---

## 发现 6 — IFN-γ 阳性对照是循环验证（tautology），且缺少真正的非免疫阴性对照（专长聚焦点 5）

### 【Problem】
§2.8 的 Tier-2 阳性对照门控要求"IFN-γ（经典 MHC-II 诱导剂）必须 rescue ≥3/5 抗原呈递基因"。但 IFN-γ 的 `targets` 列表（脚本 `08_virtual_ko_cmap.py:35`）**本就手工填了 HLA-DRA/HLA-DRB1/HLA-DQA1/HLA-DQB1/CD74 这些抗原呈递基因**，所以该门控按构造必然通过——它是验证"整理者先验"，不是验证"方法能识别真正阳性药"。同时稿件没有真正的**非免疫阴性对照**（已知不作用于免疫的化合物不应高分）。

### 【Evidence】
- 脚本 `08_virtual_ko_cmap.py:81` 的 `ifn_rescue = [g for g in ["HLA-DRA","HLA-DRB1","HLA-DQA1","CD74","CIITA"] if g in set(down_axis)]`——这 5 个基因正是 IFN-γ 在 `DRUG_MAP` 里被手工指定的靶基因。稿件 §3.7（manuscript.md:116）报"IFN-γ rescued 4/5 antigen-presentation genes"，本质是该手工列表与 Mars1-down 轴生物学重叠的必然结果。
- `08_positive_control_check.csv` 第 2 行 `IFN_gamma_rescues_antigen_presentation_axis = True` 正是这一 tautology 的产物。
- 真正的"阳性对照"本应是：**不依赖手工靶列表**，把已知免疫重建剂（如 IFN-γ 若在小分子层、或 vorinostat/entinostat 这类有独立 HLA-II 上调证据的化合物）直接跑同一套 L1000 rescue 管线，要求其排名高于中位数。但 IFN-γ 是生物制剂不在 trt_cp，`S08_l1000_positive_control.csv` 里它标为 N/A。
- 糖皮质激素（prednisone/dexamethasone）虽被标为"阳性对照"，实则是**失败的正面例子**（免疫抑制药却高分），稿件正确地把它当作 caveat；但它恰恰暴露了"缺非免疫阴性对照"——应当补充一组与免疫无关的化合物（如代谢酶抑制剂、DNA 损伤剂）的分布，证明它们整体不高分。

### 【Why it matters】
阳性对照若按构造必然通过，则它**不提供任何方法学判别力**，却占用 Tier-2 门控的信用。审稿人会认为该门控是"装饰性"的。真正需要的是"独立阳性 + 独立阴性"双向判别，才能证明 rescue 度量有特异性。

### 【Specific fix】
1. 用独立数据重建阳性对照（不依赖手工靶列表）。建议：
   > "As an independent method-positive control, we required a set of compounds with established antigen-presentation-restorative transcriptional signatures (retrieved independently of our curated target lists, e.g., from the iLINCS signatures of IFN-γ/GM-CSF pathway inducers) to rank above the 50th percentile of the 20,413-compound rescue distribution; X/Y met this criterion."
2. 增加真正的非免疫阴性对照：
   > "As a negative control, we compiled N compounds with no known immune indication (e.g., DNA topoisomerase inhibitors, HMG-CoA-reductase-independent metabolic agents) and verified their median rescue did not exceed the library median (0.006); this demonstrates the metric is not trivially assigning high scores to all perturbagens."
3. 将糖皮质激素从"阳性对照"重新归类为"特异性反例（failed positive）"，明确其论证角色是显示"rescue≠功能恢复"，而非"方法通过阳性对照"。

---

## 发现 7 — "虚拟敲除"名不副实：无真实扰动签名，退化为"hub 本身下调"（专长聚焦点 6）

### 【Problem】
§2.8 / §3.3 把"hub-gene virtual knockdown to phenocopy immunoparalysis"作为阳性对照，但实现上**没有任何 LINCS CRISPR-KO / siRNA 敲除签名或 in-silico 扰动模拟**；它仅检查"hub 基因是否本身落在 Mars1-down 轴里"，并将"hub 下调 ⇒ 敲除会加重麻痹"作为逻辑结论。这是把"描述性事实"包装成"扰动阳性对照"。

### 【Evidence】
- 脚本 `08_virtual_ko_cmap.py:82-90`：
  ```
  hub_genes = hub["gene"].tolist()
  ko_same_dir = [g for g in hub_genes if g in set(down_axis)]   # hub 在 Mars1 中下调
  ...
  {"check":"hub_KO_phenocopies_immunoparalysis","passed":len(ko_same_dir)>0,
   "detail":f"hub 在 Mars1 下调(虚拟KO加剧麻痹): {ko_same_dir}"}
  ```
  即只要 hub 基因在 Mars1 中下调，就判定"虚拟敲除阳性对照通过"——没有调用任何敲除签名。
- 稿件 §3.3（manuscript.md:102）原文："Virtual knockdown of these hubs phenocopies immunoparalysis (they are themselves Mars1-down), satisfying the knockdown positive control."——作者自己承认该"虚拟敲除"等价于"hub 本身下调"，即循环论证。
- `03_results/08_positive_control_check.csv` 第 3 行确实产出了 `hub_KO_phenocopies_immunoparalysis = True`，但产物是上述 trivial 检查，并非真实虚拟敲除分析结果。

### 【Why it matters】
"virtual knockdown"在药物重定位语境下通常意味着用 LINCS 的 `trt_gene`（过表达）/ `trt_sh`（敲低）或 CRISPR-KO 签名，验证"敲除 hub 后转录组趋近疾病态"。本稿件并无此类产物，却用该术语并通过阳性对照，**虚标了方法学验证层级**。若外审按方法学细查，会判定为"声称了未执行的对照"。

### 【Specific fix】
二选一：
1. **补做真实虚拟敲除**（推荐）：从 LINCS GSE92742 的 `trt_sh`/`trt_gene` 或 ARCHS4/DECREASE 取 hub 基因的敲除 / 敲低签名，计算其与 Mars1-down Axis 的连接度（签名应正相关于疾病轴），作为真正的 perturbation 阳性对照；或
2. **诚实降级术语**：若不做扰动模拟，应删除"virtual knockdown"表述，改为：
   > "Directionality sanity check: all six hub genes are themselves down-regulated in Mars1 (confirmed in §3.1), so their loss-of-function is directionally concordant with the immunosuppressed program. This is a consistency check, not an independent perturbation positive control, and is not used to validate the repositioning pipeline."
   并把它从 Tier-2 "positive-control gate" 中移除或明确标注为非判别性检查。

---

## 发现 8 — `wtcs` 数值不一致：稿件写 1.17，源文件为 0.21（数字错误，附属于 §3.9）

### 【Problem】
稿件 §3.9（manuscript.md:135-136）写 lenalidomide "wtcs 1.17"，但源数据与公式都给出约 0.21，存在明确数字不一致。

### 【Evidence】
- `03_results/S08_l1000_candidate_scores.csv` 第 4 行：lenalidomide `wtcs = 0.2058`。
- 我按脚本公式 `wtcs = (Σ mean_pct − n/2)/√n` 反推：lenalidomide `rescue_score = 0.0439` ⇒ `mean_pct` 均值 = 0.5439 ⇒ `wtcs = (0.5439×22 − 11)/√22 = 0.966/4.690 = 0.206`，与 0.2058 一致。
- 稿件 "1.17" 更接近 `S08_l1000_immuno_overlap.csv` 中 pravastatin 的 `wtcs 1.1557`——很可能是把 Top 救援剂的 wtcs 误抄到了 lenalidomide 描述里。

### 【Why it matters】
虽是小数字，但 `wtcs` 被正文作为连接度证据呈现，且在 §3.9 与 §7 数字溯源表都指向 `S08_l1000_candidate_scores.csv`。这类"正文 ≠ 源文件"的不一致会触发数据溯源审计（A3）质疑整篇数字可信度。

### 【Specific fix】
> "lenalidomide ... (rescue 0.044, wtcs 0.21)" —— 将 "1.17" 改为 "0.21"，并与 `S08_l1000_candidate_scores.csv`（wtcs 0.2058）对齐；同时核对 azithromycin 的 wtcs（源文件 0.0626）是否在正文或表中需要呈现。

---

## 方法学证据层级总评（evidence-tier synthesis）

把稿件的三条重定位证据链按"特异性 / 可证伪性 / 独立性"三维排一个层级，有助于作者与审稿人判断整体 claim 的强度：

| 证据层 | 方法 | 特异性 | 独立性（vs 整理者先验） | 覆盖候选 |
|---|---|---|---|---|
| S08 `rescue_fraction` | 手工靶基因集 ∩ Mars1-down 轴 | 低（下游响应基因，非真实靶点） | 低（靶列表手工填，IFN-γ 门控循环） | 7/7 |
| S08b 文献规则层 | RCT / 上市适应症注释 | 中（外部文献，非本数据集） | 高（独立于本分析） | 7/7 |
| §3.9 L1000 反向连接度 | 单集 rank-percentile rescue | 中（含非特异性高分） | 高（unbiased 数据库） | 2/7（仅小分子） |
| 虚拟敲除阳性对照 | hub 是否本身下调 | 无（trivial） | 无（循环） | 6 hub |

关键判断：**稿件最强的 unbiased 证据（L1000）只覆盖 2/7 候选，而覆盖 7/7 的 S08 `rescue_fraction` 恰恰是特异性最低、最依赖先验的一层**。因此摘要与结论里"in-silico repositioning nominates ..."的语气应向下校准——对 5 个非小分子候选，真正成立的只是"S08b 文献机制注释 + S08 手工重叠"，而非"in-silico 连接度提名"。这不是否定稿件，而是把 claim 的边界说准，避免被方法学审稿人抓"标题与证据不匹配"。

此外，三条证据链之间**缺乏交叉验证的量化聚合**：S08 的 `rescue_fraction` 排序（IL-7>GM-CSF>IFN-γ>...) 与 S08b 临床转化层级（IL-7>GM-CSF>IFN-γ>...) 一致，但二者都来自作者的同一套先验整理，属于"双重印证同一先验"而非"独立证据收敛"。L1000 给出的 lenalidomide/azithromycin 排名（top 26.6% / ≈中位）并未反向约束 S08 排序。建议作者在讨论里明确这一"证据同源性"局限，或引入一个真正独立的排序源（如独立队列的差异表达、或独立数据库靶点）来做三角验证。

---

## 发现 1（补充）— `rescue_fraction` 缺乏统计显著性框架，使分数不可比较

### 【Problem】
`rescue_fraction` 是纯计数比例，没有 Fisher / 超几何检验，也没有考虑 Mars1-down 轴的基线大小。IL-7 的 1.00（5/5）与 BCG 的 0.20（1/5）之间的"差距"无法判断是否为随机重叠所致。

### 【Evidence】
- `08_candidates_drugs.csv` 仅给 `n_target_genes / n_rescue / rescue_fraction`，无 P 值、OR 或 FDR。Mars1-down 轴本身含 ~21–23 个免疫基因（占 25 共识基因的大多数），随机挑 5 个免疫相关基因有较高先验概率落在其中。
- 例如 IL-7 的 5 个靶（CD3D/E、CD8A、IL7R、LCK）全部是 T 细胞基因，而 Mars1-down 轴本就富含 T 细胞 / 抗原呈递基因（§3.6 显示 CD4/CD8 模块相关性最高），故 5/5 可能部分由"轴本身偏向淋巴系"造成，而非 IL-7 特异。

### 【Why it matters】
没有显著性框架，Table 2 的排序只是"作者先验的序数化"，无法支撑"IL-7 显著优于 BCG"的定量结论。审稿人会要求至少报告富集检验。

### 【Specific fix】
在 Table 2 增加两列：
> "For each candidate we report a two-sided Fisher exact test of its direct-target set (DGIdb/ChEMBL) against the Mars1-down axis, with odds ratio and BH-FDR across the 7 candidates. Candidates whose target overlap is not significant after correction are flagged as mechanism-annotated rather than connectivity-validated."

---

## 发现 4（补充）— L1000 landmark 覆盖与签名级连接度的保真度

### 【Problem】
LINCS L1000 直接测量约 978 个 landmark 基因，其余 ~11,000 个基因由线性推断模型还原。稿件的 22 个查询基因多为推断值，抗原呈递基因（HLA-DRA/DRB1、CD74）的恢复保真度未被评估；且用的是"单集 rank-percentile"代理，而非 iLINCS 官方签名级连接度（带 up/down 双尾 KS 的 τ）。

### 【Evidence】
- `S08_l1000_connectivity.py:53-59` 用 `gene_info.txt.gz` 的 `pr_gene_symbol` 把 22 个查询基因映射到 gctx 列，脚本未区分 landmark vs inferred，也未报告二者的计数。
- 脚本注释（line 20）自承是"iLINCS-style wtcs proxy (not the full up/down dual-KS tau)"，即放弃了方向感知与签名级比对，保真度低于官方 iLINCS。

### 【Why it matters】
若 22 个查询基因中多数被推断，rescue 信号经过推断链衰减，且抗原呈递基因恰是免疫特异性最强的部分，其推断误差会系统性削弱"抗原呈递轴救援"这一核心论断的可靠性。

### 【Specific fix】
> "We separated the 22 query genes into L1000 landmarks (directly measured) versus inferred genes and report the count of each; rescue was recomputed restricted to landmarks as a sensitivity analysis. We additionally computed the official iLINCS signed connectivity score (τ, dual-tail KS on up- and down-regulated genes) for lenalidomide and azithromycin to confirm the rank-percentile proxy did not invert the conclusion."

---

## 发现 6（补充）— 建议的阴性对照化合物清单

### 【Problem】
除糖皮质激素外，缺少一组与免疫无关化合物的 rescue 分布作为阴性对照，无法证明度量不是"给所有扰动都打高分"。

### 【Specific fix】
在 §3.9 增补：
> "Negative-control set (N=200, sampled from trt_cp): DNA topoisomerase I/II inhibitors (e.g., topotecan, etoposide), HMG-CoA-reductase-independent metabolic agents (e.g., metformin, 2-deoxyglucose), and nucleotide-analogue DNA synthesis inhibitors (e.g., cytarabine). Their median rescue (report value) was not significantly above the library median 0.006 (Wilcoxon P=…), demonstrating the metric discriminates immune from non-immune perturbations only weakly and motivating the functional-validation requirement."

---

## § Stands up（我怀疑过、但核查后确认稿件正确的地方）

以下各项我最初持怀疑态度，但亲自重算 / 核对源文件后确认稿件**正确**，记录在此作为交付物：

1. **§3.1 的 "21/25 方向性下调、22/25 显著（FDR<0.05）"** —— 我逐行核对 `S01_immunoparalysis_direction.csv`：25 基因中 Mars1_down 共 23 个、Mars1_up 2 个（PDCD1、LAG3）；其中 FDR<0.05 的共 22 个（含 PDCD1 这一 up 基因），故"方向性下调 21 + 显著 22"自洽正确。✓
2. **§3.9 背景统计（mean/median 0.006，53.6% >0）** —— 我重算 `S08_l1000_rescue_trtcp.csv`（20,413 行）得 mean 0.0064、median 0.0055、frac>0 = 0.5362，与稿件四舍五入一致。✓
3. **§3.9 "top rescue 0.32" 与候选排名** —— 全库最大 rescue = 0.3182（≈0.32，由 BRD-K89995901 取得），确认稿件"最强救援 rescue 0.32"正确；lenalidomide rank 5435/20413（top 26.6%）、azithromycin 9152/20413（pct 0.448，≈中位）与 `S08_l1000_candidate_scores.csv` 完全一致。✓
4. **§3.7 的 rescue_fraction 计数本身** —— IL-7 5/5=1.00、GM-CSF 5/6=0.833、IFN-γ 5/7=0.714、Azithromycin 2/3=0.667、Lenalidomide 2/5=0.40、Thymosin 0.40、BCG 1/5=0.20，与 `08_candidates_drugs.csv` 一致；计算无误（问题在"target"语义，非算术）。✓
5. **糖皮质激素也高分的 caveat 诚实性** —— 我确认 `S08_l1000_positive_control.csv` 中 prednisone rescue 0.136（rank 651）、dexamethasone 0.0315（rank 6808），稿件如实标注"必要非充分"，未掩饰。✓

---

## 六专长聚焦点逐条对应小结

| 派发聚焦点 | 本评审对应发现 | 结论 |
|---|---|---|
| 1. `target` 定义特异性（是否应为真实靶点） | 发现 1 + 发现 1 补充 | 当前为下游响应基因集，非真实靶点；建议换 DGIdb/ChEMBL 重算并加 Fisher 检验 |
| 2. Mars1-down axis 定义（是否与 §3.1 同一集） | 发现 2 | 否——真实 query 为 25 共识免疫基因中 22 个可测者，含 2 个 up 基因、缺 2 个 hub；需 signed 重定义 |
| 3. L1000 能否表征功能免疫恢复 + 糖皮质激素 caveat 充分性 | 发现 3、发现 4（+补充） | BRD 误标 BET 须改；caveat 已诚实但需补非特异高分化合物与显著性框架 |
| 4. 仅 2/7 在 L1000 是否削弱 claim | 发现 5 | 是，需把连接度证据显式限定到小分子，其余标为假设生成 |
| 5. 阳性对照门控力度（IFN-γ 是否 tautology） | 发现 6（+补充） | 是循环验证，需独立阳性 + 非免疫阴性双向对照 |
| 6. 虚拟敲除是否真实产物（是否虚标） | 发现 7 | 名不副实，无真实扰动签名，需补做或降级术语 |

---

## 发现 5（补充）— 非小分子候选的替代 in-silico 证据路径

### 【Problem】
对 IL-7/GM-CSF/IFN-γ/胸腺肽α1/BCG 这 5 个无法进 L1000 `trt_cp` 的候选，稿件仅以 S08b 文献层兜底，缺乏任何"计算"层面的第二证据，使"计算重定位"对多数候选落空。

### 【Evidence】
- `S08_l1000_candidate_scores.csv` 只有 2 行；`S08_l1000_positive_control.csv` 中 IFN-γ 标 N/A。
- `08b_clinical_translation.csv` 提供了 RCT / 上市证据，但这是**文献注释**而非本分析产出的连接度。

### 【Why it matters】
若能为生物制剂也提供一条独立的 in-silico 证据（如基于已知靶点-基因调控网络），可把"5/7 无连接度"的缺口补一部分，提升整体 claim 的整齐度。

### 【Specific fix】
> "For the five biologic/vaccine candidates absent from L1000 trt_cp, we supplemented the literature-rule layer (S08b) with an independent in-silico check: using the INDRA/DrugBank target–gene network, we verified that each candidate's established receptors/targets (e.g., IL7R, CSF2RB, IFNGR1/2) are themselves down-regulated in Mars1, providing a mechanistic (not connectivity) concordance. These remain hypothesis-generating pending functional validation (S11)."

---

## § Questions for the authors（需作者澄清，不代答）

1. **真实靶点来源**：7 个候选的 `rescue_fraction` 当前基于手工"响应基因集"。请说明是否有计划用 DGIdb/ChEMBL 真实靶点重算？若重算后真实靶点与 Mars1-down 轴重叠很低，作者是否准备下调相关候选的优先级？
2. **L1000 query 22 基因的定义脚本**：`mars1_down_l1000_idx.json` 的生成脚本是否在仓库中（`02_scripts/` 未见生成该 json 的脚本）？请补充该 json 的生成代码与时间戳，以便审计"22"这一数字的确切来源与方向处理。
3. **Top BRD 化合物的真实身份**：能否提供 Top 25 救援剂的 `pert_iname` + pharmacologic class 映射表？其中确实有多少是 BET 抑制剂，多少是其他类别（激酶抑制剂、凋亡诱导剂等）？
4. **虚拟敲除的实现意图**：作者是否计划在返修中加入基于 LINCS `trt_sh`/CRISPR-KO 签名的真实虚拟敲除分析？还是接受将其降级为"方向性一致性检查"？
5. **非免疫阴性对照**：是否有计划补充一组与免疫无关的化合物的 rescue 分布作为阴性对照？目前仅有糖皮质激素这一"失败正面例子"，缺乏真正的阴性判别。
6. **显著性阈值**：rescue / wtcs 是否设定了基于 20,413 背景的显著性判据（z-score 或 top-k%）？lenalidomide（top 26.6%）与 azithromycin（≈中位）是否越过该阈值，作者如何界定"显著救援"？

---

## § What I actually checked（审计轨迹）

**读取的文件（亲自核对）：**
- `05_reports/review/_PANEL_BRIEF.md` —— 独立性纪律与必查数字清单。
- `05_reports/manuscript.md`（全文 299 行）—— §2.8、§3.1、§3.3、§3.7、§3.8、§3.9、§5 #7、摘要、结论、§7 溯源表。
- `03_results/08_candidates_drugs.csv` —— 7 候选 rescue_fraction 与 target 列表（逐行核对）。
- `03_results/08_positive_control_check.csv` —— IFN-γ 门控与 hub-KO 检查（确认 tautology）。
- `03_results/S08_l1000_candidate_scores.csv` —— azithromycin/lenalidomide 的 rescue/rank/wtcs。
- `03_results/S08_l1000_positive_control.csv` —— 糖皮质激素与已知免疫调节剂的 rescue。
- `03_results/S08_l1000_immuno_overlap.csv` —— Top 救援剂（含非免疫化合物：四氯乙烯、制霉菌素、卡那霉素、放线菌素等）。
- `03_results/S01_immunoparalysis_direction.csv` —— 25 共识免疫基因方向 / FDR（用于核查 §3.1 数字与 query 集方向）。
- `03_results/08b_clinical_translation.csv` —— 候选临床转化层级（确认与 rescue 层级一致）。
- `01_data/LINCS/mars1_down_l1000_idx.json` —— 真实 22 基因 L1000 query 集合（发现含 PDCD1/LAG3 两个 up 基因，缺 HAVCR2/FCGR3A/TIGIT）。
- `02_scripts/python/08_virtual_ko_cmap.py` —— 确认 rescue_fraction 与"虚拟敲除"均为手工 / 逻辑实现，无真实扰动签名。
- `02_scripts/python/S08_l1000_connectivity.py` 与 `S08_l1000_postprocess.py` —— 确认 rescue/wtcs 公式、rank 列来源、Top 救援剂为 BRD- 匿名 ID。

**运行的重算（Python，03 源文件）：**
- 对 `S08_l1000_rescue_trtcp.csv`（20,413 行）计算 rescue 分布：mean 0.0064、median 0.0055、frac>0 = 0.5362；最大 rescue 0.3182；Top 8 救援剂全部为 BRD- 前缀。
- 按公式反推 lenalidomide wtcs = 0.206，对照源文件 0.2058，确认稿件 "1.17" 为错误。
- 将 json 的 22 基因逐一与 `S01_immunoparalysis_direction.csv` 方向比对，确认 LAG3、PDCD1 为 Mars1_up，HAVCR2/FCGR3A/TIGIT 缺失（含 2 hub）。

**差异 / 未决项：**
- 稿件 wtcs 1.17（lenalidomide）≠ 源 0.2058 —— 已作为发现 8 记录。
- `S08_l1000_rescue_trtcp.csv` 本身不含 rescue_rank/pct_rank 列（由 postprocess 写入派生文件），属轻微的溯源不一致，但排名数字（5435/9152）在 `candidate_scores.csv` 中正确，不影响结论。
- 未发现其他正文与源文件之间的重大数字冲突（§3.1、§3.9 背景与排名均核对一致）。

**未读取（遵守独立性纪律）：** 其他专家评审文件、`*REVIEW*`/`*RESPONSE*`、PIPELINE 执行注释、`*_gen_*.py`、`06_literature/`、`GITHUB_DEPOSIT_SOP.md`、`.workbuddy/`。

---

## 数字核对速查表（正文 claim ↔ 源文件 ↔ 我的重算）

| 稿件 claim | 位置 | 源文件 / 公式 | 我的核对结果 | 判定 |
|---|---|---|---|---|
| 21/25 方向性下调、22/25 显著 | §3.1 | `S01_immunoparalysis_direction.csv` | 23 down / 2 up；22 FDR<0.05（含 1 up） | ✓ 一致 |
| rescue_fraction IL-7 1.00 / GM-CSF 0.833 / IFN-γ 0.714 / Azi 0.667 / Lena 0.40 / Tα1 0.40 / BCG 0.20 | §3.7 / Table 2 | `08_candidates_drugs.csv` | 计数与 CSV 完全一致 | ✓ 算术正确（语义见发现 1） |
| L1000 背景 mean/median 0.006，53.6% >0 | §3.9 | `S08_l1000_rescue_trtcp.csv`（20,413 行） | 0.0064 / 0.0055 / 0.5362 | ✓ 四舍五入一致 |
| max rescue 0.32 | §3.9 | 同上加排序 | 0.3182 (BRD-K89995901) | ✓ 一致 |
| lenalidomide rank 5435/20413, top 26.6%, rescue 0.044, **wtcs 1.17** | §3.9 | `S08_l1000_candidate_scores.csv` | rescue 0.0439 / rank 5435 / pct 0.26625；wtcs 应为 0.2058（公式反推 0.206） | ✗ **wtcs 1.17 错误，应为 0.21** |
| azithromycin rank 9152/20413, rescue 0.013 | §3.9 | `S08_l1000_candidate_scores.csv` | rescue 0.0133 / rank 9152 / pct 0.448 | ✓ 一致 |
| prednisone rescue 0.136 rank 651；dexamethasone 0.032 rank 6808 | §3.9 | `S08_l1000_positive_control.csv` | 0.1364/651；0.0315/6808 | ✓ 一致 |
| "22 Mars1-down genes" | §3.9 | `mars1_down_l1000_idx.json` | 实际 22 = 25 共识免疫基因中可测者，含 PDCD1/LAG3（up）、缺 HAVCR2/FCGR3A/TIGIT（含 2 hub） | ✗ **非纯 Mars1-down** |
| Top 救援剂 "BRD-series (BET inhibitors)" | §3.9 | `S08_l1000_rescue_trtcp.csv` Top 8 | 全部 BRD- 匿名 ID，未解析药理类 | ✗ **BRD≠BET，须解析真实身份** |
| IFN-γ rescue 4/5 抗原呈递基因（阳性对照通过） | §3.7 / §2.8 | `08_positive_control_check.csv` + `08_virtual_ko_cmap.py:81` | 靶列表手工含这 5 个 AP 基因 | ✗ **循环验证** |
| hub 虚拟敲除阳性对照通过 | §3.3 | `08_virtual_ko_cmap.py:82-90` | 仅检查 hub 是否本身下调 | ✗ **名不副实** |
