import json
import os
from datetime import datetime

AUDIT_FILE = "data/audit_logs.json"

def log_audit(record):
    """
    record = {
        "clause": str,
        "analysis": dict,
        "risk": str,
        "score": int
    }
    """

    os.makedirs("data", exist_ok=True)

    audit_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "clause": record.get("clause", ""),
        "ownership": record.get("analysis", {}).get("ownership", ""),
        "exclusivity": record.get("analysis", {}).get("exclusivity", ""),
        "risk": record.get("risk", ""),
        "score": record.get("score", ""),
        "risk_reason": record.get("analysis", {}).get("risk_reason", ""),
        "suggested_fix": record.get("analysis", {}).get("suggested_fix", "")
    }

    if os.path.exists(AUDIT_FILE):
        with open(AUDIT_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(audit_entry)

    with open(AUDIT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
