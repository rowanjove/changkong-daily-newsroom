本表为**运行仓**脚本/审计对照。分享 Skill ZIP **不**随包提供这些脚本；读者不应假设解压即可执行。

# 14 · 脚本与审计地图

> 相对 newsroom 根的路径名，供重建对照。本 skill **不含**源码全文。

## 顶层

| 路径 | 用途 |
|------|------|
| `scripts/build_site.py` | 构建静态站 |
| `scripts/validate_site.py` | 站点校验 |
| `scripts/deploy_pages.sh` | 门禁后部署（读环境变量） |
| `scripts/backup_state.py` | 状态备份 |

## `scripts/pipeline/`

| 路径 | 用途 |
|------|------|
| `build_from_json.py` | 自 final JSON 渲染 |
| `md_to_draft.py` | Markdown 回填 Draft |
| `schema.py` | 字段校验 |
| `hard_gate.py` | Hard Gate |
| `normalize.py` | 规范化 |
| `dedupe.py` | 去重 |
| `rank.py` | 排序 |
| `sanitize_public.py` | 公开字段消毒 |
| `render_report.py` | 报告渲染 |
| `report_hash.py` | content_hash / report_hash canonical |
| `policy_loader.py` | 读取 policy.yaml |
| `claims.py` | 原子 claim normalize / 独立源 / narrative 校验 |
| `verified_score.py` | `evidence_confidence`; legacy `verified_score` read alias only; new output forbidden |
| `category_semantics.py` | 财经一级等分类语义 |
| `source_priority.py` | 来源优先级 |
| `semantic_dedup.py` | 语义去重 |
| `title_check.py` | 标题检查 |
| `json_repair.py` | JSON 修复 |
| `quality_metrics.py` | 质量指标计算 |
| `retrospective.py` | T+1 复盘骨架 |
| `merge_desk_state.py` | 串行 merge 共享 events/seen |
| `archive_index.py` | 归档索引 |
| `github_editorial.py` | GitHub/开源编辑辅助 |
| `reclassify_finance.py` | 财经重分类辅助 |
| `gap_scan_checklist.md` | Gap Scan 清单 |

## `audits/`

| 路径 | 用途 |
|------|------|
| `check_desk_quotas.py` | 定稿版面上限（max-only） |
| `check_freshness_dedup.py` | 时效 + 去重 |
| `check_public_html.py` | 公开 HTML 合规 |
| `check_publish_gates.py` | 发布门禁合并入口 |
| `scan_public_copy_regression.py` | 公开文案回归 |
| `check_content_hash.py` | content_hash 软审计 |
| `check_semantic_dedup.py` | 语义去重软审计 |
| `check_quality_metrics.py` | 质量指标软审计 |
| `check_json_schemas.py` | JSON Schema 手写校验 |
| `source_reliability.py` | 来源长期统计（软） |
| `test_phase1_refactor.py` | Phase1 验收 |
| `test_phase2_4_refactor.py` | Phase2–4 验收 |
| `test_golden_regression.py` | golden 回归 |
| `test_pipeline_units.py` | 管道单元 |
| `test_gate_signal.py` | signal / gate |
| `test_sanitize_watchlist.py` | sanitize / watchlist |
| `test_category_semantics.py` | 分类语义 |
| `test_github_editorial.py` | GitHub 编辑辅助 |
| `test_template_finance_p0.py` | 财经模板 |
| `run_all_tests.sh` | 一键回归 |

## 配置与 golden

| 路径 | 用途 |
|------|------|
| `config/policy.yaml` | 机器权威常量（分享包用 `config/policy.example.yaml`） |
| `config/schemas/*.schema.json` | candidate/verified/final/gap/claims/retrospective |
| `config/golden/` | importance / regression / content_hash vectors |
| `config/gap_scan_report.schema.json` | Gap Scan 报告 |
| `config/feeds-*.json` | 四线源列表 |

## 质量与事故目录

| 路径 | 用途 |
|------|------|
| `audits/quality/` | 日质量指标 |
| `audits/retrospective/` | T+1 复盘 |
| `audits/incidents/` | 事故库（勿写入真人点名） |
| `audits/fixtures/` | 测试夹具 / major_events 基准 |

## 推荐一键（尚书令）

```bash
python3 scripts/build_site.py \
  && python3 scripts/validate_site.py \
  && python3 audits/check_public_html.py \
  && python3 audits/check_desk_quotas.py \
  && python3 audits/check_freshness_dedup.py \
  && python3 audits/scan_public_copy_regression.py
# 全部 PASS 后再：
# bash scripts/deploy_pages.sh
```
