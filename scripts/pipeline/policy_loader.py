"""
Policy Loader for Changkong Daily Newsroom.
Loads and validates policy configuration from config/policy.yaml.
"""
from pathlib import Path
import yaml

DEFAULT_POLICY_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "policy.yaml"

def load_policy(policy_path=None):
    path = Path(policy_path) if policy_path else DEFAULT_POLICY_PATH
    if not path.exists():
        # Fallback to example
        example_path = path.parent / "policy.example.yaml"
        if example_path.exists():
            path = example_path
        else:
            raise FileNotFoundError(f"Policy file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        policy = yaml.safe_load(f)
    return policy

if __name__ == "__main__":
    p = load_policy()
    print(f"Loaded policy for: {p.get('timezone', 'unknown tz')}, version={p.get('pipeline_version')}")
