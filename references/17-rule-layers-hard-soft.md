# 17 · HARD / SOFT / EDITORIAL 规则分层

> 机器权威索引：`policy.yaml` → `rule_layers`。任何 HARD Gate 须可追溯到结构字段 + audits/tests。

| 层 | 含义 | 失败后果 |
|----|------|----------|
| **HARD** | 违反则不得发布 / 不得进正式池 | BLOCK deploy 或淘汰出正式栏 |
| **SOFT** | 质量建议 | WARN；不单独 BLOCK |
| **EDITORIAL** | 编辑原则 | 人工/丞相判断；不作机器硬拒绝 |

## HARD（与 Policy / Validator / Tests 对齐）

正式发布阻断（任一 FAIL → BLOCK DEPLOY；与 `policy.yaml` `rule_layers.HARD` 一一对应）：

- `truth_gate`
- `freshness_gate`
- `dedup_gate`
- `evidence_gate`
- `risk_gate`
- `publication_critical_claim_ids_presence`
- `coverage_map_presence`
- `coverage_map_schema_valid`
- `source_level_c_discovery_only`
- `source_level_d_forbidden`
- `public_payload_sanitization`
- `schema_validation`
- `content_hash_validation`
- `desk_max_items`
- `min_items_zero`
- `evidence_confidence_publish_threshold`
- `importance_publish_threshold`
- `freshness_max_age`
- `fact_lock`
- `claim_semantics_in_story`
- `no_internal_leak_to_html`
- `publish_gates_all_pass`
- `narrative_supporting_claim_ids`

## SOFT

- `importance_precheck_warn`
- `quality_metrics_warn`
- `editorial_drift_alert`
- `source_reliability_ranking`
- `coverage_gap_resolution`

## EDITORIAL

- `attention_budget_tiering`
- `cross_desk_competition`
- `reader_value`
- `narrative_thread_selection`
- `why_it_matters_optional`

## 操作纪律

- 改 HARD 阈值 → 只改 `policy.yaml` + 补/跑测试。  
- SOFT 超标不作为单独 BLOCK 理由（除非另有 HARD 触发）。  
- EDITORIAL 失败 → 重写/降/并/删，不发明「机器硬拒绝码」替代编辑判断。  
- **禁止** Policy HARD / 文档 SOFT 或文档 BLOCK / validator 未实现的不一致。

完整 Rule→Validator 映射见 `references/17a-rule-enforcement-map.md`。
