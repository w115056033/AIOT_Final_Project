# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path(r"assets\build_figures.py")
s = p.read_text(encoding="utf-8")

# interaction chips + arrow
s = s.replace('rounded(ax, ix, 6.40, 2.02, 0.55, fc=SAND, ec=MOSS, lw=0.9)\n        ax.text(ix + 1.01, 6.675,',
              'rounded(ax, ix, 6.26, 2.02, 0.55, fc=SAND, ec=MOSS, lw=0.9)\n        ax.text(ix + 1.01, 6.535,')
s = s.replace('arrow(ax, 4.15, 7.73, 4.15, 6.97, color=MOSS, lw=1.4)',
              'arrow(ax, 4.15, 7.73, 4.15, 6.83, color=MOSS, lw=1.4)')

# agent header and box
s = s.replace('band_header(5.95, "③"', 'band_header(6.05, "③"')
s = s.replace('rounded(ax, 2.10, 4.30, 8.85, 1.30, fc="#E8F0EA", ec=PINE, lw=1.4)',
              'rounded(ax, 2.10, 4.35, 8.85, 1.28, fc="#E8F0EA", ec=PINE, lw=1.4)')
s = s.replace('rounded(ax, sx, 4.66, 1.10, 0.62, fc=fc, ec=ec, lw=1.0, rad=0.012)',
              'rounded(ax, sx, 4.70, 1.10, 0.60, fc=fc, ec=ec, lw=1.0, rad=0.012)')
s = s.replace('ax.text(sx + 0.55, 5.06, t', 'ax.text(sx + 0.55, 5.09, t')
s = s.replace('ax.text(sx + 0.55, 4.85, d', 'ax.text(sx + 0.55, 4.88, d')
s = s.replace('arrow(ax, sx + 1.12, 4.97, sx + 1.25, 4.97', 'arrow(ax, sx + 1.12, 4.99, sx + 1.25, 4.99')
s = s.replace('ax.text(2.28, 4.43, "State machine', 'ax.text(2.28, 4.46, "State machine')
s = s.replace('arrow(ax, 6.60, 6.38, 6.60, 5.62, color=MOSS, lw=1.5)',
              'arrow(ax, 6.60, 6.24, 6.60, 5.65, color=MOSS, lw=1.5)')

# data header + chips
s = s.replace('band_header(3.42, "⑤"', 'band_header(3.50, "⑤"')
s = s.replace('rounded(ax, dx, 2.40, 1.62, 0.72, fc=WHITE, ec=col, lw=1.2)',
              'rounded(ax, dx, 2.26, 1.62, 0.72, fc=WHITE, ec=col, lw=1.2)')
s = s.replace('ax.add_patch(Rectangle((dx, 2.40), 0.07, 0.72', 'ax.add_patch(Rectangle((dx, 2.26), 0.07, 0.72')
s = s.replace('ax.text(dx + 0.16, 2.98, t', 'ax.text(dx + 0.16, 2.84, t')
s = s.replace('ax.text(dx + 0.16, 2.71, d', 'ax.text(dx + 0.16, 2.57, d')
s = s.replace('arrow(ax, 6.60, 3.78, 6.60, 3.15, color=MOSS, lw=1.5)',
              'arrow(ax, 6.60, 3.78, 6.60, 3.01, color=MOSS, lw=1.5)')

p.write_text(s, encoding="utf-8")
print("patched")
