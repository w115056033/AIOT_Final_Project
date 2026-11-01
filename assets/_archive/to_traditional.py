from pathlib import Path
from zhconv import convert

p = Path(r"C:\Users\User\Desktop\文件\週3_物聯網應用與資料分析_陳煥\week8_2026_10_28\報告\Proposal_Document.md")
t = p.read_text(encoding="utf-8")
converted = convert(t, "zh-tw")
p.write_text(converted, encoding="utf-8")
print("converted", len(t), "->", len(converted))
