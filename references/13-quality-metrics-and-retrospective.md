# 13 · 质量指标、来源可靠性与 T+1

> 计算：`scripts/pipeline/quality_metrics.py` → `audits/quality/`。  
> 软审计：`audits/check_quality_metrics.py`（超标 WARN，不单独 BLOCK）。  
> 目标常量：`policy.quality_targets`。

## 负向（少犯错 · SOFT）

| 指标 | 目标 |
|------|------|
| 旧闻率 `old_news_rate` | < 3% |
| 后续纠错率 | < 1%（人工/事故库） |
| 重复新闻率 `duplicate_rate` | 接近 0 |
| 低重要度刊登率 | 接近 0（importance < 50） |
| 单源重大新闻比例 | 尽量低 |
| 漏报率 | Gap Scan + 周抽持续下降 |

## 正向（做得好）

| 指标 | 可算性 |
|------|--------|
| Major / Top Story Recall | 有 `audits/fixtures/major_events/DATE.json` 才算；否则 `null` 占位 |
| Primary Source Ratio | ✅ 目标 ≥ 0.4 |
| Independent Sources/Story | ✅ 优先 claim 级均值 ≥ 1.0 |
| Supported Claim Ratio | ✅ ≥ 0.80 |
| Cluster Compression | ✅ |
| Useful Story Ratio | ✅ ≥ 0.8 |
| Editorial Drift | SOFT；相对 golden 子分漂移（默认告警阈值约 ±8） |

历史稿缺字段记 `n/a`，不因归档缺字段 FAIL。

## 来源长期可靠性（Phase4）

`audits/source_reliability.py`：`link_failure_rate` / `correction_rate` / `original_source_ratio` / `source_chain_dup_rate`。  
**HARD：** 绝不能因历史好跳过 Truth / Evidence / Risk。

## T+1 retrospective（Phase3）

```bash
python3 scripts/pipeline/retrospective.py --for-date YYYY-MM-DD
# → audits/retrospective/YYYY-MM-DD.json
```

骨架覆盖漏报/误判/来源失败/评分漂移等提议字段。  
**禁止自动改 `policy.yaml`**；规则变更走明确人工提案。  
Schema：`config/schemas/retrospective.schema.json`。

## golden

- `config/golden/importance_benchmarks.json`  
- `config/golden/regression_fixtures.json`  
- `config/golden/content_hash_vectors.json`  
- 测试：`audits/test_golden_regression.py`、`audits/test_phase1_refactor.py`、`audits/test_phase2_4_refactor.py`


## r2 正式公式

- **Supported Claim Ratio** = (verified + qualified) / all public claims（分母 0 → N/A）
- **Verified Claim Ratio**（若保留）= verified-only / all（不得与 Supported 同值混用）
- **Useful Story** = importance≥门槛 AND evidence≥门槛 AND ¬signal_only
- Coverage HARD：`coverage_map_presence` + `coverage_map_schema_valid`；SOFT：`coverage_gap_resolution`
- 禁止 Agent 主观填写百分比；须可从 final_report 重算


正式六项定义见 `references/13a-quality-metric-definitions.md`。Useful Story 公式须与 Policy 完全一致。
