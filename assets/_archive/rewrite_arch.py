# -*- coding: utf-8 -*-
import pathlib

p = pathlib.Path(r"assets\build_figures.py")
s = p.read_text(encoding="utf-8")
start = s.index("def architecture():")
end = s.index("# =========================================================\n# 3. Flowchart", start)

new = r'''def architecture():
    fig, ax = plt.subplots(figsize=(16, 10.2), dpi=220)
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)
    ax.set_xlim(0, 16); ax.set_ylim(0, 10.2); ax.axis("off")

    ax.text(0.55, 9.95, "TrailGuard TW — 系統架構", fontsize=25, fontweight="bold", color=DARK, va="top")
    ax.text(0.55, 9.52, "Evidence-grounded Domain Data Agent｜LLM 負責理解與解釋，Analytics Engine 負責計算與驗證",
            fontsize=11.5, color=SLATE, va="top")
    ax.plot([0.55, 10.9], [9.30, 9.30], color=MOSS, lw=1.2, alpha=0.7)

    # Right safety rail
    rounded(ax, 11.25, 0.95, 4.1, 8.15, fc="#EDF3EE", ec=MOSS, lw=1.2)
    ax.text(11.55, 8.78, "Safety & Evidence Layer", fontsize=12.5, fontweight="bold", color=PINE)
    ax.text(11.55, 8.48, "跨層治理，不屬於單一模組", fontsize=9, color=SLATE)
    rail = [
        ("Evidence Ledger", "每個數字／規則 → 來源＋時間戳"),
        ("Hard Red Flags", "颱風、封閉、AMS 症狀 → 覆寫評分"),
        ("Source Hierarchy", "官方 > 同儕審查 > 社群"),
        ("Privacy by Design", "最小化個資、可刪除、可離線"),
        ("Human Escalation", "119／112、留守人、專業判斷"),
        ("Uncertainty", "P50／P90、信心等級、敏感度"),
    ]
    yy = 8.02
    for i, (t, d) in enumerate(rail):
        ax.add_patch(Circle((11.55, yy - 0.07), 0.055, fc=EMBER, ec="none"))
        ax.text(11.70, yy, t, fontsize=9.6, fontweight="bold", color=DARK, va="top")
        ax.text(11.70, yy - 0.27, d, fontsize=8.3, color=SLATE, va="top")
        yy -= 0.92

    def band_header(y, num, title, sub):
        ax.add_patch(Circle((0.78, y), 0.22, fc=PINE, ec="none"))
        ax.text(0.78, y - 0.005, num, fontsize=10.5, color=WHITE, ha="center", va="center", fontweight="bold")
        ax.text(1.12, y + 0.08, title, fontsize=12.2, fontweight="bold", color=DARK, va="center")
        ax.text(1.12, y - 0.24, sub, fontsize=8.4, color=SLATE, va="center")

    # ---- Band 1: users + interaction ----
    band_header(8.80, "①", "使用者與應用情境", "新手自組隊、進階領隊、家庭／親子（MVP 以前兩者為主）")
    ux = 2.15
    for label in ["新手自組隊\n（2–4 人）", "進階領隊\n（多日縱走）", "家庭／親子\n（單日）"]:
        rounded(ax, ux, 7.75, 2.55, 0.55, fc=WHITE, ec=MOSS, lw=1.0)
        ax.text(ux + 1.275, 8.025, label, fontsize=8.6, color=DARK, ha="center", va="center", linespacing=1.2)
        ux += 2.75

    band_header(7.35, "②", "問題輸入與互動介面", "自然語言＋結構化 Trip Brief＋地圖／PDF／離線卡")
    ix = 2.15
    for label in ["Chat\n追問與補齊", "Trip Brief\n體能／經驗／限制", "Map\n路線與撤退點", "PDF／離線\n行前包"]:
        rounded(ax, ix, 6.40, 2.02, 0.55, fc=SAND, ec=MOSS, lw=0.9)
        ax.text(ix + 1.01, 6.675, label, fontsize=8.4, color=DARK, ha="center", va="center", linespacing=1.18)
        ix += 2.18

    arrow(ax, 4.15, 7.73, 4.15, 6.97, color=MOSS, lw=1.4)

    # ---- Band 2: agent ----
    band_header(5.95, "③", "領域資料分析代理人（核心大腦）", "Understand → Plan → Acquire → Analyze → Generate → Verify → Interact")
    rounded(ax, 2.10, 4.30, 8.85, 1.30, fc="#E8F0EA", ec=PINE, lw=1.4)
    steps = [
        ("Understand", "意圖／限制"), ("Plan", "拆解子任務"), ("Acquire", "呼叫工具"),
        ("Analyze", "計算與模型"), ("Generate", "3 個候選"), ("Verify", "證據核對"),
        ("Interact", "呈現與追問"),
    ]
    sx = 2.28
    for i, (t, d) in enumerate(steps):
        fc = "#FBE9DF" if t == "Verify" else WHITE
        ec = EMBER if t == "Verify" else PINE
        rounded(ax, sx, 4.66, 1.10, 0.62, fc=fc, ec=ec, lw=1.0, rad=0.012)
        ax.text(sx + 0.55, 5.06, t, fontsize=7.8, fontweight="bold", color=DARK, ha="center", va="center")
        ax.text(sx + 0.55, 4.85, d, fontsize=6.7, color=SLATE, ha="center", va="center")
        if i < len(steps) - 1:
            arrow(ax, sx + 1.12, 4.97, sx + 1.25, 4.97, color=MOSS, lw=1.0)
        sx += 1.26
    ax.text(2.28, 4.43, "State machine＋typed tools＋structured outputs＋reflection loop（Verify 可退回 Plan／Generate）",
            fontsize=7.4, color=SLATE, va="center")

    caps = ["TALK", "KNOW", "SENSE", "ANALYZE", "THINK", "SHOW"]
    cx = 2.28
    for c in caps:
        rounded(ax, cx, 3.80, 1.32, 0.28, fc=PINE, ec=PINE, lw=0.8, rad=0.010)
        ax.text(cx + 0.66, 3.94, c, fontsize=7.1, color=WHITE, ha="center", va="center", fontweight="bold")
        cx += 1.42
    ax.text(10.15, 3.94, "④ 六大能力", fontsize=7.6, color=PINE, ha="right", va="center", fontweight="bold")
    arrow(ax, 6.60, 6.38, 6.60, 5.62, color=MOSS, lw=1.5)

    # ---- Band 3: data & tools ----
    band_header(3.42, "⑤", "資料來源與工具層", "知道什麼時候該用哪一種資料；不把 LLM 當資料庫")
    data = [
        ("IoT／穿戴", "GPS、氣壓、心率、SpO2\n（手機＋ESP32 選配）", SKY),
        ("內部資料", "使用者檔案、行程紀錄\n評測標註、事故資料", PINE),
        ("外部 API", "CWA 天氣、警特報\n公路／園區狀態", EMBER),
        ("知識庫", "官方規則、步程、山屋\n高山症、裝備、RAG", MOSS),
        ("分析工具", "Python、GeoPandas\nOR-Tools、scikit-learn", GOLD),
    ]
    dx = 2.15
    for t, d, col in data:
        rounded(ax, dx, 2.40, 1.62, 0.72, fc=WHITE, ec=col, lw=1.2)
        ax.add_patch(Rectangle((dx, 2.40), 0.07, 0.72, fc=col, ec="none"))
        ax.text(dx + 0.16, 2.98, t, fontsize=8.1, fontweight="bold", color=DARK, va="center")
        ax.text(dx + 0.16, 2.71, d, fontsize=6.9, color=SLATE, va="center", linespacing=1.2)
        dx += 1.76
    arrow(ax, 6.60, 3.78, 6.60, 3.15, color=MOSS, lw=1.5)

    # ---- Band 4: analytics -> decision -> output ----
    for x, num, title, sub in [
        (2.10, "⑥", "分析引擎", "步程、天氣窗、AMS、風險、最佳化"),
        (4.95, "⑦", "決策與建議", "Go／No-Go、3 個方案、撤退點"),
        (7.80, "⑧", "輸出與互動", "Chat、Dashboard、Map、PDF、Alert"),
    ]:
        ax.add_patch(Circle((x + 0.18, 2.02), 0.17, fc=PINE, ec="none"))
        ax.text(x + 0.18, 2.015, num, fontsize=8.8, color=WHITE, ha="center", va="center", fontweight="bold")
        ax.text(x + 0.42, 2.06, title, fontsize=9.8, fontweight="bold", color=DARK, va="center")
        ax.text(x + 0.42, 1.82, sub, fontsize=6.9, color=SLATE, va="center")

    rounded(ax, 2.10, 1.00, 2.55, 0.68, fc="#EDF3EE", ec=PINE, lw=1.2)
    ax.text(3.37, 1.41, "Analytics Engine", fontsize=9.0, fontweight="bold", color=PINE, ha="center")
    ax.text(3.37, 1.18, "時間 P50/P90｜風險分解｜敏感度", fontsize=6.8, color=SLATE, ha="center")
    arrow(ax, 4.68, 1.34, 4.92, 1.34, color=MOSS, lw=1.3)

    rounded(ax, 4.95, 1.00, 2.55, 0.68, fc="#FBE9DF", ec=EMBER, lw=1.2)
    ax.text(6.22, 1.41, "Decision Layer", fontsize=9.0, fontweight="bold", color=EMBER, ha="center")
    ax.text(6.22, 1.18, "安全／平衡／進取＋Evidence", fontsize=6.8, color=SLATE, ha="center")
    arrow(ax, 7.53, 1.34, 7.77, 1.34, color=MOSS, lw=1.3)

    rounded(ax, 7.80, 1.00, 3.12, 0.68, fc=WHITE, ec=PINE, lw=1.2)
    ax.text(9.36, 1.41, "Output Layer", fontsize=9.0, fontweight="bold", color=PINE, ha="center")
    ax.text(9.36, 1.18, "行前簡報｜風險儀表板｜離線緊急卡", fontsize=6.8, color=SLATE, ha="center")

    # feedback loop
    arrow(ax, 10.95, 1.34, 11.15, 1.34, color=MOSS, lw=1.2, ls="--")
    arrow(ax, 10.95, 1.34, 10.95, 3.70, color=MOSS, lw=1.2, ls="--", rad=0)
    ax.text(11.02, 2.55, "feedback", fontsize=6.9, color=MOSS, rotation=90, va="center")

    save(fig, "fig_architecture.png")


'''

p.write_text(s[:start] + new + s[end:], encoding="utf-8")
print("rewritten")
