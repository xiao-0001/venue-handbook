# AGENTS.md

本專案的完整規則寫在 [CLAUDE.md](CLAUDE.md)，所有 AI 助手（Codex、Claude Code、Cursor 等）都請先讀那份文件，再開始修改。

最重要的四件事：

1. 內容只改 `data/venues/<id>.json`；`index.html` 和 `venues/*.html` 是產生出來的，不要手改。
2. 每條規定都要附 `sources/` 裡官方文件的逐字原文（`quote`），不可以用自己的印象補內容。
3. 文件裡找不到的資訊，寫「官方文件沒有寫到（YYYY/MM/DD 擷取版本）」。
4. 改完執行 `python3 build.py`，必須顯示「建置完成」才算完成。
