def is_ip_clause(clause: str) -> bool:
    keywords = ["intellectual property", "IP", "copyright", "patent", "trademark"]
    clause_lower = clause.lower()
    return any(k.lower() in clause_lower for k in keywords)

def infer_ip_meaning(clause: str):
    # Simplified rules for demo
    ownership = "Client" if "exclusive" in clause.lower() else "Shared"
    exclusivity = "Exclusive" if "exclusive" in clause.lower() else "Non-exclusive"
    return {"ownership": ownership, "exclusivity": exclusivity}
