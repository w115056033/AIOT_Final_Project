# -*- coding: utf-8 -*-
"""Build Proposal_Document.docx from Proposal_Document.md.

The markdown intentionally uses a small, documented subset:
- # / ## / ### headings
- paragraphs, **bold**, `code`
- - bullets, 1. numbered lists
- pipe tables
- ![caption](path) images
- > callouts
- ``` code fences
- <!-- PAGEBREAK -->, <!-- LANDSCAPE -->, <!-- PORTRAIT -->, <!-- TOC -->
"""
from __future__ import annotations

import re
import json
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION_START
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Emu
from docx.enum.text import WD_LINE_SPACING
from PIL import Image

BASE = Path(r"C:\Users\User\Desktop\文件\週3_物聯網應用與資料分析_陳煥\week8_2026_10_28\報告")
MD_PATH = BASE / "Proposal_Document.md"
OUT_PATH = BASE / "Proposal_Document.docx"

# Palette
FOREST = "0B241D"
PINE = "1F5C4A"
MOSS = "7FA88C"
SAND = "F4EFE6"
CREAM = "FBF8F1"
EMBER = "D97745"
SLATE = "33413C"
RED = "B23A32"
SKY = "6C9BB5"
GOLD = "C9A227"
INK = "1E2A26"
MUTED = "68736E"
BORDER = "D8D2C4"

FONT_CN = "Microsoft JhengHei"
FONT_EN = "Aptos"
FONT_MONO = "Consolas"


def rgb(hexstr: str) -> RGBColor:
    return RGBColor.from_string(hexstr)


def set_run_font(run, size=None, bold=None, color=None, font=FONT_CN, italic=None):
    if font:
        run.font.name = font
        run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), FONT_CN)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color:
        run.font.color.rgb = rgb(color)


def shade(element, fill: str):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    element.append(shd)


def set_cell_shading(cell, fill: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shade(tcPr, fill)


def set_cell_margins(cell, top=50, start=70, bottom=50, end=70):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.first_child_found_in("w:tcMar")
    if tcMar is None:
        tcMar = OxmlElement("w:tcMar")
        tcPr.append(tcMar)
    for m, v in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tcMar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tcMar.append(node)
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table, color=BORDER, sz=4):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = tblPr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tblPr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = borders.find(qn(f"w:{edge}"))
        if el is None:
            el = OxmlElement(f"w:{edge}")
            borders.append(el)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(sz))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)


def remove_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = tblPr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tblPr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = borders.find(qn(f"w:{edge}"))
        if el is None:
            el = OxmlElement(f"w:{edge}")
            borders.append(el)
        el.set(qn("w:val"), "nil")


def set_table_width(table, width_cm: float):
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblW = tblPr.first_child_found_in("w:tblW")
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    tblW.set(qn("w:w"), str(int(width_cm * 567)))
    tblW.set(qn("w:type"), "dxa")
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:cantSplit")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def add_bottom_border(paragraph, color=EMBER, sz=8, space=4):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = pPr.first_child_found_in("w:pBdr")
    if pBdr is None:
        pBdr = OxmlElement("w:pBdr")
        pPr.append(pBdr)
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(sz))
    bottom.set(qn("w:space"), str(space))
    bottom.set(qn("w:color"), color)
    pBdr.append(bottom)


def add_left_border(paragraph, color=EMBER, sz=14, space=8):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = pPr.first_child_found_in("w:pBdr")
    if pBdr is None:
        pBdr = OxmlElement("w:pBdr")
        pPr.append(pBdr)
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), str(sz))
    left.set(qn("w:space"), str(space))
    left.set(qn("w:color"), color)
    pBdr.append(left)


def add_paragraph_shading(paragraph, fill: str):
    pPr = paragraph._p.get_or_add_pPr()
    shade(pPr, fill)


def set_keep_with_next(paragraph, val=True):
    paragraph.paragraph_format.keep_with_next = val


def add_page_number_footer(section):
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run("TrailGuard TW｜v0.1 Proposal｜第 ")
    set_run_font(r, 8, color=MUTED)
    add_field(p, "PAGE")
    r = p.add_run(" 頁／共 ")
    set_run_font(r, 8, color=MUTED)
    add_field(p, "NUMPAGES")
    r = p.add_run(" 頁")
    set_run_font(r, 8, color=MUTED)


