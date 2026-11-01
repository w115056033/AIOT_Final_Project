# -*- coding: utf-8 -*-
"""Generate figures for the TrailGuard TW proposal package."""
from __future__ import annotations

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Circle, Rectangle
from matplotlib.lines import Line2D

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(BASE, "assets")
os.makedirs(ASSETS, exist_ok=True)

# ---------- palette ----------
DARK = "#0B241D"
FOREST = "#12352B"
PINE = "#1F5C4A"
MOSS = "#7FA88C"
SAND = "#F4EFE6"
CREAM = "#FBF8F1"
EMBER = "#D97745"
SLATE = "#33413C"
RED = "#B23A32"
SKY = "#6C9BB5"
GOLD = "#C9A227"
WHITE = "#FFFFFF"

plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["pdf.fonttype"] = 42


def save(fig, name):
    path = os.path.join(ASSETS, name)
    fig.savefig(path, dpi=220, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print("saved", path)


def rounded(ax, x, y, w, h, fc=WHITE, ec=PINE, lw=1.4, rad=0.018, alpha=1.0, z=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.004,rounding_size={rad}",
                       fc=fc, ec=ec, lw=lw, alpha=alpha, zorder=z)
    ax.add_patch(p)
    return p


def arrow(ax, x1, y1, x2, y2, color=SLATE, lw=1.8, style="-|>", rad=0.0, z=3, ls="-"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=14,
                        color=color, lw=lw, connectionstyle=f"arc3,rad={rad}", zorder=z, linestyle=ls)
    ax.add_patch(a)


# =========================================================
# 1. Cover art
# =========================================================
def cover():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=220)
    fig.patch.set_facecolor(DARK)
    ax.set_facecolor(DARK)
    ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis("off")

    # subtle contour / grid
    for i in range(1, 14):
        xs = np.linspace(0, 16, 400)
        ys = 1.0 + i * 0.55 + 0.10 * np.sin(xs * 0.9 + i * 0.7)
        ax.plot(xs, ys, color=MOSS, lw=0.5, alpha=0.10, zorder=1)

    # sun
    ax.add_patch(Circle((12.9, 7.1), 0.55, fc=EMBER, ec="none", alpha=0.92, zorder=2))
    ax.add_patch(Circle((12.9, 7.1), 0.95, fc=EMBER, ec="none", alpha=0.08, zorder=1))

    x = np.linspace(0, 16, 900)
    layers = [
        (2.30, 0.55, 0.9, "#0E2B23", 0.95),
        (1.75, 0.72, 1.4, "#14382E", 0.95),
        (1.15, 0.95, 2.0, "#1B4738", 0.95),
        (0.55, 1.10, 2.6, "#245845", 0.95),
    ]
    for base, amp, freq, color, alpha in layers:
        y = base + amp * (0.55 * np.sin(x * freq) + 0.30 * np.sin(x * freq * 2.3 + 1.2)
                          + 0.15 * np.sin(x * freq * 5.1 + 0.4))
        y = np.maximum(y, base - 0.15)
        ax.fill_between(x, 0, y, color=color, alpha=alpha, zorder=3)
        ax.plot(x, y, color=MOSS, lw=0.8, alpha=0.25, zorder=4)

    # ridge highlight line
    y = 1.15 + 0.95 * (0.55 * np.sin(x * 2.0) + 0.30 * np.sin(x * 4.6 + 1.2) + 0.15 * np.sin(x * 10.2 + 0.4))
    ax.plot(x, y, color=EMBER, lw=1.4, alpha=0.55, zorder=5)

    # small markers / waypoints
    for xx in [3.2, 6.1, 8.7, 11.4, 13.8]:
        yy = 0.82 + 0.10 * np.sin(xx)
        ax.plot(xx, yy, marker="o", ms=3.5, color=SAND, alpha=0.55, zorder=6)

    fig.subplots_adjust(0, 0, 1, 1)
    save(fig, "fig_cover.png")


