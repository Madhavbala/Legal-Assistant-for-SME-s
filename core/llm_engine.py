import streamlit as st
from groq import Groq
from core.ip_rules import infer_ip_meaning

def analyze_clause_with_llm(clause: str, lang: str) -> dict:
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY missing")

    client = Groq(api_key=api_key)

    prompt = f"""
Analyze the following clause and respond in JSON.

Clause:
{clause}

Instructions:
- Provide ownership (Client / Shared / Service Provider / Unclear)
- Provide exclusivity (Exclusive / Non-exclusive)
- Explain why it is risky
- Suggest a safer alternative
- Respond in English even if input is Hindi
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    content = response.choices[0].message.content

    rule_result = infer_ip_meaning(clause)

    return {
        "ownership": rule_result["ownership"],
        "exclusivity": rule_result["exclusivity"],
        "risk_reason": content,
        "suggested_fix": "Consider shared ownership or limited license rights."
    }
