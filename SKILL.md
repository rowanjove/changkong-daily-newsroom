---
name: Changkong Daily Newsroom
description: >-
  Use when building, running, auditing, or adapting a Chinese-language
  multi-agent daily newspaper pipeline (research → verify → finalize →
  static publish) with four roles, five eligibility gates, three-axis
  scoring, atomic claims, policy.yaml single source of truth, Attention
  Budget, Narrative Layer, fact lock, HARD/SOFT/EDITORIAL layers, and
  the 2026-09 Phase1–4 operating system.
---

# 长空日报 / Newsroom 日报系统

> 系统快照：**2026-09 Phase1–4**。本 skill 已脱敏，不含真人名、私有域名、API 密钥、私钥仓、agent 标识符或真实日报正文。  
> 实现对照脚本相对路径自行落地；**不含源码仓库全文**。  
> **机器权威常量：** 运行仓 `config/policy.yaml`（分享包示例见 `config/policy.example.yaml`）。  
> Phase1：三轴、五资格闸、原子 claim、policy 单源。  
> **Skill 1.0 SPEC FROZEN（spec 1.0 frozen / runtime_status=not_verified · 2026-09-v1.0）**：publishable 含 Truth Gate；Evidence=min(critical claims)（Claim 分见 references/06b-evidence-rubric.md）；content_hash=hash(sanitize_public_payload)；C 级 discovery_only；confidence 全 0–100 整数；trends_soft_min=0。Phase2–4：Attention Budget、selection_reason、JSON Schema、content_hash canonical、并行幂等、golden、T+1 retrospective、Narrative Layer、来源可靠性统计（**不**跳过 Truth Gate）、HARD/SOFT/EDITORIAL。

---

## 1. 何时使用

在下列场景触发本 skill：

- **搭建或适配**一套中文多 Agent「早报」流水线（采编 → 核验 → 定稿 → 静态刊印）
- **每日运行**四人制内阁：中书令查、给事中审、丞相定稿、尚书令刊印
- **审计 / 重修**配额、五资格闸、三轴评分、原子 claim、事实锁、公开文案 sanitize、发布门禁
- **落地 Phase1–4 OS**：policy 单源、Attention Budget、Narrative Layer、并行幂等、T+1、golden
- **排查**「凑数上线」「旧闻伪装 NEW」「兴趣分救低重要度」「why/trends 偷渡未核验」「内部编辑痕迹泄漏」类回归

不适用：晚报 / 周报 / 突发号外产品设计；单纯 CMS 后台开发；含密钥的运维凭据管理。

---

## 2. 系统总览

### 2.1 产品

- **仅**一种产品：长空日报（每日一早报）
- 本地早间内阁开工 → 目标本地上午上线（相对时刻见 §3；时区 `YOUR_TIMEZONE`）
- **不做**晚报、周报、突发号外

### 2.2 角色边界（HARD）

| 序 | 角色 | 职责 | 沟通 |
|----|------|------|------|
| 1 | **中书令** | 查：四线**隔离上下文**采编 + Coverage Gap Scan → `inbox/` | 内阁群 |
| 2 | **给事中** | 审：资格五闸（Truth / Freshness / Dedup / Evidence / Risk）→ `verified/`；Importance **移交丞相** | 内阁群 |
| 3 | **丞相** | Importance·跨栏·Reader Value·Story Budget·Display Tier；趋势·观察；**事实锁** | 内阁群；**唯一可私聊委托方** |
| 4 | **尚书令** | 刊印：`build_site.py` + 校验 + 发布门禁 + 部署 | 内阁群 |

```text
中书令  发现 + Coverage Matrix Gap Scan → inbox/
给事中  Truth / Freshness / Dedup / Evidence Sufficiency / Risk·Eligibility
        → verified/（可附 importance_precheck，不因重要度永久淘汰）
丞相    Importance / 跨栏 / Reader Value / Story Budget / Display Tier
        事实锁扩至 why_it_matters / trends（仅 verified|qualified claims）
尚书令  build + 机器门禁 + deploy
```

- 内阁群含四人。历史角色（鸿胪 / 户部 / 工部 / 访牍 / 勘梓）已停用。
- **仅丞相**私聊委托方；其余角色不私聊用户、不自开「绕过门禁」的部署。
- **丞相不得**自行 build / deploy。

### 2.3 数据流（唯一正式源）

```text
inbox/                         ← 中书令候选（四线分文件）
  → verified/                  ← 给事中资格五闸
  → Draft / Schema / Hard Gate / Normalize / Dedup / Rank
  → data/YYYY-MM-DD/07_final_report.json   ★ 正式发布唯一数据源
  → site/*.html                ← 尚书令 build
reports/daily/*.md             仅备份 / 人工查看，禁止作正式渲染输入
```

