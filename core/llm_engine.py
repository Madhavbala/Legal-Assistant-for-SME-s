from core.ip_rules import infer_ip_meaning

def analyze_clause_with_llm(clause, lang):
    """
    Simulated LLM analysis
    Combines simple deterministic rules + explanation
    """
    rule_result = infer_ip_meaning(clause)

    # Add more detailed explanation for user
    risk_reason = (
        f"{rule_result['risk_reason']} "
        "Please review the clause carefully and adjust ownership/exclusivity terms."
    )
    suggested_fix = rule_result['suggested_fix']

    return {
        "risk_reason": risk_reason,
        "suggested_fix": suggested_fix
    }
