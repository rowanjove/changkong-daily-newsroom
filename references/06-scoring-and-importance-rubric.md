 > r2: publishable 含 Truth Gate；claim.confidence 与 story evidence 均为 **0–100 整数**；Story evidence=`min(critical claims)`。Evidence Rubric 见本包 `references/06b-evidence-rubric.md`（不依赖 live 外部文件）。

# 06 · 三轴评分与 importance rubric

> 机器权威：`config/policy.yaml`。黄金样例：`config/golden/importance_benchmarks.json`。

## 三轴（HARD）

| 轴 | 字段 | 含义 | 尺度 |
|----|------|------|------|
| 公共新闻价值 | `news_importance` | 事件本身多重要 | 0–100 |
| 证据确定度 | `evidence_confidence` | 当前证据有多确定 | 0–100；`verified_score` 仅 legacy read alias only；`evidence_confidence` 唯一权威；新输出禁止生成 |
| 兴趣相关度 | `interest_relevance` | 对 `YOUR_INTEREST_LIST` 的相关度 | 0–100 |

兴趣高 ≠ 重要；**兴趣分不得把低重要度 filler 救进正式栏。**

### 废弃 / 映射

| 字段 | 状态 |
|------|------|
| `importance.source_confidence` | **不得再计入** news_importance |
| `verified_score` | legacy read alias only；`evidence_confidence` 唯一权威；新输出禁止生成 |
| `evidence_status` | 公开离散标签 |
| `importance_precheck` | 给事中建议；非硬淘汰 |

## news_importance 五维（合计 100）

权重默认（policy）：

| 子分 | 权重 |
|------|-----:|
| scope | 0–25 |
| consequence | 0–25 |
| magnitude | 0–20 |
| duration | 0–15 |
| novelty | 0–15 |

打分：先选区间，再取整；子分旁注一句依据。禁止凭感觉打无依据细分数。

### 锚点摘要

**scope：** 0–4 局部 → 15–19 单国全国 → 23–25 全球系统级。  
**consequence：** 0–4 几乎无后果 → 15–19 重大监管/市场/安全 → 23–25 历史转折（极少）。  
**magnitude：** 0–3 名义变化 → 13–16 行业格局级 → 17–20 极端。  
**duration：** 0–2 一日热点 → 13–15 多年结构。  
**novelty：** 0–2 旧闻翻炒 → 10–12 首次重要类型 → 13–15 范式级首次。

### 禁止

- 用「技术细节多」抬高 scope/magnitude  
- 把 source_confidence / 来源多少计入五维  
- 为凑版面抬分  
- 重要但证据不足时**压低** importance（应保留高分 + 低 evidence → watchlist）

## 等级参考（按 news_importance）

| 分 | 等级 | 处理 |
|----|------|------|
| 90–100 | S | TOP / Breaking |
| 80–89 | A | 栏目靠前 |
| 65–79 | B | 可进栏（证据亦达标） |
| 50–64 | C | 默认不进；可 upcoming |
| <50 | 低 | 给事中不得仅因此永久淘汰；丞相决定 |

默认 `publish_threshold = 65`。

## hard_caps（配置化）

| 类型 | 上限（默认） |
|------|-------------:|
| software_patch_minor | 60 |
| partner_announcement_generic | 60 |
| github_ordinary_pr_release | 55 |
| meeting_no_outcome | 55 |
| corporate_promo_generic | 50 |
| offline_event_ordinary | 45 |

条目可设 `importance_cap_type`；脚本 `apply_importance_hard_caps()` 钳制。

## 角色分工

```text
中书令:   preliminary_score / news_importance 初估
给事中:   evidence_confidence + 资格闸 + 可选 importance_precheck
丞相:     news_importance 终裁、跨栏、Reader Value、Story Budget、Display Tier
```

只有 NEW / UPDATE / CORRECTION 进入丞相正式候选池。  
UNVERIFIED / 证据不足 → upcoming 或 watchlist。
