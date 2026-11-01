from pathlib import Path
import re, sys

p = Path(r"C:\Users\User\Desktop\文件\週3_物聯網應用與資料分析_陳煥\week8_2026_10_28\報告\Proposal_Document.md")
t = p.read_text(encoding="utf-8")
# Characters that are simplified-only (a practical subset). Some are shared, so
# only flag suspicious multi-character words and clearly simplified variants.
bad = [
    "路线", "数据", "网络", "应用", "这个", "为什", "台湾", "资讯", "云端", "风险",
    "应该", "进行", "透过", "软体", "硬体", "资料库", "连结", "网路", "行动", "装置",
    "通讯", "许可", "申请", "抽签", "统计", "平台", "法规", "范围", "团队", "成员",
    "时间", "问题", "学习", "训练", "预测", "评估", "设计", "架构", "流程", "测试",
    "最佳化", "建立", "实作", "内容", "整合", "产生", "包含", "支援", "验证",
    "国际", "开发", "开放", "关於", "关于", "机制", "数据", "机器", "学习",
    "这个", "这些", "那些", "为何", "什么", "怎么", "因为", "所以", "并且",
    "可以", "能够", "透过", "藉由", "并", "与", "为", "个", "这", "来", "时",
]
found = []
for b in bad:
    i = 0
    while True:
        i = t.find(b, i)
        if i < 0:
            break
        found.append((b, t.count("\n", 0, i) + 1, t[max(0, i-18):i+18].replace("\n", " ")))
        i += len(b)
print("count", len(found))
for b, line, ctx in found[:300]:
    print(f"{b}\tL{line}\t{ctx}")
