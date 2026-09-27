# 15 · 视觉与公开 HTML 规则

## 报纸感原则

- 报纸风：今日提要、瘦身头条、四栏 +「更多新闻」、sticky 导航、`#finance` / `#story-<id>` 锚点。  
- 铅印/纸墨气质；不大改视觉与四大栏目框架（Phase1–4 明确不做 lead 大改版 HTML）。  
- 刊头默认「长空日报」，可改但须保持报纸感。

## 公开可渲染字段（示例）

`importance`（若公开离散化）、`evidence_status`、`evidence_note`、`key_facts`、`why_it_matters`、`next_watch`、`timeline`、`satellites`、`related_event`、`related_event_label`、`display_tier`、标题、摘要、来源；报告级 `upcoming`、`trends`。

## 禁止泄漏（HARD）

`verified_score`、`evidence_confidence`、内部评分腔、`signal_only`、`formal_pool`、`agent_note`、`selection_reason`、`rejection_reason`、`importance_precheck`、`editor_notes`、编辑部核验指令；旧可信三词「高可信/较高可信/基本可信」。

对照：`sanitize_public.py`、`audits/check_public_html.py`、`scan_public_copy_regression.py`。  
内部审计字段列表：`policy.internal_audit_fields`。

## 视觉锁定

细节常量见运行仓 `config/visual-lock.md`（分享包不复制私有资产文件）。原则：不因归档或管道升级擅自改版日报正文视觉。
