import streamlit as st
from groq import Groq
from core.ip_rules import infer_ip_meaning

MODEL_NAME = "openai/gpt-oss-120b"  

def analyze_clause_with_llm(clause: str, lang: str) -> dict:
    clause = clause.strip()
    if not clause or len(clause) < 5:
        return {
            "ownership": "Unknown",
            "exclusivity": "Unknown",
            "risk_reason": "Clause too short to analyze",
            "suggested_fix": "No action required"
        }

    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY missing")

    client = Groq(api_key=api_key)

    prompt = f"""
Analyze the following contract clause. Respond in JSON. Respond in English even if input is Hindi.

Clause:
{clause}

Instructions:
- Ownership (Client / Shared / Service Provider / Unclear)
- Exclusivity (Exclusive / Non-exclusive)
- Explain why risky
- Suggest safer alternative
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        content = response.choices[0].message.content
    except Exception as e:
        content = f"Error in LLM analysis: {str(e)}"

    rule_result = infer_ip_meaning(clause)

    return {
        "ownership": rule_result["ownership"],
        "exclusivity": rule_result["exclusivity"],
        "risk_reason": content,
        "suggested_fix": "Consider shared ownership or limited license rights."
    }