# =========================================================
# 2. Architecture
# =========================================================
def architecture():
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
        rounded(ax, ix, 6.26, 2.02, 0.55, fc=SAND, ec=MOSS, lw=0.9)
        ax.text(ix + 1.01, 6.535, label, fontsize=8.4, color=DARK, ha="center", va="center", linespacing=1.18)
        ix += 2.18

    arrow(ax, 4.15, 7.73, 4.15, 6.83, color=MOSS, lw=1.4)

    # ---- Band 2: agent ----
    band_header(6.05, "③", "領域資料分析代理人（核心大腦）", "Understand → Plan → Acquire → Analyze → Generate → Verify → Interact")
    rounded(ax, 2.10, 4.35, 8.85, 1.28, fc="#E8F0EA", ec=PINE, lw=1.4)
    steps = [
        ("Understand", "意圖／限制"), ("Plan", "拆解子任務"), ("Acquire", "呼叫工具"),
        ("Analyze", "計算與模型"), ("Generate", "3 個候選"), ("Verify", "證據核對"),
        ("Interact", "呈現與追問"),
    ]
    sx = 2.28
    for i, (t, d) in enumerate(steps):
        fc = "#FBE9DF" if t == "Verify" else WHITE
        ec = EMBER if t == "Verify" else PINE
        rounded(ax, sx, 4.70, 1.10, 0.60, fc=fc, ec=ec, lw=1.0, rad=0.012)
        ax.text(sx + 0.55, 5.09, t, fontsize=7.8, fontweight="bold", color=DARK, ha="center", va="center")
        ax.text(sx + 0.55, 4.88, d, fontsize=6.7, color=SLATE, ha="center", va="center")
        if i < len(steps) - 1:
            arrow(ax, sx + 1.12, 4.99, sx + 1.25, 4.99, color=MOSS, lw=1.0)
        sx += 1.26
    ax.text(2.28, 4.46, "State machine＋typed tools＋structured outputs＋reflection loop（Verify 可退回 Plan／Generate）",
            fontsize=7.4, color=SLATE, va="center")

    caps = ["TALK", "KNOW", "SENSE", "ANALYZE", "THINK", "SHOW"]
    cx = 2.28
    for c in caps:
        rounded(ax, cx, 3.80, 1.32, 0.28, fc=PINE, ec=PINE, lw=0.8, rad=0.010)
        ax.text(cx + 0.66, 3.94, c, fontsize=7.1, color=WHITE, ha="center", va="center", fontweight="bold")
        cx += 1.42
    ax.text(10.15, 3.94, "④ 六大能力", fontsize=7.6, color=PINE, ha="right", va="center", fontweight="bold")
    arrow(ax, 6.60, 6.24, 6.60, 5.65, color=MOSS, lw=1.5)

    # ---- Band 3: data & tools ----
    band_header(3.50, "⑤", "資料來源與工具層", "知道什麼時候該用哪一種資料；不把 LLM 當資料庫")
    data = [
        ("IoT／穿戴", "GPS、氣壓、心率、SpO2\n（手機＋ESP32 選配）", SKY),
        ("內部資料", "使用者檔案、行程紀錄\n評測標註、事故資料", PINE),
        ("外部 API", "CWA 天氣、警特報\n公路／園區狀態", EMBER),
        ("知識庫", "官方規則、步程、山屋\n高山症、裝備、RAG", MOSS),
        ("分析工具", "Python、GeoPandas\nOR-Tools、scikit-learn", GOLD),
    ]
    dx = 2.15
    for t, d, col in data:
        rounded(ax, dx, 2.26, 1.62, 0.72, fc=WHITE, ec=col, lw=1.2)
        ax.add_patch(Rectangle((dx, 2.26), 0.07, 0.72, fc=col, ec="none"))
        ax.text(dx + 0.16, 2.84, t, fontsize=8.1, fontweight="bold", color=DARK, va="center")
        ax.text(dx + 0.16, 2.57, d, fontsize=6.9, color=SLATE, va="center", linespacing=1.2)
        dx += 1.76
    arrow(ax, 6.60, 3.78, 6.60, 3.01, color=MOSS, lw=1.5)

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


# =========================================================
# 3. Flowchart
# =========================================================
def flowchart():
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


