def calculate_ip_risk(llm_result: dict) -> tuple:
    score = 0
    risk = "Low"

    reason = llm_result.get("risk_reason", "").lower()
    if "exclusive" in llm_result.get("exclusivity","").lower():
        score += 40
    if "client" not in llm_result.get("ownership","").lower():
        score += 30
    if "high" in reason or "restrict" in reason:
        score += 30

    if score >= 70:
        risk = "High"
    elif score >= 40:
        risk = "Medium"

    return risk, score
