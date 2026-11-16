# CLAUDE.md：頂會投稿速查手冊

這份文件是給 AI 助手（Claude Code、Codex 等）看的專案規則。新增或修改任何內容之前，請先讀完。

## 專案目的

把 AI 頂會（ACL/ARR、NeurIPS、ICLR、ICML、CVPR……）的投稿規則整理成繁體中文速查網站，給準備投稿的研究生和大學部學生使用。

這個網站最重要的原則是**正確**，好不好看其次。投稿規則每年都會改，記錯一條（例如頁數上限）就可能被 desk reject。所以：

- 每一條規定都必須來自 `sources/` 裡的官方文件，並附上逐字原文。
- 不可以用 AI 自己的印象或網路上的二手資料補內容。
- 文件裡找不到的，就寫「官方文件沒有寫到」，不要猜。

## 檔案結構

```
venue-handbook/
├── CLAUDE.md              ← 本文件：專案規則
├── AGENTS.md              ← 給其他 AI 工具的入口，內容指向本文件
├── README.md              ← 給人看的專案說明
├── build.py               ← 建置腳本：檢查原文 + 產生 HTML
├── data/venues/<id>.json  ← 每個會議一份資料（唯一需要手動編輯的內容）
├── sources/*.txt          ← 官方文件的純文字擷取版本（原文的依據）
├── templates/             ← 頁面樣板（index.html、venue.html）
├── assets/style.css       ← 全站唯一的樣式表
├── index.html             ← 由 build.py 產生，不要手改
└── venues/<id>.html       ← 由 build.py 產生，不要手改
```

**`index.html` 和 `venues/*.html` 都是產生出來的檔案。** 要改內容，改 `data/venues/<id>.json`；要改版面，改 `templates/` 或 `assets/style.css`。改完一律執行 `python3 build.py`。

## 頁面結構（每個會議頁面都一樣）

每個會議頁面固定有六個段落，順序和名稱寫在 `build.py` 的 `SECTIONS`，不要在個別頁面增減：

| key | 段落標題 | 寫什麼 |
|---|---|---|
| `pages` | 頁數與格式 | 正文頁數上限、哪些不算頁數、camera-ready 加頁 |
| `anonymity` | 匿名與預印本 | 雙盲規定、arXiv／預印本政策 |
| `appendix` | 附錄與補充材料 | 附錄放哪裡、審稿人要不要看 |
| `llm` | LLM／生成式 AI 使用規定 | 能不能用、要不要揭露、prompt injection |
| `rebuttal` | Rebuttal 與作者回覆 | 長度、能不能放新結果、能不能放連結 |
| `special` | 這個會議特有的規定 | 其他會議沒有的重要規定（1～3 條） |

**每個段落的第一條是重點**，首頁的「快速比較」表格會直接取用，所以第一條要寫成最能代表這個段落的一句話。

## 資料格式：`data/venues/<id>.json`

```json
{
  "id": "neurips",
  "name": "NeurIPS",
  "full_name": "Conference on Neural Information Processing Systems",
  "edition": "NeurIPS 2026",
  "order": 2,
  "summary": "一句話介紹這個會議投稿時最需要注意的事。",
  "sources": [
    {
      "file": "neurips2026_handbook.txt",
      "title": "NeurIPS 2026 主會議手冊",
      "url": "https://neurips.cc/Conferences/2026/MainTrackHandbook",
      "captured": "2026/11/02"
    }
  ],
  "sections": {
    "pages": [
      {
        "zh": "正文（含圖表）最多 9 頁；參考文獻、附錄和 checklist 不算頁數。",
        "quote": "The main text of a submitted paper is limited to nine content pages, including all figures and tables.",
        "file": "neurips2026_handbook.txt"
      }
    ],
    "anonymity": [], "appendix": [], "llm": [], "rebuttal": [], "special": []
  }
}
```

欄位規則：

- `id`：小寫英文和連字號，必須和檔名相同，例如 `acl-arr`、`neurips`。它也會成為網址 `venues/<id>.html`。
- `full_name`：照會議官網首頁或 CFP 上的正式全名。經 ARR 投稿的 *ACL 系列會議，在後面加「（經 ACL Rolling Review 投稿）」。
- `order`：首頁和導覽列的排列順序，整數。新增會議時用目前最大值 + 1，排在最後面。
- `edition`：資料對應的年份，例如 `ICLR 2026`。官網還沒公布新年份時，沿用舊版並寫清楚年份。
- `summary`：只能重述這一頁已經寫到的規定，不可以加新資訊。
- `sources`：這個會議用到的每一份官方文件。`file` 必須存在於 `sources/`。
- 每條規定（fact）有三個欄位：
  - `zh`：繁體中文（台灣用語）的一句話。專有名詞保留英文，例如 desk reject、camera-ready、rebuttal。
  - `quote`：從 `sources/<file>` **逐字複製**的英文原文，20～300 字元，空白和換行可以不一樣。
  - `file`：原文所在的檔名，必須列在這個會議的 `sources` 裡。
- 文件裡**完全**找不到某個段落的資訊時，該段落只放一條：`{"zh": "官方文件沒有寫到（YYYY/MM/DD 擷取版本）", "quote": "", "file": ""}`，日期填這個會議 `sources` 的擷取日期。
- 段落裡只找得到**部分**資訊時（例如 rebuttal 只寫了日期，沒寫長度），只列找得到的規定，不要為缺少的細項另外加「沒有寫到」。

## 寫作規則

