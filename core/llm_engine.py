def calculate_risk_score(analysis: dict) -> int:
    """
    Returns a risk score between 0 and 100
    """

    score = 0

    # Ownership
    if analysis.get("ownership", "").lower() in ["client", "assigned", "exclusive"]:
        score += 30

    # Exclusivity
    if analysis.get("exclusivity", "").lower() == "exclusive":
        score += 25

    # Favor
    if analysis.get("favor", "").lower() in ["one-sided", "client"]:
        score += 25

    # Explanation keywords
    explanation = analysis.get("risk_reason", "").lower()

    high_risk_words = [
        "overly broad",
        "no carve",
        "no license",
        "indefinite",
        "exclusive",
        "all rights",
        "without limitation",
        "forever"
    ]

    for word in high_risk_words:
        if word in explanation:
            score += 3

    # Cap score
    return min(score, 100)
