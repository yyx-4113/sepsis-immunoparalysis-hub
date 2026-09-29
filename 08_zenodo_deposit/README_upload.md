# Zenodo 上传说明（v1.19.1）

## 重要：为何不在沙箱内直接上传

本项目的 WorkBuddy 沙箱网络被代理白名单限制，**只能到达 GitHub，无法解析/连接 `zenodo.org`**（DNS 解析失败、代理返回 000）。因此 mint DOI 这一步**必须在你本机（能正常访问 zenodo.org 的机器）完成**。下面给出两条路线，二选一即可——**不要两条都做，否则会产生重复的 Zenodo 记录**。

存档包已就绪：`sepsis-immunoparalysis-hub-v1.19.1.zip`（5.76 MB，已排除 43 GB 原始数据）。

---

## 路线 A：脚本一键上传（推荐，最少手动操作）

要求：本机有 Python 3（标准库即可，无需 pip 安装任何包）。

1. 把本仓库 clone / 拷贝到本机（至少包含 `08_zenodo_deposit/` 目录）。
2. 打开终端，进入 `08_zenodo_deposit/`。
3. 设置 Zenodo 个人访问令牌（仅在终端环境变量，**不要写进任何文件或分享**）：
   - Windows PowerShell：`$env:ZENODO_TOKEN = "你的token"`
   - macOS/Linux：`export ZENODO_TOKEN="你的token"`
4. 运行：
   ```bash
   python publish_zenodo.py
   ```
5. 脚本依次完成：创建 deposition → 上传 zip → 写入 metadata → 发布，并打印：
   - `DOI`（本版本 DOI，形如 `10.5281/zenodo.XXXXXXX`）
   - `Concept DOI`（永久概念 DOI，跨版本不变）
   - `Record URL`

> 若你的本机需要代理才能访问外网，先设置 `HTTPS_PROXY` / `HTTP_PROXY` 环境变量，脚本会自动使用。

---

## 路线 B：zenodo.org 网页手动上传

1. 登录 https://zenodo.org （用你的账户，即 token 对应的账户）。
2. 右上角 **Upload** → **New upload**。
3. 把 `sepsis-immunoparalysis-hub-v1.19.1.zip` 拖入文件区。
4. 按下方字段填写（内容均与 `zenodo_metadata.json` 一致，可直接复制）：

   | 字段 | 值 |
   |------|-----|
   | Upload type | Software |
   | Title | Reproducible multi-omics pipeline and in-silico drug repositioning for the immunosuppressed Mars1 sepsis endotype (v1.19.1) |
   | Authors | Yang, Yongxin（ORCID 0009-0004-9698-6552）；Affiliation: The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou, Fujian 350003, China |
   | Description | 复制 `zenodo_metadata.json` 中 `metadata.description` 全文 |
   | Keywords | sepsis, immunoparalysis, MARS endotype, multi-omics, drug repositioning, LINCS L1000, transcriptomics, Mendelian randomization, reproducible research |
   | License | MIT |
   | Version | v1.19.1 |
   | Related identifiers | isSupplementTo → https://github.com/yyx-4113/sepsis-immunoparalysis-hub |
   | Resource type (related) | Software |
   | Access right | Open |

5. 点 **Publish**。发布后页面给出 DOI。

---

## 取得 DOI 后：回填到以下文件

把 `10.5281/zenodo.XXXXXXX` 回填（将"will be minted on acceptance"替换为实际 DOI，并保留 GitHub tag v1.19.1 引用）：

- `05_reports/manuscript.md` — §Data availability 段
- `07_submission_v1.19.1/Reporting_Summary.docx` — Data availability 段
- `07_submission_v1.19.1/Data_Availability_Statement.txt` — 粘贴到 Snapp 的文本
- `07_submission_v1.19.1/SUBMISSION_MANIFEST.md`
- `CITATION.cff` — 加 `identifiers: [{type: doi, value: 10.5281/zenodo.XXXXXXX}]`
- `08_zenodo_deposit/zenodo_metadata.json` — 加 `related_identifiers` 项（relation `isCitedBy` 待文章接收后补）

回填后提交并推送即可。

## 安全提示

- **令牌仅存在于你本机的一次性环境变量**，不要写入仓库、不要截图分享、不要用明文 `--token` 参数。
- Zenodo 一旦 Publish 即生成公开、不可逆的 DOI；发布前请核对 metadata 与 zip 内容。
- 如果你日后走 GitHub release 自动集成路线，请勿同时用脚本上传，以免重复。
