"""
Publish Gates Audit Module (尚书令 · 刊印前门禁检查)
Audits:
1. Desk quotas (max items per desk)
2. Public leakage (no internal fields or scores leaked)
3. Content hash integrity
"""
import sys
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
from scripts.pipeline.policy_loader import load_policy

FORBIDDEN_LEAKAGE_PATTERNS = [
    r"selection_reason",
    r"verified_score",
    r"signal_only",
    r"agent_note",
    r"REJECT_",
    r"HIGH_RISK",
    r"TODO_VERIFY"
]

def audit_report(report_data: dict, policy: dict) -> bool:
    errors = []
    public_data = report_data.get("public_data", {})
    desks = public_data.get("desks", {})
    desks_cfg = policy.get("desks", {})

    # 1. Quota check
    for desk_name, stories in desks.items():
        limit = desks_cfg.get(desk_name, {}).get("max_items", 8)
        if len(stories) > limit:
            errors.append(f"Quota exceeded for desk '{desk_name}': {len(stories)} > {limit}")

    # 2. Content Hash check
    chash = public_data.get("content_hash")
    if not chash or len(chash) < 8:
        errors.append("Invalid or missing content_hash in public_data")

    # 3. Leakage check in serialized public JSON
    public_json_str = json.dumps(public_data, ensure_ascii=False)
    for pattern in FORBIDDEN_LEAKAGE_PATTERNS:
        if re.search(pattern, public_json_str, re.IGNORECASE):
            errors.append(f"Internal leak detected matching pattern: '{pattern}'")

    if errors:
        print(" [AUDIT FAILED] Publish gates blocked:")
        for err in errors:
            print(f"   - {err}")
        return False
    
    print(" [AUDIT PASSED] All publish gates passed successfully.")
    return True

def main():
    candidate_files = list((REPO_ROOT / "dist").glob("final_report_*.json"))
    if not candidate_files:
        print("No report found in dist/. Please run pipeline first.")
        sys.exit(1)
    
    report_file = candidate_files[-1]
    with open(report_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    policy = load_policy()
    passed = audit_report(data, policy)
    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