四栏：**中国 / 国际 / 财经 / 前沿科技**（财经为一级栏目，非附属）。

### 2.4 Phase1 三轴与刊登公式（核心语义）

```text
news_importance       公共新闻价值（scope+consequence+magnitude+duration+novelty；不含 source_confidence）
evidence_confidence   证据确定度 0–100；verified_score 仅 legacy read alias only；evidence_confidence 唯一权威；新输出禁止生成 verified_score
interest_relevance    兴趣相关度（次级；不得救 filler）

publishable =
  truth_gate == PASS
  AND freshness_gate == PASS
  AND dedup_gate == PASS
  AND evidence_gate == PASS
  AND risk_gate == PASS
  AND news_importance >= publish_threshold
```

- 高 importance + 低 evidence → **watchlist / 待确认**，不得人为压低 importance。
- 机器权威常量：`config/policy.yaml`（desk 上限、freshness、门槛、硬上限、attention/narrative/time_rules/content_hash/quality_targets/rule_layers）。
- 给事中可写 `importance_precheck`，**不因主观重要度永久淘汰已核验事件**。
- `verified_claims` 为原子模型（`claim_type` / `status` / `source_role` / `independent_source_count`）；旧 `{claim,sources}` 仍可读。
- why / trends 只能基于 `verified|qualified` claims；厂商宣称 → `self_reported` + `VENDOR_CLAIM_ONLY`。
- Gap Scan 须输出 **coverage map**，不得只勾 `no_major_gap: true`。
- **无最低刊登条数**；宁缺毋滥。

### 2.5 Phase2–4 机器化与体验（摘要）

- **Attention Budget：** `must_know` / `should_know` / `optional` ↔ `lead` / `primary` / `more`；无强制条数；入选写 `selection_reason`（仅内部）。
- **selection_reason** / `rejection_reason`：仅内部审计，sanitize 不进 HTML。
- **今日主线（Narrative Layer / trends）：** 0–4 条；正式支持条件见 `references/08-editorial-desk.md` §4 / `policy.narrative`；不足隐藏，禁止凑数。
- **T+1 retrospective：** `scripts/pipeline/retrospective.py` 次日复盘骨架；**禁止**自动改 policy。
- **并行幂等：** 每线只写本 desk inbox；共享 `events.json` / `seen.json` 串行 merge（`merge_desk_state.py`）；stage / deploy 对同 `content_hash` 幂等。
- **golden：** `config/golden/` + `audits/test_golden_regression.py`（importance / regression / content_hash vectors）。
- **规则分层：** HARD / SOFT / EDITORIAL（见 `references/17` + policy `rule_layers`）。
- **测试入口：** `audits/test_phase1_refactor.py`、`audits/test_phase2_4_refactor.py`、`audits/test_golden_regression.py`、`audits/run_all_tests.sh`。

---

## 3. 一日时间线（相对本地早间）

以 `YOUR_TIMEZONE` 本地时间为准（示例 `Asia/Shanghai`，偏移 `+08:00`）：

| 相对时刻 | 动作 | 角色 |
|----------|------|------|
| 本地早间开工（约 T+0） | 内阁早报调度：确认日期、昨日遗留、四线 Task | 丞相 |
| T+0 → T+60～90min | 四线隔离采编 + 每线 Gap Scan → 四份 inbox | 中书令 |
| 四线齐后 | 资格五闸逐条审核 → verified（可并行 desk partial） | 给事中 |
| 审毕 | 串行 merge 共享 state → 跨栏竞争、事件簇、主栏/更多、trends/upcoming、事实锁定稿 → `07_final_report.json` | 丞相 |
| 定稿后 | `build_site` → validate → 配额/时效/公开文案门禁 | 尚书令 |
| 全部 PASS | 推静态产物 → CDN/Pages → `https://YOUR_SITE/` | 尚书令 |
| 目标上线（约开工后 2h） | 内阁群汇报；仅丞相向委托方摘要 | 丞相 |
| T+1 | retrospective 骨架 + 质量指标（SOFT） | 丞相 / 运维 |

阻塞：任一单线源全挂或候选严重不足 → 中书令内阁群 @丞相；由丞相决定是否告知委托方。

---

## 4. 逐步操作清单（按角色）

### 4.1 中书令（查）

