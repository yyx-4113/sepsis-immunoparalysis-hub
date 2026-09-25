# ============================================================
# insert_references.py
# 将 build_references.py 生成的 29 条参考文献写入 manuscript.md，
# 替换旧的 core-set stub；并清理 Funding 段的 [Verify before submission] 标注
# （用户已确认无基金资助）
# ============================================================
import re, io

MANU = "05_reports/manuscript.md"
GEN = "03_results/generated_references.md"

with open(GEN, encoding="utf-8") as f:
    gen_lines = f.read().splitlines()
# drop generated heading + following blank line, keep numbered entries
entries = [ln for ln in gen_lines if re.match(r"^\d+\.\s", ln)]
assert len(entries) >= 25, f"unexpected entry count: {len(entries)}"
ref_block = "## References\n\n" + "\n".join(entries) + "\n"

with open(MANU, encoding="utf-8") as f:
    text = f.read()

# --- Funding: confirm no-funding, remove verify tag ---
text = re.sub(
    r"This work received no specific grant from any funding agency \(single-author, self-funded\)\. \[Verify before submission\]",
    "This work received no specific grant from any funding agency or commercial entity. "
    "The author is solely responsible for all costs associated with this study.",
    text,
)

# --- References: replace everything from '## References' to end of file ---
idx = text.find("## References")
assert idx != -1, "References section not found"
text = text[:idx] + ref_block

with open(MANU, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Inserted {len(entries)} references; Funding tag cleared.")
print("References section now ends at char", idx, "-> rewritten.")
