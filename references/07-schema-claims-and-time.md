# 07 · Schema、四时间与原子 claims

无法确认写 `"unknown"`；URL 不得编造。旧数据无 `schema_version` 视为 **1**。

## P0 必填

四时间 + `event_id`。给事中补充原子 `verified_claims`。

## P1 / Phase1 建议

- `sources[].source_level`（S–D）与 `source_role`
- `news_importance` / `evidence_confidence` / `interest_relevance` 三轴
- 五维子分（**不含** source_confidence）

---

## 候选示例（脱敏）

```json
{
  "id": "example-product-2026-08-29",
  "event_id": "vendor-example-product-launch-2026-08-29",
  "title": "事件标题",
  "category": "前沿科技",
  "schema_version": 2,
  "event_time": "2026-08-29T01:20:00+08:00",
  "first_reported_at": "2026-08-29T01:25:00+08:00",
  "source_published_at": "2026-08-29T01:30:00+08:00",
  "material_update_at": null,
  "summary": "事件事实摘要",
  "entities": ["Example Corp", "Example Product"],
  "sources": [
    {
      "name": "Official Source",
      "url": "https://example.com/announcement",
      "type": "primary",
      "source_level": "S",
      "source_role": "primary_actor",
      "published_at": "2026-08-29T01:30:00+08:00"
    }
  ],
  "news_importance": 72,
  "interest_relevance": 40,
  "evidence_confidence": 55,
  "importance": {
    "scope": 18,
    "consequence": 18,
    "magnitude": 14,
    "duration": 10,
    "novelty": 12
  },
  "signal_only": false,
  "possible_old_news": false,
  "possible_duplicate": false
}
```

时区偏移按 `YOUR_TIMEZONE` 调整。

## 四时间

| 字段 | 含义 |
|------|------|
| `event_time` | 事件真正发生；未知=`unknown`；禁伪 00:00:00 |
| `first_reported_at` | 首次公开报道 |
| `source_published_at` | 当前引用文章发布时间 |
| `material_update_at` | 最近实质新增事实；无则 null |

`published_time` 兼容旧字段，语义同 `source_published_at`，不得冒充 `event_time`。  
细则：`policy.time_rules`。

## 给事中至少补充

`status`（NEW/UPDATE/DUPLICATE/OLD/UNVERIFIED/CORRECTION）、`verified_claims`、四时间核对、`evidence_confidence`、`importance_precheck`（可选）、`news_importance`、`interest_relevance`、五维、`contradiction_search`（争议）、`risk_flags`、`editor_notes`。

进入正式候选池：NEW / UPDATE / CORRECTION。UNVERIFIED 只进 upcoming / watchlist。

## 原子 verified_claims

```json
{
  "claim_id": "c1",
  "text": "该公司称推理性能提升 40%",
  "claim_type": "self_reported",
  "status": "qualified",
  "confidence": 70,
  "sources": [
    {
      "name": "Company Blog",
      "url": "https://example.com/blog",
      "source_level": "S",
      "source_role": "primary_actor"
    }
  ],
  "independent_source_count": 1,
  "contradictions": [],
  "valid_as_of": "2026-09-27T08:00:00+08:00",
  "risk_level": "normal",
  "VENDOR_CLAIM_ONLY": true
}
```

| claim_type | fact / self_reported / estimate / allegation / forecast / analysis |
| status | verified / qualified / conflicting / unverified |

丞相事实锁：**仅** `verified|qualified`。迁移：`claims.normalize_*`。

## 编辑部 / 注意力字段（可选）

`event_cluster_id`、`cluster_role`、`timeline`、`satellites`、`evidence_status`、`evidence_note`、`display_tier`（lead|primary|more）、`attention_tier`（must_know|should_know|optional）、`selection_reason`（内部）、`rejection_reason`、`related_event` / `related_event_label`。

报告级：`upcoming`、`trends`（Narrative）、`content_hash` / `report_hash`。

## 数据库分工

- `database/events.json`：世界上发生过哪些事件  
- `database/seen.json`：已向读者报道过哪些  
- `database/watchlist.json`：未确认信号  
- `database/corrections.json`：更正记录  

不要把 events 与 seen 合并。共享写入须串行 merge（见 12）。


## r2 补充

- `publication_critical_claim_ids`：标题/摘要/关键数字/主因果必需的 claim_id 列表
- `claim.confidence`：**0–100 整数**（输入 0–1 会 ×100）
- Trend：`supporting_claim_ids` 必填（与 `supporting_story_ids` 并列）
- `why_it_matters` 可 `{text, supporting_claim_ids}`
- `content_hash = hash(sanitize_public_payload)`
- timezone 权威仅顶层 `Asia/Shanghai`（由 IANA 推导 offset，无第二权威）


## 语义保持（Fact Lock）

见 `06b` 语义矩阵；机器检查 `validate_claim_semantics_in_story()`。
`verified_score`：legacy read alias only；`evidence_confidence` 唯一权威；新输出禁止生成。
