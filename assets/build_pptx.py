# -*- coding: utf-8 -*-
"""Build Proposal_PPT.pptx (16:9, native shapes, Traditional Chinese).

Run: python assets/build_pptx.py
"""
from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt, Emu
from lxml import etree
from PIL import Image

BASE = Path(r"C:\Users\User\Desktop\文件\週3_物聯網應用與資料分析_陳煥\week8_2026_10_28\報告")
ASSETS = BASE / "assets"
OUT = BASE / "Proposal_PPT.pptx"

# palette
FOREST = RGBColor(0x0B, 0x24, 0x1D)
PINE = RGBColor(0x1F, 0x5C, 0x4A)
MOSS = RGBColor(0x7F, 0xA8, 0x8C)
SAND = RGBColor(0xF4, 0xEF, 0xE6)
CREAM = RGBColor(0xFB, 0xF8, 0xF1)
EMBER = RGBColor(0xD9, 0x77, 0x45)
SLATE = RGBColor(0x33, 0x41, 0x3C)
RED = RGBColor(0xB2, 0x3A, 0x32)
SKY = RGBColor(0x6C, 0x9B, 0xB5)
GOLD = RGBColor(0xC9, 0xA2, 0x27)
INK = RGBColor(0x1E, 0x2A, 0x26)
MUTED = RGBColor(0x68, 0x73, 0x6E)
BORDER = RGBColor(0xD8, 0xD2, 0xC4)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PALE = RGBColor(0xF0, 0xEB, 0xDF)
DARKCARD = RGBColor(0x11, 0x33, 0x2A)

CN = "Microsoft JhengHei"
EN = "Aptos"
MONO = "Consolas"

W = 13.333
H = 7.5
MX = 0.72
CW = W - 2 * MX

prs = Presentation()
prs.slide_width = Inches(W)
prs.slide_height = Inches(H)
BLANK = prs.slide_layouts[6]


# ----------------------------------------------------------------------------
# primitives
# ----------------------------------------------------------------------------
def _set_font(run, size=None, bold=None, color=None, font=CN, italic=None):
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    if font:
        run.font.name = font
        rPr = run._r.get_or_add_rPr()
        for tag in ("a:ea", "a:cs"):
            el = rPr.find(qn(tag))
            if el is None:
                el = etree.SubElement(rPr, qn(tag))
            el.set("typeface", font)


def _fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color


def _no_line(shape):
    shape.line.fill.background()


def rect(slide, x, y, w, h, fill=None, line=None, lw=0.75, radius=None, dash=None):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    style = s._element.find(qn("p:style"))
    if style is not None:
        s._element.remove(style)
    if fill is None:
        s.fill.background()
    else:
        _fill(s, fill)
    if line is None:
        _no_line(s)
    else:
        s.line.color.rgb = line
        s.line.width = Pt(lw)
        if dash:
            s.line.dash_style = dash
    if radius:
        try:
            s.adjustments[0] = radius
        except Exception:
            pass
    s.text_frame.word_wrap = True
    s.text_frame.margin_left = 0
    s.text_frame.margin_right = 0
    s.text_frame.margin_top = 0
    s.text_frame.margin_bottom = 0
    return s


def fill_alpha(shape, pct):
    """Set solid-fill transparency (pct = opacity 0-100)."""
    sf = shape._element.spPr.find(qn("a:solidFill"))
    if sf is None:
        return
    clr = sf.find(qn("a:srgbClr"))
    if clr is None:
        return
    a = etree.SubElement(clr, qn("a:alpha"))
    a.set("val", str(int(pct * 1000)))


def line(slide, x1, y1, x2, y2, color=BORDER, width=1.0, dash=None):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    if dash:
        c.line.dash_style = dash
    return c


