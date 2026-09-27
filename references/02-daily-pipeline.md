# 02 · 每日 JSON 管道

## 唯一正式数据源

```text
inbox/ → verified/ → Draft / Gate / Rank
  → data/YYYY-MM-DD/07_final_report.json   ★
  → site/*.html
```

`reports/daily/*.md` **禁止**作正式渲染输入。

## 典型阶段

| 阶段 | 输入 | 输出 | 角色 |
|------|------|------|------|
| 采编 | feeds | inbox 四文件 | 中书令 |
| 核验 | inbox | verified / partial | 给事中 |
| merge | partial | events/seen（串行） | 工具 / 丞相侧 |
| 定稿 | verified | Draft JSON | 丞相 |
| Schema / Hard Gate / Normalize / Dedup / Rank / Sanitize | Draft | 中间态 | 管道脚本 |
| Final | 中间态 | `07_final_report.json` + `content_hash` | 管道 |
| Build | final | `site/` | 尚书令 |
| Gates | site + final | PASS/FAIL | 尚书令 |
| Deploy | site | `YOUR_SITE` | 尚书令（仅 PASS） |

## Hard Gate（摘要）

正式可刊登（机器）：

```text
publishable =
  truth_gate == PASS
  AND freshness_gate == PASS
  AND dedup_gate == PASS
  AND evidence_gate == PASS
  AND risk_gate == PASS
  AND news_importance ≥ policy.importance.publish_threshold
高 importance + 低 evidence → watchlist，保留高 importance。

对照：`scripts/pipeline/hard_gate.py`、`schema.py`、`sanitize_public.py`、`claims.py`、`policy_loader.py`。

## schema_version

- 缺省无版本视为 **1**；接受 `1`/`1.0`/`2`/`2.0`。
- v2 字段（`evidence_confidence`、原子 claim、`source_role`、coverage map、`attention_tier` 等）渐进 optional。
- JSON Schema 文件：`config/schemas/*.schema.json`；校验：`audits/check_json_schemas.py`（手写必填/类型；可不依赖 jsonschema 库）。

## 禁止

- Markdown 定稿直接当站点数据源
- 跳过 Hard Gate / sanitize 出站
- 并行任务直写共享 state（见 references/12）
