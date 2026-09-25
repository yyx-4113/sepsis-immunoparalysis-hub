# GitHub 复现包投稿操作手册（中文）

本手册说明如何把本项目（`sepsis-immunoparalysis-hub`）作为**可复现研究包**发布到 GitHub，
并在稿件录用/上线后作为数据可用性声明（Data Availability Statement）的实名仓库 URL 来源。

> 纪律：数据可用性声明一律写**实名仓库 URL + 版本 tag + MANIFEST 校验和**，禁止 "available on request"。

---

## 0. 前置条件

- 已注册 GitHub 账号 `yyx-4113`（科研账号；课程作业账号 `yongxinyang` 与本稿无关，勿引用）。
- 本地已安装 git，且能访问 github.com（中国大陆通常需开代理软件并对齐端口；若 `git ls-remote` 报
  `127.0.0.1:443` 连接失败，先清代理直连或对齐代理端口）。
- 本仓库**不含**大数据矩阵：LINCS `GSE92742_Level5_COMPZ.gctx`（~23 GB）不入库，仅在 README 注明下载方式。

## 1. 初始化与首次提交

```bash
cd <本仓库根目录>
git init
git branch -M main
git add LICENSE CITATION.cff README.md MANIFEST.csv \
        00_pipeline 02_scripts 03_results 04_figures 05_reports 06_literature
git commit -m "Initial reproducible analysis package (v1.0.0)"
git remote add origin git@github.com:yyx-4113/sepsis-immunoparalysis-hub.git
git push -u origin main
```

## 2. 打版本 tag（数据可用性声明要用）

```bash
git tag -a v1.0.0 -m "Sepsis immunoparalysis hub: multi-omics + L1000 repositioning v1.0.0"
git push origin v1.0.0
```

- tag 触发 `.github/workflows/release.yml`：自动校验 `MANIFEST.csv` 中所有产物的 SHA-256，
  并创建 GitHub Release 附带 MANIFEST/CITATION.cff/LICENSE。

## 3. 数据可用性声明写法（稿件内）

> Processed expression and phenotype matrices, all result tables, and analysis code are available at
> **https://github.com/yyx-4113/sepsis-immunoparalysis-hub** (tag **v1.0.0**); file integrity is
> verified by `MANIFEST.csv` (SHA-256). Raw inputs: GEO GSE65682 (GPL13667), ArrayExpress
> E-MTAB-4451 (GPL10558), GEO GSE92742 (LINCS L1000). This study used and re-analyzed public
> research data; no new primary data were generated.

## 4. 更新产物后如何重新发布

1. 复跑受影响脚本，确认 `03_results/`、`04_figures/` 更新。
2. 重新生成 MANIFEST：`python -c "import hashlib,os,csv; ..."` 或运行生成脚本（见 README）。
3. `git add -A && git commit -m "..." && git push`。
4. 升版本号（如 v1.0.1）→ `git tag -a v1.0.1 -m "..." && git push origin v1.0.1`。

## 5. 注意事项

- 切勿 `git add` 整个 `01_data/`（含 21 GB LINCS gctx），用 `.gitignore` 排除：
  `echo "01_data/LINCS/*.gctx" >> .gitignore`。
- 提交前确认不含任何个人令牌（OpenGWAS JWT、GitHub token）— 本仓库不含凭证文件。
- 作者署名只用 **Yongxin Yang**（无 MD / PhD / MS 等研究生以上学位头衔）；ORCID 0009-0004-9698-6552。
