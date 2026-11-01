from pathlib import Path
from collections import Counter

p = Path(r"C:\Users\User\Desktop\文件\週3_物聯網應用與資料分析_陳煥\week8_2026_10_28\報告\Proposal_Document.md")
t = p.read_text(encoding="utf-8")
simplified_only = "约体资开这为与个来时间会说过还进远边关门问题实际验证据数网络应该软硬标记连结网路行动装置通讯许可申请抽签统计法规范围团队员学习训练预测评估设计架构测试最佳化建立实作内容整合产生包含支援国际开发机制机器为何什么怎么因为并且能够藉由"
cnt = Counter(ch for ch in t if ch in simplified_only)
print(cnt)
for ch, _ in cnt.most_common():
    for i, line in enumerate(t.splitlines(), 1):
        if ch in line:
            print(f"{ch}\tL{i}\t{line[:120]}")
