def analyze_clause_with_llm(clause, lang):
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
        # Safe fallback if API fails
        return {
            "ownership": "unclear",
            "exclusivity": "unclear",
            "favor": "unclear",
            "risk_reason": f"LLM error: {str(e)}",
            "suggested_fix": "Manual legal review recommended."
        }
