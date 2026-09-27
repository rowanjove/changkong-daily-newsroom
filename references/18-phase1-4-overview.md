# 18 · Phase1–4 / 1.0 总览（诚实状态表）

> **Skill 1.0 SPEC FROZEN** · `spec_version: 1.0` / `spec_status: frozen` / `runtime_status: not_verified`  
> pipeline_version `2026-09-v1.0` · timezone 权威：`Asia/Shanghai`（offset 运行时推导）。  
> 本分享包提供规范（**SPEC_DEFINED**）；**不得**把 SPEC 写成 RUNTIME PASS / FINAL。  
> 无随包 Runtime 源码 → 包内条目保持 SPEC_DEFINED / NOT_VERIFIED，不以 live ALL_PASS 冒充 ZIP 已验证。

运行仓可能另存历史 refactor notes；**本 Skill 不依赖它们**即可理解角色、数据流、Evidence Rubric、Policy、Schema、Gates、Metrics 与验收 Case。

## 三态说明

| 状态 | 含义 |
|------|------|
| SPEC_DEFINED | 规范与 Policy 已定义 |
| RUNTIME_VERIFIED | 真实运行仓有测试结果支持 |
| NOT_VERIFIED | 分享包内无法自行证明 |

## 验收对照（摘录）

| Case / 主题 | 规范状态 | Runtime 状态 |
|---|---|---|
| 高 importance + 低 evidence → watchlist | SPEC_DEFINED | 需真实仓 `test_v1_finalize` / r2 |
| 厂商宣称 → self_reported + 归因 | SPEC_DEFINED | 需真实仓语义锁测试 |
| Reuters+转载 → independent=1 | SPEC_DEFINED | 需真实仓 claims 测试 |
| 旧闻无新事实不得 NEW | SPEC_DEFINED | 需真实仓 |
| 实质更新可为 UPDATE | SPEC_DEFINED | 需真实仓 |
| trends/why 不得偷渡未核验 | SPEC_DEFINED | 需真实仓 |
| content_hash 内部字段不影响 Hash | SPEC_DEFINED | 需 Hash Vectors A–G |
| 无最低条数 / 不凑数 | SPEC_DEFINED | Policy 可静态核对 |
| C = discovery_only | SPEC_DEFINED | Policy + claims |
| Coverage presence/schema HARD；gap SOFT | SPEC_DEFINED | Policy rule_layers |
| verified_score legacy read alias only；evidence_confidence 唯一权威；新输出禁止生成 | SPEC_DEFINED | 需真实仓 ensure_* |
| timezone Asia/Shanghai | SPEC_DEFINED | Policy 可静态核对 |
| Skill 自洽（含 06b/13a/17a） | SPEC_DEFINED | 包内文件存在即可核对 |
| Case 01–30 全量 | SPEC_DEFINED | RUNTIME_VERIFIED 仅当运行仓输出结果文件 |

仅在真实仓执行测试并有结果文件时，才可将 Runtime 列写为 `RUNTIME_VERIFIED: PASS`。

## 冻结架构提醒

四角色、五资格闸、事实锁、event_id、四时间、Claim→Event→Story→Report 数据模型在 1.0 冻结。后续靠 Golden / T+1 / Rubric 校准迭代，而不是继续堆 Prompt。
