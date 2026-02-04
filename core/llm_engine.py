import streamlit as st
from groq import Groq

MODEL_NAME = "llama3-70b-8192"

def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def analyze_clause_with_llm(clause, lang):

    client = get_groq_client()

    if client is None:
        return {
            "ownership": "Unknown",
            "exclusivity": "Unknown",
            "risk_reason": "LLM unavailable. Groq API key not configured.",
            "suggested_fix": "Configure GROQ_API_KEY in Streamlit secrets."
        }

    prompt = f"""
    Analyze the following contract clause.

    Language: {lang}

    Clause:
    {clause}

    Respond strictly in this format:
    Ownership: <Company / Vendor / Shared / Unclear>
    Exclusivity: <Yes / No / Unclear>
    RiskReason: <Short explanation>
    SuggestedFix: <SME friendly alternative>
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    text = response.choices[0].message.content

    return parse_llm_response(text)

def parse_llm_response(text):

    result = {
        "ownership": "Unclear",
        "exclusivity": "Unclear",
        "risk_reason": "",
        "suggested_fix": ""
    }

    for line in text.splitlines():
        line = line.strip()

        if line.lower().startswith("ownership"):
            result["ownership"] = line.split(":", 1)[1].strip()

        elif line.lower().startswith("exclusivity"):
            result["exclusivity"] = line.split(":", 1)[1].strip()

        elif line.lower().startswith("riskreason"):
            result["risk_reason"] = line.split(":", 1)[1].strip()

        elif line.lower().startswith("suggestedfix"):
            result["suggested_fix"] = line.split(":", 1)[1].strip()

    return result
