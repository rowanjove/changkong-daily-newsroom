# 13a · Quality Metric Definitions（2026-09-v1）

> 机器权威阈值：`config/policy.yaml` → `quality_targets`。  
> 本文件定义 **Name / Purpose / Numerator / Denominator / N/A / Window / HARD|SOFT / Machine Source**。  
> T+1 retrospective 只建议，不自动改 Policy。

---

## Supported Claim Ratio

| 项 | 定义 |
|----|------|
| Name | Supported Claim Ratio |
| Purpose | 衡量公开 Claim 中已支持（verified + qualified）占比 |
| Numerator | `status ∈ {verified, qualified}` 的 public claims 数 |
| Denominator | 全部 public claims 数（各刊登 story 的 `verified_claims`） |
| N/A | denominator == 0 |
| Window | 单个 `report.date`（`policy.timezone`=Asia/Shanghai） |
| HARD/SOFT | **SOFT**（目标 `supported_claim_ratio_min`，默认 0.80） |
| Machine Source | `scripts/pipeline/quality_metrics.py` → `supported_claim_ratio` |

验收例：6 verified + 2 qualified + 2 unverified → **0.80**。

**不得**再使用易混淆的 `Verified Claim Density` 指代本 Ratio。  
若仍写 **Verified Claim Ratio**，仅允许定义为 verified-only / all（同例 → **0.60**），不得与 Supported 同值混用。

旧键 `verified_claim_ratio_min`：loader 可读兼容，**非** Policy 权威。

---

## Useful Story Ratio

| 项 | 定义 |
|----|------|
| Name | Useful Story Ratio |
| Purpose | 刊登稿中「重要且证据充分」占比 |
| Useful Story | `published != false` AND `news_importance >= importance.publish_threshold` AND `evidence_confidence >= evidence.publish_threshold` AND `signal_only != true` |
| Numerator | Useful Story 数 |
| Denominator | published stories 数 |
| N/A | denominator == 0；缺 importance 或 evidence 的条目不计入 Useful |
| Window | 单个 report.date |
| HARD/SOFT | **SOFT**（`useful_story_ratio_min`） |
| Machine Source | `quality_metrics.py` → `useful_story_ratio` |

---

## Primary Source Ratio

| 项 | 定义 |
|----|------|
| Name | Primary Source Ratio |
| Purpose | 含有效一手/原始来源的刊登稿占比 |
| Numerator | 至少含 1 个 valid primary/original source 的 published stories |
| Valid primary roles | `primary_actor` / `data_provider` / `regulator` / `court_record`；或 source_level=S / type=official|primary |
| 不算真正 Primary | 纯转载、社区、无 URL 空壳、C discovery_only |
| Denominator | published stories |
| N/A | denominator == 0 |
| Window | 单个 report.date |
| HARD/SOFT | **SOFT** |
| Machine Source | `quality_metrics.py` → `primary_source_ratio` |

---

## Independent Sources / Story

| 项 | 定义 |
|----|------|
| Name | Independent Sources per Story |
| Purpose | 平均每篇独立来源数（伪多源坍缩后） |
| Numerator | Σ(story-level independent source count)；优先 critical claims 的 source chain 去重 |
| Denominator | published stories |
| N/A | denominator == 0 |
| Window | 单个 report.date |
| HARD/SOFT | **SOFT** |
| Machine Source | `quality_metrics.py` + `claims.independent_source_count` |

---

## Cluster Compression Ratio

| 项 | 定义 |
|----|------|
| Name | Cluster Compression Ratio |
| Purpose | 事件簇压缩程度 |
| Formula（选定） | `unique event clusters / published stories`（实现：cluster_count / n_items） |
| N/A | 无 cluster 输入或 n==0 |
| HARD/SOFT | **SOFT**（不作 HARD Gate） |
| Machine Source | `quality_metrics.py` → `cluster_compression_ratio` |

---

## Major Event Recall / Top Story Recall

| 项 | 定义 |
|----|------|
| Name | Major Event Recall / Top Story Recall |
| Purpose | 相对外部基准的召回 |
| Numerator / Denominator | hit(baseline ids ∩ published) / |baseline ids| |
| N/A | 无 `audits/fixtures/major_events/YYYY-MM-DD.json` → **null** |
| HARD/SOFT | **SOFT** |
| Machine Source | `quality_metrics.py`（禁止 Agent 手填「今天没有漏大事」） |

---

## Editorial Drift

| 项 | 定义 |
|----|------|
| Name | Editorial Drift |
| Purpose | Golden Cases 上评分/刊登一致性漂移 |
| 记录 | importance subscore delta；evidence confidence delta；publishability mismatch；classification mismatch |
| 基准 | Golden Cases，**不是**日报之间互比 |
| HARD/SOFT | **SOFT** |
| Machine Source | `audits/test_golden_regression.py` + retrospective |

---

## Old News Rate / Duplicate Rate / Low Importance Rate

本文件是正式质量指标定义的唯一来源；这些指标均为 **SOFT**。
