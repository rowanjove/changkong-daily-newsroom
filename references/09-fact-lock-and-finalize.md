# 09 · 事实锁与定稿纪律

## 事实锁（HARD · Phase1 扩展）

给事中 `verified` / `verified_claims`（及已核验事实字段）一经输出即冻结。

丞相**仅可**：改写、压缩、调序、改善标题、统一风格、写「为什么重要」（分析语气，且仅基于 `verified|qualified` claims）。

丞相**不得**：

- 新增数字、背景事实、因果关系  
- 凭记忆或自行搜索直接写入正文  
- 通过 `trends` / `why_it_matters` / `next_watch` 偷渡未核验事实  

需要新事实 → **打回给事中重新核验**。

辅助：`claims.sanitize_why_or_trend_text`、`validate_trends_against_claims`。

## 事实与分析分离

- **核心事实 / key_facts：** 只允许已核验 claims。  
- **为什么重要：** 宜用「可能 / 或将 / 如果持续 / 值得关注 / 尚需观察」；避免无证据的「必然 / 注定 / 彻底改变」。  
- 争议必须保留归因（指控 ≠ 判决）。

## 跨栏目竞争（P1）

先问：**今天全站最重要的新闻是什么？** 再排栏目。

- 允许某线多发、另一线少发（在版面预算内）。  
- 不为栏目平衡强留低价值条。  
- 正式排序主看 `news_importance`；另须 `evidence_confidence` 达标；`interest_relevance` 仅次要加成。

## 定稿产出

1. 过读者视角清单（见 08）。  
2. Attention Budget 分层；写内部 `selection_reason`。  
3. Narrative trends 0–4；正式支持条件见 `references/08-editorial-desk.md` §4 / `policy.narrative`；不足隐藏。  
4. upcoming 弱则隐藏。  
5. 管道产出 `data/YYYY-MM-DD/07_final_report.json` + `content_hash`。  
6. 派尚书令；**自己不 build/deploy**。

## T+1（衔接）

次日可跑 retrospective 骨架（见 13）。**禁止**自动改 policy。


## 语义保持（r2 Fact Lock）

- fact+verified → 可直接陈述
- self_reported → 保留「公司称/官方称/据其公布」
- allegation → 保留「指控/声称/涉嫌」
- estimate → 保留「估计/约/据估算」
- forecast → 保留预测/未来语气
- conflicting → 明确来源冲突
