# core/ip_rules.py

def is_ip_clause(clause: str) -> bool:
    clause_lower = clause.lower()
    keywords = [
        "intellectual property", "ownership", "exclusive", "assign",
        "no rights to reuse", "no rights to modify", "license",
        "patent", "copyright"
    ]
    return any(k in clause_lower for k in keywords)

# If llm_engine.py calls infer_ip_meaning, define it like this:
def infer_ip_meaning(clause: str) -> str:
    """
    Dummy placeholder: returns a short description of IP meaning in clause.
    You can enhance with actual NLP/LLM later.
    """
    if "intellectual property" in clause.lower():
        return "This clause involves intellectual property ownership."
    return "No IP meaning detected."
