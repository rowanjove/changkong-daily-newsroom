#!/usr/bin/env python3
"""
Changkong Daily Newsroom · 一键运行演示 (One-Click Demo Runner)
Runs the entire multi-agent newsroom pipeline:
中书令采编 -> 给事中五资格闸 -> 丞相定稿与事实锁 -> 尚书令静态刊印 -> 发布门禁审计
"""
import sys
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.pipeline.pipeline_runner import run_pipeline
from scripts.build_site import build_site
from audits.check_publish_gates import audit_report
from scripts.pipeline.policy_loader import load_policy

def main():
    print("=" * 65)
    print("   长空日报 / Newsroom 日报系统 · 内阁流水线演示 (Demo Runner)")
    print("=" * 65)
    print(" 机制：四人制内阁 | 五资格闸 | 三轴评分 | 事实锁 | 静态刊印")
    print("-" * 65)

    inbox_file = REPO_ROOT / "fixtures" / "mock_inbox.json"
    dist_dir = REPO_ROOT / "dist"
    ref_time = datetime(2026, 8, 29, 8, 0, 0)

    # 1. Pipeline Run
    print("\n[Step 1] 中书令提供候选池，给事中执行【资格五闸】核验...")
    pipeline_result = run_pipeline(inbox_path=inbox_file, output_dir=dist_dir, reference_time=ref_time)
    
    verified_results = pipeline_result["verified_results"]
    for r in verified_results:
        eid = r["event_id"]
        status = r["status"]
        imp = r["news_importance"]
        ev = r["evidence_confidence"]
        reasons = r["rejection_reasons"]
        
        status_symbol = {
            "VERIFIED": "  [通过]",
            "WATCHLIST": "  [观察/待确认]",
            "REJECTED": " [淘汰]"
        }.get(status, status)

        reason_str = f" 原因: {', '.join(reasons)}" if reasons else ""
        print(f"  {status_symbol} {eid} (重要度:{imp}, 证据分:{ev}){reason_str}")

    # 2. Editorial Desk
    final_report = pipeline_result["final_report"]
    public_data = final_report["public_data"]
    lead = public_data.get("lead_story", {})
    watchlist = public_data.get("watchlist", [])

    print("\n[Step 2] 丞相定稿与【事实锁】编排...")
    print(f"  ★ 今日全站头条 (Lead Story): {lead.get('title')}")
    print(f"  ★ 今日侧栏要闻: {len(public_data.get('side_stories', []))} 条")
    print(f"  ★ 提前关注 (Watchlist / 证据待核实): {len(watchlist)} 条")
    for w in watchlist:
        print(f"     - {w}")
    print(f"  ★ Content Hash (幂等标识): {final_report.get('content_hash')}")

    # 3. Build Site
    print("\n[Step 3] 尚书令基于典雅报纸模板执行【静态刊印】...")
    iso_date = public_data.get("iso_date")
    out_html = dist_dir / f"{iso_date}.html"
    index_html = dist_dir / "index.html"
    build_site(final_report, out_html)
    build_site(final_report, index_html)
    print(f"  -> 生成归档页面: {out_html.relative_to(REPO_ROOT)}")
    print(f"  -> 更新默认首页: {index_html.relative_to(REPO_ROOT)}")

    # 4. Audit
    print("\n[Step 4] 尚书令执行上线前【发布门禁审计 (Publish Gates)】...")
    policy = load_policy()
    passed = audit_report(final_report, policy)

    print("\n" + "=" * 65)
    if passed:
        print("  内阁早报刊印成功！所有门禁全部通过！")
        print(f"  本地预览文件: {index_html.resolve()}")
    else:
        print("  发布门禁拦截，禁止部署上线！")
        sys.exit(1)
    print("=" * 65)

if __name__ == "__main__":
    main()