1. 拆成 **四个独立 desk 任务**（中国 / 国际 / 财经 / 前沿科技），**禁止**同一长上下文串跑四线。
2. 每线：按 `config/feeds-*.json` 拉源 → 选题 → 写字段（**四时间 + event_id + source_level + 尽量 source_role**）→ **Coverage Gap Scan** → 落盘 `inbox/{china,intl,finance,tech}-YYYY-MM-DD.json`。
3. 每线候选宽进 **10–20**；不为凑数抬重要度；D 级源不当正式指望。
4. Gap Scan 输出 coverage map（`policy.coverage_keys` 每键 `checked|gap|deferred|n/a`）+ `major_gaps_found`。
5. 四线齐后短报内阁群：「四线已齐，请审」。
6. **不做**：审、定稿、build、deploy、私聊委托方、直写共享 `events.json`/`seen.json`。

### 4.2 给事中（审）

1. 读四份 inbox（或 desk partial），**依次**过五资格闸；任一 HARD 失败 → 不得进正式可刊登池（可进 watchlist）。
2. 输出：`event_id`、`status`、四时间、原子 `verified_claims[]`、`evidence_confidence`（唯一权威；`verified_score` 仅 legacy read alias only；新输出禁止生成）、`news_importance` / `importance_precheck` / `interest_relevance`、`evidence_status` 建议、`risk_flags`、争议条 `contradiction_search`。
3. Importance **不**作硬淘汰闸；低分仅软警告或移交丞相。
4. 核验指令 / TODO **只写** `editor_notes`，禁止进公开字段。
5. 落盘 `verified/YYYY-MM-DD-morning.json` 或 `verified/_partial/{desk}-YYYY-MM-DD.json`。

### 4.3 丞相（定稿）

1. 先问：今天全站最重要的新闻是什么？再排栏目（允许某线多、某线少）。
2. **事实锁**：只改写/压缩/调序/标题/风格/可选 why；**不得**新增数字、背景事实、因果；需要新事实 → 打回给事中。why/trends 仅基于 `verified|qualified` claims。
3. Attention Budget 分层（无强制数量）；事件簇克制；主栏默认 4–6 +「更多新闻」；why/next 严格可选；trends 0–4（正式支持条件见 `references/08-editorial-desk.md` §4 / `policy.narrative`）；upcoming ≤3–5（弱则隐藏）。
4. 写 `selection_reason`（内部）；过读者视角检查清单；跑管道产出 `07_final_report.json`（含 `content_hash`）。
5. 派尚书令刊印；**自己不 build/deploy**；需要时私聊委托方。

### 4.4 尚书令（刊印）

```bash
python3 scripts/build_site.py
python3 scripts/validate_site.py
python3 audits/check_public_html.py
python3 audits/check_desk_quotas.py
python3 audits/check_freshness_dedup.py
# 或：python3 audits/check_publish_gates.py
python3 audits/scan_public_copy_regression.py   # 建议
```

全部 PASS → 经 `scripts/deploy_pages.sh`（或等价）推静态产物到 `YOUR_DEPLOY_CHANNEL` → `https://YOUR_SITE/`。  
任一门禁失败 → **BLOCK**，不得部署。同 `content_hash` 视为幂等 noop。

---

## 5. 硬约束速查

| 约束 | 要点 |
|------|------|
| **宁缺毋滥** | 定稿无最低条数；仅上限：中国/国际 0–8、财经 0–6、前沿科技 0–8 |
| **事实锁** | 丞相不得发明新事实；why/trends 只读 `verified\|qualified` claims |
| **禁编造** | URL / 引语 / 数字 / 职务 / 时间；打不开的链接 = 废条 |
| **证据标签** | 公开只用：`已确认` / `基本确认` / `单源` / `来源冲突` / `待确认`；禁旧「高可信」三词 |
| **四时间** | `event_time` ≠ `source_published_at`；旧闻无实质更新不得作 NEW |
| **三轴分离** | 正式排序主看 `news_importance`；`interest_relevance` 不得救 filler；`evidence_confidence` 独立 |
| **来源等级** | S–D；**D 禁止进正式日报**；C 仅线索；伪多源只算 1；S 级 primary_actor ≠ 客观事实 |
| **公开消毒** | 禁止泄漏 `verified_score`、`signal_only`、`agent_note`、`selection_reason`、编辑部核验指令 |
| **URL 兼容** | 单日 `/YYYY-MM-DD.html` 永久有效；归档三级 URL 见 references/11 |
| **财经一级** | 同一事件只进一栏；科技纯财报无产品实质 → 财经 |
| **门禁失败** | 配额 / 时效去重 / validate / 公开文案任一项 FAIL → 禁止上线 |
| **policy 单源** | 改核心阈值只改 `policy.yaml`，并跑 Phase1/2–4 测试 |
| **不自动改 policy** | T+1 retrospective 只提议，永不自动写回 |

