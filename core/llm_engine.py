import streamlit as st
from groq import Groq, GroqError

from core.ip_rules import infer_ip_meaning

MODEL_NAME = "llama3-8b-8192"


def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


# STEP 3: Prompt clarity function (THIS IS WHERE IT GOES)
def build_prompt(clause, lang):
    return f"""
You are a contract lawyer.

Analyze the intellectual property implications of the clause below.

Return EXACTLY in this format:

Ownership: Company | Vendor | Shared | Unclear
Exclusivity: Yes | No | Unclear
RiskReason: short explanation in simple English
SuggestedFix: SME friendly alternative clause

Clause:
{clause}
"""


def analyze_clause_with_llm(clause, lang):

    # Always run rule-based inference first
    rule_result = infer_ip_meaning(clause)

    client = get_groq_client()
    if client is None:
        return rule_result

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": build_prompt(clause, lang)}
            ],
            temperature=0
        )

        llm_text = response.choices[0].message.content
        llm_result = parse_llm_response(llm_text)

        # Merge rule-based results if LLM is weak or unclear
        for key in ["ownership", "exclusivity", "risk_reason", "suggested_fix"]:
            if llm_result.get(key) in ["Unclear", "", None]:
                llm_result[key] = rule_result[key]

        return llm_result

    except GroqError:
        return rule_result
    except Exception:
        return rule_result


def parse_llm_response(text):

    result = {
        "ownership": "Unclear",
        "exclusivity": "Unclear",
        "risk_reason": "",
        "suggested_fix": ""
    }

    for line in text.splitlines():
        line = line.strip()

        if line.startswith("Ownership:"):
            result["ownership"] = line.split(":", 1)[1].strip()

        elif line.startswith("Exclusivity:"):
            result["exclusivity"] = line.split(":", 1)[1].strip()

        elif line.startswith("RiskReason:"):
            result["risk_reason"] = line.split(":", 1)[1].strip()

        elif line.startswith("SuggestedFix:"):
            result["suggested_fix"] = line.split(":", 1)[1].strip()

    return result
