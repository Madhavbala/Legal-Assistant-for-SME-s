import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
from utils.prompts import EN_PROMPT, HI_PROMPT  # <- important

# Load .env for GROQ API key
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def safe_json_parse(text):
    """
    Safely parse JSON returned by LLM.
    If parsing fails, return default structure to avoid crashing.
    """
    try:
        return json.loads(text)
    except:
        # Try extracting JSON using regex
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass

    # Fallback
    return {
        "ownership": "unclear",
        "exclusivity": "unclear",
        "favor": "unclear",
        "risk_reason": "LLM response could not be parsed reliably.",
        "suggested_fix": "Manual legal review recommended."
    }

def analyze_clause_with_llm(clause, lang):
    """
    Analyze a single clause using Groq LLM.
    lang: "English" or "Hindi"
    Returns a dictionary with ownership, exclusivity, favor, risk_reason, suggested_fix
    """
    # Choose prompt based on language
    prompt = HI_PROMPT if lang == "Hindi" else EN_PROMPT
    prompt = prompt.format(clause=clause)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a legal assistant. Respond ONLY with valid JSON. No explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        raw_text = response.choices[0].message.content.strip()
        return safe_json_parse(raw_text)

    except Exception as e:
        # Return safe fallback if API fails
        return {
            "ownership": "unclear",
            "exclusivity": "unclear",
            "favor": "unclear",
            "risk_reason": f"LLM error: {str(e)}",
            "suggested_fix": "Manual legal review recommended."
        }
