import json
from pathlib import Path

AUDIT_FILE = Path("data/audit_logs.json")
AUDIT_FILE.parent.mkdir(exist_ok=True)

def log_audit(results: list):
    if AUDIT_FILE.exists():
        try:
            data = json.loads(AUDIT_FILE.read_text())
        except:
            data = []
    else:
        data = []

    data.extend(results)
    AUDIT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))
