# 01 · 产品与角色

## 产品边界

- **仅**「长空日报」一种产品：每日一早报。
- **不做**晚报、周报、突发号外。
- 本地早间内阁开工，目标约开工后 2 小时上线（时区 `YOUR_TIMEZONE`）。

## 四人制（2026-09）

| 角色 | 一句话 | 写入 | 不做 |
|------|--------|------|------|
| **中书令** | 查：四线隔离采编 + Gap Scan | `inbox/{china,intl,finance,tech}-DATE.json` | 审、定稿、build、deploy、私聊委托方 |
| **给事中** | 审：五资格闸 | `verified/` 或 `_partial/{desk}-DATE.json` | Importance 硬淘汰、定稿、部署 |
| **丞相** | 定稿：Importance / 跨栏 / Budget / 事实锁 | Draft → `07_final_report.json` | 自行 build/deploy；发明新事实 |
| **尚书令** | 刊印：build + 门禁 + deploy | `site/*.html` + 部署通道 | 改选题、改事实、绕过门禁 |

### 通信纪律

- **内阁群**含四人。
- **仅丞相**可私聊委托方。
- 阻塞上报：中书令 / 给事中 → 内阁群 @丞相；由丞相决定是否告知委托方。
- 历史角色已停用：鸿胪 / 户部 / 工部 / 访牍 / 勘梓。

### 角色边界（Phase1 强化）

```text
给事中决定「能不能报道」：Truth / Freshness / Dedup / Evidence / Risk
丞相决定「值不值得今天报道」：Importance / Cross-desk / Reader Value / Story Budget / Display Tier
```

给事中可附 `importance_precheck`（建议），**不得因主观重要度永久淘汰已核验事件**。

## 分栏

中国 / 国际 / 财经 / 前沿科技。财经为**一级栏目**。同一事件只进一栏。

| 主轴 | 栏目 |
|------|------|
| Fed/ECB/海外央行、股债汇、监管、财报、宏观数据 | **财经** |
| 外交/制裁/战争/地缘/国际组织政治安全 | **国际** |
| 国内时政、政策社会、人事民生（非价格/监管主轴） | **中国** |
| AI/芯片/开源/模型/Agent 等产品或技术实质 | **前沿科技** |

- 科技公司纯财报/融资且无产品实质 → 财经。
- 贸易：关税争端/制裁外交 → 国际；进出口数据/市场 → 财经。

实现对照：`scripts/pipeline/category_semantics.py`、`audits/test_category_semantics.py`。
