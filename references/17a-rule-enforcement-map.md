# 17a · Rule → Machine Check Map（2026-09-v1.0）

> 原则：**HARD 规则如果找不到机器检查位置，就不算真正实现。**  
> Layer 权威：`config/policy.yaml` → `rule_layers`。

| Rule | Layer | Source Field | Validator / Audit | Test |
|------|-------|--------------|-------------------|------|
| truth_gate | HARD | `story.truth_gate` | `hard_gate.truth_gate_pass` | `test_v1_final_cleanup` Case7 / finalize Case01 |
| freshness_gate | HARD | `story.freshness_gate` / time | `hard_gate.freshness_gate_pass` / `check_freshness_dedup.py` | Case7 / freshness audits |
| dedup_gate | HARD | `event_id` / dedup | `hard_gate.dedup_gate_pass` / `dedupe.py` | Case7 |
| evidence_gate | HARD | `evidence_confidence` + critical ids | `hard_gate.evidence_gate_pass` / `verified_score.py` | Case1/3/7 |
| risk_gate | HARD | sources / risk flags | `hard_gate.risk_gate_pass` | Case5/7 |
| publication_critical_claim_ids_presence | HARD | `publication_critical_claim_ids` | `hard_gate.publication_critical_claim_ids_gate_pass` | Case1/2 |
| coverage_map_presence | HARD | gap_scan.coverage | schema / gap audit | finalize Case19 |
| coverage_map_schema_valid | HARD | gap_scan schema | `gap_scan*.schema.json` | finalize Case19 |
| source_level_c_discovery_only | HARD | `source_level_c` policy | `claims.filter_evidence_sources` / `is_c_level_source` | Case5 |
| source_level_d_forbidden | HARD | `sources[].source_level` | `hard_gate` / `score_claim_confidence` | Case5 |
| public_payload_sanitization | HARD | sanitize output | `sanitize_public.py` / `check_public_html.py` | sanitize tests |
| schema_validation | HARD | report / story schema | `schema.py` / `check_json_schemas.py` | schema audits |
| content_hash_validation | HARD | `content_hash` | `report_hash.py` = sha256(canonical(sanitize)) | Case9/10 |
| desk_max_items | HARD | desk quotas | `check_desk_quotas.py` | desk audits |
| min_items_zero | HARD | `publish.min_items_*` | policy + quotas | finalize |
| evidence_confidence_publish_threshold | HARD | `evidence_confidence` | `hard_gate` | Case3/7 |
| importance_publish_threshold | HARD | `news_importance` | `hard_gate.is_publishable` | Case7 |
| freshness_max_age | HARD | event/source time | `hard_gate.freshness_gate_pass` / `check_freshness_dedup.py` | freshness audits |
| fact_lock | HARD | claims ↔ public text | `validate_claim_semantics_in_story` | finalize Case04–07 |
| claim_semantics_in_story | HARD | title/summary/key_facts/why | `claims.validate_claim_semantics_in_story` | finalize |
| no_internal_leak_to_html | HARD | sanitize output | `sanitize_public.py` | sanitize tests |
| publish_gates_all_pass | HARD | site + final | `check_publish_gates.py` | run_all_tests |
| narrative_supporting_claim_ids | HARD | trends.supporting_* | `validate_narrative_trends` | Case8 |
| coverage_gap_resolution | SOFT | gap_scan gaps | quality / retrospective | finalize |
| importance_precheck_warn | SOFT | `importance_precheck` | soft warn only | phase tests |
| quality_metrics_warn | SOFT | metrics JSON | `quality_metrics.py` | Case6 |
| editorial_drift_alert | SOFT | golden deltas | `test_golden_regression.py` | golden |
| source_reliability_ranking | SOFT | reliability JSON | `source_reliability.py` | optional |
| attention_budget_tiering | EDITORIAL | `attention_tier` | none / human | no BLOCK |
| cross_desk_competition | EDITORIAL | selection | none / human | no BLOCK |
| reader_value | EDITORIAL | selection | none / human | no BLOCK |
| narrative_thread_selection | EDITORIAL | trends choice | structural HARD above | Case8 |
| why_it_matters_optional | EDITORIAL | why presence | optional; factual why → claim-bound HARD | finalize |

## content_hash

| Rule | Layer | Path |
|------|-------|------|
| hash(sanitize_public_payload) | HARD | `content_hash = sha256(canonical(sanitize_public_payload(report)))`；无手工白名单权威 |

## Legacy（新 Policy 不出现权威位）

| Key | Status |
|-----|--------|
| `verified_score` | legacy read alias only；evidence_confidence 唯一权威；新输出禁止生成 |
| `candidate_min` / `candidate_max` | legacy input only；权威为 `candidate_target_*` |
| `source_level_c_alone_major` | 已从新 Policy 删除；loader 可读兼容但忽略 |
| `verified_claim_density` | 不用 Density 表示 Ratio；新 metrics 权威输出 `supported_claim_ratio`；可选 `verified_claim_ratio`=verified-only |
| `timezone_offset` / `time_rules.timezone` | 非权威；仅 `timezone: Asia/Shanghai` + derived |

## 诚实性

分享 Skill **不含**完整运行源码时，上表「Validator/Test」列为 **Runtime implementation reference**；规范状态写 `SPEC_DEFINED`，仅在真实仓跑通后标 `RUNTIME_VERIFIED`。ZIP 不虚构 PASS。
