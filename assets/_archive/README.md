# `assets/_archive/`

這裡放的是一次性維護腳本，**已執行完畢，不需要重跑**。保留是為了讓接手的人看得出來當初做了哪些批次修正。

| 腳本 | 用途 |
|---|---|
| `check_chars.py` | 掃描文件中的簡體字與異體字 |
| `check_text.py` | 檢查文字斷行、空白與數字格式 |
| `fix_terms.py` | 批次替換用詞（體／與／並…） |
| `to_traditional.py` | 簡體轉繁體對照替換 |
| `patch_arch.py` / `rewrite_arch.py` | 重建簡報架構圖（後改為原生圖形） |
| `patch_figs.py` / `rewrite_flow.py` | 重建流程圖與裁切版本 |

> 正式流程只用 `build_figures.py`、`build_docx.py`、`build_pptx.py` 與 `extract_toc_pages.py`。
