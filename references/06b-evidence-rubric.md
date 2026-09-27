# Evidence Rubric（Claim → Story · 2026-09-v1.0 · 确定化 · 禁模糊区间）

> **机器权威：** [`policy.yaml`](../config/policy.yaml) → `evidence`。  
> **Skill 自洽副本：** `references/06b-evidence-rubric.md`（须与本文件语义一致）。  
> **实现：** `scripts/pipeline/claims.py`（`score_claim_confidence` / `validate_claim_semantics_in_story`）、`scripts/pipeline/verified_score.py`。  
> **量纲：** 全系统 confidence 统一为 **0–100 整数**（禁止与 0–1 混用同名）。

---

## 1. Story Evidence（派生规则 · HARD）

```text
Story.evidence_confidence =
  min(confidence of claims in publication_critical_claim_ids)
```

`policy.evidence.critical_claims_aggregation: min`（冻结）。  
可选 `weighted_min`：对 critical claim 乘 `evidence_weight∈(0,1]` 后再取 min（默认权重 1）。**算法须在 Policy 唯一给出，不得由 Agent 自行理解。**

**禁止**用全部 Claim 的简单平均值抬高标题核心弱 Claim。

### publication_critical_claim_ids（新稿 HARD）

Story **必须**标记哪些 Claim 是下列成立所必需（`length >= 1`）：

- 标题核心结论
- 摘要核心结论
- 关键数字
- 主要因果判断
- 任何会显著改变读者理解的 Claim

```text
新稿 / 正式刊登：
  publication_critical_claim_ids 缺失或 [] → HARD BLOCK
  不得用标题/摘要启发式猜 critical 并自动补齐
  不得回退 structural heuristic 填 evidence_confidence

历史旧数据读取（归档/迁移 ONLY）：
  允许 structural heuristic，但必须设 legacy_evidence_inferred = true
  带该标记的稿件不得当作新正式稿发布
```

`policy.evidence.require_publication_critical_claim_ids: true`

---

## 2. Claim Confidence 基础档位（人类解释 vs 机器固定 base）

> **机器权威：** `policy.evidence.base_scores`（整数，禁止从区间任选）。  
> 人类可用「95–100」等区间**解释**该档含义，但必须写明 **Machine base = 表中固定值**。

| 人类解释档 | class（机器） | Machine base | 典型条件（解释用） |
|------------|---------------|--------------|-------------------|
| 95–100 | `direct_strong` | **95** | 法院判决原文；监管正式公告；官方统计库；「已发布」且官方页证明发布行为；多高质量独立原始来源一致无冲突 |
| 85–94 | `highly_confirmed` | **85** | 一高质量一级来源 + 真正独立高质量确认；多家可靠媒体独立一致；原始数据 + 独立媒体解释 |
| 75–84 | `reliable_limited` | **75** | 高质量单源直接报道无显著冲突；多家实质依赖同一原始来源；原文明确但上下文不全 |
| 60–74 | `qualified_supported` | **60** | `self_reported`；估计缺完整原始数据；单源发展中；数字/范围不确定。通常 `qualified`，公开须归因 |
| 40–59 | `weak_signal` | **40** | 匿名单源；高风险低独立；明显冲突；数字无法确认。通常 watchlist / unverified / conflicting |
| 0–39 | `unsupported` | **0** | 社区传言；无法追溯；聚合二手；**D 级**。不得进正式 Evidence |

注意：`primary_actor` 只能证明自身行为或「作出了某项声明」，不能自动证明声明内容客观真实。

### §4 分类 IF 链（deterministic · first match）

```text
硬排除: D 级 OR 仅 C/空源 → unsupported
冲突且不足以双确认 → weak_signal
ELIF verified fact + 原文(S/regulator/court/data) + (ind≥2 OR strong_role) → direct_strong
ELIF ind≥2 + verified|qualified + 无冲突 → highly_confirmed
ELIF ind≥1 + verified fact + 无冲突 → reliable_limited
ELIF self_reported|estimate|forecast|allegation|qualified → qualified_supported
ELIF unverified|conflicting → weak_signal
ELSE → unsupported
```

`policy.evidence.classification_priority` 与实现对齐。算法：**classify → fixed base → fixed modifiers → caps → clamp(floor,ceiling)**。

---

## 3. Confidence 调整因子（Policy 固定值 · 可机器验收）

