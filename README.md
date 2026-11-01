# 山徑守護者（TrailGuard TW）

**以證據為基礎的臺灣高山行程規劃與風險決策支援代理人**

> An Evidence-Grounded Domain Data Agent for High-Mountain Trip Planning and Risk Decision Support in Taiwan

---

## 1. 專案簡介

臺灣在 2019 年「開放山林」後，高山活動快速成長，但山域事故並沒有隨之下降。內政部統計 2015–2024 年間共發生 3,450 件山域事故，其中迷路 1,263 件（約 37%）；國家公園署亦指出，2023–2025 年高山型國家公園的事故發生率已由 2016–2019 年的 0.04–0.05% 上升至 0.08–0.09%。

問題不在於「有沒有一個登山 App」，而在於**行前決策與風險資訊沒有被有效整合**：入園申請、氣象預報、步程參考、山屋水源、醫療指引、社群路況分散在不同網站與 PDF，新手自組隊必須自行拼湊，才能回答「這條路線適合我們嗎？」「午後雷雨會卡在哪一段？」「幾點前沒到撤退點就該回頭？」。

**TrailGuard TW** 是一個決策支援代理人，而不是聊天機器人。它的主要輸出是可追溯、可驗證、可行動的**行前決策包**：

- 三個候選行程（安全／平衡／進取）
- 逐段風險儀表板
- 撤退點與回頭時間
- 裝備與水源檢查表
- 離線緊急卡
- 每一項數字的**來源與時間戳**

### 核心設計原則

| 原則 | 說明 |
|---|---|
| 分工 | LLM 負責理解、規劃與解釋；Python Analytics Engine 負責計算、驗證與提供證據 |
| 證據鏈 | 所有數值與規則寫入 **Evidence Ledger**：*No source, no number.* |
| 硬性紅旗 | 颱風警報、步道封閉、嚴重高山症症狀 → 直接 NO-GO 或升級人工，不被平均分數抵銷 |
| 知識層 | **時序知識圖譜（Temporal KG）＋ 混合式 RAG**，整合官方規範、步道分級、山屋水源、事故統計、醫學指引與社群回報 |
| 安全優先的評估 | 以 **False-Safe Rate** 為一級指標：寧可誤報不安全，也不可誤報安全 |

---

## 2. 團隊

| 項目 | 內容 |
|---|---|
| 課程 | 物聯網應用與資料分析 |
| 授課教師 | 陳煥 教授 |
| 組員 | 陳俊安、廖家暉、温偉成、郭冠良 |
| 學期 | 2026 秋季（week8 提案） |

---

## 3. 目前狀態

> **提案階段（Proposal v0.1）**：系統設計已完成，**尚未實作、尚未執行實驗**。
> 文件中所有成效數字（CSR、EGR、False-Safe Rate、MAE、SUS 等）皆為**設計目標或驗收門檻**，不是已觀察到的實驗結果。

已完成：

- [x] 提案文件（DOCX／Markdown）
- [x] 提案簡報（35 頁，含講者備註）
- [x] 系統設計與交接文件（`DESIGN.md`）
- [x] 架構圖、流程圖、風險矩陣、甘特圖

待完成（Final Handover）：

- [ ] 知識庫 v1（5–8 條路線）
- [ ] Agent MVP（可跑完一次完整規劃）
- [ ] 120 案例評估與 baselines
- [ ] 使用者測試（SUS、專家訪談）
- [ ] 期末簡報（> 20 頁）與示範影片（> 10 分鐘）

---

## 4. 交付物

| 檔案 | 說明 |
|---|---|
| `Proposal_Document.docx` | 提案文件交付版（41 頁）：Abstract、Introduction、Related Work、Deep Research、Proposed Scheme、References、附錄 |
| `Proposal_Document.md` | 提案文件可編輯來源（DOCX 由 `assets/build_docx.py` 產生） |
| `Proposal_PPT.pptx` | 提案簡報（35 頁、16:9、全頁講者備註） |
| `DESIGN.md` | 系統設計與交接文件：問題 → 需求 → 架構 → 元件 → 資料 → AI/分析 → 領域知識 → 演算法 → 實作 → 執行 → 結果 |
| `assets/fig_*.png` | 文件與簡報共用圖表 |

> `Proposal_Document.pdf`、`Proposal_PPT.pdf` 為版面檢查用的衍生檔，不納入版本控制，可依下方指令重新產生。

---

## 5. 專案結構

