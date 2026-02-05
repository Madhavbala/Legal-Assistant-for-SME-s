# core/llm_engine.py

def analyze_clause_with_llm(clause_text: str, language: str = "en") -> dict:
    """
    Lightweight rule + placeholder LLM analysis.
    Returns a fixed schema to avoid KeyError.
    """

    risk = "Low"
    explanation = "No obvious legal risk detected."

    risky_keywords = [
        "indemnify",
        "liability",
        "termination",
        "penalty",
        "breach",
        "damages",
        "irrevocable",
        "exclusive"
    ]

    for word in risky_keywords:
        if word.lower() in clause_text.lower():
            risk = "High"
            explanation = f"The clause contains the risky term '{word}'."
            break

    return {
        "clause": clause_text,
        "risk_level": risk,
        "analysis": explanation
    }


def calculate_risk_score(results: list) -> int:
    """
    Simple numeric risk score (0–100)
    """

    if not results:
        return 0

    score = 0
    for r in results:
        if r["risk_level"] == "High":
            score += 20
        elif r["risk_level"] == "Medium":
            score += 10

    return min(score, 100)
