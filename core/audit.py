import json
import os

AUDIT_FILE = os.path.join("data", "audit_logs.json")
os.makedirs("data", exist_ok=True)
if not os.path.exists(AUDIT_FILE):
    with open(AUDIT_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

def log_audit(result: dict):
    with open(AUDIT_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data.append(result)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()
