import os
import json
import re
import streamlit as st
from groq import Groq
from utils.prompts import EN_PROMPT, HI_PROMPT


def get_groq_client():
    """
    Safely get Groq client using Streamlit secrets or env vars
    """
    api_key = None

    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY not found in Streamlit secrets")

    return Groq(api_key=api_key)


def analyze_clause_with_llm(clause: str, language: str):
    """
    Analyze IP clause using Groq LLM
    Returns clean dict (not raw JSON string)
    """

    if not clause.strip():
        return None

    prompt = EN_PROMPT if language == "English" else HI_PROMPT
    prompt = prompt.format(clause=clause)

    try:
        client = get_groq_client()

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        raw_text = response.choices[0].message.content.strip()

        # Extract JSON safely
        json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return {
                "RiskExplanation": raw_text,
                "SaferAlternative": "No structured suggestion returned."
            }

    except Exception as e:
        return {
            "RiskExplanation": f"Error in LLM analysis: {str(e)}",
            "SaferAlternative": "LLM analysis failed."
        }
