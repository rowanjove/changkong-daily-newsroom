"""
Gates Module (给事中 · 资格五闸)
Implements the 5 eligibility gates:
1. Truth Gate
2. Freshness Gate
3. Dedup Gate
4. Evidence Sufficiency Gate
5. Risk / Eligibility Gate
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple

def evaluate_truth_gate(event: Dict[str, Any], policy: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons = []
    # 1. Source level check
    source_level = event.get("source_level", "B").upper()
    if source_level == "D":
        reasons.append("REJECT_D_LEVEL_SOURCE")
    
    # 2. Check vendor claims
    claims = event.get("verified_claims", [])
    has_vendor_only = False
    for c in claims:
        if c.get("claim_type") == "vendor_claim" or c.get("source_role") == "primary_actor":
            if not c.get("independent_verified", False):
                has_vendor_only = True
                c["status"] = "self_reported"
                c["tag"] = "VENDOR_CLAIM_ONLY"
    
    if event.get("is_pure_vendor_claim", False) and not event.get("corroborated", False):
        reasons.append("VENDOR_CLAIM_ONLY")

    # 3. Contradictions
    if event.get("unresolved_contradiction", False):
        reasons.append("CONFLICTING_SOURCES")

    passed = len(reasons) == 0
    return passed, reasons

def evaluate_freshness_gate(event: Dict[str, Any], policy: Dict[str, Any], reference_time: datetime) -> Tuple[bool, List[str]]:
    reasons = []
    desk = event.get("desk", "中国")
    freshness_cfg = policy.get("freshness", {})
    
    desk_hours_map = {
        "中国": freshness_cfg.get("china_policy_hours", 48),
        "国际": freshness_cfg.get("international_hours", 36),
        "财经": freshness_cfg.get("finance_hours", 36),
        "前沿科技": freshness_cfg.get("technology_hours", 48)
    }
    max_hours = desk_hours_map.get(desk, 48)

    event_time_str = event.get("event_time")
    if not event_time_str:
        return False, ["MISSING_EVENT_TIME"]
    
    try:
        if "T" in event_time_str:
            event_dt = datetime.fromisoformat(event_time_str.replace("Z", "+00:00"))
            # remove tz for naive comparison
            event_dt = event_dt.replace(tzinfo=None)
        else:
            event_dt = datetime.strptime(event_time_str, "%Y-%m-%d")
    except Exception:
        return False, ["INVALID_EVENT_TIME_FORMAT"]

    age = reference_time - event_dt
    if age > timedelta(hours=max_hours):
        # Is there a material update?
        if not event.get("has_material_update", False):
            reasons.append("REJECT_OLD_NEWS")

    passed = len(reasons) == 0
    return passed, reasons

def evaluate_dedup_gate(event: Dict[str, Any], seen_event_ids: set) -> Tuple[bool, List[str]]:
    reasons = []
    event_id = event.get("event_id")
    if not event_id:
        return False, ["MISSING_EVENT_ID"]
    
    if event_id in seen_event_ids:
        if not event.get("is_follow_up", False):
            reasons.append("REJECT_DUPLICATE_EVENT")
    
    passed = len(reasons) == 0
    return passed, reasons

def evaluate_evidence_gate(event: Dict[str, Any], policy: Dict[str, Any]) -> Tuple[bool, int, str, List[str]]:
    reasons = []
    ev_cfg = policy.get("evidence", {})
    threshold = ev_cfg.get("publish_threshold", 60)
    
    # Calculate evidence score based on critical claims
    claims = event.get("verified_claims", [])
    critical_ids = event.get("publication_critical_claim_ids", [])
    
    scores = []
    for c in claims:
        # If critical_ids specified, only aggregate critical ones
        if critical_ids and c.get("claim_id") not in critical_ids:
            continue
        score = c.get("confidence", 70)
        # Penalties for single unverified source or vendor claim
        if c.get("tag") == "VENDOR_CLAIM_ONLY":
            score = min(score, 55)
        scores.append(score)
    
    if not scores:
        overall_evidence = event.get("evidence_confidence", 50)
    else:
        overall_evidence = min(scores)

    # Determine confidence label
    if overall_evidence >= 85:
        confidence_label = "已确认"
    elif overall_evidence >= 65:
        confidence_label = "基本确认"
    elif overall_evidence >= 50:
        confidence_label = "单源"
    else:
        confidence_label = "待确认"
    
    passed = overall_evidence >= threshold
    if not passed:
        reasons.append("INSUFFICIENT_EVIDENCE")

    return passed, overall_evidence, confidence_label, reasons

def evaluate_risk_gate(event: Dict[str, Any], policy: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons = []
    if event.get("signal_only", False):
        reasons.append("REJECT_SIGNAL_ONLY")
    
    risk_flags = event.get("risk_flags", [])
    if "LEGAL_RISK_BLOCK" in risk_flags or "SEVERE_MISINFORMATION" in risk_flags:
        reasons.append("HIGH_RISK_BLOCK")

    passed = len(reasons) == 0
    return passed, reasons

def verify_candidate(event: Dict[str, Any], policy: Dict[str, Any], seen_ids: set, reference_time: datetime) -> Dict[str, Any]:
    """
    Runs an inbox candidate through the 5 gates.
    """
    g_truth, r_truth = evaluate_truth_gate(event, policy)
    g_fresh, r_fresh = evaluate_freshness_gate(event, policy, reference_time)
    g_dedup, r_dedup = evaluate_dedup_gate(event, seen_ids)
    g_ev, ev_score, conf_label, r_ev = evaluate_evidence_gate(event, policy)
    g_risk, r_risk = evaluate_risk_gate(event, policy)

    passed_all_gates = g_truth and g_fresh and g_dedup and g_ev and g_risk
    all_reasons = r_truth + r_fresh + r_dedup + r_ev + r_risk

    importance = event.get("news_importance", 50)
    
    # Determine verified status
    if passed_all_gates:
        status = "VERIFIED"
    elif g_truth and g_fresh and g_dedup and g_risk and (not g_ev) and importance >= 65:
        # High importance + lower evidence => WATCHLIST
        status = "WATCHLIST"
    else:
        status = "REJECTED"

    return {
        "event_id": event.get("event_id"),
        "raw_event": event,
        "status": status,
        "evidence_confidence": ev_score,
        "confidence_label": conf_label,
        "news_importance": importance,
        "passed_gates": {
            "truth": g_truth,
            "freshness": g_fresh,
            "dedup": g_dedup,
            "evidence": g_ev,
            "risk": g_risk
        },
        "rejection_reasons": all_reasons
    }