def add_field(paragraph, field_code: str):
    run = paragraph.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = f" {field_code} "
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    txt = OxmlElement("w:t")
    txt.text = "1"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_sep)
    run._r.append(txt)
    run._r.append(fld_end)
    set_run_font(run, 8, color=MUTED)


def add_header(section, width_cm):
    section.header.is_linked_to_previous = False
    p = section.header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run("TrailGuard TW｜以證據為基礎的臺灣高山行程規劃與風險決策支援代理人")
    set_run_font(r, 8, color=MUTED)
    add_bottom_border(p, color=MOSS, sz=4, space=2)


def setup_section(section, landscape=False, first_page=False):
    if landscape:
        section.orientation = WD_ORIENT.LANDSCAPE
        section.page_width = Cm(29.7)
        section.page_height = Cm(21.0)
        section.left_margin = Cm(1.5)
        section.right_margin = Cm(1.5)
        section.top_margin = Cm(1.6)
        section.bottom_margin = Cm(1.5)
        section.header_distance = Cm(0.7)
        section.footer_distance = Cm(0.7)
    else:
        section.orientation = WD_ORIENT.PORTRAIT
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.left_margin = Cm(2.2)
        section.right_margin = Cm(2.2)
        section.top_margin = Cm(2.2)
        section.bottom_margin = Cm(2.0)
        section.header_distance = Cm(0.9)
        section.footer_distance = Cm(0.9)
    section.different_first_page_header_footer = first_page


def body_width(section):
    return (section.page_width - section.left_margin - section.right_margin) / 360000.0


def add_rich_text(paragraph, text: str, size=10.5, color=INK, bold=False, font=FONT_CN):
    """Small inline parser for **bold** and `code`."""
    pattern = re.compile(r"(\*\*.+?\*\*|`.+?`)")
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            r = paragraph.add_run(text[pos:m.start()])
            set_run_font(r, size, bold=bold, color=color, font=font)
        token = m.group(0)
        if token.startswith("**") and token.endswith("**"):
            r = paragraph.add_run(token[2:-2])
            set_run_font(r, size, bold=True, color=color, font=font)
        else:
            r = paragraph.add_run(token[1:-1])
            set_run_font(r, size, bold=bold, color=color, font=FONT_MONO)
            r.font.size = Pt(max(size - 0.8, 7.0))
        pos = m.end()
    if pos < len(text):
        r = paragraph.add_run(text[pos:])
        set_run_font(r, size, bold=bold, color=color, font=font)


def add_heading(doc, text: str, level: int, first=False):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    if level == 1:
        p.paragraph_format.page_break_before = True
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(8)
        add_bottom_border(p, color=EMBER, sz=12, space=4)
        r = p.add_run(text)
        set_run_font(r, 19, bold=True, color=FOREST)
        # outline level 1
        pPr = p._p.get_or_add_pPr()
        outline = OxmlElement("w:outlineLvl")
        outline.set(qn("w:val"), "0")
        pPr.append(outline)
    elif level == 2:
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(5)
        r = p.add_run(text)
        set_run_font(r, 13.5, bold=True, color=PINE)
        pPr = p._p.get_or_add_pPr()
        outline = OxmlElement("w:outlineLvl")
        outline.set(qn("w:val"), "1")
        pPr.append(outline)
    else:
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        set_run_font(r, 11.5, bold=True, color=SLATE)
        pPr = p._p.get_or_add_pPr()
        outline = OxmlElement("w:outlineLvl")
        outline.set(qn("w:val"), "2")
        pPr.append(outline)
    return p


def add_body_paragraph(doc, text: str, ref=False, compact=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)
    pf.line_spacing = 1.45
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if ref:
        pf.left_indent = Cm(0.75)
        pf.first_line_indent = Cm(-0.75)
        pf.space_after = Pt(3)
        pf.line_spacing = 1.25
        add_rich_text(p, text, size=9.2, color=SLATE)
    elif compact:
        # The abstract must fit on its allotted pages: slightly tighter leading.
        pf.space_after = Pt(4)
        pf.line_spacing = 1.33
        add_rich_text(p, text, size=10.2, color=INK)
    else:
        add_rich_text(p, text, size=10.5, color=INK)
    return p


def add_bullet(doc, text: str, numbered=False, compact=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.72)
    pf.first_line_indent = Cm(-0.42)
    pf.space_before = Pt(0)
    pf.space_after = Pt(3)
    pf.line_spacing = 1.35
    size = 10.2 if compact else 10.5
    if numbered:
        add_rich_text(p, text, size=size, color=INK)
    else:
        add_rich_text(p, "•  " + text, size=size, color=INK)
    return p


