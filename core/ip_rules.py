# core/ip_rules.py

def is_ip_clause(clause: str) -> bool:
    clause_lower = clause.lower()
    keywords = [
        "intellectual property", "ownership", "exclusive", "assign",
        "no rights to reuse", "no rights to modify", "license",
        "patent", "copyright"
    ]
    return any(k in clause_lower for k in keywords)
