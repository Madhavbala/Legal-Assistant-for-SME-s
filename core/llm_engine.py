import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
from utils.prompts import EN_PROMPT, HI_PROMPT

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def safe_json_parse(text):
    """
    Extract JSON object safely from LLM response
    """
    try:
        # Try direct parse
        return json.loads(text)
    except:
        # Try extracting JSON using regex
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass

    # Fallback (never crash app)
    return {
        "ownership": "unclear",
        "exclusivity": "unclear",
        "favor": "unclear",
        "risk_reason": "LLM response could not be parsed reliably.",
        "suggested_fix": "Manual legal review recommended."
    }


def analyze_clause_with_llm(clause, lang):
    prompt = HI_PROMPT if lang == "Hindi" else EN_PROMPT
    prompt = prompt.format(clause=clause)

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
