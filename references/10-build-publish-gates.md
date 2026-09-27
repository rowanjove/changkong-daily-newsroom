# 10 · 刊印与发布门禁

## 角色

尚书令执行 build + 校验 + 门禁 + 部署。丞相不得自行 build/deploy。  
凭据只从环境变量读取，永不写入仓库或 skill。

## Deploy 前必须全部 PASS

```bash
python3 scripts/build_site.py
python3 scripts/validate_site.py
python3 audits/check_public_html.py
python3 audits/check_desk_quotas.py
python3 audits/check_freshness_dedup.py
# 便捷合并：
python3 audits/check_publish_gates.py
# 建议：
python3 audits/scan_public_copy_regression.py
```

任一门禁失败 → **BLOCK**，不得部署。

## 部署概念（脱敏）

```text
门禁全部 PASS
  → scripts/deploy_pages.sh（或等价）
  → 同步 site/ → YOUR_STATIC_REPO / 静态产物目录
  → YOUR_DEPLOY_CHANNEL（git push / CDN CLI / Pages）
  → https://YOUR_SITE/
```

- 私密静态仓仅含静态产物；勿手改仓内 HTML。  
- Secrets：`YOUR_CDN_TOKEN` / `YOUR_CDN_ACCOUNT` / `YOUR_CDN_PROJECT` 等只进环境变量与托管 secrets。  
- 同日相同 `content_hash` → 幂等 noop（见 12）。

## content_hash / report_hash（Phase2 canonical）

r2：`content_hash = SHA-256(canonical_json(sanitize_public_payload(report)))`；规则见 `policy.content_hash` 与 `report_hash.py`（不再以人工字段白名单为主路径）。

应含：

- `report_hash`（历史字段名）  
- `content_hash`（同值别名：canonical published payload 的 sha256）

排除示例：`editor_notes`、`selection_reason`、`rejection_reason`、`generated_at`、`_meta` 等。  
同内容仅字段顺序变化 → hash 不变。  
软审计：`audits/check_content_hash.py`。测试：`test_phase2_4_refactor.py` / `golden/content_hash_vectors.json`。

## 首页 / 归档

- `site/index.html` = 最新日报；每日 `site/YYYY-MM-DD.html`。  
- 归档三级 URL 见 11。  
- 正式渲染唯一数据源：`07_final_report.json`。
