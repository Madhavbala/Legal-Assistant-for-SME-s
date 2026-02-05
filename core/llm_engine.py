# core/llm_engine.py

import json

# ----------------------------
# Clause Analysis (LLM-safe)
# ----------------------------
def analyze_clause_with_llm(clause_text, language="English"):
    """
    Returns a structured dict (never raw JSON string)
    """

    # 🔹 Replace this with Groq call later
    # For now, deterministic + safe structure

    result = {
        "clause": clause_text,
        "ownership": "assigned",
        "exclusivity": "exclusive",
        "favor": "one-sided",
        "risk_reason": (
            "The clause transfers ownership and rights primarily to one party "
            "without clearly defining limitations or protections."
        ),
        "suggested_fix": (
            "Add explicit limitations, retained rights, or indemnification clauses "
            "to balance obligations between both parties."
        ),
        "risk_level": "High"
    }

    return result


# ----------------------------
# Overall Risk Score
# ----------------------------
def calculate_risk_score(results):
    """
    Converts clause risk levels into a 0–100 score
    """

    score_map = {
        "Low": 20,
        "Medium": 50,
        "High": 80
    }

    if not results:
        return 0

    total = 0
    for r in results:
        total += score_map.get(r.get("risk_level", "Medium"), 50)

    return round(total / len(results))