---

## 6. 指向 references/ 与 config/

| 文件 | 内容 |
|------|------|
| `references/01-product-and-roles.md` | 产品边界、四人职责、通信纪律 |
| `references/02-daily-pipeline.md` | JSON 管道、Hard Gate、中间态 |
| `references/03-quotas-and-desks.md` | 候选宽进 / 定稿上限 / Attention Budget / 分栏 |
| `references/04-sourcing-and-source-levels.md` | 信源硬规则、S–D、source_role、VENDOR_CLAIM |
| `references/05-gates-five.md` | 五资格闸全文级操作说明 |
| `references/06-scoring-and-importance-rubric.md` | 三轴 + 五维锚点 rubric + hard_caps |
| `references/07-schema-claims-and-time.md` | 字段、四时间、原子 claims、schema_version |
| `references/08-editorial-desk.md` | 事件簇、更多新闻、why/next、Narrative、upcoming |
| `references/09-fact-lock-and-finalize.md` | 事实锁、跨栏竞争、定稿纪律 |
| `references/10-build-publish-gates.md` | build / validate / 部署概念 / content_hash |
| `references/11-archive-system.md` | 三级 URL、90 天、轻量 JSON |
| `references/12-concurrency-and-idempotency.md` | 并行 desk、串行 merge、幂等 deploy |
| `references/13-quality-metrics-and-retrospective.md` | 质量指标、来源可靠性、T+1 |
| `references/14-scripts-and-audits-map.md` | 脚本与审计相对路径地图 |
| `references/15-visual-and-html-rules.md` | 报纸感原则、公开字段、sanitize |
| `references/16-ops-checklist.md` | 日常运维与回归检查清单 |
| `references/17-rule-layers-hard-soft.md` | HARD / SOFT / EDITORIAL 分层 |
| `references/18-phase1-4-overview.md` | Phase1–4 验收对照与向后兼容 |
| `config/policy.example.yaml` | 脱敏机器常量模板 |

---

## 7. 适配新站点时的占位符清单

| 占位符 | 说明 |
|--------|------|
| `https://YOUR_SITE/` | 公开站点根；单日页与归档均挂此根下 |
| `YOUR_TIMEZONE` | 本地时区与 ISO 偏移（例 `Asia/Shanghai` / `+08:00`） |
| `YOUR_DEPLOY_CHANNEL` | 本地门禁 PASS → push 静态产物 → CDN/Pages |
| `YOUR_STATIC_REPO` | （可选）仅静态 HTML/CSS/JS 的发布仓 |
| `YOUR_CDN_PROJECT` | CDN / Pages 项目名（凭据只进环境变量） |
| `YOUR_INTEREST_LIST` | 兴趣轴加权配置；**不得压过** `news_importance` |
| `config/feeds-*.json` | 四线 RSS/Atom/栏目页列表 |
| 刊头文案 | 默认「长空日报」；可改但须保持报纸感 |

**密钥红线：** 任何 API 密钥、云账号标识、私钥材料、hosts 机密 **只**放环境变量或密钥库，**永不**写入 skill、仓库明文或 HTML。

---

## 8. 实现边界（明确）

- 本 skill **不含**源码仓库全文、真实日报内容、私有 PRD 全文。
- 落地时对照 `references/14` 中的脚本名自行实现或从已有仓拷贝**脱敏后**代码。
- 质量指标目标见 `references/13` / `16`；事故库只保留 schema / 示例，不点名真人。

---

## 快速拒绝清单（Do not）

- 为凑满旧制「每栏 8–12 / 合计 32–48」填充低价值项  
- 门禁 FAIL 仍部署  
- 跳过财经一级栏或把财经当国际/中国附属  
- 公开 HTML 泄漏内部字段或旧可信三词  
- 用兴趣分把低 `news_importance` filler 救进正式栏  
- 把 Markdown 定稿直接当站点数据源  
- 在 skill 或静态仓写入真实凭据  
- 因来源历史表现好跳过 Truth Gate  
- 自动脚本改写 `policy.yaml`  
- why / trends 偷渡未核验数字或因果

### publication_critical_claim_ids（1.0 Final Cleanup）

- 新稿正式刊登：`publication_critical_claim_ids` 必须存在且 length≥1，否则 **HARD BLOCK**。
- **不得**用标题/摘要启发式猜 critical 并自动补齐。
- 唯一例外：历史旧数据读取可 heuristic，但必须设 `legacy_evidence_inferred=true`，且不得用于新稿正式发布。
- Runtime implementation reference：`verified_score.py` / `hard_gate.py`。

