# -*- coding: utf-8 -*-
import pathlib

p = pathlib.Path(r"assets\build_figures.py")
s = p.read_text(encoding="utf-8")
start = s.index("def flowchart():")
end = s.index("# =========================================================\n# 4. Risk matrix", start)

new = r'''def flowchart():
    fig, ax = plt.subplots(figsize=(16, 9.2), dpi=220)
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)
    ax.set_xlim(0, 16); ax.set_ylim(0, 9.2); ax.axis("off")

    ax.text(0.55, 8.85, "TrailGuard TW — 處理流程", fontsize=24, fontweight="bold", color=DARK, va="top")
    ax.text(0.55, 8.42, "Input → Processing → AI／Analytics → Decision → Output，含追問、例外、驗證與回饋迴圈",
            fontsize=10.8, color=SLATE, va="top")
    ax.plot([0.55, 10.2], [8.22, 8.22], color=MOSS, lw=1.1, alpha=0.7)

    def box(x, y, w, h, title, sub="", fc=WHITE, ec=PINE, tc=DARK, fs=14, sfs=8.0):
        rounded(ax, x, y, w, h, fc=fc, ec=ec, lw=1.2)
        if sub:
            ax.text(x + w/2, y + h*0.62, title, fontsize=fs, fontweight="bold", color=tc, ha="center", va="center")
            ax.text(x + w/2, y + h*0.27, sub, fontsize=sfs, color=SLATE, ha="center", va="center", linespacing=1.2)
        else:
            ax.text(x + w/2, y + h/2, title, fontsize=fs, fontweight="bold", color=tc, ha="center", va="center")

    def diamond(x, y, w, h, title, sub=""):
        pts = [(x + w/2, y + h), (x + w, y + h/2), (x + w/2, y), (x, y + h/2)]
        ax.add_patch(Polygon(pts, closed=True, fc="#FBE9DF", ec=EMBER, lw=1.3, zorder=2))
        ax.text(x + w/2, y + h*0.58, title, fontsize=9.6, fontweight="bold", color=DARK, ha="center", va="center")
        if sub:
            ax.text(x + w/2, y + h*0.36, sub, fontsize=6.9, color=SLATE, ha="center", va="center")

    def poly_arrow(points, color=MOSS, lw=1.4, ls="-", label=None, lx=None, ly=None, lcolor=None):
        for i in range(len(points) - 2):
            ax.plot([points[i][0], points[i+1][0]], [points[i][1], points[i+1][1]], color=color, lw=lw, ls=ls, zorder=3)
        arrow(ax, points[-2][0], points[-2][1], points[-1][0], points[-1][1], color=color, lw=lw, ls=ls)
        if label:
            ax.text(lx, ly, label, fontsize=7.8, color=lcolor or color, fontweight="bold", va="center")

    # ---------- left column ----------
    box(0.70, 7.55, 2.50, 0.62, "Start", "使用者提出需求", fc="#EDF3EE", fs=14)
    box(0.70, 6.35, 2.50, 0.72, "Parse & Understand", "意圖、實體、限制、風險旗標", fs=12.6, sfs=7.4)
    diamond(0.52, 5.05, 2.86, 1.02, "Slot 足夠？", "缺體能／日期／經驗")
    box(0.70, 3.65, 2.50, 0.70, "Plan & Decompose", "子任務、工具、資料需求", fs=12.6, sfs=7.4)
    box(0.70, 2.35, 2.50, 0.70, "Parallel Acquire", "天氣／許可／山屋／路線／KB", fs=12.6, sfs=7.4)

    # clarify side box
    box(3.55, 5.12, 1.72, 0.78, "Clarify", "一次只問必要問題", fc=SAND, fs=12.0, sfs=7.2)

    # left vertical flow
    arrow(ax, 1.95, 7.53, 1.95, 7.09)
    arrow(ax, 1.95, 6.33, 1.95, 6.09)
    arrow(ax, 1.95, 5.03, 1.95, 4.37)
    ax.text(2.04, 4.70, "Yes", fontsize=8, color=PINE, fontweight="bold")
    arrow(ax, 1.95, 3.63, 1.95, 3.07)

    # No -> Clarify
    arrow(ax, 3.40, 5.56, 3.53, 5.56, color=EMBER, lw=1.4)
    ax.text(3.40, 5.70, "No", fontsize=8, color=EMBER, fontweight="bold")
    # Clarify -> back to Parse (re-ask)
    poly_arrow([(4.41, 5.92), (4.41, 6.70), (3.22, 6.70)], color=MOSS, lw=1.1, ls="--",
               label="re-ask", lx=4.52, ly=6.45, lcolor=MOSS)

    # ---------- middle column ----------
    box(5.70, 7.38, 2.80, 0.72, "Validate & Normalize", "時效、單位、衝突、缺漏", fs=13.0, sfs=7.6)
    box(5.70, 6.18, 2.80, 0.72, "Analytics", "步程 P50/P90、風險、天氣窗", fs=13.0, sfs=7.6)
    box(5.70, 4.98, 2.80, 0.72, "Generate Candidates", "安全／平衡／進取 3 方案", fs=13.0, sfs=7.6)
    diamond(5.56, 3.55, 3.08, 1.08, "Hard constraints?", "許可、封閉、日照、床位")
    diamond(5.56, 2.05, 3.08, 1.02, "Critical red flag?", "颱風、AMS 症狀、落雷")
    box(5.70, 0.88, 2.80, 0.70, "Verify Evidence", "無來源→重寫；衝突→揭露", fc="#FBE9DF", ec=EMBER, fs=12.4, sfs=7.4)

    # middle vertical flow
    arrow(ax, 7.10, 7.36, 7.10, 6.92)
    arrow(ax, 7.10, 6.16, 7.10, 5.72)
    arrow(ax, 7.10, 4.96, 7.10, 4.65)
    arrow(ax, 7.10, 3.53, 7.10, 3.09)
    ax.text(7.19, 3.28, "Yes", fontsize=8, color=PINE, fontweight="bold")
    arrow(ax, 7.10, 2.03, 7.10, 1.60)
    ax.text(7.19, 1.79, "No", fontsize=8, color=PINE, fontweight="bold")

    # Hard constraints No -> Relax -> back to Generate
    box(9.00, 3.64, 2.00, 0.74, "Relax / Alternative", "改日期、改路線、改天數", fc=SAND, fs=10.8, sfs=6.9)
    arrow(ax, 8.66, 4.09, 8.98, 4.09, color=EMBER, lw=1.4)
    ax.text(8.68, 4.23, "No", fontsize=8, color=EMBER, fontweight="bold")
    poly_arrow([(10.00, 4.40), (10.00, 5.34), (8.52, 5.34)], color=MOSS, lw=1.1, ls="--",
               label="re-plan", lx=10.12, ly=4.95, lcolor=MOSS)

    # Critical Yes -> No-Go
    box(9.00, 2.18, 2.00, 0.74, "No-Go / Escalate", "停止計畫、聯絡留守人", fc="#F6DEDB", ec=RED, fs=11.0, sfs=6.9)
    arrow(ax, 8.66, 2.56, 8.98, 2.56, color=RED, lw=1.4)
    ax.text(8.68, 2.70, "Yes", fontsize=8, color=RED, fontweight="bold")

    # Verify -> Output
    box(9.00, 0.88, 2.20, 0.70, "Output", "Chat＋Dashboard＋PDF＋離線卡", fc="#EDF3EE", fs=12.0, sfs=6.8)
    arrow(ax, 8.52, 1.23, 8.98, 1.23, color=PINE, lw=1.4)

    # ---------- human decision + feedback ----------
    box(11.55, 2.18, 2.20, 0.74, "Human Decision", "使用者／領隊仍是最終決策者", fc=WHITE, ec=MOSS, fs=10.6, sfs=6.6)
    arrow(ax, 11.02, 2.56, 11.52, 2.56, color=MOSS, lw=1.0, ls="--")

    box(11.55, 0.88, 2.20, 0.70, "Feedback", "行後紀錄、校正、通知", fc="#EDF3EE", fs=11.4, sfs=6.8)
    arrow(ax, 11.22, 1.23, 11.52, 1.23, color=PINE, lw=1.3)

    # feedback loop along bottom and left margin
    poly_arrow([(12.65, 0.86), (12.65, 0.55), (0.35, 0.55), (0.35, 6.70), (0.68, 6.70)],
               color=MOSS, lw=1.1, ls="--", label="feedback / recalibration", lx=6.45, ly=0.36, lcolor=MOSS)

    # data bundle from Acquire to Validate (right of left column, left of middle)
    poly_arrow([(3.22, 2.70), (5.44, 2.70), (5.44, 7.74), (5.68, 7.74)], color=MOSS, lw=1.5)
    ax.text(5.50, 6.95, "data", fontsize=7.2, color=MOSS, rotation=90, va="center")

    # legend / footer
    ax.text(0.70, 0.22, "橘色菱形為決策節點；紅旗（typhoon／closure／AMS 症狀／lightning）會覆寫加權風險分數，優先輸出 No-Go 或替代方案。",
            fontsize=7.4, color=SLATE, va="center")
    ax.text(0.70, 0.07, "資料來源：CWA、國家公園署、林業署、警政署、OSM、上河步程、研究文獻與使用者輸入。",
            fontsize=6.9, color=SLATE, va="center", alpha=0.85)

    save(fig, "fig_flowchart.png")


'''

p.write_text(s[:start] + new + s[end:], encoding="utf-8")
print("flowchart rewritten")
