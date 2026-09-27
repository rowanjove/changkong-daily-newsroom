# 03 · 配额与分栏

> 机器上限权威：`config/policy.yaml` → `desks.*.max_items`。改常量只改 policy。

## 候选池（中书令 · 宽进）

| 板块 | 候选 | Feed |
|------|------|------|
| 中国 | 10–20 | `feeds-china.json` |
| 国际 | 10–20 | `feeds-intl.json` |
| 财经 | 10–20 | `feeds-finance.json` |
| 前沿科技 | 10–20 | `feeds-tech.json` |

合计 aspirational **40–80**。**不是**发布门禁。候选不足优先 Gap Scan 补漏，禁止低价值硬凑。

## 定稿 / 线上（HARD · 仅上限）

| 板块 | 定稿条数 |
|------|----------|
| 中国 | **0–8** |
| 国际 | **0–8** |
| 财经 | **0–6** |
| 前沿科技 | **0–8** |

- **无最低条数。** 宁缺毋滥。
- 栏内可见默认 4–6（中/际/科技 ≈5、财经 ≈4）；其余折叠「更多新闻」；折叠条**仍计入**定稿上限；重大少时可 3–4。
- 审计：`audits/check_desk_quotas.py`（max-only）+ `audits/check_freshness_dedup.py`；deploy 前须 PASS。

## Attention Budget（Phase2/4）

| attention_tier | display_tier | 含义 |
|----------------|--------------|------|
| must_know | lead | 今天必须知道 |
| should_know | primary | 值得知道 |
| optional | more | 有兴趣再看 |

- **无强制数量**；不得因预算凑数（`policy.attention_budget.no_minimum_counts`）。
- 体验参考总量约 12–30（SOFT，非配额）。
- 入选写 `selection_reason`（内部）；拒绝写 `rejection_reason`。

## Narrative / upcoming

- 今日主线 `trends`：**0–4**；每条 `supporting_story_ids >= 2 AND supporting_claim_ids >= 1`；不足隐藏；禁止 filler。
- `upcoming`（今晚 / 未来24h / 未来3天）：最多 3–5；弱/全空隐藏。旧键 `early_watch`/`tomorrow`/`watchlist` 为别名。

## 取源顺序

1. 按该线 `feeds-*.json` 依次拉取。  
2. 连续失败 → 备源；记 state。  
3. 全挂 → 回退检索，仍须 sourcing 硬规则。  
4. 阻塞 → 内阁群 @丞相（正式稿无「交不出 ≥8」要求）。


`trends_soft_min: 0` — 无可信主线则 trends=[] 隐藏，禁止凑数。
