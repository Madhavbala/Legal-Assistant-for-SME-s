def calculate_ip_risk(llm_result):

    score = 0

    ownership = llm_result.get("ownership", "Unclear")
    exclusivity = llm_result.get("exclusivity", "Unclear")

    if ownership == "Unclear":
        score += 30

    if ownership == "Company":
        score += 40

    if exclusivity == "Yes":
        score += 30

    if score >= 70:
        risk = "High"
    elif score >= 40:
        risk = "Medium"
    else:
        risk = "Low"

    return risk, score
