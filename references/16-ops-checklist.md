# 16 · 运维与日常检查清单

## A. 每日开工（丞相）

- [ ] 确认本地日期与 `YOUR_TIMEZONE`
- [ ] 确认昨日遗留 / 更正（`corrections`）
- [ ] 派中书令四线隔离 Task
- [ ] 阻塞通道畅通（内阁群）

## B. 中书令收工

- [ ] 四文件 inbox 已落盘，条数各约 10–20
- [ ] 每线完成 Coverage Gap Scan（coverage map + major_gaps_found）
- [ ] 四时间 + event_id + source_level（+ source_role）尽量齐全
- [ ] 未直写共享 events/seen
- [ ] 内阁群通知「四线已齐」

## C. 给事中收工

- [ ] 五资格闸逐条；拒绝原因在枚举内
- [ ] 原子 `verified_claims` 完整；争议条有 contradiction_search
- [ ] `evidence_confidence` 已填；Importance 不作硬淘汰
- [ ] 公开建议 `evidence_status`；内部备注只在 editor_notes
- [ ] verified / partial 落盘

## D. 丞相定稿

- [ ] 串行 merge 已完成（若使用 partial）
- [ ] 跨栏竞争；宁缺毋滥
- [ ] 事实锁未破（why/trends 无偷渡）
- [ ] Attention / 事件簇 / 主栏 / 更多 / Narrative / upcoming
- [ ] 读者视角清单全过；`selection_reason` 仅内部
- [ ] `07_final_report.json` + content_hash
- [ ] 派尚书令（自己不 deploy）

## E. 尚书令上线

- [ ] build / validate / public_html / desk_quotas / freshness_dedup
- [ ] （建议）scan_public_copy_regression
- [ ] 全部 PASS → deploy → 抽查 `https://YOUR_SITE/` 与 `/YYYY-MM-DD.html`
- [ ] 同 hash 幂等；归档索引更新

## F. T+1 / 质量（SOFT）

- [ ] `retrospective.py --for-date`（不自动改 policy）
- [ ] `quality_metrics.py`；超标仅 WARN
- [ ] （可选）`source_reliability.py`

## G. 回归红线（发现即停发）

1. 门禁 FAIL 仍上线  
2. 公开页出现内部编辑短语或旧「高可信」三词  
3. 兴趣分救低重要度 filler  
4. 旧闻伪装 NEW / 无实质更新重发  
5. D 级源进正式栏  
6. 丞相发明新数字/因果；why/trends 偷渡  
7. 静态仓或 skill 中出现真实 API 密钥 / 私有域名 / 私钥材料  
8. 因来源历史好跳过 Truth Gate  
9. 自动脚本改写 policy.yaml  

## H. 适配新站点最小步骤

1. 复制本 skill → 替换占位符。  
2. 复制 `config/policy.example.yaml` → 运行仓 `policy.yaml`，改时区。  
3. 准备四线 feeds 与空目录：`inbox/`、`verified/`、`data/`、`site/`、`database/`。  
4. 落地 14 中核心脚本。  
5. 先跑通样例 JSON → HTML → 门禁，再接 Agent。  
6. 凭据只进环境变量；分享包保持脱敏。