```text
.
├─ Proposal_Document.md          # 提案文件來源（Markdown）
├─ Proposal_Document.docx        # 提案文件交付版
├─ Proposal_PPT.pptx             # 提案簡報
├─ DESIGN.md                     # 系統設計與交接文件
├─ README.md
├─ assets/
│  ├─ build_figures.py           # 產生所有圖表
│  ├─ build_docx.py              # Markdown/內容 → DOCX
│  ├─ build_pptx.py              # 內容 → PPTX（原生圖形）
│  ├─ fig_cover.png
│  ├─ fig_architecture.png
│  ├─ fig_flowchart.png
│  ├─ fig_risk_matrix.png
│  ├─ fig_gantt.png
│  ├─ fig_flowchart_crop.png
│  └─ toc_pages.json             # DOCX 目錄頁碼對照
└─ 期末專題提案作業規範.md          # 課程規範（參考）
```

---

## 6. Installation

文件產生流程只需要 Python 與中文字型，不需要 GPU、不需要 API key。

```bash
# Python 3.11+
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install python-docx python-pptx matplotlib pymupdf pillow
```

- 圖表使用 **Microsoft JhengHei**（微軟正黑體）；非 Windows 環境請改 `assets/build_figures.py` 內的字型設定。
- 若要將 DOCX／PPTX 轉為 PDF 檢查版面，需安裝 **LibreOffice**（`soffice`）。

---

## 7. How to Run

```bash
# 1) 產生圖表
python assets/build_figures.py

# 2) 產生 DOCX（41 頁）
python assets/build_docx.py

# 3) 產生 PPTX（35 頁）
python assets/build_pptx.py

# 4) 轉 PDF 檢查版面
soffice --headless --convert-to pdf --outdir . Proposal_Document.docx Proposal_PPT.pptx
```

> LibreOffice 的 `--convert-to` 會在程序結束後才寫入 PDF，批次轉檔時請確認 PDF 的修改時間已更新，再進行畫面檢查。

### 未來的系統指令（尚未實作）

以下介面為 `DESIGN.md` §10.2 的約定，**目前不存在**：

```bash
python scripts/ingest.py --routes data/routes.yaml
python scripts/build_kg.py
uvicorn app.main:app --reload --port 8000
python scripts/evaluate.py --cases data/eval/cases.yaml
```

---

## 8. Demo 腳本（提案版）

提案階段的示範流程以「決策包」為主，對應 `DESIGN.md` §5 的狀態機：

1. **輸入行程簡報**：路線、日期、人數、經驗等級、既往高山症史。
2. **缺槽追問**：缺少的日期或經驗等級會被追問，而不是被猜測。
3. **工具呼叫**：步程估計 → 天氣窗格 → 高山症風險 → 路線風險分解 → 行程最佳化。
4. **產生三個候選**：安全／平衡／進取，並列出各自的風險、登頂機率與時間緩衝。
5. **紅旗檢查**：若命中颱風、封閉或嚴重症狀，直接輸出 NO-GO 並說明理由。
6. **輸出決策包**：逐段儀表板、撤退點與回頭時間、裝備與水源清單、離線緊急卡、Evidence Ledger。

---

## 9. 評估設計（目標值）

| 指標 | 定義 | 目標 |
|---|---|---|
| CSR | Constraint Satisfaction Rate，硬性限制滿足率 | ≥ 85% |
| EGR | Evidence Grounding Rate，數值可追溯比例 | ≥ 95% |
| False-Safe Rate | 實際不安全卻被判為安全的比例 | ≤ 2% |
| Hiking-time MAE | 步程估計平均絕對誤差 | ≤ 20% |
| Expert acceptability | 專家可接受度（5 點量表） | ≥ 4.0 |
| SUS | 系統易用性量表 | ≥ 75 |
| P95 latency | 端到端回應時間 | ≤ 60 秒 |

- 資料集：30 條路線 × 3 種人物設定 = 90 個核心情境，加上 30 個壓力／對抗案例，共 **120 案例**。
- 上述數值為**驗收門檻**，實驗尚未執行。

---

## 10. 文件導覽

`DESIGN.md` 依下列順序撰寫，建議從 §0 讀起：

| 章節 | 內容 |
|---|---|
| §0–§2 | 文件目的、問題定義、需求 |
| §3–§4 | 系統架構、元件職責與工具契約 |
| §5 | 決策流程與狀態機 |
| §6–§7 | 資料來源、時序知識圖譜 schema |
| §8 | 分析模型與最佳化 |
| §9 | 實作規劃、測試策略、里程碑 |
| §10 | How to Run |
| §11 | 評估協定 |
| §12–§14 | 限制、倫理、參考文獻 |
| 附錄 A–C | 工具 JSON 範例、紅旗與天氣門檻、交接檢查清單 |

---

## 11. 授權與致謝

本專案為課程作業，僅供學術使用。資料來源包括內政部、國家公園署、中央氣象署、上河文化與相關學術文獻，使用時請遵循各來源之授權條款。完整引用請見 `Proposal_Document.docx` 的 References 與 `DESIGN.md` 附錄。
