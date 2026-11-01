# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path(r"assets\build_figures.py")
s = p.read_text(encoding="utf-8")

# Risk matrix: use additive severity for color and move note out of axes
s = s.replace('color = cmap(min(1.0, (score - 1) / 24.0))', 'color = cmap(min(1.0, (i + j) / 8.0))')
s = s.replace('ax.text(1.02, 0.82, "注意：此圖為方法示意，非實際路線觀測值；實際分數由路線、天氣、生理與作業四類因子計算。",\n            fontsize=7.8, color=SLATE)',
              'fig.text(0.12, 0.025, "注意：此圖為方法示意，非實際路線觀測值；實際分數由路線、天氣、生理與作業四類因子計算。",\n             fontsize=7.8, color=SLATE)')
s = s.replace('fig.tight_layout()\n    save(fig, "fig_risk_matrix.png")',
              'fig.subplots_adjust(left=0.12, right=0.97, top=0.90, bottom=0.16)\n    save(fig, "fig_risk_matrix.png")')

# Gantt: extend xlim, move milestone note
s = s.replace('ax.set_xlim(0.5, 16.5)', 'ax.set_xlim(0.5, 17.0)')
s = s.replace('ax.text(0.6, -0.55, "里程碑：W4 知識庫 v1｜W8 Agent MVP｜W12 核心實驗｜W14 使用者測試｜W16 Final Handover",\n            fontsize=7.8, color=SLATE)',
              'ax.text(0.6, -0.62, "里程碑：W4 知識庫 v1｜W8 Agent MVP｜W12 核心實驗｜W14 使用者測試｜W16 Final Handover",\n            fontsize=7.8, color=SLATE)')
p.write_text(s, encoding="utf-8")
print("patched risk/gantt")
