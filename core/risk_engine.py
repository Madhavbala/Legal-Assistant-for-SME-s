def calculate_ip_risk(llm_result: dict):
    # Example scoring
    score = 40  # Dummy for demo
    risk = "Medium" if score < 70 else "High"
    return risk, score
