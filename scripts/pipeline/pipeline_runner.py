"""
Pipeline Runner
Coordinates:
中书令 inbox -> 给事中 gates -> 丞相 editorial -> 07_final_report.json
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from .policy_loader import load_policy
from .gates import verify_candidate
from .editorial import finalize_edition

def run_pipeline(inbox_path: Path, output_dir: Path, reference_time: datetime = None) -> Dict[str, Any]:
    if reference_time is None:
        reference_time = datetime(2026, 8, 29, 8, 0, 0)
    
    iso_date = reference_time.strftime("%Y-%m-%d")
    weekday_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    date_str = f"{reference_time.year}年{reference_time.month}月{reference_time.day}日　{weekday_names[reference_time.weekday()]}"

    policy = load_policy()

    # 1. Read inbox
    with open(inbox_path, "r", encoding="utf-8") as f:
        inbox_data = json.load(f)
    
    candidates = inbox_data if isinstance(inbox_data, list) else inbox_data.get("candidates", [])

    # 2. 给事中: Run gates
    verified_results = []
    seen_ids = set()
    for item in candidates:
        res = verify_candidate(item, policy, seen_ids, reference_time)
        verified_results.append(res)
        if item.get("event_id"):
            seen_ids.add(item["event_id"])

    # 3. 丞相: Finalize
    forecast_summary = inbox_data.get("forecast_summary", "今日聚焦重要政策调整、全球地缘动态与前沿开源大模型突破。")
    final_report = finalize_edition(
        verified_results=verified_results,
        policy=policy,
        iso_date=iso_date,
        date_str=date_str,
        forecast_summary=forecast_summary
    )

    # 4. Save 07_final_report.json
    output_dir.mkdir(parents=True, exist_ok=True)
    report_file = output_dir / f"final_report_{iso_date}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(final_report, f, ensure_ascii=False, indent=2)

    return {
        "final_report": final_report,
        "verified_results": verified_results,
        "report_file": report_file
    }