def add_callout(doc, lines: list[str]):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.45)
    pf.right_indent = Cm(0.25)
    pf.space_before = Pt(6)
    pf.space_after = Pt(8)
    pf.line_spacing = 1.35
    add_paragraph_shading(p, SAND)
    add_left_border(p, color=EMBER, sz=18, space=8)
    for i, line in enumerate(lines):
        if i:
            p.add_run().add_break()
        add_rich_text(p, line, size=9.8, color=SLATE)
    return p


def add_code_block(doc, lines: list[str]):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.35)
    pf.right_indent = Cm(0.2)
    pf.space_before = Pt(5)
    pf.space_after = Pt(8)
    pf.line_spacing = 1.0
    add_paragraph_shading(p, "F7F3EA")
    add_left_border(p, color=MOSS, sz=14, space=6)
    for i, line in enumerate(lines):
        if i:
            p.add_run().add_break()
        r = p.add_run(line if line else " ")
        set_run_font(r, 7.8, color=INK, font=FONT_MONO)
        r._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), FONT_MONO)
    return p


def add_image(doc, path: Path, caption: str, width_cm: float):
    if not path.exists():
        raise FileNotFoundError(path)
    # 依圖片比例限制最大高度，避免接近正方形的圖佔滿整頁
    with Image.open(path) as im:
        aspect = im.size[0] / im.size[1]
    max_h_cm = 11.0
    if width_cm / aspect > max_h_cm:
        width_cm = max_h_cm * aspect
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run()
    run.add_picture(str(path), width=Cm(width_cm))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(0)
    cap.paragraph_format.space_after = Pt(10)
    if "：" in caption:
        prefix, rest = caption.split("：", 1)
        r = cap.add_run(prefix + "：")
        set_run_font(r, 9, bold=True, color=PINE)
        r = cap.add_run(rest)
        set_run_font(r, 9, color=MUTED)
    else:
        r = cap.add_run(caption)
        set_run_font(r, 9, color=MUTED)
    return p


def parse_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip().strip("`") for c in line.split("|")]


def table_widths(n: int, total: float) -> list[float]:
    if n == 8:
        return [1.15, 1.0, 3.35, 3.05, 3.55, 3.75, 5.35, 5.15]  # 26.35cm, fits landscape 26.7
    weights = {
        2: [1.0, 1.8],
        3: [0.9, 1.4, 1.4],
        4: [0.9, 1.25, 1.25, 1.0],
        5: [0.9, 1.15, 1.25, 0.95, 0.75],
        6: [0.8, 1.2, 1.0, 0.95, 0.8, 0.65],
        7: [0.7, 1.0, 1.1, 1.0, 1.0, 0.9, 0.9],
    }.get(n, [1.0] * n)
    s = sum(weights)
    return [total * w / s for w in weights]


