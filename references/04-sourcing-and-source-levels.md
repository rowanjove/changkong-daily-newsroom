# 04 · 信源、S–D 与 source_role

## 硬规则

1. **禁止编造** URL、引语、数字、职务、时间；打不开 = 废条。
2. 每条 ≥1 可点一手/权威源；硬新闻优先 ≥2 独立源。
3. 展开编辑分析：关键事实 + 来源名+URL 必填；why/next 严格可选。
4. 二级转载标「据某某」；无法核验 → 待确认，不得进要闻/正式 TOP。
5. 公开证据标签：`已确认` / `基本确认` / `单源` / `来源冲突` / `待确认`；禁旧「高可信」三词。
6. 去 AI 味：短句、主体+动词+数字；禁空话套话。
7. 文章发布时间 ≠ 事件发生时间。
8. 伪多源：多家转载同一原文只算 1；追溯 `original_source` / `source_chain`。
9. **D 禁止正式日报**；C=`discovery_only: true`（policy 选定）。
10. 高风险数字须有证据；争议题强制 `contradiction_search`。
11. 内部核验指令只进 `editor_notes`。

## 来源等级 S–D

| 级 | 含义 | 用途 |
|----|------|------|
| **S** | 直接原始（官网/公告/法院/论文/央行原文等） | 首选 |
| **A** | 高质量主流媒体（Reuters/AP/AFP/新华社/Bloomberg/FT/BBC/财新等） | 硬新闻骨干 |
| **B** | 其他可靠媒体 | 辅助；不得作为正式 Evidence（若为 C）；B 级辅助须谨慎 |
| **C** | 社区/论坛/自媒体/聚合 | **discovery_only**：仅作 Discovery Lead，**不计入正式 Evidence 或 independent_source_count**，不得作为公开 Sources 支撑 |
| **D** | 未知或无法追溯 | **禁止正式日报** |

## source_role（与 S–D 正交 · Phase1）

| role | 含义 |
|------|------|
| primary_actor | 当事方 |
| regulator | 监管 |
| court_record | 法院/裁判文书 |
| data_provider | 数据发布方 |
| independent_observer | 独立观察（通讯社/调查） |
| expert_analysis | 专家分析 |
| community_signal | 社区信号 |

**S 级 primary_actor ≠ 客观事实已证实。** 厂商性能宣称 → `claim_type=self_reported`，`status` 至多 `qualified`，公开须归因（「该公司称…」），并标 `VENDOR_CLAIM_ONLY`。

## Claim 级独立源

- Reuters 原文 + N 家转载 → `independent_source_count = 1`
- 公司新闻稿被多家照抄 → 1
- **每个 claim 单独计数**，不只在 story 级

对照：`scripts/pipeline/claims.py`、`source_priority.py`。

## 来源长期可靠性（Phase4 · SOFT）

`audits/source_reliability.py` → `audits/quality/source_reliability.json`。  
指标可助排序与核验成本分配，**绝不能**因历史表现好跳过 Truth / Evidence / Risk。D 级仍禁入。
