def calculate_ip_risk(llm_result):
    score = 0

    if llm_result["ownership"] == "assigned":
        score += 50
    if llm_result["exclusivity"] == "exclusive":
        score += 30
    if llm_result["favor"] == "one-sided":
        score += 20

    if score >= 70:
        return "High", score
    if score >= 40:
        return "Medium", score
    return "Low", score