def add_table_caption(doc, text: str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    set_run_font(r, 8.8, bold=True, color=PINE)


def add_table(doc, rows: list[list[str]], landscape=False, section_width=16.6):
    if not rows:
        return None
    ncols = len(rows[0])
    # pad / trim rows
    norm = []
    for row in rows:
        row = row[:ncols] + [""] * max(0, ncols - len(row))
        norm.append(row)
    table = doc.add_table(rows=len(norm), cols=ncols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_width(table, section_width)
    widths = table_widths(ncols, section_width)
    for i, w in enumerate(widths):
        table.columns[i].width = Cm(w)
    set_table_borders(table)
    header_font = 7.9 if landscape else (7.6 if ncols >= 6 else 8.2)
    body_font = 7.7 if landscape else (7.4 if ncols >= 6 else 8.0)
    for r_idx, row in enumerate(norm):
        tr = table.rows[r_idx]
        cant_split(tr)
        if r_idx == 0:
            repeat_header(tr)
        for c_idx, value in enumerate(row):
            cell = tr.cells[c_idx]
            cell.width = Cm(widths[c_idx])
            set_cell_margins(cell, top=45, start=60, bottom=45, end=60)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            # remove bold markers inside table cells
            text = value.replace("**", "")
            r = p.add_run(text)
            if r_idx == 0:
                set_run_font(r, header_font, bold=True, color="FFFFFF")
            else:
                set_run_font(r, body_font, color=INK)
            if r_idx == 0:
                set_cell_shading(cell, FOREST)
            elif r_idx % 2 == 0:
                set_cell_shading(cell, "F7F3EA")
    # small spacer
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(2)
    sp.paragraph_format.line_spacing = 1.0
    return table


def add_toc(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = r' TOC \o "1-2" \h \z \u '
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    txt = OxmlElement("w:t")
    txt.text = "目錄將於開啟文件時自動更新；若未更新，請在目錄上按右鍵→更新功能變數。"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_sep)
    run._r.append(txt)
    run._r.append(fld_end)
    set_run_font(run, 9, color=MUTED)


def extract_headings(body: str):
    out = []
    for line in body.splitlines():
        if line.startswith("# "):
            out.append((1, line[2:].strip()))
        elif line.startswith("## "):
            out.append((2, line[3:].strip()))
    return out


def load_toc_map():
    path = BASE / "assets" / "toc_pages.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def add_manual_toc(doc, headings, page_map):
    # Two-column TOC: split at a major section boundary so no H2 is orphaned.
    split = len(headings) // 2
    for i, (level, text) in enumerate(headings):
        if level == 1 and text.startswith("參、"):
            split = i
            break
    columns = [headings[:split], headings[split:]]

    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_width(table, 16.4)
    remove_table_borders(table)
    for ci, col in enumerate(columns):
        cell = table.rows[0].cells[ci]
        cell.width = Cm(8.2)
        set_cell_margins(cell, top=0, start=0, bottom=0, end=120)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
        # header
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.tab_stops.add_tab_stop(Cm(7.55), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        r = p.add_run("章節")
        set_run_font(r, 8.0, bold=True, color=MUTED)
        r = p.add_run("\t頁次")
        set_run_font(r, 8.0, bold=True, color=MUTED)
        add_bottom_border(p, color=BORDER, sz=4, space=1)

        for level, text in col:
            p = cell.add_paragraph()
            pf = p.paragraph_format
            pf.space_before = Pt(1.6 if level == 1 else 0.1)
            pf.space_after = Pt(0.2)
            pf.line_spacing = 0.95
            pf.left_indent = Cm(0) if level == 1 else Cm(0.32)
            pf.tab_stops.add_tab_stop(Cm(7.55), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
            r = p.add_run(text)
            set_run_font(r, 8.8 if level == 1 else 7.8, bold=(level == 1), color=FOREST if level == 1 else SLATE)
            r = p.add_run("\t")
            page = page_map.get(text)
            r = p.add_run(str(page) if page else "—")
            set_run_font(r, 8.0, bold=(level == 1), color=PINE if level == 1 else MUTED)


def add_cover(doc):
    # top image
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(8)
    p.add_run().add_picture(str(BASE / "assets" / "fig_cover.png"), width=Cm(15.8))

    # eyebrow
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("期末專題提案｜DOMAIN DATA AGENT")
    set_run_font(r, 9, bold=True, color=EMBER)

    # title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("山徑守護者")
    set_run_font(r, 29, bold=True, color=FOREST)
    r = p.add_run("（TrailGuard TW）")
    set_run_font(r, 15.5, bold=True, color=PINE)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("以證據為基礎的臺灣高山行程規劃與風險決策支援代理人")
    set_run_font(r, 14.5, bold=True, color=PINE)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run("An Evidence-Grounded Domain Data Agent for High-Mountain Trip Planning and Risk Decision Support in Taiwan")
    set_run_font(r, 9.2, color=MUTED)

    # rule
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(6)
    add_bottom_border(p, color=EMBER, sz=12, space=2)

    # metadata block
    meta = [
        ("課程", "物聯網應用與資料分析"),
        ("授課教師", "陳煥 教授"),
        ("組員", "陳俊安、廖家暉、温偉成、郭冠良"),
        ("日期", "2026-10-31"),
        ("版本", "v0.1 Proposal"),
    ]
    table = doc.add_table(rows=len(meta), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_width(table, 10.5)
    for i, (k, v) in enumerate(meta):
        row = table.rows[i]
        row.cells[0].width = Cm(3.0)
        row.cells[1].width = Cm(7.5)
        for c in row.cells:
            set_cell_margins(c, 28, 55, 28, 55)
            c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p0 = row.cells[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = p0.add_run(k)
        set_run_font(r, 9.2, bold=True, color=PINE)
        p1 = row.cells[1].paragraphs[0]
        r = p1.add_run(v)
        set_run_font(r, 9.2, color=INK)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("本文件為提案版本。所有系統成效數字均為設計目標或驗收門檻，尚未進行正式實驗。")
    set_run_font(r, 8, color=MUTED)


def add_info_page(doc):
    p = doc.add_paragraph()
    p.paragraph_format.page_break_before = True
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("文件資訊")
    set_run_font(r, 17, bold=True, color=FOREST)
    add_bottom_border(p, color=EMBER, sz=10, space=3)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.4
    add_rich_text(p, "本文件依課程「期末專題提案作業規範」撰寫，包含 Abstract、Introduction、Related Work、Deep Research、Proposed Scheme 與 References。文件設計為可在 Final Handover 階段持續維護：Markdown 為可編輯來源，DOCX 為交付版本，DESIGN.md 則記錄工程實作細節。", 10.2, SLATE)

    rows = [
        ["項目", "內容"],
        ["專題名稱", "山徑守護者（TrailGuard TW）"],
        ["英文名稱", "An Evidence-Grounded Domain Data Agent for High-Mountain Trip Planning and Risk Decision Support in Taiwan"],
        ["課程", "物聯網應用與資料分析"],
        ["授課教師", "陳煥 教授"],
        ["組員", "陳俊安、廖家暉、温偉成、郭冠良"],
        ["文件版本", "v0.1 Proposal（2026-10-31）"],
        ["文件狀態", "提案階段；實驗尚未執行，成效數字均為目標值"],
        ["主要交付", "Proposal_Document.docx／Proposal_Document.md／Proposal_PPT.pptx／DESIGN.md"],
    ]
    add_table(doc, rows, landscape=False, section_width=16.6)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("版本紀錄")
    set_run_font(r, 12, bold=True, color=PINE)
    rows2 = [
        ["版本", "日期", "變更摘要"],
        ["v0.1", "2026-10-31", "初版提案：問題、文獻、深度研究、架構、流程、虛擬碼與評估設計"],
    ]
    add_table(doc, rows2, landscape=False, section_width=16.6)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.line_spacing = 1.35
    add_rich_text(p, "**閱讀建議：** 若時間有限，請先讀「摘要」與「肆、提出方案」的 C–K 節；若要看研究方法，請讀「貳、相關研究」與「肆、N、評估設計」。所有引用編號對應「伍、參考文獻」。", 9.8, SLATE)


def add_toc_page(doc, headings, page_map):
    p = doc.add_paragraph()
    p.paragraph_format.page_break_before = True
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("目錄")
    set_run_font(r, 17, bold=True, color=FOREST)
    add_bottom_border(p, color=EMBER, sz=10, space=3)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("CONTENTS")
    set_run_font(r, 8.5, bold=True, color=GOLD)
    add_manual_toc(doc, headings, page_map)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.line_spacing = 1.25
    add_rich_text(p, "註：頁次為本文件列印版面之頁碼；若在 Word 中重新排版，頁次可能變動。", 8.2, MUTED)


def set_doc_defaults(doc):
    style = doc.styles["Normal"]
    style.font.name = FONT_CN
    style.font.size = Pt(10.5)
    style.font.color.rgb = rgb(INK)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), FONT_CN)
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.line_spacing = 1.45
    # update fields on open
    settings = doc.settings.element
    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    settings.append(update)


def build():
    md = MD_PATH.read_text(encoding="utf-8")
    # Keep only body from the first "# 摘要"
    idx = md.find("# 摘要")
    if idx < 0:
        raise ValueError("Cannot find '# 摘要' in markdown")
    body = md[idx:]
    body = body.replace("<!-- TOC -->", "").strip()

    doc = Document()
    set_doc_defaults(doc)
    sec = doc.sections[0]
    setup_section(sec, landscape=False, first_page=True)
    headings = extract_headings(body)
    page_map = load_toc_map()
    # cover has no header/footer
    add_cover(doc)
    add_info_page(doc)
    add_toc_page(doc, headings, page_map)

    # body starts on a new page via H1 page_break_before
    section = doc.sections[-1]
    add_header(section, 16.6)
    add_page_number_footer(section)

    lines = body.splitlines()
    i = 0
    first_h1 = True  # heading itself handles page break
    in_abstract = False
    pending_caption = None
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped == "<!-- LANDSCAPE -->":
            new_sec = doc.add_section(WD_SECTION_START.NEW_PAGE)
            setup_section(new_sec, landscape=True)
            add_header(new_sec, 26.7)
            add_page_number_footer(new_sec)
            i += 1
            continue

        if stripped == "<!-- PORTRAIT -->":
            new_sec = doc.add_section(WD_SECTION_START.NEW_PAGE)
            setup_section(new_sec, landscape=False)
            add_header(new_sec, 16.6)
            add_page_number_footer(new_sec)
            i += 1
            continue

        if stripped == "<!-- PAGEBREAK -->":
            doc.add_page_break()
            i += 1
            continue

        if stripped.startswith("<!-- TABLE"):
            cap = stripped[len("<!-- TABLE"):]
            if cap.endswith("-->"):
                cap = cap[:-3]
            pending_caption = cap.strip()
            i += 1
            continue

        if stripped.startswith("# "):
            h1 = stripped[2:].strip()
            in_abstract = h1 == "摘要"
            add_heading(doc, h1, 1)
            i += 1
            continue
        if stripped.startswith("## "):
            add_heading(doc, stripped[3:].strip(), 2)
            i += 1
            continue
        if stripped.startswith("### "):
            add_heading(doc, stripped[4:].strip(), 3)
            i += 1
            continue

        if stripped == "---":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(6)
            add_bottom_border(p, color=BORDER, sz=4, space=2)
            i += 1
            continue
        # code fence
        if stripped.startswith("```"):
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i].rstrip("\n"))
                i += 1
            if i < len(lines):
                i += 1
            add_code_block(doc, code_lines)
            continue

        # image
        m = re.match(r"!\[(.*?)\]\((.*?)\)", stripped)
        if m:
            caption, rel = m.group(1), m.group(2)
            img_path = BASE / rel.replace("/", "\\")
            # width: landscape section 17.5cm, portrait 16.2cm
            cur_sec = doc.sections[-1]
            if cur_sec.orientation == WD_ORIENT.LANDSCAPE:
                w = min(18.0, body_width(cur_sec) - 1.0)
            else:
                w = min(16.2, body_width(cur_sec) - 0.4)
            add_image(doc, img_path, caption, w)
            i += 1
            continue

        # table
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:\-|]+\|[\s:\-|]*$", lines[i + 1]):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                if re.match(r"^\s*\|?[\s:\-|]+\|[\s:\-|]*$", lines[i].strip()):
                    i += 1
                    continue
                rows.append(parse_table_row(lines[i]))
                i += 1
            cur_sec = doc.sections[-1]
            landscape = cur_sec.orientation == WD_ORIENT.LANDSCAPE
            width = body_width(cur_sec) - (0.3 if landscape else 0.0)
            if pending_caption:
                add_table_caption(doc, pending_caption)
                pending_caption = None
            add_table(doc, rows, landscape=landscape, section_width=width)
            continue

        # blockquote
        if stripped.startswith(">"):
            qlines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                qlines.append(lines[i].strip()[1:].strip())
                i += 1
            add_callout(doc, qlines)
            continue

        # lists
        if stripped.startswith("- "):
            while i < len(lines) and lines[i].strip().startswith("- "):
                add_bullet(doc, lines[i].strip()[2:].strip(), numbered=False, compact=in_abstract)
                i += 1
            continue

        if re.match(r"^\d+\.\s+", stripped):
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                add_bullet(doc, lines[i].strip(), numbered=True, compact=in_abstract)
                i += 1
            continue

        # paragraph: join continuation lines until blank or block starter
        para_lines = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (not nxt or nxt.startswith("#") or nxt.startswith("|") or nxt.startswith(">")
                    or nxt.startswith("- ") or nxt.startswith("```") or nxt.startswith("![")
                    or nxt == "---" or nxt.startswith("<!--") or re.match(r"^\d+\.\s+", nxt)):
                break
            para_lines.append(nxt)
            i += 1
        text = " ".join(para_lines)
        is_ref = bool(re.match(r"^\[\d+\]", text))
        add_body_paragraph(doc, text, ref=is_ref, compact=in_abstract)

    doc.core_properties.title = "山徑守護者（TrailGuard TW）— 期末專題提案"
    doc.core_properties.author = "陳俊安、廖家暉、温偉成、郭冠良"
    doc.core_properties.subject = "物聯網應用與資料分析｜期末專題 Proposal"
    doc.core_properties.keywords = "登山安全, 風險決策, RAG, 知識圖譜, 領域資料代理人, 臺灣高山"
    doc.core_properties.comments = "v0.1 Proposal, 2026-10-31. 實驗尚未執行，數字為目標值。"

    doc.save(OUT_PATH)
    print(f"saved {OUT_PATH} ({OUT_PATH.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    build()
