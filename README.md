# 頂會投稿速查手冊

整理 AI 頂會（ACL/ARR、NeurIPS、ICLR、ICML、CVPR）投稿規則的繁體中文速查網站：頁數、匿名、附錄、LLM 使用規定、rebuttal，以及各會議特有的規定。

每一條規定都附官方原文和出處，由 `build.py` 自動檢查原文確實出現在 `sources/` 的官方文件裡。

## 本機預覽

```bash
python3 build.py          # 檢查資料並產生 HTML
python3 -m http.server    # 打開 http://localhost:8000
```

不需要安裝任何套件。

## 新增或修改內容

請看 [CLAUDE.md](CLAUDE.md)。簡單來說：

1. 官方文件存成純文字放進 `sources/`
2. 在 `data/venues/` 新增或修改 `<id>.json`，每條規定附逐字原文
3. 執行 `python3 build.py`

## 免責聲明

資料擷取自各會議官網（2026/11/02），規定可能隨時更新，投稿前請以官網最新公告為準。
