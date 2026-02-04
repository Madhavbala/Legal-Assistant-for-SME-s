# core/ip_rules.py

def infer_ip_meaning(clause: str) -> dict:
    """
    Analyze clause and return ownership and exclusivity info.
    Always returns a dictionary with keys: ownership, exclusivity
    """
    clause_lower = clause.lower()
    
    ownership = "Unknown"
    exclusivity = "Unknown"
    
    if "client" in clause_lower:
        ownership = "Client"
    elif "provider" in clause_lower or "service provider" in clause_lower:
        ownership = "Service Provider"

    if "exclusive" in clause_lower:
        exclusivity = "Exclusive"
    elif "non-exclusive" in clause_lower:
        exclusivity = "Non-Exclusive"

    return {
        "ownership": ownership,
        "exclusivity": exclusivity,
        "risk_reason": "",
        "suggested_fix": ""
    }
