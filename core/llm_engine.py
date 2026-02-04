import streamlit as st
from groq import Groq, GroqError

MODEL_NAME = "llama3-8b-8192"

def get_groq_client():
    key = st.secrets.get("GROQ_API_KEY")
    if not key:
        return None
    return Groq(api_key=key)

def analyze_clause_with_llm(clause, lang):

    client = get_groq_client()
    if client is None:
        return fallback()

    prompt = f"""
Analyze the contract clause below.

Return EXACTLY in this format:

Ownership: Company | Vendor | Shared | Unclear
Exclusivity: Yes | No | Unclear
RiskReason: short explanation
SuggestedFix: SME friendly alternative

Clause:
{clause}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return parse(response.choices[0].message.content)

    except GroqError:
        return fallback()

def parse(text):

    result = {
        "ownership": "Unclear",
        "exclusivity": "Unclear",
        "risk_reason": "Not available",
        "suggested_fix": "Not available"
    }

    for line in text.splitlines():
        if line.startswith("Ownership:"):
            result["ownership"] = line.split(":", 1)[1].strip()
        elif line.startswith("Exclusivity:"):
            result["exclusivity"] = line.split(":", 1)[1].strip()
        elif line.startswith("RiskReason:"):
            result["risk_reason"] = line.split(":", 1)[1].strip()
        elif line.startswith("SuggestedFix:"):
            result["suggested_fix"] = line.split(":", 1)[1].strip()

    return result

def fallback():
    return {
        "ownership": "Unclear",
        "exclusivity": "Unclear",
        "risk_reason": "LLM unavailable",
        "suggested_fix": "Please review manually"
    }
