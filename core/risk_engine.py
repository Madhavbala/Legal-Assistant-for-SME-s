def calculate_ip_risk(analysis: dict):
    """
    Calculate risk level based on clause analysis.
    Returns tuple: (RiskLevel, Score 0-100)
    """
    # Simple scoring logic based on keywords
    score = 0
    clause_text = analysis.get("risk_reason", "").lower()

    if "overly broad" in clause_text or "no definition" in clause_text:
        score += 20
    if "no carve-out" in clause_text:
        score += 10
    if "no license back" in clause_text:
        score += 10
    if "moral rights" in clause_text or "unenforceable" in clause_text:
        score += 10

    # Determine risk level
    if score >= 40:
        risk = "Medium"
    elif score >= 20:
        risk = "Low"
    else:
        risk = "High"

    # Cap score at 100
    score = min(score, 100)
    return risk, score