# =========================================================
# 4. Risk matrix
# =========================================================
def risk_matrix():
    fig, ax = plt.subplots(figsize=(10.5, 7.6), dpi=220)
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)

    # color grid
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "risk", ["#4F7F5F", "#9CBF8E", "#E8D48B", "#E3A15E", "#C85A4A"])
    for i in range(5):
        for j in range(5):
            score = (i + 1) * (j + 1)
            color = cmap(min(1.0, (i + j) / 8.0))
            ax.add_patch(Rectangle((i + 1, j + 1), 1, 1, fc=color, ec=CREAM, lw=1.5, alpha=0.92))
            ax.text(i + 1.5, j + 1.5, str(score), fontsize=8, color=WHITE if score > 15 else SLATE,
                    ha="center", va="center", alpha=0.65)

    labels = [
        (4.5, 4.45, "颱風／豪雨", 0.02), (2.5, 4.55, "高山症", 0.0), (3.5, 3.55, "迷途", 0.0),
        (3.4, 2.55, "午後雷雨", 0.0), (2.4, 2.45, "抽籤／許可", 0.0), (4.4, 2.55, "落石／坍方", 0.0),
        (3.6, 1.55, "低溫／失溫", 0.0), (2.5, 1.45, "通訊死角", 0.0), (4.5, 1.55, "疲勞", 0.0),
        (1.5, 3.55, "水源不足", 0.0),
    ]
    for x, y, t, rot in labels:
        ax.text(x, y, t, fontsize=8.2, color=DARK, ha="center", va="center", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.22", fc=WHITE, ec="none", alpha=0.82))

    ax.set_xlim(1, 6); ax.set_ylim(1, 6)
    ax.set_xticks([1.5, 2.5, 3.5, 4.5, 5.5])
    ax.set_xticklabels(["很低", "低", "中", "高", "很高"], fontsize=9.5)
    ax.set_yticks([1.5, 2.5, 3.5, 4.5, 5.5])
    ax.set_yticklabels(["輕微", "較低", "中等", "嚴重", "致命"], fontsize=9.5)
    ax.set_xlabel("發生機率（Likelihood）", fontsize=11, color=SLATE, labelpad=8)
    ax.set_ylabel("影響程度（Impact）", fontsize=11, color=SLATE, labelpad=8)
    ax.set_title("風險矩陣（示意）：先看紅旗，再看加權分數", fontsize=16, fontweight="bold", color=DARK, pad=16)
    fig.text(0.12, 0.025, "注意：此圖為方法示意，非實際路線觀測值；實際分數由路線、天氣、生理與作業四類因子計算。",
             fontsize=7.8, color=SLATE)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)
    ax.set_aspect("equal")
    fig.subplots_adjust(left=0.12, right=0.97, top=0.90, bottom=0.16)
    save(fig, "fig_risk_matrix.png")


# =========================================================
# 5. Gantt
# =========================================================
def gantt():
    fig, ax = plt.subplots(figsize=(13.5, 6.4), dpi=220)
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)

    tasks = [
        ("文獻與資料盤點", 1, 2, PINE),
        ("知識庫與 Temporal KG", 3, 4, MOSS),
        ("分析引擎（步程／風險）", 4, 6, EMBER),
        ("Agent Orchestrator＋Tools", 5, 8, SKY),
        ("Web UI／PDF／離線卡", 7, 10, GOLD),
        ("核心實驗與消融", 9, 12, PINE),
        ("壓力測試與紅隊", 11, 13, RED),
        ("使用者測試", 13, 14, MOSS),
        ("文件、影片、Handover", 15, 16, SLATE),
    ]
    for i, (name, start, end, color) in enumerate(tasks):
        y = len(tasks) - i - 1
        ax.barh(y, end - start + 1, left=start - 0.5, height=0.52, color=color, alpha=0.88, edgecolor="none")
        ax.text(start - 0.65, y, name, fontsize=9.6, color=DARK, ha="right", va="center", fontweight="bold")
        # milestone diamonds
        ax.plot(end + 0.5, y, marker="D", ms=5, color=color, markeredgecolor=WHITE, markeredgewidth=1.0, zorder=4)

    # phase bands
    for x0, x1, label, alpha in [(0.5, 4.5, "Foundation", 0.06), (4.5, 10.5, "Build", 0.06), (10.5, 14.5, "Validate", 0.06), (14.5, 16.5, "Handover", 0.06)]:
        ax.axvspan(x0, x1, color=PINE, alpha=alpha, lw=0)
        ax.text((x0 + x1)/2, len(tasks) - 0.28, label, fontsize=8.6, color=PINE, ha="center", va="center", fontweight="bold")

    ax.set_xlim(0.5, 17.0)
    ax.set_ylim(-0.7, len(tasks) - 0.05)
    ax.set_xticks(range(1, 17))
    ax.set_xticklabels([f"W{i}" for i in range(1, 17)], fontsize=8.8)
    ax.set_yticks([])
    ax.grid(axis="x", color=MOSS, alpha=0.22, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_title("16 週實作與驗證時程（Proposal 規劃）", fontsize=16, fontweight="bold", color=DARK, pad=14)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(MOSS)
    ax.tick_params(axis="x", colors=SLATE, length=0)
    ax.text(0.6, -0.62, "里程碑：W4 知識庫 v1｜W8 Agent MVP｜W12 核心實驗｜W14 使用者測試｜W16 Final Handover",
            fontsize=7.8, color=SLATE)
    fig.tight_layout()
    save(fig, "fig_gantt.png")


if __name__ == "__main__":
    cover()
    architecture()
    flowchart()
    risk_matrix()
    gantt()
    print("All figures generated.")
