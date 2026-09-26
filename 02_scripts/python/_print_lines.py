import sys
p = "05_reports/manuscript.md"
targets = [int(x) for x in sys.argv[1:]]
lines = open(p, encoding="utf-8").read().split("\n")
for ln in targets:
    print(f"===== LINE {ln} (len={len(lines[ln-1])}) =====")
    print(lines[ln-1])
    print()