def text(slide, x, y, w, h, runs, size=12, color=INK, bold=False, font=CN,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line_spacing=1.15,
         space_after=0, margins=(0, 0, 0, 0), autofit=False):
    """runs: str or list of (text, dict) or list of paragraphs (list of runs)."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left, tf.margin_right, tf.margin_top, tf.margin_bottom = [Inches(m) for m in margins]
    if autofit:
        tf.fit_text()
    if isinstance(runs, str):
        paras = [[(runs, {})]]
    elif runs and isinstance(runs[0], tuple):
        paras = [runs]
    else:
        paras = runs
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        p.space_after = Pt(space_after)
        p.space_before = Pt(0)
        if isinstance(para, str):
            para = [(para, {})]
        for t, opt in para:
            r = p.add_run()
            r.text = t
            _set_font(r, opt.get("size", size), opt.get("bold", bold),
                      opt.get("color", color), opt.get("font", font), opt.get("italic"))
    return tb


def notes(slide, txt):
    slide.notes_slide.notes_text_frame.text = txt


def new_slide(bg=CREAM):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = bg
    return s


def footer(slide, num, dark=False):
    c = MOSS if dark else MUTED
    text(slide, MX, 7.12, 8.2, 0.24, "TrailGuard TW｜期末專題提案", 8, c, font=EN)
    text(slide, W - MX - 1.2, 7.12, 1.2, 0.24, f"{num:02d}", 8.5, c, bold=True,
         align=PP_ALIGN.RIGHT, font=EN)


def header(slide, kicker, title, source=None, title_size=27):
    text(slide, MX, 0.42, 9.0, 0.28, kicker, 10.5, EMBER, bold=True, font=EN)
    text(slide, MX, 0.73, CW, 0.62, title, title_size, FOREST, bold=True, line_spacing=1.02)
    line(slide, MX, 1.53, W - MX, 1.53, MOSS, 0.9)
    if source:
        text(slide, MX, 6.82, CW, 0.24, source, 8, MUTED, font=CN)


def section(num, en, title, desc, page):
    s = new_slide(FOREST)
    # faint frame lines
    line(s, MX, 0.55, W - MX, 0.55, RGBColor(0x2A, 0x4A, 0x3F), 0.75)
    line(s, MX, 6.95, W - MX, 6.95, RGBColor(0x2A, 0x4A, 0x3F), 0.75)
    text(s, MX, 1.05, 3.0, 0.35, en, 10, EMBER, bold=True, font=EN)
    text(s, MX, 1.55, 4.6, 1.5, num, 96, RGBColor(0x24, 0x45, 0x39), bold=True, font=EN)
    text(s, MX, 3.25, 9.6, 1.0, title, 40, CREAM, bold=True, line_spacing=1.05)
    text(s, MX, 4.55, 9.2, 0.9, desc, 14, MOSS, line_spacing=1.35)
    line(s, MX, 5.75, MX + 1.25, 5.75, EMBER, 4)
    text(s, W - MX - 1.2, 6.55, 1.2, 0.3, f"{page:02d}", 9, MOSS, align=PP_ALIGN.RIGHT, font=EN)
    return s


def pic_fit(slide, path, x, y, w, h, border=False):
    iw, ih = Image.open(path).size
    scale = min(w / iw, h / ih)
    nw, nh = iw * scale, ih * scale
    px = x + (w - nw) / 2
    py = y + (h - nh) / 2
    p = slide.shapes.add_picture(str(path), Inches(px), Inches(py), Inches(nw), Inches(nh))
    if border:
        p.line.color.rgb = BORDER
        p.line.width = Pt(0.75)
    return p, (px, py, nw, nh)


def pill(slide, x, y, w, h, label, fill=SAND, color=PINE, size=9, bold=True):
    shp = rect(slide, x, y, w, h, fill=fill, radius=0.5)
    text(slide, x, y + 0.02, w, h - 0.04, label, size, color, bold=bold,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return shp


def table(slide, data, x, y, w, h, col_ratios, header_fill=FOREST, header_color=WHITE,
          size=9, head_size=9, row_fill=(WHITE, PALE), first_col_bold=False):
    rows, cols = len(data), len(data[0])
    shp = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = shp.table
    # kill default banding style
    tblPr = tbl._tbl.tblPr
    tblPr.set("bandRow", "0")
    tblPr.set("firstRow", "1")
    total = sum(col_ratios)
    for i, ratio in enumerate(col_ratios):
        tbl.columns[i].width = Emu(int(Inches(w) * ratio / total))
    for ri, row in enumerate(data):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.07)
            cell.margin_top = Inches(0.035)
            cell.margin_bottom = Inches(0.035)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = header_fill if ri == 0 else row_fill[(ri + 1) % 2]
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            p.line_spacing = 1.0
            r = p.add_run()
            r.text = str(val)
            _set_font(r, head_size if ri == 0 else size, True if ri == 0 else (first_col_bold and ci == 0),
                      header_color if ri == 0 else INK)
    return tbl


def bullet_list(slide, x, y, w, items, size=12.5, color=INK, gap=0.42, bullet_color=EMBER,
                bold_lead=True, line_spacing=1.2):
    yy = y
    for item in items:
        rect(slide, x, yy + 0.075, 0.075, 0.075, fill=bullet_color)
        if isinstance(item, tuple):
            lead, rest = item
            text(slide, x + 0.22, yy - 0.02, w - 0.22, gap,
                 [[(lead + "　", {"bold": True, "color": FOREST}), (rest, {"color": color})]],
                 size, color, line_spacing=line_spacing)
        else:
            text(slide, x + 0.22, yy - 0.02, w - 0.22, gap, item, size, color, line_spacing=line_spacing)
        yy += gap
    return yy


# ----------------------------------------------------------------------------
# 01 cover
# ----------------------------------------------------------------------------
s = new_slide(FOREST)
pic_fit(s, ASSETS / "fig_cover.png", 0, 0, W, H)
# the illustration's left side is already dark; add a readable caption band
band = rect(s, 0, 5.42, W, 2.08, fill=FOREST)
fill_alpha(band, 92)
line(s, 0, 5.42, W, 5.42, RGBColor(0x2F, 0x51, 0x44), 0.8)

text(s, 0.85, 0.72, 6.0, 0.3, "期末專題提案｜DOMAIN DATA AGENT", 10.5, EMBER, bold=True, font=EN)
text(s, 0.85, 1.35, 7.6, 1.15, "山徑守護者", 54, CREAM, bold=True)
text(s, 0.85, 2.32, 7.0, 0.55, [[("TrailGuard ", {"size": 26, "color": MOSS, "bold": True}),
                                   ("TW", {"size": 26, "color": MOSS, "bold": True})]], 26)
line(s, 0.88, 3.02, 6.35, 3.02, EMBER, 3)
text(s, 0.85, 3.22, 7.5, 0.95,
     "以證據為基礎的臺灣高山行程規劃\n與風險決策支援代理人", 21, CREAM, bold=True, line_spacing=1.28)
text(s, 0.85, 4.55, 7.4, 0.7,
     "An Evidence-Grounded Domain Data Agent for High-Mountain\nTrip Planning and Risk Decision Support in Taiwan",
     9.5, MOSS, font=EN, line_spacing=1.3)
line(s, 0.88, 5.62, 5.9, 5.62, RGBColor(0x3A, 0x5A, 0x4E), 0.9)
text(s, 0.85, 5.82, 7.6, 0.3, "物聯網應用與資料分析　｜　陳煥 教授　｜　2026-10-31", 10.5, CREAM)
text(s, 0.85, 6.18, 7.6, 0.3, "組員：陳俊安、廖家暉、温偉成、郭冠良　｜　v0.1 Proposal", 10.5, RGBColor(0xB9, 0xCF, 0xC3))
text(s, 0.85, 6.78, 7.7, 0.3, "提案版本：所有成效數字均為設計目標或驗收門檻，尚未進行正式實驗。", 8.5, RGBColor(0xA9, 0xBF, 0xB3))
notes(s, "開場：這份提案要解決的不是『再做一個登山 App』，而是高山決策裡最容易被忽略的一件事——系統什麼時候應該說不。"
         "我們會先給數字，再給研究缺口，最後說明 TrailGuard TW 的架構、流程與驗證方式。"
         "先說清楚：目前是提案階段，所有成效數字都是目標，不是實驗結果。")

# ----------------------------------------------------------------------------
# 02 agenda
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "AGENDA", "今天要走完的六個段落")
items = [
    ("01", "問題與動機", "山難數字背後，缺的是哪一個決策環節？"),
    ("02", "文獻與缺口", "AI 規劃與登山領域，各自走到哪裡？"),
    ("03", "深度研究", "專家怎麼想？爭論什麼？如何判斷理解？"),
    ("04", "提出方案", "TrailGuard TW 的架構、模組、分析與流程"),
    ("05", "驗證與時程", "120 個案例、False-Safe Rate、16 週"),
    ("06", "結論", "把不確定性與安全責任設計進架構"),
]
for i, (num, t, d) in enumerate(items):
    col, row = i % 2, i // 2
    x = MX + col * 6.05
    y = 1.9 + row * 1.62
    text(s, x, y, 0.72, 0.4, num, 13, EMBER, bold=True, font=EN)
    text(s, x + 0.62, y - 0.03, 5.0, 0.35, t, 16, FOREST, bold=True)
    text(s, x + 0.62, y + 0.36, 4.95, 0.7, d, 10.5, SLATE, line_spacing=1.25)
    if row < 2:
        line(s, x + 0.62, y + 1.28, x + 5.45, y + 1.28, BORDER, 0.6)
footer(s, 2)
notes(s, "整份簡報沿著六個段落走。先建立問題的正當性，再用文獻說明缺口，接著用五個思維、三個爭論、十個問題把領域知識講深，"
         "最後才進到系統設計與驗證。這樣安排是刻意的：先讓大家同意『問題值得做』，再談『怎麼做』。")

# ----------------------------------------------------------------------------
# 03 section 01
# ----------------------------------------------------------------------------
s = section("01", "PROBLEM & MOTIVATION", "山上的風險，多半不是意外", "而是行前決策裡，一個沒有被檢查的假設。", 3)
notes(s, "第一個段落先把問題站穩。臺灣的山很近、很容易親近，但正因為容易，風險常被低估。")

# ----------------------------------------------------------------------------
# 04 stats
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "01　問題與動機", "數字不是背景，而是決策失誤的累積",
       "來源：[1] 內政部（2025-02-13）；[2] 環境資訊中心（2026-02-12）。數字為官方統計，非本系統實驗結果。")
stats = [
    ("3,450", "件", "2015–2024 年山域事故", "平均每年約 345 件，且未見下降趨勢。", FOREST),
    ("37%", "迷路", "1,263 件為迷路，占比最高", "通訊點不足與路跡不清是結構性問題。", EMBER),
    ("9", "件／萬人", "2025 年三座高山型國家公園", "15.2 萬人次入園，事故原因以創傷 31.2% 最高。", PINE),
    ("0.08–0.09%", "事故率", "2023–2025 年，近 2016–2019 的兩倍", "裝備與資訊普及，並沒有讓風險自動下降。", RED),
]
for i, (big, unit, label, desc, col) in enumerate(stats):
    x = MX + i * 3.02
    rect(s, x, 1.86, 2.86, 3.55, fill=WHITE, line=BORDER, lw=0.6)
    rect(s, x, 1.86, 2.86, 0.07, fill=col)
    text(s, x + 0.2, 2.12, 2.45, 0.75, big, 27 if len(big) < 8 else 21, col, bold=True, font=EN)
    text(s, x + 0.2, 2.78, 2.4, 0.28, unit, 9.5, MUTED, bold=True)
    text(s, x + 0.2, 3.12, 2.45, 0.62, label, 11, FOREST, bold=True, line_spacing=1.2)
    text(s, x + 0.2, 3.82, 2.45, 1.35, desc, 9.5, SLATE, line_spacing=1.35)
rect(s, MX, 5.62, CW, 0.92, fill=SAND)
rect(s, MX, 5.62, 0.08, 0.92, fill=EMBER)
text(s, MX + 0.3, 5.72, CW - 0.5, 0.72,
     [[("真正的缺口：", {"bold": True, "color": FOREST}),
       ("資料很多，但沒有被轉成「這次要不要去、走到哪裡、幾點回頭」的決策。事故率上升，說明資訊普及不等於風險下降。", {"color": SLATE})]],
     11.5, SLATE, line_spacing=1.3)
footer(s, 4)
notes(s, "四個數字。第一，十年 3,450 件，平均每年 345 件。第二，迷路占 37%，這其實是資訊與導航問題。"
         "第三，2025 年三座高山型國家公園 15.2 萬人次、每萬人 9 件。第四，事故率從 2016–2019 的 0.04–0.05% 上升到 0.08–0.09%。"
         "我想強調的是最後一句：裝備變好、資訊變多，風險沒有自動下降，因為決策沒有變好。")

# ----------------------------------------------------------------------------
# 05 why existing tools fail
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "01　問題與動機", "五個環節，沒有一個對新手友善",
       "來源：[6] 一站式服務網；[7] 氣象署；[9] 上河文化；[10] TravelPlanner（ICML 2024）。")
cards = [
    ("01", "資訊分散", "入園、天氣、路況、GPX、山屋分布在 5 個以上網站與 PDF。", SKY),
    ("02", "知識過時", "舊部落格與去年的 GPX，被當成今年的路況。", GOLD),
    ("03", "平均建議", "路線難度是一個標籤，但風險是隊伍、天氣與時間的函數。", PINE),
    ("04", "事後統計", "事故資料告訴你過去發生什麼，不告訴你這次會不會發生。", MOSS),
]
for i, (num, t, d, col) in enumerate(cards):
    x = MX + (i % 2) * 3.02
    y = 1.86 + (i // 2) * 2.15
    rect(s, x, y, 2.86, 1.92, fill=WHITE, line=BORDER, lw=0.6)
    text(s, x + 0.2, y + 0.14, 0.6, 0.3, num, 9.5, col, bold=True, font=EN)
    text(s, x + 0.2, y + 0.44, 2.45, 0.32, t, 14, FOREST, bold=True)
    text(s, x + 0.2, y + 0.88, 2.45, 0.95, d, 9.8, SLATE, line_spacing=1.32)
# right dark panel
rect(s, 6.72, 1.86, 5.88, 4.02, fill=FOREST)
text(s, 7.02, 2.12, 5.2, 0.3, "LLM 也不是萬靈丹", 9.5, EMBER, bold=True, font=EN)
text(s, 7.02, 2.5, 2.4, 1.0, "0.6%", 55, CREAM, bold=True, font=EN)
text(s, 9.35, 2.62, 3.0, 0.85, "GPT-4 在 TravelPlanner\n多重約束規劃的成功率", 10.5, MOSS, line_spacing=1.3)
text(s, 7.02, 3.72, 5.3, 1.95,
     "模型能寫出「看起來很完整」的行程，卻常漏掉硬性限制、混淆資料時效，"
     "甚至給出沒有來源支撐的樂觀建議。問題不是生成能力，而是驗證與責任。",
     11, CREAM, line_spacing=1.45)
text(s, 7.02, 5.52, 5.2, 0.3, "— TravelPlanner, ICML 2024 [10]", 8.5, MOSS, font=EN)
text(s, MX, 6.22, CW, 0.42,
     [[("所以我們要做的不是聊天機器人，", {"color": SLATE}),
       ("而是一個把「查證、計算、拒絕」變成流程的決策支援系統。", {"bold": True, "color": FOREST})]],
     12.5)
footer(s, 5)
notes(s, "現有工具不是不好，而是各自只解一段。一站式服務網管許可、氣象署管天氣、社群管路況、上河管步程，"
         "但新手要的是『整合後的決定』。右邊這個 0.6% 很關鍵：TravelPlanner 讓 GPT-4 在 1,225 個真實需求上規劃，"
         "完全滿足所有約束的比率只有 0.6%。所以我們不能只靠 LLM 生成，必須有工具與驗證層。")

# ----------------------------------------------------------------------------
# 06 problem definition
# ----------------------------------------------------------------------------
s = new_slide(FOREST)
text(s, MX, 0.62, 4.0, 0.3, "01　問題定義", 10.5, EMBER, bold=True, font=EN)
text(s, MX, 1.18, 11.9, 1.55,
     "「如何在資料不完整、預報不確定、\n使用者能力差異大的情況下，產生一份\n不會把不該上山的人送上山的計畫？」",
     25, CREAM, bold=True, line_spacing=1.42)
line(s, MX, 3.38, MX + 1.4, 3.38, EMBER, 4)
subs = [
    ("語意", "聽懂「輕鬆一點」背後的抽籤、山屋、午後雷雨與高山症。"),
    ("資料", "對齊官方規則、即時天氣、封閉與水源，而不是訓練記憶。"),
    ("分析", "用可檢查的數值估步程、風險與不確定性，不憑感覺。"),
    ("責任", "紅旗時敢說不，說明原因、給替代，並把決定交還給人。"),
]
for i, (t, d) in enumerate(subs):
    x = MX + i * 3.05
    text(s, x, 4.55, 2.75, 0.3, f"0{i+1}", 9.5, EMBER, bold=True, font=EN)
    text(s, x, 4.88, 2.75, 0.35, t, 15, CREAM, bold=True)
    text(s, x, 5.32, 2.72, 1.05, d, 10, MOSS, line_spacing=1.4)
text(s, MX, 6.78, 11.8, 0.3, "這四個問題，對應後面的四個設計層：LLM、資料層、分析引擎、安全與證據層。", 9.5, RGBColor(0x9A, 0xB5, 0xA8))
notes(s, "這是整份提案的核心問句。注意它問的不是『怎麼生成計畫』，而是『怎麼不把不該上山的人送上山』。"
         "這句話拆成四個子問題：語意、資料、分析、責任。後面的架構就是逐一回應這四件事。")

# ----------------------------------------------------------------------------
# 07 section 02
# ----------------------------------------------------------------------------
s = section("02", "RELATED WORK & GAP", "兩邊都很成熟，中間卻沒有橋", "AI 規劃研究與登山領域知識，各自解決了一半的問題。", 7)
notes(s, "第二段看文獻。我們刻意把 AI 與登山領域放在同一張圖上，因為這兩個社群其實很少互相引用。")

# ----------------------------------------------------------------------------
# 08 landscape 2x2
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "02　文獻與缺口", "四個研究叢集，各自成熟，但沒有交會",
       "代表文獻：[10] TravelPlanner；[11] Agentic RAG；[15] GraphRAG；[17] 步程驗證；[18] 個人化步程；[20] WMS 高山症指引。")
clusters = [
    ("A｜LLM 規劃與代理", "TravelPlanner 0.6% 成功率；ReAct 與 Agentic RAG 讓代理會規劃、反思、呼叫工具。", "強項：語言與任務拆解\n弱點：約束漏檢、無安全責任", SKY),
    ("B｜檢索與知識圖譜", "RAG、Self-RAG、GraphRAG 處理知識取得與跨文件理解；Temporal KG 處理時效。", "強項：知識覆蓋與引用\n弱點：缺領域硬規則與即時狀態", PINE),
    ("C｜步程與個人化", "Tobler／Naismith 為 baseline；GPS 驗證顯示平台估算有顯著偏差；個人化可改善誤差。", "強項：可計算、可比較\n弱點：缺天氣、海拔與隊伍情境", GOLD),
    ("D｜山域風險與醫學", "事故統計、步道分級、高山症指引與紅旗處置，構成領域的安全底線。", "強項：後果明確、規則清楚\n弱點：多為事後統計、非個人化、非即時", EMBER),
]
for i, (t, d, sw, col) in enumerate(clusters):
    x = MX + (i % 2) * 6.02
    y = 1.82 + (i // 2) * 2.18
    rect(s, x, y, 5.86, 2.0, fill=WHITE, line=BORDER, lw=0.6)
    rect(s, x, y, 0.07, 2.0, fill=col)
    text(s, x + 0.25, y + 0.14, 5.3, 0.3, t, 12.5, FOREST, bold=True)
    text(s, x + 0.25, y + 0.52, 5.35, 0.86, d, 9.6, SLATE, line_spacing=1.3)
    line(s, x + 0.25, y + 1.06, x + 5.58, y + 1.06, BORDER, 0.6)
    text(s, x + 0.25, y + 1.18, 5.35, 0.55, sw, 8.8, MUTED, line_spacing=1.25)
# gap bar
rect(s, MX, 6.06, CW, 0.44, fill=SAND)
text(s, MX, 6.11, CW, 0.36, "缺口：時效 × 個人化 × 硬規則 × 證據", 10.5, FOREST, bold=True,
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
footer(s, 8)
notes(s, "左上：LLM 代理很會規劃，但 TravelPlanner 證明它會漏約束。右上：RAG 與知識圖譜解決知識取得，但不會判斷『這條路今天封了沒』。"
         "左下：步程研究可以算得很準，但多是單一路線、單一地區。右下：登山領域有很多安全規則，但通常是事後統計或靜態指引。"
         "四個叢集的中間，就是我們的缺口。")

# ----------------------------------------------------------------------------
# 09 article table
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "02　文獻與缺口", "七篇關鍵文獻（節選自 12 篇）",
       "完整 12 篇與 8 欄位對照見 Proposal_Document 表 1；此處節錄與本專題最直接相關的 7 篇。")
data = [
    ["Ref.", "主題", "方法", "關鍵發現", "對本專題的意義"],
    ["[10] 2024", "真實行程規劃", "LLM agent + benchmark", "GPT-4 多重約束成功率僅 0.6%", "需要工具與驗證層，不能只靠生成"],
    ["[15] 2024", "全局問答", "GraphRAG", "改善跨文件與全局理解", "知識圖譜是必要的檢索結構"],
    ["[17] 2025", "步程估算驗證", "GPS 軌跡比較", "平台估算與實際時間有顯著偏差", "步程必須校正，並以 P90 規劃"],
    ["[18] 2012", "個人化步程", "個人化成本函數", "相較 Naismith 最多改善 23%", "個人化有效，但需揭露資料稀疏"],
    ["[20] 2019", "高山症指引", "專家共識", "有症狀勿上升、重症下降", "紅旗規則的醫學依據"],
    ["[1] 2025", "臺灣事故統計", "官方統計", "3,450 件、迷路 37%", "問題定義與風險樣態"],
    ["[2] 2026", "高山事故率", "官方統計", "0.08–0.09%、每萬人 9 件", "風險正在上升，非飽和"],
]
table(s, data, MX, 1.82, CW, 4.55, [0.9, 1.55, 1.95, 2.85, 2.9], size=8.7, head_size=9)
text(s, MX, 6.5, CW, 0.28, "這張表同時是我們的研究定位：不是發明新模型，而是把四個叢集接成一個可運作、可驗證的系統。", 9.5, SLATE)
footer(s, 9)
notes(s, "這張表把文獻收斂成五個欄位：出處、主題、方法、關鍵發現、對我們的意義。最右邊那欄是關鍵——我們不是要發明新的 LLM，"
         "而是把已經成熟的東西接起來。例如 TravelPlanner 告訴我們需要驗證，GraphRAG 告訴我們需要圖譜，"
         "步程研究告訴我們需要個人化與 P90，WMS 指引告訴我們紅旗的醫學底線。")

# ----------------------------------------------------------------------------
# 10 gap
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "02　文獻與缺口", "三個沒有被接起來的地方", "Research Gap：缺一個能把時效、個人化、硬規則與證據追溯整合在一起的臺灣高山代理人。")
gaps = [
    ("時效沒有進模型", "官方公告、山屋狀態、崩塌與水源每天都在變；但 LLM 的知識停在訓練截止日，RAG 也常忽略文件有效期。",
     "→ 時序知識圖譜＋有效期欄位", SKY),
    ("個人化沒有進安全", "步程可以個人化，但風險規則常被平均值或路線標籤取代；新手被系統性低估。",
     "→ 個人化只調可調項，紅旗不可覆寫", GOLD),
    ("證據沒有進介面", "使用者看到一個分數，卻不知道它從哪來、何時有效、衝突出現在哪。",
     "→ Evidence Ledger＋衝突顯示", EMBER),
]
for i, (t, d, fix, col) in enumerate(gaps):
    y = 1.86 + i * 1.56
    rect(s, MX, y, CW, 1.34, fill=WHITE, line=BORDER, lw=0.6)
    rect(s, MX, y, 0.08, 1.34, fill=col)
    text(s, MX + 0.3, y + 0.18, 3.5, 0.34, t, 14, FOREST, bold=True)
    text(s, MX + 3.95, y + 0.16, 4.7, 0.95, d, 9.8, SLATE, line_spacing=1.32)
    text(s, MX + 8.85, y + 0.42, 3.4, 0.5, fix, 9.5, col, bold=True, line_spacing=1.25)
text(s, MX, 6.55, CW, 0.3, "所以 TrailGuard TW 的定位不是「更好的聊天機器人」，而是「把四個東西接起來的決策基礎設施」。", 10.5, PINE, bold=True)
footer(s, 10)
notes(s, "文獻看完了，缺口其實很清楚：第一，時效沒有進模型；第二，個人化沒有進安全；第三，證據沒有進介面。"
         "右邊是我們對應的設計。這三條也正好對應後面的 Temporal KG、紅旗覆寫與 Evidence Ledger。")

# ----------------------------------------------------------------------------
# 11 section 03
# ----------------------------------------------------------------------------
s = section("03", "DEEP RESEARCH", "專家不是比較勇敢，是比較會留餘裕", "五個思維、三個爭論、十個問題，定義什麼叫「真的懂」。", 11)
notes(s, "第三段是深度研究。這部分不是文獻回顧，而是回答：這個領域的專家怎麼想？他們在爭什麼？我們怎麼判斷一個人真的懂？")

# ----------------------------------------------------------------------------
# 12 five mindsets
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "03　深度研究", "五個核心思維：從「攻頂」轉向「回來」",
       "右欄是設計意涵：每個思維都要能在程式或 UI 裡被看見，否則它只是簡報上的一句話。")
minds = [
    ("01", "安全餘裕優先於效率", "保留時間、體力、飲水與撤退餘裕；預設會出事。", "P90 規劃、20% 緩衝、回頭時間", PINE),
    ("02", "證據有階層，時間會改變答案", "官方公告與網友留言不是同等證據；去年的路況不等於今年。", "來源階層、valid_from／valid_to", SKY),
    ("03", "風險是情境的函數，不是標籤", "同一條路，對新手、雪季、午後雷雨的風險完全不同。", "Route × Weather × Team × Time", GOLD),
    ("04", "計畫是假設，不是承諾", "行前計畫一定會被現場修正；要設檢查點與替代路線。", "IF-THEN 規則、可重算的計畫物件", EMBER),
    ("05", "撤退與問責是人類的責任", "AI 可以提示紅旗，但不能代替領隊承擔責任。", "NO-GO／HOLD、理由欄、留守人", RED),
]
for i, (num, t, d, impl, col) in enumerate(minds):
    y = 1.8 + i * 0.97
    text(s, MX, y + 0.05, 0.55, 0.35, num, 9.5, col, bold=True, font=EN)
    text(s, MX + 0.5, y, 3.55, 0.35, t, 12.5, FOREST, bold=True)
    text(s, MX + 0.5, y + 0.32, 5.5, 0.55, d, 9.3, SLATE, line_spacing=1.25)
    text(s, 7.55, y + 0.16, 5.0, 0.5, impl, 9.5, col, bold=True, line_spacing=1.2)
    if i < 4:
        line(s, MX, y + 0.86, W - MX, y + 0.86, BORDER, 0.5)
footer(s, 12)
notes(s, "五個思維。第一個是安全餘裕：專家不是比較敢，是比較會留退路。第二個是證據階層與時效。"
         "第三個是風險的情境性。第四個是把計畫當假設，所以我們輸出的是可重算的物件，不是一份 PDF。"
         "第五個最重要：撤退與問責是人類的責任，AI 只能把紅旗與證據整理好。右邊是每個思維對應的設計。")

# ----------------------------------------------------------------------------
# 13 controversies
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "03　深度研究", "三個專業爭論：我們的答案不是折衷，是分層")
cols = [
    ("爭論一", "面對不確定預報", "保守否決", "颱風、豪雨、雷暴就 NO-GO，避免僥倖。",
     "保留彈性", "40% 降雨不等於一定下雨；過度保守會造成狼來了。",
     "立即致命的紅旗硬否決；機率性風險分級、揭露不確定性。", SKY),
    ("爭論二", "步程與風險規則", "標準化", "上河步程、Naismith、國家公園分級可溝通、可比較。",
     "高度個人化", "體能、揹負、經驗與易感性不同；標準化會低估新手。",
     "標準化當 baseline，個人化只調可調項，不能覆寫紅旗。", GOLD),
    ("爭論三", "AI 的角色", "明確建議", "使用者要的是答案；模糊的「僅供參考」失去價值。",
     "輔助判斷", "風險涉及價值與現場；過度明確會造成 automation bias。",
     "分級建議＋證據＋替代方案；紅旗可說不建議，但不代替現場判斷。", EMBER),
]
for i, (tag, topic, a, ad, b, bd, sol, col) in enumerate(cols):
    x = MX + i * 4.02
    rect(s, x, 1.84, 3.82, 4.52, fill=WHITE, line=BORDER, lw=0.6)
    text(s, x + 0.22, 2.0, 3.3, 0.25, tag, 8.5, col, bold=True, font=EN)
    text(s, x + 0.22, 2.28, 3.4, 0.32, topic, 13, FOREST, bold=True)
    text(s, x + 0.22, 2.76, 3.3, 0.3, "A｜" + a, 10, PINE, bold=True)
    text(s, x + 0.22, 3.14, 3.38, 0.78, ad, 9, MUTED, line_spacing=1.3)
    text(s, x + 0.22, 3.96, 3.3, 0.3, "B｜" + b, 10, EMBER, bold=True)
    text(s, x + 0.22, 4.34, 3.38, 0.78, bd, 9, MUTED, line_spacing=1.3)
    line(s, x + 0.22, 5.16, x + 3.6, 5.16, BORDER, 0.6)
    text(s, x + 0.22, 5.26, 3.35, 0.95, sol, 9.4, FOREST, bold=True, line_spacing=1.32)
text(s, MX, 6.55, CW, 0.3, "共同原則：硬性紅旗用否決，機率性風險用分級；系統給建議，人類留理由。", 10, SLATE)
footer(s, 13)
notes(s, "三個爭論。第一個是保守否決還是保留彈性。我們的答案不是折衷，而是分層：颱風、封閉、雷暴、嚴重症狀這種立即致命的，硬否決；"
         "降雨 40% 這種機率性的，分級並揭露不確定性。第二個是標準化還是個人化，我們用標準化當 baseline，個人化只調可調項。"
         "第三個是 AI 要不要給明確建議，我們給分級建議與替代方案，但責任留給人。")

# ----------------------------------------------------------------------------
# 14 ten questions 1/2
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "03　深度研究", "十個問題，測的是判斷，不是名詞（1/2）", "每個問題都附「好的回答應該展現什麼」，用於專家訪談與評估標註。")
qs = [
    ("Q1", "事故率只有 0.08–0.09%，為什麼還要做風險系統？", "後果嚴重、救援成本高、多數可預防；比率上升代表風險未下降。"),
    ("Q2", "預報午後降雨 40%，你會取消嗎？", "看降雨時段、暴露地形、撤退點與雨具，不把概率當二分法。"),
    ("Q3", "安全與登頂成功率怎麼取捨？", "區分可接受與不可接受風險；給三個候選，讓使用者看見代價。"),
    ("Q4", "使用者謊報體能或隱瞞病史怎麼辦？", "保守先驗、行為問題、行程檢查點動態校正；關鍵自述標「未驗證」。"),
    ("Q5", "官方說開放、社群說崩塌，信誰？", "官方是行政基準、社群是即時提示；顯示衝突、標時間位置、保守處置。"),
]
for i, (q, t, a) in enumerate(qs):
    y = 1.82 + i * 0.98
    text(s, MX, y + 0.04, 0.5, 0.3, q, 9.5, EMBER, bold=True, font=EN)
    text(s, MX + 0.52, y, 5.55, 0.42, t, 10.8, FOREST, bold=True, line_spacing=1.15)
    text(s, 6.75, y + 0.02, 5.85, 0.62, a, 9.3, SLATE, line_spacing=1.28)
    if i < 4:
        line(s, MX, y + 0.86, W - MX, y + 0.86, BORDER, 0.5)
footer(s, 14)
notes(s, "十個問題分兩頁。Q1 到 Q5 偏概念與判斷。Q1 是『比率這麼低，為何還要做』，答案是後果與可預防性，不是比率本身。"
         "Q2 是機率思考，40% 不是二分法。Q3 是價值取捨，我們用三個候選把代價攤開。"
         "Q4 是資料品質，Q5 是來源衝突，這兩個直接對應後面的設計。")

# ----------------------------------------------------------------------------
# 15 ten questions 2/2
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "03　深度研究", "十個問題，測的是判斷，不是名詞（2/2）", "後五題偏設計、臨場處置與評估，是系統行為的直接測試。")
qs = [
    ("Q6", "Naismith、Tobler、個人化 ML，哪個好？", "比資料需求、偏差、可解釋性；以 Tobler 為 baseline，加個人化與不確定性。"),
    ("Q7", "系統應該有權限直接說「不可以去」嗎？", "硬紅旗可以 NO-GO；軟風險給條件與替代；不代替人類做價值判斷。"),
    ("Q8", "隊友在 3,500 m 步態不穩、嘔吐，怎麼辦？", "辨識高山腦水腫紅旗，立即下降、求救、通知留守人；不給藥物劑量。"),
    ("Q9", "入園核准了，但出發前地震封閉？", "許可不是安全保證；以最新封閉為硬約束，重算替代或延期。"),
    ("Q10", "怎麼證明系統的建議「安全」？", "專家標註、對抗案例、FSR、CSR、EGR 與前瞻測試；安全是反事實的。"),
]
for i, (q, t, a) in enumerate(qs):
    y = 1.82 + i * 0.98
    text(s, MX, y + 0.04, 0.6, 0.3, q, 9.5, EMBER, bold=True, font=EN)
    text(s, MX + 0.62, y, 5.45, 0.42, t, 10.8, FOREST, bold=True, line_spacing=1.15)
    text(s, 6.75, y + 0.02, 5.85, 0.62, a, 9.3, SLATE, line_spacing=1.28)
    if i < 4:
        line(s, MX, y + 0.86, W - MX, y + 0.86, BORDER, 0.5)
footer(s, 15)
notes(s, "Q6 到 Q10 更接近系統設計。Q6 是模型選擇，我們不追逐最複雜的模型，而是用可解釋的 baseline 加校正。"
         "Q7 是權限邊界。Q8 是臨場紅旗，這題沒有模糊空間。Q9 是制度與現實的落差。Q10 是評估，也是整份提案的方法論核心："
         "安全不能用滿意度證明，要用反事實與錯誤成本來量。")

# ----------------------------------------------------------------------------
# 16 section 04
# ----------------------------------------------------------------------------
s = section("04", "PROPOSED SCHEME", "讓 LLM 負責理解，讓計算負責證據", "一個核心代理人、一個分析引擎、一個知識層、一個跨層的安全層。", 16)
notes(s, "進到方案。先講一句話：我們不讓 LLM 算數字，也不讓它決定紅旗。它負責理解、追問、規劃與解釋；計算與驗證交給工具。")

# ----------------------------------------------------------------------------
# 17 solution overview
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "04　提出方案", "一個會算、會查、也會說不的代理人", "設計原則：Evidence before fluency；Safety before optimization；Human in the loop。")
# three layers
layers = [
    ("LLM 大腦", "理解意圖、追問缺槽、拆解任務、生成說明", SKY, "03"),
    ("Analytics Engine", "步程 P50/P90、天氣窗格、AMS 風險、路線風險、行程最佳化", PINE, "05"),
    ("Knowledge Layer", "Temporal KG＋Hybrid RAG：官方規範、步道、山屋、水源、事故、醫學", GOLD, "06"),
]
for i, (t, d, col, tag) in enumerate(layers):
    y = 1.86 + i * 1.16
    rect(s, MX, y, 8.1, 0.98, fill=WHITE, line=BORDER, lw=0.6)
    rect(s, MX, y, 0.08, 0.98, fill=col)
    text(s, MX + 0.28, y + 0.14, 2.55, 0.3, t, 12.5, FOREST, bold=True)
    text(s, MX + 2.9, y + 0.14, 4.95, 0.72, d, 9.4, SLATE, line_spacing=1.25)
    text(s, MX + 7.42, y + 0.3, 0.5, 0.25, tag, 8.5, col, bold=True, font=EN)
# safety layer
rect(s, MX, 5.42, CW, 0.92, fill=FOREST)
text(s, MX + 0.28, 5.55, 4.3, 0.28, "Safety & Evidence Layer（跨層）", 9.5, EMBER, bold=True, font=EN)
text(s, MX + 0.28, 5.86, 8.6, 0.3, "來源階層、Evidence Ledger、紅旗覆寫、隱私、P50/P90", 8.8, CREAM)
text(s, W - MX - 2.3, 5.72, 2.0, 0.3, "No source, no number.", 9.5, EMBER, bold=True, align=PP_ALIGN.RIGHT, font=EN)
# output card right
rect(s, 9.15, 1.86, 3.45, 3.35, fill=SAND)
text(s, 9.4, 2.04, 3.0, 0.28, "輸出：行前決策包", 9, PINE, bold=True)
out = ["3 個候選：安全／平衡／進取", "逐段風險儀表板", "撤退點與回頭時間", "裝備、水源、通訊檢查表", "離線緊急卡與留守人腳本", "每個數字的來源與時間戳"]
yy = 2.42
for o in out:
    text(s, 9.4, yy, 0.18, 0.25, "▪", 8, EMBER, bold=True)
    text(s, 9.62, yy - 0.01, 2.85, 0.42, o, 8.8, SLATE, line_spacing=1.15)
    yy += 0.4
footer(s, 17)
notes(s, "整體是三層加一個跨層。LLM 負責語言與任務，Analytics Engine 負責計算，Knowledge Layer 負責查。"
         "右邊是使用者真正拿到的東西：不是一段文字，而是三個候選、逐段儀表板、撤退點、檢查表與離線卡。"
         "下面那條 Safety & Evidence Layer 橫跨三層，負責來源、帳本、紅旗與不確定性。")

# ----------------------------------------------------------------------------
# 18 scenario
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "04　提出方案", "情境：玉山三天兩夜，兩位第一次上高山", "人物誌：2 位新手＋1 位半經驗；4/10–4/12；不想住山屋、不單攻、不走雪季。")
# vertical timeline
tl_x = 1.98
line(s, tl_x, 2.04, tl_x, 5.94, MOSS, 1.2)
steps = [
    ("D-30", "需求訪談", "抽籤、山屋、體力、病史；確認「不單攻」是硬條件。"),
    ("D-14", "候選行程", "安全／平衡／進取三案；逐段 P90 與撤退點。"),
    ("D-1", "行前複查", "天氣、封閉、床位、裝備；輸出離線卡。"),
    ("D1", "現場檢查", "12:00 未到排雲→啟動 B 計畫。"),
    ("D2", "攻頂窗口", "11:30 前通過暴露段；午後雷雨則折返。"),
    ("D3", "撤退", "保留 20% 時間緩衝，天黑前回登山口。"),
]
for i, (d, t, desc) in enumerate(steps):
    y = 1.86 + i * 0.70
    hl = i in (3, 4)
    col = EMBER if hl else PINE
    text(s, MX, y + 0.04, 1.06, 0.26, d, 8.6, col, bold=True, font=EN, align=PP_ALIGN.RIGHT)
    rect(s, tl_x - 0.10, y + 0.09, 0.20, 0.20, fill=col, radius=0.5)
    text(s, tl_x + 0.24, y - 0.01, 1.95, 0.3, t, 10.2, FOREST, bold=True)
    text(s, tl_x + 0.24, y + 0.29, 6.0, 0.34, desc, 8.4, SLATE, line_spacing=1.2)
# stop-the-trip callout
rect(s, MX, 6.14, CW, 0.54, fill=SAND)
rect(s, MX, 6.14, 0.08, 0.54, fill=EMBER)
text(s, MX + 0.26, 6.24, CW - 0.45, 0.36,
     [[("4/10 颱風警報、步道封閉　→　", {"bold": True, "color": RED}),
       ("系統直接 NO-GO，不讓加權分數抵銷；並提供延期窗口、替代路線與許可變更清單。", {"color": SLATE})]],
     9.5, SLATE)
# right package
rect(s, 8.62, 1.82, 3.98, 4.24, fill=WHITE, line=BORDER, lw=0.6)
text(s, 8.86, 2.0, 3.4, 0.3, "系統輸出（節錄）", 9, PINE, bold=True)
rows = [
    ("方案 A 安全", "三天兩夜、排雲山莊、D3 早退", PINE),
    ("方案 B 平衡", "若未抽中，改住東埔山莊＋兩天一夜", GOLD),
    ("方案 C 進取", "加走西峰，僅在天氣與體能允許時", EMBER),
]
yy = 2.42
for t, d, c in rows:
    text(s, 8.86, yy, 0.16, 0.25, "●", 8, c, bold=True)
    text(s, 9.1, yy - 0.02, 3.2, 0.28, t, 10, FOREST, bold=True)
    text(s, 9.1, yy + 0.28, 3.2, 0.55, d, 8.5, SLATE, line_spacing=1.2)
    yy += 0.92
text(s, 8.86, 5.52, 3.4, 0.5, "＋ 逐段風險、撤退點、裝備清單、離線卡", 8.5, MUTED, line_spacing=1.25)
footer(s, 18)
notes(s, "這是一個具體情境：兩位新手、一位半經驗，玉山三天兩夜。左邊是時間軸，從 D-30 的需求訪談到 D3 撤退。"
         "注意 D1 與 D2 的檢查點：12:00 沒到排雲就啟動 B 計畫，11:30 前通過暴露段。這就是把計畫當假設。"
         "下面這個 4/10 颱風案例是重點：系統不會說『其他項目很安全所以可以去』，而是直接 NO-GO。")

# ----------------------------------------------------------------------------
# 19 architecture
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "04　提出方案", "系統架構：四層設計，一個跨層的安全層")
x0, bw = MX, CW
BY = [1.70, 2.78, 3.86, 4.94]
BH = 0.94


def band(y, color):
    rect(s, x0, y, bw, BH, fill=WHITE, line=BORDER, lw=0.6)
    rect(s, x0, y, 0.07, BH, fill=color)


def mod(x, y, num, title, color, tw=1.75):
    text(s, x, y + 0.32, 0.34, 0.3, num, 11.5, color, bold=True)
    text(s, x + 0.40, y + 0.31, tw, 0.3, title, 10.4, FOREST, bold=True)


# band 1: ①②
band(BY[0], SKY)
mod(x0 + 0.22, BY[0], "①", "使用者與情境", SKY, 1.6)
for j, label in enumerate(["人物誌", "Trip Brief", "保守程度"]):
    pill(s, x0 + 2.45 + j * 1.12, BY[0] + 0.32, 1.0, 0.30, label, SAND, SLATE, 8)
line(s, x0 + 5.95, BY[0] + 0.18, x0 + 5.95, BY[0] + 0.76, BORDER, 0.6)
mod(x0 + 6.12, BY[0], "②", "輸入與互動", SKY, 1.5)
for j, (label, wd) in enumerate([("Chat", 0.72), ("地圖", 0.72), ("GPX", 0.72), ("PDF／截圖", 1.15)]):
    pill(s, x0 + 8.02 + j * 0.88, BY[0] + 0.32, wd, 0.30, label, SAND, SLATE, 8)

# band 2: ③ pipeline
band(BY[1], PINE)
mod(x0 + 0.22, BY[1], "③", "領域資料代理人（核心大腦）", PINE, 3.9)
steps = ["Understand", "Plan", "Acquire", "Analyze", "Generate", "Verify", "Interact"]
for j, st in enumerate(steps):
    px = x0 + 4.95 + j * 0.98
    pill(s, px, BY[1] + 0.32, 0.86, 0.30, st, PALE if st != "Verify" else RGBColor(0xF6, 0xE3, 0xD2), PINE, 6.8)
    if j < 6:
        text(s, px + 0.85, BY[1] + 0.33, 0.14, 0.28, "›", 9, MUTED, bold=True, align=PP_ALIGN.CENTER)

# band 3: ④⑤⑥
band(BY[2], MOSS)
for j, (num, t, d) in enumerate([
    ("④", "資料取得與檢索", "CWA API、開放資料、GPX／PDF、具名社群"),
    ("⑤", "分析引擎", "步程 P50／P90、天氣窗格、AMS、路線風險、最佳化"),
    ("⑥", "知識整合", "Temporal KG＋Hybrid RAG；10 類實體、9 種關聯"),
]):
    gx = x0 + j * 4.0
    if j:
        line(s, gx - 0.12, BY[2] + 0.18, gx - 0.12, BY[2] + 0.76, BORDER, 0.6)
    text(s, gx + 0.22, BY[2] + 0.11, 0.34, 0.3, num, 11, GOLD, bold=True)
    text(s, gx + 0.60, BY[2] + 0.10, 3.2, 0.3, t, 10.4, FOREST, bold=True)
    text(s, gx + 0.60, BY[2] + 0.44, 3.2, 0.42, d, 7.9, SLATE, line_spacing=1.2)

# band 4: ⑦⑧
band(BY[3], EMBER)
for j, (num, t, d) in enumerate([
    ("⑦", "決策與建議", "四級決策；紅旗是否決權，優先於分數"),
    ("⑧", "輸出與互動", "儀表板、PDF、離線緊急卡、行後回饋"),
]):
    gx = x0 + j * 6.0
    if j:
        line(s, gx - 0.12, BY[3] + 0.18, gx - 0.12, BY[3] + 0.76, BORDER, 0.6)
    text(s, gx + 0.22, BY[3] + 0.11, 0.34, 0.3, num, 11, EMBER, bold=True)
    text(s, gx + 0.60, BY[3] + 0.10, 2.2, 0.3, t, 10.4, FOREST, bold=True)
    text(s, gx + 2.75, BY[3] + 0.11, 3.0, 0.55, d, 8.4, SLATE, line_spacing=1.2)

# cross-cutting safety layer
rect(s, x0, 6.02, bw, 0.60, fill=FOREST)
text(s, x0 + 0.24, 6.20, 3.55, 0.26, "Safety & Evidence Layer（跨層）", 8.8, EMBER, bold=True, font=EN)
text(s, x0 + 3.80, 6.21, 7.7, 0.26,
     "Evidence Ledger・Hard Red Flags・Source Hierarchy・Privacy by Design・P50／P90", 7.9, CREAM)
text(s, MX, 6.74, CW, 0.26, "LLM 不是資料庫，也不是計算器；它是協調者與解釋者。每個工具都有 schema，回傳值必附 provenance。", 9.0, SLATE)
footer(s, 19)
notes(s, "這是系統架構。左邊是使用者與情境，中間是核心代理人，下面接工具與資料，右邊是跨層的安全與證據層。"
         "請注意每個工具都有明確的輸入輸出 schema，回傳值一定附 provenance。這是我們能說『No source, no number』的工程基礎。")

# ----------------------------------------------------------------------------
# 20 eight modules
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "04　提出方案", "八個模組：每個模組都有一個「不信任 LLM」的理由", "模組①–⑧ 對應架構圖編號；③⑤⑥ 是主要運算與知識層。")
mods = [
    ("①", "使用者與情境", "人物誌、trip brief、保守程度", SKY),
    ("②", "輸入與互動", "自然語言、地圖、GPX、PDF", SKY),
    ("③", "領域資料代理人", "狀態機＋工具呼叫，Understand→Verify", PINE),
    ("④", "資料取得與檢索", "API、爬蟲、GPX、PDF、社群", MOSS),
    ("⑤", "分析引擎", "步程、天氣、AMS、風險、最佳化", GOLD),
    ("⑥", "知識整合", "Temporal KG＋Hybrid RAG", GOLD),
    ("⑦", "決策與建議", "GO／CONDITIONAL／HOLD／NO-GO", EMBER),
    ("⑧", "輸出與互動", "儀表板、PDF、離線卡、回饋", EMBER),
]
for i, (num, t, d, col) in enumerate(mods):
    x = MX + (i % 4) * 3.02
    y = 1.86 + (i // 4) * 2.18
    rect(s, x, y, 2.86, 1.96, fill=WHITE, line=BORDER, lw=0.6)
    text(s, x + 0.2, y + 0.14, 0.45, 0.3, num, 12, col, bold=True, font=EN)
    text(s, x + 0.62, y + 0.14, 2.05, 0.55, t, 11.5, FOREST, bold=True, line_spacing=1.15)
    text(s, x + 0.2, y + 0.86, 2.48, 0.95, d, 8.8, SLATE, line_spacing=1.3)
rect(s, MX, 6.14, CW, 0.5, fill=SAND)
text(s, MX + 0.25, 6.2, CW - 0.45, 0.4,
     "LLM 只能引用工具結果，不能自行改寫數字；模組⑦的紅旗層擁有否決權，優先於任何平均分數。", 9.5, FOREST, bold=True)
footer(s, 20)
notes(s, "八個模組。①②是入口，③是核心大腦，④⑤⑥是工具與知識，⑦是決策，⑧是輸出。"
         "我想強調的是：每個模組都預設『LLM 可能會錯』。所以③用狀態機限制流程，⑤用 Python 算數字，⑥用圖譜與 RAG 查證據，"
         "⑦用紅旗層保留否決權。這不是不信任模型，而是把責任放在對的地方。")

# ----------------------------------------------------------------------------
# 21 data governance
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "04　提出方案", "資料治理：先問「什麼時候有效」，再問「準不準」",
       "資料來源：[6] 一站式服務網；[7] 氣象署 F-D0047-091；[8] 政府資料開放平台；[9] 上河文化。")
# pyramid
levels = [
    ("官方公告／法規", 5.4, PINE),
    ("同儕審查文獻／醫學指引", 4.6, RGBColor(0x2E, 0x6B, 0x57)),
    ("官方統計／開放資料", 3.8, MOSS),
    ("具名社群回報／GPX", 3.0, GOLD),
    ("匿名社群貼文", 2.2, EMBER),
]
yy = 2.0
for i, (t, w, col) in enumerate(levels):
    x = MX + (5.9 - w) / 2
    rect(s, x, yy, w, 0.62, fill=col)
    text(s, x, yy + 0.04, w, 0.54, t, 8.6, WHITE if i < 3 else FOREST, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    yy += 0.74
text(s, MX, 5.9, 5.9, 0.28, "信任高　→　信任低", 8.5, MUTED, align=PP_ALIGN.CENTER)
# rules
rules = [
    ("有效期", "每筆資料都有 observed_at、retrieved_at、valid_from、valid_to。", PINE),
    ("衝突", "官方與社群衝突時顯示雙方與時間，不自動合併成確定答案。", GOLD),
    ("缺資料", "不推測、不以 0 代替；標記「估計」或輸出「資料不足」。", EMBER),
    ("社群", "只能作為提示與待查證，不能單獨成為 GO／NO-GO 的唯一依據。", SKY),
]
for i, (t, d, col) in enumerate(rules):
    x = 6.55 + (i % 2) * 3.02
    y = 1.9 + (i // 2) * 1.62
    rect(s, x, y, 2.86, 1.42, fill=WHITE, line=BORDER, lw=0.6)
    rect(s, x, y, 2.86, 0.06, fill=col)
    text(s, x + 0.18, y + 0.18, 2.5, 0.3, t, 11, FOREST, bold=True)
    text(s, x + 0.18, y + 0.55, 2.52, 0.8, d, 8.6, SLATE, line_spacing=1.28)
text(s, 6.55, 5.28, 5.9, 1.1,
     "治理不是為了「資料乾淨」，而是為了在資料不乾淨時，系統仍然知道該保守到什麼程度。",
     10, PINE, bold=True, line_spacing=1.4)
footer(s, 21)
notes(s, "資料治理是這個題目最容易做得漂亮、也最容易做假的地方。左邊是來源階層：官方、同儕審查、官方統計、具名社群、匿名社群。"
         "右邊是四條規則。最重要的是『缺資料不推測』：很多系統會用平均值補，但在安全關鍵領域，補一個 0 會讓風險看起來更低。"
         "我們寧可輸出『資料不足』。")

# ----------------------------------------------------------------------------
# 22 temporal KG
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "04　提出方案", "時序知識圖譜：把「有效期限」寫進每一條邊", "實體 10 類、關聯 9 種；每個事實都能回答「什麼時候有效、什麼時候被取代」。")
cx, cy = 5.55, 4.15
LX, LW = MX, 2.55
RX, RW = 6.30, 2.55
AX1, AX2 = 3.37, 6.18
triples = [
    ("Route", "玉山主峰線", FOREST, "hasSegment", "2026-04-01 → 2026-04-30", "Segment", "排雲→主峰", SKY),
    ("Route", "玉山主峰線", FOREST, "staysAt", "床位狀態 2026-10-30 07:10", "Hut", "排雲山莊", PINE),
    ("Segment", "排雲→主峰", SKY, "waterAt", "現地觀測 2026-10-28", "WaterSource", "看天池", MOSS),
    ("Route", "玉山主峰線", FOREST, "affectedBy", "2026-04-03 → 2026-04-18", "HazardEvent", "崩塌／封閉", RED),
    ("HazardEvent", "崩塌／封閉", RED, "supersededBy", "解除公告 2026-04-19", "HazardEvent", "解除（現行）", RED),
    ("Route", "玉山主峰線", FOREST, "governedBy", "2025-01-01 → 未定", "Regulation", "入園規範", GOLD),
    ("Route", "玉山主峰線", FOREST, "supportedBy", "取得 2026-10-31 05:40", "Evidence", "官方公告", EMBER),
]
for i, (an, al, ac, rel, tm, bn, bl, bc) in enumerate(triples):
    y = 1.82 + i * 0.63
    rect(s, LX, y, LW, 0.50, fill=WHITE, line=ac, lw=0.9, radius=0.12)
    text(s, LX + 0.12, y + 0.04, LW - 0.24, 0.22, an, 6.6, ac, bold=True, font=EN)
    text(s, LX + 0.12, y + 0.22, LW - 0.24, 0.24, al, 8.4, FOREST, bold=True)
    text(s, AX1, y + 0.09, AX2 - AX1, 0.20,
         [[(rel, {"font": MONO, "bold": True, "color": SLATE, "size": 6.9}),
           ("　" + tm, {"color": MUTED, "size": 6.4})]],
         align=PP_ALIGN.CENTER)
    line(s, AX1, y + 0.37, AX2, y + 0.37, BORDER, 0.9)
    tri = s.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(AX2), Inches(y + 0.325), Inches(0.10), Inches(0.09))
    tri.rotation = 90
    _tstyle = tri._element.find(qn("p:style"))
    if _tstyle is not None:
        tri._element.remove(_tstyle)
    _fill(tri, MUTED)
    _no_line(tri)
    rect(s, RX, y, RW, 0.50, fill=WHITE, line=bc, lw=0.9, radius=0.12)
    text(s, RX + 0.12, y + 0.04, RW - 0.24, 0.22, bn, 6.6, bc, bold=True, font=EN)
    text(s, RX + 0.12, y + 0.22, RW - 0.24, 0.24, bl, 8.4, FOREST, bold=True)
# right panel
rect(s, 9.20, 1.86, 3.40, 4.24, fill=SAND)
text(s, 9.42, 2.02, 2.95, 0.3, "五個時間欄位", 9.5, PINE, bold=True)
fields = [
    ("observed_at", "事件實際發生時間"),
    ("retrieved_at", "系統取得時間"),
    ("valid_from", "資料開始有效"),
    ("valid_to", "資料失效時間"),
    ("superseded_by", "被哪一筆取代"),
]
yy = 2.42
for k, v in fields:
    text(s, 9.42, yy, 2.95, 0.24, k, 7.8, EMBER, bold=True, font=MONO)
    text(s, 9.42, yy + 0.22, 2.95, 0.3, v, 8.0, SLATE)
    yy += 0.70
text(s, MX, 6.38, 8.4, 0.3, "沒有時間的知識，只是謠言；有時間的知識，才能被負責任地使用。", 9.6, PINE, bold=True)
footer(s, 22)
notes(s, "這是時序知識圖譜的概念圖。左邊是實體：路線、路段、山屋、水源、通訊點、崩塌、規範、證據。"
         "每一條邊都帶時間：什麼時候觀測、什麼時候取得、什麼時候有效、什麼時候失效、被哪一筆取代。"
         "這樣系統才能回答：這條水源的資訊是什麼時候的？這個封閉公告解除了嗎？")

# ----------------------------------------------------------------------------
# 23 analytics
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "04　提出方案", "分析引擎：三個可以被檢查的計算", "LLM 只能引用計算結果；所有參數都標記版本，並以蒙地卡羅輸出 P50／P90。")
cards = [
    ("01", "步程", "Tobler 坡度速度＋個人化校正",
     "T_hat = T_base × f_fitness × f_load × f_weather × f_altitude",
     "以 P90 規劃；步程 MAE 目標 ≤ 20%。",
     "model tobler-v1.2｜GPX 實測校正｜蒙地卡羅 10,000 次", PINE),
    ("02", "天氣窗格", "逐段時間窗的加權風險",
     "W = max_t [0.35 P_precip + 0.25 P_thunder + 0.20 wind + 0.20 visibility]",
     "硬門檻：陣風 >15 m/s、能見度 <500 m、積雪／結冰。",
     "source CWA F-D0047-091｜門檻依 WMS 2019 指引", SKY),
    ("03", "高山症", "透明評分卡＋進階機率模型",
     "p_AMS = σ(β0 + β1 ΔH_sleep + β2 H_max + β3 prior_AMS + β4 SpO2 + β5 symptoms)",
     "四級輸出；步態不穩、休息時呼吸困難→立即下降。",
     "model lls-lr-v1｜Lake Louise 評分｜玉山 AMS 研究", EMBER),
]
for i, (num, t, sub, formula, note, src, col) in enumerate(cards):
    x = MX + i * 4.02
    rect(s, x, 1.86, 3.82, 4.0, fill=WHITE, line=BORDER, lw=0.6)
    rect(s, x, 1.86, 3.82, 0.07, fill=col)
    text(s, x + 0.22, 2.04, 0.5, 0.28, num, 9, col, bold=True, font=EN)
    text(s, x + 0.65, 2.01, 2.9, 0.35, t, 15, FOREST, bold=True)
    text(s, x + 0.22, 2.46, 3.4, 0.3, sub, 8.6, MUTED)
    rect(s, x + 0.22, 2.82, 3.38, 1.16, fill=SAND)
    text(s, x + 0.32, 2.86, 3.18, 1.08, formula, 8.5, INK, font=MONO, line_spacing=1.3,
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 0.22, 4.12, 3.38, 0.62, note, 9.0, SLATE, line_spacing=1.3)
    line(s, x + 0.22, 4.88, x + 3.60, 4.88, BORDER, 0.6)
    text(s, x + 0.22, 4.96, 3.38, 0.22, "參數來源與版本", 7.2, MUTED, bold=True)
    text(s, x + 0.22, 5.18, 3.38, 0.55, src, 7.5, SLATE, line_spacing=1.25)
text(s, MX, 6.06, CW, 0.4,
     [[("重點：", {"bold": True, "color": FOREST}), ("公式不是裝飾。每一個參數都要有來源、版本與敏感度分析；沒有來源的參數，不能進入計算。", {"color": SLATE})]],
     10)
footer(s, 23)
notes(s, "三個計算。步程用 Tobler 當 baseline，加上體能、揹負、天氣、海拔校正，最後用蒙地卡羅輸出 P50 與 P90。"
         "天氣窗格是把降雨、雷暴、風速、能見度合成一個逐段風險，並設硬門檻。高山症用透明評分卡，進階才用 logistic regression。"
         "三個計算都有一個共同點：參數有版本、有來源，LLM 不能改。")

# ----------------------------------------------------------------------------
# 24 risk + red flags
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "04　提出方案", "紅旗優先於分數：寧可少一個山頂，多一個回家的人", "圖 3：風險矩陣為方法示意，非實際路線觀測值。")
pic_fit(s, ASSETS / "fig_risk_matrix.png", MX, 1.78, 5.3, 4.9)
flags = [
    ("氣象", "颱風、豪雨、雷暴、陣風 >15 m/s", "NO-GO／延期", RED),
    ("封閉", "步道封閉、崩塌、地震後管制", "NO-GO／改線", RED),
    ("醫療", "步態不穩、休息時呼吸困難、意識改變", "立即下降、求救", EMBER),
    ("許可", "未取得入園／入山、山屋未中籤", "HOLD／替代", GOLD),
    ("裝備", "缺保暖、雨具、頭燈、離線地圖", "CONDITIONAL", SKY),
]
yy = 1.9
for t, d, act, col in flags:
    rect(s, 6.45, yy, 6.15, 0.82, fill=WHITE, line=BORDER, lw=0.5)
    rect(s, 6.45, yy, 0.07, 0.82, fill=col)
    text(s, 6.68, yy + 0.1, 0.95, 0.3, t, 9.5, col, bold=True)
    text(s, 7.62, yy + 0.08, 3.2, 0.62, d, 8.6, SLATE, line_spacing=1.2)
    text(s, 10.9, yy + 0.18, 1.55, 0.4, act, 8.4, col, bold=True, align=PP_ALIGN.RIGHT)
    yy += 0.94
text(s, 6.45, 6.5, 6.15, 0.3, "紅旗不參與加權：任一成立，直接覆寫分數。", 10, RED, bold=True)
footer(s, 24)
notes(s, "左邊是風險矩陣，但右上角才是重點：紅旗。我們把風險分成兩層：一般風險可以用加權分數溝通，"
         "但氣象、封閉、醫療、許可、裝備這五類紅旗不參與加權。任何一個成立，就直接覆寫分數。"
         "這樣做是因為錯誤的代價不對稱：少爬一座山可以再來，少一個人回不了家不行。")

# ----------------------------------------------------------------------------
# 25 optimization
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "04　提出方案", "行程最佳化：不是排景點，是在約束下找三個候選", "求解器：OR-Tools CP-SAT 或啟發式搜尋；輸出安全、平衡、進取三個 Pareto 候選。")
text(s, MX, 1.86, 5.8, 0.3, "目標函數", 9, PINE, bold=True)
text(s, MX, 2.18, 5.8, 0.62, "min  R_total + λ1 × 逾時懲罰 + λ2 × 成本 + λ3 × 行程變動", 9.5, INK, font=MONO, line_spacing=1.3)
text(s, MX, 2.96, 5.8, 0.3, "硬約束", 9, PINE, bold=True)
cons = ["許可與封閉狀態", "山屋床位與入住規則", "日照與最晚撤退時間", "每段 P90 不超過可用時間", "飲水、保暖、緊急裝備", "使用者明確不可接受條件"]
for i, c in enumerate(cons):
    text(s, MX, 3.3 + i * 0.42, 0.2, 0.3, "—", 8, EMBER, bold=True)
    text(s, MX + 0.22, 3.28 + i * 0.42, 5.3, 0.3, c, 9.5, SLATE)
text(s, MX, 5.95, 5.8, 0.55, "硬約束不是懲罰項。不滿足就是不可行，不會被其他優點抵銷。", 9.5, RED, bold=True, line_spacing=1.3)
# plan cards
plans = [
    ("A｜安全", "P90＋20% 緩衝\n最保守的撤退點",
     [("風險", "低", 0.33), ("登頂機率", "中", 0.50), ("時間緩衝", "+20%", 0.90)],
     "第一次上高山、保守隊伍", PINE),
    ("B｜平衡", "標準 P90\n保留一個備案",
     [("風險", "中", 0.60), ("登頂機率", "較高", 0.75), ("時間緩衝", "標準", 0.65)],
     "有基本體能、想保留彈性", GOLD),
    ("C｜進取", "壓縮緩衝\n需良好體能與天氣",
     [("風險", "較高", 0.85), ("登頂機率", "最高", 0.95), ("時間緩衝", "壓縮", 0.40)],
     "資深隊伍、天氣穩定", EMBER),
]
for i, (t, d, metrics, fit, col) in enumerate(plans):
    x = 6.45 + i * 2.1
    rect(s, x, 1.9, 1.95, 4.2, fill=WHITE, line=BORDER, lw=0.6)
    rect(s, x, 1.9, 1.95, 0.07, fill=col)
    text(s, x + 0.14, 2.08, 1.75, 0.3, t, 10.5, FOREST, bold=True)
    text(s, x + 0.14, 2.45, 1.7, 0.6, d, 8.4, SLATE, line_spacing=1.35)
    for j, (lab, val, pct) in enumerate(metrics):
        my = 3.22 + j * 0.58
        text(s, x + 0.14, my, 1.67, 0.22, lab, 7.2, MUTED)
        text(s, x + 0.14, my, 1.67, 0.22, val, 7.6, col, bold=True, align=PP_ALIGN.RIGHT)
        rect(s, x + 0.14, my + 0.23, 1.67, 0.07, fill=PALE)
        rect(s, x + 0.14, my + 0.23, 1.67 * pct, 0.07, fill=col)
    line(s, x + 0.14, 4.92, x + 1.81, 4.92, BORDER, 0.5)
    text(s, x + 0.14, 5.0, 1.67, 0.2, "適合", 7.2, MUTED)
    text(s, x + 0.14, 5.2, 1.67, 0.7, fit, 8.0, SLATE, line_spacing=1.3)
text(s, 6.45, 6.32, 6.2, 0.3, "三個候選都附限制滿足率與風險分解，讓使用者看見代價。", 8.6, MUTED)
footer(s, 25)
notes(s, "最佳化不是幫使用者選一個答案，而是把可行空間攤開。左邊是目標函數與硬約束，右邊是三個候選。"
         "請注意：硬約束不是懲罰項，不滿足就是不可行，不會被『風景很美』或『比較便宜』抵銷。"
         "三個候選都附限制滿足率與風險分解，使用者可以看到每個選擇的代價。")

# ----------------------------------------------------------------------------
# 26 flowchart
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "04　提出方案", "處理流程：四個地方可以停下來",
       "設計原則：Happy path 不是重點，例外路徑才是安全關鍵系統的核心。｜圖 2：四個「停下來」的分支。")
pic_fit(s, ASSETS / "fig_flowchart_crop.png", 0.50, 1.72, 7.25, 4.70)
stops = [
    ("01", "缺槽追問", "一次只問一個關鍵問題，避免替使用者猜測。", "ASK", SKY),
    ("02", "硬限制不滿足", "不滿足就是不可行，不靠其他優點加分抵銷。", "HOLD", GOLD),
    ("03", "紅旗成立", "直接 NO-GO，或升級為人工決策與通報。", "NO-GO", RED),
    ("04", "證據不足", "輸出「資料不足」，不以平均值或 0 補值。", "UNKNOWN", SLATE),
]
yy = 1.80
for num, t, d, tag, col in stops:
    rect(s, 7.95, yy, 4.66, 1.12, fill=WHITE, line=BORDER, lw=0.6)
    rect(s, 7.95, yy, 0.07, 1.12, fill=col)
    text(s, 8.18, yy + 0.14, 0.45, 0.26, num, 8.5, col, bold=True, font=EN)
    text(s, 8.65, yy + 0.12, 2.7, 0.3, t, 10.4, FOREST, bold=True)
    text(s, 8.65, yy + 0.46, 2.75, 0.55, d, 8.3, SLATE, line_spacing=1.25)
    pill(s, 11.50, yy + 0.40, 0.95, 0.28, tag, PALE, col, 7.0)
    yy += 1.20
footer(s, 26)
notes(s, "這是處理流程。左邊是理解與規劃，中間是取得、分析、生成，右邊是驗證與輸出。"
         "請看四個停下來的地方：缺槽追問、硬限制不滿足、紅旗成立、證據不足。一般系統把這些當失敗，我們把它們當安全設計。"
         "因為在登山情境裡，停下來比硬著頭皮走完更重要。")

# ----------------------------------------------------------------------------
# 27 pseudocode
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "04　提出方案", "虛擬碼：先驗證，再生成", "Algorithm 1 節錄；完整版本見 Proposal_Document 肆、K。")
code = [
    "Algorithm 1: Evidence-Grounded Trip Planning Agent",
    "Input : user query Q, profile U, dates D",
    "Output: candidate plans P, risk report R, ledger E",
    "",
    "01  intent, slots ← parse_and_link(Q, U, D)",
    "02  if missing_critical_slots:",
    "03      ask_one_question_at_a_time(slots); return",
    "04  task_graph ← decompose(intent, slots)",
    "05  data ← parallel_acquire(task_graph, sources)",
    "06  data ← normalize_and_validate(data)",
    "07  knowledge ← hybrid_retrieve(task_graph, data, KG, KB)",
    "08  T ← estimate_hiking_time(data, U, knowledge)",
    "09  W ← compute_weather_windows(data, T)",
    "10  A ← screen_ams_risk(U, data, knowledge)",
    "11  Route ← decompose_route_risk(data, W, A, U)",
    "12  P ← optimize_itineraries(T, W, A, Route, constraints)",
    "13  for each candidate p in P do",
    "14      V ← verify_hard_constraints(p, data, knowledge)",
    "15      F ← check_red_flags(p, data, knowledge)",
    "16      E ← audit_evidence(p, knowledge)",
    "17      if F.critical then mark NO_GO(p); escalate(p)",
    "18      else if V.nonempty then mark REVISE(p, V)",
    "19      else mark feasible(p, R, E)",
    "20  end for",
    "21  rank feasible candidates by risk, margin, fit",
]
rect(s, MX, 1.8, 7.9, 4.95, fill=RGBColor(0x12, 0x2B, 0x24))
text(s, MX + 0.22, 1.92, 7.5, 4.75, [[(c, {})] for c in code], 9.4, RGBColor(0xE8, 0xE2, 0xD4),
     font=MONO, line_spacing=1.2)
# annotations
ann = [
    ("停下來", "缺槽追問，一次只問一個問題", SKY),
    ("算清楚", "步程、天氣、AMS、風險都由工具計算", PINE),
    ("說不", "紅旗優先，直接 NO-GO 或升級人工", RED),
    ("留紀錄", "每個候選都產出 Evidence Ledger", GOLD),
]
yy = 1.86
for t, d, col in ann:
    rect(s, 8.95, yy, 3.65, 1.05, fill=WHITE, line=BORDER, lw=0.6)
    rect(s, 8.95, yy, 0.07, 1.05, fill=col)
    text(s, 9.16, yy + 0.12, 3.25, 0.28, t, 10.5, col, bold=True)
    text(s, 9.16, yy + 0.46, 3.25, 0.5, d, 8.4, SLATE, line_spacing=1.25)
    yy += 1.2
footer(s, 27)
notes(s, "這是 Algorithm 1 的節錄。整個流程有 21 行，但只有四個概念：停下來、算清楚、說不、留紀錄。"
         "第 02 行缺槽就問，第 08 到 12 行全部是工具計算，第 15 到 17 行是紅旗，第 16 與 19 行是證據帳本。"
         "我們刻意不讓 LLM 直接輸出最終數字，因為那是最容易出錯的地方。")

# ----------------------------------------------------------------------------
# 28 evidence ledger
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "04　提出方案", "Evidence Ledger：沒有來源，就沒有數字", "每一筆 claim 都能回答：從哪來、什麼時候取得、什麼時候有效、信心多少。")
data = [
    ["Claim", "Value", "Source", "Retrieved", "Valid", "Conf."],
    ["步程 P90", "147 min", "GPX 實測＋Tobler v1", "2026-10-30", "2026-12-31", "0.78"],
    ["午後雷雨機率", "60%", "CWA F-D0047-091", "2026-10-31 06:00", "2026-10-31 18:00", "0.90"],
    ["排雲山莊床位", "0（候補）", "一站式服務網", "2026-10-31 07:10", "2026-10-31", "0.95"],
    ["R_total", "62／100", "加權公式 v1.2", "2026-10-30", "2026-11-30", "0.70"],
    ["步道狀態", "封閉", "國家公園公告", "2026-10-31 05:40", "直至解除", "0.99"],
]
table(s, data, MX, 1.86, CW, 2.72, [1.35, 1.25, 3.2, 1.85, 1.65, 0.75], size=8.8, head_size=9)
# rules
rules = [
    ("01", "有來源，才輸出", "數值 claim 必須對應至少一個 evidence_id；否則不輸出。", PINE),
    ("02", "過期，就降權", "valid_to 已過 → 降權、標「待查證」，不直接刪除。", GOLD),
    ("03", "衝突，就並列", "官方與社群不一致 → 顯示雙方與時間，不強行合併。", SKY),
    ("04", "缺資料，就說不知道", "不以平均值或 0 代替；輸出「資料不足」與替代查詢。", RED),
]
for i, (num, t, d, col) in enumerate(rules):
    x = MX + i * 3.02
    rect(s, x, 4.82, 2.82, 1.42, fill=WHITE, line=BORDER, lw=0.6)
    rect(s, x, 4.82, 2.82, 0.06, fill=col)
    text(s, x + 0.18, 4.96, 0.4, 0.24, num, 7.6, col, bold=True, font=EN)
    text(s, x + 0.18, 5.18, 2.46, 0.3, t, 10, FOREST, bold=True)
    text(s, x + 0.18, 5.54, 2.46, 0.62, d, 8.3, SLATE, line_spacing=1.28)
rect(s, MX, 6.38, CW, 0.40, fill=SAND)
text(s, MX + 0.24, 6.46, CW - 0.45, 0.26,
     "不是讓答案更漂亮，而是讓答案可以被質疑——這是整個系統的誠實機制。", 9.2, FOREST, bold=True)
footer(s, 28)
notes(s, "Evidence Ledger 是整個系統的誠實機制。左邊是示意表：每一個數字都有來源、取得時間、有效期間與信心。"
         "右邊是四條規則。最重要的是第三與第四條：衝突要並列，缺資料要說不知道。很多 AI 系統的危險不是答錯，"
         "而是用很確定的語氣答一個沒有來源的數字。")

# ----------------------------------------------------------------------------
# 29 section 05
# ----------------------------------------------------------------------------
s = section("05", "EVALUATION & ROADMAP", "先證明量得出來，再證明做得好", "120 個案例、五組對照、一個以錯誤安全為核心的指標。", 29)
notes(s, "第五段是驗證。我們刻意把評估設計放在功能之前講，因為這個題目如果量不出『假安全』，就很難說服別人它真的安全。")

# ----------------------------------------------------------------------------
# 30 evaluation design
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "05　驗證與時程", "120 個案例，五組對照，八個指標", "重要：本頁為實驗設計，尚未執行；所有數值為目標與驗收門檻。")
text(s, MX, 1.82, 4.2, 0.3, "資料集", 9, PINE, bold=True)
text(s, MX, 2.14, 2.0, 0.9, "120", 42, FOREST, bold=True, font=EN)
text(s, MX + 1.55, 2.32, 2.6, 0.5, "個評估案例", 10, MUTED)
dataset = [
    ("30", "條臺灣高山／中級山路線"),
    ("× 3", "種人物誌：新手、半經驗、資深領隊"),
    ("= 90", "個核心情境"),
    ("+ 30", "個壓力／對抗案例"),
]
yy = 3.02
for k, v in dataset:
    text(s, MX, yy, 0.8, 0.28, k, 9.5, EMBER, bold=True, font=EN)
    text(s, MX + 0.85, yy, 3.1, 0.32, v, 8.8, SLATE)
    yy += 0.42
text(s, MX, 5.0, 4.3, 0.3, "對照組", 9, PINE, bold=True)
base = "GPT-4o zero-shot｜GPT-4o＋web search｜RAG-only｜人工流程｜消融：no KG／no verifier／no red flag／no personalization"
text(s, MX, 5.3, 4.3, 1.0, base, 8.4, SLATE, line_spacing=1.4)
# metrics table
data = [
    ["指標", "定義", "目標"],
    ["CSR", "滿足硬性限制／總硬性限制", "≥ 85%"],
    ["EGR", "有有效來源的數值 claim／總數值 claim", "≥ 95%"],
    ["FSR", "不該 GO 卻給 GO／所有不安全案例", "≤ 2%"],
    ["步程 MAE", "預測與實測步程的平均絕對誤差", "≤ 20%"],
    ["專家接受度", "1–5 分", "≥ 4.0"],
    ["SUS", "系統使用性量表", "≥ 75"],
    ["P95 延遲", "完整規劃回應時間", "≤ 60 秒"],
]
table(s, data, 5.45, 1.82, 7.15, 3.72, [1.35, 4.1, 1.0], size=8.4, head_size=8.8)
text(s, 5.45, 5.75, 7.15, 0.85, "統計：paired t-test／Wilcoxon、McNemar、95% CI 與效果量；FSR 與 CSR 依路線難度、人物誌、資料完整度分層。", 8.4, SLATE, line_spacing=1.35)
footer(s, 30)
notes(s, "評估設計。30 條路線乘 3 種人物誌是 90 個核心情境，加 30 個壓力與對抗案例，總共 120 個。"
         "對照組有五類，包含 GPT-4o、RAG-only、人工流程，以及四個消融版本。指標有八個，但今天只講一個最關鍵的：FSR。"
         "再次強調，這些是設計與門檻，不是結果。")

# ----------------------------------------------------------------------------
# 31 false-safe
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "05　驗證與時程", "為什麼量測 False-Safe：說 GO 的代價不對稱", "FSR = 不該 GO 卻給 GO 的案例 ÷ 所有不安全案例；目標 ≤ 2%。")
# 2x2
x0, y0, cw, ch = MX, 1.95, 2.55, 1.55
labels = [
    ("系統說 GO", "系統說 NO-GO／HOLD", ""),
]
# headers
text(s, x0 + 2.55, 1.62, 2.55, 0.28, "系統說 GO", 9, MUTED, bold=True, align=PP_ALIGN.CENTER)
text(s, x0 + 5.1, 1.62, 2.55, 0.28, "系統說 NO-GO", 9, MUTED, bold=True, align=PP_ALIGN.CENTER)
text(s, x0, 1.95, 2.5, 0.3, "實際安全", 9, MUTED, bold=True, align=PP_ALIGN.RIGHT)
text(s, x0, 3.5, 2.5, 0.3, "實際不安全", 9, MUTED, bold=True, align=PP_ALIGN.RIGHT)
cells = [
    (x0 + 2.55, 1.95, "正確放行", "True GO", PALE, PINE),
    (x0 + 5.1, 1.95, "過度保守", "False NO-GO", PALE, GOLD),
    (x0 + 2.55, 3.5, "錯誤安全", "False-Safe（致命）", RGBColor(0xF3, 0xDC, 0xD8), RED),
    (x0 + 5.1, 3.5, "正確阻擋", "True NO-GO", PALE, PINE),
]
for x, y, t, sub, fill, col in cells:
    rect(s, x, y, 2.45, 1.45, fill=fill, line=BORDER, lw=0.8)
    text(s, x + 0.1, y + 0.3, 2.25, 0.35, t, 11.5, col, bold=True, align=PP_ALIGN.CENTER)
    text(s, x + 0.1, y + 0.78, 2.25, 0.3, sub, 8, MUTED, align=PP_ALIGN.CENTER, font=EN)
text(s, MX, 5.22, 7.5, 0.95,
     [[("一般 benchmark 問：", {"color": SLATE}), ("「行程有沒有滿足偏好？」", {"bold": True, "color": FOREST})],
      [("我們問：", {"color": SLATE}), ("「有沒有人被系統錯誤地鼓勵上山？」", {"bold": True, "color": RED})]],
     11.5, SLATE, line_spacing=1.55)
# right panel
rect(s, 9.55, 1.86, 3.05, 4.10, fill=FOREST)
text(s, 9.80, 2.04, 2.6, 0.28, "為什麼門檻是 2%？", 9.5, EMBER, bold=True)
text(s, 9.78, 2.34, 2.7, 0.62, "≤ 2%", 30, EMBER, bold=True, font=EN)
text(s, 9.80, 3.06, 2.58, 1.3,
     "錯誤不對稱：錯誤放行可能造成死亡或不可逆傷害；過度保守只造成行程取消。",
     8.8, CREAM, line_spacing=1.4)
line(s, 9.80, 4.42, 12.35, 4.42, RGBColor(0x2A, 0x4A, 0x3F), 0.8)
text(s, 9.80, 4.56, 1.15, 0.24, "錯誤安全", 8.4, RED, bold=True)
text(s, 11.0, 4.56, 1.45, 0.24, "死亡／不可逆", 8.2, CREAM)
text(s, 9.80, 5.04, 1.15, 0.24, "過度保守", 8.4, GOLD, bold=True)
text(s, 11.0, 5.04, 1.45, 0.24, "行程取消", 8.2, CREAM)
text(s, 9.80, 5.50, 2.55, 0.3, "所以寧可保守，也不讓 FSR 失控。", 8.2, EMBER, bold=True)
text(s, MX, 6.5, CW, 0.3, "這個指標也決定了產品設計：紅旗必須有否決權，否則 FSR 不可能壓到 2% 以下。", 9.5, PINE, bold=True)
footer(s, 31)
notes(s, "這頁是整份提案的價值核心。左邊是 2x2：正確放行、過度保守、錯誤安全、正確阻擋。"
         "一般規劃 benchmark 量的是『有沒有滿足偏好』，我們量的是『有沒有把不該上山的人送上山』。"
         "為什麼門檻是 2%？因為錯誤不對稱：False-Safe 可能致命，過度保守只是取消行程。所以我們寧可保守。")

# ----------------------------------------------------------------------------
# 32 gantt
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "05　驗證與時程", "16 週：先把量測做出來，再談功能", "圖 4：W4 知識庫 v1、W8 Agent MVP、W12 核心實驗、W14 使用者測試、W16 Final Handover。")
pic_fit(s, ASSETS / "fig_gantt.png", MX, 1.8, 11.9, 4.3)
# milestones
ms = [("W4", "知識庫 v1"), ("W8", "Agent MVP"), ("W12", "核心實驗"), ("W14", "使用者測試"), ("W16", "Handover")]
for i, (w, t) in enumerate(ms):
    x = MX + 0.25 + i * 2.42
    text(s, x, 6.28, 1.0, 0.26, w, 9, EMBER, bold=True, font=EN)
    text(s, x + 0.5, 6.28, 1.85, 0.26, t, 8.6, FOREST, bold=True)
footer(s, 32)
notes(s, "時程 16 週，分成四個階段：Foundation、Build、Validate、Handover。"
         "我特別想講 W12：核心實驗一定要在 W12 完成，因為 W14 要跑使用者測試，W15 到 W16 才有時間寫文件與錄影。"
         "如果實驗延後，最後的交付一定會壓縮。")

# ----------------------------------------------------------------------------
# 33 outcomes & limitations
# ----------------------------------------------------------------------------
s = new_slide()
header(s, "05　驗證與時程", "預期成果與限制：不把「還沒做」說成「已經做到」")
text(s, MX, 1.82, 5.7, 0.3, "預期成果", 10, PINE, bold=True)
outcomes = [
    "可操作原型：5–8 條路線、3 種人物誌、完整行前決策包",
    "評估協定：120 個案例、專家標註、對照組、錯誤分類",
    "技術資產：Temporal KG schema、Hybrid RAG、Evidence Ledger",
    "文件：Proposal、DESIGN.md、README、Final PPT、Demo 影片",
    "可轉移性：可延伸到其他戶外活動、防災與健康決策",
]
yy = 2.2
for o in outcomes:
    text(s, MX, yy, 0.18, 0.25, "▪", 8, PINE, bold=True)
    text(s, MX + 0.22, yy - 0.02, 5.25, 0.55, o, 9.3, SLATE, line_spacing=1.3)
    yy += 0.72
text(s, 6.6, 1.82, 5.8, 0.3, "限制與風險", 10, RED, bold=True)
limits = [
    ("資料取得", "官方 API 與公告格式不一，部分資料需人工維護。"),
    ("專家標註", "2–3 位專家的時間有限，kappa 可能低於 0.7。"),
    ("步程校正", "臺灣 GPX 實測資料不足，初期誤差可能偏高。"),
    ("場域驗證", "提案階段無法做前瞻性野外驗證。"),
    ("成本與延遲", "多工具呼叫與 rerank 會增加延遲與 API 成本。"),
]
yy = 2.2
for t, d in limits:
    text(s, 6.6, yy, 1.35, 0.28, t, 9, RED, bold=True)
    text(s, 7.95, yy - 0.02, 4.4, 0.55, d, 8.8, SLATE, line_spacing=1.28)
    yy += 0.72
rect(s, MX, 6.0, CW, 0.55, fill=SAND)
text(s, MX + 0.25, 6.08, CW - 0.45, 0.4,
     "所有數字都是驗收門檻；若未達標，我們會報告失敗原因與錯誤分類，而不是修改定義。", 9.3, FOREST, bold=True)
footer(s, 33)
notes(s, "預期成果與限制。左邊是我們希望交付的東西，右邊是我們現在就知道的風險。"
         "我想特別誠實地說：提案階段不可能做前瞻性野外驗證，專家標註也可能不一致，步程校正資料也不足。"
         "這些不是掩飾，而是設計時就要納入的限制。最後一句：如果沒達標，我們報告失敗原因，不改定義。")

# ----------------------------------------------------------------------------
# 34 conclusion
# ----------------------------------------------------------------------------
s = new_slide(FOREST)
text(s, MX, 0.55, 4.0, 0.3, "06　結論", 10.5, EMBER, bold=True, font=EN)
text(s, MX, 1.15, 11.6, 1.85,
     "把不確定性、時效性與安全責任，\n設計進 AI Agent 的架構，\n而不是事後補救。",
     28, CREAM, bold=True, line_spacing=1.38)
line(s, MX, 3.35, MX + 1.5, 3.35, EMBER, 4)
takeaways = [
    ("Evidence before fluency", "先有證據，再有文字。", "No source, no number."),
    ("Safety before optimization", "先過紅旗，再談最佳化。", "紅旗是否決權，不是加分項。"),
    ("Human in the loop", "系統給建議，人類留理由。", "撤退與問責，永遠是人類的責任。"),
]
for i, (en, cn, note) in enumerate(takeaways):
    x = MX + i * 3.95
    text(s, x, 4.0, 3.6, 0.28, en, 8.5, MOSS, bold=True, font=EN)
    text(s, x, 4.35, 3.6, 0.35, cn, 12.5, CREAM, bold=True)
    text(s, x, 4.82, 3.55, 0.7, note, 8.8, RGBColor(0x9A, 0xB5, 0xA8), line_spacing=1.3)
line(s, MX, 5.95, W - MX, 5.95, RGBColor(0x2A, 0x4A, 0x3F), 0.8)
text(s, MX, 6.15, 7.5, 0.4, "TrailGuard TW｜山徑守護者", 13, CREAM, bold=True)
text(s, W - MX - 4.0, 6.2, 4.0, 0.3, "期末專題提案｜2026-10-31", 9, MOSS, align=PP_ALIGN.RIGHT)
notes(s, "結論三句話：Evidence before fluency、Safety before optimization、Human in the loop。"
         "這三句話聽起來很簡單，但每一個都要在架構裡有對應的機制：Evidence Ledger、紅旗覆寫、人類決策與理由欄。"
         "如果只記得住一頁，我希望是這一頁。")

# ----------------------------------------------------------------------------
# 35 Q&A
# ----------------------------------------------------------------------------
s = new_slide(FOREST)
pic_fit(s, ASSETS / "fig_cover.png", 0, 0, W, H)
band = rect(s, 0, 5.05, W, 2.45, fill=FOREST)
fill_alpha(band, 90)
text(s, 0.85, 1.5, 4.0, 0.3, "Q & A", 10.5, EMBER, bold=True, font=EN)
text(s, 0.85, 1.95, 8.2, 1.0, "問題與討論", 42, CREAM, bold=True)
line(s, 0.88, 3.25, 5.2, 3.25, EMBER, 3)
text(s, 0.85, 3.52, 7.4, 1.2,
     "歡迎挑戰我們的假設：\n資料拿得到嗎？紅旗門檻怎麼定？FSR 真的量得出來嗎？",
     15, RGBColor(0xB9, 0xCF, 0xC3), line_spacing=1.5)
text(s, 0.85, 5.55, 7.8, 0.3, "本提案尚未執行實驗；所有成效數字均為設計目標與驗收門檻。", 9, RGBColor(0xA9, 0xBF, 0xB3))
text(s, 0.85, 6.55, 6.0, 0.3, "TrailGuard TW｜山徑守護者", 10, CREAM, bold=True)
notes(s, "最後開放討論。我最希望被挑戰的三個問題是：資料真的拿得到嗎？紅旗門檻怎麼定？FSR 真的量得出來嗎？"
         "這三個問題如果沒有好答案，這個系統就不成立。謝謝大家。")

prs.core_properties.title = "山徑守護者（TrailGuard TW）— 期末專題提案"
prs.core_properties.author = "陳俊安、廖家暉、温偉成、郭冠良"
prs.core_properties.subject = "物聯網應用與資料分析｜期末專題 Proposal"
prs.core_properties.keywords = "登山安全, 風險決策, RAG, 知識圖譜, 領域資料代理人, 臺灣高山"

prs.save(OUT)
print(f"saved {OUT} ({OUT.stat().st_size/1024:.1f} KB), {len(prs.slides)} slides")
