# 11 · 归档系统

静态历史索引；无数据库/后端。刊印入口仍为 `scripts/build_site.py` → `pipeline/build_from_json.py`。

## URL（稳定）

| 路径 | 说明 |
|------|------|
| `/archive.html` | 归档首页：最近日报 + 年/月入口 + 日期跳转 + 搜索 |
| `/archive/YYYY/` | 年份页 |
| `/archive/YYYY/MM/` | 月份页：当月全部日报条目（无正文） |
| `/YYYY-MM-DD.html` | 单日日报（**路径不变**，永久有效） |

## 首页行为

- 最近日报：约 **90** 天（`ARCHIVE_RECENT_DAYS`）。  
- 按年浏览：仅年份入口。  
- 按月：最近约 12–18 个月入口；更早进年份页。  
- 日期跳转：原生 select + 少量 JS。  
- 搜索：客户端读轻量索引 JSON，不加载全文。

## 轻量索引 JSON（构建写入 `site/data/`）

- `archive-index.json` — 元年份/月份元索引  
- `archive-YYYY.json` — 该年期次条目（date / weekday / title / summary / topics / url）  
- `archive.json` — 兼容 `{daily:[dates], weekly:[]}`

字段提取确定性，不编造。实现：`scripts/pipeline/archive_index.py`、`templates/archive*.html`、`site/assets/archive-search.js`。

## 兼容

旧链 `/archive.html`、`/YYYY-MM-DD.html` 继续有效。日报正文视觉不因归档升级而改版。