1. `zh` 只能翻譯或濃縮 `quote` 的意思，**不可以超出原文**。原文說 "should"（應該），不要寫成「必須」；原文說 "may"，不要寫成「一定會」。
2. 數字、日期、頁數要和原文完全一致。
3. 一條規定只講一件事，一句話寫完。
4. 不加 emoji，不用「值得注意的是」「綜上所述」這類套話。
5. 不同會議的規定不可以互相套用。A 會議的文件裡沒寫，就不能拿 B 會議的規定補。
   - 例外的處理方式：如果 A 會議的官方文件寫明「遵守 B 的規定」（例如 EMNLP 寫 "should follow all of the ARR submission requirements"），就把這句原文列成一條規定，讓讀者知道要去看 B 的頁面；**不要**把 B 的規定複製進 A 的頁面，因為兩邊的擷取日期和適用的投稿週期可能不同。

## 新增一個會議（例如 EMNLP）

1. **取得官方文件**：把該會議官網的徵稿說明（CFP）、作者指南存成純文字，放進 `sources/`。
   - 算數的官方文件：CFP、作者指南／作者說明、CFP 直接連結的政策頁（例如論文誠信政策）。
   - 不算數的：部落格文章、公告、新聞、第三方整理的網站。
   - 選最新一屆已公布 CFP 的版本；新一屆的官網還沒上線時，用最近一屆，並把年份寫進 `edition`。
   - 檔名：`<會議小寫><年份>_<文件類型>.txt`，例如 `emnlp2026_cfp.txt`、`emnlp2026_authorguide.txt`。
   - 檔案前兩行固定為：
     ```
     文件：EMNLP_2026_徵稿說明
     來源：https://...（YYYY/MM/DD 擷取）
     ```
   - 刪掉網頁的 cookie 提示、導覽列等雜訊，其餘內容保持原樣，不要改寫。
2. **建立資料檔**：複製 `data/venues/neurips.json` 成 `data/venues/emnlp.json`，改 `id`、`name`、`full_name`、`edition`、`order`、`sources`。
3. **逐段填寫六個段落**：每一條都要在 `sources/` 找到原文，複製到 `quote`。
4. **執行 `python3 build.py`**。它會：
   - 檢查必要欄位、六個段落是否都有內容；
   - 檢查每一條 `quote` 是否真的出現在對應的 `sources/` 檔案裡，找不到就停止並列出是哪一條；
   - 產生 `venues/emnlp.html`，並自動把新會議加進首頁卡片、比較表和導覽列。
5. **在瀏覽器檢查**：`python3 -m http.server`，打開 http://localhost:8000 ，確認新頁面和首頁比較表正常。不能開本機伺服器時，直接用瀏覽器打開 `index.html`，或至少檢查產生的 HTML 裡有新會議的卡片、比較表欄位和導覽連結，並在回報中說明沒有用瀏覽器看過。

不需要改 `index.html`、`templates/` 或 `build.py`。

## 更新到新年份（例如 ICLR 2026 → ICLR 2027）

1. 把新年份的官方文件放進 `sources/`（新檔名，例如 `iclr2027_authorguide.txt`），舊檔案保留。
2. 修改 `data/venues/iclr.json` 的 `edition`、`sources`，逐條重新核對規定，`quote` 改成新文件的原文。
3. 執行 `python3 build.py`。

## 修改樣式

- 所有樣式都在 `assets/style.css`，顏色用 `:root` 裡的 CSS 變數，深色模式在 `prefers-color-scheme: dark` 區塊裡設定一次就好。
- 不使用外部 CSS／JS 框架或 CDN，網站要能直接用 GitHub Pages 打開。
- 版面要在手機寬度正常顯示：比較表放在 `.table-wrap` 裡橫向捲動，其他內容不能超出畫面。

## 完成前的檢查清單

- [ ] `python3 build.py` 顯示「建置完成」，沒有任何錯誤
- [ ] 新內容只改了 `data/`、`sources/`（或明確要求的樣板、樣式）
- [ ] 沒有手動修改 `index.html`、`venues/*.html`
- [ ] 每條 `zh` 都沒有超出 `quote` 的意思
- [ ] 本機打開首頁和新頁面看過一次

## 回報格式

完成後請回報：用了哪些官方網頁、新增或修改了哪些檔案、`python3 build.py` 的最後一行輸出，以及這份 CLAUDE.md 有哪裡不清楚、需要用猜的。不清楚的地方會被拿來修訂本文件。

## 絕對不要做的事

- 不要在沒有 `sources/` 原文的情況下新增規定，也不要為了讓建置通過而修改 `sources/` 的原文。
- 不要關掉或繞過 `build.py` 的原文檢查。
- 不要手動編輯 `index.html` 或 `venues/*.html`。
- 不要引入需要安裝的套件或建置工具，`build.py` 只用 Python 標準函式庫。

## 規則修訂紀錄

- **v1（2026/11/16）**：建立專案，收錄 ACL/ARR、NeurIPS、ICLR、ICML、CVPR。
- **v2（2026/11/16）**：請一個沒看過專案的 AI 只讀本文件新增 EMNLP。它成功完成（6 個會議、132 條規定，`build.py` 通過），但回報了 7 個需要用猜的地方。依此補充：會議文件寫「遵守 ARR 規定」時的處理方式、部分資訊的寫法、「沒有寫到」的日期、哪些網頁算官方文件、`full_name` 和 `order` 怎麼決定、無法開本機伺服器時的檢查方式，以及完成後的回報格式。README 和首頁頁尾也改成不寫死會議數量和日期，新增會議時不用跟著改。
