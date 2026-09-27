# 12 · 并行、幂等与崩溃恢复（Phase2）

> 实现 stub：`scripts/pipeline/merge_desk_state.py`。

## HARD 规则

1. **每线只写本 desk inbox**  
   中书令四线并行时，中国线只写 `inbox/china-…`（或约定前缀），不得写他线。给事中同理：verified 分 desk 或 `_partial/{desk}-DATE.json`。

2. **禁止并行任务直接改共享状态**  
   `database/events.json`、`database/seen.json`、`state/publish_hashes.json` **不得**被并行 desk 直接 write。共享状态由后续**串行 merge/commit**更新。

3. **Stage 可重跑（幂等）**  
   重复跑同一 stage 不得产生重复 `event_id`、重复发布 hash、破坏 state。inbox/verified 按 id upsert。`attach_report_hash` / deploy 对同 content_hash 视为 DUPLICATE_PUBLISH（跳过或 WARN）。

4. **Deploy 幂等**  
   同日相同 `content_hash` → 不重复推送视为成功/noop。失败时保留上一有效 `site/`；不得半发布覆盖。

5. **Crash recovery**  
   每 stage 落盘中间产物。Resume 从最近完整 stage 继续；merge 使用原子写（temp + rename）。不完整 `_partial` 不得直接进 final。

## 推荐时序

```text
[并行] desk×4 中书令 → inbox/{desk}/…
[并行] desk×4 给事中 → verified/_partial/{desk}-DATE.json
[串行] merge_desk_state.py  ← 唯一写 events.json / seen.json
[串行] 丞相定稿 → 07_final_report.json
[串行] 尚书令 build + HARD gates + deploy（幂等）
```

## merge 接口（stub）

```bash
python3 scripts/pipeline/merge_desk_state.py --date YYYY-MM-DD [--dry-run]
```

- 读入各 desk partial verified  
- 串行 upsert `event_id` → `database/events.json`  
- `seen.json` 仅在成功 publish 后更新（或由 deploy 钩子）  
- 原子写：`*.tmp` → fsync → rename

## SOFT

并行度、超时、重试次数为运维建议，不进 HARD gate。无分布式锁（有意避免过度工程）；纪律依赖 Agent 遵守「不直写共享 state」。
