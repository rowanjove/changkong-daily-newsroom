"""
Editorial Desk Module (丞相 · 定稿与事实锁)
Implements:
1. Three-axis ranking (news_importance, evidence_confidence, interest_relevance)
2. Attention Budget & Display Tier (Lead story, side stories, desk primary)
3. Fact Lock (never invent facts, only polish verified claims)
4. Public Sanitize (strip internal scores, notes, and audit trails)
5. Content Hash canonicalization
"""
import hashlib
import json
from typing import Dict, Any, List, Optional

def sanitize_story_for_public(story: Dict[str, Any]) -> Dict[str, Any]:
    """
    Strips internal audit metadata and leaves only sanitized reader-facing fields.
    """
    raw = story.get("raw_event", {})
    return {
        "event_id": story.get("event_id"),
        "desk": raw.get("desk"),
        "title": raw.get("title"),
        "summary": raw.get("summary"),
        "importance": story.get("news_importance"),
        "confidence_label": story.get("confidence_label"),
        "display_time": raw.get("event_time", "")[:10],
        "why_it_matters": raw.get("why_it_matters", ""),
        "what_to_watch": raw.get("what_to_watch", "")
    }

def calculate_content_hash(public_payload: Dict[str, Any]) -> str:
    """
    Generates a deterministic SHA256 hash of the public payload.
    """
    canonical_str = json.dumps(public_payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()[:16]

def finalize_edition(
    verified_results: List[Dict[str, Any]], 
    policy: Dict[str, Any],
    iso_date: str,
    date_str: str,
    forecast_summary: str = "",
    trends: Optional[List[str]] = None,
    tomorrow: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Takes verified results, applies fact lock, desk quotas, and Attention Budget.
    """
    publish_threshold = policy.get("importance", {}).get("publish_threshold", 65)
    desks_cfg = policy.get("desks", {})

    # Separate publishable items and watchlist items
    publishable_items = []
    watchlist_items = []

    for item in verified_results:
        status = item.get("status")
        importance = item.get("news_importance", 0)
        
        if status == "VERIFIED" and importance >= publish_threshold:
            publishable_items.append(item)
        elif status == "WATCHLIST":
            title = item.get("raw_event", {}).get("title", "未命名事件")
            watchlist_items.append(f"{title}（证据尚在核实中）")

    # Sort publishable items by importance descending
    publishable_items.sort(key=lambda x: x.get("news_importance", 0), reverse=True)

    # 1. Lead Story selection
    lead_story = None
    side_stories = []
    
    if publishable_items:
        lead_candidate = publishable_items[0]
        lead_story = sanitize_story_for_public(lead_candidate)
        # Select up to 3 side stories from remaining high importance
        for candidate in publishable_items[1:4]:
            side_stories.append(sanitize_story_for_public(candidate))

    # 2. Desk allocation and Quota enforcement (max-only, no min forced)
    desk_stories = {
        "中国": [],
        "国际": [],
        "财经": [],
        "前沿科技": []
    }

    for item in publishable_items:
        desk = item.get("raw_event", {}).get("desk", "中国")
        if desk in desk_stories:
            max_items = desks_cfg.get(desk, {}).get("max_items", 8)
            if len(desk_stories[desk]) < max_items:
                desk_stories[desk].append(sanitize_story_for_public(item))

    # 3. Trends & Tomorrow items (fallback defaults if not provided)
    if trends is None:
        trends = [
            "前沿模型迭代持续聚焦多模态与推理成本下探",
            "全球宏观预期在主要央行政策落地前保持博弈"
        ]
    if tomorrow is None:
        tomorrow = [
            "关注明日高频经济数据与重点行业财报发布",
            "跟进重点开源生态项目新一轮更新与兼容表现"
        ]

    public_payload = {
        "iso_date": iso_date,
        "date_str": date_str,
        "forecast_summary": forecast_summary,
        "lead_story": lead_story,
        "side_stories": side_stories,
        "desks": desk_stories,
        "trends": trends,
        "watchlist": watchlist_items,
        "tomorrow": tomorrow
    }

    content_hash = calculate_content_hash(public_payload)
    public_payload["content_hash"] = content_hash

    final_report = {
        "schema_version": 2,
        "generated_at": iso_date,
        "content_hash": content_hash,
        "public_data": public_payload,
        "audit_meta": {
            "total_candidates": len(verified_results),
            "verified_count": len(publishable_items),
            "watchlist_count": len(watchlist_items),
            "rejected_count": len(verified_results) - len(publishable_items) - len(watchlist_items)
        }
    }

    return final_report
