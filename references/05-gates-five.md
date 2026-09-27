# 05 · 给事中资格五闸（文件名历史称「四闸」）

> 机器常量：`config/policy.yaml`。三轴：`06-scoring-and-importance-rubric.md`。

## 角色边界（HARD）

```text
给事中 HARD：
  Truth → Freshness → Dedup → Evidence Sufficiency → Risk/Eligibility

丞相：
  Importance / Cross-desk / Reader Value / Story Budget / Display Tier
```

给事中可附 `importance_precheck`，**不得因主观重要度永久淘汰已核验事件**。  
`LOW_IMPORTANCE` / `REJECT_LOW_IMPORTANCE` 仅软警告或移交丞相。

任一资格闸 HARD 失败 → 不得进正式可刊登池（可进 watchlist / 待确认）。

```text
publishable =
  truth_gate == PASS
  AND freshness_gate == PASS
  AND dedup_gate == PASS
  AND evidence_gate == PASS
  AND risk_gate == PASS
  AND news_importance >= publish_threshold
```

任一 `truth_gate != PASS` 不得正式刊登。

---

## 1. Truth Gate

事件真实；标题事实有源；数字/人名/职务准确；区分计划/宣布/批准/成交/实施；预测≠事实；厂商自测≠客观事实（→ `self_reported` + `VENDOR_CLAIM_ONLY`）；媒体分析≠官方结论；D 禁入；C = discovery_only（不计 Evidence / 独立源 / 公开源）。

必须做**原子声明核验** → `verified_claims[]`。

高风险数字（人数、金额、%、伤亡、军售、融资、估值、GDP、关税、股价、模型参数、Token、性能提升、排名、裁员比例等）：标题关键数字须有明确证据，否则删数字 / 降表述 / 淘汰。

争议题（战争/外交/法律指控/商业纠纷/安全/重大科技争议）：除 confirmation 外必须 `contradiction_search`；冲突无法消解 → `CONFLICTING_SOURCES`。

## 2. Freshness Gate

四时间：`event_time` / `first_reported_at` / `source_published_at` / `material_update_at`。

硬规则：

1. 旧闻无实质更新，不得作 NEW 进正式池。  
2. 不得把文章发布时间当作事件日。  
3. 超过 policy freshness 窗口须回答「今天新增了什么？」答不出 → `REJECT_OLD_NEWS`。

实质更新：新政策落地、新判决、新制裁、新伤亡、新调查结论、新融资、新监管批准、新谈判结果、新官方回应、新证据、新技术/版本正式上线等。  
不算：媒体重报、专家解读、热搜翻红、二次盘点、无新增事实的专访。

机器：`audits/check_freshness_dedup.py`（读 policy）。辅助：`claims.classify_old_vs_update`。

## 3. Dedup Gate

稳定 `event_id`（主体+动作+对象+大致时间+地点）。历史窗：`policy.dedup.windows_days`（默认 7/14/30）。

- 无足以改变新闻价值的新事实 → `REJECT_DUPLICATE_EVENT`  
- 有 → `FOLLOW_UP` / `is_follow_up=true`，不得伪装全新事件

## 4. Evidence Sufficiency Gate（Phase1）

核心：**当前证据是否足以支撑「已确认/基本确认」式刊登？**

1. `evidence_confidence`（0–100；`verified_score` 仅 legacy read alias）≥ `policy.evidence.publish_threshold`（默认 60）；新稿须 `publication_critical_claim_ids` length≥1  
2. 关键事实 claim 为 `verified|qualified`  
3. 独立源：伪多源不得虚高  
4. 厂商宣称不得 `fact`+`verified`  
5. 高风险数字有证据链  

**高 importance + 低 evidence → watchlist，保留高 importance。**

## 5. Risk / Eligibility Gate

1. D 禁止正式日报  
2. C = discovery_only（不计 Evidence / 独立源 / 公开源）  
3. 严重 `risk_flags` → 淘汰或待确认  
4. `signal_only` / UNVERIFIED → 不得进正式栏

## Importance（移交丞相 · 非给事中硬淘汰）

见 `06`。五条测试由丞相执行：栏目若只能发 5 条仍选它吗？

## 拒绝 / 风险原因枚举

```text
FAKE_OR_UNVERIFIED
OLD_NEWS / REJECT_OLD_NEWS
DUPLICATE_EVENT / REJECT_DUPLICATE_EVENT
INSUFFICIENT_SOURCE / INSUFFICIENT_EVIDENCE
VENDOR_CLAIM_ONLY
UNVERIFIED_NUMBER / REJECT_UNVERIFIED_NUMBER
MISLEADING_TITLE
NO_MATERIAL_UPDATE
CONFLICTING_SOURCES / REJECT_CONFLICTING_SOURCES
SOURCE_LEVEL_D
LOW_IMPORTANCE / REJECT_LOW_IMPORTANCE   # 软：仅建议/丞相侧
```

## 给事中输出要点

`event_id`、`status`、四时间、原子 `verified_claims[]`、`evidence_confidence`（唯一权威；`verified_score` 仅 legacy read alias only；新输出禁止生成）、`news_importance`（可与 `importance_precheck` 并列）、`interest_relevance`、五维子分、`is_follow_up`、`risk_flags`、`editor_notes`、争议条 `contradiction_search`。

规则分层见 `17-rule-layers-hard-soft.md`。


`verified_score`：legacy read alias only；`evidence_confidence` 唯一权威；新输出禁止生成。


Evidence Gate 评分细则见 `references/06b-evidence-rubric.md`。C 级 = discovery_only（与 Policy 一致）。
