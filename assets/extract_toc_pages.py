from pathlib import Path
import json
import re
import unicodedata

import pymupdf

BASE = Path(r"C:\Users\User\Desktop\文件\週3_物聯網應用與資料分析_陳煥\week8_2026_10_28\報告")
MD = BASE / "Proposal_Document.md"
PDF = BASE / "Proposal_Document.pdf"
OUT = BASE / "assets" / "toc_pages.json"


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\u00ad", "")
    s = re.sub(r"[\s\u200b\u200c\u200d]+", "", s)
    return s


def headings_from_md() -> list[tuple[int, str]]:
    text = MD.read_text(encoding="utf-8")
    idx = text.find("# 摘要")
    text = text[idx:]
    out = []
    for line in text.splitlines():
        if line.startswith("# "):
            out.append((1, line[2:].strip()))
        elif line.startswith("## "):
            out.append((2, line[3:].strip()))
    return out


def main():
    doc = pymupdf.open(PDF)
    pages = [norm(doc[i].get_text("text")) for i in range(doc.page_count)]
    headings = headings_from_md()
    mapping = {}
    missing = []
    for level, h in headings:
        needle = norm(h)
        found = None
        for i in range(3, len(pages)):
            if needle in pages[i]:
                found = i + 1
                break
        if found is None:
            # fallback: first 24 characters, then first 14
            for n in (24, 14, 8):
                short = needle[:n]
                for i in range(3, len(pages)):
                    if short and short in pages[i]:
                        found = i + 1
                        break
                if found:
                    break
        if found is None:
            missing.append(h)
        else:
            mapping[h] = found
    OUT.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    print("mapped", len(mapping), "of", len(headings))
    if missing:
        print("MISSING:")
        for h in missing:
            print(" -", h)
    for h in headings:
        print(f"{mapping.get(h, '??'):>3}  {'  ' if h[0]==2 else ''}{h[1]}")


if __name__ == "__main__":
    main()
