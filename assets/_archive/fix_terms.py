from pathlib import Path

p = Path(r"C:\Users\User\Desktop\文件\週3_物聯網應用與資料分析_陳煥\week8_2026_10_28\報告\Proposal_Document.md")
t = p.read_text(encoding="utf-8")
for a, b in [("平臺", "平台"), ("儀錶", "儀表"), ("約佔", "約占")]:
    t = t.replace(a, b)
p.write_text(t, encoding="utf-8")
print("ok")
