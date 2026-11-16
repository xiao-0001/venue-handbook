"""頂會投稿速查手冊的建置腳本。

讀取 data/venues/*.json，檢查每一條規定的原文都出現在 sources/ 的官方文件裡，
再用 templates/ 的樣板產生 index.html 與 venues/<id>.html。

用法：python3 build.py
只用 Python 標準函式庫，不需要安裝任何套件。
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "venues"
SOURCES = ROOT / "sources"
OUT = ROOT / "venues"

# 每個會議頁面固定的六個段落，順序就是頁面上的順序
SECTIONS = [
    ("pages", "頁數與格式"),
    ("anonymity", "匿名與預印本"),
    ("appendix", "附錄與補充材料"),
    ("llm", "LLM／生成式 AI 使用規定"),
    ("rebuttal", "Rebuttal 與作者回覆"),
    ("special", "這個會議特有的規定"),
]
NOT_FOUND = "官方文件沒有寫到"
REQUIRED_KEYS = ["id", "name", "full_name", "edition", "order", "summary", "sources", "sections"]


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def fail(errors):
    print("建置失敗，請修正以下問題：")
    for e in errors:
        print("  -", e)
    sys.exit(1)


def load_venues():
    venues, errors = [], []
    source_cache = {}
    for path in sorted(DATA.glob("*.json")):
        v = json.loads(path.read_text(encoding="utf-8"))
        where = path.name
        for key in REQUIRED_KEYS:
            if key not in v:
                errors.append(f"{where}：缺少欄位 {key}")
        if errors:
            continue
        if v["id"] != path.stem:
            errors.append(f"{where}：id「{v['id']}」必須和檔名相同")
        files = {s["file"] for s in v["sources"]}
        for s in v["sources"]:
            if not (SOURCES / s["file"]).exists():
                errors.append(f"{where}：sources/{s['file']} 不存在")
        for key, title in SECTIONS:
            facts = v["sections"].get(key)
            if not facts:
                errors.append(f"{where}：段落 {key}（{title}）至少要有一條")
                continue
            for i, f in enumerate(facts, 1):
                label = f"{where} {key} 第 {i} 條"
                if f["zh"].startswith(NOT_FOUND):
                    continue
                if not f.get("quote") or not f.get("file"):
                    errors.append(f"{label}：必須附上原文 quote 和來源 file")
                    continue
                if f["file"] not in files:
                    errors.append(f"{label}：file「{f['file']}」沒有列在這個會議的 sources")
                    continue
                if f["file"] not in source_cache:
                    source_cache[f["file"]] = norm((SOURCES / f["file"]).read_text(encoding="utf-8"))
                if norm(f["quote"]) not in source_cache[f["file"]]:
                    errors.append(f"{label}：原文在 sources/{f['file']} 裡找不到，可能是抄錯或捏造")
        venues.append(v)
    if errors:
        fail(errors)
    return sorted(venues, key=lambda v: v["order"])


def render_fact(f, sources):
    zh = html.escape(f["zh"])
    if f["zh"].startswith(NOT_FOUND):
        return f'<li class="fact missing">{zh}</li>'
    src = sources[f["file"]]
    return (
        f'<li class="fact">{zh}'
        f'<details><summary>官方原文</summary>'
        f'<blockquote lang="en">{html.escape(norm(f["quote"]))}</blockquote>'
        f'<p class="cite">出處：<a href="{html.escape(src["url"])}">{html.escape(src["title"])}</a>'
        f'（{html.escape(src["captured"])} 擷取）</p></details></li>'
    )


def fill(template, values):
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def build_venue(v, nav):
    sources = {s["file"]: s for s in v["sources"]}
    sections = []
    for key, title in SECTIONS:
        items = "\n".join(render_fact(f, sources) for f in v["sections"][key])
        sections.append(f'<section id="{key}"><h2>{title}</h2><ul class="facts">{items}</ul></section>')
    toc = "".join(f'<a href="#{k}">{t}</a>' for k, t in SECTIONS)
    src_list = "".join(
        f'<li><a href="{html.escape(s["url"])}">{html.escape(s["title"])}</a>（{html.escape(s["captured"])} 擷取，'
        f'<code>sources/{html.escape(s["file"])}</code>）</li>'
        for s in v["sources"]
    )
    page = fill((ROOT / "templates" / "venue.html").read_text(encoding="utf-8"), {
        "name": html.escape(v["name"]),
        "full_name": html.escape(v["full_name"]),
        "edition": html.escape(v["edition"]),
        "summary": html.escape(v["summary"]),
        "toc": toc,
        "sections": "\n".join(sections),
        "sources": src_list,
        "nav": nav,
    })
    (OUT / f"{v['id']}.html").write_text(page, encoding="utf-8")


def build_index(venues, nav):
    cards = "".join(
        f'<a class="card" href="venues/{v["id"]}.html"><h3>{html.escape(v["name"])}</h3>'
        f'<p class="edition">{html.escape(v["edition"])}</p><p>{html.escape(v["summary"])}</p></a>'
        for v in venues
    )
    head = "".join(f'<th scope="col"><a href="venues/{v["id"]}.html">{html.escape(v["name"])}</a></th>' for v in venues)
    rows = ""
    for key, title in SECTIONS[:5]:
        cells = "".join(f'<td>{html.escape(v["sections"][key][0]["zh"])}</td>' for v in venues)
        rows += f'<tr><th scope="row">{title}</th>{cells}</tr>'
    page = fill((ROOT / "templates" / "index.html").read_text(encoding="utf-8"), {
        "cards": cards, "head": head, "rows": rows, "nav": nav, "count": str(len(venues)),
    })
    (ROOT / "index.html").write_text(page, encoding="utf-8")


def main():
    venues = load_venues()
    OUT.mkdir(exist_ok=True)
    nav_venue = "".join(f'<a href="{v["id"]}.html">{html.escape(v["name"])}</a>' for v in venues)
    nav_index = "".join(f'<a href="venues/{v["id"]}.html">{html.escape(v["name"])}</a>' for v in venues)
    for v in venues:
        build_venue(v, nav_venue)
    build_index(venues, nav_index)
    n = sum(len(v["sections"][k]) for v in venues for k, _ in SECTIONS)
    print(f"建置完成：{len(venues)} 個會議、{n} 條規定，所有原文都已對照 sources/ 檢查通過。")


if __name__ == "__main__":
    main()
