IP_KEYWORDS = [
    "intellectual property", "IP", "ownership", "patent", "copyright",
    "trademark", "license", "exclusivity", "use of software", "developed together"
]

def is_ip_clause(clause: str) -> bool:
    clause_lower = clause.lower()
    for kw in IP_KEYWORDS:
        if kw.lower() in clause_lower:
            return True
    return False