不得任意加减分。**禁止** `+5～+10` / `-10～-30` / 酌情 / 视情况 等模糊区间。机器只读 `policy.evidence.modifiers` / `caps`：

| 调整项 | Policy key | 确定值 | 机器标记 |
|--------|------------|--------|----------|
| 真正独立的第二高质量来源（只 + 一次） | `independent_second_high_quality_source` | **+8** | `independent_second_high_quality_source:+8` |
| 直接原始文件 / 官方原始记录 / S 级原文 | `direct_original_record` | **+5** | `direct_original_record:+5` |
| 引用链同一 Reuters/AP/官方稿 | （独立源去重） | **+0** | source_chain 去重；伪多源不加分 |
| 弱冲突 | `conflict_weak` | **−10** | `source_conflict_weak:-10` |
| 中等冲突（缺省） | `conflict_medium` | **−20** | `source_conflict_medium:-20` |
| 强冲突 | `conflict_strong` | **−30** | `source_conflict_strong:-30` |

**no_double_counting：** 若 class=`direct_strong` 因原文成立，**不再** `+direct_original_record`（见 `policy.evidence.no_double_counting`）。

### Caps（硬上限 · Policy）

| 条件 | Policy key | Cap | 机器标记 |
|------|------------|-----|----------|
| 高风险数字仅单可靠源 | `high_risk_single_source` | **74** | `high_risk_single_source_cap:74` |
| 厂商自报 Benchmark 作客观性能（无独立验证） | `vendor_benchmark_objective_unverified` | **59** | `vendor_benchmark_objective_cap:59` |
| 厂商 Benchmark 作归因「厂商称」 | `vendor_attributed_claim` | **90** | `vendor_attributed_cap:90` |
| 社区 / C 级 | — | **不计 Evidence** | discovery_only；`filter_evidence_sources` |
| D 级 | — | **禁** | HARD → unsupported/0 |

冲突强度：`conflict_strength` ∈ {`weak`,`medium`,`strong`}（同义 `low`/`high`）。缺省 = medium。

**deterministic：** 同一 Claim 输入 → 同一 class / base / adjustments / confidence。

---

## 4. Claim Status 与分数不是同义

| 组合 | 含义 |
|------|------|
| `fact + verified` + 高分 | 可直接陈述 |
| `self_reported` + confidence 90 | 仍可为 `status=qualified`：高度确定「公司确实这样说」，不代表内容被独立证明 |
| `allegation` | 须保留指控语气，不得写成定罪 |
| `estimate` / `forecast` | 须保留不确定 / 未来语气 |
| `conflicting` | 须公开来源冲突，不得挑一方当已确认事实 |
| `unverified` | 不得进入正式事实正文 |

---

## 5. 语义保持矩阵（Fact Lock · HARD）

| claim_type / status | 允许公开方式 |
|---------------------|--------------|
| `fact + verified` | 可直接陈述 |
| `self_reported` | 必须保留「公司称 / 官方称 / 据其公布」等归因 |
| `allegation` | 必须保留「指控 / 声称 / 涉嫌」，不得写成定罪事实 |
| `estimate` | 必须保留「估计 / 约 / 据估算」等不确定性 |
| `forecast` | 必须保留未来/预测语气 |
| `conflicting` | 必须明确存在来源冲突 |
| `unverified` | 不得进入正式事实正文 |

机器检查：`validate_claim_semantics_in_story()`。  
标题 / 摘要 / key_facts 丢归因/时态/不确定/争议 → **BLOCK**。  
`why_it_matters` 出现则至少重写后才能发布；含数字/因果/背景须 `supporting_claim_ids`。

---

## 6. 可解释性

`ensure_evidence_confidence` 附加 `_evidence_explanation`：

- aggregation
- publication_critical_claim_ids
- 各 critical claim 的 confidence / type / status / text
- evidence_from_critical_min
- missing_critical_ids / legacy_evidence_inferred

同一 Golden Case 多次运行，在输入 Claim 不变时应得到相同 min 分。

---

## 7. 与门禁

```text
publication_critical_claim_ids_presence PASS  ⇔  ids 存在且 length>=1
                                               且 NOT legacy_evidence_inferred
evidence_gate PASS  ⇔  上式 PASS
                    AND evidence_confidence ≥ policy.evidence.publish_threshold
publishable 另须 truth/freshness/dedup/risk + importance（见 gates）
高 importance + 低 evidence → watchlist；不得人为压低 news_importance
```
